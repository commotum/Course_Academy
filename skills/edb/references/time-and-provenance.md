# Time and provenance

## Select the right view

| Question | Use |
| --- | --- |
| What facts hold at the captured basis? | Plain database value |
| What held no later than logical T? | `db.clone().as_of(t)`; inclusive upper boundary |
| Which surviving assertions are newer than T? | `db.clone().since(t)`; exclusive lower boundary |
| What retained assertions and retractions occurred? | `history()`; add as-of/since for a window |
| What happened in a transaction-time range? | Captured log `tx_range(start, end)`; inclusive start, exclusive end |
| Who contributed a fact, and when? | Bind datom S and Tx; join source/transaction entities |

Logical T and encoded Tx IDs differ; use `t_to_tx`/`tx_to_t`. Native `TimePoint` also supports Tx and Instant. Wall-clock instants are not unique; use T/Tx for exact boundaries. CLI `--as-of`/`--since` take logical T, not Tx IDs or dates.

Time filters do not advance an old value or change its working schema/ident dictionary. `basis_t()` is the underlying capture, while `as_of_t()`/`since_t()` are view boundaries. Repeated bounds replace their respective prior bounds. History preserves existing filters and disables assertion/retraction collapse. Pull and Entity reject history with `database/history-not-point-in-time`.

`since` alone is not a changes feed: current visibility still suppresses retracted facts. It may hide the older unique identity needed for lookup. Resolve IDs in a plain value or join named views:

```edn
[:find ?name
 :in $ $recent ?email
 :where [$ ?p :person/email ?email]
        [$recent ?p :person/name ?name]]
```

Bind `$` to the plain value and `$recent` to its since view. Idents are special: they resolve through the underlying captured dictionary, even when datom filters hide the corresponding facts.

## Audit facts and contributors

Bind `$` to the plain value and `$history` to its history view:

```edn
[:find ?name ?tx ?contributor ?instant ?added
 :in $ $history ?email
 :where [$ ?p :person/email ?email]
        [$history ?p :person/name ?name ?tx ?contributor ?added]
        [$history ?tx :db/txInstant ?instant]]
```

Return Tx and contributor to distinguish repeated assertions. Join the contributor ID to source attributes in a deliberately chosen view; using current source descriptions answers a different question from using past descriptions. Sort by logical transaction order when displaying a timeline, since multiple Tx entities can share an instant.

A current/as-of value collapses withdrawals across all sources before applying since/source/custom predicates. Excluding a retracting source or transaction does not restore the prior current assertion. History filters select the retained events directly. Custom `filter` predicates compose by conjunction and should be deterministic; their callback context has custom predicates removed. Filters neither repair history nor enforce an untrusted-code access boundary.

## Logs and causal reads

For exact events, use `db.log_value()?` on a committed live or repository value so fact/log joins share a basis. Eager fixtures, speculative values, and opaque custom filters cannot supply this committed log. `conn.log()` captures its own endpoint; separate captures can differ if the connection advances. Later commits do not extend a captured log cursor.

```edn
[:find ?tx ?e ?a ?v ?source ?added
 :in $log ?start ?end
 :where [(tx-ids $log ?start ?end) [?tx ...]]
        [(tx-data $log ?tx) [[?e ?a ?v ?tx ?source ?added]]]]
```

Bind `$log` to a captured log; bounds are nil, nonnegative T values, Tx refs, or instants. Raw log datoms contain numeric attribute refs; join with a database attribute inventory for names when needed. Log data can retain events omitted by indexed `noHistory`; it remains subject to excision and retention.

`conn.db()` captures the most recently adopted value without I/O; it does not prove latest durable state or unconditional read-after-write observation. Prefer a successful write report's exact `db_after`. Across callers, send its `basis_t` and use `connection.sync_to(t, timeout)?`; the result may include later transactions. Apply `.as_of(t)` if the data upper boundary must be T. `sync()` obtains a fresh durable head. Logical synchronization does not prove physical AVET/index readiness; use the relevant schema/index wait.

For the exact retained value across processes, use snapshot reference/reopen APIs rather than equating an as-of boundary with identical schema/basis. Snapshot references are neither credentials nor retention pins. `noHistory` cannot restore omitted facts, and ordinary retraction is distinct from irreversible excision; use upstream procedures when removal from retained history is the task.
