//! Lifecycle decisions derived from finalized history, never separate counters.
use crate::{Result, learning, retrieval, schema::EntitySnapshot};
use chrono::{DateTime, Utc};
use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};

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
    let mut starts = BTreeSet::new();
    let mut ends = BTreeMap::new();
    for e in &s.status_history {
        if e.attribute != "learner-task/status" || !tasks.contains(&e.entity) {
            continue;
        }
        let st = s.ident(&e.value)?;
        if st == "learner-task.status/started" {
            starts.insert(e.entity);
        }
        ends.insert(e.entity, (crate::schema::parse_instant(&e.at)?, st));
    }
    let mut finished = vec![];
    for &task in &tasks {
        let st = state(s, task)?;
        if !starts.contains(&task) || !matches!(st.as_str(), "completed" | "failed") {
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
            at: *at,
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
    // Missing recorded starts deliberately excludes partially imported attempts.
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
/// Apply the same gates to recommendations and API start/resume eligibility.
pub fn filter_candidates(
    s: &EntitySnapshot,
    l: u64,
    mut plan: Vec<learning::PlannedActivity>,
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
            || crate::inventory::ready(
                s,
                &s.refs(p.topic, "topic/knowledge-points")
                    .unwrap_or_default(),
                &seen,
                true,
            )
            .unwrap_or(false)
    });
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
    Ok(plan)
}
