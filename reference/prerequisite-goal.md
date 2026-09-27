# Pasteable Codex Goal

Build the Electrical-and-Computer-Engineering prerequisite-identification step
into a multi-pass, fault-tolerant, fully resumable pipeline that generates only
direct readiness prerequisite edges from compiled lessons by combining
course-map-aware generation, no-map skill extraction, course-map skill matching,
and Mathematical Foundations matching. Use this plan as the reference:
`/home/jake/Developer/MA/WORKING-PROGRESS/prerequisite-goal.md`.

# Prerequisite Identification Goal Plan

The prerequisite-identification step should produce a robust merged prerequisite
graph by running several complementary passes, then normalizing their outputs
into one final direct-edge set.

The governing edge standard remains:

1. Use prerequisites only for readiness gating.
2. Require the dependency to be lesson-wide, not just one example or step.
3. Prefer the nearest direct prerequisite, not the full ancestor chain.
4. Reject edges that are only useful context, historical background, related
   material, or incidental practice.

## Operating Requirements

Each phase should be cached and resumable at the individual topic level. A valid
completed artifact should be reused; an invalid, missing, stale, or failed
artifact should not be treated as completed. Usage-limit failures, malformed
outputs, and validation failures should be logged without blocking unrelated
topics that can still proceed.

Common LLM mistakes should be handled by prevalidation and deterministic repair
where possible. The pipeline should normalize JSON, remove duplicate edges,
remove self-edges, reject unknown topic IDs, and reduce transitive edges after
the generated candidate sets are merged. These repairable issues should not be
overemphasized in the prompt as hard failure cases.

## Phase 1: Map-Aware Course Prerequisites

Give the runner:

1. The compiled lesson.
2. The course map for the course being developed.

The runner identifies direct course-topic prerequisites using the course map as
the candidate topic universe, while remembering that course-map order is
presentation order, not dependency order.

Output: `v1` prerequisite set.

## Phase 2: No-Map Skill Extraction

Give the runner only the compiled lesson, without the course map.

The runner identifies the lesson-wide prerequisite skills, concepts, procedures,
representations, and mappings that a learner must already have before starting
the lesson.

This phase should not choose topic IDs. It should produce a course-agnostic
candidate prerequisite skill list.

Output: candidate prerequisite skill list.

## Phase 3: Course-Map Skill Matching

Give the runner:

1. The candidate prerequisite skill list from Phase 2.
2. The course map for the course being developed.

The runner maps the candidate skills to the closest matching topics in the
course map. These mapped topics become a second course-specific prerequisite
set.

Output: `v2` prerequisite set.

## Phase 4: Mathematical Foundations III Matching

Give the runner:

1. The candidate prerequisite skill list from Phase 2.
2. The Mathematical Foundations III course map.

The runner maps any candidate skills that correspond to Mathematical Foundations
III topics.

Output: external MF3 prerequisite set.

## Phase 5: Mathematical Foundations II Matching

Give the runner:

1. The candidate prerequisite skill list from Phase 2.
2. The Mathematical Foundations II course map.

The runner maps any candidate skills that correspond to Mathematical Foundations
II topics.

Output: external MF2 prerequisite set.

## Phase 6: Mathematical Foundations I Matching

Give the runner:

1. The candidate prerequisite skill list from Phase 2.
2. The Mathematical Foundations I course map.

The runner maps any candidate skills that correspond to Mathematical Foundations
I topics.

Output: external MF1 prerequisite set.

## Final Normalize And Merge

Combine all generated prerequisite sets:

```text
v1 course-map prerequisites
+ v2 candidate-matched course prerequisites
+ MF3 matched prerequisites
+ MF2 matched prerequisites
+ MF1 matched prerequisites
```

Then deterministically normalize the combined output:

- remove self-edges
- remove duplicates
- remove unknown topic IDs
- preserve only direct readiness prerequisites
- remove transitive edges where a nearer prerequisite already covers an ancestor
- prevent cycles
- recompute prerequisite counts
- write the final canonical prerequisite artifact

The final output should be the normalized direct prerequisite set for each topic,
ready to publish as the course's canonical `Prerequisites.csv` and to use when
inserting prerequisite sections into compiled lesson markdown.
