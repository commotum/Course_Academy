# Four-stage extraction

## 1. Specific originals

`source.json` is an exact complete wrapper copy, including IDs and absent attributes. `source-cases.json` covers all six originals through normal parameterized generator execution. `source-components.json` records each complete original prompt, solution, field, bank value, exact coefficient/log argument and explicit expression-pattern recipe.

q-15707 has an integral-equals prompt, c=2 and a monic x+1 denominator. Its differential line writes du=dx. q-49453 uses a Calculate prompt, c=3 and x+4, and writes dx=du. Both pull out the numerator, substitute, integrate reciprocal u, and restore x. q-49450 and q-49454 have numerator 1 and monic shifted denominators; they omit redundant numerator-factor and Jacobian-factor rows. The first uses an equals prompt and negative shift; the second a Calculate prompt and positive shift. Their substituted row retains the source's redundant `\cdot` followed by a differential. This is well-formed TeX and not a new factor.

q-49452 uses the offset-first denominator 2−3x, a negative nonunit derivative and a signed −1/3 differential. It explicitly substitutes the signed differential, factors it outside the integral, integrates, and returns to x. q-49511 uses Calculate, a displaystyle integral, numerator 2, denominator `3x + 5`, and plain `dx`. Its choices use spaced `\ln \mid ... \mid + C`. Its missing worked solution, correct designation and difficulty are omissions, not empty values. Public original replay retains them. A separate completed profile infers 2/3 ln|3x+5|+C by differentiation and uses the canonical solution chain; the inferred attributes never count as observed matches.

## 2. Shared family

Calculate an indefinite integral of a nonzero constant divided by a nonconstant linear real expression. Substitute u=ax+b, use du/dx=a and dx=(1/a)du, integrate 1/u to ln|u|+C, and restore x. A five-choice radio response supplies a whole primitive. Absolute value is mandatory. The primitive is valid on each connected component of R excluding −b/a. The source does not specify a common constant connecting the two components.

## 3. Components and banks

All original choices, including incorrect ones, are mapped in `source-components.json`. Coefficient historical recipes are [c,1/c,−c,−1/c,1] multiplying ln|ax+b|. Negative-slope recipes are [1/a,−1/a,a,−a,−1] multiplying the displayed log. Negative-shift recipes are ln|ax+b|, −ln|ax+b|, ln|x|, −ln|x|, −ln|ax−b|. Positive-shift historical recipes are ln|ax+b|, (1/b)ln|ax+b|, b ln|ax+b|, ln|x|, b ln|x|. Incomplete q-49511 recipes are [ca,−c/a,c/a,c,−c] multiplying the displayed log.

These formulas exactly reproduce the complete source banks, but the use of b or 1/b as a prefactor does not establish the original author's intended error. All original profiles are labeled evidence-only. Changed-parameter evidence replay remains parameterized and supported within conservative bounds; it never returns literal captured records.

Normal coefficient banks reflect numerator reciprocal/sign/omission errors. Normal negative-slope banks reflect omitted, inverted and signed substitution coefficients. Normal shifted-monic banks contain the correct log, its wrong sign, omitted-shift logs of either sign, and the reflected-shift log. Normal canonical/nonunit banks multiply the correct log argument by [c/a,−c/a,c,ca,1/a], corresponding to correct scaling, sign reversal, omitted Jacobian, multiplied rather than divided Jacobian, and omitted numerator. No explanation of a distractor is added to learner content.

## 4. Reusable masks and slots

The denominator, numerator, slope, reciprocal slope and resultant c/a are whole mathematical slots. Monic source masks keep a=1 and retain their original row omissions, wording, dx/du orientation and final return to x. Negative-slope masks retain offset-first spelling and the signed substitution row. General nonunit masks follow canonical e-449's factor-c, substitute-Jacobian, factor-c/a, log-u, log-x stages. Parentheses around the substituted differential make signed and fractional factors explicit.

Template IDs select source family masks; profiles select an entire bank before sampling. `original` reproduces original evidence, including q-49511 omissions. `method` is the supported normal profile. `completed` selects only the separately inferred q-49511 completion. One deterministic fixed solution is rendered per instance, independent of chosen answer; no response-specific diagnosis occurs.

The script accepts exact rational parameters and applies every level/template bound to explicit inputs. Its mathematical fingerprint is the canceled actual integrand, independent of label, bank/profile, template alias or option order. Presentation identity hashes version, actual difficulty, printed prompt, printed fixed solution, complete sorted answer values, and omission flags. Answer UUIDs are field-owned. Seed/order changes at fixed content preserve IDs. Proportional numerator/denominator spellings deduplicate as the same mathematical task.

Any linear log argument has real domain excluding its unique zero. Whole-bank pairwise response equivalence compares derivatives on common real intervals, so ln|−F| and ln|kF| cannot evade collision rejection. Correctness also requires the prompt pole and the primitive pole to match; equality only on a smaller punctured domain is insufficient for the full intended domain.
