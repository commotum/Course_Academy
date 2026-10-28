# Steps 5 and 7 — plot extraction and generator decision

The eight practice sources have no asset references or plots in the prompt, solution or choices. Their questions use a displayed repeated integral with an empty box. Plot rating is **none**. Step 7 needs no renderer.

The canonical example e-12382 contains `images/69/69764cda6db58d51cf12ab33a352191513d3f572292203135108bfc15f902584.svg`. Its original path remains exact in frozen evidence. XML inspection of the full source asset, including its MathJax title, paths, viewBox and dimensions, identifies a typeset equation rather than a geometric diagram. It displays the surface integral equal to ∫₀²∫₀¹ [empty boxed expression] dy dx. The box’s generated HTML in the SVG title is an internal MathJax formatting artifact, not mathematical surface geometry. There are no axes, geometric scales, arrows, domain shading or labels to reconstruct. `plot-extraction.json` records its original path, read-only inspection path, SHA256 and complete decoded title.

The owning topic’s polar sibling has a semicircle image; that diagram belongs to the separate polar-evaluation KP and is not used in this generator. This KP has only rectangular Cartesian setup questions. New mathematical content stays in LaTeX; no direct SVG, image model, Matplotlib or TikZ output is needed. No source path was silently rewritten to a preview path.
