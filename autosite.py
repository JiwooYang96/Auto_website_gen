#!/usr/bin/env python3
"""Autosite: semi-automatic concept website builder.

  python3 autosite.py build [slug ...]   build sites (default: every lead with status "new")
  python3 autosite.py shoot <slug>       take desktop, hero and mobile screenshots
  python3 autosite.py check <slug>       run the fact and requirement checks
  python3 autosite.py review             make review/index.html to approve sites
  python3 autosite.py approve <slug>     mark a site ready to send
  python3 autosite.py reject <slug> [note]

Building runs Claude Code headless (`claude -p`) on your Claude plan, using the
frontend-design skill and the rules in CLAUDE.md.
"""
import argparse
import html
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEADS = ROOT / "leads"
SITES = ROOT / "sites"
REVIEW = ROOT / "review"

ALLOWED_TOOLS = [
    "Read", "Write", "Edit", "Glob", "Grep",
    "Bash(python3 autosite.py shoot:*)",
]
PLACEHOLDERS = [
    r"lorem ipsum", r"\b123 main st", r"\(555\)\s?555", r"your (text|name|business) here",
    r"\bTODO\b", r"\[business[_ ]name\]", r"example\.com\b",
]


# ---------- leads ----------
def load_lead(slug):
    path = LEADS / f"{slug}.json"
    if not path.exists():
        sys.exit(f"No lead file: {path}")
    return json.loads(path.read_text())


def save_lead(lead):
    (LEADS / f"{lead['slug']}.json").write_text(json.dumps(lead, indent=2, ensure_ascii=False) + "\n")


def all_leads():
    return [json.loads(p.read_text()) for p in sorted(LEADS.glob("*.json"))]


# ---------- build ----------
def build_prompt(slug, problems=None):
    prompt = (
        f"Build the concept homepage for the lead in leads/{slug}.json. "
        "Follow CLAUDE.md exactly, including the frontend-design skill process, "
        f"the screenshot self-critique, and the design-log entry. Write sites/{slug}/index.html."
    )
    if problems:
        prompt += (
            f"\n\nsites/{slug}/index.html already exists but failed these checks. "
            "Fix only these problems, keep the design:\n- " + "\n- ".join(problems)
        )
    return prompt


def run_claude(slug, problems=None, model=None):
    cmd = ["claude", "-p", build_prompt(slug, problems),
           "--allowedTools", ",".join(ALLOWED_TOOLS),
           "--output-format", "text"]
    if model:
        cmd += ["--model", model]
    log = SITES / slug / "build.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as f:
        f.write(f"\n===== {'fix' if problems else 'build'} =====\n")
        result = subprocess.run(cmd, cwd=ROOT, stdout=f, stderr=subprocess.STDOUT, timeout=1800)
    return result.returncode == 0


def build_one(slug, model=None, max_fixes=1):
    lead = load_lead(slug)
    print(f"[{slug}] building...")
    if not run_claude(slug, model=model):
        lead["status"] = "build_failed"
        save_lead(lead)
        print(f"[{slug}] Claude run failed, see sites/{slug}/build.log")
        return
    problems = check(slug, quiet=True)
    for _ in range(max_fixes):
        if not problems:
            break
        print(f"[{slug}] {len(problems)} check(s) failed, asking for a fix...")
        run_claude(slug, problems=problems, model=model)
        problems = check(slug, quiet=True)
    shoot(slug)
    lead["status"] = "needs_review" if not problems else "needs_fix"
    lead["check_problems"] = problems
    save_lead(lead)
    print(f"[{slug}] {lead['status']}" + (f": {problems}" if problems else ""))


def cmd_build(args):
    slugs = args.slugs or [l["slug"] for l in all_leads() if l.get("status", "new") == "new"]
    if not slugs:
        print("No leads with status 'new'.")
        return
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        list(pool.map(lambda s: build_one(s, model=args.model), slugs))
    print("Done. Run: python3 autosite.py review")


# ---------- screenshots ----------
def shoot(slug):
    from playwright.sync_api import sync_playwright
    page_file = SITES / slug / "index.html"
    if not page_file.exists():
        print(f"[{slug}] no index.html to screenshot")
        return
    url = page_file.as_uri()
    out = SITES / slug
    with sync_playwright() as p:
        browser = p.chromium.launch()
        desk = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1,
                                reduced_motion="reduce")  # final state, no half-played animations
        desk.goto(url, wait_until="networkidle")
        desk.wait_for_timeout(1200)  # let fonts and any load animation settle
        desk.screenshot(path=str(out / "hero.png"))  # first screen: use this in emails
        desk.screenshot(path=str(out / "desktop.png"), full_page=True)
        mob = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                               reduced_motion="reduce")
        mob.goto(url, wait_until="networkidle")
        mob.wait_for_timeout(1200)
        mob.screenshot(path=str(out / "mobile.png"), full_page=True)
        browser.close()
    print(f"[{slug}] screenshots saved: hero.png, desktop.png, mobile.png")


# ---------- checks ----------
class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self._skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def digits(s):
    return re.sub(r"\D", "", s or "")


def check(slug, quiet=False):
    lead = load_lead(slug)
    page = SITES / slug / "index.html"
    if not page.exists():
        return ["sites/{}/index.html was not created".format(slug)]
    raw = page.read_text(errors="ignore")
    parser = TextOnly()
    parser.feed(raw)
    text = html.unescape(" ".join(parser.parts))
    text_norm = re.sub(r"\s+", " ", text)
    lead_blob = json.dumps(lead, ensure_ascii=False)
    problems = []

    if not re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', raw, re.I):
        problems.append('Missing <meta name="robots" content="noindex, nofollow">')
    if 'id="concept-banner"' not in raw and "id='concept-banner'" not in raw:
        problems.append('Missing the concept banner element with id="concept-banner"')
    elif "not the official website" not in text_norm.lower():
        problems.append('Concept banner must say "Not the official website."')
    if not re.search(r'<meta[^>]+name=["\']viewport', raw, re.I):
        problems.append("Missing viewport meta tag (needed for mobile)")
    if lead["business_name"].lower() not in text_norm.lower():
        problems.append(f"Business name '{lead['business_name']}' does not appear on the page")

    if lead.get("phone"):
        if digits(lead["phone"]) not in digits(raw):
            problems.append(f"Phone number {lead['phone']} is missing")
        if "tel:" not in raw:
            problems.append("Phone should be a tel: link")
    # any other phone-like number on the page is probably invented
    lead_digits = digits(lead.get("phone"))
    for m in re.findall(r"\(?\b\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b", text_norm):
        if digits(m) != lead_digits:
            problems.append(f"Unknown phone number on page: {m}")
    if lead.get("email") and lead["email"].lower() not in raw.lower():
        problems.append(f"Email {lead['email']} is missing")
    for email in set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text_norm)):
        if email.lower() not in lead_blob.lower():
            problems.append(f"Unknown email on page: {email}")
    if lead.get("address"):
        street = lead["address"].split(",")[0].strip().lower()
        if street not in text_norm.lower():
            problems.append(f"Address '{lead['address']}' is missing")

    # prices not in the lead file are invented
    for price in set(re.findall(r"\$\s?\d+(?:\.\d{2})?", text_norm)):
        if price.replace(" ", "") not in lead_blob:
            problems.append(f"Price {price} is not in the lead file (invented?)")
    # years / 'since' claims not in the lead file
    for year in set(re.findall(r"\b(?:since|est\.?|established)\s+(\d{4})", text_norm, re.I)):
        if year not in lead_blob:
            problems.append(f"Claim 'since {year}' is not in the lead file")
    # images must come from the lead's photos
    for src in re.findall(r'<img[^>]+src=["\']([^"\']+)', raw, re.I):
        if src.startswith("data:"):
            continue
        if src not in lead.get("photos", []):
            problems.append(f"Image not from lead photos: {src[:80]}")
    for pat in PLACEHOLDERS:
        if re.search(pat, text_norm, re.I) and not re.search(pat, lead_blob, re.I):
            problems.append(f"Placeholder text found: /{pat}/")

    if not quiet:
        if problems:
            print(f"[{slug}] {len(problems)} problem(s):")
            for p in problems:
                print("  -", p)
        else:
            print(f"[{slug}] all checks passed")
    return problems


# ---------- review ----------
def cmd_review(_args):
    REVIEW.mkdir(exist_ok=True)
    order = {"needs_fix": 0, "needs_review": 1, "build_failed": 2, "approved": 3, "rejected": 4, "new": 5}
    leads = sorted(all_leads(), key=lambda l: order.get(l.get("status", "new"), 9))
    cards = []
    for l in leads:
        slug = l["slug"]
        site = Path("../sites") / slug
        has = (SITES / slug / "hero.png").exists()
        probs = "".join(f"<li>{html.escape(p)}</li>" for p in l.get("check_problems", []))
        cards.append(f"""
<article class="lead {html.escape(l.get('status','new'))}">
  <header>
    <h2>{html.escape(l['business_name'])}</h2>
    <p>{html.escape(l.get('category',''))}, {html.escape(l.get('city',''))}</p>
    <p class="status">{html.escape(l.get('status','new').replace('_',' '))}</p>
  </header>
  {f'<div class="shots"><a href="{site}/index.html"><img src="{site}/hero.png" alt="Desktop first screen"></a><a href="{site}/mobile.png"><img class="m" src="{site}/mobile.png" alt="Mobile full page"></a></div>' if has else '<p>Not built yet.</p>'}
  {f'<ul class="probs">{probs}</ul>' if probs else ''}
  <p class="cmd">Approve: <code>python3 autosite.py approve {slug}</code><br>
     Reject: <code>python3 autosite.py reject {slug} "reason"</code></p>
</article>""")
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Autosite review</title>
<style>
body{{font:15px/1.5 system-ui,sans-serif;margin:0;padding:24px;background:#f3f4f6;color:#1f2937}}
h1{{margin:0 0 16px}} .lead{{background:#fff;border-radius:10px;padding:18px;margin:0 0 20px}}
.lead header{{display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}} .lead h2{{margin:0;font-size:18px}}
.lead header p{{margin:0;color:#6b7280}} .status{{font-weight:600;color:#1f2937!important}}
.needs_fix .status,.build_failed .status{{color:#b91c1c!important}} .approved .status{{color:#15803d!important}}
.shots{{display:flex;gap:12px;margin-top:12px;align-items:flex-start;overflow-x:auto}}
.shots img{{height:320px;border:1px solid #e5e7eb;border-radius:6px}} .shots img.m{{height:320px;width:auto;object-fit:cover;object-position:top}}
.probs{{color:#b91c1c}} .cmd{{color:#6b7280;font-size:13px}} code{{background:#f3f4f6;padding:1px 5px;border-radius:4px}}
</style></head><body><h1>Sites to review ({sum(1 for l in leads if l.get('status')=='needs_review')} waiting)</h1>
{''.join(cards)}</body></html>"""
    (REVIEW / "index.html").write_text(page)
    print(f"Open {REVIEW / 'index.html'}")


def set_status(slug, status, note=None):
    lead = load_lead(slug)
    lead["status"] = status
    if note:
        lead["review_note"] = note
    save_lead(lead)
    print(f"[{slug}] {status}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("slugs", nargs="*")
    b.add_argument("--jobs", type=int, default=2, help="sites built in parallel (default 2)")
    b.add_argument("--model", help="Claude model to use, e.g. opus or sonnet")
    s = sub.add_parser("shoot"); s.add_argument("slug")
    c = sub.add_parser("check"); c.add_argument("slug")
    sub.add_parser("review")
    a = sub.add_parser("approve"); a.add_argument("slug")
    r = sub.add_parser("reject"); r.add_argument("slug"); r.add_argument("note", nargs="?")
    args = ap.parse_args()
    if args.cmd == "build":
        cmd_build(args)
    elif args.cmd == "shoot":
        shoot(args.slug)
    elif args.cmd == "check":
        sys.exit(1 if check(args.slug) else 0)
    elif args.cmd == "review":
        cmd_review(args)
    elif args.cmd == "approve":
        set_status(args.slug, "approved")
    elif args.cmd == "reject":
        set_status(args.slug, "rejected", args.note)


if __name__ == "__main__":
    main()
