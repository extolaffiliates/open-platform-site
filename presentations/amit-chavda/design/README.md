# Design direction (OpenDesign)

- Base system: `open-design/design-systems/corporate`: structured grid, minimalist layout, 8pt baseline, Poppins display / Open Sans text / IBM Plex Mono labels.
- Colour swap: corporate's blue/purple replaced by the Extol palette (`tokens.css`). Dark slides use Pine, accent is Sage, page is Cream; never pure black or white.
- Chart rule (OpenDesign `frame-data-chart-nyt` + McKinsey method): one highlighted series in Sage/Pine, everything else Moss at low weight, direct labels, no legend.
- Every renderer (Guizang, Spectacle, Quarkdown, PPTX) uses these tokens.
