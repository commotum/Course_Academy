# Plot extraction and specification

## 1. Originals

All four PNGs were opened on white at their full original 353×298 resolution, as `original-0.png` through `original-3.png` and the combined inspection sheet `original-contact.png`.

| Original | Source reference | Role |
|---|---|---|
| 0 | images/31/31b430f003171dcc04a8f17402d6035fbbc305c244d3676bbf5da83fa447bd50.png | q-28675, q-29608 worked solutions and tutorial |
| 1 | images/32/326418398ce1a33f03a21f3bdb58107856f4ccb72241429f1604486281e60822.png | q-27638 and canonical worked solutions |
| 2 | images/73/732955302ca49a41f6c43cf242d7c869e630e88d804c4b56a5beb3b081f2d230.png | q-103289 worked solution |
| 3 | images/c2/c2d0606829588b01f6cba2fa4785b201c47a6d9ffa325d54e64544c9769d7e4a.png | q-103295 worked solution |

Each shows three blue increasing tangent branches, crossing the x-axis at −π, 0, π. Dashed gray vertical asymptotes stand at −3π/2, −π/2, π/2, 3π/2. The black axes cross at the origin and have arrows pointing right/up, with x/y labels. Signed y ticks are −4, −2, 2, 4; x ticks are the six stated half-π/π positions. Curves approach every adjacent asymptote, leaving the frame through top/bottom. No filled/open endpoint is marked. No answer option contains a plot. The differences between the four assets concern raster composition/text positions, not meaningfully different functions.

## 2. Generalized visual

A standard, untransformed tangent graph used as fixed worked-solution context. None of the permitted parameter changes alters the plotted function, its zeros, signs or asymptotes. Its geometry is independent of proposed true/false claims, which remain text. Therefore the plot requirement is none for changed instances: a single reusable graph suffices.

## 3. Components

The Matplotlib recipe fixes y=tan x and separately samples numeric coordinates in each branch, never across an asymptote. Axes bounds are x∈[−1.9π,1.9π], y∈[−5,5]; branch centers are −π,0,π; poles are odd half multiples in view. Exact labels are shared across all normal questions. Styling: blue solid curve, gray dashed poles, black axes/ticks, white opaque background. The figure is 768×640 pixels for readable review; aspect ratio is a presentation choice because no metric geometry is assessed.

## 4. Reusable specification and QA

`graph(force=False)` returns the normal solution asset path. `tangent.png` is created using Matplotlib, with `tangent.json` storing actual Python/renderer version, bounds, exact anchor sets and PNG hash. Cache reuse requires both files; fresh writes use unique temporary paths and atomic replacement. No direct SVG/image model is used. Raw observed profiles retain exact original asset references for string fidelity. The rendered graph was independently opened: signed tick labels, x/y labels, axis arrows, three zeros, four dashed poles, branch direction and clear separation all matched the extracted geometry. Exact raster styling is not claimed. The validator also independently checks tan(kπ)=0 and cos((k+1/2)π)=0 at every rendered anchor and the renderer provenance/hash.
