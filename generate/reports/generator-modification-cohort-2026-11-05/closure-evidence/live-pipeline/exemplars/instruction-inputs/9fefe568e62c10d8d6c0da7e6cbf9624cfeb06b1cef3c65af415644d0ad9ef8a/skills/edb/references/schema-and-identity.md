# Schema and identity

## Inspect before authoring

Attributes themselves are entities. This query inventories installed attributes and resolves their type/cardinality refs to readable names:

```edn
[:find ?name ?type ?cardinality
 :where [?a :db/valueType ?t]
        [?a :db/ident ?name]
        [?t :db/ident ?type]
        [?a :db/cardinality ?c]
        [?c :db/ident ?cardinality]]
```

Pull `[*]` on an attribute ident to inspect documentation, uniqueness, indexing, component, and history properties. In a dynamic attribute query, constrain `?a` with `[?a :db/valueType _]`: `:db/ident` also names entities that are not attributes, which can otherwise cause `query/unknown-attribute`.

## Declare attributes

Submit schema as an ordinary transaction with one source. Commit it before facts using the new attribute names: transaction identifiers and input attributes resolve against db-before. The following schema supports the people examples in this skill:

```edn
[{:db/ident :person/email
  :db/valueType :db.type/string
  :db/cardinality :db.cardinality/one
  :db/unique :db.unique/identity
  :db/doc "Unique contact email"}
 {:db/ident :person/name
  :db/valueType :db.type/string
  :db/cardinality :db.cardinality/one}
 {:db/ident :person/age
  :db/valueType :db.type/long
  :db/cardinality :db.cardinality/one
  :db/index true}
 {:db/ident :person/tags
  :db/valueType :db.type/keyword
  :db/cardinality :db.cardinality/many}
 {:db/ident :person/friends
  :db/valueType :db.type/ref
  :db/cardinality :db.cardinality/many}]
```

| Property | Meaning and choice |
| --- | --- |
| `:db/ident`, `:db/valueType`, `:db/cardinality` | Required attribute name, exact value type, and one/many value shape |
| `:db/unique :db.unique/identity` | Unique domain key with tempid upsert |
| `:db/unique :db.unique/value` | Unique ownership without tempid upsert |
| `:db/index true` | Requests AVET/SAVET value lookup and ranges; check physical readiness |
| `:db/isComponent true` | Ref ownership for anonymous nested children, default Pull expansion, and entity-retraction cascade |
| `:db/fulltext true` | Optional analyzed search on strings; choose at installation |
| `:db/noHistory true` | Allows omission of old indexed facts; useful for high churn when audit history is unnecessary |
| `:db/doc` | Explain the attribute's meaning and conventions |

Model a relationship in one direction; reverse reference navigation is already supported. Use a component only for owned parts, not shared peers such as products or friends. Cardinality-many stores a set; model an explicit position or relationship entity when domain order or edge metadata matters.

## Choose the right identifier

| Identifier | Use |
| --- | --- |
| Numeric ID / `#edb/ref` | Existing issued entity; use report IDs or resolved IDs |
| Ident such as `:status/active` | Programmatic schema/enumeration names; avoid one ident for every domain record |
| Lookup ref `[:person/email "alice@example.com"]` | Existing entity through a unique attribute |
| Tempid `"alice"` | Transaction-local allocation or identity upsert; same string in another transaction is unrelated |

`:db.unique/identity` can resolve a tempid/anonymous map to an existing holder. Identity claims that point to different existing entities fail; this is not arbitrary entity merging. `:db.unique/value` rejects a new tempid claiming another holder's value. Unique attributes must be cardinality-one and cannot be bytes; NaN cannot identify an entity. UUID type alone does not enforce uniqueness.

Lookup refs require a unique attribute and use the supplied read value or transaction db-before. To connect newly created entities in one transaction, use shared tempids. Transactions accept lookup refs in entity, ref-value, and source positions. Query patterns resolve them in entity position; to constrain a reference target, bind its ID through another entity-position clause. Raw tuple sources never resolve schema or lookup refs.

For keyword enumerations, choose either literal keyword values or refs to identified enumeration entities deliberately. Ref enumerations can carry their own documentation and metadata. Pull returns ID maps for noncomponent refs; request nested `[:db/ident]` for their names. Lazy entity navigation instead returns an ident keyword for forward identified refs.

## Value conventions

EDN is data, not executable Clojure. `:person/name` is a keyword, `"name"` a string, and `?name` a query variable. Lists/vectors/maps can be authoring syntax without being stored values. Parsed `EdnValue`, stored `Value`, and general `QueryValue` are separate domains.

Common stored literals: `42` Long, `42N` BigInt, `1.0` Double, `1.0M` BigDec, `#edb/float "1.0"` Float, `#inst "2026-10-11T12:00:00Z"`, `#uuid "f40e770e-9ad5-11e7-abc4-cec278b6b50a"`, `#edb/bytes "010203"`, and `#edb/uri "https://example.com"`. Types are exact admission contracts; cross-numeric query equality does not coerce stored assertions. Scalar nil is not stored; retract to express absence. Instants store milliseconds and reject excess precision.

Logical numeric equality can unify `1.0M` and `1.00M`, but top-level stored decimal facts preserve their different scales; retracting one does not retract the other. URI identity compares components while retaining input spelling. Preserve original representations for exact retries.

## Constraints and evolution

An entity spec names required attributes and optionally predicates. After the people attributes exist, install this spec in its own transaction:

```edn
[{:db/ident :person/required
  :db.entity/attrs [:person/email :person/name]}]
```

Later request it via `:db/ensure :person/required` in an entity map or `[:db/ensure entity :person/required]`. Definitions come from db-before, checks inspect complete proposed db-after, and enforcement is explicitly requested each time. Predicates must return literal true. Attribute predicates validate asserted values, not all old data retroactively. Custom code must be deployed where assessment runs.

Grow schema additively and keep name meanings stable. Renaming an ident preserves its old alias; reusing that name for another entity redirects old clients. Installed attributes cannot be removed. Value type, fulltext flag, and tuple definitions are immutable: introduce a new attribute and migrate when needed. Many-to-one requires at most one resulting value per entity.

For uniqueness on an existing unindexed attribute with history: enable indexing, wait with `sync_schema(schema_tx_t, timeout)`, use the returned value/check `has_avet`, resolve duplicate current values, then add uniqueness in a later transaction. Setting indexing and uniqueness together does not backfill history first.

Stored tuples have 2–8 slots and declared types. Composite tuples derive from cardinality-one constituents; constituent-only assertions on a fresh tempid do not automatically upsert an existing composite identity. Supply an explicit identity hint, lookup ref, or ID. Installation does not populate old entities until constituents are transacted. Read the upstream tuple sections before designing or migrating composite keys.
