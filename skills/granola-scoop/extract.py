#!/usr/bin/env python3
"""
Granola Meeting Extractor - No external dependencies required.
Extracts meeting notes from Granola's local cache.
"""

import json
import os
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path


CACHE_PATH = os.path.expanduser("~/Library/Application Support/Granola/cache-v3.json")
OUTPUT_DIR = os.path.expanduser("~/.granola-scoop/output")


def load_granola_cache():
    """Load and parse the Granola cache file. Returns (documents, transcripts)."""
    if not os.path.exists(CACHE_PATH):
        raise FileNotFoundError(f"Granola cache not found at: {CACHE_PATH}")

    with open(CACHE_PATH, 'r') as f:
        data = json.load(f)

    cache_str = data.get('cache', '{}')
    cache = json.loads(cache_str)
    state = cache.get('state', {})
    return state.get('documents', {}), state.get('transcripts', {})


def parse_date(date_str):
    """Parse ISO date string to datetime."""
    if not date_str:
        return None
    try:
        # Handle various ISO formats
        date_str = date_str.replace('Z', '+00:00')
        if '.' in date_str:
            date_str = date_str.split('.')[0]
        return datetime.fromisoformat(date_str.replace('+00:00', ''))
    except (ValueError, AttributeError):
        return None


def slugify(text):
    """Convert text to a filename-safe slug."""
    if not text:
        return "untitled"
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text[:50].strip('-')


def get_attendees(doc):
    """Extract attendee names from a document."""
    attendees = []

    # From google_calendar_event
    event = doc.get('google_calendar_event', {})
    if event and isinstance(event, dict):
        event_attendees = event.get('attendees', [])
        if isinstance(event_attendees, list):
            for att in event_attendees:
                if isinstance(att, dict):
                    name = att.get('displayName') or att.get('email', '').split('@')[0]
                    if name:
                        attendees.append(name)

    # From people field - can be a list or a dict containing attendees
    people = doc.get('people')
    if isinstance(people, dict):
        # It's actually an event-like structure with an attendees key
        people_list = people.get('attendees', [])
        if isinstance(people_list, list):
            for p in people_list:
                if isinstance(p, dict):
                    name = p.get('name') or p.get('displayName')
                    if name and name not in attendees:
                        attendees.append(name)
    elif isinstance(people, list):
        for p in people:
            if isinstance(p, dict):
                name = p.get('name')
            elif isinstance(p, str):
                name = p
            else:
                continue
            if name and name not in attendees:
                attendees.append(name)

    return attendees


def format_transcript(transcript_segments):
    """Format transcript segments into readable text."""
    if not transcript_segments or not isinstance(transcript_segments, list):
        return ''

    lines = []
    current_speaker = None

    for seg in transcript_segments:
        if not isinstance(seg, dict):
            continue

        text = seg.get('text', '').strip()
        if not text:
            continue

        speaker = seg.get('source', 'Unknown')
        if speaker == 'system':
            speaker = 'Speaker'

        if speaker != current_speaker:
            if lines:
                lines.append('')
            lines.append(f"**{speaker}:** {text}")
            current_speaker = speaker
        else:
            lines[-1] += f" {text}"

    return '\n'.join(lines)


def format_meeting_markdown(doc, transcript_segments=None):
    """Format a meeting document as markdown."""
    title = doc.get('title', 'Untitled Meeting')
    created = doc.get('created_at', '')

    # Handle notes - prefer markdown, fallback to plain text
    notes = ''
    if doc.get('notes_markdown') and isinstance(doc.get('notes_markdown'), str):
        notes = doc.get('notes_markdown')
    elif doc.get('notes_plain') and isinstance(doc.get('notes_plain'), str):
        notes = doc.get('notes_plain')

    # Handle overview - can be string, dict, or other
    overview = doc.get('overview', '')
    if isinstance(overview, dict):
        overview = overview.get('content', '') or ''
    elif not isinstance(overview, str):
        overview = ''
    attendees = get_attendees(doc)

    # Parse date for display
    date_obj = parse_date(created)
    date_display = date_obj.strftime('%B %d, %Y at %I:%M %p') if date_obj else created

    lines = [
        f"# {title}",
        "",
        f"**Date:** {date_display}",
    ]

    if attendees:
        lines.append(f"**Attendees:** {', '.join(attendees)}")

    lines.append("")

    if notes:
        lines.extend(["## Notes", "", notes, ""])

    if overview:
        lines.extend(["## Summary", "", overview, ""])

    # Add transcript if available
    transcript_text = format_transcript(transcript_segments)
    if transcript_text:
        lines.extend(["## Transcript", "", transcript_text, ""])

    return '\n'.join(lines)


def extract_meetings(days=7, limit=None, list_only=False):
    """Extract meetings from the last N days."""
    documents, transcripts = load_granola_cache()

    cutoff = datetime.now() - timedelta(days=days)
    meetings = []

    for doc_id, doc in documents.items():
        # Skip deleted documents
        if doc.get('deleted_at'):
            continue

        # Skip non-meeting documents
        if doc.get('type') and doc.get('type') != 'meeting':
            continue

        created = parse_date(doc.get('created_at'))
        if not created or created < cutoff:
            continue

        meetings.append({
            'id': doc_id,
            'title': doc.get('title', 'Untitled'),
            'created_at': created,
            'doc': doc
        })

    # Sort by date, newest first
    meetings.sort(key=lambda x: x['created_at'], reverse=True)

    if limit:
        meetings = meetings[:limit]

    if not meetings:
        print(f"No meetings found in the last {days} days.")
        return []

    if list_only:
        print(f"Found {len(meetings)} meetings in the last {days} days:\n")
        for m in meetings:
            date_str = m['created_at'].strftime('%Y-%m-%d')
            print(f"  {date_str}: {m['title']}")
        return meetings

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Extracting {len(meetings)} meetings to {OUTPUT_DIR}\n")

    exported = []
    for m in meetings:
        date_str = m['created_at'].strftime('%Y-%m-%d')
        slug = slugify(m['title'])
        filename = f"{date_str}-{slug}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # Get transcript for this document if available
        doc_id = m['id']
        transcript_segments = transcripts.get(doc_id, [])

        content = format_meeting_markdown(m['doc'], transcript_segments)

        with open(filepath, 'w') as f:
            f.write(content)

        print(f"  {filename}")
        exported.append({
            'title': m['title'],
            'date': date_str,
            'file': filepath
        })

    print(f"\nExported {len(exported)} meetings.")
    return exported


def main():
    parser = argparse.ArgumentParser(description='Extract Granola meeting notes')
    parser.add_argument('--days', type=int, default=7, help='Days to look back (default: 7)')
    parser.add_argument('--limit', type=int, help='Max number of meetings to extract')
    parser.add_argument('--list', action='store_true', help='List meetings without exporting')

    args = parser.parse_args()

    try:
        extract_meetings(days=args.days, limit=args.limit, list_only=args.list)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing Granola cache: {e}")
        exit(1)


if __name__ == '__main__':
    main()
