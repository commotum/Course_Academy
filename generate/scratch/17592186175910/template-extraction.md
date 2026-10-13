# Templates and source components

q-44399: reference y=-x+3, red parallel l2 intersects the y-axis at the marked point (0,-1). The blue and red lines have slope -1. Source graph has axes and ticks; the intercept is labeled -1. Prompt includes graph, reference equation, parallel relation, and equation request. One radio field has five full equations; no solution or key. Correct equation is y=-x-1 by the graph.

q-215701: reference y=(1/2)x; red l2 passes through marked (-4,4), with dashed projections to axes and labels -4 and 4. Reference passes through origin; red intercept is 6. Prompt asks for equation and supplies y= before the field-1 blank. The response fragment is x/2+6, not a full equation. There are no source choices, solution, or key.

Shared purpose: transfer the reference slope to a parallel line and determine the intercept from a marked point. Never use the reference intercept as the unknown line's intercept. Point and slope must be explicit in a readable diagram. Fixed prompt structure and field shape are preserved. Both prompts replay exactly, including source image references and spacing. Normal variants retain the same mathematical notation and use regenerated diagrams.

The entire observed radio bank at m=-1, b=-1 maps as follows. The recipes reproduce full equations, not independent equation sides.

|Original value|Recipe at general m,b|Full source value reproduced|Interpretation|
|---|---|---|---|
|y=-x-1|y=m*x+b|yes|correct, graph-derived key|
|y=x+1|y=-m*x-b|yes|both signs reversed|
|y=-x+1|y=m*x-b|yes|intercept sign reversed|
|y=x|y=-m*x|yes|slope sign reversed and intercept omitted|
|y=-x|y=m*x|yes|intercept omitted|

One eligible complete profile is chosen before constructing its bank. m and b are nonzero, so all five full equations are distinct and only one satisfies the given parallel slope and marked point. No pooled or mixed bank, option feedback, or additional distractor is added. The profile's generalized mistake interpretations are inferred; its exact observed value transformations are verified.

Observed parameter values: m=-1,c=3,x0=0,y0=-1 and m=1/2,c=0,x0=-4,y0=4. Normal sampling is a bounded authored extension: easy m in {-3,-2,-1,1,2,3}, intercept in {-5,-3,-1,1,3,5}; moderate m in {±1/2,±2/3,±3/2}, x0 in {±2,±4,±6}, y0 in {±1,±3,±5}, with |c|<=8. Reference c=b+2 in normal generation avoids overlapping lines; observed c=0 and 3 remain accepted for exact replay. Source cases are not lost merely because normal sampling uses a narrower policy. All x,y are real.

Correct answer is computed first as b=y0-m*x0. The authored fixed solution follows the canonical sequence: equal parallel slopes, repeat reference equation, extract slope, identify point, point-slope equation, substitute, simplify to y=m*x+b. Original practice solutions are missing; this is an explicitly authored repair in generated content only. No source question or answer is overwritten.

Novelty key is (exact m, marked x0, marked y0), excluding seed, UUID, choice order, and reference-line intercept c. The full bounded normal set has finite capacity recorded in validation.json. A changed reference intercept alone is never new inventory. At fixed parameters the question identity is stable even when seed differs; changing generator rendering requires review and version change.
