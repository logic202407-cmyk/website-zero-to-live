#!/usr/bin/env python3
"""Build and verify the local release using Python 3.10+ and the standard library.

Usage: python3 scripts/release.py {build,check}

The explicit allowlist below defines release inputs; Git state is irrelevant.
The archive omits repository-only .github files, dist, and root SHA256SUMS.
SHA256SUMS covers every release input, optional .github input, and both outputs,
excluding itself. Stored ZIP entries avoid zlib-version-dependent output bytes.
Neither command removes stale artifacts. Check performs no filesystem writes.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

SKILL_NAME = "website-zero-to-live"
ROOT_FILES = (
    ".gitattributes", ".gitignore", "CHANGELOG.md", "CONTRIBUTING.md", "LEGAL.md",
    "LICENSE", "README.md", "SECURITY.md", "SKILL.md", "THIRD_PARTY_NOTICES.md",
)
REQUIRED_FILES = tuple(name for name in ROOT_FILES if not name.startswith("."))
SOURCE_DIRS = ("agents", "assets", "docs", "references", "scripts", "tests")
IGNORED_PARTS = frozenset({
    ".git", ".pytest_cache", ".mypy_cache", ".ruff_cache", "__pycache__",
    "node_modules", ".DS_Store", "Thumbs.db",
})
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
FILE_MODE = stat.S_IFREG | 0o644
MANIFEST_NAME = "MANIFEST.json"
VERSION_RE = re.compile(
    r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?\Z"
)
SECRET_PATTERNS = (
    ("private key", re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{60,}\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("OpenAI-style token", re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{40,}\b")),
)


class ReleaseError(ValueError):
    """An invalid input or release; its message is safe to print."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReleaseError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(name: str) -> bool:
    """Accept only a normalized, relative POSIX file path."""
    return bool(name) and not any(ch in name for ch in "\\\x00\r\n:") and (
        not name.startswith("/") and not name.endswith("/")
        and all(part not in ("", ".", "..") for part in name.split("/"))
    )


def text_bytes(name: str, data: bytes) -> str:
    require(b"\r" not in data, f"{name}: CR/CRLF is forbidden; use LF line endings")
    require(not data.startswith(b"\xef\xbb\xbf"), f"{name}: UTF-8 BOM is forbidden")
    require(b"\x00" not in data, f"{name}: unexpected NUL byte")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ReleaseError(f"{name}: text must be UTF-8") from exc


def scalar(value: str, context: str) -> str:
    """Read the deliberately small scalar subset used by this skill's YAML."""
    value = value.strip()
    require(bool(value), f"{context}: expected a scalar value")
    if value.startswith('"'):
        try:
            result = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ReleaseError(f"{context}: invalid double-quoted scalar") from exc
        require(isinstance(result, str), f"{context}: expected a string")
        return result
    if value.startswith("'"):
        require(value.endswith("'") and len(value) >= 2, f"{context}: unclosed quote")
        return value[1:-1].replace("''", "'")
    require(not value.startswith(("[", "{", "&", "*", "!", "|", ">")),
            f"{context}: use a plain or quoted single-line scalar")
    return value.split(" #", 1)[0].strip()


def read_metadata(skill_text: str) -> dict[str, str]:
    lines = skill_text.splitlines()
    require(bool(lines) and lines[0] == "---", "SKILL.md: missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ReleaseError("SKILL.md: unclosed YAML frontmatter") from exc
    top: dict[str, str] = {}
    metadata: dict[str, str] = {}
    in_metadata = False
    seen_metadata = False
    for number, line in enumerate(lines[1:end], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"( {0,2})([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)", line)
        require(match is not None, f"SKILL.md:{number}: unsupported frontmatter syntax")
        indent, key, value = match.groups()
        if not indent:
            in_metadata = key == "metadata"
            if in_metadata:
                require(not seen_metadata and not value, "SKILL.md: invalid metadata mapping")
                seen_metadata = True
                continue
            target = top
        else:
            require(indent == "  " and in_metadata,
                    f"SKILL.md:{number}: only metadata supports two-space nesting")
            target = metadata
        require(key not in target, f"SKILL.md:{number}: duplicate key {key}")
        target[key] = scalar(value, f"SKILL.md:{number}")
    require(top.get("name") == SKILL_NAME, f"SKILL.md: name must be {SKILL_NAME}")
    require(1 <= len(top.get("description", "").strip()) <= 1024,
            "SKILL.md: description must contain 1–1024 characters")
    version = metadata.get("version", "")
    require(VERSION_RE.fullmatch(version) is not None,
            "SKILL.md: metadata.version must be a semantic version")
    require(top.get("license") == "MIT", "SKILL.md: license must be MIT")
    return {"skill": SKILL_NAME, "version": version, "license": "MIT"}


def collect_inputs(root: Path) -> tuple[dict[str, bytes], dict[str, bytes]]:
    """Return package inputs and repository-only inputs, rejecting symlinks."""
    package: dict[str, bytes] = {}
    repository: dict[str, bytes] = {}

    def add(path: Path, result: dict[str, bytes]) -> None:
        name = path.relative_to(root).as_posix()
        require(safe_path(name), f"Unsafe input path: {name!r}")
        require(not path.is_symlink(), f"Symlink inputs are forbidden: {name}")
        require(path.is_file(), f"Input is not a regular file: {name}")
        result[name] = path.read_bytes()

    def walk(directory: Path, result: dict[str, bytes]) -> None:
        require(not directory.is_symlink(), f"Symlink directory is forbidden: {directory.name}")
        require(directory.is_dir(), f"Expected an input directory: {directory.name}")
        for child in sorted(directory.iterdir()):
            if child.name in IGNORED_PARTS or child.suffix in (".pyc", ".pyo"):
                continue
            require(not child.is_symlink(), f"Symlink inputs are forbidden: {child.relative_to(root)}")
            if child.is_dir():
                walk(child, result)
            else:
                add(child, result)

    for name in ROOT_FILES:
        path = root / name
        if name in REQUIRED_FILES:
            require(path.exists(), f"Missing required release file: {name}")
        if path.exists() or path.is_symlink():
            add(path, package)
    for name in SOURCE_DIRS:
        path = root / name
        require(path.exists(), f"Missing required source directory: {name}")
        walk(path, package)
    github = root / ".github"
    if github.exists() or github.is_symlink():
        walk(github, repository)
    for name in ("scripts/release.py", "tests/test_release.py", "agents/openai.yaml"):
        require(name in package, f"Missing required release file: {name}")
    return dict(sorted(package.items())), dict(sorted(repository.items()))


def release_names(metadata: dict[str, str]) -> tuple[str, str]:
    archive = f"dist/{metadata['skill']}-{metadata['version']}.zip"
    return archive, archive + ".sha256"


def unfenced_markdown(name: str, text: str) -> str:
    """Check backtick/tilde fence balance, returning prose for link checks."""
    fence: tuple[str, int, int] | None = None
    output: list[str] = []
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= fence[1] and not match[2].strip():
                fence = None
            output.append("")
        elif match:
            require(not (match[1][0] == "`" and "`" in match[2]),
                    f"{name}:{number}: invalid backtick fence info string")
            fence = (match[1][0], len(match[1]), number)
            output.append("")
        else:
            output.append(line)
    require(fence is None, f"{name}: unclosed Markdown fence" + (f" at line {fence[2]}" if fence else ""))
    # Code spans can contain Markdown-looking examples; do not follow those.
    return re.sub(r"(`+).*?\1(?!`)", "", "\n".join(output), flags=re.DOTALL)


def validate_links(root: Path, name: str, prose: str, generated: set[str]) -> None:
    references: dict[str, str] = {}
    targets: list[str] = []
    for match in re.finditer(r"^ {0,3}\[([^\]\n]+)\]:\s*(<[^>\n]+>|\S+)", prose, re.MULTILINE):
        references[" ".join(match[1].split()).casefold()] = match[2]
        targets.append(match[2])
    for match in re.finditer(
        r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|(?:\\.|[^\s()]|\([^()\n]*\))+)(?:\s+[^\n]*?)?\s*\)", prose
    ):
        targets.append(match[1])
    for match in re.finditer(r"!?\[([^\]\n]+)\]\[([^\]\n]*)\]", prose):
        key = " ".join((match[2] or match[1]).split()).casefold()
        require(key in references, f"{name}: undefined Markdown link reference [{key}]")
    targets.extend(match[2] for match in re.finditer(r"\b(?:href|src)\s*=\s*(['\"])(.*?)\1", prose))
    for target in targets:
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        target = re.sub(r"\\([()\[\] ])", r"\1", target)
        try:
            parsed = urlsplit(target)
        except ValueError as exc:
            raise ReleaseError(f"{name}: malformed link {target!r}") from exc
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue  # External URLs, same-document anchors, and queries are not fetched.
        path = unquote(parsed.path)
        require(not path.startswith(("/", "\\")), f"{name}: non-portable absolute file link {target!r}")
        candidate = (root / PurePosixPath(name).parent / path).resolve()
        try:
            relative = candidate.relative_to(root.resolve()).as_posix()
        except ValueError as exc:
            raise ReleaseError(f"{name}: file link escapes repository: {target!r}") from exc
        require(candidate.exists() or relative in generated, f"{name}: broken file link {target!r}")


def validate_inputs(root: Path, package: dict[str, bytes], repository: dict[str, bytes]) -> dict[str, str]:
    require(not (root / "dist").is_symlink(), "dist must not be a symlink")
    texts = {name: text_bytes(name, data) for name, data in (package | repository).items()}
    metadata = read_metadata(texts["SKILL.md"])
    license_text = texts["LICENSE"]
    require("MIT License" in license_text and "Permission is hereby granted, free of charge" in license_text
            and "THE SOFTWARE IS PROVIDED" in license_text,
            "LICENSE: expected the MIT license text")
    generated = set(release_names(metadata)) | {"SHA256SUMS"}
    for name, text in texts.items():
        for label, pattern in SECRET_PATTERNS:
            require(pattern.search(text) is None, f"{name}: possible {label}; review before release")
        if name.lower().endswith(".md"):
            validate_links(root, name, unfenced_markdown(name, text), generated)
    return metadata


def manifest_bytes(package: dict[str, bytes], metadata: dict[str, str]) -> bytes:
    manifest = dict(metadata, files={name: sha256(data) for name, data in sorted(package.items())})
    return (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def make_archive(package: dict[str, bytes], metadata: dict[str, str]) -> bytes:
    members = package | {MANIFEST_NAME: manifest_bytes(package, metadata)}
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED, allowZip64=False) as archive:
        for name, data in sorted(members.items()):
            entry = zipfile.ZipInfo(f"{metadata['skill']}/{name}", date_time=FIXED_TIME)
            entry.create_system = 3
            entry.external_attr = FILE_MODE << 16
            entry.compress_type = zipfile.ZIP_STORED
            archive.writestr(entry, data)
    return buffer.getvalue()


def check_dist(root: Path, expected: set[str], require_outputs: bool) -> None:
    dist = root / "dist"
    require(not dist.is_symlink(), "dist must not be a symlink")
    if not dist.exists():
        require(not require_outputs, "Missing dist directory; run build first")
        return
    require(dist.is_dir(), "dist must be a directory")
    actual = {entry.relative_to(root).as_posix() for entry in dist.iterdir()}
    unexpected = actual - expected
    require(not unexpected, "Unexpected/stale dist entries; remove them explicitly: " + ", ".join(sorted(unexpected)))
    if require_outputs:
        require(actual == expected, "Missing release output(s): " + ", ".join(sorted(expected - actual)))
    for name in actual:
        require(not (root / name).is_symlink() and (root / name).is_file(),
                f"Release output must be a regular file: {name}")


def checksums_bytes(inputs: dict[str, bytes]) -> bytes:
    return "".join(f"{sha256(data)}  {name}\n" for name, data in sorted(inputs.items())).encode("utf-8")


def check_archive(data: bytes, package: dict[str, bytes], metadata: dict[str, str]) -> None:
    prefix = metadata["skill"] + "/"
    expected_members = {prefix + name for name in package} | {prefix + MANIFEST_NAME}
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()
            names = [entry.filename for entry in entries]
            for name in names:
                require(safe_path(name) and name.startswith(prefix), f"Unsafe ZIP member: {name!r}")
            require(len(names) == len(set(names)), "ZIP contains duplicate member names")
            require(set(names) == expected_members, "ZIP member set differs from release inputs")
            require(names == sorted(names), "ZIP members are not in deterministic sorted order")
            require(not archive.comment, "ZIP archive comment must be empty")
            for entry in entries:
                require(entry.date_time == FIXED_TIME and entry.create_system == 3
                        and entry.external_attr == FILE_MODE << 16
                        and entry.compress_type == zipfile.ZIP_STORED
                        and not entry.extra and not entry.comment and not entry.flag_bits & 1,
                        f"ZIP member metadata is not canonical: {entry.filename}")
                name = entry.filename[len(prefix):]
                expected = manifest_bytes(package, metadata) if name == MANIFEST_NAME else package[name]
                require(entry.file_size == len(expected), f"ZIP member size mismatch: {name}")
                actual = archive.read(entry)  # Also checks each member's CRC.
                require(actual == expected, f"ZIP member content/hash mismatch: {name}")
            # Exact canonical JSON validates metadata, hashes, and nonrecursive file membership.
            actual_manifest = archive.read(prefix + MANIFEST_NAME)
            require(actual_manifest == manifest_bytes(package, metadata), "MANIFEST.json is not canonical")
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError, OSError) as exc:
        raise ReleaseError(f"Invalid/corrupt ZIP: {exc}") from exc
    require(data == make_archive(package, metadata), "ZIP bytes differ from deterministic build")


def build(root: Path) -> None:
    package, repository = collect_inputs(root)
    metadata = validate_inputs(root, package, repository)
    archive_name, sidecar_name = release_names(metadata)
    check_dist(root, {archive_name, sidecar_name}, require_outputs=False)
    checksum_path = root / "SHA256SUMS"
    require(not checksum_path.is_symlink(), "SHA256SUMS must not be a symlink")
    require(not checksum_path.exists() or checksum_path.is_file(), "SHA256SUMS must be a regular file")
    archive = make_archive(package, metadata)
    sidecar = f"{sha256(archive)}  {PurePosixPath(archive_name).name}\n".encode("utf-8")
    sums = checksums_bytes(package | repository | {archive_name: archive, sidecar_name: sidecar})
    (root / "dist").mkdir(exist_ok=True)
    (root / archive_name).write_bytes(archive)
    (root / sidecar_name).write_bytes(sidecar)
    checksum_path.write_bytes(sums)
    check(root)


def check(root: Path) -> None:
    package, repository = collect_inputs(root)
    metadata = validate_inputs(root, package, repository)
    archive_name, sidecar_name = release_names(metadata)
    check_dist(root, {archive_name, sidecar_name}, require_outputs=True)
    archive = (root / archive_name).read_bytes()
    check_archive(archive, package, metadata)
    sidecar = (root / sidecar_name).read_bytes()
    require(sidecar == f"{sha256(archive)}  {PurePosixPath(archive_name).name}\n".encode("utf-8"),
            "ZIP SHA256 sidecar mismatch")
    checksum_path = root / "SHA256SUMS"
    require(checksum_path.is_file() and not checksum_path.is_symlink(), "Missing/unsafe root SHA256SUMS")
    expected = checksums_bytes(package | repository | {archive_name: archive, sidecar_name: sidecar})
    require(checksum_path.read_bytes() == expected,
            "Root SHA256SUMS differs: checksums, ordering, or full file coverage is invalid")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("build", "check"))
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    try:
        {"build": build, "check": check}[args.command](root)
    except (ReleaseError, OSError, zipfile.LargeZipFile) as exc:
        print(f"release {args.command} failed: {exc}", file=sys.stderr)
        return 1
    print(f"release {args.command}: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
