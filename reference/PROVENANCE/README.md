# Authorship and provenance across the Course Academy schema

Date: 2026-10-05  
Status: Schema and import-tooling review; recommendations, not an implemented provenance schema.

## Recommendation

Use one shared provenance mechanism that can apply to every entity. For questions, grading, curriculum relationships, and calculated values, it also needs to identify the provenance of individual facts. Different parts of one entity can come from different sources.

Use a small shared agent schema for the people, organizations, models, and software involved. An author reference provides basic attribution; provenance records reuse those agents to describe how particular facts were obtained and verified. Keep the existing learner model. EDB permits agent attributes on the same learner entity; an optional person reference is needed only if person and learner-profile identities are intentionally separate.

Use EDB's existing transaction entities and retained fact history as the foundation for provenance. Add explicit evidence records where one transaction combines different sources, or later observations corroborate an existing value. A generator can itself be a software agent with generator-specific attributes; it does not require a duplicate agent entity.

Basic attribution is useful throughout the database. Detailed evidence is essential where grading, question generation, difficulty, or learner progress depends on a fact. The scores below describe implementation priority, not confidence in the existing data.

The review found **23 core entity types**, plus the fixed XP-rule records. Question generators are referenced but do not yet have their own defined schema. Enum values, validation specifications, and schema attributes are excluded from the core-entity count. The `diagnostic-probe/*` routing attributes belong to step entities rather than a separate probe entity.

## Authorship does not automatically follow course membership

[`course/school`](../../schema/data/2-1-course.edn) identifies the institution offering a course. It does not establish authorship or identify the source of the course's content.

Units and modules could inherit an explicitly recorded source as a default, provided the source actually covers those records. Their membership links are ordinary references that permit reuse, however, and locally edited material needs its own attribution. A course's institution is insufficient evidence that it authored every linked unit, module, topic, or question.

Shared import evidence can cover many unchanged records without duplicating the same metadata. That inheritance should follow documented source coverage, with explicit overrides for local additions and changes.

## Importance by entity

Scale: **5 = essential; 4 = high; 3 = useful; 2 = basic attribution sufficient; 1 = minimal value.** For learner and calculated state, provenance means the origin and derivation of observations or values rather than authorship of instructional content.

| Core entity | Importance | What its provenance should explain |
|---|---:|---|
| Course group | **2/5** | Who created the grouping and selected its courses. Usually local catalog organization. |
| Course | **4/5** | Source of the description, overview, and curriculum structure; distinguish official material from our adaptations. |
| Course outcome | **4/5** | Whether the outcome is officially published, paraphrased, or authored by us. |
| Unit | **3/5** | Origin of its title, organization, and module membership. Shared import evidence will often suffice. |
| Module | **3/5** | Origin of its title and topic grouping, including subsequent local changes. |
| Topic | **5/5** | Source of prerequisite relationships and KP membership; whether its workload multiplier is a default or calibrated from observed base XP. |
| Encompassing relationship | **5/5** | Who determined the coverage relationship and weight, and what supports them. These influence implicit learning credit. |
| Knowledge point | **5/5** | Origin of the skill definition, canonical-example assignment, question membership, and targeted prerequisites. These relationships determine what a generator should reproduce. |
| Activity | **4/5** | Whether its structure was imported or locally assembled; source of expected duration, time limits, and scope. |
| Step | **3/5** | Who selected and ordered the content. Explicit provenance becomes especially important for authored diagnostic branches and duration estimates. |
| Tutorial | **4/5** | Original instructional source, author, and any rewriting or generated additions. |
| Question, including worked examples | **5/5** | Separate origins of the problem, worked solution, difficulty rating, calculator requirement, and any reconstruction. |
| Answer field | **5/5** | Whether its interaction type and choices were directly captured, inferred from another question in the KP, or authored; evidence supporting its correct-answer reference. |
| Answer | **5/5** | Whether its value and feedback were captured, extracted, generated, or entered by a learner. Authored distractors particularly need attribution. |
| Multistep problem | **4/5** | Source of the shared context and whether the sequence of parts is original or our composition. |
| Assigned problem | **4/5** | Exact assignment/problem source and who mapped it to our topics. The source problem and our topic mapping can have different origins. |
| Learner | **2/5** | Origin of identity and preference changes. Ordinary account/update history is generally sufficient. |
| Learner task | **5/5** | Origin of reported outcomes, time, and XP; distinguish actual learner activity from automated capture activity. |
| Task item | **5/5** | Who supplied the response, where correctness and duration came from, and which content/grader version was used. |
| Learner progress | **5/5** | Which observations, initialization rules, imports, and engine version produced the state. Particularly important for inferred versus observed performance. |
| Overall learner performance | **4/5** | Which attempts and calculation rules produced its accuracy and evidence totals. |
| FIRe policy | **4/5** | Who chose the parameters, their supporting rationale, and which revision was applied. |
| Question-selection weights | **4/5** | Whether the distributions are observed, fitted, or deliberately chosen, and their applicable activity types. |
| Fixed XP-rule records | **4/5** | Formula version, derivation, supporting data, and adoption decision. These currently exist as documented identities rather than adjustable parameter records. |
| Question generator — proposed | **5/5** | Author, code/template version, source examples, parameter constraints, difficulty rules, and validation evidence. Generated questions should reference the exact generator revision and parameters. |

The curriculum entities are defined in [schema/data](../../schema/data/), instructional entities in [schema/content](../../schema/content/), learner records in [schema/learner](../../schema/learner/), and configuration/rule records in [schema/engine](../../schema/engine/).

Worked examples are already question entities: their role comes from [`knowledge-point/canonical-example`](../../schema/data/6-knowledge-point.edn). Difficulty labels and answer types are enum values; the important provenance concerns assigning those values to particular content.

## Individual assertions need their own evidence

An illustrative mixed-source question could legitimately contain all of the following:

| Fact | Provenance |
|---|---|
| Problem statement | Captured from Math Academy's archived lesson HTML. |
| Worked solution | Captured by `question_capture`. |
| Difficulty | Our estimate. |
| Field type | Inferred from other questions in the same KP. |
| Distractor choices | Authored by us. |
| Correct-answer assignment | Extracted from the worked solution, subsequently confirmed by a successful Math Academy submission. |

Calling that entire question “Math Academy authored” would obscure these distinctions. Likewise, identifying `question_capture` as the source does not establish whether a particular value was observed in the page, interpreted by a solver, or confirmed by grading.

### Correct-answer evidence

Correctness is asserted by [`answer-field/correct`](../../schema/content/5-answer-field.edn), which points to an answer entity. Its provenance needs to establish why that answer is correct for that field and question. The answer value's author and the evidence establishing its correctness are separate concerns.

The following are distinct evidence paths:

- An explicit correct answer shown by Math Academy.
- A submitted value confirmed by a successful Math Academy grade.
- Our extraction or interpretation of the terminal answer in a captured worked solution.
- Our independently calculated or generated answer.
- A later independent verification of any of those values.

A failed submission followed by a revealed worked solution does not make our extracted replacement answer grade-confirmed. Successful grading supports the submitted values that match the captured attempt; it does not establish the entire choice set, difficulty rating, or another version of the question.

[`Answer` entities](../../schema/content/6-answer.edn) can serve as authored options and as identical learner-entered values within the same field. Consequently, the actor responsible for an individual submission belongs with its attempt evidence; it cannot be represented reliably by assigning one author to the deduplicated answer value.

### Difficulty and adapted questions

An authentic Math Academy difficulty rating may describe an earlier version of a question. Changing multiple choice to a blank, inventing distractors, or altering scaffolding can change the demand placed on the learner.

The [historical-question preparation code](../../scripts/prepare_historical_questions.py) already records:

> MA rating of the original question, before local response adaptation

Preserve the distinction between the observed rating of the original form and any estimate for our adapted or generated form. Provenance should identify the content version to which a rating applies.

The current [`question/difficulty` documentation](../../schema/content/4-question.edn) describes observed Math Academy E/M/H ratings. Supporting local estimates explicitly would also require aligning that documentation with the intended semantics.

### Relationships and derived values

Prerequisite edges, question-to-KP membership, canonical-example selection, and assignment-to-topic mappings are assertions worth tracing, even though not all have separate relationship entities. For many-valued references, evidence should identify the particular relationship being supported.

Similarly, an observed base-XP value, a locally predicted duration, and a workload multiplier calibrated from that observation have different derivations. A calculation should retain the relevant input versions and formula/policy version.

Automated capture results must remain distinguishable from actual learner evidence. Source attribution alone does not authorize incorporating automated performance into a person's progress.

## Existing provenance support and its limits

[`scripts/question_capture/provenance.py`](../../scripts/question_capture/provenance.py) already reconstructs attribute-level evidence from saved captures and documented authoring records. It does not itself write provenance entities to the database.

| Existing category | What it establishes |
|---|---|
| `ma_capture` | Imported problem/solution text matches saved capture text, or the difficulty matches saved activity metadata. |
| `ma_widget` | The answer-field interaction type matches the captured field. |
| `ma_complete_choices` | Captured choices are complete and match the imported choice collection. |
| `ma_successful_grade` | The actual result was Correct and the submitted value matches the imported correct value. |
| `ma_explicit_answer` | Explicit source evidence identifies the correct answer. A hook exists for live extraction, but the current extractor does not expose `source_correct`; some historical correction records provide explicit evidence. |
| `model_interpretation` | A key was interpreted without the stronger explicit-answer or successful-grade evidence. |
| `local_estimate` | A locally estimated difficulty documented in an authoring batch. |
| `local_authored` | Locally authored content, including worked solutions and distractors. |
| `local_reconstruction` | Locally reconstructed wording or response structure. |
| `local_interpretation` | A locally interpreted correct key in the documented historical preparation/repair records. |

Evidence records already include useful elements such as question and field identity, attribute and value, source path and hash, transaction evidence, and verification database basis. The [database importer](../../scripts/question_capture/database.py) saves reconciliation evidence and replacement decisions in files. **No shared provenance/authorship attributes are currently defined in the schema.** Math Academy IDs identify content; they do not establish the source or verification of every current value.

Coverage is selective. The authoring-record reader handles particular documented batches, and the importer can inspect prior saved captures. This does not establish the author of every older value. Unknown provenance should remain unknown until supported by evidence; age, an external ID, or course membership is insufficient.

Two import paths illustrate why these distinctions matter:

1. The [archived-lesson seed importer](../../scripts/generate_ma_lesson_seed.py) reads `MA/DATA/Lessons` and can recover original fields and choices. It explicitly omits correct-key assertions where the source does not establish the answer.
2. The [historical question-format audit](../../scripts/audit_historical_question_formats.py) can infer a response format from archived examples in the same KP and locally assemble choices. Its records distinguish that reconstruction from recovery of the original question's actual options.

## Minimal agent and authorship schema

The proposed agent entity and author reference are useful foundations. Authorship answers “who created this?”; provenance also answers “where did this value come from, and why do we trust it?”

| Original proposal | Recommendation |
|---|---|
| An `:author` reference | Keep it under a shared namespace such as `:authorship/author`. Use it for entity-wide attribution where appropriate, with finer attribution for individual facts. |
| An agent entity | Keep it. Shared stable identities avoid repeated names and allow the same person or organization to appear in different roles. |
| Organization, person, and model types | Keep all three and add software for deterministic generators and other programs. |
| An agent name | Keep it, alongside a stable ID. Names alone should not establish identity. |
| Refactor learners into agents | Keep learner identity, preferences, progress, and history. EDB allows the same entity to carry person-agent attributes. Use an optional `:learner/agent` reference only if person and learner-profile records are deliberately separate. |

The smallest authorship-only addition would have these attributes:

| Proposed attribute | Type | Cardinality | Purpose |
|---|---|---|---|
| `:agent/id` | UUID, unique identity | One | Stable agent identity. |
| `:agent/name` | String | One | Display name. |
| `:agent/type` | Ref to enum | One | Organization, person, model, or software. |
| `:authorship/author` | Ref to agent | Many | Authors of the entity carrying this attribute. |
| `:learner/agent` | Ref to agent | One, optional | Person associated with a separate learner profile, if that separation is needed. Omit when the learner entity itself carries the agent attributes. |

Suggested enum identities, following the existing schema's naming convention, are `:agent.type/org`, `:agent.type/person`, `:agent.type/model`, and `:agent.type/software`. Author and learner references are ordinary references to shared agents, not component ownership.

Many-valued authorship permits multiple contributors. It still does not explain which parts each supplied: listing Math Academy and a model together as a question's authors would not identify the origin of its difficulty rating or answer key. A capture program should be recorded as the extraction tool without automatically becoming the author of the captured text.

The first four attributes provide authorship and agent identity; the fifth is an optional relationship. Transaction metadata and, where necessary, the evidence records described below cover individual assertions, derivation, and verification. The names and types here are a proposal, not installed schema.

### Learners and school affiliation

A learner record continues to represent a person's learning state. Because EDB entities are open collections of facts, it can also carry the person's agent identity and type without changing its existing learner relationships. If person identity and learner profiles need independent lifecycles, the optional agent reference connects those separate records. Do not introduce that split merely to simulate separate database tables.

Being an agent does not make a model or program a learner. Models and capture scripts can create content or submit automated answers without their actions becoming evidence in the person's learning history.

School affiliation remains a separate relationship from authorship. An organization reference could eventually supplement the `course/school` string, but “offers this course” and “authored this material” remain distinct claims. Install a new ref attribute if needed; do not change the existing string attribute's type in place. That change is not required to introduce authorship.

## Generators and authorship through code

### Discussion and analysis sources

The generator/schema discussion occurred in this conversation. The [saved discussion](/home/jake/.codex/sessions/2026/10/03/rollout-2026-10-03T18-34-37-01a1048c-7835-7d43-9859-4c10ebf97f1f.jsonl) considered a shared difficulty-factor catalog, then revised the recommendation to build a concrete generator first and defer the shared catalog until two or three generators demonstrate which factors recur. It also recommended on-demand generation, template identities and parameters, and selection that avoids excessive structural repetition. That was a design recommendation, not an implemented generator schema.

Thread `01a0fa20-034f-7671-a28b-702142706776` supplies a separate [worked analysis of Computing Higher Order Derivatives](/home/jake/.codex/sessions/2026/10/01/rollout-2026-10-01T17-59-57-01a0fa20-034f-7671-a28b-702142706776.jsonl), in its 2026-10-05 18:54–19:12 UTC messages. Its final comparison found these generation families in the captured sample:

| Band | Structure to preserve |
|---|---|
| Easy | Two terms that survive three differentiation passes. |
| Moderate | Three terms after preparation, including terms that disappear during three differentiation passes. |
| Hard | Two persistent terms, including a trigonometric term, through four differentiation passes. |

These are inferred templates for this KP, not a recovered universal Math Academy rating rule. In particular, rewriting occurs in easy questions too, so rewriting alone is not the observed separator. The [pattern-analysis prompt](../new-skills/patterns.md) supplies the reusable analysis process.

### Minimal generator representation

Keep [`knowledge-point/question-generator`](../../schema/data/6-knowledge-point.edn) as its existing cardinality-one, noncomponent ref. Its target can be a software agent carrying generator-specific facts:

| Fact on the generator entity | Purpose |
|---|---|
| `:agent/id` | Stable identity; no second UUID is needed solely to label the generator role. |
| `:agent/name` and `:agent/type` = `:agent.type/software` | Identify the generating program. |
| `:authorship/author` | Human or model authors of the program. |
| Proposed `:question-generator/script-path`, a string | Repository-relative location of the executable script under a configured repository root. |

The source code remains in the versioned repository. Store generator configuration in the code initially; add narrowly scoped attributes only when the application needs to query or edit particular settings as data. A shared difficulty-factor taxonomy can remain deferred.

The generator's authors, the software that produced a question, and the evidence validating its output are different roles. A question's generation evidence points to the software agent and exact execution inputs; the software's author relationship identifies the people or models who wrote it. Do not automatically label generated questions as Math Academy authored merely because their templates were inferred from Math Academy examples.

The earlier [answer-grading proposal](../answer-grading-proposal.md) recommended putting a script path directly on the KP when the only requirement was locating code. The provenance requirement now gives the generator a separate identity and additional meaningful facts. Preserve the installed ref attribute and put the path on its target, rather than converting that ref to a string.

### What to retain for generated output

For each output, retain the generator identity, exact repository/code revision or content hash, template identity, actual parameters, and seed where randomness is used. Preserve the referenced source and any dependency/runtime versions that affect reproduction; a hash or a mutable path alone cannot reconstruct the code. These details can live in a saved generation artifact linked from the database rather than requiring a separate schema attribute for every parameter.

Use the insertion transaction as the generation event when it accurately represents one coherent generation operation. If generation happened separately or one run spans several imports, reference the separate run evidence and preserve its own time. If a transaction imports multiple questions with different parameters, the evidence must map inputs to each output; one undifferentiated transaction-wide parameter set is insufficient.

Record validation separately from production. A generator computing an answer is not independent verification of that answer. Store accepted questions, fields, choices, and correct keys as ordinary content; grading an existing question must not rerun the latest script to reconstruct its old answer.

Template identity and parameter fingerprints help reject exact repeats. Avoiding near duplicates also requires deliberate structural variation and selection using learner exposure. Neither purpose requires a universal difficulty-factor catalog at the outset.

## Provenance records using shared agents

Keep four concerns distinguishable:

1. **Creator:** A reference to an organization, person, model, or software agent. For observations and verification, identify the relevant actor in that role rather than treating every participant as an author.
2. **Source evidence:** The exact capture, HTML, screenshot, graded attempt, or other artifact, with enough identity and version information to retrieve and verify it.
3. **Derivation:** Directly observed, extracted, inferred, reconstructed, or generated, including the responsible tool or generator version.
4. **Verification:** How the particular assertion was checked, tied to its value and content version.

The same mechanism should support attribution of a whole entity or import batch when appropriate, and finer evidence for individual attribute values and relationships. Multiple sources or verification events may support the same fact; later verification should preserve the original derivation.

### Start with transaction metadata

EDB explicitly recommends recording who, where, and why on transaction entities. A datom already records its assertion transaction, which can refer to the actor, source artifact, generation evidence, and derivation method. This avoids copying the same import metadata onto every entity and rebuilding EDB's transaction history in a parallel log.

Transaction-level facts describe their documented scope. The importer that submitted the transaction is not necessarily the author of its content. One source/method can cover a coherent batch, but a transaction containing an imported prompt, authored choices, and an inferred key needs evidence distinguishing those assertions. Preserve atomic content updates rather than splitting them solely to force a single provenance label per transaction.

A small additional evidence record therefore needs to identify what it applies to, who supplied or checked it, how it was obtained, and its supporting evidence. For an individual assertion, the target must distinguish the database, entity, attribute, particular value or relationship, and applicable assertion transaction/version. Entity, attribute, and transaction alone are insufficient when several values of a cardinality-many attribute were asserted together.

Use refs to existing entity, attribute, and transaction entities where appropriate, together with an unambiguous typed-value selection from retained history or a precisely located evidence artifact. EDB does not provide a universal arbitrary-value schema type, and a datom is not itself an entity that can be targeted with an ordinary ref. Do not force all possible values into a generic tuple or ambiguous text representation.

Add later observations or verification as new evidence even when the content value is unchanged. Reasserting an already present identical fact may be redundant and does not reliably create a new source-bearing assertion. Keep original assertion time, source observation time, and later verification time distinct.

For example, Math Academy can supply a worked solution, a model can extract a correct answer from it, and a later Math Academy graded submission can confirm that answer. These are distinct contributions that reuse the same agent identities. Keep the extraction evidence when adding the later verification.

For generators, retain the exact generator/template revision and parameters for each generated question, together with its source examples and validation evidence. That makes the question reproducible and allows a generator correction to identify affected output.

## EDB design requirements and current-schema review

The review used all four requested local guides:

- [Best practices](../../../EDB/docs/02_core_concepts/05_best_practices.md).
- [Data modeling](../../../EDB/docs/03_schema/04_data_modeling.md).
- [Schema is database data](../../../EDB/docs/03_schema/00_schema.md).
- [Value and identity rules](../../../EDB/docs/03_schema/01_identity_and_values.md).

These requirements apply to the existing schema and to the proposed agent, generator, and provenance additions:

| EDB guidance | Application here |
|---|---|
| Entities are open collections of facts. | Agent, learner, and generator roles can share an entity where they share identity. Avoid a separate entity or duplicate ID just to emulate a table or class. |
| Model each relationship in one direction. | Keep KP → generator, author refs, and evidence → source/generator. Obtain reverse relationships by query; do not maintain duplicate agent → authored-content or generator → generated-questions lists. |
| Use ref-valued idents for shared enums. | Agent type and derivation-method vocabularies use installed ident entities. A ref's namespace does not enforce enum membership; validate the allowed values explicitly. |
| Use domain identities and lookup refs. | Give agents a stable unique identity; names and script paths are not automatically identities. Add uniqueness to an external key only after establishing its scope. |
| Components express ownership. | Keep shared agents, generators, sources, and enum targets noncomponent. Use components only for genuinely owned children; refs and components do not by themselves enforce every ownership invariant. |
| Grow schema without reusing names or changing established meaning. | Add generator attributes to the existing ref target. Add a new school-organization ref if needed. Do not change installed ref/string types in place. Preserve old names and their semantics when migrating. |
| Attribute resolution uses db-before. | Install new attributes and enum idents before application transactions use their names. Wait for dependent installation commits. |
| Cardinality-one means at most one, not required. | Define and invoke required-attribute specs and validation where needed. Check ref targets, enum membership, ranges, and domain invariants explicitly. |
| Retained history supports audit trails. | Keep history for source assertions, answer keys, generation metadata, and evidence. High churn alone is not a reason to use `noHistory` when historical queries are required. |
| Transaction metadata supplies when/who/where/why. | Reuse transaction entities for shared import or generation context; add targeted evidence where source attribution differs or a later observation corroborates a fact. |
| Logical T and transaction entity IDs are distinct. | Use exact database basis/transaction coordinates for historical interpretation. Do not substitute a timestamp, confuse T with a tx ref, or assume coordinates survive a cross-database migration unchanged. |
| Source time and transaction time differ. | Preserve an older source observation time in application evidence if it cannot legally be used as `txInstant`; EDB transaction instants must be nondecreasing and not in the future. |
| Values and unique identities have defined equality rules. | UUIDs are suitable stable agent identities. If a digest becomes an identity, use a supported scalar representation such as a string; bytes cannot be unique keys. Do not put long arbitrary prompts or parameters in tuples, whose slots have tighter limits. |
| Schema intent does not imply index readiness. | Inspect existing data and complete required index work before enabling uniqueness on populated attributes. Do not assume a schema-file edit completes a live migration. |
| Reads and writes must preserve their basis and retry identity. | Read one immutable database value for a generation/import decision, apply appropriate concurrency guards, retain exact requests for unknown-outcome retries, and verify using the transaction's `db-after`. |

### Findings in the current schema

The static inventory contains 35 EDN files, including 23 attribute-declaration files with 162 distinct attributes, plus fixed XP identities and seed data. Every declared attribute has a value type, cardinality, and documentation. The declaration files largely follow these conventions: stable domain identities, ref-valued enums, one-directional relationships, explicit component ownership, retained history, and opt-in entity specifications. A source-file review alone cannot certify the installed database, all write paths, or every past migration.

The review identified these concrete items to resolve:

1. **Generator representation is unfinished.** The existing KP attribute is already a ref; [schema/README.md](../../schema/README.md) and the older grading proposal still discuss a direct-path alternative. The software-agent target proposed here resolves the new authorship requirement without changing that attribute's type.
2. **FIRe policy documentation is stale.** [`policy/initial-accuracy` and `policy/speed-exponent`](../../schema/engine/1-fire-policy.edn) still describe topic difficulty as a normalization or repetition input. [`topic/difficulty`](../../schema/data/5-1-topic.edn) now explicitly describes an XP-only workload multiplier. Reconcile those descriptions with the current implementation; do not treat this contradiction as evidence that the XP multiplier belongs in retention calculations.
3. **Difficulty attribution needs a defined expansion.** The question schema describes an observed MA rating, while some documented imports contain local estimates. Decide and document how estimated and original-versus-adapted ratings are represented, preserving their provenance and historical meanings.
4. **Required and semantic checks are explicit contracts.** Entity specs require invocation; many content schemas document additional writer/application checks. Installing enum refs or validation specs alone does not establish that every import calls the necessary checks.
5. **External IDs need scope before uniqueness.** `learner-task/math-academy-id` deliberately avoids global uniqueness because its cross-learner scope is unestablished. `activity/math-academy-id` also lacks a unique constraint. Establish source-key scope before changing either; the guide's external-key recommendation is not permission to merge distinct records.
6. **Other schema documentation has drifted.** The schema README says there is no `learner/queue`, while the current learner schema defines a self-directed topic queue; it also lists `3-default-fire-policy.edn` instead of the existing `4-default-fire-policy.edn`. Treat `schema/notes.md` as historical scratch analysis. Statements about outstanding runtime migrations need a separate check against current runtime behavior.
7. **Seed installation and replay are different operations.** The [default policy seed](../../schema/engine/4-default-fire-policy.edn) is explicitly install-once and contains anonymous owned question-weight records. Replaying it as a new request can create new child records. Exact retries retain the original request identity; later edits should address the existing children. This is a handling requirement, not a finding of duplicated live data.

### Validation performed

Built the existing project with `cargo build --offline`, compiled the [native schema checker](../../tests/validate_fire_schema.rs) against the cached sibling EDB release, and ran it with `--schema-only` on 2026-10-05. It passed installation of all **25 current schema/configuration files**: the 23 declaration files, fixed XP identities, and default policy seed.

The checker also passed its explicit policy, difficulty, and progress predicate checks, required-field checks, single-owner topic progress checks, identity-preserving updates, component deletion, and history checks. The `--schema-only` mode excludes the retired activity fixture. Validation used an in-memory database and made no durable database writes.

This establishes admission of the current schema files and the checker's specific invariants. It does not validate all live data, every application rule, or the proposed agent/generator/provenance attributes, which are not yet implemented. The documentation inconsistencies above remain findings to resolve.

This review updates the design report. The proposed agent, generator, and provenance attributes have not been installed, and no live database migration is implied by these recommendations.
