"""Run: python3 -B scripts/test_check.py  (stdlib only, no network; -B avoids writing __pycache__)."""
import contextlib, io, json, os, sys, tempfile, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check

INC = {"slug": "s1", "title": "Node.js HTTP smuggling", "product": "Node.js", "tags": ["node"], "status": "live",
       "severity": "high", "patchStatus": "patched", "updatedAt": "2026-11-01T00:00:00Z",
       "url": "https://pwn.watch/s1", "json": "https://pwn.watch/s1.json"}
RSS = """<rss><channel>
<item><title>A</title><link>https://x/a</link><guid>a@2026-11-05</guid><description>Patch.</description>
<category>Needs attention</category><category>SSH</category></item>
<item><title>B</title><link>https://x/b</link><guid>b@2026-07-20</guid><description>Old.</description>
<category>Reference</category></item>
</channel></rss>"""


def feeds(incidents, rss=RSS):
    pwn = json.dumps({"updatedAt": "2026-11-09T00:00:00Z", "incidents": incidents}).encode()
    return lambda url: pwn if url == check.INCIDENTS_URL else rss.encode()


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        check.WATCHLIST, check.SEEN = os.path.join(self.dir, "watchlist.json"), os.path.join(self.dir, "seen.json")
        json.dump({"tags": ["ssh"], "keywords": ["node.js"]}, open(check.WATCHLIST, "w"))

    def run_check(self, fetch, commit=False):
        check.fetch_raw = fetch
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            check.check(all_live=True, commit=commit)
        return out.getvalue()

    def test_matching_is_whole_word_or_tag(self):
        watch = {"tags": {"ssh"}, "keywords": ["node"]}
        self.assertTrue(check.matches({"title": "node RCE"}, watch))
        self.assertFalse(check.matches({"title": "nodejs RCE"}, watch))
        self.assertTrue(check.matches({"title": "x", "tags": ["SSH"]}, watch))

    def test_zero_wire_keeps_only_needs_attention(self):
        check.fetch_raw = feeds([])
        items, total = check.zero_wire()
        self.assertEqual(total, 2)
        self.assertEqual([(z["slug"], z["guid"]) for z in items], [("zerowire:a", "a@2026-11-05")])

    def test_lock_versions(self):
        mix = '%{\n  "bandit": {:hex, :bandit, "1.14.1", "abc", [:mix], [], "hexpm", "def"},\n}'
        npm = json.dumps({"packages": {"": {}, "node_modules/vite": {"version": "6.0.1"},
                                       "node_modules/vite/node_modules/x": {"version": "1"}}})
        self.assertEqual(check.lock_versions(mix), "bandit 1.14.1")
        self.assertEqual(check.lock_versions(npm), "vite 6.0.1")

    def test_commit_then_rerun_reports_nothing_new(self):
        first = self.run_check(feeds([INC]), commit=True)
        self.assertIn("1 new/updated", first)
        self.assertIn("🆕", first)
        second = self.run_check(feeds([INC]))
        self.assertIn("0 new/updated", second)
        self.assertNotIn("🆕", second)
        self.assertIn("Node.js HTTP smuggling", second)  # still listed under all live matches
        self.assertFalse(os.path.exists(check.SEEN + ".tmp"))

    def test_empty_feeds_fail_loudly(self):
        with self.assertRaises(SystemExit):
            self.run_check(feeds([]))
        with self.assertRaises(SystemExit):
            self.run_check(feeds([INC], rss="<rss><channel></channel></rss>"))


if __name__ == "__main__":
    unittest.main()
