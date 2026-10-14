# Queried route cells

The moderate three-station family `sum_139689` used the literal `holes` from q-139689: A→B, B→B, C→A. Sampling copied them and validation rejected any other triple. Each other source-derived family also had its own fixed triple. Across all three-station families, C→C was never queried. Known zero/nonzero edge positions were fixed as well.

Version `route-matrix-6` treats the captured cell positions as exact replay evidence. New source-derived variants sample one loop plus two other directed relations, or three off-diagonal relations for the no-loop blank family, and shuffle the answer-slot assignment. Known occupied cells also move while their count is retained. Hard already sampled relations, but now also shuffles the loop’s answer slot. Current graph density and table formatting constraints stay intact.

Radio questions retain a+b+c, the source response shape. Blank questions retain three separate counts. No additional arithmetic operators were introduced. Explicit changed cells are supported; the same-graph regression verifies that moving queried cells changes the rendered table, solution directions, canonical answer and identities. Raw erroneous source prose is restricted to exact replay.

The before census shows one triple per template. In 100 moderate samples, the current generator uses all nine cells in every answer slot, with 40 distinct unordered triples and 99 distinct adjacency matrices. Three rendered examples (seeds 0, 3, 48) query every cell once across the set. Complete source banks still match all seven sources. Native grading passes 76 accepted and 115 rejected checks. All 800 sampled variants pass density, table-cell, answer-slot and deterministic replay checks.

This change updates the registered generator implementation and its verified package. No existing database question or learner response was modified in this task. Existing saved questions keep their previous queried cells. The former 49-variant limit and sum_139685 omission-bank exclusion depended on fixed cell/edge positions and are superseded; that omission profile is now exercised in native QA.
