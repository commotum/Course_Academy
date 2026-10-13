# Initial Value Problems and Initial Conditions

Captured provenance: database `math`, basis **1356**, lineage
`01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` copies the complete
capture wrapper without changing the database evidence.

All **11 practice sources are easy**. Each asks which of three displayed systems
is a **first-order** IVP, with “Select all that apply.” The response consists of
three separate checkbox fields keyed `I`, `II`, `III`; each owns exactly two text
answers, `false` and `true`. There are 33 field banks, 66 choice values, and 33
captured correct refs. No field, difficulty, or worked-solution attributes are
missing. No blank, radio, or plotted field is observed. Plot rating: **none**.

The generator keeps eleven observed equation-structure recipes rather than
merging distinct ODE components or condition layouts. Their field layout and
opening exposition are shared. The six observed selection patterns are I only,
II only, III only, I and II, II and III, and I and III. These are six correct
designation patterns, not six opaque numerical distractor banks: every field's
complete answer bank is the same boolean pair.

The eleven sources, their exact components, all original choice UUIDs, and the
complete parameterized ODE recipes are mapped in `template-extraction.md`.
Every source is represented in `source-cases.json`; public `observed_raw`
replay preserves every prompt and complete worked solution exactly.

## Curriculum boundary and authored levels

Following `activity/first-step` and `step/next` gives this route:
Introduction → Identifying the Order of an ODE → Autonomous ODE tutorial →
Autonomous/Nonautonomous KP → First-Order IVP tutorial → this KP. The first-order
IVP tutorial defines an ODE together with a function value at a point in its
domain, and supplies a nested equation `x(2x²-y')=-1`. The canonical IVP example
contrasts two first-order systems against a second-order ODE with two initial
conditions. The order sibling uses third-order Leibniz notation. The topic's
captured prerequisite is Second and Higher-Order Derivatives; following topics
include Modeling With First-Order ODEs, Verifying Solutions, and First-Order
Linear ODEs. These later skills are excluded here.

All defaults retain the same first-order IVP recognition request and three
checkboxes. They do not solve or differentiate an ODE, expand the nested factors,
or test existence, uniqueness, autonomy, linearity, or solution consistency.
Moderate/hard are **authored missing-level scopes**, not observed labels.

| Level | Per-instance recognition workload | Bounds |
|---|---|---|
| Easy | Three prime-notation ODEs, one derivative occurrence per equation, orders 1/2; missing conditions versus function value or complete second-order data | Positive leading integer 2–5; other integer 1–5; initial points 2–4; base initial values −5–5 |
| Moderate | Three prime-notation ODEs with a nonconstant leading factor and one additional term; higher-order equations include a lower derivative; chained point data; at least one order-2/3 system | Same coefficient/point bounds; order ≤3; at most three chained initial values |
| Hard | Three nested factors each containing an already-written Leibniz derivative, plus a prime derivative outside; at least one order-2/3 system requires identifying the highest of the displayed derivative orders | Same coefficient/point bounds; order ≤3; at most three separately displayed initial values; no differentiation of a nested function |

Highest-order coefficients cannot disappear: easy uses a positive integer;
moderate uses `a+x²`; hard uses `a+x²` for orders 2/3 and `a+x²+x` for order 1,
with `a≥2`. Explicit parameters obey the same guards as sampling. Easy has 9
finite category multisets; moderate and hard each have 12. These have 36/54/54
ordered display layouts respectively. Reordering unchanged systems changes
presentation and correct field positions, but does **not** count as a new task.
Numerical coefficients and initial values also create presentation variants,
but do **not** count as new semantic tasks.
The representation/scan workload distinguishes the three authored scopes.

## Source domain wording issue

`q-96987` (17592186234496), System III, contains `1/x` and `y(0)=1`. The displayed
ODE is undefined at that point, contradicting the tutorial's “at a point in its
domain” requirement. The captured bank nevertheless marks III true. Raw public
replay preserves the evidence and is explicitly evidence-only/ineligible.
`observed_domain_repair` changes **only** that initial point to 2 by default and
updates the fixed solution's matching point. `domain-repair.json` records this
small repair; its designation match does not hide the raw domain issue.

Other sources include singular coefficients or inconsistent initial data at
defined points. Those remain formal first-order IVPs under the structural
recognition criterion: existence or uniqueness is not required or assessed.
Normal `observed_regular` variants sample small positive points 2–4, and positive
log arguments where applicable. This is an authored generation restriction,
not a recovered rule or a repair of those structural classifications.

No source-format or notation normalization is needed. Unicode primes and the
source's function-application glyph are preserved where observed. No plots or
unreadable assets require extraction or generation.
