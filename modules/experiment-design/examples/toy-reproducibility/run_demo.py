#!/usr/bin/env python3
"""Original, local-only teaching experiment. Python standard library only."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import random
import sys

CONDITIONS = ["raw_1nn", "scaled_1nn", "scaled_1nn_without_x0"]
ARTIFACTS = ["protocol.json", "dataset.json", "runs.json"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)
            + "\n").encode("utf-8")


def validate_protocol(p):
    expected = {"schema_version", "study_id", "data_seed", "n_samples",
                "label_flip_every", "split_seeds", "train_size",
                "validation_size", "conditions", "metric", "selection_rule"}
    if set(p) != expected or p["schema_version"] != 1:
        raise ValueError("Unsupported protocol fields or schema version")
    for field in ("data_seed", "n_samples", "label_flip_every", "train_size",
                  "validation_size"):
        if type(p[field]) is not int:
            raise ValueError(field + " must be an integer")
    if not 30 <= p["n_samples"] <= 1000 or p["label_flip_every"] < 2:
        raise ValueError("Use 30..1000 samples and label_flip_every >= 2")
    if (p["train_size"] < 2 or p["validation_size"] < 1
            or p["train_size"] + p["validation_size"] >= p["n_samples"]):
        raise ValueError("All three splits must be nonempty; train needs >= 2")
    seeds = p["split_seeds"]
    if (not isinstance(seeds, list) or not 1 <= len(seeds) <= 10
            or any(type(s) is not int for s in seeds)
            or len(seeds) != len(set(seeds))):
        raise ValueError("Use 1..10 distinct integer split seeds")
    if (p["conditions"] != CONDITIONS or p["metric"] != "accuracy"
            or not isinstance(p["study_id"], str) or not p["study_id"]
            or p["selection_rule"] != "none; all conditions and seeds are fixed before evaluation"):
        raise ValueError("Conditions, metric and no-selection rule must stay explicit")


def generate_data(p):
    rng = random.Random(p["data_seed"])
    data = []
    for sample_id in range(p["n_samples"]):
        x0, x1 = rng.randint(-100, 100), rng.randint(-10000, 10000)
        label = int(x0 >= 0)
        if rng.randrange(p["label_flip_every"]) == 0:
            label = 1 - label
        data.append({"id": sample_id, "x": [x0, x1], "y": label})
    return data


def make_splits(p, seed):
    order = list(range(p["n_samples"]))
    random.Random(seed).shuffle(order)
    a, b = p["train_size"], p["train_size"] + p["validation_size"]
    return {"train": order[:a], "validation": order[a:b], "test": order[b:]}


def train_ranges(train):
    return [max(1, max(r["x"][j] for r in train)
                - min(r["x"][j] for r in train)) for j in range(2)]


def predict(train, query, ranges, condition):
    # Multiplying squared scaled distance by a shared positive denominator
    # preserves its order and keeps this two-feature example integer-only.
    # Tie-breaking by immutable sample ID makes ties explicit.
    def distance(row):
        d0, d1 = (query[j] - row["x"][j] for j in range(2))
        if condition == "raw_1nn":
            return d0 * d0 + d1 * d1
        if condition == "scaled_1nn":
            return d0 * d0 * ranges[1] ** 2 + d1 * d1 * ranges[0] ** 2
        if condition == "scaled_1nn_without_x0":
            return d1 * d1 * ranges[0] ** 2
        raise ValueError("Unknown condition")
    nearest = min(train, key=lambda row: (distance(row), row["id"]))
    return nearest["y"]


def evaluate(train, held_out, ranges, condition):
    predictions = [{"sample_id": row["id"], "target": row["y"],
                    "prediction": predict(train, row["x"], ranges, condition)}
                   for row in held_out]
    correct = sum(x["target"] == x["prediction"] for x in predictions)
    return {"n": len(predictions), "correct": correct,
            "accuracy": correct / len(predictions), "predictions": predictions}


def build_runs(p, data):
    runs = []
    for seed in p["split_seeds"]:
        splits = make_splits(p, seed)
        train = [data[i] for i in splits["train"]]
        ranges = train_ranges(train)
        conditions = []
        for condition in p["conditions"]:
            conditions.append({"condition": condition,
                "validation": evaluate(train, [data[i] for i in splits["validation"]], ranges, condition),
                "test": evaluate(train, [data[i] for i in splits["test"]], ranges, condition)})
        runs.append({"split_seed": seed, "splits": splits,
                     "train_feature_ranges": ranges, "conditions": conditions})
    return runs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=Path(__file__).with_name("protocol.json"))
    parser.add_argument("--output", type=Path, required=True,
                        help="New directory; existing paths are never overwritten")
    args = parser.parse_args()
    protocol_bytes = args.protocol.read_bytes()
    protocol = json.loads(protocol_bytes)
    validate_protocol(protocol)
    if args.output.exists() or args.output.is_symlink():
        raise ValueError("Output already exists; choose a new directory")
    data = generate_data(protocol)
    artifacts = {"protocol.json": protocol_bytes,
                 "dataset.json": json_bytes(data),
                 "runs.json": json_bytes(build_runs(protocol, data))}
    source_dir = Path(__file__).resolve().parent
    manifest = {"schema_version": 1,
                "artifact_sha256": {name: digest(content) for name, content in artifacts.items()},
                "source_sha256": {name: digest((source_dir / name).read_bytes())
                                  for name in ("run_demo.py", "verify_demo.py")},
                "environment": {"python": platform.python_version(),
                                "implementation": platform.python_implementation(),
                                "platform": platform.platform()}}
    # Creating without exist_ok is a final overwrite guard if another process
    # created the directory while the in-memory experiment was running.
    args.output.mkdir(parents=True, exist_ok=False)
    for name, content in artifacts.items():
        (args.output / name).write_bytes(content)
    (args.output / "manifest.json").write_bytes(json_bytes(manifest))
    print("Created 4 output files; %d seeds x %d conditions. No network or upstream code used."
          % (len(protocol["split_seeds"]), len(CONDITIONS)))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print("Demo failed: " + str(exc), file=sys.stderr)
        sys.exit(1)
