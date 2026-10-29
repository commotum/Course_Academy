//! Task clocks use status history, with saved duration checkpoints for imports.
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

/// A migration's recording instant is later than the original completion.
/// Preserve the source date without changing transaction or working clocks.
pub fn task_finished_at(snapshot: &EntitySnapshot, task: u64, recorded_at: DateTime<Utc>) -> Result<DateTime<Utc>> {
    let Some(value) = snapshot.entity(task)?.get("learner-task/finished-at") else {
        return Ok(recorded_at);
    };
    let finished = parse_instant(value)?;
    if !matches!(status(snapshot, task, "learner-task/status")?.as_str(),
        "learner-task.status/completed" | "learner-task.status/failed") || finished > recorded_at
    {
        return Err("original task finish requires a terminal task and cannot follow its recorded finish".into());
    }
    Ok(finished)
}

pub fn task_started(snapshot: &EntitySnapshot, task: u64) -> Result<DateTime<Utc>> {
    let events = history(snapshot, task, "learner-task/status")?;
    if matches!(
        events[0].1.as_str(),
        "learner-task.status/paused"
            | "learner-task.status/completed"
            | "learner-task.status/failed"
    ) {
        // An imported task has no original start in this database. Its first
        // recorded status is the earliest local bound, even after resuming.
        saved_elapsed(snapshot, task, "learner-task/elapsed-seconds")?;
        return Ok(events[0].0);
    }
    events
        .into_iter()
        .find(|(_, s)| s == "learner-task.status/started")
        .map(|(at, _)| at)
        .ok_or("task has no recorded start".into())
}

fn saved_elapsed(snapshot: &EntitySnapshot, entity: u64, attribute: &str) -> Result<f64> {
    snapshot
        .entity(entity)?
        .get(attribute)
        .and_then(serde_json::Value::as_f64)
        .filter(|seconds| seconds.is_finite() && *seconds >= 0.0)
        .ok_or_else(|| format!("imported timing requires finite nonnegative {attribute}"))
}

pub fn elapsed(snapshot: &EntitySnapshot, item: u64, at: DateTime<Utc>) -> Result<f64> {
    let periods = snapshot.refs(item,"task-item/working-periods")?;
    if !periods.is_empty() {
        let running=status(snapshot,item,"task-item/status")?=="task-item.status/started";
        let mut intervals=periods.into_iter().map(|p| {
            let e=snapshot.entity(p)?;
            Ok((parse_instant(e.get("working-period/started-at").ok_or("working period needs a start")?)?,e.get("working-period/ended-at").map(parse_instant).transpose()?))
        }).collect::<Result<Vec<_>>>()?;
        intervals.sort_by_key(|p|p.0);
        let mut total=0.;let mut previous=None;let mut open=false;
        for (start,end) in intervals {
            if start>at || end.is_some_and(|end|end<start||end>at) || previous.is_some_and(|end|start<end) || open {return Err("invalid working periods".into());}
            open=end.is_none(); previous=end;
            total+=(end.unwrap_or(at)-start).num_milliseconds() as f64/1000.;
        }
        if open!=running {return Err("working period disagrees with presentation status".into());}
        return Ok(total);
    }
    let events = history(snapshot, item, "task-item/status")?;
    let imported = events[0].1 != "task-item.status/started";
    if imported && events[0].1 != "task-item.status/paused" && !terminal(&events[0].1) {
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
                "task-item.status/paused" => {
                    current == "task-item.status/started"
                        || terminal(&current)
                            && snapshot
                                .owners(item, "learner-task/items")?
                                .iter()
                                .any(|task| {
                                    snapshot
                                        .reference(*task, "learner-task/activity")
                                        .ok()
                                        .and_then(|a| {
                                            snapshot
                                                .entity(a)
                                                .ok()?
                                                .get("activity/type")
                                                .and_then(|v| snapshot.ident(v).ok())
                                        })
                                        .as_deref()
                                        == Some("activity.type/assessment")
                                })
                }
                // Regrading changes the recorded outcome without reopening
                // the presentation or adding working time after submission.
                "task-item.status/correct" | "task-item.status/incorrect" => matches!(
                    current.as_str(),
                    "task-item.status/correct" | "task-item.status/incorrect"
                ),
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
    if imported {
        // Every timing transition saves the cumulative duration alongside its
        // new status. The current checkpoint already includes closed intervals
        // since import; adding those intervals again would double-count them.
        total = saved_elapsed(snapshot, item, "task-item/elapsed-seconds")?;
    }
    if let Some((before, status)) = previous {
        if status == "task-item.status/started" {
            total += (at - before).num_milliseconds() as f64 / 1000.0;
        }
    }
    if let Some(value) = snapshot.entity(item)?.get("task-item/working-ended-at") {
        let ended = parse_instant(value)?;
        if !terminal(&status(snapshot,item,"task-item/status")?) || ended > at || ended < events_first(snapshot,item)? {
            return Err("invalid working-time submission cutoff".into());
        }
        // Imported checkpoints are saved with the cutoff already applied.
        if !imported { total = (total - working_after(snapshot,item,ended,at)?).max(0.0); }
    }
    Ok(total)
}

fn events_first(snapshot:&EntitySnapshot,item:u64)->Result<DateTime<Utc>> {
    Ok(history(snapshot,item,"task-item/status")?[0].0)
}

fn working_after(snapshot:&EntitySnapshot,item:u64,until:DateTime<Utc>,at:DateTime<Utc>)->Result<f64> {
    let events=history(snapshot,item,"task-item/status")?;
    let mut waiting=0.;
    for (index,(start,state)) in events.iter().enumerate() {
        if state != "task-item.status/started" {continue;}
        let end=events.get(index+1).map(|event|event.0).unwrap_or(at).min(at);
        waiting += (end-(*start).max(until)).num_milliseconds().max(0) as f64/1000.;
    }
    Ok(waiting)
}

/// Cut off working time at admission while keeping the transaction clock current.
pub fn elapsed_until(snapshot:&EntitySnapshot,item:u64,at:DateTime<Utc>,until:DateTime<Utc>)->Result<f64> {
    if until>at || until<events_first(snapshot,item)? {return Err("invalid submission instant".into());}
    Ok((elapsed(snapshot,item,at)?-working_after(snapshot,item,until,at)?).max(0.))
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

#[cfg(test)]
mod tests {
    use super::*;
    use crate::schema::{instant_value, keyword};
    use serde_json::{Value, json};

    fn at(seconds: i64) -> DateTime<Utc> {
        DateTime::from_timestamp(seconds, 0).unwrap()
    }

    #[test]
    fn migrated_finish_uses_original_date_without_rewriting_timing_history() {
        let mut s = captured("learner-task/status", &[("completed", 100)], Some(20.));
        let before = s.status_history.clone();
        assert_eq!(task_finished_at(&s,1,at(100)).unwrap(),at(100));
        s.entities.get_mut(&1).unwrap().insert("learner-task/finished-at".into(),instant_value(at(10)));
        assert_eq!(task_finished_at(&s,1,at(100)).unwrap(),at(10));
        assert_eq!(s.status_history.len(),before.len());
        assert_eq!(s.status_history[0].at,before[0].at);
        s.entities.get_mut(&1).unwrap().insert("learner-task/finished-at".into(),instant_value(at(101)));
        assert!(task_finished_at(&s,1,at(100)).is_err());
        let mut paused = captured("learner-task/status", &[("paused",100)],Some(20.));
        paused.entities.get_mut(&1).unwrap().insert("learner-task/finished-at".into(),instant_value(at(10)));
        assert!(task_finished_at(&paused,1,at(100)).is_err());
    }

    fn captured(
        attribute: &str,
        events: &[(&str, i64)],
        checkpoint: Option<f64>,
    ) -> EntitySnapshot {
        let kind = attribute.split('/').next().unwrap();
        let prefix = attribute.replace('/', ".");
        let name = |state: &str| format!("{prefix}/{state}");
        let mut entities = serde_json::Map::new();
        let mut entity = serde_json::Map::new();
        entity.insert(format!("{kind}/id"), json!("imported"));
        entity.insert(attribute.into(), keyword(&name(events.last().unwrap().0)));
        if let Some(seconds) = checkpoint {
            entity.insert(format!("{kind}/elapsed-seconds"), json!(seconds));
        }
        entities.insert("1".into(), Value::Object(entity));
        let mut history = vec![];
        for (index, (state, seconds)) in events.iter().enumerate() {
            let ident = name(state);
            // A repeated status refers to the same enum entity.
            let enum_id = events.iter().position(|(s, _)| s == state).unwrap() + 10;
            entities.insert(enum_id.to_string(), json!({"db/ident":keyword(&ident)}));
            history.push(
                json!({"entity":1,"attribute":attribute,"value":keyword(&ident),
                "t":index+1,"at":instant_value(at(*seconds))}),
            );
        }
        EntitySnapshot::from_json(
            &json!({"entities":entities,"basis_t":events.len(),"status_history":history}),
        )
        .unwrap()
    }

    #[test]
    fn submitted_items_exclude_processing_time_and_import_checkpoints_are_not_cut_twice() {
        let active=captured("task-item/status",&[("started",10),("paused",20),("started",40)],Some(10.));
        assert_eq!(elapsed_until(&active,1,at(100),at(50)).unwrap(),20.);
        let mut completed=captured("task-item/status",&[("started",10),("paused",20),("started",40),("correct",100)],Some(20.));
        completed.entities.get_mut(&1).unwrap().insert("task-item/working-ended-at".into(),instant_value(at(50)));
        assert_eq!(elapsed(&completed,1,at(120)).unwrap(),20.);
        let imported=captured("task-item/status",&[("paused",10),("started",20),("paused",40),("started",50)],Some(38.789));
        assert!((elapsed_until(&imported,1,at(100),at(30)).unwrap()-28.789).abs()<1e-9);
        let mut imported_completed=captured("task-item/status",&[("paused",10),("started",20),("paused",40),("started",50),("correct",100)],Some(28.789));
        imported_completed.entities.get_mut(&1).unwrap().insert("task-item/working-ended-at".into(),instant_value(at(30)));
        assert_eq!(elapsed(&imported_completed,1,at(120)).unwrap(),28.789);
        assert!(elapsed_until(&active,1,at(100),at(101)).is_err());
    }

    #[test]
    fn imported_durations_use_the_latest_checkpoint_once() {
        let paused = captured("task-item/status", &[("paused", 10)], Some(38.789));
        assert_eq!(elapsed(&paused, 1, at(100)).unwrap(), 38.789);
        let resumed = captured(
            "task-item/status",
            &[("paused", 10), ("started", 20)],
            Some(38.789),
        );
        assert_eq!(elapsed(&resumed, 1, at(23)).unwrap(), 41.789);
        let paused_again = captured(
            "task-item/status",
            &[("paused", 10), ("started", 20), ("paused", 23)],
            Some(41.789),
        );
        assert_eq!(elapsed(&paused_again, 1, at(100)).unwrap(), 41.789);
        let completed = captured(
            "task-item/status",
            &[
                ("paused", 10),
                ("started", 20),
                ("paused", 23),
                ("started", 30),
                ("correct", 35),
            ],
            Some(46.789),
        );
        assert_eq!(elapsed(&completed, 1, at(100)).unwrap(), 46.789);
        for state in ["completed", "correct", "incorrect", "skipped"] {
            let terminal = captured("task-item/status", &[(state, 10)], Some(7.25));
            assert_eq!(elapsed(&terminal, 1, at(100)).unwrap(), 7.25);
        }
    }

    #[test]
    fn imported_timing_still_requires_valid_checkpoints_and_transitions() {
        for checkpoint in [None, Some(-1.0)] {
            let snapshot = captured("task-item/status", &[("paused", 10)], checkpoint);
            assert!(
                elapsed(&snapshot, 1, at(20))
                    .unwrap_err()
                    .contains("elapsed-seconds")
            );
        }
        for states in [
            vec![("paused", 10), ("correct", 20)],
            vec![("correct", 10), ("started", 20)],
        ] {
            let snapshot = captured("task-item/status", &states, Some(5.0));
            assert!(
                elapsed(&snapshot, 1, at(30))
                    .unwrap_err()
                    .contains("transition")
            );
        }
        let snapshot = captured("task-item/status", &[("paused", 10)], Some(5.0));
        assert!(
            elapsed(&snapshot, 1, at(9))
                .unwrap_err()
                .contains("predates")
        );
    }

    #[test]
    fn native_timing_remains_derived_from_full_history() {
        let snapshot = captured(
            "task-item/status",
            &[("started", 10), ("paused", 15), ("started", 20)],
            Some(100.0),
        );
        assert_eq!(elapsed(&snapshot, 1, at(23)).unwrap(), 8.0);
    }

    #[test]
    fn regrading_preserves_closed_working_intervals_and_submission_cutoff() {
        let mut native = captured(
            "task-item/status",
            &[("started",10),("paused",15),("started",20),
              ("incorrect",35),("correct",100),("incorrect",150),("correct",200)],
            Some(20.0),
        );
        assert_eq!(elapsed(&native,1,at(300)).unwrap(),20.0);
        native.entities.get_mut(&1).unwrap().insert(
            "task-item/working-ended-at".into(), instant_value(at(30)),
        );
        assert_eq!(elapsed(&native,1,at(300)).unwrap(),15.0);
        let imported = captured(
            "task-item/status", &[("incorrect",10),("correct",100)], Some(7.25),
        );
        assert_eq!(elapsed(&imported,1,at(300)).unwrap(),7.25);
        for states in [
            vec![("correct",10),("started",100)],
            vec![("incorrect",10),("paused",100)],
            vec![("skipped",10),("correct",100)],
            vec![("completed",10),("correct",100)],
        ] {
            assert!(elapsed(&captured("task-item/status",&states,Some(7.25)),1,at(300)).is_err());
        }
    }

    #[test]
    fn imported_task_start_bound_remains_its_first_recorded_status() {
        for state in ["paused", "completed", "failed"] {
            let snapshot = captured("learner-task/status", &[(state, 10)], Some(38.789));
            assert_eq!(task_started(&snapshot, 1).unwrap(), at(10));
        }
        let resumed = captured(
            "learner-task/status",
            &[("paused", 10), ("started", 20)],
            Some(38.789),
        );
        assert_eq!(task_started(&resumed, 1).unwrap(), at(10));
        let native = captured(
            "learner-task/status",
            &[("unlocked", 10), ("started", 20)],
            Some(0.0),
        );
        assert_eq!(task_started(&native, 1).unwrap(), at(20));
        let missing = captured("learner-task/status", &[("paused", 10)], None);
        assert!(task_started(&missing, 1).is_err());
    }
}
