# Four-stage extraction

## 1. Specific source descriptions

`source-map.json` preserves all 19 records' IDs, raw prompts, exact bank strings, original field types/key presence, initial triples and full worked solutions. Each prompt supplies a first-order ODE, one initial point and a candidate function with a single scalar A. It asks only for A, never an ODE-solving method. Parameters include signed integer inputs/values, rational initial values, exponential constants, and familiar trig angles π/4 and π/2. x is independent, y dependent. Real local solution domains exclude zero denominators, trig poles and nonpositive log arguments.

The two older inline radios have no captured difficulty, worked solution or correct designation. Later radios use a displayed IVP and typically finish by stating the resulting solution. Blanks end with `$A=${{field-1}}` and omit that final paragraph. Sine/cosine blank prose says “We are given” and “into the solution”; other sources say “We're given” and “into our solution.” These sentences remain complete masks, including original punctuation and omissions. q-352656 deliberately repeats its partially substituted exponential equation; the repeated row is retained.

## 2. Shared pattern and purpose

Given a valid one-parameter solution family, substitute its initial input/output, evaluate the supplied function and isolate A. Power and reciprocal-power recover A=b/u^n or b u^n; exponential gives b exp(-ku); trig gives b/sin(ku) or b/cos(ku); reciprocal affine gives 1/b-ku; log affine gives exp(b)-u. The differential equation is shown as context and independently checked by differentiation; the learner is not required to discover or solve it.

## 3. Component and bank mapping

Every component is a complete ODE+condition, supplied equation, condition equation, ordered aligned block, final solution equation, or answer fragment. No short expression is globally replaced across prose. `masks.json` carries the fixed source sentences and whole-component slots. The script's `components` renders all function-dependent forms from k,u,b and computed A; optional evaluation rows and the final paragraph depend on the source layout. `source-map.json` assigns every original bank member its exact value, formula, observed profile and interpretation limit.

Observed radio recipes, with a denoting the derived A, are:

| Profile | Complete ordered bank formulas | Interpretation limit |
|---|---|---|
| q-141055 | b exp(u), a, 1/b, b exp(ku), b | expression patterns; inferred mistakes unverified |
| q-141117 | u−1/b, a, b, 2a, u | expression patterns; inferred mistakes unverified |
| q-141111 | −cos(ku), −a, b, cos(ku), a | expression patterns; inferred mistakes unverified |
| q-141115 | exp(b)+u, 2exp(b)−u, 2u, a, u | expression patterns; inferred mistakes unverified |
| q-141107 | 4a, −a, 2a, −2a, a | opaque proportional value pattern only |
| q-141108 | 0, −2a, 2a, −a, a | opaque proportional value pattern only |
| q-141109 | 2a, a, −a/2, 0, −a | opaque proportional value pattern only |
| q-141114 | a/3, a, −a/3, 2a, −a | opaque proportional value pattern only |
| q-141112 | −a/3, a, a/2, 3a/4, −a/2 | opaque proportional value pattern only |
| q-141113 | −a/8, −a/2, a, −a, a/16 | opaque proportional value pattern only |
| q-141116 | −a/4, a/4, a, a/2, −a/2 | opaque proportional value pattern only |

Opaque proportional profiles reproduce entire observed banks and generalize their exact value pattern. They are explicitly evidence only; a numerical match does not establish a recovered source error method. Even completed opaque profiles are ineligible for learning. The separately authored normal radio banks are now complete family-specific wrong-operation profiles derived from the displayed initial substitution, as documented in `authored-banks.md`. The former uniform scaling/shift bank was removed because its values were not consistently grounded in the supplied equation. Each replacement profile is selected before parameter sampling, and the whole instance is rejected for any undefined, nonreal, duplicate or equivalent member. No learner-facing error diagnosis is invented. Blank profiles have the one derived constant and the supplied scalar fragment notation.

## 4. Reusable template and limits

Fixed components are the complete prose and ordered stage structure. Variable components are the ODE coefficient, initial point, function argument, derived constant and all dependent row values. Source replay keeps exact lexical braces, spaces, natural-log term order, final equations and repeated/omitted rows; normal presentation repairs unmarked trig operators. Unary power/reciprocal legacy layouts constrain k to the coefficient their layout actually describes. Explicit invalid parameters raise errors rather than being silently resampled. Sampling selects a complete bank before rendering, checks all members, and resamples the whole instance only in random mode.

Normal easy samplers keep n≤4, nonzero integer power inputs |u|≤3, signed exponential integer/half-integer inputs |u|≤3, trig angles from π/6,π/4,π/3,π/2,2π/3,3π/4 subject to nonzero factor and nonsingular ODE, reciprocal coefficients ±1 and rational inputs of denominator ≤2, and log integer initial outputs |b|≤3. Initial outputs are nonzero and bounded. Level-specific missing-level restrictions are enforced again on explicit inputs. These are finite workload domains, not claims of unlimited variety or new recovered templates. Parameters that affect substitution appear in the mathematical fingerprint; variable/layout/profile aliases and complete answer banks do not. Presentation identity hashes the actual full prompt, solution, field shape, complete bank and presence of the correct ref/difficulty.

No plots occur, so extraction and generation steps 5 and 7 require no renderer or assets.

## Reduced-number workload revision

The easy reduced-output catalog is explicit in `EASY_RATIONAL_VALUES` and `EASY_TRIG_VALUES`, reused by the sampler and `validate_parameters`. Nontrig rationals use reduced numerator magnitude 1–8 and reduced denominator 1–4 (44 distinct values). Log retains its tighter integer-output condition. Trig values are the 14 signed familiar special-angle values ±1,±2,±3,±√2,±√3,±√2/2,±√3/2. Mathematical simplification can admit alternate input spellings of those same reduced values, but cannot admit a new displayed number form.

The earlier guard accepted small-magnitude inputs with arbitrarily large denominators or radical complexity. That was a workload bypass, corrected in version `ivp-constant-v2`. Validation now rejects positive/negative 1/1000003, √5, (√2+√3)/4 and √2/1000003 in every easy source layout under default, observed and completed profiles (285 calls). It also checks actual displayed functions/stages and native grading at rational catalog edges and the supported radical values. Source replay still reproduces all 19 prompts, 63 values and 17 present solutions exactly.
