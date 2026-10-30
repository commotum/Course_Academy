# LaTeX quality audit: The Vector Equation of a Line

Read-only audit of topic **17592186049485**, Math Academy1376, at **basis11863**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. No EDB writes or application source changes.

Strict actual-player MathJax checks pass **367/367 fields**, with zero undefined commands, leaked display delimiters or matrix-layout failures. This does **not** mean the notation is correct: one segment expression is visibly corrupted, and source vector fonts were lost.

## Findings

1. **Malformed segment notation (medium):** question **17592186106065**, MA `q-162143`, `question/problem`, stores `$PQ^(―)$`. It visibly produces superscript parentheses/bar over the Q rather than a segment bar spanning PQ. Use `$\overline{PQ}$`. Compare [actual rendering](visual/broken-segment.png) and [original screenshot](source-evidence/14-question-162143.png).

2. **Lost vector boldface (medium):** **32 fields directly confirmed against original source**; **217 fields across182 entities** share the same pattern and are repair candidates. The footprint is125 answer values,54 solutions,36 problems and2 tutorial bodies. Original MathML explicitly contains `mathvariant="bold"`; stored equations use italic `r,p,v` or `i,j,k`. Scalar `t` remains correctly italic. For example, tutorial **17592186107157** retains bold vector names in prose but displays plain `r=p+tv`; canonical segment solution **17592186105466** switches between bold basis vectors and scalar-looking `i,j,k`. Plain letters could be a valid consistent convention, but the source-to-stored comparison and mixed treatment here establish a lost convention. Restore vector fonts from the source, preserving scalar coefficients `a,b,c,t`. [Exact source-confirmed fields and broader candidates](vector-formatting-evidence.json), [source introduction](source-evidence/01-step-44724.png), [actual introduction](visual/introduction.png), [mixed segment notation](visual/canonical-segment.png).

   The loss already appears in the original extracted lesson JSON/Markdown while retained source MathML has bold metadata. The current secondary converter has explicit bold support; no particular historical conversion stage was proven responsible.

3. **Missing answer key and solution (high, completeness issue):** the same question **17592186106065** has no `answer-field/correct` on field **17592186102276** and no `question/worked-solution`. Its existing choice **17592186102278**, value **2**, is correct: `a=4`, `b=-3`, `c=1`, so `a+b+c=2`. All other50 practice questions have correct links, and all other54 questions have solutions. This affects assessability even though the five choices render normally.

4. **Principal-square-root notation (low, inherited from source):** all13 fixed-distance solutions use a step such as `\sqrt{18t^2}` followed by `\pm3t\sqrt2`. The rigorous simplification is `3\sqrt2\,|t|`, then `|t|=2`, then `t=\pm2`. Final coordinates and keys are correct. The original canonical screenshot contains exactly the same step, so this is a source-inherited rigor issue, not import corruption. [Original canonical derivation](source-evidence/09-step-44732.png), [actual derivation](visual/arrows-and-norm.png); exact13 IDs are in [findings.json](findings.json).

## Coverage and checks

| Knowledge point | Entity | Practice | Canonical |
|---|---:|---:|---:|
| Point and direction vector |17592186105896|10|17592186105463|
| Two given points |17592186105897|15|17592186105464|
| Points a fixed distance away |17592186105898|12|17592186105465|
| Line segment |17592186105899|14|17592186105466|

The55 unique questions,3 tutorials,4 scoped activities and20 steps were extracted through explicit bounded Pull patterns with unbounded cardinality-many selectors. Titles were included in the inventory; none contains math. All51 practice questions are radio questions with5 choices each:255 authored answer values, no learner-entered response entities. There are no linked retired questions, generated questions, generator registrations or answer-feedback fields at this basis.

All367 existing instructional fields were strictly rendered:55 problems,54 solutions,255 answer values and3 tutorial bodies. Every equation and choice source string was reviewed for symbols, vector/scalar roles, arrow/hat conventions, grouping, missing terms, endpoint arithmetic, interval bounds, and matrix/fence layout. No malformed repaired `\overset{\to -}` arrows remain.308 matrix/fence geometry measurements were retained by the renderer. Arrow forms currently render as arrows; the fixed-length `\overset{―}{PQ}` notation elsewhere is readable but would benefit from normalization to `\overline{PQ}` when repairing segment notation.

An independent numerical geometry check validates all185 choices in the first37 practice questions: line membership, parallel directions and fixed-distance endpoints each identify exactly the stored key. The14 segment questions and4 canonical examples were manually checked; their arithmetic and bounds are correct apart from the missing key/solution above. See [semantic checks](semantic-choice-checks.json).

## Evidence and limitations

- [Pinned snapshot](snapshot.json), saved EDN queries/results, [all-string field inventory](field-inventory.json), [render input](render-input.json), and [strict render results](render-verification.json).
- Seven representative actual-player screenshot groups were visually inspected in [visual](visual/manifest.json): introduction, canonical arrows/norm, canonical segment, malformed segment, segment basis-vector solution, segment tutorial and matrix line solution. Every field was rendered automatically; every field was not individually screenshotted.
- The original lesson HTML/screenshots cover tutorials,4 canonical examples and8 initial practice questions. Source MathML snippets and4 original screenshots are retained in `source-evidence/`. The other captured questions were reviewed in EDB source strings and geometrically checked; their historical capture HTML was not individually compared.
- **32** is the source-confirmed font-loss count; **217** is the broader candidate footprint, not217 individually source-verified cases. No source or database repair was performed.
