# Seed import plan

Supporting documentation is stored under `/home/jake/Developer/Course_Academy/reference/edb-math`. Database files, images, schema, seeds, and prepared transaction EDNs remain under `/media/jake/SSD/EDB/math`; relative data paths below refer to that database folder.

These files organize the Math Academy curriculum, OSU course-map imports, and local additions as separate transactions.

The seven Math Academy seed files were committed to `math` on 2026-10-09 at bases 23–29. File 1 registered `:org/Math-Academy` with `:person/jake` as source; files 2–7 used `:org/Math-Academy` as source. The OSU seeds and local engine defaults have not been transacted.

## 1. Register the Math Academy source

Transact `math-academy/1-math-academy.edn` with `:person/jake` as source. It creates the ordinary entity identified by `:org/Math-Academy`, using only built-in attributes.

Use `:org/Math-Academy` as source for the MA baseline files below.

## 2. Import the Math Academy curriculum

After registering the source in file 1, transact these files in numeric order:

| Order | File | Contents |
|---|---|---|
| 2 | `2-course-groups.edn` | Nine group UUIDs and titles; no memberships or group validation yet. |
| 3 | `3-courses.edn` | 32 course UUIDs, MA IDs, titles, and existing mnemonic codes; descriptions, overviews, and 1,054 owned learning outcomes follow at the bottom. |
| 4 | `4-units.edn` | 315 unit identities and titles. |
| 5 | `5-modules.edn` | 1,122 module identities and titles. |
| 6 | `6-topics.edn` | 2,971 named topics and four prerequisite-only ID placeholders. |
| 7 | `7-graph.edn` | 32 group memberships; 42 suggested course-navigation links; 315 course/unit memberships and 283 unit-navigation links; 1,122 unit/module memberships and 807 module-navigation links; 7,555 module/topic placements; 6,560 topic prerequisite edges. |

Files 2-6 create the entities. File 7 connects them using existing-entity lookup refs and validates the completed groups, courses, units, and modules. File 3 includes descriptive content in a final section, using the same tempids as its basic course records. Application UUIDs and learning-outcome ordering are preserved.

The course codes and suggested course navigation are retained from the previous Course_Academy catalog. Codes were locally assigned with Codex assistance; the navigation links were locally selected. Their placement here does not mean they were published by Math Academy. Group membership follows captured MA metadata; topic prerequisites come from captured graphs and lesson tables of contents.

The archived MA lesson baseline was imported on 2026-10-09 at bases 30–70, with `:org/Math-Academy` as source for all 41 transactions. It contains 2,964 lessons, 6,016 tutorials, 9,636 knowledge points and canonical worked examples, 19,646 practice questions, 22,840 answer fields, and 9,167 step-specific prerequisite relationships. Correct-answer keys remain unset. Prepared transactions, receipts, and verified database counts are in [the lesson import folder](../imports/math-academy/lessons/).

Study-vault repairs, generated answer keys, and newer automated captures remain later imports.

## 3. Keep OSU imports separate

Transact `oregon-state/1-course-groups.edn` first to create the empty **OSU-MTH** group. Then transact `oregon-state/2-courses.edn` to create the six OSU courses and 62 outcomes, assign all six courses to OSU-MTH, and validate the group. Matching course tempids allow creation and membership in the same transaction. Use `:person/jake` as source for this local seed set.

The course maps are local compilations whose underlying official source URLs have not been recovered. Do not automatically attribute their wording to an official OSU source. OSU-MTH is a local grouping independent of the MA University group.

## 4. Keep local additions separate

| File in `local/` | Contents | Apply after |
|---|---|---|
| `default-fire-policy.edn` | Local engine defaults and lesson/review selection distributions. These are not recovered MA parameters. | Engine schema |

These files are excluded from the MA-source import. Choose the responsible local contributor as source when adopting them; do not invent an unknown historical model identity.

## Course-group differences

The old mixed seed placed Precalculus in High School - Traditional and used Advanced Placement as a group title. The saved MA metadata instead places Precalculus in High School - Integrated Math and uses AP Courses.

The MA baseline follows the captured metadata. The OSU courses belong to their own OSU-MTH group rather than the MA University group. Suggested course-navigation links are retained in `math-academy/7-graph.edn`.

## Original inputs

The original seed files in `/home/jake/Developer/Course_Academy/schema` remain unchanged. The inventory and source descriptions are in `/home/jake/Developer/Course_Academy/schema-v2/seeds.md`.

Captured group metadata comes from `/home/jake/Developer/MA/COURSES/Math-Academy/**/Info-*.json`; the other MA seeds come from the consolidated MA data described in that report. These are selected curriculum files, not an archive of every downloaded artifact.
