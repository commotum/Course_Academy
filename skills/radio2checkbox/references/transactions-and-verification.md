# Transactions and verification

Read [EDB transactions](../../edb/references/transactions.md) and the existing integration before implementing commands. Verify schema and the installed build's signatures rather than assuming Datomic APIs.

## Read scope and replacement shape

Use a fixed basis and recorded lineage. A useful question Pull shape is:

```edn
[*
 {:question/difficulty [:db/id :db/ident]}
 {[:knowledge-point/_questions :limit nil]
  [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:knowledge-point/_canonical-example :limit nil]
  [:db/id :knowledge-point/id]}
 {[:question/answer-fields :limit nil]
  [*
   {:answer-field/type [:db/id :db/ident]}
   {[:answer-field/choices :limit nil]
    [* {:answer/type [:db/id :db/ident]}]}
   {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}]
```

Resolve topic links through `:topic/knowledge-points` (reverse Pull `:topic/_knowledge-points`). Query task items whose content is the question and incoming references to old fields/answers. Pull all task-item responses and state. Keep query EDN and input EDN separate and use bounded entity collections for large reads. Pass this Pull pattern as fixed EDN text: the lightweight Python `edn.loads` cannot decode vector map keys such as `[:question/answer-fields :limit nil]`; the native EDB parser supports them.

For each selectable object create:

- A field with `:answer-field/id` UUID, `:answer-field/key` label, and `:answer-field/type :answer-field.type/checkbox`.
- Exactly two **owned** answers with separate `:answer/id` UUIDs, `:answer/type :answer.type/text`, and `:answer/value` strings `"false"` / `"true"`.
- `:answer-field/choices` referencing those two answers and `:answer-field/correct` referencing the one matching the object's truth value.
- A link from `:question/answer-fields` to that field.

Use the project's `stable_id` convention. Previous identity tokens were `<question/math-academy-id>/authored-checkbox-v1/<label>` with `stable_id('field', token)` and `stable_id('answer', token + '/' + value)`. Verify prospective identities are absent, or reconcile an already authored entity against the intended shape; a blind identity upsert can modify existing content.

Explicitly retract old `:question/answer-fields` links. Retain old fields and answers unchanged; do not retract entities, excise history, or alter a shared old answer. A cardinality-many assertion adds links and does not replace them. Add a prompt CAS if changing `:question/problem`.

Request the application's ensures: `:answer/validate`, `:answer-field/validate`, `:question/validate`, and `:task-item/validate` for affected entities. Preview and writer processes must have matching native callback registries; a stock CLI preview may lack them.

## Saved responses

For each actual old response, use the explicit old-choice-to-subset mapping. Replace the old response reference with one owned Boolean answer **for every** new field, true or false. Do not submit literal strings where native grading expects answer IDs. Preserve all other task-item state. Audit uses outside the scoped questions before detaching or changing relationships.

Keep a manifest with original answer IDs/values, subset, new answer identities, affected task items, and before/after response references. Validate wrong choices as well as the canonical key. A selected wrong option must remain wrong for the same semantic reason. Questions with no saved responses still need a recorded incoming-use check.

## Provenance and exact requests

Resolve the actual agent contributor and use it for both speculative and durable transactions. Do not attribute authored changes to `:org/Math-Academy` or manufacture an ident without checking conventions. Prior migrations used `:agent/gpt-6.1-sol-high`; this is historical evidence, not a hardcoded future identity. Verify the source of **every** explicit/generated datom. Sources contribute to one shared current record; they do not form an override hierarchy.

Use a basis guard when keys, attachments, incoming uses, or learner state depend on the captured reads. Persist the exact EDN bytes and hash, source, UUIDs, basis/options, request key, and intent **before** sending. All logical forms in a transaction describe one proposed information set against the same db-before; they are not ordered imperative updates.

## Batching and concurrent capture

Keep each complete question conversion and its learner-response mappings atomic. A practical starting size is **100–250 questions, often about 200**; scale by actual forms, bytes, incoming uses, and validation cost. This is a project recommendation, not an EDB rule. The last 195-question batches were roughly 650–675 KiB EDN and 8,400 datoms each. Datoms, transaction forms, and admission operations are different counts. Check installed/configured limits; defaults such as 16 MiB CLI input or 100,000 admitted operations are ceilings, not targets.

For submission, the user's preferred workflow is **one batch group at a time**: capture the current database, refresh that group's questions/keys/ownership/incoming uses, prepare and natively preview its exact guarded request, commit it, and retain/validate its receipt before previewing the next group. Each group has its own captured basis; unrelated writes between groups do not require redoing confirmed groups. Preserve concurrent source repairs after reviewing their meaning. Reconcile an uncertain request exactly before any refresh. Preview dependent solution corrections separately after the conversions are confirmed.

For a chain preview, hold one immutable native database value, apply batch one speculatively, and pass each report's `db_after` to the next `with_forms`. Record predicted bases and compare durable receipts. An `as_of` view of a newer value does not recreate an earlier writable basis: speculation assesses its full underlying basis. A held value does not lock the database or guarantee indefinite retention.

If the live writer advances before a guarded batch, expect rejection and reconcile status. Keep confirmed batches; re-read and rebuild only definitively unsubmitted/rejected remaining work. Never recompute a request with an unknown outcome. Slowing capture improves the opportunity to commit a fresh preview but supplies no concurrency guarantee.

## Meaningful verification

Before submitting, inspect the native speculative report's `db_after` and check:

- Exact new identities, field types/keys, owned Boolean banks, correct refs, links, prompts, and response mappings.
- Expected old-link/response/prompt retractions; only allowed entities/attributes are touched. Old field/answer entities and unrelated mathematical content remain unchanged.
- All datom provenance and installed validators; current solution, rating, KP/topic and canonical memberships are preserved unless an explicit separate repair is included.
- Native grading accepts the canonical subset, rejects each single-checkbox flip, handles incomplete responses as required, and preserves the grade of every mapped old option. Distinguish structural/grading checks from independent mathematical verification.

Read speculative entities through the report's native tempid map. Submit the original logical forms, not preview-resolved entity IDs or a projected datom diff. Preview allocates no durable identities and reserves no request outcome.

After an authorized submit, save the receipt immediately, then verify the confirmed report and exact committed basis. Read back all affected questions and response mappings, retained original entities, and the prior historical snapshot. Persist counts, source, basis before/after, request identity, hashes, and verification results. Mark a commit only from confirmed evidence, even if local report formatting fails afterward.

## Outcome recovery

| Outcome | Next action |
| --- | --- |
| Confirmed commit | Save/recover receipt and verify; do not create a new request |
| Confirmed basis/CAS rejection | Archive the rejected preparation, refresh affected remaining work, rebuild and preview a new request |
| Timeout, lost reply, unknown outcome | Reconcile the exact original request under the same key with bounded retry; preserve all files |
| Same key with different intent | Recover the original intent; do not bypass it with another key |
| Commit confirmed, local decoding/report failure | Repair local verification or recover report; do not replay as new intent |

If the exact request cannot be recovered or its outcome stays unknown after bounded reconciliation, stop dependent writes and report the unresolved status. Retained receipts and commit intents take precedence over a stale plan file saying “prepared.”
