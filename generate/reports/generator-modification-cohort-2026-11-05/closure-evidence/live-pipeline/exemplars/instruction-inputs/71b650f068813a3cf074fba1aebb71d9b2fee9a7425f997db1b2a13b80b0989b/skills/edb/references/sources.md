# Upstream sources and scope

The condensed references are self-contained for ordinary application work. They summarize the documentation in `/home/jake/Developer/EDB/docs`, reviewed on 2026-10-11 at source revision `f771bb56322f942d2bd292eab1abbc7fdcd65da1` (package `edb-core` 0.1.0). Relocate the checkout root when using another environment. Version-specific source/docs take precedence over this condensation.

The review covered the documentation map, chapter introductions, and feature boundaries throughout the guide, with detailed reading of the core model, schema/identity, transaction semantics, query/Pull, synchronization, error handling, and everyday interfaces. This is a task reference, not a bundled copy of every API or operational manual.

## Main authorities

| Condensed reference | Primary upstream documents, relative to `docs/` |
| --- | --- |
| Core concepts | `00_start_here/00_introduction.md`; `02_core_concepts/00_database_values.md`, `01_data_model.md`, `04_entities.md`, `05_best_practices.md` |
| Schema and identity | `03_schema/00_schema.md`, `01_identity_and_values.md`, `02_schema_reference.md`, `03_changing_schema.md`, `04_data_modeling.md`, `05_identity_and_uniqueness.md`; `02_core_concepts/02_programming_with_data_and_edn.md` |
| Query and Pull | `05_query_and_pull/00_queries.md`, `01_application_data.md`, `02_pull_and_entities.md`, `04_diagnostics.md`, `05_query_reference.md`, `06_pull_reference.md`, `07_executing_queries.md`; `09_optional/technical_notes/04_outer_joins.md` |
| Transactions | `04_transactions/00_transactions.md`, `04_transaction_data.md`, `05_transaction_model.md`, `06_processing_transactions.md`, `07_transaction_functions.md`, `08_acid.md`; `07_peer_api/07_error_handling.md`; `09_optional/technical_notes/00_updating_transactions.md`, `01_composing_transactions.md` |
| Time and provenance | `02_core_concepts/03_database_filters.md`; `04_transactions/09_synchronization.md`; `06_indexes/00_indexes_and_log.md`; `07_peer_api/00_connections.md`, `03_change_consumers.md`, `06_log_api.md` |
| Interfaces | `01_tutorials/00_edn_workflow.md`, `01_application_workflow.md`, `02_in_memory.md`; `07_peer_api/01_async_client.md`, `02_native_computation.md`, `04_native_api_reference.md`; `09_optional/03_database_tools.md`; `00_start_here/06_release_notices.md` |

For exact native fields and signatures, use `07_peer_api/types/`, `09_client_api_sync.md`, and `10_client_api_async.md`, then the matching `src/` implementation if needed. Start at [the documentation index](/home/jake/Developer/EDB/docs/README.md).

## Load only when the task needs it

| Need | Upstream route |
| --- | --- |
| Explicit ordered datom ranges or paginated Pull | `06_indexes/04_index_apis.md`, `03_index_pull.md`, `05_rseek_datoms.md`; six index orders in `00_indexes_and_log.md` |
| Fulltext expression grammar/ranking/limits | `05_query_and_pull/03_fulltext.md` |
| Tuple/composite keys or numeric identity details | Tuple sections of `03_schema/02_schema_reference.md`; `01_identity_and_values.md` |
| Allocation locality, partitions, UUID helpers | `04_transactions/02_partitions.md`; IDs are not creation timestamps; `entid_at` is not a general creation cutoff |
| Custom native functions or persisted programs | `07_peer_api/02_native_computation.md`; `04_transactions/01_persisted_programs.md`, `07_transaction_functions.md` |
| Durable change reactions | `07_peer_api/03_change_consumers.md`; acknowledgments need reference-write access; no exactly-once external effects |
| Actual I/O or transaction cost diagnostics | `07_peer_api/08_io_stats.md`; `04_transactions/03_diagnostics.md`; logical counters are not SQL round trips or RSS |
| Setup, transport, provisioning, administration | `01_tutorials/01_application_workflow.md`; `08_operations/00_deployment.md`, `01_administration.md`, `14_configuration_reference.md`; `09_optional/04_remote_transactions.md` |
| Backup/offline reads, restore, retention, excision | `08_operations/05_backup_reads.md`, `11_backup_and_restore.md`, `00_deployment.md`; `09_optional/08_excision.md` |
| Maintenance, HA, capacity, telemetry, caching, hints | Remaining `08_operations/` guides; `09_optional/00_local_cache.md`, `01_transaction_hints.md`, `02_log_cache.md` |
| Build/format compatibility | `00_start_here/06_release_notices.md`; `releases/0.1.0.md` |

Keep these procedures upstream. When maintaining the skill, add an omitted detail only if a recurring application task or a concrete correctness failure demonstrates its need. Prefer correcting an existing reference to adding another general checklist or copying an entire manual.
