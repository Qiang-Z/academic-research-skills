#!/usr/bin/env python3
"""Repeat bounded CPU checks; writes only to a NEW output directory.

This authored test harness does not install or run ARIS, connect to a service,
or validate a published research claim. Exit 2 means a recorded behavioral defect.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() or output.is_symlink():
        parser.error("Output must be a new directory")
    here = Path(__file__).resolve().parent
    root = here.parents[3]
    example = root / "modules/experiment-design/examples/toy-reproducibility"
    run, verify = example / "run_demo.py", example / "verify_demo.py"
    plan_files = [here / name for name in ("EXPERIMENT_PLAN.md", "ABLATION_PLAN.md")]
    if not all(p.is_file() for p in plan_files):
        parser.error("Freeze the two plan documents before running")
    source_files = [run, verify, example / "protocol.json", Path(__file__), *plan_files]
    source_hashes = {p.relative_to(root).as_posix(): sha(p) for p in source_files}
    output.mkdir(parents=True, exist_ok=False)
    report = {
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "authored CPU fixture; no upstream execution in this harness",
        "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                        "platform": platform.platform(), "dependencies": "Python standard library only"},
        "source_sha256": source_hashes, "tests": [],
    }

    def clean(value):
        for original, replacement in ((str(output), "<OUTPUT>"), (str(root), "<REPO>"), (sys.executable, "<PYTHON>")):
            value = value.replace(original, replacement).replace(original.replace("\\", "/"), replacement)
        return value

    def invoke(test_id, arguments, expected_code, marker):
        command = [sys.executable, "-B", "-X", "utf8", *map(str, arguments)]
        started = time.monotonic()
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        timed_out = False
        try:
            stdout, stderr = proc.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            timed_out = True
        passed = not timed_out and proc.returncode == expected_code and marker in stdout + stderr
        report["tests"].append({"id": test_id, "command_argv": [clean(x) for x in command],
            "pid": proc.pid, "elapsed_seconds": round(time.monotonic() - started, 4),
            "expected_exit": expected_code, "expected_message": marker, "exit_code": proc.returncode,
            "timed_out": timed_out, "stdout": clean(stdout), "stderr": clean(stderr),
            "result": "PASS" if passed else "FAIL"})
        return passed

    a, b = output / "run-a", output / "run-b"
    assert invoke("run-a", [run, "--output", a], 0, "3 seeds x 3 conditions")
    assert invoke("run-b", [run, "--output", b], 0, "3 seeds x 3 conditions")
    assert invoke("verify-a", [verify, a], 0, "PASS:")
    assert invoke("compare-rerun", [verify, a, "--compare", b], 0, "byte-identical")
    assert invoke("reject-existing-output", [run, "--output", a], 1, "Output already exists")
    assert invoke("reject-same-directory-compare", [verify, a, "--compare", a], 1, "two different directories")
    protocol = json.loads((example / "protocol.json").read_bytes())
    for name, change, marker in (
        ("invalid-split", {"train_size": 240}, "All three splits must be nonempty"),
        ("duplicate-seeds", {"split_seeds": [11, 11]}, "distinct integer split seeds"),
    ):
        bad_protocol = output / (name + ".json")
        write_json(bad_protocol, {**protocol, **change})
        assert invoke("reject-" + name, [run, "--protocol", bad_protocol, "--output", output / name], 1, marker)
        assert not (output / name).exists()
    missing = output / "missing-artifact"
    shutil.copytree(a, missing)
    (missing / "runs.json").unlink()
    assert invoke("reject-missing-artifact", [verify, missing], 1, "missing output files")
    tampered = output / "tampered-metric"
    shutil.copytree(a, tampered)
    bad_runs = json.loads((tampered / "runs.json").read_bytes())
    bad_runs[0]["conditions"][0]["test"]["accuracy"] = 1.0
    write_json(tampered / "runs.json", bad_runs)
    manifest = json.loads((tampered / "manifest.json").read_bytes())
    manifest["artifact_sha256"]["runs.json"] = sha(tampered / "runs.json")
    write_json(tampered / "manifest.json", manifest)
    assert invoke("reject-metric-after-rehash", [verify, tampered], 1, "Metric mismatch")

    # Independent rational-distance calculation; does not import the demo.
    data = json.loads((a / "dataset.json").read_bytes())
    runs = json.loads((a / "runs.json").read_bytes())
    checked = 0
    metrics = []
    for record in runs:
        train = [data[i] for i in record["splits"]["train"]]
        scale = [max(1, max(p["x"][j] for p in train) - min(p["x"][j] for p in train)) for j in (0, 1)]
        for condition in record["conditions"]:
            for part in ("validation", "test"):
                result = condition[part]
                correct = 0
                for item in result["predictions"]:
                    query = data[item["sample_id"]]
                    name = condition["condition"]
                    def distance(row):
                        differences = [query["x"][j] - row["x"][j] for j in (0, 1)]
                        if name == "raw_1nn":
                            return sum(x*x for x in differences)
                        dimensions = (1,) if name == "scaled_1nn_without_x0" else (0, 1)
                        return sum(Fraction(differences[j], scale[j]) ** 2 for j in dimensions)
                    nearest = min(train, key=lambda row: (distance(row), row["id"]))
                    assert nearest["y"] == item["prediction"]
                    assert item["target"] == query["y"]
                    correct += nearest["y"] == query["y"]
                    checked += 1
                assert result["correct"] == correct and result["accuracy"] == correct / len(result["predictions"])
                metrics.append({"seed": record["split_seed"], "condition": condition["condition"], "split": part,
                                "correct": correct, "n": len(result["predictions"]), "accuracy": result["accuracy"]})
    report["independent_recalculation"] = {"result": "PASS", "prediction_count": checked, "method": "fractions.Fraction distance; no demo import", "metrics": metrics}
    report["artifact_sha256"] = {name: {p.name: sha(p) for p in folder.iterdir()} for name, folder in (("run-a", a), ("run-b", b))}

    # Exploratory schema-type probe, beyond the frozen primary protocol.
    boolean_protocol = output / "boolean-schema.json"
    write_json(boolean_protocol, {**protocol, "schema_version": True})
    invoke("reject-boolean-schema", [run, "--protocol", boolean_protocol, "--output", output / "boolean-schema"], 1, "schema version")
    if (output / "boolean-schema").is_dir():
        invoke("reject-boolean-schema-artifact", [verify, output / "boolean-schema"], 1, "schema version")
    report["source_files_unchanged"] = source_hashes == {p.relative_to(root).as_posix(): sha(p) for p in source_files}
    assert report["source_files_unchanged"]
    report["summary"] = {"process_checks": len(report["tests"]), "passed": sum(t["result"] == "PASS" for t in report["tests"]), "failed": sum(t["result"] == "FAIL" for t in report["tests"])}
    write_json(output / "cpu-results.json", report)
    print(json.dumps(report["summary"]))
    print("Independent predictions verified:", checked)
    print("Reports written to the requested new output directory.")
    return 2 if report["summary"]["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
