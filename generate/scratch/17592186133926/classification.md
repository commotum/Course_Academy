# Circulation Over Space Curves — classification

Frozen source: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, KP `17592186133926`, UUID `74196b81-0e52-5d10-a099-ccd849d03a98`. The snapshot is copied without mutation in `source.json`. `topic.json` and `lesson.json` retain their capture wrappers. The topic is Stokes' Theorem, MA 2138, database `17592186049762`.

There are **eight practice sources**, five labeled easy, two moderate, and one unrated. Every source has one radio field `selection` with five math choices. Seven sources have a correct designation and worked solution. q-162238 has neither, and has no difficulty attribute. Its raw public replay preserves all three omissions. No source question, answer, or worked solution contains a plot reference; plot rating is **none** for every template.

| Source | Original difficulty | Observed mask / operation | Bank |
| --- | --- | --- | --- |
| q-161925 | easy | xy rotation, absent z force, cos/sin of πt, z=1−t², −1≤t<1; constant integrand | raw:q-161925 |
| q-162230 | easy | xy rotation plus z force, sin/cos of t, z=t², −π≤t<π; constant plus cubic integrand | raw:q-162230 |
| q-162237 | easy | yz rotation, sin/cos of t, x=sin t, 0≤t<2π; constant integrand | raw:q-162237 |
| q-162229 | easy | xy rotation, ellipse x=2cosπt, y=sinπt, z=2, 0≤t<2; chain factor π | raw:q-162229 |
| q-162228 | easy | yz rotation, cos/sin of 2πt, x=t²−t, 0≤t<1; chain factor 2π | raw:q-162228 |
| q-162220 | moderate | symmetric xy force; cos²−sin² and double-angle primitive over 0≤t<2π | raw:q-162220 |
| q-162235 | moderate | (x+y)i−zk; quadratic coordinate cancellation and sine product over −1≤t<1 | raw:q-162235 |
| q-162238 | unrated | (y−x)i; polynomial loop x=t²−t, y=t³−t, z=sin2πt, 0≤t<1 | raw:q-162238 |

The eight observed masks remain distinct because their prompt structures, component notation, or exact solution stages differ. Changed numbers alone do not establish an additional observed template. Normal generation uses six authored families grouping the same operators: three easy, two moderate, one hard. The five easy originals support the three easy families; both moderate families are covered by default sampling.

The **actual linked lesson order**, obtained from activity/first-step and step/next, is:

1. Introduction, step 17592186134937.
2. Circulation Over Space Curves, step 17592186134928, assigned KP.
3. A Review of Green's Theorem, step 17592186134927.
4. Induced Orientations of Boundary Curves, step 17592186134938.
5. Stokes' Theorem, step 17592186134932.
6. Evaluating a Surface Integral Using Stokes' Theorem, step 17592186134930.
7. Using Stokes' Theorem to Evaluate Line Integrals, step 17592186134931.
8. Evaluating a Line Integral Using Stokes' Theorem, step 17592186134929.

The explicit key prerequisite is **Circulation**, topic MA 3713, database 17592186050773. The Introduction defines circulation as the direct closed-curve work integral, specifies traversal once, and makes the sign depend on orientation. The canonical example e-12421 substitutes three coordinates, differentiates all three, forms the componentwise dot product, reduces a trig identity plus a polynomial, and integrates over [0,2]. All normal questions retain this direct method. They do not require curl, normals, surface selection, Stokes' theorem, or evaluation of a surface integral.

The missing hard rating is an **authored design**, anchored to the unrated q-162238, not a recovered source label. It requires expansion of a cubic-minus-quadratic force component times a linear derivative and exact integration of three polynomial terms with denominators 3,4,5. The source prompt itself supplies this operation. Normal hard parameters preserve its cancellation and exact three-term workload. The sibling surface-integral canonical also contains polynomial direct-line-integral arithmetic, but its surface request and theorem are excluded here.

Two captured solution errors survive only in ineligible evidence: q-162230 changes cos²(t) to cos²(πt) in a reduction row; q-162235 loses the negative z-force sign in its scalar product and subsequent integrand/primitive. Both original final scalars remain mathematically correct. Normal generation recomputes the complete stages with the correct signs. q-162238's authoritative original widget is copied separately; it confirms all five choices and absence of a captured solution/key. Its independently derived correct value is −1/60; this inference is separate from the seven matched original designations.
