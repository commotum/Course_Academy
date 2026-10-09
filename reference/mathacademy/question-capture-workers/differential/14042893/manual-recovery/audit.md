# Laplace proof dropdown recovery

The saved q340719 screenshot/DOM showed its intended wrong integral selected and
rejection feedback. The correct retry timed out because `SelectList` opens its
menu on frame mousedown, but its original window handler closes the menu when
the event targets a nested selected formula. The center click therefore opened
and immediately hid the owned option menu.

The focused repair scrolls the existing frame, reads its visible hit targets,
and performs a native click at observed frame padding. It retains the original
owned option node, native option click, and complete value/image verification.
No source widget, choice, application state, grading, pattern, or pacing changed.

`before-tests.txt` reproduces the hidden-option timeout with the old click.
`focused-tests.txt` passes 23 original-widget/proof/select tests. The unrelated
Partial Credit fixture assertion also fails identically before repair because
its JSON result changes while its retained HTML still says Correct. The new
four tests also passed independently on the installed source in the parent chat.
`source-install.json` records the snapshot-guarded installation under the shared
source lock. The unchanged saved retry and source extraction are retained in
`scripts/question_capture/fixtures/laplace-select`.

Only the owned Differential Equations supervisor was checkpoint-stopped. Its
unrelated lesson 14039310 saved its history checkpoint; the account capture lock
was confirmed released before the bounded recovery started. `normal-command.json`
retains the exact original argv/profile, and `resume-command.json` records the
bounded recovery invocation with the existing master EDB release/socket.

The actual server accepted q340719's correct retry. `first-recovered-stage.json`
records the retained rejected stage and recovered source grade in the original
persistent solver session. The question then completed as source Partial Credit,
with six fields and five proof stages; that distinct source result is preserved.
The same runner continued to the next canonical example.

Recovery finished successfully: lesson passed with 10/12 XP, nine graded practice
questions, three original canonical examples, and complete history. The existing
master EDB release committed content at basis 1596 → 1597. Its focused committed
receipt/readback verification covers twelve records, nine new questions, confirms
learner/engine facts unchanged, and confirms no-op reimport. The original solver
session remains `01a11b0b-4ec0-7450-9181-25f4a64b01e3`. q340719 and q340731 retain
Partial Credit; no result was rewritten to Incorrect.

`recovery.json` and `edb-import/verification.json` record the verified receipt and
content hash. `normal-restart.json` confirms the account's normal worker restarted
with argv exactly equal to `normal-command.json`, the same browser profile, and
no recovery override. Supervisor 3831144 and capture worker 3831148 own the account
lock in normal tmux window ma:3. Other accounts were not stopped.
