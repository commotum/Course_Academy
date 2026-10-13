# Template extraction: reciprocal ratio

Protocol: [4-template-extraction](../../../docs/4-template-extraction.md), with [plot extraction](plot-extraction.md). Basis **1522**. [Source questions](source-questions.md) reproduce all originals and complete answer banks; [source cases](source-cases.json) map every component and choice before generalization.

## Specific originals

Write a supplied coordinate as n/b and let K=√(b²−n²). Each question recovers the other coordinate K/b and asks for b/K.

| Source | Given | Target | K | Exact answer | Source sequence |
|---|---|---|---|---|---|
| q-124750 | y=1/5 | sec θ | 2√6 | 5√6/12 | Identity → positive cosine → reciprocal → rationalize |
| q-124743 | x=1/3 | csc θ | 2√2 | 3√2/4 | Identity → positive sine → reciprocal → rationalize |
| q-65062 | y=√3/3 | sec θ | √6 | √6/2 | Identity → positive cosine → reciprocal → rationalize and cancel |
| q-85234 | y=√2/3 | sec θ | √7 | 3√7/7 | Identity → positive cosine → reciprocal → rationalize |
| q-65064 | x=√15/5 | csc θ | √10 | √10/2 | Identity → positive sine → reciprocal → rationalize and cancel |
| q-65066 | y=3/5 | sec θ | 4 | 5/4 | No stored solution; answer computed independently |

Inputs are exact positive rational or radical fractions, not measured decimals. Sign comes from the first-quadrant diagram. Every answer is an exact scalar reciprocal ratio, with no degree unit or requested angle.

## Shared pattern and reusable components

Recover the missing sine or cosine using sin²θ+cos²θ=1, select the positive branch, and invert it to obtain cosecant or secant. The target always corresponds to the missing coordinate: given x, ask csc; given y, ask sec.

Fixed components: unit-circle prompt image, “The diagram above …” narrative, one `selection` radio field, five math choices, and one worked solution independent of the chosen option. Variable components: n, b, given axis, function name, all intermediate values, point location, angle, and target answer. Conditional components: simplify a square root, rationalize an irrational denominator, and cancel common factors. Maintain the four observed source families and their separate solution-role wording.

Constraints: b>0; 0<n/b<1; θ strictly in the first quadrant; K>0; all reciprocal denominators nonzero. Observed (n,b) are (1,5), (1,3), (√3,3), (√2,3), (√15,5), and unrated (3,5). Do not infer that n must be an integer or that b=5 is the only useful denominator.

## Markdown/value template

```text
![]({prompt_plot})

The diagram above shows the unit circle. Given that the ${axis}$-coordinate
of the point $P$ is ${given_coordinate},$ use the Pythagorean identity
to find ${target_function}\theta.$
```

The worked solution retains its annotated plot, x=cos θ and y=sin θ, the known coordinate, the three-row identity rearrangement, numerical substitution, and explicit positive-root choice. It then gives the reciprocal. The rationalization block is conditional on K/b being irrational. Preserve source wording and one fixed solution per question; no option-specific feedback is present in the originals.

Calculations are `known=n/b`, `other=sqrt(1-known**2)`, and `answer=1/other`; the plot uses exactly those coordinates. The worked solution must not imply that every input requires rationalization.

## Choice-bank profiles

All six five-choice banks are retained separately in [source-cases.json](source-cases.json), including every answer UUID/entity, original value, field, and complete expression pattern. Numeric radical choices are represented by coefficient/radicand/denominator parameters; entire values are retained even when their underlying error mechanism is unclear. Prompt-based candidate recipes include taking the opposite sign, failing to reciprocate, omitting a denominator scale, or using the supplied numerator in place of b. A candidate that happens to reproduce one source value is not evidence of the original author rule.

For example, `q-65062` includes −n/K, −b/K, 1/K, n/K, and correct b/K at n=√3, b=3. That is a coherent complete observed bank, not a bag of interchangeable distractors. `q-124743` instead has several expressions with altered coefficients and radicands whose generation is unresolved. Do not substitute a more plausible bank and claim fidelity. Future extrapolation must retain source profiles or clearly declare authored banks.

## Missing-easy family

Use positive Pythagorean triples: choose integers a,c,b>0 with a²+c²=b², give a/b, and request b/c. This retains identity recovery, quadrant selection, and inversion, while removing irrational-root simplification and rationalization. Restrict a,c<b; optionally use primitive triples to avoid merely repeated scaled instances. Proposed examples include (a,c,b)=(5,12,13), (8,15,17), and (7,24,25). These are authored sampling choices, not recovered bank limits.

[Authored probe](../probes.md#reciprocal-ratio) gives x=5/13 and asks for csc θ=13/12, preserving the five-choice field and providing a declared authored distractor bank. The source `q-65066` and complete canonical `e-3484` already support the simpler mathematics. **Best judgment: an easy setting is natural here; the missing easy label does not imply a mathematical scope barrier.**
