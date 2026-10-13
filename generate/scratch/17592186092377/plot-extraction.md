# Plot extraction and generator specification

## Stage 1: specific plots

All 15 original prompt assets are present under `/media/jake/SSD/EDB/math/images`. Original plot montages source-plots-0.png through source-plots-2.png were visually inspected, with alpha composited onto white so source axes/labels remain visible. No answer-choice or worked-solution plots occur.

| Source | Shape and geometry | Endpoint cues |
|---|---|---|
| q-10255 | cycloid; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-10260 | power; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-10256 | astroid; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-10261 | epicycle; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-348086 | involute; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-348088 | involute; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-351427 | circle; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-351428 | circle; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-351429 | linear; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-351438 | spiral; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-351439 | astroid; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-351471 | epicycle3; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-351474 | linear; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-351505 | polynomial; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |
| q-351508 | power; exact x/y listed in Stage 1 | solid assessed arc, dotted continuation, start/end parameter labels and direction arrow |

## Stage 2: generalized visual pattern

Cartesian parametric curve, solid blue assessed interval, faint dotted continuation, exact interval endpoint dots/labels, and a forward parameter-direction arrow. The plot supplements the stated formulas and does not require measuring a length. Moderate plot rating applies to the 15 templates requiring a parameter-dependent curve; three source templates have no plots.

## Stage 3: components and mathematical ties

Coordinates are cX(t),cY(t). The plotted interval is the identical [a,u] used by the integral. Both endpoint labels are derived from the same exact parameters. The arrow uses points from the exact sampled assessed segment, preserving source orientation. Dotted context is visibly different from the assessed segment. Axes are x/y, equal aspect, small grid, white background. Original assets are reused only when c=1 and u=b exactly.

## Stage 4: renderer specification and QA

`render_plots` computes 401 exact-instance numeric coordinate samples and 601 context samples, writes data under plot-input/, and delegates to `render.py` using Matplotlib Agg. Figure 5.8×4.6 inches, 135 dpi, blue curve width 2.3, endpoint annotations and arrow, equal aspect and tight layout. The primary environment lacks Matplotlib; a cached read-only Python 3.10 dependency fallback is used, with runtime versions recorded in render-provenance.json. No package installation, image model or direct SVG.

Original visual QA: source-plots-0.png, source-plots-1.png, source-plots-2.png. Generated visual QA: generated-plots-*.png montage pages, and individual plots/ content files linked by review.json. Check shape, interval endpoints, parameter arrow, equal scaling, contrast, labels and clipping for every generated plotted template.


Final visual review: all 15 source plots and 50 generated/default/boundary/CLI assets were inspected in source-plots-0–2.png and generated-plots-0–8.png. Direction arrows follow increasing t. Labels are inside visible bounds; solid assessed arcs and dotted continuation differ clearly. The earlier overly broad spiral context and clipped labels were corrected.

The canonical-context e-603 spiral asset images/15/15d185178bf8882f837c19361d630c0e537e145ca2337cad4655677255d0348a.png was also inspected; it is lesson context and is not included in the 15 counted practice plots.
