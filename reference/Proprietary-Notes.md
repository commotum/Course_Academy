• 1. FIRe vs. Repetition Compression

  They are closely related, but not the same thing.

  FIRe is the broader spaced-repetition model/algorithm. It answers: “When a student does
  work on topic X, how should repetition credit or penalty update X and related topics?” It
  handles implicit trickle-down credit, partial encompassings, student-topic learning speed,
  memory decay, and graph propagation.

  Repetition compression is a task-selection strategy that uses FIRe’s graph/repetition
  machinery. It answers: “Given a set of due reviews, what smallest or highest-value task
  set can knock out those reviews implicitly?”

  So I’d model it like this:

  FIRe = scoring / propagation / scheduling model
  Repetition compression = optimization policy that uses FIRe to choose tasks

  They are not fundamentally separate products. Repetition compression is probably a major
  behavior inside the FIRe-powered spaced repetition system. But conceptually, FIRe computes
  and updates repetition state; repetition compression chooses efficient tasks from that
  state.

  2. Dependency Chain

  If building these from scratch, I’d put the chain like this:

  1. Knowledge Graph
     Everything else depends on this. You need topics, prerequisites, key prerequisites,
     courses, modules, questions, knowledge points, and eventually encompassing edges/
     weights.

  2. Answer-choice validation tooling
     This can be built early once the question/content database exists. It is not
     conceptually upstream of FIRe or diagnostics, but it is upstream of trustworthy
     multiple-choice assessments.

  3. Plus-minus diagnostic scoring
     This depends on the graph. It defines how diagnostic answer evidence propagates through
     prerequisites/post-requisites and how confidence is represented per topic.

  4. Diagnostic Algorithm / Diagnostic Tests
     This depends on the graph, question bank, and plus-minus scoring. The diagnostic
     selector decides which questions to ask; plus-minus scoring interprets the answers.

  5. FIRe
     This depends on the graph, especially encompassing relationships/weights, and on per-
     student knowledge/repetition profiles. In production, diagnostics seed the student’s
     initial profile, but FIRe can be built separately once the graph and task-result model
     exist.

  6. Dynamic Task Selection
     This is the top-level orchestration layer. It needs the graph, diagnostic-derived
     knowledge profile, FIRe review state, available lessons/reviews/quizzes, prerequisites,
     remediation rules, and repetition compression.

  A cleaner dependency diagram:

  Knowledge Graph
    -> Question/answer database
        -> Answer-choice validation tooling

  Knowledge Graph
    -> Plus-minus diagnostic scoring
        -> Diagnostic algorithm/tests
            -> Initial student knowledge profile

  Knowledge Graph + student profile + task results
    -> FIRe
        -> due reviews + implicit credit predictions
            -> Dynamic task selection / repetition compression

  3. Graph Data Structures And Attributes Needed

  At minimum, each topic node needs:

  topic_id
  title
  course_id(s)
  module_id
  difficulty estimate
  core/supplemental flag
  is_leaf_topic
  is_foundation_topic
  mastery_floor eligibility
  equivalent_topic group, if any

  Each topic needs content structure:

  lesson_id
  knowledge_points[]
  questions[]
  worked_examples[]
  assessment_items[]
  expected_time / time threshold

  Each knowledge point should carry:

  knowledge_point_id
  topic_id
  sequence_order
  key_prerequisite_topic_ids[]
  question_ids[]

  The graph needs several edge types:

  direct_prerequisite: A -> B
  key_prerequisite: KP/topic -> prerequisite topic
  post_requisite: inverse of prerequisite
  encompassing: advanced topic -> simpler topic
  equivalent_topic / non-ancestor encompassing
  same_module relation
  course membership / module membership

  For FIRe and repetition compression, encompassing edges need weights:

  source_topic_id
  target_topic_id
  encompassing_weight   # 0..1 or similar
  is_full_encompassing
  is_partial_encompassing
  is_inferred_or_explicit
  domain_expert_set

  For diagnostics, you need metadata like:

  diagnostic_eligible
  diagnostic_question_ids
  leaf_topic representative group
  compressed_diagnostic_graph ancestors/progeny
  coverage radius, e.g. within 3 prerequisite edges
  question -> topic mapping
  question -> prerequisite coverage
  expected solve time

  For each student, you need a knowledge profile over the graph:

  conditional_completion flag
  plus_minus balance
  confidence
  accuracy estimate
  next_due_at
  student-topic learning speed
  recent answer history

  Dynamic task selection then sits on top of all of this and ranks candidate tasks by things
  like:

  is_on_knowledge_frontier
  prerequisites mastered
  due review coverage
  implicit reviews knocked out
  future review reduction
  course progress importance
  core topic priority
  remediation urgency
  student-topic learning speed
  available task type: lesson/review/quiz/remediation

  The hard part is not just storing a graph. The hard part is storing multiple kinds of
  edges with different semantics: prerequisites for readiness, key prerequisites for
  remediation, encompassings for implicit repetition credit, and diagnostic inference links
  for evidence propagation.


---

• The graph should not be one generic “topic graph.” It needs several edge types with
  different meanings. Reusing one edge type for everything would make the later algorithms
  ambiguous.

  Core Direction
  I’d use this convention:

  prerequisite edge: simpler topic -> advanced topic
  encompassing edge: advanced topic -> simpler topic

  So prerequisites point “up” the learning path, while encompassings point “down” toward
  skills implicitly practiced by the advanced topic.

  1. Direct Prerequisite Edges
  These define readiness.

  Adding Fractions -> Adding Mixed Numbers
  Multiplying One-Digit Numbers -> Multiplying Two-Digit by One-Digit

  Purpose:

  - decide whether a student is ready for a new lesson
  - define the knowledge frontier
  - propagate diagnostic evidence
  - support topological ordering of curriculum

  Attributes:

  from_topic_id
  to_topic_id
  edge_type = direct_prerequisite
  strength / requiredness
  source = expert / inferred

  Most of the system depends on this layer.

  2. Key Prerequisite Edges
  These are more precise than normal prerequisites. They connect a specific knowledge point
  or lesson step to the prerequisite topic most directly used there.

  Example:

  KP: Evaluating an Exponential Expression
    -> key prerequisite: Multiplying Negative Numbers

  Purpose:

  - targeted remediation
  - if a student fails twice at the same knowledge point, assign reviews on the implicated
    prerequisite

  - avoid vague “go review the whole prerequisite chain” behavior

  Attributes:

  knowledge_point_id
  prerequisite_topic_id
  edge_type = key_prerequisite
  remediation_priority

  These are not just curriculum-order edges. They are diagnostic/remediation hooks.

  3. Encompassing Edges
  These encode “doing the advanced topic gives practice on the simpler topic.”

  Example:

  Multiplying Two-Digit by One-Digit -> Multiplying One-Digit Numbers
  Multiplying Two-Digit by One-Digit -> Adding One-Digit to Two-Digit

  Purpose:

  - implicit review credit
  - repetition compression
  - FIRe propagation
  - deciding whether a due review can be “knocked out” by another task

  Attributes:

  advanced_topic_id
  simpler_topic_id
  edge_type = encompassing
  weight = 0.0..1.0
  is_full_encompassing
  is_partial_encompassing
  explicit_or_inferred

  A full encompassing might have weight 1.0. A partial encompassing might be 0.2, 0.4, etc.,
  meaning the advanced topic only sometimes or partially exercises the simpler skill.

  4. Weighted Encompassing / FIRe Edges
  This is the most important weighted edge layer.

  The docs imply you do not set every pairwise weight. You set weights where they matter,
  usually near direct/key prerequisite edges, and infer the rest through repetition flow.

  So you want something like:

  A -> B weight 1.0
  B -> C weight 0.5

  Then work on A may send full credit to B and fractional downstream credit to C.

  Use cases:

  - positive credit travels down to simpler encompassed topics
  - negative credit travels up to advanced topics that depend on the failed simpler topic
  - partial credit fades over paths

  5. Non-Ancestor Encompassing Edges
  These are encompassing edges between topics that are not connected by prerequisite
  ancestry.

  Example:

  - algebra-based statistics topic
  - calculus-based statistics equivalent topic

  The advanced treatment may fully encompass the simpler treatment even if the simpler
  version is not literally a prerequisite.

  Attributes:

  edge_type = non_ancestor_encompassing
  weight = 1.0 or partial
  equivalent_topic_group_id

  These matter for cross-course credit.

  6. Equivalent Topic Edges / Groups
  Sometimes the cleaner structure is not an edge, but a group:

  equivalent_group_id = "mean_and_variance"
  topics = [
    algebra_stats_mean_variance,
    calculus_stats_mean_variance
  ]

  Then you can derive non-ancestor encompassing edges between advanced and simpler variants.

  7. Same-Module / Correlation Edges
  The diagnostic section mentions looser correlation-based inference, especially leaf topics
  in the same module.

  Example:

  leaf_topic_A --same_module--> leaf_topic_B

  Purpose:

  - if a student answers a representative leaf topic correctly, give some diagnostic credit
    to nearby/sibling leaf topics

  - reduce diagnostic length

  This should be separate from prerequisite/encompassing because it is weaker evidence.

  Attributes:

  topic_id
  related_topic_id
  edge_type = same_module_correlation
  diagnostic_credit_weight

  8. Diagnostic Compression Edges
  The diagnostic algorithm compresses the graph into a smaller diagnostic graph where topics
  are “covered” by nearby ancestors/progeny.

  This may be derived rather than stored manually.

  You need to know:

  topic_id
  diagnostic_representative_topic_id
  ancestor_distance
  progeny_distance
  coverage_radius

  Purpose:

  - choose fewer diagnostic questions
  - ensure every topic is covered at the desired granularity
  - infer knowledge frontier efficiently

  9. Post-Requisite Edges
  These are just inverse prerequisite edges.

  You probably do not need to store them separately unless performance demands it.

  direct prerequisite: A -> B
  post-requisite view: B has prerequisite A; A has post-requisite B

  Purpose:

  - incorrect diagnostic answers propagate upward to post-requisites
  - failed simpler topics can reduce confidence in more advanced topics

  10. Content Structure Edges
  These are not “knowledge graph” edges in the strict topic-topic sense, but they matter.

  course -> module -> topic -> knowledge_point -> question
  question -> assessed_topic
  question -> prerequisite_topics_exercised

  Purpose:

  - lessons
  - diagnostics
  - quizzes
  - review generation
  - remediation

  Practical Minimum
  To build the system, I’d start with these edge tables:

  topic_prerequisite_edges
  - prerequisite_topic_id
  - postrequisite_topic_id
  - requiredness

  knowledge_point_key_prerequisites
  - knowledge_point_id
  - prerequisite_topic_id
  - remediation_priority

  topic_encompassing_edges
  - advanced_topic_id
  - simpler_topic_id
  - weight
  - explicit_or_inferred
  - source

  topic_equivalence_groups
  - equivalent_group_id
  - topic_id
  - level / course_order

  topic_module_membership
  - topic_id
  - module_id
  - is_leaf_topic

  Then derive:

  - post-requisites from prerequisites
  - diagnostic compressed graph from prerequisite ancestry
  - inferred encompassing paths from explicit encompassing weights
  - dynamic review knock-outs from FIRe state plus encompassing weights.


---


Ok, a few questions:

1. Are FIRe and Repetition Compression closely related? Are they basically the same thing? Or fundamentally different in some way?
2. Out of the following components, what is the dependency chain? ie, if we were to build each of these ourselves, in which order would we need to build them?

    - Knowledge Graph
    - FIRe (Algorithm?)
    - Diagnostic Algorithm (Diagnostic tests)
    - Plus-minus diagnostic scoring
    - Dynamic task selection
    - Answer-choice validation tooling

3. Which data structures and attributes would we need to have in our graph to pull this off?


• These are broader “Math Academy-built system” references, not all direct uses of the word
  proprietary.

  - Automated platform / teaching machine
    Math Academy describes itself as an adaptive, fully automated online platform that
    emulates expert tutor decisions. The “teaching machine” language refers to automating
    individualized learning strategies that were first attempted manually. See DATA/The Math
    Academy Way/I-PRELIMINARIES/1-The-Two-Sigma-Solution/1-The-Two-Sigma-Solution.md:35.

  - Knowledge graph
    The central curriculum data structure: thousands of interlinked topics, relationships,
    prerequisites, key prerequisites, and encompassings. It powers algorithmic decisions
    about placement, learning paths, remediation, review, and diagnostics. See DATA/The Math
    Academy Way/I-PRELIMINARIES/4-Core-Technology-the-Knowledge-Graph/4-Core-Technology-the-
    Knowledge-Graph.md:3.

  - FIRe
    Fractional Implicit Repetition, described as Math Academy’s proprietary or novel spaced
    repetition model. It generalizes spaced repetition to hierarchical math knowledge by
    letting advanced-topic repetitions “trickle down” to simpler topics, while calibrating
    to each student-topic pair. See DATA/The Math Academy Way/III-COGNITIVE-LEARNING-
    STRATEGIES/18-Spaced-Repetition-Distributed-Practice/18-Spaced-Repetition-Distributed-
    Practice.md:125 and DATA/The Math Academy Way/V-TECHNICAL-DEEP-DIVES/29-Technical-Deep-
    Dive-on-Spaced-Repetition/29-Technical-Deep-Dive-on-Spaced-Repetition.md:5.

  - Repetition compression
    The process of replacing many due reviews with a smaller set of tasks that implicitly
    cover them. A new lesson or review can “knock out” other due reviews if it exercises the
    same component skills. See DATA/The Math Academy Way/III-COGNITIVE-LEARNING-
    STRATEGIES/18-Spaced-Repetition-Distributed-Practice/18-Spaced-Repetition-Distributed-
    Practice.md:162.

  - Diagnostic algorithm
    The adaptive diagnostic system estimates a student’s knowledge frontier while minimizing
    questions. It uses graph structure, encompassings, correlation-based inference, and a
    compressed diagnostic graph to infer knowledge across many topics from fewer questions.
    See DATA/The Math Academy Way/V-TECHNICAL-DEEP-DIVES/30-Technical-Deep-Dive-on-
    Diagnostic-Exams/30-Technical-Deep-Dive-on-Diagnostic-Exams.md:5.

  - Plus-minus diagnostic scoring
    A diagnostic evidence mechanism. Each topic gets a plus-minus balance: sign predicts
    whether the student knows it, magnitude represents confidence. Answer evidence
    propagates through the graph to prerequisites and post-requisites. See DATA/The Math
    Academy Way/V-TECHNICAL-DEEP-DIVES/30-Technical-Deep-Dive-on-Diagnostic-Exams/30-
    Technical-Deep-Dive-on-Diagnostic-Exams.md:54.

  - Learning analytics tools
    Internal tools for analyzing content performance at high granularity: topic, knowledge
    point, and individual question. They are used to find where students struggle and refine
    content or algorithms. See DATA/The Math Academy Way/III-COGNITIVE-LEARNING-
    STRATEGIES/21-Targeted-Remediation/21-Targeted-Remediation.md:73.

  - XP / leagues / penalties
    The gamification and incentive system. XP is calibrated to focused productive work;
    leagues incentivize quantity; scaled XP and penalties incentivize quality and discourage
    gaming. See DATA/The Math Academy Way/III-COGNITIVE-LEARNING-STRATEGIES/22-
    Gamification/22-Gamification.md:41.

  - Dynamic task selection
    The dashboard is not a fixed queue. Tasks are selected dynamically based on what is
    optimal now, including whether a new lesson can knock out existing reviews. See DATA/The
    Math Academy Way/VI-FREQUENTLY-ASKED-QUESTIONS/FAQ-The-Practice-Experience/FAQ-The-
    Practice-Experience.md:297.

  - Answer-choice validation tooling
    An internal validation tool run against the database to ensure correct answers are
    randomly distributed across multiple-choice options. See DATA/The Math Academy Way/VI-
    FREQUENTLY-ASKED-QUESTIONS/FAQ-XP-and-Practice-Schedules/FAQ-XP-and-Practice-
    Schedules.md:51.

  - MA’s ALEKS-comparison notes
    Internal future-addition notes comparing Math Academy’s graph/diagnostic approach to
    ALEKS knowledge space theory. The notes say MA moved away from exhaustive combinatorial
    knowledge-state filtering toward quantities “flowing through the graph,” partly for
    scalability and spaced repetition. See DATA/The Math Academy Way/BACK-MATTER/Notes-for-
    Future-Additions/Notes-for-Future-Additions.md:76.



