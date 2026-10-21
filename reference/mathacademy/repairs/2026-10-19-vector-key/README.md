# q-104098: separately attributed local repair

The last capture omission was caused by a defective original Math Academy question, not a missing screenshot or an extraction failure. All five captured choices are wrong for P=(-3,-1,4) and Q=(1,8,9). The original worked solution also has incorrect signs. Math Academy's original grading key remains unconfirmed.

At the user's request to fix remaining capture gaps, the local catalog question now retains the five original choices and adds a sixth, mathematically correct choice under the existing `:agent/codex` contributor. Its solution explains the correction and includes the original explanation. This is a local content revision, not a recovered Math Academy answer key.

The native commits preserve the original problem, original answer values, and original radio controls with Math Academy attribution. Only Codex contributes the additional answer, correct-answer link, and corrected solution. The original explanation remains in EDB history and in the corrected solution, and all captured source, checkpoint, and completion bytes remain unchanged. The repair makes no changes to learner facts, original outcomes, timing, XP, or Math Academy itself.

The complete equation is r × (4,9,5) = (-41,31,-23). The canonical example e-4922 supplies the method: subtract position vectors to obtain the direction, then compute p × v. Exact arithmetic verifies both given points and rejects every original option.

- [Native commit verification](verification.json): guarded, source-aware commits at bases 4779–4781, with the final layout repair at 4783.
- [Independent mathematical checks](mathematical-verification.json): all five original equations tested against both points.
- [Actual application grading](grading/verification.json): `/api/preview-answer` accepts the local choice and rejects all five originals, without creating attempts.
- [Frozen original question](source-question.json) and [source hashes / scope](evidence.json).

The historical activity verified through normal Database Commit at basis 4782, with zero omissions and a no-op repeat import. All four running accounts report zero capture gaps. No counters or results were manually cleared.
