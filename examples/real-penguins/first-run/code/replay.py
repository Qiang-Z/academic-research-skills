#!/usr/bin/env python3
"""Replay this one fixed Penguins case through the generic custom handoff CLI.

This original case driver executes two explicit local programs. It is not a
generic topic adapter and never executes command strings from JSON.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

CASE = Path(__file__).resolve().parent
ROOT = CASE.parents[1]
RUNNER = ROOT / 'scripts/research_pipeline.py'


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def invoke(args, folder, label, expected=0):
    logs = folder / 'logs'
    logs.mkdir(exist_ok=True)
    argv = [sys.executable, '-B', '-X', 'utf8', *map(str, args)]
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    start = now()
    try:
        completed = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8', timeout=120)
        code, stdout, stderr = completed.returncode, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as exc:
        code = None
        stdout = exc.stdout or b''; stderr = exc.stderr or b''
        stdout = stdout.decode('utf-8', 'replace') if isinstance(stdout, bytes) else stdout
        stderr = stderr.decode('utf-8', 'replace') if isinstance(stderr, bytes) else stderr
    # Public logs retain arguments and outputs, with local machine paths redacted.
    def portable(value):
        return str(value).replace(str(folder), '<run>').replace(str(ROOT), '<repo>').replace(sys.executable, '<python>')
    (logs / (label + '.stdout.txt')).write_text(portable(stdout), encoding='utf-8')
    (logs / (label + '.stderr.txt')).write_text(portable(stderr), encoding='utf-8')
    save(logs / (label + '.command.json'), {'argv': [portable(x) for x in argv], 'started_at': start,
         'finished_at': now(), 'exit_code': code, 'expected_exit_code': expected, 'timeout_seconds': 120,
         'python': platform.python_version(), 'platform': platform.system()})
    if code != expected:
        raise RuntimeError(f'{label}: exit {code}, expected {expected}; logs retained in {folder}')
    return ['logs/' + label + suffix for suffix in ('.command.json', '.stdout.txt', '.stderr.txt')]


def report(folder, numeric_logs):
    metrics = read(folder / 'results/metrics.json')
    by_species = read(folder / 'results/species_metrics.json')
    primary = {m['condition']: m for m in metrics if m['split'] == 'primary'}
    difference = primary['flipper_ols']['mae_g'] - primary['flipper_species_ols']['mae_g']
    claims = [
        {'id': 'C1', 'text': '官方数据共344条，按本题所需两列筛选后保留342条；主划分训练223条、测试119条。', 'artifact_ids': ['data_audit', 'splits'], 'source_ids': ['D1'], 'locator': 'data_audit.json; splits.json split=primary'},
        *[{'id': 'C' + str(i + 2), 'text': f"2009年留出记录上，{condition}的MAE为{primary[condition]['mae_g']:.1f}克，RMSE为{primary[condition]['rmse_g']:.1f}克（n=119）。",
           'artifact_ids': ['metrics', 'predictions'], 'source_ids': [], 'locator': 'metrics.json split=primary condition=' + condition}
          for i, condition in enumerate(('mean_baseline', 'flipper_ols', 'flipper_species_ols'))],
        {'id': 'C5', 'text': f'在本次2009年留出记录上，加入物种后MAE比仅用鳍长{'降低' if difference >= 0 else '增加'}{abs(difference):.1f}克；这是固定划分上的描述性差异。',
         'artifact_ids': ['metrics'], 'source_ids': [], 'locator': 'primary flipper_ols MAE minus flipper_species_ols MAE'},
        {'id': 'C6', 'text': 'Horst等2022年论文已讨论鳍长与体重的关系以及加入物种的回归示例；本例是增加时间留出评价的教学延伸。',
         'artifact_ids': [], 'source_ids': ['P2'], 'locator': 'Horst2022: Linear relationships, Figure 4; Discussion'}]
    limitations = [
        '这是三个物种、三个岛屿、三个繁殖季的公开观测数据，不能推广到所有企鹅、地区或未来季节。',
        '原采样包含同巢成对成鸟；简化CSV缺少巢ID，跨年个体重复情况未确认。时间留出不保证个体独立或完全隔离。',
        '物种模型要求预测时已知物种；物种与岛屿等因素相关，本比较不证明物种的因果作用。',
        '两个时间划分共享观测；不合并为独立重复，不报告p值或置信区间，也不声称统计显著或稳定胜出。',
        '排除2条鳍长或体重缺失记录；未建模缺失机制。性别未作预测变量，9条仅缺性别的可用记录仍保留。',
        '论文按来源表指定章节阅读；三个EDI原始数据门户本轮未能读取，实际计算使用固定版本的官方公开CSV。',
        '已有论文关系和基准知识在设计时已知；本地方案先于本次指标计算，但不是外部预注册或Gorman原文完整复现。',
        '流程核验只证明交接结构与引用摘要一致；另行的独立程序复算仅覆盖本固定案例的数值，不等于同行评审。']
    analysis = {'unit': '逐条成鸟观测；两次时间留出分别描述，独立性未知不做总体推断。',
        'comparisons': '全部2个预定划分×3个条件；699条预测、6组模型及总指标、18组物种指标由独立标量/组内中心化实现复算。',
        'claims': claims, 'limitations': limitations, 'execution_records': numeric_logs,
        'numeric_validation_scope': 'case-specific independent recalculation; read logs/numeric.stdout.txt'}
    save(folder / 'analysis.json', analysis)
    return analysis, metrics, by_species


def write_report(folder, analysis, metrics, by_species):
    mapping = {'claims': analysis['claims'], 'limitations': analysis['limitations'],
               'review_status': 'template_generated', 'review_scope': '根据本次通过独立复算的结果和固定来源记录生成；没有外部同行评审或自动全文语义审查。'}
    save(folder / 'claims.json', mapping)
    mode = read(folder / 'evidence.json')['mode']
    lines = ['# 已知物种能否改善企鹅体重预测？', '',
        '真实公开数据教学比较。鳍长是翅膀状鳍肢的长度；MAE是预测体重与实测体重的平均绝对差，越小越好。', '',
        '## 方法', '',
        '主比较用2007–2008年223条观测训练，2009年119条观测测试。预定补充比较用2007年109条训练、2008年114条测试。年份表示简化CSV的季节标签。',
        '三条件为训练体重均值、鳍长普通最小二乘回归、鳍长加物种截距回归（共享斜率）。全部参数只在训练集拟合，x=(鳍长mm−200)/10是固定单位换算。没有调参或依据结果选择条件。',
        '均值条件回答“只知道平均体重怎样”；鳍长条件增加测量信息；物种条件还要求知道物种。详细方案见protocol.json，原始预测在results/predictions.csv。', '',
        '## 主要结果', ''] + ['- ' + c['text'] for c in analysis['claims']]
    lines += ['', '| 划分 | 条件 | 测试记录 | MAE（克） | RMSE（克） |', '|---|---|---:|---:|---:|']
    for m in metrics:
        lines.append(f"| {m['split']} | {m['condition']} | {m['n']} | {m['mae_g']:.1f} | {m['rmse_g']:.1f} |")
    lines += ['', '补充划分按原计划保留，无论它是否呈现与主划分相同的方向。下面按物种展开，以免总体均值遮住组内结果。', '',
              '| 划分 | 物种 | 条件 | 测试记录 | MAE（克） | RMSE（克） |', '|---|---|---|---:|---:|---:|']
    for m in by_species:
        lines.append(f"| {m['split']} | {m['species']} | {m['condition']} | {m['n']} | {m['mae_g']:.1f} | {m['rmse_g']:.1f} |")
    lines += ['', '## 解释和限制', '', '这些误差描述本次固定留出样本。群间差异可能提供预测信息，但没有分离性别、岛屿、年份等作用；不作因果解释。', ''] + ['- ' + x for x in analysis['limitations']]
    lines += ['', '## 来源与核验', '', f'本次evidence.mode={mode}；replay命令一律复用历史阅读记录，不会重新联网阅读。原始阅读范围和失败网址保留在evidence.json。']
    for source in read(folder / 'evidence.json')['sources']:
        lines.append(f"- {source['id']}（{source['status']}）：{source['url']}；{source['read_scope']}")
    lines += ['', '公开数据：Palmer Penguins / PAL-LTER，固定官方快照，CC0 1.0；保留来源作者与数据引用。',
              '独立数值检查见logs/numeric.stdout.txt；阶段记录见state.json/events.jsonl；报告主张定位见claims.json。',
              '这是结果模板和受限教学研究，不是可直接投稿的论文。下一步可在另一独立数据来源按新协议检验泛化；不能把本轮测试集继续用于挑模型。']
    (folder / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def run_pipeline(output, evidence):
    if sys.flags.optimize:
        raise ValueError('Run without -O')
    output = output.resolve()
    if output.exists() or output.is_relative_to(ROOT):
        raise ValueError('Choose a NEW output directory outside repository')
    # init creates the directory itself; capture it outside before moving its logs.
    result = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(RUNNER), 'init', '--topic',
        '加入物种信息，能否改善仅用鳍长预测企鹅体重的效果？', '--output', str(output)],
        cwd=ROOT, capture_output=True, text=True, encoding='utf-8', timeout=120)
    if result.returncode != 2:
        raise RuntimeError('Expected init to stop for missing scope: ' + result.stderr + result.stdout)
    (output / 'logs').mkdir()
    save(output / 'logs/init.json', {'exit_code': result.returncode, 'stdout': result.stdout.replace(str(output), '<run>'), 'stderr': result.stderr, 'recorded_at': now()})
    save(output / 'question.json', {'question': '加入物种信息，能否改善仅用鳍长预测企鹅体重的效果？',
         'scope': 'Palmer Penguins三个物种的固定时间留出、三种简单回归条件；教学延伸，不检验因果或新颖性。',
         'resources': '已取得固定公开CSV、两篇论文限定阅读和许可记录；本机CPU与Python标准库。',
         'stopping_condition': '完成固定2×3条件、独立核算及六步交接；程序120秒上限；缺数据或核验失败时保留日志并停止。'})
    invoke([RUNNER, 'advance', '--run', output], output, '01-question', 2)
    save(output / 'evidence.json', evidence)
    invoke([RUNNER, 'advance', '--run', output], output, '02-evidence', 2)
    (output / 'data').mkdir(); (output / 'code').mkdir()
    shutil.copyfile(CASE / 'data/penguins.csv', output / 'data/penguins.csv')
    for name in ('run_case.py', 'verify_case.py', 'replay.py'):
        shutil.copyfile(CASE / name, output / 'code' / name)
    protocol = read(CASE / 'protocol-template.json')
    protocol['frozen_at'] = now()
    protocol['data'] = [{'path': 'data/penguins.csv', 'sha256': digest(output / 'data/penguins.csv'), 'source_id': 'D1', 'license': 'CC0-1.0'}]
    protocol['code'] = [{'path': 'code/' + n, 'sha256': digest(output / 'code' / n)} for n in ('run_case.py', 'verify_case.py', 'replay.py')]
    save(output / 'protocol.json', protocol)
    invoke([RUNNER, 'advance', '--run', output], output, '03-protocol', 2)
    experiment_logs = invoke([output / 'code/run_case.py', '--run', output], output, 'experiment')
    save(output / 'experiment.json', {'status': 'measured', 'protocol_sha256': digest(output / 'protocol.json'),
         'command': 'python -B -X utf8 <run>/code/run_case.py --run <run>',
         'environment': 'Python ' + platform.python_version() + '; ' + platform.system() + '; CPU; standard library; offline',
         'artifacts': [{'id': p.stem, 'path': p.relative_to(output).as_posix(), 'sha256': digest(p)} for p in sorted((output / 'results').iterdir())],
         'failures': [], 'execution_records': experiment_logs})
    invoke([RUNNER, 'advance', '--run', output], output, '04-experiment', 2)
    numeric_logs = invoke([output / 'code/verify_case.py', '--run', output], output, 'numeric')
    analysis, metrics, by_species = report(output, numeric_logs)
    invoke([RUNNER, 'advance', '--run', output], output, '05-analysis', 2)
    write_report(output, analysis, metrics, by_species)
    invoke([RUNNER, 'advance', '--run', output], output, '06-report', 0)
    invoke([RUNNER, 'verify', '--run', output], output, '07-integrity', 0)
    print(json.dumps({'status': 'complete', 'mode': 'custom', 'evidence_mode': evidence['mode'], 'report': str(output / 'REPORT.md'),
                      'numeric_checks': read(output / 'logs/numeric.stdout.txt')}, ensure_ascii=False))
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    prior = read(CASE / 'sources.json')
    prior['mode'] = 'reused'
    prior['search_log'] = []
    prior['scope'] = 'Offline replay of 2026-10-23 reading records; no new searches or source retrieval. Original logs: examples/real-penguins/sources.json.'
    run_pipeline(args.output, prior)
