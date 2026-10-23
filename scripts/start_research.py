#!/usr/bin/env python3
"""Beginner intake for custom research. No network, installs or user-code execution."""
import argparse
from contextlib import redirect_stdout
import csv
import hashlib
import importlib.metadata
import io
import json
import os
from pathlib import Path
import platform
import re
import shutil
import sys
import tempfile
from urllib.parse import urlsplit
import uuid
import zipfile

import research_pipeline as pipeline

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 50 * 1024 * 1024
MAX_ROWS = 1000
MISSING = {'', 'na', 'n/a', 'nan', 'null', 'none'}


def save(path, value):
    pipeline.write(path, value)


def file_hash(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def requirement(value):
    match = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9_.-]*)(?:==([A-Za-z0-9][A-Za-z0-9_.+!-]*))?', value)
    if not match:
        raise ValueError('依赖只接受包名或包名==确切版本；复杂环境请由助手另行检查。')
    return match.groups()


def dependency(value, reason):
    name, pinned = requirement(value)
    result = {'name': name, 'reason': reason, 'requested': value, 'import_tested': False}
    try:
        version = importlib.metadata.version(name)
        result.update(version=version, status='manual_check' if not isinstance(version, str) or not version else
                      'version_mismatch' if pinned and pinned != version else 'metadata_detected')
    except importlib.metadata.PackageNotFoundError:
        result.update(version=None, status='not_detected')
    except (OSError, ValueError):
        result.update(version=None, status='manual_check')
    return result


def source_name(value):
    if value.startswith(('https://', 'http://')):
        parsed = urlsplit(value)
        if not parsed.hostname or parsed.username or parsed.password:
            raise ValueError('请提供不含账号口令的论文/数据网址。')
        return value
    return str(Path(value).expanduser().resolve())


def add_materials(intake, papers, data, requirements):
    for kind, values in (('paper', papers), ('data', data)):
        for value in values:
            source = source_name(value)
            if any(x['kind'] == kind and x['source'] == source for x in intake['materials']):
                continue
            intake['materials'].append({'id': 'M' + str(len(intake['materials']) + 1).zfill(3), 'kind': kind, 'source': source})
    for value in requirements:
        requirement(value)
        if value not in intake['requirements']:
            intake['requirements'].append(value)


def table_preview(path):
    """Inspect a bounded row sample; never return cell values or choose a target."""
    csv.field_size_limit(1024 * 1024)
    last = None
    for encoding in ('utf-8-sig', 'gb18030'):
        try:
            with path.open(encoding=encoding, newline='') as stream:
                sample = stream.read(8192)
                if '\x00' in sample:
                    raise ValueError('发现二进制/UTF-16内容；请导出UTF-8 CSV或由助手选合适解析器。')
                stream.seek(0)
                delimiter = '\t' if path.suffix.lower() == '.tsv' else ','
                if path.suffix.lower() == '.csv':
                    try:
                        delimiter = csv.Sniffer().sniff(sample, delimiters=',;\t').delimiter
                    except csv.Error:
                        pass
                reader = csv.reader(stream, delimiter=delimiter, strict=True)
                headers = next(reader, None)
                if not headers or any(not h.strip() for h in headers) or len(headers) != len(set(headers)):
                    raise ValueError('缺少有效表头，或列名为空/重复；请先核对表头。')
                count, missing, ragged, complete = 0, [0] * len(headers), 0, True
                for row in reader:
                    if count == MAX_ROWS:
                        complete = False
                        break
                    count += 1
                    if len(row) != len(headers):
                        ragged += 1
                    else:
                        for i, cell in enumerate(row):
                            missing[i] += cell.strip().lower() in MISSING
                if count == 0:
                    raise ValueError('只有表头，没有数据记录。')
                return {'columns': headers, 'rows_inspected': count, 'complete_scan': complete,
                        'ragged_rows_in_sample': ragged, 'missing_in_sample': dict(zip(headers, missing)),
                        'encoding': encoding, 'delimiter': delimiter, 'sample_limit': MAX_ROWS,
                        'scope': '结构预览；缺失标记是候选，不删行、不推断变量含义、不选目标。'}
        except UnicodeError as exc:
            last = exc
    raise ValueError('不能按UTF-8或GB18030解码；请告知编码或提供UTF-8副本。') from last


def inspect_material(run, item):
    result = {k: item[k] for k in ('id', 'kind', 'source')}
    source = item['source']
    if source.startswith(('http://', 'https://')):
        return dict(result, status='pending_retrieval', message='已登记链接；本检查器未联网、未获取、未阅读。')
    path = Path(source)
    if not path.is_file():
        return dict(result, status='missing', message='找不到这个本地文件；核对路径，或提供可访问的文件。')
    if path.is_symlink() or any(p.is_symlink() for p in path.parents):
        return dict(result, status='unsupported', message='请提供原文件的真实路径，避免符号链接改变材料指向。')
    if path.resolve().is_relative_to(run.resolve()):
        return dict(result, status='unsupported', message='请登记项目外的原始材料；项目内已有副本无需重复添加。')
    try:
        size = path.stat().st_size
        if size == 0:
            return dict(result, status='empty', message='文件为空；请提供有内容的材料。')
        if size > MAX_BYTES:
            return dict(result, status='too_large', bytes=size, message='超过50MiB自动接收范围；由助手按需读取或另备有代表性的脱敏样本，不能把样本冒充全量。')
        current = file_hash(path)
        if 'sha256' in item and current != item['sha256']:
            return dict(result, status='source_changed', message='原始材料与接收时不同；保留旧档案，改用新运行目录接收新版。')
        if 'path' not in item:
            clean = re.sub(r'[^\w.\-]', '_', path.stem)[:85] + path.suffix[:14]
            relative = 'materials/' + item['id'] + '-' + clean
            dest = pipeline.safe(run, relative, exists=False)
            # A partial intake never overwrites an existing material snapshot.
            with path.open('rb') as src, dest.open('xb') as dst:
                shutil.copyfileobj(src, dst)
            if file_hash(dest) != current or file_hash(path) != current:
                raise ValueError('复制期间材料发生变化；请停止编辑原文件并另开运行。')
            item.update(path=relative, sha256=current, received_at=pipeline.now())
        dest = pipeline.safe(run, item['path'])
        if file_hash(dest) != item['sha256']:
            return dict(result, status='snapshot_changed', message='项目材料副本被改写；请保留记录，另开运行，不能沿用旧摘要。')
        result.update(path=item['path'], sha256=current, bytes=size, read_scope='not_read_by_this_checker')
        suffix = dest.suffix.lower()
        if suffix in ('.csv', '.tsv') and item['kind'] == 'data':
            preview = table_preview(dest)
            result['inspection'] = preview
            status = 'invalid_format' if preview['ragged_rows_in_sample'] else 'table_preview'
            return dict(result, status=status, message='已预览表格结构；不代表数据适合当前研究。' if status == 'table_preview' else '预览行的列数不一致；请核对分隔符、引号与缺失列。')
        if suffix in ('.md', '.txt'):
            try:
                with dest.open(encoding='utf-8-sig') as stream:
                    text = stream.read(65536)
            except UnicodeError:
                return dict(result, status='invalid_format', message='文本不是可读取的UTF-8；请转为UTF-8或提供可复制片段。')
            if not text.strip() or '\x00' in text:
                return dict(result, status='invalid_format', message='未检测到可用文本；请提供正文或明确的片段。')
            return dict(result, status='text_available', message='已接收文本，检查了开头至多65536字符的编码；未做论文阅读、身份或结论核验。')
        if suffix == '.pdf':
            with dest.open('rb') as stream:
                if not stream.read(5).startswith(b'%PDF-'):
                    return dict(result, status='invalid_format', message='扩展名为PDF，但未检测到PDF文件头；请重新导出文件。')
            return dict(result, status='requires_reader', suggested_dependency='pypdf', message='PDF已接收，仅核对文件头；助手还需实际读取。可用现有PDF工具，或提供摘要/正文文本；扫描版可能需要OCR。')
        if suffix == '.xlsx':
            try:
                with zipfile.ZipFile(dest) as archive:
                    if 'xl/workbook.xml' not in archive.namelist():
                        raise ValueError('工作簿结构缺失')
            except (zipfile.BadZipFile, ValueError):
                return dict(result, status='invalid_format', message='未检测到有效XLSX容器；请重新导出或提供CSV。')
            return dict(result, status='requires_reader', suggested_dependency='openpyxl', message='已接收XLSX容器；尚未读取工作表、公式或单元格。可由助手解析，或导出所需表为CSV。')
        return dict(result, status='unsupported', message='文件已接收；此格式没有自动结构预览，请由助手选择适合的读取工具。')
    except (OSError, ValueError, csv.Error) as exc:
        return dict(result, status='unreadable', message='材料检查未完成：' + str(exc))


def check(run, papers=(), data=(), requirements=()):
    run = pipeline.external(run)
    with pipeline.locked(run):
        intake = pipeline.object_read(pipeline.safe(run, 'intake.json'))
        if intake.get('schema_version') != 1:
            raise ValueError('不支持的材料登记版本。')
        state = pipeline.load_state(run)
        issues = []
        try:
            pipeline.integrity(run, state)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            issues.append({'code': 'pipeline_integrity', 'message': str(exc), 'action': '已有阶段或执行器变化；保留此运行，另开项目，不修改历史摘要。'})
        protocol = next(x for x in state['stages'] if x['id'] == 'protocol')
        if (papers or data or requirements) and (protocol['status'] == 'accepted' or issues):
            raise ValueError('协议已固定或完整性异常；新增研究材料/依赖请另开运行，不修改当前档案。')
        add_materials(intake, papers, data, requirements)
        results = [inspect_material(run, item) for item in intake['materials']]
        for kind, label in (('paper', '论文'), ('data', '数据')):
            if not any(x['kind'] == kind for x in results):
                issues.append({'code': 'missing_' + kind, 'message': '尚未提供' + label + '。',
                               'action': '补充' + label + '文件/链接；暂时没有也可先由助手收窄问题与寻找材料。'})
        for result in results:
            if result['status'] not in ('table_preview', 'text_available'):
                label = '论文' if result['kind'] == 'paper' else '数据'
                supplied = result['source'] if result['source'].startswith(('http://', 'https://')) else Path(result['source']).name
                action = ('请助手实际获取' if result['status'] == 'pending_retrieval' else '请助手处理') + label + '：' + supplied
                issues.append({'code': result['status'], 'material_id': result['id'], 'message': result['message'],
                               'action': action + '；完成后重查，其他可读材料可先整理。'})
        dependencies = [dependency(value, '助手或用户为当前研究显式声明') for value in intake['requirements']]
        for result in results:
            if 'suggested_dependency' in result:
                dependencies.append(dependency(result['suggested_dependency'], result['id'] + '的可选本地解析路径；可用宿主工具或转换文本替代'))
        for dep in dependencies:
            if dep['requested'] in intake['requirements'] and dep['status'] != 'metadata_detected':
                issues.append({'code': 'dependency_' + dep['status'], 'message': dep['name'] + '：未满足声明的安装元数据条件。',
                               'action': '由助手确认当前解释器与必要版本，再决定环境准备；本入口不安装包或执行包代码。'})
        stage = next((s for s in state['stages'] if s['status'] != 'accepted'), None)
        integrity_error = any(x['code'] in ('pipeline_integrity', 'source_changed', 'snapshot_changed') for x in issues)
        status = 'integrity_error' if integrity_error else 'needs_attention' if issues else 'pipeline_complete' if state['status'] == 'complete' else 'ready_for_review'
        if integrity_error:
            actions = ['保留此目录和记录，由助手检查变化原因；数据、方案或代码更新后另开运行。']
        elif stage is None:
            actions = ['阅读REPORT.md并核对实际验证范围；如换问题、材料或实现，创建新运行。',
                       '材料预览状态与六步进度独立；宿主已读PDF或已获取链接不会自动改变检查器的预览标签，请以evidence的实际记录核对。']
        else:
            actions = [x['action'] for x in issues[:2]]
            actions.append({'question': '请助手读取现有材料，明确研究范围、观测单位和停止条件，再按NEXT.md推进。',
                'evidence': '请助手实际阅读/获取资料，记录身份、版本、阅读范围与失败；不要把材料登记当已读证据。',
                'protocol': '请助手补齐数据字典、来源/许可、单位、比较/划分和指标，并在实验前固定实际代码与依赖配置。',
                'experiment': '先由助手检查所选代码的必要环境并做小范围功能验证，再按已固定协议实际运行和保留日志。',
                'analysis': '请助手核对全部条件、分母和逐条结果，执行适合本题的独立核验，保留负结果。',
                'report': '请助手将主张逐项对应证据，保留限制和未决项，再生成并核验报告。'}[stage['id']])
        result = {'schema_version': 1, 'checked_at': pipeline.now(), 'status': status,
            'question': intake['question'], 'materials': results, 'dependencies': dependencies, 'issues': issues,
            'next_actions': list(dict.fromkeys(actions))[:3],
            'pipeline': {'status': state['status'], 'current_stage': stage['id'] if stage else None, 'problem': stage.get('problem') if stage else None},
            'environment': {'python': platform.python_version(), 'executable': sys.executable, 'core': 'standard library', 'platform': platform.system()},
            'checker_sha256': file_hash(Path(__file__)),
            'scope': '材料接收/有限结构预览与包安装元数据；无联网、无全文阅读、无任意代码导入/执行、无安装、无模型/科学有效性判断。',
            'not_checked': ['实际论文阅读范围和引用支持', '数据的来源/许可、字典、采样单位与研究适用性', '尚未选择的实验代码、GPU/外部服务与模型运行依赖']}
        result['handoff_notes'] = []
        if any(s['id'] == 'question' and s['status'] == 'accepted' for s in state['stages']):
            result['handoff_notes'].append('材料检查不会修改已接受的问题范围；若新材料改变范围或停止条件，请另开运行。')
        if any(s['id'] == 'evidence' and s['status'] == 'accepted' for s in state['stages']):
            result['handoff_notes'].append('已接受证据仍是原evidence.json；这里接收的补充论文未自动纳入已固定证据。若阅读后改变来源、主张或方案，请另开运行。')
        history = pipeline.safe(run, 'intake-checks', exists=False)
        history.mkdir(exist_ok=True)
        number = 1
        while (history / f'{number:04d}.json').exists():
            number += 1
        save(pipeline.safe(run, f'intake-checks/{number:04d}.json', exists=False), result)
        save(pipeline.safe(run, 'intake.json'), intake)
        save(pipeline.safe(run, 'CHECKS.json', exists=False), result)
        render(run, result)
    print('项目目录：' + str(run))
    print({'ready_for_review': '材料检查完成，可以开始阅读与定题；研究尚未完成。', 'needs_attention': '已建立/更新项目，以下材料或环境仍需处理。',
           'integrity_error': '检测到材料或已接受记录变化，请先处理完整性问题。', 'pipeline_complete': '已有六步交接完成记录；材料检查不增加科学验证范围。'}[status])
    for action in result['next_actions']:
        print('- ' + action)
    print('中文检查页：' + str(run / 'START_HERE.md'))
    return 0 if status in ('ready_for_review', 'pipeline_complete') else 2


def render(run, result):
    labels = {'paper': '论文', 'data': '数据'}
    lines = ['# 从这里继续', '', '最初提供的问题：' + result['question'], '',
             '本页是材料检查结果，不是研究结果。先处理当前缺口；JSON与六步交接由助手维护。', '',
             '## 已收到', '']
    for material in result['materials']:
        lines += ['- ' + labels[material['kind']] + '：' + material['source'],
                  '  - ' + material['message']]
        if material.get('path'):
            lines.append('  - 项目副本：`' + material['path'] + '`；科学阅读范围：尚未由本检查器阅读。')
        if 'inspection' in material:
            i = material['inspection']
            lines.append('  - 列名：' + '、'.join(i['columns']) + f"；检查{i['rows_inspected']}行，" + ('已扫描当前表全部记录。' if i['complete_scan'] else '仅为前1000行预览。'))
    if not result['materials']:
        lines.append('尚未提供论文或数据；可以先与助手收窄问题。')
    lines += ['', '## 当前缺口', '']
    lines += ['- ' + x['message'] for x in result['issues']] or ['- 自动材料检查未发现阻塞项；仍需实际阅读与研究设计。']
    lines += ['', '## 当前环境', '', '- 检查器正在Python ' + result['environment']['python'] + '运行；本入口只用标准库。']
    meanings = {'metadata_detected': '检测到安装元数据；未导入或验证功能', 'not_detected': '未检测到安装元数据', 'version_mismatch': '安装版本与声明不符', 'manual_check': '需要人工/宿主检查'}
    for d in result['dependencies']:
        lines.append('- ' + d['name'] + '：' + meanings[d['status']] + '；' + d['reason'])
    lines.append('- 模型、GPU和外部服务依赖要在方案选定后检查；不预装整套科研工具。')
    lines += ['', '## 下一步', ''] + [str(i) + '. ' + action for i, action in enumerate(result['next_actions'], 1)]
    lines += ['', *result['handoff_notes']]
    launcher = 'py -3.12 -B -X utf8' if os.name == 'nt' else 'python3 -B -X utf8'
    stages = {'question': '明确问题', 'evidence': '阅读与来源', 'protocol': '固定方案',
              'experiment': '实际实验', 'analysis': '核验与分析', 'report': '报告与主张', None: '交接已完成'}
    lines += ['', '当前六步阶段：' + stages[result['pipeline']['current_stage']] + '。具体交付要求见[NEXT.md](NEXT.md)。',
              '给助手：先读仓库 workflows/automated-research/SKILL.md 当前阶段路由；论文登记不等于evidence中status=read。',
              '重新检查：`' + launcher + ' scripts/start_research.py check --run "本项目目录"`。它更新检查页、追加检查历史，不推进或改写已接受阶段。',
              '核对数据字典、来源/许可和样本单位后再定方案；不要自动套用企鹅例子的目标、模型或删缺失规则。']
    pipeline.safe(run, 'START_HERE.md', exists=False).write_text('\n'.join(lines) + '\n', encoding='utf-8')


def start(args):
    if not args.question.strip() or args.question.strip().upper() in ('TODO', 'TBD', 'UNKNOWN'):
        raise ValueError('请用一句话提供实际研究问题。')
    intake = {'schema_version': 1, 'question': args.question, 'created_at': pipeline.now(), 'materials': [], 'requirements': []}
    add_materials(intake, args.paper, args.data, args.require)
    output = args.output or Path(tempfile.gettempdir()) / ('ars-research-' + uuid.uuid4().hex)
    output = pipeline.initialize(output, 'custom', args.question)
    pipeline.safe(output, 'materials', exists=False).mkdir()
    save(output / 'intake.json', intake)
    # Keep scientific scope and stopping decisions genuinely pending.
    with redirect_stdout(io.StringIO()):
        pipeline.advance(output)
    return check(output)


def main(argv=None):
    parser = argparse.ArgumentParser(description='用研究问题、论文和数据建立项目，自动检查材料并给出中文下一步。')
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('start', 'check'):
        p = sub.add_parser(command)
        p.add_argument('--paper', action='append', default=[])
        p.add_argument('--data', action='append', default=[])
        p.add_argument('--require', action='append', default=[])
        if command == 'start':
            p.add_argument('--question', required=True)
            p.add_argument('--output', type=Path)
        else:
            p.add_argument('--run', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if sys.flags.optimize:
            raise ValueError('请去掉-O或PYTHONOPTIMIZE后运行。')
        if args.command == 'start':
            return start(args)
        return check(args.run, args.paper, args.data, args.require)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('未完成材料检查：' + str(exc), file=sys.stderr)
        print('已有项目请使用check；更换已固定材料时创建仓库外的新目录。', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
