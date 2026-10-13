# Building a faithful question generator

The goal is to reproduce the structure and teaching style of the existing question bank while generating new mathematical instances. Mathematical correctness is necessary, but fidelity also depends on the question wording, notation, difficulty boundaries, answer choices, and the sequence of steps in the worked solution.

Start with the complete source questions for one knowledge point. A difficulty level can contain several structural templates, so analyze those separately before deciding which parameters to vary. Distinguish patterns observed in the source from assumptions about how the original questions were generated, especially when inferring distractor transformations.

A shared prompt/solution template may have several distinct choice-bank profiles. Map every original incorrect option to a parameterized recipe before merging patterns, preserving compound transformations and altered constants. Select a complete observed profile rather than the first valid recipes from a pooled list. Replay all source banks at their original parameters and compare complete equations or expressions, including valid equation rescaling and domain restrictions; report fidelity independently of mathematical correctness and grader compatibility. Every supported source bank must match in full, with source errors and exclusions recorded explicitly.

Answer-field type is part of the template. A single-answer multiple-choice (`radio`) field presents choices and identifies the correct option; a typed-answer (`blank`) field expects an expression that the learner's grader can evaluate. Generate distractors only for choice fields. For blanks, record the field key, placeholder position, supplied notation, and exact portion of the answer the learner must enter.

For example, **Finding the Cartesian Equation of a Curve Defined Parametrically With Trigonometric Functions**, knowledge point `17592186100890`, contains both types. An ellipse blank followed by `=1` expects only the left-hand expression, while a blank preceded by `y=` expects only the right-hand expression. Neither expects a complete equation. Its draft generator is in `generate/scratch/17592186100890.py`; it supports only field-type combinations observed in the source and uses positive scaling by default for moderate questions, retaining source coefficient provenance.

In the current schema, a blank still has an owned canonical answer entity referenced by both `:answer-field/choices` and `:answer-field/correct`; that answer is a grading reference, not a displayed distractor. Preserve delimiter-free mathematical answer values and render surrounding notation through the prompt. Check accepted equivalent entries and rejected incorrect entries with the learner's actual grader before serving questions: SymPy checks in the generator do not establish engine grading compatibility. Retain domain and branch restrictions separately from the expression, and identify source errors instead of copying them.

Each generated question should have one fixed worked solution, regardless of the learner's selected answer. Preserve the source's repeated instructional sentences and intermediate algebra rather than replacing them with a shorter explanation. Where the originals provide no option feedback or distractor reasoning, keep those explanations out of the question presentation; internal error recipes can still guide choice generation.

Our first example was **Using the Product Rules for Differentiation**, knowledge point `17592186115393`: easy questions use scalar–vector products, moderate questions use dot products, and hard questions use cross products. Some moderate and hard questions involve a derivative as one factor, and one moderate template evaluates the result at zero. That first draft was removed and has not yet been rebuilt.

This workflow produces a reviewable generator before database integration. Match the existing schema's field types and answer representations, and retain enough version and parameter information to reproduce an instance. Database writes and decisions about storing generator recipes belong to a later stage.

## Step-by-step process

1. Pull every source question, answer field, choice, correct answer, and worked solution.
2. Group questions by structural template and answer-field type within each difficulty.
3. Record each template's notation, domains, parameter ranges, answer shapes, and grading rules.
4. Preserve its repeated wording, field placeholders, supplied notation, and ordered solution steps.
5. Identify which values can change without changing the template or answer-field contract.
6. Map every original incorrect choice to an explicit parameterized recipe and complete source bank profile.
7. Generate parameters and compute the exact correct answer or required blank fragment.
8. Select a source bank profile and build all its distinct distractors, or retain only the canonical answer for blanks.
9. Render the prompt, answer fields, and one fixed worked solution through the preserved template.
10. Replay every source bank at its original parameters and require a complete mathematical match independent of option order.
11. Check correctness, actual grading, profile selection, parameter boundaries, formatting, ownership, and schema compatibility.
12. Report source-bank fidelity separately from correctness and grading, including every missing or extra option.
13. Review originals and variants side by side before freezing the generator version.

For choice fields, use the observed choice count: these source banks have four distractors for five-choice questions. Blank fields have no distractor-generation step. Follow the numbered [generation guide](docs/3-classify.md) for implementation and validation details.
