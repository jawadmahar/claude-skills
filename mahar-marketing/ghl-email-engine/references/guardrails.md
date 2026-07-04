# GHL Guardrails - what can never happen, and why

Director requirement: connecting Claude to GHL must not be able to break anything. GHL's own UI makes you type DELETE before destructive actions; anything driven through an API skips those prompts, so the protection has to be rebuilt in layers here. Defence in depth - each layer alone would be enough, all four are in place.

## Layer 1: token scopes (GHL side - set up by whoever creates the PIT)

The Private Integration Token is created with ONLY these scopes:
`contacts.readonly`, `contacts.write`, `conversations/message.write`, `workflows.readonly`, `opportunities.readonly`.

No scope for deleting contacts, editing pipelines, changing settings, managing users, or touching calendars/funnels/sites. Even a bug (or a bad instruction to Claude) cannot exceed the token. One token per sub-account keeps each entity isolated - a mistake in Muffin Break's location can never touch STEMEX's contacts.

**Never create a PIT with broader scopes than the list above for Claude's use.** If a future feature needs more, create a separate token for that feature and review it then.

## Layer 2: transport blocklist (this client)

`ghl_client.py` refuses at the lowest level:

- Any HTTP method except GET/POST (no DELETE, PUT, PATCH exist in the code path)
- Any endpoint not on an explicit allowlist (contact search, tagging, workflow enrolment, email send)

So "delete all contacts" is not a dangerous command that requires confirmation - it is not expressible. There is no code that can do it, with or without consent.

## Layer 3: read-only by default

Writes (send email, add tag, enrol in workflow) additionally require `GHL_ALLOW_WRITE=1` in the environment. Day-to-day analysis sessions run without it and are physically read-only. Set it only for a session whose purpose is sending.

## Layer 4: operational rails (send_campaign.py)

- Refuses to target the whole contact list - a segment filter (tag / stage / inactivity) is mandatory
- `--dry-run` renders everything, sends nothing; recommended before every first send
- Live sends require typing `SEND` interactively, or an explicit `--yes` flag
- Hard cap of 500 recipients per invocation; bigger audiences must go through a GHL Workflow, where GHL's own throttling and unsubscribe handling apply
- DND contacts and contacts without email are always skipped
- Every send appends to `send-log.jsonl` - full audit trail of who was sent what, when

## Rules for Claude when operating GHL (also applies via MCP)

1. Never perform a destructive operation (delete, merge, bulk edit) through the API, even if asked casually. Direct the user to the GHL UI, which has its own typed confirmation.
2. Bulk operations affecting more than 500 contacts: propose, show the exact segment count, and wait for explicit approval.
3. Before the first live send of any new sequence: dry-run output must be reviewed by a human.
4. Anything touching pipeline structure, automations, or settings: read-only. Changes there happen in the GHL UI only.
5. When connecting the GHL MCP server in Claude settings, use the same least-privilege PIT from Layer 1 - never an Agency-level key.

## What "safe to say to Claude" looks like

Safe, expressible, guarded: "send the win-back email 1 to lapsed-60d Muffin Break contacts", "how many contacts in New Enquiry?", "tag these contacts winback-sent".

Not expressible at all (blocked by Layers 1+2): deleting anything, editing existing contacts' data, changing pipelines, exporting the whole database, touching another entity's sub-account with this token.
