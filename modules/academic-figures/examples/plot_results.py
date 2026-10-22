#!/usr/bin/env python3
"""Original Matplotlib teaching figures from verified experiment/analysis artifacts."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ANALYSIS_DIR = HERE.parents[1] / 'data-analysis' / 'examples' / 'paired-analysis'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def verified_analysis(experiment, analysis):
    sys.path.insert(0, str(ANALYSIS_DIR))
    try:
        spec = importlib.util.spec_from_file_location('ars_teaching_analysis_verifier', ANALYSIS_DIR / 'verify_analysis.py')
        verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)
        verifier.check_directory(experiment, analysis)
        return verifier.analysis.strict_json((analysis / 'analysis.json').read_bytes())
    finally:
        sys.path.pop(0)


def generate(experiment, analysis, output):
    if output.exists() or output.is_symlink():
        raise ValueError('Output already exists; choose a new directory')
    if any(output.resolve().is_relative_to(p.resolve()) for p in (experiment, analysis)):
        raise ValueError('Output cannot be inside an input directory')
    before = {str(p): digest(p) for folder in (experiment, analysis) for p in folder.iterdir() if p.is_file()}
    data = verified_analysis(experiment, analysis)
    rows = [r for r in data['descriptive_rows'] if r['evaluation_split'] == 'test']
    seeds = sorted({r['split_seed'] for r in rows})
    conditions = ['raw_1nn', 'scaled_1nn', 'scaled_1nn_without_x0']
    lookup = {(r['split_seed'], r['condition']): r for r in rows}
    if len(lookup) != len(rows) or set(lookup) != {(s, c) for s in seeds for c in conditions}:
        raise ValueError('Incomplete or duplicate condition coverage')
    paired = data['paired_bootstrap']
    point, (lo, hi) = paired['point_difference_pp'], paired['interval_pp']
    # Render the endpoints directly: a percentile interval need not contain its point estimate.
    plotted = {'descriptive_test_rows': rows, 'paired_bootstrap': paired,
               'analysis_status': data['analysis_status'], 'interpretation_limits': data['interpretation_limits']}
    with tempfile.TemporaryDirectory(prefix='ars-mpl-cache-') as cache:
        os.environ['MPLCONFIGDIR'] = cache
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy
        matplotlib.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                                    'svg.fonttype': 'none', 'svg.hashsalt': 'ars-teaching-v1',
                                    'axes.spines.top': False, 'axes.spines.right': False})
        fig, (ax, interval) = plt.subplots(1, 2, figsize=(10.8, 4.4), gridspec_kw={'width_ratios': [1.35, 1]})
        names = ['Raw 1-NN', 'Scaled 1-NN', 'Scaled, feature 0 removed']
        for ci, (condition, label, color, marker) in enumerate(zip(
                conditions, names, ['#0072B2', '#D55E00', '#009E73'], ['o', 's', '^'])):
            xs = [i + (ci - 1) * .20 for i in range(len(seeds))]
            ys = [lookup[(s, condition)]['accuracy'] * 100 for s in seeds]
            ax.scatter(xs, ys, label=label, color=color, marker=marker, s=52, zorder=3)
            for x, y in zip(xs, ys):
                ax.annotate(f'{y:.1f}', (x, y), xytext=(0, 7), textcoords='offset points',
                            ha='center', va='bottom', fontsize=8)
        ax.set_xticks(range(len(seeds)), [str(s) for s in seeds])
        ax.set_xlabel('Data split seed (shared source dataset)')
        ax.set_ylabel('Test accuracy (%)')
        ax.set_ylim(0, 105)
        ax.set_xlim(-.55, len(seeds) - .45)
        ax.grid(axis='y', color='#dddddd', linewidth=.7)
        ax.legend(loc='lower center', fontsize=8, frameon=False)
        interval.axvline(0, color='#777777', linestyle='--', linewidth=1)
        interval.hlines(0, lo, hi, color='#D55E00', linewidth=2)
        interval.vlines([lo, hi], -.07, .07, color='#D55E00', linewidth=1.5)
        interval.scatter([point], [0], marker='s', color='#D55E00', s=55, zorder=3)
        interval.annotate(f'{point:+.2f} pp\n[{lo:.2f}, {hi:.2f}]', (point, 0),
                          xytext=(0, 20), textcoords='offset points', ha='center', fontsize=10)
        interval.set_xlabel('Accuracy difference (percentage points)')
        interval.set_yticks([0], ['Scaled\nminus raw'])
        interval.set_ylim(-.65, .8)
        span = max(1, max(0, point, hi) - min(0, point, lo))
        interval.set_xlim(min(0, point, lo) - .16 * span, max(0, point, hi) + .16 * span)
        interval.text(.5, .05, f"Fixed split {paired['split_seed']}; {paired['n_pairs']} pairs\n"
                      f"{paired['resamples']:,} paired resamples; 95% percentile CI",
                      transform=interval.transAxes, ha='center', va='bottom', fontsize=8)
        fig.tight_layout(w_pad=3)
        if any(digest(Path(p)) != sha for p, sha in before.items()):
            raise ValueError('Input changed during plotting')
        output.mkdir(parents=True, exist_ok=False)
        fig.savefig(output / 'comparison.svg', metadata={'Date': None, 'Creator': 'ARS original teaching example'})
        fig.savefig(output / 'comparison.pdf', metadata={'CreationDate': None, 'ModDate': None,
                                                        'Creator': 'ARS original teaching example'})
        fig.savefig(output / 'comparison.png', dpi=180, metadata={'Software': 'ARS original teaching example'})
        plt.close(fig)
        versions = {'python': platform.python_version(), 'platform': platform.platform(),
                    'matplotlib': matplotlib.__version__, 'numpy': numpy.__version__}
    (output / 'plotted-data.json').write_bytes(json_bytes(plotted))
    sizes = '; '.join(f"split {s}: n={lookup[(s, conditions[0])]['n']} per condition" for s in seeds)
    caption = ('# Teaching figure caption\n\n'
               'Left: all test results by data split and condition. Points are observed accuracies; no cross-seed '
               f'interval is estimated. {sizes}. The splits share one source dataset and are not independent studies.\n\n'
               f"Right: scaled minus raw accuracy for fixed split {paired['split_seed']}, "
               f"{paired['n_pairs']} paired test samples. Point difference {point:.4f} percentage points; "
               f"95% paired percentile bootstrap interval [{lo:.4f}, {hi:.4f}], "
               f"{paired['resamples']} resamples, random seed {paired['random_seed']}. "
               'Conditional on the fixed fitted models and IID test observations; excludes training, '
               'model-selection and across-split uncertainty. Post-hoc synthetic teaching analysis, '
               'without a confirmatory significance claim.\n')
    (output / 'caption.md').write_text(caption, encoding='utf-8')
    names = ['comparison.svg', 'comparison.pdf', 'comparison.png', 'plotted-data.json', 'caption.md']
    manifest = {'schema_version': 1, 'artifact_sha256': {n: digest(output / n) for n in names},
                'input_manifest_sha256': {'experiment': digest(experiment / 'manifest.json'),
                                          'analysis': digest(analysis / 'manifest.json')},
                'source_sha256': {'plot_results.py': digest(HERE / 'plot_results.py')},
                'environment': versions, 'upstream_skill_executed': False}
    (output / 'manifest.json').write_bytes(json_bytes(manifest))
    print('Created 6 figure artifacts from verified inputs; no upstream skill workflow executed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--experiment', type=Path, required=True)
    parser.add_argument('--analysis', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    generate(args.experiment, args.analysis, args.output)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, ImportError) as exc:
        print('Figure generation failed: ' + str(exc), file=sys.stderr)
        sys.exit(1)
