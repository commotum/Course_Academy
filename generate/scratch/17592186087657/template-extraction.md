# Four extraction stages

## 1. Specific observed questions

All nine prompts state that XY is a diameter, give two integer coordinate pairs, and ask for the full equation of the circle. Diagrams show a red circle, blue dashed diameter and endpoint labels. No numerical reading from an unlabeled graph is required. Moderate examples are horizontal/vertical diameters; hard examples have two nonzero differences and radical distance reduction. See source.json for all raw fields and classification.md for per-source omissions and labels.

## 2. Shared pattern

Given X=(x₁,y₁), Y=(x₂,y₂), compute d=√((x₁−x₂)²+(y₁−y₂)²), r=d/2, midpoint (h,k)=((x₁+x₂)/2,(y₁+y₂)/2), and choose the complete relation (x−h)²+(y−k)²=r². The equation is compared as a whole, up to a nonzero scalar.

## 3. Component map

Every observed field is selection / radio / five complete math equations. Let z=r² and D=4z. The recipes below map every original value one-to-one; their psychological interpretations are hypotheses, while their algebraic operation patterns are exact and source-grounded. They do not represent recovered authoring code.

### q-15292

Parameters: {"x1": 2, "y1": 2, "x2": -4, "y2": 2}. Profile: q-15292.

| Source value | Operation recipe | Captured correct designation |

|---|---|---|

| `$x^{2} + y^{2} = 9$` | omit both midpoint coordinates, r² | absent in field |

| `$(x - 1)^{2} + (y - 2)^{2} = 9$` | reflect x midpoint, r² | absent in field |

| `$(x + 1)^{2} + (y - 2)^{2} = 9$` | correct midpoint and r² | absent in field |

| `$(x + 1)^{2} + (y - 2)^{2} = 36$` | correct midpoint, diameter² | absent in field |

| `$(x - 1)^{2} + (y - 2)^{2} = 36$` | reflect x midpoint, diameter² | absent in field |

### q-15297

Parameters: {"x1": 6, "y1": 4, "x2": -4, "y2": 2}. Profile: q-15297.

| Source value | Operation recipe | Captured correct designation |

|---|---|---|

| `$x^{2} + (y - 3)^{2} = \sqrt{26}$` | omit x midpoint, radius unsquared | absent in field |

| `$(x - 3)^{2} + (y - 1)^{2} = \sqrt{26}$` | swap midpoint coordinates, radius unsquared | absent in field |

| `$x^{2} + (y - 3)^{2} = 26$` | omit x midpoint, r² | absent in field |

| `$(x - 1)^{2} + (y - 3)^{2} = \sqrt{26}$` | correct midpoint, radius unsquared | absent in field |

| `$(x - 1)^{2} + (y - 3)^{2} = 26$` | correct midpoint and r² | absent in field |

### q-117102

Parameters: {"x1": 2, "y1": 4, "x2": 2, "y2": 0}. Profile: q-117102.

| Source value | Operation recipe | Captured correct designation |

|---|---|---|

| `$(x+2)^{2}+(y+2)^{2}=4$` | reflect both midpoint coordinates, r² | no |

| `$(x-2)^{2}+(y-2)^{2}=16$` | correct midpoint, diameter² | no |

| `$(x+2)^{2}+(y+2)^{2}=16$` | reflect both midpoint coordinates, diameter² | no |

| `$(x-2)^{2}+(y+2)^{2}=4$` | reflect y midpoint, r² | no |

| `$(x-2)^{2}+(y-2)^{2}=4$` | correct midpoint and r² | yes |

### q-117103

Parameters: {"x1": 2, "y1": -1, "x2": 2, "y2": 1}. Profile: q-117103.

| Source value | Operation recipe | Captured correct designation |

|---|---|---|

| `$(x-2)^{2}+{y}^{2}=1$` | correct midpoint and r² | yes |

| `$(x+2)^{2}+{y}^{2}=4$` | reflect x midpoint, diameter² | no |

| `$(x-2)^{2}+{y}^{2}=4$` | correct midpoint, diameter² | no |

| `${x}^{2}+(y-2)^{2}=4$` | swap midpoint coordinates, diameter² | no |

| `$(x+2)^{2}+{y}^{2}=1$` | reflect x midpoint, r² | no |

### q-117105

Parameters: {"x1": -3, "y1": 0, "x2": 1, "y2": -2}. Profile: q-117105.

| Source value | Operation recipe | Captured correct designation |

|---|---|---|

| `$(x+1)^{2}+(y-1)^{2}=5$` | reflect y midpoint, r² | no |

| `$(x-1)^{2}+(y-1)^{2}=20$` | reflect both midpoint coordinates, diameter² | no |

| `$(x+1)^{2}+(y+1)^{2}=20$` | correct midpoint, diameter² | no |

| `$(x-1)^{2}+(y-1)^{2}=5$` | reflect both midpoint coordinates, r² | no |

| `$(x+1)^{2}+(y+1)^{2}=5$` | correct midpoint and r² | yes |

### q-117106

Parameters: {"x1": -2, "y1": 0, "x2": 0, "y2": 2}. Profile: q-117106.

| Source value | Operation recipe | Captured correct designation |

|---|---|---|

| `$(x+1)^{2}+(y-1)^{2}=8$` | correct midpoint, diameter² | no |

| `$(x-1)^{2}+(y+1)^{2}=8$` | reflect both midpoint coordinates, diameter² | no |

| `$(x+1)^{2}+(y+1)^{2}=2$` | reflect y midpoint, r² | no |

| `$(x-1)^{2}+(y+1)^{2}=2$` | reflect both midpoint coordinates, r² | no |

| `$(x+1)^{2}+(y-1)^{2}=2$` | correct midpoint and r² | yes |

### q-117107

Parameters: {"x1": -1, "y1": -3, "x2": 3, "y2": 1}. Profile: q-117107.

| Source value | Operation recipe | Captured correct designation |

|---|---|---|

| `$(x-1)^{2}+(y+1)^{2}=8$` | correct midpoint and r² | yes |

| `$(x-1)^{2}+(y+1)^{2}=32$` | correct midpoint, diameter² | no |

| `$(x+1)^{2}+(y-1)^{2}=32$` | reflect both midpoint coordinates, diameter² | no |

| `$(x-1)^{2}+(y-1)^{2}=8$` | reflect y midpoint, r² | no |

| `$(x+1)^{2}+(y-1)^{2}=8$` | reflect both midpoint coordinates, r² | no |

### q-70987

Parameters: {"x1": 7, "y1": 3, "x2": -1, "y2": 3}. Profile: q-70987.

| Source value | Operation recipe | Captured correct designation |

|---|---|---|

| `$(x+3)^{2}+(y+3)^{2}=4$` | reflect both midpoint coordinates, radius unsquared | no |

| `$(x-3)^{2}+(y-3)^{2}=16$` | correct midpoint and r² | yes |

| `$(x+3)^{2}-(y+3)^{2}=4$` | reflect both midpoint coordinates, subtract y-square, radius unsquared | no |

| `$(x-3)^{2}+(y-3)^{2}=4$` | correct midpoint, radius unsquared | no |

| `$(x+3)^{2}+(y+3)^{2}=16$` | reflect both midpoint coordinates, r² | no |

### q-70990

Parameters: {"x1": -3, "y1": 2, "x2": 3, "y2": 4}. Profile: q-70990.

| Source value | Operation recipe | Captured correct designation |

|---|---|---|

| `$(x-3)^{2}-{y}^{2}=10$` | swap midpoint coordinates, subtract y-square, r² | no |

| `$(x-3)^{2}+{y}^{2}=10$` | swap midpoint coordinates, r² | no |

| `${x}^{2}+(y-3)^{2}=10$` | correct midpoint and r² | yes |

| `$(x+3)^{2}+{y}^{2}=10$` | swap midpoint coordinates then reflect x coordinate, r² | no |

| `${x}^{2}+(y+3)^{2}=10$` | reflect y midpoint, r² | no |

## 4. Reusable masks and constraints

Source replay replaces complete coordinate-pair components in the prompt and complete display blocks in the solution. General-circle, distance substitution, signed difference evaluation, arithmetic sum, optional square-factor extraction, half-diameter, midpoint substitution, equation substitution and final equation are distinct nodes. q-117105 retains its extra factored-sum row; q-117106/q-117107 retain sum-to-factor rows; q-70990 retains total-to-factor row; moderate sources retain four distance rows. Source prose including radius/center/endpoints is filled independently. The full seven present solution strings match exactly at source parameters; absent strings stay absent. q-70987 omits the redundant XY/2 equality and retains that omission.

Authored defaults have five options chosen as one complete bank before sampling: easy uses correct r², diameter², unsquared radius, X-as-center and Y-as-center; moderate/hard use correct midpoint/r², reflected midpoint/r², midpoint/diameter², X-as-center/r², and unhalved coordinate sums/r². All arise from actual midpoint, distance, radius and equation operations. No random perturbation bank or option diagnosis is shown. Any duplicate equation or second correct answer rejects the whole instance.

No mathematically wrong source correct ref was found. q-15292 and q-15297 have no captured correct ref, solution or difficulty: public raw replay preserves these omissions and marks evidence-only. Their independently derived correct equations are metadata, never counted as matched designations. Explicit normal authored completion with the same observed profile supplies a supported correct ref and full solution for native grading. Original MA lesson JSON confirms five-choice radio widgets and the same complete banks; it also has no worked solution or captured key for those two questions.

Raw prompts preserve legacy diameter notation XY^(―) / overset{―}{XY}; defaults use overline{XY}. This is a notation choice for authored presentation, not a mathematical repair. Exact originals reuse their immutable source assets. Every changed parameter set receives its own new geometry and matching labels. No observed scalar distractor here needs a fitted/opaque replay polynomial.
