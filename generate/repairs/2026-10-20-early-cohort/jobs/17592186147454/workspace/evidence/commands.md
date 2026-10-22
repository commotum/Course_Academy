Run from the workspace with the job Python executable. All tools below are offline; outputs stay in the workspace. No publication or database transaction was performed.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python repair_check.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python validate_repair.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python inventory_check.py
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence --math-root /media/jake/SSD/EDB/math --limit 7
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python shortcut_check.py
```

repair_check.py implements both retained finding IDs, tests the exact minimal q-109154 call and its twelve shifts, the previously rejected q_scale=2 call, and the exact q-109029 shift=1 call. It independently parses visible ODEs, all five choices, and the worked solution. Ten fixed-bank counterfactual sets make every option correct in turn. A fully specified instance is invariant under seed changes.

validate_repair.py replays all ten complete source banks and fifty choices, checks two coefficient/shift boundaries per family, a small ordinary moderate sample (24), and a five-record CLI batch (seed 98301). It batches native grader responses in grader-input.json; exact native, delivery, and relocation commands/results are recorded in their *-execution.json files. Shared check_delivery.py is used for both difficulty bands and separately for the final batch. Package versions and runtime hashes are saved in packaging-results.json.

inventory_check.py reproduces the one captured generated item with the exact historical generator, not the repaired generator's new identities. All original source questions are excluded from generated-item classification. affected-inventory.json uses a path relative to the job's specified author-1 evidence root pointing to the workspace copy; this respects the workspace-only write constraint.

shortcut_check.py reads visible bank formulas and keys before/after actual delivery filtering. For each profile the same five formulas support five different correct responses. Shortest, longest, and lexicographic formula cues score 1/5 within every controlled bank at both stages. It also checks correct positions, source-bank memory, semantic equation counts, actual UI radio ordering, and read-only modeled learner selection. Actual learner histories, configured weights, and future entity IDs are unavailable; modeled IDs are explicitly synthetic.

Validation-only parsing uses the retained antlr4-python3-runtime 4.11.1 copy in evidence/deps (copied from the previous review). It is not a generator runtime dependency. Runtime uses only Python 3.13.5 and SymPy 1.14.0, pinned in the manifest and requirements.txt.
