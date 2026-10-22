# Templates and bounded capability

`template-extraction.json` maps every source prompt, solution, field, correct
value and all 60 choices to its original field/profile and a complete expression
recipe. These are fixed symbolic expressions, not inferred numeric error rules.
The JSON distinguishes each source and retains literal malformed source evidence.

The supported backbone is: recall the four clauses of the invertible matrix
theorem; identify one missing symbolic fragment; choose one of five options;
read a full-theorem reminder and the concrete missing expression. Domain: real
n by n matrices with integer n >= 1. A zero subspace, scalar zero, scalar dimension,
matrix and ambient vector space are different types.

The missing fragment is a categorical target slot. Its mathematical operation,
side of the equality and answer shape determine the template. The seven usable
profiles cover all five supported targets. The complete source bank is chosen
before replay; no banks are pooled, synthesized, shuffled or mixed. All other
components are fixed because the recovered task assesses recognition of this
particular symbolic theorem, not arithmetic.

No numerical slot is observed or declared. Renaming A or n, changing spacing,
reordering the clauses, or changing option order does not change the assessed
relation. Replaying another bank at the same target also repeats the task.
The finite supported domain is exhausted by existing source identities, so the
normal generator returns an explicit finite-limit with no instances. `--replay`
is evidence-only and always marks output ineligible for learning.

Other theorem fragments could be studied in future authored extensions. That
possibility is **not** a proof of current supported capacity: they require their
own answer contracts and nonambiguous banks. This package makes a conservative,
bounded source-backed capability claim, not a claim that no future question
about this topic can ever be authored.

Excluded source evidence:

- q-141343: dim Col(A^-1) and dim Col(A) both equal n; the blank marker is absent.
- q-141192: TeX grouping makes n and {n} identical, likewise 1 and {1}; no marker.
- q-142302: no visible marker; q-141344 already supplies a complete adjective task.
- q-142357: for invertible A, Col(A), Col(A^-1), and Col(A^n) are all R^n.
- q-141345: for invertible A, Null(A) and Null(A^-1) are both the zero subspace.

Replay fidelity is separate from eligibility: all twelve complete banks replay
exactly, including excluded source evidence. Only seven profiles are graded as
supported. No source correction is silently served or written to the database.
