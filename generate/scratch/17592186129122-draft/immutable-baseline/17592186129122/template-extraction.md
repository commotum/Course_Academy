# Step 4 — template extraction

## Stage 1 — specific original descriptions

### q-43404 — rad_sine_fraction
A=1/6, B=5/3, C=-1/2 π. Uses sin, fraction frequency notation, fraction amplitude notation. Complete original prompt and solution appear in review.md; exact component masks appear in template-masks.json.
The solution states the general formula, identifies B in prose, then gives one quotient-to-period calculation in the final sentence.

### q-53457 — rad_cos_fraction
A=1/2, B=1/3, C=0/1 π. Uses cos, multiplier frequency notation, fraction amplitude notation. Complete original prompt and solution appear in review.md; exact component masks appear in template-masks.json.
Original worked-solution attribute is absent.

### q-117580 — rad_cos_integer
A=1/1, B=12/1, C=-1/6 π. Uses cos, integer frequency notation, unit amplitude notation. Complete original prompt and solution appear in review.md; exact component masks appear in template-masks.json.
The solution states the general formula, identifies B in prose, then gives one quotient-to-period calculation in the final sentence.

### q-117583 — degree_sine_fraction
A=1/1, B=8/3, C=20/1 degrees. Uses sin, fraction frequency notation, unit amplitude notation. Complete original prompt and solution appear in review.md; exact component masks appear in template-masks.json.
The solution states the general formula, identifies B in prose, then gives one quotient-to-period calculation in the final sentence.

### q-117578 — rad_sine_scaled_fraction
A=-3/1, B=3/4, C=1/3 π. Uses sin, fraction frequency notation, integer amplitude notation. Complete original prompt and solution appear in review.md; exact component masks appear in template-masks.json.
The solution states the general formula, identifies B in prose, then gives one quotient-to-period calculation in the final sentence.

### q-117579 — degree_sine_scaled_fraction
A=-4/1, B=4/3, C=-45/1 degrees. Uses sin, fraction frequency notation, integer amplitude notation. Complete original prompt and solution appear in review.md; exact component masks appear in template-masks.json.
The solution states the general formula, identifies B in prose, then gives one quotient-to-period calculation in the final sentence.

### q-43411 — degree_cos_integer
A=1/1, B=8/1, C=90/1 degrees. Uses cos, integer frequency notation, unit amplitude notation. Complete original prompt and solution appear in review.md; exact component masks appear in template-masks.json.
The solution states the general formula, identifies B in prose, then gives one quotient-to-period calculation in the final sentence.

### q-81513 — degree_sine_integer
A=-2/1, B=9/1, C=-1/1 degrees. Uses sin, integer frequency notation, integer amplitude notation. Complete original prompt and solution appear in review.md; exact component masks appear in template-masks.json.
The solution states the general formula, identifies B in prose, then gives one quotient-to-period calculation in the final sentence.

## Stage 2 — generalized shared pattern

Given a nonconstant transformed sine/cosine formula, identify its linear argument coefficient B and calculate a positive period by dividing the base period (2π radians or 360°) by |B|. Positive B is observed; signed and factored coefficients are authored missing-level extensions. Amplitude and additive shifts are displayed context and do not affect the period.

## Stage 3 — complete component and bank maps

All prompt mathematical components are complete slots @A@, @BX@ and @C@. Entire conclusion calculation is independently masked as @PERIOD_STAGE@; the prose identification has @B@. Shared opening sentences are preserved exactly except the documented normal-only q-43411 rule correction. No short textual symbol substitution occurs across unrelated prose. Raw missing attributes remain absent.

| Source | Choice index | Original complete value | Scalar component (π or degrees) | Recipe / interpretation |
|---|---:|---|---|---|
| q-43404 | 0 | `\frac{6\pi }{5}` | 6/5 | Independent displayed scalar slot o0; opaque intention, evidence-only |
| q-43404 | 1 | `\frac{\pi }{2}` | 1/2 | Independent displayed scalar slot o1; opaque intention, evidence-only |
| q-43404 | 2 | `\frac{5\pi }{3}` | 5/3 | Independent displayed scalar slot o2; opaque intention, evidence-only |
| q-43404 | 3 | `\frac{\pi }{6}` | 1/6 | Independent displayed scalar slot o3; opaque intention, evidence-only |
| q-43404 | 4 | `2\pi ` | 2/1 | Independent displayed scalar slot o4; opaque intention, evidence-only |
| q-53457 | 0 | `\frac{1}{3}π` | 1/3 | Independent displayed scalar slot o0; opaque intention, evidence-only |
| q-53457 | 1 | `3π` | 3/1 | Independent displayed scalar slot o1; opaque intention, evidence-only |
| q-53457 | 2 | `π` | 1/1 | Independent displayed scalar slot o2; opaque intention, evidence-only |
| q-53457 | 3 | `2π` | 2/1 | Independent displayed scalar slot o3; opaque intention, evidence-only |
| q-53457 | 4 | `6π` | 6/1 | Independent displayed scalar slot o4; opaque intention, evidence-only |
| q-117578 | 0 | `\frac{3\pi }{2}` | 3/2 | Independent displayed scalar slot o0; opaque intention, evidence-only |
| q-117578 | 1 | `\frac{4\pi }{3}` | 4/3 | Independent displayed scalar slot o1; opaque intention, evidence-only |
| q-117578 | 2 | `\frac{\pi }{3}` | 1/3 | Independent displayed scalar slot o2; opaque intention, evidence-only |
| q-117578 | 3 | `\frac{8\pi }{3}` | 8/3 | Independent displayed scalar slot o3; opaque intention, evidence-only |
| q-117578 | 4 | `\frac{\pi }{4}` | 1/4 | Independent displayed scalar slot o4; opaque intention, evidence-only |
| q-117579 | 0 | `{300}^{∘}` | 300/1 | Independent displayed scalar slot o0; opaque intention, evidence-only |
| q-117579 | 1 | `{270}^{∘}` | 270/1 | Independent displayed scalar slot o1; opaque intention, evidence-only |
| q-117579 | 2 | `{480}^{∘}` | 480/1 | Independent displayed scalar slot o2; opaque intention, evidence-only |
| q-117579 | 3 | `{90}^{∘}` | 90/1 | Independent displayed scalar slot o3; opaque intention, evidence-only |
| q-117579 | 4 | `{120}^{∘}` | 120/1 | Independent displayed scalar slot o4; opaque intention, evidence-only |
| q-43411 | 0 | `{60}^{∘}` | 60/1 | Independent displayed scalar slot o0; opaque intention, evidence-only |
| q-43411 | 1 | `{30}^{∘}` | 30/1 | Independent displayed scalar slot o1; opaque intention, evidence-only |
| q-43411 | 2 | `{45}^{∘}` | 45/1 | Independent displayed scalar slot o2; opaque intention, evidence-only |
| q-43411 | 3 | `{15}^{∘}` | 15/1 | Independent displayed scalar slot o3; opaque intention, evidence-only |
| q-43411 | 4 | `{75}^{∘}` | 75/1 | Independent displayed scalar slot o4; opaque intention, evidence-only |
| q-81513 | 0 | `{90}^{∘}` | 90/1 | Independent displayed scalar slot o0; opaque intention, evidence-only |
| q-81513 | 1 | `{120}^{∘}` | 120/1 | Independent displayed scalar slot o1; opaque intention, evidence-only |
| q-81513 | 2 | `{30}^{∘}` | 30/1 | Independent displayed scalar slot o2; opaque intention, evidence-only |
| q-81513 | 3 | `{75}^{∘}` | 75/1 | Independent displayed scalar slot o3; opaque intention, evidence-only |
| q-81513 | 4 | `{40}^{∘}` | 40/1 | Independent displayed scalar slot o4; opaque intention, evidence-only |

The six full bank sets are retained as profiles raw:q-43404, raw:q-53457, raw:q-117578, raw:q-117579, raw:q-43411 and raw:q-81513. The raw fieldless profiles raw:q-117580/raw:q-117583 preserve no bank. Independent scalar parameters are faithful display components; they are not functions fitted to B and are never learner defaults. Mathematical verification identifies one correct displayed scalar in each present source bank, with stored designation absence separately recorded for q-53457.

## Stage 4 — reusable template and parameter constraints

Fixed prose, punctuation, invisible function-application glyph and π/degree spelling are part of the observed source masks. Variable complete components render from exact reduced rational parameters. Optional components are source attribute presence, not random omissions. Unit/one-amplitude families retain unit amplitude, fractional amplitude families retain positive proper fractions, integer amplitude families retain nonzero signed integers. Shift-free q-53457 remains shift-free; other source masks keep a nonzero additive shift. Different sampled numbers are variants of the same assessed method, not claimed recovered new templates.

| Level | Same-level workload | Finite frequency domain / guard |
|---|---|---|
| easy | Identify positive direct B; reciprocal division | Integer B=3..12 or reduced positive n/d with n=1..12, d=2..6; normal complete-bank collisions excluded. Original B=1/3 retained; source B=12 retained. |
| moderate (authored) | Identify negative direct rational B; take magnitude; reciprocal division | Reduced negative n/d, n=1..12, d=2..6, noninteger; zero and positive B prohibited. |
| hard (authored) | Multiply one rational by integer k, perform at least one cancellation, take magnitude, reciprocal division | Negative reduced n/d, n=1..12, d=2..12; k=2..6; gcd(k,d)>1; product remains noninteger, magnitude≤12, reduced product numerator≤60. |

Amplitude is nonzero, magnitude≤6 and denominator≤6. Radian shifts have denominator≤6 and degree shifts have magnitude≤90; no shift is assessed. Every explicit call enforces the same level-specific arithmetic guards as samplers. The widened hard denominator bounds are authored familiar small-integer fractions, preserving the same single product/cancellation demand; all hard tasks are unordered peers. Neither signs nor factor structure may disappear into an easy/moderate instance. Distinct factorizations recovering identical B are excluded from meaningful task counts.

Normal method bank is selected as a complete profile before parameters: P/|B| (correct), P|B| (multiply instead of divide), P/(2|B|) (use the tangent base period), 2P/|B| (double the sinusoidal base period), P (ignore the horizontal scaling). These are actual frequency/base-period operations. All five are rendered together; no pooled first-valid replacement or per-option random perturbation occurs. Positive/equal equivalent values reject the entire instance.

Meaningful task fingerprints use level/demand, angular scale and recovered signed B. They exclude amplitude, shift, sine/cosine aliases, notation, bank profiles, unused metadata and alternative factorizations. Content identity hashes the actual rendered prompt, fixed solution, actual complete bank, difficulty and field/key presence. Seed changes shuffle options without changing identity.

## Frozen review and limitations

The frozen source wrappers and authoritative-widget extraction document provenance. No graph, further mathematical branch or sibling-KP assessment is added. Raw exact solution fidelity includes the q-43411 misleading opening; normal mathematical correctness corrects it separately. Native checks for raw fieldless/keyless records cannot be claimed; authored complete radios exercise the real grader. Historical error intention remains unresolved in all six banks, while exact raw values/wording/absence are fully preserved.
