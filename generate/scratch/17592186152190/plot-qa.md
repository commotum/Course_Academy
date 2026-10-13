# Visual QA

Inspected source-montage-0.png, source-montage-1.png and source-montage-2.png: all 36 practice images, white-composited with source IDs and placement roles. Also inspected canonical-montage.png: both e-6818 images. All source plots show the intended cardinal quarter/half and correct physical center/radii. q-274866's plot agrees with its prompt rather than its erroneous copied center/radii prose.

Inspected generated-montage-0.png through generated-montage-8.png: all **53 unique plot pairs / 106 PNGs** used by the 84 validated records, including all source parameter replays, all template/bank generated variants and minimum/maximum radius plus signed-center boundaries. plot-contact-index.json lists the exact inspected mathematical object and its prompt/solution assets. Checked the skinny a=2,b=8 boundary solution at original resolution as well.

Observed: solid blue assessed quarter/half is correct throughout; dashed complement is restricted to solutions and the q-328327 context-style prompt. Closed endpoint dots stay on the exact ellipse. Positive/negative translated centers and unequal radii have readable coordinate extrema and center labels. Limits include all extrema and origin with proportional margins. Axes keep equal coordinate scale. Cardinal parameter labels are visible, including theta=2pi when the rightmost point is the upper bound. No endpoint label is exposed in the question plot. No clipping or text overlap prevents reading at the generated 728×624 display size. Contact sheets reduce text size for inspection; original PNGs remain available.

Presentation changes from source are limited to Matplotlib styling: light coordinate grids through all extreme/center ticks substitute for the original selective dashed projection guides; axes use chart spines and explicit x/y labels rather than source arrowheads. Arc geometry, endpoint inclusion and assessed-segment/context distinction are preserved. No source plot used a curve direction arrow. A source solution's four cardinal theta labels remain four cardinal parameter labels; no misleading general ellipse polar-angle wedge is drawn.

Recreate contact sheets after validation:

```sh
.venv/bin/python generate/scratch/17592186152190/montage.py generated
```

Renderer and cached dependency versions are in render-provenance.json. Plot specifications derive from the same exact instance, with no independent sampling. Mathematical tests independently parse learner-visible equations and parameter intervals, derive endpoint coordinates, and compare render specification parameters.
