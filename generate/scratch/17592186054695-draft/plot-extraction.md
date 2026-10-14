# Four-stage plot extraction and render specification

## 1. Specific plots

All 20 original answer image occurrences (15 distinct native PNGs) were visually inspected at full native resolution. They show gray square unit gridlines, black x/y axes with arrows, numeric labels commonly every two units, a red full line, no choice markers. They use **different origins and different bounds**: q-102054's bank places the origin near pixel x=114; many others place it near x=64. An image path match is not the geometric proof. `source-plot-inspection.json` fits each original occurrence's own black axes, gray grid step and every red-line pixel to independently confirm its complete slope/intercept. Lines and intercepts agree with the table in template-extraction.md; no discrepancy with baseline geometry was found.

The two available original final graphs were inspected independently: q-102054 has blue points (0,0),(1,−2), q-109055 blue points (0,2),(8,−2). The canonical uses red points (0,3),(4,1), same red line. Every marker lies on its computed line. These are actual chosen forward-substitution points, not generic intercepts. The three independent inventory questions were inspected in full, including their five-choice banks and final blue point markers. They vary homogeneous coefficient to −4,−3,−1 and retain x=0,1; their records are exact inventory, not original difficulty evidence.

## 2. Shared visual purpose

Compare whole line equations through graph direction, shift and coefficient, then show the correct line through the two actually computed points. Graphs are mathematically scaled and are central to the answer.

## 3. Components

Background: white. Coordinates: independently calibrated origin; gray grid; numeric tick labels; black real zero axes with x/y arrow labels. Curves: one complete red affine line per choice, each using its own entire equation. Solution: same correct red line plus exactly the two source-role blue point markers and legible coordinate labels. No invented feedback or labels identify an answer option as right/wrong.

Raw originals retain exact captured paths and available solution paths. Native dimensions, PNG SHA256 and per-image axis/grid/line fit are recorded. Source choices have no marked points; complete-line fit provides two or more calibrated points and direction from all red pixels. Raw plotted lines may have different bounds; normal banks share bounds so scale is not an answer clue.

## 4. Reusable specification

Matplotlib only. Choice bank selected and exact whole lines computed before rendering. Common bounds include zero, all intercepts, one-unit line values and the two chosen correct points, with at least two units margin; reject total span >34. Integer major ticks carry real signed numeric labels. Easy/M use unit grid; H adds halfunit gray minor grid, with its actual point y-coordinates exactly halfinteger. The unit major grid and plotted coordinate labels keep the halfunit reading visible. x/y glyphs are outside the arrow tips; true `0` is placed beside the axis intersection. Correct plot has two blue coordinate labels with white backing and offset away from the red line; source-like roles remain clear. No named-line glyph is necessary in this source family.

Plots are deterministic data-derived assets with exact line/point/reading-grid sidecars, runtime versions and hashes. Unique temporary directories hold each render input and intermediate PNG; final PNG and JSON writes are atomic. Thread calls are locked for Matplotlib safety; independent processes get unique inputs and equivalent atomic outputs. Fresh identical/different concurrent renders are tested without old cache hits. Assets are never pruned during parent QA. Actual rendered pixel geometry is fitted separately from symbolic mathematics and grading.
