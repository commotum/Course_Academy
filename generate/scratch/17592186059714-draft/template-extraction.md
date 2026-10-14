# Four extraction stages

## 1. Specific original records

q1325 asks the magnitude of v=(4,-1), followed by the scientific-calculator block. Bank order in immutable EDB is 5,3,sqrt(17),sqrt(5),sqrt(7). No rating, worked solution, feedback or correct reference is captured. q18046 asks |a| for a=(-12,3), retains the same calculator instruction, and has bank 3sqrt(19),sqrt(152),3sqrt(15),3sqrt(17),sqrt(157), with the same omissions. Both correct values are independently inferable but cannot count as captured correct references.

q18047 asks |a| for (5,9). Its easy solution retains the exact opening (including trailing space), then the formal formula, substituted squares, 25+81, and sqrt106; it does not insert a separate sum-only row. q18048 asks magnitude for (-4,8), is easy, and retains formal formula, signed substitution, 16+64, sqrt80, sqrt(16*5), 4sqrt5. Both are fieldless; no unknown original answer widget is invented. All raw parameterized text at original inputs is exact, including punctuation and absence of feedback.

## 2. General shared backbone

Given two real components directly, evaluate sqrt(x²+y²). The two roles are the supplied horizontal/vertical components and their corresponding ordered squares. The nonnegative root is required. Each source mask keeps its wording and operative row sequence. Normal completions of absent solutions use the canonical opening and explicit formal/substituted/evaluated-squares/summed-root/reduced-result stages; q18047 and q18048 keep their captured sequences. Different components never change this skill.

## 3. Component and complete bank maps

source-components.json contains every source option, exact value, squared value, matched recipe, source field and interpretation status. q1325 squared-bank pattern is (25,9,17,5,7); q18046 pattern is (171,152,135,153,157). With a positive homothety s of the source vector, raw options are s*sqrt(each captured squared value), retaining the original exact lexeme at s=1. This is a genuinely parameterized homogeneous pattern, not a fitted scale/offset perturbation. It is evidence-only: values do not uniquely establish the historical mistake operations. Raw banks stay out of normal generation. Positive scales retain baseline bounds1..8 and1..3 respectively. Changed raw profiles are tested through the public generate API, not a private copied-payload branch.

Normal complete bank `norm-stages` consists of sqrt(x²+y²), x²+y² (omit final root), |x|+|y| (replace norm by absolute sum), sqrt(|x|+|y|) (omit both squares), sqrt(|x²-y²|) (subtract squared terms). Complete bank `omit-component` consists of sqrt(x²+y²), x²+y², |x|, |y| (omit the other squared term before the root), |x|+|y|. These operations arise from the actual squaring/sum/root method. There is no first-valid pool, random perturbation, scalar fit or invented error-specific feedback. Derive the correct norm first; construct every member of the preselected bank and reject the whole bank on any pairwise equality. Exact values are the actual response criterion, including equal radicals rendered differently.

## 4. Reusable masks and slots

Template slot x and y replace the complete component tuple, complete substituted operands, each ordered evaluated square, radicand, optional extracted rational square factor and final reduced result. q18047 retains its direct final-root fourth row. q18048 retains all six rows, including explicit factorization and concluding root. Normal q1325/q18046 use the canonical sentence and five rows because their original worked solutions are absent; this is explicitly authored completion. Calculator paragraph and known true schema flag remain in both source-radio families. No new rounding rule is introduced.

Variable slot constraints are the documented reduced arithmetic bands in classification.md and generate.validate_parameters. Optional components are only source-present difficulty, solution, answer-field or calculator attributes in raw replay; normal fields/keys/ratings are authored completions. q18048's factorization mask requires an extracted square factor different from1 in normal generation. Explicit invalid inputs raise instead of changing caller parameters. Raw easy solution masks allow integers within1..12; raw historical radios allow only their validated positive-scale slot.

Content IDs use version, actual displayed prompt, fixed solution, calculator attribute, rating and complete displayed bank. They ignore seed, option order and profile aliases. Field and answer UUIDs are owned by the resulting question. Mathematical fingerprints separately track the unordered two squared operands; equal final norms from different square sums retain different task fingerprints. API metadata stays outside learner-facing content.

Raw limitations: all four original grading contracts are incomplete; historical scalar error intent is opaque. This is preserved and reported separately from exact source fidelity, independent mathematical correctness and real native checks on normal completions. No source bank/math errors were found. No figures are required.
