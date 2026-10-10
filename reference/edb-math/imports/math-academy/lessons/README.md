# Archived Math Academy lesson import

Supporting documentation is stored under `/home/jake/Developer/Course_Academy/reference/edb-math`. Database files, images, schema, seeds, and prepared transaction EDNs remain under `/media/jake/SSD/EDB/math`; relative data paths below refer to that database folder.

Completed on 2026-10-09: all 41 batches committed at bases 30–70 with `:org/Math-Academy` as source. Database counts match the generated manifest, and no correct-answer keys were asserted. See `verification.json` and `receipts/`.

The EDN batches are generated directly from `/home/jake/Developer/MA/DATA/Lessons/*/Source/*.json`. The generator reuses the existing MA Markdown renderer and the hashed image mapping in `math/images/math-academy-map.json`. It does not read lesson Markdown or CSVs.

Practice identifiers retain `q-<question-id>` and canonical worked examples retain `e-<content-id>`. The few duplicated MA IDs omit the conflicting external identity and use distinct deterministic UUIDs, matching the old importer. Worked examples remain question entities linked from knowledge points. Answer fields and captured choices are included; correct-answer keys are deliberately unset. Blank fields have no authored answer values until an answer source supplies them. Questions, examples, tutorials, knowledge points, steps, and lessons request their installed specifications; incomplete answer fields do not request `answer-field/validate`.

Image references are `images/<first-two-hash-characters>/<sha256>.png`, relative to the math directory. All source images remain intact.

`manifest.json` records counts, batch order, source, request keys, optimistic basis guards, and commit outcomes. `receipts/` contains transaction receipts. All transactions use `:org/Math-Academy`. The first batch contains one complete lesson; subsequent batches contain at most 75 lessons.

The generator is `math/bin/generate-ma-lessons-json.py`; run it with `/home/jake/Developer/MA/.venv/bin/python` and `--output` pointing to a new empty directory. It adapts the existing math-placeholder parser to handle half-open interval notation and uses the existing select-option renderer for inline HTML choices.

The submission script is `math/bin/transact-ma-lessons.py`. After an unknown outcome, retain the same batch bytes, request key, source, and saved basis guard and rerun it; the database provides exact-retry receipts. Completed batches are skipped.
