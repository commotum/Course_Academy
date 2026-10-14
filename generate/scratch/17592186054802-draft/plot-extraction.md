# Plot extraction and native calibration

## 1. Specific originals

All four full native prompt PNGs were viewed at original dimensions. q-54285 and q-59732 are334×304, origin pixel(79,225), unit spacing31px both axes; every second integer tick is labeled. Their red curves respectively cross(0,2) and(4,4), and(0,4) and(4,0). q-71837 is327×304, origin(64,214), unit25.5px; intercepts(0,6),(2,0), steep negative red line. q-54293 is327×304, origin(115,188), unit25.5px; intercepts(0,2),(4,0), shallow negative red line. Calibrations use axis-zero locations, labeled grid scale and actual visible line geometry, not generation metadata or only a correct formula. Both original solution plots were also viewed in full at327×304 and show blue A/B intercept markers, matching their corresponding prompt calibrations. q-54285/q-59732 have no captured solution plots.

## 2. Shared pattern and purpose

A unit Cartesian grid, black axes with positive-end arrows and x/y labels, red unbounded line clipped to the plot window. Graph geometry supplies the problem's information. Marked solution plots add two visible blue points A/B and their labels without changing the line. Styling does not replace geometry.

## 3. Components and dependencies

Exact rational slope/intercept and selected point coordinates share the question parameters. Plot bounds contain both points and zero with3units of margin, squared to retain equal units. Integer grid, labels on every unit for spans≤14 and every second unit for larger windows; signs remain explicit and zero labels are omitted to avoid axis crossings. Source originals retain exact asset paths only after calibration. New assets are Matplotlib Agg552×552 PNGs, with axes, curve and markers from the same parameters. Tick-label glyph bounding boxes are measured after drawing and must clear the zero axes by≥4px. Native red curve pixels are independently fitted, with seven expected curve probes and blue marker probes. Grid spacing is checked against gray native pixels. All generated plots are inspected through actual pixels, not solely hashes/sidecars.

## 4. Reusable specification

`plot(profile,p,role)` derives all line values, limits, ticks and markers from the supplied instance. It never samples. Prompt and solution roles share the curve. q-54285 uses A(0,b),B(t,2b); q-59732 and original hard profiles use A(0,b),B(t,0). Authored families use A(0,b),B(u,mu+b), with integral readable coordinates including signed/fraction boundary cases. No plotting-from-equation learner task is introduced.

Source reuse is restricted to exact original parameters and each inspected native source asset; source calibration JSON gives independent red-pixel fit results for all six original images. Changed parameters always render anew. Only Matplotlib is used, no direct SVG or image models. Unique temporary PNG/JSON files atomically replace each deterministic final asset; a rendering lock protects Matplotlib's state. Fresh concurrent same/different inputs are checked in a newly created private render directory, and all evidence assets are retained. Cache use requires both PNG and sidecar. No shared render input path, shared edits or asset publication occurs.
