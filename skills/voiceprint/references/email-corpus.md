# Email corpus collection

## Select accounts

Scan the connected tool list for every email MCP. Do not assume Gmail or a single
account. Common signatures include Gmail `search_threads` / `get_thread`, google-mcp
`gmail_search` / `gmail_read`, Outlook or Microsoft 365 tools, and tools containing
`mail`, `email`, or `messages` for Fastmail, ProtonMail, Hey, and generic IMAP.

List every distinct connector and ask which accounts to include and the user's
authored address for each. If none are connected, tell the user to install a connector
for their provider and stop.

## Delegate the pull

A 50-message search plus full-content fetches can overflow the main context. Give a
fresh-context worker the connector tool names and authored address for each account,
provider-specific "recent sent mail" query syntax, and every collection rule below.
Require a cleaned structured corpus, never raw provider JSON.

For each account:

1. Pull the user's authored sent messages. Prefer a messages-level API with a sender
   filter. If only a threads API exists, search sent threads and then keep only messages
   whose sender contains the authored address.
2. Paginate until at least 40 authored messages are collected. Target about 50 per
   account before balancing; accept fewer for a low-volume account.
3. Fetch each full message body.
4. Strip quoted reply chains: `>` lines, "On [date], X wrote:" blocks, Outlook-style
   "From: ... Sent: ... Subject: ..." headers, and everything below those headers.
5. Strip only multi-line contact signatures containing email addresses, phone numbers,
   URLs, company or title lines, or legal disclaimers.
6. Preserve minimalist one-line sign-offs under about 25 characters when they contain
   no email address, URL, or phone number. These are voice signals.
7. Drop messages under 30 words after cleaning. Relax to 20 only if the clean set would
   otherwise stay below 40.
8. Drop self-sends and messages to automated addresses such as `noreply@`,
   `notifications@`, `calendar-notification@`, or `mailer-daemon@`.
9. Keep a mix of intros, replies, follow-ups, declines, and status updates. Tag each
   message with its source account.

## Merge and return

Merge to about 50 messages total with meaningful representation from every account.
Sample down a dominant account rather than allowing a 45/5 split. Deduplicate exact
copies, preserving all source-account tags.

Return one structured entry per message with subject, primary recipient and recipient
count, date, source account, cleaned authored body including a preserved minimalist
sign-off, and word count. Add a per-account count summary.

Show the subject list to the user and ask which pieces were mostly AI-drafted. Remove
those pieces before analysis so generated patterns do not feed back into the voiceprint.
