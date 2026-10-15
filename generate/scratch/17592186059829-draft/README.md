# Closed-interval draft ready for independent root QA

The registered numeric script and its entire evidence/cache tree are immutable. The pre-import baseline covers104 files, including the sibling numeric CPython cache. Only the `17592186059829-draft.py` script and its matching draft tree contain proposed work. This draft has not been registered, transacted, replenished or committed. Parent approval is pending.

The frozen2275 wrapper is byte-for-byte `source.json`; `topic.json` and `lessons.json` retain the frozen contextual evidence. `source-cases.json` holds exactly3 original MA practice wrappers. `independent-inventory.json` holds the13 captured nonMA records verbatim with independent-authorship labels. The canonical example is context, not a practice question. Raw q-59295 is ineligible because its rating, key and solution are absent; its separately authored supported repair has a proved key and matching reverse-conversion solution stages. q-154728's question mark moves outside the math delimiter in generated content.

The source's two conversion methods, five-choice radio fields, whole banks, common prose and ordered solution displays are preserved. Both endpoints always define a bounded closed target. Integer, rational and signed-surd endpoint policies are inherited; rational moderate and hard designs are labeled authored extensions. Frozen topic context includes Surds/Compound Inequalities and a sibling canonical y/√2 conversion, supporting endpoint reading without adding solving or a new target branch. Variables x/y/t and ascending/descending full chains vary together across printed prompts, choices and every operative equation. Variable aliases, orientation, bank profiles, seeds and option order do not increase semantic capacity. Capacities are easy600, moderate5880 and hard924, with300 easy/moderate overlap; the union has7104 mathematical tasks.

Run from repository root:

```sh
.venv/bin/python -B generate/scratch/17592186059829-draft.py --difficulty all --count 1 --seed 71 --format json
.venv/bin/python -B generate/scratch/17592186059829-draft/validate.py
.venv/bin/python -B generate/scratch/17592186059829-draft/validate-inventory.py
.venv/bin/python -B generate/scratch/17592186059829-draft/validate-native-radio.py
.venv/bin/python -B generate/scratch/17592186059829-draft/validate-cli.py
```

`--format markdown` is also supported. API seed/count reject booleans, strings and fractional values. CLI all/count1 returns a3-element list. Counts above finite task capacity fail immediately. Batches deduplicate mathematical fingerprints, including across levels; final CLI regression generated300 unique tasks,100 per level, with deterministic replay.

`validation.json` records7954 independent printed-record checks and19652 counted operative-equation checks, including all7704 selected profile/endpoint banks. `source-replay.json` records15/15 original choices,12/12 distractors,3/3 whole banks,2/2 recorded keys and2/2 captured worked solutions. No missing source key is counted as captured. Eight meaningful corrupted-intermediate controls preserve final keys and are rejected. `inventory-preservation.json` verifies all13 prior normal questions retain identical question/field UUIDs, all65 answer UUIDs, full prose, banks and keys.

Native evidence uses the verified current-source engine build copied to `check-engine`. `reused-grader-build.json` retains its build chain; engine-provenance.json verifies28 engine-source hashes,11 dependency hashes, compiled library, helper source and binary hashes. The shared frozen runner is not used as evidence of current-source correspondence. Across160 full-field fixtures, native ID grading accepted160 correct choices and rejected640 wrong choices. Another160 equivalent zero-padded correct entity-ID inputs were accepted and160 equivalent wrong IDs were rejected. The480 expression/foreign-ID probes remain explicitly recorded as unresolved contract errors: radio IDs and expressions are separate submission contracts. There are no blank fields for native mathematical-entry equivalence checks; mathematical set equivalence is independently validated from actual displayed content.

`render-report.json` covers51 actual Markdown/DOMPurify/MathJax records, comprising3 originals and48 variants, with15 screenshots and zero math errors, exposed delimiters or overflow. The harness uses actual app answerValue/Markdown routines, radio-choice wrappers and styling. Manual inspection reads originals and integer/rational/surd variants in both orientations; visual-review.json records observations. All48 rendered variants exactly replay against the final generator.

`freeze-manifest.json` binds the final script and every draft file, excluding only that manifest's own recursive hash. Run root QA with bytecode disabled (`-B` or `sys.dont_write_bytecode=True`) to avoid modifying the frozen evidence tree. Root QA remains separate from this worker's checks.
