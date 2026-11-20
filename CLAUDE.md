# Autosite: concept website builder

You build one concept homepage for one real local business per run. The page is a
sales preview sent to the owner, so it must look like a professional studio made it
specifically for them, and every fact on it must be true.

## Before designing
1. Read `.claude/skills/frontend-design/SKILL.md` and follow it fully: plan, review
   the plan against the brief, build, then critique with screenshots.
2. Read the lead file you were given (`leads/<slug>.json`). It is the brief.
3. Read `design-log.md`. Every past site is listed there with its palette, type and
   layout idea. Do not reuse a typeface pairing, base palette or hero concept from
   the last 10 entries. Each client must get its own identity.

## Facts: the hard rules
- Use only facts present in the lead file: name, services, prices, hours, address,
  phone, email, owner name, story, reviews. Copy them exactly.
- Never invent hours, prices, services, awards, years in business, staff names,
  testimonials or statistics. If a section would need a fact you don't have, leave
  the section out.
- You may write short new copy (headlines, descriptions) that restates or frames
  facts from the lead file. It must not add new claims.
- Images: use only the URLs in `photos`. If there are none, design without photos
  (type, color, CSS shapes). Never use stock photos or placeholder services.
- Unknown facts are never shown as placeholders ("Lorem ipsum", "123 Main St",
  "(555)", "Your text here").

## Required on every page
- `<meta name="robots" content="noindex, nofollow">` in the head.
- A slim, unobtrusive banner as the first element in <body> (not position:fixed,
  which breaks full-page screenshots):
  `Concept design for {business_name} by {studio_name}. Not the official website.`
  with `id="concept-banner"`. Take studio_name from `studio.json`.
- Phone as a `tel:` link and address as a Google Maps link, if present.
- One clear main action that fits the business (call, book, order, visit).
- Responsive to 375px wide, visible keyboard focus, `prefers-reduced-motion` respected.
  Anything laid out horizontally (timelines, rows of stats) needs its own phone layout.
- Use classes, not :first-of-type / :last-of-type, to style specific items.

## Output
- A single self-contained file: `sites/<slug>/index.html` (inline CSS, minimal or no
  JS, Google Fonts allowed). Nothing else is written outside `sites/<slug>/`, except
  the design-log entry below.
- Self-critique: run `python3 autosite.py shoot <slug>` and Read the PNGs in
  `sites/<slug>/`. Fix what looks generic, cramped or broken. Repeat at most twice.
- Finally append one line to `design-log.md`:
  `- <slug> | <palette hexes> | <typefaces> | <hero/layout concept in a few words>`
