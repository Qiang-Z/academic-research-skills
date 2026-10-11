#!/usr/bin/env python3
"""Verify the delivered file allowlist, checksums and pinned upstream files.

Uses Python standard library only. Does not execute upstream code or use network.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


def digest(path):
    # type: (Path) -> str
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_file(root, rel):
    # type: (Path, str) -> Path
    p = PurePosixPath(rel)
    if not rel or p.is_absolute() or ".." in p.parts or ".git" in p.parts:
        raise ValueError("Unsafe manifest path: " + rel)
    full = root.joinpath(*p.parts)
    if not full.is_file() or full.is_symlink():
        raise ValueError("Missing or non-regular file: " + rel)
    try:
        full.resolve().relative_to(root.resolve())
    except ValueError:
        raise ValueError("Path leaves repository: " + rel)
    return full


def verify_hashes(root, checksum_name):
    # type: (Path, str) -> int
    count = 0
    seen = set()
    for line in (root / checksum_name).read_text(encoding="utf-8").splitlines():
        expected, rel = line.split("  ", 1)
        if rel in seen or len(expected) != 64:
            raise ValueError("Invalid or duplicate checksum entry: " + rel)
        seen.add(rel)
        if digest(safe_file(root, rel)) != expected:
            raise ValueError("SHA-256 mismatch: " + rel)
        count += 1
    return count


def main():
    root = Path(__file__).resolve().parent.parent
    names = (root / "PUBLISH_FILES.txt").read_text(encoding="utf-8").splitlines()
    if len(names) != len(set(names)):
        raise ValueError("Publish allowlist contains duplicate paths")
    for rel in names:
        safe_file(root, rel)
    actual = set()
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if ".git" in rel.parts:
            continue
        if p.is_symlink():
            raise ValueError("Symbolic link found: " + str(rel))
        if p.is_file():
            actual.add(rel.as_posix())
    if actual != set(names):
        extra = sorted(actual - set(names))
        missing = sorted(set(names) - actual)
        raise ValueError("Files differ from allowlist. Extra=%r Missing=%r" % (extra[:8], missing[:8]))
    checked = verify_hashes(root, "SHA256SUMS.txt")
    registry = json.loads((root / "MODULES.json").read_text(encoding="utf-8"))
    upstream = 0
    for module in registry["modules"]:
        base = root / module["path"]
        manifest = json.loads(safe_file(root, module["manifest"]).read_text(encoding="utf-8"))
        for source in manifest["sources"]:
            source_root = base / source["bundle_relative_path"]
            for item in source["files"]:
                p = safe_file(source_root, item["path"])
                if digest(p) != item["sha256"]:
                    raise ValueError("Pinned upstream file mismatch: " + str(p.relative_to(root)))
                upstream += 1
    print("Verification OK: %d allowlisted files, %d checksums, %d upstream files." % (len(names), checked, upstream))
    print("No upstream code was executed. GitHub publication status was not checked.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        print("Verification failed: %s" % exc, file=sys.stderr)
        sys.exit(1)
