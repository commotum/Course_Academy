# Radical chain-rule evidence package

Knowledge point: **Differentiating a Radical Function Using the Chain Rule**

Topic: 1108; KP UUID: `2f0cdac9-57b2-5634-8d98-d6adf8a85204`.

Upload this ZIP to ChatGPT Pro and use PROMPT_FOR_CHATGPT_PRO.md. This has the same evidence-package structure as the earlier image-question ZIPs, with a prompt tailored to question-template and difficulty analysis.

- QUESTIONS.md and database_content.json: canonical example plus 9 database practice questions, exported read-only at basis 495.
- CAPTURED_QUESTIONS.md and automated_captures.json: 8 recently captured practice questions ({'easy': 2, 'moderate': 4, 'hard': 2}), plus the captured canonical example where available. These preserve source worked solutions and difficulty labels.
- BAND_COMPARISON.md: question IDs, observed bands, prompts, and response formats.
- capture_evidence/: relevant before/after snapshots, history explanation snapshots, screenshots, solver records, raw source labels, and import verification from the two automated activities. These are source evidence; wrong learner or automated answers may appear.
- raw_html/: the matching saved history question HTML.
- historical_questions.json, historical_observations.json, historical_raw_questions.json: any additional staged/history records matching this KP; empty arrays mean none were found.
- original_lesson/: the full archived source lesson, including PDF, HTML, JSON, section screenshots, and images. It contains neighboring KPs for context.
- content_schema/: the question, answer-field, answer, and knowledge-point schemas.
- image_assets/ and assets.json: portable copies for normalized image references, with unavailable references explicitly listed.
- manifest.json: file sizes and SHA-256 checksums.

For blank fields, a stored choices array is not a list of displayed answer choices. It can include the correct answer and an incorrect submitted value. Source multiple-choice fields are explicitly marked radio.

Normalized top-level Markdown and JSON use package-relative images. Original archived HTML and raw capture snapshots may retain external scripts or original asset paths; use the accompanying PDF, screenshots, and local original_lesson/Images/ files. No missing asset has been replaced with invented content. No database or learner state was changed.

The canonical example e-182 is stored with difficulty easy in the database at basis 495, but the saved automated canonical-example capture records difficulty null. Its canonical role is established by the KP reference. The easy label is a stored database value, not an observed source difficulty label for this example. This discrepancy is preserved for review; no database change was made.
