---
name: postal-mail-unsubscribe
description: Opt out of unsolicited postal marketing (junk mail) by researching the sender's data-protection contact, drafting a UK GDPR opt-out email, and leaving it in the connected Gmail account. Use when the user shares a photo or scan of a postal letter, flyer, or marketing mailer and says things like "unsubscribe from this postal letter", "stop this junk mail", "opt me out of this", or "I keep getting these letters, make them stop".
---

# Postal Mail Unsubscribe

Turn a photo of junk postal mail into a ready-to-send (or sent) GDPR opt-out email, with no manual research from the user.

## When to use

Trigger whenever the user shares an image/scan of a physical letter, flyer, or marketing mailer and asks to stop receiving it. Common phrasings: "unsubscribe from this postal letter", "stop these letters", "opt me out", "I don't want these any more".

## What you need

- An image of the mailer (the user provides it).
- A connected **Gmail** MCP integration (for drafting/sending). Load the tools via ToolSearch: `select:mcp__Gmail__create_draft,mcp__Gmail__list_drafts`.
- **WebSearch** / **WebFetch** for finding the opt-out contact. Load via `select:WebSearch,WebFetch`.

## Workflow

1. **Read the mailer.** Use the Read tool on the image. Extract:
   - Sender company name and any website/phone.
   - The exact name and postal address the letter is addressed to (you will quote these back so the company can find the record).
   - Any printed opt-out instructions, reference number, or QR/short code.

2. **Find the opt-out contact.** Search the web for the company's documented way to stop postal marketing. Priority order:
   1. The company's own "how to opt out / unsubscribe" help page.
   2. The Data Protection Officer (DPO) / privacy / data-protection email.
   3. A general support/contact email as fallback.
   Confirm the address against an official source (their domain, help centre, or privacy policy). Note what details they ask you to include. See `references/uk-opt-out-playbook.md` for legal grounding and known contacts.

3. **Draft the email** in the connected Gmail account with `mcp__Gmail__create_draft`. One draft per company. Use the template in `references/email-template.md`. Always:
   - Address it to the verified opt-out/DPO email; CC a secondary privacy address if one exists.
   - Quote the recipient name, business, and postal address from the letter.
   - Cite **Article 21(2) UK GDPR** (right to object to direct marketing) and **PECR 2003**.
   - Ask for written confirmation of suppression and the data source if third-party sourced.
   - Use British English, professional and direct, no em dashes.

4. **Send if permitted.** If the user has given standing permission to send, and a send tool is available, send it. The current Gmail integration only supports **draft creation** (no send tool), so leave the email in Drafts and tell the user to open it and hit Send. Do not claim an email was sent when only a draft was created.

5. **Verify your own work.** Call `mcp__Gmail__list_drafts` with `query: subject:"Opt-out request"` and `view: DRAFT_VIEW_FULL`. Confirm each draft exists with the right recipient, subject, and the correct name/address in the body. Report the verification result.

6. **Notify.** Tell the user: which inbox to open, one line per company (company -> opt-out address), whether each is a draft or sent, and the sources you used. This is the "job done" notification.

## Guardrails

- **Never invent an opt-out address.** If you cannot verify one, say so and offer the postal-address or phone fallback rather than guessing.
- **Verify before claiming done.** Always list the drafts back; never report success on a tool call you did not confirm.
- **Draft vs send:** default to drafts unless the user has clearly authorised sending AND a send capability exists.
- One company per email. Do not bundle multiple senders into one message.
- If the connected mailbox is ambiguous, confirm which account before drafting.
