# Classification

Snapshot: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The untouched wrapper is `source.json`; owning topic is Introduction to Matrices (17592186048896 / MA 861).

Seven practice sources were independently inspected, including every complete bank and every image. All diagrams are directed multigraphs: route multiplicity is the number of arrows with the specified ordered departure/arrival, including loops. Entries are not matrix products or numbers of multistage journeys. Ordinary table rows mean **From** and columns mean **To**. Rows must be read in their displayed order; collection order does not establish direction.

| Template | Source | Captured level | Supported level | Fields | Bank | Plot |
|---|---|---|---|---|---|---|
| sum_138940 | q-138940 | unrated | easy, authored assignment | one radio | 1,2,3,4,5 | heavy |
| sum_139685 | q-139685 | unrated | easy, authored assignment | one radio | 0,1,2,3,5 | heavy |
| sum_139689 | q-139689 | moderate | moderate | one radio, HTML matrix | 0,1,2,3,4 | heavy |
| sum_139719 | q-139719 | easy | easy | one radio, four stations | 0,1,2,3,4 | heavy |
| blanks_319346 | q-319346 | easy | easy | three blanks | counts 2,1,3 by field key | heavy |
| blanks_319412 | q-319412 | easy | easy | three blanks, four stations | counts 2,2,0 | heavy |
| blanks_319429 | q-319429 | easy | easy | three blanks with loops | counts 3,2,1 | heavy |
| sum_permuted_four | none | none | hard, authored | one radio, four stations | authored omission/direction/total count | heavy |

There are six observed easy templates counting the two explicitly assigned unrated originals, one observed moderate template, and zero observed hard templates. Keeping these seven masks separate preserves missing-entry positions, three/four-station layouts, bus/train and line/route wording, HTML/Markdown layout, and full solution sequences. These are presentation/missing-entry families, not seven different mathematical skills. Four source radio profiles comprise three numerical catalogs, but remain tied to their original template instances. Three observed blank templates have no distractor bank. Every template requires parameter-dependent diagrams except exact original adjacency matrices, where the captured image is reused.

The source labels are not a strict density hierarchy: an easy three-blank example already has 12 arrows. Hard therefore does not claim “more arrows” alone makes it hard. Its additional demand is reading independent nonidentity row and column orders before matching each directed arrow count. It remains a three-count sum among four labeled stations, with one queried loop and at least one parallel-route count. No matrix arithmetic, index notation, determinant, graph powers, weighted routes, or indirect journeys are introduced.

The lesson route was followed through `activity/first-step` and `step/next`:
Introduction → Square Matrices → Determining Dimensions → Matrices With One Row or Column → Single Row/Column Dimensions → Identifying a Matrix by Description → Using Matrices for Modeling → Matrices for Route Planning. The modeling tutorial explicitly fills departure rows and destination columns. Sibling KPs assess dimensions/description only; the later topic edges lead to matrix addition, determinants, index notation and augmented systems. Those later operations are outside this generator. The canonical example identifies three directed entries including self routes and then sums them. It anchors the missing hard level's same three-entry workload; its harder ordering is an authored design, not a recovered label.

## Source anomalies

- q-138940 and q-139685 lack difficulty, correct designation, and worked solution in EDB. Their original MA JSON/Markdown widgets confirm one radio and complete five-choice banks but contain no recovered solution or correctness marking. Independent diagram reading gives sums **4** and **1** respectively. The generator supplies easy labels and three-count worked solutions, explicitly authored. Missing designations never count as matched source refs.
- q-319429 has the correct second answer `field-2=2` and completed table B→B=2, but the second explanation discusses B→C=2. Its diagram actually has two B self loops. Normal generated solution repairs that one paragraph to B→B. The raw solution remains accessible through `generate(..., profile='raw_solution_319429')`; it is evidence with a known response-stage mismatch. Full raw solution exactness and normal repaired exactness have separate denominators.
- q-319346's final bullet says “there is $3$ route”; this grammatical blemish is retained at original parameters for prose fidelity. Mathematical count and direction are correct.
- The scalar source wrong choices give no defensible unique error-operation interpretation. They are preserved as complete finite count catalogs for replay, rather than attaching arbitrary error recipes. Authored default banks assess omitted queried counts, reversing directed relations and counting all routes.
