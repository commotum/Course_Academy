# Template extraction (step 4)

Frozen snapshot and owning curriculum: math basis 1356, topic 1934 The Gradient Vector; prerequisite Introduction to Partial Derivatives (1929). Lesson route follows activity/first-step 17592186125274 then step/next: introduction, this two-variable KP, three-variable gradient, zero-gradient points, properties of gradient. Directional derivatives and normal-vector geometry are downstream separate topics. No branch or within-level progression is introduced.

## Stage 1: Specific source observations

### q-35990: polynomial (:question.difficulty/easy)

Evaluate $∇h(x,y)$ at $(2,3)$ if $h(x,y)=4{x}^{2}-3xy+2{y}^{2}+y.$

Original parameters: `{"a": 4, "b": -3, "c": 2, "d": 1, "u": 2, "v": 3}`. Original solution: present with exact family chain.

Layout: 2 source fields.

Field 0: `selection`, `:answer-field.type/radio`. Correct designation **absent**.

1. `16i + 12j`

2. `9i - 6j`

3. `7i + 7j`

4. `9i + 12j`

5. `16i + 6j`

Field 1: `selection`, `:answer-field.type/radio`. Correct designation present.

1. `7\text{ }i+7\text{ }j` (original correct)

2. `16\text{ }i+12\text{ }j`

3. `9\text{ }i-6\text{ }j`

4. `9\text{ }i+12\text{ }j`

5. `16\text{ }i+6\text{ }j`

### q-36909: root (:question.difficulty/easy)

Evaluate $∇f(x,y)$ at $(2,1)$ if $f(x,y)={x}^{2}\sqrt{y+3}.$

Original parameters: `{"c": 3, "u": 2, "v": 1}`. Original solution: present with exact family chain.

Layout: 1 source fields.

Field 0: `selection`, `:answer-field.type/radio`. Correct designation present.

1. `⟨4,\,\frac{1}{2}⟩`

2. `⟨2,\,0⟩`

3. `⟨1,\,8⟩`

4. `⟨16,\,1⟩`

5. `⟨8,\,1⟩` (original correct)

### q-36910: log_cos (:question.difficulty/easy)

Given  $g(x,y)=\operatorname{ln}⁡(xy)+\operatorname{cos}⁡({y}^{2})$, find $∇g(x,y).$

Original parameters: `{"n": 2, "a": 1, "b": 1}`. Original solution: present with exact family chain.

Layout: 1 source fields.

Field 0: `selection`, `:answer-field.type/radio`. Correct designation present.

1. `x\text{ }i+(y-2\operatorname{sin}⁡({y}^{2}))\text{ }j`

2. `\frac{1}{x}\text{ }i+(\frac{1}{y}-2y\operatorname{sin}⁡({y}^{2}))\text{ }j` (original correct)

3. `\frac{1}{x}\text{ }i+(\frac{1}{y}+2y\operatorname{sin}⁡y)\text{ }j`

4. `\frac{1}{x}\text{ }i+\frac{1}{y}\text{ }j`

5. `\frac{1}{x}\text{ }i+2y(\frac{1}{y}-\operatorname{sin}⁡({y}^{2}))\text{ }j`

### q-71350: sin_log (:question.difficulty/easy)

Given  $f(x,y)=\operatorname{sin}⁡(xy)+{x}^{2}\operatorname{ln}⁡y$, find $∇f(x,y).$

Original parameters: `{"n": 2, "a": 1, "b": 1}`. Original solution: present with exact family chain.

Layout: 1 source fields.

Field 0: `selection`, `:answer-field.type/radio`. Correct designation present.

1. `(y\operatorname{sin}⁡(xy)+2x\operatorname{ln}⁡y)\text{ }i+(x\operatorname{sin}⁡(xy)+\frac{{x}^{2}}{y})\text{ }j`

2. `(x\operatorname{cos}⁡(xy)+2x\operatorname{ln}⁡y)\text{ }i+(y\operatorname{cos}⁡(xy)+\frac{{x}^{2}}{y})\text{ }j`

3. `y\operatorname{cos}⁡(xy)\text{ }i+\frac{{x}^{2}}{y}\text{ }j`

4. `(x\operatorname{sin}⁡(xy)+2x\operatorname{ln}⁡y)\text{ }i+(y\operatorname{sin}⁡(xy)+\frac{{x}^{2}}{y})\text{ }j`

5. `(y\operatorname{cos}⁡(xy)+2x\operatorname{ln}⁡y)\text{ }i+(x\operatorname{cos}⁡(xy)+\frac{{x}^{2}}{y})\text{ }j` (original correct)

### q-36005: atan_product (:question.difficulty/moderate)

Evaluate $∇h(x,y)$ at $(1,1)$ if $h(x,y)=4x\operatorname{arctan}⁡y.$

Original parameters: `{"a": 4, "u": 1, "v": 1}`. Original solution: present with exact family chain.

Layout: 1 source fields.

Field 0: `selection`, `:answer-field.type/radio`. Correct designation present.

1. `⟨\pi ,\,\frac{1}{2}⟩`

2. `⟨1,\,1⟩`

3. `⟨2\pi ,\,0⟩`

4. `⟨\pi ,\,2⟩` (original correct)

5. `⟨\frac{\pi }{4},\,\frac{1}{2}⟩`

### q-36009: radial_log (:question.difficulty/moderate)

Evaluate the gradient of $g(x,y)$ at the point $(\frac{1}{2},0)$ if $g(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}).$

Original parameters: `{"u": "1/2", "v": 0}`. Original solution: present with exact family chain.

Layout: 1 source fields.

Field 0: `selection`, `:answer-field.type/radio`. Correct designation present.

1. `⟨4,\,0⟩` (original correct)

2. `⟨\frac{1}{2},\,\frac{1}{2}⟩`

3. `⟨8,\,0⟩`

4. `⟨\frac{1}{2},\,0⟩`

5. `⟨8,\,\frac{1}{2}⟩`

### q-127650: atan_ratio (:question.difficulty/moderate)

If $h(x,y)=\operatorname{arctan}⁡(\frac{y}{x}),$ find $∇h(x,y).$

Original parameters: `{"k": 1}`. Original solution: present with exact family chain.

Layout: 1 source fields.

Field 0: `selection`, `:answer-field.type/radio`. Correct designation present.

1. `-\frac{x}{{x}^{2}+{y}^{2}}\,i+\frac{y}{{x}^{2}+{y}^{2}}\,j`

2. `\frac{x}{{x}^{2}+{y}^{2}}\,i-\frac{y}{{x}^{2}+{y}^{2}}\,j`

3. `-\frac{{y}^{2}}{{x}^{2}+{y}^{2}}\,i+\frac{{x}^{2}}{{x}^{2}+{y}^{2}}\,j`

4. `-\frac{y}{{x}^{2}+{y}^{2}}\,i+\frac{x}{{x}^{2}+{y}^{2}}\,j` (original correct)

5. `\frac{y}{{x}^{2}+{y}^{2}}\,i-\frac{x}{{x}^{2}+{y}^{2}}\,j`

### q-35988: quotient (unrated)

Given $f(x, y) = \frac{3x + 2y}{x - y}$, find $∇f(x, y)$.

Original parameters: `{"a": 3, "b": 2, "k": 1}`. Original solution: absent; public raw replay omits it.

Layout: 1 source fields.

Field 0: `selection`, `:answer-field.type/radio`. Correct designation **absent**.

1. `- (5)/((x - y)^{2})(yi - xj)`

2. `- (5)/((x - y)^{2})(xi - yj)`

3. `(5)/((x - y)^{2})(yi + xj)`

4. `-5(xi - yj)`

5. `-5(yi - xj)`

### q-168115: components (:question.difficulty/moderate)

Find the direction of the greatest rate of expansion of the fluid at the point $(1,1).$ Do not normalize the answer.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        The required direction is $∇(\text{div}\,V)\,{|}_{(1,\,1)}=⟨$

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$,$

                                    
                                
                                    
                            
                                        {{field-2}}                
                                    
                                
                                    
                                        
                                        
$⟩.$

Original parameters: `{"u": 1, "v": 1, "P": 4, "Q": 2}`. Original solution: present with exact family chain.

Layout: 2 source fields.

Field 0: `field-1`, `:answer-field.type/blank`. Correct designation present.

1. `4` (original correct)

Field 1: `field-2`, `:answer-field.type/blank`. Correct designation present.

1. `2` (original correct)

## Stage 2: Generalized shared pattern

Compute each coordinate partial with the other coordinate held fixed; form its vector in the original basis/tuple notation; when a point is supplied substitute only after obtaining symbolic components. The contextual source simply assembles previously known scalar partials. Every family keeps its own common prose and ordered formal/operator, chain/product, reduction, substitution and conclusion rows.

## Stage 3: Components and complete banks

Each list below is an entire bank chosen before parameter sampling. A,B denote the correct x,y components at the requested point, or symbolically if no point. No individual option is replaced after a collision; the whole sampled instance is rejected. Source intent inferred from operation shapes is not asserted to be recovered author code.

- polynomial: (2au,2cv), (-bv,bu), correct, (-bv,2cv), (2au,2cv+bu). The first omits cross and linear terms; the second retains cross terms with an x sign error; fourth combines those omissions; fifth omits x cross and y linear. Raw repeats this complete bank in both source fields; normal removes the legacy field.

- root raw: (A/2,B/2), (u,0), (B,A), (2A,B), correct. Historical errors are underdetermined; ineligible replay only. Authored normal: correct, (A/2,B) omit power factor, (A,2B) omit square-root factor 2, swap, negate y derivative.

- log_cos: (a x,a y-b n sin(y^n)), correct, (a/x,a/y+b n y^(n-1) sin y), (a/x,a/y), (a/x,n y^(n-1)(a/y-b sin(y^n))). These encode reciprocal omission/inner derivative omission, sign plus wrong inner argument, omitted cosine derivative, and overapplying the inner derivative to the log term.

- sin_log: replace cos by sin in both chain terms; swap held-coordinate multipliers x/y in trig terms; omit x power-log term and y trig term; combine swapped multipliers with retained sin; correct. Both a and b apply to their own entire original terms.

- atan_product raw: (A,B/a), (u,v), (2A,0), correct, (A/a,B/a). Scalar source values cannot establish source intended error operations (especially coordinates and 2A,0). Authored normal: correct, omit a in x, omit a in y, swap components, wrong sign x.

- radial_log raw: correct, (u,u), (2/u²,0), (u,v), (2/u²,u). Only original numerical pattern is supported, not recovered intent. Authored normal: correct, omit inner factor 2, apply inner factor twice, swap, wrong sign x.

- atan_ratio: wrong held-coordinate swap with x negative; swapped with y negative; erroneously squared numerator coordinates; correct; negate both true components. With k: denominator k²x²+y² and correct (-k y/den,k x/den); every original option receives that same denominator and applicable k.

- quotient: correct -(ak+b)/(x-ky)² (y,-x); swap x,y; wrong x sign in correct shape; omit quotient denominator with swapped coordinates; omit denominator in correct coordinates. The absent original designation is independently inferred but not inserted in raw.

- components: the two scalar blanks P,Q, no added distractors. Raw prompt depends on unseen prior parts; normal explicitly supplies partials.

- authored hard quotient: correct; omit both negative denominator-derivative terms; change x quotient subtraction to addition; change y quotient subtraction to addition; swap components. Wrong operations use the actual printed numerator and denominator before point evaluation.

## Stage 4: Reusable masks, constraints and authorship

`observed_mask` compiles complete family expressions, derivative/evaluation rows and coordinate tuples into one-pass slots. It does not branch to return a literal source record at original params. Shared prose and stage omission choices remain in the source skeleton. Raw original worked solutions are compared as complete exact strings; bank choices are independently parsed and matched one-to-one as vectors. Learner-attribute key-presence parity is checked separately from newly owned generated identities; original IDs/database refs remain in source.json. `normal_solution` repairs h/f notation, supplies the contextual source scalar partials, and adds the missing quotient solution; these are separate authored additions.

Parameters and explicit-call bounds: polynomial signed nonzero a,b,c,d magnitude≤6 and nonzero u,v magnitude≤4; sampled coefficients a,c positive, b negative, d±1/±2. Root shift c=1..24, u nonzero magnitude≤5, v=-4..9, v+c in {4,9,16,25}; samples guarantee that same perfect-square evaluation workload. Log/trig powers n=2..6 and coprime a,b=1..6. Atan product a=2..8, u nonzero magnitude≤5, v=±1. Radial log u any reduced nonzero rational with |numerator|≤8, denominator≤8, v=0. Atan and linear quotient k positive primitive rational with numerator/denominator≤8; quotient a,b=1..8. Scalar component assembly P,Q nonzero magnitude≤8, location -4..4 (location excluded from mathematical fingerprint). Hard a=1..5,b=1..4,u,v=1..4, all terms and denominator positive and active.

Hard is an authored difficulty claim: f=(x²y+a y²)/(x+b y), evaluated at (u,v). Both coordinate derivatives require a quotient subtraction; the numerator x derivative has 2xy, while its y derivative has x²+2ay. Both nonzero coordinate substitutions remain active. These are the same held-coordinate first partials and vector assembly taught by prerequisite 1929 and the canonical (x-y)cos y evaluation. No gradient product-property identity, optimization, geometry, normalization or directional derivative is asked. Its greater bookkeeping is simultaneous in every hard instance; there is no progression within the level.

Meaningful bounded domains: each symbolic log/trig family has 5 powers × 23 coprime coefficient pairs = 115 scalar-ratio-distinct tasks. Each atan-ratio / quotient denominator shape has 43 primitive positive ratios; independent numerator common scaling is not counted as extra tasks. Radial evaluation has 86 signed reduced nonzero coordinates. Polynomial/root/hard have larger coefficient/point domains, with bank collisions rejected. `mathematical_fingerprint` normalizes common scalar factors and excludes profile/bank/order/location-only aliases. Variety counts below are domain claims, not a claim every bank-boundary combination is collision-free.

## Source anomalies and evidence limits

Original q-35988 omitted solution, difficulty and correct ref; raw omits all three. Original polynomial duplicated legacy field is retained raw but normal uses the authoritative lesson widget. Original atan_ratio names h in prompt and f in solution; raw exact fidelity retains that mismatch, normal fixes the symbol. Original contextual fluid question refers to absent previous data; it is documented as context-underdetermined and raw evidence-only. Opaque scalar banks are public raw replay only, with separate defensible normal banks. No source math repair or TeX escape repair is claimed. `decoded-backslash-audit.json` counts actual decoded ord-92 runs; intentional aligned row separators are not escaped-command defects.

## Steps 5 and 7: Plot specification

Plot rating none. No practice source contains a mathematical plot, option raster or image-driven assessment. No Matplotlib/TikZ renderer or assets are necessary.

## Mathematical domains

Polynomial and atan-product functions have real coordinate domains. The root partial formulas require y+c>0. The log-cos family requires xy>0; sin-log requires y>0. Radial log requires x²+y²>0. Atan ratio requires x≠0 with positive k. Linear quotient requires x-ky≠0. Authored hard requires x+by≠0, and sampled/explicit positive u,v guarantee this at evaluation. All generated component-assembly records supply existing partials at their stated point; raw contextual evidence cannot establish the omitted scalar function domain.
