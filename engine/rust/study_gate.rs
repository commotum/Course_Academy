//! Authoritative Study-only exclusivity; voluntary topic actions remain separate.
use crate::{Result, inventory, learning, retrieval, scheduling, schema::EntitySnapshot};
use chrono::{DateTime, Utc};
use serde::Serialize;
use std::collections::BTreeSet;

#[derive(Clone, Debug, Default, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct StudyGate {
    pub active: bool,
    pub kind: Option<&'static str>,
    pub activity_ids: BTreeSet<u64>,
    pub task_ids: BTreeSet<u64>,
}
impl StudyGate {
    pub fn allows(&self, activity: u64, task: Option<u64>) -> bool {
        !self.active
            || self.activity_ids.contains(&activity)
            || task.is_some_and(|id| self.task_ids.contains(&id))
    }
}

/// Resolve only mandatory work, without ranking ordinary lessons/reviews or
/// preparing transactions. Call at queue/lifecycle boundaries and retain the
/// result during assessment drafts and navigation.
pub fn resolve(s: &EntitySnapshot, learner: u64, at: DateTime<Utc>) -> Result<StudyGate> {
    let h = scheduling::lifecycle(s, learner)?;
    let tasks = s.refs(learner, "learner/activity")?;
    let mut repairs = BTreeSet::new();
    for (&(origin, topic), kind) in &h.repairs {
        if h.assessment_origin(s, origin)?
            && learning::topic_in_study_focus(s, learner, topic)?
            && (kind != "lesson" || (h.retry_ready(topic) && !h.lesson_blocked(s, topic)?))
        {
            repairs.insert((topic, kind.clone()));
        }
    }
    let mut gate = StudyGate::default();
    let mut seen = None;
    for (topic, kind) in repairs {
        let mut ready = false;
        for &task in &tasks {
            let state = scheduling::state(s, task)?;
            if !matches!(state.as_str(), "locked" | "unlocked" | "started" | "paused") {
                continue;
            }
            let activity = s.reference(task, "learner-task/activity")?;
            if retrieval::kind(s, activity)? != kind
                || s.optional_ref(activity, "activity/scope")? != Some(topic)
            {
                continue;
            }
            let ongoing = matches!(state.as_str(), "started" | "paused");
            let origins = s.refs(task, "learner-task/remediation-for")?;
            let linked = origins.iter().any(|origin| {
                h.repairs.get(&(*origin, topic)) == Some(&kind)
                    && h.assessment_origin(s, *origin).unwrap_or(false)
            });
            if !linked && (ongoing || !origins.is_empty()) {
                continue;
            }
            let usable = if ongoing {
                true
            } else if kind == "lesson" {
                let unavailable = unavailable(s, learner, &mut seen)?;
                inventory::lesson_ready(s, &s.refs(topic, "topic/knowledge-points")?, unavailable)?
                    && learning::lesson_steps(s, activity).is_ok()
                    && learning::first_content(s, activity, learner)?.is_some()
            } else {
                let unavailable = unavailable(s, learner, &mut seen)?;
                learning::lesson_steps(s, activity)?.iter().all(|step| {
                    !unavailable.contains(&step.content)
                        && learning::validate_practice_question(s, step.content).is_ok()
                })
            };
            if usable {
                ready = true;
                gate.activity_ids.insert(activity);
                gate.task_ids.insert(task);
            }
        }
        // A ready obligation already excludes unrelated work before its task
        // is materialized by the background planner. Supply/retry shortages
        // retain the established ordinary-study fallback.
        if !ready {
            let unavailable = unavailable(s, learner, &mut seen)?;
            if kind == "review" {
                ready = retrieval::review_ready_for_gate(s, learner, topic, unavailable, &h)?;
            } else {
                for activity in s.owners(topic, "activity/scope")? {
                    if retrieval::kind(s, activity)? == "lesson"
                        && inventory::lesson_ready(
                            s,
                            &s.refs(topic, "topic/knowledge-points")?,
                            unavailable,
                        )?
                        && learning::first_content(s, activity, learner)?.is_some()
                    {
                        ready = true;
                        gate.activity_ids.insert(activity);
                        break;
                    }
                }
            }
        }
        gate.active |= ready;
    }
    if gate.active {
        gate.kind = Some("repairs");
        return Ok(gate);
    }
    if h.xp < retrieval::ASSESSMENT_REQUIRED_XP {
        return Ok(gate);
    }
    let mut ordinary = vec![];
    for task in tasks {
        let state = scheduling::state(s, task)?;
        if !matches!(state.as_str(), "locked" | "unlocked" | "started" | "paused")
            || s.optional_ref(task, "learner-task/retake-of")?.is_some()
        {
            continue;
        }
        let activity = s.reference(task, "learner-task/activity")?;
        if retrieval::kind(s, activity)? != "assessment"
            || !learning::activity_in_study_focus(s, learner, activity)?
        {
            continue;
        }
        if matches!(state.as_str(), "started" | "paused") {
            gate.active = true;
            gate.kind = Some("assessment");
            gate.activity_ids.insert(activity);
            gate.task_ids.insert(task);
        } else if state != "locked"
            || s.entity(task)?
                .get("learner-task/priority")
                .and_then(serde_json::Value::as_f64)
                != Some(0.)
        {
            ordinary.push((task, activity));
        }
    }
    if gate.active {
        return Ok(gate);
    }
    if !ordinary.is_empty() {
        let eligible = retrieval::assessment_topics(s, learner, at)?;
        let unavailable = unavailable(s, learner, &mut seen)?;
        for (task, activity) in ordinary {
            if retrieval::ordinary_assessment_ready_with_context(
                s,
                activity,
                unavailable,
                &h.assessed,
                &eligible,
            )
            .unwrap_or(false)
            {
                gate.active = true;
                gate.kind = Some("assessment");
                gate.activity_ids.insert(activity);
                gate.task_ids.insert(task);
            }
        }
    }
    if !gate.active && retrieval::assessment_definition(s, learner, at)?.is_some() {
        gate.active = true;
        gate.kind = Some("assessment");
    }
    Ok(gate)
}

fn unavailable<'a>(
    s: &EntitySnapshot,
    learner: u64,
    seen: &'a mut Option<BTreeSet<u64>>,
) -> Result<&'a BTreeSet<u64>> {
    if seen.is_none() {
        *seen = Some(learning::unavailable_questions(s, learner)?);
    }
    Ok(seen.as_ref().unwrap())
}
