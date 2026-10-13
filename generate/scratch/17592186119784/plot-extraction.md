# Plot extraction

No practice prompt, bank or solution contains a plot; matrices are standard LaTeX. No renderer is required for generated instances.

Canonical e-4498 has four raster assets, inspected at their full original resolution from `/media/jake/SSD/EDB/math/images`:

| Role | Asset | Read mathematical content |
| --- | --- | --- |
| Prompt | `4d/4dd9b1c1b3d789c166ecd8f6d2a909609c7f4324705c84115cce84a29181bf32.png` | A has rows (0,0,0,0), (0,1,0,0), (0,1,0,0), (0,0,1,2) |
| Statement I false | `c1/c1ec838cd30cca8fbb2e3996d5a7d84dadb233e1951d05b532a9d606d887eb2f.png` | Same A; a32=a43=1 highlighted red, below diagonal |
| Statement II true | `f3/f39c68a9b1f5e16caffbf159b629a958e147e14099334b049bdfcd857eef84d2.png` | Same A; complete upper region zero, highlighted blue |
| Statement III false | `f4/f4415c87201f5b92f23e3320c313cd58ac4e720135928645896f976614c5eaa0.png` | Aᵀ−A has rows (0,0,0,0), (0,0,1,0), (0,−1,0,1), (0,0,−1,0); two above-diagonal +1 entries highlighted red |

The shared visual pattern is a typeset matrix whose selected region explains a zero/nonzero triangular condition. Brackets, matrix name, entries, and selected region are the components. Color is an instructional highlight rather than geometry. These assets establish the canonical solution method; they are not embedded in source practice replays or generated questions. Normal LaTeX matrix stages show the actual parameter-dependent object without inventing a plot or copying a static canonical matrix. Plot rating **none**.
