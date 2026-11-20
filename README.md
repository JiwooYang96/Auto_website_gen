# Auto_website_gen

Semi-automatic concept websites for cold outreach. Give it a business's real details,
and Claude Code builds a one-page concept site with the frontend-design skill,
screenshots it, and checks it for invented facts. You approve before anything is sent.

It runs on your Claude Pro/Max plan through the `claude` CLI. No API key needed.

## Setup (once)

```bash
npm install -g @anthropic-ai/claude-code   # then run `claude` once and sign in
pip install playwright && playwright install chromium
```

Edit `studio.json` with your studio name.

## Using it from your phone (Claude Code on the web)

Open this repo in Claude Code from the Claude app. Then just ask in plain words:

- "Build the site for leads/my-slug.json following CLAUDE.md"
- "Add a lead for [business], [city] from this info: ..."
- "Run the checks and screenshots for my-slug and show me the screenshots"
- "Approve my-slug"

Claude follows `CLAUDE.md` and the skill in `.claude/skills/` the same way the
`build` script does. If Playwright isn't installed yet, ask Claude to run
`pip install playwright && playwright install chromium` first.

## Daily flow (on a computer or server)

1. **Add leads.** One JSON file per business in `leads/`. Copy
   `leads/example-harbor-street-bakery.json`. Only put real, verified facts in it:
   everything in the file is treated as true and may appear on the site. Set
   `"status": "new"`. (Later, your scraper or Harvey writes these files.)
2. **Build.**
   ```bash
   python3 autosite.py build              # every lead with status "new"
   python3 autosite.py build my-slug      # one lead
   python3 autosite.py build --jobs 3     # 3 at a time
   ```
   Each build: Claude reads the skill, plans a design that's different from past
   sites (it reads `design-log.md`), builds `sites/<slug>/index.html`, screenshots
   and critiques it, then the script runs fact checks and asks Claude to fix
   anything that fails.
3. **Review.** `python3 autosite.py review`, then open `review/index.html`. Sites
   that failed checks are listed first.
4. **Approve or reject.**
   ```bash
   python3 autosite.py approve my-slug
   python3 autosite.py reject my-slug "hero too busy"
   ```
   Approved sites are the ones to deploy and send.

## What you get per site (`sites/<slug>/`)

| File | Use |
|---|---|
| `index.html` | The site. Single file, deploy as-is. |
| `hero.png` | First screen on desktop. Best image for the follow-up email. |
| `desktop.png`, `mobile.png` | Full-page screenshots for review. |
| `build.log` | What Claude did, for debugging. |

## Built-in safety checks (`python3 autosite.py check <slug>`)

- noindex tag, viewport tag, "Concept design ... Not the official website." banner
- business name, phone (as a `tel:` link), email and address present
- no phone numbers, emails, prices, "since 19xx" claims or images that aren't in the lead file
- no placeholder text (lorem ipsum, 123 Main St, (555) 555...)

The checks catch the common ways AI invents facts, not all of them. Read each site
before approving it, especially opening hours and service lists.

## Rules Claude follows

See `CLAUDE.md`. Edit it to change the house rules (required sections, banner text,
how many past designs to avoid repeating).

## Not included yet

- Deploying to your preview domain
- Scraping lead data
- Sending emails (Harvey/Sellbird handles this)

## Skills included

| Skill | Used for | Source and license |
|---|---|---|
| frontend-design | Distinctive design for every site | anthropics/skills, Apache 2.0 |
| webapp-testing | Browser testing and screenshots with Playwright | anthropics/skills, Apache 2.0 |
| copywriting | Page copy built from real facts | coreyhaines31/marketingskills, MIT |
| accessibility | WCAG checks (contrast, focus, headings) | addyosmani/web-quality-skills, MIT |
| performance | Keeping pages fast and light | addyosmani/web-quality-skills, MIT |
| seo | Search basics for final, paid sites | addyosmani/web-quality-skills, MIT |
| schema | LocalBusiness structured data for final sites | coreyhaines31/marketingskills, MIT |
| cold-email | Writing outreach emails and follow-ups | coreyhaines31/marketingskills, MIT |
| image-to-code | Building a site from a flyer, mockup or screenshot you provide | Leonxlnx/imagegen-skills, MIT |
| design-md | Using the reference library and writing a DESIGN.md per client | written for this repo |

`design-references/` holds 84 DESIGN.md files extracted from real brands' public
sites (VoltAgent/awesome-design-md, MIT). They're for studying craft, not for copying
a brand onto a client; the brands' identities belong to their owners.

`CLAUDE.md` says when each one is used. Each skill folder keeps its original license
file. Copied from anthropics/skills@e4bb5d9, addyosmani/web-quality-skills@afa8da9 and
coreyhaines31/marketingskills@5b2b400, Leonxlnx/imagegen-skills@beb16b0 and
VoltAgent/awesome-design-md@fcc7028; to update one, replace its folder with the
newer version from that repo.

To turn a paid concept into the live site, ask Claude: "finalize <slug>".
