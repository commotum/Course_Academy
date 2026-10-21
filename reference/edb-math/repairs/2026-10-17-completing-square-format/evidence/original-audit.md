# Completing the Square — LaTeX and Markdown audit

Lesson activity: `17592186068977`. Topic: `17592186050372`. Original question: `17592186511718`.

Audit generated: 2026-10-17T23:55:19.563505+00:00. All instructional content was obtained in one read-only EDB query. Snapshot SHA-256: `fecc10ecc81cb0cf847dcf822e2b85038a7e5a487d063346836a7ebc01694066`.

No EDB transactions, content edits, or application changes were made. Audit artifacts are stored only in this temporary folder.

## Coverage

- All 6 lesson steps, in linked presentation order; the route is connected and acyclic.
- Both tutorials, all 4 canonical examples, and all 73 practice questions across the lesson’s four knowledge points.
- All 69 available worked solutions, 102 answer fields, and 264 distinct math answer entities. No answer feedback is stored on these entities.
- The current application Markdown parser, field controls, sanitizer, CSS, and MathJax configuration were used in an isolated browser fixture. No learner task was started and no answers were submitted.
- All 79 content items were rendered at 893 px and 375 px, in both editable and answered display modes: 316 item renders. Desktop editable mode produced 811 math containers.
- No browser exceptions, MathJax errors, or card/prompt horizontal overflow were reported. Source checks found no unmatched math delimiters or unbalanced TeX braces. Every authored field placeholder resolves to a field. All answer entities belong to captured choice collections.
- Representative rendered tutorials, examples, and the original question were visually inspected. This is a formatting audit, not a full independent mathematical or grading audit.

## Findings

### U — Misplaced underbrace: 30 practice worked solutions

Each uses `{{...}}_{⏟}`. MathJax treats the brace glyph as a subscript on the expression, rather than drawing a brace spanning the first three terms. This is a visible defect even though the renderer reports no syntax error. Use `\underbrace{...}` when repairs are authorized. Both canonical examples that teach adding and subtracting a square already use proper underbraces; the general tutorial does too.

### A — Equals signs at the ends of equation rows: 34 content entities

Both tutorials and 32 worked solutions (2 canonical examples and 30 practice questions) contain this layout, across 67 aligned environments. For example:

```latex
\begin{aligned}
x^2+14x+49 & = \\
x^2+2\cdot7x+7^2 & = \\
(x+7)^2 &
\end{aligned}
```

This renders as successive expressions with trailing equals signs and an empty right side on each intermediate row. Some final rows put a period alone in the right column. The content is readable, but the layout is nonstandard and looks like an import artifact. A conventional chain would keep the original expression on the first left side, then use `&= ...` on subsequent rows. This is a layout cleanup, not a TeX parse failure.

### S — Missing separation between prose and the answer equation: 4 prompts

IDs: `17592186069187`, `17592186511861`, `17592186069188`, `17592186069169`.

Three have `constant.$(` with no separating space or paragraph break. The fourth has adjacent `$...$.$...$` runs. Put the response equation in a separate paragraph for consistent presentation.

### W — Prompt wording disagrees with its scaffold: 1 question

Question `17592186532655` asks for “the sum of a perfect square and a constant,” but the scaffold explicitly uses a minus sign and the solution gives `(x-2)^2-10`. “Difference” would match its current scaffold. This is a wording inconsistency rather than malformed LaTeX.

### Optional source normalization

- **P:** 16 question prompts put the question mark inside math, e.g. `$q?$`. They render, but `$q$?` keeps sentence punctuation in prose. Other inline commas and periods also occur inside math and can be normalized consistently; display-equation punctuation is not automatically an error.
- **B:** 138 attributes on 112 entities use brace-grouped closing parentheses, such as `(x+p{)}^{2}`. This is valid TeX and renders correctly; `(x+p)^2` is clearer source. This includes answer values as well as prompts and solutions.

### M — Existing missing material, outside formatting repairs

8 practice questions have no worked solution and also lack correct-answer links: 11 unkeyed fields total. These are existing content gaps, not rendering failures. Their existing prompts and choices were still included in the formatting checks.

## Lesson route

| Step | Step entity | Content entity | Content |
| --- | --- | --- | --- |
| 1 | `17592186069834` | `17592186069995` | Introduction |
| 2 | `17592186069835` | `17592186068873` | Completing the Square When the Perfect Square is Isolated |
| 3 | `17592186069836` | `17592186068874` | Completing the Square When the Perfect Square is Isolated: Negative Linear Term |
| 4 | `17592186069837` | `17592186069946` | Completing the Square |
| 5 | `17592186069838` | `17592186068875` | Completing the Square on a Quadratic Expression |
| 6 | `17592186069839` | `17592186068876` | Completing the Square on a Quadratic Expression with a Negative Linear Term |

## Exact affected attributes

### U

| Entity | Attribute |
| --- | --- |
| `17592186069186` | `:question/worked-solution` |
| `17592186272296` | `:question/worked-solution` |
| `17592186272299` | `:question/worked-solution` |
| `17592186290593` | `:question/worked-solution` |
| `17592186290594` | `:question/worked-solution` |
| `17592186292540` | `:question/worked-solution` |
| `17592186323842` | `:question/worked-solution` |
| `17592186400930` | `:question/worked-solution` |
| `17592186511786` | `:question/worked-solution` |
| `17592186511794` | `:question/worked-solution` |
| `17592186511815` | `:question/worked-solution` |
| `17592186532698` | `:question/worked-solution` |
| `17592186233459` | `:question/worked-solution` |
| `17592186272303` | `:question/worked-solution` |
| `17592186272304` | `:question/worked-solution` |
| `17592186290595` | `:question/worked-solution` |
| `17592186290596` | `:question/worked-solution` |
| `17592186290597` | `:question/worked-solution` |
| `17592186323839` | `:question/worked-solution` |
| `17592186400937` | `:question/worked-solution` |
| `17592186511718` | `:question/worked-solution` |
| `17592186511729` | `:question/worked-solution` |
| `17592186511732` | `:question/worked-solution` |
| `17592186511741` | `:question/worked-solution` |
| `17592186511744` | `:question/worked-solution` |
| `17592186511753` | `:question/worked-solution` |
| `17592186511762` | `:question/worked-solution` |
| `17592186511769` | `:question/worked-solution` |
| `17592186532669` | `:question/worked-solution` |
| `17592186532681` | `:question/worked-solution` |

### A

| Entity | Attribute |
| --- | --- |
| `17592186068672` | `:question/worked-solution` |
| `17592186272292` | `:question/worked-solution` |
| `17592186290587` | `:question/worked-solution` |
| `17592186290588` | `:question/worked-solution` |
| `17592186290589` | `:question/worked-solution` |
| `17592186290590` | `:question/worked-solution` |
| `17592186511833` | `:question/worked-solution` |
| `17592186511842` | `:question/worked-solution` |
| `17592186511846` | `:question/worked-solution` |
| `17592186511848` | `:question/worked-solution` |
| `17592186511861` | `:question/worked-solution` |
| `17592186511863` | `:question/worked-solution` |
| `17592186511864` | `:question/worked-solution` |
| `17592186511868` | `:question/worked-solution` |
| `17592186511879` | `:question/worked-solution` |
| `17592186511880` | `:question/worked-solution` |
| `17592186532662` | `:question/worked-solution` |
| `17592186532699` | `:question/worked-solution` |
| `17592186068677` | `:question/worked-solution` |
| `17592186272042` | `:question/worked-solution` |
| `17592186272043` | `:question/worked-solution` |
| `17592186272044` | `:question/worked-solution` |
| `17592186272045` | `:question/worked-solution` |
| `17592186290463` | `:question/worked-solution` |
| `17592186290592` | `:question/worked-solution` |
| `17592186511892` | `:question/worked-solution` |
| `17592186511898` | `:question/worked-solution` |
| `17592186511901` | `:question/worked-solution` |
| `17592186511908` | `:question/worked-solution` |
| `17592186532655` | `:question/worked-solution` |
| `17592186532680` | `:question/worked-solution` |
| `17592186549954` | `:question/worked-solution` |
| `17592186069995` | `:tutorial/content` |
| `17592186069946` | `:tutorial/content` |

### S

| Entity | Attribute |
| --- | --- |
| `17592186069187` | `:question/problem` |
| `17592186511861` | `:question/problem` |
| `17592186069188` | `:question/problem` |
| `17592186069169` | `:question/problem` |

### W

| Entity | Attribute |
| --- | --- |
| `17592186532655` | `:question/problem` |

### P

| Entity | Attribute |
| --- | --- |
| `17592186069186` | `:question/problem` |
| `17592186292540` | `:question/problem` |
| `17592186400930` | `:question/problem` |
| `17592186511786` | `:question/problem` |
| `17592186511794` | `:question/problem` |
| `17592186511815` | `:question/problem` |
| `17592186290597` | `:question/problem` |
| `17592186323839` | `:question/problem` |
| `17592186400937` | `:question/problem` |
| `17592186511718` | `:question/problem` |
| `17592186511729` | `:question/problem` |
| `17592186511732` | `:question/problem` |
| `17592186511744` | `:question/problem` |
| `17592186511753` | `:question/problem` |
| `17592186511762` | `:question/problem` |
| `17592186511769` | `:question/problem` |

### M

| Entity | Attribute |
| --- | --- |
| `17592186069049` | `:question/worked-solution` |
| `17592186069051` | `:question/worked-solution` |
| `17592186069187` | `:question/worked-solution` |
| `17592186069052` | `:question/worked-solution` |
| `17592186069188` | `:question/worked-solution` |
| `17592186069050` | `:question/worked-solution` |
| `17592186069169` | `:question/worked-solution` |
| `17592186069189` | `:question/worked-solution` |

## Per-item coverage

Flags: U = misplaced underbrace; A = trailing equals alignment; S = missing prose/equation separation; W = scaffold wording; P = question mark inside inline math; B = valid but awkward parenthesis grouping; M = missing solution and answer key. A dash means none of these source patterns was found; it does not claim a complete mathematical audit. Every item passed the browser rendering checks described above.

| Entity | Role | Flags |
| --- | --- | --- |
| `17592186068672` | Canonical example | A |
| `17592186069049` | Practice question | M |
| `17592186069051` | Practice question | M |
| `17592186069187` | Practice question | S, M |
| `17592186272292` | Practice question | A, B |
| `17592186290587` | Practice question | A, B |
| `17592186290588` | Practice question | A, B |
| `17592186290589` | Practice question | A, B |
| `17592186290590` | Practice question | A, B |
| `17592186511833` | Practice question | A, B |
| `17592186511842` | Practice question | A, B |
| `17592186511846` | Practice question | A, B |
| `17592186511848` | Practice question | A, B |
| `17592186511861` | Practice question | A, S, B |
| `17592186511863` | Practice question | A, B |
| `17592186511864` | Practice question | A, B |
| `17592186511868` | Practice question | A, B |
| `17592186511879` | Practice question | A, B |
| `17592186511880` | Practice question | A, B |
| `17592186532662` | Practice question | A |
| `17592186532699` | Practice question | A |
| `17592186068677` | Canonical example | A |
| `17592186069052` | Practice question | M |
| `17592186069188` | Practice question | S, M |
| `17592186272042` | Practice question | A, B |
| `17592186272043` | Practice question | A, B |
| `17592186272044` | Practice question | A, B |
| `17592186272045` | Practice question | A |
| `17592186290463` | Practice question | A, B |
| `17592186290592` | Practice question | A, B |
| `17592186511892` | Practice question | A, B |
| `17592186511898` | Practice question | A, B |
| `17592186511901` | Practice question | A, B |
| `17592186511908` | Practice question | A, B |
| `17592186532655` | Practice question | A, W |
| `17592186532680` | Practice question | A |
| `17592186549954` | Practice question | A |
| `17592186068429` | Canonical example | — |
| `17592186069050` | Practice question | M |
| `17592186069186` | Practice question | U, P |
| `17592186272296` | Practice question | U |
| `17592186272299` | Practice question | U, B |
| `17592186290593` | Practice question | U, B |
| `17592186290594` | Practice question | U, B |
| `17592186292540` | Practice question | U, P, B |
| `17592186323842` | Practice question | U, B |
| `17592186400930` | Practice question | U, P, B |
| `17592186511786` | Practice question | U, P, B |
| `17592186511792` | Practice question | — |
| `17592186511794` | Practice question | U, P, B |
| `17592186511802` | Practice question | — |
| `17592186511812` | Practice question | — |
| `17592186511813` | Practice question | — |
| `17592186511815` | Practice question | U, P, B |
| `17592186511819` | Practice question | — |
| `17592186532698` | Practice question | U |
| `17592186068430` | Canonical example | — |
| `17592186069169` | Practice question | S, M |
| `17592186069189` | Practice question | M |
| `17592186233459` | Practice question | U |
| `17592186272303` | Practice question | U, B |
| `17592186272304` | Practice question | U, B |
| `17592186290595` | Practice question | U, B |
| `17592186290596` | Practice question | U, B |
| `17592186290597` | Practice question | U, P, B |
| `17592186323839` | Practice question | U, P, B |
| `17592186400937` | Practice question | U, P |
| `17592186511718` | Practice question | U, P, B |
| `17592186511729` | Practice question | U, P, B |
| `17592186511732` | Practice question | U, P, B |
| `17592186511741` | Practice question | U, B |
| `17592186511744` | Practice question | U, P, B |
| `17592186511753` | Practice question | U, P, B |
| `17592186511762` | Practice question | U, P, B |
| `17592186511769` | Practice question | U, P, B |
| `17592186532669` | Practice question | U |
| `17592186532681` | Practice question | U |
| `17592186069995` | Tutorial: Introduction | A |
| `17592186069946` | Tutorial: Completing the Square | A |

## Supporting artifacts

- [Live lesson snapshot](lesson.edn)
- [Parsed snapshot](lesson.json)
- [Browser measurements](browser-report.json)
- [Representative rendered content](representative-render.png)
- [Question and worked-solution text](all-questions.txt)
