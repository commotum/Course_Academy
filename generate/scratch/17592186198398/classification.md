# Classification at basis 1356

Database `math`; basis 1356; lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Frozen source is `source.json`, unchanged from the capture wrapper. Seven practice questions: five moderate, two unrated. All use one five-choice math radio keyed `selection`. No plot in practice prompts, choices or solutions. Plot rating **none**. Canonical transformation vector diagrams are mathematical notation, not geometric graphs, and normal solutions retain the same transformation formula as TeX.

| Source DB ID | MA ID | Observed level | Template | Required scalar | Complete bank |
|---|---|---|---|---|---|
| 17592186198623 | q-162139 | absent | power | 3 | 3, −2, 4, 2, 1 |
| 17592186198964 | q-39055 | absent | vcosu | 2 | 2, 2√3, ln(2)/4, √2, ln(2) |
| 17592186374090 | q-161916 | moderate | ucosv | 2 | 2/3, 3, 1/2, 2, 5 |
| 17592186374097 | q-161917 | moderate | sum | 12 | 12, 10, 15, 8, 7 |
| 17592186374125 | q-161929 | moderate | exp | 2(e³−1) | √2(e³−2), 2e³, e³−1, 4(e³−2), 2(e³−1) |
| 17592186374132 | q-161931 | moderate | zcosu | −6 | 9, −2/3, 1/6, −6, −1/9 |
| 17592186374139 | q-161934 | moderate | sinsin | −1 | −8, −1/2, −1/4, −1, −2 |

The two unlabeled required values above are independent mathematical inferences, not observed correct designations. Raw replay preserves absent `:question/difficulty`, `:question/worked-solution` and `:answer-field/correct`. Their API routing is explicitly authored moderate. Seven template/bank pairs are distinct: integrand operation, transformation structure, legacy single-inline versus multiline layout and sequential sum versus separated-product worked stages matter. The two legacy layouts have no worked solution; the five rated solutions share all opening prose and the four numbered steps.

`q-161916` omits the final closing parenthesis of the last endpoint difference `(1-(-1)`. It retains the correct scalar 2 and correct determinant −2. Exact public raw replay retains this formatting error and is ineligible. Normal authored output expands balanced individual terms. Decoded source inspection verifies single backslash characters in all legacy choice commands: apparent extra escaping in a printed Python list is not a source error. No source mathematical error was found.

The activity route follows `activity/first-step` 17592186199269 and `step/next`: introduction → setup KP98397 → evaluation KP98398 → volume KP98399. Incoming prerequisites are 3D Jacobian, double-integral change of variables and triple-integral volume computations. The canonical evaluation transforms `(x+y²)^15 z` into `u^15 w/4` over a box, then evaluates separated one-variable primitives. Thus linear/quadratic shears, constant determinant, elementary power/exp/trig primitives and rectangular bounds are within scope. Volume reconstruction and selecting a substitution remain outside this generator.

No observed easy/hard counts are invented. Authored easy lowers the polynomial integrand to `uv`, keeps zero lower endpoints and familiar integer bounds, and still computes the Jacobian and whole scalar integral. Authored hard keeps each source family and familiar primitive operations, but all three lower endpoints AND each lower primitive component are nonzero; three separate lower contributions must be evaluated before collection. Moderate requires at least one zero lower endpoint; hard rejects cosine/sine endpoints where its corresponding primitive vanishes. These guardrails apply equally to explicit parameters and random sampling, and the checked mathematical task domains are disjoint. There is no within-level progression or new integration method.
