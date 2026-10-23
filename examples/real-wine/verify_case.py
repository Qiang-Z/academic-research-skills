#!/usr/bin/env python3
"""Independently recalculate Wine predictions and data separation; no runner imports."""
import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check(folder):
    manifest = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    for key, base in [('input_sha256', HERE), ('source_sha256', HERE), ('artifact_sha256', folder)]:
        for name, expected in manifest[key].items():
            p = base/name
            if not p.resolve().is_relative_to(base.resolve()) or p.is_symlink() or sha(p) != expected:
                raise ValueError('Hash or path mismatch: ' + name)
    data = [list(map(float, r)) for r in csv.reader((HERE/'data/wine.data').read_text(encoding='utf-8').splitlines())]
    assert len(data) == 178 and all(len(r) == 14 for r in data)
    protocol = json.loads((HERE/'protocol.json').read_text(encoding='utf-8'))
    predictions = list(csv.DictReader((folder/'predictions.csv').read_text(encoding='utf-8').splitlines()))
    assert len(predictions) == 810
    splits = json.loads((folder/'splits.json').read_text(encoding='utf-8'))
    scalers = json.loads((folder/'scalers.json').read_text(encoding='utf-8'))
    metrics = json.loads((folder/'metrics.json').read_text(encoding='utf-8'))
    assert [x['seed'] for x in splits] == [protocol['primary_seed'], *protocol['supplementary_seeds']]
    assert len(metrics) == 18 and len(scalers) == 6
    for split, scaler in zip(splits, scalers):
        seed = split['seed']; train_ids, test_ids = split['train_ids'], split['test_ids']
        assert len(train_ids) == 133 and len(test_ids) == 45
        assert set(train_ids).isdisjoint(test_ids) and sorted(train_ids+test_ids) == list(range(1, 179))
        rng, expected_test = random.Random(seed), []
        for c in (1, 2, 3):
            ids = [i+1 for i, r in enumerate(data) if r[0] == c]; rng.shuffle(ids)
            expected_test.extend(ids[:math.ceil(.25*len(ids))])
        assert test_ids == sorted(expected_test), 'Partition does not match fixed protocol'
        assert scaler['fit_ids'] == train_ids and scaler['seed'] == seed, 'Scaler fitted on wrong rows'
        means = [sum(data[i-1][j] for i in train_ids)/len(train_ids) for j in range(1, 14)]
        sigmas = [math.sqrt(sum((data[i-1][j]-means[j-1])**2 for i in train_ids)/len(train_ids)) or 1. for j in range(1, 14)]
        for j in range(13):
            assert math.isclose(means[j], scaler['mean'][j], rel_tol=1e-12, abs_tol=1e-9), 'Mean mismatch'
            assert math.isclose(sigmas[j], scaler['scale_ddof0'][j], rel_tol=1e-12, abs_tol=1e-9), 'Scale mismatch'
        majority = Counter(int(data[i-1][0]) for i in train_ids)
        for condition in ['majority_train', 'raw_5nn', 'zscore_train_5nn']:
            group = [r for r in predictions if int(r['seed']) == seed and r['condition'] == condition]
            assert [int(r['row_id']) for r in group] == test_ids
            for r in group:
                item = int(r['row_id']); truth = int(data[item-1][0])
                if condition == 'majority_train':
                    expected = sorted(majority, key=lambda c: (-majority[c], c))[0]; ids = []
                else:
                    scales = sigmas if condition.startswith('zscore') else [1.]*13
                    # Transform first, then calculate distance; the runner uses direct scaled differences.
                    query = [(x-m)/s for x, m, s in zip(data[item-1][1:], means, scales)]
                    candidates = []
                    for i in train_ids:
                        x = [(v-m)/s for v, m, s in zip(data[i-1][1:], means, scales)]
                        candidates.append((math.fsum((a-b)**2 for a, b in zip(query, x)), i))
                    ids = [i for _, i in sorted(candidates)[:5]]
                    votes = Counter(int(data[i-1][0]) for i in ids)
                    expected = sorted(votes, key=lambda c: (-votes[c], c))[0]
                assert int(r['y_true']) == truth, 'Wrong ground truth'
                assert int(r['y_pred']) == expected, 'Prediction does not match independent calculation'
                assert json.loads(r['neighbor_ids']) == ids, 'Incorrect neighbor IDs'
            observed = next(m for m in metrics if m['seed'] == seed and m['condition'] == condition)
            cm = [[sum(int(r['y_true']) == a and int(r['y_pred']) == b for r in group) for b in (1, 2, 3)] for a in (1, 2, 3)]
            correct = sum(cm[i][i] for i in range(3))
            assert observed['correct'] == correct and observed['n'] == 45
            assert observed['confusion_matrix'] == cm
            assert math.isclose(observed['accuracy'], correct/45)
            assert math.isclose(observed['balanced_accuracy'], sum(cm[i][i]/sum(cm[i]) for i in range(3))/3)
    paired = json.loads((folder/'paired-analysis.json').read_text(encoding='utf-8'))
    primary = [r for r in predictions if int(r['seed']) == protocol['primary_seed']]
    by_condition = {c: {int(r['row_id']): r for r in primary if r['condition'] == c} for c in ['raw_5nn', 'zscore_train_5nn']}
    expected_pairs, gains, losses = [], 0, 0
    strata = {c: [] for c in (1, 2, 3)}
    for i, r in sorted(by_condition['raw_5nn'].items()):
        other = by_condition['zscore_train_5nn'][i]
        a, b = int(r['y_true'] == r['y_pred']), int(other['y_true'] == other['y_pred'])
        gains += b > a; losses += a > b; strata[int(r['y_true'])].append(b-a)
        expected_pairs.append({'row_id': i, 'label': int(r['y_true']), 'raw_correct': a, 'scaled_correct': b})
    assert paired['pairs'] == expected_pairs and paired['n_pairs'] == 45
    expected_counts = {'gained': gains, 'lost': losses,
                       'both_correct': sum(r['raw_correct'] and r['scaled_correct'] for r in expected_pairs),
                       'both_wrong': sum(not r['raw_correct'] and not r['scaled_correct'] for r in expected_pairs)}
    assert paired['paired_counts'] == expected_counts
    assert math.isclose(paired['difference_pp'], (gains-losses)/45*100)
    rng = random.Random(731); hist = Counter()
    for _ in range(10000):
        hist[sum(g[rng.randrange(len(g))] for g in strata.values() for _ in range(len(g)))] += 1
    assert paired['bootstrap_net_correct_histogram'] == [{'net_correct': k, 'count': v} for k, v in sorted(hist.items())]
    ordered = sorted(k for k, v in hist.items() for _ in range(v))
    expected_ci = []
    for q in [.025, .975]:
        p = q*9999; lo = int(p); f = p-lo
        expected_ci.append((ordered[lo]*(1-f) + ordered[min(lo+1, 9999)]*f)/45*100)
    assert all(math.isclose(a, b) for a, b in zip(paired['interval_pp'], expected_ci)), 'Interval mismatch'
    return {'prediction_records': 810, 'groups': 18, 'pairing': expected_counts, 'difference_pp': paired['difference_pp']}


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--input', type=Path, required=True)
    a = p.parse_args()
    try:
        result = check(a.input)
        print('PASS: independent prediction, train-only scaling, metrics and paired interval checks: ' + json.dumps(result))
        return 0
    except (OSError, ValueError, AssertionError, KeyError, TypeError, StopIteration) as exc:
        print('Wine verification failed: ' + str(exc), file=sys.stderr); return 1


if __name__ == '__main__':
    sys.exit(main())
