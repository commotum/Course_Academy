# Other Completing the Square lessons: LaTeX and Markdown audit

Database: `math`. Lineage: `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Snapshot: **basis 3529**.

No EDB transactions or content changes were made. This audit covers the ten other topic titles containing “Completing the Square”; it excludes the base lesson already repaired at basis 3520.

## Coverage

- 10 lesson activities; all 43 linked lesson steps; 31 knowledge points.
- All 12 tutorials, 31 canonical examples, 275 practice questions, and 273 available worked solutions.
- All 315 answer fields and 1,262 distinct answer values (1,009 math and 253 text). No answer feedback is stored on these entries.
- All lesson routes are connected and acyclic. No unmatched math delimiters, unbalanced TeX braces/environments, orphan field placeholders, raw rendered answer placeholders, or unexpected Markdown code blocks were found.
- The browser rendered all 318 items at desktop (893 px) and mobile (375 px) widths, in editable and answered states: 1,272 item renders and 4,250 math containers in desktop editable mode.
- No browser exceptions, MathJax error nodes, or outer card/prompt horizontal overflow were reported. Those checks do not detect the visible legacy-command and notation defects below. Long mathematical lines can still require internal scrolling.
- Source and geometry checks covered every item. Representative anomalies were visually inspected; the screenshots omit image elements. All three referenced diagram assets resolve in the local image library. This is a formatting audit with two incidental algebra findings, not a complete independent answer-key or mathematical audit.

## Findings by lesson

| Lesson | Practice questions | Findings | Missing solutions | Questions missing keys |
| --- | ---: | --- | ---: | ---: |
| Integrating Functions by Completing the Square | 41 | 2 examples with visible row-spacing commands; 3 attributes with unformatted function names; 2 confirmed sign typos | 6 | 6 |
| Determining Circle Properties by Completing the Square | 31 | broken bold in tutorial | 1 | 2 |
| Calculating the Vertex of a Parabola by Completing the Square | 13 | No substantive formatting defect identified in these checks | 3 | 3 |
| Integration Using Inverse Reciprocal Hyperbolic Functions and Completing the Square | 25 | 2 examples with visible row-spacing commands | 0 | 0 |
| Solving Quadratic Equations by Completing the Square | 27 | No substantive formatting defect identified in these checks | 1 | 3 |
| Finding the Center and Axes of Ellipses by Completing the Square | 19 | No substantive formatting defect identified in these checks | 4 | 4 |
| Integration Using Hyperbolic Functions and Completing the Square | 8 | 35 attributes with unformatted function names | 8 | 8 |
| Completing the Square With Odd Linear Terms | 21 | 10 misplaced-underbrace solutions; 8 content items with trailing equals signs; 3 prompts missing prose/equation separation | 6 | 6 |
| Solving Quadratic Equations With Leading Coefficients by Completing the Square | 36 | No substantive formatting defect identified in these checks | 3 | 3 |
| Completing the Square With Leading Coefficients | 54 | 53 misplaced-underbrace solutions | 1 | 1 |

## Confirmed formatting defects

### Misplaced underbraces: 63 practice solutions

10 are in **Completing the Square With Odd Linear Terms**, and 53 are in **Completing the Square With Leading Coefficients**. They store `..._{⏟}` where a spanning `\underbrace{...}` is intended. Canonical examples in these lessons already use proper underbraces.

### Broken legacy equation rows: four canonical examples, five display blocks

Examples `17592186068504`, `17592186068506`, `17592186166644`, and `17592186166647` use legacy `\eqalign{...}` blocks containing single-backslash `\[3pt]` or `\[5pt]` row separators. These visibly render the commands instead of producing line breaks; entire derivations run across one row. Example `17592186068506` has two affected blocks. Replace the affected environments with standard `aligned` and proper `\\` row breaks during a repair.

The visible failure was confirmed in [two ordinary integration examples](sample-0.png) and [two inverse reciprocal hyperbolic integration examples](sample-1.png). These are real display failures even though MathJax reports no error nodes.

### Trailing equals alignment: eight content entities

Both odd-linear-term tutorials, one canonical example, and five practice solutions use the same end-of-row equals-sign layout as the base lesson did. There are 15 aligned environments across those eight entities, including one harmless single-row wrapper; 14 environments contain the trailing-equals pattern. [Rendered tutorials](sample-2.png) show the result. Use conventional equation chains with the equals signs before each new expression.

### Unformatted named functions: 38 attributes

43 occurrences across 38 attributes use bare `arsinh`, `arcosh`, `artanh`, `arcsin`, or `arctan` in math. They render as products of italic letters, rather than named operators. The affected attributes comprise one tutorial, six worked solutions, and 31 answer values. Standard TeX commands or `\operatorname{...}` would express the intended notation. This is visible in the [hyperbolic integration tutorial](sample-3.png), which also retains awkward slash-form fractions such as `\int(1)/(...)dx`.

### Broken Markdown emphasis: one tutorial

Circle tutorial `17592186079635` contains `**Step 1. **Group...`; the space before the closing marker prevents bold formatting and leaves raw asterisks visible. It should read `**Step 1.** Group...`. See the [rendered circle tutorial](sample-3.png).

### Missing prose/equation separation: three prompts

Questions `17592186184553`, `17592186184554`, and `17592186184555` run the instructions directly into the answer equation. All three belong to the odd-linear-term lesson. A paragraph break before the equation would match the other prompts.

## Two confirmed sign typos encountered during review

These go beyond formatting and should be reviewed as mathematical content repairs:

- **`17592186287952`**, `:question/worked-solution`: A completing-square line changes the sign of the linear term from -6x to +6x before returning to the correct (x-3)^2+1.
- **`17592186292695`**, `:question/worked-solution`: In the final displayed integral chain, the original radical 1-2x-x^2 becomes 1+2x-x^2 in its first integrand.

Both are in **Integrating Functions by Completing the Square**. The polynomial differences between the incorrect and intended expressions are respectively `12*x` and `4*x`, confirmed with exact symbolic algebra. The surrounding steps return to the intended expression; these findings do not independently establish that every final answer is correct.

## Existing content gaps and optional cleanup

- **33 practice questions lack worked solutions.** All 31 canonical examples have worked solutions.
- **36 practice questions have missing correct-answer links, affecting 39 fields.** These include all 33 questions without solutions and three additional questions. In the hyperbolic integration lesson, all eight existing practice questions lack both solutions and keys.
- 28 attributes retain valid but awkward grouping such as `(x+1{)}^2`; this is optional source normalization, not a rendering failure.
- Inline sentence punctuation inside math also remains a style cleanup. Display-equation punctuation is not automatically an error.
- All 21 flagged Markdown tables are genuine x-to-u limit-conversion tables with consistent columns; they are not malformed fraction captures.

## Exact affected entities and attributes

### Misplaced underbrace

| Entity | Attribute | Detail |
| --- | --- | --- |
| `17592186272293` | `:question/worked-solution` |  |
| `17592186272294` | `:question/worked-solution` |  |
| `17592186272295` | `:question/worked-solution` |  |
| `17592186272297` | `:question/worked-solution` |  |
| `17592186272298` | `:question/worked-solution` |  |
| `17592186272049` | `:question/worked-solution` |  |
| `17592186272050` | `:question/worked-solution` |  |
| `17592186272300` | `:question/worked-solution` |  |
| `17592186290408` | `:question/worked-solution` |  |
| `17592186290409` | `:question/worked-solution` |  |
| `17592186184448` | `:question/worked-solution` |  |
| `17592186272052` | `:question/worked-solution` |  |
| `17592186272054` | `:question/worked-solution` |  |
| `17592186290355` | `:question/worked-solution` |  |
| `17592186290356` | `:question/worked-solution` |  |
| `17592186501168` | `:question/worked-solution` |  |
| `17592186501188` | `:question/worked-solution` |  |
| `17592186501230` | `:question/worked-solution` |  |
| `17592186566242` | `:question/worked-solution` |  |
| `17592186566260` | `:question/worked-solution` |  |
| `17592186566268` | `:question/worked-solution` |  |
| `17592186184484` | `:question/worked-solution` |  |
| `17592186184806` | `:question/worked-solution` |  |
| `17592186272127` | `:question/worked-solution` |  |
| `17592186272128` | `:question/worked-solution` |  |
| `17592186290359` | `:question/worked-solution` |  |
| `17592186320740` | `:question/worked-solution` |  |
| `17592186501138` | `:question/worked-solution` |  |
| `17592186501166` | `:question/worked-solution` |  |
| `17592186501218` | `:question/worked-solution` |  |
| `17592186501243` | `:question/worked-solution` |  |
| `17592186521467` | `:question/worked-solution` |  |
| `17592186521557` | `:question/worked-solution` |  |
| `17592186566243` | `:question/worked-solution` |  |
| `17592186566264` | `:question/worked-solution` |  |
| `17592186184483` | `:question/worked-solution` |  |
| `17592186184485` | `:question/worked-solution` |  |
| `17592186272058` | `:question/worked-solution` |  |
| `17592186272059` | `:question/worked-solution` |  |
| `17592186272060` | `:question/worked-solution` |  |
| `17592186272061` | `:question/worked-solution` |  |
| `17592186272062` | `:question/worked-solution` |  |
| `17592186272081` | `:question/worked-solution` |  |
| `17592186272329` | `:question/worked-solution` |  |
| `17592186501163` | `:question/worked-solution` |  |
| `17592186501206` | `:question/worked-solution` |  |
| `17592186501236` | `:question/worked-solution` |  |
| `17592186521522` | `:question/worked-solution` |  |
| `17592186521565` | `:question/worked-solution` |  |
| `17592186566227` | `:question/worked-solution` |  |
| `17592186184804` | `:question/worked-solution` |  |
| `17592186184805` | `:question/worked-solution` |  |
| `17592186272070` | `:question/worked-solution` |  |
| `17592186272124` | `:question/worked-solution` |  |
| `17592186290358` | `:question/worked-solution` |  |
| `17592186320743` | `:question/worked-solution` |  |
| `17592186332891` | `:question/worked-solution` |  |
| `17592186332892` | `:question/worked-solution` |  |
| `17592186332893` | `:question/worked-solution` |  |
| `17592186501192` | `:question/worked-solution` |  |
| `17592186566232` | `:question/worked-solution` |  |
| `17592186566240` | `:question/worked-solution` |  |
| `17592186566256` | `:question/worked-solution` |  |

### Trailing equals alignment

| Entity | Attribute | Detail |
| --- | --- | --- |
| `17592186183961` | `:question/worked-solution` |  |
| `17592186272046` | `:question/worked-solution` |  |
| `17592186290376` | `:question/worked-solution` |  |
| `17592186290405` | `:question/worked-solution` |  |
| `17592186290406` | `:question/worked-solution` |  |
| `17592186290407` | `:question/worked-solution` |  |
| `17592186185383` | `:tutorial/content` |  |
| `17592186185384` | `:tutorial/content` |  |

### Legacy equation rows

| Entity | Attribute | Detail |
| --- | --- | --- |
| `17592186068504` | `:question/worked-solution` |  |
| `17592186068506` | `:question/worked-solution` |  |
| `17592186166644` | `:question/worked-solution` |  |
| `17592186166647` | `:question/worked-solution` |  |

### Missing prompt separation

| Entity | Attribute | Detail |
| --- | --- | --- |
| `17592186184553` | `:question/problem` |  |
| `17592186184554` | `:question/problem` |  |
| `17592186184555` | `:question/problem` |  |

### Missing worked solutions

| Entity | Attribute | Detail |
| --- | --- | --- |
| `17592186069377` | `:question/worked-solution` |  |
| `17592186069381` | `:question/worked-solution` |  |
| `17592186069400` | `:question/worked-solution` |  |
| `17592186069281` | `:question/worked-solution` |  |
| `17592186069172` | `:question/worked-solution` |  |
| `17592186069283` | `:question/worked-solution` |  |
| `17592186079065` | `:question/worked-solution` |  |
| `17592186172271` | `:question/worked-solution` |  |
| `17592186172272` | `:question/worked-solution` |  |
| `17592186172273` | `:question/worked-solution` |  |
| `17592186069059` | `:question/worked-solution` |  |
| `17592186088331` | `:question/worked-solution` |  |
| `17592186088332` | `:question/worked-solution` |  |
| `17592186088042` | `:question/worked-solution` |  |
| `17592186088043` | `:question/worked-solution` |  |
| `17592186167372` | `:question/worked-solution` |  |
| `17592186167447` | `:question/worked-solution` |  |
| `17592186167374` | `:question/worked-solution` |  |
| `17592186167449` | `:question/worked-solution` |  |
| `17592186167375` | `:question/worked-solution` |  |
| `17592186167376` | `:question/worked-solution` |  |
| `17592186167371` | `:question/worked-solution` |  |
| `17592186167373` | `:question/worked-solution` |  |
| `17592186184478` | `:question/worked-solution` |  |
| `17592186184553` | `:question/worked-solution` |  |
| `17592186184457` | `:question/worked-solution` |  |
| `17592186184554` | `:question/worked-solution` |  |
| `17592186184555` | `:question/worked-solution` |  |
| `17592186184800` | `:question/worked-solution` |  |
| `17592186184816` | `:question/worked-solution` |  |
| `17592186184502` | `:question/worked-solution` |  |
| `17592186184750` | `:question/worked-solution` |  |
| `17592186184482` | `:question/worked-solution` |  |

### Missing correct-answer links

| Entity | Attribute | Detail |
| --- | --- | --- |
| `17592186069377` | `:question/answer-fields` | 17592186067432 |
| `17592186069381` | `:question/answer-fields` | 17592186067456 |
| `17592186069400` | `:question/answer-fields` | 17592186067570 |
| `17592186069281` | `:question/answer-fields` | 17592186066856 |
| `17592186069172` | `:question/answer-fields` | 17592186066261 |
| `17592186069283` | `:question/answer-fields` | 17592186066868 |
| `17592186079061` | `:question/answer-fields` | 17592186077144 |
| `17592186079065` | `:question/answer-fields` | 17592186077168 |
| `17592186172271` | `:question/answer-fields` | 17592186168489 |
| `17592186172272` | `:question/answer-fields` | 17592186168495 |
| `17592186172273` | `:question/answer-fields` | 17592186168501 |
| `17592186069059` | `:question/answer-fields` | 17592186065787 |
| `17592186069217` | `:question/answer-fields` | 17592186066484 |
| `17592186069268` | `:question/answer-fields` | 17592186066778 |
| `17592186088331` | `:question/answer-fields` | 17592186086640 |
| `17592186088332` | `:question/answer-fields` | 17592186086646 |
| `17592186088042` | `:question/answer-fields` | 17592186084986 |
| `17592186088043` | `:question/answer-fields` | 17592186084992 |
| `17592186167372` | `:question/answer-fields` | 17592186165440 |
| `17592186167447` | `:question/answer-fields` | 17592186165890 |
| `17592186167374` | `:question/answer-fields` | 17592186165452 |
| `17592186167449` | `:question/answer-fields` | 17592186165902 |
| `17592186167375` | `:question/answer-fields` | 17592186165458 |
| `17592186167376` | `:question/answer-fields` | 17592186165464 |
| `17592186167371` | `:question/answer-fields` | 17592186165434 |
| `17592186167373` | `:question/answer-fields` | 17592186165446 |
| `17592186184478` | `:question/answer-fields` | 17592186181045 |
| `17592186184553` | `:question/answer-fields` | 17592186181476, 17592186181477 |
| `17592186184457` | `:question/answer-fields` | 17592186180919 |
| `17592186184554` | `:question/answer-fields` | 17592186181478, 17592186181479 |
| `17592186184555` | `:question/answer-fields` | 17592186181480, 17592186181481 |
| `17592186184800` | `:question/answer-fields` | 17592186183409 |
| `17592186184816` | `:question/answer-fields` | 17592186183505 |
| `17592186184502` | `:question/answer-fields` | 17592186181188 |
| `17592186184750` | `:question/answer-fields` | 17592186183109 |
| `17592186184482` | `:question/answer-fields` | 17592186181069 |

### Unformatted function names

| Entity | Attribute | Names |
| --- | --- | --- |
| `17592186165435` | `:answer/value` | arcosh |
| `17592186165436` | `:answer/value` | arsinh |
| `17592186165437` | `:answer/value` | arsinh |
| `17592186165438` | `:answer/value` | arsinh |
| `17592186165439` | `:answer/value` | arcosh |
| `17592186165447` | `:answer/value` | arcosh |
| `17592186165448` | `:answer/value` | arcosh |
| `17592186165449` | `:answer/value` | arcosh |
| `17592186165450` | `:answer/value` | arsinh |
| `17592186165451` | `:answer/value` | arsinh |
| `17592186165455` | `:answer/value` | arcosh |
| `17592186165459` | `:answer/value` | artanh |
| `17592186165460` | `:answer/value` | artanh |
| `17592186165461` | `:answer/value` | artanh |
| `17592186165462` | `:answer/value` | artanh |
| `17592186165463` | `:answer/value` | artanh |
| `17592186165465` | `:answer/value` | artanh |
| `17592186165466` | `:answer/value` | artanh |
| `17592186165467` | `:answer/value` | artanh |
| `17592186165468` | `:answer/value` | artanh |
| `17592186165469` | `:answer/value` | artanh |
| `17592186165891` | `:answer/value` | arcosh |
| `17592186165892` | `:answer/value` | arsinh |
| `17592186165893` | `:answer/value` | arsinh |
| `17592186165894` | `:answer/value` | arcosh |
| `17592186165895` | `:answer/value` | arsinh |
| `17592186165903` | `:answer/value` | arcosh |
| `17592186165904` | `:answer/value` | arcosh |
| `17592186165905` | `:answer/value` | arcosh |
| `17592186165906` | `:answer/value` | arcosh |
| `17592186165907` | `:answer/value` | arcosh |
| `17592186166618` | `:question/worked-solution` | arsinh |
| `17592186166620` | `:question/worked-solution` | artanh |
| `17592186166621` | `:question/worked-solution` | arcosh |
| `17592186168098` | `:tutorial/content` | arsinh |
| `17592186319250` | `:question/worked-solution` | arcsin |
| `17592186319261` | `:question/worked-solution` | arcsin |
| `17592186319267` | `:question/worked-solution` | arctan |

## Lesson identities and route coverage

| Topic | Lesson activity | Title | Steps | Tutorials | Examples | Practice |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `17592186048167` | `17592186068972` | Integrating Functions by Completing the Square | 5 | 1 | 4 | 41 |
| `17592186048436` | `17592186078682` | Determining Circle Properties by Completing the Square | 3 | 1 | 2 | 31 |
| `17592186048551` | `17592186172206` | Calculating the Vertex of a Parabola by Completing the Square | 3 | 1 | 2 | 13 |
| `17592186049052` | `17592186167030` | Integration Using Inverse Reciprocal Hyperbolic Functions and Completing the Square | 5 | 1 | 4 | 25 |
| `17592186049250` | `17592186068953` | Solving Quadratic Equations by Completing the Square | 4 | 1 | 3 | 27 |
| `17592186049761` | `17592186087923` | Finding the Center and Axes of Ellipses by Completing the Square | 3 | 1 | 2 | 19 |
| `17592186049966` | `17592186167029` | Integration Using Hyperbolic Functions and Completing the Square | 5 | 1 | 4 | 8 |
| `17592186050044` | `17592186184426` | Completing the Square With Odd Linear Terms | 5 | 2 | 3 | 21 |
| `17592186050222` | `17592186184433` | Solving Quadratic Equations With Leading Coefficients by Completing the Square | 5 | 2 | 3 | 36 |
| `17592186051078` | `17592186184409` | Completing the Square With Leading Coefficients | 5 | 1 | 4 | 54 |

## Supporting evidence

- [Database snapshot](lessons.edn) and [read-only query](lessons-query.edn).
- [Inventory and routes](inventory.json), [source findings](source-findings.json), and [additional notation findings](additional-source-review.json).
- [Full tutorial/example/question source](source-review.txt).
- [Browser summary](browser-summary.json), [measurements](browser-report.json), and [visual probes](visual-probes.json).
- [Image asset resolution](images.json) and [confirmed sign typos](confirmed-sign-typos.json).
