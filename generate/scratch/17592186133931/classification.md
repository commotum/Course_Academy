# Classification — basis 1356

Database `math`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; source wrapper is preserved unchanged in `source.json`.

| Captured level | Practice count | Field types | Distinct families | Plots |
|---|---:|---|---:|---|
| easy | 0 | absent | 0 observed; 1 authored constant-divergence family | none |
| moderate | 10 | 9 five-choice scalar math radios; 1 single integrand math blank | 10 observed | none |
| hard | 0 | absent | 0 observed; 1 authored canonical polynomial family | none |
| unrated | 1 | five-choice scalar math radio, missing correct ref and solution | 1 observed `xz` family | none |

Each original scalar bank is retained as its own public `observed:<db_id>` profile, including all original distractors. Radios with superficially similar polynomial divergences are not merged: their field components, zero-partial positions, cancellations, factor allocation, primitive notation and endpoint stages differ.

| Source | Template | Divergence | Answer / shape | Original bank |
|---|---|---|---|---|
| 17592186134139 | xz | 2z | designation absent; independently 2, radio | −3, 2, 4, −1, 3 |
| 17592186134140 | cos | 2x cos z | 4, radio | 1, 12, 8, 2, 4 |
| 17592186235537 | context_setup | prior part states 2x | 2x integrand fragment, blank | 2x |
| 17592186281505 | xy_a | 3xy | 48, radio | 28, 36, 16, 12, 48 |
| 17592186281506 | log | y/x | 4, radio | 2, 4, 6, 1, 8 |
| 17592186281507 | affine | 2x+2 | 6, radio | 2, 3, 6, 8, 4 |
| 17592186281508 | xy_b | 4xy | 6, radio | 2, 12, 6, 3, 4 |
| 17592186374200 | cancel_x | 2x | 32, radio | 16, 36, 32, 18, 24 |
| 17592186374207 | cancel_x2 | 3x² | 12, radio | 12, 9, 6, 18, 24 |
| 17592186430948 | cancel_z | 4z | 18, radio | 8, 3, 12, 9, 18 |
| 17592186430950 | exp | 3x² e^z | 4, radio | 2 ln 3, 8, 4, (ln 3)/2, 2 |

Owning topic: 17592186050534, The Divergence Theorem (MA 2135). Route follows `activity/first-step` then `step/next`: Introduction → The Divergence Theorem → Calculating the Flux Across a Surface → Writing the Flux Across a Closed Surface as a Triple Integral → Calculating Flux Across the Surface of a Known Solid → Calculating Flux Across a Closed Surface. The latter two siblings distinguish known-solid-volume and setup-only tasks from this assessed full calculation. Topic prerequisites include triple-integral volumes, flux through closed surfaces and Green's theorem in flux form. All normal questions remain rectangular closed-surface calculations; no new shapes, variable boundaries, coordinate changes or direct face integrals are introduced.

The easy authoring anchor is the lesson's tutorial field `<2x+1,3z,xy>` over a rectangular solid. Hard's anchor is the assigned KP's canonical field `<e^z,x²y²,4x²yz>`; positive translated bounds author the extra endpoint bookkeeping within this same method. Each level retains equal reasoning demands throughout its domain.

No practice prompt, bank or solution contains a plot reference. Lesson illustrations motivate the theorem but are not assessed data in these questions and do not enter generated output. Plot rating none needs no renderer.
