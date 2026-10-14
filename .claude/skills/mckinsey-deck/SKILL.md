---
name: mckinsey-deck
description: Build a consulting-grade (McKinsey-style) presentation - storyline first, action titles, one message per slide, sourced exhibits - then render it with ALL of OpenDesign, Guizang, Spectacle and Quarkdown. ALWAYS use when asked for any presentation, deck, slides, board deck, strategy deck, pitch, QBR, investor update, "McKinsey style" slides, or any deck meant to drive a decision.
---

# McKinsey-style deck

Work in this order. Do not open a rendering tool before step 4.

## 1. Frame the question
- Write the one governing question the deck answers, the audience, and the decision you want from them.
- Write the answer in one sentence (the "governing thought"). If you cannot, you are not ready to make slides.

## 2. Storyline (Pyramid Principle + SCR)
- Opening: **Situation** (what the audience already agrees with) -> **Complication** (what changed / what is at risk) -> **Resolution** (the governing thought).
- Under the governing thought, 3-5 supporting arguments that are MECE (no overlaps, no gaps).
- Each argument is backed by facts/analysis. Answer first, evidence second (top-down), never a chronological "here is what we did".

## 3. Ghost deck
- Write the deck as a list of **action titles only**, one per slide. Read them top to bottom: they alone must tell the whole story (the "horizontal read").
- Action title rules: a full sentence stating the "so what", max ~2 lines (~15-25 words), quantified where possible.
  - Bad: "Market overview". Good: "The SMB segment grew 18% a year since 2021 and is now 40% of the profit pool".
- Sketch, for each title, the one exhibit that proves it (chart type + data needed). Mark data gaps.

## 4. Build each slide
- One message per slide. Everything on it proves the title (the "vertical read"); cut what doesn't.
- Anatomy: action title -> optional tracker/section marker -> exhibit (chart/table/framework) -> callouts that point at the evidence -> footnotes + **source line** on every data slide.
- Charts: pick by message - comparison = bar, trend = line/column, composition = stacked/waterfall, correlation = scatter. Highlight the one series that matters with the accent colour; grey everything else. Label data directly, drop gridlines and legends where possible.
- Consistent grid, fonts and colours across slides; no decorative clip-art.
- Executive summary slide up front (the pyramid in prose); next steps / decision ask at the end.
- Never invent numbers. If data is missing, show a clearly labelled placeholder and list it in the open-items.

## 5. Render with ALL four tools (standing user instruction)
Every deck is produced in all of these, from the same storyline, into `presentations/<deck-name>/`:
| Step | Tool | Output |
| --- | --- | --- |
| Design direction | OpenDesign `~/tools/open-design/design-systems/<system>` (default `corporate`) + skills `data-report`, `frame-data-chart-nyt`, `frontend-slides` | Colours, type, chart specs used by every renderer |
| Live deck | `guizang-ppt-skill` (Style B Swiss for data/strategy, Style A for narrative) | `guizang/index.html` (presenter mode) |
| React deck | Spectacle (`~/tools/spectacle`, MDX or JSX) | `spectacle/` project |
| Markdown deck + PDF | Quarkdown (`.doctype {slides}`) | `quarkdown/main.qd` -> HTML/PDF |
Also produce a `.pptx` (`anthropic-skills:pptx`) when the deck must be edited by others. For Extol Affiliates work, apply `anthropic-skills:extolaffiliatescolours`.
If a renderer cannot build in this environment, still write its source files and report which one failed and why. Never skip a tool silently.

## 6. Quality check before handing over
- Horizontal read: titles alone tell the story; each title is a claim, not a topic.
- Vertical read: every slide's body proves its title; every number has a source.
- MECE check on the argument structure; SCR is visible in the first 2-3 slides.
- One clear ask at the end. Typos, alignment, consistent number formats (units, decimals, currency).
