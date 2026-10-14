# Presentation toolkit

Consulting-grade decks for Extol Affiliates: the McKinsey method (as a Claude skill) plus four open-source renderers.

- Install everything: `./presentation-toolkit/install.sh` (clones to `~/tools`, skills to `~/.claude/skills`).
- Method: `.claude/skills/mckinsey-deck/SKILL.md` (loaded automatically by Claude Code in this repo).

## The method (slideworks.io, "How McKinsey consultants make presentations")

1. **Frame the question** and write the answer in one sentence before any slide exists.
2. **Storyline**: Situation -> Complication -> Resolution, then a MECE pyramid of 3-5 supporting arguments. Answer first.
3. **Ghost deck**: action titles only, one per slide; the titles alone must tell the story (horizontal read).
4. **Slides**: one message each; the exhibit proves the title (vertical read); highlight the one series that matters; source every number.
5. **Exec summary up front, decision ask at the end.**

## The four tools compared

| | Guizang PPT skill | OpenDesign | Spectacle | Quarkdown |
| --- | --- | --- | --- | --- |
| What it is | Claude/Codex skill that writes one-file HTML decks | Local-first "Claude Design" app: daemon + web UI driving your agent CLI, 500+ skills, 100+ design systems | React library for slide decks | Markdown superset compiler (functions, variables) -> HTML slides, docs, books, PDF |
| Input | Prompt | Prompt + design system | JSX / MDX / Markdown | `.qd` Markdown |
| Output | Single `.html`, presenter mode, rehearsal timer | HTML artifacts, decks, prototypes, exports | Web app (deployable), PDF via print | HTML, PDF |
| Edit in PowerPoint | No | Via `pptx` skills | No | No |
| Best for | Keynotes, live talks, social covers | Exploring many visual directions fast, brand systems | Dev-heavy, interactive, version-controlled decks | Long-form reports + slides from one source |
| Runtime | None (Node only for validators) | Node 24, pnpm 10.33 | Node, pnpm | Java 17+, Chromium for PDF |
| Licence | AGPL-3.0 | Apache-2.0 | MIT | GPL-3.0 |
| Weak spot | No collaborative editing, light on dense tables | Heavy (460 MB repo), early-stage, many moving parts | Engineering effort per deck | Smaller ecosystem, typesetting learning curve |

### Recommendation
- **Client/board decks that get edited by others** -> keep `.pptx` (`anthropic-skills:pptx`), structured with `mckinsey-deck`.
- **Talks, webinars, launch keynotes** -> Guizang Style B (Swiss) for data, Style A for narrative.
- **Reusable Extol report templates (proposal + appendix + slides from one source)** -> Quarkdown.
- **Interactive sales demos embedded on the site** -> Spectacle.
- **Brand exploration / many directions quickly** -> OpenDesign (run locally, not in CI).

Licence note: Guizang (AGPL) and Quarkdown (GPL) are fine as tools; do not copy their source into proprietary products you distribute or host.
