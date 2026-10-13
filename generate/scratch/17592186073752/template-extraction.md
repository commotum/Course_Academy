# Four extraction stages

## 1. Describe each observed question

q-167194: b=480-10a, 20b+400a=7200. a=-12 and b=600; two scalar blanks. Its displayed question includes only the second equation, while its solution displays both. It substitutes into the b-first equation, distributes 20, collects a terms, subtracts 9600, divides by 200, then backsubstitutes. Thousands use `\,`. q-167210 has identical prose/structure with C=240,k=20,m=30,n=900,R=6000, a=-4,b=320. q-167226 reverses term order: 70a+9b=600, b=75-5a, a=-3,b=90. Its expansion is 70a+675-45a, followed by 25a+675; this ordering remains separate.

q-171690: x+5y=13 and y=x+5; supplied (x,y) tuple with field-1=x and field-2=y. Banks, refs, difficulty and worked solution are absent. The independent solve gives x=-2,y=3. The captured widget confirms scalar tuple fragments, not a single tuple answer. q-4133: 3a+2b=4, -4a+b=2; one five-option radio asks for a-b. Solving b=2+4a and 3a+2(2+4a)=4 gives a=0,b=2, so a-b=-2. q-5179: 3p=15, p+2q=9; five-option scalar radio asks p-q. p=5,q=2, so p-q=3. Neither radio captures a correct ref or worked solution. All coefficients are integers and all source results are integers. No plots occur.

## 2. Generalize the shared pattern

Isolate one variable (or use an already isolated/known variable), substitute into the other equation, distribute, collect, isolate the remaining variable, and backsubstitute. Return the requested scalar difference or two scalar fragments. Unique linear systems only. Normal output provides the information needed to solve each question independently.

## 3. Component and whole-bank mapping

`source-cases.json` maps every source to its template, original parameters, and whole profile. `component-mapping.json` lists every field, captured answer UUID/value, derived answer where absent, and recipe. The parameters are:

- coefficient templates: C,k,m,n,R for b=C-ka and mb+na=R, with a=(R-mC)/(n-mk), b=C-ka. Order is b-first or a-first. Each blank's single option is that exact coordinate.
- tuple_xy: k,C,h for x+ky=C, y=x+h; x=(C-kh)/(1+k), y=x+h.
- difference_ab: A,B,C,S,T for Aa+Bb=C, Sa+b=T; a=(C-BT)/(A-BS), b=T-Sa, D=a-b.
- direct_pq: k,C,n,R for kp=C, p+nq=R; p=C/k, q=(R-p)/n, D=p-q.

Complete source_4133 bank: D/2, -D, -D/2, -3D/2, D. At the original parameters these reproduce respectively -1,2,1,3,-2. This is an empirical multiplicative numerical profile, with unknown distractor intent, not a recovered mistake algorithm. It generalizes complete values without a literal answer lookup and is only selected explicitly for source evidence.

Complete source_5179 bank: D,-2q,-D,q,p -> 3,-4,-3,2,5. Reverse subtraction and reporting a coordinate are supported method interpretations; the -2q option's interpretation is unresolved. This whole profile is retained explicitly without claiming the source authoring algorithm.

Default authored radios use one complete bank D,-D,a+b,a,b (or p,q). These correspond to correct difference, reverse difference, adding coordinates and reporting only one coordinate. Any correct/wrong collision, duplicated value or incomplete bank rejects the entire question. No replacement pool or first-valid recipe selection occurs. The bank is not feedback in learner content. Exactly one eligible answer is required.

## 4. Reusable rendering, guards, and stage masks

The script renders all prose from fixed sentence constants and complete algebraic component masks. Existing coefficient worked solutions reproduce the full prose and ordered row groups 2/6/2 after the literal-brace repair only. The six middle rows retain the original equation, substituted grouped product, expanded three terms, collected two terms, isolated coefficient times variable, final coordinate. Backsubstitution retains the grouped negative coordinate before reduction. The validator reads equations from displayed strings, independently derives the substitution from a printed original equation, and checks exact polynomial equality between substituted, expanded, collected and isolated rows; merely evaluating all rows at a zero coordinate would miss a distribution sign error. q-171690's newly authored solution has 6/2 rows; q-5179 has 2/4; q-4133 and hard unit_pair have 2/6/2. Missing worked solutions are authored, not counted as source matches.

Easy coefficient explicit bounds: integer C in 1..600, k in 1..30, m in 1..100, n in 1..1000; 0<n-mk<=500, a integer in -15..-1, b in 1..1000, R>0. Tuple k has absolute value 1..6 excluding -1, |C|<=80, 1<=|h|<=12 and an integer result. Direct k,n in 1..6, |C|,|R|<=60 and integer results. Moderate/hard use nonzero integer A,B,S with absolute magnitude 1..6, 1<=|C|,|T|<=80 and nonsingular A-BS. Moderate coordinates are integers of absolute magnitude <=12; hard both have reduced denominators 2..7 and absolute magnitude <=12. Guards apply to explicit inputs and sampled variants. Samples choose whole method banks before rendering and reject whole invalid systems/banks. Each difficulty's template variations are unordered peers. Moderate/hard require nonzero constants and two nonzero substituted products B*T and -B*S*variable before cancellation; a zero isolated constant cannot reduce the advertised distribution workload.

Presentation repairs: escape unmatched literal `{` as `\{`; q-171690 replaces malformed `$$,` with the separately supplied inline comma `$,$` (spacing is insignificant). Prompt equation whitespace is normalized only in comparisons. No algebra changes occur. Source_context profiles preserve the original contextual prompt; defaults add b=C-ka so the first equation is available before submission. These additions are separate from exact-source replay. Source missing fields receive derived scalar answer banks/refs without claiming captured correct designation matches.

Math-task fingerprints normalize the two complete linear equations up to nonzero scalar and equation order, normalize variable names, and include pair-versus-difference response. They exclude banks and layouts. Content identity includes version, level, actual prompt, fixed solution, complete answer bank and field shape; seed, choice order and profile aliases are excluded. Own field UUIDs own every answer UUID and correct lookup ref.
