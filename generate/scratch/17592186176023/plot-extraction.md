# Plot extraction and generator specification

## 1. Specific original diagrams

assets.json preserves14 distinct PNG references and their source IDs/roles. source-montage.png composites transparency on white. Canonical: radius2 upper semicircle, segment from(−2,0) to(2,0), arc back to(−2,0), positive orientation; solution blue upper half-disk. Moderate solution diagrams: full disks of radii2,5,1,√2,3, all counterclockwise orange boundaries, positive horizontal/vertical axes and radius labels, blue interior with D and C labels. q126759 reuses the radius2 disk from q109119.

q125717: radius2 first-quadrant quarter disk; bottom segment points right, circular arc points counterclockwise up/left, vertical segment points down. q126747: radius4 first-quadrant sector bounded byθ=0 andπ/3; bottom rightward, arc increasingθ, oblique ray inward, dashed angle guideπ/3 and dashed extension toward radius4 on y-axis. Solution shows blue D. q126756: radius3 second-quadrant quarter disk; y-axis segment points upward, arc points left/down, negative x-axis segment points right. q126758: radii2 and4 first-quadrant annular sector; bottom segment rightward, outer arc increasingθ, y-axis segment downward, inner arc decreasingθ. Source drawings are axes-based without a full Cartesian grid. No option plots exist; therefore the complete displayed answer banks are scalar banks.

## 2. Shared role

Hard plots supply outer/inner radii, θ bounds and positive boundary traversal, all needed to evaluate the scalar integral. Moderate and easy solution plots illustrate D after the theorem is applied. Plot rating moderate across generated source-shaped families; parameter changes require new geometry.

## 3. Components

White background; equal-scale axes through the origin; orange circular arcs and radial segments; dark direction arrows; exact cardinal radius labels; optional rational-π angle guide; blue filled D only in solution images. Outer radius√s, inner radiusa, anglesπ·lo,π·hi come from the exact question instance. Outer traversal increasesθ, terminal ray inward, inner traversal decreasesθ, initial ray outward. Full disks have no radial rays. Arrows follow each segment's ordered sample coordinates. The common radius label uses a radical for s=2. Plot bounds derive from outer radius with1.3 padding.

## 4. Reusable implementation

render_plots(p,shaded) creates Matplotlib PNGs and exact-parameter/version sidecars in the private plots directory. The content-hash includes geometry and shading; seed, coefficient and bank are irrelevant to identical geometry. PNG+sidecar are both required for cache hits. Writes use unique temporary files and atomic replacements, with a process-local lock for Matplotlib concurrency. Changed coefficient does not resample plots. Fresh identical/different concurrent calls are validated.

The source geometry is transcribed from inspected arrow tails/tips, labelled endpoints and angle guide, not inferred from image paths. Original assets are reused only in explicit raw evidence profiles; normal plots are regenerated from exact parameters. Incidental raster styling is normalized. D is retained; normal axes and arrows retain all assessed orientation and endpoint cues. q126747 dashed extension is replaced by explicit cardinal radius label/angle guide on the changed boundary; no missing endpoint is silently inferred. Figure reproduction is semantic geometry fidelity, not pixel identity. review.json and review.md include each normal source-family anchor and changed variants, allowing inspection beside raw diagrams.

Visual QA of generated-montage.png covered changed full disks, a familiar radical disk, anisotropic sector, second-quadrant sector and quarter annulus, including signed axis labels and every oriented boundary segment. plot-label-review.png verifies the final full-disk D placement off the axes and restored C label; this label-only revision uses renderer_revision2 to preserve existing cache assets. No newly created image caches are pruned during parent QA.
