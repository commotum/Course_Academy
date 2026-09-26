# Assignment Cleanup Standard

## Markdown file boundary

- Begin every Markdown file created or modified by lesson cleanup with exactly one empty line. The first byte is a newline and substantive content begins on line 2.
- Collapse multiple leading empty lines to one.
- Represent an otherwise empty placeholder `.md` file as a single newline.
- Preserve a final newline at end of file.

## Quiz type selection

Invoke `$quiz-block-factory` before creating or changing a quiz block. Its schema reference is the single authority for supported types, canonical fields, answer encoding, feedback placement, and validation. Do not maintain a second field or type table in this cleanup reference.

For cleanup, preserve the source response shape and supplied choices. Choose among the factory-supported types from the task's response shape, not the number of sentences in its stem. Never change a fixed-choice source question into a different assessment merely to avoid an unknown answer key.

## Multipart problems

- Put shared givens, directions, and diagrams once before the part blocks.
- Give each independently answerable part its own block ID: `q-5a`, `q-5b`, and so on.
- Do not create a separate block for a drawing, derivation, explanation, or “show your work” direction that only supports one answer field. Use one block for the answerable response and include the supporting-work checklist in its feedback or reference answer.
- Use mixed types when appropriate. A diagram part can be `free`, followed by calculation parts using `blank`.
- Use one `select` only when all parts draw from the same option bank.
- Use one `multi-select` only when grouped dropdowns materially improve clarity.
- Do not force an entire multipart problem into `free` because one part requires a drawing.

## Correctness and source fidelity

- Preserve supplied option wording and academic meaning.
- Follow `$quiz-block-factory` for canonical correctness fields and cardinality once the answer key is established.
- Do not change a source question into checkbox merely because the correct radio option says “B and D only.”
- Repeated option text is not an image duplicate. Preserve it when it is present in the source, and report ambiguity if it creates more than one equivalent answer.
- Do not infer a missing answer key from option position or prior shuffle order.
- When the key is known, use the factory's feedback standard. Explain each supplied distractor's objective error and the controlling rule; attribute a specific misconception only when the option or source context supports it.
- When the key is genuinely unknown, do not invent correct flags, answer explanations, or a student's reasoning. Preserve the source question, run structural validation, and report both the exception and any consequent correctness-validation failure. In a mixed document, still require and lint feedback for the known-key blocks; treat only failures confined to unknown-key blocks as explicit exceptions.
- For `free`, follow the factory's reference-answer and feedback policy; do not imply that wording must match exactly.
- For `blank`, put the literal response the student should type inside `==...==`, not a typeset representation of that response.
- Match the number of blanks to the source response slots. Preserve multiple source blanks even when their entries combine into one mathematical expression. If the source provides one response slot, keep one blank rather than inventing separately labeled component blanks.
- Keep hidden answers plain and keyboard-enterable. Never wrap them in `$...$` or include LaTeX such as `\frac`, `\times`, `\sqrt`, `\mathrm`, or spacing commands. Do not include an equation label such as `f_5=` or a unit when the prompt requests a number only.
- Use `input_mode: math` when a symbolic or numerical answer should render as live visual math. Author its answer in keyboard form, such as `(x+3)^2-2`, `sqrt(x+1)`, or `2pi/5`; do not put LaTeX commands inside `==...==`.
- Display math may contain multiple live blanks on one row or across `\\` row breaks. Keep markers outside LaTeX brace groups that must remain syntactically intact.
- Prefer `require_exact: true` when an authoritative answer has one canonical typed form. Use `require_exact: false` only for an intentional answer-reveal field or when multiple equivalent typed forms make exact string grading inappropriate.
- In `input_mode: math`, exact grading compares math structure without algebraic simplification. Use reveal-only grading when algebraically equivalent alternate structures should be accepted conceptually.
- Use ordinary typed forms for nonnumeric answers too, such as `increases`, `pi/3`, or `x^2 + 1`. Put polished LaTeX in the prompt or feedback instead.

## Typed blank answers

- Treat the text inside each answer marker as input data, not display content.
- Match the source response format. If it says “Enter your answer in Hz,” store `500`, not `500 Hz`, `$500\ \mathrm{Hz}$`, or `$f_5=5.0\times10^2\ \mathrm{Hz}$`.
- Preserve meaningful decimal zeros when the typed answer requires them, such as `0.40`. When an integer entry such as `500` represents two significant figures, document the precise form $5.0\times10^2$ in feedback rather than encoding it in the input answer.
- For a symbolic or textual response, choose a natural ASCII form that can be typed without LaTeX knowledge. If several forms are equally valid, do not force exact string grading.
- For a live-math response, add `input_mode: math` and use the same natural keyboard form. The plugin restructures the entry visually as the learner types.
- State the expected input convention in the prompt when ambiguity is possible: “Enter a number only,” “Do not include units,” or “Use `pi` for $\pi$.”

## Numerical answers and significant figures

- Always independently check numerical answers, including supplied answers, for arithmetic, units, and significant figures.
- Follow an explicit rounding, decimal-place, tolerance, or significant-figure instruction from the source when one is present.
- Otherwise, round multiplication and division results to the fewest significant figures among the measured givens. For addition and subtraction, round to the least precise decimal place.
- Treat counted quantities, defined conversion factors, mathematical constants, and symbolic coefficients as exact unless the source indicates otherwise.
- Keep guard digits throughout intermediate calculations and round only the final displayed answer. Do not create intermediate-rounding error in feedback.
- Preserve trailing zeros that communicate precision, including forms such as $0.40$ or $2.0\times10^3$. If the source expects a bare integer input such as `2000`, preserve the significant-figure notation in feedback.
- Do not force a decimal approximation when an exact symbolic answer is more appropriate. When useful, show the exact expression first and its correctly rounded numerical value second.
- Keep units attached to displayed numerical results in prose and feedback, and verify that the unit dimensions are consistent. Omit units from the hidden answer when the source asks for a number only.
- If an authoritative supplied answer conflicts with the significant figures implied by the prompt, preserve the source meaning, use the best-supported presentation, and report the ambiguity rather than silently guessing.

## IDs and option order

- Use unique block IDs across the document.
- Use problem-based IDs: `q-1`, `q-8`, `q-8a`.
- Use short option IDs such as `a`, `b`, `c` within `radio` and `checkbox`.
- Use semantic IDs in shared option banks when helpful: `increases`, `decreases`, `unchanged`.
- Use `shuffle: true` only when reordering cannot change meaning.
- Omit shuffle for sequences, “all of the above,” “none of the above,” paired labels tied to order, or choices referenced by another part.

## Question and image order

For a single quiz block, keep the entire assessable stem and image in `content`:

````markdown
## Problem 3

```quiz
type: radio
id: q-3
shuffle: true
content: |-
  **Question 3**

  The graph shows ...

  ![](<Source/Assignment/Images/descriptive-graph.png>)
options:
...
```
````

For multipart work, keep shared material outside:

````markdown
## Problem 4

Shared setup and directions.

![](<Source/Assignment/Images/shared-diagram.png>)

```quiz
type: free
id: q-4a
content: |-
  **Question 4 — Part A**

  Draw ...
correct: |-
  The drawing should include ...
```

```quiz
type: blank
id: q-4b
require_exact: true
content: |-
  **Part B**

  Enter the result in meters per second as a number only: ==42==
feedback: |-
  The correctly rounded result is $42\ \mathrm{m/s}$.
```
````

Do not repeat the same shared image between adjacent part blocks. Across separate problem sections, reuse the same canonical file path when the source diagram is the same; repeat the embed when each question must remain independently readable.

## Daily lecture quiz folders

Treat the source notes as canonical:

```text
2026-06-24-M1-1/
├── 2026-06-24-M1-1.md
└── Source/
    ├── M1-1-PRE.md
    ├── M1-1-LEC.md
    └── Images/
```

For a single-step PRE or LEC question, do not add `## Problem N`. Put the source question label inside the block:

````markdown
```quiz
type: radio
id: m1-1pre-q1
content: |-
  **Question 1**

  Question text...
options:
...
```
````

For a multipart source question, use one `## Question N` heading for shared context and put only the part labels inside the associated blocks.

Make the dated root note a composition rather than a copy:

```markdown
## Pre-Lecture Quiz

![[Source/M1-1-PRE]]

## Lecture Quiz

![[Source/M1-1-LEC]]
```

Omit a section whose source is missing or empty. Preserve source-specific quiz IDs so PRE and LEC IDs remain unique when embedded together.

## Image ownership and naming

Canonical assignment path:

```text
Assignment/
├── Assignment.md
└── Source/
    └── Assignment/
        └── Images/
            └── descriptive-name.png
```

Assignment-owned images include:

- Images referenced by the assignment root Markdown.
- Loose screenshots or uploads dropped into the assignment root.
- Files already inside `Source/<assignment-name>/Images`.

For daily lecture folders, use the shared `Source/Images` directory. PRE and LEC source notes reference those images as `Images/<descriptive-name>`. The dated root note receives the images through source-note embeds and must not contain rewritten duplicate image links.

Protected images include:

- `Lessons/...`
- `Prerequisites/...`
- `Source/<Math-Academy-topic>/...`
- Any other copied source package not owned by the assignment

Naming rules:

- Use lowercase kebab-case.
- Name the physical setup or information shown: `rod-ball-inelastic-collision.png`.
- Include `graph`, `diagram`, `geometry`, `free-body-diagram`, or another useful qualifier.
- Avoid generic names such as `image.png`, `screenshot-2.png`, or opaque upload hashes.
- Avoid problem numbers when the same image serves several questions.
- Preserve the original extension unless conversion has a clear benefit.

## Duplicate policy

Classify candidates in this order:

1. Exact byte duplicates: safe to consolidate after reference checks.
2. Exact decoded-pixel duplicates: safe to consolidate after reference checks even if metadata or encoding differs.
3. Visually similar candidates: inspect manually; do not delete automatically.
4. Same subject but different crop, resolution, annotation, labels, or state: retain when the difference carries information.

Always update all Markdown references before removing the redundant file. Re-run the audit afterward.
