# Captured Math Academy historical questions

Supporting documentation is stored under `/home/jake/Developer/Course_Academy/reference/edb-math`. Database files, images, schema, seeds, and prepared transaction EDNs remain under `/media/jake/SSD/EDB/math`; relative data paths below refer to that database folder.

Transacted and verified at basis **70 → 71**, with `:org/Math-Academy` as source. Receipt: `receipt.edn`; verification: `verification.json`.

`questions.edn` retains captured prompts, worked solutions, observed difficulty, original answer controls where saved, and membership in existing knowledge points. Missing controls remain absent. Only keys directly displayed by MA in history response controls are included. Solver-selected keys from the separate automated lesson capture are omitted.

The 1,506-question selection matches `format-audit/questions.json`; content is recovered from the original captures, before response authoring. It includes 1,493 historical questions and 13 questions from the October 4 automated lesson capture. The 69 previously deferred questions remain outside this selection.

Images use `images/<first-two-hash-characters>/<sha256>.png`, relative to the math database folder.

`evidence.json` records the source files and topic/step/example identities used for each question. `report.json` records counts and validation.
