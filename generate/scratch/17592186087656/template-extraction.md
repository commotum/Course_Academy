# Four extraction stages

## 1. Specific source descriptions

Each question gives a circle equation in two Cartesian coordinates with coefficient one on both translated squares and positive RHS. Every response is a whole prose pair “The center is $(a,b)$ and [the] radius is $r$”; no equation fragment or blank field occurs.

| Source | Displayed shifts a,b | RHS S | Radius form | Prompt/solution features | Bank |
|---|---|---:|---|---|---|
| q-7521 | 2,3 | 6 | sqrt(6) | compact; no article; radical square parenthesized | q-7521 |
| q-7527 | -5,-1 | 4 | 2 | spaced polynomial; question mark outside math; missing difficulty/solution/correct; positive reflected tuple has comma space | q-7527 |
| q-117087 | 5,0 | 3 | sqrt(3) | “the radius”; bare `{y}^2` in given/comparison; restored `(y-0)^2`; extra grouping around radical square | q-117087 |
| q-70900 | 2,-2 | 9 | 3 | negative y offset explicitly written as y-(-2) in final row | q-70900 |
| q-70935 | -3,-3 | 5 | sqrt(5) | both negative offsets restored in final row | q-70935 |
| q-70933 | -1,-6 | 16 | 4 | both negative offsets restored in final row | q-70933 |
| q-117084 | -5,3 | 81 | 9 | “the radius”; x-(-5) in final row | q-117084 |
| q-117086 | 7,10 | 100 | 10 | “the radius”; final LHS repeats given LHS because no negative/zero shift | q-117086 |

All original field layouts are one five-choice text radio keyed `selection`. All source choice values and original choice IDs are mapped one-to-one in `bank-map.json`, including q-7527's absent correct designation. Source-cases preserve every practice record and its observed difficulty omission. Nothing is inferred as an observed label.

## 2. General shared pattern

Read a and b by matching `(x-a)^2+(y-b)^2=S` with the generic circle equation, and read the radius as the positive square root `sqrt(S)`. The answer is the ordered center and radius pair; matching only a scalar radius cannot establish answer equivalence. Negative translations use nested signs, and zero translations can be implicit in the given equation.

## 3. Component and bank mapping

Variable components: complete x-square and y-square, RHS S, complete center tuple, exact positive root, root squared in the final comparison row, and each complete answer sentence. Fixed components: general-equation display, comparison sentence, generic comparison row, “We see that” and conclusion sentence. Conditional components: article “the”, source spacing, implicit zero term, restoration of negative/zero translations, integer versus radical squared notation, legacy omission of solution/difficulty/correct ref. Prompt and solution are constructed from mathematical slots, never global textual replacement.

Each complete bank is selected before sampling. Define C=(a,b), R=sqrt(S), B=(-a,-b), X=(-a,b), Y=(a,-b), O=(0,0). Every profile comprises all five following pairs, rendered using its captured prose style:

| Profile | Complete ordered recipe bank |
|---|---|
| q-7521 | (C,S), (B,S), (O,R), (B,R), (C,R) |
| q-7527 | (C,R), (C,S), (B,R), (B,S), (C,S²) |
| q-117087 | (B,S), (O,R), (B,R), (C,S), (C,R) |
| q-70900 | (Y,R), (X,R), (B,R), (C,S), (C,R) |
| q-70935 | (C,S), (B,S), (B,R), (C,R), (Y,S) |
| q-70933 | (C,R), (C,S), (B,R), (X,R), (B,S) |
| q-117084 | (B,S), (C,R), (B,R), (C,S), (Y,R) |
| q-117086 | (B,S), (O,R), (C,R), (B,R), (C,S) |
| authored | (C,R), (B,R), (X,R), (Y,R), (C,S) |
| authored_axis | (C,R), (B,R), (C,S), (B,S), (O,R) |

Sign-error recipes take literal constants in the translated squares rather than reversing them. Radius errors omit the square root or square the given RHS again. Origin recipes drop the translated terms' offsets. Compound errors apply both operations. These are direct operations of the assessed matching/root method; the exact source author's intent is not independently recoverable, and these labels are author metadata rather than learner diagnoses. There are no opaque polynomial-fit values. All banks reproduce all observed members numerically and textually, including the source-specific redundant `4^{2}`.

## 4. Reusable rendered template and restrictions

The normal prompt is “What is the center and [the] radius of the circle with equation $<complete translated squares>=<S>?$”. Source q-7527 uses its exact captured spaced form and punctuation. A normal fixed worked solution has the general-equation display, shared comparison sentence, exactly three ordered rows (generic, actual given equation, explicitly interpreted center shifts and squared radius), parameterized a/b/r sentence, and parameterized final center/radius sentence. Original redundant final rows are retained, not algebraically collapsed. Authored hard questions retain this entire sequence and additionally display `r = sqrt(S) = sqrt(c²·d) = c sqrt(d)` before the substitution prose, with a visible factor product; all three stages are independently checked. This is an authored arithmetic explanation, not an observed source row.

The complete bank is computed and rejected as a whole if any pair is duplicated or the correct pair is not unique. No first-valid distractor replacement occurs. Profiles requiring sign errors become invalid when their reflected values coincide; normal axis questions use the explicitly separate authored_axis bank. Radius S=1 is excluded because R=S. Everything is exact SymPy mathematics and deterministically sampled. The actual rendered equation, all option triples, comparison rows, and prose values are independently parsed by `validate.py`; metadata equality alone is insufficient.

## Source incompleteness and separate completion

q-7527 has no difficulty, solution, or correct designation in the capture. The local authoritative topic widget in `/home/jake/Developer/MA/DATA/Lessons/843/Source/843.json` confirms the same five choices and one multiple-choice layout; its private excerpt is `authoritative-q-7527.json`. It supplies no correct designation. Mathematics uniquely derives center (-5,-1) and radius 2. `profile=q-7527` remains a parameterized raw API replay, preserving omissions and flagged evidence-only. `profile=q-7527_completed` is a separately labeled inferred completion with this correct ref, authored easy assignment, and the shared worked-solution stages. It is eligible for learning and native-tested; its added fields do not count as source-fidelity matches. No raw missing designation is counted as matched. There are no mathematical source errors or malformed TeX requiring repair.

## Identity, dependencies and freeze

Canonical task fingerprint is reduced (a,b,S), independent of seed, bank, spacing, and difficulty; it represents the assessed extraction from the standard equation. Presentation/content identity includes generator version, displayed prompt, fixed solution, full unordered displayed bank, correct designation/omission and actual difficulty/omission. UUIDs are deterministic and field-owned. Different orderings alone preserve identity. Metadata records real SymPy version, basis/lineage, source IDs and domain separately from learner content. `validation.json` records frozen script and native-engine SHA256s. Work stops after step 7; no database records are prepared or written.
