# Original math images suitable for native reconstruction

**Source-fidelity decision:** These original illustrations are not import errors. Preserve them by default. The user chose to restore the original determinant mnemonic while keeping the necessary formula repairs. This inventory records optional redesign possibilities and does not authorize replacements.

Read-only audit of database `math` at **T8100**, after the determinant mnemonic in tutorial **17592186060931** was replaced at T8086. Found **88 source raster assets used 124 times in 91 content fields/entities across 24 lessons** that are good candidates for native mathematical reconstruction. No database content was changed by this audit.

These are visually reviewed candidates, not completed repairs. **77 assets** are primarily annotated mathematical notation: formulas, arithmetic/sequence steps, labels, arrows, boxed steps, or schematic matrices. **11 assets** are symbolic dependency/change-of-coordinate diagrams. A repair must retain the explanatory structure and color; replacing a diagram with only its final equation would lose information.

## Why these survived

All 88 are confirmed original source images. For 48, the archived lesson HTML contains an original `<img src="/graphics/…">` matching the source image map. Retained capture metadata establishes original image elements for the others. They were not MathJax formulas accidentally rasterized during extraction. Import faithfully preserved the source's raster format.

The previous formula-image audit identified whole-formula MathJax SVG/PNG fallbacks. Its classification deliberately accepted original source images as graphics. That provenance check does not answer whether a source image is mostly mathematical notation that would be better displayed natively. The determinant mnemonic exposed this second category.

## Examples

| Entity | Attribute | Image contents |
| --- | --- | --- |
| **17592186056023** | `tutorial/content` | Colored distributive-law formula with arrows from the multiplier to the terms. |
| **17592186056059** | `tutorial/content` | `2 × 3 = 6`, with arrows labeling both factors and the product. |
| **17592186079625** | `tutorial/content` | Geometric sequence with `×3` arrows between successive terms. |
| **17592186079726** | `tutorial/content` | Arithmetic sequence with `+2` arrows between successive terms. |
| **17592186121144** | `tutorial/content` | Cubing/cube-root mnemonic connecting 4 and 64. |
| **17592186130380** | `tutorial/content` | Row-echelon staircase matrix, leading entries, and zero region. |
| **17592186142631** | `question/worked-solution` | Division formula annotated with dividend, divisor, and quotient labels. |
| **17592186176970** | `tutorial/content` | Squaring/square-root mnemonic connecting 10 and 100. |
| **17592186130348** | `tutorial/content` | Change-of-basis commutative diagram with symbolic matrix labels. |
| **17592186168061** | `tutorial/content` | Multivariable chain-rule dependency trees with derivative labels. |

The last chain-rule asset alone appears in **19 current fields**, including tutorial and worked-solution records. Deduplicating by image address identifies every current use of the selected image, rather than repairing only the first example encountered.

## Scope and limits

The native read-only export examined **2,913,976 current facts**. The image inventory covers **37,695 image-bearing fields and 37,234 distinct assets**, with ownership and lesson context. No original MathJax-image asset from the earlier audit remains referenced at this basis. Every one of the **204 currently referenced SVG assets** was checked structurally; none has the signature of a standalone MathJax formula rendering.

This follow-up visually reviewed **789 distinct raster assets** selected from short/wide tutorial images, matrix/vector/chain-rule tutorials, relevant algebra and sequence lessons including worked solutions, and short newly encountered assets. Ordinary plots, spatial geometry, area models, and state-machine diagrams were retained outside this initial notation-focused list. Such graphics may also benefit from vector reconstruction, but that is a broader redesign task.

**This is not an exhaustive semantic review of every raster image.** In particular, tall figures, other unselected lesson graphics, and longer newly encountered images can contain further candidates. The confirmed count is a lower bound. Image dimensions/topic filtering is used only to prioritize review, never to establish a defect by itself.

## Evidence and repair inputs

- [Candidate inventory](candidates.csv): entity, attribute, lesson title, asset address, category, MA identity, and surrounding content.
- [Full candidate evidence](candidates.json): exact asset spans, current-value hashes, all current uses, original source paths/tags, and retained capture provenance.
- [Current candidate content](candidate-fields.json): original values and fact provenance for the 91 selected fields at T8100. Future repairs should reread and guard current values with CAS.
- [Visual review decisions](visual-review.json), [SVG structural review](svg-review.json), [inventory counts](inventory-summary.json), and [review summary](summary.json).
- Candidate contact sheets: [1](confirmed-candidates-0.png), [2](confirmed-candidates-1.png), [3](confirmed-candidates-2.png).

`inventory.py` builds the current-use inventory from the immutable export. `curate.py` records the visual selections and binds them to source evidence. Large full-database work files remain under `.local/edb/native-math-visual-audit-2026-10-26/`.
