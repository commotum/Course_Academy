Use this ZIP to reconstruct missing graph answer-choice groups for the knowledge point "Determining Whether a Function Is Continuous at a Given Point" (topic 462).

Start with MISSING_GRAPHS.md and QUESTIONS.md. Reconstruct these question IDs: q-48086.

Use the saved mathematical problem and worked solution to determine the correct graph. Inspect the canonical example and existing questions, their stored choices, original_lesson/462.pdf, original_lesson/462.json, and image_assets/ for Math Academy's graph conventions. The full lesson is background context; focus on this particular knowledge point. historical_raw_questions.json and raw_html/ contain the original evidence. Ignore studentAnswer and studentAnswerHeader when determining correctness: those contain the learner's submitted answer and can be wrong. A stored database correct answer is explicitly labeled in QUESTIONS.md.

The original choices are missing for the requested IDs. Do not claim to have recovered the exact original distractors. Author a new group of 5 mathematically plausible choices, exactly one correct, matching the response task and the source drawing style. If the evidence cannot determine the original target image, explain the limitation and create an equivalent question with clearly documented prompt changes. In particular, a question asking only for a graph continuous at a given x does not determine a unique original graph; create a valid new choice group satisfying that criterion. Do not invent source facts.

Use Python and Matplotlib to generate the actual diagrams. Preserve equal units where geometrically appropriate, axis arrows/labels, origin, ticks, open/closed endpoints, asymptotes, breaks, periodic boundaries, and transformation coordinates. Keep comparable scales and styling across each group so visual formatting does not reveal the correct choice. Derive distractors from specific likely mathematical mistakes and explain why each is wrong. Verify the equation, domain, roots, vertex, intercepts, orientation, and endpoint inclusion as applicable. For source image coordinates, distinguish observed values from estimates and state uncertainty.

Return a ZIP containing:
- generate_choices.py, with dependencies and a single command that regenerates all output;
- one PNG and one SVG per choice, named <question-id>-choice-1 through -choice-5;
- one labeled choice-group contact sheet per question for review;
- answer_choices.json with records shaped as below;
- reconstruction_notes.md giving derivation, source references, distractor mistakes, and any uncertainty or changed prompt.

JSON contract (paths relative to the returned ZIP):
{"questions":[{"math_academy_id":"q-...","problem":"original or explicitly revised prompt","answer_fields":[{"key":"selection","type":"radio","choices":[{"type":"image","value":"images/q-...-choice-1.png"}],"correct_value":"images/q-...-choice-1.png"}],"reconstructed":true}]}
Include all five choices in each choices array. correct_value must exactly equal one of its choice image paths. Do not transact into any database. Provide the artifacts themselves, not just proposed code.
