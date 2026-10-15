# Plot extraction and generation

The five q-122699 images are 360×304 PNGs. Each has a white background, gray unit grid, black x/y axes and numbered ticks, three orange anchor dots and three blue directed arrows. The dot is the tail; the arrowhead is the tail plus the vector, in the same units on both axes. No normalization is used. They carry the entire response meaning, so plot rating is heavy. The correct source image is also repeated after the worked solution.

All original anchors and exact displacements are recorded in reference/source-bank-mapping.json and were read at original resolution from the unit grid. Source filenames and correct designation are retained there. The canonical example uses a composite diagram and a solution diagram; these remain unchanged, excluded from practice.

Matplotlib generates every variant with the same three anchors, orange tails, blue arrows, equal axis scaling and fixed limits (-9,9) in each direction for all five choices. This expands the source viewport to include every endpoint of the bounded coefficient domain. Fixed shared axes prevent option-specific scale cues. Labels x/y and legible ticks are retained; there are no diagram option letters to become stale. No field formula appears on an answer diagram. Rendering consumes the exact instance vectors and writes a JSON sidecar. Images have reproducible content hashes in their local filenames, and are published to the application image store only if new practice is needed. The current job requires registration only, so no new image bytes need publishing.

The source contact sheet and generated review sheet support side-by-side visual inspection. Mathematical correctness is separate from styling fidelity and native grading.
