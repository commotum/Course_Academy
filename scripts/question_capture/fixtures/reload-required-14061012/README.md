# Reload Required submission recovery

`page.html` and `state.json` are exact byte copies of the diagnostic artifacts at
`reference/mathacademy/question-capture-workers/multivariable/14061012/diagnostics/1791491979889079982/`.
`capture.record_failure` saves the activity checkpoint alongside the failing DOM.
This snapshot retains q-318979 as `submitting` and the visible dialog with the
exact title `Reload Required` and message
`Something has changed that requires the page to reload.`

The automatic repair job
`.local/question_capture-workers/multivariable/capture-repair/4e538b8a94-1791493216689359386/`
originally generated a test that read the mutable activity's `state.json`.
Live recovery later graded and completed that activity, invalidating its setup
assertion. The regression now reads only these frozen, repository-local copies.
Embedded historical paths remain original evidence strings; the test does not
follow them or access a live account, browser session, or database.

SHA-256 hashes:

- `page.html`: `add278a893344a275078642ef77b63dd01b28d710b7572c1a7e3d7109939a91a`
- `state.json`: `975d1cefcce0bce1ee7ee3c2811965c9e7437e904a7d1e443a5c67e9b74a10f3`

The tests preserve exact visibility/title/message guards, one paced navigation,
the submitting checkpoint, stop handling, and the absence of interaction clicks.
Mocked navigation tests the dialog handler; existing activity recovery tests
separately verify reconciliation of grades and restored unanswered controls.
