Run from evidence_root. Python is /home/jake/Developer/Course_Academy/.venv/bin/python; all invocations used -B. No database writes or publishing occurred.

- python -B audit.py
- python -B followup.py
- python -B boundaries.py
- /home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-report.json
- /home/jake/Developer/Course_Academy/generate/runs/current/check-engine shortcut-grader-input.json shortcut-grader-report.json
- /home/jake/Developer/Course_Academy/generate/runs/current/check-engine boundary-grader-input.json boundary-grader-report.json
- python -B relocated/17592186161967.py --count 2 --seed 38191 > relocated-output.json
- python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input fresh-samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-fresh --math-root /media/jake/SSD/EDB/math
- Same delivery command with batch.json / delivery-batch, and source-replays.json / delivery-source.
- python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --math-root /media/jake/SSD/EDB/math
- Same renderer command with target-render-records.json / target-render.
- python -B layout_probe.py (actual renderer with extra read-only browser layout measurements; unmodified UI)
- python -B reproduce_shortcut.py > minimal-reproduction.txt (expected exit 1; demonstrated failure)
- python -B finalize.py

Shared source-reading and UI code references: generate/principles.md; generate/pipeline/validation-tools.md; engine/rust/question_selection.rs:117-209; engine/rust/learning.rs:149-164 and :595-623; ui/learning.js:690-701. Runtime sampler rejects ambiguous columns, duplicate bank choices and absolute target entries over 12, at most 300 attempts. Trace records in resampling.json. Selection excludes previously seen/unusable/retired questions before difficulty-weighted selection; choiceOrder hashes item/field/choice IDs and invalidates the initial authored-position hypothesis.
