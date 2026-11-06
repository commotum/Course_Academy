# Everyday interfaces

## Reuse existing configuration

Rust crate: `edb-core`, import name `edb_core`, executable `edb`. Other languages can invoke the executable and exchange EDN; do not invent a Python/HTTP/JVM client. Use the project's installed executable or matching checkout. Shared `0.1.0` package versions do not establish development-build compatibility; peers and writers should use the same source revision.

Live reads need authorized PostgreSQL access; writes additionally need configured local/remote transaction transport. A remote transaction token does not authorize cold reads. Opening a connection does not provision storage, create a logical database, or start an attached writer. Read tasks do not require a running writer. Use existing configuration and the installed CLI's `--help`; operational setup belongs in the upstream application guide.

## CLI patterns

Assume `EDB_DATABASE` and `EDB_ENDPOINT` already identify the intended database and writer, and `EDB_POSTGRES_URL` configures appropriate access. Choose `EDB_REQUEST_KEY` once for the logical submission and retain it for recovery. Files contain one EDN value. The request source must reflect the application's actual contributor; the command below assumes the contributor was previously bootstrapped.

```sh
edb query --database "$EDB_DATABASE" --file query.edn --inputs inputs.edn
edb pull --database "$EDB_DATABASE" --file pattern.edn --entity '[:person/email "alice@example.com"]'
edb with --database "$EDB_DATABASE" --source ':application.source/contributor' --file tx.edn
edb transact --database "$EDB_DATABASE" --endpoint "$EDB_ENDPOINT" \
  --request-key "$EDB_REQUEST_KEY" --source ':application.source/contributor' --file tx.edn
```

`inputs.edn` is a vector of non-source `:in` arguments, such as `["alice@example.com"]`, in order. `--file -` takes stdin; only one input file may be stdin. For mixed sources, `--sources sources.edn` can describe databases/views/logs and raw relations:

```edn
{$now {:database "people"}
 $history {:database "people" :history true}
 $rows [["alice@example.com" "external-label"]]}
```

Use actual database names in descriptors. Raw relation cells are literal query data, including general maps/sets/nil; no schema or lookup-ref resolution occurs. Data-only queries need neither PostgreSQL nor `--database`. Query/Pull/with can read backups via `--repository PATH`; refer to the backup-read guide when needed.

`query --query-stats` returns `:edb/ret` plus diagnostics; diagnostics are an execution option, not a query section. `with` reports `:edb/committed false`; it does not publish. Durable receipt output may confirm commit while carrying `:edb/report-error`; handle that as confirmed commit.

## Rust reads and previews

This function receives a captured `DatabaseValue` and keeps input data separate from query syntax:

```rust
use edb_core::{DatabaseValue, QueryControl, QuerySourceValue};
use edb_core::edn::{EdnValue, write_edn};
use edb_core::edn_query::{EdnQueryArgument, parse_query_edn};

fn person(db: &DatabaseValue, email: &str) -> Result<String, Box<dyn std::error::Error>> {
    let query = parse_query_edn(
        "[:find (pull ?p [:db/id :person/name :person/age]) :in $ ?email :where [?p :person/email ?email]]",
    )?;
    let bound = query.bind(&[
        EdnQueryArgument::Source(QuerySourceValue::Database(db.clone())),
        EdnQueryArgument::Data(EdnValue::String(email.into())),
    ])?;
    let outcome = bound.execute(&QueryControl::default(), None)?;
    Ok(write_edn(&bound.result_to_edn(&outcome.result)?)?)
}
```

Use `conn.db()` to capture; `db.pull(&parse_pull_edn(pattern)?, identifier)` for direct projection. Native `Query` uses `db.query` or `QueryEngine::execute_sources` for named sources. Library defaults allow broad reads; choose explicit timeout/work/row/allocation controls for application-supplied queries. Controls are cooperative and do not forcibly preempt arbitrary callbacks or in-flight SQL.

For isolated fixtures, start with `Database::bootstrap()?`; apply schema through `with_edn(schema, 0, source.clone())?`, then data on its `db_after` at a nondecreasing instant. Use `EntityRef::Ident(Keyword::new("db.source", "system"))` for the fixture source. Obtain the read value with `report.db_after.database_value()`. All such changes are speculative and require no PostgreSQL/writer.

## Choose the execution boundary

`Connection::transact` applies to an attached writer. A separately running writer uses configured socket or verified remote transport (`transact_socket`, `transact_remote`, or a configured transaction client). Inspect the project's code and upstream transport signatures before choosing one; do not assume opening a read connection attached a writer.

Synchronous APIs can block; use `AsyncClient`/`AsyncExecutor` when integrating with an async application. Check both admission and awaited execution errors. Dropping an admitted transaction future abandons its result, not necessarily its submission. Async chunked query sequences still prepare joins eagerly.

Custom query functions are explicitly registered in that invocation's `QueryExtensions`. Native transaction functions/predicates must be deployed on the writer and relevant preview processes; the stock writer registry is empty. Stored `:db/fn` hashes refer to deployed native program content, not Clojure source or arbitrary closures. Read the upstream computation/program guides only when extending these mechanisms.
