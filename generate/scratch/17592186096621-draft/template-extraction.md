# Template extraction

The stable backbone is quotient differentiation of the supplied elementary functions, preserving ordered numerator/denominator roles, response shape, and each family’s source solution stages. Moderate additionally substitutes one exact point in the derivative. Scalar and target slots are sampled only after choosing the complete source bank. The parameterized source chains live in `family_chains.py`; original parameters use the normalized source prose and stages, with supported repairs listed separately. Missing solutions use an explicitly authored canonical quotient chain.

For each source template the only numerical function slot is a nonzero numerator scale `a ∈ {-12,…,-1,1,…,12}`. Original scale is 1. The denominator structure, argument, and exponent remain fixed because they determine the source differentiation method and workload. Denominator scaling is not an extra advertised slot: simultaneous numerator/denominator scalar aliases are deduplicated mathematically. Signs and unit scales are retained.

| Source family | Original quotient | Target | Response/bank | Ordered stages |
| --- | --- | --- | --- | --- |
| q-17921 | $\frac{\cos{\left(x \right)}}{\ln{\left(x \right)}}$ | none | q-17921-complete-observed | authored rule → formal derivative operands → evaluated derivative products → expansion → factored result |
| q-47999 | $\frac{x^{2}}{\sin{\left(x \right)}}$ | none | q-47999-complete-observed | authored rule → formal derivative operands → evaluated derivative products → expansion → factored result |
| q-340318 | $x e^{- 3 x}$ | $1$ | blank | rule → formal operands → evaluated products → exponential factor → cancellation; 3 target rows |
| q-9908 | $\frac{\cos{\left(x \right)}}{\sin{\left(x \right)} + 1}$ | $\frac{\pi}{2}$ | blank | rule → formal operands → evaluated products → expanded numerator → grouped trig squares; identity sentence; replace squares → factor → cancel; 3 target rows |
| q-167328 | $- \frac{e^{x}}{8 \sin{\left(x \right)}}$ | none | blank | rule → formal operands → evaluated products → common factor → reduced quotient |
| q-167782 | $- \frac{e^{x}}{8 \sin{\left(x \right)}}$ | none | blank | same five quotient stages; inner numerator fragment in complete fraction context |
| q-166075 | $- \frac{e^{x}}{8 \sin{\left(x \right)}}$ | none | blank | same five quotient stages; full derivative blank |
| q-2385 | $\frac{\cos{\left(x \right)}}{10 x^{2}}$ | none | q-2385-complete-observed | rule → evaluated products → expansion → explicit cancellation factor → reduced quotient |
| q-340308 | $\frac{\tan{\left(x \right)}}{x}$ | none | blank | rule → formal operands → secant derivative products → collected numerator |
| q-340309 | $\frac{x}{\sin{\left(x \right)}}$ | none | blank | rule → formal operands → evaluated products → collected numerator |
| q-340316 | $\frac{2^{x}}{x^{2} - 1}$ | $0$ | blank | rule → formal operands → exponential-base derivative products → common exponential factor; 3 target rows |
| q-47943 | $\frac{e^{x}}{\cos{\left(x \right)}}$ | none | q-47943-complete-observed | rule → formal operands → expanded signed products → common exponential factor |
| q-47998 | $\frac{\sin{\left(x \right)}}{x^{2}}$ | none | q-47998-complete-observed | rule → formal operands → expanded products → factor x → cancellation |
| q-48504 | $\frac{x^{2}}{\ln{\left(x \right)}}$ | $e$ | q-48504-complete-observed | rule → formal operands → logarithmic derivative products → reduce x²/x → factor x; 3 target rows |
| q-48507 | $\frac{\sin{\left(x \right)}}{2 x}$ | $\pi$ | q-48507-complete-observed | rule → formal operands → evaluated products → common scalar factor → cancellation; 4 target rows |

For each choice in `source-components.json`, the full original expression is the executable opaque recipe, multiplied by the numerator scale. This applies to all easy radio profiles. It intentionally makes no claim about the learner’s misconception; compound and apparently odd expressions remain intact. Each complete original five-option bank stays one profile, with no pooled first-valid selection. At original parameters, all 35 radio options and seven captured singleton blank values map one-to-one; q-9908 has no captured bank.

Moderate radio q-48504 uses the complete target-aware profile `[S,a/4,2a/3,a,S/2]`, where `S` is the derived tangent slope. At `(a,t)=(1,e)` this is exactly `[e,1/4,2/3,1,e/2]`. q-48507 uses `[a/(4t),-at,2at,-a/2,S]`, matching `[1/(4π),-π,2π,-1/2,-1/(2π)]` at `(1,π)`. These are conservative authored target generalizations of opaque observed patterns; intent remains unresolved. A whole profile collision rejects the instance; in particular q-48504 at `t=√e` gives two zero choices. The target remains declared and tested; it is not deleted to force a passing bank.

The target slots are the exact finite sets in `capabilities.json`. They preserve one derivative evaluation and comparable exact arithmetic. Every target reference, evaluated formula, conclusion, and key is derived from that same slot. Undefined original-domain points are rejected, including x=0 for sin(x)/(2x), x=±1 for 2^x/(x²−1), x=1 for x²/ln(x), and 3π/2 for cos(x)/(1+sin(x)). The original logarithmic x>0 and trigonometric pole restrictions remain part of the mathematical task identity.

The hard authored family is `(x²+a sin x)/(exp x+b cos x)`, `a,b ∈ {-3,-2,-1,1,2,3,4,5}`. Both coefficients are substantive and nonzero, so every variant retains two-term numerator and denominator and four derivative terms. There is no within-level progression: sampled pairs are independent alternatives at one workload. Its complete authored bank is `[N/v²,(u′v+uv′)/v²,N/v,u′/v′,N/u²]`, `N=u′v−uv′`; any equivalent or undefined pair rejects the entire selected bank. This is a separate authored profile, not an observed MA source bank.

Raw public replays preserve all omissions exactly and are marked evidence-only/ineligible. Normal source anchors preserve shared wording and ordered mathematical stages while normalizing TeX, repairing redundant aligned wrappers, completing missing shared f/h definitions, and restoring the malformed fragment fraction as an embedded equation-table field. Every such repair is recorded, with raw evidence retained. No source has been silently discarded.
