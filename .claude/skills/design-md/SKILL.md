---
name: design-md
description: Use the DESIGN.md reference library in design-references/ and write a DESIGN.md for each client. Use when studying how a real brand handles type, spacing or components, when asked to "match the craft of" a reference site, or when finalizing a paid client site.
---

# DESIGN.md: references and per-client design systems

A DESIGN.md is one markdown file that describes a site's visual language (colors,
type, spacing, components, do's and don'ts) so an agent can build matching UI.

## The reference library (`design-references/`)

84 DESIGN.md files extracted from real brands' public websites (Stripe, Linear,
Apple, Airbnb, Notion and more), from VoltAgent/awesome-design-md (MIT). Each folder
holds `DESIGN.md` (the spec) and `README.md`.

These are other companies' visual identities. Use them to learn craft, never to
dress a client in another brand:

- **Do:** study how a reference handles a type scale, spacing rhythm, button
  hierarchy, or a section's density, and apply that level of discipline to the
  client's own palette, type and concept.
- **Do:** when the user names a reference ("as clean as Linear"), read that
  DESIGN.md for its principles and Do's and Don'ts.
- **Don't:** copy a reference's palette, typefaces, logo treatment, signature
  components or copy onto a client site. A bakery must never look like Stripe.
- **Don't:** load the whole library. Read one or two files that fit the question.
- Concept sites still follow `frontend-design` and the design-log rule in
  `CLAUDE.md`: every client gets its own identity.

## Per-client DESIGN.md (when finalizing)

When a site is finalized (`finalize <slug>`), write `sites/<slug>/final/DESIGN.md`
from the finished page, so later edits stay consistent. Read one reference file
first to match the format. Use these sections, filled from the actual CSS of the
final page, not invented:

1. Overview: the concept in 2 to 3 sentences
2. Colors: each token with hex and its job (surface, text, accent, button)
3. Typography: families, weights, the type scale (sizes for h1 to body), line
   heights
4. Layout: max width, gutters, section spacing, breakpoints
5. Shapes: border radius scale, borders
6. Components: buttons (primary, secondary), any signature component (for example
   "admission ticket price rows"), navigation, footer
7. Motion: the one orchestrated moment and its reduced-motion fallback
8. Do's and Don'ts: what keeps future edits on-brand for this client

Credit: reference files from VoltAgent/awesome-design-md, MIT (see
`design-references/LICENSE`). The extracted tokens describe publicly visible CSS;
the brands' identities belong to their owners.
