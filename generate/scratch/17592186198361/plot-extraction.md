# Plot extraction / specification

No practice prompt, worked solution or answer option contains a plot asset. All rated source transformations use inline TeX matrices. The canonical e-7285 uses two unchanged notation rasters, and the lesson introduction uses one conceptual diagram. All three were inspected at **original resolution** using the actual stored PNGs, not just Markdown references.

1. Specific assets: `b8/b83369a26291155dbb8a5031d91fcf869cff259b7c170b6a15d58d317cee934d.png` shows T mapping the column(u,v) to the column(x(u,v),y(u,v)); `46/461f793c9e8d6c3e5e5f67f846bade4acea9d40dc6c3975659d60167c33f6579.png` shows inverse T⁻¹ mapping(x,y) to(u(x,y),v(x,y)). Neither labels numerical geometry. `66/668b8a0dae060c7929b92c6abe3601b0ede0b8444d92f33f4a8b5627410a4447.png` shows an orange rectangle Δ in a uv frame, a blue curved region D in an xy frame, pink T arrow pointing right and T⁻¹ arrow pointing left. It illustrates the change-of-variables formula generally, with no coordinate tick values.
2. Shared visual idea: forward/inverse coordinate maps and region correspondence. This is explanatory context, not a diagram-reading assessment.
3. Fixed components: symbolic variable-column labels; generic axes/regions/directional labels in the introduction. There are no parameter-connected plot labels, bounds or distractor curves.
4. Reusable specification: keep these unchanged if rendering the canonical/introductory lesson itself. Practice generator source-shaped prose uses its original TeX matrices and never imports a generic curved-region diagram as if it depicts a sampled linear parallelogram. No changed diagrams or new assets are needed. Plot rating **none** at every practice level.

Full-bank rasters for unrated originals `/home/jake/Developer/MA/DATA/Lessons/4132/Source/Sections/03-question-38129.png` (1460×1488) and `04-question-38371.png` (1460×1190) were inspected at original resolution. They show five mathematical text choices, not plotted choices; captured JSON reproduces all five displayed formulas and supplied coordinate maps. These rasters do not expose a correct designation.

Asset dimensions and hashes are recorded in `plot-provenance.json`. No Matplotlib/TikZ render was required; no generated SVG or image model is used. Runtime Python/SymPy versions are recorded separately in validation.json.
