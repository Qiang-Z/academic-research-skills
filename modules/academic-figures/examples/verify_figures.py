#!/usr/bin/env python3
"""Verify original teaching plot artifacts and their input provenance."""
import argparse
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
import plot_results as plot

NAMES = {'comparison.svg', 'comparison.pdf', 'comparison.png', 'plotted-data.json', 'caption.md', 'manifest.json'}


def check(experiment, analysis, output):
    if output.is_symlink() or not output.is_dir() or {p.name for p in output.iterdir()} != NAMES:
        raise ValueError('Unexpected figure file set or directory')
    if any(not p.is_file() or p.is_symlink() for p in output.iterdir()):
        raise ValueError('Expected regular figure files')
    source = plot.verified_analysis(experiment, analysis)
    manifest = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
    expected = {n: plot.digest(output / n) for n in NAMES - {'manifest.json'}}
    fields = {'schema_version', 'artifact_sha256', 'input_manifest_sha256', 'source_sha256', 'environment', 'upstream_skill_executed'}
    if not isinstance(manifest, dict) or set(manifest) != fields or type(manifest.get('schema_version')) is not int or manifest['schema_version'] != 1 or manifest.get('artifact_sha256') != expected:
        raise ValueError('Figure hashes or schema differ')
    environment = manifest.get('environment')
    if not isinstance(environment, dict) or set(environment) != {'python', 'platform', 'matplotlib', 'numpy'} or not all(isinstance(v, str) and v for v in environment.values()) or manifest.get('upstream_skill_executed') is not False:
        raise ValueError('Figure environment or execution status differs')
    if manifest.get('source_sha256') != {'plot_results.py': plot.digest(plot.HERE / 'plot_results.py')}:
        raise ValueError('Figure source version differs')
    if manifest.get('input_manifest_sha256') != {'experiment': plot.digest(experiment / 'manifest.json'),
                                                'analysis': plot.digest(analysis / 'manifest.json')}:
        raise ValueError('Input provenance differs')
    expected_data = {'descriptive_test_rows': [r for r in source['descriptive_rows'] if r['evaluation_split'] == 'test'],
                     'paired_bootstrap': source['paired_bootstrap'], 'analysis_status': source['analysis_status'],
                     'interpretation_limits': source['interpretation_limits']}
    if (output / 'plotted-data.json').read_bytes() != plot.json_bytes(expected_data):
        raise ValueError('Plotted values differ from verified analysis')
    svg = ET.parse(output / 'comparison.svg').getroot()
    if svg.tag != '{http://www.w3.org/2000/svg}svg':
        raise ValueError('Invalid SVG root')
    if not (output / 'comparison.pdf').read_bytes().startswith(b'%PDF-'):
        raise ValueError('Invalid PDF header')
    if not (output / 'comparison.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('Invalid PNG header')
    return manifest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--experiment', type=Path, required=True)
    p.add_argument('--analysis', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--compare', type=Path)
    a = p.parse_args()
    check(a.experiment, a.analysis, a.output)
    if a.compare:
        if a.compare.resolve() == a.output.resolve():
            raise ValueError('Comparison must use a different output directory')
        check(a.experiment, a.analysis, a.compare)
        for n in NAMES - {'manifest.json'}:
            if (a.output / n).read_bytes() != (a.compare / n).read_bytes():
                raise ValueError('Figure rerun differs: ' + n)
    print('PASS: figure provenance, hashes, plotted data and file formats; visual/scientific review is separate.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, ET.ParseError) as exc:
        print('Figure verification failed: ' + str(exc), file=sys.stderr)
        sys.exit(1)
