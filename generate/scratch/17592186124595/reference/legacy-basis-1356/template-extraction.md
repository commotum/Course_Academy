# Template extraction: four stages

Math basis 1356, exact raw wrapper in source.json. C=cos(theta), S=sin(theta). Every row below belongs to field selection, type radio, value type math. Each listed five-member bank is atomic. Exact raw source values are retained; generalized expressions are inferred parameterized shapes, not claims of recovered author intent. Correct entries are mathematical derivative fragments, not whole equations. No rounding instructions or blanks occur.


## Stage 1: specific observations

Each original is described below with its exact parameters, full original values, and corresponding shape. q37186 and q95001 have no captured difficulty, correct ref or solution. Seven others are moderate. All function variables are r and theta, while x/y specify the desired derivative. Radial powers are 1 except q95130 (2); angular frequencies are 1,2,3,4. Constants have signs −1,+1,+2. No numerical evaluation point or axis-specific angle restrictions occur. All solutions use the chain-rule formula, two polar partial derivatives, and a final aligned chain of expressions; counts vary as documented.


## Stage 2: shared pattern

Calculate a first Cartesian partial derivative of a function already given in plane polar coordinates. Find both polar partials; multiply by the correct coordinate factors (including 1/r and the x minus sign); then simplify at the source-supported level. Fixed formula, full prose and field shapes are preserved. These are nine families because their complete function expressions, pedagogical row masks, and banks differ.


## Stage 3: component and whole-bank mapping


### q-37186 — offset_sine_y


Function/target pattern: `A r(b+sin(kθ)), y`. Original parameters: `{"A": 1, "b": 1, "k": 2, "name": "w"}`. Profile: `observed:q-37186`. Substitution/collection rows: 2.


| Original complete value | Parameterized expression recipe | Interpretation status |
|---|---|---|

| $\cos θ + \cos θ\sin 2θ - 2\sin θ\cos 2θ$ | `A(b C+C sin(kθ)−k S cos(kθ))` | Inferred shape; cognitive intent unresolved |

| $\sin θ + \sin θ\sin 2θ + 2\cos θ\cos 2θ$ | `A(b S+S sin(kθ)+k C cos(kθ)) [correct]` | Correct, independently derived |

| $\sin θ\sin 2θ + 2\cos θ\cos 2θ$ | `A(S sin(kθ)+k C cos(kθ))` | Inferred shape; cognitive intent unresolved |

| $\sin 2θ + \sin θ\sin 2θ + 2\cos θ\cos 2θ$ | `A(b sin(kθ)+S sin(kθ)+k C cos(kθ))` | Inferred shape; cognitive intent unresolved |

| $\sin θ + \cos θ\sin 2θ - 2\sin θ\cos 2θ$ | `A(b S+C sin(kθ)−k S cos(kθ))` | Inferred shape; cognitive intent unresolved |


Original worked-solution row masks:


1. $(\sin {2 \theta} + 1)\sin \theta+\frac{1}{r}(2 r \cos {2 \theta})\cos \theta$
2. $(\sin {2 \theta} + 1) \sin {\theta}+2 \cos {\theta} \cos {2 \theta}$

### q-95001 — offset_cosine_x


Function/target pattern: `A r(b+cosθ), x`. Original parameters: `{"A": 1, "b": 2, "name": "v"}`. Profile: `observed:q-95001`. Substitution/collection rows: 3.


| Original complete value | Parameterized expression recipe | Interpretation status |
|---|---|---|

| $2\cos θ + 1$ | `A(b C+1) [correct]` | Correct, independently derived |

| $\cos θ + 1$ | `A(b C/2+1)` | Inferred shape; cognitive intent unresolved |

| $2\sin θ - 1$ | `A(b S−1)` | Inferred shape; cognitive intent unresolved |

| $2\cos θ$ | `A b C` | Inferred shape; cognitive intent unresolved |

| $2\sin θ + 1$ | `A(b S+1)` | Inferred shape; cognitive intent unresolved |


Original worked-solution row masks:


1. $(\cos {\theta} + 2)\cos \theta-\frac{1}{r}(- r \sin {\theta})\sin \theta$
2. $(\cos {\theta} + 2) \cos {\theta}+\sin^{2} {\theta}$
3. $2 \cos {\theta} + 1$

### q-165282 — sine_minus_y


Function/target pattern: `A r(sinθ−b), y`. Original parameters: `{"A": 1, "b": 1, "name": "h"}`. Profile: `observed:q-165282`. Substitution/collection rows: 3.


| Original complete value | Parameterized expression recipe | Interpretation status |
|---|---|---|

| $r(1-\operatorname{sin}⁡\theta )$ | `A r(1−b S)` | Inferred shape; cognitive intent unresolved |

| $1+\operatorname{cos}⁡\theta $ | `A(1+b C)` | Inferred shape; cognitive intent unresolved |

| $r-\operatorname{sin}⁡\theta $ | `A(r−b S)` | Inferred shape; cognitive intent unresolved |

| $\operatorname{cos}⁡\theta -\operatorname{sin}⁡\theta $ | `A(C−b S)` | Inferred shape; cognitive intent unresolved |

| $1-\operatorname{sin}⁡\theta $ | `A(1−b S) [correct]` | Correct, independently derived |


Original worked-solution row masks:


1. $(\sin {\theta} - 1)\sin \theta+\frac{1}{r}(r \cos {\theta})\cos \theta$
2. $\sin^{2} \theta-\sin \theta+\cos^{2} \theta$
3. $1 - \sin {\theta}$

### q-95129 — radial_plus_sine_x


Function/target pattern: `A(a r+sinθ), x`. Original parameters: `{"A": 1, "a": 2, "name": "h"}`. Profile: `observed:q-95129`. Substitution/collection rows: 3.


| Original complete value | Parameterized expression recipe | Interpretation status |
|---|---|---|

| $2\operatorname{sin}⁡\theta +2r\operatorname{cos}⁡2\theta $ | `A(a S+a r cos(2θ))` | Inferred shape; cognitive intent unresolved |

| $\frac{1}{2r}\operatorname{sin}⁡2\theta $ | `A sin(2θ)/(2r)` | Inferred shape; cognitive intent unresolved |

| $2\operatorname{cos}⁡\theta +r\operatorname{sin}⁡2\theta $ | `A(a C+r sin(2θ))` | Inferred shape; cognitive intent unresolved |

| $2\operatorname{cos}⁡\theta -\frac{1}{2r}\operatorname{sin}⁡2\theta $ | `A(a C−sin(2θ)/(2r)) [correct]` | Correct, independently derived |

| ${cos}^{2}⁡\theta +\frac{1}{r}{sin}^{2}⁡\theta $ | `A(C²+S²/r)` | Inferred shape; cognitive intent unresolved |


Original worked-solution row masks:


1. $(2)\cos \theta-\frac{1}{r}(\cos {\theta})\sin \theta$
2. $2 \cos {\theta}- \frac{\sin {\theta} \cos {\theta}}{r}$
3. $2\cos \theta- \frac{\sin {2 \theta}}{2 r}$

### q-95130 — power_cosine_y


Function/target pattern: `A r^p cos(kθ), y`. Original parameters: `{"A": 1, "p": 2, "k": 3, "name": "g"}`. Profile: `observed:q-95130`. Substitution/collection rows: 2.


| Original complete value | Parameterized expression recipe | Interpretation status |
|---|---|---|

| $r(3\operatorname{sin}⁡\theta \operatorname{cos}⁡3\theta +2\operatorname{cos}⁡\theta \operatorname{sin}⁡3\theta )$ | `A r^(p−1)(k S cos(kθ)+p C sin(kθ))` | Inferred shape; cognitive intent unresolved |

| $r(2\operatorname{sin}⁡\theta -3\operatorname{cos}⁡\theta )$ | `A r^(p−1)(p S−k C)` | Inferred shape; cognitive intent unresolved |

| $2\operatorname{sin}⁡\theta \operatorname{cos}⁡3\theta -3\operatorname{cos}⁡\theta \operatorname{sin}⁡3\theta $ | `A(p S cos(kθ)−k C sin(kθ))` | Inferred shape; cognitive intent unresolved |

| $\operatorname{cos}⁡3\theta -\operatorname{sin}⁡3\theta $ | `A(cos(kθ)−sin(kθ))` | Inferred shape; cognitive intent unresolved |

| $r(2\operatorname{sin}⁡\theta \operatorname{cos}⁡3\theta -3\operatorname{cos}⁡\theta \operatorname{sin}⁡3\theta )$ | `A r^(p−1)(p S cos(kθ)−k C sin(kθ)) [correct]` | Correct, independently derived |


Original worked-solution row masks:


1. $(2 r \cos {3 \theta})\sin \theta+\frac{1}{r}(- 3 r^{2} \sin {3 \theta})\cos \theta$
2. $r(2\sin \theta\cos 3\theta-3\cos \theta\sin 3\theta)$

### q-95132 — double_sine_x


Function/target pattern: `A r sin(2θ), x`. Original parameters: `{"A": 1, "name": "f"}`. Profile: `observed:q-95132`. Substitution/collection rows: 5.


| Original complete value | Parameterized expression recipe | Interpretation status |
|---|---|---|

| $3{sin}^{2}⁡\theta $ | `3 A S²` | Inferred shape; cognitive intent unresolved |

| ${cos}^{3}⁡\theta \operatorname{sin}⁡\theta $ | `A C³ S` | Inferred shape; cognitive intent unresolved |

| $2{sin}^{3}⁡\theta \operatorname{cos}⁡\theta $ | `2 A S³ C` | Inferred shape; cognitive intent unresolved |

| $2{sin}^{3}⁡\theta $ | `2 A S³ [correct]` | Correct, independently derived |

| $2{cos}^{3}⁡\theta $ | `2 A C³` | Inferred shape; cognitive intent unresolved |


Original worked-solution row masks:


1. $(\sin {2 \theta})\cos \theta-\frac{1}{r}(2 r \cos {2 \theta})\sin \theta$
2. $\sin 2\theta\cos \theta-2\cos 2\theta\sin \theta$
3. $2\sin \theta\cos \theta\cos \theta-2\sin \theta(\cos^{2} \theta-\sin^{2} \theta)$
4. $2\sin \theta\cos^{2} \theta-2\sin \theta\cos^{2} \theta+2\sin^{3} \theta$
5. $2\sin^{3} \theta$

### q-95133 — cosine_y


Function/target pattern: `A r cos(kθ), y`. Original parameters: `{"A": 1, "k": 2, "name": "w"}`. Profile: `observed:q-95133`. Substitution/collection rows: 2.


| Original complete value | Parameterized expression recipe | Interpretation status |
|---|---|---|

| $-2\operatorname{sin}⁡2\theta \operatorname{cos}⁡\theta $ | `−A k sin(kθ) C` | Inferred shape; cognitive intent unresolved |

| $\operatorname{cos}⁡2\theta \operatorname{sin}⁡\theta -2\operatorname{cos}⁡\theta \operatorname{sin}⁡2\theta $ | `A(cos(kθ) S−k C sin(kθ)) [correct]` | Correct, independently derived |

| $\operatorname{sin}⁡\theta +2\operatorname{cos}⁡\theta $ | `A(S+k C)` | Inferred shape; cognitive intent unresolved |

| $\operatorname{cos}⁡2\theta (\operatorname{sin}⁡\theta -2\operatorname{cos}⁡\theta )$ | `A cos(kθ)(S−k C)` | Inferred shape; cognitive intent unresolved |

| $\operatorname{sin}⁡2\theta (\operatorname{sin}⁡\theta -2\operatorname{cos}⁡\theta )$ | `A sin(kθ)(S−k C)` | Inferred shape; cognitive intent unresolved |


Original worked-solution row masks:


1. $(\cos {2 \theta})\sin \theta+\frac{1}{r}(- 2 r \sin {2 \theta})\cos \theta$
2. $\sin {\theta} \cos {2 \theta}- 2 \sin {2 \theta} \cos {\theta}$

### q-95020 — sine_y


Function/target pattern: `A r sin(kθ), y`. Original parameters: `{"A": 1, "k": 4, "name": "u"}`. Profile: `observed:q-95020`. Substitution/collection rows: 2.


| Original complete value | Parameterized expression recipe | Interpretation status |
|---|---|---|

| $\operatorname{sin}⁡4\theta +4\operatorname{cos}⁡4\theta \operatorname{cos}⁡\theta $ | `A(sin(kθ)+k cos(kθ) C)` | Inferred shape; cognitive intent unresolved |

| $\operatorname{sin}⁡\theta \operatorname{sin}⁡4\theta +4\operatorname{cos}⁡\theta $ | `A(S sin(kθ)+k C)` | Inferred shape; cognitive intent unresolved |

| $\operatorname{sin}⁡\theta \operatorname{sin}⁡4\theta +4\operatorname{cos}⁡4\theta $ | `A(S sin(kθ)+k cos(kθ))` | Inferred shape; cognitive intent unresolved |

| $\operatorname{sin}⁡\theta +4\operatorname{cos}⁡4\theta \operatorname{cos}⁡\theta $ | `A(S+k cos(kθ) C)` | Inferred shape; cognitive intent unresolved |

| $\operatorname{sin}⁡\theta \operatorname{sin}⁡4\theta +4\operatorname{cos}⁡4\theta \operatorname{cos}⁡\theta $ | `A(S sin(kθ)+k cos(kθ) C) [correct]` | Correct, independently derived |


Original worked-solution row masks:


1. $(\sin {4 \theta})\sin \theta+\frac{1}{r}(4 r \cos {4 \theta})\cos \theta$
2. $\sin {\theta} \sin {4 \theta}+4 \cos {\theta} \cos {4 \theta}$

### q-95134 — offset_sine_x


Function/target pattern: `A r(b+sinθ), x`. Original parameters: `{"A": 1, "b": 2, "name": "u"}`. Profile: `observed:q-95134`. Substitution/collection rows: 3.


| Original complete value | Parameterized expression recipe | Interpretation status |
|---|---|---|

| $2r\operatorname{cos}⁡\theta $ | `A b r C` | Inferred shape; cognitive intent unresolved |

| $2\operatorname{cos}⁡\theta $ | `A b C [correct]` | Correct, independently derived |

| $2r\operatorname{sin}⁡\theta -\operatorname{sin}⁡(2\theta )$ | `A(b r S−sin(2θ))` | Inferred shape; cognitive intent unresolved |

| $2\operatorname{cos}⁡\theta +\operatorname{sin}⁡(2\theta )$ | `A(b C+sin(2θ))` | Inferred shape; cognitive intent unresolved |

| $2\operatorname{sin}⁡\theta $ | `A b S` | Inferred shape; cognitive intent unresolved |


Original worked-solution row masks:


1. $(\sin {\theta} + 2)\cos \theta-\frac{1}{r}(r \cos {\theta})\sin \theta$
2. $2\cos \theta+\sin \theta\cos \theta-\sin \theta\cos \theta$
3. $2 \cos {\theta}$

## Stage 4: reusable masks and constraints

`render_math` calculates the displayed polar partials first and fills complete math slots in the fixed source prose skeleton. `render` replaces the complete first function equation slot; it never globally substitutes a short expression in prose, names, arguments or coordinate labels. Seven source solution skeletons each contain exactly three display blocks. q37186/q95001 receive an explicitly authored three-block solution because no original one exists. Every normal generated solution has one fixed sequence independent of chosen answer.

The first final-block row always retains `(f_r)cosθ−(1/r)(f_θ)sinθ` or its y version, including negative partials grouped in parentheses. q95130 keeps its source two-row substitution/factored result. q95133 and q95020 keep two rows. q95129 retains substitution → product expression → double-angle expression. q165282 retains substitution → three-term square distribution → collection. q95134 retains both cancelling sine-cosine products before collection. q95132 retains five rows: chain-rule substitution, evaluated coefficients, double-angle substitution, three-term uncancelled distribution, and collected cubic. Math readback checks every displayed row, not just the final answer; structure assertions require the uncancelled terms.

Variable slots: nonzero bounded A, supported scalar a/b, radial p, frequency k, and complete function name where applicable. No optional source rows are dropped. The specialized cubic family fixes k=2 and radial p=1 because otherwise its identity/cancellation workload changes. The offset-cosine family fixes k=1 to retain identity simplification; its second source wrong recipe b/2 is an inferred numerical-pattern generalization. That interpretation is not promoted to default. The sinusoidal offset x family also fixes k=1 to preserve its cancellation rows. Original parameter sets are valid through the normal interface.

Source profiles calculate exactly all five observed expressions together. Correctness is independently checked against the inverse Cartesian Jacobian; every displayed full expression is compared one-to-one under exact trig equivalence. Reject the whole sampled instance if any option is invalid or equivalent; never replace a subset using a first-valid pool. Source q95130 retains its radial omission shape even when another parameterization would collide; then the whole bank is rejected.

Authored defaults: answer, omit angular contribution, reverse angular sign, use other Cartesian axis, retain one erroneous radial factor. Easy instead uses radial-only answer, rotated coordinate factor, omitted radial exponent multiplier, extra r, and reversed sign. These are complete five-operation banks, separately labeled and checked. No source-bank inference is described as an observed error diagnosis.

Scope/ranges and missing-level justification are in classification.md; all explicit inputs use those same bounds. Hard permits nonzero offsets, supported trig kind/axis and bounded p/k: no higher derivative, new trig identity skill, cylindrical/spherical task, or inverse Cartesian→polar question.

Domain: r>0, theta real on a locally continuous branch. Formula validity is local; no claim at the origin. T-independent radial functions use the same coordinate relation. Choices are functions on this domain, so collision checking uses whole functional equivalence, not isolated evaluations.

Identities: question content includes VERSION, actual displayed problem, fixed solution, orderless complete displayed bank, correct expression, field shape and domain. Bank/prose changes produce different content identity. The mathematical fingerprint canonicalizes the function using expanded integer-angle trig expressions and the target Cartesian axis; it excludes function label, seed, profile, bank, layout and level. The assessed operation is derivative of this complete function, not solely its final value.

Anomalies/fidelity denominators: q165282 final h_x label is repaired to h_y (one mathematical-label repair; 6/7 raw labels otherwise preserved). Unicode function-application marks and operatorname/squared-word TeX become standard trig notation. Raw exact worked-solution strings are 0/7, normalized fixed prose and ordered equivalent math stages are 7/7. Every original bank still has 5/5 complete value matches. q37186/q95001 independent correct refs are inferred (2), while present original refs match 7/7. No missing source worked solution is reported as matched. Normal source-parameter rendering is not literal-source returning, and varied parameters exercise every profile.

## Plots, steps 5 and 7

None required: source practice has no image references. No renderer or asset recreation is applicable. The context tree diagram is a static lesson illustration and is not inserted into practice.

