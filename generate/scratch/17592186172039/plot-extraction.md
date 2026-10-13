# Four-stage plot extraction and step 7 specification

## 1. Individual source diagrams

The source image directory is `/media/jake/SSD/EDB/math/images`. Four distinct source files were visually inspected; unchanged copies are preserved under this evidence folder's `images/` directory so `review.md` renders exact replay references.

| Diagram | Sources / use | Quadrant signs I,II,III,IV | Visible detail |
|---|---|---|---|
| images/6e/6ef852c9c15dc6f591119906abe479949f929edb6dc26f21588b4de545d02da2.png | q96767,q119766,q97482 | +,−,+,− | Four labels; alternating blue/beige backgrounds |
| images/2c/2c218c7df2bf4e159b4bffaccb4296beab8e3f44ab82d56b3589050af92ccf8e.png | q119769,q97477,canonical | −,+,−,+ | Four labels; opposite alternating colors |
| images/d1/d1e4f48450a7f2032d755a5255d1a1e8a726dd16d273dae5dc1e587826d5ce58.png | q119774 | +,+,+,+ | Uniform blue; source labels only in I and III, applying globally |
| images/96/96c937cf10d45d8870a4a56e257d184dcf2e4caf11312c05df9f385f9c5ee7a8.png | q97487 | −,+,+,− | Blue left, beige right; four labels |

Each approximately 354×298 raster has centered black coordinate axes, positive-direction arrowheads, x at right and y above, no tick values, no slope segments, and labels `f(x,y)>0` or `<0`. This is a qualitative sign-region diagram, not a drawn slope field. There are no geometric endpoints or scale-dependent features. Zero sets are explained in the surrounding source prose; the images do not explicitly label axes as zero. Those are coordinate axes, not a universal claim that f vanishes on both.

## 2. Generalized visual pattern

A fixed coordinate plane shows the four usual open quadrants, whose fills and strict sign labels derive from the exact printed monomial. It illustrates the global sign classification used by the three statements. The plot rating remains **light**, one small simple worked-solution image. No prompt/choice plots are needed.

## 3. Component mapping

Fixed: white margin, centered x/y axes, arrows to positive directions, axis letters, no ticks, rectangle quadrant boundaries. Variable: four signs, blue fill for positive, pale beige for negative, strict f(x,y) comparison label. Image role and placement are fixed between the sign-map introduction and statement checks.

The relevant zero-set data is separate from coordinate-axis styling. Both x=0 and y=0 are zero for observed bilinear/parity monomials. For authored easy cx only x=0 is zero; y=0 generally has nonzero slope. Easy therefore receives its own diagram/sidecar even when an observed xy² diagram has the same quadrant colors. The solution explicitly states the correct zero set.

## 4. Reusable specification, renderer and QA

`render_plots(parameters)` computes exact quadrant signs with SymPy. It reuses an immutable source image only when both the four signs and observed zero-axis semantics match. All missing maps render with **Matplotlib**, never direct SVG, image models or a newly installed dependency. Six authored diagram files cover two easy sign patterns, positive xy², both x²y signs, and negative x²y². Authored maps label all four quadrants, avoiding ambiguities from sparse source annotations.

The primary Python 3.13 venv lacks Matplotlib. `render.py` uses the existing cached read-only Python 3.10 runtime/wheels, as demonstrated in earlier scratch work. `render-provenance.json` records exact versions and resolved dependency locations. It writes only within this evidence folder and a unique matplotlib cache directory in /tmp. PNGs and sidecars use unique temporary files and atomic replacements, preventing concurrent call mixups; the input specification travels as a dedicated process argument, not a shared input file. Four concurrent calls with identical and different maps were verified; cold-cache generator calls also require both PNG and sidecar before a cache hit, and concurrent identical/different generated instances return matching complete pairs.

The renderer never samples or makes correctness decisions. Sidecars bind four signs and zero axes to the instance. Positive-symbol substitution from the actual displayed equation independently verifies every sign on the entire open quadrant and checks values on both axes. All six authored plots have been rendered and visually inspected: signs, fills, axes/arrowheads, x/y labels, and boundaries are legible, with no clipping or overlaps. The first two cx maps deliberately do not inherit a false y=0 zero claim.
