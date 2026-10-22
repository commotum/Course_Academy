# Solving for One Coefficient in a Linear Combination

Captured source basis: 2607. KP: 17592186119805, UUID 33586620-e110-5a37-874f-a92103c5e9fb.
The complete source Pull, canonical example, all ten practice questions and field-owned answers are in `reference/source.*`. `source-components.json` records each source's individual vectors, scalar, target letter, prompt, worked solution, full bank and recipe mapping.

## Classification

Easy: six complete radio questions, five choices each, key `selection`. Two Markdown/value backbones: positive supplied scalar plus an unknown coefficient (q-34249, q-105152, q-105154, q-34051, q-34600), and vector subtraction with the unknown coefficient (q-34241). Dimensions two, three and four are parameter features of the same componentwise isolation method. Each source is a distinct complete choice-bank profile.

Moderate: three complete radio questions, five choices each, key `selection`. One backbone: a positive known scalar times a vector plus an unknown coefficient times another vector equals the zero vector. The first coordinate gives a candidate; substitution into the remaining coordinates contradicts the vector equality. Profiles q-34570, q-34602 and q-73923 retain their complete banks separately. The supplied second vector's first two components are nonzero, their required ratios differ, and the candidate from the first component is integral.

Unrated q-34250 has a prompt and five choices, but no correct link, worked solution or difficulty. Its mathematics implies coefficient 4; this observation is evidence only. Preserve it without modification and exclude it from rated practice and source-bank fidelity claims. No hard source exists. An absent level alone is not evidence of impossibility; this package's bounded capability deliberately supports only the observed workloads and leaves the nominal hard shortage of five explicit. New source evidence reopens classification.

All practice prompts and solutions supply column vectors directly in LaTeX. Plot rating: **none**. The canonical SVG is rendered mathematics giving the vectors, and is not used as generated content. No plot extraction or plot generation is necessary for these practice templates.

## Backbone and variable slots

For unique-coefficient questions supply `c*a + s*u = b`, compute `b = c*a+s*u`, isolate `s*u=b-c*a`, simplify that residual and read the coefficient. The subtraction profile keeps `a-s*u=b`, `c=1`, and isolates `s*u=a-b`. Keep the unknown's role, source target letter, field type, notation, dimensions per bank profile and ordered solution stages. The letter has no mathematical effect and is not a novelty slot.

For inconsistent questions supply `c*a+s*u=0`, isolate `s*u=-c*a`, use the first component to find candidate `t`, display `t*u` and the unequal required residual, and conclude no solution. Keep the two supplied vectors' roles, zero right-hand side, first-component candidate and subsequent consistency check. No new operations or field layouts are introduced.

Normal sampling is a conservative finite neighborhood, explicitly narrower than the full mathematical family: change one coordinate of either supplied vector by -2,-1,0,1,2; vary the positive known coefficient by at most one and the easy solution scalar by at most one. The subtraction coefficient remains 1. Preserve source dimension and target letter. Require a nonzero second vector, unique nonzero easy scalar, distinct complete choice values, and all inconsistent-profile conditions above. Moderate candidate coefficients remain integral; source rational distractors are retained exactly. Source parameters remain available for replay.

Compute every prompt vector, solution vector, component candidate and key from the same parameters. When a known scalar or vector changes, rebuild all dependent values. There are no independent plot parameters or eligible positional targets: the first coordinate is fixed because it is the observed first step in each contradiction proof. Coordinate values are covered separately by exhaustive domain validation.

## Choice-bank interpretation

Each profile selects all five recipes before validation. `source-components.json` maps every original option to a recipe; `t=-c*a[0]/u[0]` and `z=-c*a[1]/u[1]`. Easy recipes use the correct scalar `s` and known coefficient `c`. These algebraic patterns reproduce observed banks; their psychological interpretation is unresolved. In particular q-105154 uses inferred affine offsets `s+2` and `-s-2`, rather than asserting a particular learner misconception. Those offsets remain explicit in the frozen profile. Do not pool profiles or take the first distinct distractors from different banks. Reject the whole candidate if recipes collide or a second correct answer appears.

## Validation and persistence

`validate.py` exhaustively checks every bounded candidate, independently reads the rendered vector equation, solves its coordinate consistency, verifies the designated answer, every solution matrix and the displayed candidate equation, and runs every option through the actual learner radio grader. Source replay compares complete mathematical banks with correct designation, prompt vectors, scalar and sign, and ordered solution matrices; notation differences are reported separately. `review.md` pairs each original with a changed-coordinate variant for direct review.

Stable question identities include parameters and the complete source profile; field and answer UUIDs are owned by their parent. Seeds do not affect identity. Mathematical fingerprints exclude seed, option order, letters and common coordinate ordering/scaling. Replenishment excludes source and canonical tasks and every existing generated task, regardless of learner exposure.

The registered generator is `generate/scratch/17592186119805.py`. `replenish.py` uses existing native inventory, EDB queries, validation preview and writer. It acquires the application's `api.lock`, rechecks current basis and inventory, validates only missing fresh instances, previews, retains the exact attributed basis-guarded request, submits and verifies content at the receipt basis while holding that lock. All source questions, canonical content and learner history are preserved. Retained exact requests are recovered before new submissions.
