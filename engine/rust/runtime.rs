//! Automatic item-completion boundary. Returned guarded transactions are the
//! only writes: a rejected or conflicting operation leaves the loaded engine intact.
use crate::Result;
use crate::activities::*;
use crate::core::{Event, FireEngine, TopicState};
use crate::schema::{
    EntitySnapshot, LoadedRuntime, TransactionPlan, completion_transaction, keyword,
    task_transaction, value_id_string,
};
use crate::timing;
use chrono::{DateTime, Timelike, Utc};
use num_rational::BigRational;
use num_traits::ToPrimitive;
use serde::{Deserialize, Serialize};
use serde_json::{Map, Value, json};
use std::collections::{BTreeMap, BTreeSet};

type Entity = Map<String, Value>;

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(default, deny_unknown_fields)]
pub struct ActivityRules {
    pub diagnostic_skip_policy: String,
    pub diagnostic_uses_assessment_accuracy: bool,
    pub use_fitted_xp: bool,
}
impl Default for ActivityRules {
    fn default() -> Self {
        Self {
            diagnostic_skip_policy: "negative".into(),
            diagnostic_uses_assessment_accuracy: false,
            use_fitted_xp: false,
        }
    }
}
impl ActivityRules {
    pub fn validate(&self) -> Result<()> {
        if !matches!(self.diagnostic_skip_policy.as_str(), "negative" | "neutral") {
            return Err("diagnostic skip policy must be negative or neutral".into());
        }
        Ok(())
    }
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize, Default)]
pub struct Delivery {
    pub complete: bool,
    pub passed: Option<bool>,
    pub next_content: Vec<u64>,
    pub retry_question: Option<u64>,
    pub needs_questions_for: Option<u64>,
}
pub struct Completion {
    pub transaction: TransactionPlan,
    pub engine: FireEngine,
    pub delivery: Delivery,
}
#[derive(Clone, Debug)]
pub struct CompletionOptions {
    pub completed_at: DateTime<Utc>,
    pub result: Option<bool>,
    pub performance: f64,
    pub response_refs: Vec<Value>,
    pub response_entities: Vec<Value>,
    pub take_retry: Option<bool>,
    pub xp_award: Option<i64>,
    pub rules: ActivityRules,
}
impl CompletionOptions {
    pub fn new(completed_at: DateTime<Utc>) -> Self {
        Self {
            completed_at,
            result: None,
            performance: 1.0,
            response_refs: vec![],
            response_entities: vec![],
            take_retry: None,
            xp_award: None,
            rules: ActivityRules::default(),
        }
    }
}
fn days(at: DateTime<Utc>) -> f64 {
    crate::schema::timestamp_days(at)
}
fn seconds_between(end: DateTime<Utc>, start: DateTime<Utc>) -> f64 {
    let delta = end - start;
    delta.num_seconds() as f64 + delta.subsec_nanos() as f64 / 1e9
}
fn number(value: &Value, name: &str) -> Result<f64> {
    value
        .as_f64()
        .filter(|n| n.is_finite())
        .ok_or_else(|| format!("{name} must be a finite number"))
}
fn positive(value: f64, name: &str) -> Result<()> {
    if !value.is_finite() || value <= 0.0 {
        return Err(format!("{name} must be positive and finite"));
    }
    Ok(())
}
fn owners(snapshot: &EntitySnapshot, attr: &str, child: u64) -> Result<Vec<u64>> {
    let mut result = vec![];
    for eid in snapshot.entities.keys() {
        if snapshot.refs(*eid, attr)?.contains(&child) {
            result.push(*eid);
        }
    }
    Ok(result)
}
fn kind(snapshot: &EntitySnapshot, eid: u64, names: &[&str]) -> Result<String> {
    let entity = snapshot.entity(eid)?;
    let kinds: Vec<_> = names
        .iter()
        .filter(|n| entity.contains_key(&format!("{n}/id")))
        .collect();
    if kinds.len() != 1 {
        return Err(format!("{eid} must identify exactly one of {names:?}"));
    }
    Ok((*kinds[0]).into())
}
fn ordered(snapshot: &EntitySnapshot, ids: Vec<u64>, index: &str) -> Result<Vec<u64>> {
    let mut indices = BTreeMap::new();
    for eid in ids {
        let n = snapshot
            .entity(eid)?
            .get(index)
            .and_then(Value::as_u64)
            .filter(|n| *n > 0)
            .ok_or_else(|| format!("{index} must be positive and unique within its owner"))?;
        if indices.insert(n, eid).is_some() {
            return Err(format!(
                "{index} must be positive and unique within its owner"
            ));
        }
    }
    Ok(indices.into_values().collect())
}
fn task_items(snapshot: &EntitySnapshot, task: u64) -> Result<Vec<u64>> {
    let members: BTreeSet<_> = snapshot
        .refs(task, "learner-task/items")?
        .into_iter()
        .collect();
    if members.is_empty() {
        return Ok(vec![]);
    }
    let mut incoming = BTreeMap::new();
    let mut next = BTreeMap::new();
    for &item in &members {
        if snapshot.owners(item, "learner-task/items")? != vec![task] {
            return Err("task chain item must belong exclusively to its task".into());
        }
        let predecessors = snapshot.owners(item, "task-item/next")?;
        if predecessors
            .iter()
            .any(|previous| !members.contains(previous))
        {
            return Err("task-item/next predecessor belongs outside the task".into());
        }
        if predecessors.len() > 1 {
            return Err("task-item/next cannot merge presentation paths".into());
        }
        incoming.insert(item, predecessors.len());
        if let Some(following) = snapshot.optional_ref(item, "task-item/next")? {
            if !members.contains(&following) {
                return Err("task-item/next must reference another item in its task".into());
            }
            next.insert(item, following);
        }
    }
    let heads: Vec<_> = members
        .iter()
        .filter(|item| incoming[item] == 0)
        .copied()
        .collect();
    if heads.len() != 1 {
        return Err("task presentation chain must have exactly one head".into());
    }
    let mut ordered = vec![];
    let mut visited = BTreeSet::new();
    let mut current = Some(heads[0]);
    while let Some(item) = current {
        if !visited.insert(item) {
            return Err("task presentation chain contains a cycle".into());
        }
        ordered.push(item);
        current = next.get(&item).copied();
    }
    if visited != members {
        return Err("task presentation chain contains disconnected items".into());
    }
    Ok(ordered)
}
fn result(snapshot: &EntitySnapshot, entity: &Entity) -> Result<Outcome> {
    let Some(value) = entity.get("task-item/status").filter(|v| !v.is_null()) else {
        return Ok(None);
    };
    match snapshot.ident(value)?.trim_start_matches(':') {
        "task-item.status/correct" => Ok(Some(true)),
        "task-item.status/incorrect" => Ok(Some(false)),
        "task-item.status/skipped" => Ok(None),
        _ => Err("unknown question result".into()),
    }
}
fn content_id(snapshot: &EntitySnapshot, item: &Entity) -> Result<Option<u64>> {
    item.get("task-item/content")
        .filter(|v| !v.is_null())
        .map(|v| snapshot.eid(v))
        .transpose()
}
fn question(snapshot: &EntitySnapshot, item: &Entity) -> Result<bool> {
    Ok(match content_id(snapshot, item)? {
        Some(content) => {
            let record = snapshot.entity(content)?;
            record.contains_key("question/id")
                && !snapshot.is_example(content)
        }
        None => false,
    })
}
fn question_pool(snapshot: &EntitySnapshot, activity: u64, attr: &str) -> Result<Vec<u64>> {
    let pool = snapshot.refs(activity, attr)?;
    if pool.is_empty() {
        return Err("activity needs an available question pool".into());
    }
    for q in &pool {
        snapshot.topic_for_question(*q)?;
    }
    Ok(pool)
}
pub fn scope_topics(snapshot: &EntitySnapshot, scope: u64) -> Result<BTreeSet<u64>> {
    fn walk(
        snapshot: &EntitySnapshot,
        eid: u64,
        topics: &mut BTreeSet<u64>,
        active: &mut BTreeSet<u64>,
    ) -> Result<()> {
        if active.contains(&eid) {
            return Err("curriculum scope contains a cycle".into());
        }
        let kind = kind(snapshot, eid, &["course", "unit", "module", "topic"])?;
        if kind == "topic" {
            topics.insert(eid);
            return Ok(());
        }
        active.insert(eid);
        let attr = match kind.as_str() {
            "course" => "course/units",
            "unit" => "unit/modules",
            _ => "module/topics",
        };
        for child in snapshot.refs(eid, attr)? {
            walk(snapshot, child, topics, active)?;
        }
        active.remove(&eid);
        Ok(())
    }
    let mut topics = BTreeSet::new();
    walk(snapshot, scope, &mut topics, &mut BTreeSet::new())?;
    let mut pending: Vec<_> = topics.iter().copied().collect();
    while let Some(topic) = pending.pop() {
        for prerequisite in snapshot.owners(topic, "topic/next")? {
            kind(snapshot, prerequisite, &["topic"])?;
            if topics.insert(prerequisite) {
                pending.push(prerequisite);
            }
        }
    }
    Ok(topics)
}

struct SelectionContext {
    policy: u64,
    learner: u64,
    task: u64,
}
fn selected_questions(
    snapshot: &EntitySnapshot,
    context: &SelectionContext,
    activity_type: &str,
    bank: u64,
    answered: usize,
    remaining: Vec<u64>,
) -> Result<Vec<u64>> {
    let seen =
        crate::question_selection::seen_before_task(snapshot, context.learner, context.task)?;
    let remaining: Vec<_> = remaining
        .into_iter()
        .filter(|q| !seen.contains(q))
        .collect();
    let weights =
        crate::question_selection::weights(snapshot, context.policy, activity_type, answered)?;
    if weights.is_none() {
        return Ok(remaining);
    }
    let seed = format!("task-{}/kp-{bank}/slot-{answered}", context.task);
    Ok(
        crate::question_selection::select(snapshot, &remaining, weights, &seed)?
            .into_iter()
            .collect(),
    )
}

fn lesson_delivery(
    snapshot: &EntitySnapshot,
    activity: u64,
    items: &[Entity],
    context: &SelectionContext,
) -> Result<Delivery> {
    let topic = snapshot.reference(activity, "lesson/topic")?;
    let members: BTreeSet<_> = snapshot
        .refs(topic, "topic/knowledge-points")?
        .into_iter()
        .collect();
    let steps = ordered(
        snapshot,
        snapshot.refs(activity, "lesson/steps")?,
        "lesson-step/index",
    )?;
    if steps.is_empty() || members.is_empty() {
        return Err("lesson needs steps and at least one assessed knowledge point".into());
    }
    let mut placements = vec![];
    let mut seen_kps = BTreeSet::new();
    for step in steps {
        let content = snapshot.reference(step, "lesson-step/content")?;
        let k = kind(snapshot, content, &["tutorial", "knowledge-point"])?;
        let presentation = if k == "knowledge-point" {
            if !members.contains(&content) || !seen_kps.insert(content) {
                return Err("lesson knowledge-point membership is invalid or repeated".into());
            }
            snapshot.reference(content, "knowledge-point/canonical-example")?
        } else {
            content
        };
        placements.push((content, k, presentation));
    }
    if seen_kps != members {
        return Err("lesson does not cover all topic knowledge points".into());
    }
    let mut cursor = 0;
    for (content, k, presentation) in placements {
        if cursor == items.len() {
            return Ok(Delivery {
                next_content: vec![presentation],
                ..Default::default()
            });
        }
        if content_id(snapshot, &items[cursor])? != Some(presentation) {
            return Err("item does not follow the authored lesson sequence".into());
        }
        cursor += 1;
        if k == "tutorial" {
            continue;
        }
        let pool = question_pool(snapshot, content, "knowledge-point/questions")?;
        let mut outcomes = vec![];
        let mut used = BTreeSet::new();
        while cursor < items.len() {
            let q = content_id(snapshot, &items[cursor])?;
            let Some(q) = q.filter(|q| pool.contains(q)) else {
                break;
            };
            if !used.insert(q) {
                return Err("lesson practice must use a fresh question".into());
            }
            if snapshot.topic_for_question(q)? != topic {
                return Err("lesson question resolves to another topic".into());
            }
            outcomes.push(result(snapshot, &items[cursor])?);
            cursor += 1;
            if evaluate_kp_prefix(&outcomes)?.complete() {
                break;
            }
        }
        let decision = evaluate_kp_prefix(&outcomes)?;
        if !decision.complete() {
            let remaining: Vec<_> = pool.into_iter().filter(|q| !used.contains(q)).collect();
            let remaining = selected_questions(
                snapshot,
                context,
                "lesson",
                content,
                outcomes.len(),
                remaining,
            )?;
            if cursor != items.len() {
                return Err("cannot advance before knowledge-point mastery".into());
            }
            return Ok(if remaining.is_empty() {
                Delivery {
                    needs_questions_for: Some(content),
                    ..Default::default()
                }
            } else {
                Delivery {
                    next_content: remaining,
                    ..Default::default()
                }
            });
        }
        if decision.passed() == Some(false) {
            if cursor != items.len() {
                return Err("items follow a failed lesson".into());
            }
            return Ok(Delivery {
                complete: true,
                passed: Some(false),
                ..Default::default()
            });
        }
    }
    if cursor != items.len() {
        return Err("items follow the end of the lesson".into());
    }
    Ok(Delivery {
        complete: true,
        passed: Some(true),
        ..Default::default()
    })
}

/// Validate the entire authored graph and identify original wrong answers
/// replaced by completed silly-mistake retries. An unanswered retry replaces nothing.
fn diagnostic_path(
    snapshot: &EntitySnapshot,
    activity: u64,
    items: &[Entity],
    take_retry: Option<bool>,
) -> Result<(Delivery, BTreeSet<usize>)> {
    let probes: BTreeSet<_> = snapshot
        .refs(activity, "diagnostic/probes")?
        .into_iter()
        .collect();
    let start = snapshot.reference(activity, "diagnostic/start")?;
    if probes.is_empty() || !probes.contains(&start) {
        return Err("diagnostic start must be an owned probe".into());
    }
    let eligible = scope_topics(snapshot, snapshot.reference(activity, "diagnostic/scope")?)?;
    const BRANCHES: [&str; 4] = [
        "on-correct",
        "on-incorrect",
        "on-skipped",
        "on-silly-mistake",
    ];
    for probe in &probes {
        let q = snapshot.reference(*probe, "diagnostic-probe/question")?;
        let topic = snapshot.topic_for_question(q)?;
        if !eligible.contains(&topic) {
            return Err("probe topic is outside diagnostic scope and its foundations".into());
        }
        for branch in BRANCHES {
            if snapshot
                .optional_ref(*probe, &format!("diagnostic-probe/{branch}"))?
                .is_some_and(|t| !probes.contains(&t))
            {
                return Err("diagnostic branch leaves its owner".into());
            }
        }
        if let Some(alternate) =
            snapshot.optional_ref(*probe, "diagnostic-probe/on-silly-mistake")?
        {
            let other = snapshot.reference(alternate, "diagnostic-probe/question")?;
            let difficulty =
                snapshot.ident(&json!(snapshot.reference(q, "question/difficulty")?))?;
            let other_difficulty =
                snapshot.ident(&json!(snapshot.reference(other, "question/difficulty")?))?;
            if other == q
                || snapshot.topic_for_question(other)? != topic
                || ![
                    "question.difficulty/easy",
                    "question.difficulty/moderate",
                    "question.difficulty/hard",
                ]
                .contains(&difficulty.as_str())
                || difficulty != other_difficulty
                || snapshot
                    .optional_ref(alternate, "diagnostic-probe/on-silly-mistake")?
                    .is_some()
            {
                return Err(
                    "retry must be one different same-topic/same-difficulty question".into(),
                );
            }
            if let Some(ordinary) =
                snapshot.optional_ref(*probe, "diagnostic-probe/on-incorrect")?
                && snapshot.reference(ordinary, "diagnostic-probe/question")? == other
            {
                return Err("incorrect and retry branches must be distinguishable from recorded question identity".into());
            }
        }
    }
    fn visit(
        snapshot: &EntitySnapshot,
        probe: u64,
        active: &mut BTreeSet<u64>,
        finished: &mut BTreeSet<u64>,
    ) -> Result<()> {
        if active.contains(&probe) {
            return Err("diagnostic branches must terminate".into());
        }
        if finished.contains(&probe) {
            return Ok(());
        }
        active.insert(probe);
        for branch in BRANCHES {
            if let Some(t) = snapshot.optional_ref(probe, &format!("diagnostic-probe/{branch}"))? {
                visit(snapshot, t, active, finished)?;
            }
        }
        active.remove(&probe);
        finished.insert(probe);
        Ok(())
    }
    let (mut active, mut finished) = (BTreeSet::new(), BTreeSet::new());
    for probe in &probes {
        visit(snapshot, *probe, &mut active, &mut finished)?;
    }
    let mut probe = Some(start);
    let mut superseded = BTreeSet::new();
    for (index, item) in items.iter().enumerate() {
        let current = probe.ok_or("item does not follow the diagnostic graph")?;
        if content_id(snapshot, item)?
            != Some(snapshot.reference(current, "diagnostic-probe/question")?)
        {
            return Err("item does not follow the diagnostic graph".into());
        }
        let result = result(snapshot, item)?;
        let branch = match result {
            Some(true) => "on-correct",
            Some(false) => "on-incorrect",
            None => "on-skipped",
        };
        let ordinary = snapshot.optional_ref(current, &format!("diagnostic-probe/{branch}"))?;
        let retry = if result == Some(false) {
            snapshot.optional_ref(current, "diagnostic-probe/on-silly-mistake")?
        } else {
            None
        };
        if index + 1 < items.len() {
            let next_question = content_id(snapshot, &items[index + 1])?;
            let mut choices = BTreeSet::new();
            for p in [ordinary, retry].into_iter().flatten() {
                if Some(snapshot.reference(p, "diagnostic-probe/question")?) == next_question {
                    choices.insert(p);
                }
            }
            if choices.len() != 1 {
                return Err("recorded diagnostic continuation is ambiguous or invalid".into());
            }
            probe = choices.into_iter().next();
            if probe == retry {
                superseded.insert(index);
            }
        } else {
            if retry.is_some() && take_retry.is_none() {
                return Err(
                    "choose whether to accept the offered retry before completing this item".into(),
                );
            }
            if take_retry == Some(true) && retry.is_none() {
                return Err("no retry is available for this result".into());
            }
            let selected = if take_retry == Some(true) {
                retry
            } else {
                ordinary
            };
            let next_content = selected
                .map(|p| snapshot.reference(p, "diagnostic-probe/question"))
                .transpose()?
                .into_iter()
                .collect();
            let retry_question = retry
                .map(|p| snapshot.reference(p, "diagnostic-probe/question"))
                .transpose()?;
            return Ok((
                Delivery {
                    complete: selected.is_none(),
                    next_content,
                    retry_question,
                    ..Default::default()
                },
                superseded,
            ));
        }
    }
    Ok((
        Delivery {
            next_content: vec![snapshot.reference(start, "diagnostic-probe/question")?],
            ..Default::default()
        },
        superseded,
    ))
}
fn delivery(
    snapshot: &EntitySnapshot,
    activity: u64,
    kind: &str,
    items: &[Entity],
    take_retry: Option<bool>,
    context: &SelectionContext,
) -> Result<Delivery> {
    if kind == "lesson" {
        return lesson_delivery(snapshot, activity, items, context);
    }
    if kind == "diagnostic" {
        return Ok(diagnostic_path(snapshot, activity, items, take_retry)?.0);
    }
    let mut questions = vec![];
    for item in items {
        if !question(snapshot, item)? {
            return Err(format!("{kind} contains only questions"));
        }
        questions.push(content_id(snapshot, item)?.unwrap());
    }
    if kind == "multistep" {
        let steps = ordered(
            snapshot,
            snapshot.refs(activity, "multistep/steps")?,
            "multistep-step/index",
        )?;
        let all: Vec<_> = steps
            .iter()
            .map(|s| snapshot.reference(*s, "multistep-step/question"))
            .collect::<Result<_>>()?;
        if all.is_empty() || questions.len() > all.len() || questions != all[..questions.len()] {
            return Err("items must follow multistep question placements".into());
        }
        return Ok(Delivery {
            complete: questions.len() == all.len(),
            next_content: all.get(questions.len()).copied().into_iter().collect(),
            ..Default::default()
        });
    }
    let pool = question_pool(snapshot, activity, &format!("{kind}/questions"))?;
    let used: BTreeSet<_> = questions.iter().copied().collect();
    if used.len() != questions.len() || questions.iter().any(|q| !pool.contains(q)) {
        return Err("questions must be distinct members of the activity".into());
    }
    let remaining: Vec<_> = pool.iter().filter(|q| !used.contains(q)).copied().collect();
    if kind == "review" {
        let topic = snapshot.reference(activity, "review/topic")?;
        if pool.len() != 5 {
            return Err("live review requires five questions from its target topic".into());
        }
        for q in pool {
            if snapshot.topic_for_question(q)? != topic {
                return Err("live review requires five questions from its target topic".into());
            }
        }
        let outcomes = items
            .iter()
            .map(|i| result(snapshot, i))
            .collect::<Result<Vec<_>>>()?;
        let decision = evaluate_review_prefix(&outcomes)?;
        let remaining = if decision.complete() {
            vec![]
        } else {
            selected_questions(
                snapshot,
                context,
                "review",
                activity,
                outcomes.len(),
                remaining,
            )?
        };
        let needs_questions_for = (!decision.complete() && remaining.is_empty()).then_some(topic);
        return Ok(Delivery {
            complete: decision.complete(),
            passed: decision.passed(),
            next_content: remaining,
            needs_questions_for,
            ..Default::default()
        });
    }
    Ok(Delivery {
        complete: remaining.is_empty(),
        next_content: remaining,
        ..Default::default()
    })
}
fn place_diagnostic(
    loaded: &LoadedRuntime,
    engine: &mut FireEngine,
    activity: u64,
    items: &[Entity],
    at: f64,
    rules: &ActivityRules,
) -> Result<()> {
    let snapshot = &loaded.snapshot;
    let superseded = diagnostic_path(snapshot, activity, items, Some(false))?.1;
    let mut prerequisites = BTreeMap::new();
    for (eid, topic) in &loaded.topic_eid_to_id {
        let mut parents = vec![];
        for p in snapshot.owners(*eid, "topic/next")? {
            parents.push(
                loaded
                    .topic_eid_to_id
                    .get(&p)
                    .ok_or("unknown prerequisite topic")?
                    .clone(),
            );
        }
        prerequisites.insert(topic.clone(), parents);
    }
    let mut balance = DiagnosticBalance::new(prerequisites, &rules.diagnostic_skip_policy)?;
    for (index, observed) in items.iter().enumerate() {
        if superseded.contains(&index) {
            continue;
        }
        let eid = snapshot.topic_for_question(
            content_id(snapshot, observed)?.ok_or("diagnostic item requires content")?,
        )?;
        let t = loaded
            .topic_eid_to_id
            .get(&eid)
            .ok_or("unknown diagnostic topic")?;
        let correct = result(snapshot, observed)?;
        let weight = if correct == Some(true) {
            observed
                .get("task-item/performance")
                .map(|v| number(v, "performance"))
                .transpose()?
                .unwrap_or(1.0)
        } else {
            1.0
        };
        balance.apply(t, correct, weight)?;
    }
    let states = engine.states.entry(loaded.learner.clone()).or_default();
    for (target, repetitions) in balance.positive_repetitions() {
        if states.get(&target).is_some_and(|s| s.learned) {
            continue;
        }
        let state = states
            .entry(target)
            .or_insert_with(|| TopicState::new(engine.policy.prior_accuracy, false));
        state.learned = true;
        state.repetitions = repetitions;
        state.memory = engine.policy.restored_memory;
        state.memory_at = at;
        state.interval_days = engine.policy.interval(repetitions)?;
    }
    Ok(())
}

pub fn transition_item(
    loaded: &LoadedRuntime,
    item: u64,
    status: &str,
    at: DateTime<Utc>,
) -> Result<TransactionPlan> {
    let snapshot = &loaded.snapshot;
    let task = snapshot.item_task(item, loaded.learner_eid)?;
    let items = task_items(snapshot, task)?;
    let position = items
        .iter()
        .position(|i| *i == item)
        .ok_or("item absent from task chain")?;
    for prior in &items[..position] {
        if !timing::terminal(&timing::status(snapshot, *prior, "task-item/status")?) {
            return Err("previous presentation has not completed".into());
        }
    }
    for later in &items[position + 1..] {
        if timing::terminal(&timing::status(snapshot, *later, "task-item/status")?) {
            return Err("cannot change timing before completed presentations".into());
        }
    }
    crate::schema::transition_transaction(loaded, item, status, at)
}

pub fn complete_item(
    loaded: &LoadedRuntime,
    item_eid: u64,
    options: CompletionOptions,
) -> Result<Completion> {
    let CompletionOptions {
        completed_at,
        result: submitted_result,
        performance,
        response_refs,
        response_entities,
        take_retry,
        xp_award,
        rules,
    } = options;
    rules.validate()?;
    let completed_at = completed_at
        .with_nanosecond(completed_at.nanosecond() / 1_000_000 * 1_000_000)
        .ok_or("invalid completion instant")?;
    let snapshot = &loaded.snapshot;
    let at = days(completed_at);
    if at
        < *loaded
            .engine
            .latest
            .get(&loaded.learner)
            .unwrap_or(&f64::NEG_INFINITY)
    {
        return Err("completion predates accepted learner evidence".into());
    }
    positive(performance, "performance")?;
    let mut item = snapshot.entity(item_eid)?.clone();
    if timing::status(snapshot, item_eid, "task-item/status")? != "task-item.status/started" {
        return Err("only a started item can complete".into());
    }
    timing::active_item(snapshot, loaded.learner_eid)?;
    timing::elapsed(snapshot, item_eid, completed_at)?;
    let task_owners = owners(snapshot, "learner-task/items", item_eid)?;
    if task_owners.len() != 1 {
        return Err("item must have one learner-task owner".into());
    }
    let task_eid = task_owners[0];
    let task = snapshot.entity(task_eid)?;
    if owners(snapshot, "learner/activity", task_eid)? != [loaded.learner_eid] {
        return Err("task must belong to the loaded learner".into());
    }
    let status = snapshot.ident(&json!(snapshot.reference(task_eid, "learner-task/status")?))?;
    if status != "learner-task.status/started" {
        return Err("only a started task can accept completion".into());
    }
    let started = timing::task_started(snapshot, task_eid)?;
    if completed_at < started {
        return Err("completion predates task start".into());
    }
    let activity = snapshot.reference(task_eid, "learner-task/activity")?;
    let kind = kind(
        snapshot,
        activity,
        &["lesson", "review", "assessment", "multistep", "diagnostic"],
    )?;
    if kind == "diagnostic" && performance > 1.0 {
        return Err("diagnostic positive evidence weight must be at most one".into());
    }
    if kind == "lesson" {
        let target = snapshot.reference(activity, "lesson/topic")?;
        for prerequisite in snapshot.owners(target, "topic/next")? {
            let t = loaded
                .topic_eid_to_id
                .get(&prerequisite)
                .ok_or("unknown prerequisite topic")?;
            let state = loaded
                .engine
                .states
                .get(&loaded.learner)
                .and_then(|s| s.get(t));
            if state.is_none()
                || !state.unwrap().learned
                || state.unwrap().memory_now(at)? <= loaded.engine.policy.due_threshold
            {
                return Err("lesson prerequisite is not currently ready".into());
            }
        }
    }
    if take_retry == Some(true) && kind != "diagnostic" {
        return Err("retry branching applies only to diagnostics".into());
    }
    let item_ids = task_items(snapshot, task_eid)?;
    let position = item_ids
        .iter()
        .position(|e| *e == item_eid)
        .ok_or("item is not owned by task")?;
    let mut prefix = vec![];
    for eid in &item_ids[..position] {
        let previous = snapshot.entity(*eid)?;
        if !timing::terminal(&timing::status(snapshot, *eid, "task-item/status")?) {
            return Err("previous presentation has not completed".into());
        }
        let previous_at = timing::status_at(snapshot, *eid, "task-item/status")?;
        if previous_at > completed_at {
            return Err("item completion order must be chronological".into());
        }
        if question(snapshot, previous)? {
            result(snapshot, previous)?;
        }
        prefix.push(previous.clone());
    }
    for eid in &item_ids[position + 1..] {
        if timing::terminal(&timing::status(snapshot, *eid, "task-item/status")?) {
            return Err("cannot insert evidence before completed presentations".into());
        }
    }
    let is_question = question(snapshot, &item)?;
    if !is_question
        && (submitted_result.is_some()
            || !response_refs.is_empty()
            || !response_entities.is_empty())
    {
        return Err("instruction completion cannot have an answer result".into());
    }
    let content = content_id(snapshot, &item)?.ok_or("new presentation needs known content")?;
    let mut item_change = Map::from_iter([("db/id".into(), json!(item_eid))]);
    if !is_question {
        item.insert(
            "task-item/status".into(),
            keyword("task-item.status/completed"),
        );
        item_change.insert(
            "task-item/status".into(),
            keyword("task-item.status/completed"),
        );
    }
    if is_question {
        let name = match submitted_result {
            Some(true) => "correct",
            Some(false) => "incorrect",
            None => "skipped",
        };
        let ident = format!("task-item.status/{name}");
        let mut matches = vec![];
        for (eid, entity) in &snapshot.entities {
            if let Some(value) = entity.get("db/ident")
                && snapshot.ident(value)? == ident
            {
                matches.push(*eid);
            }
        }
        if matches.len() != 1 {
            return Err("result enum must be installed exactly once".into());
        }
        item.insert("task-item/status".into(), json!(matches[0]));
        item_change.insert("task-item/status".into(), keyword(&ident));
        if submitted_result.is_some() {
            item_change.insert("task-item/performance".into(), json!(performance));
            item.insert("task-item/performance".into(), json!(performance));
        } else if !response_refs.is_empty()
            || !response_entities.is_empty()
            || !snapshot.refs(item_eid, "task-item/responses")?.is_empty()
        {
            return Err("a skipped question cannot contain submitted responses".into());
        }
        if !response_refs.is_empty() {
            item_change.insert("task-item/responses".into(), json!(response_refs));
        }
    }
    let selection = SelectionContext {
        policy: loaded.policy_eid,
        learner: loaded.learner_eid,
        task: task_eid,
    };
    let before = delivery(snapshot, activity, &kind, &prefix, Some(false), &selection)?;
    if (before.complete || !before.next_content.contains(&content))
        && Some(content) != before.retry_question
    {
        return Err("presentation is not a permitted continuation".into());
    }
    let mut items = prefix;
    items.push(item.clone());
    let mut delivered = delivery(snapshot, activity, &kind, &items, take_retry, &selection)?;
    if let Some(limit) = snapshot
        .entity(activity)?
        .get(&format!("{kind}/time-limit-seconds"))
    {
        let limit = number(limit, "time limit")?;
        if limit <= 0.0 {
            return Err("timed task requires a positive limit and actual start time".into());
        }
        let elapsed = seconds_between(completed_at, started);
        if elapsed > limit {
            return Err("answer arrived after the task time limit".into());
        }
        if elapsed == limit {
            delivered = Delivery {
                complete: true,
                passed: delivered.passed,
                ..Default::default()
            };
        }
    }
    let mut engine = loaded.engine.clone();
    let topic_eid = if is_question {
        Some(snapshot.topic_for_question(content)?)
    } else {
        None
    };
    let topic = topic_eid
        .map(|e| {
            loaded
                .topic_eid_to_id
                .get(&e)
                .cloned()
                .ok_or_else(|| "unknown question topic".to_string())
        })
        .transpose()?;
    let event_id = value_id_string(item.get("task-item/id").ok_or("task item requires id")?)?;
    let assessment =
        kind == "assessment" || kind == "diagnostic" && rules.diagnostic_uses_assessment_accuracy;
    let event = |suffix: &str, topic: &str, passed: bool, quality: f64, learned: bool| Event {
        id: format!("{event_id}:{suffix}"),
        learner: loaded.learner.clone(),
        topic: topic.into(),
        at,
        passed,
        quality,
        assessment,
        learned,
        kind: kind.clone(),
        ..Default::default()
    };
    if is_question && let Some(passed) = submitted_result {
        engine.apply_accuracy(event("answer", topic.as_ref().unwrap(), passed, 1.0, false))?;
    }
    if matches!(kind.as_str(), "assessment" | "multistep")
        && is_question
        && let Some(passed) = submitted_result
    {
        let questions = if kind == "assessment" {
            snapshot.refs(activity, "assessment/questions")?
        } else {
            snapshot
                .refs(activity, "multistep/steps")?
                .iter()
                .map(|s| snapshot.reference(*s, "multistep-step/question"))
                .collect::<Result<Vec<_>>>()?
        };
        let mut count = 0;
        for q in questions {
            if Some(snapshot.topic_for_question(q)?) == topic_eid {
                count += 1;
            }
        }
        if count == 0 {
            return Err("question topic absent from activity".into());
        }
        engine.apply_retention(event(
            "retention",
            topic.as_ref().unwrap(),
            passed,
            performance / count as f64,
            false,
        ))?;
    }
    if matches!(kind.as_str(), "lesson" | "review") && delivered.complete {
        let target = snapshot.reference(activity, &format!("{kind}/topic"))?;
        let mut performances = vec![];
        for i in &items {
            if question(snapshot, i)? && result(snapshot, i)?.is_some() {
                performances.push(
                    i.get("task-item/performance")
                        .map(|v| number(v, "performance"))
                        .transpose()?
                        .unwrap_or(1.0),
                );
            }
        }
        let quality = if performances.is_empty() {
            1.0
        } else {
            performances.iter().sum::<f64>() / performances.len() as f64
        };
        let passed = delivered.passed.unwrap_or(false);
        engine.apply_retention(event(
            "retention",
            loaded
                .topic_eid_to_id
                .get(&target)
                .ok_or("unknown activity topic")?,
            passed,
            quality,
            kind == "lesson" && passed,
        ))?;
    }
    if kind == "diagnostic" && delivered.complete {
        place_diagnostic(loaded, &mut engine, activity, &items, at, &rules)?;
    }
    let mut changes = response_entities;
    changes.push(Value::Object(item_change));
    if delivered.complete {
        let mut change = Map::from_iter([
            ("db/id".into(), json!(task_eid)),
            (
                "learner-task/status".into(),
                keyword(if delivered.passed == Some(false) {
                    "learner-task.status/failed"
                } else {
                    "learner-task.status/completed"
                }),
            ),
        ]);
        let mut outcomes = vec![];
        for i in &items {
            if question(snapshot, i)? {
                outcomes.push(result(snapshot, i)?);
            }
        }
        let mut award = xp_award;
        if award.is_none()
            && let Some(base) = task.get("learner-task/xp-base")
            && (matches!(kind.as_str(), "lesson" | "review")
                && outcomes.iter().all(|o| *o == Some(true))
                || rules.use_fitted_xp && matches!(kind.as_str(), "assessment" | "multistep"))
        {
            // Preserve integer bases exactly before evaluating rational formulas.
            let base = if let Some(i) = base.as_i64() {
                BigRational::from_integer(i.into())
            } else {
                number(base, "base XP")?.exact()?
            };
            let computed = match kind.as_str() {
                "lesson" => lesson_xp_candidate(base, &outcomes, None)?,
                "review" => review_xp_candidate(base, &outcomes, None)?,
                "assessment" => assessment_xp_candidate(base, &outcomes)?,
                _ => multistep_xp_candidate(base, &outcomes)?,
            };
            award = Some(computed.to_i64().ok_or("XP award exceeds EDB long range")?);
        }
        if let Some(award) = award {
            change.insert("learner-task/xp-earned".into(), json!(award));
        }
        changes.push(Value::Object(change));
    } else if xp_award.is_some() {
        return Err("task XP can be awarded only at completion".into());
    }
    engine.latest.insert(loaded.learner.clone(), at);
    let transaction = completion_transaction(loaded, item_eid, completed_at, changes, &engine)?;
    Ok(Completion {
        transaction,
        engine,
        delivery: delivered,
    })
}

pub fn expire_task(
    loaded: &LoadedRuntime,
    task_eid: u64,
    completed_at: DateTime<Utc>,
    xp_award: Option<i64>,
    rules: ActivityRules,
) -> Result<Completion> {
    rules.validate()?;
    let completed_at = completed_at
        .with_nanosecond(completed_at.nanosecond() / 1_000_000 * 1_000_000)
        .ok_or("invalid completion instant")?;
    let at = days(completed_at);
    let snapshot = &loaded.snapshot;
    if owners(snapshot, "learner/activity", task_eid)? != [loaded.learner_eid] {
        return Err("task must belong to the loaded learner".into());
    }
    if !["learner-task.status/started", "learner-task.status/paused"].contains(
        &snapshot
            .ident(&json!(snapshot.reference(task_eid, "learner-task/status")?))?
            .as_str(),
    ) {
        return Err("only a started task can expire".into());
    }
    let activity = snapshot.reference(task_eid, "learner-task/activity")?;
    let kind = kind(snapshot, activity, &["assessment", "diagnostic"])?;
    let limit = snapshot
        .entity(activity)?
        .get(&format!("{kind}/time-limit-seconds"))
        .ok_or("expiry requires a time limit")?;
    let limit = number(limit, "time limit")?;
    let started = timing::task_started(snapshot, task_eid)?;
    if limit <= 0.0 {
        return Err("expiry requires a positive limit and known start".into());
    }
    if seconds_between(completed_at, started) < limit {
        return Err("task time limit has not expired".into());
    }
    if at
        < *loaded
            .engine
            .latest
            .get(&loaded.learner)
            .unwrap_or(&f64::NEG_INFINITY)
    {
        return Err("expiry predates accepted learner evidence".into());
    }
    let mut items = vec![];
    let mut pending = false;
    for eid in task_items(snapshot, task_eid)? {
        let item = snapshot.entity(eid)?;
        if !timing::terminal(&timing::status(snapshot, eid, "task-item/status")?) {
            pending = true;
            continue;
        }
        if pending || !question(snapshot, item)? {
            return Err("timed activity has an incomplete or invalid answer history".into());
        }
        items.push(item.clone());
    }
    let selection = SelectionContext {
        policy: loaded.policy_eid,
        learner: loaded.learner_eid,
        task: task_eid,
    };
    delivery(snapshot, activity, &kind, &items, Some(false), &selection)?;
    let mut engine = loaded.engine.clone();
    if kind == "diagnostic" {
        place_diagnostic(loaded, &mut engine, activity, &items, at, &rules)?;
    }
    engine.latest.insert(loaded.learner.clone(), at);
    let mut change = Map::from_iter([("db/id".into(), json!(task_eid))]);
    if let Some(award) = xp_award {
        change.insert("learner-task/xp-earned".into(), json!(award));
    }
    let transaction = task_transaction(
        loaded,
        task_eid,
        completed_at,
        vec![Value::Object(change)],
        &engine,
    )?;
    Ok(Completion {
        transaction,
        engine,
        delivery: Delivery {
            complete: true,
            ..Default::default()
        },
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::schema::{StatusAssertion, instant_value, load_runtime};
    use chrono::Duration;

    fn start() -> DateTime<Utc> {
        DateTime::parse_from_rfc3339("2026-09-28T00:00:00Z")
            .unwrap()
            .with_timezone(&Utc)
    }
    fn uuid(id: u64) -> Value {
        json!({"$uuid":format!("00000000-0000-0000-0000-{id:012x}")})
    }
    struct Fixture {
        entities: BTreeMap<u64, Entity>,
        basis: u64,
        enums: BTreeMap<String, u64>,
        history: Vec<StatusAssertion>,
    }
    impl Fixture {
        fn new(kind: &str) -> Self {
            // The source fixture is an entity capture, not an engine-state dump.
            let snapshot = EntitySnapshot::from_json(
                &serde_json::from_str(include_str!("fixtures/review.json")).unwrap(),
            )
            .unwrap();
            let enums = snapshot
                .entities
                .iter()
                .filter_map(|(e, r)| r.get("db/ident").map(|i| (snapshot.ident(i).unwrap(), *e)))
                .collect();
            let mut f = Self {
                entities: snapshot.entities,
                basis: snapshot.basis_t,
                enums,
                history: snapshot.status_history,
            };
            match kind {
                "review" => {},
                "lesson" => {
                    f.put(210,json!({"tutorial/id":uuid(210),"tutorial/title":"Introduction","tutorial/content":"Subtract the constant."}));
                    f.put(220,json!({"lesson-step/id":uuid(220),"lesson-step/index":1,"lesson-step/content":210}));
                    f.put(221,json!({"lesson-step/id":uuid(221),"lesson-step/index":2,"lesson-step/content":40}));
                    f.put(4,json!({"lesson/id":uuid(4),"lesson/topic":20,"lesson/steps":[221,220]}));
                },
                "assessment" => f.put(4,json!({"assessment/id":uuid(4),"assessment/title":"Mixed topics","assessment/questions":[100,101,110]})),
                "multistep" => {
                    for (step,q) in [(220,100),(221,110),(222,101)] { f.put(step,json!({"multistep-step/id":uuid(step),"multistep-step/index":step-219,"multistep-step/question":q})); }
                    f.put(4,json!({"multistep/id":uuid(4),"multistep/steps":[222,220,221]}));
                },
                "diagnostic" => {
                    f.set(21,"topic/next",json!([20]));
                    for (probe,q) in [(300,100),(301,120),(302,130),(303,101)] { f.put(probe,json!({"diagnostic-probe/id":uuid(probe),"diagnostic-probe/question":q})); }
                    for (attr,target) in [("on-correct",301),("on-incorrect",302),("on-skipped",302),("on-silly-mistake",303)] { f.set(300,&format!("diagnostic-probe/{attr}"),json!(target)); }
                    for (attr,target) in [("on-correct",301),("on-incorrect",302),("on-skipped",302)] { f.set(303,&format!("diagnostic-probe/{attr}"),json!(target)); }
                    f.put(4,json!({"diagnostic/id":uuid(4),"diagnostic/title":"Placement","diagnostic/scope":10,"diagnostic/probes":[300,301,302,303],"diagnostic/start":300}));
                },
                _ => panic!("unknown fixture kind"),
            }
            f
        }
        fn put(&mut self, eid: u64, value: Value) {
            self.entities
                .insert(eid, value.as_object().unwrap().clone());
        }
        fn set(&mut self, eid: u64, attr: &str, value: Value) {
            if matches!(attr, "learner-task/status" | "task-item/status")
                && self.entities[&eid].get(attr) != Some(&value)
            {
                self.basis += 1;
                self.history.push(StatusAssertion {
                    entity: eid,
                    attribute: attr.into(),
                    value: value.clone(),
                    t: self.basis,
                    at: self
                        .history
                        .last()
                        .map(|h| h.at.clone())
                        .unwrap_or(instant_value(start())),
                });
            }
            self.entities
                .get_mut(&eid)
                .unwrap()
                .insert(attr.into(), value);
        }
        fn load(&self) -> LoadedRuntime {
            load_runtime(
                EntitySnapshot::from_json(&json!({"entities":self.entities,"basis_t":self.basis,"status_history":self.history})).unwrap(),
                1,
                2,
            )
            .unwrap()
        }
        fn present(&mut self, content: u64) -> u64 {
            let eid = 1001
                + self.entities[&3]["learner-task/items"]
                    .as_array()
                    .unwrap()
                    .len() as u64;
            self.present_as(content, eid)
        }
        fn present_as(&mut self, content: u64, eid: u64) -> u64 {
            let snapshot = EntitySnapshot::new(self.entities.clone(), self.basis).unwrap();
            if let Some(tail) = task_items(&snapshot, 3).unwrap().last() {
                self.set(*tail, "task-item/next", json!(eid));
            }
            let items = self
                .entities
                .get_mut(&3)
                .unwrap()
                .get_mut("learner-task/items")
                .unwrap()
                .as_array_mut()
                .unwrap();
            items.push(json!(eid));
            self.put(
                eid,
                json!({"task-item/id":uuid(eid),"task-item/content":content}),
            );
            self.set(
                eid,
                "task-item/status",
                json!(self.enums["task-item.status/started"]),
            );
            eid
        }
        fn seed(&mut self, topic: u64, repetitions: f64) {
            let eid = 500 + topic;
            self.put(eid,json!({"progress/id":format!("learner-topic-{topic}"),"progress/topic":topic,"progress/policy":2,
                "progress/repetitions":repetitions,"progress/memory":1.0,"progress/memory-at":instant_value(start()-Duration::days(2)),
                "progress/interval-days":1.0,"progress/learned":true,"progress/assessment-accuracy":0.8,"progress/practice-accuracy":0.8,
                "progress/assessment-mass":0.0,"progress/practice-mass":0.0}));
            self.entities
                .get_mut(&1)
                .unwrap()
                .entry("learner/knowledge-profile")
                .or_insert(json!([]))
                .as_array_mut()
                .unwrap()
                .push(json!(eid));
        }
        fn state(&self, topic: u64) -> TopicState {
            let l = self.load();
            l.engine.states[&l.learner][&l.topic_eid_to_id[&topic]].clone()
        }
        fn apply(&mut self, plan: &TransactionPlan) {
            assert_eq!(plan.compare_basis_t, self.basis);
            let mut tempids = BTreeMap::new();
            for form in &plan.forms {
                if let Some(temp) = form.get("db/id").and_then(Value::as_str)
                    && temp != "edb.tx"
                    && !tempids.contains_key(temp)
                {
                    let id = self.entities.keys().max().unwrap() + 1;
                    tempids.insert(temp.to_string(), id);
                    self.entities.insert(id, Map::new());
                }
            }
            let resolve = |v: &Value| -> Value {
                if let Some(ident) = v.get("$keyword").and_then(Value::as_str) {
                    return json!(self.enums[ident]);
                }
                if let Some(id) = v.as_str().and_then(|s| tempids.get(s)) {
                    return json!(id);
                }
                v.clone()
            };
            let mut records = self.entities.clone();
            for form in &plan.forms {
                if let Some(map) = form.as_object() {
                    if map.get("db/id") == Some(&json!("edb.tx")) {
                        continue;
                    }
                    let id = resolve(&map["db/id"]).as_u64().unwrap();
                    for (attr, value) in map {
                        if matches!(attr.as_str(), "db/id" | "db/ensure") {
                            continue;
                        }
                        if let Some(values) = value.as_array() {
                            let old = records
                                .get_mut(&id)
                                .unwrap()
                                .entry(attr)
                                .or_insert(json!([]))
                                .as_array_mut()
                                .unwrap();
                            for value in values {
                                let value = resolve(value);
                                if !old.contains(&value) {
                                    old.push(value);
                                }
                            }
                        } else {
                            records
                                .get_mut(&id)
                                .unwrap()
                                .insert(attr.clone(), resolve(value));
                        }
                    }
                } else {
                    let values = form.as_array().unwrap();
                    let op = values[0]["$keyword"].as_str().unwrap();
                    let id = values[1].as_u64().unwrap();
                    let attr = values[2]["$keyword"].as_str().unwrap();
                    match op {
                        "db/cas" => {
                            assert_eq!(
                                records[&id].get(attr).unwrap_or(&Value::Null),
                                &resolve(&values[3])
                            );
                            records
                                .get_mut(&id)
                                .unwrap()
                                .insert(attr.into(), resolve(&values[4]));
                        }
                        "db/retract" => {
                            if records[&id].get(attr) == Some(&values[3]) {
                                records.get_mut(&id).unwrap().remove(attr);
                            }
                        }
                        _ => panic!("unsupported fixture operation {op}"),
                    }
                }
            }
            self.basis += 1;
            let at = plan
                .forms
                .iter()
                .find(|f| f.get("db/id") == Some(&json!("edb.tx")))
                .unwrap()["db/txInstant"]
                .clone();
            for (eid, record) in &records {
                for attribute in ["learner-task/status", "task-item/status"] {
                    if let Some(value) = record.get(attribute) {
                        if self.entities.get(eid).and_then(|r| r.get(attribute)) != Some(value) {
                            self.history.push(StatusAssertion {
                                entity: *eid,
                                attribute: attribute.into(),
                                value: value.clone(),
                                t: self.basis,
                                at: at.clone(),
                            });
                        }
                    }
                }
            }
            self.entities = records;
        }
        fn answer_with(
            &mut self,
            content: u64,
            result: Outcome,
            mut options: CompletionOptions,
        ) -> Completion {
            let eid = self.present(content);
            options.result = result;
            let loaded = self.load();
            let before = loaded.engine.snapshot();
            let done = complete_item(&loaded, eid, options).unwrap();
            assert_eq!(loaded.engine.snapshot(), before);
            self.apply(&done.transaction);
            done
        }
        fn answer(&mut self, content: u64, result: Outcome) -> Completion {
            let n = self.entities[&3]["learner-task/items"]
                .as_array()
                .unwrap()
                .len()
                + 1;
            self.answer_with(
                content,
                result,
                CompletionOptions::new(start() + Duration::seconds(n as i64)),
            )
        }
    }

    #[test]
    fn review_delivery_uses_its_own_initial_and_remedial_weights() {
        let mut f = Fixture::new("review");
        f.put(
            9502,
            json!({"db/ident":{"$keyword":"question.difficulty/easy"}}),
        );
        f.put(
            9500,
            json!({"db/ident":{"$keyword":"activity.type/review"}}),
        );
        f.put(9501,json!({"question-weights/activity-type":9500,
            "question-weights/initial-easy":1.0,"question-weights/initial-moderate":0.0,"question-weights/initial-hard":0.0,
            "question-weights/remedial-easy":0.0,"question-weights/remedial-moderate":1.0,"question-weights/remedial-hard":0.0}));
        f.set(2, "policy/question-selection-weights", json!([9501]));
        let pool = f.entities[&4]["review/questions"]
            .as_array()
            .unwrap()
            .clone();
        let mut easy = vec![];
        let mut moderate = vec![];
        for (i, q) in pool.iter().enumerate() {
            let q = q.as_u64().unwrap();
            if i < 3 {
                easy.push(q);
            } else {
                moderate.push(q);
            }
            f.set(q,"question/difficulty",json!({"$keyword":if i < 3 {"question.difficulty/easy"} else {"question.difficulty/moderate"}}));
        }
        let s = f.load().snapshot;
        let context = SelectionContext {
            policy: 2,
            learner: 1,
            task: 3,
        };
        let mut prefix = vec![];
        for slot in 0..4 {
            let d = delivery(&s, 4, "review", &prefix, None, &context).unwrap();
            assert_eq!(d.next_content.len(), 1);
            let q = d.next_content[0];
            assert!(if slot < 3 {
                easy.contains(&q)
            } else {
                moderate.contains(&q)
            });
            assert_eq!(
                delivery(&s, 4, "review", &prefix, None, &context).unwrap(),
                d
            );
            prefix.push(json!({"task-item/content":q,"task-item/status":{"$keyword":"task-item.status/incorrect"}}).as_object().unwrap().clone());
        }
    }

    #[test]
    fn review_accuracy_updates_once_and_retention_only_on_terminal_streak() {
        let mut f = Fixture::new("review");
        f.seed(20, 0.0);
        f.set(3, "learner-task/xp-base", json!(6));
        for (i, q) in [100, 101, 102].iter().enumerate() {
            let done = f.answer(*q, Some(true));
            let state = f.state(20);
            assert_eq!(state.ability.practice_mass, (i + 1) as f64);
            assert_eq!(
                f.load().engine.global_ability["learner"].practice_mass,
                (i + 1) as f64
            );
            if i < 2 {
                assert!(!done.delivery.complete);
                assert_eq!(state.repetitions, 0.0);
            } else {
                assert_eq!(done.delivery.passed, Some(true));
                assert!(state.repetitions > 1.0);
            }
        }
        assert_eq!(f.entities[&3]["learner-task/xp-earned"], 8);
        assert_eq!(
            f.entities[&3]["learner-task/status"],
            f.enums["learner-task.status/completed"]
        );
    }
    #[test]
    fn lesson_authored_sequence_mastery_failure_and_exhaustion() {
        let mut f = Fixture::new("lesson");
        assert_eq!(f.answer(210, None).delivery.next_content, vec![200]);
        assert!(!f.load().engine.global_ability.contains_key("learner"));
        assert_eq!(
            f.answer(200, None).delivery.next_content,
            vec![100, 101, 102, 103, 104]
        );
        assert!(!f.answer(100, Some(true)).delivery.complete);
        assert!(!f.state(20).learned);
        assert_eq!(f.answer(101, Some(true)).delivery.passed, Some(true));
        assert!(f.state(20).learned);
        assert_eq!(f.state(20).evidence_mass(), 2.0);
        assert_eq!(
            f.entities[&3]["learner-task/status"],
            f.enums["learner-task.status/completed"]
        );
        let mut f = Fixture::new("lesson");
        f.answer(210, None);
        f.answer(200, None);
        for (q, r) in (100..105).zip([true, false, true, false, true]) {
            f.answer(q, Some(r));
        }
        let s = f.state(20);
        assert!(!s.learned);
        assert_eq!(
            (s.repetitions, s.memory, s.evidence_mass()),
            (0.0, 0.0, 5.0)
        );
        assert_eq!(
            f.entities[&3]["learner-task/status"],
            f.enums["learner-task.status/failed"]
        );
        let mut f = Fixture::new("lesson");
        f.set(40, "knowledge-point/questions", json!([100]));
        f.answer(210, None);
        f.answer(200, None);
        let done = f.answer(100, Some(true));
        assert!(!done.delivery.complete);
        assert_eq!(done.delivery.needs_questions_for, Some(40));
        assert_eq!(f.state(20).evidence_mass(), 1.0);
    }
    #[test]
    fn assessment_and_multistep_distribute_topic_retention_and_channels() {
        for kind in ["assessment", "multistep"] {
            let mut f = Fixture::new(kind);
            f.seed(20, 3.0);
            f.seed(21, 3.0);
            f.answer(100, Some(true));
            assert_eq!(f.state(21).evidence_mass(), 0.0);
            f.answer(110, Some(false));
            let done = f.answer(101, Some(true));
            assert!(done.delivery.complete);
            assert_eq!(done.delivery.passed, None);
            assert_eq!(
                f.entities[&3]["learner-task/status"],
                f.enums["learner-task.status/completed"]
            );
            assert!(f.state(20).repetitions > 3.0);
            assert!(f.state(21).repetitions < 3.0);
            let a = f.load().engine.global_ability["learner"].clone();
            assert_eq!(
                (a.assessment_mass, a.practice_mass),
                if kind == "assessment" {
                    (3.0, 0.0)
                } else {
                    (0.0, 3.0)
                }
            );
        }
    }
    #[test]
    fn skipped_questions_are_recorded_without_accuracy_or_submitted_responses() {
        let mut f = Fixture::new("review");
        f.seed(20, 0.0);
        f.answer(100, None);
        assert_eq!(f.state(20).evidence_mass(), 0.0);
        assert!(!f.entities[&1001].contains_key("task-item/performance"));
        let eid = f.present(101);
        f.set(eid, "task-item/responses", json!([3101]));
        let l = f.load();
        assert!(
            complete_item(
                &l,
                eid,
                CompletionOptions::new(start() + Duration::seconds(2))
            )
            .err()
            .unwrap()
            .contains("skipped question cannot")
        );
    }
    fn retry(f: &mut Fixture, performance: f64, outcome: Outcome) {
        let mut o = CompletionOptions::new(start() + Duration::seconds(1));
        o.take_retry = Some(true);
        assert_eq!(
            f.answer_with(100, Some(false), o).delivery.next_content,
            vec![101]
        );
        let mut o = CompletionOptions::new(start() + Duration::seconds(2));
        o.performance = performance;
        f.answer_with(101, outcome, o);
    }
    #[test]
    fn diagnostic_retry_replaces_frontier_but_keeps_both_accuracy_observations() {
        let mut f = Fixture::new("diagnostic");
        retry(&mut f, 1.0, Some(true));
        f.answer(120, Some(true));
        assert_eq!(f.state(20).repetitions, 1.0);
        assert_eq!(f.state(20).evidence_mass(), 2.0);
        assert_eq!(f.state(21).repetitions, 1.0);
        assert_eq!(f.load().engine.global_ability["learner"].practice_mass, 3.0);
        assert_eq!(
            f.entities[&3]["learner-task/status"],
            f.enums["learner-task.status/completed"]
        );
        let mut f = Fixture::new("diagnostic");
        f.set(20, "topic/next", json!([22]));
        retry(&mut f, 0.25, Some(true));
        let mut o = CompletionOptions::new(start() + Duration::seconds(3));
        o.performance = 0.5;
        f.answer_with(120, Some(true), o);
        assert_eq!(f.state(20).repetitions, 0.75);
        assert_eq!(f.state(21).repetitions, 0.75);
        assert_eq!(f.state(22).repetitions, 0.5);
        // An ordinary same-topic continuation must retain the first failure.
        let mut f = Fixture::new("diagnostic");
        f.set(302, "diagnostic-probe/question", json!(102));
        let mut o = CompletionOptions::new(start() + Duration::seconds(1));
        o.take_retry = Some(false);
        f.answer_with(100, Some(false), o);
        f.answer(102, Some(true));
        assert!(!f.state(20).learned);
        assert_eq!(f.state(20).evidence_mass(), 2.0);
    }
    #[test]
    fn incorrect_or_skipped_retry_contributes_only_one_negative() {
        for outcome in [Some(false), None] {
            let mut f = Fixture::new("diagnostic");
            f.set(20, "topic/next", json!([23]));
            f.put(
                304,
                json!({"diagnostic-probe/id":uuid(304),"diagnostic-probe/question":131}),
            );
            f.set(4, "diagnostic/probes", json!([300, 301, 302, 303, 304]));
            f.set(302, "diagnostic-probe/on-correct", json!(304));
            retry(&mut f, 1.0, outcome);
            f.answer(130, Some(true));
            f.answer(131, Some(true));
            assert_eq!(f.state(20).repetitions, 1.0);
            assert_eq!(f.state(23).repetitions, 1.0);
        }
    }
    #[test]
    fn diagnostic_retries_require_explicit_choice_and_unambiguous_valid_graph() {
        let mut f = Fixture::new("diagnostic");
        let eid = f.present(100);
        let l = f.load();
        let mut o = CompletionOptions::new(start() + Duration::seconds(1));
        o.result = Some(false);
        assert!(
            complete_item(&l, eid, o.clone())
                .err()
                .unwrap()
                .contains("choose whether")
        );
        o.take_retry = Some(true);
        for target in [302, 303] {
            let mut g = Fixture::new("diagnostic");
            g.set(300, "diagnostic-probe/on-incorrect", json!(target));
            g.set(target, "diagnostic-probe/question", json!(101));
            let eid = g.present(100);
            let l = g.load();
            assert!(
                complete_item(&l, eid, o.clone())
                    .err()
                    .unwrap()
                    .contains("distinguishable")
            );
        }
        let mut g = Fixture::new("diagnostic");
        g.set(100, "question/difficulty", json!(0.5));
        g.set(101, "question/difficulty", json!(0.5));
        let eid = g.present(100);
        assert!(complete_item(&g.load(), eid, o).is_err());
    }
    #[test]
    fn timer_closes_only_observed_work_and_unanswered_retry_keeps_original() {
        let mut f = Fixture::new("assessment");
        f.seed(20, 0.0);
        f.seed(21, 0.0);
        f.set(4, "assessment/time-limit-seconds", json!(60.0));
        f.set(3, "learner-task/xp-base", json!(15));
        f.answer(100, Some(true));
        let pending = f.present(110);
        let l = f.load();
        let before = l.engine.snapshot();
        assert!(
            expire_task(
                &l,
                3,
                start() + Duration::seconds(59),
                None,
                ActivityRules::default()
            )
            .is_err()
        );
        let done = expire_task(
            &l,
            3,
            start() + Duration::seconds(60),
            None,
            ActivityRules::default(),
        )
        .unwrap();
        assert_eq!(l.engine.snapshot(), before);
        f.apply(&done.transaction);
        assert_eq!(done.delivery.passed, None);
        assert_eq!(
            f.entities[&3]["learner-task/status"],
            f.enums["learner-task.status/completed"]
        );
        assert_eq!(
            f.entities[&pending]["task-item/status"],
            f.enums["task-item.status/paused"]
        );
        assert!(!f.entities[&3].contains_key("learner-task/xp-earned"));
        assert_eq!(f.state(21).evidence_mass(), 0.0);
        for outcome in [Some(true), Some(false)] {
            let mut f = Fixture::new("diagnostic");
            f.set(4, "diagnostic/time-limit-seconds", json!(60.0));
            let mut o = CompletionOptions::new(start() + Duration::seconds(1));
            o.performance = 0.5;
            o.take_retry = Some(outcome == Some(false));
            f.answer_with(100, outcome, o);
            let pending = f.present(if outcome == Some(true) { 120 } else { 101 });
            let done = expire_task(
                &f.load(),
                3,
                start() + Duration::seconds(60),
                None,
                ActivityRules::default(),
            )
            .unwrap();
            f.apply(&done.transaction);
            assert_eq!(
                f.entities[&pending]["task-item/status"],
                f.enums["task-item.status/paused"]
            );
            assert_eq!(f.state(20).learned, outcome == Some(true));
            if outcome == Some(true) {
                assert_eq!(f.state(20).repetitions, 0.5);
                assert_eq!(f.state(21).repetitions, 0.5);
            }
        }
    }
    #[test]
    fn completion_rejections_are_atomic_and_repeated_plans_identical() {
        let mut f = Fixture::new("review");
        f.seed(20, 0.0);
        let eid = f.present(100);
        let l = f.load();
        let before = l.engine.snapshot();
        let mut o = CompletionOptions::new(start() + Duration::seconds(1));
        o.result = Some(true);
        o.xp_award = Some(7);
        assert!(
            complete_item(&l, eid, o.clone())
                .err()
                .unwrap()
                .contains("XP can be awarded only")
        );
        assert_eq!(l.engine.snapshot(), before);
        o.xp_award = None;
        let first = complete_item(&l, eid, o.clone()).unwrap();
        let second = complete_item(&l, eid, o.clone()).unwrap();
        assert_eq!(first.transaction.edn, second.transaction.edn);
        assert_eq!(
            first.transaction.request_key,
            second.transaction.request_key
        );
        assert_eq!(
            first.transaction.compare_basis_t,
            second.transaction.compare_basis_t
        );
        assert_eq!(l.engine.snapshot(), before);
        f.apply(&first.transaction);
        assert!(
            complete_item(&f.load(), eid, o)
                .err()
                .unwrap()
                .contains("started")
        );
        for prereq in [true, false] {
            let mut f = Fixture::new("lesson");
            if prereq {
                f.set(21, "topic/next", json!([20]));
            }
            let eid = f.present(if prereq { 210 } else { 100 });
            let mut o = CompletionOptions::new(start() + Duration::seconds(1));
            if !prereq {
                o.result = Some(true);
            }
            assert!(complete_item(&f.load(), eid, o).is_err());
        }
    }

    #[test]
    fn only_started_tasks_accept_observed_item_writes_or_expiry() {
        for status in ["locked", "unlocked", "completed", "failed"] {
            let mut f = Fixture::new("assessment");
            f.set(4, "assessment/time-limit-seconds", json!(60.0));
            f.set(
                3,
                "learner-task/status",
                json!(f.enums[&format!("learner-task.status/{status}")]),
            );
            let item = f.present(100);
            let loaded = f.load();
            let before = loaded.engine.snapshot();
            let at = start() + Duration::seconds(60);
            let mut options = CompletionOptions::new(at);
            options.result = Some(true);
            assert!(
                complete_item(&loaded, item, options)
                    .err()
                    .unwrap()
                    .contains("started")
            );
            assert!(
                expire_task(&loaded, 3, at, None, ActivityRules::default())
                    .err()
                    .unwrap()
                    .contains("started")
            );
            assert!(
                completion_transaction(&loaded, item, at, vec![], &loaded.engine)
                    .unwrap_err()
                    .contains("started")
            );
            assert!(
                task_transaction(&loaded, 3, at, vec![], &loaded.engine)
                    .unwrap_err()
                    .contains("started")
            );
            assert_eq!(loaded.engine.snapshot(), before);
        }
    }

    #[test]
    fn status_history_excludes_pauses_and_updates_item_and_task_totals() {
        let mut f = Fixture::new("assessment");
        f.seed(20, 0.0);
        f.seed(21, 0.0);
        let item = f.present(100);
        let states = f.load().engine.states.clone();
        let pause =
            transition_item(&f.load(), item, "paused", start() + Duration::seconds(5)).unwrap();
        assert!(
            pause
                .forms
                .iter()
                .any(|form| form.get("db/id") == Some(&json!("edb.tx"))
                    && form["db/txInstant"] == instant_value(start() + Duration::seconds(5)))
        );
        f.apply(&pause);
        assert_eq!(f.entities[&item]["task-item/elapsed-seconds"], 5.0);
        assert_eq!(f.entities[&3]["learner-task/elapsed-seconds"], 5.0);
        assert_eq!(f.load().engine.states, states);
        let mut options = CompletionOptions::new(start() + Duration::seconds(6));
        options.result = Some(true);
        assert!(complete_item(&f.load(), item, options).is_err());
        let resume =
            transition_item(&f.load(), item, "started", start() + Duration::seconds(12)).unwrap();
        f.apply(&resume);
        assert_eq!(f.entities[&item]["task-item/elapsed-seconds"], 5.0);
        let mut options = CompletionOptions::new(start() + Duration::seconds(15));
        options.result = Some(true);
        let done = complete_item(&f.load(), item, options).unwrap();
        f.apply(&done.transaction);
        assert_eq!(f.entities[&item]["task-item/elapsed-seconds"], 8.0);
        assert_eq!(f.entities[&3]["learner-task/elapsed-seconds"], 8.0);
        assert_eq!(
            timing::status_at(&f.load().snapshot, item, "task-item/status").unwrap(),
            start() + Duration::seconds(15)
        );
        let next = f.present(110);
        let mut options = CompletionOptions::new(start() + Duration::seconds(17));
        options.result = Some(false);
        let done = complete_item(&f.load(), next, options).unwrap();
        f.apply(&done.transaction);
        assert_eq!(f.entities[&next]["task-item/elapsed-seconds"], 2.0);
        assert_eq!(f.entities[&3]["learner-task/elapsed-seconds"], 10.0);
    }

    #[test]
    fn history_is_required_for_writes_and_deadlines_continue_while_paused() {
        let mut f = Fixture::new("assessment");
        f.set(4, "assessment/time-limit-seconds", json!(10.0));
        let item = f.present(100);
        let missing = load_runtime(
            EntitySnapshot::new(f.entities.clone(), f.basis).unwrap(),
            1,
            2,
        )
        .unwrap();
        assert!(transition_item(&missing, item, "paused", start() + Duration::seconds(1)).is_err());
        let pause =
            transition_item(&f.load(), item, "paused", start() + Duration::seconds(3)).unwrap();
        f.apply(&pause);
        assert!(
            transition_item(&f.load(), item, "started", start() + Duration::seconds(11)).is_err()
        );
        f.set(
            3,
            "learner-task/status",
            json!(f.enums["learner-task.status/paused"]),
        );
        assert!(
            expire_task(
                &f.load(),
                3,
                start() + Duration::seconds(9),
                None,
                ActivityRules::default()
            )
            .is_err()
        );
        let done = expire_task(
            &f.load(),
            3,
            start() + Duration::seconds(10),
            None,
            ActivityRules::default(),
        )
        .unwrap();
        f.apply(&done.transaction);
        assert_eq!(f.entities[&3]["learner-task/elapsed-seconds"], 3.0);
        assert_eq!(
            f.entities[&item]["task-item/status"],
            f.enums["task-item.status/paused"]
        );
        assert!(!f.load().engine.global_ability.contains_key("learner"));
        assert!(
            transition_item(&f.load(), item, "started", start() + Duration::seconds(11)).is_err()
        );

        let mut bad = json!({"entities":f.entities,"basis_t":f.basis,"status_history":f.history});
        bad["status_history"][0]["entity"] = json!(1);
        assert!(EntitySnapshot::from_json(&bad).is_err());
        let mut duplicate =
            json!({"entities":f.entities,"basis_t":f.basis,"status_history":f.history});
        let event = duplicate["status_history"][0].clone();
        duplicate["status_history"]
            .as_array_mut()
            .unwrap()
            .push(event);
        assert!(EntitySnapshot::from_json(&duplicate).is_err());

        let mut f = Fixture::new("assessment");
        let first = f.present(100);
        f.present(110);
        assert!(
            transition_item(&f.load(), first, "paused", start() + Duration::seconds(1)).is_err()
        );
    }

    #[test]
    fn presentation_chain_controls_completion_and_expiry_without_eid_order() {
        for expire in [false, true] {
            let mut f = Fixture::new("assessment");
            f.seed(20, 0.0);
            f.seed(21, 0.0);
            f.set(4, "assessment/time-limit-seconds", json!(60.0));
            for (position, (question, eid)) in [(100, 3002), (110, 3000), (101, 3001)]
                .into_iter()
                .enumerate()
            {
                f.present_as(question, eid);
                if expire && position == 1 {
                    break;
                }
                let mut options =
                    CompletionOptions::new(start() + Duration::seconds(position as i64 + 1));
                options.result = Some(true);
                let done = complete_item(&f.load(), eid, options).unwrap();
                assert_eq!(done.delivery.complete, position == 2);
                f.apply(&done.transaction);
            }
            if expire {
                f.set(3, "learner-task/items", json!([3000, 3002]));
                assert_eq!(task_items(&f.load().snapshot, 3).unwrap(), [3002, 3000]);
                let done = expire_task(
                    &f.load(),
                    3,
                    start() + Duration::seconds(60),
                    None,
                    ActivityRules::default(),
                )
                .unwrap();
                f.apply(&done.transaction);
                assert_eq!(
                    f.entities[&3000]["task-item/status"],
                    f.enums["task-item.status/paused"]
                );
                assert_eq!(f.state(20).evidence_mass(), 1.0);
                assert_eq!(f.state(21).evidence_mass(), 0.0);
            } else {
                f.set(3, "learner-task/items", json!([3001, 3002, 3000]));
                assert_eq!(
                    task_items(&f.load().snapshot, 3).unwrap(),
                    [3002, 3000, 3001]
                );
                assert_eq!(f.state(20).evidence_mass(), 2.0);
                assert_eq!(f.state(21).evidence_mass(), 1.0);
                assert!(!f.entities[&3001].contains_key("task-item/next"));
            }
            assert_eq!(
                f.entities[&3]["learner-task/status"],
                f.enums["learner-task.status/completed"]
            );
        }
    }

    #[test]
    fn malformed_presentation_chains_reject_completion_and_expiry_atomically() {
        assert!(
            task_items(&Fixture::new("assessment").load().snapshot, 3)
                .unwrap()
                .is_empty()
        );
        for fault in [
            "cycle",
            "merge",
            "multiple-heads",
            "disconnected",
            "foreign-next",
            "foreign-predecessor",
            "shared-member",
        ] {
            let mut f = Fixture::new("assessment");
            f.set(4, "assessment/time-limit-seconds", json!(60.0));
            let a = f.present(100);
            let b = f.present(110);
            let c = f.present(101);
            match fault {
                "cycle" => f.set(c, "task-item/next", json!(a)),
                "merge" => f.set(a, "task-item/next", json!(c)),
                "multiple-heads" => {
                    f.entities.get_mut(&a).unwrap().remove("task-item/next");
                }
                "disconnected" => {
                    f.set(a, "task-item/next", json!(c));
                    f.set(b, "task-item/next", json!(b));
                }
                "foreign-next" => {
                    f.put(
                        800,
                        json!({"task-item/id":uuid(800), "task-item/content":100}),
                    );
                    f.set(c, "task-item/next", json!(800));
                }
                "foreign-predecessor" => f.put(
                    800,
                    json!({"task-item/id":uuid(800), "task-item/content":100, "task-item/next":a}),
                ),
                "shared-member" => f.put(
                    800,
                    json!({"learner-task/id":uuid(800), "learner-task/items":[b]}),
                ),
                _ => unreachable!(),
            }
            let loaded = f.load();
            let before = loaded.engine.snapshot();
            assert!(task_items(&loaded.snapshot, 3).is_err(), "{fault}");
            let at = start() + Duration::seconds(60);
            let mut options = CompletionOptions::new(at);
            options.result = Some(true);
            assert!(complete_item(&loaded, a, options).is_err(), "{fault}");
            assert!(
                expire_task(&loaded, 3, at, None, ActivityRules::default()).is_err(),
                "{fault}"
            );
            assert_eq!(loaded.engine.snapshot(), before, "{fault}");
        }
    }

    #[test]
    fn forward_topic_edges_supply_incoming_readiness_and_external_scope_ancestors() {
        let mut f = Fixture::new("lesson");
        // Only 20 belongs to this course. 23 -> 21 -> 20 -> 22 makes the
        // direction observable: scope includes external ancestors, not 22.
        f.set(12, "module/topics", json!([20]));
        f.set(23, "topic/next", json!([21]));
        f.set(21, "topic/next", json!([20]));
        f.set(20, "topic/next", json!([22]));
        let loaded = f.load();
        assert_eq!(
            scope_topics(&loaded.snapshot, 10).unwrap(),
            BTreeSet::from([20, 21, 23])
        );
        assert_eq!(
            scope_topics(&loaded.snapshot, 20).unwrap(),
            BTreeSet::from([20, 21, 23])
        );
        assert_eq!(
            loaded.engine.neighborhoods[&loaded.topic_eid_to_id[&20]],
            vec![loaded.topic_eid_to_id[&21].clone()]
        );
        assert!(
            !loaded
                .engine
                .neighborhoods
                .contains_key(&loaded.topic_eid_to_id[&23])
        );
        let item = f.present(210);
        let options = CompletionOptions::new(start() + Duration::seconds(1));
        assert!(
            complete_item(&f.load(), item, options.clone())
                .err()
                .unwrap()
                .contains("prerequisite")
        );
        f.seed(21, 1.0);
        f.set(521, "progress/memory-at", instant_value(start()));
        // The unlearned dependent 22 cannot block starting 20's lesson.
        assert!(complete_item(&f.load(), item, options).is_ok());
        f.set(20, "topic/next", json!([40]));
        assert!(
            load_runtime(EntitySnapshot::new(f.entities, f.basis).unwrap(), 1, 2)
                .unwrap_err()
                .contains("topic/next must reference known topics")
        );
    }
}
