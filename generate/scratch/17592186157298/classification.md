# Classification at basis 2758

KP 17592186157298, UUID aad77980-4324-5d52-a93f-a37ab3390ef8: Converting an Integral Over a Region Enclosed Between Two Curves to Polar Coordinates.

All 11 practice questions have one `selection` radio field, five math choices, a field-owned correct answer and a worked solution. All are rated **moderate**. The canonical example is evidence only, never available practice. `reference/initial/source.edn` and `source.json` retain the complete captured records. `reference/initial/inventory.json` records the application's current request at the same basis; its `available: 0` is an unclassified-job sentinel, not a count of the moderate bank.

| Template / source ID | Circle center; radius | Line; selected region | Integrand | Plot rating |
|---|---|---|---|---|
| q-83789 | (0,1); 1 | y=1; full upper cap | y² | moderate |
| q-83980 | (0,0); 4 | x=2√2; first-quadrant cap | y/x | moderate |
| q-161101 | (-1,1); √2 | y=x+2; upper-left cap | xy | moderate |
| q-85065 | (-2,0); 2 | x=-3; full left cap | xy | moderate |
| q-85067 | (0,0); 1 | x=-√2/2; second-quadrant cap | √(x²+y²) | moderate |
| q-85182 | (2,0); 2 | x=3; fourth-quadrant cap | y/x² | moderate |
| q-161100 | (1,1); √2 | y=2-x; upper-right cap | x | moderate |
| q-85062 | (0,-2); 2 | y=-3; full lower cap | x²+y² | moderate |
| q-85181 | (0,2); 2 | y=3; second-quadrant cap | x²/(x²+y²) | moderate |
| q-83979 | (1,0); 1 | x=1; full right cap | x+y | moderate |
| q-83975 | (0,0); 2 | y=√2; first-quadrant cap | x² | moderate |

Eleven prompt/solution mathematical backbones are retained separately: changing the supplied integrand or centered-versus-offset circle changes the substitution or radial-bound stages. Each has one complete source choice-bank profile named `<source>:complete-bank`. Every original choice is assigned explicitly in `components.json`, including exact source value, field/answer identities, tuple recipe, and replay result. The generator never pools distractors from different profiles.

The source plots have been inspected in `reference/initial/source-contact.png`. Each template needs new figures when its scale changes: two recurring figures communicate the Cartesian shaded region and its angular bounds. Partial caps require an axis boundary in addition to the named line and circle; their particular sector must stay fixed. Source plots are readable. There are no plot choices or mathematical images replacing answer values.

Easy and hard have no source evidence. This is a bounded unsupported capability, not proof that such questions are mathematically impossible. Moderate templates are not relabeled. Both unsupported bands retain an explicit reserve deficit of five, and new evidence must reopen classification.

Source errors remain unchanged: q-161100 and q-161101 have solution diagrams labeled with squared radius 1 instead of 2; q-161101 has one intermediate lower-bound denominator sinθ−sinθ instead of sinθ−cosθ; q-83975 has sin²θ in one intermediate x² substitution instead of cos²θ; q-85062's below-origin diagram has inconsistent positive-looking line/tick labels. Generated solutions and figures derive their values from the equations. These source instances are conservatively excluded from this package's validated availability calculation.
