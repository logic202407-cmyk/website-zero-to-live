"""Isolated release-tool tests; never build or edit the real repository's dist."""
from __future__ import annotations

import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
import zipfile

# Keep test execution free of bytecode-cache side effects in the checkout.
sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location("release", Path(__file__).resolve().parents[1] / "scripts" / "release.py")
assert SPEC and SPEC.loader
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="website-release-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in release.ROOT_FILES:
            self.write(name, "# Release fixture\n")
        for name in release.SOURCE_DIRS:
            (self.root / name).mkdir()
        self.write("SKILL.md", """---
name: website-zero-to-live
description: "A test skill."
license: MIT
metadata:
  version: "1.1.2"
---

# Test skill

[Usage](docs/usage.md#intro)
""")
        self.write("LICENSE", "MIT License\nPermission is hereby granted, free of charge\nTHE SOFTWARE IS PROVIDED\n")
        self.write("README.md", "[Skill](SKILL.md)\n[Download](dist/website-zero-to-live-1.1.2.zip)\n")
        self.write("scripts/release.py", "# Fixture release script\n")
        self.write("tests/test_release.py", "# Fixture test module\n")
        self.write("agents/openai.yaml", 'interface:\n  display_name: "Test"\n')
        self.write("assets/template.md", "# Template\n")
        self.write("references/example.md", "# Reference\n")
        self.write("docs/usage.md", "# Usage\n\n```text\n[Ignored example](missing.md)\n```\n")
        self.write(".github/workflows/validate.yml", "name: Validate\n")
        self.archive_name = "dist/website-zero-to-live-1.1.2.zip"
        self.archive = self.root / self.archive_name

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8") if isinstance(text, str) else text)

    def read_outputs(self):
        return {name: (self.root / name).read_bytes() for name in (
            self.archive_name, self.archive_name + ".sha256", "SHA256SUMS"
        )}

    def rewrite_archive(self, transform):
        with zipfile.ZipFile(self.archive) as archive:
            entries = [(entry, archive.read(entry)) for entry in archive.infolist()]
        result = io.BytesIO()
        with zipfile.ZipFile(result, "w", compression=zipfile.ZIP_STORED) as archive:
            for entry, data in transform(entries):
                archive.writestr(entry, data)
        self.archive.write_bytes(result.getvalue())

    def assert_check_fails(self, expected):
        with self.assertRaisesRegex(release.ReleaseError, expected):
            release.check(self.root)

    def test_deterministic_outputs_ignore_mtime_and_mode(self):
        release.build(self.root)
        first = self.read_outputs()
        for path in self.root.rglob("*"):
            if path.is_file():
                os.utime(path, (1_700_000_000, 1_700_000_000))
                path.chmod(0o600)
        release.build(self.root)
        self.assertEqual(first, self.read_outputs())
        release.check(self.root)

    def test_manifest_members_and_checksum_coverage(self):
        self.write(".git/config", "ignored repository internals\n")
        self.write("scripts/__pycache__/ignored.pyc", b"\x00\xff")
        release.build(self.root)
        package, repository = release.collect_inputs(self.root)
        with zipfile.ZipFile(self.archive) as archive:
            manifest = json.loads(archive.read("website-zero-to-live/MANIFEST.json"))
            self.assertEqual(manifest["skill"], "website-zero-to-live")
            self.assertEqual(manifest["version"], "1.1.2")
            self.assertEqual(manifest["license"], "MIT")
            self.assertEqual(manifest["files"], {name: release.sha256(data) for name, data in package.items()})
            self.assertEqual(set(archive.namelist()), {"website-zero-to-live/" + name for name in package} | {"website-zero-to-live/MANIFEST.json"})
            for entry in archive.infolist():
                self.assertEqual(entry.date_time, release.FIXED_TIME)
                self.assertEqual(entry.external_attr >> 16, stat.S_IFREG | 0o644)
                self.assertEqual(entry.compress_type, zipfile.ZIP_STORED)
        sums = (self.root / "SHA256SUMS").read_text()
        self.assertIn("  .github/workflows/validate.yml\n", sums)
        self.assertNotIn(".git/config", sums)
        self.assertNotIn("__pycache__", sums)
        self.assertNotIn("  SHA256SUMS\n", sums)
        self.assertEqual(len(sums.splitlines()), len(package) + len(repository) + 2)

    def test_check_does_not_mutate_files(self):
        release.build(self.root)
        def snapshot():
            return {path.relative_to(self.root).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
                    for path in self.root.rglob("*") if path.is_file()}
        before = snapshot()
        release.check(self.root)
        self.assertEqual(snapshot(), before)

    def test_missing_license_fails(self):
        (self.root / "LICENSE").unlink()
        with self.assertRaisesRegex(release.ReleaseError, "Missing required release file: LICENSE"):
            release.build(self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_missing_required_source_fails(self):
        (self.root / "agents/openai.yaml").unlink()
        with self.assertRaisesRegex(release.ReleaseError, "Missing required release file: agents/openai.yaml"):
            release.build(self.root)

    def test_missing_manifest_input_is_detected(self):
        release.build(self.root)
        (self.root / "assets/template.md").unlink()
        self.assert_check_fails("member set differs")

    def test_changed_source_is_detected(self):
        release.build(self.root)
        self.write("assets/template.md", "# Changed!\n")
        self.assert_check_fails("member (?:size|content/hash) mismatch")

    def test_missing_license_metadata_fails(self):
        skill = (self.root / "SKILL.md").read_text().replace("license: MIT\n", "")
        self.write("SKILL.md", skill)
        with self.assertRaisesRegex(release.ReleaseError, "license must be MIT"):
            release.build(self.root)

    def test_invalid_version_fails(self):
        skill = (self.root / "SKILL.md").read_text().replace('"1.1.2"', '"../../escape"')
        self.write("SKILL.md", skill)
        with self.assertRaisesRegex(release.ReleaseError, "semantic version"):
            release.build(self.root)

    def test_corrupt_zip_is_detected(self):
        release.build(self.root)
        self.archive.write_bytes(self.archive.read_bytes()[:40])
        self.assert_check_fails("Invalid/corrupt ZIP")

    def test_crc_corruption_is_detected(self):
        release.build(self.root)
        data = self.archive.read_bytes()
        self.assertIn(b"# Template\n", data)
        self.archive.write_bytes(data.replace(b"# Template\n", b"# TemplatX\n", 1))
        self.assert_check_fails("Invalid/corrupt ZIP")

    def test_member_tamper_is_detected(self):
        release.build(self.root)
        self.rewrite_archive(lambda entries: [
            (entry, b"# TemplatX\n" if entry.filename.endswith("assets/template.md") else data)
            for entry, data in entries
        ])
        self.assert_check_fails("content/hash mismatch")

    def test_manifest_tamper_is_detected(self):
        release.build(self.root)
        self.rewrite_archive(lambda entries: [
            (entry, data.replace(b'"1.1.2"', b'"1.1.3"') if entry.filename.endswith("MANIFEST.json") else data)
            for entry, data in entries
        ])
        self.assert_check_fails("content/hash mismatch: MANIFEST.json")

    def test_unsafe_member_is_detected(self):
        release.build(self.root)
        self.rewrite_archive(lambda entries: entries + [("website-zero-to-live/../escape.txt", b"unsafe\n")])
        self.assert_check_fails("Unsafe ZIP member")

    def test_extra_member_is_detected(self):
        release.build(self.root)
        self.rewrite_archive(lambda entries: entries + [("website-zero-to-live/unexpected.md", b"unexpected\n")])
        self.assert_check_fails("member set differs")

    def test_missing_member_is_detected(self):
        release.build(self.root)
        self.rewrite_archive(lambda entries: [(entry, data) for entry, data in entries if not entry.filename.endswith("LICENSE")])
        self.assert_check_fails("member set differs")

    def test_sidecar_tamper_is_detected(self):
        release.build(self.root)
        self.write(self.archive_name + ".sha256", "wrong\n")
        self.assert_check_fails("SHA256 sidecar mismatch")

    def test_root_checksums_require_full_coverage(self):
        release.build(self.root)
        lines = (self.root / "SHA256SUMS").read_text().splitlines(keepends=True)
        self.write("SHA256SUMS", "".join(lines[1:]))
        self.assert_check_fails("full file coverage")

    def test_github_tamper_is_detected(self):
        release.build(self.root)
        self.write(".github/workflows/validate.yml", "name: Changed\n")
        self.assert_check_fails("Root SHA256SUMS differs")

    def test_stale_artifact_fails_without_deletion(self):
        release.build(self.root)
        self.write("dist/website-zero-to-live-1.1.1.zip", b"old artifact")
        before = self.read_outputs()
        for command in (release.check, release.build):
            with self.assertRaisesRegex(release.ReleaseError, "Unexpected/stale dist"):
                command(self.root)
        self.assertEqual(before, self.read_outputs())
        self.assertEqual((self.root / "dist/website-zero-to-live-1.1.1.zip").read_bytes(), b"old artifact")

    def test_binary_crlf_and_unclosed_fences_fail(self):
        for data, message in (
            (b"\xff\n", "UTF-8"), (b"text\r\n", "CR/CRLF"),
            (b"```text\nunclosed\n", "unclosed Markdown fence"),
        ):
            with self.subTest(message=message):
                self.write("assets/template.md", data)
                with self.assertRaisesRegex(release.ReleaseError, message):
                    release.build(self.root)

    def test_broken_relative_and_reference_links_fail(self):
        for text, message in (
            ("[Bad](missing.md)\n", "broken file link"),
            ("[Bad](../../escape.md)\n", "escapes repository"),
            ("[Bad][unknown]\n", "undefined Markdown link reference"),
        ):
            with self.subTest(message=message):
                self.write("assets/template.md", text)
                with self.assertRaisesRegex(release.ReleaseError, message):
                    release.build(self.root)

    def test_valid_links_fences_and_code_examples(self):
        self.write("assets/with space.md", "# Space\n")
        self.write("assets/template.md", """[Skill](../SKILL.md#not-validated)
[Space](with%20space.md)
[Angle](<with space.md>)
[Reference][skill]

[skill]: ../SKILL.md "Title"

`[Example](does-not-exist.md)`

~~~~text
```nested example
[Example](does-not-exist.md)
~~~~
""")
        release.build(self.root)
        release.check(self.root)

    def test_secret_patterns_fail_without_echoing_secret(self):
        fake = "gh" + "p_" + "A" * 36
        self.write("assets/template.md", fake + "\n")
        with self.assertRaisesRegex(release.ReleaseError, "possible GitHub token") as caught:
            release.build(self.root)
        self.assertNotIn(fake, str(caught.exception))

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unavailable")
    def test_symlink_input_is_rejected(self):
        (self.root / "assets/link.md").symlink_to(self.root / "README.md")
        with self.assertRaisesRegex(release.ReleaseError, "Symlink inputs are forbidden"):
            release.build(self.root)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unavailable")
    def test_symlink_dist_is_rejected(self):
        (self.root / "dist").symlink_to(self.root / "assets", target_is_directory=True)
        with self.assertRaisesRegex(release.ReleaseError, "dist must not be a symlink"):
            release.build(self.root)

    def test_appended_archive_bytes_are_rejected(self):
        release.build(self.root)
        self.archive.write_bytes(self.archive.read_bytes() + b"trailing bytes")
        self.assert_check_fails("ZIP bytes differ")


if __name__ == "__main__":
    unittest.main()
