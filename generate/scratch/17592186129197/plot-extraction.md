# Plot extraction and reusable specification

Every original practice plot was viewed at native pixels (362×300, except q-82878 363×300). Transparent/background considerations do not alter the observed white raster. Canonical region e-7283 was also viewed. Its two tiny transformation assets are standalone math, rather than geometrical plots.

## 1. Individual native descriptions/calibrations

Pixel coordinates below are measured within each original raster, with y pixels downward. Stroke/antialias uncertainty is about 2 px; axes need independent calibration.

| Source | Origin/scale/features | Full boundary inclusion and local features |
|---|---|---|
| q-82874 | Origin (63,247); u=1 at274 (~211 px/unit), v=1 at73 (~174 px/unit). | Blue v=u⁴, red v=u, all curve segments bounding the filled lens solid/included; dotted exterior continuations are outside the bounded region. Roots at (0,0),(1,1). Dashed endpoint guide at u=1. Black vertical upward arrow through lens. |
| q-160885 | Origin (57,272); u=1 at113 (~56 px/unit); v=1 at216 (~56 px/unit). | Red left u=1 and bottom v=1 edges solid, blue v=4/u solid; endpoints (1,1),(1,4),(4,1). Fill above/below the correct sides. Upward black slice arrow. |
| q-82878 | Origin (170,267); endpoints x≈36/303 at u=±√2 (~94 px/unit); v=1 y≈199, vertex v=3 y≈66 (~67 px/unit). | Blue downward parabola, red v=1, both bounding segments solid/included; exterior dotted continuations. Dashed ±√2 guides. Upward arrow left of vertical axis. |
| q-83943 | Origin (169,265); u=±1 x≈102/237 (~67.5 px/unit); v=3 y≈54, vertex v=2 y≈125 (~70 px/unit). | Blue top v=3 and red lower v=u²+2 bounding segments solid/included; dotted continuations beyond roots. Two dashed u endpoint guides. Upward slice arrow. |
| q-83947 | Horizontal zero axis y≈104, top v=1 y≈48, vertex v=−3 y≈274 (~56 px/unit vertically). Horizontal geometry symmetric about x≈169, while drawn vertical axis x≈135: inconsistent source calibration. | Red upward parabola and blue v=1 bounding pieces solid/included, dotted exterior. ±2 guides at x≈34/304. **Do not infer a valid common horizontal coordinate scale from this malformed source.** Normal redraw fixes the axis and labels. |
| q-160710 | Origin (75,252); u=1 x≈169 (~94 px/unit); v=1 y≈159, v=2 y≈65 (~94 px/unit). | Red left u=1/bottom v=1, blue v=2/u, all three bounding edges solid/included. Vertices (1,1),(1,2),(2,1). Origin-to-v=1 and the v=1→2 segment agree within stroke allowance. |
| e-7283 | Origin/vertex (169,274); u=±2 x≈34/304 (~67.5 px/unit), v=4 y≈62 (~53 px/unit). | Solid red v=u²/blue v=4 bounding segments, dotted exterior, dashed endpoints and upward interior arrow. |

## 2. Generalization

A shaded type-I region in the uv-plane illustrates vertical integration after transforming the original xy region. The figure accompanies Step 1. All defining edges are included, each solid, and every intersection/vertex is derived from the same instance. Distinct per-axis scales are acceptable and explicitly recorded. Boundary inclusion is not inferred from shaded interiors.

## 3. Components

White background; visible u/v zero axes; signed exact endpoint tick labels; lower and upper boundary curves; vertical left segment for product-hyperbola families; light blue fill; Δ label; black upward vertical slice arrow; blue upper and red lower equations. Curve labels are placed in axes coordinates with white text backgrounds to avoid covering geometry. Source colors vary by family; consistent upper/lower colors in normal output are a documented styling normalization, with no mathematical significance.

## 4. Reusable specification

Matplotlib plots the computed interval `[lo,hi]`, lower and upper expressions at 401 points. Bounds include zero and all extrema on the assessed domain, plus margins from both spans. Every boundary remains solid; dotted outside continuations and dashed endpoint guides are incidental source context and omitted in normal output. Exact endpoints are retained as ticks; no wrong-option images are needed. The upward arrow stays inside the vertical slice and cannot resample parameters. Figure size676×546 pixels; sidecar records exact bounds, axis limits, parameters, renderer version and inclusion.

Cache key includes complete geometry/family/parameters. PNG and JSON are both required for a cache hit. Every writer uses its own mkstemp names and os.replace, with no common render-input file. Fresh identical and different calls are exercised concurrently in a private fresh directory. A per-process lock protects Matplotlib’s global mathtext parser; files remain unique/atomic across processes. Initial unrestricted threads exposed a real mathtext race; the lock fixes it. Private assets remain available for parent QA; no shared asset directories are changed or pruned.
