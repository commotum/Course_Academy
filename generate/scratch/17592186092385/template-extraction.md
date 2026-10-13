# Templates and banks

The core task is to differentiate at a supplied point, take the negative
reciprocal tangent slope, form the normal line, and solve its intersection with
the requested coordinate axis. Preserve the five solution blocks and all prose
between them. A radio expects the whole ordered pair; two blanks expect its
individual coordinates with the surrounding parentheses and comma supplied.

`templates.json` contains all ten source-specific descriptions and every
original bank option with its field ownership, complete mathematical value,
recipe and profile. Seven complete sources are supported. Their Markdown
replays exactly at scale 1. Missing fields or canonical values in q-10878,
q-71542 and q-342222 prevent source-bank fidelity; those structures are excluded.

For p the point abscissa, let y0=f(p), m=f'(p), n=-1/m and b=y0-n*p.
The normal is y=n*x+b. Let I=-b/n for an x-intercept or I=b for a y-intercept.
The observed complete radio profiles are:

| Source | Ordered scalar recipes | Coordinate layout |
|---|---|---|
| q-10871 | -p, p, m, I, I/m | (value,0) |
| q-11124 | 1/m, y0, y0+1/(2*m), 1/(2*m), I | (0,value) |
| q-104073 | -I, I, -p, y0-p, -(y0-p) | (0,value) |
| q-104075 | m, 1/I, 1/m, p, I | (value,0) |

These are observed expression patterns, not established explanations of learner
mistakes. Each reproduces every source option at scale 1. No profile pooling,
extra distractors, option feedback or mixed banks are used. The three complete
blank templates have field-1=I and field-2=0, each with one owned canonical
answer. Source-bank validation separately verifies correct designation.

The bounded authored extension replaces f with s*f, s an integer from 1 through
12, retaining the source abscissa and axis. It recomputes the point ordinate,
derivative, slopes, normal equation, intercept, answer banks and solution. This
preserves the observed signs, zero abscissa, fractional powers and negative
power without adding a new method. It deliberately does not sample negative or
zero scales, different abscissas, additional terms, or new difficulty bands.
Source-scale values remain in the catalog for replay; existing mathematical
tasks are excluded before committing. There are 36 easy and 48 moderate tasks.

Radical templates use x>0, the reciprocal template uses x!=0, and quadratics
use real x. All source and sampled points lie inside these domains. All tangent
slopes are finite and nonzero. Reject ambiguous or colliding complete banks.

For variants, preserve the derivative rewrite, tangent evaluation, reciprocal,
point-slope/distribution/simplification, and axis substitution sequence. Retain
the shorter zero-abscissa sequence and the extra intercept rearrangement used
by the two easy blank sources. Every variant has one fixed worked solution.
Full original notation and layout fidelity is established for replay; generated
math uses canonical LaTeX, with the same surrounding source prose and layout.

No source mathematical errors were found in the seven supported records.
No new or reused plot assets are required, so stages 5 and 7 need no renderer.
Source evidence changes require reclassification before a new commit.
