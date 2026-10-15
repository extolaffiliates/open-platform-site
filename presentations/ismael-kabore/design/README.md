# Design direction (OpenDesign)

- Base system: `open-design/design-systems/corporate`: structured grid, minimalist layout, 8pt baseline, Poppins display / Open Sans text / IBM Plex Mono labels.
- Colour: certified Extol tokens from `extolaffiliates/website` DESIGN.md §04 (`tokens.css`): Oat page, Forest ink, field-top dark slides, Moss accent on dark, Fern accent on light; never pure black or white.
- Logo: `extol-logo-512.png` (website), transparent marks `extol-mark-on-light.png` / `extol-mark-on-dark.png`.
- Type: the website uses Oranienbaum (one weight); decks keep a sans for dense slides, as in `Effectivepoint_x_Extol`.
- Chart rule (OpenDesign `frame-data-chart-nyt` + McKinsey method): one highlighted series in Sage/Pine, everything else Moss at low weight, direct labels, no legend.
- Every renderer (Guizang, Spectacle, Quarkdown, PPTX) uses these tokens.
