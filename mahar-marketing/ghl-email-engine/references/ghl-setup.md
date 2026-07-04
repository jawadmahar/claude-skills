# GHL Setup - tokens, scopes, deliverability, workflows

## 1. Create a Private Integration Token (once per sub-account)

1. In GHL, open the sub-account (Location) for the entity, e.g. Explorazone.
2. Settings > **Private Integrations** > Create new integration, name it `claude-email-engine`.
3. Grant these scopes (least privilege):
   - `contacts.readonly` and `contacts.write` (search, tag)
   - `conversations/message.write` (send email)
   - `workflows.readonly` (list workflows for enrolment)
   - `opportunities.readonly` (pipeline-stage segmentation)
4. Copy the token once - GHL will not show it again.
5. Settings > Business Profile: copy the **Location ID**.

Then in the environment where Claude or the scripts run:

```bash
export GHL_API_KEY="pit-xxxxxxxx"
export GHL_LOCATION_ID="XXXXXXXXXXXX"
```

One PIT per entity keeps blast-radius small; switch entity by switching the two variables. To connect GHL as an MCP server in Claude (so Claude can call it without scripts), GHL's MCP endpoint is `https://services.leadconnectorhq.com/mcp/` with the same PIT plus locationId header - add it under Settings > Connectors in Claude with those credentials.

## 2. Deliverability checklist (you send from your own GHL IP)

Because sending is direct from GHL (dedicated IP, no Mailchimp), deliverability is yours to protect:

- **SPF, DKIM, DMARC** verified per sending domain (GHL > Settings > Email Services > Dedicated Domain). All three must show green before the first campaign.
- **Warm the IP**: if a domain has not sent bulk email before, start with <100/day for a week, then double weekly. The 500-recipient cap in `send_campaign.py` exists partly for this.
- **One-click unsubscribe** must be on (GHL adds the header when configured under Email Services). UK PECR and GDPR require a working opt-out on every marketing email.
- **Lawful basis**: leads from Meta lead forms gave contact consent for follow-up; keep the consent text used on the form in GHL as a custom field. For lapsed-customer win-backs, soft opt-in applies (existing customers, similar services) - still honour opt-outs immediately.
- Watch bounce and complaint rates in GHL > Marketing > Emails > Statistics; pause any sequence over 2% bounces or 0.1% complaints.

## 3. Install a sequence as a GHL Workflow (evergreen automation)

The JSON sequences in `assets/sequences/` map 1:1 onto GHL Workflow steps:

1. Automation > Workflows > Create Workflow > start from scratch.
2. Trigger: **Contact Tag Added** (e.g. `meta-lead`) - the Meta lead-form integration or Claude can apply this tag.
3. For each email in the JSON: add **Send Email** step, paste subject/body, replace `{{entity.*}}` tokens with the entity's real values (workflows are per-sub-account so entity is implicit), keep `{{contact.first_name}}` as a GHL merge field.
4. Between emails add **Wait** steps using each email's `delay_days`.
5. Add exit condition: contact replies or books -> remove from workflow (Goal event).
6. Publish. From then on it is fully evergreen - every tagged lead gets the sequence with zero manual sends.

`ghl_client.py enroll --workflow-id <id> --tag <tag>` backfills existing contacts into the published workflow.

## 4. Pipeline conventions used by the scripts

- Meta lead-form leads should land with tag `meta-lead` plus an entity/campaign tag (e.g. `short-breaks`).
- Lapsed segmentation uses GHL `lastActivity`; the `--inactive-days 60` filter means no opens, clicks, replies or visits logged in 60 days.
- After a win-back send, `--tag-after winback-sent-2026Q3` prevents double-sending the same wave.

## 5. Closing the loop with Meta (do this - it is the biggest lever)

Connect each pixel/dataset to GHL pipeline events via Meta's Conversions API (GHL > Marketing > native FB CAPI integration, or Events Manager > CRM connection). When a lead reaches "booked" or "purchased" in GHL, Meta learns which ad produced *customers* rather than form-fills - Meta's own estimate is ~24% lower cost per quality lead. This single integration improves every campaign the other two skills produce.
