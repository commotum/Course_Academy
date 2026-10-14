# Plot extraction and rendering

## 1. Specific plots and full-native inspection

Twenty-one unique 360×304 rasters occur across 25 practice-option placements, the five two-image solutions and canonical e-8658. `source-native-0.png` through `source-native-2.png` show seven complete native plots each; the final row images 6c, b7 and ff were also inspected individually at full native resolution. `source-contact.png` shows the complete set. `plot-spec.json` maps every asset, two marked coordinates, branches/quadrants, asymptotes, fitted origin, independent pixels per x/y unit and curve residual. Source text labels supply exact ordinate values; pixel calibration is measured separately for each raster and has normal antialias/marker uncertainty.

All figures have white/transparent background, black zero axes with positive-direction arrowheads, axis labels x and y, no tick marks/grid, two blue reciprocal branches and two filled blue marks at x=±1 with exact coordinate labels. Every positive curve lies in quadrants I/III, every negative distractor in II/IV. Both axes are asymptotes; curves do not connect across x=0. No arrows occur on the curves themselves.

## 2. Shared visual pattern

The visible coordinate labels determine the coefficient through xy, with branch sign and asymptote positions providing additional checks. Uncalibrated silhouettes do not suffice: most images use about 42 px/x-unit and 35 px/y-unit, but 10/x uses about 7 px/y-unit; 5/x uses about 24 px/x-unit and 20 px/y-unit; the wide base/canonical plots use about 28 px/x-unit and 23 px/y-unit. Correct 5/x and wrong 10/x thus cannot be mapped from curve height alone. ALL incorrect–incorrect pairs are different c/x functions after their own label/scale calibration.

## 3. Components

Each source entry in plot-spec.json specifies native dimensions, origin, marked-point pixel centers, exact point coordinates, independent axis scales, coefficient c, curve quadrants and x=0/y=0 asymptotes. Raster geometric consistency is verified by converting blue-stroke pixels through that entry's transform and checking xy=c; median relative errors range approximately 1.2–5.2%, consistent with finite strokes in shallow curves. This is a bounded geometric check, not an assertion that unknown source plotting limits were recovered exactly.

## 4. Reusable specification

Matplotlib renders separate c/x branches for x<0 and x>0. No clipped curve samples connect across the asymptote. Bounds derive from |c| and marked x: x bounds ±4.1m, y bounds ±2.6|c|/m. Actual zero axes are arrowed, and marked points (±m,±c/m) have visible fraction/integer coordinate labels. Normal m=1 easy/moderate, m=2 hard. Independent scale adaptation makes mathematical labels mandatory: all normal graphs have native 360×304 readable labels, marker clearance ≥40 pixels vertically and ≥35 horizontally, and unclipped text bounding boxes. There are no invented unlabelled tick assumptions. Blue-stroke checks confirm exact evaluated branch points are visible at native pixels.

Changed answer plots, base plot and correct solution plot all derive from the exact same instance. Original raw profiles retain exact raster paths only at matching original n,d; changed profiles run the same extracted formulas through the renderer. Dynamic plot files and sidecars use deterministic hashes, unique temporary names and atomic replacement; cache hits require both files. A thread lock protects Matplotlib. Concurrent fresh identical/different parameter render tests pass. No direct SVG or image model is used.

`generated-native.png` was visually inspected: easy contractions/integers, moderate nonunit rational scales and hard nonunit-coordinate fractional labels remain readable. Both positive and negative boundary choices are independently checked in validate.py. Renderer versions: Python 3.13.5, Matplotlib 3.11.2.
