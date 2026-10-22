#!/usr/bin/env python3
"""Original, standard-library teaching analysis of the repository's CPU example."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import random
import sys

sys.dont_write_bytecode = True
SOURCE_DIR = Path(__file__).resolve().parent
EXPERIMENT_DIR = SOURCE_DIR.parents[2] / "experiment-design" / "examples" / "toy-reproducibility"
INPUT_FILES = {"protocol.json", "dataset.json", "runs.json", "manifest.json"}
ARTIFACTS = {"analysis_protocol.json", "input_manifest.json", "analysis.json"}
SOURCE_FILES = {"analyze_demo.py", "verify_analysis.py"}
CONDITIONS = ["raw_1nn", "scaled_1nn", "scaled_1nn_without_x0"]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(content):
    return hashlib.sha256(content).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


def strict_json(content):
    def reject_constant(value):
        raise ValueError("Non-finite JSON number: " + value)

    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "Duplicate JSON key: " + key)
            result[key] = value
        return result

    return json.loads(content, parse_constant=reject_constant, object_pairs_hook=unique_keys)


def exact_keys(value, keys, label):
    require(isinstance(value, dict) and set(value) == set(keys), "Unsupported fields: " + label)


def validate_protocol(p):
    exact_keys(p, {"schema_version", "analysis_id", "analysis_status", "baseline", "comparison",
                   "evaluation_split", "fixed_split_seed", "bootstrap_resamples", "bootstrap_seed",
                   "confidence_level", "interval_method"}, "analysis protocol")
    for key in ("schema_version", "fixed_split_seed", "bootstrap_resamples", "bootstrap_seed"):
        require(type(p[key]) is int, key + " must be an integer")
    require(p["schema_version"] == 1 and p["fixed_split_seed"] == 11,
            "This teaching protocol supports schema 1 and fixed split seed 11 only")
    require(isinstance(p["analysis_id"], str) and bool(p["analysis_id"].strip()), "Empty analysis ID")
    require(p["analysis_status"] == "post-hoc teaching; not preregistered or confirmatory",
            "Keep the post-hoc teaching status explicit")
    require(p["baseline"] == "raw_1nn" and p["comparison"] == "scaled_1nn"
            and p["evaluation_split"] == "test", "Unsupported comparison or evaluation split")
    require(type(p["confidence_level"]) is float and p["confidence_level"] == 0.95
            and p["interval_method"] == "percentile-linear", "Only the stated 95% percentile interval is supported")
    require(100 <= p["bootstrap_resamples"] <= 50000, "Use 100..50000 bootstrap resamples")


def check_input_schema(objects):
    experiment_protocol = objects["protocol.json"]
    require(isinstance(experiment_protocol, dict)
            and type(experiment_protocol.get("schema_version")) is int
            and experiment_protocol["schema_version"] == 1, "Unsupported input protocol schema")
    manifest = objects["manifest.json"]
    exact_keys(manifest, {"schema_version", "artifact_sha256", "source_sha256", "environment"}, "input manifest")
    require(type(manifest["schema_version"]) is int and manifest["schema_version"] == 1,
            "Unsupported input schema")
    exact_keys(manifest["environment"], {"python", "implementation", "platform"}, "input environment")
    require(all(isinstance(v, str) and v for v in manifest["environment"].values()), "Invalid input environment")
    data, runs = objects["dataset.json"], objects["runs.json"]
    require(isinstance(data, list) and isinstance(runs, list), "Expected dataset and runs arrays")
    for row in data:
        exact_keys(row, {"id", "x", "y"}, "sample")
        require(type(row["id"]) is int and type(row["y"]) is int and row["y"] in (0, 1), "Invalid sample ID/label")
        require(isinstance(row["x"], list) and len(row["x"]) == 2
                and all(type(x) is int for x in row["x"]), "Invalid sample features")
    for run in runs:
        exact_keys(run, {"split_seed", "splits", "train_feature_ranges", "conditions"}, "run")
        require(type(run["split_seed"]) is int, "Invalid split seed")
        exact_keys(run["splits"], {"train", "validation", "test"}, "splits")
        require(all(isinstance(ids, list) and all(type(i) is int for i in ids)
                    for ids in run["splits"].values()), "Invalid split IDs")
        ranges = run["train_feature_ranges"]
        require(isinstance(ranges, list) and len(ranges) == 2
                and all(type(x) is int and x > 0 for x in ranges), "Invalid feature ranges")
        require(isinstance(run["conditions"], list), "Expected conditions array")
        for condition in run["conditions"]:
            exact_keys(condition, {"condition", "validation", "test"}, "condition")
            for part in ("validation", "test"):
                result = condition[part]
                exact_keys(result, {"n", "correct", "accuracy", "predictions"}, "evaluation")
                require(type(result["n"]) is int and type(result["correct"]) is int
                        and type(result["accuracy"]) in (int, float)
                        and math.isfinite(result["accuracy"]), "Invalid evaluation metrics")
                require(isinstance(result["predictions"], list), "Expected prediction array")
                for record in result["predictions"]:
                    exact_keys(record, {"sample_id", "target", "prediction"}, "prediction")
                    require(type(record["sample_id"]) is int
                            and all(type(record[k]) is int and record[k] in (0, 1)
                                    for k in ("target", "prediction")), "Invalid prediction record")


def load_input(folder):
    require(folder.is_dir() and not folder.is_symlink(), "Input must be a regular directory")
    require({p.name for p in folder.iterdir()} == INPUT_FILES, "Unknown or missing input files")
    raw = {}
    for name in INPUT_FILES:
        path = folder / name
        require(path.is_file() and not path.is_symlink(), "Input must contain regular files: " + name)
        raw[name] = path.read_bytes()
    objects = {name: strict_json(content) for name, content in raw.items()}
    check_input_schema(objects)
    # This is the repository's original teaching verifier, not an upstream snapshot.
    # Its import only defines functions; experiment execution remains in its main guard.
    sys.path.insert(0, str(EXPERIMENT_DIR))
    try:
        spec = importlib.util.spec_from_file_location("ars_original_experiment_verifier", EXPERIMENT_DIR / "verify_demo.py")
        verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)
        verifier.check_directory(folder)
    finally:
        sys.path.pop(0)
    # Ensure the bytes retained for analysis still match the validated files.
    require(all((folder / name).read_bytes() == content for name, content in raw.items()),
            "Input changed during validation")
    require(11 in objects["protocol.json"]["split_seeds"], "Input must include the fixed teaching seed 11")
    return raw, objects


def pair_records(baseline, comparison):
    def by_id(records):
        require(isinstance(records, list) and bool(records), "Empty prediction pairs")
        lookup = {}
        for row in records:
            exact_keys(row, {"sample_id", "target", "prediction"}, "paired prediction")
            sample_id = row["sample_id"]
            require(type(sample_id) is int and sample_id not in lookup, "Duplicate or invalid paired sample ID")
            require(all(type(row[k]) is int and row[k] in (0, 1) for k in ("target", "prediction")),
                    "Pair labels and predictions must be binary integers")
            lookup[sample_id] = row
        return lookup

    left, right = by_id(baseline), by_id(comparison)
    require(set(left) == set(right), "Paired sample IDs differ")
    pairs = []
    for sample_id in sorted(left):
        a, b = left[sample_id], right[sample_id]
        require(a["target"] == b["target"], "Paired targets differ")
        ca, cb = int(a["prediction"] == a["target"]), int(b["prediction"] == b["target"])
        pairs.append({"sample_id": sample_id, "baseline_correct": ca,
                      "comparison_correct": cb, "delta_correct": cb - ca})
    return pairs


def linear_percentile(sorted_values, probability):
    require(bool(sorted_values) and 0 <= probability <= 1, "Invalid percentile input")
    index = probability * (len(sorted_values) - 1)
    lower, upper = math.floor(index), math.ceil(index)
    return sorted_values[lower] + (sorted_values[upper] - sorted_values[lower]) * (index - lower)


def paired_bootstrap(deltas, resamples, seed):
    require(bool(deltas) and all(type(d) is int and d in (-1, 0, 1) for d in deltas), "Invalid paired deltas")
    require(type(resamples) is int and resamples > 0 and type(seed) is int, "Invalid bootstrap settings")
    rng = random.Random(seed)
    n = len(deltas)
    # Resampling a pair's delta uses the SAME index for its two correctness values.
    totals = [sum(deltas[rng.randrange(n)] for _ in range(n)) for _ in range(resamples)]
    values = sorted(100.0 * total / n for total in totals)
    return {"point_difference_pp": 100.0 * sum(deltas) / n,
            "interval_pp": [linear_percentile(values, 0.025), linear_percentile(values, 0.975)],
            "resample_sum_counts": [{"delta_correct_sum": k, "resamples": v}
                                    for k, v in sorted(Counter(totals).items())]}


def build_analysis(objects, protocol):
    rows = []
    selected_pairs = None
    for run in objects["runs.json"]:
        conditions = {c["condition"]: c for c in run["conditions"]}
        for part in ("validation", "test"):
            baseline = conditions[protocol["baseline"]][part]["predictions"]
            for name in CONDITIONS:
                predictions = conditions[name][part]["predictions"]
                pairs = pair_records(baseline, predictions)
                n = len(pairs)
                correct = sum(p["comparison_correct"] for p in pairs)
                rows.append({"split_seed": run["split_seed"], "evaluation_split": part,
                             "condition": name, "n": n, "correct": correct,
                             "accuracy": correct / n, "baseline": protocol["baseline"],
                             "difference_vs_baseline_pp": 100.0 * sum(p["delta_correct"] for p in pairs) / n,
                             "gained_vs_baseline": sum(p["delta_correct"] == 1 for p in pairs),
                             "lost_vs_baseline": sum(p["delta_correct"] == -1 for p in pairs)})
                if (run["split_seed"] == protocol["fixed_split_seed"] and part == protocol["evaluation_split"]
                        and name == protocol["comparison"]):
                    selected_pairs = pairs
    require(selected_pairs is not None, "Fixed teaching comparison is missing")
    bootstrap = paired_bootstrap([p["delta_correct"] for p in selected_pairs],
                                 protocol["bootstrap_resamples"], protocol["bootstrap_seed"])
    bootstrap.update({"split_seed": protocol["fixed_split_seed"], "evaluation_split": "test",
                      "baseline": protocol["baseline"], "comparison": protocol["comparison"],
                      "n_pairs": len(selected_pairs), "resamples": protocol["bootstrap_resamples"],
                      "random_seed": protocol["bootstrap_seed"], "confidence_level": 0.95,
                      "interval_method": protocol["interval_method"], "pairs": selected_pairs})
    return {"schema_version": 1, "analysis_id": protocol["analysis_id"],
            "analysis_status": protocol["analysis_status"], "descriptive_rows": rows,
            "paired_bootstrap": bootstrap,
            "interpretation_limits": [
                "Post-hoc teaching analysis: no preregistration, confirmatory claim, p-value or significance decision.",
                "IID test observations are assumed; the interval is conditional on this fixed split and these fitted models.",
                "The interval excludes training, model-selection and across-split uncertainty; coverage is not guaranteed.",
                "The split seeds reuse one dataset; do not pool their sample counts or treat them as independent studies.",
                "Seed 11 is fixed for illustration, not chosen by ranking results; all seeds and conditions remain visible."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Unmodified original CPU experiment output directory")
    parser.add_argument("--output", type=Path, required=True, help="New analysis output directory; never overwritten")
    parser.add_argument("--protocol", type=Path, default=SOURCE_DIR / "analysis_protocol.json")
    args = parser.parse_args()
    require(not args.output.exists() and not args.output.is_symlink(), "Output already exists; choose a new directory")
    require(not args.output.resolve().is_relative_to(args.input.resolve()), "Output cannot be inside the input directory")
    protocol_bytes = args.protocol.read_bytes()
    protocol = strict_json(protocol_bytes)
    validate_protocol(protocol)
    raw, objects = load_input(args.input)
    artifacts = {"analysis_protocol.json": protocol_bytes, "input_manifest.json": raw["manifest.json"],
                 "analysis.json": json_bytes(build_analysis(objects, protocol))}
    manifest = {"schema_version": 1,
                "artifact_sha256": {name: digest(content) for name, content in artifacts.items()},
                "input_artifact_sha256": {name: digest(content) for name, content in raw.items()},
                "input_source_sha256": objects["manifest.json"]["source_sha256"],
                "source_sha256": {name: digest((SOURCE_DIR / name).read_bytes()) for name in SOURCE_FILES},
                "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                                "platform": platform.platform()}}
    args.output.mkdir(parents=True, exist_ok=False)
    for name, content in artifacts.items():
        (args.output / name).write_bytes(content)
    (args.output / "manifest.json").write_bytes(json_bytes(manifest))
    print("Created 4 analysis files: all seeds/conditions retained; one fixed-seed paired bootstrap. Teaching only.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, IndexError, ZeroDivisionError, OverflowError, AttributeError) as exc:
        print("Analysis failed: " + str(exc), file=sys.stderr)
        sys.exit(1)
