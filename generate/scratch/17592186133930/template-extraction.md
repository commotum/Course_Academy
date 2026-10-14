# Template extraction

## 1. Describe each question before generalization

### q-162410 (db17592186134137; observed moderate)

Field: $x\,i+xz\,j+3z\,k.$. Geometry: `('sphere', 5, (0, 2, -1))`. Held-coordinate component derivatives: `[1, 0, 3]`.

Full original problem and complete fixed worked solution are in source.json and replayed side by side in review.md. Source theorem block → formal ordered partial derivatives → three evaluated contributions (including zero terms) → constant reduction → triple integral → constant factored out → constant times Volume(R) → numerical volume formula → final exact flux.

### q-162411 (db17592186134138; observed easy)

Field: $⟨{z}^{2},\,2y,\,{x}^{2}+y⟩$. Geometry: `('cylinder', 1, 2, 'z')`. Held-coordinate component derivatives: `[0, 2, 0]`.

Full original problem and complete fixed worked solution are in source.json and replayed side by side in review.md. Source theorem block → formal ordered partial derivatives → three evaluated contributions (including zero terms) → constant reduction → triple integral → constant factored out → constant times Volume(R) → numerical volume formula → final exact flux.

### q-162569 (db17592186281499; observed easy)

Field: $⟨x-y,\,y+z,\,2x-3z⟩$. Geometry: `('cylinder', 2, 3, 'x')`. Held-coordinate component derivatives: `[1, 1, -3]`.

Full original problem and complete fixed worked solution are in source.json and replayed side by side in review.md. Source theorem block → formal ordered partial derivatives → three evaluated contributions (including zero terms) → constant reduction → triple integral → constant factored out → constant times Volume(R) → numerical volume formula → final exact flux.

### q-162572 (db17592186281500; observed easy)

Field: $⟨3x+y{e}^{z},\,xy+2,\,1-xz⟩$. Geometry: `('box', 1, 2, 3)`. Held-coordinate component derivatives: `[3, x, -x]`.

Full original problem and complete fixed worked solution are in source.json and replayed side by side in review.md. Source theorem block → formal ordered partial derivatives → three evaluated contributions (including zero terms) → constant reduction → triple integral → constant factored out → constant times Volume(R) → numerical volume formula → final exact flux.

### q-162578 (db17592186281501; observed moderate)

Field: $z\,i+6y\,j+(x+3z)\,k.$. Geometry: `('sphere', 2, (0, 0, 4))`. Held-coordinate component derivatives: `[0, 6, 3]`.

Full original problem and complete fixed worked solution are in source.json and replayed side by side in review.md. Source theorem block → formal ordered partial derivatives → three evaluated contributions (including zero terms) → constant reduction → triple integral → constant factored out → constant times Volume(R) → numerical volume formula → final exact flux.

### q-162580 (db17592186281502; observed moderate)

Field: $({y}^{2}-{x}^{2})\,i+4y\,j+2xz\,k.$. Geometry: `('sphere', 1, (-2, 1, 0))`. Held-coordinate component derivatives: `[-2*x, 4, 2*x]`.

Full original problem and complete fixed worked solution are in source.json and replayed side by side in review.md. Source theorem block → formal ordered partial derivatives → three evaluated contributions (including zero terms) → constant reduction → triple integral → constant factored out → constant times Volume(R) → numerical volume formula → final exact flux.

### q-162570 (db17592186374186; observed easy)

Field: $⟨1-2x,\,5y-3{z}^{2},\,{x}^{3}-{y}^{2}⟩$. Geometry: `('cylinder', 3, 2, 'y')`. Held-coordinate component derivatives: `[-2, 5, 0]`.

Full original problem and complete fixed worked solution are in source.json and replayed side by side in review.md. Source theorem block → formal ordered partial derivatives → three evaluated contributions (including zero terms) → constant reduction → triple integral → constant factored out → constant times Volume(R) → numerical volume formula → final exact flux.

### q-162571 (db17592186374193; observed easy)

Field: $⟨3x-y{z}^{2},\,y+{e}^{z},\,2y\operatorname{sin}⁡x⟩$. Geometry: `('box', 1, 2, 1)`. Held-coordinate component derivatives: `[3, 1, 0]`.

Full original problem and complete fixed worked solution are in source.json and replayed side by side in review.md. Source theorem block → formal ordered partial derivatives → three evaluated contributions (including zero terms) → constant reduction → triple integral → constant factored out → constant times Volume(R) → numerical volume formula → final exact flux.

### q-162573 (db17592186430949; observed easy)

Field: $⟨y-z,\,y-2x,\,x+4z⟩$. Geometry: `('box', 4, 2, 2)`. Held-coordinate component derivatives: `[0, 1, 4]`.

Full original problem and complete fixed worked solution are in source.json and replayed side by side in review.md. Source theorem block → formal ordered partial derivatives → three evaluated contributions (including zero terms) → constant reduction → triple integral → constant factored out → constant times Volume(R) → numerical volume formula → final exact flux.

### q-162574 (db17592186430951; observed moderate)

Field: $(yz-2x)\,i+3y\,j+(x+z)\,k.$. Geometry: `('sphere', 3, (0, 2, 0))`. Held-coordinate component derivatives: `[-2, 3, 1]`.

Full original problem and complete fixed worked solution are in source.json and replayed side by side in review.md. Source theorem block → formal ordered partial derivatives → three evaluated contributions (including zero terms) → constant reduction → triple integral → constant factored out → constant times Volume(R) → numerical volume formula → final exact flux.

## 2. Generalize

Compute ∂P/∂x+∂Q/∂y+∂R/∂z while holding other coordinates fixed. The result is constant even where cross terms cancel. Recognize the already-known closed solid, then multiply by its geometric volume. All source operative prose, source ordering of the formal derivative components, factorization and volume stages are retained. No antiderivative stages are added.

## 3. Components and complete observed banks

Each original value below is preserved byte-for-byte at k=1. Public raw profiles use parameterized homogeneous field scaling: each complete observed value v maps to kv. This is an evidence scaling relation, not a recovered explanation of its wrong operation. All historical wrong-operation interpretations remain opaque; none of these banks enters default learning generation. The correct value follows actual scaled differentiation and unchanged volume.

### raw-q-162410

Field0: key `selection`; radio; correct attribute present.

| Captured value | Complete parameter recipe | Designation |
|---|---|---|

| $\frac{16\pi }{3}$ | $k\left(\frac{16\pi }{3}\right)$ | wrong |

| $\frac{25{\pi }^{2}}{4}$ | $k\left(\frac{25{\pi }^{2}}{4}\right)$ | wrong |

| $\frac{2\,000\pi }{3}$ | $k\left(\frac{2\,000\pi }{3}\right)$ | correct |

| $\frac{400\pi }{3}$ | $k\left(\frac{400\pi }{3}\right)$ | wrong |

| $\frac{800\pi }{3}$ | $k\left(\frac{800\pi }{3}\right)$ | wrong |

### raw-q-162411

Field0: key `selection`; radio; correct attribute **absent (legacy)**.

| Captured value | Complete parameter recipe | Designation |
|---|---|---|

| $\frac{π}{2}$ | $k\left(\frac{π}{2}\right)$ | unrecorded |

| $2π$ | $k\left(2π\right)$ | unrecorded |

| $6π$ | $k\left(6π\right)$ | unrecorded |

| $\frac{4π}{3}$ | $k\left(\frac{4π}{3}\right)$ | unrecorded |

| $4π$ | $k\left(4π\right)$ | unrecorded |

Field1: key `selection`; radio; correct attribute present.

| Captured value | Complete parameter recipe | Designation |
|---|---|---|

| $4\pi $ | $k\left(4\pi \right)$ | correct |

| $\frac{4\pi }{3}$ | $k\left(\frac{4\pi }{3}\right)$ | wrong |

| $\frac{\pi }{2}$ | $k\left(\frac{\pi }{2}\right)$ | wrong |

| $6\pi $ | $k\left(6\pi \right)$ | wrong |

| $2\pi $ | $k\left(2\pi \right)$ | wrong |

### raw-q-162569

Field0: key `selection`; radio; correct attribute present.

| Captured value | Complete parameter recipe | Designation |
|---|---|---|

| $4\pi $ | $k\left(4\pi \right)$ | wrong |

| $-12\pi $ | $k\left(-12\pi \right)$ | correct |

| $-16\pi $ | $k\left(-16\pi \right)$ | wrong |

| $6\pi $ | $k\left(6\pi \right)$ | wrong |

| $-8\pi $ | $k\left(-8\pi \right)$ | wrong |

### raw-q-162572

Field0: key `selection`; radio; correct attribute present.

| Captured value | Complete parameter recipe | Designation |
|---|---|---|

| $18$ | $k\left(18\right)$ | correct |

| $24$ | $k\left(24\right)$ | wrong |

| $21$ | $k\left(21\right)$ | wrong |

| $16$ | $k\left(16\right)$ | wrong |

| $12$ | $k\left(12\right)$ | wrong |

### raw-q-162578

Field0: key `selection`; radio; correct attribute present.

| Captured value | Complete parameter recipe | Designation |
|---|---|---|

| $64\pi $ | $k\left(64\pi \right)$ | wrong |

| $\frac{128\pi }{3}$ | $k\left(\frac{128\pi }{3}\right)$ | wrong |

| $\frac{256\pi }{3}$ | $k\left(\frac{256\pi }{3}\right)$ | wrong |

| $96\pi $ | $k\left(96\pi \right)$ | correct |

| $78\pi $ | $k\left(78\pi \right)$ | wrong |

### raw-q-162580

Field0: key `selection`; radio; correct attribute present.

| Captured value | Complete parameter recipe | Designation |
|---|---|---|

| $12\pi $ | $k\left(12\pi \right)$ | wrong |

| $\frac{8\pi }{3}$ | $k\left(\frac{8\pi }{3}\right)$ | wrong |

| $\frac{32\pi }{3}$ | $k\left(\frac{32\pi }{3}\right)$ | wrong |

| $18\pi $ | $k\left(18\pi \right)$ | wrong |

| $\frac{16\pi }{3}$ | $k\left(\frac{16\pi }{3}\right)$ | correct |

### raw-q-162570

Field0: key `selection`; radio; correct attribute present.

| Captured value | Complete parameter recipe | Designation |
|---|---|---|

| $32\pi $ | $k\left(32\pi \right)$ | wrong |

| $54\pi $ | $k\left(54\pi \right)$ | correct |

| $64\pi $ | $k\left(64\pi \right)$ | wrong |

| $27\pi $ | $k\left(27\pi \right)$ | wrong |

| $48\pi $ | $k\left(48\pi \right)$ | wrong |

### raw-q-162571

Field0: key `selection`; radio; correct attribute present.

| Captured value | Complete parameter recipe | Designation |
|---|---|---|

| $10$ | $k\left(10\right)$ | wrong |

| $8$ | $k\left(8\right)$ | correct |

| $4$ | $k\left(4\right)$ | wrong |

| $-2$ | $k\left(-2\right)$ | wrong |

| $-6$ | $k\left(-6\right)$ | wrong |

### raw-q-162573

Field0: key `selection`; radio; correct attribute present.

| Captured value | Complete parameter recipe | Designation |
|---|---|---|

| $50$ | $k\left(50\right)$ | wrong |

| $42$ | $k\left(42\right)$ | wrong |

| $80$ | $k\left(80\right)$ | correct |

| $64$ | $k\left(64\right)$ | wrong |

| $96$ | $k\left(96\right)$ | wrong |

### raw-q-162574

Field0: key `selection`; radio; correct attribute present.

| Captured value | Complete parameter recipe | Designation |
|---|---|---|

| $81\pi $ | $k\left(81\pi \right)$ | wrong |

| $72\pi $ | $k\left(72\pi \right)$ | correct |

| $64\pi $ | $k\left(64\pi \right)$ | wrong |

| $36\pi $ | $k\left(36\pi \right)$ | wrong |

| $48\pi $ | $k\left(48\pi \right)$ | wrong |

## 4. Reusable masks, domains and authored banks

Prompt masks replace whole field formulas and whole sphere equations; diagram labels/height/radius are complete slots. Divergence and flux blocks are complete structured masks with the same source stages. At observed slots, each slot retains its original notation and whitespace. Changed slots use exact SymPy values; source theorem/prose remains unchanged. k multiplies each complete component, so all held-coordinate derivative terms are scaled together; this extension does not claim independent coefficient recovery. It preserves each source expression inside visible parentheses when k is not1.

Normal default bank chooses the family before parameters and uses all five fixed operations below; no per-option replacement occurs. Let D be the actual constant divergence, V the actual volume. Every whole bank rejects equivalence, including coincidences with the correct scalar.

| Solid | Complete bank in fixed recipe order |
|---|---|
| Sphere radius r | DV; -DV (orientation reversal); V (omit divergence); D(4πr²/3) (use area power instead of volume power); D(4πr³) (omit /3) |
| Cylinder r,h | DV; -DV; V; Dπrh (omit radius factor); Dπr² (omit height) |
| Box a,b,c | DV; -DV; V; Dab (omit c); Dac (omit b) |

Bounds apply to explicit input and sampling alike; see README.md. Sphere radii2..5 are anchored to observed radii1,2,3,5, with radius1 retained only in evidence because this authored complete bank degenerates there. Easy lengths are integer1..4 or radius/height2..4, within observed dimension forms. Normal choices remain signed because physical flux can be negative; there is no positivity rule for flux. The seed selects family, parameters and shuffle; order changes do not alter identity.

Hard authored field is `(y²-a x²+2bxy, cy-by²,2axz)` with a,b1..3,c2..6; its ordered partials `-2ax+2by`, `c-2by`, `2ax` sum to c. This adds one cancellation pair to the q162580 method, with fixed degree and bounded coefficients. Hard has independently meaningful coefficient triples and four radii; center translation is excluded from mathematical-task counts.

Incidental sphere centers are retained in content identity and geometry validation but excluded from mathematical fingerprints. Catalog sizes are enumerated in validation.json without counting option order, raw profiles or variable-letter aliases. Historical raw bank scaling is intentionally unavailable for defaults. Source key-presence comparison includes missing correct refs; omission is not converted to a fabricated designation.
