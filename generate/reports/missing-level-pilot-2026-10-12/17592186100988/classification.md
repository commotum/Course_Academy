# Classification: Finding an Entry of a Matrix

EDB `math`, basis **1522**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. KP `17592186100988`, canonical example `e-4371`. Protocol: [3-classify](../../../docs/3-classify.md).

The selected missing **moderate** score is **92.5497**, based on five distinct rated questions. The bank contains five easy questions and two unrated questions; there are no moderate or hard labels. No question generator is associated with this KP. Its owning topic is **Index Notation for Matrices**.

Read all seven practice prompts, 27 answer values, and all five available worked solutions. Each question has exactly one field. [Specific originals and every choice](source-questions.md) and [structured component/choice mapping](source-cases.json) preserve the full inventory.

| Difficulty | Field type | Markdown/value templates | Bank profiles | Plots |
|---|---|---:|---:|---|
| Easy | Radio `selection` | 1 | 3 | None |
| Easy | Blank `field-1` | 1 | None | None |
| Moderate | No sources | 0 | None | None |
| Hard | No sources | 0 | None | None |
| Unrated | Radio `selection` | 2 incomplete families | 2 | None |

The rated radio template asks for a supplied index, displays a rectangular matrix, and repeats the matrix after identifying the entry. `q-279260`, `q-13497`, and `q-125561` share that pattern. The “lies” versus “should lie” wording and punctuation are retained as source render styles; they do not add a mathematical template. Their three complete five-choice banks remain separate profiles. `q-13497` includes a text “No such entry” option; the other two rated banks do not.

The blank template, `q-279539` and `q-279540`, adds `${letter}_{ij}=$` and `{{field-1}}`. It expects the entry alone, not an equation or index pair. Its owned single answer is a grading reference, not a distractor.

`q-13488` is an inline, in-bounds radio source. `q-13496` asks for row 4 in a three-row matrix. Both lack difficulty, a correct-answer reference, and a worked solution. Their mathematically supported answers are respectively 2 and “No such entry”; those conclusions are recorded separately from missing source markings.

All source matrices are typeset mathematics, not images or plots. Increasing dimensions requires changing matrix Markdown, not plotting infrastructure.

The source already labels a **5×4 matrix with target e₅₃ as easy**. Larger dimensions therefore offer weak grounds for inventing a moderate setting. The adjacent KPs separately cover square matrices and describing an entry in index notation. Reversing the task to request an index pair would cross that boundary. Transposition or matrix arithmetic would introduce additional procedures.

**Classification result:** many numerical and layout variants are easy to write; a genuinely distinct moderate family is difficult to justify while retaining this KP's one-operation scope.
