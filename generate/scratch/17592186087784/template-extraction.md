# Four-stage template extraction

## 1. Specific observed questions

`choice-mapping.json` is the complete component ledger: original ID, mathematical parameters, every field key, complete exact answer values, and original correct values. `source-cases.json` maps those components to templates/profiles without omitting unrated sources. Source radii are positive integers 1–7; all parametrizations are x=r cos θ+h, y=r sin θ+k. All arcs are closed. θ increases counterclockwise at unit angular speed. Full-circle teaching formulas use [0,2π), except q-275161 and q-321976 use (0,2π]; both cover the full circle once and are preserved.

| Sources | Template | Specific assessed domain (multiples of π) | Fixed presentation/solution distinction |
|---|---|---|---|
| q-78681, q-106294, q-79270 | easy_semi_radio | [0,1] | origin semicircle; three distinct five-option banks |
| q-79165, q-79168 | easy_arc_radio | [0,1/4], [0,5/4] | origin arc; orange angle cue relative to vertical axis |
| q-79166 | easy_threequarter_radio | [0,3/2] | three-quarter-circle prose |
| q-79271, q-79272 | easy_quarter_radio | [0,1/2] | quarter-circle prose; two complete banks; unit coefficient omitted |
| q-321947 | easy_arc_blank | [0,7/6] | arc of a circle; lower and upper endpoint blanks; π/3 cue |
| q-321948 | easy_quarter_blank | [0,1/2] | quarter-circle prompt; arc wording in source solution |
| q-106293 | moderate_quarter_radio | [1/2,1] | nonzero start; interval-only answer values |
| q-275161 | moderate_arc_blank | [1,2] | lower semicircle; full-circle domain (0,2π] |
| q-79205 (unrated) | moderate_compact_radio | [1,3/2] | Unicode θ/π inline equations; missing correct ref and solution |
| q-79210 | hard_quarter_radio | [0,1/2] | radius 3, center (5,-4), interval-only choices |
| q-321976 | hard_threequarter_blank | [1/2,2] | radius 1, center (-1,1), translated reference through center |

## 2. Shared pattern

Read the endpoints of a displayed arc as central angles of the supplied standard circle parametrization, then restrict θ to the closed increasing interval. The response is either a whole θ-domain (possibly with θ∈ prefix) or two angle fragments keyed to the existing interval placeholders. Translation changes the central-angle reference, not the interval or orientation.

## 3. Components and complete bank recipes

`contract.json` contains extracted reusable prose with `{r}`, `{h}`, `{k}`, `{equations}`, `{interval}`, `{prompt_plot}`, and `{solution_plot}` tokens. Shared worked sentences and stage order are copied into these templates. Generic circle formula, identified radius/center, full-circle substitution, central-angle explanation, worked plot, interval restriction, and final equations remain one fixed solution per instance. Equations derive from the radius/center; angle fragments and domain expressions derive from exact rational multiples of π. There is no branch returning a source payload.

Each observed radio profile records five categorical angular candidates as exact rational endpoint pairs and endpoint openness. These are parameterized circular arc/domain objects, not an answer lookup: membership of the independently computed correct interval determines the correct option. Each complete bank is eligible for its captured angular interval while radius and applicable center can vary. Its four distractors express the other displayed angular sectors/full traversal; the original intended cognitive mistakes are not identifiable from intervals alone and are **not claimed as recovered**. Bank constants are geometric candidates; unlike a scalar polynomial fit, they have direct curricular meaning. `choice-mapping.json` plus each contract profile gives every exact original value and its endpoint recipe one-to-one, including q-79168's wrong [0,5π/2] traversal and q-78681's negative-angle distractors. No recipe from another bank is inserted to make a source profile pass.

Authored default profiles compute the entire five-member bank before acceptance: correct [a,b]; initial half [a,(a+b)/2]; final half [(a+b)/2,b]; full circle [0,2π); and preceding [0,a] if a>0, otherwise following [b,2π]. All are distinct valid domains with different assessed arcs. Reject the whole bank on duplication, zero-width interval, or missing correct value. No invented distractor diagnosis appears in learner prose.

## 4. Reusable constraints and proposed variation

Exact arithmetic uses SymPy rationals; answers stay delimiter-free TeX. Radius is integer 1–8; translated-center coordinates are integers -6–6 excluding (0,0) in sampling (explicit inputs permit -8–8). Standard cos/sin, orientation, and speed remain fixed. All authored displayed domains lie within [0,2π], start<end, familiar π/2, π/4, or π/6 multiples. Circle-fraction prose enforces its exact sweep.

Easy starts at zero and identifies a single familiar endpoint. The six observed layouts are unordered. Arc templates sample upper endpoints π/4, 3π/4, 5π/4, 7π/6, while fixed circle fractions retain their sweep. Moderate origin arcs use nonzero starts: quarter-circle layouts rotate among quadrants II–IV; two-blank arcs use [π,2π], [π/2,3π/2], [π/4,5π/4], [3π/4,7π/4]. Both endpoints use the same previously taught angle-reading operation. Hard questions use translated centers and either one of four quarter-circle sectors or [0,3π/2]/[π/2,2π]. These are peer variations; no staged difficulty progression or new mathematical branch is introduced.

There are 7 distinct easy angular tasks, 7 moderate angular tasks, and 6 hard angular tasks before radius/center changes. Deduplicating presentation/bank differences yields 56 easy circle/domain tasks, 56 moderate, and 8,064 hard in the default sampler (8 radii, 168 nonzero centers). These are mathematical objects, not claims of that many distinct skills; radius changes alone do not create a new reasoning route. Authored variations are design claims supported by the lesson's angle table, full-circle/semicircle explanation, canonical restriction example, and translated-circle predecessor.

## Source-format repair

The owning original MA capture is `/home/jake/Developer/MA/DATA/Lessons/806/Source/806.json`; its q-79205 widget is copied as `original-widget-79205.json`. Its choice letters are a=[0,3π/2], b=[0,π/2], c=[π,3π/2], d=[3π/2,2π], e=[π/2,3π/2]. It contains neither a correct designation nor a worked solution. The original MA graphic and EDB asset both show the third-quadrant quarter arc from (-4,0) to (0,-4). x=4cosθ and y=4sinθ give those endpoints at θ=π and 3π/2; the whole arc lies where both cosθ and sinθ are nonpositive. Thus choice c is uniquely correct. This correct ref and its standard source-style solution are explicitly authored repairs. All five observed options are matched; the missing designation and missing solution do not count as original matches. Its moderate label is authored and the raw capture remains unchanged.

## Identity and grading contract

Canonical mathematical fingerprint includes actual curve, parametrization, angular interval/openness, orientation, speed, and assessed task; it excludes level, layout, bank profile, rendering style, and parameter spelling. Content identity includes generator version, displayed prompt, fixed worked solution, full owned bank/field keys and correct values. Equivalent rational parameter spellings normalize before hashing. Native grading checks every owned radio option, both blank keys, canonical fragments, unreduced rational multiples of π, and wrong endpoint values. These sources have no “Do not round” wording or precision requirement: original exact-answer wording is retained and no form-sensitive rounding workaround applies. No engine edits are made.
