# Step 4: four-stage template extraction

## 1. Describe each original specifically

The complete original prompts, solution prose and complete banks are in source.json; source-cases.json records every original's parameterization and bank. The following table inventories the assessed line and solution stage sequence. All use one selection radio and five whole-equation math choices.

| Source | Level | Given a,b,c | Given slope | Conversion rows |
|---|---|---|---|---:|
| q-44404 | moderate | 1,5,10 | -1/5 | 3 |
| q-44514 | easy | 12,-4,5 | 3 | 3 |
| q-23378 | easy | 5,-1,7 | 5 | 3 |
| q-23618 | easy | 8,-1,2 | 8 | 3 |
| q-23621 | moderate | 1,3,6 | -1/3 | 3 |
| q-28338 | moderate | 4,10,20 | -2/5 | 4 |
| q-28341 | easy | 16,4,12 | -4 | 3 |
| q-59763 | easy | 4,2,8 | -2 | 3 |

The prompt asks which line is perpendicular to the displayed standard-form equation. Solutions share exactly: product criterion; conversion introduction; aligned conversion; identification of given slope; identification of chosen line/slope; multiplication; conclusion. q-28338 includes an unreduced division row before the reduced row. q-28341 uses x in the numerator of two option fractions but ordinary coefficient fractions when discussing slope.

## 2. Generalized pattern

For ax+by=c with a,b nonzero, compute m=-a/b and intercept c/b by isolating y. Each candidate y=sx+d is perpendicular iff ms=-1. Intercepts do not determine perpendicularity. The required response is a whole displayed equation selected by radio, not an equation fragment, slope blank or unknown parameter.

## 3. Components and complete banks

Notation: m=-a/b, P=-1/m, R=1/m, U is an explicitly supplied incidental candidate slope. Each listed slope combines with its paired independently supplied intercept d; those independent intercept slots preserve complete displayed equations. The constants are observed parameters, not a guessed dependence on the given line. The index refers to this recipe order, before option shuffling.

| Profile/source | Complete ordered slopes | Paired original intercepts | Correct index | Interpretation limits |
|---|---|---|---:|---|
| q-44404 | P,U,-m,m,R | -4,1,-6,15,-1 | 0 | U=-1; wrong slope intent unresolved |
| q-44514 | m,-m,U,P,R | 8,-1,0,3,0 | 3 | U=4/5; wrong slope intent unresolved |
| q-23378 | P,U,-m,m,m/2 | -6,-2,-5,1,3 | 0 | U=1/2; m/2 observed relationship, intent unresolved |
| q-23618 | R,m,P,U,-m | 2,1,8,8,2 | 2 | U=1; intent unresolved |
| q-23621 | 0,m,P,R,-m | m,0,0,1,-3 | 2 | first full equation y=m, a horizontal line |
| q-28338 | m,-m,P,U,R | 4,-3/2,-4,16/5,12/5 | 2 | U=-1/2; intent unresolved |
| q-28341 | -m,m,P,2P,U | 3,3,-5,-5/2,2 | 2 | U=-2/3; 2P observed relationship, intent unresolved |
| q-59763 | -m,m,P,R,-m | 0,1,5,-7,-3 | 2 | same-slope distractors are distinct full lines |

Every source option is accounted for by the full slope/intercept pair. U is not a fitted polynomial, guessed method error, or default distractor. Explicit U and d parameters define mathematical candidates whose slopes are independently tested. Observed scalar coincidences do not establish the original authoring code. Profiles remain selectable for replay and labeled variants. Standard slope/error relationships are parameterized without claiming recovered pedagogical intent.

The authored default is one complete bank [P,m,-m,R,0] with five independently sampled intercepts. It derives the required negative reciprocal plus four method-related alternatives: retain the slope, change only its sign, reciprocate without changing sign, omit the x term. These operation labels live only in metadata. Reject the whole sampled instance if full equations duplicate, any extra candidate is perpendicular, or any scope guard fails. No first-valid distractor pool, replacement of invalid choices, or new learner diagnosis is used.

## 4. Reusable value/Markdown template

Fixed sentences are the complete shared source prose, rendered in assemble(). Complete mathematical components are constructed structurally: standard line, isolated-y equation, optional unreduced slope/intercept fractions, reduced slope-intercept equation, chosen candidate and slope product. No blind prose replacements occur. Four-row layout inserts exactly one raw-fraction row; source q-28338 retains -4/10 and 20/10 before -2/5 and 2. Negative factors are parenthesized in the product as in the sources. The same one fixed worked solution is shown regardless of selected wrong option.

Required computed values: m=-a/b, n=c/b, P=-1/m, complete candidate pairs, exact uniqueness, one perpendicular candidate, conversion rows and product. Template standard3 omits the raw-fraction row; standard4 retains it. Bank selection precedes generation. Input/whole-bank failure rejects the entire explicit instance or resamples the entire random instance; it never changes an explicit parameter.

Source exactness is established separately from source mathematical equivalence, mathematical correctness and native radio grading. There are no repairs or excluded sources. Raw capture question/answer IDs are evidence only; generated UUID identities are field owned. Full content identity includes version, level, displayed prompt, complete solution, sorted complete bank and correct equation. Seed/option ordering cannot change identity. Mathematical task identity separately excludes source/profile/bank/intercept/scalar/layout spelling.

# Steps 5 and 7: plots

Plot rating none for all original and authored templates. All expressions are LaTeX text. No practice prompt, choice or worked solution refers to an asset; no plot extraction or renderer is needed. The owning lesson's introductory graph is outside this KP's practice templates. Stop after step 7; no registration or database preparation.
