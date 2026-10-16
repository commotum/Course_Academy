# Review controls

Run `python generate/pipeline/fixtures/build.py /tmp/generator-review-controls`.
Each resulting package is independently runnable with the usual generator CLI.
Give the reviewer only the shared `source/`, one package, the standard reviewer
prompt, and a fresh evidence directory. Keep this answer key outside its context.

These are synthetic controls, never live database content. All three packages
produce mathematically correct answers and replay every source case correctly
through `generate(parameters=...)`. They differ in ordinary sampling:

* `a` varies values and all four target cells within the source skill.
* `b` varies values but always asks for the upper-left entry. The source teaches
  both indices and includes all four positions; this is unjustified restriction.
* `c` asks for a sum of two diagonal entries. The answer is correct, but reading
  two entries and adding introduces an operation expressly outside this lesson.

An end-to-end review should accept `a` after completing the checks, reject `b`
with a `restriction` finding, and reject `c` with a `drift` finding. A rejected
control does not pass the evaluation merely because an unrelated tool failed:
the expected pedagogical finding must be present with source evidence and a
reproducible case. These controls establish that the reviewer can detect these
specific failures; they are not proof that all pedagogical failures are detectable.
