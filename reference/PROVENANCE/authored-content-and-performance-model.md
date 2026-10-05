# Authorship, source materials, content blueprints, and performance

Date: 2026-10-05  
Status: Design review and recommendations. The [three generic schema drafts](../../schema-v2/generics/) have been written; they have not been installed. Native validators, runtime integration, and the other proposed behavioral changes remain unimplemented.

This report records the recent discussion of shared performance records, authored tags, school materials, generated courses, and the proposed **tag → block → hyperdoc** model. It supplements the [earlier provenance audit](README.md). Where their recommendations differ, this report describes the newer, lighter direction; the earlier audit remains useful evidence about existing imports and attribution gaps.

## Recommended direction

Use a small shared agent model and one shared author attribute. Give independently attributable values their own identity when necessary: a difficulty assignment can have a different author from the question's problem statement, answer fields, or worked solution. Do not require a source/method/evidence framework for every authored value.

For authored content, use native EDB attributes as tag-type definitions, tag entities as attributed answers, blocks as collections of tags, and hyperdocs as compositions of blocks. Use EDB entity specs plus shared native predicates to enforce the blueprint rules. Authored metadata describes the rules; the deployed validators enforce them.

Add a small source-item model for lecture notes, worksheets, quizzes, exams, and other supplied materials. Reuse the existing course, assignment, question, multipart-problem, and learner-task models. A source can be recorded before it has been converted into interactive content.

Keep numerical learner state in a shared performance model. Store assessment/practice accuracy and evidence mass; compute expected accuracy from topic evidence and current prerequisite state. Do not store another frozen initial value, and do not convert the whole learning engine into generic tags merely to unify its authoring interface.

## What the current system already represents

| Concern | Current support | Relevant limitation |
|---|---|---|
| Generated and imported courses | Ordinary course, unit, module, topic, and content entities; MA IDs are optional. | Authorship is not established by an external ID or school affiliation. |
| Reusing MA material | Ordinary curriculum membership refs permit shared topics/content. | Shared navigation/prerequisite edges cannot also express independent personal ordering. |
| Self-directed study | Cross-course `learner/targets`, immediate `learner/queue`, and a mode flag. | Queue membership is unordered; current scheduling chooses its order. |
| School assignments | Assignment activity, ordered steps, assigned problems, questions/multisteps, course affiliation, deadlines. | Original source identity and problem labels are not consistently first-class database facts. |
| Personal activity | Learner tasks and task items hold responses, outcomes, time, and XP. | Importing content or running the capture bot must not establish personal performance. |
| Attribution | Source IDs, captured artifacts, and external import audits. | The reviewed repository schema does not define general author/tag/block/hyperdoc attributes. |
| Accuracy | Assessment/practice accuracy and mass at topic and overall scopes. | Repeated schema fields; topic evidence currently includes graph propagation. |
| Expected accuracy | Prerequisite-based values recorded at initialization. | The implementation freezes them; the proposed design makes the prediction current. |

Sources: [course](../../schema/data/2-1-course.edn), [module membership](../../schema/data/4-module.edn), [learner](../../schema/learner/1-1-learner.edn), [activities](../../schema/content/0-activity.edn), [assigned problems](../../schema/content/8-assigned-problem.edn), [learner tasks](../../schema/learner/2-1-learner-task.edn), [accuracy updates](../../engine/rust/calibration.rs), and [engine state and propagation](../../engine/rust/core.rs).

## 1. Authorship belongs to the contribution

Use the same proposed `:who/author` reference on ordinary content, authored tag assignments, software generators, and schema/type definitions. Reference an agent entity representing a person, organization, model, or software. A generator can itself have agent and generator attributes; EDB does not require a second entity merely because it has both roles.

Retain the earlier proposal's UUID `:agent/id`, display name, and ref-valued agent type. Use one shared, cardinality-one `:who/author` attribute: every complete tag, block, hyperdoc, and authored blueprint has exactly one author agent. Native cardinality enforces at most one, and the required-attribute specs enforce presence. Contributions by different agents belong to distinct entities rather than a list of authors on the containing entity. This supersedes the earlier many-valued authorship proposal. The existing learner entity can also carry person-agent attributes; an extra learner-to-agent wrapper is unnecessary unless those identities intentionally have separate lifecycles.

For example, Jake presses the UI button to create an assignment. Jake is the author of that hyperdoc. A Python generator creates some blocks and is the author of those blocks and any tags it authors. A manually written block has Jake as its author; a block written by an agent has that agent as its author. The generator can itself have a single `:who/author` identifying who authored its code. None of these child contributions changes the assignment hyperdoc's author.

```text
Assignment hyperdoc → who/author → Jake
  ├─ Generated block → who/author → Python generator
  │                                  └─ who/author → its code's author
  ├─ Manual block    → who/author → Jake
  └─ Agent block     → who/author → that agent
```

Each tag follows the same rule independently; reusing a tag preserves its author. The creator of a container does not automatically author its descendants. Here authorship identifies the contribution's creator, not an access-control role; adding generated content does not transfer document ownership or permissions.

| Contribution | Meaning of its author |
|---|---|
| Tag-type definition | Who defined the question, accepted answer shape, and meaning. |
| Tag instance | Who supplied this particular answer or classification. |
| Block | Who assembled this collection of authored facts. |
| Hyperdoc | Who selected and arranged its blocks. |
| Source document | Who authored the supplied material, when known. |
| Generator | Who authored its code; generated outputs can separately identify the software that produced them. |

The author of the global vocabulary word `hard` is not the author of every assignment of `hard` to a question. Similarly, the author of a document does not automatically replace the authors of the blocks it includes.

School affiliation is not authorship. Uploading a file does not make the uploader its author. A folder named `SOURCE` does not prove that its prose is an instructor's original rather than a transcription or generated outline. Preserve unknown attribution instead of inferring it from location.

Strict authored-content specs and partial import specs therefore have different requirements. Newly authored tags must have an author. Historical material with unknown authorship may remain in source items, existing records, or explicitly validated partial import records until attribution is established; do not present those records as complete authored tags. Validate any supplied author refs, and never assign the importer as the original author merely to pass the strict spec.

Correct-answer authorship also differs from verification. A model may supply a key that is later confirmed by MA grading. An author reference answers who supplied it; it does not itself prove successful grading. Preserve the existing capture evidence where available without making a new verification ledger a prerequisite for basic authorship. The earlier audit documents the [different evidence paths](README.md#individual-assertions-need-their-own-evidence).

Replace an attributed value and its author together. One question can retain its identity as content changes; retained database history provides its earlier state. This does not require permanent parallel copies of every adapted question.

## 2. Native EDB attributes as tag-type blueprints

EDB already defines value types, cardinality, indexes, documentation, and validation hooks. Its schema entities can also carry application metadata. Use those capabilities instead of constructing an untyped value system inside the database.

A tag type should be the native attribute entity itself, annotated with an author, a question/prompt, and optional supported constraints. For example, the proposed attribute `:tag.value/difficulty` would accept a ref to an allowed E/M/H vocabulary value. A prompt-text tag would use a string attribute; a numerical rating would use a numeric attribute.

The following is an illustrative definition, not an installation transaction. Its metadata attributes, agent identities, and enum entities must be installed first; the existing application does not yet understand these names.

```edn
{:db/ident :tag.value/difficulty
 :db/valueType :db.type/ref
 :db/cardinality :db.cardinality/one
 :db/doc "Authored difficulty classification for the described content."
 :tag-type/question "How difficult is this question?"
 :tag-type/choices [:question.difficulty/easy
                    :question.difficulty/moderate
                    :question.difficulty/hard]
 :who/author
 [:agent/id #uuid "cfa90423-45a9-43e5-8caf-3b5cb3362937"]}
```

An instance answers that question:

```edn
{:tag/id #uuid "203e6549-017c-4c06-a8f8-9b173659bb43"
 :tag/type :tag.value/difficulty
 :tag.value/difficulty :question.difficulty/hard
 :who/author
 [:agent/id #uuid "f8bc5fb2-ddf3-4a84-bd65-64267a742dd9"]
 :db/ensure :tag/validate}
```

The illustrative UUID lookups stand for the agent defining the blueprint and the agent assigning the rating, respectively. Each author value is one lookup ref, without an outer collection. Here `:tag/type` points to the same schema entity whose attribute holds the answer. A generic editor can discover that attribute and expose a uniform **type, value, author** interface.

This deliberately adjusts the earlier generic `tag/value` proposal. A single ref-valued attribute works for categorical tags, but cannot directly hold text, booleans, or numbers. EDB has no arbitrary “any value” attribute type. Native answer attributes preserve useful database typing without stringifying values or wrapping every scalar in another entity.

The strict shared tag validator should require identity, exactly one valid author reference, a registered tag type, and its selected answer attribute. It should check permitted choices or ranges and reject conflicting additional tag-answer attributes. Ordinary extra metadata remains allowed. An enum ref alone does not enforce vocabulary membership.

Native cardinality controls the number of answers **inside one tag**. It does not control how many tags of that type a block contains. Those are separate collection rules.

References: [Annotate Schema](/home/jake/Developer/EDB/docs/02_core_concepts/05_best_practices.md#annotate-schema), [schema metadata and entity specs](/home/jake/Developer/EDB/docs/03_schema/02_schema_reference.md), and [enum references and membership](/home/jake/Developer/EDB/docs/03_schema/04_data_modeling.md).

## 3. Blocks, hyperdocs, and their blueprints

The proposed authoring vocabulary is:

```text
Tag       = an authored answer to a predefined question
Block     = an authored collection of tags
Hyperdoc  = an authored composition of blocks
```

Use stable domain identities for instances and refs to authored type definitions. A block might have `block/id`, `block/type`, `block/tags`, and the common author attribute. A hyperdoc has corresponding identity, type, composition, and author facts. These are proposed names, not currently installed schemas.

A worked-example block blueprint could require exactly one problem-text tag and one worked-solution tag, while allowing an optional difficulty tag. A lesson hyperdoc blueprint could require tutorial and worked-example blocks. Blueprints themselves can be native entity specs with application metadata describing the permitted collection rules.

There are two kinds of validation:

| Rule | Enforcement |
|---|---|
| The block has an identity, author, type, and tags. | Native `:db.entity/attrs` on an explicitly ensured spec. |
| A worked example contains the required problem and solution tag types. | Shared entity predicate following the tag refs. |
| Only one current difficulty assignment exists in this block. | Block-level multiplicity check. |
| A difficulty value belongs to the permitted vocabulary. | Tag predicate examining the type's rules. |
| A document has valid placements, required block types, and valid order. | Hyperdoc predicate examining the proposed composition. |

Requiring `:block/tags` means at least one tag exists. It does not mean that the required *kinds* of tags exist. Native required-attribute specs do not automatically look through arbitrary nested collections.

Start with a small rule vocabulary: required tag/block types, singular tags, and supported value constraints. Allow additional metadata and optional tags rather than making every blueprint a closed class. Add more expressive occurrence or ordering rules when actual documents need them.

### Order and ownership

Cardinality-many refs are sets. For ordered reusable blocks, use owned placements:

```text
Hyperdoc → placements → blocks → tags
               │
             index
```

A placement supplies the block's position in that document. This permits the same block to appear in multiple documents or twice in one document without changing its global order. Existing [activity steps](../../schema/content/1-step.edn) already separate placement/routing from reusable content in this way.

Use ordinary refs for shared agents, tag types, enum values, sources, and reusable blocks/tags. Use components only for exclusively owned parts, such as document placements or a tag assignment deliberately owned by one block. Component declarations do not themselves enforce single ownership or recursively validate every child.

Store each relationship once and query its reverse. Do not add duplicate tag-to-block and block-to-tag membership facts merely to make both navigation directions available.

Editing a reused tag or block changes what all current references resolve to. Reuse should be intentional. An independent adaptation can get a distinct content identity; an edit to the same content can keep its identity and rely on history. Historical attempts must resolve content at the relevant historical database basis when current content has changed.

## 4. Enforcing blueprints at the transaction boundary

EDB automatically enforces native value types and cardinality. Entity-spec enforcement is different: a transaction must explicitly request `:db/ensure`. A `tag/type` or `block/type` ref does not attach an automatic permanent constraint.

The controlled application write path should:

1. Validate new type definitions against the supported blueprint shape.
2. Request the appropriate specs for every affected tag, block, and hyperdoc.
3. Include affected containers when a child or membership changes. Removed links may require finding parents in db-before as well as the proposed state.
4. Apply value, author, and membership changes in one transaction.
5. Let native predicates inspect the complete proposed db-after and reject the entire transaction if any required structure is invalid.

A raw transaction that omits the required ensures can bypass entity-spec checks. Registering predicates alone is not sufficient. All relevant importers, editors, and generation writers must use the enforced path; front-end validation alone does not establish the invariant.

Authorable rules are data interpreted by a small deployed validator. They do not automatically execute arbitrary Python or JavaScript stored in a blueprint. The project already registers native EDB predicates in its [transactor](../../engine/edb/transactor.rs); new validators would extend that mechanism.

Spec definitions resolve from db-before, while entity predicates inspect db-after. Install new attributes/specs before transactions that use them. Changing a blueprint does not automatically validate existing instances. Keep rule changes separate from instance writes; use new definitions for incompatible meanings or value types, and explicitly audit/migrate affected instances when adopting them.

Retain history for authorship, content values, membership, and blueprint definitions. EDB's history does not archive external files, source code, or native binaries; retain those artifacts separately when reproducibility matters. There is no need to add a separate initial-value field merely to preserve the first asserted value.

References: [entity specs and explicit ensures](/home/jake/Developer/EDB/docs/03_schema/02_schema_reference.md#entity-specs), [native deployments](/home/jake/Developer/EDB/docs/07_peer_api/02_native_computation.md), and [additive schema evolution](/home/jake/Developer/EDB/docs/02_core_concepts/05_best_practices.md#grow-schema-and-never-break-it).

## 5. External source items and school records

Add a small source-item schema. Its initial facts should be stable identity, title, kind, archived location, optional associated course/date, and the shared author ref when known. Kinds such as lecture notes, homework, quiz, and exam can be ref-valued enums. A content hash is useful when identifying an exact archived file version; it does not replace preserving the file itself.

Use a shared many-ref such as `content/sources` from derived or extracted content to its sources. Source items may exist without any parsed questions or runnable activity. Keep source-document time separate from import transaction time.

For example, the inspected [Continuous-Time Signal Processing source folder](/home/jake/Developer/MA/COURSES/Electrical-and-Computer-Engineering/Continuous-Time-Signal-Processing/SOURCE-Continuous-Time-Signal-Processing) contains 37 lecture Markdown outlines, four homework Markdown documents, and three PNG diagrams. Its [Assignment 1](</home/jake/Developer/MA/COURSES/Electrical-and-Computer-Engineering/Continuous-Time-Signal-Processing/SOURCE-Continuous-Time-Signal-Processing/Homework/WHW1/ECE 203 - Assignment 1.md>) has numbered problems, lettered subparts, and shared signal diagrams. It already fits:

```text
Assignment activity → source document
                    → course and deadline
                    → ordered steps → assigned problem
                                        → question or multistep
                                        → supporting topics

Learner task → assignment activity
             → actual responses, time, and completion
```

Retain source-local labels such as “Problem 1(a)” or “Exercise 2.1.43.” They are not globally unique question identities. Add a locator or source fragment when more precise attribution is needed; do not require an entity for every paragraph or diagram initially.

The [existing importer](../../scripts/import_school_assignments.py) already separates assignment instructions, questions, shared multipart context, problem coverage, and activity structure. It saves paths, hashes, and source mappings in audit files. The missing improvement is a queryable, durable link to the source item and original problem label.

Three relationships must remain distinct:

- **Source:** where a problem or passage came from.
- **Coverage/preparation:** the topics required to understand it.
- **Authored additions:** generated lessons, explanations, answer fields, distractors, and keys.

A supporting MA lesson is not automatically the source or author of a university exercise. A school worksheet's author does not automatically author our added answer key. Current [MTH 256 homework](</home/jake/Developer/study/vault/F26/256/10-02-26_WHW-1.md>) explicitly distinguishes linked source material from authored study answers, explanations, and graphics.

An archived exam is a source document. A local practice activity assembled from it is an adaptation. A submitted response, marked paper, or instructor feedback can also be a source item linked to the relevant learner task. Official marks should remain distinct from local checker outcomes and XP; exact grade/submission attributes remain to be designed when implementing that workflow.

EDB permits several roles on one entity when they describe the same object. Source metadata can therefore annotate existing content in appropriate cases. An original PDF and a rewritten interactive activity are different objects and should have separate linked identities.

## 6. Generated courses and personal use of MA content

Use one course model for generated, imported, and mixed courses. A generated course has its own identity and organization, with optional reused topics/content. MA identifiers remain absent unless they actually identify the imported entity.

For a local curriculum, author its own grouping entities where grouping differs, and reference shared topics and content. Topic progress remains about the learner and topic rather than being duplicated for every course containing it.

Existing `learner/targets` and `learner/queue` support long-term destinations and immediate cross-course requests. `learner/course` is the UI-selected course, not a complete enrollment record. No new offering/enrollment hierarchy is needed merely to record several school courses and their dated assignments.

There is an ordering limitation: the self-directed queue is an unordered set, currently scheduled by ongoing work, prerequisite layers, and priority. Engine mode also interleaves lessons across modules. If persistent authored sequences are required, add course/plan-owned placements referencing shared topics or activities. Do not repurpose shared `topic/next` prerequisites or shared unit/module navigation as personal order.

A named study plan becomes useful when saving and switching distinct target sets with their own order or deadlines. It is not required for the source-item work. See the current [study and planning implementation](../../engine/rust/learning.rs) and [learner schema](../../schema/learner/1-1-learner.edn).

## 7. Shared performance and derived bands

The strongest numerical abstraction is a shared performance record containing assessment and practice channels. Each channel stores accuracy and evidence mass. Expected accuracy is a current prediction derived from that topic evidence and current direct-prerequisite state.

| Quantity | Meaning and recommendation |
|---|---|
| Assessment/practice accuracy | Running outcome estimates in 0–1; retain separate channels. |
| Assessment/practice mass | Accumulated observation weight, possibly fractional. It is not bounded confidence. |
| Expected accuracy | Compute from topic evidence and a prerequisite-based prediction; do not freeze it at initialization. |
| Repetitions | Nonnegative fractional reinforcement state; derive the display band. |
| Memory | Time-anchored decaying state, potentially above 1; not an accuracy probability. |
| Topic difficulty | Currently a base-XP workload multiplier; a clearer name would say that. |
| Question difficulty | Currently authored/imported E/M/H categories, with no adaptive scalar underneath. |
| Task-item performance | A positive contribution multiplier, potentially above 1; distinct from accuracy. |

Current accuracy uses an exponentially weighted update, while mass accumulates evidence weights. Accuracy is not simply lifetime successes divided by mass. The engine currently combines assessment/practice accuracy by their equal mean. Extracting a common entity should not silently change those mathematics. See [calibration.rs](../../engine/rust/calibration.rs).

The agreed direction is to make “performance so far” summarize direct observations on the actual topic, and put prerequisite inference into expected performance. The current engine also propagates accuracy evidence through the graph and preserves frozen forecasts, so this is a behavioral change, not just a schema rename. Retention propagation is a separate concern.

One proposed, uncalibrated prediction rule for each channel is:

```text
w = topic_mass / (topic_mass + k)
expected_accuracy = w × topic_accuracy
                  + (1 − w) × prerequisite_prediction
```

Here `k > 0` controls when direct evidence outweighs prerequisite prediction. Neither `k` nor the mapping from prerequisite mastery to expected accuracy has been selected. With no local evidence, use the prerequisite prediction without treating a placeholder accuracy as an observation. A fallback is also needed where prerequisites have no usable evidence. Use underlying numerical prerequisite state rather than rounded display colors.

Do not store a separate frozen initial value. History retains the first assertion of stored values. A derived prediction that was never stored is not itself in history; reproducing it requires the historical inputs and calculation version.

The UI already derives repetition bands as `min(6, floor(repetitions))`: **0, 1, 2, 3, 4, 5, 6+**, plus missing data. This is a useful reusable scalar-to-band pattern, not evidence that repetitions measure current recall probability. See [course.js](../../ui/course.js).

Question difficulty could eventually use a scalar with derived bands, but neither the update rule nor the scalar's meaning is established. Encoding E/M/H as 1/2/3 does not measure equal distances. The XP workload weights 1/2/4 do not establish such a scale either. For one learner, authored structural difficulty and changing personal accuracy are sufficient starting points.

## 8. Recommended implementation scope

1. Add shared agents/authorship and a small source-item model. Preserve unknown authorship and link existing source artifacts rather than requiring complete historical reconstruction first.
2. Implement one authored tag/block/hyperdoc example using native typed attributes, specs, deployed validators, and a controlled writer. Exercise replacement of a value and author, required-tag checks, and reuse through ordered placements before broader content migration.
3. Extend source links and problem labels in school importers. Keep imported content, generated additions, and personal attempts distinct.
4. Refactor shared performance separately: direct observation channels, computed expectations, and explicit handling of the old propagated/frozen fields. Decide the prediction rule before migrating behavior.

Do not require a generic source/method record on every tag, a new class hierarchy for every document kind, a population difficulty model, or a wholesale conversion of engine state into hyperdocs. Keep stable native domain attributes where a separate authored value entity provides no practical benefit.

Before implementing, settle the remaining concrete details: the final agent/type vocabulary, which tag assignments are owned versus reusable, the small first set of blueprint rules, and the expected-accuracy formula. Those are design choices rather than limitations of EDB.

## EDB guidance used

- [Best practices](/home/jake/Developer/EDB/docs/02_core_concepts/05_best_practices.md): accretion, one-directional relationships, enum idents, schema annotations, transaction metadata, and history.
- [Schema basics](/home/jake/Developer/EDB/docs/03_schema/00_schema.md): open entities, native attributes, cardinality, and additive schema.
- [Identity and values](/home/jake/Developer/EDB/docs/03_schema/01_identity_and_values.md): immutable facts and transaction coordinates.
- [Data modeling](/home/jake/Developer/EDB/docs/03_schema/04_data_modeling.md): enum entities, ordinary refs, and explicit membership validation.
- [Schema reference](/home/jake/Developer/EDB/docs/03_schema/02_schema_reference.md): native types, components, predicates, entity specs, and evolution constraints.
- [Native computation](/home/jake/Developer/EDB/docs/07_peer_api/02_native_computation.md): deployment and transaction-time predicate execution.
