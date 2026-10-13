# Template extraction

## 1. Specific source descriptions

`component-map.json` contains every original prompt mask, every available complete ordered solution mask and every field/choice object with original IDs, types, values and key presence. `source.json` is the untouched wrapper and `source-cases.json` assigns all eleven replay cases. The nine shared solutions rearrange the curve, define `f`, compute `(f_y,-f_x)`, impose its zero dot product with the given nonzero vector, substitute the resulting relation, solve, and state the complete point set. They retain their actual differing substitution variable, row counts, factoring steps, terminal signs and final prose. No source math or key correction was needed beyond the two genuine omissions.

q-36332 uses `2xy+3y²=x²+4`, vector j, and two symmetric integer points. q-65208 uses `9x²y=3y³−6x`, vector i, with actual two branches `y=±x`; the three regular solutions include the origin. q-130223 uses `x²y=−8x−4`, vector j, a reciprocal substitution and one integer point. q-72410 uses a coupled quadratic with two opposite points; q-72440 reduces to two distinct linear factors; q-72416 includes an origin and a second point. q-130225 uses j and an axis condition with the rational ordinate 1/3. q-72427 uses i and shifted substitution `y=x+1`. q-130209 uses vector i+j and one rational point `(-1/4,-7/8)`. q-130217 uses vector −i+j and two circle points. q-72412 uses i and the relation `y=2x`. All original complete choices, including both singleton and multi-point omissions, are mapped, not inferred from only the correct option.

## 2. Shared mathematical pattern

For an implicit regular plane curve `F(x,y)=0`, a tangent vector is `(F_y,-F_x)`. For given `(u,v)≠(0,0)`, solve the system `F=0`, `uF_y−vF_x=0`, retaining all real regular points. Require the complete finite set in one radio option. Zero tangent vectors are excluded; every permitted source translation and normal task is checked for regularity. Do not normalize the tangent or compute its length.

## 3. Component and complete-bank mapping

All eleven historical banks remain separate profiles. Their parameterization is geometric translation, not a polynomial fit: replace every complete mathematical variable component `x` by `x−h` and `y` by `y−k`, and every whole tuple `(a,b)` by `(a+h,b+k)`. Protect partial-derivative operators, subscripts, symbolic `f(x,y)`/`t(x,y)` labels and TeX commands. Translation has derivative one, so every original derivative/substitution row remains valid. Source point-set spellings and answer types are recovered exactly at `h=k=0`. Numeric singleton options may underdetermine their original error recipe; each transformed historical bank is explicitly opaque and evidence-only, including a profile that completes missing refs and solutions.

The authored complete easy bank is: solve; use `y=x`; reverse x's solved sign; omit division by b, producing `(br,−br)`; omit y substitution, producing `(r,0)`. Its correct set is `{(r,−r)}`. The moderate bank is: solve; omit negative root; omit positive root; use the incorrect substitution sign `y=−mx`; swap the two coordinate roles. Its correct set is `{(r,mr),(−r,−mr)}`. The hard bank is: solve; omit second root; omit first root; use `x=y` instead of `x=−y`; swap coordinate roles. Its correct set is `{(−a,a),(−b,b)}`. These are full point-set response mistakes in the actual tangent-condition, quadratic-root and back-substitution method. No arbitrary unrelated offsets, pooled-option selection or per-choice feedback is used.

## 4. Reusable templates and guards

Normal easy curve: `A y²+2Axy=br+by−Ax²`. Bounds A=1..4, b=2..5, r=−6..6 excluding zero. The dot condition gives `y=−x`; cancellation leaves `bx=br`. b>1 prevents the omit-division choice from colliding with the correct answer. All tasks retain the canonical single linear-solving demand. Coefficients/signs vary, not the number of algebraic branches.

Normal moderate curve: `D y²+2mxy=m²x²+(D+1)m²r²`. Bounds D=1..3, m=2..4, r=1..4. D=1 and D=3 are observed number forms in q-72410/q-36332. The dot condition gives `y=mx`; the substitution leaves `(D+1)m²x²=(D+1)m²r²`, hence two familiar integer roots. m≥2 keeps the swap-coordinate bank member distinct. D changes the actual quadratic coefficient rather than multiplying the whole equation by an incidental scalar. Largest constant is 1024; no irrational root or additional factoring skill appears.

Normal hard curve: `x²+2xy=−(a+b)y+ab`. Nonzero integers a<b in −6..6 and a+b≠0. The dot condition gives `x=−y`; `(y−a)(y−b)=0` gives two unequal regular points. The sum guard retains the source's linear-y term and excludes reflected-set collisions; |ab|≤36 and |a+b|≤11. Signed and unequal roots remain the same factorable-quadratic method.

Observed evidence translation bounds h,k=−3..3, integers only. Every normal/evidence sampler and explicit call applies its same finite bounds. Complete profiles are selected before sampling; equivalence or ambiguity rejects the whole instance. Exact polynomial constraints use domain EX, including all displayed-bank coefficients, so source rational coordinates do not force a rational-curve-only coercion assumption. No algebraic coefficient input is advertised; non-integer parameter inputs are rejected.

`observed_raw` preserves absence of source difficulty/solution/correct refs. `observed_completed` adds an explicitly inferred hard assignment, correct ref and a full supported solution only where absent; both remain evidence-only. These completion counts are separate from original exact matches. Defaults are authored learning records. The original external/database IDs remain in immutable evidence, while generated field-owned UUIDs and enum strings use the local record contract.

For the reciprocal substitution in q-130223, `x−h≠0` is explicit in runtime metadata: the displayed curve's nonzero constant makes `x=h` impossible. Translation preserves that exclusion. Both branches of q-65208's inferred solution are separately read back against their real univariate root sets; duplicate origin occurrences collapse only when collecting the final point set.
