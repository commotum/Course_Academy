# Committed assignment import

Originally prepared against math basis **1904**. Revalidated and previewed against
basis **1926**, then committed with user authorization on October 13, 2026. The
three transactions advanced the database through bases **1927–1929**.
See [commit receipts and verification](commit/result.json).

| Assignment | Due, Pacific time | Problems | Questions |
|---|---|---:|---:|
| MTH 255 Recitation Worksheet 3 | October 15, 2026 | 5 | 12 |
| MTH 255 Written Homework 3 | October 15, 2026 | 5 | 9 |
| MTH 256 Recitation Activity 3 | October 14, 2026 | 5 | 5 |
| MTH 256 Written Homework 2 | October 16, 2026 | 4 | 6 |
| MTH 341 Written Homework 2 | October 14, 2026 | 20 | 33 |

All five deadlines are interpreted as 23:59:59 America/Los_Angeles, matching the
existing importer. The source links and textbook page references are retained.
Stable UUIDs derive from course, assignment code, problem, and part; renaming a
dated file does not change its identity.

The three requests must run in order:

1. [Assigned material](1-assigned-material.edn), source `:org/Oregon-State`:
   assignment definitions, course links, deadlines, prompts, source diagrams,
   multipart containment, and step ordering. OSU identifies the assigning
   institution; publisher and textbook attribution remains in the source links.
2. [Authored study content](2-authored-study-content.edn), source
   `:agent/gpt-6.1-sol-high`: reference answers, worked solutions, response fields,
   topic mappings, and condensed local instructions. [Writing-session evidence](author-evidence.json)
   identifies gpt-6.1-sol at high reasoning for these five files. The earlier
   October 10 assignments used gpt-6-astra-high, not this model.
3. [Learner links](3-learner-links.edn), source `:person/jake`: add the five
   assignments and **25 additional coverage topics** to the learner's targets.
   Existing assignments and targets remain. No tasks, responses, progress,
   grades, XP, or scheduler settings are changed.

The resulting graph has **39 assigned problems, 65 questions, 12 multisteps,
82 steps, five information tutorials, and 71 response fields/answers**. Of the
fields, 44 are blanks and 27 are free responses. Free responses collect written
work and expose reference answers without automatically grading it or awarding
mastery credit. No difficulty ratings or estimated question times are invented.

[Verification](verification.json) compares all 350 generated entities and 1,272
attributes with the chained speculative db-after. All current native field
validators passed. Every stage was repeated immediately, producing no material
datoms; each report's source was verified. Seven images are staged under
`assets/images/`, with original bytes checked by SHA-256. They were also
installed in the live image library during the authorized commit, with their
hashes checked again afterward.

The original `1-request.json`, `2-request.json`, and `3-request.json` remain as
unsubmitted preparation records. The authorized submissions, with refreshed
basis guards and exact retry keys, are saved in `commit/stage*-request.json`;
their confirmed receipts are `commit/stage*-commit.edn`. All 350 entities were
read back at the exact committed basis, 1929, and matched the refreshed preview.
All prior learner assignment and target links were preserved. The learner now
has 24 assignments. Never replace a request after an unknown submission outcome;
recover that exact request and key first.

This package covers the five newly imported assignments. MTH 256 Study Guide 1
and Online Homework 2 are separate pending scope selection.
