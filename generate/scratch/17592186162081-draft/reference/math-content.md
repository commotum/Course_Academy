# Math content format: course-academy-tex-v1

Capture, stored lesson content, and generators share this format. Its implementation
is `scripts/question_capture/math_format.py`; the player renders it through the
existing Markdown math protection and MathJax configuration.

| Content | Stored form |
| --- | --- |
| Inline math in prose | `$x+1$` |
| Display math in prose | `$$` on its own line, TeX, then `$$` on its own line |
| Math answer (`:answer.type/math`) | Bare TeX, without dollar delimiters; the UI supplies them once |
| Ordinary square-bracket matrix or column vector | `\begin{bmatrix}1 & 3 \\ 2 & 0\end{bmatrix}` |
| Augmented matrix | `\left[\begin{array}{cc|c}1 & 3 & 7 \\ 2 & 0 & 4\end{array}\right]` |
| System with a left brace | `\left\{\begin{aligned}x+3y &=7 \\ 2x &=4\end{aligned}\right.` |
| Equations without a brace | `\begin{aligned}x+3y &=7 \\ 2x &=4\end{aligned}` |

Use `&` between matrix columns and **two literal backslashes** between rows.
JSON serialization escapes those backslashes; deserialize exactly once. Use `&=`
for equation alignment. An annotation belongs in a separate alignment pair (`&&`).
A braced system ends with the invisible delimiter `\right.`. A literal `{` starts
a TeX group; `\{` alone makes a fixed-size glyph and is not the system convention.
Piecewise functions retain `cases` when rows have values and conditions.
Parenthesized matrices and determinants retain `pmatrix` and `vmatrix`.

An augmentation bar is mathematical content. Choose it explicitly from the matrix's
role or source MathML column rules. Never infer it from the lesson title or from
an occurrence of “augmented” elsewhere in a question. A coefficient matrix has no
augmentation bar, even in a worked solution that also shows an augmented matrix.

## Producer integration

Use `matrix_tex(rows, augmented=...)` and `system_tex(equations)` for new content.
Use `normalize_prose` for prose and `normalize_tex` for math answers **before**
calculating content IDs. Decorate a generator's public `generate` function with
`checked_math_content` so invalid or noncanonical content fails before saving.
The capture transaction builder calls `normalize_capture_question` at its save
boundary, after DOM extraction and before transaction construction.

Normalization repairs supported legacy wrappers without guessing missing math.
Validation rejects unpaired dollar delimiters, unbalanced groups/environments,
legacy layout macros, and ragged matrix rows. Unknown images remain image assets;
only recoverable mathematical source is converted to TeX. Keep immutable source
captures for fidelity checks and compare mathematics separately from typography.

Run `python3 -m unittest discover -s scripts/question_capture -p test_math_format.py`.
For lesson migrations, also render the complete affected content with the player's
actual Markdown, sanitization, and MathJax pipeline. A lack of MathJax errors alone
is insufficient: check for exposed delimiters, row counts, scalable braces, and
aligned equals signs.
