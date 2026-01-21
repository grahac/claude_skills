---
name: granola
description: Extract and display Granola meeting notes. USE WHEN user asks to "extract granola meetings", "analyze my meetings", "what meetings did I have", or "show my meeting notes".
---

# Granola Meeting Extraction

Extract meeting notes from Granola's local cache without any external API dependencies.

## When to Use

- User asks: "Extract my last 7 days of Granola meetings"
- User asks: "What meetings did I have this week?"
- User asks: "Show my recent meeting notes"

## How to Extract

Run the extraction script:

```bash
python3 ~/.claude/skills/granola/extract.py --days <N>
```

Options:
- `--days N` - Extract meetings from the last N days (default: 7)
- `--limit N` - Limit to N most recent meetings
- `--list` - Just list meeting titles without full export

## Output

Files are saved to: `~/.granola-scoop/output/`

Filename format: `YYYY-MM-DD-meeting-title.md`

Each file contains:
- Meeting metadata (title, date, attendees)
- Your notes from the meeting
- Granola's AI summary/overview

## After Extraction

After running the script, offer to:
1. Show summaries of the extracted meetings
2. Read specific meeting notes
3. Search for mentions of people/companies

## Troubleshooting

### "Granola cache not found"
- Ensure Granola is installed
- Cache location: `~/Library/Application Support/Granola/cache-v3.json`
- Record at least one meeting in Granola

### "No meetings found"
- Try increasing `--days` value
- Check if Granola has meetings in that period
