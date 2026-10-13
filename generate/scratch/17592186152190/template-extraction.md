# Template extraction

## 1. Describe each original before generalizing

Basis 1356 raw records are source.json. Each question uses exact positive integer radii, standard cosine x / sine y parameterization, zero or integer center offsets, one visible quarter/half arc, and asks for the parameter domain. All interval endpoints are included. The full ellipse uses [0,2pi), while some distractors cover a closed full circle. No rounding is required.

q-78682: easy, {"a": 3, "b": 2, "h": 0, "k": 0, "lo": "0", "hi": "1/2"}. selection: radio (5 values). Template easy_radio_ac731b91; bank observed_b3e761626b.

q-79278: moderate, {"a": 3, "b": 2, "h": 0, "k": 0, "lo": "1", "hi": "2"}. selection: radio (5 values). Template moderate_radio_aa1b6f42; bank observed_28e3eff896.

q-106400: easy, {"a": 3, "b": 5, "h": 0, "k": 0, "lo": "0", "hi": "1"}. selection: radio (5 values). Template easy_radio_c0d3295b; bank observed_eaf0b1fed8.

q-106402: easy, {"a": 5, "b": 2, "h": 0, "k": 0, "lo": "0", "hi": "1/2"}. selection: radio (5 values). Template easy_radio_ac731b91; bank observed_fbd6fa90a4.

q-106403: moderate, {"a": 2, "b": 3, "h": 0, "k": 0, "lo": "1", "hi": "3/2"}. selection: radio (5 values). Template moderate_radio_e32a0128; bank observed_2bd75d9dae.

q-106404: moderate, {"a": 5, "b": 3, "h": 0, "k": 0, "lo": "1/2", "hi": "3/2"}. selection: radio (5 values). Template moderate_radio_0de09b08; bank observed_c16c9e05d2.

q-106711: moderate, {"a": 4, "b": 2, "h": 0, "k": 0, "lo": "3/2", "hi": "2"}. selection: radio (5 values). Template moderate_radio_c37a84a7; bank observed_09b9812705.

q-274866: hard, {"a": 3, "b": 2, "h": 1, "k": 3, "lo": "0", "hi": "1/2"}. field-1: blank (1 values), field-2: blank (1 values). Template hard_blank_af37bd55; bank None.

q-327822: easy, {"a": 4, "b": 3, "h": 0, "k": 0, "lo": "0", "hi": "1/2"}. field-2: blank (1 values), field-1: blank (1 values). Template easy_blank_691deb7a; bank None.

q-327828: easy, {"a": 6, "b": 4, "h": 0, "k": 0, "lo": "0", "hi": "1/2"}. field-1: blank (1 values), field-2: blank (1 values). Template easy_blank_c5a59315; bank None.

q-327831: moderate, {"a": 4, "b": 2, "h": 0, "k": 0, "lo": "3/2", "hi": "2"}. field-1: blank (1 values), field-2: blank (1 values). Template moderate_blank_266662f0; bank None.

q-327835: easy, {"a": 8, "b": 3, "h": 0, "k": 0, "lo": "0", "hi": "1"}. field-1: blank (1 values), field-2: blank (1 values). Template easy_blank_12424cb0; bank None.

q-327847: hard, {"a": 4, "b": 5, "h": -2, "k": 1, "lo": "0", "hi": "1/2"}. field-1: blank (1 values), field-2: blank (1 values). Template hard_blank_36791858; bank None.

q-328327: hard, {"a": 5, "b": 3, "h": -1, "k": 2, "lo": "1/2", "hi": "3/2"}. field-1: blank (1 values), field-2: blank (1 values). Template hard_blank_87dc1f6a; bank None.

q-79273: easy, {"a": 4, "b": 3, "h": 0, "k": 0, "lo": "0", "hi": "1"}. selection: radio (5 values). Template easy_radio_c0d3295b; bank observed_11bfd74e2d.

q-79275: easy, {"a": 2, "b": 4, "h": 0, "k": 0, "lo": "0", "hi": "1"}. selection: radio (5 values). Template easy_radio_c0d3295b; bank observed_eaf0b1fed8.

q-79280: hard, {"a": 2, "b": 3, "h": 3, "k": 1, "lo": "0", "hi": "1/2"}. selection: radio (5 values). Template hard_radio_6363d106; bank observed_02fc2b22d3.

q-79282: hard, {"a": 4, "b": 2, "h": -3, "k": -1, "lo": "0", "hi": "1"}. selection: radio (5 values). Template hard_radio_94c0e6da; bank observed_8a53286cfe.

## 2. Generalized pattern

Recover the closed parameter interval whose cosine/sine signs give the shown quarter or half of an axis-aligned ellipse. Translations change center and endpoint coordinates while leaving the parameter signs relative to the center unchanged. Answer a whole membership interval in radio form or its two endpoint fragments in blank form. The per-level reasoning demand remains fixed as specified in classification.md.

## 3. Component and complete-bank map

choice-mapping.json enumerates EVERY original displayed value, field key, correctness designation, parameter object, template and bank profile. Its radio recipes are [lo,hi,right_closed] in multiples of pi, defining explicit geometric arcs on the unit circle. Profiles contain the whole observed five-option bank in templates.json. These categorical intervals are invariant under radii/translation: they are mathematically meaningful geometric alternatives, not unexplained numeric fits. The precise historical author mistake remains unresolved; no distractor diagnosis is presented. Blank recipes are lower/upper endpoint projections.

Each prompt consists of image, named quarter/semi/half arc, numeric equations, domain question, and optional two keyed placeholders. Solutions retain generic equation, In our case radius/center sentence, full ellipse, interval restriction explanation, solution image, We can see interval sentence, and final restricted equations. The q-327847 extended sign explanation and q-327831 fourth-quadrant explanation remain separate skeletons.

## 4. Reusable template and constraints

templates.json stores extracted prose skeletons with explicit @@a@@, @@b@@, @@h@@, @@k@@, signed-offset, prompt-image and solution-image slots. This is source extraction data, not a literal source-payload branch. Normal generate() always substitutes all numeric equations, full and restricted, and computes endpoint fields from validated arc parameters. The categorical arc endpoints belong to the template, which rejects any incompatible explicit interval. Bank compatibility and a whole-instance five-distinct-choice check happen before rendering. One fixed solution is independent of choice order.

Fixed: standard cosine/sine parametrization, full-period interval, shared prose/layout, named arc and closed endpoint convention. Variable: radii, center, all concrete equations, concrete center/radius sentences and both plots. Conditional: hard center offsets, plus/minus/omitted zero; prompt full-ellipse context only for q-328327; blank/radio layout. Identities include full prompt, fixed solution, complete bank/layout and version; physical fingerprints exclude presentation/profile and seed.

Observed radii 2..8 and centers 0,±1,±2,3. Proposed equal-level sampler: unequal positive integer radii 2..8 (42 ordered pairs), origin at easy/moderate; hard centers -4..4 except origin (80 centers, 3360 objects per arc). Equal radii are excluded to keep ellipses noncircular, not to create difficulty. All observed values remain eligible. There are 84 possible easy objects across two arcs, 168 moderate across four arcs, 10080 hard across three translated arcs. Numeric object changes do not count as new skills or recovered templates. No authored missing levels or authored mixed banks.

## Source errors and supported repairs

All 18 solutions call theta a geometric central angle formed by a point on a noncircular ellipse. This is false: atan2(y-k,x-h)=atan2(b sin(theta),a cos(theta)), generally not theta. The smallest repair retains the restriction paragraph but calls theta the parameter angle of normalized unit-circle coordinates. Plots correctly label cardinal parameter angles, so no source plotted answer/domain is changed. Exact original prose fidelity is reported separately as 0/18; repaired solution coverage is 18/18.

q-274866: prompt and plotted center are (1,3), radii (3,2); its In our case sentence copies (3,1), a=2,b=3. The parameterized sentence uses the prompt-derived (h,k),a,b; raw original stays unchanged. q-327831 final equation wrongly renames x,y as p,q; repaired to x,y. q-79282 generic y equation lacks a separator before theta; repaired comma. All original answer values/designations are still matched: no exclusion or fabricated fields.

Remaining historical distractor-intent limits are metadata interpretation limits, not unanswered bank comparisons. All complete displayed values are independently replay-checked.
