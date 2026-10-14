# Classification (math, basis 1356)

Lineage: `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Frozen wrappers are retained as `source.json`; no database writes. Seven practices: six rated hard, one unrated. Six sources have one radio field; q-82874 has TWO captured `selection` radio widgets. Each field owns five math choices, and none has answer feedback. q-38374 omits difficulty, worked solution **and correct reference**. The older q-82874 widget omits its correct reference; the later widget has the original correct reference3/20. No easy or moderate source labels were inferred.

| Template | Sources | Observed level | Plot requirement |
|---|---|---|---|
| Simple sheared parabola, horizontal cap | q-38374 | absent | none in original; moderate in authored normal output |
| Quartic versus sloped line | q-82874 | hard | moderate, solution region |
| Product hyperbola, y±ax variables | q-160885 | hard | moderate, solution region |
| Downward parabola with translated v | q-82878 | hard | moderate, solution region |
| Upward shifted parabola, horizontal cap | q-83943 | hard | moderate, solution region |
| Upward shifted parabola, vertical cap in xy | q-83947 | hard | moderate, solution region |
| Product hyperbola, x±ay variables | q-160710 | hard | moderate, solution region |

Seven observed Markdown/value templates and seven public raw profiles preserve eight complete field-owned banks (40 values,6 existing correct refs,2 absent refs). The two q-82874 widgets have the same value bank but distinct identities and correct-ref presence. The two hyperbolas share integration mathematics but retain their distinct supplied maps, determinant matrices and boundary substitutions. They are unordered same-level applications. The original five-option banks are public `raw:q-ID` profiles, all explicitly ineligible evidence; several numerical wrong-answer intentions are underdetermined. Normal output uses a separately labeled complete `method` bank, selected before sampling.

## Curriculum and authored missing levels

The route is followed through first-step/next, not collection order: Introduction → The Change of Variables Formula → A Worked Example → Mapping an Area to a Rectangular Region: Transformations Given → Mapping an Area to a Rectangular Region: Transformations Not Given → Finding an Area by Transforming to a Type I Region. Prerequisites are Transformations of Regions Between Curves (4134) and Double Integrals Over Type I Regions (2151). Neighboring rectangular-region KPs are outside these generators.

Easy is an authored assignment of the q-38374 method: unit determinant shear, unshifted upward parabola, positive perfect-square gap through36, with integer shear coefficients through8. Moderate is authored from canonical e-7283 (`u=3x−2y,v=x+y`) together with the direct symmetric-interval primitive stages in q-83943: mixed two-coordinate map, nonunit determinant and reciprocal factor, still unshifted and perfect-square endpoints. This adds determinant arithmetic within this KP; it does not ask learners to choose a transformation. Hard retains the six observed families and ratings. Up/vertical require nonzero shifts, down requires a positive translation and nonsquare gap; quartic and hyperbola retain their respective degree-four and logarithmic workload. Explicit inputs obey the same guards as random samplers. There is no within-level progression.

## Source anomalies and treatment

- q-38374: absent rating/solution/correct ref. Authoritative `/home/jake/Developer/MA/DATA/Lessons/1998/Source/1998.json` widget confirms the same five values and one field, but supplies no key or solution. Raw replay omits all three. Normal easy independently derives `∫[-1,1](1−u²)du=4/3`; this is an authored completion, not a matched original designation.
- q-82874: the older widget’s correct reference is absent; the later widget supplies3/20. Raw output retains both widgets with distinct field-owned IDs and each omission/present ref intact. The authoritative MA capture has one five-option multiple-choice widget; normal output retains one assessment field and uses the later captured designation as corroborating evidence. The source intersection row states `u³(u−1)=0`. The curve intersection is `u⁴=u`, hence `u(u³−1)=0`. Roots and final area happen to agree; the printed polynomial is wrong. Raw evidence retains it, normal output uses the correct factorization.
- q-82878: prose states `y=v+1` after defining `v=y+1`. Correct substitution is `y=v−1`. The actual source curve calculation and final area are correct. Normal prose uses the actual supplied map, avoiding the bad inverse statement.
- Source system/set strings contain literal unmatched grouping braces. Raw profiles preserve decoded bytes. Normal output uses visible `\left\{...\right.` systems and escaped set braces, independently checked for balanced groups.
- q-83947 image: its vertical axis at approximately x=135 px differs from parabola's vertex/symmetry center at approximately x=169 px. The labels ±2 also do not agree with this axis. Raw image evidence is preserved; all normal geometry is newly calibrated from the displayed domain.

All raw profiles are evidence-only. Native grading of present source designations is recorded separately from mathematical correctness and source-format completion.


## Full-field audit correction

Parent QA caught a first-widget-only fidelity comparison in the initial draft. Public raw replay and private validation now inspect every frozen widget, every owned choice/type/feedback presence and every existing/missing correct ref. The missing-second-field mutation is rejected. The shared parent fidelity helper reports7 prompts,6 solutions,8 fields,40 values,6 refs,2 absent refs and1 unrated question. Native fixtures project each present original widget separately; the duplicate-key raw record remains ineligible evidence.
