# Core concepts and the SQL/CRUD transition

## The information model

A datom is `[e a v tx source added?]`: entity, attribute, typed value, transaction entity, contributing source entity, and assertion/retraction flag. Datoms are immutable. Ordinary change accumulates assertions and retractions, producing a new database value.

An entity is the collection of facts about one E. There are no application tables or mandatory closed record types. Schema declares attribute properties; any entity can possess any installed attribute. Namespaces organize names, not membership. `:db/id` is entity-map syntax and a read pseudo-key, not a stored attribute.

`DatabaseValue` is an immutable captured read basis. A connection advances by adopting newer values; previously captured values remain unchanged. Reusing one value keeps queries, Pull, and entity navigation consistent. Local evaluation can still load cold immutable objects from storage.

| Familiar application pattern | EDB convention |
| --- | --- |
| Table schema with columns and row membership | Attribute schema with open entities; require domain properties explicitly when needed |
| INSERT a record | Assert facts using a tempid or implicit map ID; unique identity may upsert an existing entity |
| UPDATE a field | Assert a new cardinality-one value; EDB generates the prior value's retraction |
| Replace a whole record/document | Map input asserts only supplied facts; explicitly retract unwanted facts |
| Replace an array | Cardinality-many is a set of values; compute additions and removals explicitly |
| DELETE a row | Retract facts, or retract an entity and its component descendants; history may remain |
| SQL NULL in an optional column | Usually absence of a fact; scalar nil is not stored |
| JOIN ... ON ... | Shared Datalog variables unify bindings |
| LEFT JOIN for optional output | Find entities with Datalog, select optional attributes with Pull; use `get-else` if a value must participate in query logic |
| Ordered statements in a transaction | One declarative information set; expansion reads the same db-before |
| Trigger or stored procedure | Pure transaction function generates forms from db-before; explicitly ensured entity predicates check proposed db-after |
| Separate audit table | Datom Tx/S/Op plus queryable transaction metadata and retained history/log |
| A query sent to a SQL server | Rust peer evaluates against explicit values; PostgreSQL stores opaque immutable objects and guarded references |

These are modeling differences, not claims that SQL cannot provide snapshots, ACID transactions, or audit history. EDB makes immutable values and per-fact time/source coordinates its application model.

## One current record, multiple contributors

Source is an ordinary entity describing a person, institution, importer, or other contributor. The application supplies it once per transaction; EDB does not infer it from credentials. Tx metadata can describe why a change occurred, separately from its contributor.

If sources A and B assert the same E/A/V in separate transactions, both contributions retain attribution, while Pull/entity reads project one distinct value. Cardinality and uniqueness apply across sources. Retracting E/A/V withdraws every current contribution to that fact, recording the retractor as the new datom's source. It does not edit earlier attribution. Filtering current data to source A cannot restore a fact source B withdrew. Query history for past contributions.

Distinguish a named query source such as `$history` (an input value) from the datom source S (an entity ID). They serve different purposes.

## Identity, time, and constraints

- Entity IDs are opaque, database-local issued IDs. Tempids request allocation; constructing an integer does not allocate an entity.
- Logical T orders committed transactions. Tx is an encoded entity ID; use `t_to_tx`/`tx_to_t`. `:db/txInstant` is wall-clock time and may be shared by several transactions.
- Schema and transaction entities are ordinary data. Attribute constraints do not require every entity to have that attribute. An entity spec runs only when explicitly requested with `:db/ensure`.
- Entity `Eq`/`Hash` uses database origin and entity ID, ignoring time and attribute state. Compare selected Pull/query results for state equality; include a snapshot key when caching by time.
- A numeric entity handle or an ID-only Pull map does not prove visible domain facts exist. Test an identifying fact or resolve a unique domain identity.

## Practical limits

One authoritative writer serializes durable transactions per database; adding peers scales reads, not concurrent writers. Retaining history costs storage and maintenance. `:db/noHistory`, excision, authorization, and collection can limit historical reads; captured values do not pin storage forever.

Keep large media/documents in an appropriate object store and store their IDs, URIs, or hashes in EDB. Use actual query/I/O diagnostics for performance claims. Filters are trusted application read views, not tenant authorization or erasure boundaries.
