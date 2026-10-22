#!/usr/bin/env python3
"""Check the original teaching analysis, its inputs, and an optional independent rerun."""
import argparse
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import analyze_demo as analysis


def check_directory(input_dir, output_dir):
    require = analysis.require
    require(output_dir.is_dir() and not output_dir.is_symlink(), "Expected a regular analysis directory")
    names = analysis.ARTIFACTS | {"manifest.json"}
    require({p.name for p in output_dir.iterdir()} == names, "Unexpected or missing analysis files")
    for name in names:
        path = output_dir / name
        require(path.is_file() and not path.is_symlink(), "Expected regular analysis file: " + name)
    contents = {name: (output_dir / name).read_bytes() for name in names}
    objects = {name: analysis.strict_json(content) for name, content in contents.items()}
    manifest = objects["manifest.json"]
    analysis.exact_keys(manifest, {"schema_version", "artifact_sha256", "input_artifact_sha256",
                                 "input_source_sha256", "source_sha256", "environment"}, "analysis manifest")
    require(type(manifest["schema_version"]) is int and manifest["schema_version"] == 1, "Unsupported output schema")
    analysis.exact_keys(manifest["environment"], {"python", "implementation", "platform"}, "analysis environment")
    require(all(isinstance(v, str) and v for v in manifest["environment"].values()), "Invalid analysis environment")
    require(manifest["artifact_sha256"] == {name: analysis.digest(contents[name]) for name in analysis.ARTIFACTS},
            "Analysis artifact hash mismatch or incomplete coverage")
    require(manifest["source_sha256"] == {name: analysis.digest((analysis.SOURCE_DIR / name).read_bytes())
                                           for name in analysis.SOURCE_FILES}, "Analysis source version differs")
    raw_input, input_objects = analysis.load_input(input_dir)
    require(manifest["input_artifact_sha256"] == {name: analysis.digest(content) for name, content in raw_input.items()},
            "Input hashes differ from analyzed input")
    require(contents["input_manifest.json"] == raw_input["manifest.json"], "Input manifest snapshot differs")
    require(manifest["input_source_sha256"] == input_objects["manifest.json"]["source_sha256"], "Input source hashes differ")
    protocol = objects["analysis_protocol.json"]
    analysis.validate_protocol(protocol)
    require(contents["analysis.json"] == analysis.json_bytes(analysis.build_analysis(input_objects, protocol)),
            "Analysis differs from recomputed paired statistics")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--compare", type=Path, help="A different independently generated analysis directory")
    args = parser.parse_args()
    first = check_directory(args.input, args.output)
    if args.compare:
        analysis.require(args.output.resolve() != args.compare.resolve(), "Comparison needs different directories")
        second = check_directory(args.input, args.compare)
        analysis.require(first["input_artifact_sha256"] == second["input_artifact_sha256"]
                         and first["source_sha256"] == second["source_sha256"], "Comparison sources differ")
        for name in analysis.ARTIFACTS:
            analysis.require((args.output / name).read_bytes() == (args.compare / name).read_bytes(),
                             "Independent analysis rerun differs: " + name)
        print("PASS: input, protocol, paired analysis and bootstrap distribution are byte-identical across two outputs.")
    else:
        print("PASS: original input, analysis hashes, protocol, pairing and recomputed statistics checked.")
    print("This verifies local teaching artifacts, not upstream workflows or population-level scientific claims.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, IndexError, ZeroDivisionError, OverflowError, AttributeError) as exc:
        print("Verification failed: " + str(exc), file=sys.stderr)
        sys.exit(1)
