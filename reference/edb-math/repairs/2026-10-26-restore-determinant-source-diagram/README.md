# Restore the source determinant illustration

Committed **T8114** on 2026-10-26, following the user's decision to replicate the original source faithfully.

Only `:tutorial/content` on **17592186060931** changed: the authored native mnemonic added at T8086 was replaced with the exact original image reference, `images/25/2594f99e0f02241dc6d01f85c82923103df1d6fb4dda5ca03d438637f5178a28.png`. The result exactly matches the content before T8086, including the necessary complete-equation repairs from T8029. No earlier damaged import content was restored.

The preview loaded and decoded the original asset and visually confirmed its blue solid/red dashed diagonals. Actual player rendering verified that every other mathematical expression is unchanged and there are no MathJax errors. The preview fixture sets its image to eager loading for the explicit decode check; production UI code is unchanged.

An exact old-value CAS protected the update. Native speculative validation, receipt datom verification, and readback at T8114 passed. Only the content retraction/assertion and transaction timestamp were recorded. Answer data, entity identity, and learner history are unchanged.

See [transaction](transaction.edn), [verification](verification.json), [render verification](render-verification.json), and [restored diagram](restored-diagram.png).

The other source-image candidates remain unchanged. They are optional redesign possibilities, not import defects; intentional source illustrations should be preserved by default.
