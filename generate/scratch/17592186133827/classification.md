# Classification at math basis 1356

Snapshot lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; immutable capture is `source.json`.

Six practices: four rated moderate (`q-76186`, `q-167612`, `q-76479`, `q-76484`), one rated hard (`q-76496`), and one unrated (`q-76187`). Every source has one five-option math radio field named `selection`. No easy examples, blank fields, plots, or mixed layouts are observed. Each practice has a distinct curve/integrand and worked-solution family; each owns a distinct complete bank. The unrated source lacks its worked solution and correct ref as well as difficulty. Public `raw:q-76187` retains all three omissions.

| Generator family | Observed rating | Source | Mathematical workload | Plot rating |
|---|---|---|---|---|
| ratio | moderate | q-76186 | Shift cancellation; planar parabola; square-root substitution; two perfect-square endpoints | none |
| cubic | moderate | q-167612 | Cubic coordinate substitution and collection; factored speed; fourth-power substitution | none |
| cos_diagonal | moderate | q-76479 | Quadratic coordinate into cosine; positive-parameter absolute value; trig primitive | none |
| sine_line | moderate | q-76484 | Two squared sine coordinates; Pythagorean speed; nonnegative cosine; sine substitution | none |
| sin_cos | unrated | q-76187 | Three coordinates, sine/cosine product; decreasing cosine-square substitution | none |
| space_ratio | hard | q-76496 | Three-component speed; rational sum cancellation; two nonzero radical endpoints | none |
| parabola_easy | authored easy | none | Direct y=t replacement, two-component speed, u=4t²+1; zero lower parameter bound | none |

The canonical example requires a three-coordinate ratio and square-root substitution. Its ratio is undefined at its stated endpoint t=0; the integral is interpreted by continuous extension/improper endpoint, not copied into easy output. The authored easy family uses f=ky on r=(t²,t), avoiding that defect while reducing the numerator/denominator bookkeeping. It still evaluates the line integral and performs substitution, so it does not migrate to sibling KP 133829's setup-only task. All easy instances have the same operations and perfect-square substituted bounds. There is no progression within a level.

Lesson order reconstructed from `activity/first-step` and `step/next`: Introduction (34750) → General Formula (34751) → setup sibling 133829 (34744) → elementary evaluation sibling 133830 (34745) → this substitution KP (34740) → Derivation (34741). Substitution prerequisites are algebraic and trigonometric substitution; the listed integration-by-parts prerequisite is not used to invent branches absent from these examples.

The unrated source receives an explicitly authored moderate routing assignment for normal output. Its derivative, absolute-value domain, and elementary substitution demands are comparable to the observed trig examples, with no new integration method. The actual original widget in `/home/jake/Developer/MA/DATA/Lessons/2107/Source/2107.json` confirms one five-choice radio layout and no images, not a duplicate legacy field.
