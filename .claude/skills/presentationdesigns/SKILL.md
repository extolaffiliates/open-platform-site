---
name: presentationdesigns
description: End-to-end Extol presentation pipeline - research the audience, write a McKinsey-style storyline, render it with ALL of OpenDesign, Guizang, Spectacle, Quarkdown and an editable PPTX, then QA every version with Impeccable and the deck validators. Use for /presentationdesigns, or any request to make, remake, adapt or polish a presentation, deck, pitch, proposal deck or slides (e.g. "remake the Ismael deck for <person>").
user-invocable: true
argument-hint: "<who/what the deck is for> [source deck link]"
---

# /presentationdesigns

One storyline in, five renderings out, all checked before hand-over. Output lives in `presentations/<deck-name>/` (kebab-case, e.g. `amit-chavda`). Worked example: `presentations/amit-chavda/`.

## 0. Tools ready
Run `QUICK=1 presentation-toolkit/install.sh` if any of these are missing: `~/.claude/skills/guizang-ppt-skill`, `~/.claude/skills/impeccable`, `~/tools/open-design`, `~/tools/spectacle`, `~/tools/quarkdown`.

## 1. Inputs (ask only for what you cannot find)
- **Source deck** (remakes): read it with Google Drive `read_file_content`; keep its structure, tool stack, control/approval logic and close unless the new audience needs otherwise.
- **Who it is for**: search Drive and Gmail first; then Apollo `apollo_people_match` with their LinkedIn URL (LinkedIn itself is blocked from the cloud container). Paid enrichment beyond a standard match (company enrich, phone, waterfall) needs the user's OK first.
- **Their company / startup, goal, audiences, what is already live, raw content they can supply**: one `AskUserQuestion` round for the gaps.
- **Extol's own facts** come from the website repo `extolaffiliates/website` (attach with `add_repo`; extol.si itself is blocked from the container): `llms.txt` for positioning, principles and case studies with sourced numbers; `DESIGN.md` §04 for certified brand colours; `assets/img/logo-512.png` for the mark; `portfolio/index.html` for the portfolio deck. Add a proof slide from these case studies to every proposal.
- **Other prospects' decks are confidential.** When a deck references another prospect or client (e.g. "met at the same event"), use public facts and the approach only, never their metrics or our analysis of them, describe proposals as proposals (not results), and add a `[confirm with <name> before sending]` placeholder.
- Never invent facts, quotes, numbers or product claims. Unknowns become visible `[bracketed placeholders]` on the slide and in the README "Still to fill" list.
- Regulated or employed people (health, finance, someone with an employer): add a guardrails slide covering what they cannot say and who signs off.

## 2. Storyline (`mckinsey-deck` skill)
Write `storyline.md` first: frame (question, audience, decision, governing thought), facts used with sources, placeholders, ghost deck of action titles, then per-slide content and speaker notes. Every renderer copies from this file; change content here, not in one renderer.

## 3. Design direction (OpenDesign)
`design/tokens.css` + `design/README.md`: structure from `~/tools/open-design/design-systems/<system>` (default `corporate`), colours from `extolaffiliates/website` DESIGN.md §04 for Extol work (Oat `#EDE9DC` page, Oat 2 `#E4DFCE` cards, Forest `#1D2A1B` ink, field-top `#0C1A11` dark slides, Moss `#C6DE93` accent on dark, Fern `#55703A` accent on light); these supersede the approximate `extolaffiliatescolours` skill. Copy `presentations/amit-chavda/design/` (tokens + transparent logo marks) as the starting point. For charts use OpenDesign `frame-data-chart-nyt` / `data-report` and the `dataviz` skill.

## 4. Render all five
| Output | How |
| --- | --- |
| `guizang/index.html` | `guizang-ppt-skill`, Style B Swiss (data/strategy) or A (narrative). Locked `data-layout="S01-S22"` layouts only, speaker notes per slide, English UI, Extol tokens on `--paper/--ink/--accent`. Big job: delegate to a subagent with the storyline path. Copy `assets/motion.min.js` next to it. |
| `spectacle/index.html` | Spectacle one-page pattern (import map from `~/tools/spectacle/examples/one-page/index.html`, React + htm via esm.sh). No build needed. |
| `quarkdown/main.qd` + `styles.css` | `.doctype {slides}`, `.autopagebreak maxdepth:{1}`, `.theme {paperwhite} layout:{minimal}`, cards via `.container classname:{...}` inside `.grid columns:{n}`, notes via `.speakernote`. |
| `pptx/<Name>_x_Extol.pptx` | `pptx/build_pptx.py` (python-pptx, 16:9, blank layout, Extol colours, notes on each slide). Copy `presentations/amit-chavda/pptx/build_pptx.py` as the starting point. |
| `README.md` | Table of outputs, "Still to fill", "Changed from the source deck". |

## 5. QA (always, before hand-over)
Run `.claude/skills/presentationdesigns/scripts/qa.sh presentations/<deck-name>`. It runs the Impeccable detector on the HTML decks, both Guizang validators, a Spectacle syntax check, a PPTX render to a contact sheet, and Quarkdown if installed.
- Look at the PPTX contact sheet and the Guizang screenshots (render with Playwright at 1920x1080) yourself: no overflow, clipping or overlap, and placeholders visible.
- Fix every Impeccable **low-contrast** and **cramped-padding** finding. Accept by design in Swiss decks: `tight-leading` on display titles, `overused-font: inter`, `repeating-stripes-gradient` (the dot background).
- Detector quirks: it misreads `border-*:0` as a visible border (write `border-*:none`), and it cannot evaluate `max()`/`vh` in padding (use px when fixing spacing).
- Muted text on cards needs at least 4.5:1: keep ink opacity at or above .75 on `#F6F8EC`.
- Optional deeper pass: `/impeccable critique` or `/impeccable polish` on `guizang/index.html`.

## 6. Hand-over
- Commit `presentations/<deck-name>/` and push to the session branch.
- Send the user a preview (contact sheet PNG), the PDF and the PPTX (`SendUserFile`), plus the GitHub folder link.
- Report honestly which renderers could not build in this environment (e.g. npm, esm.sh or Quarkdown blocked) and why. Never skip a tool silently.
- List the remaining placeholders. Offer to upload the PPTX to the same Drive folder as the source deck; don't do it unasked.
