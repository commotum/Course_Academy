
# Four plot extraction stages


## 1. Specific inspection

All 67 assets were inspected individually at original resolution: canonical solution, eleven practice solution plots, and all 55 plotted answer choices. Most are 360×304; q119132 options 2–4 are 359×304 and q50198 options 3–4 are 360×308. Source plots have white/transparent backgrounds, black coordinate axes and arrows at positive axis ends, labeled integer ticks (some labels only every second unit), and red/black/blue curves. Solution plots add color-matched C labels. There are no curve traversal arrows, endpoint dots, or initial-condition markers. Viewport clipping is not a mathematical endpoint; finite exponential tails show a sampled drawing, not a finite-domain ODE. Logarithm/reciprocal questions explicitly restrict x>0; horizontally shifted distractor branches have their own singular boundaries.

## 2. Shared visual pattern

Three plotted curves illustrate a general solution family. A correct family preserves derivative shape, scale, orientation, shift and domain while allowing arbitrary vertical constants. Compare the whole image rather than one curve or one intercept. Some wrong options use horizontal shifts and are not a constant-translate family.

## 3. Complete per-bank geometry

Recipes below are ordered exactly as the newer/sole captured source field, before generator shuffling. Each row lists all three complete curves and colors. Original reference assets are retained exactly. Four metric coefficients marked empirical are inferential raster fits and remain explicit evidence-only profiles. Qualitative shape/orientation/branch identification is confirmed for every choice; exact PNG equality is reported separately from metric recovery.

### q-50195

Primitive parameters: `{"family": "quadratic", "a": "1", "h": "1", "k": "1", "constants": ["-1", "0", "1"]}`. Correct source image index: 3.
| Choice | Complete curves | Colors | Metric confidence |
|---|---|---|---|
| 1 | `x+1; x; x-1` | black,blue,red | coordinate/shape extraction; raster calibrated |
| 2 | `-(x-1)**2+1; -(x-1)**2; -(x-1)**2-1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 3 | `(x-1)**2-1; (x-1)**2; (x-1)**2+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 4 | `x**3+1; x**3; x**3-1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 5 | `x**2+1; x**2; x**2-1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| Asset role | Pixel origin | Pixels per x/y unit | Reference |
|---|---|---|---|
| solution | [141, 223] | [56, 54] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50195-solution.png) |
| 1 | [141, 167] | [56, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50195-1.png) |
| 2 | [141, 128] | [56, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50195-2.png) |
| 3 | [141, 223] | [56, 54] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50195-3.png) |
| 4 | [169, 167] | [67, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50195-4.png) |
| 5 | [169, 235] | [67, 45] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50195-5.png) |

### q-50196

Primitive parameters: `{"family": "cubic", "a": "-1", "h": "-1", "k": "1", "constants": ["-1", "0", "1"]}`. Correct source image index: 1.
| Choice | Complete curves | Colors | Metric confidence |
|---|---|---|---|
| 1 | `-(x+1)**3+-1; -(x+1)**3+0; -(x+1)**3+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 2 | `-(x-1)**2+-1; -(x-1)**2+0; -(x-1)**2+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 3 | `(x-1)**3+-1; (x-1)**3+0; (x-1)**3+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 4 | `-(x+1)**2+-1; -(x+1)**2+0; -(x+1)**2+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 5 | `-x**3+-1; -x**3+0; -x**3+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| Asset role | Pixel origin | Pixels per x/y unit | Reference |
|---|---|---|---|
| solution | [169, 167] | [38, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50196-solution.png) |
| 1 | [169, 167] | [38, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50196-1.png) |
| 2 | [169, 167] | [38, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50196-2.png) |
| 3 | [169, 167] | [38, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50196-3.png) |
| 4 | [169, 167] | [38, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50196-4.png) |
| 5 | [169, 167] | [38, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50196-5.png) |

### q-119132

Primitive parameters: `{"family": "exponential", "a": "-2", "h": "0", "k": "-1/4", "constants": ["0", "3", "6"]}`. Correct source image index: 4.
| Choice | Complete curves | Colors | Metric confidence |
|---|---|---|---|
| 1 | `-x**2/4; -x**2/4+2; -x**2/4+4` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 2 | `2*exp(-x/4)+1; 2*exp(-x/4)-2; 2*exp(-x/4)-5` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 3 | `-2*exp(x/4)-1; -2*exp(x/4)+2; -2*exp(x/4)+5` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 4 | `-2*exp(-x/4); -2*exp(-x/4)+3; -2*exp(-x/4)+6` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 5 | `x**2/4; x**2/4+2; x**2/4+4` | red,black,blue | coordinate/shape extraction; raster calibrated |
| Asset role | Pixel origin | Pixels per x/y unit | Reference |
|---|---|---|---|
| solution | [169, 163] | [20, 16.5] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119132-solution.png) |
| 1 | [169, 163] | [31, 25.5] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119132-1.png) |
| 2 | [169, 163] | [20, 16.5] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119132-2.png) |
| 3 | [169, 163] | [20, 16.5] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119132-3.png) |
| 4 | [169, 163] | [20, 16.5] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119132-4.png) |
| 5 | [169, 240] | [31, 25.5] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119132-5.png) |

### q-49947

Primitive parameters: `{"family": "logarithmic", "a": "1", "h": "0", "k": "1", "constants": ["-1", "0", "2"]}`. Correct source image index: 1.
| Choice | Complete curves | Colors | Metric confidence |
|---|---|---|---|
| 1 | `log(x)-1; log(x); log(x)+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 2 | `1/(x-2); 1/x; 1/(x-1)` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 3 | `x-2; x; x+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 4 | `log(x-2); log(x); log(x-1)` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 5 | `1/x-2; 1/x; 1/x+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| Asset role | Pixel origin | Pixels per x/y unit | Reference |
|---|---|---|---|
| solution | [85, 167] | [56, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-49947-solution.png) |
| 1 | [85, 167] | [56, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-49947-1.png) |
| 2 | [85, 234] | [56, 46] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-49947-2.png) |
| 3 | [102, 204] | [67, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-49947-3.png) |
| 4 | [73, 125] | [49, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-49947-4.png) |
| 5 | [73, 204] | [49, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-49947-5.png) |

### q-50197

Primitive parameters: `{"family": "reciprocal", "a": "1", "h": "0", "k": "1", "constants": ["-1", "0", "1"]}`. Correct source image index: 4.
| Choice | Complete curves | Colors | Metric confidence |
|---|---|---|---|
| 1 | `x-1; x; x+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 2 | `x**2/4; x**2/4+1; x**2/4-1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 3 | `-1/x-1; -1/x; -1/x+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 4 | `1/x-1; 1/x; 1/x+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 5 | `-sqrt(3*x); -sqrt(3*x)+1; -sqrt(3*x)-1` | red,black,blue | empirical coefficient; original raster retained |
| Asset role | Pixel origin | Pixels per x/y unit | Reference |
|---|---|---|---|
| solution | [85, 234] | [56, 46] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50197-solution.png) |
| 1 | [85, 234] | [56, 46] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50197-1.png) |
| 2 | [85, 234] | [56, 46] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50197-2.png) |
| 3 | [85, 100] | [56, 46] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50197-3.png) |
| 4 | [85, 234] | [56, 46] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50197-4.png) |
| 5 | [85, 100] | [56, 46] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50197-5.png) |

### q-50198

Primitive parameters: `{"family": "linear", "a": "-2", "h": "0", "k": "1", "constants": ["-3", "0", "3"]}`. Correct source image index: 1.
| Choice | Complete curves | Colors | Metric confidence |
|---|---|---|---|
| 1 | `-2*x-3; -2*x; -2*x+3` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 2 | `-x**3/8-1; -x**3/8; -x**3/8+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 3 | `x**2-2; x**2; x**2+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 4 | `-x**2-2; -x**2; -x**2+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 5 | `2*x-3; 2*x; 2*x+3` | red,black,blue | coordinate/shape extraction; raster calibrated |
| Asset role | Pixel origin | Pixels per x/y unit | Reference |
|---|---|---|---|
| solution | [169, 150] | [38, 35] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50198-solution.png) |
| 1 | [169, 150] | [38, 35] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50198-1.png) |
| 2 | [169, 167] | [38, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50198-2.png) |
| 3 | [169, 163] | [38, 28] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50198-3.png) |
| 4 | [169, 162] | [38, 28] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50198-4.png) |
| 5 | [169, 150] | [38, 35] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-50198-5.png) |

### q-79565

Primitive parameters: `{"family": "quadratic", "a": "1", "h": "0", "k": "1", "constants": ["-1", "0", "1"]}`. Correct source image index: 1.
| Choice | Complete curves | Colors | Metric confidence |
|---|---|---|---|
| 1 | `x**2+1; x**2+0; x**2+-1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 2 | `2*x+1; 2*x+0; 2*x+-1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 3 | `-x**2+1; -x**2+0; -x**2+-1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 4 | `x**3+1; x**3+0; x**3+-1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 5 | `(x+1)**3; x**3; (x-1)**3` | red,black,blue | coordinate/shape extraction; raster calibrated |
| Asset role | Pixel origin | Pixels per x/y unit | Reference |
|---|---|---|---|
| solution | [169, 204] | [67, 67] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79565-solution.png) |
| 1 | [169, 204] | [67, 67] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79565-1.png) |
| 2 | [169, 163] | [80, 80] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79565-2.png) |
| 3 | [169, 123] | [67, 67] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79565-3.png) |
| 4 | [169, 163] | [67, 63] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79565-4.png) |
| 5 | [169, 163] | [67, 63] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79565-5.png) |

### q-79566

Primitive parameters: `{"family": "cubic", "a": "1/2", "h": "-2", "k": "1", "constants": ["-1", "0", "1"]}`. Correct source image index: 1.
| Choice | Complete curves | Colors | Metric confidence |
|---|---|---|---|
| 1 | `(x+2)**3/2+-1; (x+2)**3/2+0; (x+2)**3/2+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 2 | `3*(x+2)**2/2+-1; 3*(x+2)**2/2+0; 3*(x+2)**2/2+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 3 | `(x+3)**3/2; (x+2)**3/2; (x+1)**3/2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 4 | `-3*(x+2)**2/2+-1; -3*(x+2)**2/2+0; -3*(x+2)**2/2+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 5 | `-(x+2)**3/2+-1; -(x+2)**3/2+0; -(x+2)**3/2+1` | red,black,blue | coordinate/shape extraction; raster calibrated |
| Asset role | Pixel origin | Pixels per x/y unit | Reference |
|---|---|---|---|
| solution | [295, 167] | [54, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79566-solution.png) |
| 1 | [295, 167] | [54, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79566-1.png) |
| 2 | [295, 167] | [54, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79566-2.png) |
| 3 | [275, 167] | [49, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79566-3.png) |
| 4 | [295, 156] | [54, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79566-4.png) |
| 5 | [295, 167] | [54, 39] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79566-5.png) |

### q-119139

Primitive parameters: `{"family": "exponential", "a": "-2", "h": "0", "k": "2", "constants": ["-2", "0", "2"]}`. Correct source image index: 3.
| Choice | Complete curves | Colors | Metric confidence |
|---|---|---|---|
| 1 | `2*exp(2*x)+-2; 2*exp(2*x)+0; 2*exp(2*x)+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 2 | `-(x+2)**2/4+-2; -(x+2)**2/4+0; -(x+2)**2/4+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 3 | `-2*exp(2*x)+-2; -2*exp(2*x)+0; -2*exp(2*x)+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 4 | `(x+2)**2/4+-2; (x+2)**2/4+0; (x+2)**2/4+2` | red,black,blue | empirical coefficient; original raster retained |
| 5 | `-2*exp(-2*x)+-2; -2*exp(-2*x)+0; -2*exp(-2*x)+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| Asset role | Pixel origin | Pixels per x/y unit | Reference |
|---|---|---|---|
| solution | [232, 163] | [31, 31] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119139-solution.png) |
| 1 | [232, 163] | [31, 31] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119139-1.png) |
| 2 | [232, 163] | [31, 31] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119139-2.png) |
| 3 | [232, 163] | [31, 31] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119139-3.png) |
| 4 | [194, 188] | [26, 25.5] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119139-4.png) |
| 5 | [106, 163] | [31, 31] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119139-5.png) |

### q-119142

Primitive parameters: `{"family": "cubic", "a": "-1/4", "h": "1", "k": "1", "constants": ["-2", "0", "2"]}`. Correct source image index: 2.
| Choice | Complete curves | Colors | Metric confidence |
|---|---|---|---|
| 1 | `3*(x+1)**2/4+-2; 3*(x+1)**2/4+0; 3*(x+1)**2/4+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 2 | `-(x-1)**3/4+-2; -(x-1)**3/4+0; -(x-1)**3/4+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 3 | `-(x+1)**3/4+-2; -(x+1)**3/4+0; -(x+1)**3/4+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 4 | `(x-1)**3/4+-2; (x-1)**3/4+0; (x-1)**3/4+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 5 | `-3*(x-1)**2/4+-2; -3*(x-1)**2/4+0; -3*(x-1)**2/4+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| Asset role | Pixel origin | Pixels per x/y unit | Reference |
|---|---|---|---|
| solution | [169, 163] | [31, 31] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119142-solution.png) |
| 1 | [169, 163] | [31, 31] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119142-1.png) |
| 2 | [169, 163] | [31, 31] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119142-2.png) |
| 3 | [169, 163] | [31, 31] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119142-3.png) |
| 4 | [169, 163] | [31, 31] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119142-4.png) |
| 5 | [169, 163] | [31, 31] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-119142-5.png) |

### q-79563

Primitive parameters: `{"family": "linear", "a": "3", "h": "0", "k": "1", "constants": ["-2", "0", "2"]}`. Correct source image index: 5.
| Choice | Complete curves | Colors | Metric confidence |
|---|---|---|---|
| 1 | `-3*x+-2; -3*x+0; -3*x+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 2 | `3*x**3+-2; 3*x**3+0; 3*x**3+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| 3 | `-3*x**2+-2; -3*x**2+0; -3*x**2+2` | red,black,blue | empirical coefficient; original raster retained |
| 4 | `3*x**2+-2; 3*x**2+0; 3*x**2+2` | red,black,blue | empirical coefficient; original raster retained |
| 5 | `3*x+-2; 3*x+0; 3*x+2` | red,black,blue | coordinate/shape extraction; raster calibrated |
| Asset role | Pixel origin | Pixels per x/y unit | Reference |
|---|---|---|---|
| solution | [169, 163] | [67, 56] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79563-solution.png) |
| 1 | [169, 163] | [67, 56] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79563-1.png) |
| 2 | [169, 163] | [46, 40] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79563-2.png) |
| 3 | [169, 133] | [52.5, 48] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79563-3.png) |
| 4 | [169, 192] | [52.5, 48.5] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79563-4.png) |
| 5 | [169, 163] | [67, 56] | [full resolution](/home/jake/Developer/Course_Academy/generate/scratch/17592186096698/source-assets/q-79563-5.png) |

## 4. Reusable specification

Matplotlib draws black axes with positive axis arrows, readable coordinate ticks, three color-matched curves and optional C labels. Instance geometry includes exact curve expressions, color order, coordinate bounds, tick increment, positive-domain branch minima and optional labels. Bounds derive from primitive shift, rate and magnitude. Correct and wrong plots share axes in normal output. Every option uses its own mathematics from the same question instance; the renderer never samples.
All changed-parameter plots are freshly rendered or cached by the complete geometry digest. A cache hit requires both PNG and sidecar. Immutable unique request files prevent concurrent mixing; each final PNG and sidecar is individually atomically replaced. Sidecars record geometry, runtime and dependencies. The primary environment lacks Matplotlib; the renderer uses cached Python3.10/wheels read-only. No install, direct SVG or image model.
Raw reference profiles reuse original assets; affine curve transport supplies changed-parameter evidence. Original per-plot geometry is in raster-evidence.json and differs from the uniform authored specification. The raw distractor authoring intentions are unknown, even where curve geometry is recognizable.
Normal examples at all levels were visually checked. Source transparent pixels were displayed against white. Polynomial extrema/inflections, exponential orientation/asymptote, positive-domain singular tails, intercept scales and colors were checked. Curve tails are clipped by the viewport, consistent with source sketch convention. No artificial endpoints or traversal direction are asserted.
