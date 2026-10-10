# Math database import report

This report records the completed migration through **EDB basis 132**, verified on October 10, 2026 UTC. The new database is named **`math`**, stored at **`/media/jake/SSD/EDB/math`** on the FireCuda SSD. All 61 newer-capture original batches have committed. Assistant corrections remain unapplied.

## 1. What we prioritized

The aim was to build a usable Math Academy content database while preserving attribution and edit history:

- Establish the database, Jake's source entity, and schema before importing content.
- Import the archived curriculum and lessons first, followed by historical questions and newer captures.
- Preserve Math Academy's original content, including its mathematical errors, before introducing our corrections.
- Reuse existing entities when content is updated, so earlier versions remain in the history of the same object.
- Preserve images as separate files on the SSD and give database content stable relative image references.
- For the newer captures, require complete answer fields and confirmed source keys before accepting a practice question.
- Keep generated answer keys, authored distractors, learner state, and engine state out of the original-content import.
- Keep the SSD focused on the database, images, runtime files, schemas, seeds, and transaction EDNs. Supporting reports, mappings, receipts, helpers, and evidence belong in Course_Academy's `reference` directory.

We did not turn every CSV, JSON, HTML file, screenshot, or Markdown export into a database artifact. Those files serve as import inputs and evidence. Their useful content is represented by structured records; the images remain separately stored.

## 2. The order we followed

An EDB **basis** identifies a committed database version. Previewing a transaction does not advance the stored database.

| Stage | What happened | Source | Committed basis |
|---|---|---|---|
| Database initialization and source bootstrap | Created `math`; registered Jake through a self-referencing transaction using a temporary ID | Jake, permanently identified as `:person/jake` | Before schema installation |
| Schema installation | Installed the data, content, learner, and engine schemas; copied their EDNs into `math/schema` | `:person/jake` | Before curriculum import |
| MA source registration | Created the entity identified as `:org/Math-Academy` | `:person/jake` | 23 |
| Curriculum seeds | Created groups, courses, units, modules, topics, then their graph relationships | `:org/Math-Academy` | 24–29 |
| Archived lessons | Imported 41 batches generated from the original MA lesson JSON | `:org/Math-Academy` | 30–70 |
| Historical questions | Imported one authoritative-content batch selected from the earlier history-question import | `:org/Math-Academy` | 71 |
| Newer completed captures | Imported 61 batches, including current placements for six affected lessons | `:org/Math-Academy` | 72–132 |
| Our mathematical corrections | Prepared separately; assistant source still needs to be created | Future assistant source | **Not committed** |

The curriculum seed order was `1-math-academy`, `2-course-groups`, `3-courses`, `4-units`, `5-modules`, `6-topics`, and `7-graph`. Entities were created before graph links that refer to them. Course descriptions, overviews, and outcomes were placed at the bottom of the courses file.

**A provenance exception already exists in the seeds:** the retained course codes were locally assigned with Codex assistance, and suggested course-navigation links were locally selected. They were included in MA-source seed transactions, but they are not confirmed MA-authored metadata. The newer original-content import did not add generated mathematical content; that does not make every earlier seed value MA-authored.

OSU seeds and local engine defaults have not been transacted. Installing learner/engine schema did not migrate old learner/engine state.

## 3. Archived lessons and historical questions

### Archived lesson baseline

The lesson generator read **`/home/jake/Developer/MA/DATA/Lessons/*/Source/*.json`** directly, using the existing MA Markdown renderer. It did not use the repaired study-vault Markdown, CSV exports, or generated answer-key campaign as content inputs.

The baseline contained:

| Content | Count |
|---|---:|
| Lessons | 2,964 |
| Tutorials | 6,016 |
| Knowledge points and their canonical worked examples | 9,636 each |
| Practice questions | 19,646 |
| Answer fields | 22,840 |
| Step-specific prerequisite relationships | 9,167 |

Captured answer controls and choices were preserved, but **no correct-answer keys were asserted** in this stage. Blank fields could remain without authored answer values. This established the archived source baseline without filling gaps with generated answers.

### Historical-question import

The old 1,506-question selection was retained, but its content was reconstructed from the original captures rather than replaying the old response-repair transactions. It comprised **1,493 historical questions** and **13 questions from an October 4 automated lesson capture**, attached to 605 existing KPs across 308 topics.

The source evidence came from the historical activity captures under `reference/mathacademy/progress-history-2026-10-04` and the original lesson-capture evidence associated with the earlier import. The old `format-audit/questions.json` helped identify the selected questions; its locally authored alternatives were not accepted as original MA content.

This stage imported captured prompts, solutions, observed difficulty, memberships, **464 answer fields**, and **421 directly displayed correct keys**. Only **360 questions** had saved original controls; **1,146** lacked them. The 69 questions deferred by the earlier import remained excluded.

That is an important distinction from the later rule: **the historical import preserved incomplete records, while the newer-capture import required complete confirmed answer structures**. Completing the newer import does not establish that every question already in the database is ready for grading.

## 4. Where the newer captures came from

All paths in this table are relative to `/home/jake/Developer/Course_Academy/reference/mathacademy`.

| Stream | Capture root |
|---|---|
| Original account, now Mathematical Methods | `question-capture/` |
| Linear Algebra | `question-capture-workers/linear/` |
| Multivariable Calculus | `question-capture-workers/multivariable/` |
| Differential Equations | `question-capture-workers/differential/` |

Each task folder could contain normalized `content.json`, source HTML/JSON, completion/recovery `state.json`, downloaded assets and their manifest, and the old database's import transaction, receipt, and verification.

We reviewed **2,198 verified completed activities** and excluded **12 unfinished activities**. Old import verification helped distinguish imported captures from unfinished work; completion evidence also allowed verified captures that had not written to the old database.

The existing `content.json` records were useful indexes, but were not blindly trusted for answer keys because some had been changed by the automated workflow. Original source evidence included:

- Before-answer question HTML/JSON and `state.json` question snapshots for prompts, controls, and choices.
- After-answer and history HTML/JSON for revealed solutions and feedback.
- Completed activity-page HTML and explicit correct-response controls for source keys.
- Saved `example-<id>.json` and HTML for canonical worked examples.
- Saved `tutorial-<content-id>.html` for explanations, equations, diagrams, tables, and links.
- Assessment and diagnostic instruction HTML.
- Shared contexts and recorded question order for multipart problems.

The review retained **27,324 verified source occurrences**. Repeated practice questions were deduplicated by their MA identity. Where occurrences differed, preparation selected the latest complete source occurrence available using recorded old basis and task order. **We did not replay every captured occurrence as a separate historical transaction.** EDB retains the versions actually imported at each stage; the capture archive preserves the fuller occurrence evidence.

## 5. How content and answers were prepared

Source HTML was converted to Markdown with LaTeX and local image links. Tables and instructional text were retained. Exact saved inline SVG was stored when conversion to text could not preserve a source formula or graphic.

Practice questions retained `q-<id>` identities; canonical worked examples retained `e-<id>` identities. Existing UUIDs were reused. Knowledge points were resolved in the new database using source topic/example identities. Old numeric database IDs and old transaction EDNs were not replayed.

For newer practice questions, preparation required every answer field to have a confirmed correct answer and, where applicable, the original MA choice list. Accepted evidence included directly displayed correct-response controls, a captured MA choice marked Correct, and explicit values or choices stated in MA's authored solution. An entered submission was not treated as authoritative solely because a learner or solver supplied it; accepted submission evidence also had to be confirmed by the source solution.

Some keys were extracted from explicit final expressions, completed templates, labeled cells, or stated truth labels in the source solution. This is **derived extraction**, but it does not introduce a newly solved answer. Questions requiring algebraic solving, interpretation, invented choices, or a mathematical correction were held instead.

UUID creation, HTML conversion, deduplication, schema mapping, key extraction, and multipart assignment wrappers are derived representations. **The original batches contain no LLM-generated answer keys or locally authored distractors.** Observed difficulty was preserved rather than inferred from elapsed time.

## 6. What the newer batches committed

These counts describe the newer import's verified coverage, not net additions or whole-database totals.

| Content | Verified coverage |
|---|---:|
| Practice questions | 19,700 |
| New practice-question identities within that set | 17,445 |
| Canonical worked examples | 2,823 |
| Complete answer fields | 23,108 |
| Answer entities associated with those fields | 86,995 |
| Tutorials | 1,998 |
| Distinct assessment/diagnostic instruction bodies | 28, from 37 captures |
| Multipart problems, including context and order | 28 |
| New knowledge points | 3 |
| New topics | 0 |
| Verified KP/question memberships | 19,700 |

The 2,823 canonical examples reuse 2,820 existing identities and add three new ones. The tutorials reuse 1,987 existing identities, including one replacement that retains the old entity, and add 11 genuine additional tutorial identities.

### Lesson overlaps and ordering

We checked the six affected live topic pages against the archived lessons:

| Topic | Updated lesson | Final steps |
|---|---|---:|
| 1106 | Describing the Position Vector of a Point Using Known Vectors | 7 |
| 2053 | Calculating Volumes of Solids Using Triple Integrals | 9 |
| 2543 | Power Series Solutions of Differential Equations | 6 |
| 3178 | Flux in Three-Dimensional Vector Fields | 9 |
| 6377 | Equilibrium Points and Stability for Systems of ODEs | 4 |
| 6669 | Piecewise Continuity and Piecewise Smoothness | 7 |

The eleven new tutorials were additional sections. Three new example/KP sections were also placed. The final lesson transaction added **14 steps**, reused **28 existing step UUIDs**, updated **19 canonical-example links**, and established complete first-step/next-step routes. It corrected the example order in topic 2543 and the topic/lesson title in 6669.

For topic 6377, tutorial **15932 replaced 14488** and placement **655321 replaced 588705**. We updated the existing tutorial and step by their stable UUIDs. Their current MA IDs and contents changed, while the old IDs and content remain in history on the same database entities. The initially proposed duplicate replacement entity was not imported.

The old/new ID mappings are also recorded in import metadata. That metadata is not an automatic database lookup alias for a retracted MA ID. Ordinary overlaps retained existing identities; Markdown rendering differences alone were not treated as proof of an authored MA revision.

These checks establish current ordering for the six reviewed lessons, not a fresh website audit of the entire MA catalog.

## 7. Image storage

The image library is **`/media/jake/SSD/EDB/math/images`**, inside the database's filesystem folder. Images are stored by SHA-256 of their exact bytes, grouped by the first two hash characters:

```text
/media/jake/SSD/EDB/math/
  postgres/                 database storage and WAL
  images/
    73/
      7325a35720157e2331ade1b9abd042f90030361c1560dd3bf98de08cc495e4c4.png
    ...
  schema/                   installed schema EDNs
  seeds/                    organized seed EDNs
  imports/                  content and correction transaction EDNs
  bin/                      required writer runtime
```

Database content refers to the example above as:

```text
images/73/7325a35720157e2331ade1b9abd042f90030361c1560dd3bf98de08cc495e4c4.png
```

The application resolves that path against the `math` directory. Exported Markdown needs its links resolved for the export destination.

Identical bytes reuse the same hash-named file. Different bytes remain separate even if the pictures look similar. Files are copied without resizing or image conversion, preserving PNG/SVG extensions. Original capture files remain available. Image bytes are **not transacted into EDB**, and this import did not require additional image schema or image entities.

The library currently contains **24,507 files: 23,748 PNGs and 759 SVGs**. This is a library count, not a claim that every file is referenced by currently committed content; preparation also preserved assets for later correction work.

For newer question/example/multipart/correction material, image preparation reviewed 12,640 source paths representing 11,281 unique images, installing 9,603 previously absent images. Tutorial preparation installed another 788 hashed files. All **35 previously missing graphics** were recovered using the correct separately verified account: Methods 22, Linear Algebra 1, Multivariable Calculus 6, and Differential Equations 6. No activities were performed to retrieve them, and no generated diagrams were substituted.

Source-to-library mappings, saved hashes, byte sizes, and verification records live under:

- `reference/edb-math/images/math-academy-map.json` for the archived lessons.
- `reference/edb-math/imports/math-academy/newer-captures/asset-map.json` and `additional-asset-map.json` for newer material.
- `image-verification.json`, `tutorial-image-verification.json`, and `graphic-recovery.json` in that newer-capture folder.

The SSD is not a hash archive of all downloaded files. Hashing here gives images stable storage names; transaction input hashes in the reference manifests separately identify the exact validated EDN bytes submitted.

## 8. How the newer transactions ran

The committed EDNs are under:

**`/media/jake/SSD/EDB/math/imports/math-academy/newer-captures/1-originals`**

| Order | Batch files | Purpose |
|---|---|---|
| 1–51 | `001-questions.edn` through `051-questions.edn` | Practice questions, canonical examples, answer structures, memberships, and associated KP/multipart records |
| 52–59 | `052-tutorials.edn` through `059-tutorials.edn` | Tutorial bodies and the same-entity tutorial/step replacement |
| 60 | `060-instructions.edn` | Assessment/diagnostic instructional text |
| 61 | `061-lesson-activities.edn` | Current ownership, placements, titles, canonical-example links, and ordering for the six reviewed lessons |

Preparation checked EDN parsing, complete answer references, unique identities, component ownership, local image paths, and file sizes. Native EDB **`with` previews** tested the transactions without committing. The final lesson preview included its prerequisite prepared entities.

The actual import then submitted all 61 batches sequentially to the writer at `/tmp/edb-math/writer.sock`. Every request specified **`:org/Math-Academy`**, a saved request key, and the expected database basis. Each batch's exact input bytes were checked against the validated hash before submission. Each commit receipt was saved and checked before the next submission.

The import advanced **71 → 132**, recording **595,839 datoms** across the receipts. Datoms include assertions and retractions; this count is not an entity count. Every receipt's source was confirmed as Math Academy. Exact retries must retain the same request key, bytes, source, and basis intent; a fresh key should not be used to repeat a completed batch.

Post-commit reads at basis 132 verified exact prepared question/tutorial content, all answer structures and keys, all 19,700 memberships, multipart contexts and order, and all 42 steps in the six lesson routes. History reads confirmed the replaced tutorial and step kept their original identities, and the unused duplicate tutorial entity was absent.

Receipts, request keys, input hashes, committed bases, and verification results are stored in `reference/edb-math/imports/math-academy/newer-captures`, chiefly `original-batches.json`, `manifest.json`, and `receipts/`.

## 9. What remains outside the import

| Material | Status and reason |
|---|---|
| 2,103 newer practice questions | Held: controls and solutions exist, but every correct key could not be confirmed without interpretation. No partially keyed newer practice questions entered the ready batches. |
| 12 unfinished activities | Excluded as requested. |
| Earlier 69 deferred historical questions | Remain outside the historical selection. |
| Generated study-vault answer keys and repairs | Not imported in this original-content sequence. |
| Locally authored choices and reconstructed controls | Excluded from MA-original question content. |
| Learner submissions, outcomes, timing, earned XP, mastery, and learner/engine state | Not migrated as reusable content. Source feedback could support a key without importing the attempt itself. |
| Complete assessment/diagnostic definitions and routing | Not inferred from individual attempts. Introductory text was preserved; incomplete definition evidence remains in reference files. |
| OSU seeds and local engine defaults | Prepared separately, not transacted. |
| Our mathematical corrections | 74 drafts covering 88 verified events on 83 question/example entities; not applied. All 83 originals are now present. |

The correction drafts are under **`math/imports/math-academy/newer-captures/2-corrections`**. Their evidence and review are under `reference/edb-math/imports/math-academy/newer-captures/correction-review.md` and the original `reference/mathacademy/mathematical-corrections` archive.

The intended next correction stage is to register the assistant as a source, review the drafts, and transact them after the originals. **Neither Jake nor Math Academy should be attributed as the author of assistant corrections.** The original erroneous values will remain in immutable history. Separately, 198 recorded answer-replacement decisions include restoration and formatting, so they should not all be counted as mathematical corrections.

## 10. Supporting records

All paths below are relative to `/home/jake/Developer/Course_Academy/reference`:

- [Seed organization and provenance](edb-math/seeds/README.md).
- [Archived lesson import](edb-math/imports/math-academy/lessons/README.md), with its manifest, verification, and receipts.
- [Historical-question import](edb-math/imports/math-academy/history-questions/README.md), with its report, evidence, and verification.
- [Newer-capture import](edb-math/imports/math-academy/newer-captures/README.md).
- [Detailed newer-content review](edb-math/imports/math-academy/newer-captures/full-content-review.md).
- [Exact newer-batch order and commit results](edb-math/imports/math-academy/newer-captures/original-batches.json).
- [Newer-import manifest and post-commit verification](edb-math/imports/math-academy/newer-captures/manifest.json).
- [Correction review](edb-math/imports/math-academy/newer-captures/correction-review.md).
- [Image storage convention](edb-math/images/README.md).

The original captures remain under `reference/mathacademy`. Reports and preparation records remain in `reference/edb-math`; this report is not stored on the SSD.
