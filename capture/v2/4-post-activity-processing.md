# 4. Post-Activity Processing

Python runs this stage after Activity Capture has finished its source review.

1. Return to the account dashboard and read the completed-activity list. Record the task ID, outcome, earned XP, and any displayed base XP or penalty.
2. Update the account's daily XP totals, counting each task once, including after a restart.
3. Read the tracked courses' progress pages. Record course completion percentages and displayed topic progress, and compare them with the previous observation.
4. Save the observations and original page HTML with the account, course, task ID, and capture time. Keep previous observations for later analysis, including encompassing relationships.
5. Update retake instructions: a negative-XP lesson or review makes its next retake all-correct. Clear that requirement after a completed all-correct retake of the same activity type and topic.
6. Save this stage's progress and pass the capture to Database Preparation. Retry missing page reads without repeating the completed activity.

Learner results and progress remain saved observations for later import. Source-content issues return to Activity Capture; Database Preparation handles the topic-difficulty calculation.
