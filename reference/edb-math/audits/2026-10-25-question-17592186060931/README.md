# Missing outer determinant equation: 17592186060931

Read-only investigation of tutorial **3012**, “Introduction,” in topic **152**, “The Determinant of a 2x2 Matrix.” Source step **16233** matches the database route. No database content was changed.

After “is denoted det(A) and computed as,” the stored content contains only:

```tex
\begin{aligned}a & b \\ c & d\end{aligned}
```

The archived source contains the full colored equation, semantically:

```tex
\det(A) = \begin{vmatrix}a & b \\ c & d\end{vmatrix} = ad-bc.
```

The introductory matrix and numerical matrix also lost their leading `A =` labels and entry colors. The later numeric evaluation `2·3 − 1·5 = 1` survives because its source formula has an ordinary complete TeX title.

## Reproduced cause

The original HTML at `/home/jake/Developer/MA/DATA/Lessons/152/Source/152.html`, in `#step-16233`, has a legacy SVG whose `<title>` mixes outer TeX text with a nested MathJax rendering of only the matrix. For `MathJax-SVG-4-Title`, its direct text nodes are:

```tex
\text {det} ({A}) = \left|
```

and:

```tex
\right| = {\color{blue}ad} - {\color{red}bc}.
```

Between them, the nested assistive MathML contains only an `mtable` of the four colored entries.

`MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py:532` (`extract_math_from_node`) searches for descendant assistive MathML first, returning it before considering the enclosing SVG title. Applied to this exact source, it extracts **`a|b; c|d`** and drops the surrounding TeX and colors. This faulty value is already present in the saved `152.json` as `[MATH: a|b; c|d]`.

The subsequent Markdown stage, `.../5-MD/md.py:304` (`convert_standalone_matrix_notation`), interprets that bare grid as a `bmatrix`. Running the two archived pipeline functions reproduces the truncated stored import. See `reproduction.json`, which records source hashes and the exact output.

## Retained history

`content-history.edn` confirms that the first retained database assertion at **T35** already lacked the determinant equation. **T126** changed the matrix layout to unfenced `aligned`; **T2155** repaired bracketed matrix environments while leaving this bare grid untouched. **T5766** moved given matrices into display math without restoring the missing content. Thus the missing `det(A)`, determinant bars and `ad-bc` predate those formatting repairs.

The source-aware repair must recover the complete outer formula, not merely change `aligned` into `vmatrix`. The prevention rule is to distinguish complete formula MathML from partial descendant MathML embedded in a mixed SVG title. Preserve or reconstruct the whole expression, including surrounding TeX; unsupported mixed structures must not silently degrade into only the inner fragment. Other formulas using that source shape are candidates for the same class of loss; this investigation does not claim a database-wide count.

The current browser extractors already recognize mixed titles and preserve the whole SVG when they cannot safely reconstruct its TeX. The older upstream JSON extractor above still reproduces the destructive preference for partial MathML. Existing corrupted database rows and derived source Markdown require explicit source-based repair regardless of those newer guards.
