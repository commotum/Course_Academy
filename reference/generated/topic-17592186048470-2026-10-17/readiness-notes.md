# Lesson readiness evidence

At basis 3404, **The Change of Base Formula for Logarithms** has two inventory
blockers. KP 17592186054744 has 2 available usable questions and needs 3 more;
KP 17592186054745 has 3 and needs 2 more. KP 17592186054746 has 7 and already
meets the five-question lesson requirement. None has a registered generator.

`before-readiness.json` records the exact fresh question IDs, invalid bank
members and their native validation reasons. No target-bank question is
excluded as seen or reserved. Missing canonical answer links or missing answer
fields cause the invalid exclusions; this diagnostic does not repair them.

The initial full candidate finder failed on its broad learner-history query.
It was not rerun. `readiness.rs` instead reads only this topic's KP banks and
answer components, exact reverse owners of those questions, and this learner's
own task/item references. The bounded read took under one second: 3 KPs, 143
learner tasks, 425 history items, 1,183 projected entities, and **zero global
attribute scans**. It calls the existing engine predicates
`learning::unavailable_questions`, `inventory::practice_pool`,
`inventory::lesson_shortages`, and `inventory::lesson_ready`.

After publication, verify fresh inventory without creating a learner attempt:

```sh
.venv/bin/python reference/generated/topic-17592186048470-2026-10-17/verify_readiness.py --label after --require-ready
```

This read-only command captures the current basis, verifies the existing
database lineage, and saves basis-named input/result files. It opens no writer,
submits no transaction, starts no jobs, and creates no learner activity. It
checks the inventory admission condition, not a user-facing attempt or any
unrelated scheduling restrictions. The parent agent owns pipeline publication.
