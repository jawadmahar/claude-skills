#!/usr/bin/env python3
"""GoHighLevel (LeadConnector API v2) client + CLI. Standard library only.

Auth: environment variables GHL_API_KEY (Private Integration Token) and
GHL_LOCATION_ID (sub-account). Never hardcode credentials.

CLI:
  ghl_client.py contacts --tag lapsed-60d [--pipeline-stage "New Enquiry"]
                         [--inactive-days 60] [--count-only] [--json]
  ghl_client.py send-email --contact-id X --subject "..." --html-file body.html
  ghl_client.py enroll --workflow-id W --tag meta-lead
  ghl_client.py tag --contact-id X --add "welcomed"
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

BASE = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"


class GHLError(RuntimeError):
    pass


class GHLClient:
    def __init__(self, api_key=None, location_id=None):
        self.api_key = api_key or os.environ.get("GHL_API_KEY", "")
        self.location_id = location_id or os.environ.get("GHL_LOCATION_ID", "")
        if not self.api_key or not self.location_id:
            raise GHLError(
                "GHL_API_KEY and GHL_LOCATION_ID must be set. "
                "See references/ghl-setup.md for how to create a Private Integration Token.")

    def _request(self, method, path, params=None, body=None, retries=3):
        url = BASE + path
        if params:
            url += "?" + urllib.parse.urlencode(params, doseq=True)
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method, headers={
            "Authorization": f"Bearer {self.api_key}",
            "Version": API_VERSION,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        for attempt in range(1, retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    payload = resp.read().decode("utf-8")
                    return json.loads(payload) if payload else {}
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < retries:  # rate limited - back off
                    time.sleep(2 ** attempt)
                    continue
                detail = e.read().decode("utf-8", "replace")[:300]
                raise GHLError(f"{method} {path} -> HTTP {e.code}: {detail}") from e
            except urllib.error.URLError as e:
                if attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                raise GHLError(f"{method} {path} -> network error: {e.reason}") from e

    # -- contacts ----------------------------------------------------------
    def search_contacts(self, tag=None, pipeline_stage=None, inactive_days=None, limit=500):
        """Return contacts matching all given criteria. Paginates automatically."""
        results, page_after = [], None
        while len(results) < limit:
            body = {"locationId": self.location_id,
                    "pageLimit": min(100, limit - len(results))}
            filters = []
            if tag:
                filters.append({"field": "tags", "operator": "contains", "value": tag})
            if inactive_days:
                cutoff = (datetime.now(timezone.utc) - timedelta(days=inactive_days))
                filters.append({"field": "lastActivity", "operator": "lt",
                                "value": cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")})
            if filters:
                body["filters"] = filters
            if page_after:
                body["searchAfter"] = page_after
            resp = self._request("POST", "/contacts/search", body=body)
            batch = resp.get("contacts", [])
            if not batch:
                break
            if pipeline_stage:
                batch = [c for c in batch if _in_stage(c, pipeline_stage)]
            results.extend(batch)
            page_after = resp.get("searchAfter") or (batch[-1].get("searchAfter") if batch else None)
            if not page_after or len(batch) < 100:
                break
        return results[:limit]

    def add_tag(self, contact_id, tags):
        return self._request("POST", f"/contacts/{contact_id}/tags",
                             body={"tags": tags if isinstance(tags, list) else [tags]})

    # -- messaging ---------------------------------------------------------
    def send_email(self, contact_id, subject, html, from_name=None, from_email=None):
        body = {"type": "Email", "contactId": contact_id,
                "subject": subject, "html": html}
        if from_name:
            body["emailFrom"] = f"{from_name} <{from_email}>" if from_email else from_name
        return self._request("POST", "/conversations/messages", body=body)

    # -- workflows ---------------------------------------------------------
    def enroll_in_workflow(self, contact_id, workflow_id):
        return self._request(
            "POST", f"/contacts/{contact_id}/workflow/{workflow_id}",
            body={"eventStartTime": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")})


def _in_stage(contact, stage_name):
    for opp in contact.get("opportunities", []) or []:
        if stage_name.lower() in str(opp.get("pipelineStageName", "")).lower():
            return True
    return False


def sendable(contact):
    """True if the contact can be emailed (has address, not DND)."""
    return bool(contact.get("email")) and not contact.get("dnd", False)


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("contacts", help="search contacts")
    c.add_argument("--tag")
    c.add_argument("--pipeline-stage")
    c.add_argument("--inactive-days", type=int)
    c.add_argument("--count-only", action="store_true")
    c.add_argument("--json", action="store_true")

    e = sub.add_parser("send-email", help="send one email to one contact")
    e.add_argument("--contact-id", required=True)
    e.add_argument("--subject", required=True)
    e.add_argument("--html-file", required=True)

    w = sub.add_parser("enroll", help="enrol tagged contacts into a GHL workflow")
    w.add_argument("--workflow-id", required=True)
    w.add_argument("--tag", required=True)

    t = sub.add_parser("tag", help="add a tag to a contact")
    t.add_argument("--contact-id", required=True)
    t.add_argument("--add", required=True)

    args = p.parse_args()
    try:
        client = GHLClient()
        if args.cmd == "contacts":
            found = client.search_contacts(args.tag, args.pipeline_stage, args.inactive_days)
            if args.count_only:
                print(len(found))
            elif args.json:
                print(json.dumps(found, indent=2))
            else:
                for ct in found:
                    flag = "" if sendable(ct) else "  [NOT SENDABLE: dnd or no email]"
                    print(f"{ct.get('id')}  {ct.get('firstName', '')} {ct.get('lastName', '')}"
                          f"  {ct.get('email', '-')}{flag}")
                print(f"-- {len(found)} contacts", file=sys.stderr)
        elif args.cmd == "send-email":
            html = open(args.html_file, encoding="utf-8").read()
            resp = client.send_email(args.contact_id, args.subject, html)
            print(json.dumps(resp, indent=2))
        elif args.cmd == "enroll":
            targets = [ct for ct in client.search_contacts(tag=args.tag) if sendable(ct)]
            for ct in targets:
                client.enroll_in_workflow(ct["id"], args.workflow_id)
                print(f"enrolled {ct.get('email')}")
            print(f"-- {len(targets)} enrolled", file=sys.stderr)
        elif args.cmd == "tag":
            client.add_tag(args.contact_id, args.add)
            print("tagged")
    except GHLError as err:
        sys.exit(f"GHL error: {err}")


if __name__ == "__main__":
    main()
