//! Reviews and timed assessments over the shared activity/step model.
//! Plans are immutable; the application commits definitions, reservations and
//! evidence using its existing exact-basis, replayable transaction boundary.
use crate::{
    Result, activities,
    core::Event,
    learning,
    schema::{EntitySnapshot, timestamp_days, writeback},
    timing,
};
use chrono::{DateTime, Utc};
use num_traits::ToPrimitive;
use serde_json::{Value, json};
use std::collections::{BTreeMap, BTreeSet};

pub const ASSESSMENT_XP: f64 = 120.0;
pub const ASSESSMENT_REQUIRED_XP: f64 = 150.0;
pub const ASSESSMENT_SECONDS: f64 = 900.0;
// Provisional learning-age floor for ordinary assessments only. Reviews do
// not reset acquisition age, and remediation must not inherit this delay.
pub const ASSESSMENT_TOPIC_AGE_HOURS: i64 = 48;
pub const ASSESSMENT_MIN_NEW_TOPICS: usize = 5;
// Captured questions do not yet contain measured duration estimates.
const QUESTION_SECONDS: f64 = 90.0;

pub fn kind(s: &EntitySnapshot, activity: u64) -> Result<String> {
    Ok(s.ident(&json!(s.reference(activity, "activity/type")?))?
        .rsplit('/')
        .next()
        .unwrap()
        .into())
}
pub fn supported(s: &EntitySnapshot, activity: u64) -> Result<bool> {
    Ok(matches!(
        kind(s, activity)?.as_str(),
        "review" | "assessment"
    ))
}
fn state(s: &EntitySnapshot, eid: u64, attr: &str) -> Result<String> {
    Ok(timing::status(s, eid, attr)?
        .rsplit('/')
        .next()
        .unwrap()
        .into())
}
pub fn outcomes(s: &EntitySnapshot, items: &[u64]) -> Result<Vec<activities::Outcome>> {
    items
        .iter()
        .filter_map(|i| match learning::question_outcome(s, *i) {
            Ok(Some(v)) => Some(Ok(v)),
            Ok(None) => None,
            Err(e) => Some(Err(e)),
        })
        .collect()
}
pub fn position(s: &EntitySnapshot, activity: u64, items: &[u64]) -> Result<learning::Position> {
    let steps = learning::lesson_steps(s, activity)?;
    if kind(s, activity)? == "review" && steps.len() != 5 {
        return Err("A review must reserve five fresh questions".into());
    }
    if kind(s, activity)? == "assessment" {
        let reserved: BTreeSet<_> = steps.iter().map(|st| st.content).collect();
        let mut visited = BTreeSet::new();
        for &item in items {
            let q = s.reference(item, "task-item/content")?;
            if !reserved.contains(&q) || !visited.insert(q) {
                return Err("Assessment presentation is outside its route or duplicated".into());
            }
        }
        let next = steps
            .iter()
            .find(|st| !visited.contains(&st.content))
            .map(|st| st.content);
        return Ok(learning::Position {
            next,
            passed: visited.len() == steps.len(),
            failed: false,
            shortage: None,
            deferred: vec![],
        });
    }
    let mut answered = vec![];
    for (index, item) in items.iter().enumerate() {
        if index >= steps.len() || s.reference(*item, "task-item/content")? != steps[index].content
        {
            return Err("Retrieval presentations must follow their reserved route".into());
        }
        let Some(outcome) = learning::question_outcome(s, *item)? else {
            if index + 1 != items.len() {
                return Err("Unanswered question precedes later content".into());
            }
            return Ok(learning::Position {
                next: Some(steps[index].content),
                passed: false,
                shortage: None,
                failed: false,
                deferred: vec![],
            });
        };
        answered.push(outcome);
        if kind(s, activity)? == "review" {
            let decision = activities::evaluate_review_prefix(&answered)?;
            if decision.complete() {
                if index + 1 != items.len() {
                    return Err("Review continues beyond its stopping prefix".into());
                }
                return Ok(learning::Position {
                    next: None,
                    passed: decision.passed() == Some(true),
                    failed: decision.passed() == Some(false),
                    shortage: None,
                    deferred: vec![],
                });
            }
        }
    }
    let next = steps.get(items.len()).map(|step| step.content);
    Ok(learning::Position {
        next,
        passed: next.is_none(),
        failed: false,
        shortage: None,
        deferred: vec![],
    })
}
pub fn xp(s: &EntitySnapshot, activity: u64, items: &[u64], base: i64) -> Result<i64> {
    let answers = outcomes(s, items)?;
    let total = if kind(s, activity)? == "assessment" {
        learning::lesson_steps(s, activity)?.len()
    } else {
        answers.len()
    };
    activities::earned_xp(
        &kind(s, activity)?,
        base,
        answers.iter().filter(|a| **a == Some(true)).count(),
        total,
        answers.last().copied().flatten(),
    )?
    .to_i64()
    .ok_or_else(|| "XP outside supported range".into())
}
pub fn fresh(s: &EntitySnapshot, learner: u64, activity: u64) -> Result<bool> {
    let seen = learning::unavailable_questions(s, learner)?;
    Ok(learning::lesson_steps(s, activity)?.iter().all(|step| {
        !seen.contains(&step.content)
            && learning::validate_practice_question(s, step.content).is_ok()
    }))
}
pub fn remaining(s: &EntitySnapshot, task: u64, at: DateTime<Utc>) -> Result<Option<f64>> {
    let activity = s.reference(task, "learner-task/activity")?;
    if kind(s, activity)? != "assessment"
        || !matches!(
            state(s, task, "learner-task/status")?.as_str(),
            "started" | "paused"
        )
    {
        return Ok(None);
    }
    let seconds = s
        .entity(activity)?
        .get("activity/time-limit-seconds")
        .and_then(Value::as_f64)
        .filter(|v| v.is_finite() && *v > 0.0)
        .ok_or("Assessment requires a positive wall-clock time limit")?;
    Ok(Some(
        (seconds - (at - timing::task_started(s, task)?).num_milliseconds() as f64 / 1000.0)
            .max(0.0),
    ))
}
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
    let kind = kind(s, activity)?;
    if question.is_none() && (!completed || kind == "assessment") {
        return Ok(vec![]);
    }
    let loaded = learning::learning_runtime(s, learner, at)?;
    let mut engine = loaded.engine.clone();
    let target = if let Some(q) = question {
        s.topic_for_question(q)?
    } else {
        s.reference(activity, "activity/scope")?
    };
    let topic = loaded
        .topic_eid_to_id
        .get(&target)
        .ok_or("Unknown retrieval topic")?;
    let event = |suffix: &str| Event {
        id: format!("{suffix}:{event_id}"),
        learner: loaded.learner.clone(),
        topic: topic.clone(),
        at: timestamp_days(at),
        passed: correct,
        kind: kind.clone(),
        assessment: kind == "assessment",
        ..Event::default()
    };
    if question.is_some() {
        engine.apply_accuracy(event("answer"))?;
    }
    if kind == "assessment" || completed {
        engine.apply_retention(event("retention"))?;
    }
    let mut forms = writeback(&loaded, &engine, vec![], "learning", event_id, at)?.forms;
    forms.retain(|v| v.get("db/id") != Some(&json!("edb.tx")));
    if kind == "review" && completed && correct && s.refs(learner, "learner/queue")?.contains(&target) {
        // Completing a queued topic through review satisfies the same explicit
        // study selection as a lesson, in the completion transaction itself.
        forms.push(json!([crate::schema::keyword("db/retract"), learner, crate::schema::keyword("learner/queue"), target]));
    }
    Ok(forms)
}

pub fn assessment_credit(
    s: &EntitySnapshot,
    learner: u64,
    results: &[(u64, bool)],
    event_id: &str,
    at: DateTime<Utc>,
) -> Result<Vec<Value>> {
    if results.is_empty() {
        return Ok(vec![]);
    }
    let loaded = learning::learning_runtime(s, learner, at)?;
    let mut engine = loaded.engine.clone();
    for &(q, correct) in results {
        let target = s.topic_for_question(q)?;
        let topic = loaded
            .topic_eid_to_id
            .get(&target)
            .ok_or("Unknown assessment topic")?;
        let event = |suffix: &str| Event {
            id: format!("{suffix}:{event_id}:{q}"),
            learner: loaded.learner.clone(),
            topic: topic.clone(),
            at: timestamp_days(at),
            passed: correct,
            kind: "assessment".into(),
            assessment: true,
            ..Event::default()
        };
        engine.apply_accuracy(event("answer"))?;
        engine.apply_retention(event("retention"))?;
    }
    let mut forms = writeback(&loaded, &engine, vec![], "learning", event_id, at)?.forms;
    forms.retain(|v| v.get("db/id") != Some(&json!("edb.tx")));
    Ok(forms)
}

#[derive(Clone, Debug)]
pub struct Definition {
    pub kind: String,
    pub topic: Option<u64>,
    pub questions: Vec<u64>,
    pub title: String,
    pub priority: f64,
    pub expected_seconds: f64,
    pub remediation_for: Vec<u64>,
    pub retake_of: Option<u64>,
    pub existing_activity: Option<u64>,
}
fn bank(s: &EntitySnapshot, topic: u64, seen: &BTreeSet<u64>) -> Result<Vec<u64>> {
    crate::inventory::practice_pool(s, &s.refs(topic, "topic/knowledge-points")?, seen)
}

fn history(s: &EntitySnapshot, learner: u64) -> Result<crate::scheduling::Lifecycle> {
    crate::scheduling::lifecycle(s, learner)
}

/// Currently learned topics whose first successful lesson is at least 48 hours
/// old, at any graph layer. Study's practice recommendation floor does not
/// restrict assessment evidence. Reviews do not reset this clock.
pub fn assessment_topics(
    s: &EntitySnapshot,
    learner: u64,
    at: DateTime<Utc>,
) -> Result<BTreeSet<u64>> {
    let h = history(s, learner)?;
    let mut topics = BTreeSet::new();
    for progress in s.refs(learner, "learner/knowledge-profile")? {
        let topic = s.reference(progress, "progress/topic")?;
        if !learning::topic_in_study_focus(s, learner, topic)? { continue; }
        if s.entity(progress)?.get("progress/learned") == Some(&json!(true))
            && h.mastered.get(&topic).is_some_and(|learned| {
                at - *learned >= chrono::Duration::hours(ASSESSMENT_TOPIC_AGE_HOURS)
            })
        {
            topics.insert(topic);
        }
    }
    Ok(topics)
}

/// Admission depends on one available rated question across a topic. The
/// rolling per-band inventory targets must not exclude otherwise usable topics.
pub fn assessment_pools(
    s: &EntitySnapshot,
    learner: u64,
    at: DateTime<Utc>,
) -> Result<BTreeMap<u64, Vec<u64>>> {
    let seen = learning::unavailable_questions(s, learner)?;
    let mut pools = BTreeMap::new();
    for topic in assessment_topics(s, learner, at)? {
        let pool =
            crate::assessment_sampling::pool(s, &s.refs(topic, "topic/knowledge-points")?, &seen)?;
        if !pool.is_empty() {
            pools.insert(topic, pool);
        }
    }
    Ok(pools)
}

/// A never-started ordinary quiz must still contain five eligible new topics.
/// Started routes and retakes are checked separately by callers.
pub fn ordinary_assessment_ready(
    s: &EntitySnapshot,
    learner: u64,
    activity: u64,
    at: DateTime<Utc>,
) -> Result<bool> {
    if !fresh(s, learner, activity)? {
        return Ok(false);
    }
    let h = history(s, learner)?;
    let eligible = assessment_topics(s, learner, at)?;
    ordinary_assessment_ready_with_context(s,activity,&learning::unavailable_questions(s,learner)?,&h.assessed,&eligible)
}

/// Check saved quiz routes against one captured learner context. Home can have
/// hundreds of old unstarted definitions; their questions differ, while their
/// learner history, seen questions and eligible-topic set are identical.
pub(crate) fn ordinary_assessment_ready_with_context(
    s:&EntitySnapshot,activity:u64,seen:&BTreeSet<u64>,assessed:&BTreeSet<u64>,eligible:&BTreeSet<u64>,
)->Result<bool>{
    let steps=learning::lesson_steps(s,activity)?;
    if steps.iter().any(|step|seen.contains(&step.content)
        ||learning::validate_practice_question(s,step.content).is_err()) {return Ok(false);}
    let mut new = BTreeSet::new();
    for step in steps {
        let topic = s.topic_for_question(step.content)?;
        if !eligible.contains(&topic)
            || crate::assessment_sampling::band(s, step.content)?.is_none()
        {
            return Ok(false);
        }
        if !assessed.contains(&topic) {
            new.insert(topic);
        }
    }
    Ok(new.len() >= ASSESSMENT_MIN_NEW_TOPICS)
}

/// Build an ordinary assessment from current eligible supply. Callers enforce
/// cadence and whether an existing unstarted definition may be replaced.
pub fn assessment_definition(
    s: &EntitySnapshot,
    learner: u64,
    at: DateTime<Utc>,
) -> Result<Option<Definition>> {
    let h = history(s, learner)?;
    let pools = assessment_pools(s, learner, at)?;
    if pools.keys().filter(|topic| !h.assessed.contains(topic)).count()
        < ASSESSMENT_MIN_NEW_TOPICS
    {
        return Ok(None);
    }
    let policy = crate::question_selection::active_policy(s)?;
    let weights = crate::question_selection::weights_for_phase(
        s,
        policy,
        "assessment",
        crate::question_selection::Phase::Initial,
    )?
    .ok_or("assessment question weights are not configured")?;
    let loaded = learning::learning_runtime(s, learner, at)?;
    let mut topic_weights = BTreeMap::new();
    for &topic in pools.keys() {
        let mut coverage: f64 = 0.0;
        for &other in pools.keys().filter(|other| **other != topic) {
            coverage = coverage.max(
                loaded
                    .engine
                    .graph
                    .coverage(&loaded.topic_eid_to_id[&other])
                    .get(&loaded.topic_eid_to_id[&topic])
                    .copied()
                    .unwrap_or(0.0),
            );
        }
        topic_weights.insert(
            topic,
            (if h.assessed.contains(&topic) {
                1.0
            } else {
                4.0
            }) * (0.05 + 0.95 * (1.0 - coverage).powi(2)),
        );
    }
    let questions = crate::assessment_sampling::ordinary(
        s,
        learner,
        &h,
        pools,
        weights,
        topic_weights,
        &format!("assessment-{learner}-{}", s.basis_t),
    )?;
    if questions.is_empty() {
        return Ok(None);
    }
    Ok(Some(Definition {
        kind: "assessment".into(),
        topic: None,
        title: "Practice assessment".into(),
        priority: 7000.0,
        expected_seconds: questions
            .iter()
            .map(|q| crate::assessment_sampling::seconds(s, *q))
            .collect::<Result<Vec<_>>>()?
            .iter()
            .sum(),
        questions,
        remediation_for: vec![],
        retake_of: None,
        existing_activity: None,
    }))
}
pub fn relearn_topics(s: &EntitySnapshot, learner: u64) -> Result<BTreeSet<u64>> {
    Ok(history(s, learner)?
        .repairs
        .into_iter()
        .filter_map(|((_, topic), kind)| (kind == "lesson").then_some(topic))
        .collect())
}
pub(crate) fn due_topics(
    s: &EntitySnapshot,
    learner: u64,
    at: DateTime<Utc>,
) -> Result<BTreeSet<u64>> {
    let mut result = BTreeSet::new();
    let policies = s.entities.with_attribute("policy/id");
    let Some(threshold) = policies
        .first()
        .and_then(|p| s.entities[p].get("policy/review-threshold"))
        .and_then(Value::as_f64)
    else {
        return Ok(result);
    };
    for progress in s.refs(learner, "learner/knowledge-profile")? {
        let r = s.entity(progress)?;
        if r.get("progress/learned") != Some(&json!(true)) {
            continue;
        }
        if let (Some(memory), Some(interval), Some(anchor)) = (
            r.get("progress/memory").and_then(Value::as_f64),
            r.get("progress/interval-days").and_then(Value::as_f64),
            r.get("progress/memory-at"),
        ) {
            let elapsed = timestamp_days(at) - crate::schema::instant_days(anchor)?;
            if memory.is_finite()
                && interval.is_finite()
                && interval > 0.0
                && elapsed >= 0.0
                && memory * 2.0_f64.powf(-elapsed / interval) <= threshold + 1e-12
            {
                let topic = s.reference(progress, "progress/topic")?;
                if learning::topic_in_study_focus(s, learner, topic)? { result.insert(topic); }
            }
        }
    }
    Ok(result)
}

/// Existing tasks only: reads never create definitions or reserve questions.
pub fn candidates(
    s: &EntitySnapshot,
    learner: u64,
    _course: u64,
    at: DateTime<Utc>,
    _automatic: bool,
) -> Result<Vec<learning::PlannedActivity>> {
    let h = history(s, learner)?;
    let due = due_topics(s, learner, at)?;
    let mut result = vec![];
    for task in s.refs(learner, "learner/activity")? {
        let activity = s.reference(task, "learner-task/activity")?;
        let kind = kind(s, activity)?;
        if !learning::activity_in_study_focus(s, learner, activity)? { continue; }
        let mut origins = s.refs(task, "learner-task/remediation-for")?;
        if !supported(s, activity)? && origins.is_empty() {
            continue;
        }
        let status = state(s, task, "learner-task/status")?;
        let ongoing = matches!(status.as_str(), "started" | "paused");
        // Queue refresh retires superseded offers by locking them at zero
        // priority. An eligibility expansion must not revive an old quiz beside
        // its replacement. Started routes always remain resumable.
        if kind == "assessment" && status == "locked"
            && s.entity(task)?.get("learner-task/priority").and_then(Value::as_f64) == Some(0.0)
        {
            continue;
        }
        if !ongoing
            && (!matches!(status.as_str(), "locked" | "unlocked")
                || kind != "lesson" && !fresh(s, learner, activity)?)
        {
            continue;
        }
        let topic = s
            .optional_ref(activity, "activity/scope")?
            .unwrap_or_else(|| {
                learning::lesson_steps(s, activity)
                    .ok()
                    .and_then(|v| {
                        v.first()
                            .and_then(|st| s.topic_for_question(st.content).ok())
                    })
                    .unwrap_or(0)
            });
        if origins.is_empty() && !ongoing {
            origins = h
                .repairs
                .iter()
                .filter_map(|((o, t), k)| (*t == topic && k == &kind).then_some(*o))
                .collect();
        }
        let required = origins
            .iter()
            .any(|o| h.repairs.get(&(*o, topic)).is_some_and(|k| k == &kind));
        if !origins.is_empty() && !required {
            continue;
        }
        if kind == "lesson" && (!h.retry_ready(topic) || h.lesson_blocked(s, topic)?) {
            continue;
        }
        let retake = s.optional_ref(task, "learner-task/retake-of")?;
        if kind == "assessment" && !ongoing && retake.is_none()
            && !ordinary_assessment_ready(s, learner, activity, at)?
        {
            continue;
        }
        if let Some(original) = retake {
            if !h.retake_ready(s, original)? {
                continue;
            }
        }
        if !ongoing
            && !required
            && retake.is_none()
            && (kind == "review" && !due.contains(&topic)
                || kind == "assessment" && h.xp < ASSESSMENT_XP)
        {
            continue;
        }
        let globally_required = required
            && origins
                .iter()
                .any(|o| h.assessment_origin(s, *o).unwrap_or(false));
        let assessment_required =
            kind == "assessment" && retake.is_none() && h.xp >= ASSESSMENT_REQUIRED_XP;
        result.push(learning::PlannedActivity {
            activity,
            topic,
            priority: if globally_required {
                12000.0
            } else if assessment_required {
                11000.0
            } else if ongoing {
                10001.0
            } else if required {
                8000.0
            } else if kind == "review" {
                let stored = s
                    .entity(task)?
                    .get("learner-task/priority")
                    .and_then(Value::as_f64)
                    .unwrap_or(5000.0);
                if stored >= 5500.0 {
                    stored
                } else {
                    stored + 1000.0
                }
            } else {
                s.entity(task)?
                    .get("learner-task/priority")
                    .and_then(Value::as_f64)
                    .unwrap_or(5000.0)
            },
            target_count: 0,
            target_topics: vec![],
            remaining_topics: 0,
            nearest_target_steps: None,
            due: None,
            reason: if globally_required {
                "Required practice after assessment"
            } else if required {
                "Required prerequisite repair"
            } else if retake.is_some() {
                "Optional assessment retake"
            } else if assessment_required {
                "Required assessment after 150 practice XP"
            } else if ongoing {
                "Resume your activity"
            } else if kind == "assessment" {
                "Optional assessment after 120 practice XP"
            } else {
                "Spaced review is due"
            }
            .into(),
        });
    }
    Ok(result)
}
fn review_definition(
    s: &EntitySnapshot, learner: u64, topic: u64, seen: &BTreeSet<u64>,
    h: &crate::scheduling::Lifecycle, policy: u64,
) -> Result<Option<Definition>> {
    let origins: Vec<_> = h.repairs.keys().filter_map(|(origin, t)| (*t == topic).then_some(*origin)).collect();
    let mut pool = bank(s, topic, &seen)?;
    // Preserve one fresh same-KP/same-band alternative for an eventual retake.
    for &original in &h.retakes {
        for st in learning::lesson_steps(s, s.reference(original, "learner-task/activity")?)? {
            if s.topic_for_question(st.content)? != topic {
                continue;
            }
            let kp = crate::scheduling::original_kp(s, st.content)?;
            for band in 0..3 {
                let protected = pool.iter().copied().find(|q| {
                    s.owners(*q, "knowledge-point/questions").ok() == Some(vec![kp])
                        && crate::assessment_sampling::band(s, *q).ok().flatten() == Some(band)
                });
                if let Some(q) = protected {
                    pool.retain(|v| *v != q);
                }
            }
        }
    }
    if pool.len() < 5 {
        return Ok(None);
    }
    let mut questions = vec![];
    for slot in 0..5 {
        let weights = crate::question_selection::weights(s, policy, "review", slot)?;
        let Some(q) = crate::question_selection::select(
            s,
            &pool,
            weights,
            &format!("review-{learner}-{topic}-{}-{slot}", s.basis_t),
        )?
        else {
            break;
        };
        questions.push(q);
        pool.retain(|v| *v != q);
    }
    if questions.len() != 5 {
        return Ok(None);
    }
    Ok(Some(Definition {
        kind: "review".into(),
        topic: Some(topic),
        questions,
        title: format!(
            "Review: {}",
            s.entity(topic)?
                .get("topic/title")
                .and_then(Value::as_str)
                .unwrap_or("Topic")
        ),
        priority: if origins.is_empty() { 6000.0 } else { 8000.0 },
        expected_seconds: 3.0 * QUESTION_SECONDS,
        remediation_for: origins,
        retake_of: None,
        existing_activity: None,
    }))
}

/// Explicit practice uses the ordinary review selector and lifecycle policies.
pub fn selected_review(s: &EntitySnapshot, learner: u64, topic: u64) -> Result<Definition> {
    if !s.entity(topic)?.contains_key("topic/id") { return Err("Review requires a topic entity ID".into()); }
    // Manual review is the learner's choice, including before a first lesson
    // or while relearning is recommended. Automatic scheduling still uses its
    // own learned/due rules; only usable question supply limits this selector.
    let h = history(s, learner)?;
    let seen = learning::unavailable_questions(s, learner)?;
    let policy = crate::question_selection::active_policy(s)?;
    review_definition(s, learner, topic, &seen, &h, policy)?
        .ok_or_else(|| "Review needs at least five fresh, gradable questions for this topic".into())
}

pub fn schedule(
    s: &EntitySnapshot,
    learner: u64,
    course: u64,
    at: DateTime<Utc>,
) -> Result<Vec<Definition>> {
    let h = history(s, learner)?;
    let pending = candidates(s, learner, course, at, true)?;
    let seen = learning::unavailable_questions(s, learner)?;
    if due_topics(s, learner, at)?.is_empty()
        && h.repairs.is_empty()
        && h.retakes.is_empty()
        && h.xp < ASSESSMENT_XP
    {
        return Ok(vec![]);
    }
    let policy = crate::question_selection::active_policy(s)?;
    let mut definitions = vec![];
    let mut due = due_topics(s, learner, at)?;
    due.extend(h.repairs.keys().map(|(_, topic)| topic));
    for topic in due {
        if !learning::topic_in_study_focus(s, learner, topic)? { continue; }
        let origins: Vec<_> = h
            .repairs
            .keys()
            .filter_map(|(origin, t)| (*t == topic).then_some(*origin))
            .collect();
        let needs_lesson = origins.iter().any(|o| h.repairs[&(*o, topic)] == "lesson");
        let next = if needs_lesson { "lesson" } else { "review" };
        if pending
            .iter()
            .any(|p| p.topic == topic && kind(s, p.activity).ok().as_deref() == Some(next))
        {
            continue;
        }
        if needs_lesson {
            if !h.retry_ready(topic) || h.lesson_blocked(s, topic)? {
                continue;
            }
            let activity = s
                .entities
                .with_attribute("activity/id")
                .into_iter()
                .find(|a| {
                    kind(s, *a).ok().as_deref() == Some("lesson")
                        && s.optional_ref(*a, "activity/scope").ok().flatten() == Some(topic)
                });
            if let Some(activity) = activity {
                if crate::inventory::lesson_ready(
                    s,
                    &s.refs(topic, "topic/knowledge-points")?,
                    &seen,
                )? && learning::first_content(s, activity, learner)?.is_some()
                {
                    definitions.push(Definition {
                        kind: "lesson".into(),
                        topic: Some(topic),
                        questions: vec![],
                        title: "Required relearning".into(),
                        priority: 12000.0,
                        expected_seconds: 0.0,
                        remediation_for: origins,
                        retake_of: None,
                        existing_activity: Some(activity),
                    });
                }
            }
            continue;
        }
        if pending
            .iter()
            .any(|p| p.topic == topic && kind(s, p.activity).ok().as_deref() == Some("review"))
        {
            continue;
        }
        if let Some(definition) = review_definition(s, learner, topic, &seen, &h, policy)? {
            definitions.push(definition);
        }
    }
    if definitions.iter().any(|d| d.kind == "review") {
        let loaded = learning::learning_runtime(s, learner, at)?;
        let ranked=loaded.engine.rank(&loaded.learner,timestamp_days(at),definitions.iter().filter(|d|d.kind=="review").map(|d|json!({"topic":loaded.topic_eid_to_id[&d.topic.unwrap()],"expected_minutes":d.expected_seconds/60.0,"kind":"review","entityId":d.topic})).collect())?;
        let order: BTreeMap<_, _> = ranked
            .iter()
            .enumerate()
            .map(|(i, r)| (r["entityId"].as_u64().unwrap(), i))
            .collect();
        definitions.sort_by(|a, b| {
            b.priority.total_cmp(&a.priority).then_with(|| {
                order
                    .get(&a.topic.unwrap())
                    .unwrap_or(&usize::MAX)
                    .cmp(order.get(&b.topic.unwrap()).unwrap_or(&usize::MAX))
            })
        });
        for (index, d) in definitions.iter_mut().enumerate() {
            if d.kind == "review" {
                d.priority -= index as f64;
            }
        }
    }
    // Retain all required repairs; bound only ordinary background offers.
    let mut ordinary = 0;
    definitions.retain(|d| {
        if !d.remediation_for.is_empty() {
            true
        } else {
            ordinary += 1;
            ordinary <= 5
        }
    });
    let has_ordinary = pending.iter().any(|p| {
        kind(s, p.activity).ok().as_deref() == Some("assessment")
            && s.owners(p.activity, "learner-task/activity")
                .unwrap_or_default()
                .iter()
                .any(|t| {
                    s.optional_ref(*t, "learner-task/retake-of")
                        .ok()
                        .flatten()
                        .is_none()
                })
    });
    if h.xp >= ASSESSMENT_XP && !has_ordinary {
        if let Some(definition) = assessment_definition(s, learner, at)? {
            definitions.push(definition);
        }
    }
    let weights = crate::question_selection::weights_for_phase(
        s,
        policy,
        "assessment",
        crate::question_selection::Phase::Remedial,
    )?;
    for &original in &h.retakes {
        if !learning::activity_in_study_focus(s, learner,
            s.reference(original, "learner-task/activity")?)? { continue; }
        if !h.retake_ready(s, original)? {
            continue;
        }
        let questions = crate::assessment_sampling::retake(
            s,
            learner,
            original,
            &seen,
            weights.ok_or("assessment remedial weights are not configured")?,
            &format!("retake-{original}-{}", s.basis_t),
        )?;
        if !questions.is_empty() {
            definitions.push(Definition {
                kind: "assessment".into(),
                topic: None,
                title: "Optional assessment retake".into(),
                priority: 6500.0,
                expected_seconds: questions
                    .iter()
                    .map(|q| crate::assessment_sampling::seconds(s, *q).unwrap())
                    .sum(),
                questions,
                remediation_for: vec![],
                retake_of: Some(original),
                existing_activity: None,
            });
        }
    }
    Ok(definitions)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::schema::StatusAssertion;
    fn put(s: &mut EntitySnapshot, id: u64, value: Value) {
        s.entities.insert(id, value.as_object().unwrap().clone());
    }
    fn fixture() -> EntitySnapshot {
        let mut s = learning::tests::fixture();
        for (id, ident) in [
            (1100, "activity.type/review"),
            (1101, "activity.type/assessment"),
            (1102, "learner-task.status/unlocked"),
        ] {
            put(&mut s, id, json!({"db/ident":ident}));
        }
        let mut steps = vec![];
        for slot in 0..5 {
            let id = 600 + slot;
            steps.push(id);
            let mut v = json!({"step/id":format!("step-{id}"),"step/content":100+slot});
            if slot < 4 {
                v["step/next"] = json!(id + 1);
            }
            put(&mut s, id, v);
        }
        put(
            &mut s,
            60,
            json!({"activity/id":"review","activity/type":"activity.type/review","activity/scope":3,"activity/steps":steps,"activity/first-step":600}),
        );
        s.entities
            .get_mut(&9)
            .unwrap()
            .insert("learner-task/activity".into(), json!(60));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([9]));
        EntitySnapshot::new(s.entities.into(), s.basis_t).unwrap()
    }
    fn present(s: &mut EntitySnapshot, question: u64, status: &str) -> u64 {
        let mut items = s.refs(9, "learner-task/items").unwrap();
        let id = 700 + items.len() as u64;
        put(
            s,
            id,
            json!({"task-item/id":format!("item-{id}"),"task-item/content":question,"task-item/status":format!("task-item.status/{status}")}),
        );
        if let Some(previous) = items.last() {
            s.entities
                .get_mut(previous)
                .unwrap()
                .insert("task-item/next".into(), json!(id));
        }
        items.push(id);
        s.entities
            .get_mut(&9)
            .unwrap()
            .insert("learner-task/items".into(), json!(items));
        id
    }
    fn progress(s: &mut EntitySnapshot, eid: u64, topic: u64, at: DateTime<Utc>, memory: f64) {
        put(
            s,
            eid,
            json!({"progress/id":format!("progress-{eid}"),"progress/topic":topic,"progress/policy":2,"progress/repetitions":2.0,"progress/learned":true,"progress/memory":memory,"progress/memory-at":at,"progress/interval-days":1.0,"progress/assessment-accuracy":0.5,"progress/practice-accuracy":0.5,"progress/assessment-mass":0.0,"progress/practice-mass":0.0}),
        );
    }
    fn stamp(s: &mut EntitySnapshot, task: u64, at: DateTime<Utc>, status: &str) {
        s.entities
            .get_mut(&task)
            .unwrap()
            .insert("learner-task/id".into(), json!(format!("task-{task}")));
        s.basis_t = s.basis_t.max(task * 2 + 1);
        s.status_history.push(StatusAssertion {
            entity: task,
            attribute: "learner-task/status".into(),
            value: json!("learner-task.status/started"),
            t: task * 2,
            at: json!({"$instant":(at-chrono::Duration::seconds(1)).timestamp_millis()}),
        });
        s.status_history.push(StatusAssertion {
            entity: task,
            attribute: "learner-task/status".into(),
            value: json!(format!("learner-task.status/{status}")),
            t: task * 2 + 1,
            at: json!({"$instant":at.timestamp_millis()}),
        });
    }
    #[test]
    fn successful_review_credit_removes_only_its_queued_topic() {
        let mut s = fixture();
        put(&mut s, 99, json!({"topic/id":"00000000-0000-0000-0000-000000000099","topic/title":"Other topic"}));
        s.entities.get_mut(&1).unwrap().insert("learner/queue".into(), json!([3,99]));
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(), json!([3]));
        let before = s.entities.clone();
        let at = DateTime::from_timestamp_millis(1_790_760_000_000).unwrap();
        let removal = json!([crate::schema::keyword("db/retract"),1,crate::schema::keyword("learner/queue"),3]);
        for (question, correct, completed, removed) in [
            (Some(100),true,false,false),
            (None,false,true,false),
            (None,true,false,false),
            (None,true,true,true),
            (Some(100),true,true,true),
        ] {
            let forms = learning::credit(&s,1,60,question,correct,completed,"review-queue-completion",at).unwrap();
            assert_eq!(forms.contains(&removal),removed);
            assert!(!forms.iter().any(|f|f.get(2)==Some(&crate::schema::keyword("learner/targets"))));
            assert!(!forms.contains(&json!([crate::schema::keyword("db/retract"),1,crate::schema::keyword("learner/queue"),99])));
        }
        assert_eq!(s.entities,before,"planning must not mutate the snapshot");
        s.entities.get_mut(&1).unwrap().insert("learner/queue".into(),json!([99]));
        assert!(!learning::credit(&s,1,60,None,true,true,"not-queued",at).unwrap().contains(&removal));
        s.entities.get_mut(&60).unwrap().insert("activity/type".into(),json!("activity.type/assessment"));
        s.entities.get_mut(&1).unwrap().insert("learner/queue".into(),json!([3,99]));
        assert!(!learning::credit(&s,1,60,Some(100),true,true,"assessment",at).unwrap().contains(&removal));
    }

    #[test]
    fn review_route_stops_at_three_correct_and_scores_only_presented_questions() {
        let mut s = fixture();
        for slot in 0..3 {
            assert_eq!(
                learning::next_content(&s, 60, &s.refs(9, "learner-task/items").unwrap()).unwrap(),
                Some(100 + slot)
            );
            present(&mut s, 100 + slot, "correct");
        }
        let items = s.refs(9, "learner-task/items").unwrap();
        assert_eq!(
            learning::continuation(&s, 60, &items, false, 5).unwrap(),
            (None, true, 7)
        );
        assert_eq!(items.len(), 3);
        assert!(learning::continuation_state(&s, 60, &items, false, true).is_err());
        present(&mut s, 103, "correct");
        assert!(position(&s, 60, &s.refs(9, "learner-task/items").unwrap()).is_err());
    }
    #[test]
    fn review_failure_skip_and_current_presentation_are_replayed_without_extra_draws() {
        let mut s = fixture();
        let item = present(&mut s, 100, "started");
        assert_eq!(position(&s, 60, &[item]).unwrap().next, Some(100));
        s.entities
            .get_mut(&item)
            .unwrap()
            .insert("task-item/status".into(), json!("task-item.status/skipped"));
        for slot in 1..5 {
            present(
                &mut s,
                100 + slot,
                if slot == 4 { "correct" } else { "incorrect" },
            );
        }
        let items = s.refs(9, "learner-task/items").unwrap();
        assert!(position(&s, 60, &items).unwrap().failed);
        assert_eq!(xp(&s, 60, &items, 5).unwrap(), -1);
    }
    #[test]
    fn reservations_protect_active_pools_without_becoming_history() {
        let mut s = fixture();
        assert!(learning::seen_questions(&s, 1).unwrap().is_empty());
        assert_eq!(
            learning::reserved_retrieval_questions(&s, 1).unwrap().len(),
            5
        );
        assert!(!fresh(&s, 1, 60).unwrap());
        s.entities.get_mut(&9).unwrap().insert(
            "learner-task/status".into(),
            json!("learner-task.status/unlocked"),
        );
        assert!(fresh(&s, 1, 60).unwrap());
        present(&mut s, 100, "paused");
        assert!(!fresh(&s, 1, 60).unwrap());
    }
    #[test]
    fn due_reviews_need_learned_state_and_five_fresh_questions_across_modes() {
        let mut s = fixture();
        let at = Utc::now();
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([]));
        assert!(schedule(&s, 1, 5, at).unwrap().is_empty()); // Partial imports.
        assert_eq!(selected_review(&s, 1, 3).unwrap().questions.len(), 5);
        progress(&mut s, 21, 3, at, 0.1);
        let plan = schedule(&s, 1, 5, at).unwrap();
        assert_eq!(plan.len(), 1);
        assert_eq!(plan[0].kind, "review");
        let selected = selected_review(&s, 1, 3).unwrap();
        assert_eq!(selected.questions, plan[0].questions);
        assert_eq!(selected.expected_seconds, plan[0].expected_seconds);
        assert_eq!(selected.remediation_for, plan[0].remediation_for);
        let mut not_due = s.clone();
        not_due.entities.get_mut(&21).unwrap().insert("progress/memory".into(), json!(1.0));
        assert!(schedule(&not_due, 1, 5, at).unwrap().is_empty());
        assert_eq!(selected_review(&not_due, 1, 3).unwrap().questions, selected.questions);
        assert_eq!(plan[0].questions.len(), 5);
        assert_eq!(plan[0].questions.iter().collect::<BTreeSet<_>>().len(), 5);
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(true));
        assert_eq!(schedule(&s, 1, 5, at).unwrap().len(), 1);
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(false));
        s.entities.get_mut(&41).unwrap().insert(
            "knowledge-point/questions".into(),
            json!([100, 101, 102, 103]),
        );
        assert!(schedule(&s, 1, 5, at).unwrap().is_empty());
    }

    #[test]
    fn multipart_parts_do_not_supply_reviews_or_fresh_reserved_routes() {
        let mut s = fixture();
        let at = Utc::now();
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([]));
        progress(&mut s, 21, 3, at, 0.1);
        put(
            &mut s,
            850,
            json!({"multistep/id":"multipart","multistep/steps":[851]}),
        );
        put(&mut s, 851, json!({"step/id":"part","step/content":100}));
        assert!(!fresh(&s, 1, 60).unwrap());
        assert!(learning::first_content(&s, 60, 1).is_err());
        assert!(schedule(&s, 1, 5, at).unwrap().is_empty());
        let mut extra = s.entities[&104].clone();
        extra.insert("question/id".into(), json!("extra-standalone"));
        s.entities.insert(105, extra);
        s.entities.get_mut(&41).unwrap().insert(
            "knowledge-point/questions".into(),
            json!([100, 101, 102, 103, 104, 105]),
        );
        let plan = schedule(&s, 1, 5, at).unwrap();
        assert_eq!(plan.len(), 1);
        assert_eq!(
            plan[0].questions.iter().copied().collect::<BTreeSet<_>>(),
            BTreeSet::from([101, 102, 103, 104, 105])
        );
        // An old active presentation remains readable and gradeable; once it
        // finishes the next standalone route entry is served normally.
        let saved = present(&mut s, 100, "started");
        assert_eq!(position(&s, 60, &[saved]).unwrap().next, Some(100));
        assert!(learning::grade(&s, 100, &BTreeMap::from([(200, "1/2".into())])).unwrap());
        s.entities
            .get_mut(&saved)
            .unwrap()
            .insert("task-item/status".into(), json!("task-item.status/correct"));
        assert_eq!(position(&s, 60, &[saved]).unwrap().next, Some(101));
    }

    #[test]
    fn reviews_admit_five_total_questions_and_use_unrated_fallback() {
        let mut s = fixture();
        let at = Utc::now();
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([]));
        progress(&mut s, 21, 3, at, 0.1);
        let mut extra = s.entities[&104].clone();
        extra.insert("question/id".into(), json!("extra-unrated"));
        s.entities.insert(105, extra);
        // The canonical example is also in membership, but must not count.
        s.entities
            .get_mut(&41)
            .unwrap()
            .insert("knowledge-point/canonical-example".into(), json!(100));
        s.entities.get_mut(&41).unwrap().insert(
            "knowledge-point/questions".into(),
            json!([100, 101, 102, 103, 104, 105, 105]),
        );
        for (index, (q, band)) in [(101, "easy"), (102, "moderate"), (103, "hard")]
            .into_iter()
            .enumerate()
        {
            let difficulty = 2910 + index as u64;
            put(
                &mut s,
                difficulty,
                json!({"db/ident":format!("question.difficulty/{band}")}),
            );
            s.entities
                .get_mut(&q)
                .unwrap()
                .insert("question/difficulty".into(), json!(difficulty));
        }
        put(
            &mut s,
            2900,
            json!({"question-weights/activity-type":"activity.type/review",
            "question-weights/initial-easy":50.0,"question-weights/initial-moderate":40.0,"question-weights/initial-hard":10.0,
            "question-weights/remedial-easy":45.0,"question-weights/remedial-moderate":40.0,"question-weights/remedial-hard":15.0}),
        );
        s.entities
            .get_mut(&2)
            .unwrap()
            .insert("policy/question-selection-weights".into(), json!([2900]));
        s = EntitySnapshot::new(s.entities.into(), s.basis_t).unwrap();
        let plan = schedule(&s, 1, 5, at).unwrap();
        assert_eq!(plan.len(), 1);
        assert_eq!(plan[0].kind, "review");
        assert_eq!(
            plan[0].questions.iter().copied().collect::<BTreeSet<_>>(),
            BTreeSet::from([101, 102, 103, 104, 105])
        );
        s.entities
            .get_mut(&105)
            .unwrap()
            .remove("question/answer-fields");
        assert!(schedule(&s, 1, 5, at).unwrap().is_empty());
        assert!(selected_review(&s, 1, 3).unwrap_err().contains("five fresh"));
    }
    fn assessment_fixture() -> (EntitySnapshot, DateTime<Utc>) {
        let mut s = fixture();
        put(
            &mut s,
            2900,
            json!({
                "question-weights/activity-type":"activity.type/assessment",
                "question-weights/initial-easy":50.0,"question-weights/initial-moderate":40.0,"question-weights/initial-hard":10.0,
                "question-weights/remedial-easy":45.0,"question-weights/remedial-moderate":40.0,"question-weights/remedial-hard":15.0
            }),
        );
        s.entities
            .get_mut(&2)
            .unwrap()
            .insert("policy/question-selection-weights".into(), json!([2900]));
        for (id, band) in [(2910, "easy"), (2911, "moderate"), (2912, "hard")] {
            put(
                &mut s,
                id,
                json!({"db/ident":format!("question.difficulty/{band}")}),
            );
        }
        let at = Utc::now();
        let mut tasks = vec![];
        let mut topics = vec![];
        let mut profiles = vec![];
        let question = s.entities[&100].clone();
        for slot in 0..5u64 {
            let topic = 2000 + slot;
            let kp = 2100 + slot;
            let lesson = 2200 + slot;
            let review = 2300 + slot;
            let learned = 2400 + slot;
            let reviewed = 2500 + slot;
            let item = 2600 + slot;
            let q = 2700 + slot * 10;
            topics.push(topic);
            profiles.push(2800 + slot);
            tasks.extend([learned, reviewed]);
            put(
                &mut s,
                topic,
                json!({"topic/id":format!("00000000-0000-4000-8000-{topic:012}"),"topic/knowledge-points":[kp]}),
            );
            put(
                &mut s,
                kp,
                json!({"knowledge-point/id":format!("00000000-0000-4000-8000-{kp:012}"),"knowledge-point/questions":[q,q+1,q+2,q+3,q+4,q+5,q+6]}),
            );
            for offset in 0..7 {
                let mut r = question.clone();
                r.insert("question/id".into(), json!(format!("q-{}", q + offset)));
                r.insert("question/difficulty".into(), json!(2910 + offset % 3));
                s.entities.insert(q + offset, r);
            }
            let mut bank = s.refs(kp, "knowledge-point/questions").unwrap();
            for offset in 0..24u64 {
                let id = 9000 + slot * 100 + offset;
                let mut r = question.clone();
                r.insert("question/id".into(), json!(format!("fresh-{id}")));
                r.insert("question/difficulty".into(), json!(2910 + offset % 3));
                s.entities.insert(id, r);
                bank.push(id);
            }
            s.entities
                .get_mut(&kp)
                .unwrap()
                .insert("knowledge-point/questions".into(), json!(bank));
            put(
                &mut s,
                lesson,
                json!({"activity/id":format!("lesson-{lesson}"),"activity/type":"activity.type/lesson","activity/scope":topic}),
            );
            put(
                &mut s,
                review,
                json!({"activity/id":format!("review-{review}"),"activity/type":"activity.type/review","activity/scope":topic}),
            );
            put(
                &mut s,
                learned,
                json!({"learner-task/activity":lesson,"learner-task/status":"learner-task.status/completed","learner-task/xp-earned":25.0}),
            );
            put(
                &mut s,
                reviewed,
                json!({"learner-task/activity":review,"learner-task/status":"learner-task.status/completed","learner-task/xp-earned":5.0,"learner-task/items":[item]}),
            );
            put(
                &mut s,
                item,
                json!({"task-item/content":q,"task-item/status":"task-item.status/correct"}),
            );
            stamp(&mut s, learned, at - chrono::Duration::days(3), "completed");
            stamp(
                &mut s,
                reviewed,
                at - chrono::Duration::days(1),
                "completed",
            );
            progress(&mut s, 2800 + slot, topic, at, 1.0);
        }
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!(tasks));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/knowledge-profile".into(), json!(profiles));
        s.entities
            .get_mut(&7)
            .unwrap()
            .insert("module/topics".into(), json!(topics));
        // Most fixture topics are at L30; separate tests cover lower layers.
        for layer in 0..learning::MIN_STUDY_LAYER - 1 {
            let next = if layer + 1 == learning::MIN_STUDY_LAYER - 1 {
                (2000..2005).collect::<Vec<_>>()
            } else {
                vec![30000 + layer as u64 + 1]
            };
            put(&mut s, 30000 + layer as u64,
                json!({"topic/id":format!("00000000-0000-4000-8000-{:012}",30000 + layer),"topic/next":next}));
        }
        (s, at)
    }

    #[test]
    fn assessment_admission_includes_learned_topics_below_the_practice_floor() {
        let (mut s, at) = assessment_fixture();
        assert_eq!(assessment_pools(&s, 1, at).unwrap().len(), 5);
        // Move one learned topic to L29. Its successful learning still makes
        // it valid assessment evidence.
        let last = 30000 + learning::MIN_STUDY_LAYER as u64 - 2;
        s.entities.get_mut(&last).unwrap().insert("topic/next".into(), json!([2001,2002,2003,2004]));
        s.entities.get_mut(&(last - 1)).unwrap().insert("topic/next".into(), json!([last,2000]));
        assert_eq!(learning::topic_layers(&s).unwrap()[&2000] + 1, 29);
        assert_eq!(assessment_pools(&s, 1, at).unwrap().len(), 5);
        let definition = assessment_definition(&s, 1, at).unwrap().unwrap();
        assert!(definition.questions.iter().any(|q| s.topic_for_question(*q).unwrap() == 2000));
        let status = crate::inventory::assessment_status(&s, 1, at).unwrap();
        assert_eq!(status["newEligibleTopics"], 5);
        assert_eq!(status["ready"], false);
        assert_eq!(status["required"], false);
    }

    #[test]
    fn shared_assessment_readiness_keeps_freshness_eligibility_and_new_topic_rules() {
        let (mut s,at)=assessment_fixture();
        let definition=assessment_definition(&s,1,at).unwrap().unwrap();
        let steps:Vec<_>=(0..definition.questions.len()).map(|i|60000+i as u64).collect();
        for (i,q) in definition.questions.iter().enumerate(){
            let mut step=json!({"step/id":format!("readiness-{i}"),"step/content":q});
            if let Some(next)=steps.get(i+1){step["step/next"]=json!(next);}
            put(&mut s,steps[i],step);
        }
        put(&mut s,61000,json!({"activity/id":"readiness","activity/type":"activity.type/assessment",
            "activity/steps":steps,"activity/first-step":steps[0]}));
        let seen=learning::unavailable_questions(&s,1).unwrap();
        let assessed=history(&s,1).unwrap().assessed;
        let eligible=assessment_topics(&s,1,at).unwrap();
        assert_eq!(ordinary_assessment_ready(&s,1,61000,at),Ok(true));
        assert_eq!(ordinary_assessment_ready_with_context(&s,61000,&seen,&assessed,&eligible),Ok(true));
        let mut seen_answer=seen.clone();seen_answer.insert(definition.questions[0]);
        assert_eq!(ordinary_assessment_ready_with_context(&s,61000,&seen_answer,&assessed,&eligible),Ok(false));
        let mut aged=eligible.clone();aged.remove(&s.topic_for_question(definition.questions[0]).unwrap());
        assert_eq!(ordinary_assessment_ready_with_context(&s,61000,&seen,&assessed,&aged),Ok(false));
        assert_eq!(ordinary_assessment_ready_with_context(&s,61000,&seen,&eligible,&eligible),Ok(false));
    }

    #[test]
    fn focused_assessments_sample_only_targets_and_do_not_fall_back_when_short() {
        let (mut s, at) = assessment_fixture();
        s.focused_mode = true;
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(), json!([2000,2001,2002,2003,2004]));
        let definition = assessment_definition(&s, 1, at).unwrap().unwrap();
        assert!(definition.questions.iter().all(|q|
            learning::topic_in_study_focus(&s, 1, s.topic_for_question(*q).unwrap()).unwrap()));
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(), json!([2000,2001,2002,2003]));
        assert_eq!(assessment_pools(&s, 1, at).unwrap().len(), 4);
        assert!(assessment_definition(&s, 1, at).unwrap().is_none());
        s.focused_mode = false;
        assert_eq!(assessment_pools(&s, 1, at).unwrap().len(), 5);
        assert!(assessment_definition(&s, 1, at).unwrap().is_some());
    }

    #[test]
    fn focused_saved_quizzes_check_all_topics_even_when_started_or_required() {
        let (mut s, at) = assessment_fixture();
        let definition = assessment_definition(&s, 1, at).unwrap().unwrap();
        let steps: Vec<_> = definition.questions.iter().enumerate().map(|(i, _)| 50000 + i as u64).collect();
        for (i, &q) in definition.questions.iter().enumerate() {
            put(&mut s, steps[i], json!({"step/id":format!("focus-step-{i}"),"step/content":q}));
        }
        put(&mut s, 51000, json!({"activity/id":"focus-quiz","activity/type":"activity.type/assessment",
            "activity/time-limit-seconds":900,"activity/steps":steps,"activity/first-step":steps[0]}));
        for i in 0..steps.len()-1 {
            s.entities.get_mut(&steps[i]).unwrap().insert("step/next".into(), json!(steps[i+1]));
        }
        // The representative first topic is allowed, but another quiz topic is not.
        let first = s.topic_for_question(definition.questions[0]).unwrap();
        put(&mut s, 52000, json!({"learner-task/activity":51000,
            "learner-task/status":"learner-task.status/paused","learner-task/priority":12000.0}));
        let mut tasks = s.refs(1, "learner/activity").unwrap();
        tasks.push(52000);
        s.entities.get_mut(&1).unwrap().insert("learner/activity".into(), json!(tasks));
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(), json!([first]));
        s.focused_mode = true;
        assert!(!learning::activity_in_study_focus(&s, 1, 51000).unwrap());
        assert!(!candidates(&s, 1, 5, at, true).unwrap().iter().any(|p| p.activity == 51000));
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(), json!([2000,2001,2002,2003,2004]));
        assert!(learning::activity_in_study_focus(&s, 1, 51000).unwrap());
        assert!(candidates(&s, 1, 5, at, true).unwrap().iter().any(|p| p.activity == 51000));
        s.focused_mode = false;
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(), json!([]));
        assert!(learning::activity_in_study_focus(&s, 1, 51000).unwrap());
    }

    #[test]
    fn focused_reviews_are_created_only_for_target_topics() {
        let mut s = fixture();
        let at = Utc::now();
        s.entities.get_mut(&1).unwrap().insert("learner/activity".into(), json!([]));
        progress(&mut s, 21, 3, at, 0.1);
        assert_eq!(due_topics(&s, 1, at).unwrap(), BTreeSet::from([3]));
        s.focused_mode = true;
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(), json!([]));
        assert!(due_topics(&s, 1, at).unwrap().is_empty());
        assert!(schedule(&s, 1, 5, at).unwrap().is_empty());
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(), json!([3]));
        assert_eq!(schedule(&s, 1, 5, at).unwrap()[0].topic, Some(3));
    }

    #[test]
    fn assessment_admission_and_status_share_one_fresh_rated_question_rule() {
        let (mut s, at) = assessment_fixture();
        for slot in 0..5u64 {
            s.entities.get_mut(&(2100 + slot)).unwrap().insert(
                "knowledge-point/questions".into(),
                json!([2701 + slot * 10]),
            );
        }
        // Topic 2002 has only an unrated question, 2003 is no longer learned,
        // and 2004 has not reached its first-successful-lesson age threshold.
        s.entities
            .get_mut(&2721)
            .unwrap()
            .remove("question/difficulty");
        s.entities
            .get_mut(&2803)
            .unwrap()
            .insert("progress/learned".into(), json!(false));
        for event in &mut s.status_history {
            if event.entity == 2404 && event.value == json!("learner-task.status/completed") {
                event.at = json!({"$instant":(at-chrono::Duration::hours(48)+chrono::Duration::milliseconds(1)).timestamp_millis()});
            }
        }
        let pools = assessment_pools(&s, 1, at).unwrap();
        assert_eq!(
            pools.keys().copied().collect::<BTreeSet<_>>(),
            BTreeSet::from([2000, 2001])
        );
        assert!(pools.values().all(|pool| pool.len() == 1));
        assert!(
            !crate::inventory::ready(
                &s,
                &[2100],
                &learning::unavailable_questions(&s, 1).unwrap(),
                false
            )
            .unwrap()
        );
        let status = crate::inventory::assessment_status(&s, 1, at).unwrap();
        assert_eq!(status["eligibleTopics"], 2);
        assert_eq!(status["agedLearnedTopics"], 3);
        assert_eq!(status["availableQuestions"], 2);
        assert_eq!(status["newEligibleTopics"], 2);
        assert_eq!(status["minimumNewTopics"], 5);
        assert_eq!(
            status["unavailableReason"],
            "Waiting for five eligible topics not previously assessed (2/5 ready)"
        );
        s.entities
            .get_mut(&2100)
            .unwrap()
            .insert("knowledge-point/questions".into(), json!([2700])); // Seen in review.
        s.entities
            .get_mut(&2711)
            .unwrap()
            .remove("question/answer-fields");
        assert!(assessment_pools(&s, 1, at).unwrap().is_empty());
        let status = crate::inventory::assessment_status(&s, 1, at).unwrap();
        assert_eq!(status["eligibleTopics"], 0);
        assert_eq!(
            status["unavailableReason"],
            "Waiting for fresh rated questions for eligible topics"
        );
    }
    #[test]
    fn assessment_minimum_counts_only_fresh_aged_topics_not_previously_assessed() {
        let (mut s, at) = assessment_fixture();
        assert!(assessment_definition(&s, 1, at).unwrap().is_some());
        // An older completed assessment establishes prior exposure independently
        // of subsequent relearning, reviews, or positive practice XP.
        put(&mut s, 6000, json!({"learner-task/activity":6001,
            "learner-task/status":"learner-task.status/completed","learner-task/items":[6003]}));
        put(&mut s, 6001, json!({"activity/type":"activity.type/assessment",
            "activity/steps":[6002],"activity/first-step":6002}));
        put(&mut s, 6002, json!({"step/content":2701}));
        put(&mut s, 6003, json!({"task-item/content":2701,"task-item/status":"task-item.status/correct"}));
        s.entities.get_mut(&1).unwrap().get_mut("learner/activity").unwrap().as_array_mut().unwrap().push(json!(6000));
        s.status_history.push(crate::schema::StatusAssertion {entity:6000,
            attribute:"learner-task/status".into(),value:json!("learner-task.status/completed"),t:1,
            at:json!({"$instant":(at-chrono::Duration::days(7)).timestamp_millis()})});
        assert_eq!(assessment_pools(&s,1,at).unwrap().len(),5);
        assert!(assessment_definition(&s,1,at).unwrap().is_none());
        let status=crate::inventory::assessment_status(&s,1,at).unwrap();
        assert_eq!(status["newEligibleTopics"],4);
        assert_eq!(status["practiceXp"],150.0);
        assert_eq!(status["required"],false);
        assert_eq!(status["unavailableReason"],"Waiting for five eligible topics not previously assessed (4/5 ready)");
        s.entities.get_mut(&2400).unwrap().insert("learner-task/xp-earned".into(),json!(125.0));
        assert_eq!(history(&s,1).unwrap().xp,250.0,"Waiting never resets practice XP");
        assert!(schedule(&s,1,5,at).unwrap().is_empty());

        let (mut s,at)=assessment_fixture();
        s.entities.get_mut(&2104).unwrap().insert("knowledge-point/questions".into(),json!([]));
        assert_eq!(assessment_topics(&s,1,at).unwrap().len(),5);
        assert!(assessment_definition(&s,1,at).unwrap().is_none());
        assert_eq!(crate::inventory::assessment_status(&s,1,at).unwrap()["newEligibleTopics"],4);
    }

    #[test]
    fn assessments_use_updated_initial_weights_and_require_configuration() {
        let (mut s, at) = assessment_fixture();
        for (id, band) in [(2910, "easy"), (2911, "moderate"), (2912, "hard")] {
            put(
                &mut s,
                id,
                json!({"db/ident":format!("question.difficulty/{band}")}),
            );
        }
        for slot in 0..5u64 {
            for offset in 1..7u64 {
                s.entities
                    .get_mut(&(2700 + slot * 10 + offset))
                    .unwrap()
                    .insert("question/difficulty".into(), json!(2910 + (offset - 1) % 3));
            }
        }
        for (band, value) in [("easy", 100.0), ("moderate", 0.0), ("hard", 0.0)] {
            s.entities
                .get_mut(&2900)
                .unwrap()
                .insert(format!("question-weights/initial-{band}"), json!(value));
        }
        // An opposite remedial distribution must not affect ordinary quizzes.
        for (band, value) in [("easy", 0.0), ("moderate", 0.0), ("hard", 100.0)] {
            s.entities
                .get_mut(&2900)
                .unwrap()
                .insert(format!("question-weights/remedial-{band}"), json!(value));
        }
        let first = schedule(&s, 1, 5, at).unwrap();
        assert_eq!(first[0].questions.len(), 5);
        assert!([2910, 2911, 2912].iter().all(|b| {
            first[0]
                .questions
                .iter()
                .any(|q| s.reference(*q, "question/difficulty").unwrap() == *b)
        }));
        // Five distinct topics can fill at most twelve minutes while retaining
        // all three available bands; duration takes precedence over the draw weights.
        assert_eq!(first[0].expected_seconds, 720.0);
        assert_eq!(
            first[0]
                .questions
                .iter()
                .filter(|q| s.reference(**q, "question/difficulty").unwrap() == 2910)
                .count(),
            1
        );
        s.entities
            .get_mut(&2900)
            .unwrap()
            .insert("question-weights/initial-easy".into(), json!(0.0));
        s.entities
            .get_mut(&2900)
            .unwrap()
            .insert("question-weights/initial-hard".into(), json!(100.0));
        let updated = schedule(&s, 1, 5, at).unwrap();
        assert!([2910, 2911, 2912].iter().all(|b| {
            updated[0]
                .questions
                .iter()
                .any(|q| s.reference(*q, "question/difficulty").unwrap() == *b)
        }));
        assert_eq!(
            updated[0]
                .questions
                .iter()
                .filter(|q| s.reference(**q, "question/difficulty").unwrap() == 2912)
                .count(),
            3
        );
        assert_ne!(first[0].questions, updated[0].questions);
        s.entities
            .get_mut(&2)
            .unwrap()
            .remove("policy/question-selection-weights");
        assert!(
            schedule(&s, 1, 5, at)
                .unwrap_err()
                .to_string()
                .contains("assessment question weights are not configured")
        );
    }

    #[test]
    fn assessment_cadence_offers_at_120_signed_xp_with_mature_topics_and_fresh_questions() {
        let (mut s, at) = assessment_fixture();
        let plans = schedule(&s, 1, 5, at).unwrap();
        assert_eq!(plans.len(), 1);
        assert_eq!(plans[0].kind, "assessment");
        assert_eq!(plans[0].questions.len(), 5);
        assert_eq!(
            plans[0]
                .questions
                .iter()
                .map(|q| s.topic_for_question(*q).unwrap())
                .collect::<BTreeSet<_>>()
                .len(),
            5
        );
        assert!(
            plans[0]
                .questions
                .iter()
                .all(|q| !learning::seen_questions(&s, 1).unwrap().contains(q))
        );
        s.entities
            .get_mut(&2400)
            .unwrap()
            .insert("learner-task/xp-earned".into(), json!(24.0));
        assert_eq!(schedule(&s, 1, 5, at).unwrap()[0].kind, "assessment");
        s.entities
            .get_mut(&2400)
            .unwrap()
            .insert("learner-task/xp-earned".into(), json!(25.0));
        s.status_history.retain(|event| event.entity != 2500);
        // Losing five finalized review XP affects cadence, not topic admission.
        assert_eq!(schedule(&s, 1, 5, at).unwrap()[0].kind, "assessment");
        s.entities
            .get_mut(&2400)
            .unwrap()
            .insert("learner-task/xp-earned".into(), json!(30.0));
        assert_eq!(schedule(&s, 1, 5, at).unwrap()[0].questions.len(), 5);
    }

    #[test]
    fn assessments_admit_unreviewed_topics_at_exactly_48_hours_from_any_course_or_study_mode() {
        let (mut s, at) = assessment_fixture();
        // The entire 150 XP comes from lessons, with no review tasks at all.
        let tasks: Vec<_> = (2400..2405).collect();
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!(tasks));
        for task in &tasks {
            s.entities
                .get_mut(task)
                .unwrap()
                .insert("learner-task/xp-earned".into(), json!(30.0));
        }
        put(&mut s, 5000, json!({"course/units":[]}));
        for event in &mut s.status_history {
            if event.entity == 2400 && event.value == json!("learner-task.status/completed") {
                event.at = json!({"$instant":(at - chrono::Duration::hours(48) + chrono::Duration::milliseconds(1)).timestamp_millis()});
            }
        }
        assert_eq!(assessment_pools(&s,1,at).unwrap().len(),4);
        assert!(schedule(&s, 1, 5000, at).unwrap().is_empty());
        for event in &mut s.status_history {
            if event.entity == 2400 && event.value == json!("learner-task.status/completed") {
                event.at =
                    json!({"$instant":(at - chrono::Duration::hours(48)).timestamp_millis()});
            }
        }
        for directed in [false, true] {
            s.entities
                .get_mut(&1)
                .unwrap()
                .insert("learner/self-directed".into(), json!(directed));
            let plans = schedule(&s, 1, 5000, at).unwrap();
            assert_eq!(plans.len(), 1);
            assert_eq!(plans[0].kind, "assessment");
            assert_eq!(plans[0].questions.len(), 5);
            assert_eq!(
                plans[0].questions,
                schedule(&s, 1, 5, at).unwrap()[0].questions
            );
        }
    }

    #[test]
    fn recent_reviews_do_not_restart_assessment_age_and_reviews_do_not_wait_48_hours() {
        let (mut s, at) = assessment_fixture();
        for event in &mut s.status_history {
            if event.entity == 2500 {
                event.at =
                    json!({"$instant":(at - chrono::Duration::minutes(1)).timestamp_millis()});
            }
        }
        assert_eq!(schedule(&s, 1, 5, at).unwrap()[0].kind, "assessment");
        for event in &mut s.status_history {
            if (2400..2405).contains(&event.entity) {
                event.at = json!({"$instant":(at - chrono::Duration::hours(1)).timestamp_millis()});
            }
        }
        s.entities
            .get_mut(&2800)
            .unwrap()
            .insert("progress/memory".into(), json!(0.1));
        let plans = schedule(&s, 1, 5, at).unwrap();
        assert_eq!(plans.len(), 1);
        assert_eq!(plans[0].kind, "review");
        assert_eq!(plans[0].topic, Some(2000));
    }
    #[test]
    fn assessment_completion_resets_cadence_and_all_wrong_or_unanswered_slots_create_remediation() {
        let (mut s, at) = assessment_fixture();
        put(
            &mut s,
            3000,
            json!({"activity/id":"assessment","activity/type":"activity.type/assessment","activity/steps":[3100,3101,3102],"activity/first-step":3100}),
        );
        put(
            &mut s,
            3001,
            json!({"learner-task/activity":3000,"learner-task/status":"learner-task.status/completed","learner-task/items":[3002,3003]}),
        );
        put(
            &mut s,
            3002,
            json!({"task-item/content":2701,"task-item/status":"task-item.status/paused","task-item/next":3003}),
        );
        put(
            &mut s,
            3003,
            json!({"task-item/content":2711,"task-item/status":"task-item.status/paused"}),
        );
        let mut tasks = s.refs(1, "learner/activity").unwrap();
        tasks.push(3001);
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!(tasks));
        for (id, q) in [(3100, 2701), (3101, 2711), (3102, 2721)] {
            let mut v = json!({"step/id":format!("step-{id}"),"step/content":q});
            if id < 3102 {
                v["step/next"] = json!(id + 1);
            }
            put(&mut s, id, v);
        }
        stamp(&mut s, 3001, at, "completed");
        let h = history(&s, 1).unwrap();
        assert_eq!(h.xp, 0.0);
        assert!(h.repairs.keys().any(|(_, topic)| *topic == 2000));
        let plans = schedule(&s, 1, 5, at).unwrap();
        assert_eq!(plans.len(), 3);
        assert_eq!(plans[0].kind, "review");
        assert_eq!(
            plans
                .iter()
                .filter_map(|p| p.topic)
                .collect::<BTreeSet<_>>(),
            BTreeSet::from([2000, 2001, 2002])
        );
        assert_eq!(plans[0].priority, 8000.0);
        // A quiz miss is still repaired immediately after a course/mode switch.
        put(&mut s, 5000, json!({"course/units":[]}));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(true));
        let plans = schedule(&s, 1, 5000, at).unwrap();
        assert_eq!(plans.len(), 3);
        assert_eq!(plans[0].kind, "review");
        assert_eq!(
            plans
                .iter()
                .filter_map(|p| p.topic)
                .collect::<BTreeSet<_>>(),
            BTreeSet::from([2000, 2001, 2002])
        );
    }
    #[test]
    fn ordinary_failed_review_only_updates_state_and_can_become_due_again() {
        let mut s = fixture();
        let at = Utc::now();
        progress(&mut s, 21, 3, at, 0.1);
        s.entities.get_mut(&9).unwrap().insert(
            "learner-task/status".into(),
            json!("learner-task.status/failed"),
        );
        stamp(&mut s, 9, at, "failed");
        assert!(relearn_topics(&s, 1).unwrap().is_empty());
        assert_eq!(schedule(&s, 1, 5, at).unwrap()[0].kind, "review");
        assert!(
            !learning::engine_candidates(&s, 1, 5, at)
                .unwrap()
                .iter()
                .any(|p| p.activity == 20)
        );
    }
}
