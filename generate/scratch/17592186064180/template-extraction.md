# Template extraction

Each complete source uses the integral rule sec²(v) -> tan(v), with linearity where needed. The required response is an antiderivative plus an arbitrary constant. Variable roles, numeric features, exact original layout, complete field/choice mappings and source-specific components are retained in source-analysis.json. templates.json contains the executable Markdown, fixed worked-solution sequence and full bank recipes. review.md compares source questions to exact replay and variants.

| Template / profile | Integrand and parameters | Complete choice recipes, in retained source order | Canonical index |
|---|---|---|---:|
| q-113936 | a sec²(theta), observed a=2 | a sec(theta)+C; -a csc(theta)+C; -csc²(theta)+C; tan²(theta)+C; a tan(theta)+C | 4 |
| q-113937 | -a sec²(z), observed a=4 | -a sec(z)+C; a tan(z)+C; a sec²(z)+C; a cot(z)+C; -a tan(z)+C | 4 |
| q-113944 | sec²(x)-b csc(x)cot(x), observed b=2 | tan(x)+b csc(x)+C; cot(x)-b csc²(x)+C; tan(x)-b cot(x)+C; cot(x)+b csc(x)+C; -tan(x)+b csc²(x)+C | 0 |
| q-2164 | b csc(x)cot(x)+sec²(x), observed b=4 | b csc(x)+tan(x)+C; -b csc(x)-tan(x)+C; b csc(x)+sec(x)+C; -b cot(x)+tan(x)+C; -b csc(x)+tan(x)+C | 4 |
| q-49122 | sec(x)(a sec(x)+b tan(x)), observed a=7,b=4 | -a tan(x)+b csc(x)+C; -a tan(x)-b csc(x)+C; a tan(x)+b sec(x)+C; a cot(x)+b sec(x)+C; a cot(x)-b sec(x)+C | 2 |

All bank expressions are observed profiles, rather than inferred descriptions of mistakes. Every option reproduces its exact original value at the source parameters; full mathematical values, designated correct answers and counts are checked independently. No pooled bank or mixed-profile bank is authored. The solutions retain every source sentence and equality line, including nested aligned markup. There are no repairs to supported sources.

Sampling is a bounded extension of observed coefficient values: positive integer magnitudes 1..9, restricted to 2..9 in the easy templates to preserve nonunit layout. Source signs, unit trig arguments and fixed variables are retained. In the two unscaled moderate templates the sec² coefficient stays 1. Sampling preserves observed values and all template conditions. It does not claim coverage of fractional or arbitrary real coefficients. Common variable renaming, seed changes, bank changes and choice order do not count as new tasks. The exact expanded integrand defines mathematical novelty, independently of bank/identity.

Every integral is local to real connected intervals avoiding all trig poles. Correct options are independently differentiated; all distractors must differentiate differently from the prompt and be pairwise inequivalent on the common domain. The complete finite parameter domain is checked, including a=b and a!=b in the factored template. No additional feedback is added to learner content.
