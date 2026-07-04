#!/usr/bin/env python3
"""Send one email from a sequence file to a GHL segment, with safety rails.

Always dry-run first. Live sends require --yes or interactive confirmation.

Usage:
  send_campaign.py assets/sequences/retargeting-lapsed.json --email 1 \
      --tag lapsed-60d --entity muffin_break --dry-run
  send_campaign.py assets/sequences/evergreen-welcome.json --email 1 \
      --tag meta-lead --entity explorazone --yes
"""
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ghl_client import GHLClient, GHLError, sendable  # noqa: E402

MAX_RECIPIENTS_DEFAULT = 500


def render(text, entity_block, contact):
    """Fill {{entity.*}} tokens locally; leave {{contact.*}} for GHL to merge."""
    out = text
    for key, value in entity_block.items():
        out = out.replace("{{entity." + key + "}}", str(value))
    first = contact.get("firstName") or "there"
    return out.replace("{{contact.first_name}}", first)


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("sequence", help="sequence JSON file")
    p.add_argument("--email", type=int, required=True, help="1-based email number in the sequence")
    p.add_argument("--entity", required=True, help="entity key in the sequence's entities block")
    p.add_argument("--tag", help="GHL tag to segment on")
    p.add_argument("--pipeline-stage", help="pipeline stage name filter")
    p.add_argument("--inactive-days", type=int, help="only contacts inactive this many days")
    p.add_argument("--max-recipients", type=int, default=MAX_RECIPIENTS_DEFAULT)
    p.add_argument("--dry-run", action="store_true", help="render and list, send nothing")
    p.add_argument("--yes", action="store_true", help="skip interactive confirmation")
    p.add_argument("--tag-after", help="tag to add to each contact after a successful send")
    args = p.parse_args()

    seq_path = Path(args.sequence)
    seq = json.loads(seq_path.read_text(encoding="utf-8"))
    emails = seq["emails"]
    if not 1 <= args.email <= len(emails):
        sys.exit(f"--email must be 1..{len(emails)}")
    email = emails[args.email - 1]
    entities = seq.get("entities", {})
    if args.entity not in entities:
        sys.exit(f"Unknown entity '{args.entity}'. Available: {', '.join(entities)}")
    entity_block = entities[args.entity]

    if not (args.tag or args.pipeline_stage or args.inactive_days):
        sys.exit("Refusing to target the whole contact list: pass --tag, "
                 "--pipeline-stage or --inactive-days.")

    try:
        client = GHLClient()
        contacts = client.search_contacts(args.tag, args.pipeline_stage,
                                          args.inactive_days, limit=args.max_recipients + 1)
    except GHLError as err:
        sys.exit(f"GHL error: {err}")

    if len(contacts) > args.max_recipients:
        sys.exit(f"Segment exceeds --max-recipients ({args.max_recipients}). "
                 f"For large sends, install the sequence as a GHL Workflow instead "
                 f"(references/ghl-setup.md).")

    targets = [c for c in contacts if sendable(c)]
    skipped = len(contacts) - len(targets)

    sample = targets[0] if targets else {"firstName": "Sample"}
    subject = render(email["subject"], entity_block, sample)
    print(f"Sequence : {seq['name']} - email {args.email}/{len(emails)} ({email['label']})")
    print(f"Entity   : {entity_block.get('brand_name', args.entity)}")
    print(f"Segment  : tag={args.tag} stage={args.pipeline_stage} "
          f"inactive={args.inactive_days}")
    print(f"Targets  : {len(targets)} sendable ({skipped} skipped: dnd/no email)")
    print(f"Subject  : {subject}")
    if args.dry_run:
        print("\n--- rendered body (first target) ---\n")
        print(render(email["html"], entity_block, sample))
        print("\nDry run - nothing sent.")
        return
    if not targets:
        sys.exit("No sendable contacts in segment.")
    if not args.yes:
        answer = input(f"Send to {len(targets)} contacts? [type SEND to confirm] ")
        if answer.strip() != "SEND":
            sys.exit("Aborted.")

    log_path = seq_path.parent / "send-log.jsonl"
    sent = failed = 0
    with open(log_path, "a", encoding="utf-8") as log:
        for ct in targets:
            try:
                client.send_email(
                    ct["id"],
                    render(email["subject"], entity_block, ct),
                    render(email["html"], entity_block, ct),
                    from_name=entity_block.get("from_name"),
                    from_email=entity_block.get("from_email"))
                if args.tag_after:
                    client.add_tag(ct["id"], args.tag_after)
                sent += 1
                status = "sent"
            except GHLError as err:
                failed += 1
                status = f"failed: {err}"
            log.write(json.dumps({
                "ts": datetime.now(timezone.utc).isoformat(),
                "sequence": seq["name"], "email": args.email,
                "entity": args.entity, "contact_id": ct["id"],
                "email_addr": ct.get("email"), "status": status}) + "\n")
            time.sleep(0.5)  # pace to respect GHL rate limits
    print(f"Done: {sent} sent, {failed} failed, {skipped} skipped. Log: {log_path}")
    if failed and not sent:
        sys.exit(1)


if __name__ == "__main__":
    main()
