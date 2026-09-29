//! Task clocks are derived from added status datoms and their transaction times.
use crate::{
    Result,
    schema::{EntitySnapshot, parse_instant},
};
use chrono::{DateTime, Utc};
use std::collections::BTreeMap;

pub fn terminal(status: &str) -> bool {
    matches!(
        status,
        "task-item.status/completed"
            | "task-item.status/skipped"
            | "task-item.status/correct"
            | "task-item.status/incorrect"
    )
}

pub fn status(snapshot: &EntitySnapshot, entity: u64, attribute: &str) -> Result<String> {
    snapshot.ident(&serde_json::json!(snapshot.reference(entity, attribute)?))
}

pub fn validate_history(snapshot: &mut EntitySnapshot) -> Result<()> {
    snapshot
        .status_history
        .sort_by(|a, b| (a.t, a.entity, &a.attribute).cmp(&(b.t, b.entity, &b.attribute)));
    let mut times = BTreeMap::new();
    let mut latest = BTreeMap::new();
    let mut previous_time = None;
    for event in &snapshot.status_history {
        snapshot.entity(event.entity)?;
        if event.t > snapshot.basis_t {
            return Err("status history exceeds captured basis".into());
        }
        let value = snapshot.ident(&event.value)?;
        let allowed = match event.attribute.as_str() {
            "task-item/status" => [
                "started",
                "paused",
                "completed",
                "skipped",
                "correct",
                "incorrect",
            ]
            .as_slice(),
            "learner-task/status" => [
                "locked",
                "unlocked",
                "started",
                "paused",
                "completed",
                "failed",
            ]
            .as_slice(),
            _ => return Err("unsupported status history attribute".into()),
        };
        let entity_kind = event.attribute.split('/').next().unwrap();
        if !snapshot.types(event.entity)?.contains(entity_kind) {
            return Err("status history attribute does not match entity type".into());
        }
        let prefix = event.attribute.replace('/', ".");
        if !allowed.iter().any(|s| value == format!("{prefix}/{s}")) {
            return Err("invalid status history enum".into());
        }
        let at = parse_instant(&event.at)?;
        if previous_time.is_some_and(|previous| at < previous) {
            return Err("status history times must be chronological".into());
        }
        previous_time = Some(at);
        if times.insert(event.t, at).is_some_and(|other| other != at) {
            return Err("one transaction must have one instant".into());
        }
        let key = (event.entity, event.attribute.clone());
        if latest
            .insert(key, (event.t, value))
            .is_some_and(|(t, _)| t == event.t)
        {
            return Err("duplicate status assertion in a transaction".into());
        }
    }
    for ((entity, attribute), (_, last)) in latest {
        if status(snapshot, entity, &attribute)? != last {
            return Err("current status disagrees with history".into());
        }
    }
    Ok(())
}

pub fn history(
    snapshot: &EntitySnapshot,
    entity: u64,
    attribute: &str,
) -> Result<Vec<(DateTime<Utc>, String)>> {
    let events = snapshot
        .status_history
        .iter()
        .filter(|h| h.entity == entity && h.attribute == attribute)
        .map(|h| Ok((parse_instant(&h.at)?, snapshot.ident(&h.value)?)))
        .collect::<Result<Vec<_>>>()?;
    if events.is_empty() {
        return Err(format!("missing {attribute} history for {entity}"));
    }
    if events.last().unwrap().1 != status(snapshot, entity, attribute)? {
        return Err("current status disagrees with history".into());
    }
    Ok(events)
}

pub fn status_at(snapshot: &EntitySnapshot, entity: u64, attribute: &str) -> Result<DateTime<Utc>> {
    Ok(history(snapshot, entity, attribute)?.last().unwrap().0)
}

pub fn task_started(snapshot: &EntitySnapshot, task: u64) -> Result<DateTime<Utc>> {
    history(snapshot, task, "learner-task/status")?
        .into_iter()
        .find(|(_, s)| s == "learner-task.status/started")
        .map(|(at, _)| at)
        .ok_or("task has no recorded start".into())
}

pub fn elapsed(snapshot: &EntitySnapshot, item: u64, at: DateTime<Utc>) -> Result<f64> {
    let events = history(snapshot, item, "task-item/status")?;
    if events[0].1 != "task-item.status/started" {
        return Err("item timing requires its original start".into());
    }
    let mut total = 0.0;
    let mut previous: Option<(DateTime<Utc>, String)> = None;
    for (time, current) in events {
        if time > at {
            return Err("timing update predates status history".into());
        }
        if let Some((before, ref prior)) = previous {
            let valid = match prior.as_str() {
                "task-item.status/started" => {
                    current == "task-item.status/paused" || terminal(&current)
                }
                "task-item.status/paused" => current == "task-item.status/started",
                _ => false,
            };
            if !valid {
                return Err("invalid item status transition history".into());
            }
            if prior == "task-item.status/started" {
                total += (time - before).num_milliseconds() as f64 / 1000.0;
            }
        }
        previous = Some((time, current));
    }
    if let Some((before, status)) = previous {
        if status == "task-item.status/started" {
            total += (at - before).num_milliseconds() as f64 / 1000.0;
        }
    }
    Ok(total)
}

pub fn task_elapsed(snapshot: &EntitySnapshot, task: u64, at: DateTime<Utc>) -> Result<f64> {
    task_started(snapshot, task)?;
    snapshot
        .refs(task, "learner-task/items")?
        .iter()
        .map(|item| elapsed(snapshot, *item, at))
        .sum()
}

pub fn active_item(snapshot: &EntitySnapshot, learner: u64) -> Result<Option<u64>> {
    let mut active = None;
    for task in snapshot.refs(learner, "learner/activity")? {
        for item in snapshot.refs(task, "learner-task/items")? {
            if status(snapshot, item, "task-item/status")? == "task-item.status/started" {
                if active.replace(item).is_some() {
                    return Err("only one actively timed item per learner is allowed".into());
                }
            }
        }
    }
    Ok(active)
}
