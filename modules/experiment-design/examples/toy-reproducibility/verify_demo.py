#!/usr/bin/env python3
"""Check local teaching artifacts and optionally compare an independent rerun."""
import argparse
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import run_demo as demo


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_directory(folder):
    require(folder.is_dir() and not folder.is_symlink(), "Expected a regular output directory")
    expected_names = set(demo.ARTIFACTS + ["manifest.json"])
    require({p.name for p in folder.iterdir()} == expected_names, "Unexpected or missing output files")
    for name in expected_names:
        path = folder / name
        require(path.is_file() and not path.is_symlink(), "Expected regular file: " + name)
    manifest = json.loads((folder / "manifest.json").read_bytes())
    require(manifest["schema_version"] == 1, "Unsupported output version")
    require(set(manifest["artifact_sha256"]) == set(demo.ARTIFACTS), "Wrong hash coverage")
    for name in demo.ARTIFACTS:
        require(demo.digest((folder / name).read_bytes()) == manifest["artifact_sha256"][name],
                "Artifact hash mismatch: " + name)
    source_dir = Path(__file__).resolve().parent
    require(set(manifest["source_sha256"]) == {"run_demo.py", "verify_demo.py"}, "Wrong source coverage")
    for name, expected in manifest["source_sha256"].items():
        require(demo.digest((source_dir / name).read_bytes()) == expected,
                "Source version differs from recorded run: " + name)
    protocol = json.loads((folder / "protocol.json").read_bytes())
    demo.validate_protocol(protocol)
    data = json.loads((folder / "dataset.json").read_bytes())
    require(data == demo.generate_data(protocol), "Data does not match the frozen generator")
    runs = json.loads((folder / "runs.json").read_bytes())
    require([r["split_seed"] for r in runs] == protocol["split_seeds"], "Seed coverage mismatch")
    for run in runs:
        splits = run["splits"]
        require(set(splits) == {"train", "validation", "test"}, "Wrong split names")
        flat = [i for part in splits.values() for i in part]
        require(len(flat) == len(set(flat)) == len(data) and set(flat) == set(range(len(data))),
                "Splits overlap or omit samples")
        require(splits == demo.make_splits(protocol, run["split_seed"]), "Split differs from protocol")
        train = [data[i] for i in splits["train"]]
        # Independently verify that scale uses training features only.
        ranges = [max(1, max(row["x"][j] for row in train)
                      - min(row["x"][j] for row in train)) for j in (0, 1)]
        require(run["train_feature_ranges"] == ranges, "Scaling differs from train-only range")
        require([c["condition"] for c in run["conditions"]] == demo.CONDITIONS,
                "Condition coverage mismatch")
        for condition in run["conditions"]:
            for part in ("validation", "test"):
                result = condition[part]
                records = result["predictions"]
                require([x["sample_id"] for x in records] == splits[part], "Prediction sample coverage mismatch")
                for item in records:
                    row = data[item["sample_id"]]
                    require(item["target"] == row["y"], "Target differs from original data")
                    expected = demo.predict(train, row["x"], ranges, condition["condition"])
                    require(item["prediction"] == expected, "Prediction differs from recorded method")
                    if condition["condition"] == "scaled_1nn_without_x0":
                        altered = [row["x"][0] + 1000000, row["x"][1]]
                        require(demo.predict(train, altered, ranges, condition["condition"]) == expected,
                                "Ablation still depends on x0")
                correct = sum(x["target"] == x["prediction"] for x in records)
                require(result["n"] == len(records) and result["correct"] == correct
                        and result["accuracy"] == correct / len(records), "Metric mismatch")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--compare", type=Path, help="A different independently generated output directory")
    args = parser.parse_args()
    first = check_directory(args.output)
    if args.compare:
        require(args.output.resolve() != args.compare.resolve(), "Comparison needs two different directories")
        second = check_directory(args.compare)
        require(first["source_sha256"] == second["source_sha256"], "Different source versions")
        for name in demo.ARTIFACTS:
            require((args.output / name).read_bytes() == (args.compare / name).read_bytes(),
                    "Independent rerun differs: " + name)
        print("PASS: both outputs verified; protocol, data, splits, predictions and metrics are byte-identical.")
    else:
        print("PASS: artifact hashes, split boundaries, train-only scaling, seed/condition coverage and metrics verified.")
    print("This verifies the local teaching example, not an upstream skill or published scientific result.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, IndexError, ZeroDivisionError) as exc:
        print("Verification failed: " + str(exc), file=sys.stderr)
        sys.exit(1)
