# Extracted transformations and complete source banks

The supplied object is an unchanged graph with two labeled extrema. The response is one coordinate pair. Choose the original extremum that becomes the requested minimum/maximum, map its horizontal coordinate, then apply vertical scaling/reflection/translation in the source worked-solution order. Positive vertical factors preserve extrema type; reflection exchanges it. All horizontal factors remain positive. Local/global scope stays with each graph.

Fixed components: source graph bytes, scope, number of choices, field key/type, transformation mask and solution stage count. These preserve the supplied graph, grading contract and assessed method. Variable slots: requested extremum (minimum or maximum), both nonzero signed shifts in [-5,-1] ∪ [1,5], positive scale from {1/3,1/2,2,3,4} for easy and {2,3,4} for moderate. Horizontal and vertical scales are independent only where the source mask includes both. Reflection remains present in all moderate masks and absent in easy masks. Zero shifts and unit scales are excluded to prevent stage collapse; this is a narrower sampling policy, not a source fact.

Let `(x,y)` denote the selected original extremum and `(u,v)` the other extremum. Transform $y=a f(t x+h)+k$ maps a point to $((x-h)/t,a y+k)$. The bank expressions below are observed value patterns, not claims about learner misconceptions. Every expression is parameterized; opaque compound/cross-coordinate patterns retain their explicit arithmetic rather than being replaced. Uniqueness and incorrectness are rechecked for the entire bank. These conservative same-method generalizations are separate from original replay parameters.

## q-121221

![](images/1e/1eb29eb3eb3627e24a23d7315295a1d889308d67895f9b798dbf9dd71ba226df.png)

The diagram above shows the local minimum and maximum of the function $y=f(x).$ What is the local maximum of $y=f(x-2)+1?$

Source extrema: minimum [-1, 1], maximum [2, 3]. Original parameters: `{"h": -2, "k": 1, "target": "maximum"}`. Template: `shift_shift`.

| Observed coordinate | Recipe | Designation |
|---|---|---|
| `(3,5)` | `(x+k,y-h)` | distractor |
| `(4,4)` | `(x-h,y+k)` | correct |
| `(5,3)` | `(y-h,x+k)` | distractor |
| `(3,2)` | `(x+k,y-k)` | distractor |
| `(0,4)` | `(x+h,y+k)` | distractor |

Solution stages: hshift, vshift. Original and generated solutions are side by side in review.md. Opening/connective prose, redundant spaces, fraction spelling and trailing option punctuation are normalized; not reported as byte-exact source fidelity. The q-211303 opening lists reflection before stretch, while its worked coordinate steps stretch then reflect. The generator consistently follows its worked coordinate sequence; these two commuting operations yield the same point.

## q-211288

![](images/09/09193a765398280ec967a89b97b6dbdf2fb0700e0bb0d8157f966cda5c7534f9.png)

The diagram above shows the global minimum and maximum of the function $y=f(x).$ What is the global minimum of $y=\frac{1}{2}f(x-5)?$

Source extrema: minimum [-2, -4], maximum [2, 2]. Original parameters: `{"h": -5, "s": "1/2", "target": "minimum"}`. Template: `shift_scale`.

| Observed coordinate | Recipe | Designation |
|---|---|---|
| `(3,-2)` | `(x-h,s*y)` | correct |
| `(-7,-2)` | `(x+h,s*y)` | distractor |
| `(-7,-8)` | `(x+h,y/s)` | distractor |
| `(3,-8)` | `(x-h,y/s)` | distractor |
| `(-1,1)` | `(s*x,s*v)` | distractor |

Solution stages: hshift, vscale. Original and generated solutions are side by side in review.md. Opening/connective prose, redundant spaces, fraction spelling and trailing option punctuation are normalized; not reported as byte-exact source fidelity. The q-211303 opening lists reflection before stretch, while its worked coordinate steps stretch then reflect. The generator consistently follows its worked coordinate sequence; these two commuting operations yield the same point.

## q-186866

![](images/f4/f4da78b7a12ed475b64c1f824e8cecdf36657c6d174f0db770219fd8dd6c0801.png)

The diagram above shows the global minimum and maximum of the function $y=f(x).$ What is the global minimum of $y=-2f(x+1)?$

Source extrema: minimum [2, -3], maximum [-1, 4]. Original parameters: `{"h": 1, "s": 2, "target": "minimum"}`. Template: `shift_scale_flip`.

| Observed coordinate | Recipe | Designation |
|---|---|---|
| `(-2,-8)` | `(x-h,-s*y)` | correct |
| `(3,-4)` | `(u+h,-y)` | distractor |
| `(-2,8).` | `(x-h,s*y)` | distractor |
| `(0,-4)` | `(x+h,-y)` | distractor |
| `(2,8).` | `(-x+h,s*y)` | distractor |

Solution stages: hshift, vscale, flip. Original and generated solutions are side by side in review.md. Opening/connective prose, redundant spaces, fraction spelling and trailing option punctuation are normalized; not reported as byte-exact source fidelity. The q-211303 opening lists reflection before stretch, while its worked coordinate steps stretch then reflect. The generator consistently follows its worked coordinate sequence; these two commuting operations yield the same point.

## q-211303

![](images/ff/ff2956aa2885a0abddd614a11e632d3dfd1114391a9d7e27d790746c159e7f79.png)

The diagram above shows the local minimum and maximum of the function $y=f(x).$ What is the local maximum of $y=-3f(x)-1?$

Source extrema: minimum [4, -1], maximum [-3, 6]. Original parameters: `{"s": 3, "k": -1, "target": "maximum"}`. Template: `scale_flip_shift`.

| Observed coordinate | Recipe | Designation |
|---|---|---|
| `(4,2)` | `(x,-s*y+k)` | correct |
| `(-4,2)` | `(-x,-s*y+k)` | distractor |
| `(1,0)` | `(x-s,y-k)` | distractor |
| `(4,-5)` | `(x,s*y+2*k)` | distractor |
| `(1,-5)` | `(x-s,s*y+2*k)` | distractor |

Solution stages: vscale, flip, vshift. Original and generated solutions are side by side in review.md. Opening/connective prose, redundant spaces, fraction spelling and trailing option punctuation are normalized; not reported as byte-exact source fidelity. The q-211303 opening lists reflection before stretch, while its worked coordinate steps stretch then reflect. The generator consistently follows its worked coordinate sequence; these two commuting operations yield the same point.

## q-211462

![](images/80/8000655c1943c60282d8844a2ae965b6415e21962c44309cd68806f04744b806.png)

The diagram above shows the global minimum and maximum of the function $y=f(x).$ What is the global maximum of $y=-f(2x)+3?$

Source extrema: minimum [2, 3], maximum [-4, 9]. Original parameters: `{"t": 2, "k": 3, "target": "maximum"}`. Template: `hscale_flip_shift`.

| Observed coordinate | Recipe | Designation |
|---|---|---|
| `(4,6)` | `(x*t,y+k)` | distractor |
| `(4,0)` | `(x*t,-y+k)` | distractor |
| `(1,0)` | `(x/t,-y+k)` | correct |
| `(1,-3)` | `(x/t,-y)` | distractor |
| `(2,6)` | `(x,y+k)` | distractor |

Solution stages: hscale, flip, vshift. Original and generated solutions are side by side in review.md. Opening/connective prose, redundant spaces, fraction spelling and trailing option punctuation are normalized; not reported as byte-exact source fidelity. The q-211303 opening lists reflection before stretch, while its worked coordinate steps stretch then reflect. The generator consistently follows its worked coordinate sequence; these two commuting operations yield the same point.

## q-211465

![](images/1e/1eb29eb3eb3627e24a23d7315295a1d889308d67895f9b798dbf9dd71ba226df.png)

The diagram above shows the local minimum and maximum of the function $y=f(x).$ What is the local minimum of 
$y=-f(x-1)-2?$

Source extrema: minimum [-1, 1], maximum [2, 3]. Original parameters: `{"h": -1, "k": -2, "target": "minimum"}`. Template: `shift_flip_shift`.

| Observed coordinate | Recipe | Designation |
|---|---|---|
| `(3,-2)` | `(x-h,k)` | distractor |
| `(-3,1)` | `(-(x-h),v)` | distractor |
| `(3,-5)` | `(x-h,-y+k)` | correct |
| `(2,-5)` | `(x,-y+k)` | distractor |
| `(2,1)` | `(x,v)` | distractor |

Solution stages: hshift, flip, vshift. Original and generated solutions are side by side in review.md. Opening/connective prose, redundant spaces, fraction spelling and trailing option punctuation are normalized; not reported as byte-exact source fidelity. The q-211303 opening lists reflection before stretch, while its worked coordinate steps stretch then reflect. The generator consistently follows its worked coordinate sequence; these two commuting operations yield the same point.

## q-211466

![](images/2d/2d046da9a89fe09f09dbd5e0658422ab8ccee8db680a2955ebe1ff0f361b5c35.png)

The diagram above shows the global minimum and maximum of the function $y=f(x).$ What is the global minimum of 
$y=-4f(3x)?$

Source extrema: minimum [-3, -2], maximum [3, 1]. Original parameters: `{"t": 3, "s": 4, "target": "minimum"}`. Template: `hscale_scale_flip`.

| Observed coordinate | Recipe | Designation |
|---|---|---|
| `(1,3)` | `(x/t,x)` | distractor |
| `(3,1)` | `(x,y)` | distractor |
| `(1,-4)` | `(x/t,-s*y)` | correct |
| `(3,-4)` | `(x,-s*y)` | distractor |
| `(0,3)` | `(0,x)` | distractor |

Solution stages: hscale, vscale, flip. Original and generated solutions are side by side in review.md. Opening/connective prose, redundant spaces, fraction spelling and trailing option punctuation are normalized; not reported as byte-exact source fidelity. The q-211303 opening lists reflection before stretch, while its worked coordinate steps stretch then reflect. The generator consistently follows its worked coordinate sequence; these two commuting operations yield the same point.

## q-211467

![](images/d8/d8d23cf36bc9fb526c0e6d041b72e6b378638f662b67aae63531c66b4a8cd6c5.png)

The diagram above shows the local minimum and maximum of the function $y=f(x).$ What is the local maximum of $y=-f(x+2)+4?$

Source extrema: minimum [1, -4], maximum [-2, -1]. Original parameters: `{"h": 2, "k": 4, "target": "maximum"}`. Template: `shift_flip_shift`.

| Observed coordinate | Recipe | Designation |
|---|---|---|
| `(2,0)` | `(h,y+k)` | distractor |
| `(2,5)` | `(h,-v+k)` | distractor |
| `(-1,8)` | `(x-h,-y+k)` | correct |
| `(3,8)` | `(x+h,-y+k)` | distractor |
| `(-1,0)` | `(x-h,y+k)` | distractor |

Solution stages: hshift, flip, vshift. Original and generated solutions are side by side in review.md. Opening/connective prose, redundant spaces, fraction spelling and trailing option punctuation are normalized; not reported as byte-exact source fidelity. The q-211303 opening lists reflection before stretch, while its worked coordinate steps stretch then reflect. The generator consistently follows its worked coordinate sequence; these two commuting operations yield the same point.

## Fieldless evidence

q-211287 (two translations), q-211304 (horizontal scale then vertical shift), q-211305 (horizontal scale then vertical scale), q-211461 (vertical scale then shift) retain their original absence of fields. Their prompt and final answer are independently verified in validation.json. No authored completion is committed. q-211287 supplies additional evidence for the complete translation backbone; the other three masks are excluded from production pending a verified response contract.

## Fidelity limits

All 8 supported source profiles reproduce the entire mathematical bank and correct designation at original parameters: 40/40 choices, 32/32 distractors. Two q-186866 distractors carry a literal trailing period; the normalized math values omit it. Every supported profile is exhaustively checked at every declared parameter and both eligible targets. Bank-invalid inputs are excluded rather than dropping or pooling choices.
