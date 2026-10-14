# Projection plots: extraction and specification

Four observed practice solutions contain projection plots; the canonical example contains a fifth. All were read at original raster resolution. Legacy widget screenshots were also inspected in full, preserving complete option order and superscript interpretation. Each projected region carries explanatory geometry; the learner prompt does not depend on reading a graph. Rating: light.

| Source asset | Geometry observed | Marked scale |
|---|---|---|
|3c03dde21942c60de527ace896bb51ad8070781126d72f5be5e2f6069700736d|full circle centered(−3,0), radius3, tangent to origin; pale blue fill and blue boundary| x ticks−6,−3, origin; arrowed x/y axes; equation label above |
|ccc5cab37aed89c0d701ce0195414796211ddc73a498eaaa1ff145a45c42e9fd|lower half circle centered(3,0), radius3; horizontal diameter from0 to6| x ticks3,6, origin; circle equation below; arrowed axes |
|831de8cf1d9833f8674a7e4cb69d01098970eefb9cf576c0537fa7be471c8c2c|left half circle centered(0,2), radius2; vertical diameter0..4| y ticks2,4; equation near upper left; arrowed axes |
|b66b8db18b2f5773addc2d00c02f2f15f4a7ead53323418e63bd50457f74466b|right half circle centered(0,4), radius4; vertical diameter0..8| y ticks4,8; equation near upper right; arrowed axes |
|a551e379767395a2422f690a66fc38defab64cff03c752c0c9a5a0748561d2f7 canonical|full right circle centered(1,0), radius1, tangent to origin| x ticks1,2; arrowed axes |

Parameterized specification: compute the polar boundary R(θ)=2(cx cosθ+cy sinθ) and sample the family's actual angular interval. Fill from origin through this boundary and back to origin, making the correct diameter/arc for half-disk restrictions. Equal axis scale, exact source center/radius, boundary equation, signed ticks, pale blue region, blue edge, arrowed axes. Derive bounds from center±radius with0.6a padding; label sits above geometry. Light gridlines are authored styling, not extra assessed data. All plotting uses the exact generated instance and no independent resampling.

Raw evidence reuses source asset references exactly. Normal output recreates its own parameter-dependent plot with Matplotlib (FigureCanvasAgg); no SVG or image models. The renderer uses a private module lock for Matplotlib thread safety, unique temporary PNG names, atomic final writes and atomic JSON sidecars. Cache hits require both files. Sidecars record Python/Matplotlib versions, radius, center, angles and sampled extents. Style-version changes add new assets without pruning any cache. The validator tests simultaneous fresh calls at identical and different parameters in a private directory and verifies sidecar geometry and distinct identities. Full-resolution final review plots were inspected: both semicircle orientations, signed full disks and quarter disk match source geometry and remain legible.
