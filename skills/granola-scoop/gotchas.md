# Granola Scoop Gotchas

Common failure patterns. Update this file every time something goes wrong.

## 1. Wrong script path
**Problem:** Running extract.py from the wrong location because the skill was installed to a different path than expected.
**Fix:** The script lives at `scripts/extract.py` relative to this skill's folder. Verify the path before running.

## 2. Granola cache not found
**Problem:** The cache file at `~/Library/Application Support/Granola/cache-v3.json` doesn't exist.
**Fix:** Granola must be installed and the user must have recorded at least one meeting. Check the path exists before attempting extraction.

## 3. No meetings found for the time range
**Problem:** User asks for "this week's meetings" but Granola has nothing in that range — maybe they didn't use it recently.
**Fix:** Try increasing the `--days` value. If still empty, confirm Granola was actively used during that period.

## 4. Offering analysis before confirming extraction succeeded
**Problem:** Jumping to "here's a summary of your meetings" before verifying the script ran successfully and files were written.
**Fix:** Always check the script exit code and verify files exist in `~/.granola-scoop/output/` before offering to analyze.

## 5. Exposing sensitive meeting content without asking
**Problem:** Dumping full meeting notes that may contain confidential information without checking if the user wants that level of detail.
**Fix:** Start with meeting titles and dates. Let the user choose which meetings to read in detail.
