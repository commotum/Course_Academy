# Classification

Frozen source: math basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The wrapper is retained verbatim in source.json. Owning topic 17592186050482 / MA4132, Computing Double Integrals Using a Change of Variables. No database reads at another basis or writes were made.

|Observed difficulty|Source|Markdown/value family|Fields|Bank profiles|Plot rating|
|---|---|---|---|---|---|
|hard|q-160433|square-linear / linear reciprocal|two captured selection radios (one legacy)|two raw banks, equivalent five values|moderate|
|unrated|q-160896|shifted affine factor times square|one radio, no correct ref|one opaque five-scalar bank|none in capture|
|hard|q-160901|coordinate times sine of shear|one radio|one five-scalar bank|moderate|
|hard|q-160904|affine factor times exponential of another affine form|one radio|one five-scalar bank|moderate|
|hard|q-160933|affine factor times exponential of its square|one radio|one five-scalar bank|moderate|
|hard|q-160935|difference of squares times cosine of squared sum|one radio|one five-scalar bank|moderate|

Six practice questions, six observed Markdown/value templates, seven captured fields/banks and 35 captured options. There are five observed correct designations; two fields have no designation. Five existing worked solutions; one missing. No observed easy/moderate labels. Canonical example e-12328 supplies the easy polynomial/shear pattern; it is not counted as a practice question.

Lesson route was recovered from `activity/first-step` 17592186199250 and successive `step/next` refs: introduction → Performing a Change of Variables (98361) → Cases When the Transformation Is Inferred From the Domain (98373) → this KP (98374). Pull collection order was not used. The introduction extends the area transformation formula to integrands. The first sibling supplies the transformation (easy asks for setup, moderate evaluates); the second infers forms from region inequalities. Here learners infer from integrand factors and transform four vertices before evaluating. All defaults keep that particular assessment.

Easy (authored): canonical `(ax+by)y²`, infer one shear and y-coordinate, map four vertices, constant Jacobian and two power primitives. Moderate (authored): complete unrated `(ax+h)(x+dy)²`, with **h nonzero** and **a≥2**, infer an affine shifted factor and shear, map four rational-coordinate vertices, then the same two power primitives. This extra affine shift cannot collapse to easy. Hard: preserve the five observed families and their reciprocal/trig/exponential primitives, including the algebraic factorization and squared-inner chain primitive where observed. Families at each level are alternatives at equal workload, not a progression. No nonlinear transforms, polar coordinates, nonrectangular transformed domains, integrals requiring new techniques, or integration by parts are added.

Original widget evidence in `/home/jake/Developer/MA/DATA/Lessons/4132/Source/4132.json` confirms q-160433 is **one** five-choice widget, not two assessment demands, and q-160896 is one five-choice radio. Raw public evidence preserves both captured q-160433 fields and omissions. Completed normal questions use one observed widget and a supported inferred designation. Unrated raw replay omits difficulty and worked solution; normal completion explicitly assigns moderate.
