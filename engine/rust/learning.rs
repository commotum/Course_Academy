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
    symbolic,
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
    if let Some(route) = s.entities.lesson_route(activity) {
        return Ok(route);
    }
    let kind = ident(s, activity, "activity/type")?;
    let retrieval = matches!(
        kind.as_str(),
        "activity.type/review" | "activity.type/assessment"
    );
    if kind != "activity.type/lesson" && !retrieval {
        return Err("the progressive player requires a lesson, review or assessment".into());
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
        if retrieval {
            validate_question(s, content)?;
            if kind == "activity.type/review"
                && s.topic_for_question(content)? != s.reference(activity, "activity/scope")?
            {
                return Err("Review questions must belong to its scope topic".into());
            }
        }
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
            if entry.questions.iter().any(|q| s.is_example(*q)) {
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
    if retrieval {
        let questions: BTreeSet<_> = result.iter().map(|step| step.content).collect();
        if questions.len() != result.len() {
            return Err("Retrieval questions must be unique".into());
        }
        if kind == "activity.type/assessment" {
            let topics = questions
                .into_iter()
                .map(|q| s.topic_for_question(q))
                .collect::<Result<BTreeSet<_>>>()?;
            if topics.len() != result.len() {
                return Err("Assessment needs one question per topic".into());
            }
        }
    }
    s.entities.cache_lesson_route(activity, &result);
    Ok(result)
}

pub(crate) fn validate_question(s: &EntitySnapshot, question: u64) -> Result<()> {
    if s.entities.question_validated(question) {
        return Ok(());
    }
    validate_response_question(s, question)?;
    if has_free_fields(s, question)? {
        return Err("free responses do not supply correctness observations for practice".into());
    }
    s.entities.mark_question_validated(question);
    Ok(())
}

/// Fresh lesson, review and assessment practice must be self-contained.
/// Do not use this for grading or replaying previously presented questions.
pub fn validate_practice_question(s: &EntitySnapshot, question: u64) -> Result<()> {
    if s.entities.practice_question_validated(question) {
        return Ok(());
    }
    validate_question(s, question)?;
    if s.entity(question)?.get("question/retired").and_then(Value::as_bool) == Some(true) {
        return Err("Retired questions are unavailable for fresh practice".into());
    }
    let mut has_checkbox = false;
    let mut has_correct_checkbox = false;
    for field in s.refs(question, "question/answer-fields")? {
        if ident(s, field, "answer-field/type")? == "answer-field.type/checkbox" {
            has_checkbox = true;
            let answer = s.reference(field, "answer-field/correct")?;
            has_correct_checkbox |= s.entity(answer)?.get("answer/value").and_then(Value::as_str)
                == Some("true");
        }
    }
    if has_checkbox && !has_correct_checkbox {
        return Err("Checkbox practice requires at least one correct selectable option".into());
    }
    if s.is_multistep_question(question)? {
        return Err(
            "multistep questions belong to their full activity, not standalone practice".into(),
        );
    }
    s.entities.mark_practice_question_validated(question);
    Ok(())
}

pub fn has_free_fields(s: &EntitySnapshot, question: u64) -> Result<bool> {
    for field in s.refs(question, "question/answer-fields")? {
        if ident(s, field, "answer-field/type")? == "answer-field.type/free" {
            return Ok(true);
        }
    }
    Ok(false)
}

/// Assignment response collection also supports ungraded written responses.
/// A free field may begin with no answers and no canonical reference.
pub fn validate_response_question(s: &EntitySnapshot, question: u64) -> Result<()> {
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
            "answer-field.type/radio"
                | "answer-field.type/select"
                | "answer-field.type/blank"
                | "answer-field.type/checkbox"
                | "answer-field.type/free"
        ) {
            return Err("unsupported answer field type".into());
        }
        let choices = s.refs(field, "answer-field/choices")?;
        let kind = ident(s, field, "answer-field/type")?;
        let correct = s.optional_ref(field, "answer-field/correct")?;
        if kind != "answer-field.type/free" && correct.is_none() {
            return Err("graded answer field needs a canonical answer".into());
        }
        if correct.is_some_and(|answer| !choices.contains(&answer)) {
            return Err("canonical answer must belong to its answer field".into());
        }
        if kind == "answer-field.type/checkbox" {
            let values = choices
                .iter()
                .map(|answer| -> Result<String> {
                    if ident(s, *answer, "answer/type")? != "answer.type/text" {
                        return Err("checkbox answers must be text true and false".into());
                    }
                    Ok(s.entity(*answer)?
                        .get("answer/value")
                        .and_then(Value::as_str)
                        .ok_or("checkbox answer needs a string value")?
                        .to_owned())
                })
                .collect::<Result<BTreeSet<_>>>()?;
            if choices.len() != 2 || values != BTreeSet::from(["true".into(), "false".into()]) {
                return Err("checkbox bank must contain exactly true and false".into());
            }
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
            let correct = correct.ok_or("blank field needs a canonical answer")?;
            let canonical = s.entity(correct)?["answer/value"].as_str().unwrap();
            if canonical.trim().is_empty() {
                return Err("canonical blank answer is empty".into());
            }
            let context = math_context(s, question)?;
            match ident(s, correct, "answer/type")?.as_str() {
                "answer.type/math"
                    if RationalParser::parse(&normalize_math(canonical)).is_some()
                        || symbolic::supports(canonical, context)
                        || comma_values(canonical, s.entity(question)?.get("question/problem").and_then(Value::as_str).unwrap_or(""))
                            .is_some_and(|values| values.iter().all(|v| symbolic::supports(v, context))) => {}
                "answer.type/text" => {}
                _ => {
                    return Err("this blank needs a symbolic grader before it can be served".into());
                }
            }
        }
    }
    Ok(())
}

pub(crate) fn seen_questions(s: &EntitySnapshot, learner: u64) -> Result<BTreeSet<u64>> {
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

pub fn ordered_presentations(s: &EntitySnapshot, task: u64) -> Result<Vec<u64>> {
    let all: BTreeSet<_> = s.refs(task, "learner-task/items")?.into_iter().collect();
    if all.is_empty() {
        return Ok(vec![]);
    }
    let mut incoming = BTreeSet::new();
    for i in &all {
        if let Some(n) = s.optional_ref(*i, "task-item/next")? {
            if !all.contains(&n) || !incoming.insert(n) {
                return Err("Invalid presentation chain".into());
            }
        }
    }
    let heads: Vec<_> = all.difference(&incoming).copied().collect();
    if heads.len() != 1 {
        return Err("Invalid presentation chain".into());
    }
    let mut out = vec![];
    let mut cur = Some(heads[0]);
    while let Some(i) = cur {
        if out.contains(&i) {
            return Err("Presentation cycle".into());
        }
        out.push(i);
        cur = s.optional_ref(i, "task-item/next")?;
    }
    if out.len() != all.len() {
        return Err("Disconnected presentations".into());
    }
    Ok(out)
}

/// Fresh supply also excludes frozen questions in active retrieval attempts.
/// Reserving a definition alone does not constitute a learner observation.
pub fn reserved_retrieval_questions(s: &EntitySnapshot, learner: u64) -> Result<BTreeSet<u64>> {
    let mut reserved = BTreeSet::new();
    for task in s.refs(learner, "learner/activity")? {
        if !s.entity(task)?.contains_key("learner-task/status") {
            continue;
        }
        if matches!(
            ident(s, task, "learner-task/status")?.as_str(),
            "learner-task.status/started" | "learner-task.status/paused"
        ) {
            let activity = s.reference(task, "learner-task/activity")?;
            if crate::retrieval::supported(s, activity)? {
                for step in s.refs(activity, "activity/steps")? {
                    reserved.insert(s.reference(step, "step/content")?);
                }
            }
        }
    }
    Ok(reserved)
}
pub fn unavailable_questions(s: &EntitySnapshot, learner: u64) -> Result<BTreeSet<u64>> {
    let mut unavailable = seen_questions(s, learner)?;
    unavailable.extend(reserved_retrieval_questions(s, learner)?);
    // A fixed future lesson question cannot be swapped after the task starts.
    for task in s.refs(learner, "learner/activity")? {
        if !s.entity(task)?.contains_key("learner-task/status") {
            continue;
        }
        if matches!(
            ident(s, task, "learner-task/status")?.as_str(),
            "learner-task.status/started" | "learner-task.status/paused"
        ) {
            let activity = s.reference(task, "learner-task/activity")?;
            if ident(s, activity, "activity/type")? == "activity.type/lesson" {
                for step in s.refs(activity, "activity/steps")? {
                    let content = s.reference(step, "step/content")?;
                    if s.is_ordinary_question(content)? {
                        unavailable.insert(content);
                    }
                }
            }
        }
    }
    Ok(unavailable)
}

/// Opening the first presentation does not establish lesson progress. Keep
/// its timing/exposure record when returning the task to an unstarted state.
pub fn lesson_has_no_progress(s: &EntitySnapshot, task: u64) -> Result<bool> {
    let activity = s.reference(task, "learner-task/activity")?;
    if ident(s, activity, "activity/type")? != "activity.type/lesson" {
        return Ok(false);
    }
    let chain = ordered_presentations(s, task)?;
    if chain.len() > 1 {
        return Ok(false);
    }
    for item in chain {
        if !matches!(ident(s, item, "task-item/status")?.as_str(),
            "task-item.status/started" | "task-item.status/paused")
            || !s.refs(item, "task-item/responses")?.is_empty()
        {
            return Ok(false);
        }
    }
    Ok(true)
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
pub struct Position {
    pub next: Option<u64>,
    pub passed: bool,
    pub shortage: Option<u64>,
    pub failed: bool,
    pub deferred: Vec<u64>,
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

pub(crate) fn question_outcome(s: &EntitySnapshot, item: u64) -> Result<Option<Option<bool>>> {
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
    if crate::retrieval::supported(s, activity)? {
        return crate::retrieval::position(s, activity, items);
    }
    position_with_deferral(s, activity, items, completed_item, None)
}

fn position_with_deferral(
    s: &EntitySnapshot,
    activity: u64,
    items: &[u64],
    completed_item: Option<u64>,
    deferred_item: Option<u64>,
) -> Result<Position> {
    let mut seen = task_learner(s, items)?
        .map(|l| unavailable_questions(s, l))
        .transpose()?
        .unwrap_or_default();
    let steps = lesson_steps(s, activity)?;
    let actual_seen = task_learner(s, items)?
        .map(|l| seen_questions(s, l))
        .transpose()?
        .unwrap_or_default();
    let mut cursor = 0;
    let mut all_correct = true;
    let mut deferred = BTreeSet::new();
    let mut outcomes_by_step: BTreeMap<u64, Vec<Option<bool>>> = BTreeMap::new();
    let mut route: Vec<_> = steps.iter().collect();
    loop {
        for step in &route {
            let current = |next, shortage, passed, pending: &BTreeSet<u64>| Position {
                next,
                shortage,
                passed,
                failed: false,
                deferred: steps
                    .iter()
                    .filter(|st| pending.contains(&st.step))
                    .map(|st| st.step)
                    .collect(),
            };
            match step.kind.as_str() {
                "tutorial" | "example" => {
                    if !consume_instruction(s, items, &mut cursor, step.content, completed_item)? {
                        return Ok(current(Some(step.content), None, false, &deferred));
                    }
                }
                "question" => {
                    let Some(item) = items.get(cursor) else {
                        if actual_seen.contains(&step.content) {
                            return Err("This authored question was already presented. Fresh content is needed; the lesson is not failed.".into());
                        }
                        return Ok(current(Some(step.content), None, false, &deferred));
                    };
                    if s.reference(*item, "task-item/content")? != step.content {
                        return Err("unexpected lesson question".into());
                    }
                    let Some(outcome) = question_outcome(s, *item)? else {
                        if cursor + 1 != items.len() {
                            return Err("unanswered question precedes later content".into());
                        }
                        return Ok(current(Some(step.content), None, false, &deferred));
                    };
                    all_correct &= outcome == Some(true);
                    cursor += 1;
                }
                "knowledge-point" => {
                    let example = step.example.unwrap();
                    let example_item = items.get(cursor).copied();
                    if !consume_instruction(s, items, &mut cursor, example, completed_item)? {
                        return Ok(current(Some(example), None, false, &deferred));
                    }
                    let outcomes = outcomes_by_step.entry(step.step).or_default();
                    let mut previous = example_item;
                    loop {
                        let decision = evaluate_kp_prefix(outcomes)?;
                        if decision.complete() {
                            if decision.passed() == Some(false) {
                                if cursor != items.len() {
                                    return Err(
                                        "presentations continue after failed practice".into()
                                    );
                                }
                                let mut p = current(None, None, false, &deferred);
                                p.failed = true;
                                return Ok(p);
                            }
                            deferred.remove(&step.step);
                            break;
                        }
                        // The marker belongs to a real, finished presentation. It
                        // records missing supply, never an invented question/skip.
                        if let Some(item) = previous {
                            let marker = s.optional_ref(item, "task-item/deferred-step")?;
                            if marker.is_some() && marker != Some(step.step) {
                                return Err("deferral does not match its lesson stage".into());
                            }
                            if marker == Some(step.step) || deferred_item == Some(item) {
                                deferred.insert(step.step);
                                break;
                            }
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
                                return Ok(current(Some(content), None, false, &deferred));
                            };
                            outcomes.push(outcome);
                            seen.insert(content);
                            previous = Some(*item);
                            cursor += 1;
                        } else {
                            let candidates = step
                                .questions
                                .iter()
                                .copied()
                                .filter(|q| {
                                    !seen.contains(q) && validate_practice_question(s, *q).is_ok()
                                })
                                .collect::<Vec<_>>();
                            if candidates.is_empty() {
                                return Ok(current(None, Some(step.step), false, &deferred));
                            }
                            let policy = crate::question_selection::active_policy(s)?;
                            let weights = crate::question_selection::weights(
                                s,
                                policy,
                                "lesson",
                                outcomes.len(),
                            )?;
                            let task = items
                                .first()
                                .map(|i| s.owners(*i, "learner-task/items"))
                                .transpose()?
                                .and_then(|o| o.first().copied())
                                .unwrap_or(activity);
                            let seed =
                                format!("task-{task}/kp-{}/slot-{}", step.content, outcomes.len());
                            let next =
                                crate::question_selection::select(s, &candidates, weights, &seed)?;
                            return Ok(current(next, None, false, &deferred));
                        }
                    }
                }
                _ => unreachable!(),
            }
        }
        if cursor == items.len() {
            return Ok(Position {
                next: None,
                shortage: None,
                failed: false,
                passed: all_correct && deferred.is_empty(),
                deferred: steps
                    .iter()
                    .filter(|st| deferred.contains(&st.step))
                    .map(|st| st.step)
                    .collect(),
            });
        }
        // A later return appends a fresh example at a marked stage. Replay only
        // still-deferred stages, retaining outcomes from earlier presentations.
        let resumed = s
            .optional_ref(items[cursor], "task-item/resumed-step")?
            .ok_or("presentations continue beyond the lesson")?;
        if !deferred.contains(&resumed) {
            return Err("resumed stage was not deferred".into());
        }
        route = steps
            .iter()
            .filter(|st| deferred.contains(&st.step))
            .skip_while(|st| st.step != resumed)
            .collect();
    }
}

/// Inspect the next click without writing or selecting an exposed answer.
pub fn continuation_state(
    s: &EntitySnapshot,
    activity: u64,
    items: &[u64],
    complete_instruction: bool,
    defer: bool,
) -> Result<Position> {
    if crate::retrieval::supported(s, activity)? {
        if complete_instruction || defer {
            return Err("Retrieval questions must be answered or skipped".into());
        }
        return crate::retrieval::position(s, activity, items);
    }
    let item = items.last().copied();
    if complete_instruction {
        let content = s.entity(s.reference(
            item.ok_or("instruction presentation required")?,
            "task-item/content",
        )?)?;
        if !content.contains_key("tutorial/id")
            && !s.is_example(s.reference(item.unwrap(), "task-item/content")?)
        {
            return Err("ordinary questions require a submitted answer".into());
        }
    }
    let p = position_with_deferral(
        s,
        activity,
        items,
        complete_instruction.then_some(item.unwrap_or(0)),
        None,
    )?;
    if defer {
        if p.shortage.is_none() {
            return Err(
                "Practice can only be deferred when fresh questions are unavailable".into(),
            );
        }
        return position_with_deferral(
            s,
            activity,
            items,
            complete_instruction.then_some(item.unwrap_or(0)),
            item,
        );
    }
    Ok(p)
}

pub fn deferred_resume_step(
    s: &EntitySnapshot,
    activity: u64,
    items: &[u64],
) -> Result<Option<u64>> {
    let p = position(s, activity, items)?;
    if p.next.is_some() || p.shortage.is_some() || p.failed {
        return Ok(None);
    }
    let seen = task_learner(s, items)?
        .map(|l| unavailable_questions(s, l))
        .transpose()?
        .unwrap_or_default();
    Ok(lesson_steps(s, activity)?
        .iter()
        .find(|st| {
            p.deferred.contains(&st.step)
                && st
                    .questions
                    .iter()
                    .any(|q| !seen.contains(q) && validate_practice_question(s, *q).is_ok())
        })
        .map(|st| st.step))
}

/// Return an existing active presentation's content, or the next fresh content.
/// The caller reserves a returned new question atomically before displaying it.
pub fn next_content(s: &EntitySnapshot, activity: u64, items: &[u64]) -> Result<Option<u64>> {
    let p = position(s, activity, items)?;
    if p.shortage.is_some() {
        return Err("More fresh questions are needed for this knowledge point. Your lesson remains unfinished; this is not a failed attempt.".into());
    }
    Ok(p.next)
}

/// The first presentation has no task owner yet. Check its learner history
/// explicitly; later adaptive draws recover ownership from existing items.
pub fn first_content(s: &EntitySnapshot, activity: u64, learner: u64) -> Result<Option<u64>> {
    if crate::retrieval::supported(s, activity)? && !crate::retrieval::fresh(s, learner, activity)?
    {
        return Err(
            "These reserved questions were presented elsewhere. Refresh Study for a fresh activity"
                .into(),
        );
    }
    let next = next_content(s, activity, &[])?;
    if let Some(q) = next
        && s.is_ordinary_question(q)?
    {
        validate_practice_question(s, q)?;
    }
    if let Some(q) = next
        && s.is_ordinary_question(q)?
        && unavailable_questions(s, learner)?.contains(&q)
    {
        return Err("This authored question was already presented. Fresh content is needed; the lesson is not failed.".into());
    }
    Ok(next)
}

pub fn lesson_passed(s: &EntitySnapshot, activity: u64, items: &[u64]) -> Result<bool> {
    let p = position(s, activity, items)?;
    Ok(p.next.is_none() && p.shortage.is_none() && p.passed)
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
    if crate::retrieval::supported(s, activity)? {
        let p = crate::retrieval::position(s, activity, items)?;
        return Ok((
            p.next,
            p.passed,
            if p.next.is_none() {
                crate::retrieval::xp(s, activity, items, base)?
            } else {
                0
            },
        ));
    }
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
    if p.shortage.is_some() {
        return Err("More fresh questions are needed for this knowledge point. Your lesson remains unfinished; this is not a failed attempt.".into());
    }
    let passed = p.next.is_none() && p.passed;
    let xp = if p.next.is_none() && (p.deferred.is_empty() || p.failed) {
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
    // Require enough supply to begin recommended work. Exhausted practice
    // within an active lesson can be deferred without claiming failure/mastery.
    plan_candidates_with_supply(s, learner, course, at, 2, true)
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum StudyScope {
    Targets,
    Course,
    Queue,
    Topic(u64),
}
impl StudyScope {
    fn explicit(self) -> bool { matches!(self, Self::Topic(_)) }
}

/// Zero-based global prerequisite layers, matching the graph's L01… badges.
/// A topic's layer is the longest path from any root, using topic/next only.
pub fn topic_layers(s: &EntitySnapshot) -> Result<BTreeMap<u64, usize>> {
    let mut layers: BTreeMap<_, _> = s
        .entities
        .with_attribute("topic/id")
        .into_iter()
        .map(|topic| (topic, 0usize))
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

pub const MIN_STUDY_LAYER: usize = 30;

/// Focus membership is exact: queue entries and prerequisites are not targets.
pub fn topic_in_study_focus(s: &EntitySnapshot, learner: u64, topic: u64) -> Result<bool> {
    Ok(!s.focused_mode || s.refs(learner, "learner/targets")?.contains(&topic))
}

/// Check every assessment topic, rather than its representative first topic.
/// Saved routes are kept intact and become eligible again outside focused mode.
pub fn activity_in_study_focus(s: &EntitySnapshot, learner: u64, activity: u64) -> Result<bool> {
    if !s.focused_mode { return Ok(true); }
    let targets: BTreeSet<_> = s.refs(learner, "learner/targets")?.into_iter().collect();
    match crate::retrieval::kind(s, activity)?.as_str() {
        "lesson" | "review" => Ok(s.optional_ref(activity, "activity/scope")?
            .is_some_and(|topic| targets.contains(&topic))),
        "assessment" => {
            let steps = lesson_steps(s, activity)?;
            if steps.is_empty() { return Ok(false); }
            for step in steps {
                if !targets.contains(&s.topic_for_question(step.content)?) { return Ok(false); }
            }
            Ok(true)
        }
        _ => Ok(false),
    }
}

/// Ordinary practice recommendations use the graph's one-based L30 cutoff.
/// Assessments use learned history at every layer, as does required follow-up
/// practice for assessment misses. Direct topic study has its own path.
fn filter_study_layers(
    s: &EntitySnapshot,
    plan: Vec<PlannedActivity>,
) -> Result<Vec<PlannedActivity>> {
    let layers = topic_layers(s)?;
    let eligible = |topic: u64| layers.get(&topic).is_some_and(|&layer| layer + 1 >= MIN_STUDY_LAYER);
    let mut result = Vec::new();
    for candidate in plan {
        if crate::retrieval::kind(s, candidate.activity)? == "assessment"
            || candidate.priority >= 12000.0
        {
            result.push(candidate);
            continue;
        }
        if let Some(topic) = s.optional_ref(candidate.activity, "activity/scope")? {
            if eligible(topic) {
                result.push(candidate);
            }
        } else {
            // Assessments span topics; their representative candidate.topic
            // alone does not describe all the questions they would serve.
            let steps = lesson_steps(s, candidate.activity)?;
            if !steps.is_empty() && steps.iter().all(|step| {
                s.topic_for_question(step.content).is_ok_and(&eligible)
            }) {
                result.push(candidate);
            }
        }
    }
    Ok(result)
}

/// Self-directed lessons use the fixed target/queue depth-two scope without
/// prerequisite mastery gates. Course mode keeps its operational readiness and
/// module rotation. Both modes preserve ongoing work and content checks.
pub fn study_candidates(
    s: &EntitySnapshot,
    learner: u64,
    course: u64,
    at: DateTime<Utc>,
) -> Result<Vec<PlannedActivity>> {
    let queued = s.entity(learner)?.get("learner/self-directed") == Some(&json!(true));
    if queued || s.focused_mode {
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
    queue_candidates_in_scope(s, learner, course, at, StudyScope::Queue)
}

/// Apply manual selection rules to one topic without copying the captured
/// database or changing the learner's queue and Study-mode preference.
/// Required queue activities do not block an explicit choice of lesson.
pub fn selected_topic_candidates(
    s: &EntitySnapshot,
    learner: u64,
    course: u64,
    topic: u64,
    at: DateTime<Utc>,
) -> Result<Vec<PlannedActivity>> {
    let mut plan = plan_candidates_in_scope(
        s, learner, course, at, 2, false, StudyScope::Topic(topic),
    )?;
    // Do not add unrelated ongoing work or retrieval activities to this
    // selection: their queue priority must not displace the requested lesson.
    plan.retain(|candidate| candidate.topic == topic);
    for candidate in &mut plan {
        if candidate.priority < 10000.0 {
            candidate.reason = "Selected for your queue".into();
        }
    }
    crate::scheduling::filter_selected_candidates(s, learner, plan)
}

fn queue_candidates_in_scope(
    s: &EntitySnapshot,
    learner: u64,
    course: u64,
    at: DateTime<Utc>,
    selection: StudyScope,
) -> Result<Vec<PlannedActivity>> {
    let mut plan = plan_candidates_in_scope(s, learner, course, at, 2, true, selection)?;
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
        if candidate.priority < 10000.0 && candidate.target_count == 0 {
            candidate.reason = "Selected for your queue".into();
        }
    }
    plan.extend(crate::retrieval::candidates(s, learner, course, at, false)?);
    plan.sort_by(|a, b| {
        (b.priority >= 10000.0)
            .cmp(&(a.priority >= 10000.0))
            .then_with(|| (b.priority >= 5000.0).cmp(&(a.priority >= 5000.0)))
            .then_with(|| {
                if a.priority >= 5000.0 && b.priority >= 5000.0 {
                    b.priority.total_cmp(&a.priority)
                } else {
                    std::cmp::Ordering::Equal
                }
            })
    });
    crate::scheduling::filter_self_directed_candidates(s, learner, filter_study_layers(s, plan)?)
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
    ongoing.extend(crate::retrieval::candidates(s, learner, course, at, true)?);
    ongoing.sort_by(|a, b| {
        (b.priority >= 10000.0)
            .cmp(&(a.priority >= 10000.0))
            .then_with(|| (b.priority >= 5000.0).cmp(&(a.priority >= 5000.0)))
            .then_with(|| {
                if a.priority >= 5000.0 && b.priority >= 5000.0 {
                    b.priority.total_cmp(&a.priority)
                } else {
                    std::cmp::Ordering::Equal
                }
            })
    });
    crate::scheduling::filter_candidates(s, learner, filter_study_layers(s, ongoing)?)
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

fn topic_prerequisites(s: &EntitySnapshot) -> Result<BTreeMap<u64, BTreeSet<u64>>> {
    let mut prerequisites: BTreeMap<u64, BTreeSet<u64>> = BTreeMap::new();
    for topic in s.entities.with_attribute("topic/id") {
        for next in s.refs(topic, "topic/next")? {
            prerequisites.entry(next).or_default().insert(topic);
        }
        for kp in s.refs(topic, "topic/knowledge-points")? {
            prerequisites.entry(topic).or_default()
                .extend(s.refs(kp, "knowledge-point/key-prerequisites")?);
        }
    }
    Ok(prerequisites)
}

/// Topics actually learned, without inferring mastery of their ancestors.
/// An explicit false flag takes precedence over historical repetition counts.
pub fn learned_topics(s: &EntitySnapshot, learner: u64) -> Result<BTreeSet<u64>> {
    learning_evidence(s, learner, false)
}

/// Exclusions from ordinary new lessons: graph band one or above, explicit
/// learned status, or completed lesson/review evidence. Imported band progress
/// remains evidence even when a local learned flag is false. Fractional progress
/// below band one alone does not exclude a topic from first-learning work.
pub fn known_lesson_topics(s: &EntitySnapshot, learner: u64) -> Result<BTreeSet<u64>> {
    learning_evidence(s, learner, true)
}

fn learning_evidence(s: &EntitySnapshot, learner: u64, graph_bands: bool) -> Result<BTreeSet<u64>> {
    let mut learned = BTreeSet::new();
    for progress in s.refs(learner, "learner/knowledge-profile")? {
        let record = s.entity(progress)?;
        let repetitions = record.get("progress/repetitions").and_then(Value::as_f64).unwrap_or(0.0);
        if !repetitions.is_finite() || repetitions < 0.0 {
            return Err("invalid imported repetition position".into());
        }
        if record.get("progress/learned") == Some(&json!(true))
            || if graph_bands { repetitions >= 1.0 }
                else { !record.contains_key("progress/learned") && repetitions > 0.0 }
        {
            learned.insert(s.reference(progress, "progress/topic")?);
        }
    }
    for task in s.refs(learner, "learner/activity")? {
        if ident(s, task, "learner-task/status")? != "learner-task.status/completed" {
            continue;
        }
        let activity = s.reference(task, "learner-task/activity")?;
        if matches!(ident(s, activity, "activity/type")?.as_str(),
            "activity.type/lesson" | "activity.type/review")
        {
            if let Some(topic) = s.optional_ref(activity, "activity/scope")? {
                learned.insert(topic);
            }
        }
    }
    Ok(learned)
}

/// Historical study bounds target preparation independently of current FIRe
/// retention. A known downstream topic also covers its prerequisite ancestry;
/// this is a planning inference, never a write to the learner's mastery record.
fn known_topic_ancestry(
    s: &EntitySnapshot,
    learner: u64,
    prerequisites: &BTreeMap<u64, BTreeSet<u64>>,
) -> Result<BTreeSet<u64>> {
    let mut pending: Vec<_> = learned_topics(s, learner)?.into_iter().collect();
    let mut known = BTreeSet::new();
    while let Some(topic) = pending.pop() {
        if known.insert(topic) {
            pending.extend(prerequisites.get(&topic).into_iter().flatten().copied());
        }
    }
    Ok(known)
}

/// Read-only preparation coverage, shared with workload estimates. Retention
/// due dates do not turn already acquired lessons back into first-learning work.
pub fn known_preparation_topics(s: &EntitySnapshot, learner: u64) -> Result<BTreeSet<u64>> {
    if s.entity(learner)?.get("learner/self-directed") == Some(&json!(true)) {
        known_lesson_topics(s, learner)
    } else {
        known_topic_ancestry(s, learner, &topic_prerequisites(s)?)
    }
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
    for assignment in s.refs(learner, "learner/assignments")? {
        if ident(s, assignment, "activity/type")? != "activity.type/assignment" {
            return Err("learner/assignments must reference assignment activities".into());
        }
        // Assignment enrollment writes coverage into learner/targets. Planning
        // only adds deadline context to that set, so explicit target removals
        // remain effective. Assignment completion never changes priorities.
        let due = s
            .entity(assignment)?
            .get("activity/due")
            .map(crate::schema::parse_instant)
            .transpose()?;
        for topic in assignment_targets(s, assignment)? {
            let Some(entry) = targets.get_mut(&topic) else {
                continue;
            };
            if let Some(due) = due {
                *entry = Some(entry.map_or(due, |previous| previous.min(due)));
            }
        }
    }
    let mut support: BTreeMap<u64, TargetSupport> = BTreeMap::new();
    for (target, due) in targets {
        if !s.entity(target)?.contains_key("topic/id") {
            return Err("learner/targets must reference topics".into());
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

pub const STUDY_PREREQUISITE_DEPTH: usize = 2;

/// The graph's default target/queue scope. Mastery and question supply do not
/// alter this boundary; they only affect which lessons can be offered within it.
pub fn study_lesson_scope(s: &EntitySnapshot, learner: u64) -> Result<BTreeSet<u64>> {
    Ok(bounded_lesson_support(s, learner, &BTreeSet::new())?.into_keys().collect())
}

fn bounded_lesson_support(
    s: &EntitySnapshot, learner: u64, learned: &BTreeSet<u64>,
) -> Result<BTreeMap<u64, TargetSupport>> {
    let layers = topic_layers(s)?;
    let mut roots: BTreeMap<u64, Option<DateTime<Utc>>> = BTreeMap::new();
    let attributes = if s.focused_mode { &["learner/targets"][..] }
        else { &["learner/targets", "learner/queue"][..] };
    for attr in attributes {
        for topic in s.refs(learner, attr)? {
            let layer = layers.get(&topic).ok_or("Study selections must reference topics")?;
            if layer + 1 >= MIN_STUDY_LAYER { roots.insert(topic, None); }
        }
    }
    for assignment in s.refs(learner, "learner/assignments")? {
        if ident(s, assignment, "activity/type")? != "activity.type/assignment" {
            return Err("learner/assignments must reference assignment activities".into());
        }
        let due = s.entity(assignment)?.get("activity/due")
            .map(crate::schema::parse_instant).transpose()?;
        for topic in assignment_targets(s, assignment)? {
            if let (Some(entry), Some(due)) = (roots.get_mut(&topic), due) {
                *entry = Some(entry.map_or(due, |previous| previous.min(due)));
            }
        }
    }
    let mut support: BTreeMap<u64, TargetSupport> = BTreeMap::new();
    for (root, due) in roots {
        let mut distances = BTreeMap::from([(root, 0)]);
        let mut pending = VecDeque::from([root]);
        while let Some(topic) = pending.pop_front() {
            let distance = distances[&topic];
            if distance == if s.focused_mode { 0 } else { STUDY_PREREQUISITE_DEPTH } { continue; }
            // Use topic/next only, matching the visible graph. KP prerequisites
            // neither enlarge the scope nor veto entry to a scoped lesson.
            for prerequisite in s.owners(topic, "topic/next")? {
                if layers[&prerequisite] + 1 < MIN_STUDY_LAYER { continue; }
                if let std::collections::btree_map::Entry::Vacant(entry) = distances.entry(prerequisite) {
                    entry.insert(distance + 1);
                    pending.push_back(prerequisite);
                }
            }
        }
        let remaining = distances.keys().filter(|topic| !learned.contains(topic)).count();
        for (topic, distance) in distances {
            let entry = support.entry(topic).or_default();
            entry.targets.insert(root);
            entry.remaining = Some(entry.remaining.map_or(remaining, |n| n.min(remaining)));
            entry.distance = Some(entry.distance.map_or(distance, |n| n.min(distance)));
            if let Some(due) = due { entry.due = Some(entry.due.map_or(due, |d| d.min(due))); }
        }
    }
    Ok(support)
}

/// Same lesson priority score, before eligibility or fresh-supply filtering.
fn inventory_priority_score(repetitions: f64, target_count: usize, remaining_topics: usize,
    nearest_target_steps: Option<usize>, due: Option<DateTime<Utc>>, at: DateTime<Utc>) -> f64 {
    let mut priority = 1.0 / (1.0 + repetitions);
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
    priority
}

/// Operational prerequisite readiness, shared by planning and generator demand.
/// Historical lesson completion is deliberately separate from current retention.
pub fn progress_ready(r: &crate::schema::Record, threshold: Option<f64>, at: DateTime<Utc>) -> Result<bool> {
    let reps = r.get("progress/repetitions").and_then(Value::as_f64).unwrap_or(0.0);
    if !reps.is_finite() || reps < 0.0 {
        return Err("invalid imported repetition position".into());
    }
    if !COMPLETE_PROGRESS.iter().all(|key| r.contains_key(*key)) {
        return Ok(reps > 0.0);
    }
    if r.get("progress/learned") != Some(&json!(true)) {
        return Ok(false);
    }
    let threshold = threshold.ok_or("operational readiness needs one configured FIRe policy")?;
    let memory = r["progress/memory"].as_f64().ok_or("invalid retention")?;
    let interval = r["progress/interval-days"].as_f64().ok_or("invalid interval")?;
    let observed = crate::schema::instant_days(&r["progress/memory-at"])?;
    if !memory.is_finite() || memory < 0.0 || !interval.is_finite() || interval <= 0.0 {
        return Err("invalid operational retention state".into());
    }
    let now = timestamp_days(at);
    Ok(now >= observed && memory * 2.0_f64.powf(-(now - observed) / interval) > threshold)
}

#[derive(Clone, Debug)]
pub struct InventoryPriority {
    pub priority: f64,
    pub target_count: usize,
    pub ongoing: bool,
    pub due: Option<DateTime<Utc>>,
}

/// Rank replenishment even when a topic's bank prevents a lesson being offered.
/// Uses the planner's target/deadline support and operational FIRe readiness.
pub fn inventory_priorities(s: &EntitySnapshot, learner: u64, at: DateTime<Utc>)
    -> Result<BTreeMap<u64, InventoryPriority>> {
    let mut ready = BTreeSet::new();
    let mut repetitions = BTreeMap::new();
    let thresholds: Vec<_> = s
        .entities
        .with_attribute("policy/id")
        .into_iter()
        .filter_map(|id| {
            s.entities[&id]
                .get("policy/review-threshold")
                .and_then(Value::as_f64)
        })
        .collect();
    let threshold = if thresholds.len() == 1 {
        Some(thresholds[0])
    } else {
        None
    };
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
        if progress_ready(r, threshold, at)? {
            ready.insert(topic);
        }
    }
    let mut prerequisites: BTreeMap<u64, BTreeSet<u64>> = BTreeMap::new();
    for topic in s.entities.with_attribute("topic/id") {
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
    let support = if s.entity(learner)?.get("learner/self-directed") == Some(&json!(true)) {
        bounded_lesson_support(s, learner, &known_lesson_topics(s, learner)?)?
    } else {
        target_support(s, learner, &prerequisites, &ready)?
    };
    let mut ongoing = BTreeSet::new();
    for task in s.refs(learner, "learner/activity")? {
        if matches!(ident(s, task, "learner-task/status")?.as_str(),
            "learner-task.status/started" | "learner-task.status/paused") {
            let activity = s.reference(task, "learner-task/activity")?;
            if let Some(topic) = s.optional_ref(activity, "activity/scope")? { ongoing.insert(topic); }
        }
    }
    Ok(s.entities.with_attribute("topic/id").into_iter().map(|topic| {
        let target = support.get(&topic);
        let target_count = target.map_or(0, |t| t.targets.len());
        let ongoing = ongoing.contains(&topic);
        let priority = inventory_priority_score(repetitions.get(&topic).copied().unwrap_or(0.0),
            target_count, target.and_then(|t| t.remaining).unwrap_or(0),
            target.and_then(|t| t.distance), target.and_then(|t| t.due), at)
            + if ongoing { 10000.0 } else { 0.0 };
        (topic, InventoryPriority { priority, target_count, ongoing, due: target.and_then(|t| t.due) })
    }).collect())
}

pub(crate) fn plan_candidates_with_supply(
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
    if let StudyScope::Topic(topic) = selection {
        if !s.entity(topic)?.contains_key("topic/id") {
            return Err("Study selection must reference a topic".into());
        }
        scope.insert(topic);
    } else if selection != StudyScope::Queue {
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
        .with_attribute("policy/id")
        .into_iter()
        .filter_map(|id| {
            s.entities[&id]
                .get("policy/review-threshold")
                .and_then(Value::as_f64)
        })
        .collect();
    let threshold = if thresholds.len() == 1 {
        Some(thresholds[0])
    } else {
        None
    };
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
        if selection.explicit() || selection == StudyScope::Queue {
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
        if progress_ready(r, threshold, at)? {
            ready.insert(topic);
        }
    }
    let prerequisites = if selection == StudyScope::Queue { BTreeMap::new() } else { topic_prerequisites(s)? };
    let support = if selection == StudyScope::Queue {
        practiced = known_lesson_topics(s, learner)?;
        bounded_lesson_support(s, learner, &practiced)?
    } else if selection == StudyScope::Targets {
        target_support(s, learner, &prerequisites, &ready)?
    } else {
        BTreeMap::new()
    };
    scope.extend(support.keys().copied());
    let seen = unavailable_questions(s, learner)?;
    let relearn = crate::retrieval::relearn_topics(s, learner)?;
    practiced.retain(|topic| !relearn.contains(topic));
    let mut finished = BTreeSet::new();
    let mut active = BTreeMap::new();
    let mut unstarted = BTreeMap::new();
    for task in s.refs(learner, "learner/activity")? {
        let status = ident(s, task, "learner-task/status")?;
        if status == "learner-task.status/completed" {
            let activity = s.reference(task, "learner-task/activity")?;
            if s.optional_ref(activity, "activity/scope")?
                .is_none_or(|topic| !relearn.contains(&topic))
            {
                finished.insert(activity);
            }
        } else if matches!(
            status.as_str(),
            "learner-task.status/started" | "learner-task.status/paused"
        ) {
            active.insert(s.reference(task, "learner-task/activity")?, task);
        } else if matches!(status.as_str(), "learner-task.status/locked" | "learner-task.status/unlocked")
            && lesson_has_no_progress(s, task)?
        {
            if let Some(item) = ordered_presentations(s, task)?.last() {
                unstarted.insert(s.reference(task, "learner-task/activity")?, s.reference(*item, "task-item/content")?);
            }
        }
    }
    let lifecycle = crate::scheduling::lifecycle(s, learner)?;
    let mut result = vec![];
    for activity in s.entities.with_attribute("activity/id") {
        if ident(s, activity, "activity/type")? != "activity.type/lesson"
            || finished.contains(&activity)
        {
            continue;
        }
        let Some(topic) = s.optional_ref(activity, "activity/scope")? else {
            continue;
        };
        if !selection.explicit() && !topic_in_study_focus(s, learner, topic)? {
            continue;
        }
        if lifecycle.lesson_blocked(s, topic)?
            || (!selection.explicit() && !lifecycle.retry_ready(topic))
        {
            continue;
        }
        if active.contains_key(&activity) {
            // Saved attempts remain resumable when changing modes or removing
            // their topic from the queue. Scope only limits new lessons.
            if lesson_steps(s, activity).is_ok() && {
                let chain = ordered_presentations(s, active[&activity])?;
                if !chain
                    .iter()
                    .any(|i| s.entities[i].contains_key("task-item/deferred-step"))
                {
                    true
                } else {
                    let p = position(s, activity, &chain)?;
                    p.next.is_some()
                        || p.shortage.is_some()
                        || p.deferred.is_empty()
                        || deferred_resume_step(s, activity, &chain)?.is_some()
                }
            } {
                result.push((activity, topic));
            }
            continue;
        }
        if !scope.contains(&topic) {
            continue;
        }
        if (exclude_practiced && practiced.contains(&topic))
            || (!selection.explicit() && selection != StudyScope::Queue
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
                    .filter(|q| !seen.contains(q) && validate_practice_question(s, **q).is_ok())
                    .take(minimum_fresh)
                    .count()
                    < minimum_fresh
            }
            "question" => {
                let saved = unstarted.get(&activity) == Some(&step.content);
                (seen.contains(&step.content) && !saved)
                    || if saved {
                        validate_question(s, step.content).is_err()
                    } else {
                        validate_practice_question(s, step.content).is_err()
                    }
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
            let mut priority = inventory_priority_score(
                repetitions.get(&topic).copied().unwrap_or(0.0), target_count,
                remaining_topics, nearest_target_steps, due, at,
            );
            let mut reason = if active.contains_key(&activity) {
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
    let seen = unavailable_questions(s, learner)?;
    let mut ready_unlearned = vec![];
    for activity in candidates_with_supply(s, learner, course, 0, true)? {
        let mut kps = vec![];
        for step in lesson_steps(s, activity)? {
            if step.kind == "knowledge-point" {
                let valid = step
                    .questions
                    .iter()
                    .filter(|q| !seen.contains(q) && validate_practice_question(s, **q).is_ok())
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

/// Validate complete submissions independently of whether a question is graded.
pub fn validate_responses(
    s: &EntitySnapshot,
    question: u64,
    responses: &BTreeMap<u64, String>,
) -> Result<()> {
    validate_response_question(s, question)?;
    let fields: BTreeSet<_> = s
        .refs(question, "question/answer-fields")?
        .into_iter()
        .collect();
    if fields != responses.keys().copied().collect() {
        return Err("answer every field of the current question".into());
    }
    for field in fields {
        let submitted = &responses[&field];
        let kind = ident(s, field, "answer-field/type")?;
        if submitted.trim().is_empty() {
            return Err("answer every field before submitting".into());
        }
        let limit = if kind == "answer-field.type/free" {
            64000
        } else {
            4096
        };
        if submitted.len() > limit {
            return Err(format!("answer exceeds {limit} bytes").into());
        }
        if !matches!(
            kind.as_str(),
            "answer-field.type/blank" | "answer-field.type/free"
        ) {
            let selected = submitted
                .parse::<u64>()
                .map_err(|_| "selected answer must identify an authored choice")?;
            if !s.refs(field, "answer-field/choices")?.contains(&selected) {
                return Err("selected answer does not belong to this field".into());
            }
        }
    }
    Ok(())
}

/// All fields must be present exactly once. Choice fields contain the selected
/// answer's decimal entity ID; blanks contain verbatim entered text. References
/// distinguish choices even when their visible values happen to be identical.
pub fn grade(s: &EntitySnapshot, question: u64, responses: &BTreeMap<u64, String>) -> Result<bool> {
    validate_question(s, question)?;
    validate_responses(s, question, responses)?;
    let fields: BTreeSet<_> = s
        .refs(question, "question/answer-fields")?
        .into_iter()
        .collect();
    if fields != responses.keys().copied().collect() {
        return Err("answer every field of the current question".into());
    }
    if let Some([(f1, a), (f2, b)]) = interchangeable_exponents(s, question)? {
        let c=math_context(s, question)?;
        // Both exponent labels may be exchanged, but duplicate roots cannot
        // replace a fundamental pair. Require one complete bijection.
        let direct=compare_math(&responses[&f1],&a,c)? && compare_math(&responses[&f2],&b,c)?;
        let swapped=compare_math(&responses[&f1],&b,c)? && compare_math(&responses[&f2],&a,c)?;
        return Ok(direct || swapped);
    }
    let mut correct = true;
    for field in fields {
        correct &= grade_field(s, question, field, &responses[&field])?;
    }
    Ok(correct)
}

/// The two exponents of c1*exp(r1*x)+c2*exp(r2*x) are labels, not an
/// ordered coordinate pair. Restrict this to that explicit two-blank contract;
/// arbitrary two-field questions retain their independent canonical values.
fn interchangeable_exponents(s: &EntitySnapshot, question: u64) -> Result<Option<[(u64,String);2]>> {
    let q=s.entity(question)?;
    let prompt=q.get("question/problem").and_then(Value::as_str).unwrap_or("").to_lowercase();
    let compact=normalize_math(&prompt);
    if !prompt.contains("general solution") || !compact.contains("c_1e^{r_1x}+c_2e^{r_2x}")
        || ["increasing order", "decreasing order", "ascending order", "descending order", "r_1<r_2", "r_1>r_2", "r_1 < r_2", "r_1 > r_2"].iter().any(|word| prompt.contains(word)) {
        return Ok(None);
    }
    let fields=s.refs(question,"question/answer-fields")?;
    if fields.len()!=2 { return Ok(None); }
    let mut pair=Vec::new();
    for f in fields {
        let key=s.entity(f)?.get("answer-field/key").and_then(Value::as_str).unwrap_or("");
        if !["r1","r2"].contains(&key) || ident(s,f,"answer-field/type")? != "answer-field.type/blank" { return Ok(None); }
        let a=s.reference(f,"answer-field/correct")?;
        if ident(s,a,"answer/type")? != "answer.type/math" { return Ok(None); }
        let value=s.entity(a)?.get("answer/value").and_then(Value::as_str).ok_or("math answer needs a value")?.to_owned();
        pair.push((f,value));
    }
    if compare_math(&pair[0].1,&pair[1].1,math_context(s,question)?)? { return Ok(None); }
    Ok(Some([pair.remove(0),pair.remove(0)]))
}

/// Compare one submitted field using the same choice/text/symbolic rules as
/// question grading. Read projections use this only after feedback is revealed.
pub fn grade_field(s: &EntitySnapshot, question: u64, field: u64, submitted: &str) -> Result<bool> {
    if submitted.trim().is_empty() {
        return Err("answer every field before submitting".into());
    }
    if submitted.len() > 4096 {
        return Err("answer exceeds 4096 bytes".into());
    }
    let expected = s.reference(field, "answer-field/correct")?;
    let canonical = s
        .entity(expected)?
        .get("answer/value")
        .and_then(|value| value.as_str())
        .ok_or("Canonical answer needs a string value")?;
    let field_kind = ident(s, field, "answer-field/type")?;
    if field_kind != "answer-field.type/blank" {
        let selected: u64 = submitted
            .parse()
            .map_err(|_| "selected answer must identify an authored choice")?;
        if !s.refs(field, "answer-field/choices")?.contains(&selected) {
            return Err("selected answer does not belong to this field".into());
        }
        Ok(selected == expected)
    } else {
        Ok(match ident(s, expected, "answer/type")?.as_str() {
            "answer.type/math" => {
                // Form-sensitive prompts must match their authored answer
                // representation. Rounding accepts equivalent decimal numerals;
                // significant figures and reduced-form work remain form-sensitive.
                let prompt = s
                    .entity(question)?
                    .get("question/problem")
                    .and_then(|value| value.as_str())
                    .ok_or("Question needs a problem statement")?
                    .to_lowercase();
                let context = math_context(s, question)?;
                if let Some(pair) = interchangeable_exponents(s, question)? {
                    return Ok(compare_math(submitted, &pair[0].1, context)?
                        || compare_math(submitted, &pair[1].1, context)?);
                }
                let key = s.entity(field)?.get("answer-field/key").and_then(Value::as_str).unwrap_or("");
                if displayed_squared_blank(&prompt, key) {
                    // Compare the mathematical object the learner completes,
                    // rather than imposing a sign on an externally squared factor.
                    compare_math(&format!("({submitted})^2"), &format!("({canonical})^2"), context)?
                } else if displayed_integration_constant(&prompt, key)
                    || displayed_solution_family_constant(&prompt, key)
                {
                    symbolic::compare_up_to_constant(submitted, canonical, context)?
                } else if key == "antiderivative" && prompt.contains("arbitrary constant")
                    && !requires_answer_form(&prompt)
                    && !["initial condition", "particular solution", "constant term is zero"]
                        .iter().any(|text| prompt.contains(text))
                {
                    match symbolic::compare_polynomial_constant_family(submitted, canonical, context)? {
                        Some(equal) => equal,
                        None => compare_math_in_context(submitted, canonical, &prompt, context)?,
                    }
                } else {
                    compare_math_in_context(submitted, canonical, &prompt, context)?
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
        })
    }
}

/// Final lesson XP uses the shared whole-task accuracy rule, including failures.
/// Unfinished work has no award. Tutorials/examples are never answer evidence.
pub fn lesson_xp(s: &EntitySnapshot, activity: u64, items: &[u64], base: i64) -> Result<i64> {
    if base < 0 {
        return Err("base XP must be nonnegative".into());
    }
    let p = position(s, activity, items)?;
    if p.shortage.is_some() {
        return Err("More fresh questions are needed for this knowledge point".into());
    }
    if p.next.is_some() || (!p.deferred.is_empty() && !p.failed) {
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

fn normalize_answer_form(value: &str) -> String {
    let text = normalize_math(value);
    let unsigned = text
        .strip_prefix('-')
        .or_else(|| text.strip_prefix('+'))
        .unwrap_or(&text);
    // Normalize only a complete decimal numeral's optional positive sign and
    // integer leading zeroes. Preserve every fractional digit and the minus
    // sign so precision requirements remain strict; leave expressions unchanged.
    if let Some((whole, fraction)) = unsigned.split_once('.')
        && whole.bytes().all(|digit| digit.is_ascii_digit())
        && !fraction.is_empty()
        && fraction.bytes().all(|digit| digit.is_ascii_digit())
    {
        let significant_whole = whole.trim_start_matches('0');
        let whole = if significant_whole.is_empty() {
            "0"
        } else {
            significant_whole
        };
        let sign = if text.starts_with('-') { "-" } else { "" };
        return format!("{sign}{whole}.{fraction}");
    }
    normalize_fraction_form(&text).unwrap_or(text)
}

fn normalize_fraction_form(value: &str) -> Option<String> {
    fn integer(mut value: &str) -> Option<num_bigint::BigInt> {
        // Parentheses only group an integer token; they do not require any
        // arithmetic or reduction. Preserve its numerator/denominator pair.
        while let Some(inner) = value.strip_prefix('(').and_then(|v| v.strip_suffix(')')) {
            value = inner;
        }
        let digits = value
            .strip_prefix('-')
            .or_else(|| value.strip_prefix('+'))
            .unwrap_or(value);
        if digits.is_empty() || !digits.bytes().all(|digit| digit.is_ascii_digit()) {
            return None;
        }
        value.parse().ok()
    }
    fn tex_argument(value: &str) -> Option<(&str, &str)> {
        if let Some(group) = value.strip_prefix('{') {
            group.split_once('}')
        } else if value.as_bytes().first()?.is_ascii_digit() {
            // An unbraced TeX argument is one token, never a whole digit run.
            Some((&value[..1], &value[1..]))
        } else {
            None
        }
    }
    let unsigned = value
        .strip_prefix('-')
        .or_else(|| value.strip_prefix('+'))
        .unwrap_or(value);
    let (numerator, denominator) = if let Some(args) = unsigned.strip_prefix(r"\frac") {
        let (numerator, args) = tex_argument(args)?;
        let (denominator, rest) = tex_argument(args)?;
        if !rest.is_empty() {
            return None;
        }
        (numerator, denominator)
    } else {
        unsigned.split_once('/')?
    };
    let mut numerator = integer(numerator)?;
    let denominator = integer(denominator)?;
    if denominator.is_zero() {
        return None;
    }
    if value.starts_with('-') {
        numerator = -numerator;
    }
    // Compare the authored integer pair, not its reduced rational value.
    // Thus TeX/slash spellings agree while 2/8 still differs from 1/4.
    Some(format!(r"\frac{{{numerator}}}{{{denominator}}}"))
}

/// Compatibility predicate for callers that need only proved equivalence.
/// The learner-facing grader uses compare_math so unsupported comparisons
/// remain errors, rather than being recorded as incorrect learner answers.
pub fn equivalent_math(a: &str, b: &str) -> bool {
    compare_math(a, b, symbolic::Context::default()).unwrap_or(false)
}

fn compare_math(a: &str, b: &str, context: symbolic::Context) -> Result<bool> {
    let (original_a, original_b) = (a, b);
    // The numeric shortcut must use the same e interpretation as the exact
    // symbolic path, including when the canonical result happens to be numeric.
    if context.natural_exponential {
        return symbolic::compare(original_a, original_b, context);
    }
    let a = normalize_math(a);
    let b = normalize_math(b);
    if a.is_empty() || b.is_empty() {
        return Err("empty mathematical answer".into());
    }
    match (RationalParser::parse(&a), RationalParser::parse(&b)) {
        (Some(a), Some(b)) => Ok(a == b),
        _ => symbolic::compare(original_a, original_b, context),
    }
}

/// A whole blank displayed as (blank)^2 is determined only up to sign.
/// Do not apply this to a term within a larger factor, another field, an
/// unsquared blank, or a prompt explicitly constraining the factor's sign/form.
fn displayed_squared_blank(prompt: &str, key: &str) -> bool {
    if key.is_empty() || requires_answer_form(prompt) {
        return false;
    }
    let constrained = regex::Regex::new(r"\b(?:positive|negative|nonnegative|nonpositive|monic)\b|leading coefficient").unwrap();
    if constrained.is_match(prompt) { return false; }
    let marker = format!("{{{{{}}}}}", key.to_lowercase());
    let mut compact: String = prompt.chars().filter(|c| !c.is_whitespace() && *c != '$').collect();
    for command in ["\\left", "\\right", "\\,", "\\!", "\\;", "\\quad", "\\qquad"] {
        compact = compact.replace(command, "");
    }
    if compact.matches(&marker).count() != 1 { return false; }
    let Some((prefix, suffix)) = compact.split_once(&marker) else { return false; };
    if !prefix.ends_with('(') { return false; }
    if suffix.starts_with(")^{2}") { return true; }
    suffix.strip_prefix(")^2").is_some_and(|tail| {
        tail.chars().next().is_none_or(|c| !c.is_ascii_digit() && c != '.')
    })
}

#[cfg(test)]
mod squared_blank_tests {
    use super::*;
    #[test]
    fn whole_squared_blank_only() {
        for prompt in [r"$p=($ {{factor}} $)^{2}-3$", r"$p=\left({{factor}}\right)^2+1$", r"$p=({{factor}})^2x$"] {
            assert!(displayed_squared_blank(prompt, "factor"), "{prompt}");
        }
        for prompt in [r"$p=({{factor}}+1)^2$", r"$p={{factor}}^2$", r"$p=({{other}})^2+{{factor}}$", r"$p=({{factor}})^20$", r"$p=({{factor}})^2.5$", r"$p=({{factor}})^3$", r"Give a monic factor: $p=({{factor}})^2$", r"Give a positive factor: $p=({{factor}})^2$", r"$p=({{factor}})^2+{{factor}}$"] {
            assert!(!displayed_squared_blank(prompt, "factor"), "{prompt}");
        }
    }
    #[test]
    fn square_comparison_accepts_sign_and_rejects_changed_factor() {
        let ctx = symbolic::Context::default();
        assert!(compare_math("(-x-3)^2", "(x+3)^2", ctx).unwrap());
        assert!(!compare_math("(x-3)^2", "(x+3)^2", ctx).unwrap());
        assert!(!compare_math("(-x-4)^2", "(x+3)^2", ctx).unwrap());
    }
}

fn displayed_integration_constant(prompt: &str, key: &str) -> bool {
    if key.is_empty() || requires_answer_form(prompt)
        || !(prompt.contains("antiderivative") || prompt.contains("indefinite integral") || prompt.contains("\\int"))
        || prompt.contains("\\int_") || prompt.contains("\\int^")
        || ["zero constant term", "constant term is zero", "constant term is 0"]
            .iter().any(|text| prompt.contains(text))
    {
        return false;
    }
    let marker = format!("{{{{{}}}}}", key.to_lowercase());
    let Some((_, suffix)) = prompt.split_once(&marker) else { return false; };
    let suffix = suffix.replace([ '$', '\n', '\r' ], " ")
        .replace("\\(", " ").replace("\\)", " ")
        .replace("\\,", " ").replace("\\!", " ").replace("\\;", " ")
        .replace("\\quad", " ").replace("\\qquad", " ");
    let Some(after_plus) = suffix.trim_start().strip_prefix('+') else { return false; };
    let Some(after_c) = after_plus.trim_start().strip_prefix('c') else { return false; };
    after_c.chars().next().is_none_or(|c| !c.is_alphanumeric() && !"_^({".contains(c))
}

/// A whole additive blank inside (blank + K) has the same constant freedom
/// even when that group is subsequently inverted, rooted, or exponentiated.
/// Require both an explicit general-ODE-solution contract and the arbitrary
/// constant adjacent to this field. Merely mentioning K elsewhere is not enough.
fn displayed_solution_family_constant(prompt: &str, key: &str) -> bool {
    if key.is_empty() || requires_answer_form(prompt)
        || !((prompt.contains("general solution") && prompt.contains("differential equation"))
            || (prompt.contains("nonconstant local solution") && prompt.contains("separating variables")))
        || ["zero constant term", "constant term is zero", "constant term is 0", "nonconstant polynomial term",
            "initial condition", "particular solution", "satisfying", "given that"]
            .iter().any(|text| prompt.contains(text))
    {
        return false;
    }
    let marker = format!("{{{{{}}}}}", key.to_lowercase());
    let mut compact = normalize_math(prompt).to_lowercase();
    if compact.matches(&marker).count() != 1 { return false; }

    // Some forms print a named box in the equation and its input below it.
    // Resolve only an unambiguous one-to-one label, not a nearby unrelated blank.
    let boxes = regex::Regex::new(r"\\boxed\{\\text\{([a-z]+)\}\}").unwrap();
    let named: Vec<_> = boxes.captures_iter(&compact).collect();
    if named.len() == 1 {
        let named_box = named[0][0].to_owned();
        let label = named[0][1].to_owned();
        let tail = format!("{label}:{marker}");
        if compact.ends_with(&tail) {
            compact.truncate(compact.len()-tail.len());
            compact = compact.replace(&named_box, &marker);
        }
    }
    // UI inputs may split one equation across separate inline math spans.
    compact = compact.replace(&format!("${marker}$"), &marker);
    // Limit coupling checks to the equation, not the prose declaring C arbitrary.
    let Some(equation) = compact.split('$').find(|part| part.contains(&marker) && part.contains('='))
        else { return false; };
    let Some((prefix, suffix)) = equation.split_once(&marker) else { return false; };
    let close = match prefix.chars().last() {
        Some('(') => ')',
        Some('{') => '}',
        _ => return false,
    };
    let Some((_, outer)) = prefix.rsplit_once('=') else { return false; };
    // Strip TeX command names when looking for additional uses of a parameter:
    // the c in \\cos is not another occurrence of the integration constant C.
    let commands = regex::Regex::new(r"\\[a-z]+").unwrap();
    ['c', 'k'].iter().any(|constant| {
        suffix.starts_with(&format!("+{constant}{close}"))
            && !commands.replace_all(outer, "").contains(*constant)
            && !commands.replace_all(&suffix[2..], "").contains(*constant)
            // The general/local family contract permits the conventional +C;
            // any explicit assignment of its value removes that freedom.
            && !compact.contains(&format!("{constant}="))
            && (compact.replace('$', "").contains(&format!("{constant}isanarbitraryconstant"))
                // An unconstrained nonconstant local solution found by separation
                // conventionally uses +C for its free integration constant.
                || (prompt.contains("nonconstant local solution") && *constant == 'c'))
    })
}

/// Split exactly two coordinates, preserving nested expression groups. This
/// is used only when the prompt explicitly requests an ordered pair, so a
/// comma in interval, function, or subscript notation is not reinterpreted.
fn ordered_pair_coordinates(value: &str) -> Option<(&str, &str)> {
    let inner = value.strip_prefix('(')?.strip_suffix(')')?;
    let mut groups = Vec::new();
    let mut comma = None;
    for (index, ch) in inner.char_indices() {
        match ch {
            '(' => groups.push(')'),
            '{' => groups.push('}'),
            '[' => groups.push(']'),
            ')' | '}' | ']' => {
                if groups.pop() != Some(ch) { return None; }
            }
            ',' if groups.is_empty() => {
                if comma.replace(index).is_some() { return None; }
            }
            _ => {}
        }
    }
    if !groups.is_empty() { return None; }
    let index = comma?;
    let (left, right) = (&inner[..index], &inner[index + 1..]);
    (!left.is_empty() && !right.is_empty()).then_some((left, right))
}

/// Bare comma lists are finite values only under an explicit comma-values
/// instruction. Nested commas and ordered pairs do not acquire set semantics.
fn comma_values(value: &str, prompt: &str) -> Option<Vec<String>> {
    let p=prompt.to_lowercase();
    if !(p.contains("values") && p.contains("separate") && p.contains("commas")) || p.contains("ordered") { return None; }
    let compact=normalize_math(value);
    let wrapped=format!("({compact})");
    let (a,b)=ordered_pair_coordinates(&wrapped)?;
    Some(vec![a.to_owned(),b.to_owned()])
}


/// Use only a single explicit f(x) definition in a request for its symbolic
/// derivative. A mention of a rational expression in unrelated practice must
/// not weaken ordinary answer-domain checks.
fn derivative_source_function(prompt: &str) -> Option<String> {
    let compact = normalize_math(prompt);
    let request = compact.replace("\\prime", "'").replace('′', "'")
        .replace(['{', '}', '^'], "");
    if !request.contains("f'(x)")
        || !["find", "calculate", "derivative", "differentiate"].iter().any(|word| prompt.contains(word))
    { return None; }
    let definitions: Vec<_> = compact.split('$')
        .filter_map(|part| part.strip_prefix("f(x)="))
        .map(|value| value.trim_end_matches([',', '.']).to_owned()).collect();
    if definitions.len() != 1 || definitions[0].is_empty() { return None; }
    Some(definitions[0].clone())
}

/// Error-preserving comparison shared by grading and content reconciliation.
pub fn compare_math_in_context(
    a: &str,
    b: &str,
    prompt: &str,
    context: symbolic::Context,
) -> Result<bool> {
    if let Some(expected)=comma_values(b,prompt) {
        let Some(actual)=comma_values(a,prompt) else { return Ok(false); };
        return crate::set_answers::compare(&format!(r"\{{{}\}}",actual.join(",")),
            &format!(r"\{{{}\}}",expected.join(",")), |x,y| compare_math(x,y,context))
            .ok_or("unsupported comma-separated values")?;
    }
    if let Some(result) = crate::set_answers::compare(a, b, |x, y| compare_math(x, y, context)) {
        return result;
    }
    // Evaluated change-of-base answers may explicitly exclude logarithms.
    // Enforce that narrow representation contract before value equivalence;
    // otherwise log_3(9) bypasses the requested denominator evaluation.
    // Keep ordinary equivalent-logarithm questions and numeric spellings free.
    if forbids_logarithms(prompt) && contains_logarithm(a) {
        return Ok(false);
    }
    if prompt.to_lowercase().contains("ordered pair") {
        let expected = normalize_math(b);
        if let Some((bx, by)) = ordered_pair_coordinates(&expected) {
            let actual = normalize_math(a);
            let Some((ax, ay)) = ordered_pair_coordinates(&actual) else { return Ok(false); };
            // Keep coordinate order and each coordinate's normal exact/form
            // constraints; neither sorting nor textual tuple equality suffices.
            return Ok(compare_math_in_context(ax, bx, prompt, context)?
                && compare_math_in_context(ay, by, prompt, context)?);
        }
    }
    // A whole symbolic log-to-exponential conversion assesses all three roles.
    // Compare that representation directly; the expression parser does not
    // parse equalities, and a reversed equality has the same role assignment.
    if requests_power_form(prompt)
        && let Some(expected) = symbolic_power_equation_form(b)
    {
        return Ok(symbolic_power_equation_form(a).is_some_and(|actual| actual == expected));
    }
    // Repeated-product exercises assess the base/exponent representation,
    // rather than only its evaluated value. Grouping syntax is immaterial.
    if requests_power_form(prompt)
        && let Some(expected) = integer_power_form(b)
    {
        return Ok(integer_power_form(a).is_some_and(|actual| actual == expected));
    }
    // Log-to-exponential conversion must retain the supplied base even when
    // the requested exponent is fractional. Numeric equivalence alone would
    // accept a different base (25^(1/3) for 5^(2/3)) or a radical.
    if requests_power_form(prompt)
        && let Some(expected) = fractional_power_form(b, false)
    {
        return Ok(fractional_power_form(a, requires_reduced_fraction(prompt))
            .is_some_and(|actual| actual == expected));
    }
    if requires_answer_form(prompt) {
        let a = normalize_answer_form(a);
        let b = normalize_answer_form(b);
        if a == b {
            return Ok(true);
        }
        if permits_equivalent_decimal_numerals(prompt)
            && let (Some(a), Some(b)) = (plain_decimal_numeral(&a), plain_decimal_numeral(&b))
        {
            // Compare the submitted value exactly. Do not round it again or
            // accept fractions/expressions in place of the requested numeral.
            return Ok(a == b);
        }
        Ok(false)
    } else {
        if let Some(source) = derivative_source_function(prompt)
            && let Some(equal) = symbolic::compare_rational_on_source_domain(a, b, &source, context)?
        {
            return Ok(equal);
        }
        compare_math(a, b, context)
    }
}

fn forbids_logarithms(prompt: &str) -> bool {
    use std::sync::LazyLock;
    static NO_LOGS: LazyLock<regex::Regex> = LazyLock::new(|| {
        regex::Regex::new(r"(?i)\b(?:no|without)\s+logarithms?\b")
            .expect("valid logarithm-free answer instruction")
    });
    NO_LOGS.is_match(prompt)
}

fn contains_logarithm(answer: &str) -> bool {
    use std::sync::LazyLock;
    static LOG: LazyLock<regex::Regex> = LazyLock::new(|| {
        regex::Regex::new(r"(?i)(?:\\|\b)(?:log|ln)(?:\b|_)")
            .expect("valid logarithm token expression")
    });
    LOG.is_match(answer)
}

fn requests_power_form(prompt: &str) -> bool {
    use std::sync::LazyLock;
    static POWER_FORM: LazyLock<regex::Regex> = LazyLock::new(|| {
        regex::Regex::new(
            r"\b(?:(?:exponent|exponential|power)\s+form|power\s+notation|as\s+a\s+(?:single\s+)?power|using\s+exponents)\b",
        ).unwrap()
    });
    POWER_FORM.is_match(&prompt.to_lowercase())
}

fn ungroup_power_slot(mut text: &str) -> Option<&str> {
    loop {
        let closing = match text.as_bytes().first()? {
            b'{' => b'}',
            b'(' => b')',
            _ => return Some(text),
        };
        let mut stack = Vec::new();
        let mut end = None;
        for (index, byte) in text.bytes().enumerate() {
            match byte {
                b'{' => stack.push(b'}'),
                b'(' => stack.push(b')'),
                b'}' | b')' => {
                    if stack.pop()? != byte { return None; }
                    if stack.is_empty() { end = Some(index); break; }
                }
                _ => {}
            }
        }
        if closing != *text.as_bytes().last()? || end != Some(text.len() - 1) {
            return Some(text);
        }
        text = &text[1..text.len() - 1];
    }
}

/// A complete base^exponent=result equation whose three slots are single
/// symbolic variables. This deliberately handles representation, not general
/// equation equivalence. Compound expressions keep the existing parser path.
fn symbolic_power_equation_form(value: &str) -> Option<(char, char, char)> {
    fn variable(text: &str) -> Option<char> {
        let text = ungroup_power_slot(text)?;
        let mut chars = text.chars();
        let variable = chars.next()?;
        (variable.is_ascii_alphabetic() && chars.next().is_none()).then_some(variable)
    }
    fn roles(power: &str, result: &str) -> Option<(char, char, char)> {
        let power = ungroup_power_slot(power)?;
        let (base, exponent) = power.split_once('^')?;
        Some((variable(base)?, variable(exponent)?, variable(result)?))
    }
    let normalized = normalize_math(value);
    let equation = ungroup_power_slot(&normalized)?;
    let (left, right) = equation.split_once('=')?;
    roles(left, right).or_else(|| roles(right, left))
}

/// A direct integer base and exponent, allowing harmless TeX/parenthesis groups.
/// Do not evaluate expressions inside either slot: 7^(2+3) has not supplied
/// the factor count, and 16807 or 49^(5/2) has lost the intended representation.
/// Other canonical answer shapes retain their existing comparison semantics.
fn integer_power_form(value: &str) -> Option<(num_bigint::BigInt, num_bigint::BigInt)> {
    fn integer(text: &str) -> Option<num_bigint::BigInt> {
        let text = ungroup_power_slot(text)?;
        let digits = text.strip_prefix('-').or_else(|| text.strip_prefix('+')).unwrap_or(text);
        if digits.is_empty() || !digits.bytes().all(|c| c.is_ascii_digit()) { return None; }
        text.parse().ok()
    }
    let normalized = normalize_math(value);
    let text = ungroup_power_slot(&normalized)?;
    let (base, exponent) = text.split_once('^')?;
    Some((integer(base)?, integer(exponent)?))
}

/// A literal integer base with a literal nonintegral rational exponent.
/// Normalize TeX/slash fraction spelling and harmless grouping, but do not
/// evaluate arithmetic in the base or exponent or convert a radical to a power.
fn fractional_power_form(value: &str, reduced_exponent: bool) -> Option<(num_bigint::BigInt, num_rational::BigRational)> {
    let normalized = normalize_math(value);
    let text = ungroup_power_slot(&normalized)?;
    let (base, exponent) = text.split_once('^')?;
    let base = ungroup_power_slot(base)?;
    let digits = base.strip_prefix('-').or_else(|| base.strip_prefix('+')).unwrap_or(base);
    if digits.is_empty() || !digits.bytes().all(|c| c.is_ascii_digit()) { return None; }
    let base = base.parse().ok()?;
    // 5^2/3 means (5^2)/3, not 5^(2/3). A bare TeX fraction is one macro.
    if !exponent.starts_with(['{', '(']) && !exponent.starts_with(r"\frac") { return None; }
    let exponent = ungroup_power_slot(exponent)?;
    let exponent = if let Some(fraction) = normalize_fraction_form(exponent) {
        let fraction = fraction.strip_prefix(r"\frac{")?.strip_suffix('}')?;
        let (numerator, denominator) = fraction.split_once("}{")?;
        let numerator: num_bigint::BigInt = numerator.parse().ok()?;
        let denominator: num_bigint::BigInt = denominator.parse().ok()?;
        let value = num_rational::BigRational::new(numerator.clone(), denominator.clone());
        // Value equality must not discard an explicit lowest-terms instruction.
        // normalize_fraction_form preserves the submitted integer pair while
        // accepting the UI's TeX and slash spellings.
        if reduced_exponent && (value.numer() != &numerator || value.denom() != &denominator) {
            return None;
        }
        value
    } else {
        if reduced_exponent { return None; }
        // A literal decimal such as 0.500 preserves the same exponent slot as
        // 1/2. Do not evaluate compound expressions or change the supplied base.
        plain_decimal_numeral(exponent)?
    };
    if exponent.is_integer() { return None; }
    Some((base, exponent))
}

fn requires_reduced_fraction(prompt: &str) -> bool {
    use std::sync::LazyLock;
    static REDUCED: LazyLock<regex::Regex> = LazyLock::new(|| {
        regex::Regex::new(r"(?i)\b(?:simplest\s+form|lowest\s+terms|reduced\s+fraction)\b")
            .expect("valid reduced fraction instruction")
    });
    REDUCED.is_match(prompt)
}

fn plain_decimal_numeral(text: &str) -> Option<num_rational::BigRational> {
    let unsigned = text.strip_prefix('-').or_else(|| text.strip_prefix('+')).unwrap_or(text);
    let mut digits = 0;
    let mut points = 0;
    for c in unsigned.bytes() {
        if c.is_ascii_digit() { digits += 1; }
        else if c == b'.' { points += 1; }
        else { return None; }
    }
    if digits == 0 || points > 1 { return None; }
    decimal_number(text).ok()
}

fn permits_equivalent_decimal_numerals(prompt: &str) -> bool {
    use std::sync::LazyLock;
    static ROUNDING: LazyLock<regex::Regex> = LazyLock::new(|| {
        regex::Regex::new(r"\b(?:round(?:ed|ing)?|decimal\s+places?)\b").unwrap()
    });
    static EXPLICIT_FORM: LazyLock<regex::Regex> = LazyLock::new(|| {
        regex::Regex::new(concat!(
            r"\b(?:significant\s+(?:figures?|digits?)|simplest\s+form|lowest\s+terms|reduced\s+fraction|",
            r"(?:include|retain|keep|show|write|display|use)\s+(?:the\s+|all\s+|any\s+)?trailing\s+zero(?:e?s)?|",
            r"exactly\s+(?:\d+|one|two|three|four|five|six)\s+(?:decimal\s+places?|digits?\s+after\s+the\s+decimal))\b"
        )).unwrap()
    });
    let prompt = prompt.to_lowercase();
    ROUNDING.is_match(&prompt) && !EXPLICIT_FORM.is_match(&prompt)
}

fn requires_answer_form(prompt: &str) -> bool {
    use std::sync::LazyLock;
    // An exact-answer instruction is not a rounding instruction. Remove only
    // the negated rounding phrase, so a separate instruction to round the final
    // answer or to give a reduced fraction still constrains its representation.
    static NEGATED_ROUNDING: LazyLock<regex::Regex> = LazyLock::new(|| {
        regex::Regex::new(
            r"\b(?:do\s+not|don['’]t|without|avoid|no|not(?:\s+be)?)\s+round(?:ed|ing)?\b",
        )
        .expect("valid negated rounding expression")
    });
    static REQUIRED_FORM: LazyLock<regex::Regex> = LazyLock::new(|| {
        regex::Regex::new(
            r"\b(?:round(?:ed|ing)?|decimal\s+places?|digits?\s+after\s+(?:the\s+)?decimal|significant\s+(?:figures?|digits?)|simplest\s+form|lowest\s+terms|reduced\s+fraction)\b",
        )
        .expect("valid answer form expression")
    });
    let prompt = prompt.to_lowercase();
    REQUIRED_FORM.is_match(&NEGATED_ROUNDING.replace_all(&prompt, ""))
}

/// Prompt and owning KP wording determine the interpretation of i, e and indices.
pub fn comparison_context(prompt: &str, titles: &[String]) -> symbolic::Context {
    let wording = std::iter::once(prompt.to_owned())
        .chain(titles.iter().cloned())
        .collect::<Vec<_>>()
        .join(" ")
        .to_lowercase();
    // Rendered e^... and constant exponents such as x^{e} denote Euler's
    // constant. In this setting 6e-6 is an
    // implicit product followed by subtraction, not a decimal exponent.
    static NATURAL_EXPONENTIAL: std::sync::LazyLock<regex::Regex> = std::sync::LazyLock::new(|| {
        regex::Regex::new(r"(?:^|[^a-z\\])e(?:\s*\})?\s*\^|\^\s*\{?\s*e(?:$|[^a-z])").expect("valid natural exponential expression")
    });
    // Read only explicit declarations in prompt prose, never a comparison to
    // be decided, a worked solution, or the owning KP's title. Restrict each
    // protected math span to a single strict sign assertion.
    static DECLARED_SIGN: std::sync::LazyLock<regex::Regex> = std::sync::LazyLock::new(|| {
        regex::Regex::new(r"\$\s*([a-z])\s*(>|<|\\gt|\\lt)\s*0\s*[.,;]?\s*\$")
            .expect("valid explicit sign declaration")
    });
    // A declaration may close a comma-separated list of premises, e.g.
    // "where $x=r\cos\theta$, $y=r\sin\theta$, and $r>0$". Match each
    // sign span separately so earlier, conflicting signs are never swallowed
    // by a greedy list match. An unanchored "and" alone is not a premise.
    static DECLARATION_PREFIX: std::sync::LazyLock<regex::Regex> = std::sync::LazyLock::new(|| {
        regex::Regex::new(r"(?i:\b(?:with|where|given that|assuming|assume|for))\s+(?:\$[^$\n]+\$\s*,\s*(?:(?i:and)\s+)?)*$")
            .expect("valid explicit declaration list prefix")
    });
    let mut positive_variables = 0;
    let mut negative_variables = 0;
    for capture in DECLARED_SIGN.captures_iter(prompt) {
        let span = capture.get(0).expect("whole sign declaration");
        let before = &prompt[..span.start()];
        if !DECLARATION_PREFIX.is_match(before) { continue; }
        let after = prompt[span.end()..].trim_start().trim_start_matches(',').trim_start();
        // A hypothetical/disjunctive or negated clause supplies no assumption.
        let clause = before.rsplit(['.', '!', '?', ';']).next().unwrap_or("");
        if clause.split_whitespace().any(|word| matches!(word, "not" | "never" | "whether" | "unless" | "or" | "if"))
            || after.starts_with("or ") || after.starts_with("and/or ")
        { continue; }
        let bit = 1_u32 << (capture[1].as_bytes()[0] - b'a');
        if matches!(&capture[2], ">" | r"\gt") { positive_variables |= bit; }
        else { negative_variables |= bit; }
    }
    let conflict = positive_variables & negative_variables;
    positive_variables &= !conflict;
    negative_variables &= !conflict;
    symbolic::Context {
        positive_variables,
        negative_variables,
        natural_exponential: NATURAL_EXPONENTIAL.is_match(&wording)
            || wording.contains(r"\exp"),
        symbolic_i: ["riemann", "sigma", "\\sum", "vector"]
            .iter()
            .any(|v| wording.contains(v)),
        integer_indices: [
            "riemann",
            "sigma",
            "\\sum",
            "series",
            "sequence",
            "recursive",
            "partial sum",
        ]
        .iter()
        .any(|v| wording.contains(v)),
    }
}

fn math_context(s: &EntitySnapshot, question: u64) -> Result<symbolic::Context> {
    let wording = s
        .entity(question)?
        .get("question/problem")
        .and_then(Value::as_str)
        .unwrap_or("")
        .to_lowercase();
    let mut titles = vec![];
    for kp in s.owners(question, "knowledge-point/questions")? {
        if let Some(title) = s
            .entity(kp)?
            .get("knowledge-point/title")
            .and_then(Value::as_str)
        {
            titles.push(title.to_owned());
        }
    }
    Ok(comparison_context(&wording, &titles))
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

pub(crate) fn learning_runtime(
    s: &EntitySnapshot,
    learner: u64,
    at: DateTime<Utc>,
) -> Result<LoadedRuntime> {
    let policies = s.entities.with_attribute("policy/id");
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
        "db/ident",
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
        .with_attribute_prefixes(&runtime_prefixes)
        .into_iter()
        .map(|eid| (eid, s.entities[&eid].clone()))
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
    for owner in s.entities.with_attribute("learner/knowledge-profile") {
        for progress in s.refs(owner, "learner/knowledge-profile")? {
            progress_owners.entry(progress).or_default().push(owner);
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
    let seeded=loaded.engine.states.get(&loaded.learner).into_iter().flat_map(|states|states.values())
        .fold(f64::NEG_INFINITY,|latest,state|latest.max(state.memory_at)
            .max(state.last_direct_at.unwrap_or(f64::NEG_INFINITY)));
    let latest=logical_learning_clock(s,learner,seeded)?;
    if latest.is_finite(){loaded.engine.latest.insert(loaded.learner.clone(),latest);}
    else{loaded.engine.latest.remove(&loaded.learner);}
    Ok(loaded)
}

// Delayed transaction publication must not make the next acknowledged answer
// appear to predate the learner's previous work. Keep progress anchors intact;
// tasks with explicit clocks contribute their logical intervals/finish instead
// of save-time status assertions. Legacy tasks retain their original history.
fn logical_learning_clock(s:&EntitySnapshot,learner:u64,mut latest:f64)->Result<f64>{
    let mut legacy=BTreeSet::new();
    for task in s.refs(learner,"learner/activity")? {
        let members=s.refs(task,"learner-task/items")?;
        let mut logical=false;
        for item in &members {
            for period in s.refs(*item,"task-item/working-periods")? {
                logical=true;
                let record=s.entity(period)?;
                latest=latest.max(crate::schema::instant_days(record.get("working-period/started-at")
                    .ok_or("working period needs a start")?)?);
                if let Some(value)=record.get("working-period/ended-at"){
                    latest=latest.max(crate::schema::instant_days(value)?);
                }
            }
        }
        if logical {
            if let Some(finished)=s.entity(task)?.get("learner-task/finished-at") {
                latest=latest.max(crate::schema::instant_days(finished)?);
            }
        }else{
            legacy.insert(task);
            legacy.extend(members);
        }
    }
    for event in &s.status_history {
        if !legacy.contains(&event.entity){continue;}
        // Queue offers are eligibility bookkeeping, rather than observations.
        if event.attribute=="learner-task/status" && matches!(s.ident(&event.value)?.as_str(),
            "learner-task.status/locked"|"learner-task.status/unlocked") {continue;}
        latest=latest.max(crate::schema::instant_days(&event.at)?);
    }
    Ok(latest)
}

#[cfg(test)]
mod logical_clock_tests {
    use super::*;
    #[test]
    fn saved_status_times_do_not_override_logical_observations_or_progress_anchors(){
        let mut s=EntitySnapshot::from_json(&json!({"basis_t":3,"entities":{
            "1":{"learner/id":"test","learner/activity":[2,5]},
            "2":{"learner-task/id":"saved","learner-task/status":11,"learner-task/items":[3],"learner-task/finished-at":{"$instant":25000}},
            "3":{"task-item/id":"answer","task-item/status":12,"task-item/working-periods":[4]},
            "4":{"working-period/id":"logical","working-period/started-at":{"$instant":10000},"working-period/ended-at":{"$instant":20000}},
            "5":{"learner-task/id":"offered","learner-task/status":13},
            "10":{"db/ident":"learner-task.status/started"},
            "11":{"db/ident":"learner-task.status/completed"},
            "12":{"db/ident":"task-item.status/correct"},
            "13":{"db/ident":"learner-task.status/unlocked"}
        },"status_history":[
            {"entity":2,"attribute":"learner-task/status","value":10,"t":1,"at":{"$instant":120000}},
            {"entity":2,"attribute":"learner-task/status","value":11,"t":2,"at":{"$instant":130000}},
            {"entity":3,"attribute":"task-item/status","value":12,"t":2,"at":{"$instant":130000}},
            {"entity":5,"attribute":"learner-task/status","value":13,"t":3,"at":{"$instant":140000}}
        ]})).unwrap();
        let days=|seconds:f64|seconds/86400.;
        assert_eq!(logical_learning_clock(&s,1,f64::NEG_INFINITY).unwrap(),days(25.));
        assert_eq!(logical_learning_clock(&s,1,days(35.)).unwrap(),days(35.));
        // A task without explicit periods still establishes its real clock.
        s.entities.get_mut(&5).unwrap().insert("learner-task/status".into(),json!(10));
        s.status_history.last_mut().unwrap().value=json!(10);
        assert_eq!(logical_learning_clock(&s,1,days(35.)).unwrap(),days(140.));
    }
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
    if crate::retrieval::supported(s, activity)? {
        return crate::retrieval::credit(
            s, learner, activity, question, correct, completed, event_id, at,
        );
    }
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
    if completed && correct && s.refs(learner, "learner/queue")?.contains(&topic_eid) {
        // Queue membership ends with successful learning, in the same guarded
        // transaction as the completion and mastery update. Targets are retained.
        forms.push(json!([crate::schema::keyword("db/retract"), learner, crate::schema::keyword("learner/queue"), topic_eid]));
    }
    Ok(forms)
}

#[cfg(test)]
pub(crate) mod tests {
    use super::*;
    use crate::core::Policy;

    #[test]
    fn whole_circle_equations_are_admitted_and_graded_without_response_writes() {
        let mut s = fixture();
        s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!("Find the Cartesian equation of the circle."));
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("(x-3)^{2}+{y}^{2}=9"));
        validate_question(&s, 100).unwrap();
        for value in ["(x-3)^2+y^2=9", "x^2-6x+y^2=0", "9=y^2+(x-3)^2"] {
            assert_eq!(grade(&s, 100, &BTreeMap::from([(200, value.to_owned())])), Ok(true));
        }
        for value in ["(x-4)^2+y^2=9", "(x-3)^2+y^2=10", "987654321"] {
            assert_eq!(grade(&s, 100, &BTreeMap::from([(200, value.to_owned())])), Ok(false));
        }
        assert!(s.refs(1, "learner/activity").unwrap().is_empty());
    }


    #[test]
    fn ordered_pair_blanks_preserve_coordinate_order_and_equivalence() {
        let mut s = fixture();
        s.entities.get_mut(&200).unwrap().insert("answer-field/type".into(), json!("answer-field.type/blank"));
        s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!("Enter the point as an ordered pair (x,y)."));
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("(-2,3)"));
        for accepted in ["(-2,3)", r"\left(-2,\frac{6}{2}\right)", "(-(1+1),9/3)"] {
            assert_eq!(grade_field(&s, 100, 200, accepted), Ok(true), "{accepted}");
        }
        for rejected in ["(3,-2)", "(-2,-3)", "(0,2)", "-2,3", "(-2,3,4)", "(-2,)", "[-2,3]", "(-2,3)+0"] {
            assert_eq!(grade_field(&s, 100, 200, rejected), Ok(false), "{rejected}");
        }
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("(1/2,3)"));
        s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!("Enter an ordered pair in simplest form."));
        assert_eq!(grade_field(&s, 100, 200, r"(\frac12,3)"), Ok(true));
        assert_eq!(grade_field(&s, 100, 200, "(2/4,3)"), Ok(false));
        // Domain restrictions still apply inside a coordinate.
        assert!(compare_math_in_context("(x/x,3)", "(1,3)", "ordered pair", symbolic::Context::default()).is_err());
        // Scalar answers in pair-related prompts keep the ordinary expression path.
        assert_eq!(compare_math_in_context("4/2", "2", "ordered pair coordinate", symbolic::Context::default()), Ok(true));
        assert!(compare_math_in_context("(-2,3)", "(-2,3)", "interval", symbolic::Context::default()).is_err());
    }

    fn id(n: u64) -> String {
        format!("00000000-0000-0000-0000-{n:012}")
    }
    fn put(entities: &mut BTreeMap<u64, serde_json::Map<String, Value>>, eid: u64, value: Value) {
        entities.insert(eid, value.as_object().unwrap().clone());
    }
    pub(crate) fn fixture() -> EntitySnapshot {
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
            "answer-field.type/checkbox",
            "answer-field.type/free",
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

    fn multistep_parts(s: &mut EntitySnapshot, questions: &[u64]) {
        let mut steps = vec![];
        for (index, question) in questions.iter().enumerate() {
            let step = 800 + index as u64;
            put(
                &mut s.entities,
                step,
                json!({"step/id":id(step),"step/content":question}),
            );
            steps.push(step);
        }
        put(
            &mut s.entities,
            850,
            json!({"multistep/id":id(850),"multistep/steps":steps}),
        );
    }

    #[test]
    fn lesson_routes_survive_learner_updates_and_invalidate_on_route_or_content_edits() {
        let mut s = fixture();
        assert_eq!(lesson_steps(&s, 20).unwrap().len(), 2);
        s.replace_records(BTreeMap::from([
            (900, json!({"task-item/content":100,"task-item/status":1010}).as_object().unwrap().clone()),
            (901, json!({"step/content":101}).as_object().unwrap().clone()),
            (902, json!({"activity/steps":[901]}).as_object().unwrap().clone()),
        ]), s.basis_t+1).unwrap();
        assert!(s.entities.lesson_route(20).is_some());
        let mut shorter = s.clone();
        let mut activity = shorter.entities[&20].clone();
        activity.insert("activity/steps".into(), json!([30]));
        let mut first = shorter.entities[&30].clone();
        first.remove("step/next");
        shorter.replace_records(BTreeMap::from([(20, activity), (30, first)]), shorter.basis_t+1).unwrap();
        assert_eq!(lesson_steps(&shorter, 20).unwrap().len(), 1);
        assert!(shorter.owners(31, "activity/steps").unwrap().is_empty());
        let mut changed = s.clone();
        let mut step = changed.entities[&30].clone();
        step.insert("step/next".into(), json!(30));
        changed.replace_records(BTreeMap::from([(30, step)]), changed.basis_t+1).unwrap();
        assert!(changed.entities.lesson_route(20).is_none());
        assert!(lesson_steps(&changed, 20).is_err());
        assert!(s.entities.lesson_route(20).is_some());
        assert_eq!(lesson_steps(&s, 20).unwrap().len(), 2);
        let mut example = s.entities[&42].clone();
        example.insert("question/worked-solution".into(), json!(""));
        s.replace_records(BTreeMap::from([(42, example)]), s.basis_t+1).unwrap();
        assert!(s.entities.lesson_route(20).is_none());
        assert!(lesson_steps(&s, 20).is_err());
    }

    #[test]
    fn question_validation_survives_answers_and_completion_but_tracks_authored_edits() {
        let mut s = fixture();
        validate_practice_question(&s, 100).unwrap();
        assert!(s.entities.question_validated(100));
        for (eid, record) in [
            (900, json!({"task-item/status":1000+10,"task-item/content":100})),
            (901, json!({"learner-task/status":1000+15,"learner-task/activity":20})),
            (902, json!({"progress/memory":0.75,"progress/repetitions":3.0})),
        ] {
            s.replace_records(BTreeMap::from([(eid, record.as_object().unwrap().clone())]), s.basis_t+1).unwrap();
            assert!(s.entities.question_validated(100));
            assert!(s.entities.practice_question_validated(100));
            validate_practice_question(&s, 100).unwrap();
        }
        // The cache of a speculative clone must not change its source.
        let mut changed = s.clone();
        let mut field = changed.entities[&200].clone();
        field.remove("answer-field/correct");
        changed.replace_records(BTreeMap::from([(200, field)]), changed.basis_t+1).unwrap();
        assert!(!changed.entities.question_validated(100));
        assert!(validate_practice_question(&changed, 100).is_err());
        assert!(s.entities.question_validated(100));
        validate_practice_question(&s, 100).unwrap();

        s.replace_records(BTreeMap::from([
            (940, json!({"step/content":100}).as_object().unwrap().clone()),
            (941, json!({"activity/steps":[940]}).as_object().unwrap().clone()),
        ]), s.basis_t+1).unwrap();
        assert!(s.entities.practice_question_validated(100));
        // Structural membership is checked even when the question itself is unchanged.
        s.replace_records(BTreeMap::from([
            (950, json!({"step/content":100}).as_object().unwrap().clone()),
            (951, json!({"multistep/steps":[950]}).as_object().unwrap().clone()),
        ]), s.basis_t+1).unwrap();
        assert!(s.entities.question_validated(100));
        assert!(validate_practice_question(&s, 100).is_err());
        validate_practice_question(&s, 101).unwrap();
        s.replace_records(BTreeMap::from([
            (950, json!({"step/content":101}).as_object().unwrap().clone()),
        ]), s.basis_t+1).unwrap();
        assert!(validate_practice_question(&s, 101).is_err());
        validate_practice_question(&s, 102).unwrap();
        s.replace_records(BTreeMap::from([
            (952, json!({"assigned-problem/content":102}).as_object().unwrap().clone()),
            (950, json!({"step/content":952}).as_object().unwrap().clone()),
        ]), s.basis_t+1).unwrap();
        assert!(validate_practice_question(&s, 102).is_err());

        let mut question = s.entities[&100].clone();
        question.insert("question/retired".into(), json!(true));
        s.replace_records(BTreeMap::from([(100, question)]), s.basis_t+1).unwrap();
        assert!(!s.entities.question_validated(100));
        assert!(validate_practice_question(&s, 100).is_err());
        // Direct fixture edits and retractions also invalidate validation.
        validate_question(&s, 101).unwrap();
        s.entities.get_mut(&201).unwrap().remove("answer-field/correct");
        assert!(!s.entities.question_validated(101));
        assert!(validate_question(&s, 101).is_err());
        validate_question(&s, 102).unwrap();
        s.replace_records(BTreeMap::from([(202, serde_json::Map::new())]), s.basis_t+1).unwrap();
        assert!(validate_question(&s, 102).is_err());
    }

    #[test]
    fn retired_questions_leave_fresh_pools_but_keep_saved_grading_and_lesson_history() {
        let mut s = fixture();
        put(&mut s.entities, 1100, json!({"db/ident":"question.difficulty/easy"}));
        for q in 100..105 {
            s.entities.get_mut(&q).unwrap().insert("question/difficulty".into(), json!(1100));
        }
        for q in 100..104 {
            s.entities.get_mut(&q).unwrap().insert("question/retired".into(), json!(true));
        }
        assert!(validate_response_question(&s, 100).is_ok());
        assert!(grade(&s, 100, &BTreeMap::from([(200, "1/2".into())])).unwrap());
        assert!(validate_practice_question(&s, 100).is_err());
        assert_eq!(crate::inventory::practice_pool(&s, &[41], &BTreeSet::new()).unwrap(), [104]);
        assert_eq!(crate::assessment_sampling::pool(&s, &[41], &BTreeSet::new()).unwrap(), [104]);
        present(&mut s, 40, "completed");
        present(&mut s, 42, "completed");
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(104));
        let saved = present(&mut s, 100, "started");
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(100));
        s.entities.get_mut(&saved).unwrap().insert("task-item/status".into(), json!("task-item.status/correct"));
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(104));
        s.entities.get_mut(&100).unwrap().insert("question/retired".into(), json!(false));
        assert!(validate_practice_question(&s, 100).is_ok());
    }

    #[test]
    fn adaptive_practice_and_inventory_exclude_multistep_parts_but_grade_saved_answers() {
        let mut s = fixture();
        put(
            &mut s.entities,
            1100,
            json!({"db/ident":"question.difficulty/easy"}),
        );
        for q in 100..105 {
            s.entities
                .get_mut(&q)
                .unwrap()
                .insert("question/difficulty".into(), json!(1100));
        }
        multistep_parts(&mut s, &[100, 101, 102, 103]);
        assert!(validate_response_question(&s, 100).is_ok());
        assert!(grade(&s, 100, &BTreeMap::from([(200, "1/2".into())])).unwrap());
        assert!(validate_practice_question(&s, 100).is_err());
        assert_eq!(
            crate::inventory::practice_pool(&s, &[41], &BTreeSet::new()).unwrap(),
            [104]
        );
        assert_eq!(
            crate::assessment_sampling::pool(&s, &[41], &BTreeSet::new()).unwrap(),
            [104]
        );
        assert_eq!(
            crate::inventory::lesson_shortages(&s, &[41], &BTreeSet::new()).unwrap(),
            [(41, 1)]
        );
        present(&mut s, 40, "completed");
        present(&mut s, 42, "completed");
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(104));
        // A presentation saved before the policy change remains answerable;
        // after it completes the next draw still chooses standalone content.
        let saved = present(&mut s, 100, "started");
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(100));
        s.entities
            .get_mut(&saved)
            .unwrap()
            .insert("task-item/status".into(), json!("task-item.status/correct"));
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(104));
    }

    #[test]
    fn an_all_multistep_practice_pool_is_a_shortage_not_a_draw_or_failure() {
        let mut s = fixture();
        multistep_parts(&mut s, &[100, 101, 102, 103, 104]);
        assert_eq!(
            crate::inventory::lesson_shortages(&s, &[41], &BTreeSet::new()).unwrap(),
            [(41, 0)]
        );
        present(&mut s, 40, "completed");
        present(&mut s, 42, "completed");
        let p = continuation_state(&s, 20, &items(&s), false, false).unwrap();
        assert_eq!(p.next, None);
        assert_eq!(p.shortage, Some(31));
        assert!(!p.failed);
        assert!(!p.passed);
    }

    #[test]
    fn explicit_multistep_leaf_routes_cannot_start_but_saved_presentations_can_finish() {
        let mut s = fixture();
        multistep_parts(&mut s, &[100]);
        s.entities
            .get_mut(&20)
            .unwrap()
            .insert("activity/steps".into(), json!([31]));
        s.entities
            .get_mut(&20)
            .unwrap()
            .insert("activity/first-step".into(), json!(31));
        s.entities
            .get_mut(&31)
            .unwrap()
            .insert("step/content".into(), json!(100));
        assert!(first_content(&s, 20, 1).unwrap_err().contains("multistep"));
        let saved = present(&mut s, 100, "started");
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(100));
        s.entities
            .get_mut(&saved)
            .unwrap()
            .insert("task-item/status".into(), json!("task-item.status/correct"));
        assert!(lesson_passed(&s, 20, &items(&s)).unwrap());
    }

    #[test]
    fn supply_deferral_continues_later_skills_and_resumes_only_unfinished_practice() {
        let mut s = fixture();
        s.entities
            .get_mut(&41)
            .unwrap()
            .insert("knowledge-point/questions".into(), json!([100, 101]));
        s.entities
            .get_mut(&31)
            .unwrap()
            .insert("step/next".into(), json!(32));
        s.entities
            .get_mut(&20)
            .unwrap()
            .insert("activity/steps".into(), json!([30, 31, 32]));
        put(
            &mut s.entities,
            32,
            json!({"step/id":id(32),"step/content":44}),
        );
        put(
            &mut s.entities,
            44,
            json!({"knowledge-point/id":id(44),"knowledge-point/canonical-example":43,"knowledge-point/questions":[102,103]}),
        );
        put(
            &mut s.entities,
            43,
            json!({"question/id":id(43),"question/problem":"Later example","question/worked-solution":"Explanation"}),
        );
        s = EntitySnapshot::new(s.entities.clone().into(), s.basis_t).unwrap();
        present(&mut s, 40, "completed");
        present(&mut s, 42, "completed");
        present(&mut s, 100, "correct");
        let blocked = present(&mut s, 101, "incorrect");
        let p = continuation_state(&s, 20, &items(&s), false, false).unwrap();
        assert_eq!(p.shortage, Some(31));
        let p = continuation_state(&s, 20, &items(&s), false, true).unwrap();
        assert_eq!(p.next, Some(43));
        assert_eq!(p.deferred, vec![31]);
        s.entities
            .get_mut(&blocked)
            .unwrap()
            .insert("task-item/deferred-step".into(), json!(31));
        present(&mut s, 43, "completed");
        present(&mut s, 102, "correct");
        present(&mut s, 103, "correct");
        let p = position(&s, 20, &items(&s)).unwrap();
        assert_eq!(p.next, None);
        assert!(!p.passed);
        assert_eq!(p.deferred, vec![31]);
        assert_eq!(lesson_xp(&s, 20, &items(&s), 10).unwrap(), 0);
        assert_eq!(deferred_resume_step(&s, 20, &items(&s)).unwrap(), None);
        s.entities.get_mut(&9).unwrap().insert(
            "learner-task/status".into(),
            json!("learner-task.status/paused"),
        );
        assert!(plan_candidates(&s, 1, 5, Utc::now()).unwrap().is_empty());
        s.entities
            .get_mut(&41)
            .unwrap()
            .insert("knowledge-point/questions".into(), json!([100, 101, 104]));
        assert_eq!(deferred_resume_step(&s, 20, &items(&s)).unwrap(), Some(31));
        assert_eq!(
            plan_candidates(&s, 1, 5, Utc::now()).unwrap()[0].activity,
            20
        );
        let resumed = present(&mut s, 42, "completed");
        s.entities
            .get_mut(&resumed)
            .unwrap()
            .insert("task-item/resumed-step".into(), json!(31));
        let again = present(&mut s, 104, "correct");
        assert_eq!(
            continuation_state(&s, 20, &items(&s), false, false)
                .unwrap()
                .shortage,
            Some(31)
        );
        s.entities
            .get_mut(&again)
            .unwrap()
            .insert("task-item/deferred-step".into(), json!(31));
        assert_eq!(position(&s, 20, &items(&s)).unwrap().deferred, vec![31]);
        // A second return preserves the new one-answer streak.
        let mut q = s.entities[&104].clone();
        q.insert("question/id".into(), json!(id(105)));
        put(&mut s.entities, 105, Value::Object(q));
        s.entities.get_mut(&41).unwrap().insert(
            "knowledge-point/questions".into(),
            json!([100, 101, 104, 105]),
        );
        let return_again = present(&mut s, 42, "completed");
        s.entities
            .get_mut(&return_again)
            .unwrap()
            .insert("task-item/resumed-step".into(), json!(31));
        assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(105));
        present(&mut s, 105, "correct");
        assert!(lesson_passed(&s, 20, &items(&s)).unwrap());
        assert!(position(&s, 20, &items(&s)).unwrap().deferred.is_empty());
        assert_eq!(items(&s).len(), 11); // Original history plus returns to only the deferred skill.
    }

    #[test]
    fn empty_practice_pool_can_be_deferred_after_example_without_inventing_a_question() {
        let mut s = fixture();
        s.entities
            .get_mut(&41)
            .unwrap()
            .insert("knowledge-point/questions".into(), json!([]));
        present(&mut s, 40, "completed");
        let example = present(&mut s, 42, "started");
        let p = continuation_state(&s, 20, &items(&s), true, false).unwrap();
        assert_eq!(p.shortage, Some(31));
        let p = continuation_state(&s, 20, &items(&s), true, true).unwrap();
        assert_eq!(p.deferred, vec![31]);
        assert_eq!(p.next, None);
        assert!(!p.passed);
        assert_eq!(
            s.entities[&example]["task-item/status"],
            json!("task-item.status/started")
        );
        assert_eq!(items(&s).len(), 2);
    }

    #[test]
    fn deferral_is_rejected_while_fresh_questions_remain() {
        let mut s = fixture();
        present(&mut s, 40, "completed");
        present(&mut s, 42, "completed");
        assert!(
            continuation_state(&s, 20, &items(&s), false, true)
                .unwrap_err()
                .contains("only be deferred")
        );
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

    // Selection tests use a known foundation chain so their small topic graphs
    // exercise normal Study behavior above the production L30 boundary.
    fn study_planning_fixture(targets: &[u64]) -> EntitySnapshot {
        let mut s = planning_fixture(targets);
        let topics = s.entities.with_attribute("topic/id");
        for topic in 90000..90029 {
            let next = if topic == 90028 { topics.clone() } else { vec![topic + 1] };
            put(&mut s.entities, topic, json!({"topic/id":id(topic),"topic/next":next}));
        }
        put(&mut s.entities, 90029, json!({"progress/topic":90028,"progress/repetitions":1.0}));
        let mut profile = s.refs(1, "learner/knowledge-profile").unwrap();
        profile.push(90029);
        s.entities.get_mut(&1).unwrap().insert("learner/knowledge-profile".into(), json!(profile));
        s
    }

    fn planning_lesson(s: &mut EntitySnapshot, topic: u64, next: &[u64]) -> u64 {
        if s.entities.contains_key(&90028) {
            let mut next_topics = s.refs(90028, "topic/next").unwrap();
            next_topics.push(topic);
            s.entities.get_mut(&90028).unwrap().insert("topic/next".into(), json!(next_topics));
        }
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

    #[test]
    fn explicit_topic_planning_matches_manual_queue_override_without_editing_records() {
        let mut s = study_planning_fixture(&[]);
        planning_lesson(&mut s, 80, &[81]);
        planning_lesson(&mut s, 81, &[]);
        let at = Utc::now();
        for directed in [false, true] {
            s.entities.get_mut(&1).unwrap().insert("learner/self-directed".into(), json!(directed));
            for topic in [80, 81] {
                let before = s.entities.clone();
                let direct = selected_topic_candidates(&s, 1, 2, topic, at).unwrap();
                let mut overridden = s.clone();
                overridden.entities.get_mut(&1).unwrap().insert("learner/self-directed".into(), json!(true));
                overridden.entities.get_mut(&1).unwrap().insert("learner/queue".into(), json!([topic]));
                let expected = queue_candidates(&overridden, 1, 2, at).unwrap();
                assert_eq!(direct.iter().map(|p|p.activity).collect::<Vec<_>>(),
                    expected.iter().filter(|p|p.topic == topic).map(|p|p.activity).collect::<Vec<_>>());
                assert_eq!(s.entities, before);
            }
        }
    }

    #[test]
    fn focused_study_serves_only_direct_targets_in_both_study_modes() {
        let mut s = study_planning_fixture(&[82]);
        planning_lesson(&mut s, 80, &[81]);
        planning_lesson(&mut s, 81, &[82]);
        planning_lesson(&mut s, 82, &[]);
        planning_lesson(&mut s, 85, &[]);
        s.entities.get_mut(&1).unwrap().insert("learner/queue".into(), json!([85]));
        put(&mut s.entities, 700, json!({"learner-task/activity":10085,
            "learner-task/status":"learner-task.status/paused"}));
        s.entities.get_mut(&1).unwrap().insert("learner/activity".into(), json!([700]));
        assert!(study_lesson_scope(&s, 1).unwrap().contains(&80));
        s.focused_mode = true;
        let before = s.entities.clone();
        assert_eq!(study_lesson_scope(&s, 1).unwrap(), BTreeSet::from([82]));
        assert_eq!(selected_topic_candidates(&s, 1, 2, 85, Utc::now()).unwrap()[0].topic, 85);
        for directed in [true, false] {
            s.entities.get_mut(&1).unwrap().insert("learner/self-directed".into(), json!(directed));
            let plan = study_candidates(&s, 1, 2, Utc::now()).unwrap();
            assert_eq!(plan.iter().map(|p| p.topic).collect::<Vec<_>>(), [82]);
        }
        s.entities.get_mut(&1).unwrap().insert("learner/self-directed".into(), json!(true));
        assert_eq!(s.entities, before);
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(), json!([]));
        assert!(study_candidates(&s, 1, 2, Utc::now()).unwrap().is_empty());
        s.focused_mode = false;
        assert!(study_candidates(&s, 1, 2, Utc::now()).unwrap().iter().any(|p| p.topic == 85));
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
    fn study_excludes_l29_and_keeps_l30_and_l31_including_saved_attempts() {
        let mut s = planning_fixture(&[]);
        for topic in 500..531 {
            planning_lesson(&mut s, topic, &if topic < 530 { vec![topic + 1] } else { vec![] });
        }
        s.entities.get_mut(&1).unwrap().insert("learner/queue".into(), json!([528,529,530]));
        put(&mut s.entities, 600, json!({"learner-task/activity":10528,
            "learner-task/status":"learner-task.status/paused"}));
        put(&mut s.entities, 601, json!({"learner-task/activity":10530,
            "learner-task/status":"learner-task.status/started"}));
        put(&mut s.entities, 602, json!({"progress/topic":528,"progress/repetitions":1.0}));
        s.entities.get_mut(&1).unwrap().insert("learner/activity".into(), json!([600,601]));
        s.entities.get_mut(&1).unwrap().insert("learner/knowledge-profile".into(), json!([602]));
        s.entities.get_mut(&7).unwrap().insert("module/topics".into(), json!([528,529,530]));
        let before = s.entities.clone();
        for self_directed in [true, false] {
            s.entities.get_mut(&1).unwrap().insert("learner/self-directed".into(), json!(self_directed));
            let plan = study_candidates(&s, 1, 5, planning_time()).unwrap();
            assert_eq!(plan.iter().map(|p| p.activity).collect::<Vec<_>>(), [10530,10529]);
        }
        // A direct topic request remains available outside the Study queue.
        assert_eq!(selected_topic_candidates(&s,1,5,528,planning_time()).unwrap()[0].activity,10528);
        s.entities.get_mut(&1).unwrap().insert("learner/self-directed".into(), json!(true));
        assert_eq!(s.entities, before);
    }

    #[test]
    fn study_does_not_hide_assessments_with_topics_below_the_practice_floor() {
        let mut s = planning_fixture(&[]);
        put(&mut s.entities, 1100, json!({"db/ident":"activity.type/assessment"}));
        let mut s = EntitySnapshot::new(s.entities.into(), s.basis_t).unwrap();
        for topic in 500..531 {
            planning_lesson(&mut s, topic, &if topic < 530 { vec![topic + 1] } else { vec![] });
            put(&mut s.entities, 40000 + topic, json!({"knowledge-point/id":id(40000+topic),
                "knowledge-point/questions":[20000+topic]}));
            s.entities.get_mut(&topic).unwrap().insert("topic/knowledge-points".into(),json!([40000+topic]));
        }
        put(&mut s.entities, 700, json!({"activity/id":id(700),"activity/type":"activity.type/assessment",
            "activity/steps":[30529,30528],"activity/first-step":30529}));
        s.entities.get_mut(&30529).unwrap().insert("step/next".into(), json!(30528));
        let candidate = PlannedActivity { activity:700, topic:529, priority:11000.0,
            target_count:0, target_topics:vec![], remaining_topics:0,
            nearest_target_steps:None, due:None, reason:"Assessment".into() };
        assert_eq!(filter_study_layers(&s,vec![candidate.clone()]).unwrap().len(),1);
        s.entities.get_mut(&700).unwrap().insert("activity/steps".into(), json!([30529,30530]));
        s.entities.get_mut(&30529).unwrap().insert("step/next".into(), json!(30530));
        assert_eq!(filter_study_layers(&s,vec![candidate]).unwrap().len(),1);
    }

    #[test]
    fn study_scope_expands_both_selection_sets_exactly_two_graph_edges() {
        let mut s = study_planning_fixture(&[83]);
        for topic in 80..84 { planning_lesson(&mut s, topic, &if topic < 83 { vec![topic+1] } else { vec![] }); }
        for topic in 90..94 { planning_lesson(&mut s, topic, &if topic < 93 { vec![topic+1] } else { vec![] }); }
        planning_lesson(&mut s, 99, &[]); // Unrelated available course work.
        s.entities.get_mut(&1).unwrap().insert("learner/queue".into(), json!([93]));
        let before = s.entities.clone();
        let scope = BTreeSet::from([81,82,83,91,92,93]);
        assert_eq!(study_lesson_scope(&s,1).unwrap(), scope);
        let plan = study_candidates(&s,1,5,planning_time()).unwrap();
        assert_eq!(plan.iter().map(|p|p.topic).collect::<BTreeSet<_>>(), scope);
        assert!(plan.iter().all(|p| p.nearest_target_steps.unwrap() <= 2));
        assert_eq!(s.entities, before);
        // Removing one source only removes its own branch; an empty selection
        // never falls back to unrelated course lessons or deeper prerequisites.
        s.entities.get_mut(&1).unwrap().insert("learner/queue".into(),json!([]));
        assert_eq!(study_lesson_scope(&s,1).unwrap(),BTreeSet::from([81,82,83]));
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(),json!([]));
        assert!(study_candidates(&s,1,5,planning_time()).unwrap().is_empty());
    }

    #[test]
    fn scoped_lessons_bypass_unknown_graph_and_skill_prerequisites() {
        let mut s = study_planning_fixture(&[83]);
        for topic in 80..84 { planning_lesson(&mut s,topic,&if topic<83 {vec![topic+1]} else {vec![]}); }
        planning_lesson(&mut s,99,&[]);
        put(&mut s.entities,900,json!({"knowledge-point/id":id(900),
            "knowledge-point/key-prerequisites":[99]}));
        s.entities.get_mut(&81).unwrap().insert("topic/knowledge-points".into(),json!([900]));
        // Ignore supply in this test so it isolates mastery from content checks.
        let plan=plan_candidates_in_scope(&s,1,5,planning_time(),0,true,StudyScope::Queue).unwrap();
        assert_eq!(plan.iter().map(|p|p.topic).collect::<BTreeSet<_>>(),BTreeSet::from([81,82,83]));
        assert!(!study_lesson_scope(&s,1).unwrap().contains(&99));
        // Course mode keeps its independent prerequisite gate.
        s.entities.get_mut(&7).unwrap().insert("module/topics".into(),json!([81,82,83]));
        assert!(engine_candidates(&s,1,5,planning_time()).unwrap().is_empty());
    }

    #[test]
    fn scoped_lessons_use_actual_learning_not_ancestor_inference_or_faded_bands() {
        let mut s=study_planning_fixture(&[83]);
        for topic in 80..84 {planning_lesson(&mut s,topic,&if topic<83 {vec![topic+1]} else {vec![]});}
        put(&mut s.entities,600,json!({"progress/topic":83,"progress/learned":true,"progress/repetitions":0.5}));
        put(&mut s.entities,601,json!({"progress/topic":82,"progress/learned":false,"progress/repetitions":0.5}));
        s.entities.get_mut(&1).unwrap().insert("learner/knowledge-profile".into(),json!([600,601]));
        s.entities.get_mut(&1).unwrap().insert("learner/queue".into(),json!([83]));
        let plan=study_candidates(&s,1,5,planning_time()).unwrap();
        assert_eq!(plan.iter().map(|p|p.topic).collect::<BTreeSet<_>>(),BTreeSet::from([81,82]));
        // Explicit Study Now keeps its manual override, outside automatic lessons.
        assert_eq!(selected_topic_candidates(&s,1,5,83,planning_time()).unwrap()[0].topic,83);
        // Completing a descendant also does not silently mark its ancestors learned.
        put(&mut s.entities,602,json!({"learner-task/activity":10083,"learner-task/status":"learner-task.status/completed"}));
        s.entities.get_mut(&1).unwrap().insert("learner/activity".into(),json!([602]));
        assert!(!learned_topics(&s,1).unwrap().contains(&81));
        assert!(!known_preparation_topics(&s,1).unwrap().contains(&81));
        assert_eq!(study_candidates(&s,1,5,planning_time()).unwrap().iter().map(|p|p.topic).collect::<BTreeSet<_>>(),BTreeSet::from([81,82]));
    }

    #[test]
    fn new_lessons_use_graph_band_one_boundary_even_when_learned_flag_is_false() {
        let mut s = study_planning_fixture(&[80,81,82,83,84,85,86]);
        for topic in 80..87 { planning_lesson(&mut s,topic,&[]); }
        for (eid,record) in [
            (600,json!({"progress/topic":80,"progress/learned":false,"progress/repetitions":1.0})),
            (601,json!({"progress/topic":81,"progress/learned":false,"progress/repetitions":0.999})),
            (602,json!({"progress/topic":82,"progress/repetitions":0.5})),
            (603,json!({"progress/topic":83,"progress/learned":true,"progress/repetitions":0.5})),
            (604,json!({"progress/topic":84,"progress/repetitions":1.0})),
            (605,json!({"progress/topic":85,"progress/learned":false,"progress/repetitions":6.5})),
        ] { put(&mut s.entities,eid,record); }
        s.entities.get_mut(&1).unwrap().insert("learner/knowledge-profile".into(),json!([600,601,602,603,604,605]));
        let before = s.entities.clone();
        let plan = study_candidates(&s,1,5,planning_time()).unwrap();
        assert_eq!(plan.iter().map(|p|p.topic).collect::<BTreeSet<_>>(),BTreeSet::from([81,82,86]));
        assert_eq!(known_preparation_topics(&s,1).unwrap(),BTreeSet::from([80,83,84,85]));
        // This is a first-learning filter, never a mutation or reinterpretation
        // of the operational learned flag used by course/review scheduling.
        assert!(!learned_topics(&s,1).unwrap().contains(&80));
        assert!(learned_topics(&s,1).unwrap().contains(&82));
        assert_eq!(s.entities,before);
        assert_eq!(selected_topic_candidates(&s,1,5,80,planning_time()).unwrap()[0].topic,80);
    }

    #[test]
    fn shortages_skip_only_the_unavailable_lessons_and_replenishment_rejoins() {
        let mut s=study_planning_fixture(&[82,83]);
        planning_lesson(&mut s,80,&[82]);
        planning_lesson(&mut s,81,&[83]);
        planning_lesson(&mut s,82,&[]);
        planning_lesson(&mut s,83,&[]);
        // Both earlier topics have real banks below the five-question minimum.
        for (topic,kp) in [(80,900),(81,901)] {
            put(&mut s.entities,kp,json!({"knowledge-point/id":id(kp),"knowledge-point/questions":[]}));
            s.entities.get_mut(&topic).unwrap().insert("topic/knowledge-points".into(),json!([kp]));
        }
        let topics=|s:&EntitySnapshot| study_candidates(s,1,5,planning_time()).unwrap().iter().map(|p|p.topic).collect::<BTreeSet<_>>();
        assert_eq!(topics(&s),BTreeSet::from([82,83]));
        for q in 24000..24005 {
            let mut question=s.entities[&100].clone();
            question.insert("question/id".into(),json!(id(q)));
            s.entities.insert(q,question);
        }
        s.entities.get_mut(&900).unwrap().insert("knowledge-point/questions".into(),json!([24000,24001,24002,24003,24004]));
        assert_eq!(topics(&s),BTreeSet::from([80,82,83]));
    }

    #[test]
    fn bounded_inventory_priorities_include_queue_prerequisites_without_supply() {
        let mut s=study_planning_fixture(&[83]);
        for topic in 80..84 {planning_lesson(&mut s,topic,&if topic<83 {vec![topic+1]} else {vec![]});}
        planning_lesson(&mut s,90,&[91]);
        planning_lesson(&mut s,91,&[]);
        s.entities.get_mut(&1).unwrap().insert("learner/queue".into(),json!([91]));
        let priorities=inventory_priorities(&s,1,planning_time()).unwrap();
        assert_eq!(priorities[&80].target_count,0);
        for topic in [81,82,83,90,91] {assert_eq!(priorities[&topic].target_count,1);}
    }

    #[test]
    fn study_targets_keep_the_five_fresh_questions_per_kp_requirement() {
        let mut s = study_planning_fixture(&[80]);
        let target = planning_lesson(&mut s,80,&[]);
        for q in 24000..24005 {
            let mut question = s.entities[&100].clone();
            question.insert("question/id".into(),json!(id(q)));
            s.entities.insert(q,question);
        }
        put(&mut s.entities,900,json!({"knowledge-point/id":id(900),
            "knowledge-point/questions":[24000,24001,24002,24003]}));
        s.entities.get_mut(&80).unwrap().insert("topic/knowledge-points".into(),json!([900]));
        assert!(study_candidates(&s,1,5,planning_time()).unwrap().is_empty());
        s.entities.get_mut(&900).unwrap().insert("knowledge-point/questions".into(),
            json!([24000,24001,24002,24003,24004]));
        assert_eq!(study_candidates(&s,1,5,planning_time()).unwrap()[0].activity,target);
    }

    #[test]
    fn self_directed_queue_resumes_unselected_attempts_before_new_cross_course_lessons() {
        for state in ["started", "paused"] {
            let mut s = study_planning_fixture(&[]);
            let selected = planning_lesson(&mut s, 80, &[]);
            let unselected = planning_lesson(&mut s, 81, &[]);
            put(
                &mut s.entities,
                601,
                json!({"learner-task/activity":unselected,"learner-task/status":format!("learner-task.status/{state}"),"learner-task/items":[]}),
            );
            s.entities.get_mut(&1).unwrap().extend(
                json!({"learner/activity":[601],"learner/queue":[80]})
                    .as_object()
                    .unwrap()
                    .clone(),
            );
            let before = s.entities.clone();
            let plan = study_candidates(&s, 1, 5, planning_time()).unwrap();
            assert_eq!(
                plan.iter().map(|p| p.activity).collect::<Vec<_>>(),
                [unselected, selected]
            );
            assert_eq!(plan[0].reason, "Continue your lesson");
            assert_eq!(s.entities, before);
            s.entities
                .get_mut(&1)
                .unwrap()
                .insert("learner/queue".into(), json!([]));
            assert_eq!(
                study_candidates(&s, 1, 5, planning_time())
                    .unwrap()
                    .iter()
                    .map(|p| p.activity)
                    .collect::<Vec<_>>(),
                [unselected]
            );
            s.entities.get_mut(&601).unwrap().insert(
                "learner-task/status".into(),
                json!("learner-task.status/completed"),
            );
            assert!(
                study_candidates(&s, 1, 5, planning_time())
                    .unwrap()
                    .is_empty()
            );
        }
    }

    #[test]
    fn study_queue_keeps_content_checks_and_rejects_non_topic_refs() {
        let mut s = study_planning_fixture(&[]);
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
        let mut s = study_planning_fixture(&[90]);
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
    fn planner_uses_nested_assignment_deadlines_only_for_selected_targets() {
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
        // Merely storing mapped assignments does not affect a learner's plan.
        let unlinked = plan_candidates(&s, 1, 5, at).unwrap();
        assert_eq!(
            unlinked.iter().map(|p| p.activity).collect::<Vec<_>>(),
            [later, sooner, 20]
        );
        assert!(unlinked.iter().all(|p| p.due.is_none()));
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
        // Removing a target wins even while both assignments still reference it.
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/targets".into(), json!([80]));
        let remaining = plan_candidates(&s, 1, 5, at).unwrap();
        assert_eq!(
            remaining.iter().map(|p| p.activity).collect::<Vec<_>>(),
            [later, 20]
        );
        assert_eq!(remaining[0].due, Some(at + chrono::Duration::days(7)));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/targets".into(), json!([]));
        let empty = plan_candidates(&s, 1, 5, at).unwrap();
        assert_eq!(empty.iter().map(|p| p.activity).collect::<Vec<_>>(), [20]);
        assert_eq!(empty[0].target_count, 0);
        assert_eq!(empty[0].due, None);
        // A later explicit addition immediately restores its own target weight
        // and earliest deadline, without restoring other assignment mappings.
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/targets".into(), json!([83]));
        let restored = plan_candidates(&s, 1, 5, at).unwrap();
        assert_eq!(
            restored.iter().map(|p| p.activity).collect::<Vec<_>>(),
            [sooner, 20]
        );
        assert_eq!(restored[0].target_topics, [83]);
        assert_eq!(restored[0].due, Some(at + chrono::Duration::hours(25)));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(false));
        assert_eq!(candidates(&s, 1, 5).unwrap(), [20]);
    }

    #[test]
    fn assignment_completion_and_failure_preserve_targets_and_priorities() {
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
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/assignments".into(), json!([700]));
        let plan = plan_candidates(&s, 1, 5, at).unwrap();
        assert_eq!(plan[0].activity, lesson);
        assert_eq!(plan[0].target_count, 1);
        assert_eq!(plan[0].due, Some(at - chrono::Duration::days(1)));
        let expected = serde_json::to_value(&plan).unwrap();

        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([600]));
        for status in ["started", "paused", "failed", "completed"] {
            put(
                &mut s.entities,
                600,
                json!({"learner-task/id":id(600),"learner-task/activity":700,"learner-task/status":format!("learner-task.status/{status}"),"learner-task/items":[]}),
            );
            assert_eq!(
                serde_json::to_value(plan_candidates(&s, 1, 5, at).unwrap()).unwrap(),
                expected,
                "assignment status {status} must not change planning"
            );
            assert_eq!(s.refs(1, "learner/targets").unwrap(), [80]);
        }

        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/targets".into(), json!([]));
        for status in ["completed", "failed"] {
            s.entities.get_mut(&600).unwrap().insert(
                "learner-task/status".into(),
                json!(format!("learner-task.status/{status}")),
            );
            let plan = plan_candidates(&s, 1, 5, at).unwrap();
            assert_eq!(plan.iter().map(|p| p.activity).collect::<Vec<_>>(), [20]);
            assert_eq!(plan[0].due, None);
        }
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
        s = EntitySnapshot::new(s.entities.into(), s.basis_t).unwrap();
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
                json!(if slot == 1 {
                    "task-item.status/incorrect"
                } else {
                    "task-item.status/correct"
                }),
            );
        }
        assert!(lesson_passed(&s, 20, &items(&s)).unwrap());
    }

    #[test]
    fn adaptive_practice_fails_after_two_wrong_and_never_reuses_other_task_questions() {
        let mut s = fixture();
        present(&mut s, 40, "completed");
        present(&mut s, 42, "completed");
        for q in 100..102 {
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
    fn lesson_advances_after_correct_streak_or_five_and_resets_at_the_next_kp() {
        for outcomes in [vec![true, true], vec![true, false, true, false, true], vec![false, true, false, true, false]] {
            let mut s = fixture();
            s.entities.get_mut(&31).unwrap().insert("step/next".into(), json!(32));
            s.entities.get_mut(&20).unwrap().insert("activity/steps".into(), json!([30, 31, 32]));
            put(&mut s.entities, 32, json!({"step/id":id(32),"step/content":44}));
            put(&mut s.entities, 44, json!({"knowledge-point/id":id(44),"knowledge-point/canonical-example":43,"knowledge-point/questions":[105,106]}));
            put(&mut s.entities, 43, json!({"question/id":id(43),"question/problem":"Next example","question/worked-solution":"Explanation"}));
            for q in [105, 106] {
                put(&mut s.entities, q, json!({"question/id":id(q),"question/problem":"Next question","question/answer-fields":[200]}));
            }
            s = EntitySnapshot::new(s.entities.clone().into(), s.basis_t).unwrap();
            present(&mut s, 40, "completed");
            present(&mut s, 42, "completed");
            for (n, correct) in outcomes.into_iter().enumerate() {
                present(&mut s, 100 + n as u64, if correct { "correct" } else { "incorrect" });
            }
            let p = position(&s, 20, &items(&s)).unwrap();
            assert_eq!(p.next, Some(43));
            assert!(!p.failed);
            assert!(p.deferred.is_empty());
            present(&mut s, 43, "completed");
            assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(105));
            present(&mut s, 105, "correct");
            assert_eq!(next_content(&s, 20, &items(&s)).unwrap(), Some(106));
            present(&mut s, 106, "correct");
            assert!(lesson_passed(&s, 20, &items(&s)).unwrap());
        }
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
    fn general_ode_scaffolds_absorb_only_additive_constant_shifts() {
        let mut s = fixture();
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("x^2"));
        for scaffold in [
            "$y=-2($\n{{x}}\n$+K)^{-1}$",
            "$y=\\pm ($ {{x}} $+K)^{1/2}$",
            "$y=\\sqrt{ $ {{x}} $+K}$",
        ] {
            s.entities.get_mut(&100).unwrap().insert("question/problem".into(),
                json!(format!("Find the general solution to the differential equation y'=x/y. K is an arbitrary constant.\n\n{scaffold}")));
            for value in ["x*x", "x^2+5", "x^2-2/3", "x^2+pi"] {
                assert_eq!(grade_field(&s,100,200,value), Ok(true), "{scaffold}: {value}");
            }
            for value in ["2*x^2", "x^3+5", "x^2+x", "5"] {
                assert_eq!(grade_field(&s,100,200,value), Ok(false), "{scaffold}: {value}");
            }
            assert!(grade_field(&s,100,200,"x^2+x/x").is_err());
        }
        for prompt in [
            "Simplify. K is an arbitrary constant. $y=($ {{x}} $+K)^{-1}$",
            "Find the general solution to the differential equation. $y=($ {{x}} $+K)^{-1}$",
            "Find the general solution to the differential equation. K is an arbitrary constant. $y=(x*$ {{x}} $+K)^{-1}$",
            "Find the general solution to the differential equation. K is an arbitrary constant. $y=($ {{x}} $^2+K)^{-1}$",
            "Find the general solution to the differential equation. K is an arbitrary constant. $y=($ {{other}} $+K)^{-1}$ {{x}}",
            "Find the general solution to the differential equation. K is an arbitrary constant. $y=($ {{x}} $+K*x)^{-1}$",
            "Find the general solution to the differential equation. K is an arbitrary constant. $y=K($ {{x}} $+K)^{-1}$",
            "Find the general solution to the differential equation. K is an arbitrary constant. $y=($ {{x}} $+K)^{-1}+K*x$",
            "Find the general solution to the differential equation. K is an arbitrary constant. Give the zero constant term. $y=($ {{x}} $+K)^{-1}$",
        ] {
            s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!(prompt));
            assert_eq!(grade_field(&s,100,200,"x^2+5"), Ok(false), "{prompt}");
        }
    }

    #[test]
    fn local_ode_argument_blanks_absorb_constants_in_direct_and_named_scaffolds() {
        let mut s = fixture();
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("(x-3)^2"));
        for prompt in [
            "Find the nonconstant local solution to $y'=2(x-3)\\sqrt{1-y^2}$ by separating variables. Express the solution as $y=\\sin(\\boxed{\\text{expression}}+C)$.\n\nExpression: {{x}}",
            "Find the general solution to the differential equation. $y=\\sin($ {{x}} $+C)$, where $C$ is an arbitrary constant.",
            "Find the general solution to the differential equation. $y=\\cos($ {{x}} $+K)$, where $K$ is an arbitrary constant.",
        ] {
            s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!(prompt));
            for value in ["x^2-6*x", "(x-3)^2+1", "(x-3)^2-2/3", "(x-3)^2+pi"] {
                assert_eq!(grade_field(&s,100,200,value), Ok(true), "{prompt}: {value}");
            }
            for value in ["2*(x-3)^2", "(x-3)^2+x", "(x-3)^3", "0"] {
                assert_eq!(grade_field(&s,100,200,value), Ok(false), "{prompt}: {value}");
            }
            assert!(grade_field(&s,100,200,"(x-3)^2+x/x").is_err());
        }
        for prompt in [
            "Find the general solution to the differential equation. $y=\\sin(x*{{x}}+C)$, where C is an arbitrary constant.",
            "Find the general solution to the differential equation. $y=\\sin({{x}}^2+C)$, where C is an arbitrary constant.",
            "Find the general solution to the differential equation. $y=\\sin({{x}}+C)+C*x$, where C is an arbitrary constant.",
            "Find the general solution to the differential equation. $y=\\sin({{x}}+C)$ with C=0.",
            "Find the general solution to the differential equation with initial condition y(3)=0. $y=\\sin({{x}}+C)$.",
            "Simplify $y=\\sin({{x}}+C)$.",
            "Find the nonconstant local solution by separating variables. $y=\\sin(\\boxed{\\text{other}}+C)$. Expression: {{x}}",
            "Find the nonconstant local solution by separating variables. $y=\\sin(\\boxed{\\text{expression}}+C)+C*x$. Expression: {{x}}",
        ] {
            s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!(prompt));
            assert_eq!(grade_field(&s,100,200,"(x-3)^2+1"), Ok(false), "{prompt}");
        }
    }

    #[test]
    fn evaluated_logarithm_answers_enforce_only_explicit_log_free_contract() {
        let context = symbolic::Context::default();
        for value in [r"\log_3 9", r"\ln(9)/\ln(3)", "log(9)/log(3)", "log_3(9)"] {
            assert!(!compare_math_in_context(value, "2",
                "Give an evaluated integer or fraction, with no logarithms.", context).unwrap(), "{value}");
        }
        assert!(!compare_math_in_context(r"t/\log_3 9", "t/2",
            "Give a multiple of t with an evaluated coefficient and no logarithms.", context).unwrap());
        for value in ["2", "2.000", "4/2", r"\frac{4}{2}"] {
            assert!(compare_math_in_context(value, "2",
                "Give an evaluated integer or fraction, with no logarithms.", context).unwrap());
        }
        assert!(compare_math_in_context("t*(1/2)", "t/2",
            "Give a multiple of t with no logarithms.", context).unwrap());
        assert!(compare_math_in_context(r"\log_3 9", "2", "Find k.", context).unwrap());
        assert!(!forbids_logarithms("Use logarithms to solve."));
        assert!(forbids_logarithms("Give an expression without logarithms."));
        assert!(!contains_logarithm("alpha + t/2"));
    }

    #[test]
    fn positive_trig_logarithm_antiderivatives_accept_optional_absolute_values() {
        let mut s = fixture();
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(),
            json!(r"-3\left(\ln\left|\cos{\left(x\right)}+2\right|\right)"));
        s.entities.get_mut(&100).unwrap().insert("question/problem".into(),
            json!(r"Find an antiderivative. $\int \frac{3\sin x}{\cos x+2}\,dx$ {{x}} $+C$"));
        for answer in [r"-3\ln(\cos x+2)", "-3ln(2+cos(x))+7/3", "-3ln(abs(cos(x)+2))"] {
            assert_eq!(grade_field(&s,100,200,answer),Ok(true),"{answer}");
        }
        for wrong in ["3ln(2+cos(x))", "-2ln(2+cos(x))", "-3ln(3+cos(x))"] {
            assert_eq!(grade_field(&s,100,200,wrong),Ok(false),"{wrong}");
        }
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(),json!("ln(abs(cos(x)))"));
        assert_ne!(grade_field(&s,100,200,"ln(cos(x))"),Ok(true));
    }
    #[test]
    fn antiderivative_blanks_absorb_numeric_constants_only_when_displayed() {
        let mut s = fixture();
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("t^7/7+5*t"));
        s.entities.get_mut(&100).unwrap().insert("question/problem".into(),
            json!("Find y(t), the antiderivative of y'(t)=5+t^6.\n$y(t)=$\n{{x}}\n$+\\,C$"));
        for value in ["t^7/7+5*t+1", "5*t+t^7/7-2/3", "t^7/7+5*t+pi"] {
            assert_eq!(grade_field(&s,100,200,value), Ok(true), "{value}");
        }
        for value in ["t^7/7+6*t+1", "t^7/6+5*t+1", "1"] {
            assert_eq!(grade_field(&s,100,200,value), Ok(false), "{value}");
        }
        assert!(grade_field(&s,100,200,"t^7/7+5*t+t/t").is_err());
        for prompt in [
            "Simplify {{x}} + C.",
            "Find the antiderivative. {{x}}", // no external arbitrary constant
            "Find the antiderivative with zero constant term. {{x}} + C",
            "Find the antiderivative. {{x}} + cos(t)",
            "Find the antiderivative. {{other}} + C and {{x}}",
            "Find the definite integral \\int_0^1 t^6 dt. {{x}} + C",
        ] {
            s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!(prompt));
            assert_eq!(grade_field(&s,100,200,"t^7/7+5*t+1"),Ok(false),"{prompt}");
        }
        s.entities.get_mut(&100).unwrap().insert("question/problem".into(),
            json!("For x != 0 calculate the integral. $\\int f(x)/x^3\\,dx=$ {{x}} $+C.$"));
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(),json!("3*x+6/x"));
        assert_eq!(grade_field(&s,100,200,"3*x+6/x+1"),Ok(true));
        assert_eq!(grade_field(&s,100,200,"0"),Ok(false));
    }

    #[test]
    fn exponent_form_preserves_integer_base_and_factor_count() {
        let mut s = fixture();
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("7^{5}"));
        for prompt in [
            "Express the product in exponent form. {{x}}",
            "Write the repeated multiplication as a power. {{x}}",
            "Write using exponents. {{x}}",
        ] {
            s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!(prompt));
            for value in ["7^5", "7^{5}", "{7}^{5}", "(7)^5", "7^(5)",
                r"\left(7\right)^{5}", "{(7)^{5}}"] {
                assert_eq!(grade_field(&s,100,200,value), Ok(true), "{prompt}: {value}");
            }
            for value in ["16807", "7*7*7*7*7", "7^4", "5^7", "49^(5/2)",
                "7^(2+3)", "7^5+0", "7^5^1", "7^{5", "{7)^{5}"] {
                assert_eq!(grade_field(&s,100,200,value), Ok(false), "{prompt}: {value}");
            }
        }
        // An ordinary equivalent-value question still accepts evaluated values.
        s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!("Evaluate the product. {{x}}"));
        assert_eq!(grade_field(&s,100,200,"16807"), Ok(true));
        // A scaffolded numeric fragment is not forced to be a complete power.
        s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!("Exponent form: $7^?$; fill the exponent. {{x}}"));
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("5"));
        assert_eq!(grade_field(&s,100,200,"5"), Ok(true));
    }

    #[test]
    fn exponential_form_symbolic_equations_preserve_all_three_roles() {
        let mut s = fixture();
        for (base, exponent, result) in [('m', 'k', 't'), ('P', 'r', 'q')] {
            let canonical = format!("{base}^{exponent}={result}");
            s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!(canonical));
            s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!(
                "Write the logarithmic equation in exponential form. {{x}}"));
            for value in [canonical.clone(), format!("{result}={base}^{{{exponent}}}"),
                format!("{{({base})^({exponent})}}=({result})"),
                format!(r"\left({base}\right)^{{{exponent}}}={result}"),
                format!("({result}=({base})^({exponent}))")] {
                assert_eq!(grade_field(&s,100,200,&value), Ok(true), "{value}");
            }
            for value in [format!("{exponent}^{base}={result}"),
                format!("{base}^{result}={exponent}"), format!("{result}^{exponent}={base}"),
                format!("{base}*{exponent}={result}"), format!("{base}^{exponent}"),
                format!("{base}^({exponent}+1)={result}"), format!("{base}^{exponent}=-{result}"),
                format!("{base}^{exponent}={result}=0"), format!("{base}^{exponent}={result}extra"),
                format!("{base}^{{{exponent}={result}"), format!("{base})^{exponent}={result}"),
                format!("{base}^({exponent})^{exponent}={result}"),
                format!(r"\log_{{{base}}}({result})={exponent}")] {
                assert_eq!(grade_field(&s,100,200,&value), Ok(false), "{value}");
            }
        }
        // A single expression, numeric fragment, or other prompt is not routed
        // through this deliberately narrow representation check.
        assert!(symbolic_power_equation_form("m^k").is_none());
        assert!(symbolic_power_equation_form("2^3=8").is_none());
        assert!(symbolic_power_equation_form("(m+1)^k=t").is_none());
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("m^k=t"));
        s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!("Evaluate. {{x}}"));
        assert!(grade_field(&s,100,200,"m^k=t").is_err());
    }

    #[test]
    fn fractional_power_lowest_terms_preserves_the_submitted_fraction() {
        let context = symbolic::Context::default();
        for instruction in ["lowest terms", "simplest form", "reduced fraction"] {
            let prompt = format!("Express the radical as a single power with a fractional exponent in {instruction}.");
            for answer in ["7^(2/3)", r"7^{\frac{2}{3}}", "{7}^{2/3}", "(7)^((2)/(3))"] {
                assert!(compare_math_in_context(answer, "7^{2/3}", &prompt, context).unwrap(), "{answer}");
            }
            for answer in ["7^(4/6)", r"7^{\frac{8}{12}}", "7^(-2/-3)", "7^(0.6666666667)", "49^(1/3)", r"\sqrt[6]{7^4}"] {
                assert!(!compare_math_in_context(answer, "7^{2/3}", &prompt, context).unwrap(), "{answer}");
            }
        }
        // Without a reduction instruction, equivalent literal exponents still work.
        assert!(compare_math_in_context("7^(4/6)", "7^{2/3}", "Write as a single power.", context).unwrap());
        assert!(compare_math_in_context("7^(0.5)", "7^{1/2}", "Write in exponential form.", context).unwrap());
    }

    #[test]
    fn exponential_form_preserves_fractional_base_exponent_roles() {
        let mut s = fixture();
        s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!(
            r"Express $\log_5(2.924)\approx 2/3$ in exponential form. {{x}} $\approx$ {{y}}"));
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("5^{2/3}"));
        for value in ["5^{2/3}", "(5)^(2/3)", r"5^{\frac{2}{3}}", r"5^{\frac23}",
            r"{\left(5\right)^{\dfrac{2}{3}}}", "5^{4/6}"] {
            assert_eq!(grade_field(&s,100,200,value), Ok(true), "{value}");
        }
        for value in ["25^{1/3}", r"\sqrt[3]{25}", "5^{3/2}", "2.924", "(2/3)^5",
            "5^(2/(1+2))", "5^2/3", "5^{2/3}+0", "5^{2/3}^1", "5^{2/3", "{5)^{2/3}"] {
            assert_eq!(grade_field(&s,100,200,value), Ok(false), "{value}");
        }
        // The other field is a supplied decimal, not a complete power.
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("2.924"));
        assert_eq!(grade_field(&s,100,200,"2.9240"), Ok(true));
        // The original unit-fraction conversion has the same contract.
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("2^{1/2}"));
        assert_eq!(grade_field(&s,100,200,r"2^{\frac12}"), Ok(true));
        assert_eq!(grade_field(&s,100,200,r"\sqrt{2}"), Ok(false));
        for value in ["2^{0.5}", "(2)^(0.500)", "2^{.50}"] {
            assert_eq!(grade_field(&s,100,200,value), Ok(true), "{value}");
        }
        for value in ["2^{0.499}", "2^{0.501}", "2^{0.5+0}", "4^{0.25}"] {
            assert_eq!(grade_field(&s,100,200,value), Ok(false), "{value}");
        }
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("7^{3/2}"));
        assert_eq!(grade_field(&s,100,200,"7^{1.500}"), Ok(true));
        assert_eq!(grade_field(&s,100,200,"7^{1.499}"), Ok(false));
        // Ordinary value equivalence keeps its original semantics.
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("2^{1/2}"));
        s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!("Evaluate. {{x}}"));
        assert_eq!(grade_field(&s,100,200,r"\sqrt{2}"), Ok(true));
    }

    #[test]
    fn grading_checks_all_fields_choice_membership_and_exact_rational_math() {
        let mut s = fixture();
        assert!(grade_field(&s, 100, 200, "0.5").unwrap());
        assert!(!grade_field(&s, 100, 200, "0.6").unwrap());
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
        assert!(grade_field(&s, 100, 200, "300").unwrap());
        assert!(!grade_field(&s, 100, 200, "399").unwrap());
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
    fn natural_exponential_answers_disambiguate_euler_products() {
        for prompt in [r"Evaluate $\int_0^2 3e^{x/2}\,\mathrm{d}x$.",
                       r"Evaluate $\int_0^2 3{e}^{x/2}\,\mathrm{d}x$."] {
            let context = comparison_context(prompt, &[]);
            assert!(context.natural_exponential);
            assert_eq!(compare_math_in_context("1e-3", "0.001", prompt, context), Ok(false));
            assert_eq!(compare_math_in_context("1 e -3", "0.001", prompt, context), Ok(false));
            assert_eq!(compare_math_in_context("1E-3", "0.001", prompt, context), Ok(true));
            for submitted in ["6e-6", r"\frac{12e-12}{2}", "6*(e-1)"] {
                assert_eq!(compare_math_in_context(submitted, "6(e-1)", prompt, context), Ok(true));
            }
            for submitted in ["0.000006", "3e-3", "6e+6"] {
                assert_eq!(compare_math_in_context(submitted, "6(e-1)", prompt, context), Ok(false));
            }
        }
        let prompt = "Write 0.001 in scientific notation.";
        let context = comparison_context(prompt, &[]);
        assert!(!context.natural_exponential);
        assert_eq!(compare_math_in_context("1e-3", "0.001", prompt, context), Ok(true));
    }

    #[test]
    fn euler_constant_exponents_disambiguate_exact_rate_answers() {
        let mut s = fixture();
        for prompt in [
            r"Given $y=3{x}^{e}+\ln x$, find the instantaneous rate at $x=1$. Do not round the answer.",
            r"Given $y=3x^e+\ln x$, find the instantaneous rate at $x=1$.",
            r"Differentiate $3x^{ e }+\ln x$ and evaluate at $x=1$.",
        ] {
            let context = comparison_context(prompt, &[]);
            assert!(context.natural_exponential, "{prompt}");
            s.entities.get_mut(&100).unwrap().insert("question/problem".into(), json!(prompt));
            s.entities.get_mut(&300).unwrap().insert("answer/value".into(), json!("3e+1"));
            for accepted in ["1+3e", "3*e+1", "3e+1", r"\frac{6e+2}{2}"] {
                assert_eq!(grade_field(&s,100,200,accepted), Ok(true), "{prompt}: {accepted}");
            }
            for rejected in ["30", "3E+1", "3e", "3e-1", "1+3e^x"] {
                assert_eq!(grade_field(&s,100,200,rejected), Ok(false), "{prompt}: {rejected}");
            }
        }
        for prompt in ["Write 30 in scientific notation.", r"Given $x^{energy}$, simplify."] {
            assert!(!comparison_context(prompt, &[]).natural_exponential);
        }
    }

    #[test]
    fn checkbox_fields_grade_one_question_with_explicit_false_answers() {
        let mut s = fixture();
        let mut fields = vec![];
        let mut responses = BTreeMap::new();
        for (n, expected) in [false, true, true, false].into_iter().enumerate() {
            let field = 400 + n as u64;
            let no = 500 + 2 * n as u64;
            let yes = no + 1;
            put(
                &mut s.entities,
                no,
                json!({"answer/id":id(no),"answer/type":"answer.type/text","answer/value":"false"}),
            );
            put(
                &mut s.entities,
                yes,
                json!({"answer/id":id(yes),"answer/type":"answer.type/text","answer/value":"true"}),
            );
            let correct = if expected { yes } else { no };
            put(
                &mut s.entities,
                field,
                json!({"answer-field/id":id(field),"answer-field/type":"answer-field.type/checkbox","answer-field/key":format!("option-{n}"),"answer-field/choices":[no,yes],"answer-field/correct":correct}),
            );
            fields.push(field);
            responses.insert(field, correct.to_string());
        }
        s.entities
            .get_mut(&100)
            .unwrap()
            .insert("question/answer-fields".into(), json!(fields));
        assert!(grade(&s, 100, &responses).unwrap());
        responses.insert(400, "501".into());
        assert!(!grade(&s, 100, &responses).unwrap());
        responses.remove(&403);
        assert!(grade(&s, 100, &responses).is_err());
        // Empty subsets remain valid historical responses, but cannot be
        // chosen for fresh lesson, review or assessment practice.
        for n in 0..4 {
            let field = 400 + n;
            let no = 500 + 2 * n;
            s.entities.get_mut(&field).unwrap()
                .insert("answer-field/correct".into(), json!(no));
            responses.insert(field, no.to_string());
        }
        assert!(validate_question(&s, 100).is_ok());
        assert!(grade(&s, 100, &responses).unwrap());
        assert!(validate_practice_question(&s, 100).is_err());
        s.entities
            .get_mut(&500)
            .unwrap()
            .insert("answer/value".into(), json!("FALSE"));
        assert!(validate_response_question(&s, 100).is_err());
    }

    #[test]
    fn free_fields_collect_without_canonical_and_never_enter_practice_or_grading() {
        let mut s = fixture();
        let field = s.entities.get_mut(&200).unwrap();
        field.insert("answer-field/type".into(), json!("answer-field.type/free"));
        field.remove("answer-field/correct");
        field.remove("answer-field/choices");
        assert!(validate_response_question(&s, 100).is_ok());
        let responses = BTreeMap::from([(200, "**Proof:** $x=y$".into())]);
        assert!(validate_responses(&s, 100, &responses).is_ok());
        assert!(validate_question(&s, 100).is_err());
        assert!(grade(&s, 100, &responses).is_err());
        let field = s.entities.get_mut(&200).unwrap();
        field.insert("answer-field/choices".into(), json!([300]));
        field.insert("answer-field/correct".into(), json!(300));
        assert!(validate_response_question(&s, 100).is_ok());
        assert!(grade(&s, 100, &responses).is_err());
        // Adding an automatically gradable field does not make a mixed question
        // produce a partial correctness observation.
        s.entities
            .get_mut(&100)
            .unwrap()
            .insert("question/answer-fields".into(), json!([200, 201]));
        assert!(validate_question(&s, 100).is_err());
    }

    #[test]
    fn supported_symbolic_blanks_are_served_and_rounding_preserves_form() {
        let mut s = fixture();
        s.entities
            .get_mut(&300)
            .unwrap()
            .insert("answer/value".into(), json!("x^2+1"));
        assert!(validate_question(&s, 100).is_ok());
        assert!(grade(&s, 100, &BTreeMap::from([(200, "1+x^2".into())])).unwrap());
        assert!(!grade(&s, 100, &BTreeMap::from([(200, "2+x^2".into())])).unwrap());
        assert!(grade(&s, 100, &BTreeMap::from([(200, "foo(x)".into())])).is_err());
        s.entities
            .get_mut(&300)
            .unwrap()
            .insert("answer/value".into(), json!("foo(x)"));
        assert!(validate_question(&s, 100).is_err());
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
    fn rounded_decimal_blanks_accept_equivalent_numerals_without_rounding_again() {
        let mut s = fixture();
        s.entities.get_mut(&100).unwrap().insert(
            "question/problem".into(),
            json!("Round your answer to three decimal places."),
        );
        for (canonical, accepted) in [
            ("0.850", ".850"),
            ("0.850", "+0.850"),
            ("0.850", "+.850"),
            ("0.850", "00.850"),
            ("0.850", "+00.850"),
            (".850", "0.850"),
            ("-0.850", "-.850"),
            ("-0.850", "-00.850"),
            ("+0.850", "+.850"),
            ("+0.850", "0.850"),
            ("00.850", ".850"),
            ("0002.050", "2.050"),
            ("2.050", "+0002.050"),
            ("0.000", ".000"),
            ("1.000", "1"),
            ("1.000", "+001"),
            ("1.000", "1.0"),
            ("1.000", "1.0000"),
            ("0.850", ".85"),
            ("0.850", "0.8500"),
            ("0.850", "+.8500"),
            ("0.850", "00.85"),
            ("0.850", "+.85"),
            ("0.850", "00.8500"),
            ("0.000", "0"),
            ("0.000", "-0.0"),
        ] {
            s.entities
                .get_mut(&300)
                .unwrap()
                .insert("answer/value".into(), json!(canonical));
            assert_eq!(
                grade(&s, 100, &BTreeMap::from([(200, accepted.into())])),
                Ok(true),
                "{accepted} must equal the rounded numeral {canonical}"
            );
        }
        s.entities
            .get_mut(&300)
            .unwrap()
            .insert("answer/value".into(), json!("0.850"));
        for rejected in [
            "00.851",
            "0002.050",
            "0.8501",
            "0.8499",
            ".851",
            "-.850",
            "17/20",
            "8.50e-1",
            ".425+.425",
            ".",
            "..850",
        ] {
            assert_eq!(
                grade(&s, 100, &BTreeMap::from([(200, rejected.into())])),
                Ok(false),
                "{rejected} must not satisfy the authored three-decimal answer"
            );
        }
    }

    #[test]
    fn significant_figures_and_explicit_decimal_format_keep_trailing_zeroes() {
        for prompt in [
            "Round to four significant figures.",
            "Use four significant digits.",
            "Round to three decimal places and include trailing zeros.",
            "Round the result and write exactly three decimal places.",
            "Write exactly three digits after the decimal point.",
        ] {
            let context = symbolic::Context::default();
            assert_eq!(compare_math_in_context("1.000", "1.000", prompt, context), Ok(true));
            assert_eq!(compare_math_in_context("1", "1.000", prompt, context), Ok(false), "{prompt}");
            assert_eq!(compare_math_in_context("1.0000", "1.000", prompt, context), Ok(false), "{prompt}");
        }
    }

    #[test]
    fn simplest_fraction_blanks_accept_ui_tex_notation_without_reducing_answers() {
        let mut s = fixture();
        s.entities.get_mut(&100).unwrap().insert(
            "question/problem".into(),
            json!("Express your answer as a fraction in its simplest form."),
        );
        for (canonical, accepted) in [
            (r"\frac{1}{4}", r"\frac14"),
            (r"\frac{1}{4}", r"\frac{1}4"),
            (r"\frac{1}{4}", r"\frac1{4}"),
            (r"\frac{1}{4}", r"\dfrac14"),
            (r"\frac{1}{4}", r"\tfrac14"),
            (r"\frac{1}{4}", "1/4"),
            ("1/4", r"\frac14"),
            (r"\frac{3}{4}", r"\frac34"),
            (r"\frac{2}{3}", r"\frac{2}3"),
            (r"\frac{12}{5}", r"\frac{12}5"),
            (r"\frac{-1}{4}", r"-\frac14"),
            (r"\frac{-1}{4}", "(-1)/4"),
            (r"\frac{1}{4}", "(1)/(4)"),
            (r"\frac{1}{4}", "((1))/((4))"),
            (r"\frac{-1}{4}", r"\frac{(-1)}{(4)}"),
        ] {
            s.entities
                .get_mut(&300)
                .unwrap()
                .insert("answer/value".into(), json!(canonical));
            assert_eq!(
                grade(&s, 100, &BTreeMap::from([(200, accepted.into())])),
                Ok(true),
                "{accepted} has the same numerator and denominator as {canonical}"
            );
        }
        s.entities
            .get_mut(&300)
            .unwrap()
            .insert("answer/value".into(), json!(r"\frac{12}{5}"));
        // TeX takes one token per unbraced argument: this is (1/2) followed by 5.
        assert_eq!(
            grade(&s, 100, &BTreeMap::from([(200, r"\frac125".into())])),
            Ok(false)
        );
        s.entities
            .get_mut(&300)
            .unwrap()
            .insert("answer/value".into(), json!(r"\frac{1}{4}"));
        for rejected in [
            "2/8",
            r"\frac28",
            r"\frac{2}{8}",
            "0.25",
            "1/(2+2)",
            "(2)/(8)",
            "(1+0)/(4)",
            "(1)/(2+2)",
            r"\frac{1}{2+2}",
            r"\frac{1}{4}+0",
            "4/1",
            r"-\frac14",
            r"\frac1",
            r"\frac{}4",
            r"\frac14x",
            r"\frac{1}{0}",
        ] {
            assert_eq!(
                grade(&s, 100, &BTreeMap::from([(200, rejected.into())])),
                Ok(false),
                "{rejected} must not satisfy the simplest fraction answer"
            );
        }
    }

    #[test]
    fn exact_answer_instructions_accept_equivalent_blank_entries() {
        let mut s = fixture();
        for prompt in [
            "Find the tangent slope. Do not round the answer.",
            "Find the arc length without rounding.",
            "Don't round the answer.",
            "Don’t round the answer.",
            "The answer must not be rounded.",
            "Give an unrounded answer.",
            "Find the distance around the curve.",
        ] {
            s.entities
                .get_mut(&100)
                .unwrap()
                .insert("question/problem".into(), json!(prompt));
            for (canonical, equivalent, wrong) in [
                ("1/5", "4/20", "3/20"),
                (
                    "\\frac{\\pi^{2}}{2}",
                    "\\frac{2\\pi^{2}}{4}",
                    "\\frac{3\\pi^{2}}{4}",
                ),
            ] {
                s.entities
                    .get_mut(&300)
                    .unwrap()
                    .insert("answer/value".into(), json!(canonical));
                assert_eq!(
                    grade(&s, 100, &BTreeMap::from([(200, equivalent.into())])),
                    Ok(true),
                    "{prompt}: {equivalent} should equal {canonical}"
                );
                assert_eq!(
                    grade(&s, 100, &BTreeMap::from([(200, wrong.into())])),
                    Ok(false),
                    "{prompt}: incorrect {wrong}"
                );
            }
        }
    }

    #[test]
    fn negated_rounding_preserves_separate_answer_form_requirements() {
        for prompt in [
            "Do not round intermediate values; round the final answer to two decimal places.",
            "Do not round. Give the answer to three significant figures.",
            "Give the exact answer without rounding, in lowest terms.",
            "Give a reduced fraction. Do not round the answer.",
            "Give your answer in simplest form.",
        ] {
            assert_eq!(
                compare_math_in_context("4/20", "1/5", prompt, symbolic::Context::default()),
                Ok(false),
                "{prompt} must still enforce the required answer form"
            );
        }
    }

    #[test]
    fn symbolic_grading_keeps_unknown_comparisons_out_of_learner_results() {
        let mut s = fixture();
        for (canonical, submitted, expected) in [
            ("2\\sqrt{10}", "\\sqrt{40}", true),
            (r"\frac{e^{\frac{3}{2}}}{3}", r"\frac{\sqrt{e^3}}{3}", true),
            (r"\frac{e^{\frac{3}{2}}}{3}", r"-\frac{\sqrt{e^3}}{3}", false),
            (r"-\frac{1}{\sqrt{(2x+7)^3}}", r"-\left(2x+7\right)^{-\frac32}", true),
            (
                "2\\sqrt{1+\\frac{x^2}{9}}",
                "\\sqrt{4+\\frac{4x^2}{9}}",
                true,
            ),
            (
                "2\\sqrt{1+\\frac{x^2}{9}}",
                "-\\sqrt{4+\\frac{4x^2}{9}}",
                false,
            ),
            ("sin(x)", "-sin(x)", false),
            ("2e^x", "3e^x", false),
            ("\\le", "<=", true),
            ("\\infty", "-∞", false),
        ] {
            s.entities
                .get_mut(&300)
                .unwrap()
                .insert("answer/value".into(), json!(canonical));
            assert_eq!(
                grade(&s, 100, &BTreeMap::from([(200, submitted.into())])),
                Ok(expected)
            );
        }
        s.entities
            .get_mut(&300)
            .unwrap()
            .insert("answer/value".into(), json!("x/x"));
        assert!(grade(&s, 100, &BTreeMap::from([(200, "1".into())])).is_err());
        s.entities
            .get_mut(&300)
            .unwrap()
            .insert("answer/value".into(), json!("1/0"));
        assert!(validate_question(&s, 100).is_err());
    }

    #[test]
    fn finalized_xp_counts_errors_separately_from_mastery() {
        for (outcomes, expected) in [
            (vec![true, true], 15),
            (vec![false, true, true], 8),
            (vec![true, false, false], -1),
            (vec![false; 2], -1),
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
    fn successful_lesson_credit_removes_only_its_topic_from_the_queue() {
        let mut s = fixture();
        put(&mut s.entities, 99, json!({"topic/id": id(99), "topic/title": "Other queued topic"}));
        s.entities.get_mut(&1).unwrap().insert("learner/queue".into(), json!([3, 99]));
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(), json!([3]));
        let before = s.entities.clone();
        let at = DateTime::from_timestamp_millis(1_790_760_000_000).unwrap();
        let removal = json!([crate::schema::keyword("db/retract"), 1, crate::schema::keyword("learner/queue"), 3]);
        for (question, correct, completed, removed) in [
            (Some(100), true, false, false),
            (None, false, true, false),
            (None, true, false, false),
            (None, true, true, true),
        ] {
            let forms = credit(&s, 1, 20, question, correct, completed, "queue-completion", at).unwrap();
            assert_eq!(forms.contains(&removal), removed);
            assert!(!forms.iter().any(|form| form.get(2) == Some(&crate::schema::keyword("learner/targets"))));
            assert!(!forms.contains(&json!([crate::schema::keyword("db/retract"), 1, crate::schema::keyword("learner/queue"), 99])));
        }
        assert_eq!(s.entities, before, "planning must not mutate the captured database");
        s.entities.get_mut(&1).unwrap().insert("learner/queue".into(), json!([99]));
        assert!(!credit(&s, 1, 20, None, true, true, "not-queued", at).unwrap().contains(&removal));
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

#[cfg(test)]
mod explicit_prompt_sign_regressions {
    use super::comparison_context;
    use crate::symbolic::compare;
    #[test]
    fn prompt_signs_are_declarations_not_questions_or_titles() {
        for prompt in ["Coordinates, with $b>0$.", "Given that $b>0.$ Find the radius.", r"For $b \gt 0$, simplify."] {
            let context = comparison_context(prompt, &[]);
            assert_eq!(compare(r"\sqrt{100b^2}", "10b", context), Ok(true), "{prompt}");
            assert_eq!(compare("-10b", "10b", context), Ok(false));
        }
        let negative = comparison_context("with $b<0$, simplify.", &[]);
        assert_eq!(compare("10|b|", "-10b", negative), Ok(true));
        for prompt in ["Determine whether $b>0$.", "Is $b>0$?", "Do not assume $b>0$.", "with $b>0$ and with $b<0$.", "with $b>0$ or $b<0$.", "with $c>0$ or with $b>0$."] {
            let context = comparison_context(prompt, &["with $b>0$".into()]);
            assert_ne!(compare("10|b|", "10b", context), Ok(true), "{prompt}");
        }
    }
}

#[cfg(test)]
mod assignment_answer_shape_tests {
    use super::*;
    #[test]
    fn comma_values_accept_both_orders_and_reject_missing_or_wrong_roots() {
        let p="Find the values of r. Separate the values by commas.";
        for a in ["4,5","5,4","8/2,10/2"] { assert_eq!(compare_math_in_context(a,"4,5",p,symbolic::Context::default()),Ok(true)); }
        for a in ["4,4","4,6","4","(4,5)"] { assert_eq!(compare_math_in_context(a,"4,5",p,symbolic::Context::default()),Ok(false)); }
        assert!(compare_math_in_context("5,4","4,5","Find an ordered pair.",symbolic::Context::default()).is_err());
        assert!(compare_math_in_context("unknown(x),5","4,5",p,symbolic::Context::default()).is_err());
    }
    #[test]
    fn exponential_root_labels_can_swap_without_accepting_duplicate_roots() {
        let mut s=tests::fixture();
        s.entities.get_mut(&100).unwrap().insert("question/problem".into(),json!(r"The general solution is $y=c_1e^{r_1x}+c_2e^{r_2x}$. Find $r_1=$ {{r1}} and $r_2=$ {{r2}}."));
        s.entities.get_mut(&100).unwrap().insert("question/answer-fields".into(),json!([200,201]));
        for (f,a,key,value) in [(200,300,"r1","4"),(201,301,"r2","-6")] {
            s.entities.insert(f,json!({"answer-field/id":format!("field-{f}"),"answer-field/key":key,"answer-field/type":"answer-field.type/blank","answer-field/choices":[a],"answer-field/correct":a}).as_object().unwrap().clone());
            s.entities.insert(a,json!({"answer/id":format!("answer-{a}"),"answer/type":"answer.type/math","answer/value":value}).as_object().unwrap().clone());
        }
        for values in [["4","-6"],["-6","4"]] {assert_eq!(grade(&s,100,&BTreeMap::from([(200,values[0].into()),(201,values[1].into())])),Ok(true));}
        for values in [["4","4"],["-6","-6"],["4","6"]] {assert_eq!(grade(&s,100,&BTreeMap::from([(200,values[0].into()),(201,values[1].into())])),Ok(false));}
        for value in ["4","-6"] {assert_eq!(grade_field(&s,100,200,value),Ok(true));}
        s.entities.get_mut(&100).unwrap().insert("question/problem".into(),json!(r"The general solution is $y=c_1e^{r_1x}+c_2e^{r_2x}$. Put the roots in increasing order."));
        assert!(interchangeable_exponents(&s,100).unwrap().is_none());
    }
}

#[cfg(test)]
mod declared_coordinate_domain_tests {
    use super::comparison_context;
    use crate::symbolic::compare;

    #[test]
    fn final_list_sign_supplies_only_the_explicit_domain() {
        let prompt = r"Let $f(r,\theta)=r^2$, where $x=r\cos\theta$, $y=r\sin\theta$, and $r>0$. Find its derivative.";
        let c = comparison_context(prompt, &[]);
        assert_eq!(compare("r/r", "1", c), Ok(true));
        assert_eq!(compare("2r^2/r", "2r", c), Ok(true));
        assert_eq!(compare("-2r^2/r", "2r", c), Ok(false));
        assert_eq!(compare(r"\sqrt{r^2}", "r", c), Ok(true));
        // A different hole is still an obligation, even with positive radius.
        assert!(compare("(r-1)/(r-1)", "1", c).is_err());
        // Unrelated variables do not inherit the radial declaration.
        assert!(compare("x/x", "1", c).is_err());
    }

    #[test]
    fn lists_preserve_conflicts_negation_and_question_boundaries() {
        for prompt in [
            "where $r>0$, and $r<0$.",
            "where $r<0$, and $r>0$.",
            "Do not assume $x=1$, and $r>0$.",
            "Determine whether $x=1$, and $r>0$.",
            "with $x=1$, and $r>0$ or $r<0$.",
            "Find a relation between $x=1$, and $r>0$.",
        ] {
            let c = comparison_context(prompt, &["where $r>0$".into()]);
            assert_ne!(compare(r"\sqrt{r^2}", "r", c), Ok(true), "{prompt}");
        }
        let negative = comparison_context("where $x=1$, and $r<0$.", &[]);
        assert_eq!(compare(r"\sqrt{r^2}", "-r", negative), Ok(true));
    }
}


#[cfg(test)]
mod derivative_source_domain_tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn derivative_cancellation_uses_original_domain_without_creating_holes() {
        let mut s = tests::fixture();
        s.entities.get_mut(&200).unwrap().insert("answer-field/type".into(),json!("answer-field.type/blank"));
        s.entities.get_mut(&300).unwrap().insert("answer/value".into(),json!("(-x^2-2x-1)/(x^2-1)^2"));
        for prompt in [
            "Given that $f(x)=\\frac{x+1}{x^2-1}$, find $f^{\\prime}(x)$. $f^{\\prime}(x)=$ {{x}}",
            "Given that $f(x)=(x+1)/(x^2-1)$, find $f'(x)$. {{x}}",
        ] {
            s.entities.get_mut(&100).unwrap().insert("question/problem".into(),json!(prompt));
            for value in ["-1/(x-1)^2", "-1/(x^2-2*x+1)", "(-x^2-2*x-1)/(x^2-1)^2"] {
                assert_eq!(grade_field(&s,100,200,value),Ok(true),"{prompt}: {value}");
            }
            for value in ["1/(x-1)^2", "-2/(x-1)^2", "-1/(x+1)^2"] {
                assert_eq!(grade_field(&s,100,200,value),Ok(false),"{value}");
            }
            // x=0 was allowed by the original function. An extra x/x hole
            // remains unresolved, never accepted as an equivalent derivative.
            assert!(grade_field(&s,100,200,"-x/(x*(x-1)^2)").is_err());
        }
        for prompt in [
            "Simplify $f(x)=(x+1)/(x^2-1)$. {{x}}",
            "Find an expression equal to $(-x^2-2x-1)/(x^2-1)^2$. {{x}}",
        ] {
            s.entities.get_mut(&100).unwrap().insert("question/problem".into(),json!(prompt));
            assert!(grade_field(&s,100,200,"-1/(x-1)^2").is_err(),"{prompt}");
        }
    }
}
