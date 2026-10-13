# Template extraction

## 1. Specific source descriptions

`source-components.json` gives every actual entry, row count, column count and complete original field bank. q-11454 has signed integers in a 2×4 bmatrix, inline after a line break; q-7806 has integers in a 2×3 bmatrix in the same layout. q-125527 is a 6×6 inline aligned array with integers (including zeros and repeated entries). q-125528 is a 2×2 array with two radical entries and −23. q-125529 is a 3×3 array containing signed integers, zero and radicals. q-69542 is a 4×2 integer array with a line break before its matrix. q-139406 is a 3×3 matrix P, introduced as Maria's representation of a table; no table is actually supplied or required. It requests rows and columns as separate blanks around ×, with capture whitespace. q-319310 is a 5×5 K with integer, radical and fractional entries and two blanks after “Let”.

All radio sources have five **ordered dimension pairs**; blanks have one integer fragment each, not a combined product. All six available solutions consist of one fixed sentence: count rows, count columns, then state the ordered dimensions. The two legacy cases have no source solution; the same canonical sentence is authored for them. The canonical sentence does not calculate entries.

## 2. Generalized shared pattern

Given one fully displayed rectangular array with at least two rows and columns, count horizontal rows and vertical columns, reporting row-count × column-count. Entry sign or number form has no effect. Preserve two-count field layouts separately from whole-pair radios, and preserve the three radio prompt/layout masks plus two blank masks separately.

## 3. Component and complete-bank mapping

`recipes.json` stores parameterized prompt masks with complete `@ARRAY@` and `@NAME@` components; it never stores a complete answer payload or chooses an answer by source ID. `source-components.json` maps every original radio choice one-to-one to its separator and the following symbolic pair recipe, evaluated with independent row/column counts r,c. Original blank mapping is field-1→r and field-2→c, while preserving original collection order.

| Profile/source | Entire bank in captured order |
|---|---|
| q-11454 | (c,r), (r,c), (r,r), (r+1,r+1), (r,c−1) |
| q-7806 | (r,c), (c,r), (c,c), (r,c+1), (r,r) |
| q-125527 | (r−1,c−1), (r,c), (r−1,c), (r−2,c−2), (r,c−2) |
| q-125528 | (r,c+1), (r−1,c−1), (r,c), (r+1,c), (r+1,c+1) |
| q-125529 | (r,c−1), (r−1,c−1), (r+2,c+2), (r+2,c), (r,c) |
| q-69542 | (r−1,c), (c,r), (r,c), (r,c+1), (r−1,c+2) |

The large offsets and midpoint-square member are exact observed **expression patterns**, with underdetermined pedagogical intent. They are available only as labeled explicit replay profiles; this document does not claim those scalar offsets recover a learner error. Five distinct positive dimension pairs are required together before any complete instance is eligible. Every observed bank is exhaustively checked on all 25 dimension pairs; exact eligible domains are recorded in `validation.json`. No pooled-bank first-valid fallback is used.

## 4. Reusable template and finite domains

Fixed: original prose and Markdown mask, environment, answer-field type/key/order, every bank recipe/separator, one row/column sentence and its stage order. Variable: a complete rectangular array and its matrix letter; derived: r, c, every bank value, each blank count and four count occurrences in solution. Source q-139406's R/P error is preserved only on explicit replay with original name P, and the raw source remains unchanged. The other available solutions replay byte-for-byte. Raw replay omits the two missing solutions/keys and unrated labels. Independent inferred counts are 2×4 and 2×3, but cannot count as matched designations or native-gradeable raw fields.

Normal easy output samples all five observed prompt families and both response layouts. Normal radio banks are separately authored complete counting-operation banks, chosen before random dimensions. Rectangular: (r,c), (c,r), (r,r), (c,c), (r+1,c+1). Square: (r,c), (r−1,c−1), (r+1,c+1), (r,c+1), (r+1,c). Square and rectangular domains are disjoint; no equivalent reversed choice enters a square bank. All complete banks are rejected if any pair is repeated, nonpositive, or there is not exactly one correct ordered pair. Explicit profiles use the same guards as samplers; no invalid member is replaced or drawn from a pooled first-valid list.

The legacy EDB dot separator is a dimension separator interpreted as an ordered pair, not evaluated by scalar multiplication. Thus 2×4 and 4×2 are distinct responses even though both products equal eight. Native radio grading checks owned IDs; independent validation separately parses every displayed ordered pair and counts actual printed rows/columns. The missing legacy keys stay absent in raw replay; native coverage excludes these two raw cases explicitly.

The historical offset recipes have underdetermined intent. For example q-125529 at r=c=3 has a 5×5 choice: both (r+2,c+2) and (2r−1,2c−1) reproduce it. q-125527 at r=c=6 similarly cannot distinguish additive undercounts from some proportional expressions from one bank alone. We retain the bounded additive count-pattern masks as evidence replay recipes, not a claim that proportional mistakes were recovered. Changed-parameter evidence is labeled opaque and ineligible for learning. The source bank values nevertheless replay exactly, not through copied payloads or answer-ID lookups.

Meaningful domains are finite and disjoint: easy `{2..6}²` (25), moderate `(2..6)×(7..12)` or `(7..12)×(2..6)` (60), hard `{7..12}²` (36), union 121. Moderate peers have exactly one extended enumeration and hard peers two. Every question still performs exactly the same two operations: count rows, count columns, then write dimensions in order. Bounds are a counting-workload design claim rather than observed labels; documentation does not claim a new mathematical method. Explicit input cannot cross domains or disguise an easy instance with complicated entries.

Easy entry syntax covers observed signed integers |n|≤30, familiar surds with radicand 2..13 and bounded fractions. Moderate/hard restrict to integers −9..9 to keep twelve-column arrays legible; numerical values remain incidental. The task fingerprint contains only ordered counts r,c, excluding entries, name, field layout, bank profile and level aliases. Content identity includes version, actual difficulty presence/value, printed prompt, entire fixed solution or its absence, field layouts, complete bank, and correct-ref presence. Option order and seed do not alter identity for fixed explicit inputs. Batches exhaust ordered shapes without replacement and reject excessive counts rather than padding with incidental variants.

This draft has no database registration, writes, or transaction payloads. Registered files are read-only evidence; registered-baseline.json and validation check their byte hashes.
