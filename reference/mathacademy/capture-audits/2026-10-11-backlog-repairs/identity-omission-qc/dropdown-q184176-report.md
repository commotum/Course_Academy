q184176 dropdown entry now positions and settles its original frame before opening, requires the whole option inside the viewport, and permits one same-node reopen only after the menu is already hidden. The public widget hides its menu on scroll; the earlier entry path scrolled the selected option after opening. Original source choice matching, exact readback, overlay refusal, accepted-field skip, and minimum adapter latency remain enforced.

73 offline browser and timing tests passed in 21.467 seconds, including the own ninth-option fixture and archived public widget handlers. Partial clipping, overlay, replacement-frame, changed-readback, and accepted-field regressions passed. Parent reviewed and approved the diff. No live browser interaction or runner restart occurred; live verification waits for the user to resume.

Exact original source paths and SHA hashes, changed function semantics, test command, and limitations are in `dropdown-q184176-report.json`.

The saved public lesson HTML and public student-lesson.css establish a fixed visible header. Pre-open positioning measures its bottom plus a2px inset, adjusts the nearest scroll container, and uses window scrolling only for an unmet inset. Actual header/window, nested-container, and scroll-limit regressions passed.
