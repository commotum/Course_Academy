# Classification at math basis 1356

KP 17592186229181, “Constructing and Solving a Dilution Model: Inflow Equals Outflow,” topic 17592186049774 / MA 6700. Frozen lineage: `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is the untouched capture wrapper.

| Observed label | Practices | Field layout | Mathematical family | Distinct full bank profiles | Plot rating |
|---|---:|---|---|---:|---|
| easy | 3 | one `selection` radio, five mathematical choices | full expression Q(t) | 3 | none |
| moderate | 2 | one `selection` radio, five rounded mass choices | Q(T), two decimal places | 2 | none |
| absent | 2 | one `selection` radio, five choices; correct ref absent | one expression / one rounded mass | 2 | none |
| hard | 0 | authored one `selection` radio, five rounded mass choices | same IVP, declared feed-unit conversion then Q(T) | authored method bank | none |

There are two mathematical Markdown/value families, with individually extracted masks for all seven context/prose/notation variants. Expression choices contain the complete equation; amount choices include kilograms. Source omission is a separate feature: unrated source masks omit difficulty, worked solution, and correct reference in public raw replay. Missing-label replay API levels are authored easy for q-339385 and moderate for q-339392, and do not insert those labels into their raw question records.

Lesson order was recovered from `:activity/first-step` and `:step/next`: Introduction → this equal-rate KP → unequal-rate “Constructing and Solving a Dilution Model” → overflow point. Collection order was not used. The introduction works with 650 L, 1300 g, 20 g/L, and equal 5 L/min rates; the canonical equal-rate example works with 800 L, 7 kg, 0.01 kg/L and 40 L/min. Key prerequisites are integrating factors (MA 877), separable mixture ODEs (1713), and general linear-ODE solutions (6678).

Hard is an explicitly authored design claim: convert the printed 10–60 g/L feed concentration to 0.01–0.06 kg/L, construct the identical constant-volume model, solve with complementary plus particular solution and initial condition, then evaluate Q(T). This adds necessary unit bookkeeping to the observed moderate demand without introducing another mathematical branch. Units and input information distinguish moderate and hard even where their normalized final IVP agrees. There is no unequal-rate volume V(t), overflow calculation, target-time logarithm, pure-water branch, or extra integration method.

Default bounds preserve source arithmetic forms: integer V = r·tau in 300–1000 L, integer r in 10–50 L/min, integer tau in 10–80 min, c in {0.01,…,0.06} kg/L, integer initial mass 1–25 kg, and integer finite evaluation time 2–12 min. Initial and equilibrium amounts are unequal, and Q(0) < 2cV keeps every reflected-initial-condition option positive. Parameters do not create a progression within a level. The source masks are a separate dimensional-similarity domain (integer mass scale 1–4 and flow/volume scale 1–3); they remain evidence only.

Authoritative original asset `/home/jake/Developer/MA/DATA/Lessons/6700/Source/6700.json` confirms the two unrated captured questions are five-choice widgets with empty bodies and no captured answer key. This supports the omission findings, not an invented observed designation. Mathematical inference uniquely identifies their correct values. No mathematical plots occur, so no rendering is needed.

## Live-source refresh at basis 2704 (2026-10-15)

The retained `reference/replenishment/initial.json` captures all ten current practice
questions and the canonical example at one basis on the same lineage. There are
now six rated easy expression questions, three rated moderate finite-time questions,
and one incomplete unrated amount question. The formerly incomplete q-339385 has
been completed by an earlier application transaction; this replenishment preserves
its current fields and history. No hard source question has appeared. The existing
validated hard unit-conversion capability remains an authored extension, supported
by the introduction's gram units, rather than an observed hard label.

The three additional sources retain the existing `selection` radio field, five
mathematical choices, constant-volume model, complementary/particular solution,
initial condition, and (for moderate) final substitution/rounding. All have plot
rating **none**. Their complete banks and independent answer checks are retained
in `reference/current-source-validation.json`:

| Source | Parameters (V, r, c, Q0, T) | Family | Bank profile |
|---|---|---|---|
| q-336752 / 17592186502082 | 600, 15, .04, 10, function | expression | opaque particular-constant bank |
| q-336736 / 17592186502104 | 400, 20, .08, 6, 5 | amount | opaque rounded-scalar bank |
| q-339383 / 17592186502108 | 300, 15, .04, 1, function | expression | sign/initial-condition and alternate decay bank |

These are new complete source profiles, not new mathematical templates. Their
opaque alternatives are explicitly excluded from normal sampling; the supported
normal profile remains the separately authored complete `method_bank` already
validated. The observed .08 concentration is preserved in evidence; the normal
sampler's .01–.06 concentration range is a narrower sampling policy, not a claim
about all source parameters. Every current complete source bank has a unique
independently computed correct value; the remaining incomplete original is
excluded from learning inventory. Existing questions are never relabeled or repaired
by the generator publication.
