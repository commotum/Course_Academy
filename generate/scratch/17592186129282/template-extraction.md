# Template extraction: four stages

## 1. Describe each original

source-components.json contains all 13 raw fields, each original prompt and fixed solution, exact parameters, function structures, every raw option and correct ref, and exact replay recipe. source.json is an unchanged capture wrapper. No original question or field is omitted.

- q-161788 / poly_sum: x=u**2 + v, y=2*u - v**3; point (1,2); J=-2*(3*u*v**2 + 1); J(point)=-26; scale=26; five complete coefficient δA choices per recorded profile.
- q-161832 / log_product: x=log(u*v), y=u*v**2; point (1,5); J=v; J(point)=5; scale=5; five complete coefficient δA choices per recorded profile.
- q-161831 / exp_product: x=v*exp(u), y=u*exp(v); point (-1,1); J=(u*v - 1)*exp(u)*exp(v); J(point)=-2; scale=2; five complete coefficient δA choices per recorded profile.
- q-161873 / reciprocal_product: x=-v + 1/u, y=u**2*v; point (2,2); J=2*u*v - 1; J(point)=7; scale=7; five complete coefficient δA choices per recorded profile.
- q-161874 / sqrt_sum: x=sqrt(u) + v**2, y=u*v; point (4,2); J=-(-sqrt(u) + 4*v**2)/2; J(point)=-7; scale=7; five complete coefficient δA choices per recorded profile.
- q-161875 / cos_sum: x=-v**2 + cos(u), y=u + v; point (0,3); J=2*v - sin(u); J(point)=6; scale=6; five complete coefficient δA choices per recorded profile.
- q-161885 / quotient_product: x=u**2/v, y=u*v; point (2,4); J=3*u**2/v; J(point)=3; scale=3; five complete coefficient δA choices per recorded profile.
- q-161887 / sqrt_product: x=sqrt(u*v), y=u*v**2; point (1,4); J=v*sqrt(u*v)/2; J(point)=4; scale=4; five complete coefficient δA choices per recorded profile.
- q-161877 / log_difference: x=log(u - v), y=-u**2 + v; point (2,1); J=-(2*u - 1)/(u - v); J(point)=-3; scale=3; five complete coefficient δA choices per recorded profile.
- q-161878 / sin_sum: x=u + v**2, y=sin(u + v); point (-3,3); J=-(2*v - 1)*cos(u + v); J(point)=-5; scale=5; five complete coefficient δA choices per recorded profile.
- q-161876 / exp_sum: x=exp(u + v), y=u**3 + v; point (-2,2); J=-(3*u**2 - 1)*exp(u)*exp(v); J(point)=-11; scale=11; five complete coefficient δA choices per recorded profile.

## 2. Generalized family

For a tiny coordinate-axis rectangle with bottom-left corner (u0,v0) and area δA, differentiate the displayed two components, form ad−bc, simplify symbolically, substitute the point, take absolute value, and select |J(u0,v0)|δA. The symbolic expression families are distinct templates; numerical points are variants.

## 3. Components and complete banks

source-components.json maps each original displayed option one-to-one to abs(J(point))*r for its exact observed rational ratio r. Since isolated scalar values underdetermine a wrong-operation recipe, these ratios are explicitly replay-only proportional expression shapes with unresolved original intent. They do not claim recovered pedagogical intent, and are never selected by default. Both legacy complete banks are preserved separately; all raw fields are compared in validation.

Normal authored banks use assessed method operations. Area bank: [C,C²,1/C,2C,C/2] (correct absolute factor, square, inverse, double, half). Determinant bank: [C,|ad+bc|,|ad|,|bc|,|2ad−bc|] at the same point. Select the entire profile first; reject the entire instance on zero/nonfinite scale, duplicate/equivalent members or nonnegative-domain failure. No pooled distractor replacement or random numerical noise. Determinant-operation banks are not registered for log_product, cos_sum, quotient_product, or sqrt_product because their fixed derivative relations force an option collision for every eligible point; those families have the area-operation bank.

## 4. Reusable Markdown/value template

Fixed: rectangle setting and shared source sentences, one selection radio with five coefficient δA answers, derivative matrix → ad−bc product → source-family symbolic simplification stages → point substitution → signed value → absolute area step. Variable: displayed component formulas, point, derivatives, determinant stages, substitution and bank values. Optional: explicit replay bank; moderate/hard small coefficient parameters. Domain constraints appear in generation metadata; source mathematical domains ensure a C¹ neighborhood at the point. Standard LaTeX normalizes Unicode and mathematical bitmap text without changing the complete mathematical object. No learner-facing error diagnoses are authored. One fixed solution is independent of chosen response.

Observed solution prose is preserved verbatim; formula notation is normalized. All scalar simplification rows from each easy family are retained (including 2v−v and 2u²/v+u²/v); generated derivative matrix may use equivalent radical fractions. This is mathematical/layout fidelity, not a byte-identical solution-string claim. Canonical asset inspection is recorded in plot-extraction.md.

Variation: easy has 11 original function forms with exact familiar evaluation families; moderate/hard use the bounds in classification.md. Canonical mathematical identity uses transformation, point and domain; presentation identity additionally includes complete bank, prompt, fixed solution and version. Changing seed/order alone preserves identity.
