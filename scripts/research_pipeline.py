#!/usr/bin/env python3
"""Six-stage local research handoff runner. Standard library, no network or installs."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
WINE = ROOT / 'examples/real-wine'
STAGES = ('question', 'evidence', 'protocol', 'experiment', 'analysis', 'report')
FILES = dict(zip(STAGES, ('question.json', 'evidence.json', 'protocol.json',
                         'experiment.json', 'analysis.json', 'REPORT.md')))
TIMEOUT = 120
MAX_ATTEMPTS = 3
SCHEMA = 1


class Blocked(ValueError):
    """A real input is still missing; this is not completion."""


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def object_read(path):
    value = read(path)
    if not isinstance(value, dict):
        raise ValueError('Expected a JSON object: ' + path.name)
    return value


def configuration_digest(state):
    value = {'mode': state['mode'], 'limits': state['limits']}
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode('utf-8')).hexdigest()


def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def save_state(run, state):
    target = safe(run, 'state.json', exists=False)
    temp = safe(run, 'state.json.tmp', exists=False)
    write(temp, state)
    os.replace(temp, target)


def safe(base, name, exists=True):
    if not isinstance(name, str) or not name or '\\' in name or ':' in name:
        raise ValueError('Unsafe relative path: ' + str(name))
    parts = PurePosixPath(name)
    if parts.is_absolute() or '..' in parts.parts or name in ('.', ''):
        raise ValueError('Unsafe relative path: ' + name)
    path = base.joinpath(*parts.parts)
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('Symbolic links are not accepted: ' + name)
    if not path.resolve().is_relative_to(base.resolve()):
        raise ValueError('Path leaves run: ' + name)
    if exists and not path.is_file():
        raise Blocked('Missing file: ' + name)
    return path


def external(path, new=False):
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('Run path cannot contain symbolic links')
    path = path.resolve()
    if path.is_relative_to(ROOT):
        raise ValueError('Choose an output directory outside the repository')
    if new and path.exists():
        raise ValueError('Output exists; choose a NEW directory')
    if not new and not path.is_dir():
        raise ValueError('Run directory does not exist')
    return path


def text_field(obj, key):
    if not isinstance(obj, dict):
        raise ValueError('Expected an object containing field: ' + key)
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip() or value.strip().upper() in ('TODO', 'TBD', 'UNKNOWN'):
        raise Blocked('Fill nonempty field: ' + key)
    return value


def list_field(obj, key, nonempty=True):
    if not isinstance(obj, dict):
        raise ValueError('Expected an object containing field: ' + key)
    value = obj.get(key)
    if not isinstance(value, list) or (nonempty and not value):
        raise Blocked('Fill list field: ' + key)
    return value


def strings(obj, key):
    values = list_field(obj, key)
    if any(not isinstance(x, str) or not x.strip() for x in values):
        raise ValueError('Expected nonempty strings: ' + key)
    return values


def unique_ids(items):
    ids = [text_field(x, 'id') for x in items]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate IDs')
    return set(ids)


def fingerprints(mode):
    names = ['scripts/research_pipeline.py']
    routing = safe(ROOT, 'workflows/automated-research/skill-routing.json')
    names.append(routing.relative_to(ROOT).as_posix())
    for stage in object_read(routing)['stages']:
        for skill in [stage['primary'], *stage.get('supplemental', [])]:
            if digest(safe(ROOT, skill['path'])) != skill['sha256']:
                raise ValueError('Skill fingerprint mismatch: ' + skill['path'])
            names.append(skill['path'])
    if mode == 'wine':
        names += ['examples/real-wine/' + n for n in (
            'run_case.py', 'verify_case.py', 'protocol.json', 'sources.json',
            'DATA_SOURCE.json', 'data/wine.data', 'data/wine.names')]
    return {n: digest(safe(ROOT, n)) for n in names}


def event(run, state, stage, status, detail):
    entry = {'at': now(), 'stage': stage, 'status': status, 'detail': detail}
    with safe(run, 'events.jsonl', exists=False).open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(entry, ensure_ascii=False) + '\n')
    state['updated_at'] = entry['at']


@contextmanager
def locked(run):
    path = safe(run, '.pipeline.lock', exists=False)
    try:
        with path.open('x', encoding='utf-8') as stream:
            stream.write(json.dumps({'pid': os.getpid(), 'at': now()}))
    except FileExistsError:
        raise ValueError('Run locked. If an earlier process died, confirm it ended before removing .pipeline.lock.')
    try:
        yield
    finally:
        path.unlink()


def load_state(run):
    state = object_read(safe(run, 'state.json'))
    if state.get('schema_version') != SCHEMA or state.get('mode') not in ('wine', 'custom'):
        raise ValueError('Not a supported pipeline run')
    stages = list_field(state, 'stages')
    if any(not isinstance(s, dict) for s in stages) or [s.get('id') for s in stages] != list(STAGES):
        raise ValueError('Invalid stage order')
    return state


def integrity(run, state):
    if configuration_digest(state) != state.get('configuration_sha256'):
        raise ValueError('Run configuration changed. Create a new run with the intended budgets.')
    current = fingerprints(state['mode'])
    if current != state['repository_inputs']:
        raise ValueError('Repository inputs or runner changed. Preserve this run and create a new run.')
    pending_seen = False
    for stage in state['stages']:
        if stage['status'] != 'accepted':
            pending_seen = True
            continue
        if pending_seen:
            raise ValueError('Accepted stage follows an incomplete stage')
        for name, expected in {**stage['inputs'], **stage['outputs']}.items():
            if digest(safe(run, name)) != expected:
                raise ValueError('Accepted input/output changed: ' + name + '. Start a new run.')


def refs(run, items, *, sources=None):
    unique_ids(items) if sources is None else None
    names = []
    for item in items:
        name = text_field(item, 'path')
        if name in ('state.json', 'state.json.tmp', 'events.jsonl', 'NEXT.md', '.pipeline.lock'):
            raise ValueError('Artifact refers to runner control file')
        if digest(safe(run, name)) != text_field(item, 'sha256'):
            raise ValueError('Artifact SHA-256 mismatch: ' + name)
        if sources is not None:
            if text_field(item, 'source_id') not in sources:
                raise ValueError('Unknown or unread data source')
            text_field(item, 'license')
        names.append(name)
    if len(names) != len(set(names)):
        raise ValueError('Duplicate artifact paths')
    return names


def source_ids(run):
    return {x['id'] for x in read(safe(run, 'evidence.json'))['sources'] if x['status'] == 'read'}


def validate_claims(claims, sources, artifacts):
    unique_ids(claims)
    if not claims:
        raise Blocked('At least one bounded claim is required')
    for claim in claims:
        text_field(claim, 'text'); text_field(claim, 'locator')
        sids = list_field(claim, 'source_ids', False)
        aids = list_field(claim, 'artifact_ids', False)
        if not sids and not aids:
            raise ValueError('Claim needs a source or measured artifact')
        if not set(sids) <= sources or not set(aids) <= artifacts:
            raise ValueError('Unknown source/artifact in claim')


def validate_stage(run, stage, mode, limits=None):
    """Custom checks are structural/provenance checks, never scientific endorsement."""
    names = [FILES[stage]]
    path = safe(run, names[0])
    limits = limits or {'host_max_searches': 4, 'host_max_sources': 8}
    obj = object_read(path) if stage != 'report' else None
    if stage == 'question':
        for key in ('question', 'scope', 'resources', 'stopping_condition'):
            text_field(obj, key)
    elif stage == 'evidence':
        if obj.get('mode') not in ('new', 'reused'):
            raise ValueError('Evidence mode must distinguish new from reused')
        logs = list_field(obj, 'search_log', False)
        if len(logs) > limits['host_max_searches']:
            raise ValueError('Recorded search count exceeds this run budget; create a separately scoped run')
        for log in logs:
            text_field(log, 'query'); text_field(log, 'status')
        records = list_field(obj, 'sources')
        if len(records) > limits['host_max_sources']:
            raise ValueError('Source count exceeds this run budget')
        unique_ids(records)
        for record in records:
            url = text_field(record, 'url')
            if not url.startswith(('https://', 'http://')):
                raise ValueError('Source needs an HTTP(S) identity URL')
            if record.get('status') not in ('read', 'unavailable'):
                raise ValueError('Source status must be read or unavailable')
            for key in ('version', 'checked_at', 'read_scope', 'locator', 'supports', 'does_not_support'):
                text_field(record, key)
            try:
                datetime.fromisoformat(record['checked_at'])
            except ValueError:
                raise ValueError('Source checked_at must be an ISO date or datetime')
        if not any(x['status'] == 'read' for x in records):
            raise Blocked('No source has a recorded reading scope')
        list_field(obj, 'unresolved', False)
    elif stage == 'protocol':
        if mode == 'wine':
            if digest(path) != digest(WINE / 'protocol.json'):
                raise ValueError('Wine demo only accepts the preserved protocol')
        else:
            for key in ('design', 'unit', 'split_or_comparison', 'leakage_control', 'stopping_rule'):
                text_field(obj, key)
            strings(obj, 'conditions'); strings(obj, 'metrics')
            if not isinstance(obj.get('previous_results_known'), bool):
                raise Blocked('Declare previous_results_known as true or false')
            names += refs(run, list_field(obj, 'data'), sources=source_ids(run))
    elif stage == 'experiment':
        if obj.get('status') != 'measured':
            raise Blocked('Experiment must contain an actual measured run')
        if text_field(obj, 'protocol_sha256') != digest(safe(run, 'protocol.json')):
            raise ValueError('Experiment does not refer to the accepted protocol')
        for key in ('command', 'environment'):
            text_field(obj, key)
        names += refs(run, list_field(obj, 'artifacts'))
        list_field(obj, 'failures', False)
    elif stage == 'analysis':
        text_field(obj, 'unit'); text_field(obj, 'comparisons'); strings(obj, 'limitations')
        artifacts = unique_ids(read(safe(run, 'experiment.json'))['artifacts'])
        validate_claims(list_field(obj, 'claims'), source_ids(run), artifacts)
    else:
        claims = object_read(safe(run, 'claims.json')); names.append('claims.json')
        analysis = read(safe(run, 'analysis.json'))
        if claims.get('claims') != analysis['claims']:
            raise ValueError('Report claim map differs from accepted analysis')
        if claims.get('limitations') != analysis['limitations']:
            raise ValueError('Report must retain analysis limitations')
        if claims.get('review_status') not in ('host_reviewed', 'template_generated'):
            raise Blocked('Declare report review_status')
        text_field(claims, 'review_scope')
        content = path.read_text(encoding='utf-8')
        for text in [c['text'] for c in analysis['claims']] + analysis['limitations']:
            if text not in content:
                raise ValueError('Report omits a mapped claim or limitation')
    if stage in ('experiment', 'analysis'):
        records = list_field(obj, 'execution_records', False) if 'execution_records' in obj else []
        failures = list_field(obj, 'failures', False) if 'failures' in obj else []
        for name in records + failures:
            if name in ('state.json', 'state.json.tmp', 'events.jsonl', 'NEXT.md', '.pipeline.lock'):
                raise ValueError('Execution record refers to runner control file')
            safe(run, name)
            names.append(name)
    return list(dict.fromkeys(names))


def instructions(stage, limits):
    return {
        'question': '填写 question.json 的四项：question＝想比较的具体问题；scope＝这次比较的范围；resources＝真实已有材料和可用资源；stopping_condition＝完成什么检查或达到什么限制时结束。四项均用非空文字；未知材料不代填。',
        'evidence': '保存 evidence.json：mode=new/reused；search_log=[{query,status}]；sources=[{id,url,version,checked_at,status:read/unavailable,read_scope,locator,supports,does_not_support}]；unresolved=[]。checked_at为实际核对日期。最多' + str(limits['host_max_searches']) + '次检索、' + str(limits['host_max_sources']) + '项来源，真实记录阅读范围与失败。',
        'protocol': '保存 protocol.json：design、unit、split_or_comparison、leakage_control、stopping_rule（字符串）；conditions、metrics（字符串数组）；previous_results_known（布尔）；data=[{path,sha256,source_id,license}]。数据路径相对此运行目录。',
        'experiment': '按已授权方案实际运行后保存 experiment.json：status=measured，protocol_sha256，command、environment（字符串），artifacts=[{id,path,sha256}]，failures=[失败记录的相对文件路径]；没有失败时用空数组。命令仅作为记录，本程序不会执行自定义命令。失败文件必须存在并会固定摘要。',
        'analysis': '核对全部条件与独立单位，保存 analysis.json：unit、comparisons（字符串），limitations（字符串数组），claims=[{id,text,artifact_ids:[],source_ids:[],locator}]。每条主张至少对应一个已登记来源或产物。',
        'report': '保存 REPORT.md 和 claims.json：claims、limitations与analysis.json完全一致；review_status=host_reviewed或template_generated；review_scope（实际检查范围）。报告包含每条主张原文和每条限制；结构通过不等于语义审核或外部审稿。',
    }[stage]


def next_file(run, state):
    incomplete = next((s for s in state['stages'] if s['status'] != 'accepted'), None)
    lines = ['# 下一步', '', '模式：' + state['mode'], '']
    if incomplete:
        lines += ['当前步骤：' + incomplete['id'], '', instructions(incomplete['id'], state['limits']), '',
                  '补齐后运行：python -B scripts/research_pipeline.py advance --run "本次输出目录"',
                  '已接受的输入和产物不可原地更改；改变研究方案时建立新运行目录。']
        route = next(s for s in object_read(safe(ROOT, 'workflows/automated-research/skill-routing.json'))['stages']
                     if s['id'] == incomplete['id'])
        lines += ['', '## 助手在此步读取的技能', '', '以下路径均相对仓库根目录；先读模块索引，再读本步主入口。', '',
                  '- 模块索引：`' + route['module_index'] + '`',
                  '- 主入口：`' + route['primary']['path'] + '`；使用条件：' + route['primary']['use_when']]
        for skill in route.get('supplemental', []):
            lines.append('- 条件参考（需要时再读）：`' + skill['path'] + '`；' + skill['use_when'])
    else:
        lines += ['六步交接完成。阅读 REPORT.md；用 verify 核对本次运行。',
                  'Wine模式有数值重算；custom模式仅核对结构、路径、摘要和引用，不自动证明科学主张。']
    safe(run, 'NEXT.md', exists=False).write_text('\n'.join(lines) + '\n', encoding='utf-8')


def command(run, stage, script, args, timeout=TIMEOUT):
    """Execute only the two audited, bundled Wine entrypoints. Never a shell string."""
    if script not in ('run_case.py', 'verify_case.py'):
        raise ValueError('Unlisted executable adapter')
    attempts = run / 'attempts'
    if attempts.exists() and not attempts.is_dir():
        raise ValueError('Invalid attempts directory')
    safe(run, 'attempts', exists=False)
    attempts.mkdir(exist_ok=True)
    number = 1
    while (attempts / f'{stage}-{number:03d}').exists():
        number += 1
    if stage in ('experiment', 'analysis') and number > MAX_ATTEMPTS:
        raise ValueError('Stage attempt budget exhausted (3). Preserve logs and create a new run after fixing the cause.')
    folder = attempts / f'{stage}-{number:03d}'
    folder.mkdir(exist_ok=False)
    output = folder / 'output'
    effective = [str(output) if x == '{output}' else str(x) for x in args]
    argv = [sys.executable, '-B', '-X', 'utf8', str(WINE / script), *effective]
    env = dict(os.environ); env.pop('PYTHONOPTIMIZE', None)
    started = now()
    try:
        result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True,
                                text=True, encoding='utf-8', errors='replace', timeout=timeout)
        code, stdout, stderr = result.returncode, result.stdout, result.stderr
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        def decoded(v):
            return v.decode('utf-8', 'replace') if isinstance(v, bytes) else (v or '')
        code, stdout, stderr, timed_out = None, decoded(exc.stdout), decoded(exc.stderr), True
    (folder / 'stdout.txt').write_text(stdout, encoding='utf-8')
    (folder / 'stderr.txt').write_text(stderr, encoding='utf-8')
    write(folder / 'command.json', {'entrypoint': 'examples/real-wine/' + script,
          'arguments': [x.replace(str(run), '<run>') for x in effective],
          'started_at': started, 'finished_at': now(), 'exit_code': code,
          'timeout_seconds': timeout, 'timed_out': timed_out, 'python': platform.python_version()})
    if timed_out or code != 0:
        raise ValueError('Adapter failed; preserved logs: ' + folder.relative_to(run).as_posix())
    return output, folder


def attempt_records(run, stage):
    """Freeze every existing attempt file, including failed logs and partial output."""
    records = []
    for folder in sorted((run / 'attempts').glob(stage + '-*')):
        safe(run, folder.relative_to(run).as_posix(), exists=False)
        if not folder.is_dir():
            raise ValueError('Attempt path is not a directory')
        for path in sorted(folder.rglob('*')):
            name = path.relative_to(run).as_posix()
            safe(run, name, exists=False)
            if path.is_file():
                records.append(name)
    return records


def failed_commands(run, stage):
    return [path.relative_to(run).as_posix() for path in sorted((run / 'attempts').glob(stage + '-*/command.json'))
            if object_read(safe(run, path.relative_to(run).as_posix()))['exit_code'] != 0]


def wine_step(run, stage):
    if stage == 'question':
        write(run / 'question.json', {'question': '训练集标准化是否改善UCI Wine固定5-NN品种分类？',
              'scope': '复跑既有公开基准比较，非新颖性或整篇论文复现。',
              'resources': '已有公开178行Wine数据，CPU与Python标准库，离线复跑。',
              'stopping_condition': '完成固定六划分、三条件、810条预测并核验；不根据测试分数换方案。',
              'origin': 'reused study question; this execution does not preregister a new study'})
    elif stage == 'evidence':
        original = read(WINE / 'sources.json')
        write(run / 'evidence.json', {'mode': 'reused', 'original_record_date': original['date'],
              'search_log': [], 'new_searches_this_run': 0,
              'sources': [dict(x, status='read', checked_at=original['date'],
                         version=x.get('version_note', x.get('observed_version', x.get('citation', 'recorded source version'))))
                          for x in original['records']],
              'unresolved': original['problems_observed'],
              'other_candidates': original['other_candidates'],
              'scope': '历史限定阅读记录的导入；本次没有联网、重读全文或刷新引用。'})
    elif stage == 'protocol':
        (run / 'protocol.json').write_bytes((WINE / 'protocol.json').read_bytes())
    elif stage == 'experiment':
        output, folder = command(run, stage, 'run_case.py', ['--output', '{output}'])
        manifest = read(safe(output, 'manifest.json'))
        names = list(manifest['artifact_sha256']) + ['manifest.json']
        write(run / 'experiment.json', {'status': 'measured', 'protocol_sha256': digest(run / 'protocol.json'),
              'command': 'Python examples/real-wine/run_case.py --output <new attempt/output>',
              'environment': 'Python ' + platform.python_version() + '; local CPU; standard library; offline',
              'artifacts': [{'id': Path(n).stem, 'path': (output / n).relative_to(run).as_posix(), 'sha256': digest(safe(output, n))} for n in names],
              'failures': failed_commands(run, stage),
              'execution_records': attempt_records(run, stage),
              'validation_scope': 'files present; numeric recalculation is the next stage'})
    elif stage == 'analysis':
        experiment = read(run / 'experiment.json')
        artifact = {x['id']: safe(run, x['path']) for x in experiment['artifacts']}
        _, folder = command(run, stage, 'verify_case.py', ['--input', artifact['manifest'].parent])
        metrics, pair = read(artifact['metrics']), read(artifact['paired-analysis'])
        primary = [m for m in metrics if m['seed'] == pair['seed']]
        claims = [{'id': 'C' + str(i + 1), 'text': f"主划分中，{m['condition']}的正确数为{m['correct']}/{m['n']}，准确率{m['accuracy']:.2%}。",
                   'artifact_ids': ['metrics', 'predictions'], 'source_ids': [],
                   'locator': 'metrics.json: seed=' + str(m['seed']) + ', condition=' + m['condition']} for i, m in enumerate(primary)]
        claims.append({'id': 'C4', 'text': f"主划分标准化相对原始尺度提高{pair['difference_pp']:.2f}个百分点；固定模型和类别比例下的95%配对分层区间为[{pair['interval_pp'][0]:.2f}, {pair['interval_pp'][1]:.2f}]个百分点。",
                       'artifact_ids': ['paired-analysis'], 'source_ids': [], 'locator': 'paired-analysis.json: difference_pp, interval_pp'})
        write(run / 'analysis.json', {'unit': '178个原始样本；主划分45个测试样本；各划分共享观测，不合并为810个独立样本。',
              'comparisons': '全部6个固定划分×3个预定条件；训练参数、预测、指标和区间已由独立实现重算。',
              'limitations': ['主划分45/45只描述本次留出样本，不能保证未来始终正确。',
                  '补充划分仅做描述；共享样本，不能当作六项独立研究合并推断。',
                  '区间未覆盖训练变化、模型选择、新地区或年份；数据没有可核对的批次分组ID。',
                  '文献记录复用历史指定阅读范围；没有本次实时检索、全文重读或外部审稿。'],
              'claims': claims, 'validation_scope': 'independent_numeric_recalculation',
              'failures': failed_commands(run, stage),
              'execution_records': attempt_records(run, stage),
              'all_metrics': metrics})
    else:
        analysis = read(run / 'analysis.json')
        claims = {'claims': analysis['claims'], 'limitations': analysis['limitations'],
                  'review_status': 'template_generated', 'review_scope': '基于本次重算数值的确定性模板；不声称LLM写作或人工/外部审稿。'}
        write(run / 'claims.json', claims)
        lines = ['# 标准化会改善葡萄酒品种分类吗？', '',
                 '这是既有UCI Wine协议的本次离线复跑报告。前三步复用既有材料，实验与数值核对在本次执行。', '',
                 '## 本次结果', ''] + ['- ' + c['text'] for c in claims['claims']]
        lines += ['', '| 划分 | 条件 | 正确数 | 准确率 |', '|---|---|---:|---:|']
        for m in analysis['all_metrics']:
            lines.append(f"| {m['seed']} | {m['condition']} | {m['correct']}/{m['n']} | {m['accuracy']:.2%} |")
        lines += ['', '## 适用范围', ''] + ['- ' + s for s in claims['limitations']]
        lines += ['', '## 复用的来源', '']
        for s in read(run / 'evidence.json')['sources']:
            lines += [f"- {s['id']}: {s['url']}；阅读范围：{s['read_scope']}"]
        lines += ['', '数据：UCI Wine，DOI 10.24432/C5PC7J，CC BY 4.0。',
                  '来源原始阅读记录日期为2026-10-23；本程序没有下载或重新阅读论文。',
                  '报告由模板生成；可选绘图未运行，不借用旧图作为本轮新产物。',
                  '逐步状态见state.json，原始运行和失败日志见attempts/，主张映射见claims.json。']
        (run / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def initialize(output, mode, topic='', max_searches=4, max_sources=8):
    output = external(output, new=True)
    if mode == 'custom' and not topic.strip():
        raise ValueError('Supply a nonempty research question')
    if any(type(x) is not int or x < 1 for x in (max_searches, max_sources)):
        raise ValueError('Search/source budgets must be positive integers')
    repo = fingerprints(mode)
    output.mkdir(parents=True, exist_ok=False)
    state = {'schema_version': SCHEMA, 'mode': mode, 'created_at': now(), 'status': 'in_progress',
             'repository_inputs': repo, 'limits': {'subprocess_timeout_seconds': TIMEOUT,
                 'automatic_retries': 0, 'max_stage_attempts': MAX_ATTEMPTS,
                 'host_max_searches': max_searches, 'host_max_sources': max_sources,
                 'network_in_runner': False, 'paid_services_in_runner': False,
                 'host_budget_note': 'Host must record actual work; runner does not meter external service spending.'},
             'stages': [{'id': s, 'status': 'pending', 'inputs': {}, 'outputs': {}} for s in STAGES]}
    state['configuration_sha256'] = configuration_digest(state)
    if mode == 'custom':
        write(output / 'question.json', {'question': topic, 'scope': '', 'resources': '', 'stopping_condition': ''})
    event(output, state, None, 'created', mode)
    save_state(output, state); next_file(output, state)
    return output


def advance(run):
    run = external(run)
    with locked(run):
        state = load_state(run)
        integrity(run, state)
        for stage in state['stages']:
            if stage['status'] == 'accepted':
                continue
            sid = stage['id']
            before = {name: expected for s in state['stages'] if s['status'] == 'accepted' for name, expected in s['outputs'].items()}
            event(run, state, sid, 'started', 'continue without rerunning accepted stages')
            try:
                if state['mode'] == 'wine':
                    wine_step(run, sid)
                names = validate_stage(run, sid, state['mode'], state['limits'])
                integrity(run, state)
                stage.update(status='accepted', inputs=before, outputs={n: digest(safe(run, n)) for n in names},
                             mode=('reused' if sid in STAGES[:3] else 'measured' if sid == 'experiment' else
                                   'independently_recalculated' if sid == 'analysis' else 'template_generated')
                                   if state['mode'] == 'wine' else 'host_supplied',
                             validation_scope='bounded_wine_adapter' if state['mode'] == 'wine' else 'structure_and_reference_integrity')
                event(run, state, sid, 'accepted', stage['validation_scope'])
            except (OSError, ValueError, KeyError, TypeError) as exc:
                status = 'blocked' if isinstance(exc, Blocked) and state['mode'] == 'custom' else 'failed'
                stage['status'] = status; stage['problem'] = str(exc); state['status'] = status
                event(run, state, sid, status, str(exc))
                save_state(run, state); next_file(run, state)
                print(status.upper() + ': ' + sid + ': ' + str(exc))
                return 2 if status == 'blocked' else 1
            stage.pop('problem', None)
            state['status'] = 'in_progress'
            save_state(run, state)
        state['status'] = 'complete'
        save_state(run, state); next_file(run, state)
        print('COMPLETE: six stages accepted; mode=' + state['mode'] + '; report=' + str(run / 'REPORT.md'))
        return 0


def verify(run):
    run = external(run)
    with locked(run):
        state = load_state(run)
        integrity(run, state)
        if state['status'] != 'complete' or any(s['status'] != 'accepted' for s in state['stages']):
            raise Blocked('Run is incomplete; consult NEXT.md')
        for stage in STAGES:
            validate_stage(run, stage, state['mode'], state['limits'])
        if state['mode'] == 'wine':
            artifacts = read(run / 'experiment.json')['artifacts']
            manifest = next(x for x in artifacts if x['id'] == 'manifest')
            command(run, 'verify', 'verify_case.py', ['--input', safe(run, manifest['path']).parent])
        scope = 'independent Wine numeric recalculation' if state['mode'] == 'wine' else 'structure and reference integrity only'
        print('PASS: ' + scope)
        return 0


def doctor():
    fingerprints('wine')
    preserved = object_read(safe(WINE, 'recorded/manifest.json'))
    for group in ('input_sha256', 'source_sha256'):
        for name, expected in preserved[group].items():
            if digest(safe(WINE, name)) != expected:
                raise ValueError('Preserved Wine adapter/input mismatch: ' + name)
    routing = safe(ROOT, 'workflows/automated-research/skill-routing.json')
    count = 0
    for stage in object_read(routing)['stages']:
        safe(ROOT, stage['module_index'])
        for skill in [stage['primary'], *stage.get('supplemental', [])]:
            if digest(safe(ROOT, skill['path'])) != skill['sha256']:
                raise ValueError('Skill fingerprint mismatch: ' + skill['path'])
            count += 1
    print(json.dumps({'python': platform.python_version(), 'core': 'standard library',
          'optional_matplotlib_available': importlib.util.find_spec('matplotlib') is not None,
          'local_skill_references_checked': count, 'network_required': False,
          'adapter': 'Wine only; custom tasks use host-prepared artifacts, no arbitrary command execution'}, ensure_ascii=False))
    return 0


def main(argv=None):
    if sys.flags.optimize:
        print('ERROR: Python -O/PYTHONOPTIMIZE disables the bundled independent verifier assertions; use normal Python.', file=sys.stderr)
        return 1
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor')
    for name in ('demo', 'init'):
        p = sub.add_parser(name); p.add_argument('--output', type=Path, required=True)
        if name == 'init':
            p.add_argument('--topic', required=True)
            p.add_argument('--max-searches', type=int, default=4)
            p.add_argument('--max-sources', type=int, default=8)
    for name in ('advance', 'status', 'verify'):
        p = sub.add_parser(name); p.add_argument('--run', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'doctor':
            return doctor()
        if args.command in ('demo', 'init'):
            folder = initialize(args.output, 'wine' if args.command == 'demo' else 'custom', getattr(args, 'topic', ''),
                                getattr(args, 'max_searches', 4), getattr(args, 'max_sources', 8))
            print('RUN: ' + str(folder))
            return advance(folder)
        if args.command == 'advance':
            return advance(args.run)
        if args.command == 'verify':
            return verify(args.run)
        folder = external(args.run); state = load_state(folder); integrity(folder, state)
        print(json.dumps({'status': state['status'], 'mode': state['mode'],
              'stages': [{'id': s['id'], 'status': s['status'], 'mode': s.get('mode')} for s in state['stages']],
              'next': 'NEXT.md'}, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, StopIteration) as exc:
        print(('BLOCKED: ' if isinstance(exc, Blocked) else 'ERROR: ') + str(exc), file=sys.stderr)
        return 2 if isinstance(exc, Blocked) else 1


if __name__ == '__main__':
    sys.exit(main())
