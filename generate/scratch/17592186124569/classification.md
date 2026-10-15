# Classification at math basis 2719

KP 17592186124569: Reconstructing a Two-Variable Function From Its Gradient. Lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. All 14 source practice questions and the canonical example were read together at this basis; the complete evidence is `reference/initial/source.json` and its exact EDB query/result.

All 13 rated practice questions are easy: 12 single radio fields with five whole-function equations, and one single blank expecting only the potential before `+C`. The remaining radio question is unrated, lacks a correct reference, and has no worked solution. There are no moderate or hard sources. The shared method integrates the x component with an arbitrary g(y), differentiates with respect to y, matches the second component, integrates g′, and substitutes. Distinct operations/primitive structures and the blank response shape remain separate templates. All prompts, banks and solutions have no plots or image references. Plot rating **none**.

The canonical example f=x²y−3y+C supports the method and easy classification; it is excluded from practice counts. Sources q-37346 and q-37343 are excluded from generator support with reasons below, never changed in EDB. q-168602 requires a preceding part that is absent from the standalone prompt. Its solution explicitly supplies F=(y³−1,3xy²+1); this premise is added only to new generated instances. The original standalone source is not counted as usable practice.

| Source | Difficulty | Response | Mathematical backbone / support |
|---|---|---|---|
| q-35994 / 17592186124943 | easy | radio (5 choices) | -y; 3-x; -x*y; 3*y |
| q-37346 / 17592186125061 | unrated | radio (5 choices) | Unrated; no correct reference or worked solution. No authoring inferred for this incomplete source. |
| q-168602 / 17592186235530 | easy | blank (1 choices) | y**3-1; 3*x*y**2+1; x*y**3-x; y |
| q-132077 / 17592186266129 | easy | radio (5 choices) | cos(x+y)+y; cos(x+y)+x; sin(x+y)+x*y; 0 |
| q-132079 / 17592186266130 | easy | radio (5 choices) | exp(y)-y*sin(x); x*exp(y)+cos(x); x*exp(y)+y*cos(x); 0 |
| q-132080 / 17592186266131 | easy | radio (5 choices) | exp(y); x*exp(y)+2*y; x*exp(y); y**2 |
| q-81734 / 17592186351356 | easy | radio (5 choices) | 2*x*y**2+1; 2*x**2*y+1; x**2*y**2+x; y |
| q-81737 / 17592186351357 | easy | radio (5 choices) | 12*x**3-1/y; (x-1)/y**2; 3*x**4-x/y; 1/y |
| q-81748 / 17592186351362 | easy | radio (5 choices) | cos(x)*sin(y); sin(x)*cos(y)+sin(y); sin(x)*sin(y); -cos(y) |
| q-81749 / 17592186351363 | easy | radio (5 choices) | y*exp(x*y); x*exp(x*y)+2*y; exp(x*y); y**2 |
| q-132084 / 17592186406697 | easy | radio (5 choices) | 2*x*sin(y); x**2*cos(y)+3*y**2; x**2*sin(y); y**3 |
| q-81736 / 17592186406699 | easy | radio (5 choices) | sin(y)+y; x*cos(y)+x; x*sin(y)+x*y; 0 |
| q-37343 / 17592186406700 | easy | radio (5 choices) | Two choices have the same gradient: x^2 y+y^3+C and x^2 y+y^3. The prompt only requires a potential, so the bank is ambiguous. |
| q-81738 / 17592186421424 | easy | radio (5 choices) | 3*x**2-y**2; 4-2*x*y; x**3-x*y**2; 4*y |
