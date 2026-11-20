# Autosite: concept website builder

You build one concept homepage for one real local business per run. The page is a
sales preview sent to the owner, so it must look like a professional studio made it
specifically for them, and every fact on it must be true.

## Skills in this project and when to use them
All live in `.claude/skills/`. The rules in this file win over any skill when they
disagree (for example: concept sites stay noindex even though the SEO skill wants
pages indexed, and copy never adds facts the lead file doesn't have).

Every concept site:
- `frontend-design`: the design process. Always.
- `copywriting`: headlines, section copy and button labels, framed from the lead
  file's facts only.
- `accessibility`: check contrast, headings, focus, link names and alt text before
  you finish.
- `performance`: keep the page light. Single file, no heavy scripts, sensible fonts.
- `webapp-testing`: Playwright patterns for anything `autosite.py shoot` doesn't
  cover (checking a click, mobile menu, console errors).
- `web-design-guidelines`: final review against Vercel's interface rules before
  you finish. Fix what it finds. Exception: headings and buttons stay in sentence
  case (frontend-design wins over its "Title Case" rule).
- `emil-design-eng`: polish pass on details (easing, timing, button feedback,
  focus and hover states) once the design works.
- `review-animations`: check the page's one orchestrated motion moment against its
  craft bar before you finish; remove motion it says doesn't earn its place.
- `impeccable`: extra critique and audit pass (`critique`, `audit`, `polish`) on a
  finished concept. Its fact rule matches ours: never add claims. Leave its hooks
  off (don't run `hooks on`) unless the user asks. Its engine downloads a compiled
  program to `~/.impeccable` on first run; if that fails or is blocked, follow its
  "Launcher unavailable" fallback and use the guides in `reference/` only.

Only when a client has paid and the site goes live (see "Final site" below):
- `seo`: titles, meta descriptions, headings, local search basics.
- `schema`: LocalBusiness JSON-LD built only from lead-file facts.

Only when a starting image exists:
- `image-to-code`: build from an image the user provides (a client's flyer, a
  mockup from an image tool, a screenshot of their current site). Claude Code can't
  generate images, so skip the skill's "generate the image first" step. Copy the
  image's look, but take every fact (names, prices, hours, phone) from the lead
  file only: text read off an image is never a source of facts.

Design references and per-client systems:
- `design-md`: the 84 brand DESIGN.md files in `design-references/` are for
  studying craft only, never for copying a brand onto a client. When finalizing,
  write a DESIGN.md for the client (see that skill).

Outreach, not site building:
- `cold-email`: when asked to write or improve the outreach emails and follow-ups.

Learning the user's taste:
- `learn-taste`: when the user corrects a design ("too busy", "bigger headline",
  "I don't like that font"), turn the correction into a rule with its reason and
  save it in a project skill at `.claude/skills/studio-taste/SKILL.md`, so every
  later site follows it. Facts and required-page rules in this file still win.

Growing the toolkit:
- `find-skills`: when asked to find or add a skill. Follow its "Project rules"
  section: ask before installing, read the files first, MIT/Apache only, install
  into this project's `.claude/skills/` (never globally, never with `-y`).

## Before designing
1. Read `.claude/skills/frontend-design/SKILL.md` and follow it fully: plan, review
   the plan against the brief, build, then critique with screenshots. Use the
   copywriting, accessibility and performance skills as listed above.
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

## Final site (only when asked: "finalize <slug>")
The client has paid. Copy `sites/<slug>/index.html` to `sites/<slug>/final/index.html`
and in the copy:
- remove the concept banner and the noindex meta tag
- apply the `seo` skill (title, meta description, one h1, local search basics)
- add LocalBusiness JSON-LD with the `schema` skill, using lead-file facts only
- re-run the `accessibility` checks
- write `sites/<slug>/final/DESIGN.md` with the `design-md` skill
Never change the concept file itself.
