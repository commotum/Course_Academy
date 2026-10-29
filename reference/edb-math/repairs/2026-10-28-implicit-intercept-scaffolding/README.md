# Independent-practice scaffolding repair

KP `17592186054847`: determine an axis intercept of a tangent or normal to an implicit curve.

The investigation, author, and reviewer prompts now require the target source questions' independent reasoning and formula recall in every practice band. The contradictory author instruction to distinguish bands through reduced support has been replaced. Shared principles and generator guidance say manageable numerical changes may preserve the same reasoning across bands. Tutorials, worked solutions, and unrelated reference KPs cannot authorize adding hints to an independent-practice prompt.

The runtime repair removes the easy branch's appended point-slope formula and axis-zero reminder. Differentiation, slope evaluation, line construction, and finding the intercept remain the learner's work. The complete explanations remain in the worked solution. Answer banks, sampling guards, and moderate/hard construction are unchanged.

Published package: `generators/db/db14b9d81fe472e20b72cfee2fa00331bd719b102731526a7637a83e2d067dd8/generator.py`.

Five clean easy questions were published. Five demonstrated generated defects were retired from fresh practice: `17592186711063`, `17592186711789`, `17592186711799`, `17592186711810`, and `17592186711812`. Retirement preserves their questions, answers, ownership, and saved learner history. Imported questions remain unchanged. The pending review of the superseded package was reconciled to the actual completed repair, preventing it from reinstalling the old generator.

Verification:

- 51 fresh questions independently checked from displayed equations and given points, through derivatives, line slopes, and axis intersections, against keys and displayed solutions.
- Real native grader: 85 valid responses accepted and 136 wrong responses rejected.
- Ten complete source replays exactly unchanged; moderate/hard final batches unchanged.
- Both axes and equation-rescaling counterfactuals checked. Existing easy-bank regression rerun at five- and twelve-question batch sizes.
- Actual publication filtering accepts all five questions in each final band. All three representative UI renders pass; easy screenshot inspected for absence of hints and completeness of solution.
- Relocated package under `/tmp` reproduces the reviewed easy output twice. Installed runtime smoke test and current all-band approval check are recorded in `live-verification.json`.

`verify_repair.py` reproduces sampling, mathematics, bank regressions, and grader inputs. `review_repair.py` checks relocation and assembles the actual final review from that evidence. The native grading report is `grading.json`; UI evidence is under `render/`. `publish_repair.py` records the guarded publication/retirement procedure. `publication/verification.json` and `retirement/verification.json` are durable transaction readbacks. `final-result.json` is this direct Codex repair review; it reuses the prior review only for unchanged source interpretation and bank design and explicitly corrects its scaffolding judgment.
