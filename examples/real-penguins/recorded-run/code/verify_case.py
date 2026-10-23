#!/usr/bin/env python3
"""Independent, standard-library numerical audit of this fixed Penguins case.

No experiment-runner imports: scalar covariance and within-species centering
reconstruct the regressions independently of the runner's matrix solver.
This verifies recorded predictions, coefficients and descriptive metrics. It
does not establish independent sampling, causality or external generalization.
"""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import sys


DATA_SHA256 = 'f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93'
SPECIES = ['Adelie', 'Chinstrap', 'Gentoo']
CONDITIONS = ['mean_baseline', 'flipper_ols', 'flipper_species_ols']
SPLITS = [
    {'id': 'primary', 'train_years': [2007, 2008], 'test_year': 2009},
    {'id': 'secondary', 'train_years': [2007], 'test_year': 2008},
]
CONFIG = {
    'data_sha256': DATA_SHA256,
    'raw_rows': 344,
    'usable_rows': 342,
    'excluded_record_ids': [4, 272],
    'missing_policy': 'drop_only_missing_flipper_or_body',
    'species_order': SPECIES,
    'flipper_center_mm': 200.0,
    'flipper_scale_mm': 10.0,
    'splits': SPLITS,
    'conditions': CONDITIONS,
}
FEATURE_NAMES = {
    'mean_baseline': ['intercept'],
    'flipper_ols': ['intercept', 'flipper_10mm'],
    'flipper_species_ols': ['intercept', 'flipper_10mm', 'Chinstrap', 'Gentoo'],
}
PREDICTION_FIELDS = ['split', 'condition', 'record_id', 'year', 'species',
                     'observed_g', 'predicted_g']


class Audit:
    def __init__(self):
        self.checks = 0

    def require(self, condition, message):
        self.checks += 1
        if not condition:
            raise ValueError(message)

    def close(self, observed, expected, message):
        self.require(type(observed) in (int, float) and math.isfinite(observed),
                     message + ': expected a finite number')
        self.require(math.isclose(observed, expected, rel_tol=1e-11, abs_tol=1e-7),
                     message + ': numeric mismatch')


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def local_file(run, name):
    path = run / name
    if not path.resolve().is_relative_to(run.resolve()):
        raise ValueError('Input escapes run directory: ' + name)
    current = path
    while current != run:
        if current.is_symlink():
            raise ValueError('Symbolic link input: ' + name)
        current = current.parent
    if not path.is_file():
        raise ValueError('Missing input file: ' + name)
    return path


def read_json(run, name):
    return json.loads(local_file(run, name).read_text(encoding='utf-8'),
                      object_pairs_hook=no_duplicate_keys)


def keyed(items, fields, audit, label):
    audit.require(isinstance(items, list), label + ': expected a list')
    result = {}
    for item in items:
        audit.require(isinstance(item, dict), label + ': expected an object')
        key = tuple(item[field] for field in fields)
        audit.require(key not in result, label + ': duplicate record ' + str(key))
        result[key] = item
    return result


def mean(values):
    return math.fsum(values) / len(values)


def coefficients(train, condition):
    """Closed forms, independent of the experiment's normal equations solver."""
    if condition == 'mean_baseline':
        return [mean([r['y'] for r in train])]
    if condition == 'flipper_ols':
        xbar = mean([r['x'] for r in train])
        ybar = mean([r['y'] for r in train])
        slope = (math.fsum((r['x'] - xbar) * (r['y'] - ybar) for r in train)
                 / math.fsum((r['x'] - xbar) ** 2 for r in train))
        return [ybar - slope * xbar, slope]
    groups = {s: [r for r in train if r['species'] == s] for s in SPECIES}
    centers = {s: (mean([r['x'] for r in rows]), mean([r['y'] for r in rows]))
               for s, rows in groups.items()}
    slope = (math.fsum((r['x'] - centers[r['species']][0])
                       * (r['y'] - centers[r['species']][1]) for r in train)
             / math.fsum((r['x'] - centers[r['species']][0]) ** 2 for r in train))
    intercepts = {s: centers[s][1] - slope * centers[s][0] for s in SPECIES}
    return [intercepts['Adelie'], slope,
            intercepts['Chinstrap'] - intercepts['Adelie'],
            intercepts['Gentoo'] - intercepts['Adelie']]


def prediction(row, beta):
    if len(beta) == 1:
        return beta[0]
    value = beta[0] + beta[1] * row['x']
    if len(beta) == 4:
        if row['species'] == 'Chinstrap':
            value += beta[2]
        elif row['species'] == 'Gentoo':
            value += beta[3]
    return value


def metric_check(observed, rows, beta, audit, label):
    audit.require(type(observed['n']) is int and observed['n'] == len(rows),
                  label + ': incorrect denominator')
    errors = [prediction(row, beta) - row['y'] for row in rows]
    audit.close(observed['mae_g'], mean([abs(e) for e in errors]), label + ' MAE')
    audit.close(observed['rmse_g'], math.sqrt(mean([e * e for e in errors])),
                label + ' RMSE')


def verify(run):
    audit = Audit()
    run = run.resolve()
    protocol = read_json(run, 'protocol.json')
    audit.require(protocol.get('config') == CONFIG,
                  'Protocol config differs from the fixed Penguins verification specification')
    raw_bytes = local_file(run, 'data/penguins.csv').read_bytes()
    audit.require(hashlib.sha256(raw_bytes).hexdigest() == DATA_SHA256,
                  'Data bytes differ from the pinned public dataset')
    raw = list(csv.DictReader(io.StringIO(raw_bytes.decode('utf-8'))))
    audit.require(len(raw) == 344, 'Wrong raw row count')
    excluded, rows = [], []
    for record_id, row in enumerate(raw, 1):
        if row['flipper_length_mm'] == 'NA' or row['body_mass_g'] == 'NA':
            excluded.append(record_id)
            continue
        audit.require(row['species'] in SPECIES, 'Unknown species in public data')
        rows.append({'record_id': record_id, 'year': int(row['year']),
                     'species': row['species'],
                     'x': (float(row['flipper_length_mm']) - 200.0) / 10.0,
                     'y': float(row['body_mass_g'])})
    audit.require(excluded == [4, 272], 'Incorrect exclusion policy')
    audit.require(len(rows) == 342, 'Wrong usable row count')
    audit.require(Counter(r['year'] for r in rows) == {2007: 109, 2008: 114, 2009: 119},
                  'Unexpected usable year counts')
    audit.require(sum(raw[r['record_id'] - 1]['sex'] == 'NA' for r in rows) == 9,
                  'Unused missing sex must not cause row exclusion')
    data_audit = read_json(run, 'results/data_audit.json')
    audit.require(data_audit == {'raw_rows': 344, 'usable_rows': 342,
                                'excluded_record_ids': [4, 272],
                                'retained_missing_sex': 9,
                                'missing_policy': CONFIG['missing_policy']},
                  'Recorded data audit differs from independently checked population')
    split_rows = keyed(read_json(run, 'results/splits.json'), ['split'], audit, 'splits')
    audit.require(set(split_rows) == {(split['id'],) for split in SPLITS},
                  'Missing or extra recorded split')

    reader = csv.DictReader(io.StringIO(local_file(run, 'results/predictions.csv')
                                        .read_text(encoding='utf-8')))
    audit.require(reader.fieldnames == PREDICTION_FIELDS, 'Prediction CSV schema mismatch')
    records = list(reader)
    audit.require(len(records) == 699, 'Expected 699 predictions across all six comparisons')
    observed_predictions = {}
    for row in records:
        audit.require(None not in row and all(value is not None for value in row.values()),
                      'Malformed prediction CSV row')
        record_id = int(row['record_id'])
        audit.require(str(record_id) == row['record_id'], 'Noncanonical record ID')
        key = (row['split'], row['condition'], record_id)
        audit.require(key not in observed_predictions, 'Duplicate prediction key: ' + str(key))
        observed_predictions[key] = row
    metric_rows = keyed(read_json(run, 'results/metrics.json'), ['split', 'condition'],
                       audit, 'metrics')
    species_rows = keyed(read_json(run, 'results/species_metrics.json'),
                        ['split', 'condition', 'species'], audit, 'species metrics')
    model_rows = keyed(read_json(run, 'results/models.json'), ['split', 'condition'],
                      audit, 'models')
    expected_groups = {(s['id'], c) for s in SPLITS for c in CONDITIONS}
    audit.require(set(metric_rows) == expected_groups, 'Missing or extra metric condition')
    audit.require(set(model_rows) == expected_groups, 'Missing or extra fitted model')
    audit.require(set(species_rows) == {(*g, s) for g in expected_groups for s in SPECIES},
                  'Missing or extra species metric condition')
    expected_predictions = set()
    counts = {}
    for split in SPLITS:
        train = [r for r in rows if r['year'] in split['train_years']]
        test = [r for r in rows if r['year'] == split['test_year']]
        audit.require(set(r['record_id'] for r in train).isdisjoint(r['record_id'] for r in test),
                      'Training/test record overlap')
        audit.require(max(r['year'] for r in train) < min(r['year'] for r in test),
                      'Training years must precede test year')
        expected_n = (223, 119) if split['id'] == 'primary' else (109, 114)
        audit.require((len(train), len(test)) == expected_n, 'Split denominator mismatch')
        split_record = split_rows[(split['id'],)]
        audit.require(split_record['train_ids'] == [r['record_id'] for r in train],
                      'Recorded training IDs differ from frozen temporal split')
        audit.require(split_record['test_ids'] == [r['record_id'] for r in test],
                      'Recorded test IDs differ from frozen temporal split')
        counts[split['id']] = {'train_n': len(train), 'test_n': len(test),
                                'test_species_n': dict(sorted(Counter(r['species'] for r in test).items()))}
        for condition in CONDITIONS:
            key = (split['id'], condition)
            beta = coefficients(train, condition)
            model = model_rows[key]
            label = '/'.join(key)
            audit.require(type(model['train_n']) is int and model['train_n'] == len(train),
                          label + ': model training count mismatch')
            audit.require(model['feature_names'] == FEATURE_NAMES[condition],
                          label + ': model feature order mismatch')
            audit.require(isinstance(model['coefficients'], list)
                          and len(model['coefficients']) == len(beta),
                          label + ': coefficient count mismatch')
            for number, (observed, expected) in enumerate(zip(model['coefficients'], beta)):
                audit.close(observed, expected, label + ': coefficient ' + str(number))
            for row in test:
                pred_key = (*key, row['record_id'])
                expected_predictions.add(pred_key)
                audit.require(pred_key in observed_predictions, 'Missing prediction: ' + str(pred_key))
                recorded = observed_predictions[pred_key]
                audit.require(recorded['year'] == str(row['year']), 'Incorrect prediction year')
                audit.require(recorded['species'] == row['species'], 'Incorrect prediction species')
                audit.close(float(recorded['observed_g']), row['y'], 'Incorrect observed target')
                audit.close(float(recorded['predicted_g']), prediction(row, beta),
                            'Prediction differs from independent fit: ' + str(pred_key))
            metric_check(metric_rows[key], test, beta, audit, label)
            for species in SPECIES:
                selected = [r for r in test if r['species'] == species]
                metric_check(species_rows[(*key, species)], selected, beta, audit,
                             label + '/' + species)
    audit.require(set(observed_predictions) == expected_predictions,
                  'Extra prediction key or incorrect split membership')
    return {'passed': True, 'check_count': audit.checks,
            'counts': {'raw_rows': 344, 'usable_rows': 342, 'excluded_record_ids': excluded,
                       'predictions': 699, 'models': 6, 'metric_rows': 6,
                       'species_metric_rows': 18, 'split_records': 2,
                       'data_audit_records': 1, 'splits': counts},
            'method': 'independent scalar OLS and within-species centered common-slope fit',
            'numeric_tolerance': {'absolute': 1e-7, 'relative': 1e-11},
            'scope': 'fixed Penguins protocol, pinned data bytes, train/test membership, all fitted coefficients, targets, predictions, MAE and RMSE',
            'does_not_establish': ['independent observations or absence of repeated individuals',
                                   'causality, external validity or statistical significance',
                                   'general validation of arbitrary custom research or upstream workflows']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = verify(args.run)
    except (ValueError, KeyError, TypeError, OSError, ZeroDivisionError) as error:
        print(json.dumps({'passed': False, 'error': str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
