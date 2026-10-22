#!/usr/bin/env python3
"""Verify the teaching chain's artifacts, fixed case, document versions and optional renderer record."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
import run_workflow as workflow


def check(folder):
    if not folder.is_dir() or folder.is_symlink():
        raise ValueError('Expected a regular workflow directory')
    handoff = json.loads((folder / 'handoff.json').read_text(encoding='utf-8'))
    fields = {'schema_version', 'case_id', 'case_map_sha256', 'document_sha256', 'stage_manifest_sha256',
              'source_sha256', 'run_log_sha256', 'upstream_renderer_executed', 'renderer', 'writing_review_knowledge'}
    if not isinstance(handoff, dict) or set(handoff) != fields:
        raise ValueError('Unexpected workflow manifest fields')
    include = handoff.get('upstream_renderer_executed')
    if type(include) is not bool or type(handoff.get('schema_version')) is not int or handoff['schema_version'] != 1:
        raise ValueError('Invalid workflow schema or renderer flag')
    expected_names = {'experiment', 'analysis', 'figures', 'run-log.json', 'handoff.json'} | ({'pipeline.svg'} if include else set())
    if {p.name for p in folder.iterdir()} != expected_names or any(p.is_symlink() for p in folder.iterdir()):
        raise ValueError('Unexpected workflow files')
    case, hashes = workflow.documents()
    if handoff.get('case_id') != case['case_id'] or handoff.get('case_map_sha256') != workflow.digest(workflow.HERE / 'case-map.json'):
        raise ValueError('Case mapping differs')
    if handoff.get('document_sha256') != hashes:
        raise ValueError('Authored document versions differ; review the handoff again')
    if handoff.get('source_sha256') != {n: workflow.digest(workflow.HERE / n) for n in ['run_workflow.py', 'verify_workflow.py']}:
        raise ValueError('Workflow source version differs')
    if handoff.get('stage_manifest_sha256') != {n: workflow.digest(folder / n / 'manifest.json') for n in ['experiment', 'analysis', 'figures']}:
        raise ValueError('Stage manifest differs')
    if handoff.get('run_log_sha256') != workflow.digest(folder / 'run-log.json'):
        raise ValueError('Run log hash differs')
    logs = json.loads((folder / 'run-log.json').read_text(encoding='utf-8'))
    expected_steps = ['experiment', 'analysis', 'figures', 'figure verification'] + (['renderer validate', 'renderer render'] if include else [])
    if not isinstance(logs, list) or any(not isinstance(x, dict) or set(x) != {'step', 'exit_code', 'stdout', 'stderr'} for x in logs) or [x.get('step') for x in logs] != expected_steps or any(type(x.get('exit_code')) is not int or x['exit_code'] != 0 for x in logs):
        raise ValueError('Missing or failed workflow stage')
    if workflow.digest(folder / 'analysis/analysis.json') != case['expected_default_analysis_sha256']:
        raise ValueError('Analysis no longer matches the case documents')
    sys.path.insert(0, str(workflow.FIG))
    try:
        spec = importlib.util.spec_from_file_location('ars_teaching_figure_verifier', workflow.FIG / 'verify_figures.py')
        verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)
        verifier.check(folder / 'experiment', folder / 'analysis', folder / 'figures')
    finally:
        sys.path.pop(0)
    if include:
        workflow.check_renderer_pin()
        expected = {'renderer_sha256': workflow.digest(workflow.RENDERER), 'spec_sha256': workflow.digest(workflow.FIG / 'pipeline-spec.json'),
                    'svg_sha256': workflow.digest(folder / 'pipeline.svg')}
        if handoff.get('renderer') != expected or ET.parse(folder / 'pipeline.svg').getroot().tag != '{http://www.w3.org/2000/svg}svg':
            raise ValueError('Renderer record or SVG differs')
    elif handoff.get('renderer') != {}:
        raise ValueError('Unexpected renderer record')
    return handoff


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, required=True)
    a = p.parse_args()
    check(a.input)
    print('PASS: complete teaching artifact chain and authored document versions checked. Scientific interpretation and external workflows remain separate.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        print('Workflow verification failed: ' + str(exc), file=sys.stderr)
        sys.exit(1)
