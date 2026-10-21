# Identical-equation investigation

Question `17592186529320` displays `2x - y = 4` twice and is classified easy.
Its correct answer, infinitely many solutions, is mathematically valid. It has
no `:question/math-academy-id` and was already present in the source inventory
before the currently registered generator package was published. Consequently,
the current package is not established as the historical creator of this UUID.

The current registered package for KP `17592186073776` is
`generators/0f/0f5fe63cbc717d3eef4e3308e209b21b135420a073e8abe4add32516ab9e6c89/generator.py`,
version `solution-count-package-v3`. Its public API accepts the exact displayed
coefficients, reproducing the prompt. Its easy sampler restricts the row scale
factor to 1 or -1; every infinite-solution easy sample therefore has identical
or negated rows. This is also enforced by the easy validator's unit elimination
multiplier requirement. Simply filtering both forms would remove all easy
infinite-solution cases; changing this requires revising the easy family.

For seeds 0 through 9999, the easy sampler produced 1,603 identical-row and
1,631 negated-row systems: all 3,234 infinite-solution cases. Moderate and hard
produced neither form. Ten public-API generations per level were checked
against the sampler. See `audit.py` and `structural-audit.json`.

## Original Math Academy evidence in EDB

At basis 4990, the lesson's three KPs contain ten questions/canonical examples
with Math Academy source IDs; its activity contains five source tutorials.
All fifteen were read from EDB and reviewed. None presents the same equation
twice, or a pair differing only by multiplication by -1, as the initial system.

Two direct examples of the infinite-solution type:

| Entity | Math Academy ID | Initial system | Relationship |
| --- | --- | --- | --- |
| 17592186075063 | tutorial 9685 | `3x - y = -2`; `6x - 2y = -4` | second equation is twice the first |
| 17592186074086 | q-237043 | `y - 3x - 2 = 0`; `4y - 12x - 8 = 0` | second equation is four times the first |

The tutorial explicitly teaches recognition of proportional equations as an
alternative to elimination. Thus recognizing the same line without fully
solving is source-backed. The special unit-multiple easy family is an authored
generator extension without an observed original example in this lesson.
This limited captured source set cannot establish what Math Academy serves
elsewhere or in uncaptured variants.

`math-academy-sources.json` contains the exact current EDB source records and
identity. `source-evidence/` retains the successful bounded requests/results;
the broad initial requests exceeded an EDB intermediate query size limit.
`read_sources.py` reproduces the successful bounded read. No database records
or registered generator packages were changed during this investigation.
