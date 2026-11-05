# 6. Template Generator

Use the templates from [Template Extraction](4-template-extraction.md), including any attached plot specifications. Start with one Python script in `generate/scratch/<knowledge-point-db-id>.py`, with documented sections for each difficulty and shared helpers.

1. Use SymPy for exact symbolic work, seeded randomness for reproducible sampling, and Matplotlib for plots, with TikZ when needed.
2. Implement parameter samplers covering the observed values and features, preserving template constraints and field types, and explicitly label extensions or narrower sampling policies.
3. Compute the correct answer first, then derive the intermediate solution values and any mathematical data needed by plots.
4. For choice fields, select an eligible source bank profile and apply all its mapped recipes; for blanks, produce the exact required answer fragment.
5. Render the original Markdown structure, field placeholders, answer values, and shared instructional sentences into one fixed worked solution.
6. If new plots are required, call [Plot Generator](7-plot-generator.md) with the same instance data and insert its returned assets; otherwise reuse unchanged assets or continue without plots.
7. Expose generators by difficulty and template, with seeded Markdown and JSON previews containing the question, fields, answers, and reproducibility metadata.
8. Replay every source question at its original parameters and bank profile, comparing its complete generated answer bank with the original bank.
9. Check every supported template, field combination, and bank profile for mathematical correctness, actual grading, parameter boundaries, profile selection, formatting, plots, and deterministic replay.
10. Report fidelity separately from correctness and grading, then review originals and variants side by side before freezing the generator version.

Resample parameters when they produce invalid or ambiguous questions. Preserve the source choice count, blank answer shape, notation, and solution sequence; keep inferred error recipes out of the learner presentation unless the source includes feedback.

Do not take the first valid recipes from a pooled list. Choose a complete profile before constructing its bank, then reject or resample the instance if any required option is correct, equivalent to another option, or otherwise invalid. Any mixed-profile bank is an explicitly labeled extension. Record the selected profile and recipes in reproducibility metadata, and ensure different authored banks cannot collide under one question identity; seed changes and option shuffling alone still do not create new questions.

Source-bank replay must match every original option to exactly one generated option, ignoring order while preserving choice count and the correct designation. Compare complete mathematical objects: equations may be equivalent under multiplication by a nonzero constant, and domains and branches must be respected. Comparing equation sides independently is insufficient. Keep rendered notation and solution-layout checks separate from algebraic equivalence.

Report matched/total source distractors and complete banks per template and profile, with every missing or extra option identified. Require full coverage for supported source banks before declaring fidelity or passing output to database preparation. Source errors need recorded evidence and a supported correction or explicit exclusion; unresolved comparisons remain failures. Correctness tests and radio ID-selection tests cannot satisfy this requirement.

Exercise every profile under its applicable parameter conditions, including zero/nonzero shifts, equal/unequal scales, and signed values where relevant. Check selected banks, not merely candidate recipe availability, so later profiles cannot be silently excluded. Vary parameters to check that recipes generalize rather than copying source literals; sparse source evidence still limits what can be inferred.

For blanks, test accepted equivalent entries and rejected incorrect entries with the actual learner grader. SymPy checks in the generator do not establish engine grading compatibility.

Use the existing question, field, and answer representations, with field-owned answer identities and delimiter-free mathematical values. Record generator version, dependency versions, seed, parameters, domains, and source references separately from those records. Keep drafts and assets local for review, then pass validated instances to [Database Preparation](8-database-prep.md).
