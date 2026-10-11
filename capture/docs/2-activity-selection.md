# 2. Activity Selection

1. Started Assessment
2. Started Diagnostic
3. Started Lesson or Review (highest priority score first)
4. Started Multistep
5. Unstarted Diagnostic
6. Unstarted Lesson or Review (highest priority score first)
7. Unstarted Multistep
8. Unstarted Assessment

Python calculates Lesson and Review priority scores from the downstream targets their topics support through the prerequisite graph. Use the same scoring policy for both types, and record the supporting targets with the selection reason.

Use queue order for equal scores, or when no scores are available. Finish the current activity before selecting another.

Use the latest saved target and graph data if the database is temporarily unavailable. Missing scores use the queue-order fallback. A completed activity whose capture and question judgments are saved does not block selection while its database import retries.

Never defer or abandon an activity for any reason. Recover and continue until it is complete. After an external interruption or manual stop, resume that activity when operation resumes.
