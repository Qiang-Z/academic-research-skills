#!/usr/bin/env python3
"""Offline UCI Wine experiment. Standard library; write only to a new external directory."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import platform
import random
import statistics
import sys
import time
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL_SHA256 = 'db7bc2257afa38c6b547ba02b2918ebf078744d1ed9d2043eee635190f26ca75'
DATA_SHA256 = '6be6b1203f3d51df0b553a70e57b8a723cd405683958204f96d23d7cd6aea659'
CONDITIONS = ['majority_train', 'raw_5nn', 'zscore_train_5nn']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, obj):
    path.write_bytes((json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8'))


def load_data(path):
    if sha(path) != DATA_SHA256:
        raise ValueError('Dataset SHA-256 mismatch; use the documented UCI Wine snapshot, not Wine Quality.')
    rows = []
    for i, row in enumerate(csv.reader(io.StringIO(path.read_text(encoding='utf-8'))), 1):
        if len(row) != 14:
            raise ValueError('Expected class plus 13 features at row ' + str(i))
        label, x = int(row[0]), list(map(float, row[1:]))
        if label not in (1, 2, 3) or not all(math.isfinite(v) for v in x):
            raise ValueError('Invalid label or non-finite feature')
        rows.append({'id': i, 'y': label, 'x': x})
    if len(rows) != 178 or Counter(r['y'] for r in rows) != {1: 59, 2: 71, 3: 48}:
        raise ValueError('Unexpected dataset population')
    return rows


def partition(rows, seed):
    rng, train, test = random.Random(seed), [], []
    for label in (1, 2, 3):
        ids = [r['id'] for r in rows if r['y'] == label]
        rng.shuffle(ids)
        size = math.ceil(len(ids) * .25)
        test.extend(ids[:size])
        train.extend(ids[size:])
    return sorted(train), sorted(test)


def predict(train, sample, scale):
    distances = [(sum(((a-b)/s)**2 for a, b, s in zip(sample['x'], r['x'], scale)), r['id'], r['y']) for r in train]
    neighbors = sorted(distances)[:5]
    votes = Counter(n[2] for n in neighbors)
    label = min(votes, key=lambda c: (-votes[c], c))
    return label, [n[1] for n in neighbors]


def metric(truth, predicted):
    confusion = [[sum(a == i and b == j for a, b in zip(truth, predicted)) for j in (1, 2, 3)] for i in (1, 2, 3)]
    correct = sum(a == b for a, b in zip(truth, predicted))
    return {'n': len(truth), 'correct': correct, 'accuracy': correct/len(truth),
            'balanced_accuracy': statistics.fmean(confusion[i][i]/sum(confusion[i]) for i in range(3)),
            'confusion_matrix': confusion, 'class_order': [1, 2, 3]}


def paired_interval(records, protocol):
    by_id = {}
    for r in records:
        if r['seed'] == protocol['primary_seed']:
            by_id.setdefault(r['row_id'], {})[r['condition']] = r
    groups, pairs = {i: [] for i in (1, 2, 3)}, []
    counts = Counter()
    for row_id, values in sorted(by_id.items()):
        a, b = values['raw_5nn'], values['zscore_train_5nn']
        raw, scaled = int(a['y_true'] == a['y_pred']), int(b['y_true'] == b['y_pred'])
        counts['both_correct' if raw and scaled else 'gained' if scaled else 'lost' if raw else 'both_wrong'] += 1
        groups[a['y_true']].append(scaled-raw)
        pairs.append({'row_id': row_id, 'label': a['y_true'], 'raw_correct': raw, 'scaled_correct': scaled})
    rng, differences = random.Random(protocol['interval']['seed']), []
    for _ in range(protocol['interval']['resamples']):
        differences.append(sum(rng.choice(g) for g in groups.values() for _ in g))
    ordered = sorted(differences)
    def quantile(q):
        pos = (len(ordered)-1)*q
        lo, hi = math.floor(pos), math.ceil(pos)
        return (ordered[lo]*(hi-pos) + ordered[hi]*(pos-lo) if lo != hi else ordered[lo])/len(pairs)*100
    return {'seed': protocol['primary_seed'], 'n_pairs': len(pairs),
            'paired_counts': {k: counts[k] for k in ['gained', 'lost', 'both_correct', 'both_wrong']},
            'difference_pp': sum(b['scaled_correct']-b['raw_correct'] for b in pairs)/len(pairs)*100,
            'interval_pp': [quantile(.025), quantile(.975)], 'method': protocol['interval'], 'pairs': pairs,
            'bootstrap_net_correct_histogram': [{'net_correct': k, 'count': v} for k, v in sorted(Counter(differences).items())]}


def run(output):
    started = time.perf_counter()
    if output.exists() or output.is_symlink():
        raise ValueError('Output exists; choose a NEW directory. Existing results are never overwritten.')
    output = output.resolve()
    if output.is_relative_to(ROOT):
        raise ValueError('Keep generated runs outside the repository; choose a new directory under TEMP.')
    protocol_path = HERE/'protocol.json'
    if sha(protocol_path) != PROTOCOL_SHA256:
        raise ValueError('Protocol changed; retain the frozen version and explicitly version a new study.')
    protocol = json.loads(protocol_path.read_text(encoding='utf-8'))
    inputs = {n: sha(HERE/n) for n in ['protocol.json', 'DATA_SOURCE.json', 'data/wine.data', 'data/wine.names', 'sources.json']}
    source_hashes = {n: sha(HERE/n) for n in ['run_case.py', 'verify_case.py']}
    rows = load_data(HERE/'data/wine.data')
    index = {r['id']: r for r in rows}
    output.mkdir(parents=True, exist_ok=False)
    splits, scalers, records, metrics = [], [], [], []
    for seed in [protocol['primary_seed'], *protocol['supplementary_seeds']]:
        train_ids, test_ids = partition(rows, seed)
        train, test = [index[i] for i in train_ids], [index[i] for i in test_ids]
        mean = [statistics.fmean(r['x'][j] for r in train) for j in range(13)]
        scale = [statistics.pstdev(r['x'][j] for r in train) or 1. for j in range(13)]
        majority = min((1, 2, 3), key=lambda c: (-sum(r['y'] == c for r in train), c))
        splits.append({'seed': seed, 'train_ids': train_ids, 'test_ids': test_ids,
                       'train_counts': dict(Counter(r['y'] for r in train)), 'test_counts': dict(Counter(r['y'] for r in test))})
        scalers.append({'seed': seed, 'fit_ids': train_ids, 'mean': mean, 'scale_ddof0': scale})
        for condition in CONDITIONS:
            predicted = []
            for sample in test:
                if condition == 'majority_train':
                    label, neighbors = majority, []
                else:
                    label, neighbors = predict(train, sample, scale if condition == 'zscore_train_5nn' else [1.]*13)
                predicted.append(label)
                records.append({'seed': seed, 'condition': condition, 'row_id': sample['id'], 'y_true': sample['y'],
                                'y_pred': label, 'neighbor_ids': json.dumps(neighbors)})
            metrics.append({'seed': seed, 'condition': condition, **metric([r['y'] for r in test], predicted)})
    audit = {'rows': len(rows), 'features': 13, 'class_counts': dict(Counter(r['y'] for r in rows)),
             'missing_or_nonfinite': 0, 'duplicate_feature_vectors': len(rows)-len({tuple(r['x']) for r in rows}),
             'target': 'cultivar class; NOT wine quality, geographic region, or chemical causation',
             'group_information': 'no harvest/vineyard/batch/group IDs available in the supplied file; row splitting cannot rule out group dependence'}
    for n, obj in [('data-audit.json', audit), ('splits.json', splits), ('scalers.json', scalers), ('metrics.json', metrics), ('paired-analysis.json', paired_interval(records, protocol))]:
        save_json(output/n, obj)
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=list(records[0]), lineterminator='\n')
    writer.writeheader(); writer.writerows(records)
    (output/'predictions.csv').write_bytes(stream.getvalue().encode('utf-8'))
    pair = json.loads((output/'paired-analysis.json').read_text(encoding='utf-8'))
    lines = ['# UCI Wine: measured results', '', 'Real public dataset; fixed design; no tuning on test outcomes.', '',
             '| split seed | condition | correct / n | accuracy | balanced accuracy |', '|---|---|---:|---:|---:|']
    for m in metrics:
        lines.append(f"| {m['seed']} | {m['condition']} | {m['correct']}/{m['n']} | {m['accuracy']:.4%} | {m['balanced_accuracy']:.4%} |")
    lines += ['', f"Primary paired difference: {pair['difference_pp']:.4f} percentage points; stratified 95% percentile interval {pair['interval_pp']}.",
              '', 'Interval conditional on primary fitted models and empirical class proportions; 10,000 class-stratified paired resamples.',
              'Six splits reuse 178 rows. Never pool their 810 prediction records as independent samples. No cross-dataset or future-vintage conclusion.',
              'The benchmark and scaling motivation were already public; this is a new execution of an established comparison, not a novel algorithm or a full reproduction of a cited paper.',
              '', 'Data: https://archive.ics.uci.edu/dataset/109/wine ; DOI: 10.24432/C5PC7J ; CC BY 4.0.',
              'Reading record and bounded interpretation: sources.json and REPORT.md in the repository case directory.']
    (output/'results.md').write_bytes(('\n'.join(lines)+'\n').encode())
    save_json(output/'run.json', {'python': platform.python_version(), 'platform': platform.system(), 'mode': 'measured, local CPU, offline',
                               'elapsed_seconds': round(time.perf_counter()-started, 6), 'protocol_sha256': PROTOCOL_SHA256})
    artifacts = {p.name: sha(p) for p in sorted(output.iterdir()) if p.is_file()}
    if any(sha(HERE/n) != h for n, h in inputs.items()) or any(sha(HERE/n) != h for n, h in source_hashes.items()):
        raise ValueError('Inputs or source code changed during execution')
    save_json(output/'manifest.json', {'schema_version': 1, 'study_id': protocol['study_id'], 'input_sha256': inputs,
                                     'source_sha256': source_hashes, 'artifact_sha256': artifacts})
    print('PASS: measured Wine experiment; 178 rows, six splits, 18 conditions, 810 prediction records.')
    print('Primary difference (pp): ' + str(pair['difference_pp']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        run(args.output)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('Wine case failed: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
