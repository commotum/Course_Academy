# Plot extraction and specification

## Stage 1 — Specific source plots

Inspected all nine practice images and canonical e9441. Each is a small approximately 360×304 white/transparent diagram: black horizontal/vertical axes, positive-end arrowheads, x/y labels; repeated blue tail-anchored arrows across quadrants; no numerical ticks or grid. q122296 shows rightward/downward on x>0, leftward/downward on x<0, growing horizontal component with |x| and constant downward component. q122463 is uniform up-left. q122629 is rightward with vertical component increasing with x, downward left of y-axis and upward right of it. q122631 has vertical arrows toward x-axis, increasing length with |y|. q122632 is vertical, downward left/upward right of y-axis, increasing with |x|. q122633 is horizontal left below/right above x-axis, increasing with |y|. q122634 is uniform rightward. q122637 is uniform downward. q122630 has constant left component and vertical component matching y, with increasing vertical lengths away from x-axis. Canonical e9441 has horizontal arrows toward the y-axis growing with |x|.

## Stage 2 — Shared pattern

A qualitative full-plane vector field conveys component directions, zero components and growth/dependency. Absolute arrow-length scale is unspecified, so a uniform positive display scale does not affect identification. It must be global per field, never independently normalize each vector.

## Stage 3 — Components

White background; equal-aspect x/y coordinates; blue field arrows, black positive-axis arrowheads/labels; rectangular quadrantal lattice; full field formulas supply each arrow vector at its tail. There are no curves, integral paths, trajectories, separate samples, or answer plots. Coordinate labels are legible and not covered by field arrows. Bounds include tails and arrow tips. Prompt role only. Source copies live in source-images and retain exact image bytes.

## Stage 4 — Reusable specification

Matplotlib Agg renders every changed field. Tail coordinates are odd half-integers from -4.5 to4.5 in both axes (100 arrows), preserving the source's axis-offset lattice. Evaluate both exact components at every tail, then apply one display scale 0.85/max magnitude. Bounds [-5.7,5.7], axes from -5.6 to5.25, labels at5.4/5.45. Figure 4.2×3.7 inches at140dpi. Colors/styling fixed. No ticks/numeric scale, since the assessment is qualitative. Signs, zero status, growth ratios and coordinate dependencies come from the same instance that supplies the correct choice.

PNG naming hashes the actual full field and style. Cache hit requires both PNG and sidecar; each input/temp PNG/temp sidecar has a unique filename; atomic replacement of completed outputs prevents mixed-instance artifacts. Sidecar records exact tail/vector values, global display scale, bounds, runtime and dependency paths. Cached Python3.10 Matplotlib dependencies are read only; no installation or shared-environment changes. Concurrent tests make fresh identical-output and different-output writes inside a private temporary folder and verify exact sidecar math. No caches are pruned.

All original and generated review diagrams are inspected as rendered contact sheets. Arrows preserve intended directions/growth, axis labels remain clear, tips fit within bounds, and directions near the axes remain visible. Heavy plot rating applies to all templates.
