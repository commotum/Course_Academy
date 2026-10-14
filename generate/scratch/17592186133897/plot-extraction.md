# Plot extraction and specification

## 1. Specific plots

Nine original plots inspected individually at360×304 after white alpha composition. q-42215: clockwise right trig loop, starts origin upward-right, then down rightside and returns upward-left; ticks x3,y±2. q-42298: curved right cusp through(0,0), C1 from(2,1)to(2,−1), C2 vertical upward x2; ticks y±1,x2. q-126722: clockwise lower loop, origin→right→bottom→left→origin; ticks x±2,y−2. q-126725: counterclockwise lower loop, origin→right→bottom→left→origin; ticks x±1,y−1. q-126818: C1 left cusp from(−2,−3)→origin→(−2,3); C2 downward vertical; ticks x−2,y±3. q-126858: C1 from(−1,1)→origin→(1,1), C2 leftward horizontal at y1; ticks x±1,y1. q-126727: narrow right loop starts origin→lower curve→right→upper→origin, counterclockwise; ticks x1,y±2. q-126859: C1 starts(−1,−2)→origin→(1,−2), C2 leftward y−2; clockwise; ticks x±1,y−2. Canonicale-9555: C1 left cusp from(−2,−1)→origin→(−2,1), C2 downward at x−2; positive orientation; ticks x−2,y±1. All original boundary segments are solid, orange C1 and pink C2; pale-blue region fill. No open endpoints or endpoint disks are shown.

The lesson’s concrete ellipse tutorial plot (asset a6/a6d9fe9cad4ccee56d5d61457c475b41371e0705f1aeccd3a18fb4a3fa8e127c.png) was also inspected at original resolution: counterclockwise ellipse, x±2,y±1. This independently anchors authored easy geometry/traversal.

## 2. Shared visual purpose

Show the complete closed region, traversal arrows and meaningful intercept/extremum scales. Plots support orientation and segment bookkeeping, while the printed parametric equations carry exact geometry. Moderate rating because every instance needs a plot but construction is one/two known plane segments.

## 3. Components

White background, black arrowed x/y axes through origin; nonzero feature ticks, no zero label; orange curve C orC1; pink C2; black traversal arrows following increasing parameter; labels C,C1,C2,D; pale-blue enclosed area. Every exact x(t),y(t),t interval is the same instance used by prompt and solutions.

## 4. Parameterized renderer

Matplotlib samples each exact segment at601 monotonically increasing parameter values. Filled boundary concatenates the same segments. Closing endpoints must meet symbolically. Curve arrows use fractions .18,.42,.68,.87 for one segment and .27,.74 for each of two segments. Bounds derive from coordinate extrema, with padding; tick labels round the exact integer extrema rather than truncate floating-point samples. Equal axis scale prevents distorted geometry; thin-loop figure bounds remain readable. Reproduce the mathematical geometry/traversal, not incidental source typography. Fresh writes use private unique temporaryPNG/JSON files, atomic final replacements and a renderer lock around Matplotlib thread-unsafe state. Cache hits require bothPNG and itsJSON sidecar. NoSVG or image models. All plot files are local draft artifacts; original-image refs preserved only in anchor raw evidence.
