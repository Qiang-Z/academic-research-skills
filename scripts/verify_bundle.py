#!/usr/bin/env python3
"""Verify the delivered allowlist, checksums, registry and pinned sources.

Uses Python standard library only. Does not execute upstream code or use network.
Only Git internals and named Baidu upload markers are outside the publish bundle.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_path(root, base, rel, directory=False, allow_parent=False):
    """Resolve module references inside root, without symlinks or drive paths."""
    if not isinstance(rel, str) or not rel or "\\" in rel or ":" in rel:
        raise ValueError("Unsafe manifest path: " + str(rel))
    parts = PurePosixPath(rel)
    if (not parts.parts or parts.is_absolute() or ".git" in parts.parts
            or (not allow_parent and ".." in parts.parts)):
        raise ValueError("Unsafe manifest path: " + rel)
    full = base.joinpath(*parts.parts)
    if any(p.is_symlink() for p in (full, *full.parents)):
        raise ValueError("Symbolic link in manifest path: " + rel)
    resolved = full.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        raise ValueError("Path leaves repository: " + rel)
    exists = resolved.is_dir() if directory else resolved.is_file()
    if not exists:
        raise ValueError("Missing or non-regular path: " + rel)
    return resolved


def safe_file(root, rel):
    return safe_path(root, root, rel)


def verify_hashes(root, checksum_name, names):
    seen = set()
    for line in (root / checksum_name).read_text(encoding="utf-8").splitlines():
        expected, rel = line.split("  ", 1)
        if (rel in seen or len(expected) != 64
                or any(c not in "0123456789abcdef" for c in expected)):
            raise ValueError("Invalid or duplicate checksum entry: " + rel)
        seen.add(rel)
        if digest(safe_file(root, rel)) != expected:
            raise ValueError("SHA-256 mismatch: " + rel)
    if seen != set(names) - {checksum_name}:
        raise ValueError("Checksum coverage differs from publish allowlist")
    return len(seen)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_by_id(manifest, source_id):
    matches = [s for s in manifest["sources"] if s["id"] == source_id]
    if len(matches) != 1:
        raise ValueError("Source ID is missing or ambiguous: " + source_id)
    return matches[0]


def verify_modules(root, registry):
    ids = [m["id"] for m in registry["modules"] + registry["planned_modules"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate module ID in curated/planned registry")
    for module in registry["planned_modules"]:
        if module["status"] != "planned":
            raise ValueError("Invalid planned module status: " + module["id"])
    loaded = []
    for module in registry["modules"]:
        if module["status"] != "curated":
            raise ValueError("Invalid curated module status: " + module["id"])
        base = safe_path(root, root, module["path"], directory=True)
        for field in ("readme", "skill_index", "manifest"):
            entry = safe_file(root, module[field])
            try:
                entry.relative_to(base)
            except ValueError:
                raise ValueError("Module entry leaves its module: " + module[field])
        manifest_path = safe_file(root, module["manifest"])
        manifest = read_json(manifest_path)
        if manifest["module_id"] != module["id"]:
            raise ValueError("Module ID differs from source manifest")
        source_ids = [s["id"] for s in manifest["sources"]]
        if not source_ids or len(source_ids) != len(set(source_ids)):
            raise ValueError("Missing or duplicate sources: " + module["id"])
        loaded.append((base, manifest_path, manifest))
    registered = {p: manifest for _, p, manifest in loaded}
    unique_files = set()
    reused_references = 0
    for base, manifest_path, manifest in loaded:
        reference_module = manifest.get("collection_mode") == "reference-existing-snapshots"
        for source in manifest["sources"]:
            reused = "reused_from_manifest" in source
            if reference_module != reused:
                raise ValueError("Source reuse metadata disagrees with collection mode")
            source_root = safe_path(root, base, source["bundle_relative_path"],
                                    directory=True, allow_parent=reused)
            originals = None
            if reused:
                origin_path = safe_path(root, base, source["reused_from_manifest"],
                                        allow_parent=True)
                if origin_path == manifest_path or origin_path not in registered:
                    raise ValueError("Reused source must refer to another registered module")
                origin = source_by_id(registered[origin_path], source["reused_source_id"])
                if "reused_from_manifest" in origin:
                    raise ValueError("Reused source must point directly to a preserved snapshot")
                for field in ("repository", "branch", "commit"):
                    if source[field] != origin[field]:
                        raise ValueError("Reused source metadata mismatch: " + field)
                origin_root = safe_path(root, origin_path.parent,
                                        origin["bundle_relative_path"], directory=True)
                if source_root != origin_root:
                    raise ValueError("Reused source directory differs from original snapshot")
                originals = {item["path"]: item for item in origin["files"]}
                if len(originals) != len(origin["files"]):
                    raise ValueError("Duplicate file paths in original source")
            paths = set()
            if not source["files"]:
                raise ValueError("Source has no pinned files: " + source["id"])
            for item in source["files"]:
                rel = item["path"]
                if rel in paths:
                    raise ValueError("Duplicate source file: " + rel)
                paths.add(rel)
                if originals is not None:
                    original = originals.get(rel)
                    if original is None or item["sha256"] != original["sha256"]:
                        raise ValueError("Reused file differs from original manifest: " + rel)
                    for field in ("bytes", "git_blob_sha1", "mode"):
                        if field in item and item[field] != original.get(field):
                            raise ValueError("Reused file metadata mismatch: " + rel)
                    reused_references += 1
                p = safe_file(source_root, rel)
                if digest(p) != item["sha256"]:
                    raise ValueError("Pinned upstream file mismatch: " + str(p.relative_to(root)))
                unique_files.add(p)
    return len(unique_files), reused_references


def is_upload_marker(path):
    return path.name.startswith(".") and path.name.endswith(".baiduyun.uploading.cfg")


def main():
    root = Path(__file__).resolve().parent.parent
    names = (root / "PUBLISH_FILES.txt").read_text(encoding="utf-8").splitlines()
    if len(names) != len(set(names)):
        raise ValueError("Publish allowlist contains duplicate paths")
    for rel in names:
        p = safe_file(root, rel)
        if is_upload_marker(p):
            raise ValueError("Local upload marker must not be published: " + rel)
    actual = set()
    ignored = 0
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if ".git" in rel.parts:
            continue
        if p.is_symlink():
            raise ValueError("Symbolic link found: " + str(rel))
        if p.is_file():
            if is_upload_marker(p):
                ignored += 1
            else:
                actual.add(rel.as_posix())
    if actual != set(names):
        extra = sorted(actual - set(names))
        missing = sorted(set(names) - actual)
        raise ValueError("Files differ from allowlist. Extra=%r Missing=%r" % (extra[:8], missing[:8]))
    checked = verify_hashes(root, "SHA256SUMS.txt", names)
    upstream, reused = verify_modules(root, read_json(root / "MODULES.json"))
    print("Verification OK: %d allowlisted files, %d checksums, %d unique upstream files, %d reused file references." % (len(names), checked, upstream, reused))
    print("Ignored %d local Baidu upload markers; none are published." % ignored)
    print("This integrity verifier did not execute upstream code. GitHub publication status was not checked.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("Verification failed: %s" % exc, file=sys.stderr)
        sys.exit(1)
