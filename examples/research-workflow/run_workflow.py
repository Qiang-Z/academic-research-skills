#!/usr/bin/env python3
"""Run the original teaching experiment, analysis and figures; index the authored handoff documents."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXP = ROOT / 'modules/experiment-design/examples/toy-reproducibility'
ANA = ROOT / 'modules/data-analysis/examples/paired-analysis'
FIG = ROOT / 'modules/academic-figures/examples'
RENDERER = ROOT / 'modules/idea-discovery/01_ARIS/upstream/skills/figure-spec/scripts/figure_renderer.py'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def documents():
    case = json.loads((HERE / 'case-map.json').read_text(encoding='utf-8'))
    hashes = {}
    for name in case['documents']:
        path = ROOT / name
        if not path.resolve().is_relative_to(ROOT.resolve()) or not path.is_file() or path.is_symlink():
            raise ValueError('Missing or unsafe handoff document: ' + name)
        hashes[name] = digest(path)
    return case, hashes


def check_renderer_pin():
    source = json.loads((ROOT / 'modules/academic-figures/SOURCE_MANIFEST.json').read_text(encoding='utf-8'))['sources'][0]
    expected = next(f['sha256'] for f in source['files'] if f['path'] == 'skills/figure-spec/scripts/figure_renderer.py')
    if digest(RENDERER) != expected:
        raise ValueError('Pinned renderer source hash differs')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True, help='New output directory; no overwrite')
    p.add_argument('--include-renderer', action='store_true', help='Also execute the pinned, reviewed ARIS SVG helper only')
    a = p.parse_args()
    if a.output.is_symlink():
        raise ValueError('Output must not be a symbolic link')
    a.output = a.output.resolve()
    if a.output.exists() or a.output.is_symlink():
        raise ValueError('Output already exists; choose a new directory')
    if a.output.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('Keep generated research artifacts outside this curated repository')
    if importlib.util.find_spec('matplotlib') is None:
        raise ValueError('Matplotlib is missing; prepare the isolated environment described in README')
    case, doc_hashes = documents()
    if a.include_renderer:
        check_renderer_pin()
    a.output.mkdir(parents=True, exist_ok=False)
    logs = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')

    def run(label, arguments):
        r = subprocess.run([sys.executable, '-B', '-X', 'utf8', *map(str, arguments)],
                           cwd=a.output, env=env, capture_output=True, text=True, encoding='utf-8', timeout=180)
        logs.append({'step': label, 'exit_code': r.returncode, 'stdout': r.stdout.strip(), 'stderr': r.stderr.strip()})
        (a.output / 'run-log.json').write_bytes(encode(logs))
        if r.returncode:
            raise ValueError(label + ' failed; see run-log.json. Partial output retained.')
        print(label + ': PASS', flush=True)

    run('experiment', [EXP / 'run_demo.py', '--output', a.output / 'experiment'])
    run('analysis', [ANA / 'analyze_demo.py', '--input', a.output / 'experiment', '--output', a.output / 'analysis'])
    if digest(a.output / 'analysis/analysis.json') != case['expected_default_analysis_sha256']:
        raise ValueError('Computed analysis no longer matches the authored teaching documents; revise them before handoff')
    run('figures', [FIG / 'plot_results.py', '--experiment', a.output / 'experiment', '--analysis', a.output / 'analysis', '--output', a.output / 'figures'])
    run('figure verification', [FIG / 'verify_figures.py', '--experiment', a.output / 'experiment', '--analysis', a.output / 'analysis', '--output', a.output / 'figures'])
    optional = {}
    if a.include_renderer:
        run('renderer validate', [RENDERER, 'validate', FIG / 'pipeline-spec.json'])
        run('renderer render', [RENDERER, 'render', FIG / 'pipeline-spec.json', '--output', a.output / 'pipeline.svg'])
        optional = {'renderer_sha256': digest(RENDERER), 'spec_sha256': digest(FIG / 'pipeline-spec.json'),
                    'svg_sha256': digest(a.output / 'pipeline.svg')}
    _, final_doc_hashes = documents()
    if final_doc_hashes != doc_hashes:
        raise ValueError('Handoff documents changed during this run')
    handoff = {'schema_version': 1, 'case_id': case['case_id'], 'case_map_sha256': digest(HERE / 'case-map.json'),
               'document_sha256': doc_hashes, 'stage_manifest_sha256': {n: digest(a.output / n / 'manifest.json') for n in ['experiment', 'analysis', 'figures']},
               'source_sha256': {n: digest(HERE / n) for n in ['run_workflow.py', 'verify_workflow.py']},
               'run_log_sha256': digest(a.output / 'run-log.json'), 'upstream_renderer_executed': a.include_renderer,
               'renderer': optional, 'writing_review_knowledge': 'pre-authored teaching documents, not live agent or external service execution'}
    (a.output / 'handoff.json').write_bytes(encode(handoff))
    print('Teaching chain completed. Authored documents indexed; no real peer review, Zotero sync or submission performed.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print('Workflow failed: ' + str(exc), file=sys.stderr)
        sys.exit(1)
