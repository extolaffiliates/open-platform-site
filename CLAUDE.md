# CLAUDE.md

## Presentations: always use the full toolkit

Whenever the user asks for a presentation, deck, slides, pitch, keynote, QBR or similar, ALWAYS use all four repos
together, following `.claude/skills/mckinsey-deck/SKILL.md`:

1. **McKinsey method** (`mckinsey-deck` skill): question -> SCR storyline -> ghost deck of action titles -> slides.
2. **OpenDesign** (`~/tools/open-design`): pick a design system from `design-systems/` (default `corporate`,
   plus Extol brand colours) and use its skills (`data-report`, `frame-data-chart-nyt`, `frontend-slides`) for exhibits.
3. **Guizang PPT skill**: render the live single-file HTML deck (Style B Swiss for data, Style A for narrative).
4. **Spectacle** (`~/tools/spectacle`): render the same storyline as a React/MDX deck.
5. **Quarkdown** (`~/tools/quarkdown`): render the same storyline as a `.qd` source with `.doctype {slides}` -> HTML/PDF.

Deliver all outputs from one shared storyline in `presentations/<deck-name>/`. If a tool cannot run (e.g. network
policy blocks npm or Java downloads), still write its source files, and tell the user exactly which tool could not
build and why. Never skip a tool silently.

Tools are installed by `presentation-toolkit/install.sh` (the SessionStart hook runs it in quick mode).
