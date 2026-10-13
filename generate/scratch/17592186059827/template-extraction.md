# Four-stage extraction

## 1. Specific source descriptions

q-1253 says exactly: `The inequality $9 < x \le 13$ can be expressed in interval notation as`. Ordered positive integer endpoints 9 and13, independent variable x, left strict/right inclusive, one five-choice selection radio field. All choices contain complete membership statements. Four choices vary the two endpoint inclusion bits and the fifth reverses endpoint order. No worked solution, correct ref or difficulty is captured.

q-25754 says exactly: `The interval $y ∈ [- 5, 2\sqrt{2})$ corresponds to the inequality`. The lower endpoint is a spaced negative integer, the upper endpoint a positive scaled square root. It has a left bracket/right parenthesis, variable y, one five-choice selection radio field. Choices contain complete compound inequalities. Four vary the comparisons; the fifth omits the lower endpoint's minus sign. No worked solution, correct ref or difficulty is captured. Source strings have zero adjacent decoded backslash pairs; JSON escaping is not a source error and no TeX repair is claimed.

## 2. Shared pattern

Translate a bounded half-open set between interval membership and a compound inequality, keeping endpoints and variable unchanged and choosing strict versus inclusive symbols independently. Endpoint forms affect reading but require no evaluation, solving, or graph interpretation. Two prompt layouts are retained as distinct families.

## 3. Components and complete banks

Let a<b, v be the independent variable, and c mean the left endpoint is included (the right endpoint is then excluded). Source bank option order is not semantically persistent. The table maps all captured options exactly; normal output shuffles all five deterministically.

| Profile/source | Captured complete choice | Parameterized operation | Correctness derived independently |
|---|---|---|---|
|1253|`x ∈ (9, 13]`|membership(a,b,left open,right closed)|correct|
|1253|`x ∈ (9, 13)`|membership(a,b,both open)|wrong|
|1253|`x ∈ [9, 13]`|membership(a,b,both closed)|wrong|
|1253|`x ∈ [9, 13)`|membership(a,b,left closed,right open)|wrong|
|1253|`x ∈ (13, 9]`|membership(b,a,original inclusion bits)|wrong; reversed endpoints denote empty set|
|25754|`-5 < y < 2\sqrt{2}`|a<v<b|wrong|
|25754|`-5 \le y < 2\sqrt{2}`|a≤v<b|correct|
|25754|`5 \le y < 2\sqrt{2}`|(-a)≤v<b|wrong; empty at source parameters|
|25754|`-5 \le y \le 2\sqrt{2}`|a≤v≤b|wrong|
|25754|`-5 < y \le 2\sqrt{2}`|a<v≤b|wrong|

All ten displayed values are reproduced exactly. Operation interpretation is descriptive, not a claim that the original author intended a particular learner error. The sign omission is eligible only with a nonzero lower endpoint and a left-closed input, preventing duplicate choices. The observed1253 profile requires right-closed input. The fifth normal authored interval-to-inequality choice reverses endpoints, using the same complete-order error seen in1253. This is labeled authored; no scalar fitting or unrelated perturbation is used. All options are independently compared as complete real sets, including the empty set, so an extra empty distractor would reject the whole instance. Reversed bounds are deliberately wrong responses to an ordered nonempty source interval, not acceptable translations.

## 4. Reusable masks, constraints and solution

The two masks preserve the source sentences. Slots are complete endpoint expressions and the variable; no global short-string substitution is used. Source25754's spaced minus is rendered as a complete negative-integer endpoint-format component in observed profiles. Math choice values are delimiter-free, while the prompt's expression is inline math. Each bank is selected whole, then constructed and checked for a unique correct value and five distinct values. Raw profiles omit rating, solution and key. Unsuffixed profiles render the same parameterized prompt/bank and add only supported absent information. Raw replay is available through generate(), including changed parameters; no literal-source return branch exists.

Shared canonical opening is copied in full. Because practice solutions are absent, subsequent stages are explicitly authored: show the given mathematical object, identify both endpoints and inclusion, state the corresponding symbol for each, and show the translated object. The interval-to-inequality sequence follows the canonical endpoint bullets and final inequality; the reverse sequence uses the same correspondence in reverse. There is one fixed solution per instance, independent of the submitted error. Independent QA parses both display blocks plus both prose endpoint values and the corresponding symbols; no source-solution sequence fidelity is claimed.

Normal easy explicit bounds are integers0..15. Normal moderate bounds are exact rationals of magnitude≤10 and denominator≤5, a<0, with at least one noninteger. Its finite sampler uses numerators−15..15 and denominators1..5. Hard explicit bounds are integers or square roots whose squares are positive integers≤144, magnitude≤15, a<0 and at least one irrational bound. Its finite sampler uses integers−8..8 and ±k√n, k=1,2,3 and n=2,3,5,6,7. Guards apply after exact reduction, including explicit inputs. All author samplers provide either inclusion orientation and either direction without an ordering/progression. Observed replay domains intentionally preserve captured parameter features, with |endpoint|≤20; this is a separate documented evidence domain, not an override available to ordinary defaults.

Finite catalogs enumerate ordered endpoint pairs, inclusion and direction. Catalog counts in validation.json exclude the four variable-letter aliases. Mathematical fingerprints likewise exclude variable spelling, bank, profile, seed and answer order; they include exact reduced endpoints, inclusion and requested direction. Content identities include actual prompt, fixed solution, full sorted bank, correct designation/absence, displayed rating/absence and version. A source profile alias that renders identical content cannot create a new identity. New banks or raw-versus-completed records have distinct identities.
