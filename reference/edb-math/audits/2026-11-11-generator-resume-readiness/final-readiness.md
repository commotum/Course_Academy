# Generator ready to resume

Cleanup is complete. **Generation is stopped**, and no global restart blocker remains.

- Recovered **2,654 jobs** with saved work and history intact.
- Restored **7,931 quota-rejected launch allowances**, plus **9 schema/capacity allowances** and **35 infrastructure process retries**. Genuine failure limits remain intact.
- Fixed the reviewer schema and fresh-donor UUID serialization failures.
- Restored one interrupted third author attempt that a phase migration had incorrectly marked finished. It remains attempt **3 of 3**; no fourth attempt was granted.
- Preserved **11 intentional content/evidence holds**: seven imported-question issues, three changed-review-evidence cases, and one answer-bank shortcut. They do not prevent the rest of the queue from running.

Independent checks found no active generator process or held worker/runtime lock. The study app is active. No publication or approval was changed by this recovery. Inventory can label resumable saved drafts `running`; that label does not mean a process is currently running.

Resume from the repository root:

```bash
uv run gen -u 25
```

Use `uv run gen -s` for status and `uv run gen -k` to stop after active turns finish.

Evidence: [final check](final-readiness.json), [main recovery verification](independent-main-recovery-check.json), [supplemental verification](independent-supplemental-recovery-check.json), [runtime check](final-runtime-check.json), and [author continuation receipt](author-continuity-repair/receipt.json). The [initial inventory audit](inventory-health.md) records the historical pre-cleanup state.
