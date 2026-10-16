# Query and Pull

## Datalog shape

Use `:find` for output, `:in` for ordered inputs, and `:where` for constraints. Omitted `:in` defaults to `$`; an explicit empty `:in` supplies no inputs. A named source selects a captured database, local relation, or log. Shared variables create joins; `_` matches independently without binding.

```edn
[:find (pull ?p [:db/id :person/email :person/name :person/age])
 :in $ ?email
 :where [?p :person/email ?email]]
```

Bind `$` to one `DatabaseValue` and `?email` to a string. A `:where` pattern requires a fact. Pull can select optional age without excluding a person whose age is absent.

Database patterns follow `[source? E A V Tx S Op]`, with trailing slots omitted. For example `[?p :person/name ?name ?tx ?contributor ?added]` exposes attribution and operation. Three-slot patterns elide that detail; include Tx/S in `:find` or `:with` when distinct contributions matter.

| `:find` form | Native result meaning |
| --- | --- |
| `:find ?e ?name` | Relation of tuples |
| `:find [?e ...]` | Collection |
| `:find ?e .` | One value, or nil |
| `:find [?e ?name]` | One tuple, or nil |

Scalar/tuple forms take the first produced row; they are not uniqueness checks or deterministic choices among multiple matches. Relations normally have set semantics and no guaranteed row order; collections also have no presentation-order contract. `:with` preserves distinctions before projection/aggregation, and distinct entities can Pull to equal maps while native results retain both. EDN relation rendering as a set cannot communicate every duplicate projected row. Preserve entity IDs when the caller needs to distinguish them. Sort explicitly for presentation.

`:keys id name` (or `:strs`/`:syms`) maps find columns to named output keys. Key count must match find width; relation/tuple finds only.

## Inputs, joins, and optional values

Input forms: `?x` scalar; `[?x ?y]` tuple; `[?x ...]` collection; `[[?x ?y]]` relation. Collection input means matching any supplied member; relation input preserves paired combinations. Prefer one collection query to a loop of queries.

```edn
[:find ?name ?friend-name
 :in $ [?email ...]
 :where [?p :person/email ?email]
        [?p :person/name ?name]
        [?p :person/friends ?friend]
        [?friend :person/name ?friend-name]]
```

To preserve an optional cardinality-one value inside query logic, use `[(get-else $ ?p :person/age 0) ?age]`; the default cannot be nil. `[(missing? $ ?p :person/age)]` tests absence. `get-some` selects the first present cardinality-one attribute; no match eliminates the row.

Common expressions: comparisons `=`, `!=`/`not=`, `<`, `<=`, `>`, `>=`; arithmetic `+`, `-`, `*`, `/`, `quot`; `count`, `str`, `subs`; `starts-with?`, `ends-with?`, `includes?`; `ground`, `tuple`, `untuple`. Predicates/functions need their arguments bound. Predicate false/nil rejects a row; zero and empty collections are truthy. Arithmetic refs are not numbers for computation. Integral division truncates; exact decimal division must terminate. String count/subs use Unicode scalar positions.

Use `not-join` for an absence test with local variables:

```edn
[:find ?name
 :where [?p :person/name ?name]
        (not-join [?p]
          [?p :person/friends ?friend]
          [?friend :person/tags :blocked])]
```

`not` requires all its variables bound outside; `not-join` requires only listed variables. Ordinary `or` branches must use the same variable set; `or-join` declares shared variables and permits branch-local ones. Negation means absence in the supplied facts, not truth outside the database.

Rules package reusable clauses; supply a rule set through `%` or static `:rules`. Multiple definitions mean OR; recursive rules stabilize their demanded relations. Required bindings must be ready, and recursive negation must be stratified. Nested `q` uses literal query data and explicit arguments. Consult the upstream rule/nested-query sections when those features are needed.

## Aggregation without accidental coalescing

Nonaggregate find variables group results. Use identity in `:with` when equal values from different entities should count separately:

```edn
[:find (count ?name) (count-distinct ?name)
 :with ?p
 :where [?p :person/name ?name]]
```

The basis set includes find and with variables; identical basis rows still coalesce. `sum`, `min`, `max`, `median`, `avg`, `variance`, `stddev`, and `distinct` are supported. `sum` keeps exact integer/decimal arithmetic unless floating inputs select Double; statistics such as avg are approximate Double. `distinct` returns a set; bounded `min n`/`max n` return ordered collections.

## Pull patterns

```edn
[:db/id :person/name
 [:person/age :default 0]
 {[:person/friends :limit 20] [:db/id :person/name]}
 {:person/_friends [:db/id :person/name]}]
```

- Attribute names select values. Missing values are omitted unless a default/transform supplies one.
- Maps specify nested selection. Noncomponent refs otherwise return `{:db/id ...}`; forward component refs default to expanded child maps.
- `:person/_friends` navigates incoming friends, unless that exact underscore-leading attribute is installed. Reverse navigation requires a ref. Typed Forward/Reverse selectors are unambiguous.
- Forward many and reverse noncomponent refs return collections; a reverse component returns one parent ID map unless explicitly nested.
- `[*]` selects available forward attributes and expands components. Use explicit patterns in application contracts so new attributes do not unexpectedly affect behavior.
- Many-valued selectors default to 1,000 visible values. `:limit n` sets a positive limit; `:limit nil` requests all. This selects index traversal order, not a domain sort, and does not bound all I/O.
- `:as` changes the output key; `:xform` names a built-in or registered transform. Limits/nesting precede transformation, defaults follow it, and defaults are never transformed.
- `{:person/friends 3}` repeats the containing pattern to bounded depth; `...` requests recursion without a selector depth cap. Cycles return ID maps; use traversal controls for expansion limits.

`pull_many` preserves input entity order. Pull requires a point-in-time value; history is for datom/query reads. Lazy `Entity` is useful for interactive associative navigation, with selected values cached per handle. It uses the same captured view and can still incur storage I/O.

## Execution and efficiency

EDB chooses ready clauses by a bound-term score, with later clauses winning ties; written order does not force execution. Give it selective inputs and connected patterns. Direct value comparisons can narrow ready AVET/SAVET ranges; `starts-with?` is not itself an index-range constraint. Use query diagnostics to inspect actual scheduling, row expansions, seeks, and scans.

Native `PreparedQuery`/bounded caches reuse validated structure, not sources, input values, results, rule answers, or fixed schedules. Parse a fixed EDN query once; `EdnQuery::bind` creates its own prepared handle and does not automatically use the global native preparation cache.

`sequence` prepares joins and aggregates eagerly and retains their rows; it only defers Pull/transforms. Preparation and consumption share the original deadline/work/allocation budgets. An error ends iteration. Query limits fail rather than silently shortening results; explicit Pull limits and search top-k have different semantics.

For optional analyzed search: install a fulltext string attribute, call `[(fulltext $ :article/text ?search) [[?e ?text ?tx ?score]]]`, and join returned IDs to structured facts. Recent facts remain searchable despite indexing lag. Fulltext has a default hit limit and physical corpus-dependent BM25 scores; relation order is not ranking and search is not an exact business invariant. Read the upstream fulltext guide for search grammar and limits.
