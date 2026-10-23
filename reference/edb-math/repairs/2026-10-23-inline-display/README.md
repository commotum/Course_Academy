Committed the authorized formatting repair to `math` in **34 CAS batches, T5766–T5799**, with source `:agent/codex`.

The repair made **17,416 formatting changes across 13,225 fields on 12,173 entities**. It created **17,339 display equations** and restored display-style sizing in **77 retained inline expressions**. This includes **5,974 substantive integral expressions promoted to display blocks**, 63 comparative integral references kept full-size within prose, and 14 integral expressions kept full-size within structured layouts.

| Content attribute | Repaired fields |
|---|---:|
| `question/problem` | 9,257 |
| `question/worked-solution` | 3,567 |
| `tutorial/content` | 390 |
| `multistep/context` | 9 |
| `answer/feedback` | 2 |

[Commit verification](verification.json) confirms every batch committed and all 13,225 fields matched their exact expected values when read again at **T5799**. The [global post-repair check](global-post-repair-check.json) scanned 2,722,266 facts, including 158,569 prose fields, and found **zero remaining changes under the validated formatting policy**.

The policy promotes substantive integrals, standalone large expressions/calculation chains, multiline derivations, large matrices, long fraction/radical calculations, and main large-operator calculations. Compact vectors, matrices and operator references remain inline when appropriate. Existing answer-table and matrix-operand layouts are preserved. Comparative integral references and formulas inside structured answer layouts receive `\displaystyle` without changing their placement.

New display equations use `$$` delimiters and explicit display style. The delimiters are protected before Markdown parsing by the actual player, allowing display math inside existing paragraphs and list items without changing their Markdown structure. Where punctuation immediately followed an equation, it was moved inside its new display delimiters. Seventeen captured question equations also needed removal of accidental source indentation that was causing Markdown code-block rendering.

[Content verification](content-verification.json) proves that every repaired field is idempotent under the policy and that answer markers were preserved. Preparation additionally checks that the sequence of mathematical bodies is unchanged except for the explicit style prefix and recorded punctuation relocation. Image references are preserved. The transaction forms update only existing scalar content attributes; question identities, answer values, answer-field/choice links, grading, lesson/KP structure, generators, learner responses and progress are unchanged.

[Renderer verification](render-verification.json) exercised all 13,225 exact before/after fields through the installed player's Markdown protection, sanitization and MathJax pipeline. It confirmed the expected display-equation count, preserved math-expression counts except for the documented newly visible code-block equations, unchanged answer slots and list/table/link/image structure, no page errors, and **no new MathJax errors or undefined commands**. Fifty-two pre-existing MathJax errors elsewhere in those fields remain unchanged.

The six reported bad examples and the supplied full-size examples are included in the repair. Before/after screenshots at desktop and mobile widths are retained under [review](review/), including [the definite-integral example](review/17592186319332-after-mobile.png), [the indefinite-integral example](review/17592186582344-after-desktop.png), and [the arithmetic-of-functions tutorial](review/17592186055964-after-mobile.png). Display equations wider than a mobile card use the player's existing horizontal scrolling.

The [pre-existing source exception inventory](preexisting-source-exceptions.json) records **67 malformed, unbalanced legacy math expressions**, none of which contain integrals. Those mathematical-content defects were retained rather than altered by a delimiter/style migration. Intentional compact and structured inline layouts are recorded in [retained-inline.json](retained-inline.json). These retained entries are distinct from unresolved formatting-policy candidates; the final scan has no such candidates.

The [batch manifest](batches.json) identifies every exact payload, field pair and SHA-256. Each `batch-NNN` folder retains its `transaction.edn`, speculative preview and proof, complete stable-key `commit-intent.json`, authorization/submission journal, committed `receipt.edn`, immediate readback and final-T5799 readback. [Preapply verification](preapply-check.json) checked all original values at one fresh basis before submission; each scalar CAS also protected against later concurrent changes. Retry reconciliation uses the original payload, source, endpoint and request key.

The diagnosis and importer reproductions are in the [read-only audit](../../audits/2026-10-23-inline-display/README.md). Capture extraction and generator code were not modified by this database repair. Large immutable input/output snapshots remain under ignored `.local/edb/inline-display-repair-current.*` and `.local/edb/inline-display-repair-after.*`.
