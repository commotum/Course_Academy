# Curriculum context for KP 17592186100890

Current read-only source, topic, and lesson captures use `math` basis 1356. The earlier basis-1308 lesson and transitive-prerequisite reads are retained as historical supporting evidence; the current route and direct prerequisites were rechecked. No database changes.

## Actual lesson route

Topic 1255: Cartesian Equations of Parametric Curves; activity 17592186101094.
Order follows `activity/first-step` and `step/next`, not Pull collection order.

1. Introduction: eliminate a parameter by substitution and translate its interval into an x-domain.
2. Finding the Cartesian Equation of a Curve Defined Parametrically: canonical e-5087 eliminates t² and concludes x ≥ 0.
3. Finding the Cartesian Equation of Curves Defined Parametrically With Trigonometric Functions: tutorial isolates scaled sine/cosine, then substitutes into the Pythagorean identity; coefficients are 1/2 and 1/3.
4. Finding the Cartesian Equation of a Curve Defined Parametrically With Trigonometric Functions: target KP; canonical e-5101 uses cosecant/cotangent and a derived Pythagorean identity.

The target KP is the final lesson step. Easy/moderate/hard are practice difficulty tiers within it, not additional stored lesson steps.

## Prerequisite evidence

Direct prerequisites include graphing parametric curves and finding their ranges, radical equations, substitution, secant-tangent and cotangent-cosecant identities, and both sine and cosine double-angle topics.

The transitive prerequisite graph includes topic 204, Extending the Trigonometric Ratios Using the Unit Circle. Its canonical examples explicitly determine quadrant signs, including a negative tangent in quadrant II. Radian trigonometric ratios and extensions also precede this topic.

## Recommendation

The moderate tier should exercise: isolate a scaled sine/cosine, recover the missing function with the Pythagorean identity, select the square-root sign from the interval, and substitute into a tangent/cotangent quotient.

Scaled coefficients, tangent/cotangent counterparts, and quadrant intervals provide variation at the same moderate difficulty. There is no instructional order within this tier. The added families, intervals, and banks are authored extensions, not observed moderate source templates. Use the same worked-solution stages, changing the quotient identity and sign sentence where necessary.

Quadrant variation is appropriate prerequisite application and may occur with any supported quotient family. Keep each interval within a single quadrant to avoid piecewise or multi-branch answer requirements. Double-angle elimination remains the distinctive hard-tier family in the observed bank, although its identities are already prerequisites.

Blank variants are compatible with response types elsewhere in this KP, but are unobserved at moderate and should be distinguished from mathematical difficulty. This revision retains radio fields for every moderate variant.

Domain correctness should be validated for every extension; the source canonical example has a known endpoint error (x ≥ 1 where x > 1 is required) and its squared equation needs y > 0 to isolate the intended branch. Do not reproduce those defects in authored questions.

## Evidence

- [Full lesson content and route](lesson-context.edn)
- [Direct prerequisites and dependent topics](topic-context.edn)
- [Quadrant-sign prerequisite examples](quadrant-prerequisite-context.edn)
- [Transitive prerequisite titles](prerequisite-titles.edn)
- [Original practice questions](source.json)

The implemented variations and exact distractor transformations are specified in [moderate-variations.md](moderate-variations.md).

## Current capture confirmation

[Current lesson wrapper](lesson-current.json) preserves database, basis 1356, and lineage. Following first-step and next gives step IDs 17592186101708 → 17592186101709 → 17592186101711 → 17592186101710, ending at this KP. The previous route is unchanged. [Current topic wrapper](topic-current.json) retains the direct topic prerequisites and sibling ordinary-substitution KP. The current KP capture also explicitly lists sine/cosine double-angle formulas, the sine/cosine Pythagorean identity, and both secant/tangent and cotangent/cosecant identities as key prerequisites.

Easy continues to isolate scaled/shifted same-angle functions and use one Pythagorean identity. Moderate recovers a missing function, chooses its quadrant sign, then forms a quotient. Hard derives a double-angle identity using the Pythagorean identity, then substitutes and isolates a quadratic expression. Neither tier adds parametric differentiation, curve tracing, graph recognition, inverse trigonometric functions, or parameter recovery from a Cartesian equation. The downstream conic-parametrization topics remain outside scope.
