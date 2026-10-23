# Plot extraction/specification

Plot rating **none**. All eight sources and the canonical example use standalone TeX matrices, not coordinate graphs or generated geometric diagrams. Matrices are rebuilt as TeX from the instance parameters. Normal variants add exactly one `\boxed{value}` marker, including repeated/negative entries. This is code-native mathematical notation and needs no Matplotlib/TikZ or image model.

The original lesson screenshot evidence was inspected at full resolution: q-13498 boxes row1,column2; q-13503 boxes row3,column3. Local PNG copies and original paths/hashes are in context-evidence.json. The capture's text/JSON removes the gray highlighting. Raw replay keeps the omission, while a supported normal question must show one explicit boxed cell. No source image is substituted for a changed matrix.

Steps5/7 require no plot generation. Formatting QA checks the actual rebuilt matrix, balanced TeX and matching placeholders. All levels retain the original brackets/row/column ordering. Standalone math rendering is not counted as a plot. A local Matplotlib typography preview (`typography-preview.png`) is visual QA only, not a prompt asset.
