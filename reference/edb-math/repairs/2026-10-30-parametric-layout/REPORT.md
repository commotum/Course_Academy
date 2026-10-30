# Responsive equation groups

Implemented and loaded into the running web service. The shared renderer recognizes unambiguous display lists of two or more distinct scalar assignments, optionally followed by a parameter domain. It renders each complete expression in display style, with a 2em gap and intrinsic CSS wrapping. Available panel width and text size determine the layout automatically; resizing does not rebuild the expressions or answer controls.

The behavior is shared by learning/quiz, topic, course, and activity-history pages. Stored LaTeX does not need device-specific spacing or line breaks. Matrices, explicit aligned/gathered derivations, inline math, coordinates, interval interiors, ambiguous value lists, and answer controls keep their existing handling. An individual expression wider than its panel retains local scrolling rather than being clipped or shrinking its font.

## Verified

- Boundary tests: `node ui/equation-groups.test.mjs`, including all three requested equations, nested TeX groups, function arguments, visible set braces, Unicode domains, and exclusions.
- Actual four-page Markdown renderers: `scripts/check_equation_groups.py` checks all 290 question/tutorial text fields from the topic at six width/font states, including 240px panels and 150% text size.
- All three examples fit on one row at 760px, wrap at 240px, and return to one row when widened; spacing is 34px at a 17px font. The same DOM nodes remain in place.
- The three real MathLive blanks in question 17592186557691 retain their field IDs, entered value, and focus during resizing. No learner submissions are used for testing.
- Live topic page: seven groups and 21 complete items render without MathJax or page errors. The local live-page check blocks all non-GET requests.
- The web service serves the new JS/CSS assets with HTTP 200; the database and writer services were not restarted.

See [responsive verification](responsive-verification.json), [live UI verification](live-ui-verification.json), and [original layout measurements](current-layout-measurements.json). The PNG examples show the equation layout in a static renderer fixture; placeholder text in their tables is not an interactive quiz screenshot.

## Lesson cleanup

At database basis **11728**, a guarded, validated transaction changed 26 text attributes on 25 questions. It removed 41 genuinely empty display blocks and corrected the line `a=3(3)-2=9-2=7` to `c=3(3)-2=9-2=7` in q-6825 / 17592186335959. The table labels x(3) as c, so this is a variable-label correction; the value 7 and final sum −2 are unchanged.

The transaction's exact datoms and readback were verified. No answer values, keys, owned banks, entity identities, links, or learner facts changed. [Commit verification](commit-content/verification.json) and [reviewed changes](content-proposals.json) retain the evidence.

The current registered table generator already removes empty display blocks and explicitly repairs q-6825 in its replay path; its installed replay was checked, so no replacement was needed. The saved worked-solution correction also has immutable-basis provenance and passed the actual importer's protection against restoring the wrong label: [verification](correction-protection-verification.json).
