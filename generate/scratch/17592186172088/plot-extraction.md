# Plot extraction

## 1. Specific originals

`original-contact.png` shows all nine distinct source images, composited on white, including canonical e-9473. Every image has black x/y/z axes meeting at the origin, italic labels, a uniformly distributed lattice of blue arrow tails, and equal-length arrows parallel to one coordinate axis. Positive x points diagonally down-left, positive y right/down, positive z upward. Axis arrowheads distinguish positive coordinate direction. No coordinate ticks or absolute vector scale occur.

| Source | Image prefix | Geometric target |
|---|---|---|
| q-122559, q-123750 | cfc15b620216 | positive x |
| q-122664 | 7a0a919af689 | positive z |
| q-122651 | 7cb4dd61f9d4 | positive x |
| q-122668, q-123749 | f89653698d9c | negative y |
| q-122670 | 64f02fa7dcd2 | negative z |
| q-123748 | bff60466ca8a | negative x |
| q-122662 | 8d978a63c661 | positive y |
| q-122667 | 9db14c13d03c | negative x |
| canonical e-9473 | de305db47bcf | negative z |

## 2. Generalization

A 3D quiver diagram encodes which components vanish, the sign of the remaining constant component and equal arrow lengths. There is no trajectory, flowline, derivative or magnitude reading. All diagrams carry the main assessment, hence heavy.

## 3. Components

Fixed: white background, black three axes and labels, blue arrow lattice, oblique orthographic projection. Variable: exact signed target component tuple and therefore arrow direction. All target fields are nonzero constants, so their zero sets are empty. Wrong formulas can have variable-component zero sets (coordinate planes for linear/square options, sin coordinate multiples of pi, logarithm argument 1); those are checked from displayed formulas but are not drawn as target plots.

## 4. Reusable specification

Shared `render_plots` uses Matplotlib mplot3d, an orthographic view (elevation 20°, azimuth 35°), 27 points with coordinates -1.5, 0, 1.5, axis bounds ±2.5, positive black axis arrowheads, labels at coordinate 2.75, and equal common arrow factor 0.6/||target||. Components come from the exact question instance; normalize=False prevents independent resampling or componentwise scale distortion. PNG and JSON sidecar carry exact components, every tail/vector, plotting factor and dependency provenance. Axis labels sit beyond arrow tails; no numeric ticks are introduced. The different projection is a documented styling change preserving 3D geometry.

The exact signed constant original field reuses its inspected original PNG when all mathematical inputs equal the source. All other instances render from the component tuple. Coefficient changes remain qualitative; the common factor preserves direction and equal lengths without implying unsupported absolute magnitude. Unique temporary inputs and atomic PNG/sidecar replacement support concurrent calls; cache hits require both files. No SVG or image model is used.
