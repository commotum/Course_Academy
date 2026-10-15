# Finite templates

Every source's complete literal prompt, ordered fields, choices, keys, solution, source ID and UUID are in `source.json`. `source-components.json` maps every source choice to its field and exact Boolean recipe; `specs.json` records the supplied curve, field relation, orientation, ordered requested path/sign predicates, and all plot references. These are discrete correlated catalog entries, rather than independently sampled slots.

The shared response contract is to judge three claims about the flux through C and -C. Both integrals use the outward normal. Reversing the curve's traversal leaves this geometric normal and the flux unchanged. The task concerns outward-normal flux, not a circulation integral or a right-hand normal convention attached to traversal.

The ordered solution backbone is:

1. State the closed-curve flux integral and identify the outward normal.
2. Explain water escaping, entering, and balanced flow, with the two shared composites.
3. Inspect the supplied field against C and judge its sign: outward, inward, pointwise tangent, or equal total inflow/outflow.
4. Judge the applicable statements about C, displaying the integral sign.
5. Explain orientation independence using the same outward normal on -C, then display its integral sign and judge the remaining statement(s).
6. Name the selected Roman-numbered subset.

The easy backbone uses inward/outward flow. Moderate has distinct tangency and balance branches; balance does not claim pointwise tangency. Circle/ellipse shape and statement roles differ between observed entries and stay tied to their exact source asset and solution. No arithmetic, new response type, field equation, integration task or new solution stage is added to the learner presentation.

`generate(level, seed, template)` selects one complete source entry and preserves the original question/field/answer UUIDs. `batch` samples without replacement by mathematical fingerprint, up to five entries per supported level. Each source template has exactly one parameter assignment, the empty map. There are no free target, coefficient, aspect-ratio or orientation slots. Passing an unsupported extension fails explicitly. The mathematical fingerprint includes the field/curve relationship and unordered path-specific claim set, excluding seed, identity, profile name, choice order and traversal orientation.

All banks contain exactly the observed text values true and false, with the canonical answer selected by the claim's truth. These are complete source profiles; there are no inferred distractor recipes. All instructions, integral notation, plot placement and worked-solution sentences replay literally. The source description and diagram are the mathematical evidence; representative symbolic models in `reference/flux-proofs.json` check sign reasoning without pretending to recover exact coefficients from pixels.

No new mathematical variants are claimed. The whole finite catalog already exists in the database. Its supported stock can be validated and the generator registered without duplicating those records. The finite bound is a policy of this verified package. Generalizing a plotted field requires a new extracted plot specification, rendered variants, mathematical proof and visual QA before expanding it.
