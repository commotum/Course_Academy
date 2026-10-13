# Four-stage template extraction

## 1. Describe each source before generalizing

q-18021: diagram included A=128°, AB=3, AC=7. Image first, then “Find the area of △ABC.” and two-place rounding. Five-choice selection radio; correct8.27. Formula bc sin A /2; identifies c=AB then b=AC then m∠A; sine evaluation; substitution with7 then3; product10.5; rounded final8.27. Its displayed sine0.788010 is truncated, despite claiming rounded to six places; correct rounding0.788011. Raw retains the error, normal corrects it without changing stages.

q-18027: same family, A=11°, AB=26, AC=22; five distinct choices, correct54.57. Identification26 then22; substituted product22×26; half-product286; sine0.190809; final54.57. Changed numbers alone do not define another template.

q-18023: included B=20°, AB=5, BC=13, same image-first setup but punctuation differs and calculator blockquote is present. Five choices. Original has no difficulty, worked solution or correct designation. Direct exact area is65 sin20°/2 ≈11.12; this independently supports a normal inferred designation, never a “matched original correct.” Its raw record keeps all three omissions.

q-279752: included B=40°, AB=4, BC=8. Blank field-1 directly after “is”, nearest tenth, “above”, no unit suffix. Formula ac sin B /2. Identifies c then a. Product8×4; half-product16; sine0.642788; final10.3. Prose wrongly says between a,b; normal corrects to a,c, raw preserves source evidence.

q-279753: included A=120°, AB=18ft, AC=12ft. Blank with supplied ft² after the placeholder. Product12×18; half-product108; sine0.866025 with ellipsis only inside final product row; final93.5 ft². That ellipsis and units are fixed components, not added to other source families.

q-280260: included B=60°, AB=BC=5, blank with two-place rounding, no “above” or units. Product5×5; half-product12.5; sine0.866025; final10.83. Source prose correctly names a,c.

## 2. Generalized pattern

Read two adjacent side lengths and their included angle from a labeled triangle, choose the corresponding bc sin A /2 or ac sin B /2 formula, identify every supplied component, evaluate sine, substitute both factors, evaluate the half-product, and round the final area to the requested precision. Responses are numeric fragments, with source rounding and unit placement preserved. Each question has one fixed worked solution independent of selected error.

## 3. Components and complete banks

The detailed per-option ledger is bank-mapping.json. It includes every source field, source answer UUID, value, exact designation presence, parameterized recipe and its interpretation limit. Three radio banks are opaque decimal patterns. Their public raw recipe uses each original decimal ratio against its anchor rounded correct area, applied to the current rounded correct area. Correct values always come from the exact mathematical area. Ratios are an explicit preservation mechanism, **not recovered error intent**, and every raw profile is ineligible/evidence-only. All original18 values and five present correct designations are compared one-to-one; the absent sixth designation is never counted matched.

Normal complete bank, selected before parameters: correct area uv sinθ/2; omission of half uv sinθ; omission of sine uv/2; replacing sine by absolute cosine uv|cosθ|/2; evaluating with squared sine uv sin²θ/2. Absolute cosine keeps the area-valued distractor positive for obtuse triangles. Each whole bank is rounded with the exact same response precision and rejected on zero/negative values or any equality. No replacement pooling or arbitrary added offsets. Blank banks contain only the exact rounded area fragment.

## 4. Reusable masks, domains and identity

Source solution masks replace complete AB/AC/BC identification components, complete substituted side product, angle argument groups, sine value, evaluated half-product, and final rounded area. Replacements are masked before insertion so new digits cannot trigger another replacement. Original shared prose, formula, identification order, sine paragraph, two aligned blocks and three arithmetic rows remain; final ft² and source ellipsis are conditional by family. q-18023 normal completion uses the same complete stage structure, explicitly inferred rather than a fabricated observed solution.

Raw anchor plots reuse exact captured paths and SHA256; changed parameters regenerate with Matplotlib. Original prompt punctuation/spacing and source blank placeholders remain exact. Public raw replay uses the ordinary generate API with explicit source cases and preserves difficulty/solution/correct-ref presence separately.

Easy sampling: integer sides2..60, directly supplied integer angle15..150°, original explicit anchors allowed down to11°. Moderate: both noninteger one-decimal sides2.1..29.9 and a supplied integer angle15..150°. Hard: one equal side length2.01..29.99 not expressible in tenths, repeated on both adjacent sides; equal base angles25..80°, included angle180−2a. All explicit calls enforce the same substantive demands and side ceiling as sampling, except raw/source easy supports positive integer sides1..60 and angle10..160. No coefficients or givens can remove the authored workload. Hard unequal sides/base angles are rejected instead of drawing an impossible triangle.

Before whole-bank rounding collisions, easy side-order-normalized numerical objects have1770 side pairs ×136 angles=240720 per rounding policy; moderate has252×253/2 side pairs ×136 angles=4,335,408; hard has2520 non-tenth hundredth lengths ×56 equal base-angle pairs=141120. Actual method-bank eligibility removes collisions (notably30°,45°,90°,135°,150° where applicable) and may remove near-rounding collisions. These are finite pre-rejection upper bounds, not claims that all are valid. The84 normal QA records are samples from broad equal-workload domains, not claims of exhaustive testing.

Mathematical fingerprints exclude seed, option order, unit spelling, vertex lettering, bank/profile and source aliases; they retain exact side values modulo side swap, included angle, actually supplied base-angle information and requested rounding precision. Content identity includes actual prompt, fixed solution, complete displayed bank, difficulty and version. Source/profile metadata is outside learner content.

Decoded byte inspection is recorded in source-string-inspection.json: individual TeX command backslashes have ordinal92, while doubled backslashes are legitimate aligned-row separators. JSON visual escaping is not treated as evidence of malformed TeX. No escape repair is claimed.
