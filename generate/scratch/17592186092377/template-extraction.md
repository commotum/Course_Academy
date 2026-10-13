# Template extraction

## Stage 1: specific source descriptions

The following table records all source coordinate functions, domains, field shapes and choices before generalization. Every original value and raw worked solution remains in source.json and review.md. The original labels are observed database labels; later sampler policies are authored scope claims.

| Source | x(t) | y(t) | Interval | Answer shape |
|---|---|---|---|---|

| q-10255 | $t - \sin{\left(t \right)}$ | $1 - \cos{\left(t \right)}$ | $[0,\pi]$ | complete scalar length |

| q-10260 | $3 t + 1$ | $2 t^{\frac{3}{2}}$ | $[0,1]$ | complete scalar length |

| q-10256 | $\sin^{3}{\left(t \right)}$ | $\cos^{3}{\left(t \right)}$ | $[0,\frac{\pi}{2}]$ | complete scalar length |

| q-10257 | $2 \cos^{3}{\left(t \right)}$ | $2 \sin^{3}{\left(t \right)}$ | $[0,\frac{\pi}{2}]$ | complete scalar length |

| q-10258 | $- 2 t \cos{\left(t \right)} + 2 \sin{\left(t \right)}$ | $2 t \sin{\left(t \right)} + 2 \cos{\left(t \right)}$ | $[0,\pi]$ | complete scalar length |

| q-10261 | $2 \cos{\left(t \right)} - \cos{\left(2 t \right)}$ | $2 \sin{\left(t \right)} - \sin{\left(2 t \right)}$ | $[0,\pi]$ | complete scalar length |

| q-20907 | $4 \sin{\left(t \right)} + 5$ | $4 \cos{\left(t \right)} + 4$ | $[0,\frac{\pi}{2}]$ | complete scalar length |

| q-348086 | $- t \cos{\left(t \right)} + \sin{\left(t \right)}$ | $- t \sin{\left(t \right)} - \cos{\left(t \right)}$ | $[0,\pi]$ | complete scalar length |

| q-348088 | $t \sin{\left(t \right)} + \cos{\left(t \right)}$ | $- t \cos{\left(t \right)} + \sin{\left(t \right)}$ | $[0,2 \pi]$ | complete scalar length |

| q-351427 | $3 \sin{\left(t \right)} + 2$ | $3 \cos{\left(t \right)} - 4$ | $[0,\frac{\pi}{3}]$ | complete scalar length |

| q-351428 | $5 \sin{\left(t \right)} - 3$ | $5 \cos{\left(t \right)} + 1$ | $[\frac{\pi}{5},\frac{\pi}{2}]$ | complete scalar length |

| q-351429 | $\frac{t^{2}}{2}$ | $\frac{\left(2 t + 1\right)^{\frac{3}{2}}}{3}$ | $[0,2]$ | complete scalar length |

| q-351438 | ${e}^{2 t} \cos{\left(t \right)}$ | ${e}^{2 t} \sin{\left(t \right)}$ | $[0,\frac{\pi}{2}]$ | exponential difference fragment inside L=√5/2(…)  |

| q-351439 | $4 \cos^{3}{\left(t \right)}$ | $4 \sin^{3}{\left(t \right)}$ | $[0,\frac{\pi}{4}]$ | complete scalar length |

| q-351471 | $3 \cos{\left(t \right)} - \cos{\left(3 t \right)}$ | $3 \sin{\left(t \right)} - \sin{\left(3 t \right)}$ | $[0,\pi]$ | complete scalar length |

| q-351474 | $\frac{\left(6 t + 1\right)^{\frac{3}{2}}}{9}$ | $\frac{3 t^{2}}{2}$ | $[0,1]$ | complete scalar length |

| q-351505 | $- \frac{t^{3}}{3} + t$ | $t^{2}$ | $[0,3]$ | complete scalar length |

| q-351508 | $4 t + 2$ | $\frac{8 t^{\frac{3}{2}}}{3}$ | $[0,2]$ | complete scalar length |


## Stage 2: generalized patterns

For each observed coordinate pair X(t),Y(t), compute X′ and Y′, simplify sqrt(X′²+Y′²) using the same source factorization/identity, integrate, and evaluate at an increasing interval [a,u]. The authored uniform scale c multiplies both coordinates, each derivative, the speed, the primitive and the length by c. Derivative product/chain-rule rows, distributed radicands, identity explanations, absolute-value/sign rows, power-rule rows, and numeric endpoint evaluations retain the source sequence. The exponential source keeps its partial blank: its field contains e^(2u)−1, with c√5/2 supplied outside the blank.

Easy contains circle constant speed, involute linear nonnegative speed, polynomial perfect-square speed and elementary square-root power integration. Moderate preserves cubic-trig factoring, exponential product-rule cancellation and its source elementary radical family. Hard preserves cosine-difference and half-angle simplification. These are unordered variants inside the original labels. The elementary-power source appears at easy and moderate; its observed labels alone do not justify inventing a new algebraic branch or claiming a recovered progression.

## Stage 3: component and complete-bank maps

Coordinate functions and interval are prompt components. Derivatives, squared-speed expressions, speed, primitive, endpoint substitutions and length are solution components. Constants that define the method (powers 2/3, trig frequencies, identity statements) stay fixed; c and u vary. The script compiles the captured math blocks into interval/evaluation slots and wraps scaled stages, rather than selecting a literal source payload or lookup answer.

For underdetermined scalar options the observed recipe is explicitly an expression-shape profile: `displayed_original_expression * L(c,u)/L(1,b)`. This is a homogeneous replay generalization, not an inferred author mistake. It is restricted to explicitly requested `profile="observed"` with explicit parameters and is never a default learner bank. Correct values are first computed from the curve integral, then checked against every source designation. The complete maps below account for every option.


### q-10255

Original field key `selection`; type `radio`; complete count 5.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 60627aba-89ef-53b6-b4ce-ca7854856bfc | $\pi $ | False | pi/4 * L(c,u) | scalar expression pattern; author intent unresolved |

| 70edbcb1-0834-5f95-9e7a-268c0a3c7bca | $4\pi $ | False | pi * L(c,u) | scalar expression pattern; author intent unresolved |

| 806bb986-60b0-52f0-9e7d-fe440e12d7b5 | $\frac{\pi }{2}$ | False | pi/8 * L(c,u) | scalar expression pattern; author intent unresolved |

| d998f6fb-b8bd-532a-8961-d0fc2000cb68 | $2\pi $ | False | pi/2 * L(c,u) | scalar expression pattern; author intent unresolved |

| da1538df-e67c-5454-aadf-6bd6796416e3 | $4$ | True | computed length | independently verified integral |

### q-10260

Original field key `selection`; type `radio`; complete count 5.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 0aa3cd51-4469-5ba2-8636-0c4ac940fa23 | $2\sqrt{\pi }-\pi $ | False | (pi - 2*sqrt(pi))/(2 - 4*sqrt(2)) * L(c,u) | scalar expression pattern; author intent unresolved |

| 1b9306d9-9701-5f33-a7ee-c92f9826deea | $4\sqrt{2}-2$ | True | computed length | independently verified integral |

| 30704c9c-37d2-55f6-ba6e-a3279d9dc991 | $8\sqrt{2}-\pi $ | False | -sqrt(2)*pi/7 - pi/14 + 4*sqrt(2)/7 + 16/7 * L(c,u) | scalar expression pattern; author intent unresolved |

| c65faa6c-8d42-5137-bf44-8cf565ae4758 | $\pi $ | False | pi/14 + sqrt(2)*pi/7 * L(c,u) | scalar expression pattern; author intent unresolved |

| dcb869b9-ae25-5d19-9d15-663789818115 | $2\sqrt{2}-2$ | False | 3/7 - sqrt(2)/7 * L(c,u) | scalar expression pattern; author intent unresolved |

### q-10256

Original field key `selection`; type `radio`; complete count 5.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 241e58ea-86ce-5450-939e-02de03cdebfc | $\frac{3}{2}$ | True | computed length | independently verified integral |

| 2e56d505-7726-5af1-871c-95766070a7e1 | $1$ | False | 2/3 * L(c,u) | scalar expression pattern; author intent unresolved |

| 5b86c06b-4025-5e46-b183-b3a382a369a6 | $\frac{2}{3}$ | False | 4/9 * L(c,u) | scalar expression pattern; author intent unresolved |

| 62be5c5d-404d-5b63-b96a-01802a0419b7 | $\frac{3}{4}$ | False | 1/2 * L(c,u) | scalar expression pattern; author intent unresolved |

| f134bbd3-d5b3-51e4-9905-9b65f60e5fa1 | $\frac{4}{3}$ | False | 8/9 * L(c,u) | scalar expression pattern; author intent unresolved |

### q-10257

Original field key `selection`; type `radio`; complete count 5.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 0a98e176-de94-501d-9654-ee79fa546361 | $\frac{3}{2}$ | False | 1/2 * L(c,u) | scalar expression pattern; author intent unresolved |

| 5cbcf497-35c1-530e-8b8a-1e4520aff5ff | $1$ | False | 1/3 * L(c,u) | scalar expression pattern; author intent unresolved |

| 64a92041-6332-5b56-9a49-329279ae7898 | $\frac{2}{3}$ | False | 2/9 * L(c,u) | scalar expression pattern; author intent unresolved |

| c676c67b-ce2e-5ee3-a924-56c7b533c894 | $\frac{1}{2}$ | False | 1/6 * L(c,u) | scalar expression pattern; author intent unresolved |

| ea75476f-d42e-58e7-be1d-885fe5dc9408 | $3$ | True | computed length | independently verified integral |

### q-10258

Original field key `selection`; type `radio`; complete count 5.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 33d582ab-25c3-5d89-b31c-eee9f2c1897c | $\frac{{\pi }^{2}}{4}$ | False | 1/4 * L(c,u) | scalar expression pattern; author intent unresolved |

| 671a11ec-27d8-52b9-9a59-8dd0d0ec54c3 | ${\pi }^{2}$ | True | computed length | independently verified integral |

| 7dedda59-24a2-5ab6-bb9d-20a20b1f41ec | $\frac{{\pi }^{2}}{2}$ | False | 1/2 * L(c,u) | scalar expression pattern; author intent unresolved |

| c654b5a5-a703-55fd-9759-75e1cbdb9a7a | $2{\pi }^{2}$ | False | 2 * L(c,u) | scalar expression pattern; author intent unresolved |

| e227f87d-b8bb-5a30-92ed-b9b3c38e19ca | $\frac{\pi }{4}$ | False | 1/(4*pi) * L(c,u) | scalar expression pattern; author intent unresolved |

### q-10261

Original field key `selection`; type `radio`; complete count 5.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 09aa28b6-42d5-5647-8c67-6ad4ae934fea | $8$ | True | computed length | independently verified integral |

| 1bb02d36-4654-5167-a760-32462c48caf1 | $2\pi $ | False | pi/4 * L(c,u) | scalar expression pattern; author intent unresolved |

| 3ead8f61-e137-5573-914b-52260b377c8b | $1$ | False | 1/8 * L(c,u) | scalar expression pattern; author intent unresolved |

| 478c7a12-33ef-5729-9381-971f513d4e4e | $4\pi $ | False | pi/2 * L(c,u) | scalar expression pattern; author intent unresolved |

| c3466be1-0698-5115-8533-dbaa1ef80524 | $\frac{16}{3}$ | False | 2/3 * L(c,u) | scalar expression pattern; author intent unresolved |

### q-20907

Original field key `selection`; type `radio`; complete count 5.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 0439511f-6bcb-5df1-b107-723ed7eac55b | $2\pi $ | True | computed length | independently verified integral |

| 11540c92-a30f-5e29-852e-f44110b49f42 | $\pi $ | False | 1/2 * L(c,u) | scalar expression pattern; author intent unresolved |

| 3dd6e6c8-c066-57ed-aca5-d04d9fd31bbf | $3\pi $ | False | 3/2 * L(c,u) | scalar expression pattern; author intent unresolved |

| 766a4044-6e95-5e6f-af50-99ef14df0af9 | $4\pi $ | False | 2 * L(c,u) | scalar expression pattern; author intent unresolved |

| d33d668e-b0ca-57c8-867a-44e3e4914dfd | $5\pi $ | False | 5/2 * L(c,u) | scalar expression pattern; author intent unresolved |

### q-348086

Original field key `field-1`; type `blank`; complete count 1.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 413af386-018a-5a79-9059-adefc2791bd5 | $\frac{{\pi }^{2}}{2}$ | True | computed length | independently verified integral |

### q-348088

Original field key `field-1`; type `blank`; complete count 1.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 63e7b79b-6298-5b7e-aa80-09f258e9f2ab | $2{\pi }^{2}$ | True | computed length | independently verified integral |

### q-351427

Original field key `field-1`; type `blank`; complete count 1.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| de455dde-6d11-5b5e-8482-288ea3511e85 | $\pi $ | True | computed length | independently verified integral |

### q-351428

Original field key `field-1`; type `blank`; complete count 1.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 0c3b7c9a-1628-5579-88b4-676c4b08825d | $\frac{3\pi }{2}$ | True | computed length | independently verified integral |

### q-351429

Original field key `field-1`; type `blank`; complete count 1.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 1df2cb4b-8bc6-564a-8b2d-5f0c079efa30 | $4$ | True | computed length | independently verified integral |

### q-351438

Original field key `field-1`; type `blank`; complete count 1.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 462c106d-60a7-517a-bb34-02784bafa0df | ${e}^{\pi }-1$ | True | e^(2u)−1 (supplied coefficient c√5/2) | independently verified integral |

### q-351439

Original field key `field-1`; type `blank`; complete count 1.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| b2bf159b-7ee8-54ca-963e-4a6cee5dc607 | $3$ | True | computed length | independently verified integral |

### q-351471

Original field key `field-1`; type `blank`; complete count 1.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| d1650979-8a8d-5c45-9228-031f33216db2 | $12$ | True | computed length | independently verified integral |

### q-351474

Original field key `field-1`; type `blank`; complete count 1.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 335fc60d-9d0b-5146-9aa1-0fb071f12d2a | $\frac{5}{2}$ | True | computed length | independently verified integral |

### q-351505

Original field key `field-1`; type `blank`; complete count 1.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| fd59335f-9ad0-5fc5-9249-f762bb6a6bd1 | $12$ | True | computed length | independently verified integral |

### q-351508

Original field key `field-1`; type `blank`; complete count 1.

| Original choice UUID | Displayed value | Correct | Parameterized component | Interpretation |
|---|---|---|---|---|

| 1f98797f-08e7-52a2-b61b-fdbd3d8f6443 | $8\sqrt{3}-\frac{8}{3}$ | True | computed length | independently verified integral |


## Stage 4: reusable templates, bounds and authored defaults

One script exposes `generate`, `generate_easy`, `generate_moderate`, and `generate_hard`. It samples an observed coordinate/solution structure, a full compatible bank, a uniform integer coordinate scale 1–6 and an endpoint; rejects the whole instance for nonpositive or duplicate choices; never fills a bank from a first-valid recipe pool. Explicit invalid parameters are rejected without changing them. All shared source prose and displayed solution row counts are preserved. UUIDs are owned by the content/field; mathematical fingerprints canonicalize exact coordinate functions, response shape and domain separately from versioned displayed prompt/solution/complete bank identities. Parameter spelling, seed and option order do not change identity.

Default endpoint pools are authored: circle intervals increment in π/24 from its original lower bound (constant speed requires no trig evaluation); involutes use πn/12 up to 2π (only integrating t); polynomial/linear/power families use integer upper endpoints 1–4. Moderate astroids use u/π in {1/12,1/8,1/6,1/4,1/3,3/8,5/12,1/2}, so cos(2u) has a familiar value. Spiral upper endpoints are πn/12 up to π/2 and remain symbolic exponential values. Cycloid and frequency-two epicycle upper endpoints are π/3,π/2,2π/3,π, keeping the final half-angle evaluation familiar. Frequency-three epicycle endpoints are π times {1/6,1/4,1/3,1/2,2/3,3/4,5/6,1}. There is no sign-crossing or piecewise integration.

Uniform coordinate scaling is an authored extension with the same differentiation, factorization and integration demands; it compensates for the deliberately restricted familiar-angle menus. No new difficulty level is authored because all three are observed. Sampler choices are a design policy, not recovered source authoring code. Bank eligibility and unique assessed instances per level are enumerated in validation.json.

Complete authored radio banks: circle uses L plus dropping the square root R²Δt, omitting the sqrt(2) factor L/√2, doubling L and halving L. Involute uses omission of power-rule division c0(u²−a²), integration of speed squared, speed change c0(u−a), and omission of scale/division u²−a²; for c0=2 its separately declared full bank uses halved L as the fourth wrong operation. Other radio families use L plus halved/doubled L, integrating speed squared, and endpoint speed times interval width. Every bank must be positive and mutually distinct; zero endpoint-speed options at astroid/epicycle boundary force whole-instance rejection. These banks are labeled authored, not asserted source intent.

Presentation compatibility repair: default blank prompts replace Do not round the answer with Give an exact answer. The actual engine learning.rs treats any round substring as normalize-only; originals retain this wording through profile="observed" and their rejected equivalent entries remain explicit capability failures. Canonical source grading and default equivalent/wrong entries are tested separately. This changes no mathematical demand or response shape.

Source-format anomaly: q-20907 has an extra closing parenthesis in the x-derivative coordinate, `d/dt(4 sin t+5))`. The smallest repair removes that parenthesis. It changes no mathematical value or teaching rule; the raw evidence is preserved. One raw source punctuation error is repaired; literal full-solution string equality is not claimed because computed endpoint/evaluation TeX is normalized; complete bank/value/designation/prose/row-count denominators are 18/18. TeX spelling normalization is tracked separately from source semantics.

