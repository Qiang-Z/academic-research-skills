#!/usr/bin/env python3
"""Execute the frozen Penguins teaching comparison; Python standard library only."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def solve(matrix, vector):
    """Small pivoted Gaussian elimination; verifier uses scalar/group centering."""
    n = len(vector)
    a = [list(row) + [v] for row, v in zip(matrix, vector)]
    for j in range(n):
        pivot = max(range(j, n), key=lambda k: abs(a[k][j]))
        a[j], a[pivot] = a[pivot], a[j]
        if abs(a[j][j]) < 1e-10:
            raise ValueError('Singular design; no fallback or model selection')
        scale = a[j][j]
        a[j] = [v / scale for v in a[j]]
        for k in range(n):
            if k != j:
                scale = a[k][j]
                a[k] = [x - scale * y for x, y in zip(a[k], a[j])]
    return [row[-1] for row in a]


def features(row, condition, config):
    x = (float(row['flipper_length_mm']) - config['flipper_center_mm']) / config['flipper_scale_mm']
    if condition == 'mean_baseline':
        return [1.0], ['intercept']
    if condition == 'flipper_ols':
        return [1.0, x], ['intercept', 'flipper_10mm']
    if condition == 'flipper_species_ols':
        return [1.0, x, float(row['species'] == 'Chinstrap'), float(row['species'] == 'Gentoo')], ['intercept', 'flipper_10mm', 'Chinstrap', 'Gentoo']
    raise ValueError('Unknown condition')


def summary(rows):
    errors = [r['predicted_g'] - r['observed_g'] for r in rows]
    return {'n': len(rows), 'mae_g': sum(abs(x) for x in errors) / len(rows),
            'rmse_g': math.sqrt(sum(x*x for x in errors) / len(rows))}


def run(folder):
    protocol = read(folder / 'protocol.json')
    config = protocol['config']
    data = folder / 'data/penguins.csv'
    if hashlib.sha256(data.read_bytes()).hexdigest() != config['data_sha256']:
        raise ValueError('Dataset bytes differ from frozen protocol')
    with data.open(encoding='utf-8', newline='') as stream:
        raw = list(csv.DictReader(stream))
    rows, excluded = [], []
    for i, row in enumerate(raw, 1):
        row = dict(row, record_id=i)
        if row['flipper_length_mm'] == 'NA' or row['body_mass_g'] == 'NA':
            excluded.append(i)
        else:
            rows.append(row)
    if (len(raw), len(rows), excluded) != (config['raw_rows'], config['usable_rows'], config['excluded_record_ids']):
        raise ValueError('Unexpected data population')
    output = folder / 'results'
    output.mkdir(exist_ok=False)
    predictions, models, metrics, by_species, splits = [], [], [], [], []
    for split in config['splits']:
        train = [r for r in rows if int(r['year']) in split['train_years']]
        test = [r for r in rows if int(r['year']) == split['test_year']]
        if not train or not test or set(r['record_id'] for r in train) & set(r['record_id'] for r in test):
            raise ValueError('Invalid temporal split')
        splits.append({'split': split['id'], 'train_ids': [r['record_id'] for r in train], 'test_ids': [r['record_id'] for r in test]})
        for condition in config['conditions']:
            design = [features(r, condition, config)[0] for r in train]
            names = features(train[0], condition, config)[1]
            y = [float(r['body_mass_g']) for r in train]
            size = len(names)
            xtx = [[sum(v[i]*v[j] for v in design) for j in range(size)] for i in range(size)]
            xty = [sum(v[i]*t for v, t in zip(design, y)) for i in range(size)]
            beta = solve(xtx, xty)
            models.append({'split': split['id'], 'condition': condition, 'train_n': len(train), 'feature_names': names, 'coefficients': beta})
            batch = []
            for r in test:
                x, _ = features(r, condition, config)
                batch.append({'split': split['id'], 'condition': condition, 'record_id': r['record_id'], 'year': int(r['year']), 'species': r['species'],
                              'observed_g': float(r['body_mass_g']), 'predicted_g': sum(a*b for a, b in zip(x, beta))})
            predictions.extend(batch)
            metrics.append({'split': split['id'], 'condition': condition, **summary(batch)})
            for species in config['species_order']:
                subset = [r for r in batch if r['species'] == species]
                by_species.append({'split': split['id'], 'condition': condition, 'species': species, **summary(subset)})
    with (output / 'predictions.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(predictions[0]))
        writer.writeheader(); writer.writerows(predictions)
    save(output / 'models.json', models)
    save(output / 'metrics.json', metrics)
    save(output / 'species_metrics.json', by_species)
    save(output / 'splits.json', splits)
    save(output / 'data_audit.json', {'raw_rows': len(raw), 'usable_rows': len(rows), 'excluded_record_ids': excluded,
         'retained_missing_sex': sum(r['sex'] == 'NA' for r in rows), 'missing_policy': config['missing_policy']})
    print(json.dumps({'status': 'measured', 'predictions': len(predictions), 'models': len(models), 'output': 'results', 'protocol_sha256': hashlib.sha256((folder / 'protocol.json').read_bytes()).hexdigest()}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    run(parser.parse_args().run.resolve())
