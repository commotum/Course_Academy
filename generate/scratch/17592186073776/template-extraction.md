# Four-stage template extraction

## 1. Describe each source before generalizing

**q-211984**: `6x + 4y = 6; - 2x - y = 5`; integer coefficients, standard RHS constants, signed initial x/y coefficients in the second equation, single inline system preceded by “Consider the following system of equations:” and followed by “This system of equations has {{field-1}}.” Select key field-1; observed values in EDB pull order are no solutions / infinitely many solutions / a single solution. Neither difficulty, answer key nor worked solution appears. Independently multiplying equation two by 3 gives `-6x-3y=15`; adding gives `y=21`, followed by `x=-13`. Therefore its inferred response is a single solution.

**q-237043**: `y - 3x - 2 = 0; 4y - 12x - 8 = 0`; y-first ordering, all terms on LHS, nonzero constants, a multiple second equation. Same prose/select layout. EDB pull order is a single solution / infinitely many solutions / no solutions. Its captured MA widget has a different display order but the identical complete value set; choice order is not a semantic bank difference. Independently rearranging gives `-3x+y=2; -12x+4y=8`; multiplying equation one by -4 and adding gives `0=0`. Inferred response: infinitely many solutions.

**q-237046**: `2x - 5y = 15; 4x - 10y =-10`; standard form; the source has no space between the final equal sign and unary minus. Same prose/select layout. EDB bank order is no solutions / infinitely many solutions / a single solution. Multiplying equation one by -2 gives `-4x+10y=-30`, adding gives `0=-40`. Inferred response: no solutions.

All prompt braces are the same literal system glyph imported as unescaped `{`. There are no solution strings to recover for these practice records. Raw omissions and source IDs are retained in `source.json`; author conclusions are separated in `source-cases.json`, review and generation metadata.

## 2. Generalized family and purpose

Both families present exactly two linear equations in x and y and request one classification from the same complete categorical bank. `standard` displays ax+by=c and dx+ey=f. `zero_rhs` displays by+ax−c=0 and ey+dx−f=0. The second family requires rearrangement before the same elimination operation. No extra number-of-variables branch is added.

## 3. Component and complete-bank mapping

The parameters a,b,c,d,e,f are *whole coefficients/constants*. Variable labels are fixed x,y and never counted as mathematical diversity. Source parameters and raw profiles are recorded one-to-one in `source-cases.json`.

| Source/profile | (a,b,c,d,e,f) | no solutions | infinitely many solutions | a single solution |
|---|---|---|---|---|
| q-211984 / raw_211984 | (6,4,6,-2,-1,5) | valid categorical wrong concept | valid categorical wrong concept | inferred correct |
| q-237043 / raw_237043 | (-3,1,2,-12,4,8) | valid categorical wrong concept | inferred correct | valid categorical wrong concept |
| q-237046 / raw_237046 | (2,-5,15,4,-10,-10) | inferred correct | valid categorical wrong concept | valid categorical wrong concept |

Each bank comprises all three rows, never an option pool. Every original text value and field type/key matches exactly; no numeric wrong-operation inference is required because the requested response is categorical. A two-solution alternative is absent from these sources and is not authored here.

Fixed components: prompt opening, response sentence/placeholder, x/y names, one select field, its three complete textual values. Variable components: six whole integers and signs. Conditional components: signs, omission of unit coefficients, zero constant terms in zero-RHS display, raw unary-minus spacing, compact negative RHS spelling, outcome-specific conclusion. Optional components: difficulty, solution and correct key are absent only in explicitly evidence-only raw profiles.

## 4. Reusable prompt, method and bounds

The raw generator constructs each prompt from six parameters and a formatting profile through the *same public generate API*. It never reads source questions or returns literal payloads; changing parameters changes the actual system. Raw profiles generalize coefficient slots while preserving the observed omissions. `counts` is the normal complete source-shaped bank.

Normal solutions share the canonical opening “Let's start by solving the system using elimination.” They retain its operative stages: identify the multiplier/cancelling term, show the system with the row multiplier annotation, display both transformed equations in prompt order, write the uncollected constant sum after cancellation, collect the statement, and interpret always-true/always-false results using the canonical/tutoring prose. The unique branch continues through y isolation, substitution into the first equation, collection, x isolation, and the single-point conclusion. `zero_rhs` adds an explicitly authored two-row rearrangement first; it does not omit the common elimination stages. No choice-specific diagnosis is shown. There is one fixed worked solution regardless of selected option.

The integer multiplier is −(larger x coefficient)/(smaller x coefficient). Exact Fraction arithmetic computes all stages before rendering; signs are rendered visibly and products of numeric factors use parentheses. Displayed equations independently yield the rank classification. QA also checks every transformed/summed/substitution equation from the actual rendered text.

Default sampling uses a smaller x coefficient from ±1..±3, first y coefficient from ±1..±3 (hard: ±1), a base constant from −6..6 (moderate/hard: nonzero), and an x multiplier of ±1 at easy or ±2..±4 otherwise. Dependent systems carry the same multiplier into y and the constant; inconsistent systems alter that constant by ±1..±3. Unique systems choose a distinct second y coefficient from ±1..±5 and a second constant from −12..12. Every choice is subject to the full level guard. Standard-form rows can be interchanged, so both first- and second-row transformations occur at moderate. These narrower sampler choices preserve the source integer arithmetic; explicit valid source inputs remain permitted under the same maximum workload ceilings.

All mathematical explicit inputs obey the same level boundaries listed in `classification.md`; unsupported templates/fields, noninteger coefficients, zero variable coefficients, excess absolute magnitudes or invalid multiplier/zero-RHS demands are rejected without replacing input parameters. Samplers choose the complete bank/family and outcome branch before sampling a valid actual system, rejecting the whole instance when constraints fail. Bounds are supported arithmetic design choices, not purported recovered source code.

Content identity includes the actual displayed prompt, difficulty/omissions, fixed solution and complete bank; seed/order changes do not alter identity. Mathematical-task identity normalizes each complete line equation by its first nonzero coefficient, sorts the equation pair and canonicalizes x/y interchange. Thus individual/global scalar multiples, equation order and variable aliases cannot inflate counts. Distinct actual line objects remain meaningful rather than collapsing all systems of a given rank or count into one task. The `zero_rhs` information form is retained because rearrangement is part of the assessed workload; profiles and answer banks are excluded from task fingerprints. Current variety counts are distinct canonical tasks from a specified 360-seed sample per level, **not estimates of total domain size or claims of thousands of skills**.

## Source repairs and omissions

Exact prompt/bank replay: 3/3 prompts and 9/9 options. Exact original correct-designation matches: 0/0 (all missing); three mathematically inferred completions. Exact solution-string matches: 0/0 strings present; 3/3 omission matches. Normal output applies the supported literal-brace presentation repair to each original-parameter completion, and authors levels and worked solutions. Raw malformed evidence is ineligible for learner use and remains available through raw profiles; normal output must pass formatting QA.

## Plot extraction / specification

Rating none for both assessed families: no prompt, choice or practice-solution graph exists. The canonical illustration is context only: two parallel descending lines labeled with its two standard equations. Inspected file `/home/jake/Developer/MA/DATA/Lessons/493/Source/Images/369f6564f4a005f3d2e493ead23a3c10.png`. It is not copied into generated tasks; there is no asset renderer or changing geometry to reconstruct. No direct SVG or image model is used.
