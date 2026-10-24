# Separate answer-control marker repair

Committed to `math` at **T6109**, source `:agent/codex`.

The generators incorrectly treated radio fields as inline inputs and appended
`{{selection}}` (or inserted it into a vector). The player only embeds blank and
select controls in Markdown; other field markers became generic underlined
“Answer” labels with no associated input. Assignment imports had the same
mismatch for free-response fields, including synthetic “Written response” lines.
The original example, `17592186491432`, came from the trig-chain-rule generator,
not the Math Academy importer. See the [original diagnosis](../../audits/2026-10-23-answer-blank/README.md).

## Database changes

- 31 radio questions: remove 24 redundant widget paragraphs; replace the 7
  embedded vector-component markers with `?`, preserving the unknown position.
- 73 free-response questions: remove redundant response-widget paragraphs.
- Register the corrected Bernoulli package using a new generator entity,
  `17592186676049`, UUID `3820a4ed-df78-58d1-bc72-54c6306f5571`.
- All existing question, field and answer identities, correct-answer links,
  choices, worked solutions, curriculum links and learner state are unchanged.

The exact [transaction](transaction.edn) contains 104 content CAS forms, the new
generator record, and a CAS of the KP's generator reference. The original
Bernoulli generator entity/package remains available as historical evidence.
The complete request and durable receipt are in [commit-intent.json](commit-intent.json)
and [receipt.edn](receipt.edn); retries must use that exact request key/payload.

## Prevention

Seven live legacy generators were corrected directly. Three additional related
legacy/draft entrypoints and the decision-variation fixtures were corrected too.
The live immutable Bernoulli package received a separately hashed successor;
its helper/data/dependency files are byte-identical. Superseded immutable
packages and archived review copies were retained unchanged.

The two assignment importer variants now leave free-response editors outside the
problem text and preserve actual blank/select placements. The shared generator
publication validator and assignment validation reject separately rendered
field markers in problem Markdown. The generator authoring instructions now
state this contract explicitly.

[Source changes](source-changes.json), [package publication](package-publication.json),
and the versioned source folder retain exact old/new evidence. The registered
source audit inspected 891 distinct paths (all present), including 307 with
marker construction sites. Legitimate blank/select markers and mathematical
TeX double-brace groups were preserved.

## Verification

- [Speculative preview](preview-verification.json) verified the exact proposed
  datoms before submitting the original payload.
- [Commit verification](verification.json) checks the exact problem values and
  registration at the receipt's db-after, T6109.
- [Global snapshot verification](global-verification.json) scans every question
  and compares the repaired ownership closures against the original snapshot.
  [Complete owned-content verification](owned-content-verification.json) compares
  the exact T6108 and T6109 question/answer trees. Other writers advanced the
  database between T6099 and T6108; unrelated changes were preserved.
- [Player rendering](render-verification.json) covers all 104 prompts: zero
  remaining bogus labels, no new math errors, and unchanged genuine inline
  input slots. The 7 embedded unknowns now display correctly.
- [Generator comparisons](generator-verification.json) cover 258 deterministic
  samples across all supported difficulty bands of the changed entrypoints,
  including every eligible parameter case of the reported trig generator.
  Answers, canonical mappings and worked solutions are equivalent; only the
  intended prompt presentation changes. Some generators derive future UUIDs
  from prompt content, so their newly generated identities naturally differ;
  existing database identities were preserved.
- Both actual [assignment importers](importer-verification.json) were exercised
  with mixed blank/free prompts and existing response-label markers.
- 110 relevant unit tests passed: question markers, generator publication,
  decision variation, assignment conversion, delivery, pipeline and packages.

The preparation, preview, application, generator comparison, renderer and global
verification scripts are retained beside their results. Full native snapshots
are in `.local/edb/choice-marker-repair-{current,after}.jsonl` (T6099 and T6109).
