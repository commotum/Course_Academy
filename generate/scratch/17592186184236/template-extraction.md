# Four-stage template extraction

## 1. Describe originals before generalizing

All prompts place their graph first, then state y=tan(Bx)+D with constant B,D. Four ask B+D, two D-B. B is positive, no vertical scaling or phase translation appears. Complete individual original records and PNG hashes are in source.json and source-geometry.json; source-assets.json resolves their references. Source answer values have one decoded backslash before `frac` (byte evidence: `[92,102,114,97,99,...]`), so there is no invented double-slash repair. The operatorname notation uses a Unicode function-application character; raw replay preserves it and normal output uses standard `\tan`.

| Source | B | D | Adjacent asymptotes | Requested | Full original bank |
|---|---:|---:|---|---|---|
| q-65448 | 1/2 | 1 | ±π | B+D | 1, 1/2, 3/2, -1/2, 3; duplicated field bank, same set |
| q-65547 | 2/3 | -2 | ±3π/4 | D-B | -4, -8/3, 6, 1/3, 5/2 |
| q-117795 | 3 | -3 | ±π/6 | B+D | 0, 3, -1, -2, 2 |
| q-141974 | 2/3 | 1 | ±3π/4 | D-B | 1/6, 1/3, -2/3, -1/3, -1/6 |
| q-143638 | 2 | -2 | ±π/4 | B+D | -1, 3, 2, 4, 0 |
| q-117796 | 5/4 | 1/2 | ±2π/5 | B+D | 7/2, 7/4, 5/2, 3, 4 |

Every exact prompt and available worked solution is represented by an individual parameter mask in masks.json. Omissions are structural, not replaced by empty lists or fabricated observed labels.

## 2. Shared mathematical pattern

Read the two consecutive symmetric asymptotes, compute their separation T, use T=π/B to identify B, read D as y(0), then calculate the requested sum or difference. The fixed solution additionally gives y=tan(Bx)+D with substituted values. All five observed solutions have the same eight equality statements when the symbolic family statement and implication stages are counted, with q-141974 preserving its additional equality inside the period row. The unrated missing solution receives an explicitly authored version of those stages only in its repair.

## 3. Components and complete banks

Let S=B+D, R=D-B. Source profile operation masks reproduce every option one-to-one. These formulas preserve the numerical evidence; coefficients whose error origin cannot be established are explicitly opaque and must not become normal learner banks.

| Profile | Complete operation bank, in captured first-field order | Interpretation status |
|---|---|---|
| raw-q-65448 | D, B, S, -B, 2S | omission/sign/doubled-result hypotheses; duplicate field raw ineligible |
| raw-q-65547 | 2D, R, -3D, B/2, 1/B-D/2 | opaque, evidence only |
| raw-q-117795 | S, B, D/3, 2D/3, 2B/3 | opaque ratios, evidence only |
| raw-q-141974 | R/2, R, -B, -R, -R/2 | omission/reversal/half-result hypotheses; evidence only |
| raw-q-143638 | D/2, B-D/2, B, B-D, S | omitted parameter/shift-sign/half-shift hypotheses; evidence only |
| raw-q-117796 | 2S, S, 2B, 2B+D, 2B+3D | final coefficient opaque; evidence only |

The duplicate q-65448 second field has the same complete value set and its original correct designation. It is compared separately. All incorrect options and all five source correct designations are checked algebraically; two missing designations remain separately missing.

Normal authored complete banks are chosen before parameters:

* `period-sign`: F(B,D), F(B/2,D), F(2B,D), F(B,-D), F(1/B,D). These represent doubled period, halved period, reversed vertical shift and confusing reciprocal horizontal scale with B.
* `omitted-sign`: F(B,D), F(0,D), F(B,0), F(-B,-D), F(B,-D). These represent ignoring one parameter or reversing their signs. F is the actual requested sum/difference, never a constant perturbation to a computed scalar.

Reject the whole instance if any two complete values coincide. Never fill a missing member from a pool. The fixed solution never depends on which error is selected and contains no invented learner-facing distractor diagnoses.

## 4. Reusable masks, domains and calculations

`masks.json` slots only complete mathematical components: H, T, unreduced doubled endpoint, inverse-period expression, B, D, shift magnitude/direction, requested result, complete Bx expression and signed vertical term. No global short-symbol replacement crosses prose, labels or arguments. q-141974's unreduced T=6π/4 stage and q-143638's reciprocal 2π/π stage are retained. A conditional addition fragment groups a negative D, preventing bare `+-`; the same conclusion is independently checked under changed signs.

The raw masks retain all source prose and layout, including original singular/plural spelling. Normal variants normalize operatorname notation and adapt the unit inflection to the displayed magnitude; the source-shaped solution sequence stays fixed. q-65547's repair is explicitly authored. Prompt asset geometry changes with the parameters; exact source geometry can reuse its unchanged source PNG.

Easy: B∈{1/3,1/2,2/3,1,3/2,2,5/2,3,4}, integer D∈[-4,4] excluding 0. Moderate: B∈{2/3,3/4,4/3,5/4,5/3,3/2,5/2}, D odd halves with |D|≤7/2. Hard: reduced B=n/d for 2≤n≤6,3≤d≤6, reduced denominator≥3; D odd quarters with |D|≤11/4. Every explicit input is guarded. The q-141974 mask additionally requires an even reduced endpoint denominator so its unreduced-to-reduced period row remains a genuine arithmetic stage under variation; explicit incompatible masks reject, and normal difference tasks select the other observed mask when that condition is absent. Source profiles preserve their original domains separately.

Mathematical task identity includes reduced B,D, the actual requested expression and coordinate-reading calibration. Phase is exactly zero, so no periodic aliases exist to count; seeds, answer order, mask labels and bank profiles are excluded from mathematical task counts. Content identity includes actual prompt, fixed solution, complete unordered bank, field layout, attribute omissions and difficulty. A source-mask alias with the same displayed content does not create a new ID. Every record is plain JSON.
