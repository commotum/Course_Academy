# Template extraction

Provenance: captured `math` basis 1356, unchanged raw record in `source.json`. `extract.py` produces `templates.json` and `source-cases.json`; the normal generator consumes named parameter skeletons and never returns a literal captured question. Source replays use the same arithmetic, formatting and bank construction as variants.

## Stage 1 — Describe each question before generalizing

| Source | Original parameters | Response and distinctive structure |
|---|---|---|
| q-37400, easy | a=2500, initial=800, k=.016, t=4 | school population after time; supplied ODE; separation, integration, exponentiation, initial condition, IVP, evaluation; integer students |
| q-335280, easy | a=20, initial=8, observation=12 at 5, target=16 | soda warming; supplied symbolic-k ODE; separates and integrates; initial constant, calibrates rate, target time; integer minutes |
| q-335282, easy | a=3, initial=1.5, k=.4, target=2 | container volume; supplied ODE; decimal initial volume; constant, target time, logarithm; singular/plural minute answer bank |
| q-15370, moderate | a=1500, initial=300, observation=500 at 10, target=800 | university flu hint; derive ODE; reduced calibration and target fractions directly; integer days |
| q-335578, moderate | a=1200, initial=200, observation=500 at 4, target=900 | resistant bacteria hint; unreduced fraction followed by reduced fraction in each logarithm chain; integer hours |
| q-335542, moderate | a=800, initial=80, observation=300 at 10, target=600 | reserve parasite hint; unreduced then reduced fractions; integer days |
| q-335590, hard | a=600, first=480 at 4, second=500 at 8, t=40 | bakery hint; two conditions; divide first deficit equation by second; rate then K then future evaluation; integer loaves |
| q-335619, hard | a=800, first=620 at 3, second=720 at 9, target=760 | app hint; two conditions; ratio rate; K via exponential, square root, rational simplification; target-day logarithm; ordinal day fragment |
| q-37389, unrated | a=500, first=390 at 3, second=400 at 6, t=42 | poultry hint; captured prompt and bank only; authored hard rating and worked solution patterned on bakery |

Every source uses five complete text options in one field, key `selection`; none is a blank or an equation-fragment input. Constants `C` and `K=e^{-C}` are preserved. The source's positive-deficit assumption is preserved. Numeric thousand separators, degrees Celsius markup, logarithm notation, aligned environments, shared sentences and paragraph order are retained verbatim at the original parameters in all eight supplied solutions.

## Stage 2 — Shared pattern and instructional purpose

Separate `dQ/(a-Q)=k dt`, integrate to `-ln|a-Q|=kt+C`, use `a-Q>0` and exponentiate to obtain `Q=a-Ke^{-kt}`. Determine the available constants from initial or timed observations, then evaluate a future quantity or solve for the target time. The hard two-observation family divides the two deficit equations before finding K. These are all applications of the same first-order inhibited growth model. Different stories and known/unknown data retain the observed reasoning workload.

## Stage 3 — Components, choices and calculations

`source-bank-math.json` maps **each of all 45 original option values** to its source field, template, original parameters, correct status, recipe, evaluated result and replay profile. Each profile contains the complete bank that occurred together; no pooled distractors are mixed. All 36 wrong choices are mapped and independently verified unequal to the rounded correct value.

Observed scalar banks do not determine the original authoring error. Their replay recipe is explicit numerical normalization: for original option v and independently computed original rounded correct c0, emit `round(v * c/c0)` for the newly computed rounded correct c. The correct option itself is recomputed from the IVP, never normalized. This is an **empirical proportional replay with unknown intent**, not a recovered misconception or default generation rule. It is deliberately restricted to explicitly selected `q-ID_empirical` profiles. We do not claim that the source wrong operations have been recovered.

The default authored five-option profile consists of the correctly computed answer and four operation errors. Future-value instances use the observation value as K, omit the initial deficit, omit the time factor from the exponent, or model the observed quantity as exponential decay. Target-time instances omit division by k, use a target/observation ratio instead of the deficit ratio, linearize the exponential with the observed initial slope (and time origin), or replace the computed logarithm factor by 1 (a single characteristic time 1/k). `generation.recipes` records each exact expression and rounding. Distractor explanation is author metadata only; no invented learner-facing diagnosis is added. A collision, a distractor rounding to the correct answer, a negative or nonfinite value, or a future-quantity value outside [0,a) rejects the whole bank. Rounded quantity options must remain in [0,round(a)]. The exact values are checked before rounding; dropping a bad member or filling it from another profile is prohibited.

The solution is fixed independently of which option is selected. Source field type, option count, units and complete fragment shapes are preserved. Answer UUIDs are owned by the field. Identity includes the displayed bank and rendered content; changing seed only reorders choices for fixed parameters/template/profile.

## Stage 4 — Reusable skeleton and domains

`templates.json` contains nine extracted named skeletons. Fixed components include every shared instructional sentence, mathematical stages, quantity symbol, story, hint and answer-field shape. Variable components are named numeric roles, exact reduced fractions, K, rate-related denominators, evaluated decimals and rounded answers. Numeric roles use independently derived quantities rather than global number replacement at generation time. Complete reduced fractions are replaced as units during extraction. Source equal-value coincidences (temperature versus deficit, initial volume versus K) are handled explicitly or remain sampling constraints rather than introducing silent wrong substitutions.

Sampling bounds are authored policies: school capacities 1000–4000, initial 100–900, rate .010–.040, evaluation 2–12 years; volume capacities 3–8 with initial half-capacity, decimal target below capacity and rate .1–.6; soda capacities 20–35, initial 3–8, later observed temperature equal to capacity minus initial temperature, calibration 3–10 minutes, target above observation below capacity; moderate capacities 800–2400 with independently varied initial, observation and target values and calibration 3–12; hard capacities 500–1200, first time 2–6, integer observation deficits, and peer future horizons or target deficits. These policies include source values through explicit parameter replay but are not claimed to be original authoring ranges. Hard app deficit ratios are rational squares, preserving the shown square-root stage. All generated quantities have nonnegative time-zero values and remain strictly below capacity for finite t.

Explicit parameter sets must have exactly the expected keys; they are validated without silent resampling. Invalid domains, observation order, unsupported algebra shape or ambiguous banks raise errors. Default sampling uses bounded deterministic rejection. There is no extra mathematical branch or within-level sequencing.

## Verification and plot extraction

No practice template has plots. Stages 5 and 7 are documented as not applicable; no renderer or source image is required. `display_math.py` independently extracts numbers from the displayed prompt, solves the model, and parses/evaluates every displayed separation, integral, exponential, logarithmic, substitution, and approximation relation. Integration rows are checked through their integrands and differential substitution. Exact expressions and decimal rounding are checked separately from native selected-option IDs. Native grading uses the actual `course_academy_engine::learning::grade_field`, never an imitation grader or database writes. All evidence remains local; work stops after step 7.

## Physical answer banks and finite ranges

All observed application options are positive. School source quantities span 850–1005 within capacity 2500; poultry quantities 420–489 within capacity 500; bakery quantities 550–590 within capacity 600. Source time options are 1–5 minutes (volume), 8–19 minutes (soda), 12–45 days (campus), 8–20 hours (culture), 20–50 days (reserve), and ordinal days 10–25 (app). Default banks follow these physical domain conventions.

Two complete authored operation profiles are eligible, selected by the response demand before sampling: future-value profile = correct IVP value / use observed quantity as K / omit initial deficit / omit t from the exponent / treat observed quantity as exponentially decaying; target-time profile = correct target time / omit division by k / replace deficit ratio by target-to-observed-quantity ratio / linearize from the observed initial slope and time / replace the logarithm factor by 1, giving the characteristic time 1/k. Each has exactly five options. The profile is never assembled from a first-valid recipe pool. Any invalid member rejects the complete instance. These latter errors have definite mathematical operations, with no numerical fitting.

For the finite authored sampler, quantity options lie between zero and the selected capacity (school capacity at most 4000; hard production at most 1200). Conservative target-time bounds are volume 0–10 minutes, soda 0–86 minutes, hard app 0–54 days, and moderate 0–1063 time units. The moderate bound follows k >= log(2350/2250)/12 and maximum deficit ratio <=47; 12 log(47)/log(2350/2250) <1063. These are safe outer bounds rather than claims that every integer occurs. `validation.json` separately gives actual observed min/max across each template's tested authored banks.

Explicit empirical profiles preserve the original bank. Their automatic variant sampler scales source quantities by factors 2–4 and observation/evaluation times by factors 2–4; a supplied numeric rate is divided by the time scale. This retains the original dimensionless decay ratios and physical bank eligibility, rather than silently extending empirical scalar choices into a near-capacity region where normalized options exceed capacity. Explicit parameters can test other supported values, with whole-instance physical and collision rejection. This scaling is labeled replay-policy evidence, not inferred original distractor intent.

Generated units are inflected from each displayed integer (`1 day`, `1 hour`, `1 minute`; plural otherwise), and ordinal suffixes follow the actual integer. Source replay preserves all original singular/plural choices and ordinal fragments exactly.
