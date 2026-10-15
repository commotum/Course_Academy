# Capture gap repairs — 2026-10-15

Three accounts showed import omissions across four completed activities. The source packages for three activities have been repaired and requeued. One genuine Math Academy answer conflict remains visible; it has not been suppressed or assigned a fabricated source key.

## Runner defects fixed

- **Foundations, diagnostic 14212321:** history rendered an unsupported `\boldsymbol` command as a red MathJax error. The differing text split live diagnostic question 45 from source q-37456. Comparison now disregards this exact formatting artifact only when its error DOM is present. Original HTML and text remain archived. The repaired package has 59 questions, a verified source identity, its actual live Correct grade, and no capture gaps. Native preparation preserves q-37456's existing separately attributed checkbox correction and all other authored content.
- **Linear, quiz 14220930:** the MathQuill editor returned `\le` for planned `\leq`. Failed readback checks repeatedly retried, consuming the available assessment time. Nine questions remained unanswered. Equivalent relation commands now compare correctly without conflating distinct operators. Local entry failures on timed assessments receive short waits and focused reconsideration after two failures. The completed-history renderer intentionally omits MC choices; the owned task answers endpoint supplies them. Recovery now verifies the task ID, question ID, actual history DOM root, and normalized prompt before restoring choices in canonical source order. Original API bytes and derived rendering are retained separately. Actual unanswered outcomes and timing are preserved. The repaired quiz package has all 17 questions and no capture gaps; its native preparation has no omissions.
- **Linear, review 14214229:** a response-owned answer had an old literal `\u2061` function-application escape and a dropped `ln` operator wrapper. Narrow math-only compatibility now reuses that answer's UUID and updates its spelling. It does not merge unmarked expressions or text answers. Native preview confirms four assertions and four retractions without changes to learner/engine attributes. The complete seven-question source package has no capture gaps. Jake's separately attributed q-304035 correction remains protected.

## Remaining source contradiction

**Multivariable, review 14220846, q-138860:** the problem and differentiation require `g(x)=\sqrt[3]{(3x+6)^4}`. Math Academy's last solution equality and final conclusion instead state `\sqrt[3]{(3x-6)^4}`, which is not one of its five choices. The learner actually submitted the other, intentionally wrong choice and received Incorrect; that outcome is unchanged. Source choice order from task history is not evidence that its first choice is the official key.

All original problem text, choices, explanation, grading, and the final competent source-error judgment are saved. The authored correction remains separate. A bounded ordinary Reference check and one request corrected to include its real Reference task ID both returned `{"error":true}` without grading evidence. No completed review was replayed, no assessment or diagnostic was interrupted, and no unsupported key was asserted. This question remains omitted from the database pending defensible source confirmation or an explicitly designed authored-correction import.

## Publication and verification

- Three complete packages were published under the database lock and entered the normal outbox: 59, 7, and 17 source questions. Actual account checkpoints, XP, completion markers, response timing, and grades were retained.
- All 169 targeted regression tests passed. Native source-aware previews passed. Protected authored corrections were preserved; the quiz preparation had no omissions; q-11735's historical response retains its owning answer identity.
- All four runners were checkpoint-resumed outside timed activities. The last health read found all four running without active capture errors.
- Database imports are pending through the existing 200-question minimum and whole-activity batching policy. No direct small transaction, timer flush, or padding was used. Prior import omissions remain visible until the normal batch verifies the repaired packages.

Evidence: [publication](published-repairs.json), [health read](final-status.json), [reload record](reloaded.json), [regression output](verification/tests.txt), [native previews](native-preview/).
