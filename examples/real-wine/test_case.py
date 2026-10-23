#!/usr/bin/env python3
"""Replay the Wine case and probe changed predictions, leakage, bad data and missing results."""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import statistics
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True, help='New external directory for temporary fixtures and test record')
    a = p.parse_args(); a.run = a.run.resolve(); a.output = a.output.resolve()
    if a.output.exists() or a.output.is_relative_to(ROOT):
        raise ValueError('Choose a new test directory outside the repository')
    a.output.mkdir(parents=True)
    before = {p.relative_to(a.run).as_posix(): digest(p) for p in a.run.rglob('*') if p.is_file()}
    logs = []

    def invoke(label, script, arguments, expected, fragment=None):
        result = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(script), *map(str, arguments)],
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1'),
                                capture_output=True, text=True, encoding='utf-8', timeout=90)
        def redact(text):
            for x, alias in [(str(a.run), '$RUN_DIR'), (str(a.output), '$TEST_DIR'), (str(ROOT), '$REPOSITORY')]:
                text = text.replace(x.replace('\\', '\\\\'), alias).replace(x, alias).replace(x.replace('\\', '/'), alias)
            return text.strip()
        ok = result.returncode == expected and (fragment is None or fragment in result.stdout+result.stderr)
        logs.append({'case': label, 'script': script.name, 'arguments': [redact(str(v)) for v in arguments],
                     'expected_exit': expected, 'exit_code': result.returncode, 'stdout': redact(result.stdout),
                     'stderr': redact(result.stderr), 'passed': ok})
        if not ok:
            raise ValueError('Unexpected result: ' + label + ' ' + redact(result.stderr))

    invoke('original_semantic_verification', HERE/'verify_case.py', ['--input', a.run], 0, 'PASS')
    second = a.output/'repeat'
    invoke('second_actual_run', HERE/'run_case.py', ['--output', second], 0, 'PASS')
    invoke('second_semantic_verification', HERE/'verify_case.py', ['--input', second], 0, 'PASS')
    deterministic = ['data-audit.json', 'splits.json', 'scalers.json', 'predictions.csv', 'metrics.json', 'paired-analysis.json', 'results.md']
    assert all((a.run/n).read_bytes() == (second/n).read_bytes() for n in deterministic)
    logs.append({'case': 'repeatable_scientific_artifacts', 'passed': True, 'files': deterministic,
                 'excluded': ['run.json elapsed time', 'manifest.json containing run.json digest', 'optional figures not rerendered']})

    def bad_copy(name):
        folder = a.output/name
        shutil.copytree(second, folder)
        return folder

    def update_artifact(folder, name):
        path = folder/'manifest.json'; obj = json.loads(path.read_text(encoding='utf-8'))
        obj['artifact_sha256'][name] = digest(folder/name)
        path.write_bytes((json.dumps(obj, sort_keys=True, indent=2)+'\n').encode())

    damaged = bad_copy('wrong_prediction')
    rows = list(csv.DictReader((damaged/'predictions.csv').read_text().splitlines()))
    # Change an actual prediction and refresh its digest: force semantic verification beyond hashing.
    rows[0]['y_pred'] = str(int(rows[0]['y_pred']) % 3 + 1)
    out = io.StringIO(newline=''); writer = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader(); writer.writerows(rows)
    (damaged/'predictions.csv').write_bytes(out.getvalue().encode()); update_artifact(damaged, 'predictions.csv')
    invoke('changed_prediction_with_refreshed_hash', HERE/'verify_case.py', ['--input', damaged], 1, 'Prediction does not match independent calculation')

    leaked = bad_copy('all_data_scaler')
    scalers = json.loads((leaked/'scalers.json').read_text())
    data = [list(map(float, r)) for r in csv.reader((HERE/'data/wine.data').read_text().splitlines())]
    # Keep claimed fit IDs unchanged while replacing actual parameters with a leaking all-row fit.
    scalers[0]['mean'] = [statistics.fmean(r[j] for r in data) for j in range(1, 14)]
    scalers[0]['scale_ddof0'] = [statistics.pstdev(r[j] for r in data) for j in range(1, 14)]
    (leaked/'scalers.json').write_bytes((json.dumps(scalers, sort_keys=True, indent=2)+'\n').encode())
    update_artifact(leaked, 'scalers.json')
    invoke('all_data_scaling_with_refreshed_hash', HERE/'verify_case.py', ['--input', leaked], 1, 'Mean mismatch')

    mirror = a.output/'mirror/examples/real-wine'; mirror.mkdir(parents=True)
    for name in ['run_case.py', 'verify_case.py', 'protocol.json', 'DATA_SOURCE.json', 'sources.json', 'data/wine.data', 'data/wine.names']:
        (mirror/name).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(HERE/name, mirror/name)
    path = mirror/'data/wine.data'; blob = path.read_bytes(); path.write_bytes(blob.replace(b'14.23', b'14.24', 1))
    assert path.read_bytes() != blob
    invoke('altered_dataset', mirror/'run_case.py', ['--output', a.output/'should_not_exist'], 1, 'Dataset SHA-256 mismatch')
    assert not (a.output/'should_not_exist').exists()
    invoke('existing_output_rejected', HERE/'run_case.py', ['--output', a.run], 1, 'Output exists')
    invoke('missing_results_rejected', HERE/'verify_case.py', ['--input', a.output/'missing'], 1, 'Wine verification failed')

    numpy_result = {'state': 'not_run', 'reason': 'NumPy optional; not a core runtime dependency'}
    try:
        import numpy as np
    except ImportError:
        pass
    else:
        # Third numeric path: vectorized matrix distances and independent voting.
        all_x, all_y = np.array([r[1:] for r in data]), np.array([int(r[0]) for r in data])
        predictions = list(csv.DictReader((a.run/'predictions.csv').read_text().splitlines()))
        n = 0
        for split in json.loads((a.run/'splits.json').read_text()):
            train = np.array(split['train_ids'])-1; test = np.array(split['test_ids'])-1
            for condition in ['raw_5nn', 'zscore_train_5nn']:
                scale = all_x[train].std(axis=0, ddof=0) if condition.startswith('zscore') else np.ones(13)
                distance = (((all_x[test, None, :]-all_x[train][None, :, :])/scale)**2).sum(axis=2)
                for row, sample in zip(distance, test):
                    nearest = np.lexsort((train, row))[:5]
                    label = int(np.argmax(np.bincount(all_y[train[nearest]], minlength=4)))
                    original = next(r for r in predictions if int(r['seed']) == split['seed'] and r['condition'] == condition and int(r['row_id']) == sample+1)
                    assert int(original['y_pred']) == label; n += 1
        numpy_result = {'state': 'pass', 'numpy': np.__version__, 'prediction_records': n, 'scope': 'two kNN conditions, six fixed splits; no sklearn implementation invoked'}
    after = {p.relative_to(a.run).as_posix(): digest(p) for p in a.run.rglob('*') if p.is_file()}
    assert before == after
    result = {'date': '2026-10-23', 'tests': logs, 'numpy_cross_check': numpy_result,
              'original_artifacts_unchanged': before == after, 'test_source_sha256': digest(Path(__file__)),
              'source_sha256': {n: digest(HERE/n) for n in ['run_case.py', 'verify_case.py', 'protocol.json']},
              'scope': 'Same-author programs and controlled corruptions; not external scientific review or arbitrary dataset support.'}
    (a.output/'checks.json').write_bytes((json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)+'\n').encode())
    print('PASS: ' + str(len(logs)) + ' recorded checks; original run unchanged. NumPy: ' + numpy_result['state'])


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, AssertionError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print('Wine tests failed: ' + str(exc), file=sys.stderr); sys.exit(1)
