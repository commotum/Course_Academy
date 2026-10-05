//! Generic activity delivery and grading used by the learner application.
//!
//! These functions compute against a captured database basis. The caller must
//! reserve presentations and commit response, timing, and credit writes together
//! with a basis guard and item-status CAS. No function here mutates a database.
use crate::{
    Result,
    activities::{decimal_number, evaluate_kp_prefix, lesson_xp_candidate},
    core::Event,
    schema::{EntitySnapshot, LoadedRuntime, load_runtime, timestamp_days, writeback},
};
use chrono::{DateTime, Utc};
use num_rational::BigRational;
use num_traits::{ToPrimitive, Zero};
use serde::Serialize;
use serde_json::{Value, json};
use std::collections::{BTreeMap, BTreeSet, VecDeque};

#[derive(Clone, Debug, Serialize)]
pub struct LessonStep {
    pub step: u64,
    pub content: u64,
    pub kind: String,
    pub example: Option<u64>,
    pub questions: Vec<u64>,
}

fn ident(s: &EntitySnapshot, eid: u64, attr: &str) -> Result<String> {
    s.ident(
        s.entity(eid)?
            .get(attr)
            .ok_or_else(|| format!("missing {attr}"))?,
    )
}

fn nonempty(s: &EntitySnapshot, eid: u64, attr: &str) -> Result<()> {
    if s.entity(eid)?
        .get(attr)
        .and_then(Value::as_str)
        .is_none_or(|v| v.trim().is_empty())
    {
        return Err(format!("{eid} needs nonempty {attr}"));
    }
    Ok(())
}

/// The current learner player supports linear lessons, including adaptive KP
/// expansion. Reject malformed routes instead of silently omitting content.
pub fn lesson_steps(s: &EntitySnapshot, activity: u64) -> Result<Vec<LessonStep>> {
    if ident(s, activity, "activity/type")? != "activity.type/lesson" {
        return Err("the progressive player requires a lesson activity".into());
    }
    let members: BTreeSet<_> = s.refs(activity, "activity/steps")?.into_iter().collect();
    let mut current = Some(s.reference(activity, "activity/first-step")?);
    let mut visited = BTreeSet::new();
    let mut result = vec![];
    while let Some(step) = current {
        if !members.contains(&step) || !visited.insert(step) {
            return Err("lesson steps must form one acyclic owned route".into());
        }
        let content = s.reference(step, "step/content")?;
        let r = s.entity(content)?;
        let mut entry = LessonStep {
            step,
            content,
            kind: String::new(),
            example: None,
            questions: vec![],
        };
        if r.contains_key("tutorial/id") {
            nonempty(s, content, "tutorial/content")?;
            entry.kind = "tutorial".into();
        } else if r.contains_key("knowledge-point/id") {
            entry.kind = "knowledge-point".into();
            let example = s.reference(content, "knowledge-point/canonical-example")?;
            if !s.entity(example)?.contains_key("question/id") {
                return Err("KP canonical example must reference a question".into());
            }
            nonempty(s, example, "question/problem")?;
            nonempty(s, example, "question/worked-solution")?;
            entry.example = Some(example);
            entry.questions = s.refs(content, "knowledge-point/questions")?;
            entry.questions.sort_unstable();
            entry.questions.dedup();
            if entry.questions.is_empty() || entry.questions.iter().any(|q| s.is_example(*q)) {
                return Err("KP needs a practice pool separate from its worked example".into());
            }
        } else if r.contains_key("question/id") {
            nonempty(s, content, "question/problem")?;
            entry.kind = if s.is_example(content) {
                nonempty(s, content, "question/worked-solution")?;
                "example"
            } else {
                validate_question(s, content)?;
                "question"
            }
            .into();
        } else {
            return Err("unsupported content in the progressive lesson".into());
        }
        result.push(entry);
        current = s.optional_ref(step, "step/next")?;
    }
    if visited != members {
        return Err("lesson contains unreachable steps".into());
    }
    Ok(result)
}

fn validate_question(s: &EntitySnapshot, question: u64) -> Result<()> {
    nonempty(s, question, "question/problem")?;
    if !s.is_ordinary_question(question)? {
        return Err("practice needs an ordinary question".into());
    }
    let fields = s.refs(question, "question/answer-fields")?;
    if fields.is_empty() {
        return Err("practice question has no answer fields".into());
    }
    let mut keys = BTreeSet::new();
    for field in fields {
        nonempty(s, field, "answer-field/key")?;
        if !keys.insert(s.entity(field)?["answer-field/key"].as_str().unwrap()) {
            return Err("question answer field keys must be unique".into());
        }
        if !matches!(
            ident(s, field, "answer-field/type")?.as_str(),
            "answer-field.type/radio" | "answer-field.type/select" | "answer-field.type/blank"
        ) {
            return Err("unsupported answer field type".into());
        }
        let choices = s.refs(field, "answer-field/choices")?;
        let correct = s.reference(field, "answer-field/correct")?;
        if !choices.contains(&correct) {
            return Err("canonical answer must belong to its answer field".into());
        }
        for answer in choices {
            if !matches!(
                ident(s, answer, "answer/type")?.as_str(),
                "answer.type/math" | "answer.type/text" | "answer.type/image"
            ) {
                return Err("unsupported answer representation".into());
            }
            if s.entity(answer)?
                .get("answer/value")
                .and_then(Value::as_str)
                .is_none()
            {
                return Err("answer needs a string value".into());
            }
        }
        if ident(s, field, "answer-field/type")? == "answer-field.type/blank" {
            let canonical = s.entity(correct)?["answer/value"].as_str().unwrap();
            if canonical.trim().is_empty() {
                return Err("canonical blank answer is empty".into());
            }
            match ident(s, correct, "answer/type")?.as_str() {
                "answer.type/math"
                    if RationalParser::parse(&normalize_math(canonical)).is_some() => {}
                "answer.type/text" => {}
                _ => {
                    return Err("this blank needs a symbolic grader before it can be served".into());
                }
            }
        }
    }
    Ok(())
}

fn seen_questions(s: &EntitySnapshot, learner: u64) -> Result<BTreeSet<u64>> {
    let mut seen = BTreeSet::new();
    for task in s.refs(learner, "learner/activity")? {
        for item in s.refs(task, "learner-task/items")? {
            if let Some(content) = s.optional_ref(item, "task-item/content")? {
                if s.is_ordinary_question(content)? {
                    seen.insert(content);
                }
            }
        }
    }
    Ok(seen)
}

fn task_learner(s: &EntitySnapshot, items: &[u64]) -> Result<Option<u64>> {
    let Some(item) = items.first() else {
        return Ok(None);
    };
    let tasks = s.owners(*item, "learner-task/items")?;
    if tasks.len() != 1 {
        return Err("presentation must have one task owner".into());
    }
    let learners = s.owners(tasks[0], "learner/activity")?;
    if learners.len() != 1 {
        return Err("task must have one learner owner".into());
    }
    let members: BTreeSet<_> = s
        .refs(tasks[0], "learner-task/items")?
        .into_iter()
        .collect();
    if items.iter().any(|i| !members.contains(i))
        || items.iter().copied().collect::<BTreeSet<_>>().len() != items.len()
    {
        return Err("presentations must be distinct members of the task".into());
    }
    Ok(Some(learners[0]))
}

#[derive(Debug)]
struct Position {
    next: Option<u64>,
    passed: bool,
}

fn consume_instruction(
    s: &EntitySnapshot,
    items: &[u64],
    cursor: &mut usize,
    content: u64,
    completed_item: Option<u64>,
) -> Result<bool> {
    let Some(item) = items.get(*cursor) else {
        return Ok(false);
    };
    if s.reference(*item, "task-item/content")? != content {
        return Err("presentation history does not follow lesson order".into());
    }
    if completed_item == Some(*item) {
        if *cursor + 1 != items.len()
            || ident(s, *item, "task-item/status")? != "task-item.status/started"
        {
            return Err("only the final active instruction can be completed".into());
        }
        *cursor += 1;
        return Ok(true);
    }
    match ident(s, *item, "task-item/status")?.as_str() {
        "task-item.status/completed" => {
            *cursor += 1;
            Ok(true)
        }
        "task-item.status/started" | "task-item.status/paused" if *cursor + 1 == items.len() => {
            Ok(false)
        }
        _ => Err("instruction needs completion before continuing".into()),
    }
}

fn question_outcome(s: &EntitySnapshot, item: u64) -> Result<Option<Option<bool>>> {
    match ident(s, item, "task-item/status")?.as_str() {
        "task-item.status/correct" => Ok(Some(Some(true))),
        "task-item.status/incorrect" => Ok(Some(Some(false))),
        "task-item.status/skipped" => Ok(Some(None)),
        "task-item.status/started" | "task-item.status/paused" => Ok(None),
        _ => Err("ordinary question has invalid completion status".into()),
    }
}

fn position(s: &EntitySnapshot, activity: u64, items: &[u64]) -> Result<Position> {
    position_after(s, activity, items, None)
}

fn position_after(
    s: &EntitySnapshot,
    activity: u64,
    items: &[u64],
    completed_item: Option<u64>,
) -> Result<Position> {
    let mut seen = if let Some(learner) = task_learner(s, items)? {
        seen_questions(s, learner)?
    } else {
        BTreeSet::new()
    };
    let mut cursor = 0;
    let mut all_correct = true;
    for step in lesson_steps(s, activity)? {
        match step.kind.as_str() {
            "tutorial" | "example" => {
                if !consume_instruction(s, items, &mut cursor, step.content, completed_item)? {
                    return Ok(Position {
                        next: Some(step.content),
                        passed: false,
                    });
                }
            }
            "question" => {
                let Some(item) = items.get(cursor) else {
                    if seen.contains(&step.content) {
                        return Err("This authored question was already presented. Fresh content is needed; the lesson is not failed.".into());
                    }
                    return Ok(Position {
                        next: Some(step.content),
                        passed: false,
                    });
                };
                if s.reference(*item, "task-item/content")? != step.content {
                    return Err("unexpected lesson question".into());
                }
                let Some(outcome) = question_outcome(s, *item)? else {
                    if cursor + 1 != items.len() {
                        return Err("unanswered question precedes later content".into());
                    }
                    return Ok(Position {
                        next: Some(step.content),
                        passed: false,
                    });
                };
                all_correct &= outcome == Some(true);
                cursor += 1;
            }
            "knowledge-point" => {
                let example = step.example.unwrap();
                if !consume_instruction(s, items, &mut cursor, example, completed_item)? {
                    return Ok(Position {
                        next: Some(example),
                        passed: false,
                    });
                }
                let mut outcomes = vec![];
                loop {
                    let decision = evaluate_kp_prefix(&outcomes)?;
                    if decision.complete() {
                        if decision.passed() == Some(false) {
                            if cursor != items.len() {
                                return Err("presentations continue after failed practice".into());
                            }
                            return Ok(Position {
                                next: None,
                                passed: false,
                            });
                        }
                        break;
                    }
                    if let Some(item) = items.get(cursor) {
                        let content = s.reference(*item, "task-item/content")?;
                        if !step.questions.contains(&content) {
                            return Err(
                                "question does not belong to current knowledge point".into()
                            );
                        }
                        let Some(outcome) = question_outcome(s, *item)? else {
                            if cursor + 1 != items.len() {
                                return Err("unanswered question precedes later content".into());
                            }
                            return Ok(Position {
                                next: Some(content),
                                passed: false,
                            });
                        };
                        outcomes.push(outcome);
                        seen.insert(content);
                        cursor += 1;
                    } else {
                        let candidates = step
                            .questions
                            .iter()
                            .copied()
                            .filter(|q| !seen.contains(q) && validate_question(s, *q).is_ok())
                            .collect::<Vec<_>>();
                        let policy = crate::question_selection::active_policy(s)?;
                        let weights = crate::question_selection::weights(
                            s,
                            policy,
                            "lesson",
                            outcomes.len(),
                        )?;
                        let task = items
                            .first()
                            .map(|item| s.owners(*item, "learner-task/items"))
                            .transpose()?
                            .and_then(|owners| owners.first().copied())
                            .unwrap_or(activity);
                        let seed =
                            format!("task-{task}/kp-{}/slot-{}", step.content, outcomes.len());
                        let next = crate::question_selection::select(s, &candidates, weights, &seed)?
                            .ok_or("More fresh questions are needed for this knowledge point. Your lesson remains unfinished; this is not a failed attempt.")?;
                        return Ok(Position {
                            next: Some(next),
                            passed: false,
                        });
                    }
                }
            }
            _ => unreachable!(),
        }
    }
    if cursor != items.len() {
        return Err("presentations continue beyond the lesson".into());
    }
    Ok(Position {
        next: None,
        passed: all_correct,
    })
}

/// Return an existing active presentation's content, or the next fresh content.
/// The caller reserves a returned new question atomically before displaying it.
pub fn next_content(s: &EntitySnapshot, activity: u64, items: &[u64]) -> Result<Option<u64>> {
    Ok(position(s, activity, items)?.next)
}

/// The first presentation has no task owner yet. Check its learner history
/// explicitly; later adaptive draws recover ownership from existing items.
pub fn first_content(s: &EntitySnapshot, activity: u64, learner: u64) -> Result<Option<u64>> {
    let next = next_content(s, activity, &[])?;
    if let Some(q) = next
        && s.is_ordinary_question(q)?
        && seen_questions(s, learner)?.contains(&q)
    {
        return Err("This authored question was already presented. Fresh content is needed; the lesson is not failed.".into());
    }
    Ok(next)
}

pub fn lesson_passed(s: &EntitySnapshot, activity: u64, items: &[u64]) -> Result<bool> {
    let p = position(s, activity, items)?;
    Ok(p.next.is_none() && p.passed)
}

/// Plan the next presentation while completing the current instruction in the
/// same transaction. The small status overlay avoids cloning the full catalog.
pub fn continuation(
    s: &EntitySnapshot,
    activity: u64,
    items: &[u64],
    complete_instruction: bool,
    base: i64,
) -> Result<(Option<u64>, bool, i64)> {
    let completed = if complete_instruction {
        let item = *items.last().ok_or("instruction presentation required")?;
        let content_id = s.reference(item, "task-item/content")?;
        let content = s.entity(content_id)?;
        if !content.contains_key("tutorial/id") && !s.is_example(content_id) {
            return Err("ordinary questions require a submitted answer".into());
        }
        Some(item)
    } else {
        None
    };
    let p = position_after(s, activity, items, completed)?;
    let passed = p.next.is_none() && p.passed;
    let xp = if p.next.is_none() {
        completed_lesson_xp(s, items, base)?
    } else {
        0
    };
    Ok((p.next, passed, xp))
}

/// An eligible lesson and the evidence behind its position in the learner queue.
/// Larger priority values sort first; ties use topic and activity entity IDs.
#[derive(Clone, Debug, Serialize)]
pub struct PlannedActivity {
    pub activity: u64,
    pub topic: u64,
    pub priority: f64,
    pub target_count: usize,
    pub target_topics: Vec<u64>,
    /// Smallest unfinished prerequisite closure among the supported targets,
    /// including that target itself. Zero for ordinary course work.
    pub remaining_topics: usize,
    pub nearest_target_steps: Option<usize>,
    pub due: Option<DateTime<Utc>>,
    pub reason: String,
}

/// Plan against one explicit clock instant. Self-directed targets broaden the
/// course scope, but never bypass prerequisites, FIRe readiness, or fresh-bank
/// checks. Started/paused lessons remain resumable after scope changes.
pub fn plan_candidates(
    s: &EntitySnapshot,
    learner: u64,
    course: u64,
    at: DateTime<Utc>,
) -> Result<Vec<PlannedActivity>> {
    // Captured lesson banks currently contain two or three questions per KP.
    // Exhaustion without a passing streak ends as failed without mastery or XP.
    plan_candidates_with_supply(s, learner, course, at, 2, true)
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum StudyScope {
    Targets,
    Course,
    Queue,
}

/// Zero-based global prerequisite layers, matching the graph's L01… badges.
/// A topic's layer is the longest path from any root, using topic/next only.
fn topic_layers(s: &EntitySnapshot) -> Result<BTreeMap<u64, usize>> {
    let mut layers: BTreeMap<_, _> = s
        .entities
        .iter()
        .filter(|(_, record)| record.contains_key("topic/id"))
        .map(|(&topic, _)| (topic, 0usize))
        .collect();
    let mut remaining: BTreeMap<_, _> = layers.keys().map(|&topic| (topic, 0usize)).collect();
    let mut outgoing = BTreeMap::new();
    for &topic in layers.keys() {
        let next = s.refs(topic, "topic/next")?;
        for &dependent in &next {
            *remaining
                .get_mut(&dependent)
                .ok_or("topic/next must reference topics")? += 1;
        }
        outgoing.insert(topic, next);
    }
    let mut roots: VecDeque<_> = remaining
        .iter()
        .filter_map(|(&topic, &count)| (count == 0).then_some(topic))
        .collect();
    let mut visited = 0;
    while let Some(topic) = roots.pop_front() {
        visited += 1;
        let next_layer = layers[&topic] + 1;
        for &dependent in &outgoing[&topic] {
            let layer = layers.get_mut(&dependent).unwrap();
            *layer = (*layer).max(next_layer);
            let count = remaining.get_mut(&dependent).unwrap();
            *count -= 1;
            if *count == 0 {
                roots.push_back(dependent);
            }
        }
    }
    if visited != layers.len() {
        return Err(
            "The prerequisite graph contains a cycle; queue layers cannot be determined".into(),
        );
    }
    Ok(layers)
}

/// Study has two independent sources. Explicit selections may cross courses
/// and bypass the engine's mastery/prerequisite gates, but never content checks.
/// Engine suggestions rotate eligible lessons across modules. Both modes keep
/// ongoing work first; explicit requests then use global layer and priority.
/// A cardinality-many queue is a set, not a user-defined ordering.
pub fn study_candidates(
    s: &EntitySnapshot,
    learner: u64,
    course: u64,
    at: DateTime<Utc>,
) -> Result<Vec<PlannedActivity>> {
    let queued = s.entity(learner)?.get("learner/self-directed") == Some(&json!(true));
    if queued {
        queue_candidates(s, learner, course, at)
    } else {
        engine_candidates(s, learner, course, at)
    }
}

/// Explicit requests remain preparable independently of the displayed Study mode.
pub fn queue_candidates(
    s: &EntitySnapshot,
    learner: u64,
    course: u64,
    at: DateTime<Utc>,
) -> Result<Vec<PlannedActivity>> {
    let mut plan = plan_candidates_in_scope(s, learner, course, at, 2, false, StudyScope::Queue)?;
    if !plan.is_empty() {
        let layers = topic_layers(s)?;
        plan.sort_by(|a, b| {
            (b.priority >= 10000.0)
                .cmp(&(a.priority >= 10000.0))
                .then_with(|| layers[&a.topic].cmp(&layers[&b.topic]))
                .then_with(|| b.priority.total_cmp(&a.priority))
                .then_with(|| a.topic.cmp(&b.topic))
                .then_with(|| a.activity.cmp(&b.activity))
        });
    }
    for candidate in &mut plan {
        if candidate.priority < 10000.0 {
            candidate.reason = "Selected for your queue".into();
        }
    }
    Ok(plan)
}

/// Engine eligibility is independent of explicit queue membership and mode.
pub fn engine_candidates(
    s: &EntitySnapshot,
    learner: u64,
    course: u64,
    at: DateTime<Utc>,
) -> Result<Vec<PlannedActivity>> {
    let plan = plan_candidates_in_scope(s, learner, course, at, 2, true, StudyScope::Course)?;

    // Preserve engine ranking inside each module. Visit modules in the order
    // of their first ranked candidate, then take one lesson from each per round.
    let mut modules = BTreeMap::new();
    for unit in s.refs(course, "course/units")? {
        for module in s.refs(unit, "unit/modules")? {
            for topic in s.refs(module, "module/topics")? {
                modules.entry(topic).or_insert(module);
            }
        }
    }
    let mut ongoing = vec![];
    let mut lanes: Vec<std::collections::VecDeque<PlannedActivity>> = vec![];
    let mut lane_indices = BTreeMap::new();
    for candidate in plan {
        if candidate.priority >= 10000.0 {
            ongoing.push(candidate);
            continue;
        }
        let module = modules
            .get(&candidate.topic)
            .copied()
            .unwrap_or(candidate.topic);
        let index = *lane_indices.entry(module).or_insert_with(|| {
            lanes.push(std::collections::VecDeque::new());
            lanes.len() - 1
        });
        lanes[index].push_back(candidate);
    }
    loop {
        let before = ongoing.len();
        for lane in &mut lanes {
            if let Some(candidate) = lane.pop_front() {
                ongoing.push(candidate);
            }
        }
        if ongoing.len() == before {
            break;
        }
    }
    Ok(ongoing)
}

/// Compatibility wrapper for callers that only need the ordered activity IDs.
pub fn candidates(s: &EntitySnapshot, learner: u64, course: u64) -> Result<Vec<u64>> {
    Ok(plan_candidates(s, learner, course, Utc::now())?
        .into_iter()
        .map(|p| p.activity)
        .collect())
}

fn candidates_with_supply(
    s: &EntitySnapshot,
    learner: u64,
    course: u64,
    minimum_fresh: usize,
    exclude_practiced: bool,
) -> Result<Vec<u64>> {
    Ok(plan_candidates_with_supply(
        s,
        learner,
        course,
        Utc::now(),
        minimum_fresh,
        exclude_practiced,
    )?
    .into_iter()
    .map(|p| p.activity)
    .collect())
}

/// Collect mapped topics without assuming assignment steps are linear lessons.
/// The visited set also bounds traversal of malformed cyclic containment.
fn assignment_targets(s: &EntitySnapshot, assignment: u64) -> Result<BTreeSet<u64>> {
    let mut pending = vec![];
    for step in s.refs(assignment, "activity/steps")? {
        pending.push(s.reference(step, "step/content")?);
    }
    let mut visited = BTreeSet::new();
    let mut targets = BTreeSet::new();
    while let Some(content) = pending.pop() {
        if !visited.insert(content) {
            continue;
        }
        let record = s.entity(content)?;
        if record.contains_key("assigned-problem/id") {
            targets.extend(s.refs(content, "assigned-problem/topic-coverage")?);
            pending.push(s.reference(content, "assigned-problem/content")?);
        }
        if record.contains_key("multistep/id") {
            for step in s.refs(content, "multistep/steps")? {
                pending.push(s.reference(step, "step/content")?);
            }
        }
    }
    Ok(targets)
}

#[derive(Default)]
struct TargetSupport {
    targets: BTreeSet<u64>,
    remaining: Option<usize>,
    distance: Option<usize>,
    due: Option<DateTime<Utc>>,
}

fn target_support(
    s: &EntitySnapshot,
    learner: u64,
    prerequisites: &BTreeMap<u64, BTreeSet<u64>>,
    ready: &BTreeSet<u64>,
) -> Result<BTreeMap<u64, TargetSupport>> {
    if s.entity(learner)?.get("learner/self-directed") != Some(&json!(true)) {
        return Ok(BTreeMap::new());
    }
    let mut targets: BTreeMap<u64, Option<DateTime<Utc>>> = s
        .refs(learner, "learner/targets")?
        .into_iter()
        .map(|topic| (topic, None))
        .collect();
    let mut completed = BTreeSet::new();
    for task in s.refs(learner, "learner/activity")? {
        if ident(s, task, "learner-task/status")? == "learner-task.status/completed" {
            completed.insert(s.reference(task, "learner-task/activity")?);
        }
    }
    for assignment in s.refs(learner, "learner/assignments")? {
        if ident(s, assignment, "activity/type")? != "activity.type/assignment" {
            return Err("learner/assignments must reference assignment activities".into());
        }
        // A completed assignment no longer calls for preparation. Failed
        // attempts retain their mapping and deadline for another attempt.
        if completed.contains(&assignment) {
            continue;
        }
        let due = s
            .entity(assignment)?
            .get("activity/due")
            .map(crate::schema::parse_instant)
            .transpose()?;
        for topic in assignment_targets(s, assignment)? {
            let entry = targets.entry(topic).or_default();
            if let Some(due) = due {
                *entry = Some(entry.map_or(due, |previous| previous.min(due)));
            }
        }
    }
    let mut support: BTreeMap<u64, TargetSupport> = BTreeMap::new();
    for (target, due) in targets {
        if !s.entity(target)?.contains_key("topic/id") {
            return Err("study targets and assignment coverage must reference topics".into());
        }
        // One breadth-first traversal per distinct target counts a shared
        // ancestor once, even through diamonds or cycles. Ready topics close
        // that branch: their own prerequisites need no new preparation now.
        let mut distances = BTreeMap::new();
        let mut pending = VecDeque::from([(target, 0)]);
        while let Some((topic, distance)) = pending.pop_front() {
            if distances.contains_key(&topic) {
                continue;
            }
            distances.insert(topic, distance);
            if !ready.contains(&topic) {
                for prerequisite in prerequisites.get(&topic).into_iter().flatten() {
                    pending.push_back((*prerequisite, distance + 1));
                }
            }
        }
        let remaining = distances.keys().filter(|t| !ready.contains(t)).count();
        for (topic, distance) in distances {
            let entry = support.entry(topic).or_default();
            entry.targets.insert(target);
            entry.remaining = Some(entry.remaining.map_or(remaining, |n| n.min(remaining)));
            entry.distance = Some(entry.distance.map_or(distance, |n| n.min(distance)));
            if let Some(due) = due {
                entry.due = Some(entry.due.map_or(due, |previous| previous.min(due)));
            }
        }
    }
    Ok(support)
}

fn plan_candidates_with_supply(
    s: &EntitySnapshot,
    learner: u64,
    course: u64,
    at: DateTime<Utc>,
    minimum_fresh: usize,
    exclude_practiced: bool,
) -> Result<Vec<PlannedActivity>> {
    plan_candidates_in_scope(
        s,
        learner,
        course,
        at,
        minimum_fresh,
        exclude_practiced,
        StudyScope::Targets,
    )
}

fn plan_candidates_in_scope(
    s: &EntitySnapshot,
    learner: u64,
    course: u64,
    at: DateTime<Utc>,
    minimum_fresh: usize,
    exclude_practiced: bool,
    selection: StudyScope,
) -> Result<Vec<PlannedActivity>> {
    let mut scope = BTreeSet::new();
    if selection == StudyScope::Queue {
        for topic in s.refs(learner, "learner/queue")? {
            if !s.entity(topic)?.contains_key("topic/id") {
                return Err("learner/queue must reference topics".into());
            }
            scope.insert(topic);
        }
    } else {
        for unit in s.refs(course, "course/units")? {
            for module in s.refs(unit, "unit/modules")? {
                scope.extend(s.refs(module, "module/topics")?);
            }
        }
    }
    let mut practiced = BTreeSet::new();
    let mut ready = BTreeSet::new();
    let mut repetitions = BTreeMap::new();
    let thresholds: Vec<_> = s
        .entities
        .values()
        .filter(|r| r.contains_key("policy/id"))
        .filter_map(|r| r.get("policy/review-threshold").and_then(Value::as_f64))
        .collect();
    let threshold = if thresholds.len() == 1 {
        Some(thresholds[0])
    } else {
        None
    };
    let now = timestamp_days(at);
    for progress in s.refs(learner, "learner/knowledge-profile")? {
        let topic = s.reference(progress, "progress/topic")?;
        let r = s.entity(progress)?;
        let reps = r
            .get("progress/repetitions")
            .and_then(Value::as_f64)
            .unwrap_or(0.0);
        if !reps.is_finite() || reps < 0.0 {
            return Err("invalid imported repetition position".into());
        }
        repetitions.insert(topic, reps);
        if selection == StudyScope::Queue {
            continue;
        }
        // A complete local state explicitly records whether learning has been
        // established. Partial historical records may only report repetitions.
        if r.get("progress/learned")
            .and_then(Value::as_bool)
            .unwrap_or(false)
            || reps > 0.0
        {
            practiced.insert(topic);
        }
        if COMPLETE_PROGRESS.iter().all(|key| r.contains_key(*key)) {
            if r.get("progress/learned") == Some(&json!(true)) {
                let threshold =
                    threshold.ok_or("operational readiness needs one configured FIRe policy")?;
                let memory = r["progress/memory"].as_f64().ok_or("invalid retention")?;
                let interval = r["progress/interval-days"]
                    .as_f64()
                    .ok_or("invalid interval")?;
                let observed = crate::schema::instant_days(&r["progress/memory-at"])?;
                if !memory.is_finite() || memory < 0.0 || !interval.is_finite() || interval <= 0.0 {
                    return Err("invalid operational retention state".into());
                }
                if now >= observed
                    && memory * 2.0_f64.powf(-(now - observed) / interval) > threshold
                {
                    ready.insert(topic);
                }
            }
        } else if reps > 0.0 {
            ready.insert(topic);
        }
    }
    let mut prerequisites: BTreeMap<u64, BTreeSet<u64>> = BTreeMap::new();
    for (&topic, r) in &s.entities {
        if r.contains_key("topic/id") {
            for next in s.refs(topic, "topic/next")? {
                prerequisites.entry(next).or_default().insert(topic);
            }
            for kp in s.refs(topic, "topic/knowledge-points")? {
                prerequisites
                    .entry(topic)
                    .or_default()
                    .extend(s.refs(kp, "knowledge-point/key-prerequisites")?);
            }
        }
    }
    let support = if selection == StudyScope::Targets {
        target_support(s, learner, &prerequisites, &ready)?
    } else {
        BTreeMap::new()
    };
    scope.extend(support.keys().copied());
    let seen = seen_questions(s, learner)?;
    let mut finished = BTreeSet::new();
    let mut active = BTreeSet::new();
    for task in s.refs(learner, "learner/activity")? {
        let status = ident(s, task, "learner-task/status")?;
        if status == "learner-task.status/completed" {
            finished.insert(s.reference(task, "learner-task/activity")?);
        } else if matches!(
            status.as_str(),
            "learner-task.status/started" | "learner-task.status/paused"
        ) {
            active.insert(s.reference(task, "learner-task/activity")?);
        }
    }
    let mut result = vec![];
    for (&activity, r) in &s.entities {
        if !r.contains_key("activity/id")
            || ident(s, activity, "activity/type")? != "activity.type/lesson"
            || finished.contains(&activity)
        {
            continue;
        }
        let Some(topic) = s.optional_ref(activity, "activity/scope")? else {
            continue;
        };
        if active.contains(&activity) {
            if (selection != StudyScope::Queue || scope.contains(&topic))
                && lesson_steps(s, activity).is_ok()
            {
                result.push((activity, topic));
            }
            continue;
        }
        if !scope.contains(&topic) {
            continue;
        }
        if (exclude_practiced && practiced.contains(&topic))
            || (selection != StudyScope::Queue
                && prerequisites
                    .get(&topic)
                    .is_some_and(|required| !required.is_subset(&ready)))
        {
            continue;
        }
        let Ok(steps) = lesson_steps(s, activity) else {
            continue;
        };
        if !steps
            .iter()
            .any(|v| v.kind == "knowledge-point" || v.kind == "question")
        {
            continue;
        }
        if steps.iter().any(|step| match step.kind.as_str() {
            "knowledge-point" => {
                step.questions
                    .iter()
                    .filter(|q| !seen.contains(q) && validate_question(s, **q).is_ok())
                    .count()
                    < minimum_fresh
            }
            "question" => {
                seen.contains(&step.content) || validate_question(s, step.content).is_err()
            }
            _ => false,
        }) {
            continue;
        }
        result.push((activity, topic));
    }
    let mut result: Vec<_> = result
        .into_iter()
        .map(|(activity, topic)| {
            let target = support.get(&topic);
            let target_topics: Vec<_> = target
                .map(|t| t.targets.iter().copied().collect())
                .unwrap_or_default();
            let target_count = target_topics.len();
            let remaining_topics = target.and_then(|t| t.remaining).unwrap_or(0);
            let nearest_target_steps = target.and_then(|t| t.distance);
            let due = target.and_then(|t| t.due);
            // Bounded, inspectable score: 0..1000 for distinct target reach,
            // 0..100 each for remaining work and graph proximity, 0..250 for
            // deadline urgency (overdue is capped), and <=1 for course ordering.
            // Ongoing work adds 10000, so it always precedes new lessons.
            let mut priority = 1.0 / (1.0 + repetitions.get(&topic).copied().unwrap_or(0.0));
            if target_count > 0 {
                priority += 1000.0 * target_count as f64 / (1.0 + target_count as f64)
                    + 100.0 / (1.0 + remaining_topics as f64)
                    + 100.0 / (1.0 + nearest_target_steps.unwrap_or(0) as f64);
            }
            if let Some(due) = due {
                // Whole hours avoid a priority write on every queue refresh.
                let days = (due - at).num_hours().max(0) as f64 / 24.0;
                priority += 250.0 / (1.0 + days);
            }
            let mut reason = if active.contains(&activity) {
                priority += 10000.0;
                "Continue your lesson".into()
            } else if target_count > 1 {
                format!("Supports {target_count} study targets")
            } else if nearest_target_steps == Some(0) {
                "One of your study targets".into()
            } else if target_count == 1 {
                "Prerequisite for a study target".into()
            } else {
                "Ready for your course".into()
            };
            if let Some(due) = due {
                reason.push_str(&format!(". Assignment due {}", due.format("%b %-d, %Y")));
            }
            PlannedActivity {
                activity,
                topic,
                priority,
                target_count,
                target_topics,
                remaining_topics,
                nearest_target_steps,
                due,
                reason,
            }
        })
        .collect();
    result.sort_by(|a, b| {
        b.priority
            .total_cmp(&a.priority)
            .then_with(|| a.topic.cmp(&b.topic))
            .then_with(|| a.activity.cmp(&b.activity))
    });
    Ok(result)
}

/// Read-only serving diagnostics, including ready lessons whose captured banks
/// cannot support the full adaptive practice allowance.
pub fn candidate_diagnostics(s: &EntitySnapshot, learner: u64, course: u64) -> Result<Value> {
    let mut counts = vec![];
    for minimum_fresh in [2, 5] {
        for exclude_practiced in [false, true] {
            let ids = candidates_with_supply(s, learner, course, minimum_fresh, exclude_practiced)?;
            counts.push(json!({"minimum_fresh":minimum_fresh,"exclude_practiced":exclude_practiced,"count":ids.len(),"activities":ids}));
        }
    }
    let seen = seen_questions(s, learner)?;
    let mut ready_unlearned = vec![];
    for activity in candidates_with_supply(s, learner, course, 0, true)? {
        let mut kps = vec![];
        for step in lesson_steps(s, activity)? {
            if step.kind == "knowledge-point" {
                let valid = step
                    .questions
                    .iter()
                    .filter(|q| !seen.contains(q) && validate_question(s, **q).is_ok())
                    .count();
                kps.push(
                    json!({"kp":step.content,"captured":step.questions.len(),"valid_fresh":valid}),
                );
            }
        }
        ready_unlearned.push(json!({"activity":activity,"topic":s.reference(activity,"activity/scope")?,"title":s.entity(activity)?.get("activity/title"),"kps":kps}));
    }
    Ok(json!({"counts":counts,"ready_unlearned":ready_unlearned}))
}

/// All fields must be present exactly once. Choice fields contain the selected
/// answer's decimal entity ID; blanks contain verbatim entered text. References
/// distinguish choices even when their visible values happen to be identical.
pub fn grade(s: &EntitySnapshot, question: u64, responses: &BTreeMap<u64, String>) -> Result<bool> {
    validate_question(s, question)?;
    let fields: BTreeSet<_> = s
        .refs(question, "question/answer-fields")?
        .into_iter()
        .collect();
    if fields != responses.keys().copied().collect() {
        return Err("answer every field of the current question".into());
    }
    let mut correct = true;
    for field in fields {
        let submitted = &responses[&field];
        if submitted.trim().is_empty() {
            return Err("answer every field before submitting".into());
        }
        if submitted.len() > 4096 {
            return Err("answer exceeds 4096 bytes".into());
        }
        let expected = s.reference(field, "answer-field/correct")?;
        let canonical = s.entity(expected)?["answer/value"].as_str().unwrap();
        let field_kind = ident(s, field, "answer-field/type")?;
        if field_kind != "answer-field.type/blank" {
            let selected: u64 = submitted
                .parse()
                .map_err(|_| "selected answer must identify an authored choice")?;
            if !s.refs(field, "answer-field/choices")?.contains(&selected) {
                return Err("selected answer does not belong to this field".into());
            }
            correct &= selected == expected;
        } else {
            correct &= match ident(s, expected, "answer/type")?.as_str() {
                "answer.type/math" => {
                    // Form-sensitive prompts must match their authored answer
                    // representation. Numeric equivalence alone cannot verify
                    // rounding, significant figures, or reduced-form work.
                    let prompt = s.entity(question)?["question/problem"]
                        .as_str()
                        .unwrap()
                        .to_lowercase();
                    let form_sensitive = [
                        "round",
                        "decimal place",
                        "significant figure",
                        "significant digit",
                        "simplest form",
                        "lowest terms",
                        "reduced fraction",
                    ]
                    .iter()
                    .any(|term| prompt.contains(term));
                    if form_sensitive {
                        normalize_math(submitted) == normalize_math(canonical)
                    } else {
                        equivalent_math(submitted, canonical)
                    }
                }
                "answer.type/text" => {
                    submitted
                        .split_whitespace()
                        .collect::<Vec<_>>()
                        .join(" ")
                        .to_lowercase()
                        == canonical
                            .split_whitespace()
                            .collect::<Vec<_>>()
                            .join(" ")
                            .to_lowercase()
                }
                _ => submitted == canonical,
            };
        }
    }
    Ok(correct)
}

/// Final lesson XP uses the shared whole-task accuracy rule, including failures.
/// Unfinished work has no award. Tutorials/examples are never answer evidence.
pub fn lesson_xp(s: &EntitySnapshot, activity: u64, items: &[u64], base: i64) -> Result<i64> {
    if base < 0 {
        return Err("base XP must be nonnegative".into());
    }
    if position(s, activity, items)?.next.is_some() {
        return Ok(0);
    }
    completed_lesson_xp(s, items, base)
}
fn completed_lesson_xp(s: &EntitySnapshot, items: &[u64], base: i64) -> Result<i64> {
    if base < 0 {
        return Err("base XP must be nonnegative".into());
    }
    let mut outcomes = vec![];
    for item in items {
        let content = s.reference(*item, "task-item/content")?;
        if s.is_ordinary_question(content)? {
            outcomes.push(
                question_outcome(s, *item)?.ok_or("XP requires completed question outcomes")?,
            );
        }
    }
    if outcomes.is_empty() {
        return Ok(0);
    }
    lesson_xp_candidate(base, &outcomes, None)?
        .to_i64()
        .ok_or_else(|| "XP outside supported range".into())
}

fn normalize_math(value: &str) -> String {
    let mut text = value
        .trim()
        .trim_matches('$')
        .replace("\\(", "")
        .replace("\\)", "")
        .replace("\\[", "")
        .replace("\\]", "")
        .replace('−', "-")
        .replace('×', "*")
        .replace('÷', "/")
        .replace("\\left", "")
        .replace("\\right", "")
        .replace("\\dfrac", "\\frac")
        .replace("\\tfrac", "\\frac")
        .replace("\\cdot", "*")
        .replace("\\times", "*")
        .replace("\\div", "/")
        .replace("\\,", "")
        .replace("\\;", "")
        .replace("\\!", "")
        .replace("\\ ", "");
    text.retain(|c| !c.is_whitespace());
    text
}

/// Conservative mathematical equivalence: exact rational arithmetic plus
/// formatting normalization. It never evaluates executable code or uses a float
/// tolerance that could accept a wrong high-precision answer. General symbolic
/// identities are deliberately not guessed.
pub fn equivalent_math(a: &str, b: &str) -> bool {
    let a = normalize_math(a);
    let b = normalize_math(b);
    if a.is_empty() || b.is_empty() {
        return false;
    }
    if a == b {
        return true;
    }
    match (RationalParser::parse(&a), RationalParser::parse(&b)) {
        (Some(a), Some(b)) => a == b,
        _ => false,
    }
}

struct RationalParser<'a> {
    input: &'a [u8],
    index: usize,
    depth: usize,
}
impl<'a> RationalParser<'a> {
    fn parse(input: &'a str) -> Option<BigRational> {
        if input.len() > 4096 {
            return None;
        }
        let mut parser = Self {
            input: input.as_bytes(),
            index: 0,
            depth: 0,
        };
        let result = parser.sum()?;
        (parser.index == parser.input.len()).then_some(result)
    }
    fn take(&mut self, c: u8) -> bool {
        if self.input.get(self.index) == Some(&c) {
            self.index += 1;
            true
        } else {
            false
        }
    }
    fn sum(&mut self) -> Option<BigRational> {
        let mut value = self.product()?;
        loop {
            if self.take(b'+') {
                value += self.product()?;
            } else if self.take(b'-') {
                value -= self.product()?;
            } else {
                return Some(value);
            }
        }
    }
    fn product(&mut self) -> Option<BigRational> {
        let mut value = self.signed()?;
        loop {
            if self.take(b'*') {
                value *= self.signed()?;
            } else if self.take(b'/') {
                let denominator = self.signed()?;
                if denominator.is_zero() {
                    return None;
                }
                value /= denominator;
            } else {
                return Some(value);
            }
        }
    }
    fn signed(&mut self) -> Option<BigRational> {
        let mut negative = false;
        while matches!(self.input.get(self.index), Some(b'+') | Some(b'-')) {
            if self.take(b'-') {
                negative = !negative;
            } else {
                self.index += 1;
            }
        }
        let value = self.power()?;
        Some(if negative { -value } else { value })
    }
    fn power(&mut self) -> Option<BigRational> {
        if self.depth >= 64 {
            return None;
        }
        let mut value = self.atom()?;
        if self.take(b'^') {
            self.depth += 1;
            let exponent = self.signed()?;
            self.depth -= 1;
            if !exponent.is_integer() {
                return None;
            }
            let exponent: i32 = exponent.to_integer().try_into().ok()?;
            if exponent.unsigned_abs() > 64
                || (value.is_zero() && exponent <= 0)
                || value.numer().bits().max(value.denom().bits())
                    * u64::from(exponent.unsigned_abs())
                    > 16_384
            {
                return None;
            }
            value = value.pow(exponent);
        }
        if self.take(b'%') {
            value /= BigRational::from_integer(100.into());
        }
        Some(value)
    }
    fn atom(&mut self) -> Option<BigRational> {
        if self.depth >= 64 {
            return None;
        }
        if self.input[self.index..].starts_with(b"\\frac") {
            self.index += 5;
            self.depth += 1;
            let numerator = self.atom()?;
            let denominator = self.atom()?;
            self.depth -= 1;
            if denominator.is_zero() {
                return None;
            }
            return Some(numerator / denominator);
        }
        for (open, close) in [(b'(', b')'), (b'{', b'}')] {
            if self.take(open) {
                self.depth += 1;
                let value = self.sum()?;
                self.depth -= 1;
                return self.take(close).then_some(value);
            }
        }
        let start = self.index;
        while self
            .input
            .get(self.index)
            .is_some_and(|c| c.is_ascii_digit() || *c == b'.')
        {
            self.index += 1;
        }
        if self.index == start || self.index - start > 256 {
            return None;
        }
        if matches!(self.input.get(self.index), Some(b'e') | Some(b'E')) {
            self.index += 1;
            let exp_start = self.index;
            if matches!(self.input.get(self.index), Some(b'+') | Some(b'-')) {
                self.index += 1;
            }
            while self.input.get(self.index).is_some_and(u8::is_ascii_digit) {
                self.index += 1;
            }
            let exponent: i32 = std::str::from_utf8(&self.input[exp_start..self.index])
                .ok()?
                .parse()
                .ok()?;
            if exponent.unsigned_abs() > 64 {
                return None;
            }
        }
        decimal_number(std::str::from_utf8(&self.input[start..self.index]).ok()?).ok()
    }
}

const COMPLETE_PROGRESS: &[&str] = &[
    "progress/policy",
    "progress/repetitions",
    "progress/memory",
    "progress/memory-at",
    "progress/interval-days",
    "progress/learned",
    "progress/assessment-accuracy",
    "progress/practice-accuracy",
    "progress/assessment-mass",
    "progress/practice-mass",
];

fn learning_runtime(s: &EntitySnapshot, learner: u64, at: DateTime<Utc>) -> Result<LoadedRuntime> {
    let policies: Vec<_> = s
        .entities
        .iter()
        .filter(|(_, r)| r.contains_key("policy/id"))
        .map(|(eid, _)| *eid)
        .collect();
    if policies.len() != 1 {
        return Err("learning requires exactly one explicitly configured FIRe policy".into());
    }
    let all_progress = s.refs(learner, "learner/knowledge-profile")?;
    let complete: Vec<_> = all_progress
        .iter()
        .copied()
        .filter(|p| {
            COMPLETE_PROGRESS
                .iter()
                .all(|key| s.entities[p].contains_key(*key))
        })
        .collect();
    // FIRe needs the curriculum graph and learner state, not question prose,
    // every answer value or every image. Keep all owners for the relationships
    // load_runtime validates, while avoiding two clones of the whole catalog
    // for each submitted answer.
    let runtime_prefixes = [
        "topic/",
        "module/",
        "knowledge-point/",
        "encompassing/",
        "learner/",
        "progress/",
        "performance/",
        "policy/",
        "question-weights/",
        "learner-task/",
        "task-item/",
    ];
    let entities = s
        .entities
        .iter()
        .filter(|(_, record)| {
            record.contains_key("db/ident")
                || record.keys().any(|key| {
                    runtime_prefixes
                        .iter()
                        .any(|prefix| key.starts_with(prefix))
                })
        })
        .map(|(eid, record)| (*eid, record.clone()))
        .collect();
    let mut captured = EntitySnapshot::new(entities, s.basis_t)?;
    captured.status_history = s.status_history.clone();
    captured
        .entities
        .get_mut(&learner)
        .ok_or("unknown learner")?
        .insert("learner/knowledge-profile".into(), json!(complete));
    let mut loaded = load_runtime(captured, learner, policies[0])?;
    loaded
        .snapshot
        .entities
        .get_mut(&learner)
        .unwrap()
        .insert("learner/knowledge-profile".into(), json!(all_progress));
    let mut progress_owners: BTreeMap<u64, Vec<u64>> = BTreeMap::new();
    for (&owner, record) in &s.entities {
        if record.contains_key("learner/knowledge-profile") {
            for progress in s.refs(owner, "learner/knowledge-profile")? {
                progress_owners.entry(progress).or_default().push(owner);
            }
        }
    }
    for p in all_progress {
        if progress_owners.get(&p) != Some(&vec![learner]) {
            return Err("progress needs exactly one learner owner".into());
        }
        let topic_eid = s.reference(p, "progress/topic")?;
        let topic = loaded
            .topic_eid_to_id
            .get(&topic_eid)
            .ok_or("unknown progress topic")?
            .clone();
        if !complete.contains(&p) {
            if loaded.progress_by_topic.insert(topic.clone(), p).is_some() {
                return Err("duplicate learner-topic progress".into());
            }
            let record = s.entity(p)?;
            // Import only observed repetitions. Initialize a local observation
            // anchor now with zero retention and zero answer evidence; do not
            // infer past timestamps, accuracy, or mastery from graph colors.
            let reps = record
                .get("progress/repetitions")
                .and_then(Value::as_f64)
                .unwrap_or(0.0);
            if !reps.is_finite() || reps < 0.0 {
                return Err("invalid imported repetitions".into());
            }
            let mut state = loaded.engine.initial_state(&loaded.learner, &topic, false);
            state.repetitions = reps;
            state.memory = 0.0;
            state.memory_at = timestamp_days(at);
            state.interval_days = loaded.engine.policy.interval(reps)?;
            loaded.engine.seed(&loaded.learner, &topic, state)?;
        }
    }
    Ok(loaded)
}

/// Native EDN forms to include in the same guarded transaction as the answer or
/// task completion. Accuracy uses observed answers once; retention uses a single
/// terminal lesson outcome. Successful first local learning establishes a current
/// retention anchor while retaining imported repetition credit. Only changed
/// states are written, so untouched partial imports remain partial.
pub fn credit(
    s: &EntitySnapshot,
    learner: u64,
    activity: u64,
    question: Option<u64>,
    correct: bool,
    completed: bool,
    event_id: &str,
    at: DateTime<Utc>,
) -> Result<Vec<Value>> {
    if question.is_none() && !completed {
        return Ok(vec![]);
    }
    if ident(s, activity, "activity/type")? != "activity.type/lesson" {
        return Err("learning credit requires a lesson".into());
    }
    let loaded = learning_runtime(s, learner, at)?;
    let topic_eid = s.reference(activity, "activity/scope")?;
    let topic = loaded
        .topic_eid_to_id
        .get(&topic_eid)
        .ok_or("lesson scope must be a topic")?;
    let mut engine = loaded.engine.clone();
    if let Some(question) = question {
        validate_question(s, question)?;
        if s.topic_for_question(question)? != topic_eid {
            return Err("question does not belong to the lesson topic".into());
        }
        engine.apply_accuracy(Event {
            id: format!("answer:{event_id}"),
            learner: loaded.learner.clone(),
            topic: topic.clone(),
            at: timestamp_days(at),
            passed: correct,
            kind: "lesson".into(),
            ..Event::default()
        })?;
    }
    if completed {
        let before = engine
            .states
            .get(&loaded.learner)
            .and_then(|states| states.get(topic));
        let banked = before
            .filter(|state| !state.learned)
            .map(|state| state.repetitions)
            .unwrap_or(0.0);
        engine.apply_retention(Event {
            id: format!("lesson:{event_id}"),
            learner: loaded.learner.clone(),
            topic: topic.clone(),
            at: timestamp_days(at),
            passed: correct,
            learned: correct,
            kind: "lesson".into(),
            ..Event::default()
        })?;
        if correct && banked > 0.0 {
            let state = engine
                .states
                .get_mut(&loaded.learner)
                .unwrap()
                .get_mut(topic)
                .unwrap();
            state.repetitions += banked;
            state.interval_days = engine.policy.interval(state.repetitions)?;
        }
    }
    let mut forms = writeback(&loaded, &engine, vec![], "learning", event_id, at)?.forms;
    forms.retain(|v| v.get("db/id") != Some(&json!("edb.tx")));
    Ok(forms)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::Policy;

    fn id(n: u64) -> String {
        format!("00000000-0000-0000-0000-{n:012}")
    }
    fn put(entities: &mut BTreeMap<u64, serde_json::Map<String, Value>>, eid: u64, value: Value) {
        entities.insert(eid, value.as_object().unwrap().clone());
    }
    fn fixture() -> EntitySnapshot {
        let mut entities = BTreeMap::new();
        for (i, name) in [
            "activity.type/lesson",
            "answer-field.type/radio",
            "answer-field.type/select",
            "answer-field.type/blank",
            "answer.type/math",
            "answer.type/text",
            "answer.type/image",
            "task-item.status/started",
            "task-item.status/paused",
            "task-item.status/completed",
            "task-item.status/correct",
            "task-item.status/incorrect",
            "task-item.status/skipped",
            "learner-task.status/started",
            "learner-task.status/paused",
            "learner-task.status/completed",
            "learner-task.status/failed",
            "policy.retention-update/decay-before-add",
            "activity.type/assignment",
        ]
        .iter()
        .enumerate()
        {
            put(&mut entities, 1000 + i as u64, json!({"db/ident":name}));
        }
        put(
            &mut entities,
            1,
            json!({"learner/id":"test-learner", "learner/activity":[], "learner/knowledge-profile":[21,22], "learner/course":5}),
        );
        let defaults = serde_json::to_value(Policy::default()).unwrap();
        let mut policy = json!({"policy/id":id(2),"policy/retention-update-order":"policy.retention-update/decay-before-add"}).as_object().unwrap().clone();
        for (attr, field) in [
            ("base-half-life-days", "base_interval_days"),
            ("interval-growth", "interval_growth"),
            ("maximum-half-life-days", "maximum_interval_days"),
            ("review-threshold", "due_threshold"),
            ("initial-retention", "restored_memory"),
            ("early-practice-discount-power", "discount_power"),
            ("initial-accuracy", "prior_accuracy"),
            ("accuracy-update-rate", "accuracy_alpha"),
            ("speed-exponent", "speed_exponent"),
            ("minimum-speed", "minimum_speed"),
            ("maximum-speed", "maximum_speed"),
            ("overdue-failure-slope", "failure_overdue_slope"),
            ("maximum-failure-multiplier", "maximum_failure_multiplier"),
            ("gate-slow-implicit", "gate_slow_implicit"),
            ("future-horizon-days", "future_horizon_days"),
        ] {
            policy.insert(format!("policy/{attr}"), defaults[field].clone());
        }
        entities.insert(2, policy);
        put(
            &mut entities,
            3,
            json!({"topic/id":id(3),"topic/knowledge-points":[41]}),
        );
        put(&mut entities, 4, json!({"topic/id":id(4),"topic/next":[3]}));
        put(
            &mut entities,
            5,
            json!({"course/id":id(5),"course/units":[6]}),
        );
        put(
            &mut entities,
            6,
            json!({"unit/id":id(6),"unit/modules":[7]}),
        );
        put(
            &mut entities,
            7,
            json!({"module/id":id(7),"module/topics":[3]}),
        );
        put(
            &mut entities,
            9,
            json!({"learner-task/id":id(9),"learner-task/status":"learner-task.status/started","learner-task/activity":20,"learner-task/items":[]}),
        );
        put(
            &mut entities,
            20,
            json!({"activity/id":id(20),"activity/type":"activity.type/lesson","activity/scope":3,"activity/steps":[31,30],"activity/first-step":30}),
        );
        put(
            &mut entities,
            21,
            json!({"progress/id":"imported-main","progress/topic":3,"progress/repetitions":7.0}),
        );
        put(
            &mut entities,
            22,
            json!({"progress/id":"imported-prerequisite","progress/topic":4,"progress/repetitions":1.0}),
        );
        put(
            &mut entities,
            30,
            json!({"step/id":id(30),"step/content":40,"step/next":31}),
        );
        put(
            &mut entities,
            31,
            json!({"step/id":id(31),"step/content":41}),
        );
        put(
            &mut entities,
            40,
            json!({"tutorial/id":id(40),"tutorial/content":"Multiply both sides by $2$."}),
        );
        put(
            &mut entities,
            41,
            json!({"knowledge-point/id":id(41),"knowledge-point/canonical-example":42,"knowledge-point/questions":[100,101,102,103,104]}),
        );
        put(
            &mut entities,
            42,
            json!({"question/id":id(42),"question/problem":"$2x=1$","question/worked-solution":"$x=1/2$"}),
        );
        for n in 0..5 {
            put(
                &mut entities,
                100 + n,
                json!({"question/id":id(100+n),"question/problem":"$2x=1$","question/answer-fields":[200+n]}),
            );
            put(
                &mut entities,
                200 + n,
                json!({"answer-field/id":id(200+n),"answer-field/key":"x","answer-field/type":"answer-field.type/blank","answer-field/choices":[300+n],"answer-field/correct":300+n}),
            );
            put(
                &mut entities,
                300 + n,
                json!({"answer/id":id(300+n),"answer/type":"answer.type/math","answer/value":"\\frac{1}{2}"}),
            );
        }
        EntitySnapshot::new(entities, 1).unwrap()
    }
    fn present(s: &mut EntitySnapshot, content: u64, status: &str) -> u64 {
        let items = s.refs(9, "learner-task/items").unwrap();
        let item = 500 + items.len() as u64;
        put(
            &mut s.entities,
            item,
            json!({"task-item/id":id(item),"task-item/content":content,"task-item/status":format!("task-item.status/{status}")}),
        );
        let mut next = items;
        if let Some(last) = next.last() {
            s.entities
                .get_mut(last)
                .unwrap()
                .insert("task-item/next".into(), json!(item));
        }
        next.push(item);
        s.entities
            .get_mut(&9)
            .unwrap()
            .insert("learner-task/items".into(), json!(next));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([9]));
        item
    }
    fn items(s: &EntitySnapshot) -> Vec<u64> {
        s.refs(9, "learner-task/items").unwrap()
    }

    fn planning_fixture(targets: &[u64]) -> EntitySnapshot {
        let mut s = fixture();
        s.entities
            .get_mut(&21)
            .unwrap()
            .insert("progress/repetitions".into(), json!(0.0));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(true));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/targets".into(), json!(targets));
        s
    }

    fn planning_lesson(s: &mut EntitySnapshot, topic: u64, next: &[u64]) -> u64 {
        let activity = 10000 + topic;
        let question = 20000 + topic;
        let step = 30000 + topic;
        put(
            &mut s.entities,
            topic,
            json!({"topic/id":id(topic), "topic/next":next}),
        );
        put(
            &mut s.entities,
            activity,
            json!({"activity/id":id(activity),"activity/type":"activity.type/lesson","activity/scope":topic,"activity/steps":[step],"activity/first-step":step}),
        );
        put(
            &mut s.entities,
            step,
            json!({"step/id":id(step),"step/content":question}),
        );
        put(
            &mut s.entities,
            question,
            json!({"question/id":id(question),"question/problem":"$2x=1$","question/answer-fields":[200]}),
        );
        activity
    }

    fn planning_time() -> DateTime<Utc> {
        DateTime::from_timestamp_millis(1_790_760_000_000).unwrap()
    }

    #[test]
    fn global_queue_layers_use_longest_topic_next_paths_and_reject_cycles() {
        let mut s = planning_fixture(&[]);
        planning_lesson(&mut s, 80, &[81, 83]);
        planning_lesson(&mut s, 81, &[82]);
        planning_lesson(&mut s, 82, &[83]);
        planning_lesson(&mut s, 83, &[]);
        let layers = topic_layers(&s).unwrap();
        assert_eq!(
            [layers[&80], layers[&81], layers[&82], layers[&83]],
            [0, 1, 2, 3]
        );
        // No learner state, course filter, or selected target changes graph ranks.
        assert_eq!(layers[&4], 0);
        assert_eq!(layers[&3], 1);
        s.entities
            .get_mut(&83)
            .unwrap()
            .insert("topic/next".into(), json!([80]));
        assert!(topic_layers(&s).unwrap_err().contains("cycle"));
    }

    #[test]
    fn self_directed_queue_orders_global_layer_then_priority_and_resumes_first() {
        let mut s = planning_fixture(&[]);
        let foundation = planning_lesson(&mut s, 80, &[82]);
        let practiced_root = planning_lesson(&mut s, 81, &[]);
        let later = planning_lesson(&mut s, 82, &[]);
        // A prerequisite outside the queue still contributes to the global rank.
        planning_lesson(&mut s, 83, &[80]);
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/queue".into(), json!([82, 80, 81]));
        put(
            &mut s.entities,
            600,
            json!({"progress/topic":81,"progress/repetitions":3.0}),
        );
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/knowledge-profile".into(), json!([600]));
        let ids = |s: &EntitySnapshot| {
            study_candidates(s, 1, 5, planning_time())
                .unwrap()
                .iter()
                .map(|p| p.activity)
                .collect::<Vec<_>>()
        };
        // The practiced root outranks practiced_root later layers despite its lower score.
        assert_eq!(ids(&s), [practiced_root, foundation, later]);
        s.entities
            .get_mut(&83)
            .unwrap()
            .insert("topic/next".into(), json!([]));
        assert_eq!(ids(&s), [foundation, practiced_root, later]);
        put(
            &mut s.entities,
            601,
            json!({"learner-task/activity":later,"learner-task/status":"learner-task.status/paused"}),
        );
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([601]));
        assert_eq!(ids(&s), [later, foundation, practiced_root]);
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(false));
        assert_eq!(
            queue_candidates(&s, 1, 5, planning_time()).unwrap()[0].activity,
            later
        );
    }

    #[test]
    fn study_queue_is_explicit_cross_course_and_does_not_fall_back() {
        let mut s = planning_fixture(&[90]);
        let queued = planning_lesson(&mut s, 80, &[]);
        planning_lesson(&mut s, 81, &[80]); // Unlearned prerequisite.
        planning_lesson(&mut s, 90, &[]); // Long-term target is not queued.
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/queue".into(), json!([80]));
        let plan = study_candidates(&s, 1, 5, planning_time()).unwrap();
        assert_eq!(
            plan.iter().map(|p| p.activity).collect::<Vec<_>>(),
            [queued]
        );
        assert_eq!(plan[0].reason, "Selected for your queue");
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/queue".into(), json!([]));
        assert!(
            study_candidates(&s, 1, 5, planning_time())
                .unwrap()
                .is_empty()
        );
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([9]));
        assert!(
            study_candidates(&s, 1, 5, planning_time())
                .unwrap()
                .is_empty()
        );
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/queue".into(), json!([3]));
        assert_eq!(
            study_candidates(&s, 1, 5, planning_time()).unwrap()[0].activity,
            20
        );
        assert_eq!(
            study_candidates(&s, 1, 5, planning_time()).unwrap()[0].reason,
            "Continue your lesson"
        );
    }

    #[test]
    fn study_queue_keeps_content_checks_and_rejects_non_topic_refs() {
        let mut s = planning_fixture(&[]);
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/queue".into(), json!([3]));
        s.entities
            .get_mut(&41)
            .unwrap()
            .insert("knowledge-point/questions".into(), json!([100]));
        assert!(
            study_candidates(&s, 1, 5, planning_time())
                .unwrap()
                .is_empty()
        );
        let lesson = planning_lesson(&mut s, 80, &[]);
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/queue".into(), json!([80]));
        s.entities
            .get_mut(&(20000 + 80))
            .unwrap()
            .remove("question/answer-fields");
        assert!(
            study_candidates(&s, 1, 5, planning_time())
                .unwrap()
                .is_empty()
        );
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/queue".into(), json!([lesson]));
        assert!(
            study_candidates(&s, 1, 5, planning_time())
                .unwrap_err()
                .contains("must reference topics")
        );
    }

    #[test]
    fn study_engine_interleaves_modules_and_ignores_queue_and_targets() {
        let mut s = planning_fixture(&[90]);
        let a = planning_lesson(&mut s, 80, &[]);
        let b = planning_lesson(&mut s, 81, &[]);
        let c = planning_lesson(&mut s, 82, &[]);
        let d = planning_lesson(&mut s, 83, &[]);
        planning_lesson(&mut s, 90, &[]);
        planning_lesson(&mut s, 91, &[83]); // Blocks d in engine mode.
        s.entities
            .get_mut(&7)
            .unwrap()
            .insert("module/topics".into(), json!([80, 81]));
        put(
            &mut s.entities,
            8,
            json!({"module/id":id(8),"module/topics":[82,83]}),
        );
        s.entities
            .get_mut(&6)
            .unwrap()
            .insert("unit/modules".into(), json!([8, 7]));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/queue".into(), json!([90]));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(false));
        let ids = |s: &EntitySnapshot| {
            study_candidates(s, 1, 5, planning_time())
                .unwrap()
                .iter()
                .map(|p| p.activity)
                .collect::<Vec<_>>()
        };
        assert_eq!(ids(&s), [a, c, b]);
        s.entities
            .get_mut(&91)
            .unwrap()
            .insert("topic/next".into(), json!([]));
        assert_eq!(ids(&s), [a, c, b, d]);
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([9]));
        assert_eq!(ids(&s), [20, a, c, b, d]);
        s.entities
            .get_mut(&1)
            .unwrap()
            .remove("learner/self-directed");
        assert_eq!(ids(&s), [20, a, c, b, d]);
    }

    #[test]
    fn planner_counts_distinct_targets_through_diamonds_and_keeps_course_work() {
        let mut s = planning_fixture(&[90, 90, 91, 92]);
        let shared = planning_lesson(&mut s, 80, &[81, 82, 91]);
        planning_lesson(&mut s, 81, &[90]);
        planning_lesson(&mut s, 82, &[90]);
        let single = planning_lesson(&mut s, 83, &[92]);
        for topic in [90, 91, 92] {
            planning_lesson(&mut s, topic, &[]);
        }
        let plan = plan_candidates(&s, 1, 5, planning_time()).unwrap();
        assert_eq!(
            plan.iter().map(|p| p.activity).collect::<Vec<_>>(),
            [shared, single, 20]
        );
        assert_eq!(plan[0].target_topics, [90, 91]);
        assert_eq!(plan[0].target_count, 2);
        assert_eq!(plan[0].nearest_target_steps, Some(1));
        assert_eq!(plan[0].remaining_topics, 2);
        assert_eq!(plan[2].target_count, 0);
        assert!(plan.iter().all(|p| p.priority.is_finite()));
        assert_eq!(
            serde_json::to_value(&plan).unwrap(),
            serde_json::to_value(plan_candidates(&s, 1, 5, planning_time()).unwrap()).unwrap()
        );
    }

    #[test]
    fn planner_gates_cross_course_targets_and_preserves_started_work_after_removal() {
        let mut s = planning_fixture(&[80]);
        let cross_course = planning_lesson(&mut s, 80, &[]);
        let plan = plan_candidates(&s, 1, 5, planning_time()).unwrap();
        assert_eq!(plan[0].activity, cross_course);
        assert_eq!(plan[0].nearest_target_steps, Some(0));
        assert_eq!(plan[0].remaining_topics, 1);
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(false));
        assert_eq!(candidates(&s, 1, 5).unwrap(), [20]);
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(true));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/targets".into(), json!([]));
        assert_eq!(candidates(&s, 1, 5).unwrap(), [20]);
        put(
            &mut s.entities,
            600,
            json!({"learner-task/id":id(600),"learner-task/activity":cross_course,"learner-task/status":"learner-task.status/paused","learner-task/items":[]}),
        );
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([600]));
        let plan = plan_candidates(&s, 1, 5, planning_time()).unwrap();
        assert_eq!(plan[0].activity, cross_course);
        assert_eq!(plan[0].target_count, 0);
        assert!(plan[0].priority >= 10000.0);
    }

    #[test]
    fn planner_uses_nested_assignment_coverage_and_earliest_deadline_without_requiring_work() {
        let at = planning_time();
        let mut s = planning_fixture(&[80, 83]);
        let later = planning_lesson(&mut s, 80, &[]);
        let sooner = planning_lesson(&mut s, 83, &[]);
        put(
            &mut s.entities,
            700,
            json!({"activity/id":id(700),"activity/type":"activity.type/assignment","activity/due":at + chrono::Duration::days(7),"activity/steps":[701]}),
        );
        put(
            &mut s.entities,
            701,
            json!({"step/id":id(701),"step/content":702}),
        );
        put(
            &mut s.entities,
            702,
            json!({"assigned-problem/id":id(702),"assigned-problem/topic-coverage":[80,83],"assigned-problem/content":20080}),
        );
        put(
            &mut s.entities,
            710,
            json!({"activity/id":id(710),"activity/type":"activity.type/assignment","activity/due":at + chrono::Duration::hours(25),"activity/steps":[711]}),
        );
        put(
            &mut s.entities,
            711,
            json!({"step/id":id(711),"step/content":712}),
        );
        put(
            &mut s.entities,
            712,
            json!({"multistep/id":id(712),"multistep/steps":[713]}),
        );
        put(
            &mut s.entities,
            713,
            json!({"step/id":id(713),"step/content":714}),
        );
        put(
            &mut s.entities,
            714,
            json!({"assigned-problem/id":id(714),"assigned-problem/topic-coverage":[83],"assigned-problem/content":715}),
        );
        put(
            &mut s.entities,
            715,
            json!({"multistep/id":id(715),"multistep/steps":[716]}),
        );
        // A containment cycle must neither hang nor count the mapped target twice.
        put(
            &mut s.entities,
            716,
            json!({"step/id":id(716),"step/content":712}),
        );
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/assignments".into(), json!([700, 710]));
        let plan = plan_candidates(&s, 1, 5, at + chrono::Duration::minutes(1)).unwrap();
        assert_eq!(
            plan.iter().map(|p| p.activity).collect::<Vec<_>>(),
            [sooner, later, 20]
        );
        assert_eq!(plan[0].target_count, 1);
        assert_eq!(plan[0].due, Some(at + chrono::Duration::hours(25)));
        assert!(!plan[0].reason.contains("required"));
        assert_eq!(
            plan[0].priority,
            plan_candidates(&s, 1, 5, at + chrono::Duration::minutes(2)).unwrap()[0].priority
        );
        let overdue = plan_candidates(&s, 1, 5, at + chrono::Duration::days(10)).unwrap();
        assert!(overdue.iter().all(|p| p.priority.is_finite()));
        assert_eq!(overdue[0].activity, later); // equal scores use topic IDs
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/targets".into(), json!([]));
        assert_eq!(plan_candidates(&s, 1, 5, at).unwrap()[0].activity, sooner);
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(false));
        assert_eq!(candidates(&s, 1, 5).unwrap(), [20]);
    }

    #[test]
    fn completed_assignments_stop_preparation_but_explicit_targets_and_failed_attempts_remain() {
        let at = planning_time();
        let mut s = planning_fixture(&[80]);
        let lesson = planning_lesson(&mut s, 80, &[]);
        put(
            &mut s.entities,
            700,
            json!({"activity/id":id(700),"activity/type":"activity.type/assignment","activity/due":at - chrono::Duration::days(1),"activity/steps":[701]}),
        );
        put(
            &mut s.entities,
            701,
            json!({"step/id":id(701),"step/content":702}),
        );
        put(
            &mut s.entities,
            702,
            json!({"assigned-problem/id":id(702),"assigned-problem/topic-coverage":[80],"assigned-problem/content":20080}),
        );
        put(
            &mut s.entities,
            600,
            json!({"learner-task/id":id(600),"learner-task/activity":700,"learner-task/status":"learner-task.status/completed","learner-task/items":[]}),
        );
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/assignments".into(), json!([700]));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([600]));

        let plan = plan_candidates(&s, 1, 5, at).unwrap();
        assert_eq!(plan[0].activity, lesson);
        assert_eq!(plan[0].target_count, 1);
        assert_eq!(plan[0].due, None);
        assert_eq!(plan[0].reason, "One of your study targets");

        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/targets".into(), json!([]));
        let plan = plan_candidates(&s, 1, 5, at).unwrap();
        assert_eq!(plan.iter().map(|p| p.activity).collect::<Vec<_>>(), [20]);

        s.entities.get_mut(&600).unwrap().insert(
            "learner-task/status".into(),
            json!("learner-task.status/failed"),
        );
        let plan = plan_candidates(&s, 1, 5, at).unwrap();
        assert_eq!(plan[0].activity, lesson);
        assert_eq!(plan[0].due, Some(at - chrono::Duration::days(1)));
    }

    #[test]
    fn planner_keeps_prerequisite_fire_and_seen_question_guards() {
        let at = planning_time();
        let mut s = planning_fixture(&[81]);
        let prerequisite = planning_lesson(&mut s, 80, &[81]);
        let target = planning_lesson(&mut s, 81, &[]);
        let key_prerequisite = planning_lesson(&mut s, 82, &[]);
        put(
            &mut s.entities,
            900,
            json!({"knowledge-point/id":id(900),"knowledge-point/key-prerequisites":[82]}),
        );
        s.entities
            .get_mut(&81)
            .unwrap()
            .insert("topic/knowledge-points".into(), json!([900]));
        let plan = plan_candidates(&s, 1, 5, at).unwrap();
        assert!(plan.iter().any(|p| p.activity == prerequisite));
        assert!(plan.iter().any(|p| p.activity == key_prerequisite));
        assert!(!plan.iter().any(|p| p.activity == target));
        put(
            &mut s.entities,
            600,
            json!({"learner-task/id":id(600),"learner-task/activity":prerequisite,"learner-task/status":"learner-task.status/failed","learner-task/items":[601]}),
        );
        put(
            &mut s.entities,
            601,
            json!({"task-item/id":id(601),"task-item/content":20080,"task-item/status":"task-item.status/incorrect"}),
        );
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([600]));
        assert!(
            !plan_candidates(&s, 1, 5, at)
                .unwrap()
                .iter()
                .any(|p| p.activity == prerequisite)
        );

        let mut s = planning_fixture(&[3]);
        put(
            &mut s.entities,
            22,
            json!({"progress/id":"known-prerequisite","progress/topic":4,"progress/policy":2,"progress/repetitions":1.0,"progress/learned":true,"progress/memory":1.0,"progress/memory-at":at,"progress/interval-days":1.0,"progress/assessment-accuracy":0.5,"progress/practice-accuracy":0.5,"progress/assessment-mass":0.0,"progress/practice-mass":0.0}),
        );
        assert_eq!(plan_candidates(&s, 1, 5, at).unwrap()[0].activity, 20);
        assert!(
            plan_candidates(&s, 1, 5, at + chrono::Duration::days(10))
                .unwrap()
                .is_empty()
        );
        assert!(
            plan_candidates(&s, 1, 5, at - chrono::Duration::hours(1))
                .unwrap()
                .is_empty()
        );
    }

    #[test]
    fn planner_cycles_remain_locked_and_shorter_remaining_work_ranks_first() {
        let mut s = planning_fixture(&[90, 91, 180]);
        let long = planning_lesson(&mut s, 80, &[81]);
        planning_lesson(&mut s, 81, &[90]);
        planning_lesson(&mut s, 90, &[]);
        let short = planning_lesson(&mut s, 83, &[91]);
        planning_lesson(&mut s, 91, &[]);
        planning_lesson(&mut s, 180, &[181]);
        planning_lesson(&mut s, 181, &[180]);
        let plan = plan_candidates(&s, 1, 5, planning_time()).unwrap();
        assert_eq!(
            plan.iter().map(|p| p.activity).collect::<Vec<_>>(),
            [short, long, 20]
        );
        assert_eq!(plan[0].remaining_topics, 2);
        assert_eq!(plan[1].remaining_topics, 3);
    }

    #[test]
    fn generic_step_order_gates_instruction_and_unanswered_questions() {
        let mut s = fixture();
        assert_eq!(next_content(&s, 20, &[]).unwrap(), Some(40));
        let item = present(&mut s, 40, "started");
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(40));
        assert_eq!(
            continuation(&s, 20, &items(&s), true, 12).unwrap(),
            (Some(42), false, 0)
        );
        assert_eq!(
            ident(&s, item, "task-item/status").unwrap(),
            "task-item.status/started"
        );
        s.entities.get_mut(&item).unwrap().insert(
            "task-item/status".into(),
            json!("task-item.status/completed"),
        );
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(42));
        present(&mut s, 42, "completed");
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(100));
        let question_item = present(&mut s, 100, "started");
        assert!(continuation(&s, 20, &items(&s), true, 12).is_err());
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(100));
        assert!(!lesson_passed(&s, 20, &items(&s)).unwrap());
        s.entities
            .get_mut(&question_item)
            .unwrap()
            .insert("task-item/status".into(), json!("task-item.status/correct"));
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(101));
        present(&mut s, 101, "correct");
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), None);
        assert!(lesson_passed(&s, 20, &items(&s)).unwrap());
        assert_eq!(
            continuation(&s, 20, &items(&s), false, 12).unwrap(),
            (None, true, 15)
        );
    }

    #[test]
    fn configured_selection_switches_phase_and_never_reshuffles_an_active_question() {
        let mut s = fixture();
        for (eid, band) in [(1100, "easy"), (1101, "moderate"), (1102, "hard")] {
            put(
                &mut s.entities,
                eid,
                json!({"db/ident":format!("question.difficulty/{band}")}),
            );
        }
        for (q, difficulty) in [
            (100, 1100),
            (101, 1100),
            (102, 1101),
            (103, 1102),
            (104, 1101),
        ] {
            s.entities
                .get_mut(&q)
                .unwrap()
                .insert("question/difficulty".into(), json!(difficulty));
        }
        put(
            &mut s.entities,
            1200,
            json!({"question-weights/activity-type":"activity.type/lesson",
            "question-weights/initial-easy":1.0,"question-weights/initial-moderate":0.0,"question-weights/initial-hard":0.0,
            "question-weights/remedial-easy":0.0,"question-weights/remedial-moderate":1.0,"question-weights/remedial-hard":0.0}),
        );
        s.entities
            .get_mut(&2)
            .unwrap()
            .insert("policy/question-selection-weights".into(), json!([1200]));
        s = EntitySnapshot::new(s.entities, s.basis_t).unwrap();
        present(&mut s, 40, "completed");
        present(&mut s, 42, "completed");
        for slot in 0..4 {
            let q = next_content(&s, 20, &items(&s)).unwrap().unwrap();
            assert_eq!(
                s.reference(q, "question/difficulty").unwrap(),
                if slot < 2 { 1100 } else { 1101 }
            );
            let item = present(&mut s, q, "started");
            assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(q));
            assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(q));
            s.entities.get_mut(&item).unwrap().insert(
                "task-item/status".into(),
                json!(if slot < 2 {
                    "task-item.status/incorrect"
                } else {
                    "task-item.status/correct"
                }),
            );
        }
        assert!(lesson_passed(&s, 20, &items(&s)).unwrap());
    }

    #[test]
    fn adaptive_practice_fails_at_five_and_never_reuses_other_task_questions() {
        let mut s = fixture();
        present(&mut s, 40, "completed");
        present(&mut s, 42, "completed");
        for q in 100..105 {
            present(&mut s, q, "incorrect");
        }
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), None);
        assert!(!lesson_passed(&s, 20, &items(&s)).unwrap());

        let mut short_bank = fixture();
        short_bank
            .entities
            .get_mut(&41)
            .unwrap()
            .insert("knowledge-point/questions".into(), json!([100, 101]));
        present(&mut short_bank, 40, "completed");
        present(&mut short_bank, 42, "completed");
        present(&mut short_bank, 100, "incorrect");
        present(&mut short_bank, 101, "correct");
        assert!(
            next_content(&short_bank, 20, &items(&short_bank))
                .unwrap_err()
                .contains("not a failed attempt")
        );
        assert!(continuation(&short_bank, 20, &items(&short_bank), false, 12).is_err());
        assert!(lesson_xp(&short_bank, 20, &items(&short_bank), 12).is_err());

        let mut s = fixture();
        present(&mut s, 40, "completed");
        present(&mut s, 42, "completed");
        put(
            &mut s.entities,
            60,
            json!({"learner-task/id":id(60),"learner-task/items":[61]}),
        );
        put(
            &mut s.entities,
            61,
            json!({"task-item/id":id(61),"task-item/content":100,"task-item/status":"task-item.status/correct"}),
        );
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([9, 60]));
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(101));
    }

    #[test]
    fn candidates_require_prerequisites_keys_and_freshness_but_resume_active_work() {
        let mut s = fixture();
        assert!(candidates(&s, 1, 5).unwrap().is_empty());
        s.entities
            .get_mut(&21)
            .unwrap()
            .insert("progress/repetitions".into(), json!(0.0));
        assert_eq!(candidates(&s, 1, 5).unwrap(), vec![20]);
        s.entities
            .get_mut(&22)
            .unwrap()
            .insert("progress/repetitions".into(), json!(0.0));
        assert!(candidates(&s, 1, 5).unwrap().is_empty());
        s.entities
            .get_mut(&22)
            .unwrap()
            .insert("progress/repetitions".into(), json!(1.0));
        for field in 200..204 {
            s.entities
                .get_mut(&field)
                .unwrap()
                .remove("answer-field/correct");
        }
        assert!(candidates(&s, 1, 5).unwrap().is_empty());
        present(&mut s, 40, "started");
        assert_eq!(candidates(&s, 1, 5).unwrap(), vec![20]);
        assert!(!s.entity(22).unwrap().contains_key("progress/learned"));
    }

    #[test]
    fn grading_checks_all_fields_choice_membership_and_exact_rational_math() {
        let mut s = fixture();
        assert!(grade(&s, 100, &BTreeMap::from([(200, "0.5".into())])).unwrap());
        assert!(
            !grade(
                &s,
                100,
                &BTreeMap::from([(200, "0.500000000000000001".into())])
            )
            .unwrap()
        );
        assert!(grade(&s, 100, &BTreeMap::new()).is_err());
        assert!(grade(&s, 100, &BTreeMap::from([(200, " ".into())])).is_err());
        assert!(
            grade(
                &s,
                100,
                &BTreeMap::from([(200, "0.5".into()), (201, "0.5".into())])
            )
            .is_err()
        );
        s.entities.get_mut(&200).unwrap().insert(
            "answer-field/type".into(),
            json!("answer-field.type/select"),
        );
        assert!(grade(&s, 100, &BTreeMap::from([(200, "300".into())])).unwrap());
        assert!(grade(&s, 100, &BTreeMap::from([(200, "0.5".into())])).is_err());
        put(
            &mut s.entities,
            399,
            json!({"answer/id":id(399),"answer/type":"answer.type/math","answer/value":"\\frac{1}{2}"}),
        );
        s.entities
            .get_mut(&200)
            .unwrap()
            .insert("answer-field/choices".into(), json!([300, 399]));
        assert!(!grade(&s, 100, &BTreeMap::from([(200, "399".into())])).unwrap());
        for (a, b) in [
            ("1/2", "\\frac{2}{4}"),
            ("−2^2", "-4"),
            ("(-2)^2", "4"),
            ("1e-3", "0.001"),
            ("25%", "1/4"),
            ("\\left(1+2\\right)/6", ".5"),
        ] {
            assert!(equivalent_math(a, b), "{a} != {b}");
        }
        for (a, b) in [
            ("1/0", "0"),
            ("1e99999999", "0"),
            ("2^9999999", "0"),
            ("x+1", "x-1"),
        ] {
            assert!(!equivalent_math(a, b));
        }
    }

    #[test]
    fn unsupported_symbolic_blanks_are_not_served_and_rounding_preserves_form() {
        let mut s = fixture();
        s.entities
            .get_mut(&300)
            .unwrap()
            .insert("answer/value".into(), json!("x^2+1"));
        assert!(validate_question(&s, 100).is_err());
        assert!(grade(&s, 100, &BTreeMap::from([(200, "1+x^2".into())])).is_err());
        s.entities
            .get_mut(&300)
            .unwrap()
            .insert("answer/value".into(), json!("0.50"));
        s.entities.get_mut(&100).unwrap().insert(
            "question/problem".into(),
            json!("Round to two decimal places."),
        );
        assert!(grade(&s, 100, &BTreeMap::from([(200, "0.50".into())])).unwrap());
        assert!(!grade(&s, 100, &BTreeMap::from([(200, "1/2".into())])).unwrap());
    }

    #[test]
    fn finalized_xp_counts_errors_separately_from_mastery() {
        for (outcomes, expected) in [
            (vec![true, true], 15),
            (vec![false, true, true], 8),
            (vec![false, false, true, true], 5),
            (vec![false; 5], -1),
            (vec![true, false, true, false, true], 7),
        ] {
            let mut s = fixture();
            present(&mut s, 40, "completed");
            present(&mut s, 42, "completed");
            assert_eq!(lesson_xp(&s, 20, &items(&s), 12).unwrap(), 0);
            for (n, correct) in outcomes.iter().enumerate() {
                present(
                    &mut s,
                    100 + n as u64,
                    if *correct { "correct" } else { "incorrect" },
                );
            }
            assert_eq!(lesson_xp(&s, 20, &items(&s), 12).unwrap(), expected);
            let (next, passed, xp) = continuation(&s, 20, &items(&s), false, 12).unwrap();
            assert_eq!(next, None);
            assert_eq!(xp, expected);
            assert_eq!(passed, lesson_passed(&s, 20, &items(&s)).unwrap());
        }
    }

    #[test]
    fn observed_credit_preserves_imported_repetitions_without_inventing_prior_memory() {
        let s = fixture();
        let at = DateTime::from_timestamp_millis(1_790_760_000_000).unwrap();
        let forms = credit(&s, 1, 20, Some(100), true, false, "answer-1", at).unwrap();
        let progress = forms
            .iter()
            .find(|v| v.get("db/id") == Some(&json!(21)))
            .unwrap();
        assert_eq!(progress["progress/repetitions"], 7.0);
        assert_eq!(progress["progress/memory"], 0.0);
        assert_eq!(progress["progress/learned"], false);
        assert_eq!(progress["progress/practice-mass"], 1.0);
        assert_eq!(
            crate::schema::parse_instant(&progress["progress/memory-at"]).unwrap(),
            at
        );
        assert!(!forms.iter().any(|v| v.get("db/id") == Some(&json!(22))));
        assert_eq!(s.entity(21).unwrap().len(), 3);

        let completed = credit(&s, 1, 20, Some(100), true, true, "answer-and-finish", at).unwrap();
        let progress = completed
            .iter()
            .find(|v| v.get("db/id") == Some(&json!(21)))
            .unwrap();
        assert!(progress["progress/repetitions"].as_f64().unwrap() > 7.0);
        assert_eq!(progress["progress/practice-mass"], 1.0);
        assert_eq!(progress["progress/learned"], true);
        assert_eq!(
            progress["progress/memory"],
            Policy::default().restored_memory
        );

        let mut missing_policy = s.clone();
        missing_policy.entities.remove(&2);
        assert!(
            credit(
                &missing_policy,
                1,
                20,
                Some(100),
                true,
                false,
                "answer-1",
                at
            )
            .is_err()
        );
    }

    #[test]
    fn malformed_generic_routes_are_rejected() {
        let mut s = fixture();
        s.entities
            .get_mut(&31)
            .unwrap()
            .insert("step/next".into(), json!(30));
        assert!(lesson_steps(&s, 20).is_err());
        s.entities.get_mut(&31).unwrap().remove("step/next");
        s.entities
            .get_mut(&20)
            .unwrap()
            .insert("activity/steps".into(), json!([30]));
        assert!(lesson_steps(&s, 20).is_err());
    }
}
