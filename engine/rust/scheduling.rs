//! Lifecycle decisions derived from finalized history, never separate counters.
use crate::{Result, learning, retrieval, schema::EntitySnapshot};
use chrono::{DateTime, Utc};
use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet, VecDeque};

/// The Study page displays this many activities. Bound diversity traversals to
/// its visible prefix, while allowing tied reviews anywhere in the backlog in.
pub const STUDY_QUEUE_LIMIT: usize = 5;

#[derive(Clone, Debug)]
pub struct Finished {
    pub task: u64,
    pub activity: u64,
    pub topic: Option<u64>,
    pub kind: String,
    pub passed: bool,
    pub at: DateTime<Utc>,
}
#[derive(Clone, Debug, Default)]
pub struct Lifecycle {
    pub xp: f64,
    pub mastered: BTreeMap<u64, DateTime<Utc>>,
    pub assessed: BTreeSet<u64>,
    /// (triggering attempt, repair topic) -> next required activity kind.
    pub repairs: BTreeMap<(u64, u64), String>,
    pub finished: Vec<Finished>,
    pub lesson_failures: BTreeMap<u64, u64>,
    pub retakes: Vec<u64>,
    pub escalated: BTreeSet<u64>,
}
pub fn state(s: &EntitySnapshot, task: u64) -> Result<String> {
    Ok(s.ident(&serde_json::json!(
        s.reference(task, "learner-task/status")?
    ))?
    .rsplit('/')
    .next()
    .unwrap()
    .into())
}
pub fn original_kp(s: &EntitySnapshot, q: u64) -> Result<u64> {
    let kps = s.owners(q, "knowledge-point/questions")?;
    match kps.as_slice() {
        [kp] => Ok(*kp),
        _ => Err("Assessment question needs one knowledge-point owner".into()),
    }
}
fn failed_kp(s: &EntitySnapshot, task: u64) -> Result<Option<u64>> {
    let items = learning::ordered_presentations(s, task)?;
    let Some(q) = items.iter().rev().find_map(|i| {
        let q = s.optional_ref(*i, "task-item/content").ok().flatten()?;
        s.is_ordinary_question(q).ok()?.then_some(q)
    }) else {
        return Ok(None);
    };
    Ok(s.owners(q, "knowledge-point/questions")?.first().copied())
}
pub fn lifecycle(s: &EntitySnapshot, learner: u64) -> Result<Lifecycle> {
    let tasks: BTreeSet<_> = s.refs(learner, "learner/activity")?.into_iter().collect();
    let mut ends = BTreeMap::new();
    for e in &s.status_history {
        if e.attribute != "learner-task/status" || !tasks.contains(&e.entity) {
            continue;
        }
        let st = s.ident(&e.value)?;
        ends.insert(e.entity, (crate::schema::parse_instant(&e.at)?, st));
    }
    let mut finished = vec![];
    for &task in &tasks {
        let st = state(s, task)?;
        if !matches!(st.as_str(), "completed" | "failed") {
            continue;
        }
        let Some((at, recorded)) = ends.get(&task) else {
            continue;
        };
        if recorded != &format!("learner-task.status/{st}") {
            return Err("Current task status disagrees with history".into());
        }
        let activity = s.reference(task, "learner-task/activity")?;
        finished.push(Finished {
            task,
            activity,
            topic: s.optional_ref(activity, "activity/scope")?,
            kind: retrieval::kind(s, activity)?,
            passed: st == "completed",
            at: crate::timing::task_finished_at(s, task, *at)?,
        });
    }
    finished.sort_by_key(|f| (f.at, f.task));
    let mut h = Lifecycle::default();
    let mut previous_failure = BTreeMap::new();
    for f in &finished {
        if f.kind == "assessment" {
            if s.optional_ref(f.task, "learner-task/retake-of")?.is_none() {
                h.xp = 0.0;
            }
            let items = learning::ordered_presentations(s, f.task)?;
            let mut correct = 0;
            let steps = learning::lesson_steps(s, f.activity)?;
            for step in &steps {
                let topic = s.topic_for_question(step.content)?;
                h.assessed.insert(topic);
                let passed = items.iter().any(|i| {
                    s.optional_ref(*i, "task-item/content").ok().flatten() == Some(step.content)
                        && learning::question_outcome(s, *i).ok() == Some(Some(Some(true)))
                });
                if passed {
                    correct += 1;
                } else {
                    h.repairs.insert((f.task, topic), "review".into());
                }
            }
            if !steps.is_empty()
                && correct * 4 < steps.len() * 3
                && s.optional_ref(f.task, "learner-task/retake-of")?.is_none()
            {
                h.retakes.push(f.task);
            }
        } else if matches!(f.kind.as_str(), "lesson" | "review" | "assignment") {
            h.xp += s
                .entity(f.task)?
                .get("learner-task/xp-earned")
                .and_then(Value::as_f64)
                .unwrap_or(0.0);
            if let Some(topic) = f.topic {
                let origins = s.refs(f.task, "learner-task/remediation-for")?;
                for origin in origins {
                    if f.passed {
                        h.repairs.remove(&(origin, topic));
                    } else if f.kind == "review" && h.repairs.contains_key(&(origin, topic)) {
                        h.repairs.insert((origin, topic), "lesson".into());
                    }
                }
                if f.kind == "lesson" {
                    if f.passed {
                        h.mastered.entry(topic).or_insert(f.at);
                        h.lesson_failures.remove(&topic);
                        previous_failure.remove(&topic);
                    } else {
                        h.lesson_failures.insert(topic, f.task);
                        if let Some(kp) = failed_kp(s, f.task)? {
                            if previous_failure.get(&topic) == Some(&kp) {
                                let prerequisites =
                                    s.refs(kp, "knowledge-point/key-prerequisites")?;
                                if !prerequisites.is_empty() {
                                    h.escalated.insert(f.task);
                                }
                                for prerequisite in prerequisites {
                                    h.repairs.insert((f.task, prerequisite), "review".into());
                                }
                            }
                            previous_failure.insert(topic, kp);
                        }
                    }
                }
            }
        }
    }
    // A recorded terminal outcome is valid history even when migration retained
    // only the final snapshot. No fabricated start or repeated credit is needed.
    h.finished = finished;
    h.retakes.retain(|original| {
        !tasks.iter().any(|t| {
            s.optional_ref(*t, "learner-task/retake-of").ok().flatten() == Some(*original)
                && (matches!(
                    state(s, *t).ok().as_deref(),
                    Some("started" | "paused" | "completed" | "failed")
                ) || s
                    .optional_ref(*t, "learner-task/activity")
                    .ok()
                    .flatten()
                    .is_some_and(|a| retrieval::fresh(s, learner, a).unwrap_or(false)))
        })
    });
    Ok(h)
}
impl Lifecycle {
    pub fn retry_ready(&self, topic: u64) -> bool {
        let Some(task) = self.lesson_failures.get(&topic) else {
            return true;
        };
        if self.escalated.contains(task) {
            return true;
        }
        let Some(failure) = self.finished.iter().find(|f| f.task == *task) else {
            return false;
        };
        self.finished
            .iter()
            .filter(|f| {
                f.at > failure.at
                    && f.passed
                    && f.topic != Some(topic)
                    && matches!(f.kind.as_str(), "lesson" | "review" | "assignment")
            })
            .count()
            >= 5
    }
    pub fn assessment_origin(&self, s: &EntitySnapshot, origin: u64) -> Result<bool> {
        let mut pending = vec![origin];
        let mut visited = BTreeSet::new();
        while let Some(task) = pending.pop() {
            if !visited.insert(task) {
                continue;
            }
            if retrieval::kind(s, s.reference(task, "learner-task/activity")?)? == "assessment" {
                return Ok(true);
            }
            pending.extend(s.refs(task, "learner-task/remediation-for")?);
        }
        Ok(false)
    }
    pub fn lesson_blocked(&self, s: &EntitySnapshot, topic: u64) -> Result<bool> {
        for (&(origin, _), _) in &self.repairs {
            if s.optional_ref(
                s.reference(origin, "learner-task/activity")?,
                "activity/scope",
            )? == Some(topic)
            {
                return Ok(true);
            }
        }
        Ok(false)
    }
    pub fn retake_ready(&self, s: &EntitySnapshot, original: u64) -> Result<bool> {
        for (&(origin, _), _) in &self.repairs {
            let mut pending = vec![origin];
            let mut seen = BTreeSet::new();
            while let Some(task) = pending.pop() {
                if task == original {
                    return Ok(false);
                }
                if seen.insert(task) {
                    pending.extend(s.refs(task, "learner-task/remediation-for")?);
                }
            }
        }
        Ok(true)
    }
}
/// Filter automatic recommendations, including their focused-mode scope.
pub fn filter_candidates(
    s: &EntitySnapshot,
    l: u64,
    plan: Vec<learning::PlannedActivity>,
) -> Result<Vec<learning::PlannedActivity>> {
    filter_candidates_with_lesson_order(s, l, filter_study_focus(s, l, plan)?, false)
}

/// An explicit topic choice keeps the ordinary supply and lifecycle checks,
/// but focused mode only limits automatic recommendations.
pub(crate) fn filter_selected_candidates(
    s: &EntitySnapshot, l: u64, plan: Vec<learning::PlannedActivity>,
) -> Result<Vec<learning::PlannedActivity>> {
    filter_candidates_with_lesson_order(s, l, plan, false)
}

fn filter_study_focus(s: &EntitySnapshot, l: u64, plan: Vec<learning::PlannedActivity>)
    -> Result<Vec<learning::PlannedActivity>> {
    let mut focused = Vec::new();
    for candidate in plan {
        if learning::activity_in_study_focus(s, l, candidate.activity)? {
            focused.push(candidate);
        }
    }
    Ok(focused)
}

/// Target/queue study uses a soft layer preference and lesson interleaving.
/// Course planning and explicit Study Now retain their existing selection rules.
pub(crate) fn filter_self_directed_candidates(
    s: &EntitySnapshot,
    l: u64,
    plan: Vec<learning::PlannedActivity>,
) -> Result<Vec<learning::PlannedActivity>> {
    filter_candidates_with_lesson_order(s, l, filter_study_focus(s, l, plan)?, true)
}

fn filter_candidates_with_lesson_order(
    s: &EntitySnapshot,
    l: u64,
    mut plan: Vec<learning::PlannedActivity>,
    interleave_lessons: bool,
) -> Result<Vec<learning::PlannedActivity>> {
    let mut unique: Vec<learning::PlannedActivity> = vec![];
    let mut positions: BTreeMap<u64, usize> = BTreeMap::new();
    for candidate in plan {
        if let Some(&index) = positions.get(&candidate.activity) {
            if candidate.priority > unique[index].priority {
                unique[index] = candidate;
            }
        } else {
            positions.insert(candidate.activity, unique.len());
            unique.push(candidate);
        }
    }
    plan = unique;
    let h = lifecycle(s, l)?;
    let seen = learning::unavailable_questions(s, l)?;
    plan.retain(|p| {
        if retrieval::kind(s, p.activity).ok().as_deref() != Some("lesson") {
            return true;
        }
        let ongoing = s
            .refs(l, "learner/activity")
            .unwrap_or_default()
            .iter()
            .any(|t| {
                s.optional_ref(*t, "learner-task/activity").ok().flatten() == Some(p.activity)
                    && matches!(state(s, *t).ok().as_deref(), Some("started" | "paused"))
            });
        ongoing
            || crate::inventory::lesson_ready(
                s,
                &s.refs(p.topic, "topic/knowledge-points")
                    .unwrap_or_default(),
                &seen,
            )
            .unwrap_or(false)
    });
    // Unavailable lessons never establish a layer frontier or consume one of
    // the diversity choices. Later usable lessons remain eligible immediately.
    if interleave_lessons {
        diversify_lessons(s, l, &h, &mut plan)?;
    }
    let mut required = BTreeSet::new();
    for p in &plan {
        if p.priority >= 12000.0 {
            required.insert(p.activity);
        }
        for task in s.refs(l, "learner/activity")? {
            if s.reference(task, "learner-task/activity")? != p.activity
                || !matches!(
                    state(s, task)?.as_str(),
                    "unlocked" | "locked" | "started" | "paused"
                )
            {
                continue;
            }
            for origin in s.refs(task, "learner-task/remediation-for")? {
                if h.repairs.contains_key(&(origin, p.topic))
                    && h.assessment_origin(s, origin)?
                    && (retrieval::kind(s, p.activity)? != "lesson" || h.retry_ready(p.topic))
                {
                    required.insert(p.activity);
                }
            }
        }
    }
    if !required.is_empty() {
        plan.retain(|p| required.contains(&p.activity));
        return Ok(plan);
    }
    let due_assessments: BTreeSet<_> = plan
        .iter()
        .filter(|p| {
            retrieval::kind(s, p.activity).ok().as_deref() == Some("assessment")
                && h.xp >= 150.0
                && s.owners(p.activity, "learner-task/activity")
                    .unwrap_or_default()
                    .iter()
                    .any(|t| {
                        s.optional_ref(*t, "learner-task/retake-of")
                            .ok()
                            .flatten()
                            .is_none()
                    })
        })
        .map(|p| p.activity)
        .collect();
    if !due_assessments.is_empty() {
        plan.retain(|p| due_assessments.contains(&p.activity));
    }
    let last_offer = s
        .refs(l, "learner/activity")?
        .into_iter()
        .filter_map(|task| {
            let a = s.reference(task, "learner-task/activity").ok()?;
            if retrieval::kind(s, a).ok()?.as_str() != "lesson"
                || !s
                    .refs(task, "learner-task/remediation-for")
                    .ok()?
                    .is_empty()
            {
                return None;
            }
            s.entity(task)
                .ok()?
                .get("learner-task/offered-at")
                .and_then(|v| crate::schema::parse_instant(v).ok())
        })
        .max();
    let reviews = h
        .finished
        .iter()
        .filter(|f| {
            f.kind == "review"
                && last_offer.is_none_or(|at| f.at > at)
                && s.refs(f.task, "learner-task/remediation-for")
                    .unwrap_or_default()
                    .is_empty()
        })
        .count();
    if reviews >= 3
        && let Some(index) = plan.iter().position(|p| {
            retrieval::kind(s, p.activity).ok().as_deref() == Some("lesson") && p.priority < 11000.0
        })
    {
        let mut lesson = plan.remove(index);
        lesson.reason = "Optional lesson after three ordinary reviews".into();
        plan.insert(0, lesson);
    }
    // Ready retakes must remain visible ahead of a backlog of unfinished
    // lessons. Required repairs returned above; required assessments already
    // narrowed the plan. Keep retakes optional by preserving their priorities.
    let mut retake_activities = BTreeSet::new();
    for task in s.refs(l, "learner/activity")? {
        if s.optional_ref(task, "learner-task/retake-of")?.is_some()
            && matches!(state(s, task)?.as_str(), "locked" | "unlocked" | "started" | "paused")
        {
            retake_activities.insert(s.reference(task, "learner-task/activity")?);
        }
    }
    plan.sort_by_key(|candidate| !retake_activities.contains(&candidate.activity));
    diversify_reviews(s, l, &mut plan)?;
    Ok(plan)
}

/// Reorder only ordinary new lesson slots. Layer preference is a score, never
/// an eligibility gate: a graph-distance bonus of at most six can mix nearby
/// layers while keeping distant later layers behind available earlier work.
/// Recent completions seed the first choice, so returning to Study also varies
/// the next lesson rather than only varying the other cards on the same page.
fn diversify_lessons(
    s: &EntitySnapshot,
    learner: u64,
    history: &Lifecycle,
    plan: &mut [learning::PlannedActivity],
) -> Result<()> {
    const DISTANCE_CAP: usize = 6;
    let mut ordinary: BTreeSet<_> = plan.iter()
        .filter(|p| p.priority < 5000.0
            && retrieval::kind(s, p.activity).ok().as_deref() == Some("lesson"))
        .map(|p| p.activity).collect();
    for task in s.refs(learner, "learner/activity")? {
        if !matches!(state(s, task)?.as_str(), "locked" | "unlocked" | "started" | "paused") {
            continue;
        }
        if matches!(state(s, task)?.as_str(), "started" | "paused")
            || !s.refs(task, "learner-task/remediation-for")?.is_empty()
            || s.optional_ref(task, "learner-task/retake-of")?.is_some()
        {
            ordinary.remove(&s.reference(task, "learner-task/activity")?);
        }
    }
    let slots: Vec<_> = (0..plan.len())
        .filter(|&i| ordinary.contains(&plan[i].activity)).collect();
    if slots.len() < 2 {
        return Ok(());
    }
    let layers = learning::topic_layers(s)?;
    let graph = s.topic_neighbors()?;
    let mut nearest: BTreeMap<_, _> = slots.iter()
        .map(|&i| (plan[i].topic, DISTANCE_CAP)).collect();
    let update_distances = |sources: Vec<u64>, nearest: &mut BTreeMap<u64, usize>| {
        let mut distances = BTreeMap::new();
        let mut pending = VecDeque::new();
        for topic in sources {
            if distances.insert(topic, 0usize).is_none() {
                pending.push_back(topic);
            }
        }
        while let Some(topic) = pending.pop_front() {
            let distance = distances[&topic];
            if let Some(value) = nearest.get_mut(&topic) {
                *value = (*value).min(distance);
            }
            if distance + 1 >= DISTANCE_CAP {
                continue;
            }
            for &neighbor in graph.get(&topic).into_iter().flatten() {
                if let std::collections::btree_map::Entry::Vacant(entry) = distances.entry(neighbor) {
                    entry.insert(distance + 1);
                    pending.push_back(neighbor);
                }
            }
        }
    };
    let recent = history.finished.iter().rev()
        .filter(|f| f.passed && matches!(f.kind.as_str(), "lesson" | "review"))
        .filter_map(|f| f.topic).take(3).collect();
    update_distances(recent, &mut nearest);
    // Rank lesson slots even when reviews precede the visible prefix, because
    // the three-review break below may promote the first lesson onto the page.
    for (chosen, &slot) in slots.iter().take(STUDY_QUEUE_LIMIT).enumerate() {
        let best = slots[chosen..].iter().copied().max_by(|&a, &b| {
            let score = |i: usize| nearest[&plan[i].topic] as i64 - layers[&plan[i].topic] as i64;
            score(a).cmp(&score(b))
                .then_with(|| layers[&plan[b].topic].cmp(&layers[&plan[a].topic]))
                .then_with(|| plan[a].priority.total_cmp(&plan[b].priority))
                .then_with(|| plan[b].topic.cmp(&plan[a].topic))
                .then_with(|| plan[b].activity.cmp(&plan[a].activity))
        }).unwrap();
        plan.swap(slot, best);
        if chosen + 1 < slots.len().min(STUDY_QUEUE_LIMIT) {
            update_distances(vec![plan[slot].topic], &mut nearest);
        }
    }
    Ok(())
}

/// Select within equal-priority ordinary review slots only. Required work,
/// resumable attempts, assessments, and the three-review lesson offer keep their
/// positions. The first review is longest overdue; subsequent reviews maximize
/// distance to the closest already selected review, then overdue age and task ID.
fn diversify_reviews(
    s: &EntitySnapshot,
    learner: u64,
    plan: &mut [learning::PlannedActivity],
) -> Result<()> {
    let activities: BTreeSet<_> = plan
        .iter()
        .filter(|p| {
            p.priority < 10000.0 && retrieval::kind(s, p.activity).ok().as_deref() == Some("review")
        })
        .map(|p| p.activity)
        .collect();
    if activities.len() < 2 {
        return Ok(());
    }
    let mut tasks = BTreeMap::new();
    for task in s.refs(learner, "learner/activity")? {
        let activity = s.reference(task, "learner-task/activity")?;
        if activities.contains(&activity)
            && matches!(state(s, task)?.as_str(), "locked" | "unlocked")
            && s.refs(task, "learner-task/remediation-for")?.is_empty()
            && s.optional_ref(task, "learner-task/retake-of")?.is_none()
        {
            tasks.insert(activity, task);
        }
    }
    if tasks.len() < 2
        || !plan
            .iter()
            .take(STUDY_QUEUE_LIMIT)
            .any(|p| tasks.contains_key(&p.activity))
    {
        return Ok(());
    }
    let threshold = s
        .entities
        .with_attribute("policy/id")
        .first()
        .and_then(|p| s.entities[p].get("policy/review-threshold"))
        .and_then(Value::as_f64);
    let mut due_at = BTreeMap::new();
    if let Some(threshold) = threshold.filter(|v| v.is_finite() && *v > 0.0) {
        for progress in s.refs(learner, "learner/knowledge-profile")? {
            let r = s.entity(progress)?;
            if r.get("progress/learned").and_then(Value::as_bool) != Some(true) {
                continue;
            }
            if let (Some(memory), Some(interval), Some(anchor)) = (
                r.get("progress/memory").and_then(Value::as_f64),
                r.get("progress/interval-days").and_then(Value::as_f64),
                r.get("progress/memory-at"),
            ) {
                if memory.is_finite() && memory >= 0.0 && interval.is_finite() && interval > 0.0 {
                    let anchor = crate::schema::instant_days(anchor)?;
                    // Match TopicState::due_at: depleted memory is due at its
                    // observation time, not infinitely far into the past.
                    let due = if memory <= threshold {
                        anchor
                    } else {
                        anchor + interval * (memory.log2() - threshold.log2())
                    };
                    due_at.insert(s.reference(progress, "progress/topic")?, due);
                }
            }
        }
    }
    let graph = s.topic_neighbors()?;
    // Every finite shortest path has fewer than V edges. Disconnected topics
    // use V rather than infinity, and equal distances remain deterministic.
    let far = graph.len().max(1);
    let mut nearest: BTreeMap<_, _> = plan.iter().map(|p| (p.topic, far)).collect();
    for slot in 0..plan.len().min(STUDY_QUEUE_LIMIT) {
        if !tasks.contains_key(&plan[slot].activity) {
            continue;
        }
        let best = (slot..plan.len())
            .filter(|&i| {
                tasks.contains_key(&plan[i].activity) && plan[i].priority == plan[slot].priority
            })
            .max_by(|&a, &b| {
                nearest[&plan[a].topic]
                    .cmp(&nearest[&plan[b].topic])
                    .then_with(|| {
                        due_at
                            .get(&plan[b].topic)
                            .unwrap_or(&f64::INFINITY)
                            .total_cmp(due_at.get(&plan[a].topic).unwrap_or(&f64::INFINITY))
                    })
                    .then_with(|| tasks[&plan[b].activity].cmp(&tasks[&plan[a].activity]))
            })
            .unwrap();
        plan.swap(slot, best);
        if slot + 1 == plan.len().min(STUDY_QUEUE_LIMIT) {
            break;
        }
        let mut distances = BTreeMap::from([(plan[slot].topic, 0)]);
        let mut pending = VecDeque::from([plan[slot].topic]);
        while let Some(topic) = pending.pop_front() {
            let distance = distances[&topic];
            if let Some(nearest) = nearest.get_mut(&topic) {
                *nearest = (*nearest).min(distance);
            }
            for &neighbor in graph.get(&topic).into_iter().flatten() {
                if let std::collections::btree_map::Entry::Vacant(entry) = distances.entry(neighbor)
                {
                    entry.insert(distance + 1);
                    pending.push_back(neighbor);
                }
            }
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    fn fixture() -> (EntitySnapshot, Vec<learning::PlannedActivity>) {
        let mut records = BTreeMap::new();
        for (id, ident) in [
            (10, "activity.type/review"),
            (11, "learner-task.status/unlocked"),
            (12, "learner-task.status/paused"),
            (13, "activity.type/lesson"),
            (14, "activity.type/assessment"),
        ] {
            records.insert(id, json!({"db/ident":ident}).as_object().unwrap().clone());
        }
        records.insert(
            1,
            json!({"learner/id":"test", "learner/activity":(300..308).collect::<Vec<_>>(),
            "learner/knowledge-profile":(400..408).collect::<Vec<_>>()})
            .as_object()
            .unwrap()
            .clone(),
        );
        records.insert(
            2,
            json!({"policy/id":"test", "policy/review-threshold":0.5})
                .as_object()
                .unwrap()
                .clone(),
        );
        let mut plan = vec![];
        for i in 0..8 {
            records.insert(
                100 + i,
                json!({"topic/id":format!("topic-{i}")})
                    .as_object()
                    .unwrap()
                    .clone(),
            );
            records.insert(
                200 + i,
                json!({"activity/id":format!("review-{i}"),"activity/type":10,
                "activity/scope":100+i})
                .as_object()
                .unwrap()
                .clone(),
            );
            records.insert(
                300 + i,
                json!({"learner-task/activity":200+i,"learner-task/status":11})
                    .as_object()
                    .unwrap()
                    .clone(),
            );
            records.insert(
                400 + i,
                json!({"progress/topic":100+i,"progress/learned":true,
                "progress/memory":1.0,"progress/interval-days":1.0,
                "progress/memory-at":{"$instant":if i==2 {0} else {86400000}}})
                .as_object()
                .unwrap()
                .clone(),
            );
            plan.push(learning::PlannedActivity {
                activity: 200 + i,
                topic: 100 + i,
                priority: 6000.0,
                target_count: 0,
                target_topics: vec![],
                remaining_topics: 0,
                nearest_target_steps: None,
                due: None,
                reason: "Spaced review is due".into(),
            });
        }
        // Intermediate topics are not due candidates. Edges point only forward;
        // diversity must still measure distance backward and across these nodes.
        for (i, from, to) in [
            (0, 100, 101),
            (1, 101, 102),
            (2, 102, 103),
            (3, 103, 104),
            (4, 104, 105),
            (5, 106, 107),
        ] {
            records
                .get_mut(&from)
                .unwrap()
                .insert("topic/next".into(), json!([900 + i]));
            records.insert(
                900 + i,
                json!({"topic/id":format!("bridge-{i}"),"topic/next":[to]})
                    .as_object()
                    .unwrap()
                    .clone(),
            );
        }
        (EntitySnapshot::new(records, 1).unwrap(), plan)
    }

    #[test]
    fn review_variety_uses_whole_undirected_graph_and_can_select_beyond_five() {
        let (s, plan) = fixture();
        let selected = filter_candidates(&s, 1, plan.clone()).unwrap();
        assert_eq!(
            selected.iter().take(5).map(|p| p.topic).collect::<Vec<_>>(),
            [102, 106, 105, 100, 101]
        );
        assert_eq!(selected.len(), plan.len());
        assert_eq!(
            selected.iter().map(|p| p.activity).collect::<BTreeSet<_>>(),
            plan.iter().map(|p| p.activity).collect()
        );
        // Deterministic even if equal-priority input order changes or a caller
        // passes the already diversified plan a second time.
        let mut reversed = plan;
        reversed.reverse();
        let again = filter_candidates(&s, 1, reversed).unwrap();
        assert_eq!(
            again.iter().take(5).map(|p| p.activity).collect::<Vec<_>>(),
            selected
                .iter()
                .take(5)
                .map(|p| p.activity)
                .collect::<Vec<_>>()
        );
        let again = filter_candidates(&s, 1, selected.clone()).unwrap();
        assert_eq!(
            again.iter().take(5).map(|p| p.activity).collect::<Vec<_>>(),
            selected
                .iter()
                .take(5)
                .map(|p| p.activity)
                .collect::<Vec<_>>()
        );
    }

    #[test]
    fn review_variety_preserves_priorities_and_fixed_activity_slots() {
        let (mut s, mut plan) = fixture();
        // A paused review, an optional lesson offer, and an assessment retain
        // their positions. Different review priorities cannot trade places.
        s.entities
            .get_mut(&300)
            .unwrap()
            .insert("learner-task/status".into(), json!(12));
        s.entities
            .get_mut(&201)
            .unwrap()
            .insert("activity/type".into(), json!(13));
        s.entities
            .get_mut(&203)
            .unwrap()
            .insert("activity/type".into(), json!(14));
        plan[0].priority = 10001.0;
        plan[1].reason = "Optional lesson after three ordinary reviews".into();
        plan[2].priority = 6500.0;
        let original = plan.clone();
        diversify_reviews(&s, 1, &mut plan).unwrap();
        for index in [0, 1, 2, 3] {
            assert_eq!(plan[index].activity, original[index].activity);
        }
        assert_eq!(plan[1].reason, original[1].reason);
        assert_eq!(
            plan.iter().map(|p| p.priority).collect::<Vec<_>>(),
            original.iter().map(|p| p.priority).collect::<Vec<_>>()
        );
    }

    #[test]
    fn review_variety_leaves_repairs_and_retakes_in_place() {
        let (mut s, mut plan) = fixture();
        s.entities
            .get_mut(&300)
            .unwrap()
            .insert("learner-task/remediation-for".into(), json!([301]));
        s.entities
            .get_mut(&301)
            .unwrap()
            .insert("learner-task/retake-of".into(), json!(300));
        diversify_reviews(&s, 1, &mut plan).unwrap();
        assert_eq!(plan[0].activity, 200);
        assert_eq!(plan[1].activity, 201);
        assert_eq!(plan[2].topic, 102);
        assert_eq!(plan[3].topic, 106);
    }

    #[test]
    fn review_variety_does_not_treat_zero_memory_as_infinitely_overdue() {
        let (mut s, plan) = fixture();
        // Topic 102 has an older observation. A recently depleted topic must
        // not jump ahead of it just because log2(0) is negative infinity.
        s.entities
            .get_mut(&403)
            .unwrap()
            .insert("progress/memory".into(), json!(0.0));
        let selected = filter_candidates(&s, 1, plan).unwrap();
        assert_eq!(selected[0].topic, 102);
    }

    #[test]
    fn review_variety_handles_missing_memory_and_isolated_topics_with_task_id_ties() {
        let (mut s, mut plan) = fixture();
        for id in 400..408 {
            s.entities.get_mut(&id).unwrap().remove("progress/memory");
        }
        for id in 100..108 {
            s.entities.get_mut(&id).unwrap().remove("topic/next");
        }
        for id in 900..906 {
            s.entities.get_mut(&id).unwrap().remove("topic/next");
        }
        plan.reverse();
        diversify_reviews(&s, 1, &mut plan).unwrap();
        assert_eq!(
            plan.iter().take(5).map(|p| p.activity).collect::<Vec<_>>(),
            [200, 201, 202, 203, 204]
        );
    }

    fn lesson_fixture() -> (EntitySnapshot, Vec<learning::PlannedActivity>) {
        let (mut s, mut plan) = fixture();
        for candidate in &mut plan {
            s.entities.get_mut(&candidate.activity).unwrap().insert("activity/type".into(), json!(13));
            candidate.priority = 1.0;
            candidate.reason = "Selected lesson".into();
        }
        (s, plan)
    }

    fn recent_topic(topic: u64) -> Lifecycle {
        Lifecycle {
            finished: vec![Finished {
                task: 0, activity: 0, topic: Some(topic), kind: "lesson".into(),
                passed: true, at: DateTime::from_timestamp(1_000, 0).unwrap(),
            }],
            ..Lifecycle::default()
        }
    }

    #[test]
    fn lesson_variety_prefers_early_layers_then_interleaves_across_the_full_pool() {
        let (s, mut plan) = lesson_fixture();
        plan.reverse();
        let selected = filter_self_directed_candidates(&s, 1, plan.clone()).unwrap();
        assert_eq!(selected.iter().take(5).map(|p| p.topic).collect::<Vec<_>>(),
            [100, 106, 101, 107, 102]);
        assert_eq!(selected.iter().map(|p| p.activity).collect::<BTreeSet<_>>(),
            plan.iter().map(|p| p.activity).collect());
        let again = filter_self_directed_candidates(&s, 1, selected.clone()).unwrap();
        assert_eq!(again.iter().take(5).map(|p| p.topic).collect::<Vec<_>>(),
            selected.iter().take(5).map(|p| p.topic).collect::<Vec<_>>());
        // The ordinary course/manual path never invokes the new lesson order.
        assert_eq!(filter_candidates(&s, 1, plan.clone()).unwrap().iter().map(|p| p.topic).collect::<Vec<_>>(),
            plan.iter().map(|p| p.topic).collect::<Vec<_>>());
    }

    #[test]
    fn lesson_variety_uses_recent_study_to_mix_layers_without_large_jumps() {
        let (s, plan) = lesson_fixture();
        let history = recent_topic(900); // Adjacent to the earliest lesson 100.
        let mut selected: Vec<_> = plan.iter().filter(|p| [100, 107, 105].contains(&p.topic)).cloned().collect();
        diversify_lessons(&s, 1, &history, &mut selected).unwrap();
        assert_eq!(selected.iter().map(|p| p.topic).collect::<Vec<_>>(), [107, 100, 105]);
        let layers = learning::topic_layers(&s).unwrap();
        assert!(layers[&107] > layers[&100], "variety may serve a later layer first");
        assert!(layers[&105] > layers[&107] + 6, "the distant lesson remains behind earlier work");
        let mut no_history: Vec<_> = plan.iter().filter(|p| [100, 107, 105].contains(&p.topic)).cloned().collect();
        diversify_lessons(&s, 1, &Lifecycle::default(), &mut no_history).unwrap();
        assert_eq!(no_history[0].topic, 100);
    }

    #[test]
    fn lesson_variety_preserves_nonlesson_and_saved_remediation_slots() {
        let (mut s, mut plan) = lesson_fixture();
        s.entities.get_mut(&200).unwrap().insert("activity/type".into(), json!(10));
        s.entities.get_mut(&201).unwrap().insert("activity/type".into(), json!(14));
        s.entities.get_mut(&302).unwrap().insert("learner-task/status".into(), json!(12));
        s.entities.get_mut(&303).unwrap().insert("learner-task/remediation-for".into(), json!([300]));
        s.entities.get_mut(&304).unwrap().insert("learner-task/retake-of".into(), json!(300));
        plan[5].priority = 12000.0;
        let before = plan.clone();
        diversify_lessons(&s, 1, &recent_topic(106), &mut plan).unwrap();
        for slot in 0..6 {
            assert_eq!(plan[slot].activity, before[slot].activity);
            assert_eq!(plan[slot].priority, before[slot].priority);
        }
        assert_eq!(plan.iter().map(|p| p.activity).collect::<BTreeSet<_>>(),
            before.iter().map(|p| p.activity).collect());
    }

    #[test]
    fn unavailable_lessons_are_removed_before_layer_and_variety_selection() {
        let (mut s, plan) = lesson_fixture();
        // Both earliest roots have empty banks. Their descendants still fill
        // the lesson slots; no earliest-layer group can become a barrier.
        s.entities.insert(950, json!({"knowledge-point/id":"empty", "knowledge-point/questions":[]})
            .as_object().unwrap().clone());
        for topic in [100, 106] {
            s.entities.get_mut(&topic).unwrap().insert("topic/knowledge-points".into(), json!([950]));
        }
        let selected = filter_self_directed_candidates(&s, 1, plan).unwrap();
        assert_eq!(selected.iter().take(2).map(|p| p.topic).collect::<Vec<_>>(), [101, 107]);
        assert_eq!(selected.len(), 6);
        assert!(selected.iter().all(|p| ![100, 106].contains(&p.topic)));
    }

    #[test]
    fn lesson_variety_ranks_beyond_review_cards_for_the_next_lesson_offer() {
        let (mut s, mut plan) = lesson_fixture();
        for candidate in plan.iter_mut().take(5) {
            s.entities.get_mut(&candidate.activity).unwrap().insert("activity/type".into(), json!(10));
            candidate.priority = 6000.0;
        }
        let first_five: Vec<_> = plan.iter().take(5).map(|p| p.activity).collect();
        diversify_lessons(&s, 1, &Lifecycle::default(), &mut plan).unwrap();
        assert_eq!(plan.iter().take(5).map(|p| p.activity).collect::<Vec<_>>(), first_five);
        assert_eq!(plan[5].topic, 106);
    }
}
