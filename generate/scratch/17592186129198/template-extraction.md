# Template extraction

Database math, basis 1356; the immutable capture in `source.json` is authoritative. Mathematical components below are scalar expressions, complete integrands, complete limits and complete equation sides. Short number substrings are never replaced across prose or labels.

## Stage 1 — describe originals specifically

The classification table identifies all ten originals, their number forms, powers, trig functions, radial/angle roles, field type/count and profile. `source.json` retains every original learner string and UUID. All bounds/integrands are recorded in `SOURCE_DATA` exactly: radial integration is always first; theta is held constant. Eight questions say Evaluate or show a trailing equals sign; q-38127 says What is and has Unicode pi/theta, without a solution; source-specific wording is preserved.

Every provided solution has two display-aligned blocks separated by the shared radial and angular integration sentences. Their ordered stages remain separate: extraction of the theta factor where present; radial primitive bracket; upper-minus-lower radial substitution; reduced angular integrand; the applicable trig identity or distribution; angular primitive; endpoint substitution; endpoint term evaluation; final collection. q-38133 intentionally retains its redundant opening integral row. q-38031 omits redundant numerical radial substitution, as observed. Source solution rows are never regenerated from a collapsed CAS final answer.

## Stage 2 — generalized families

Evaluate an already-supplied repeated polar integral, integrating its radial monomial with theta constant, substituting the supplied radial limits, and evaluating the resulting elementary trig integral with exact familiar-angle arithmetic. Return one scalar in a five-choice radio field. Individual source layouts remain distinct templates; sibling coordinate conversion and region derivation are excluded.

The authored default family construction varies genuine supplied bounds, monomial powers and angular endpoints within the classification limits. It renders radial extraction/primitive/substitution/reduction and angular identity/primitive/both endpoint substitutions/individually evaluated endpoint components/final arithmetic. Half-angle families keep formal identity, substituted argument, reduction, primitive and endpoint stages. The primitive expressions use the course's sine/cosine/cotangent notation rather than unrelated CAS alternative methods.

## Stage 3 — components and complete banks

For source-profile replay, `source-cases.json` maps every original to its template, exact `scale=1` parameters and its complete bank profile. The additional `bank-mapping.json` maps every choice (not merely the key), original field, exact value, correct designation availability and its parameterized scalar-pattern recipe. Each original bank is the complete set observed together. No bank member is pooled/replaced. Choices retain the exact raw source string at scale 1, including Unicode notation and whitespace.

One observed scalar answer rarely determines the original mistake. These profiles honestly retain that limitation: `scale * captured scalar pattern` is a homogeneous parameterized bank, not a claim that a mistake was recovered. The correct answer is computed from the actual radial/angular integral independently of the bank; no correct-value lookup is used. The complete integral/equation sides scale through the same linear slot. Observed profiles are explicit-only; default sampling uses the separate authored operation profiles.

The authored complete bank contains exactly these five operations, selected together before sampling:

1. Correct `z = F(beta)-F(alpha)`.
2. Omit the radial primitive denominator: `(n+1)z`.
3. Introduce another radial factor: evaluate the supplied repeated integral with integrand `r*f`. For the cosecant-lower family the complete profile instead omits the lower radial endpoint, integrating the upper radial primitive alone; this avoids an unrelated logarithmic distractor workload.
4. Reverse the angular orientation: `-z`.
5. Incorrectly halve only the upper angular primitive endpoint: `F(beta)/2-F(alpha)`.

Every wrong operation is tied to a displayed assessed integration component. This includes an actual extra radial factor; it is not a final-value multiply-by-two surrogate. Banks with any equal/invalid scalar are rejected as a whole. The choices do not contain learner-facing error diagnosis. Complete profile recipes and provenance remain author metadata.

## Stage 4 — reusable Markdown/value templates

Each observed template uses the captured wording/Markdown as a mathematical slot scaffold. `scale_prompt` scales the complete integral component. `scale_solution` parses each aligned equality side and scales complete expressions, preserving boundaries, whitespace, original row count, stage order and shared prose; it does not replace literals by a literal-record replay branch. The same recipe accepts scale integers 1..5, and scale 1 algebraically/presentationally reduces to the original. Every source choice is scaled by the same slot, giving a genuine homogeneous mathematical variant. Parameter changes are exact and deterministic.

Authored defaults build their prompts from the actual supplied limits and integrand. Unevaluated masks retain the radial powers/substitutions and individual angular primitive components at both endpoints. Hard extends the exact canonical half-angle method, with its difficulty rationale in classification. Authoring is explicit in metadata and review labels.

UUID content identity includes generator version, displayed prompt, fixed solution, difficulty and complete sorted displayed bank; changing option order/seed cannot create identity. Mathematical fingerprint records the canonical symbolic supplied integral components and excludes profile/bank/order. Numeric variable aliases and unused metadata do not inflate task counts. There are no plots, root branches, hidden domains or parameter-dependent assets. Every expression is finite over its stated angular interval, and supplied oriented radial limits are preserved.

## Fidelity and correctness denominators

All ten original complete banks (50 choices) are replayed through the public generator API. Original correct designation matching has denominator nine; original solution matching has denominator nine. q-38127's key/solution/rating are authored separately. Native radio UUID selection checks are distinct from full printed-math correctness, source bank matching, exact prose/stage fidelity and formatting. Validation never declares a missing original designation matched.
