#!/usr/bin/env python3
"""Plot verified measured Wine results with Matplotlib; optional to the standard-library core."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import verify_case


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--input', type=Path, required=True)
    a = p.parse_args()
    verify_case.check(a.input)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.hashsalt': 'uci-wine-scaling-v1', 'font.size': 10})
    output = a.input/'figures'
    if output.exists() or output.is_symlink():
        raise ValueError('Figure directory exists; choose a fresh complete run before plotting.')
    metrics = json.loads((a.input/'metrics.json').read_text(encoding='utf-8'))
    pair = json.loads((a.input/'paired-analysis.json').read_text(encoding='utf-8'))
    fig, axs = plt.subplots(2, 2, figsize=(12, 8), layout='constrained')
    seeds = [20261023, 11, 23, 47, 71, 101]
    colors = ['#6b7280', '#2563eb', '#c2410c']
    for c, color, label in zip(['majority_train', 'raw_5nn', 'zscore_train_5nn'], colors, ['Train majority', 'Raw 5-NN', 'Train z-score 5-NN']):
        vals = [next(m['accuracy'] for m in metrics if m['seed'] == s and m['condition'] == c)*100 for s in seeds]
        axs[0, 0].scatter(range(6), vals, label=label, color=color, s=45)
    axs[0, 0].set(xticks=range(6), xticklabels=['Primary', '11', '23', '47', '71', '101'], ylim=(0, 104),
                  ylabel='Test accuracy (%)', title='All fixed splits; overlapping observations')
    axs[0, 0].grid(axis='y', alpha=.2); axs[0, 0].legend(fontsize=8)
    lo, hi = pair['interval_pp']; point = pair['difference_pp']
    axs[0, 1].errorbar([point], [0], xerr=[[point-lo], [hi-point]], fmt='s', capsize=6, color=colors[2])
    axs[0, 1].axvline(0, linestyle='--', color='#777777')
    axs[0, 1].set(yticks=[], xlabel='Scaled minus raw (percentage points)', title='Primary split: 45 paired test observations')
    axs[0, 1].text(.5, .75, f'{point:+.2f} pp; 95% interval [{lo:.2f}, {hi:.2f}]', transform=axs[0, 1].transAxes, ha='center')
    axs[0, 1].text(.5, .15, '10,000 class-stratified paired resamples\nConditional on fitted models and class proportions', transform=axs[0, 1].transAxes, ha='center', fontsize=9)
    for ax, condition in zip(axs[1], ['raw_5nn', 'zscore_train_5nn']):
        row = next(m for m in metrics if m['seed'] == 20261023 and m['condition'] == condition)
        cm = row['confusion_matrix']; ax.imshow(cm, cmap='Blues', vmin=0, vmax=18)
        for i in range(3):
            for j in range(3):
                ax.text(j, i, str(cm[i][j]), ha='center', va='center', color='white' if cm[i][j] > 9 else 'black')
        ax.set(xticks=range(3), yticks=range(3), xticklabels=[1, 2, 3], yticklabels=[1, 2, 3], xlabel='Predicted cultivar', ylabel='True cultivar', title=f"{condition}: {row['correct']}/45")
    fig.suptitle('UCI Wine: real public data; fixed 5-NN comparison', fontsize=15)
    output.mkdir()
    fig.savefig(output/'comparison.png', dpi=160, metadata={'Software': 'Academic Research Skills real-wine'})
    fig.savefig(output/'comparison.svg', metadata={'Date': None})
    fig.savefig(output/'comparison.pdf', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)
    data = {'metrics': metrics, 'paired': {k: pair[k] for k in ['seed', 'n_pairs', 'difference_pp', 'interval_pp', 'method']}}
    (output/'plotted-data.json').write_bytes((json.dumps(data, sort_keys=True, indent=2)+'\n').encode())
    digest = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
    manifest = {'matplotlib': matplotlib.__version__, 'plot_source_sha256': digest(Path(__file__)),
                'inputs': {n: digest(a.input/n) for n in ['metrics.json', 'paired-analysis.json']},
                'artifacts': {f.name: digest(f) for f in sorted(output.iterdir())}}
    (output/'manifest.json').write_bytes((json.dumps(manifest, sort_keys=True, indent=2)+'\n').encode())
    print('PASS: measured accuracy, paired interval and two confusion matrices plotted.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, AssertionError, KeyError, TypeError, ImportError) as exc:
        print('Wine plot failed: ' + str(exc), file=sys.stderr); sys.exit(1)
