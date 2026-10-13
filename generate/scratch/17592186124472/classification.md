# Classification

Captured database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The untouched wrapper is `source.json`. There are **10 practice questions**, 5 observed easy, 3 observed moderate and 2 unrated. The canonical example is additional evidence, not practice coverage. No hard practice question exists.

All practice questions have one `selection` radio field and exactly five text choices. Choices name subsets of four panel labels. The graphs are in the prompt, never in choices. Eight practice records include a correct designation and worked solution. Two unrated records omit both; raw replay preserves these omissions, including absence of `:question/difficulty`.

| Observed prose/layout family | Sources | Difficulty | Plot rating |
|---|---|---|---|
| Single passing panel, solution diagram | q-66509, q-66514 | easy | heavy |
| Two passing panels, solution diagram | q-66510, q-66508 | easy | heavy |
| None passing, prose-only solution | q-36905 | easy | heavy |
| Single passing panel, solution diagram | q-108581, q-36063 | moderate | heavy |
| Single passing panel, prose-only solution | q-108605 | moderate | heavy |
| Captured prompt/bank, absent solution and label | q-36000, q-36897 | unrated | heavy |

The API has one raw umbrella template, `captured-graph-bank`, and ten complete source profiles retaining every prose variation and bank. These profiles have opaque geometry and are evidence-only. `extraction.json` contains every original prompt, solution, choice, key presence and individual panel description, including the canonical example.

Eligible authored practice uses three templates: `easy-graphs`, `moderate-graphs`, `hard-graphs`, each one radio field/five choices and heavy plotting. Default banks are the ten source-shaped complete subset banks, selected before parameters. They are authored extensions of those banks: the correct subset is computed from the actual four graphs, not copied from a historical key. There is no inferred distractor diagnosis in learner text.

The lesson route is read by `:activity/first-step` then `:step/next`: introduction → this KP → graph interval selection → description interval selection. This generator stays at the second step. Prerequisites are Graphs of Inverse Functions and One-To-One Functions. Later interval-selection KPs provide a boundary, not additional generator tasks.
