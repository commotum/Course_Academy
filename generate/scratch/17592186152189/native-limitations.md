# Native equivalent-entry limitations

Canonical and nontrivially factored coordinate expressions pass native grading. The following exact trig identities are mathematically verified by independent SymPy trigonometric simplification, but the unchanged native engine returns unresolved. These are **not** native accepted alternatives. Twelve checks are raw source evidence; two checks belong to normal blank records whose canonical/factored forms remain supported. Raw source profiles are ineligible for learner sampling.

| Record | Parameters | Eligibility | Actual submitted string | Actual engine error |
|---|---|---|---|---|
| source:q-274862 | `{'a': 5, 'b': 3, 'h': 2, 'k': -1}` | evidence-only | `3*cos(pi/2-theta)+(-1)` | symbolic equivalence is not established by the supported rules |
| source:q-274862 | `{'a': 5, 'b': 3, 'h': 2, 'k': -1}` | evidence-only | `5*sin(theta+pi/2)+(2)` | symbolic equivalence is not established by the supported rules |
| source:q-274862 | `{'a': 7, 'b': 2, 'h': -5, 'k': 3}` | evidence-only | `2*cos(pi/2-theta)+(3)` | symbolic equivalence is not established by the supported rules |
| source:q-274862 | `{'a': 7, 'b': 2, 'h': -5, 'k': 3}` | evidence-only | `7*sin(theta+pi/2)+(-5)` | symbolic equivalence is not established by the supported rules |
| source:q-327171 | `{'a': 3, 'b': 8, 'h': 0, 'k': 5}` | evidence-only | `3*sin(theta+pi/2)+(0)` | symbolic equivalence is not established by the supported rules |
| source:q-327171 | `{'a': 3, 'b': 8, 'h': 0, 'k': 5}` | evidence-only | `8*cos(pi/2-theta)+(5)` | symbolic equivalence is not established by the supported rules |
| source:q-327171 | `{'a': 7, 'b': 2, 'h': -5, 'k': 3}` | evidence-only | `7*sin(theta+pi/2)+(-5)` | symbolic equivalence is not established by the supported rules |
| source:q-327171 | `{'a': 7, 'b': 2, 'h': -5, 'k': 3}` | evidence-only | `2*cos(pi/2-theta)+(3)` | symbolic equivalence is not established by the supported rules |
| source:q-327172 | `{'a': 4, 'b': 5, 'h': -2, 'k': 1}` | evidence-only | `4*sin(theta+pi/2)+(-2)` | symbolic equivalence is not established by the supported rules |
| source:q-327172 | `{'a': 4, 'b': 5, 'h': -2, 'k': 1}` | evidence-only | `5*cos(pi/2-theta)+(1)` | symbolic equivalence is not established by the supported rules |
| source:q-327172 | `{'a': 7, 'b': 2, 'h': -5, 'k': 3}` | evidence-only | `7*sin(theta+pi/2)+(-5)` | symbolic equivalence is not established by the supported rules |
| source:q-327172 | `{'a': 7, 'b': 2, 'h': -5, 'k': 3}` | evidence-only | `2*cos(pi/2-theta)+(3)` | symbolic equivalence is not established by the supported rules |
| generated:hard:22 | `{'a': 3, 'b': 4, 'h': -6, 'k': 3}` | normal canonical/factored supported | `3*sin(theta+pi/2)+(-6)` | symbolic equivalence is not established by the supported rules |
| generated:hard:22 | `{'a': 3, 'b': 4, 'h': -6, 'k': 3}` | normal canonical/factored supported | `4*cos(pi/2-theta)+(3)` | symbolic equivalence is not established by the supported rules |
