# 4. Post-Activity Processing

Python runs this stage after Activity Capture has finished its source review.

1. Return to the account dashboard and read the completed-activity list. Record the task ID, outcome, earned XP, and any displayed base XP or penalty.
2. Update the account's daily XP totals, counting each task once, including after a restart.
3. Record Math Academy's displayed course completion percentage directly from the Learn page HTML. Read the tracked courses' progress pages and compare displayed topic colors and bands with the previous observation. Do not calculate course completion from the topic bands.
4. Save the observations and original page HTML with the account, course, task ID, and capture time. Keep previous observations for later analysis, including encompassing relationships.
5. Save retake instructions before selecting another activity: a negative-XP lesson or review makes its next retake all-correct. Clear that requirement after a completed all-correct retake of the same activity type and topic. Use captured completion evidence if the dashboard is unavailable; when the previous outcome is unknown, default the next retake to all-correct and record why.
6. Save this stage's progress and pass the capture to Database Preparation. Retry missing nonessential observations separately so they cannot block the next activity. Record each read's actual time; a later progress snapshot must not be labeled as the immediate post-activity state. Do not repeat the completed activity or let background reads disrupt the active activity's browser page.

Learner results and progress remain saved observations for later import. Source-content issues return to Activity Capture; Database Preparation handles the topic-difficulty calculation.

Progress-page reads use the shared navigation waits and a 1-second settling interval before capture. Between-activity pacing is saved only after the completed capture and pending import are durable. It must not repeat post-activity accounting or let a missing observation delay an already started activity.

The Learn page's `#coursePercentComplete` text is saved as `dashboard.course_progress.displayed_progress`, qualified by the course link. The dashboard's original HTML and actual capture time accompany that observation. Preserve the displayed value without calculating a replacement percentage or a percentage delta.

[Post-activity processing](../scripts/post_activity.py) saves an immutable `progress-before.json` baseline for each task and compares subsequent reads against it using both course ID and topic ID. `progress-comparison.json` records each changed topic's before/after colors and display bands. The comparison also appears in `post-activity.json`, alongside each read in `observation_history`, so a late retry retains its actual observation time and the original baseline. Replaying the same saved read does not duplicate its history entry or count XP again.

The [display-color mapping](../scripts/progress.py) preserves the original style and color: white is band 0 and the six known blue shades are bands 1–6. Unknown colors retain their raw value and have no inferred band. Missing courses, topics, or colors remain explicit comparison gaps; they never imply lost progress. Without a usable baseline, record that comparison is unavailable. These are observed display changes between reads, not exact FIRe repetitions, memory, intervals, ability, proficiency, or proof that this activity caused every change. Courses are read sequentially, and each course retains its own capture time.
