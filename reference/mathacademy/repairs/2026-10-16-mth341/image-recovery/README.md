# MTH 341 formula-image recovery

`replacements.json` maps all **105 formula image paths** from the 2026-10-16 audit to **bare TeX**. The caller supplies prose math delimiters. These assets occur in 79 distinct content fields. No database writes were performed here.

Recovery covers 85 SVG files and 20 PNG files. All 148 assets classified as genuine diagrams are excluded. SVG recovery preserves the literal TeX surrounding each embedded MathJax container and converts every retained assistive MathML fragment. The source MathML, source table entries/rules, styles, affected field IDs, and recovered TeX are in `evidence.json`.

All 20 PNGs were directly inspected through `view_image` using the four `png-sources-*.png` contact sheets, then transcribed in `recover.py`. Their matrix labels, signs, row/column order, symbolic entries, vector boldface, and punctuation were preserved. One PNG contains two matrices; both are transcribed.

Recovery preserves instructional formatting including gray pivot highlights, colored entries, augmented column rules, row-operation annotations, underbraces, double-struck real-number symbols, bold zero vectors, literal set braces, and the silver-bordered blank box used in the invertibility question. Equation systems use scalable braces with equals-aligned rows; matrices use `bmatrix` and augmented matrices use explicitly ruled `array` environments. The local converter extensions do not modify the shared capture implementation.

`verify.py` renders all 105 expressions through the application's actual MathJax configuration. All **138 resulting matrix/system tables** render successfully. For all **117 retained source MathML tables**, every flattened row's token text agrees with the rendered TeX, and augmented column rules agree. All PNG table dimensions agree with the direct transcription. There are zero renderer errors or page errors; see `render-verification.json`.

All 15 `comparison-00.png` through `comparison-14.png` sheets were inspected with `view_image`, showing every source asset beside its replacement. No incorrect entries, dropped labels, lost highlights, missing rules, or missing annotations were observed. Canonical row spacing and bracket sizing follow the application configuration. Colored relation spacing was adjusted and rechecked in `comparison-05.png` after the initial visual review.

Reproduce from the repository root:

```bash
uv run --offline --no-project --with playwright python reference/mathacademy/repairs/2026-10-16-mth341/image-recovery/recover.py
uv run --offline --no-project --with playwright python reference/mathacademy/repairs/2026-10-16-mth341/image-recovery/verify.py
```
