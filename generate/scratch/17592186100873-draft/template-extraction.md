# Four extraction stages

## 1. Specific originals

source-components.json contains every complete captured source record, explicit
A/B matrices, cell indices, field ID/type/key, answer ID/value, correct-ref
presence, inferred exact arithmetic and complete bank mapping. q-70791/70792 use
inline matrices and no stored solution/rating/key. q-130111/130120/70956 use
three-term dotted expansion; q-70946/70949/70958 use two terms. q-275547 is a
2-term dotted blank. q-318462/318463 are3-term parenthesized blanks; q-318470
is2-term parenthesized blank. Original dimensions range2–5 outer rows/columns
and2–3 inner dimension. All entries are integers; whole matrices include zero
and signed values through20; assessed factors through10, products through30,
L1 through58, bank magnitudes through58. These are coupled ceilings, not
independent coefficient boxes. No source feedback or answer fragments beyond
one scalar after the displayed cell notation occur.

## 2. Shared pattern and stable backbone

Supply two full matrices and C=AB. Request c_ij. State which row/column to
multiply; display both full matrices; extract the selected row and column;
expand the ordered scalar products; evaluate each signed product; collect to
one integer. Preserve all five aligned rows and source shared prose. One fixed
worked solution is generated independently of the learner's selected error.
The full first row is retained despite representing a selected entry; this
matches the source pedagogical shorthand, and does not ask for the full product.

## 3. Components and banks

Every source choice is individually mapped in source-components.json. Historical
scalar wrong values do not determine their operations. Their public observed:
profiles retain opaque integer patterns, computed designated correct values and
raw omissions; they are evidence-only and never sampled for learning. This is
not a claim to recover error intent. No arbitrary polynomial fit is used.
All44 values across12 banks replay;10 historical keys match,2 are truly missing.

Normal five-choice profiles are separately authored complete operations:
method-omit-sign = [sum(products), sum(all but last), sum(abs(products)),
negative sum(products), sum(row)+sum(column)].
method-reverse-column = [sum(products), dot(row,reverse(column)), first product,
sum(all but first), dot(row,row)]. These represent omission, sign loss/reversal,
entry addition, reversed alignment and use of the row as both inputs. Blanks
retain their observed one canonical scalar and supplied cell-equals fragment.
Choose a whole profile before parameters. Compute every member; reject the
entire instance for any collision or magnitude>58. Never replace a single
invalid option or select first-valid errors. No distractor diagnosis is added
to learner content. Evidence flags are explicit on all opaque public replays.

## 4. Reusable masks, slots, domains and dependencies

Source shapes, field contracts and source label sets are fixed per mask.
A and B are whole-matrix slots with compatible source shape; row and column
independently range over every valid requested cell. The eligible target role
is any entry of this same product, not a source-fixed location. Target changes
update the prompt, supplied blank fragment, prose ordinals, selected row/column,
ordered factors/products and correct key together. Source missing solutions
receive the same common instructional prose only in authored normal records.

Normal sampling uses signed integer matrices−6..6. All public explicit inputs
obey the same ceilings: whole operands≤20, selected operands≤10, each assessed
product≤30, sum of assessed absolute products≤58, every bank member≤58.
At least two assessed products are nonzero. Easy3 has unit/zero support in at
least one factor pair; Easy2 retains two substantive products. Moderate/Hard
both require three terms and all six assessed factor magnitudes2..6. Moderate
requires each product≤16 and L1 12..36; Hard requires mixed product signs and
L1 37..58. Exact original profiles keep all observed raw parameters, with the
same global source ceilings but no authored-level guards. Invalid explicit
calls raise; random calls resample whole instances. No hidden expression branches.

IDs are computed after shared math_format normalization from actual prompt,
worked solution, difficulty, field contract and complete bank; order/seed/profile
alias cannot create an ID. Task fingerprints use ordered assessed row/column
vectors plus target relation and actual level, excluding irrelevant matrix
entries, labels, distractors and seed. Full irrelevant entries remain in content
identity. Large finite integer domains provide repeated practice:600 seeds yield
598/600/600 substantive tasks (not a claim of exhaustive enumeration). Slot
coverage and fixed-matrices/changed-target regressions are separate from this
count. Exact source replays reproduce the complete original strings through
parameterized masks rather than returning completed captured question payloads.
