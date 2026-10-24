# Table fidelity audit — 17592186068570

Read-only audit of `math` at **T6707**. Entity **17592186068570** is canonical example **e-467**, “Integrating Quotients Containing Trigonometric Functions Using Substitution,” in topic **478**, “Integrating Trigonometric Functions Using Substitution.” No database or UI changes were made.

**The table's mathematical contents are correct, but the import did not preserve its original presentation or header roles.**

The source is `/home/jake/Developer/MA/DATA/Lessons/478/Source/478.html`, example `#step-617140`. Its HTML table is centered, has a full grid and centered cells, and shades the first column light blue to identify the row labels `x` and `u`. All six source cells are ordinary `td` elements, not a column-header row. Cell contents are:

| Row label | Lower bound | Upper bound |
| --- | --- | --- |
| x | 0 | π/4 |
| u | 1 | 2 |

The stored Markdown retains the correct two-by-three cell layout and contents. However, it loses the source's centered position, centered body cells and shaded row-label column. Markdown's mandatory first-row header separator promotes `x, 0, π/4` to `th` cells, while `u, 1, 2` remain `td`. The current app renders the table at the left of the solution with centered header cells, left-aligned body cells and no shaded label column. The grid remains visible; no row, column or mathematical value is missing.

## Where the degradation occurred

1. The archived normalized JSON `478/Source/478.json` already strips the original table/cell attributes, retaining plain `table/tr/td` elements and normalized math markers. Its example record is retained in [source-example.json](source-example.json).
2. The vault lesson `478/478.md:384` converts the first row into Markdown headers and retains only right alignment on the numeric columns (`---:`, `---:`). It already lacks source centering and label shading.
3. The earliest retained database solution, **T37**, matches that Markdown table, including numeric right alignment.
4. A rewrite at **T78** removes the numeric alignment markers too, producing today's three `---` separators. The six cell values are unchanged. [Retained history](history.json) confirms both versions.

The current HTML-to-Markdown table branches in `scripts/import_historical_question_content.py:153` and `scripts/question_capture/dom.js:408` exhibit the same structural loss: they flatten cells and unconditionally insert a first-row header separator, without retaining source table/cell alignment or label backgrounds. This identifies a table-conversion limitation; it does not prove either current function authored the historical T78 transaction. The earlier MathML table/grid repair targeted explicit ruled `mtable` conversions, while this example uses an HTML `table`.

## Render verification

The original table was rendered from its saved HTML/SVG without the app's generic Markdown-table CSS. The current stored solution was rendered through the actual player Markdown function, theme, stylesheet and MathJax. Both render without math errors, but their layout/roles differ as above. This is a source-fidelity issue that a zero MathJax error count cannot detect.

- [Original source table](source-html.png)
- [Current stored solution](stored-markdown.png)
- [Original cell attributes and TeX titles](source-table-proof.json)
- [Computed layout comparison](render-comparison.json)
- [Stored entity](entity.json), [ownership](ownership.json), [history](history.json)

`current-python-raw-svg-attempt.json` records a diagnostic attempt to feed the untouched legacy SVGs to the historical Python converter. That path requires saved-asset handling for these SVGs and returned empty fallbacks/errors; it is not the stored import result and is not used as evidence of missing table values.
