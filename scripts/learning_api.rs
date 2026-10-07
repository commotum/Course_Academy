//! Local learner application boundary: immutable EDB reads and guarded durable writes.
mod assignment_interaction;
mod assignment_reader;
mod developer_preview;

use chrono::{DateTime, Utc};
use course_academy_engine::{
    base_xp, learning,
    schema::{self, EntitySnapshot, Record, StatusAssertion},
    timing,
};
use edb_core::{
    Cardinality, Connection, DatabaseValue, IndexOrder, IndexPrefix, Keyword, SnapshotReference,
    TimePoint, TransactionRequest, Value, postgres_config_from_env,
};
use serde_json::{Value as Json, json};
use std::{
    collections::{BTreeMap, BTreeSet},
    error::Error,
    io::{BufRead, Read, Write},
    path::PathBuf,
    time::{Duration, Instant},
};
type Result<T> = std::result::Result<T, Box<dyn Error>>;
fn kw(s: &str) -> Json {
    schema::keyword(s)
}
fn uid() -> Result<String> {
    Ok(std::fs::read_to_string("/proc/sys/kernel/random/uuid")?
        .trim()
        .into())
}
fn uuid(v: u128) -> String {
    let s = format!("{v:032x}");
    format!(
        "{}-{}-{}-{}-{}",
        &s[..8],
        &s[8..12],
        &s[12..16],
        &s[16..20],
        &s[20..]
    )
}
fn value(v: &Value) -> Result<Json> {
    Ok(match v {
        Value::String(v) | Value::Uri(v) => json!(v),
        Value::Long(v) => json!(v),
        Value::Double(v) => json!(v),
        Value::Float(v) => json!(v),
        Value::Bool(v) => json!(v),
        Value::Ref(v) => json!(v),
        Value::Keyword(v) => kw(&v.qualified_name()),
        Value::Uuid(v) => json!({"$uuid":uuid(*v)}),
        Value::Instant(v) => json!({"$instant":v}),
        _ => return Err("unsupported domain value".into()),
    })
}
fn snapshot(db: &DatabaseValue) -> Result<EntitySnapshot> {
    let mut entities = BTreeMap::<u64, Record>::new();
    let mut instants = BTreeMap::new();
    for d in db.collect_datoms(IndexOrder::Eavt)? {
        let a = db.schema().attribute(d.attribute)?;
        let name = a.ident.qualified_name();
        if name == "db/txInstant" {
            if let Value::Instant(t) = d.value {
                instants.insert(d.entity, t);
            }
            continue;
        }
        if (name.starts_with("db/") || name.starts_with("db.")) && name != "db/ident" {
            continue;
        }
        let v = value(&d.value)?;
        let e = entities.entry(d.entity).or_default();
        if a.cardinality == Cardinality::Many {
            e.entry(name)
                .or_insert(json!([]))
                .as_array_mut()
                .unwrap()
                .push(v);
        } else {
            e.insert(name, v);
        }
    }
    let mut s = EntitySnapshot::new(entities, db.basis_t())?;
    for name in ["task-item/status", "learner-task/status"] {
        let (ns, n) = name.split_once('/').unwrap();
        let a = db
            .schema()
            .resolve_ident(&Keyword::new(ns, n))
            .ok_or("missing status schema")?;
        for d in db
            .clone()
            .history()
            .collect_datoms_with_prefix(&IndexPrefix::Aevt {
                attribute: a,
                entity: None,
                value: None,
            })?
        {
            if !d.added || !s.entities.contains_key(&d.entity) {
                continue;
            }
            s.status_history.push(StatusAssertion {
                entity: d.entity,
                attribute: name.into(),
                value: value(&d.value)?,
                t: edb_core::tx_to_t(d.tx)?,
                at: json!({"$instant":instants.get(&d.tx).ok_or("missing transaction instant")?}),
            });
        }
    }
    timing::validate_history(&mut s)?;
    Ok(s)
}

/// Read the two clock histories from their attribute indexes. Maintenance can
/// consolidate history without changing logical basis, so refresh these when
/// the physical snapshot reference changes as well as after ordinary commits.
fn refresh_history(db: &DatabaseValue, s: &mut EntitySnapshot) -> Result<()> {
    let instant_attr = db
        .schema()
        .resolve_ident(&Keyword::new("db", "txInstant"))
        .ok_or("missing transaction instant schema")?;
    let mut instants = BTreeMap::new();
    let mut history = vec![];
    for name in ["task-item/status", "learner-task/status"] {
        let (ns, n) = name.split_once('/').unwrap();
        let attribute = db
            .schema()
            .resolve_ident(&Keyword::new(ns, n))
            .ok_or("missing status schema")?;
        for d in db
            .clone()
            .history()
            .collect_datoms_with_prefix(&IndexPrefix::Aevt {
                attribute,
                entity: None,
                value: None,
            })?
        {
            if !d.added || !s.entities.contains_key(&d.entity) {
                continue;
            }
            if !instants.contains_key(&d.tx) {
                let at = db
                    .collect_datoms_with_prefix(&IndexPrefix::Eavt {
                        entity: d.tx,
                        attribute: Some(instant_attr),
                        value: None,
                    })?
                    .into_iter()
                    .find_map(|d| match d.value {
                        Value::Instant(at) => Some(at),
                        _ => None,
                    })
                    .ok_or("missing transaction instant")?;
                instants.insert(d.tx, at);
            }
            history.push(StatusAssertion {
                entity: d.entity,
                attribute: name.into(),
                value: value(&d.value)?,
                t: edb_core::tx_to_t(d.tx)?,
                at: json!({"$instant":instants[&d.tx]}),
            });
        }
    }
    s.status_history = history;
    timing::validate_history(s)?;
    Ok(())
}

/// Keep one authenticated EDB connection and projection alive. The durable
/// head is synchronized before every request; cache hits never skip that check.
/// SnapshotReference catches physical/noHistory publications at a stable basis.
struct Application {
    conn: Connection,
    learner: String,
    learner_eid: u64,
    endpoint: String,
    snapshot: EntitySnapshot,
    reference: SnapshotReference,
    home_cache: Option<(Instant, Duration, Json)>,
}
impl Application {
    fn connect(database: String, learner: String, endpoint: String) -> Result<Self> {
        let started = Instant::now();
        let conn = Connection::connect_configured_with_cache_limits(
            postgres_config_from_env()?,
            database,
            2048,
            64 * 1024 * 1024,
        )?;
        let db = conn.db();
        let snapshot = snapshot(&db)?;
        let learner_eid = snapshot
            .entities
            .iter()
            .find_map(|(eid, record)| {
                (record.get("learner/id").and_then(Json::as_str) == Some(&learner)).then_some(*eid)
            })
            .ok_or("Learner not found")?;
        let reference = db.snapshot_reference()?;
        trace("startup", started);
        Ok(Self {
            conn,
            learner,
            learner_eid,
            endpoint,
            snapshot,
            reference,
            home_cache: None,
        })
    }

    fn adopt(&mut self, db: DatabaseValue) -> Result<()> {
        let reference = db.snapshot_reference()?;
        if self.reference == reference {
            return Ok(());
        }
        let started = Instant::now();
        let old = self.reference.key();
        let new = reference.key();
        let incremental = old.lineage_id() == new.lineage_id()
            && old.generation() == new.generation()
            // This is the entity-ID issuance frontier, which grows on normal
            // task/item creation. Excision is guarded by generation instead.
            && old.eidx_frontier() <= new.eidx_frontier()
            && new.basis_t() > old.basis_t()
            && new.basis_t() - old.basis_t() <= 256;
        let mut updated = false;
        if incremental {
            // Collect changed entity IDs from the exact captured log. Fetching
            // their final EAVT records handles retractions, component deletion,
            // cardinality changes and multiple updates within one suffix.
            let result = (|| -> Result<()> {
                let mut touched = BTreeSet::new();
                let mut expected = old.basis_t() + 1;
                for tx in db.log_value()?.tx_range(
                    Some(TimePoint::T(expected)),
                    Some(TimePoint::T(new.basis_t() + 1)),
                )? {
                    let tx = tx?;
                    if tx.t != expected {
                        return Err("non-contiguous captured log".into());
                    }
                    expected += 1;
                    for datom in tx.data {
                        let name = db
                            .schema()
                            .attribute(datom.attribute)?
                            .ident
                            .qualified_name();
                        if name == "db/txInstant" {
                            continue;
                        }
                        if name.starts_with("db/") || name.starts_with("db.") {
                            return Err(
                                "schema or maintenance change requires full snapshot".into()
                            );
                        }
                        touched.insert(datom.entity);
                    }
                }
                if expected != new.basis_t() + 1 {
                    return Err("incomplete captured log".into());
                }
                let mut replacements = BTreeMap::new();
                for entity in touched {
                    let mut record = Record::new();
                    for d in db.collect_datoms_with_prefix(&IndexPrefix::Eavt {
                        entity,
                        attribute: None,
                        value: None,
                    })? {
                        let a = db.schema().attribute(d.attribute)?;
                        let name = a.ident.qualified_name();
                        if (name.starts_with("db/") || name.starts_with("db."))
                            && name != "db/ident"
                        {
                            continue;
                        }
                        let v = value(&d.value)?;
                        if a.cardinality == Cardinality::Many {
                            record
                                .entry(name)
                                .or_insert(json!([]))
                                .as_array_mut()
                                .unwrap()
                                .push(v);
                        } else {
                            record.insert(name, v);
                        }
                    }
                    replacements.insert(entity, record);
                }
                self.snapshot.replace_records(replacements, db.basis_t())?;
                refresh_history(&db, &mut self.snapshot)?;
                Ok(())
            })();
            updated = result.is_ok();
            if let Err(error) = result {
                eprintln!("Learning projection full refresh: {error}");
            }
        }
        if !updated {
            self.snapshot = snapshot(&db)?;
        }
        self.reference = reference;
        self.home_cache = None;
        trace(
            if updated {
                "incremental-refresh"
            } else {
                "full-refresh"
            },
            started,
        );
        Ok(())
    }

    fn handle(&mut self, body: Json) -> Result<Json> {
        let started = Instant::now();
        self.adopt(self.conn.sync()?)?;
        trace("sync", started);
        let action = body["action"].as_str().ok_or("Action required")?;
        // Readiness decays without commits. Cache only until the next known
        // retention boundary, with a one-minute upper bound. Mutations always
        // compute eligibility against the new captured value and current time.
        if action == "home" {
            if let Some((at, lifetime, result)) = &self.home_cache {
                if at.elapsed() < *lifetime {
                    return Ok(result.clone());
                }
            }
        }
        let started = Instant::now();
        let home_lifetime = if action == "home" {
            self.home_lifetime()
        } else {
            Duration::ZERO
        };
        let result = self.process(&body)?;
        if action == "home" {
            self.home_cache = Some((started, home_lifetime, result.clone()));
        }
        trace(action, started);
        Ok(result)
    }

    fn home_lifetime(&self) -> Duration {
        let now = schema::timestamp_days(Utc::now());
        let mut seconds: f64 = 60.0;
        // A failed/malformed estimate disables caching; home() supplies its
        // ordinary validation error instead of hiding it behind stale output.
        for record in self.snapshot.entities.values() {
            if record.get("progress/learned") != Some(&json!(true)) {
                continue;
            }
            let boundary = (|| -> Option<(f64, f64)> {
                let memory = record.get("progress/memory")?.as_f64()?;
                let interval = record.get("progress/interval-days")?.as_f64()?;
                let at = schema::instant_days(record.get("progress/memory-at")?).ok()?;
                let policy = self.snapshot.eid(record.get("progress/policy")?).ok()?;
                let threshold = self
                    .snapshot
                    .entity(policy)
                    .ok()?
                    .get("policy/review-threshold")?
                    .as_f64()?;
                if !memory.is_finite()
                    || memory <= 0.0
                    || !interval.is_finite()
                    || interval <= 0.0
                    || !threshold.is_finite()
                    || threshold <= 0.0
                {
                    return None;
                }
                Some((at, at + interval * (memory / threshold).log2()))
            })();
            let Some((anchor, due)) = boundary else {
                return Duration::ZERO;
            };
            for change in [anchor, due] {
                if change >= now {
                    seconds = seconds.min(((change - now) * 86400.0 - 0.002).max(0.0));
                }
            }
        }
        Duration::from_secs_f64(seconds)
    }
}

fn trace(stage: &str, started: Instant) {
    if std::env::var_os("LEARNING_TRACE").is_some() {
        eprintln!(
            "Learning {stage}: {:.3} ms",
            started.elapsed().as_secs_f64() * 1000.
        );
    }
}
fn text(s: &EntitySnapshot, e: u64, a: &str) -> String {
    s.entities
        .get(&e)
        .and_then(|r| r.get(a))
        .and_then(Json::as_str)
        .unwrap_or("")
        .into()
}
fn number(s: &EntitySnapshot, e: u64, a: &str) -> f64 {
    s.entities
        .get(&e)
        .and_then(|r| r.get(a))
        .and_then(Json::as_f64)
        .unwrap_or(0.)
}
fn status(s: &EntitySnapshot, e: u64, a: &str) -> Result<String> {
    Ok(timing::status(s, e, a)?.rsplit('/').next().unwrap().into())
}
fn topic_lesson(s: &EntitySnapshot, topic: u64) -> Result<u64> {
    if !s.entity(topic)?.contains_key("topic/id") {
        return Err("Study now requires a topic entity ID".into());
    }
    let mut lessons = vec![];
    for (&activity, record) in &s.entities {
        if record.contains_key("activity/id")
            && status(s, activity, "activity/type")? == "lesson"
            && s.optional_ref(activity, "activity/scope")? == Some(topic)
        {
            lessons.push(activity);
        }
    }
    match lessons.as_slice() {
        [activity] => Ok(*activity),
        [] => Err("This topic does not have a lesson activity yet".into()),
        _ => Err("This topic has multiple lesson activities; its lesson is ambiguous".into()),
    }
}

fn owned(s: &EntitySnapshot, learner: u64, task: u64) -> Result<()> {
    if s.owners(task, "learner/activity")? != vec![learner] {
        return Err("Task does not belong to this learner".into());
    }
    Ok(())
}
fn items(s: &EntitySnapshot, task: u64) -> Result<Vec<u64>> {
    learning::ordered_presentations(s, task).map_err(Into::into)
}
fn task_for(s: &EntitySnapshot, learner: u64, activity: u64) -> Result<Option<u64>> {
    let mut result = None;
    for task in s.refs(learner, "learner/activity")? {
        if s.optional_ref(task, "learner-task/activity")? == Some(activity)
            && matches!(
                status(s, task, "learner-task/status")?.as_str(),
                "locked" | "unlocked" | "started" | "paused"
            )
        {
            if result.replace(task).is_some() {
                return Err("Duplicate unfinished task".into());
            }
        }
    }
    Ok(result)
}
fn completed_task_for(s: &EntitySnapshot, learner: u64, activity: u64) -> Result<Option<u64>> {
    let mut latest = None;
    for task in s.refs(learner, "learner/activity")? {
        if s.optional_ref(task, "learner-task/activity")? == Some(activity)
            && status(s, task, "learner-task/status")? == "completed"
        {
            let finished_at = timing::status_at(s, task, "learner-task/status")?;
            let entry = (finished_at, task);
            if latest.as_ref().is_none_or(|previous| entry > *previous) {
                latest = Some(entry);
            }
        }
    }
    Ok(latest.map(|(_, task)| task))
}

fn course(s: &EntitySnapshot, l: u64) -> Result<u64> {
    Ok(s.reference(l, "learner/course")?)
}
fn learner_json(s: &EntitySnapshot, l: u64) -> Json {
    json!({"id":text(s,l,"learner/id"),"name":text(s,l,"learner/name"),
        "selfDirected":s.entities.get(&l).and_then(|r|r.get("learner/self-directed")).and_then(Json::as_bool).unwrap_or(false),
        "targets":s.refs(l,"learner/targets").unwrap_or_default(),
        "queue":s.refs(l,"learner/queue").unwrap_or_default()})
}
fn course_json(s: &EntitySnapshot, l: u64) -> Result<Json> {
    let c = course(s, l)?;
    Ok(
        json!({"id":s.entity(c)?.get("course/id").and_then(|v|v.get("$uuid")),"entityId":c,"title":text(s,c,"course/title"),"groups":course_groups_json(s,c)?}),
    )
}
fn course_groups_json(s: &EntitySnapshot, course: u64) -> Result<Vec<Json>> {
    let mut groups = Vec::new();
    for group in s.owners(course, "course-group/courses")? {
        let record = s.entity(group)?;
        if let Some(id) = record.get("course-group/id").and_then(|v| v.get("$uuid")) {
            groups.push(json!({"id":id,"title":text(s,group,"course-group/title")}));
        }
    }
    groups.sort_by(|a, b| {
        a["title"]
            .as_str()
            .cmp(&b["title"].as_str())
            .then_with(|| a["id"].as_str().cmp(&b["id"].as_str()))
    });
    Ok(groups)
}
fn profile_json(s: &EntitySnapshot, l: u64) -> Result<Json> {
    let mut courses: Vec<_> = s
        .entities
        .iter()
        .filter_map(|(_, record)| {
            let id = record.get("course/id")?.get("$uuid")?.as_str()?;
            let title = record.get("course/title")?.as_str()?;
            Some(json!({"id":id,"title":title}))
        })
        .collect();
    courses.sort_by(|a, b| a["title"].as_str().cmp(&b["title"].as_str()));
    Ok(json!({"learner":learner_json(s,l),"course":course_json(s,l)?,"courses":courses}))
}
// Selecting a lesson transfers the running session in the same guarded write.
// Browser unload callbacks are best-effort and cannot release a durable task.
fn pause_other_lessons(
    s: &EntitySnapshot,
    learner: u64,
    current: Option<u64>,
    at: DateTime<Utc>,
    forms: &mut Vec<Json>,
) -> Result<()> {
    let active = timing::active_item(s, learner)?;
    let mut handled_items = BTreeSet::new();
    for task in s.refs(learner, "learner/activity")? {
        if Some(task) == current {
            handled_items.extend(s.refs(task, "learner-task/items")?);
        } else if status(s, task, "learner-task/status")? == "started" {
            let activity = s.reference(task, "learner-task/activity")?;
            if status(s, activity, "activity/type")? != "lesson" {
                return Err("Pause the current activity before starting a lesson".into());
            }
            handled_items.extend(s.refs(task, "learner-task/items")?);
            forms.extend(mutate(s, learner, "pause", &json!({"taskId":task}), at)?.0);
        }
    }
    if active.is_some_and(|item| !handled_items.contains(&item)) {
        return Err("The active presentation does not belong to a running task".into());
    }
    Ok(())
}
fn home(s: &EntitySnapshot, l: u64) -> Result<Json> {
    let c = course(s, l)?;
    let self_directed = learner_json(s, l)["selfDirected"] == true;
    let candidates = learning::study_candidates(s, l, c, Utc::now())?;
    let mut activities = vec![];
    for candidate in candidates {
        let a = candidate.activity;
        let task = task_for(s, l, a)?;
        let state = match task {
            Some(task) => status(s, task, "learner-task/status")?,
            None if self_directed => "selected".into(),
            None => continue,
        };
        if state == "locked" && !self_directed {
            continue;
        }
        let expected = number(s, a, "activity/expected-seconds");
        let expected = if expected > 0.0 {
            expected
        } else {
            s.refs(a, "activity/steps")?
                .into_iter()
                .map(|step| number(s, step, "step/expected-seconds"))
                .sum()
        };
        let progress =
            if let Some(task) = task.filter(|_| matches!(state.as_str(), "started" | "paused")) {
                lesson_progress(s, &learning::lesson_steps(s, a)?, &items(s, task)?)?
            } else {
                Json::Null
            };
        activities.push(json!({"activityId":a,"title":text(s,a,"activity/title"),"type":"lesson","taskId":task,"status":state,
            "priority":candidate.priority,"reason":candidate.reason,"targetCount":candidate.target_count,
            "targetTopics":candidate.target_topics,"progress":progress,"expectedSeconds":if expected>0.0{Some(expected)}else{None}}));
        if activities.len() == 5 {
            break;
        }
    }
    let mut waiting = vec![];
    for t in s.refs(l, "learner/activity")? {
        if status(s, t, "learner-task/status")? != "paused" {
            continue;
        }
        let a = s.reference(t, "learner-task/activity")?;
        if status(s, a, "activity/type")? != "lesson" {
            continue;
        }
        let chain = items(s, t)?;
        if !chain
            .iter()
            .any(|i| s.entities[i].contains_key("task-item/deferred-step"))
        {
            continue;
        }
        let p = practice_state(s, a, &chain)?;
        if p.next.is_none()
            && p.shortage.is_none()
            && !p.deferred.is_empty()
            && !p.failed
            && !activities.iter().any(|entry| entry["taskId"] == t)
        {
            waiting.push(json!({"taskId":t,"title":text(s,a,"activity/title"),"pendingCount":p.deferred.len(),"canResumePractice":learning::deferred_resume_step(s,a,&chain)?.is_some()}));
        }
    }
    Ok(
        json!({"basis":s.basis_t,"learner":learner_json(s,l),"course":course_json(s,l)?,"activities":activities,"waitingActivities":waiting,"queueDescription":"Engine recommendations interleave eligible lessons across course modules; self-directed study uses your selected topic queue.","practiceNotice":"Each skill needs two correct answers in a row, with up to five questions. If fresh questions run out, you can continue to the next skill and return to unfinished practice later."}),
    )
}

/// Prepare selected and recommended work without recording a presentation or clock.
/// Self-directed selections get a prepared locked task, preserving engine eligibility.
/// The caller journals this transaction and submits it with an exact basis guard.
fn queue_forms(s: &EntitySnapshot, l: u64, at: DateTime<Utc>) -> Result<Vec<Json>> {
    let c = course(s, l)?;
    let mut plan = BTreeMap::new();
    for candidate in learning::queue_candidates(s, l, c, at)? {
        plan.insert(candidate.activity, (candidate, false));
    }
    for candidate in learning::engine_candidates(s, l, c, at)? {
        plan.insert(candidate.activity, (candidate, true));
    }
    let mut pending = BTreeMap::new();
    let mut terminal_assignments = BTreeSet::new();
    for task in s.refs(l, "learner/activity")? {
        let activity = s.reference(task, "learner-task/activity")?;
        match status(s, task, "learner-task/status")?.as_str() {
            "locked" | "unlocked" | "started" | "paused" => {
                if pending.insert(activity, task).is_some() {
                    return Err("Duplicate unfinished task".into());
                }
            }
            "completed" | "failed" => {
                terminal_assignments.insert(activity);
            }
            _ => return Err("Unknown task status".into()),
        }
    }
    let mut forms = vec![];
    let mut eligible = BTreeSet::new();
    for (_, (candidate, engine_eligible)) in plan {
        let activity = candidate.activity;
        eligible.insert(activity);
        let priority = candidate.priority;
        if !priority.is_finite() {
            return Err("Task priority must be finite".into());
        }
        if let Some(&task) = pending.get(&activity) {
            let state = status(s, task, "learner-task/status")?;
            if engine_eligible && state == "locked" {
                forms.push(cas(
                    s,
                    task,
                    "learner-task/status",
                    "learner-task.status/unlocked",
                )?);
            } else if !engine_eligible && state == "unlocked" {
                forms.push(cas(
                    s,
                    task,
                    "learner-task/status",
                    "learner-task.status/locked",
                )?);
            }
            if s.entity(task)?
                .get("learner-task/priority")
                .and_then(Json::as_f64)
                != Some(priority)
            {
                forms.push(add(json!(task), "learner-task/priority", json!(priority)));
            }
        } else {
            let temp = format!("queue-task-{activity}");
            forms.push(json!({"db/id":temp,"learner-task/id":{"$uuid":uid()?},"learner-task/activity":activity,
                "learner-task/status":kw(if engine_eligible { "learner-task.status/unlocked" } else { "learner-task.status/locked" }),"learner-task/priority":priority,"db/ensure":kw("learner-task/validate")}));
            forms.push(add(json!(l), "learner/activity", json!(temp)));
        }
    }
    for (&activity, &task) in &pending {
        let state = status(s, task, "learner-task/status")?;
        if eligible.contains(&activity) || matches!(state.as_str(), "started" | "paused") {
            continue;
        }
        if state == "unlocked" {
            forms.push(cas(
                s,
                task,
                "learner-task/status",
                "learner-task.status/locked",
            )?);
        }
        if number(s, task, "learner-task/priority") != 0.0 {
            forms.push(add(json!(task), "learner-task/priority", json!(0.0)));
        }
    }
    // Assigned activities get a record immediately. Unsupported players remain
    // locked; their mapped topics can still prioritize runnable preparation lessons.
    for activity in s.refs(l, "learner/assignments")? {
        if !s.entity(activity)?.contains_key("activity/id")
            || status(s, activity, "activity/type")? != "assignment"
        {
            return Err("Learner assignments must reference assignment activities".into());
        }
        if pending.contains_key(&activity)
            || terminal_assignments.contains(&activity)
            || eligible.contains(&activity)
        {
            continue;
        }
        let temp = format!("queue-assignment-{activity}");
        forms.push(json!({"db/id":temp,"learner-task/id":{"$uuid":uid()?},"learner-task/activity":activity,
            "learner-task/status":kw("learner-task.status/locked"),"learner-task/priority":0.0,"db/ensure":kw("learner-task/validate")}));
        forms.push(add(json!(l), "learner/activity", json!(temp)));
    }
    Ok(forms)
}
fn authored_step(
    steps: &[learning::LessonStep],
    content: u64,
) -> Option<(usize, &learning::LessonStep)> {
    steps.iter().enumerate().find(|(_, entry)| {
        entry.content == content
            || entry.example == Some(content)
            || entry.questions.contains(&content)
    })
}

/// Presentations within an adaptive skill share one authored step. Study and
/// the player report the same position rather than counting practice questions.
fn lesson_progress(
    s: &EntitySnapshot,
    steps: &[learning::LessonStep],
    chain: &[u64],
) -> Result<Json> {
    let step_number = if let Some(&item) = chain.last() {
        authored_step(steps, s.reference(item, "task-item/content")?)
            .map(|(index, _)| index + 1)
            .unwrap_or(1)
    } else {
        1
    };
    Ok(
        json!({"stepNumber":step_number,"totalSteps":steps.len(),"presented":chain.len(),
        "answered":chain.iter().filter(|i|matches!(status(s,**i,"task-item/status").as_deref(),Ok("correct"|"incorrect"))).count()}),
    )
}

// Use the displayed content's source ID, never an authored placement or topic ID.
fn content_math_academy_id(record: &Record) -> Option<String> {
    record
        .get(if record.contains_key("tutorial/id") {
            "tutorial/math-academy-id"
        } else {
            "question/math-academy-id"
        })
        .and_then(Json::as_i64)
        .map(|id| id.to_string())
}

fn task_step_json(
    s: &EntitySnapshot,
    steps: &[learning::LessonStep],
    i: u64,
    at: DateTime<Utc>,
) -> Result<Json> {
    let content = s.reference(i, "task-item/content")?;
    let e = s.entity(content)?;
    let state = status(s, i, "task-item/status")?;
    let terminal = timing::terminal(&format!("task-item.status/{state}"));
    let tutorial = e.contains_key("tutorial/id");
    let example = s.is_example(content);
    let reveal = example || terminal;
    let authored = authored_step(&steps, content);
    let title = if tutorial {
        text(s, content, "tutorial/title")
    } else if let Some((_, entry)) = authored.filter(|(_, entry)| entry.kind == "knowledge-point") {
        text(s, entry.content, "knowledge-point/title")
    } else if example {
        "Worked example".into()
    } else {
        "Practice".into()
    };
    let mut fields = vec![];
    for f in s.refs(content, "question/answer-fields")? {
        let kind = status(s, f, "answer-field/type")?;
        let mut choices = vec![];
        if kind != "blank" {
            for ch in s.refs(f, "answer-field/choices")? {
                choices.push(json!({"id":ch,"type":status(s,ch,"answer/type")?,"value":text(s,ch,"answer/value")}));
            }
        }
        let mut field = json!({"id":f,"key":text(s,f,"answer-field/key"),"type":kind,"presentation":text(s,f,"answer-field/presentation"),"choices":choices});
        if kind == "blank" {
            field["answerType"] = json!(
                s.optional_ref(f, "answer-field/correct")?
                    .map(|correct| status(s, correct, "answer/type"))
                    .transpose()?
            );
        }
        if terminal {
            let selected = s.refs(i, "task-item/responses")?.into_iter().find(|ch| {
                s.refs(f, "answer-field/choices")
                    .unwrap_or_default()
                    .contains(ch)
            });
            if let Some(ch) = selected {
                field["response"] = json!({"id":ch,"choiceId":ch,"type":status(s,ch,"answer/type")?,"value":text(s,ch,"answer/value"),"feedback":text(s,ch,"answer/feedback")});
            }
            if let Some(correct) = s.optional_ref(f, "answer-field/correct")? {
                field["correctAnswer"] = json!({"id":correct,"type":status(s,correct,"answer/type")?,"value":text(s,correct,"answer/value")});
            }
        }
        fields.push(field);
    }
    let mut step = json!({"itemId":i,"contentId":content,"kind":if tutorial{"tutorial"}else if example{"example"}else{"question"},"title":title,"markdown":text(s,content,if tutorial{"tutorial/content"}else{"question/problem"}),"fields":fields,"status":state,"canContinue":tutorial||example||terminal,"requiresCalculator":e.get("question/requires-calculator"),"elapsedSeconds":timing::elapsed(s,i,at)?});
    step["stepId"] = json!(authored.map(|(_, entry)| entry.step.to_string()));
    step["mathAcademyId"] = json!(content_math_academy_id(e));
    if reveal {
        step["solution"] = json!(text(s, content, "question/worked-solution"));
    }
    Ok(step)
}

fn practice_state(s: &EntitySnapshot, a: u64, chain: &[u64]) -> Result<learning::Position> {
    let instruction = chain
        .last()
        .map(|i| -> Result<bool> {
            let content = s.reference(*i, "task-item/content")?;
            Ok(
                (s.entity(content)?.contains_key("tutorial/id") || s.is_example(content))
                    && status(s, *i, "task-item/status")? == "started",
            )
        })
        .transpose()?
        .unwrap_or(false);
    learning::continuation_state(s, a, chain, instruction, false).map_err(Into::into)
}

fn task_json(s: &EntitySnapshot, l: u64, t: u64) -> Result<Json> {
    task_json_view(s, l, t, true)
}

// Full history is loaded when entering/resuming a lesson. Answer and continue
// responses send only the current presentation to keep advancing inexpensive.
fn task_json_view(s: &EntitySnapshot, l: u64, t: u64, include_history: bool) -> Result<Json> {
    owned(s, l, t)?;
    let a = s.reference(t, "learner-task/activity")?;
    let task_state = status(s, t, "learner-task/status")?;
    let chain = items(s, t)?;
    let at = Utc::now();
    let steps = learning::lesson_steps(s, a)?;
    let progress = lesson_progress(s, &steps, &chain)?;
    let step = chain
        .last()
        .map(|&i| task_step_json(s, &steps, i, at))
        .transpose()?
        .unwrap_or(Json::Null);
    let history = if include_history {
        chain
            .iter()
            .take(chain.len().saturating_sub(1))
            .enumerate()
            .map(|(index, &i)| {
                let step = task_step_json(s, &steps, i, at)?;
                let number = authored_step(&steps, s.reference(i, "task-item/content")?)
                    .map(|(index, _)| index + 1)
                    .unwrap_or(1);
                Ok(json!({"order":index + 1,"number":number,"total":steps.len(),"step":step}))
            })
            .collect::<Result<Vec<Json>>>()?
    } else {
        vec![]
    };
    let mut view = json!({"basis":s.basis_t,"taskId":t,"activityId":a,"learner":learner_json(s,l),"course":course_json(s,l)?,"title":text(s,a,"activity/title"),"status":task_state,"xp":number(s,t,"learner-task/xp-earned"),"xpBase":number(s,t,"learner-task/xp-base"),"elapsedSeconds":if matches!(task_state.as_str(),"unlocked"|"locked"){number(s,t,"learner-task/elapsed-seconds")}else{timing::task_elapsed(s,t,at)?},"step":step,"progress":progress});
    let practice = practice_state(s, a, &chain);
    if practice.is_err()
        && chain
            .iter()
            .any(|i| s.entities[i].contains_key("task-item/deferred-step"))
    {
        return Err(practice.err().unwrap());
    }
    if let Ok(practice) = practice {
        let awaiting = practice.next.is_none()
            && practice.shortage.is_none()
            && !practice.deferred.is_empty()
            && !practice.failed;
        view["awaitingQuestions"] = json!(awaiting);
        view["canResumePractice"] =
            json!(awaiting && learning::deferred_resume_step(s, a, &chain)?.is_some());
        view["deferredSteps"] = json!(
            practice
                .deferred
                .iter()
                .map(|id| {
                    let st = steps.iter().find(|st| st.step == *id).unwrap();
                    json!({"stepId":id,"title":text(s,st.content,"knowledge-point/title")})
                })
                .collect::<Vec<_>>()
        );
        if let Some(id) = practice.shortage {
            view["step"]["practiceShortage"] = json!({"stepId":id,"title":text(s,steps.iter().find(|st| st.step == id).unwrap().content,"knowledge-point/title")});
        }
    }
    if include_history {
        view["history"] = json!(history);
    }
    Ok(view)
}

fn needs_queue_refresh(action: &str, task_state: &str) -> bool {
    // Accuracy updates and intermediate presentations do not change learned
    // prerequisites. Replan when finishing an attempt can unlock new work.
    action == "continue" && matches!(task_state, "completed" | "failed")
}
fn add(e: Json, a: &str, v: Json) -> Json {
    json!([kw("db/add"), e, kw(a), v])
}
fn cas(s: &EntitySnapshot, e: u64, a: &str, new: &str) -> Result<Json> {
    Ok(json!([kw("db/cas"), e, kw(a), s.reference(e, a)?, kw(new)]))
}
fn transition(
    s: &EntitySnapshot,
    t: u64,
    i: u64,
    state: &str,
    at: DateTime<Utc>,
    forms: &mut Vec<Json>,
) -> Result<()> {
    let elapsed = timing::elapsed(s, i, at)?;
    let total = items(s, t)?
        .into_iter()
        .map(|other| {
            if other == i {
                elapsed
            } else {
                number(s, other, "task-item/elapsed-seconds")
            }
        })
        .sum::<f64>();
    forms.push(cas(
        s,
        i,
        "task-item/status",
        &format!("task-item.status/{state}"),
    )?);
    forms.push(add(json!(i), "task-item/elapsed-seconds", json!(elapsed)));
    forms.push(add(json!(t), "learner-task/elapsed-seconds", json!(total)));
    Ok(())
}
fn append_item(t: Json, previous: Option<u64>, content: u64, forms: &mut Vec<Json>) -> Result<()> {
    let id = uid()?;
    forms.push(json!({"db/id":"new-item","task-item/id":{"$uuid":id},"task-item/content":content,"task-item/status":kw("task-item.status/started"),"task-item/elapsed-seconds":0.0,"db/ensure":kw("task-item/validate")}));
    forms.push(add(t, "learner-task/items", json!("new-item")));
    if let Some(p) = previous {
        forms.push(add(json!(p), "task-item/next", json!("new-item")));
    }
    Ok(())
}
fn required(body: &Json, k: &str) -> Result<u64> {
    body[k]
        .as_u64()
        .ok_or_else(|| format!("{k} is required").into())
}
fn mutate(
    s: &EntitySnapshot,
    l: u64,
    action: &str,
    body: &Json,
    at: DateTime<Utc>,
) -> Result<(Vec<Json>, Json)> {
    if action.starts_with("assignment-")
        || (action == "pause"
            && body["taskId"].as_u64().is_some_and(|task| {
                s.optional_ref(task, "learner-task/activity")
                    .ok()
                    .flatten()
                    .is_some_and(|activity| {
                        matches!(
                            status(s, activity, "activity/type").as_deref(),
                            Ok("assignment")
                        )
                    })
            }))
    {
        return assignment_interaction::mutate(s, l, action, body, at);
    }
    let mut forms = vec![];
    if action == "profile-settings" {
        let requested = body["courseId"].as_str().ok_or("courseId is required")?;
        let selected = s
            .entities
            .iter()
            .find_map(|(id, record)| {
                (record
                    .get("course/id")
                    .and_then(|v| v.get("$uuid"))
                    .and_then(Json::as_str)
                    == Some(requested))
                .then_some(*id)
            })
            .ok_or("Selected course does not exist")?;
        let directed = body["selfDirected"]
            .as_bool()
            .ok_or("selfDirected must be a boolean")?;
        let old_directed = learner_json(s, l)["selfDirected"] == true;
        if course(s, l)? != selected || old_directed != directed {
            // Pause and change settings in the same transaction so no activity
            // continues timing against the previous study selection.
            for task in s.refs(l, "learner/activity")? {
                if status(s, task, "learner-task/status")? == "started" {
                    forms.extend(mutate(s, l, "pause", &json!({"taskId":task}), at)?.0);
                }
            }
            forms.push(json!([kw("db/add"), l, kw("learner/course"), selected]));
            forms.push(json!([
                kw("db/add"),
                l,
                kw("learner/self-directed"),
                directed
            ]));
        }
        return Ok((forms, json!({"profile":true})));
    }
    if action == "queue" {
        return Ok((queue_forms(s, l, at)?, json!({"queue":true})));
    }
    if action == "queue-topic" {
        let topic = required(body, "topicId")?;
        if !s.entity(topic)?.contains_key("topic/id") {
            return Err("A queue selection must reference a topic".into());
        }
        let selected = body["selected"]
            .as_bool()
            .ok_or("selected must be a boolean")?;
        let mut queue: BTreeSet<_> = s.refs(l, "learner/queue")?.into_iter().collect();
        let changed = if selected {
            queue.insert(topic)
        } else {
            queue.remove(&topic)
        };
        if changed {
            forms.push(json!([
                kw(if selected { "db/add" } else { "db/retract" }),
                l,
                kw("learner/queue"),
                topic
            ]));
        }
        let mut prospective = s.clone();
        prospective
            .entities
            .get_mut(&l)
            .unwrap()
            .insert("learner/queue".into(), json!(queue));
        // Selection and preparation commit atomically. Exact retries replay this
        // transaction; they do not create a second pending attempt or unlock it.
        forms.extend(queue_forms(&prospective, l, at)?);
        return Ok((forms, json!({"queueTopic":true})));
    }
    if action == "target" {
        if s.entity(l)?
            .get("learner/self-directed")
            .and_then(Json::as_bool)
            != Some(true)
        {
            return Err("Self-directed study is not enabled for this learner".into());
        }
        let topic = required(body, "topicId")?;
        if !s.entity(topic)?.contains_key("topic/id") {
            return Err("A study target must reference a topic".into());
        }
        let selected = body["selected"]
            .as_bool()
            .ok_or("selected must be a boolean")?;
        let mut targets: BTreeSet<_> = s.refs(l, "learner/targets")?.into_iter().collect();
        let changed = if selected {
            targets.insert(topic)
        } else {
            targets.remove(&topic)
        };
        if changed {
            forms.push(json!([
                kw(if selected { "db/add" } else { "db/retract" }),
                l,
                kw("learner/targets"),
                topic
            ]));
        }
        let mut prospective = s.clone();
        prospective
            .entities
            .get_mut(&l)
            .unwrap()
            .insert("learner/targets".into(), json!(targets));
        forms.extend(queue_forms(&prospective, l, at)?);
        return Ok((forms, json!({"targets":true})));
    }
    if action == "study-topic" {
        let topic = required(body, "topicId")?;
        let activity = topic_lesson(s, topic)?;
        // A finished lesson is available for review through its saved attempt.
        // Keep unfinished attempts resumable and never regrade completed work.
        if task_for(s, l, activity)?.is_none() {
            if let Some(task) = completed_task_for(s, l, activity)? {
                return Ok((forms, json!({"taskId":task})));
            }
        }
        // Explicit study uses the manual selection rules without persisting a
        // queue membership, preference change, or engine unlock. Starting and
        // resuming still use the same guarded, replayable lesson lifecycle.
        let mut selection = s.clone();
        let learner = selection.entities.get_mut(&l).ok_or("Learner not found")?;
        learner.insert("learner/queue".into(), json!([topic]));
        learner.insert("learner/self-directed".into(), json!(true));
        return mutate(&selection, l, "start", &json!({"activityId":activity}), at);
    }
    if action == "start" {
        let a = required(body, "activityId")?;
        let existing = task_for(s, l, a)?;
        if let Some(task) = existing {
            match status(s, task, "learner-task/status")?.as_str() {
                "paused" => return mutate(s, l, "resume", &json!({"taskId":task}), at),
                "started" => {
                    pause_other_lessons(s, l, Some(task), at, &mut forms)?;
                    return Ok((forms, json!({"taskId":task})));
                }
                _ => {}
            }
        }
        if !learning::study_candidates(s, l, course(s, l)?, at)?
            .iter()
            .any(|p| p.activity == a)
        {
            return Err("Activity is not eligible or its content is unavailable".into());
        }
        if let Some(t) = existing {
            let state = status(s, t, "learner-task/status")?;
            if matches!(state.as_str(), "locked" | "unlocked") {
                pause_other_lessons(s, l, Some(t), at, &mut forms)?;
                if !items(s, t)?.is_empty() {
                    return Err("An unstarted task cannot already have presentations".into());
                }
                forms.push(cas(
                    s,
                    t,
                    "learner-task/status",
                    "learner-task.status/started",
                )?);
                if s.entity(t)?.get("learner-task/xp-base").is_none() {
                    forms.push(add(
                        json!(t),
                        "learner-task/xp-base",
                        json!(base_xp::activity_base(s, a)?),
                    ));
                }
                let content =
                    learning::first_content(s, a, l)?.ok_or("Lesson has no available content")?;
                append_item(json!(t), None, content, &mut forms)?;
            }
            return Ok((forms, json!({"taskId":t})));
        }
        pause_other_lessons(s, l, None, at, &mut forms)?;
        let id = uid()?;
        let xp_base = base_xp::activity_base(s, a)?;
        forms.push(json!({"db/id":"new-task","learner-task/id":{"$uuid":id},"learner-task/activity":a,"learner-task/status":kw("learner-task.status/started"),"learner-task/priority":1.0,"learner-task/elapsed-seconds":0.0,"learner-task/xp-base":xp_base,"learner-task/xp-earned":0,"db/ensure":kw("learner-task/validate")}));
        forms.push(add(json!(l), "learner/activity", json!("new-task")));
        let content = learning::first_content(s, a, l)?.ok_or("Lesson has no available content")?;
        append_item(json!("new-task"), None, content, &mut forms)?;
        return Ok((forms, json!({"taskUuid":id})));
    }
    let t = required(body, "taskId")?;
    owned(s, l, t)?;
    let a = s.reference(t, "learner-task/activity")?;
    if status(s, a, "activity/type")? == "assignment" {
        return Err("Use the assignment question controls for this task".into());
    }
    let state = status(s, t, "learner-task/status")?;
    let chain = items(s, t)?;
    let i = *chain.last().ok_or("Task has no presentation")?;
    let item_state = status(s, i, "task-item/status")?;
    let content = s.reference(i, "task-item/content")?;
    let terminal = timing::terminal(&format!("task-item.status/{item_state}"));
    if action == "resume" && state == "paused" {
        let p = learning::continuation_state(s, a, &chain, false, false)?;
        if p.next.is_none() && p.shortage.is_none() && !p.deferred.is_empty() {
            let Some(step) = learning::deferred_resume_step(s, a, &chain)? else {
                return Ok((forms, json!({"taskId":t})));
            };
            pause_other_lessons(s, l, Some(t), at, &mut forms)?;
            let example = learning::lesson_steps(s, a)?
                .into_iter()
                .find(|st| st.step == step)
                .unwrap()
                .example
                .unwrap();
            forms.push(cas(
                s,
                t,
                "learner-task/status",
                "learner-task.status/started",
            )?);
            append_item(json!(t), Some(i), example, &mut forms)?;
            forms.push(add(
                json!("new-item"),
                "task-item/resumed-step",
                json!(step),
            ));
            return Ok((forms, json!({"taskId":t})));
        }
    }
    if matches!(action, "pause" | "resume") {
        let target = if action == "pause" {
            "paused"
        } else {
            "started"
        };
        if action == "resume" && matches!(state.as_str(), "started" | "paused") {
            pause_other_lessons(s, l, Some(t), at, &mut forms)?;
        }
        if state == target || matches!(state.as_str(), "completed" | "failed") {
            return Ok((forms, json!({"taskId":t})));
        }
        if !matches!(state.as_str(), "started" | "paused") {
            return Err("Task cannot change running state".into());
        }
        if !terminal {
            transition(s, t, i, target, at, &mut forms)?;
        }
        forms.push(cas(
            s,
            t,
            "learner-task/status",
            &format!("learner-task.status/{target}"),
        )?);
    } else {
        let requested = required(body, "itemId")?;
        if requested != i {
            if chain.contains(&requested) && action == "continue" {
                return Ok((forms, json!({"taskId":t})));
            }
            return Err("This presentation is no longer current".into());
        }
        if matches!(state.as_str(), "completed" | "failed") {
            return Ok((forms, json!({"taskId":t})));
        }
        if state != "started" {
            return Err("Resume the lesson before continuing".into());
        }
        let e = s.entity(content)?;
        let instruction = e.contains_key("tutorial/id") || s.is_example(content);
        if action == "answer" {
            if instruction {
                return Err("This step does not accept an answer".into());
            }
            if terminal {
                return Ok((forms, json!({"taskId":t})));
            }
            let responses = body["responses"]
                .as_array()
                .ok_or("responses must be a list")?;
            let fields = s.refs(content, "question/answer-fields")?;
            let mut submitted = BTreeMap::new();
            let mut response_refs = vec![];
            for r in responses {
                let f = required(r, "fieldId")?;
                if !fields.contains(&f) || submitted.contains_key(&f) {
                    return Err("Each answer field must appear exactly once".into());
                }
                let kind = status(s, f, "answer-field/type")?;
                let choices = s.refs(f, "answer-field/choices")?;
                let (v, response) = if kind == "blank" {
                    let v = r["value"]
                        .as_str()
                        .ok_or("Blank response must contain a string value")?;
                    if v.len() > 16000 {
                        return Err("Response is too long".into());
                    }
                    let existing = choices
                        .into_iter()
                        .find(|ch| text(s, *ch, "answer/value") == v);
                    let response = if let Some(ch) = existing {
                        json!(ch)
                    } else {
                        let key = format!("response-{f}");
                        let correct = s.reference(f, "answer-field/correct")?;
                        forms.push(json!({"db/id":key,"answer/id":{"$uuid":uid()?},"answer/type":s.reference(correct,"answer/type")?,"answer/value":v,"db/ensure":kw("answer/validate")}));
                        forms.push(add(json!(f), "answer-field/choices", json!(key)));
                        json!(key)
                    };
                    (v.to_owned(), response)
                } else {
                    let ch = required(r, "choiceId")?;
                    if !choices.contains(&ch) {
                        return Err("Choice does not belong to this field".into());
                    }
                    (ch.to_string(), json!(ch))
                };
                submitted.insert(f, v);
                response_refs.push(response);
            }
            if submitted.len() != fields.len() {
                return Err("Answer every current question field before submitting".into());
            }
            let correct = learning::grade(s, content, &submitted)?;
            for response in response_refs {
                forms.push(add(json!(i), "task-item/responses", response));
            }
            transition(
                s,
                t,
                i,
                if correct { "correct" } else { "incorrect" },
                at,
                &mut forms,
            )?;
            // Imported questions have no measured speed baseline. Persist the
            // observed duration and outcome; leave calculated performance absent.
            forms.extend(learning::credit(
                s,
                l,
                a,
                Some(content),
                correct,
                false,
                &format!("item-{i}"),
                at,
            )?);
        } else if action == "continue" {
            if !instruction && !terminal {
                return Err("Answer every current question before continuing".into());
            }
            if !terminal {
                transition(s, t, i, "completed", at, &mut forms)?;
            }
            let mut p = learning::continuation_state(s, a, &chain, !terminal, false)?;
            if let Some(stage) = p.shortage {
                forms.push(add(json!(i), "task-item/deferred-step", json!(stage)));
                p = learning::continuation_state(s, a, &chain, !terminal, true)?;
            }
            let next = p.next;
            let passed = p.passed;
            let pending = !p.deferred.is_empty() && !p.failed;
            let xp = if next.is_none() && !pending {
                learning::continuation(
                    s,
                    a,
                    &chain,
                    !terminal,
                    number(s, t, "learner-task/xp-base") as i64,
                )?
                .2
            } else {
                0
            };
            if let Some(next) = next {
                append_item(json!(t), Some(i), next, &mut forms)?;
            } else {
                forms.push(cas(
                    s,
                    t,
                    "learner-task/status",
                    if pending {
                        "learner-task.status/paused"
                    } else if passed {
                        "learner-task.status/completed"
                    } else {
                        "learner-task.status/failed"
                    },
                )?);
                forms.push(add(json!(t), "learner-task/xp-earned", json!(xp)));
                if !pending {
                    forms.extend(learning::credit(
                        s,
                        l,
                        a,
                        None,
                        passed,
                        true,
                        &format!("task-{t}"),
                        at,
                    )?);
                }
            }
        } else {
            return Err("Unknown action".into());
        }
    }
    Ok((forms, json!({"taskId":t})))
}
impl Application {
    fn process(&mut self, body: &Json) -> Result<Json> {
        let action = body["action"].as_str().ok_or("Action required")?;
        let s = &self.snapshot;
        let learner = &self.learner;
        if s.entities
            .get(&self.learner_eid)
            .and_then(|r| r.get("learner/id"))
            .and_then(Json::as_str)
            != Some(learner)
        {
            self.learner_eid = s
                .entities
                .iter()
                .find_map(|(eid, record)| {
                    (record.get("learner/id").and_then(Json::as_str) == Some(learner))
                        .then_some(*eid)
                })
                .ok_or("Learner not found")?;
        }
        let l = self.learner_eid;
        // Developer inspection must return before request journaling or any
        // learner mutation. These functions only receive an immutable snapshot.
        match action {
            "preview-home" => return developer_preview::home(s, l),
            "preview" => return developer_preview::preview(s, l, body),
            "preview-answer" => return developer_preview::check_answer(s, l, body),
            "preview-active-tasks" => return developer_preview::active_tasks(s, l),
            _ => {}
        }
        if action == "export-test-snapshot" {
            let path = std::env::var("LEARNING_SNAPSHOT_PATH")?;
            std::fs::write(
                path,
                serde_json::to_vec(
                    &json!({"basis_t":s.basis_t,"entities":s.entities,"status_history":s.status_history}),
                )?,
            )?;
            return Ok(json!({"exported":true}));
        }
        if action == "home" {
            return home(&s, l);
        }
        if action == "profile" {
            return profile_json(s, l);
        }
        if action == "assignments" {
            return assignment_reader::list(&s, l);
        }
        if action == "assignment" {
            return assignment_reader::detail_mode(
                &s,
                l,
                body["assignmentId"]
                    .as_str()
                    .ok_or("Assignment ID required")?,
                body["preview"] == true,
            );
        }
        if action == "task" {
            let task = required(body, "taskId")?;
            owned(s, l, task)?;
            let activity = s.reference(task, "learner-task/activity")?;
            if status(s, activity, "activity/type")? == "assignment" {
                let id = assignment_reader::identity(s, activity, "activity/id")?;
                let mut detail = assignment_reader::detail(s, l, &id)?;
                detail["type"] = json!("assignment");
                detail["assignmentId"] = json!(id);
                return Ok(detail);
            }
            return task_json(&s, l, task);
        }
        let request = body["requestId"]
            .as_str()
            .filter(|s| {
                s.len() >= 8
                    && s.len() <= 100
                    && s.chars().all(|c| c.is_ascii_alphanumeric() || c == '-')
            })
            .ok_or("A stable requestId is required")?;
        let journal = PathBuf::from(std::env::var("LEARNING_REQUEST_DIR")?)
            .join(format!("{learner}-{request}.json"));
        let saved: Json = if journal.exists() {
            let saved: Json = serde_json::from_slice(&std::fs::read(&journal)?)?;
            if saved["input"] != *body {
                return Err("requestId was already used for a different request".into());
            }
            saved
        } else {
            let at = Utc::now();
            let planning = Instant::now();
            let (forms, result) = mutate(&s, l, action, &body, at)?;
            trace("plan", planning);
            let saved = json!({"input":body,"edn":schema::edn(&json!(forms))?,"basis":s.basis_t,"at":at.timestamp_millis(),"result":result,"empty":forms.is_empty()});
            std::fs::create_dir_all(journal.parent().unwrap())?;
            let staging = journal.with_extension("tmp");
            let mut file = std::fs::File::create(&staging)?;
            file.write_all(&serde_json::to_vec(&saved)?)?;
            file.sync_all()?;
            std::fs::rename(staging, &journal)?;
            std::fs::File::open(journal.parent().unwrap())?.sync_all()?;
            saved
        };
        if saved["empty"] != json!(true) {
            let tx = TransactionRequest::from_edn(
                format!("learning-{learner}-{request}"),
                saved["edn"].as_str().unwrap(),
            )?
            .comparing_basis(saved["basis"].as_u64().unwrap())
            .with_tx_instant(saved["at"].as_i64().unwrap());
            let writing = Instant::now();
            let committed =
                self.conn
                    .transact_socket(&self.endpoint, tx, Duration::from_secs(30))?;
            trace("durable-write-and-open-receipt", writing);
            let observing = Instant::now();
            let db = self
                .conn
                .sync_to(committed.basis_t, Duration::from_secs(10))?;
            trace("observe-commit", observing);
            self.adopt(db)?;
        }
        let s = &self.snapshot;
        let result = &saved["result"];
        if action == "profile-settings" {
            return profile_json(s, l);
        }
        if let Some(id) = result["assignmentId"].as_str() {
            return assignment_reader::detail(s, l, id);
        }
        if matches!(action, "target" | "queue-topic") {
            return Ok(json!({"basis":s.basis_t,"learner":learner_json(s,l)}));
        }
        if action == "queue" {
            return home(s, l);
        }
        let t = if let Some(t) = result["taskId"].as_u64() {
            t
        } else {
            let id = result["taskUuid"].as_str().ok_or("Missing task result")?;
            s.entities
                .iter()
                .find_map(|(e, r)| {
                    (r.get("learner-task/id") == Some(&json!({"$uuid":id}))).then_some(*e)
                })
                .ok_or("Committed task unavailable")?
        };
        // Task evidence commits first. Intermediate steps return immediately;
        // completion refreshes availability with a separate replayable request.
        let queue_error =
            if needs_queue_refresh(action, &status(&self.snapshot, t, "learner-task/status")?) {
                let request = format!("queue-after-{l}-{}", self.snapshot.basis_t);
                self.process(&json!({"action":"queue","requestId":request}))
                    .err()
            } else {
                None
            };
        let mut view = task_json_view(
            &self.snapshot,
            l,
            t,
            matches!(action, "start" | "study-topic" | "resume"),
        )?;
        if let Some(error) = queue_error {
            eprintln!("Queue refresh postponed after saved task: {error}");
            view["queueNotice"] =
                json!("Your work is saved. Refresh the home page to update available activities.");
        }
        Ok(view)
    }
}

fn envelope(result: Result<Json>) -> Json {
    match result {
        Ok(data) => json!({"ok":true,"data":data}),
        Err(error) => {
            eprintln!("Learning API: {error}");
            let mut code = if error.to_string() == "Resume the lesson before continuing" {
                "lesson-paused"
            } else {
                "validation"
            };
            if let Some(error) = error.downcast_ref::<edb_core::SemanticError>() {
                let native = error
                    .details
                    .get("remote_code")
                    .map(String::as_str)
                    .unwrap_or(error.code);
                if native == "postgres/stale-basis" {
                    code = "basis-conflict";
                } else if matches!(
                    error.category,
                    edb_core::ErrorCategory::UnknownOutcome
                        | edb_core::ErrorCategory::Unavailable
                        | edb_core::ErrorCategory::Interrupted
                ) {
                    code = "unavailable";
                }
            }
            json!({"ok":false,"error":error.to_string(),"code":code})
        }
    }
}
fn run() -> Result<bool> {
    let mut args = std::env::args().skip(1);
    let database = args.next().ok_or("Database required")?;
    let learner = args.next().ok_or("Learner required")?;
    let endpoint = args.next().ok_or("Writer endpoint required")?;
    let serve = args.next().as_deref() == Some("--serve");
    let mut app = Application::connect(database, learner, endpoint)?;
    if serve {
        let stdin = std::io::stdin();
        let stdout = std::io::stdout();
        let mut output = stdout.lock();
        for line in stdin.lock().lines() {
            let line = line?;
            let result = serde_json::from_str(&line)
                .map_err(Into::into)
                .and_then(|body| app.handle(body));
            serde_json::to_writer(&mut output, &envelope(result))?;
            output.write_all(b"\n")?;
            output.flush()?;
        }
        Ok(true)
    } else {
        let mut input = String::new();
        std::io::stdin().read_to_string(&mut input)?;
        let result = serde_json::from_str(&input)
            .map_err(Into::into)
            .and_then(|body| app.handle(body));
        let output = envelope(result);
        println!("{output}");
        Ok(output["ok"] == json!(true))
    }
}
fn main() {
    match run() {
        Ok(true) => {}
        Ok(false) => std::process::exit(1),
        Err(error) => {
            println!("{}", envelope(Err(error)));
            std::process::exit(1);
        }
    }
}

#[cfg(test)]
mod lesson_progress_tests {
    use super::*;

    #[test]
    fn intermediate_steps_do_not_replan_the_entire_study_queue() {
        for action in ["answer", "start", "study-topic", "pause", "resume"] {
            for state in ["started", "paused", "completed", "failed"] {
                assert!(!needs_queue_refresh(action, state));
            }
        }
        assert!(!needs_queue_refresh("continue", "started"));
        assert!(needs_queue_refresh("continue", "completed"));
        assert!(needs_queue_refresh("continue", "failed"));
    }

    #[test]
    fn paused_action_rejection_is_explicit_and_distinct_from_other_validation_errors() {
        assert_eq!(
            envelope(Err("Resume the lesson before continuing".into()))["code"],
            "lesson-paused"
        );
        assert_eq!(
            envelope(Err("Task does not belong to this learner".into()))["code"],
            "validation"
        );
    }

    #[test]
    fn source_id_preserves_digits_and_never_falls_back_to_topic_or_placement() {
        let tutorial =
            json!({"tutorial/id":"intro","tutorial/math-academy-id":9007199254740993_i64});
        assert_eq!(
            content_math_academy_id(tutorial.as_object().unwrap()).as_deref(),
            Some("9007199254740993")
        );
        let question = json!({"question/id":"q","question/math-academy-id":456});
        assert_eq!(
            content_math_academy_id(question.as_object().unwrap()).as_deref(),
            Some("456")
        );
        let missing =
            json!({"question/id":"q","step/math-academy-id":789,"topic/math-academy-id":1116});
        assert!(content_math_academy_id(missing.as_object().unwrap()).is_none());
    }

    #[test]
    fn saved_position_uses_authored_steps_even_with_multiple_practice_presentations() {
        let steps = vec![
            learning::LessonStep {
                step: 10,
                content: 100,
                kind: "tutorial".into(),
                example: None,
                questions: vec![],
            },
            learning::LessonStep {
                step: 20,
                content: 200,
                kind: "knowledge-point".into(),
                example: Some(201),
                questions: vec![202, 203],
            },
            learning::LessonStep {
                step: 30,
                content: 300,
                kind: "tutorial".into(),
                example: None,
                questions: vec![],
            },
            learning::LessonStep {
                step: 40,
                content: 400,
                kind: "tutorial".into(),
                example: None,
                questions: vec![],
            },
        ];
        let records: BTreeMap<_, _> = [
            (100, json!({})),
            (200, json!({})),
            (201, json!({})),
            (202, json!({})),
            (203, json!({})),
            (300, json!({})),
            (400, json!({})),
            (900, json!({"db/ident":kw("task-item.status/correct")})),
            (901, json!({"db/ident":kw("task-item.status/paused")})),
            (1, json!({"task-item/content":100,"task-item/status":900})),
            (2, json!({"task-item/content":201,"task-item/status":900})),
            (3, json!({"task-item/content":202,"task-item/status":900})),
            (4, json!({"task-item/content":203,"task-item/status":900})),
            (5, json!({"task-item/content":300,"task-item/status":901})),
        ]
        .into_iter()
        .map(|(id, record)| (id, record.as_object().unwrap().clone()))
        .collect();
        let s = EntitySnapshot::new(records, 42).unwrap();
        let before = s.entities.clone();
        for chain in [&[1, 2][..], &[1, 2, 3][..], &[1, 2, 3, 4][..]] {
            let progress = lesson_progress(&s, &steps, chain).unwrap();
            assert_eq!(progress["stepNumber"], 2);
            assert_eq!(progress["totalSteps"], 4);
        }
        let halfway = lesson_progress(&s, &steps, &[1, 2, 3, 4, 5]).unwrap();
        assert_eq!(
            halfway,
            json!({"stepNumber":3,"totalSteps":4,"presented":5,"answered":4})
        );
        assert_eq!(lesson_progress(&s, &steps, &[]).unwrap()["stepNumber"], 1);
        assert_eq!(lesson_progress(&s, &steps, &[1]).unwrap()["stepNumber"], 1);
        assert_eq!(authored_step(&steps, 200).unwrap().0, 1);
        assert_eq!(s.entities, before);
        assert_eq!(s.basis_t, 42);
    }
}

#[cfg(test)]
mod study_queue_tests {
    use super::*;

    fn fixture() -> EntitySnapshot {
        let mut records = BTreeMap::new();
        for (eid, record) in [
            (
                1,
                json!({"learner/id":"queue-test","learner/course":2,"learner/self-directed":true,"learner/queue":[6],"learner/activity":[80,81]}),
            ),
            (
                2,
                json!({"course/id":{"$uuid":"00000000-0000-0000-0000-000000000002"},"course/title":"Test course","course/units":[3]}),
            ),
            (3, json!({"unit/modules":[4]})),
            (4, json!({"module/topics":[5]})),
            (5, json!({"topic/id":"course-topic"})),
            (6, json!({"topic/id":"queued-topic"})),
            (
                7,
                json!({"topic/id":"unlearned-prerequisite","topic/next":[6]}),
            ),
            (
                50,
                json!({"activity/id":"course-lesson","activity/type":"activity.type/lesson","activity/scope":5,"activity/title":"Course lesson","activity/expected-seconds":720.0,"activity/steps":[60],"activity/first-step":60}),
            ),
            (
                51,
                json!({"activity/id":"queued-lesson","activity/type":"activity.type/lesson","activity/scope":6,"activity/title":"Queued lesson","activity/expected-seconds":720.0,"activity/steps":[61],"activity/first-step":61}),
            ),
            (60, json!({"step/content":70})),
            (61, json!({"step/content":71})),
            (
                70,
                json!({"question/id":"course-question","question/problem":"Find x.","question/answer-fields":[90]}),
            ),
            (
                71,
                json!({"question/id":"queued-question","question/problem":"Find x.","question/answer-fields":[90]}),
            ),
            (
                80,
                json!({"learner-task/activity":50,"learner-task/status":"learner-task.status/unlocked","learner-task/priority":1.0}),
            ),
            (
                81,
                json!({"learner-task/activity":51,"learner-task/status":"learner-task.status/locked","learner-task/priority":1.0}),
            ),
            (
                90,
                json!({"answer-field/key":"x","answer-field/type":"answer-field.type/blank","answer-field/choices":[91],"answer-field/correct":91}),
            ),
            (
                91,
                json!({"answer/type":"answer.type/math","answer/value":"2"}),
            ),
        ] {
            records.insert(eid, record.as_object().unwrap().clone());
        }
        for (index, ident) in [
            "activity.type/lesson",
            "answer-field.type/blank",
            "answer.type/math",
            "learner-task.status/unlocked",
            "learner-task.status/locked",
            "learner-task.status/started",
            "task-item.status/started",
            "learner-task.status/paused",
            "task-item.status/correct",
        ]
        .iter()
        .enumerate()
        {
            records.insert(
                1000 + index as u64,
                json!({"db/ident":kw(ident)}).as_object().unwrap().clone(),
            );
        }
        EntitySnapshot::new(records, 42).unwrap()
    }

    #[test]
    fn restored_task_history_uses_saved_presentations_and_reveals_only_answered_keys() {
        let mut s = fixture();
        s.entities.get_mut(&81).unwrap().insert(
            "learner-task/status".into(),
            json!("learner-task.status/paused"),
        );
        s.entities
            .get_mut(&81)
            .unwrap()
            .insert("learner-task/items".into(), json!([96, 95]));
        s.entities.get_mut(&71).unwrap().insert(
            "question/worked-solution".into(),
            json!("The worked solution."),
        );
        s.entities
            .get_mut(&90)
            .unwrap()
            .insert("answer-field/presentation".into(), json!("checkbox"));
        s.entities.insert(95, json!({"task-item/content":71,"task-item/status":"task-item.status/correct","task-item/next":96,"task-item/responses":[91]}).as_object().unwrap().clone());
        s.entities.insert(
            96,
            json!({"task-item/content":71,"task-item/status":"task-item.status/paused"})
                .as_object()
                .unwrap()
                .clone(),
        );
        s.entities.insert(
            1100,
            json!({"db/ident":kw("task-item.status/paused")})
                .as_object()
                .unwrap()
                .clone(),
        );
        s = EntitySnapshot::new(s.entities, 42).unwrap();
        for (t, entity, attribute, value) in [
            (1, 81, "learner-task/status", "learner-task.status/started"),
            (2, 95, "task-item/status", "task-item.status/started"),
            (3, 95, "task-item/status", "task-item.status/correct"),
            (4, 96, "task-item/status", "task-item.status/started"),
            (5, 96, "task-item/status", "task-item.status/paused"),
            (5, 81, "learner-task/status", "learner-task.status/paused"),
        ] {
            s.status_history.push(StatusAssertion {
                entity,
                attribute: attribute.into(),
                value: kw(value),
                t,
                at: json!({"$instant":t * 1000}),
            });
        }
        let before = s.entities.clone();
        let view = task_json(&s, 1, 81).unwrap();
        assert_eq!(view["history"].as_array().unwrap().len(), 1);
        let entry = &view["history"][0];
        assert_eq!(entry["order"], 1);
        assert_eq!(entry["number"], 1);
        assert_eq!(entry["step"]["itemId"], 95);
        assert_eq!(entry["step"]["solution"], "The worked solution.");
        assert_eq!(entry["step"]["fields"][0]["presentation"], "checkbox");
        assert_eq!(entry["step"]["fields"][0]["response"]["value"], "2");
        assert_eq!(entry["step"]["fields"][0]["correctAnswer"]["value"], "2");
        assert_eq!(view["step"]["itemId"], 96);
        assert!(view["step"].get("solution").is_none());
        assert!(view["step"]["fields"][0].get("correctAnswer").is_none());
        assert!(
            task_json_view(&s, 1, 81, false)
                .unwrap()
                .get("history")
                .is_none()
        );
        assert!(task_json(&s, 999, 81).is_err());
        assert_eq!(s.entities, before);
    }

    #[test]
    fn exhausted_practice_defers_without_failure_and_can_be_resumed_when_supply_arrives() {
        let mut s = fixture();
        s.entities.insert(
            1101,
            json!({"db/ident":kw("task-item.status/completed")})
                .as_object()
                .unwrap()
                .clone(),
        );
        s.entities.insert(
            1102,
            json!({"db/ident":kw("task-item.status/paused")})
                .as_object()
                .unwrap()
                .clone(),
        );
        for (id, record) in [
            (61, json!({"step/content":72,"step/next":62})),
            (62, json!({"step/content":74})),
            (
                72,
                json!({"knowledge-point/id":"kp","knowledge-point/title":"Unfinished skill","knowledge-point/canonical-example":73,"knowledge-point/questions":[71]}),
            ),
            (
                73,
                json!({"question/id":"example","question/problem":"Example","question/worked-solution":"Solution"}),
            ),
            (
                74,
                json!({"tutorial/id":"later","tutorial/content":"Continue reading"}),
            ),
            (
                95,
                json!({"task-item/content":73,"task-item/status":"task-item.status/completed","task-item/next":96,"task-item/elapsed-seconds":1.0}),
            ),
            (
                96,
                json!({"task-item/content":71,"task-item/status":"task-item.status/correct","task-item/elapsed-seconds":1.0}),
            ),
        ] {
            s.entities.insert(id, record.as_object().unwrap().clone());
        }
        s.entities
            .get_mut(&51)
            .unwrap()
            .insert("activity/steps".into(), json!([61, 62]));
        s.entities.get_mut(&81).unwrap().extend(json!({"learner-task/status":"learner-task.status/started","learner-task/items":[95,96],"learner-task/xp-base":10,"learner-task/elapsed-seconds":2.0}).as_object().unwrap().clone());
        s = EntitySnapshot::new(s.entities.clone(), s.basis_t).unwrap();
        let at = DateTime::from_timestamp(10, 0).unwrap();
        let (forms, _) = mutate(&s, 1, "continue", &json!({"taskId":81,"itemId":96}), at).unwrap();
        assert!(forms.contains(&add(json!(96), "task-item/deferred-step", json!(61))));
        assert!(
            forms
                .iter()
                .any(|f| f.get("task-item/content") == Some(&json!(74)))
        );
        assert!(
            !schema::edn(&json!(forms))
                .unwrap()
                .contains("learner-task.status/failed")
        );
        s.entities.get_mut(&96).unwrap().extend(
            json!({"task-item/deferred-step":61,"task-item/next":97})
                .as_object()
                .unwrap()
                .clone(),
        );
        s.entities.insert(97,json!({"task-item/content":74,"task-item/status":"task-item.status/completed","task-item/elapsed-seconds":1.0}).as_object().unwrap().clone());
        s.entities
            .get_mut(&81)
            .unwrap()
            .insert("learner-task/items".into(), json!([95, 96, 97]));
        // A paused tutorial after a deferred skill is readable, not complete.
        s.entities
            .get_mut(&97)
            .unwrap()
            .insert("task-item/status".into(), json!("task-item.status/paused"));
        let paused = practice_state(&s, 51, &items(&s, 81).unwrap()).unwrap();
        assert_eq!(paused.next, Some(74));
        assert_eq!(paused.deferred, vec![61]);
        s.entities.get_mut(&97).unwrap().insert(
            "task-item/status".into(),
            json!("task-item.status/completed"),
        );
        let (forms, _) = mutate(&s, 1, "continue", &json!({"taskId":81,"itemId":97}), at).unwrap();
        assert!(
            forms.contains(
                &cas(&s, 81, "learner-task/status", "learner-task.status/paused").unwrap()
            )
        );
        assert!(forms.contains(&add(json!(81), "learner-task/xp-earned", json!(0))));
        assert!(!schema::edn(&json!(forms)).unwrap().contains(":progress/"));
        s.entities.get_mut(&81).unwrap().insert(
            "learner-task/status".into(),
            json!("learner-task.status/paused"),
        );
        assert!(
            mutate(&s, 1, "resume", &json!({"taskId":81}), at)
                .unwrap()
                .0
                .is_empty()
        );
        s.entities.insert(75,json!({"question/id":"new-question","question/problem":"New practice","question/answer-fields":[90]}).as_object().unwrap().clone());
        s.entities
            .get_mut(&72)
            .unwrap()
            .insert("knowledge-point/questions".into(), json!([71, 75]));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/queue".into(), json!([]));
        let dashboard = home(&s, 1).unwrap();
        assert!(dashboard["activities"].as_array().unwrap().is_empty());
        assert_eq!(dashboard["waitingActivities"][0]["taskId"], 81);
        assert_eq!(dashboard["waitingActivities"][0]["canResumePractice"], true);
        let (forms, _) = mutate(&s, 1, "resume", &json!({"taskId":81}), at).unwrap();
        assert!(forms.contains(&add(json!("new-item"), "task-item/resumed-step", json!(61))));
        assert!(
            forms
                .iter()
                .any(|f| f.get("task-item/content") == Some(&json!(73)))
        );
        assert!(
            !forms
                .iter()
                .any(|f| f.get("task-item/content") == Some(&json!(74)))
        );
    }

    #[test]
    fn study_now_starts_a_locked_topic_without_changing_queue_course_or_mode() {
        let mut s = fixture();
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(false));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/queue".into(), json!([]));
        let before = s.entities.clone();
        let at = Utc::now();
        assert!(mutate(&s, 1, "start", &json!({"activityId":51}), at).is_err());
        let (forms, result) = mutate(&s, 1, "study-topic", &json!({"topicId":6}), at).unwrap();
        assert_eq!(result["taskId"], 81);
        assert!(
            forms.contains(
                &cas(&s, 81, "learner-task/status", "learner-task.status/started").unwrap()
            )
        );
        let edn = schema::edn(&json!(forms)).unwrap();
        for untouched in [
            "learner/queue",
            "learner/self-directed",
            "learner/course",
            "learner-task.status/unlocked",
        ] {
            assert!(!edn.contains(untouched));
        }
        assert_eq!(s.entities, before);
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([]));
        let (forms, result) = mutate(&s, 1, "study-topic", &json!({"topicId":6}), at).unwrap();
        assert!(result["taskUuid"].is_string());
        let task = forms
            .iter()
            .find(|f| f.get("learner-task/activity") == Some(&json!(51)))
            .unwrap();
        assert_eq!(
            task["learner-task/status"],
            kw("learner-task.status/started")
        );
    }

    #[test]
    fn study_now_resumes_the_same_attempt_and_preserves_its_presentations() {
        let mut s = fixture();
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/queue".into(), json!([]));
        s.entities.get_mut(&81).unwrap().insert(
            "learner-task/status".into(),
            json!("learner-task.status/paused"),
        );
        s.entities
            .get_mut(&81)
            .unwrap()
            .insert("learner-task/items".into(), json!([95]));
        s.entities.insert(
            95,
            json!({"task-item/content":71,"task-item/status":"task-item.status/correct"})
                .as_object()
                .unwrap()
                .clone(),
        );
        let before = s.entities.clone();
        let at = Utc::now();
        let (forms, result) = mutate(&s, 1, "study-topic", &json!({"topicId":6}), at).unwrap();
        assert_eq!(result["taskId"], 81);
        assert_eq!(
            forms,
            vec![cas(&s, 81, "learner-task/status", "learner-task.status/started").unwrap()]
        );
        assert_eq!(s.entities, before);
        s.entities.get_mut(&80).unwrap().insert(
            "learner-task/status".into(),
            json!("learner-task.status/started"),
        );
        s.entities
            .get_mut(&80)
            .unwrap()
            .insert("learner-task/items".into(), json!([96]));
        s.entities.insert(
            96,
            json!({"task-item/content":70,"task-item/status":1008,"task-item/responses":[91]})
                .as_object()
                .unwrap()
                .clone(),
        );
        let (forms, result) = mutate(&s, 1, "study-topic", &json!({"topicId":6}), at).unwrap();
        assert_eq!(result["taskId"], 81);
        assert_eq!(
            forms,
            vec![
                cas(&s, 80, "learner-task/status", "learner-task.status/paused").unwrap(),
                cas(&s, 81, "learner-task/status", "learner-task.status/started").unwrap(),
            ]
        );
        s.entities.get_mut(&80).unwrap().insert(
            "learner-task/status".into(),
            json!("learner-task.status/unlocked"),
        );
        s.entities.get_mut(&81).unwrap().insert(
            "learner-task/status".into(),
            json!("learner-task.status/started"),
        );
        let (forms, result) = mutate(&s, 1, "study-topic", &json!({"topicId":6}), at).unwrap();
        assert_eq!(result["taskId"], 81);
        assert!(forms.is_empty());
    }

    #[test]
    fn switching_lessons_pauses_the_previous_clock_and_preserves_answers() {
        let mut s = fixture();
        s.entities.insert(
            1101,
            json!({"db/ident":kw("task-item.status/paused")})
                .as_object()
                .unwrap()
                .clone(),
        );
        s.entities.get_mut(&80).unwrap().extend(json!({"learner-task/status":1005,"learner-task/items":[95,96],"learner-task/xp-earned":0}).as_object().unwrap().clone());
        s.entities.insert(95, json!({"task-item/content":70,"task-item/status":1008,"task-item/responses":[91],"task-item/elapsed-seconds":7.0,"task-item/next":96}).as_object().unwrap().clone());
        s.entities.insert(
            96,
            json!({"task-item/content":70,"task-item/status":1006,"task-item/elapsed-seconds":0.0})
                .as_object()
                .unwrap()
                .clone(),
        );
        s = EntitySnapshot::new(s.entities, 42).unwrap();
        let at = Utc::now();
        s.status_history.push(StatusAssertion {
            entity: 96,
            attribute: "task-item/status".into(),
            value: kw("task-item.status/started"),
            t: 1,
            at: json!({"$instant":at.timestamp_millis()-20_000}),
        });
        let before = s.entities.clone();
        for action in ["start", "study-topic"] {
            let body = if action == "start" {
                json!({"activityId":51})
            } else {
                json!({"topicId":6})
            };
            let (forms, result) = mutate(&s, 1, action, &body, at).unwrap();
            assert_eq!(result["taskId"], 81);
            assert!(
                forms
                    .contains(&cas(&s, 96, "task-item/status", "task-item.status/paused").unwrap())
            );
            assert!(forms.contains(&add(json!(96), "task-item/elapsed-seconds", json!(20.0))));
            assert!(forms.contains(&add(json!(80), "learner-task/elapsed-seconds", json!(27.0))));
            assert!(forms.contains(
                &cas(&s, 80, "learner-task/status", "learner-task.status/paused").unwrap()
            ));
            assert!(forms.contains(
                &cas(&s, 81, "learner-task/status", "learner-task.status/started").unwrap()
            ));
            let edn = schema::edn(&json!(forms)).unwrap();
            for untouched in [
                "task-item/responses",
                "learner-task/xp-earned",
                "learner-task.status/completed",
                "learner/queue",
            ] {
                assert!(!edn.contains(untouched));
            }
        }
        // Starting a newly-created attempt uses the same transfer.
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([80]));
        let (forms, result) = mutate(&s, 1, "start", &json!({"activityId":51}), at).unwrap();
        assert!(result["taskUuid"].is_string());
        assert!(
            forms.contains(
                &cas(&s, 80, "learner-task/status", "learner-task.status/paused").unwrap()
            )
        );
        assert_eq!(s.entity(95).unwrap(), before.get(&95).unwrap());
        assert_eq!(s.entity(96).unwrap(), before.get(&96).unwrap());
        assert!(mutate(&s, 1, "start", &json!({"activityId":999}), at).is_err());
        assert_eq!(s.entity(80).unwrap(), before.get(&80).unwrap());
    }

    #[test]
    fn study_now_reopens_the_latest_completed_attempt_without_new_learning_or_credit() {
        let mut s = fixture();
        s.entities.get_mut(&81).unwrap().insert(
            "learner-task/status".into(),
            json!("learner-task.status/completed"),
        );
        s.entities
            .get_mut(&81)
            .unwrap()
            .insert("learner-task/xp-earned".into(), json!(7));
        s.entities.insert(83, s.entity(81).unwrap().clone());
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([80, 83, 81]));
        s.entities.insert(
            1100,
            json!({"db/ident":kw("learner-task.status/completed")})
                .as_object()
                .unwrap()
                .clone(),
        );
        s = EntitySnapshot::new(s.entities, 42).unwrap();
        for (task, t) in [(83, 1), (81, 2)] {
            s.status_history.push(StatusAssertion {
                entity: task,
                attribute: "learner-task/status".into(),
                value: kw("learner-task.status/completed"),
                t,
                at: json!({"$instant":t * 1000}),
            });
        }
        let before = s.entities.clone();
        for _ in 0..2 {
            let (forms, result) =
                mutate(&s, 1, "study-topic", &json!({"topicId":6}), Utc::now()).unwrap();
            assert!(forms.is_empty());
            assert_eq!(result["taskId"], 81);
        }
        assert_eq!(s.entities, before);
        // An unfinished attempt takes precedence over the completed history.
        s.entities.insert(85, json!({"learner-task/activity":51,"learner-task/status":"learner-task.status/paused","learner-task/items":[95]}).as_object().unwrap().clone());
        s.entities.insert(
            95,
            json!({"task-item/content":71,"task-item/status":"task-item.status/correct"})
                .as_object()
                .unwrap()
                .clone(),
        );
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([80, 81, 83, 85]));
        let (forms, result) =
            mutate(&s, 1, "study-topic", &json!({"topicId":6}), Utc::now()).unwrap();
        assert_eq!(result["taskId"], 85);
        assert_eq!(
            forms,
            vec![cas(&s, 85, "learner-task/status", "learner-task.status/started").unwrap()]
        );
    }

    #[test]
    fn study_now_resolves_only_unambiguous_topics_with_available_content() {
        let mut s = fixture();
        let at = Utc::now();
        assert!(mutate(&s, 1, "study-topic", &json!({"topicId":2}), at).is_err());
        assert!(mutate(&s, 1, "study-topic", &json!({"topicId":7}), at).is_err());
        assert!(mutate(&s, 1, "study-topic", &json!({"topicId":999}), at).is_err());
        s.entities
            .get_mut(&90)
            .unwrap()
            .remove("answer-field/correct");
        assert!(mutate(&s, 1, "study-topic", &json!({"topicId":6}), at).is_err());
        s.entities.insert(52, s.entity(51).unwrap().clone());
        assert!(
            topic_lesson(&s, 6)
                .unwrap_err()
                .to_string()
                .contains("ambiguous")
        );
    }

    #[test]
    fn study_display_materialization_start_and_preview_share_queue_selection() {
        let mut s = fixture();
        let at = Utc::now();
        let before = s.entities.clone();
        let view = home(&s, 1).unwrap();
        assert_eq!(view["learner"]["queue"], json!([6]));
        assert_eq!(view["activities"].as_array().unwrap().len(), 1);
        assert_eq!(view["activities"][0]["activityId"], 51);
        assert_eq!(
            developer_preview::home(&s, 1).unwrap()["activities"][0]["activityId"],
            51
        );
        assert_eq!(view["activities"][0]["status"], "locked");
        assert!(queue_forms(&s, 1, at).unwrap().is_empty());
        assert!(mutate(&s, 1, "start", &json!({"activityId":50}), at).is_err());
        let (forms, started) = mutate(&s, 1, "start", &json!({"activityId":51}), at).unwrap();
        assert_eq!(started["taskId"], 81);
        assert!(
            forms.contains(
                &cas(&s, 81, "learner-task/status", "learner-task.status/started").unwrap()
            )
        );
        assert!(
            !schema::edn(&json!(forms))
                .unwrap()
                .contains("learner-task.status/unlocked")
        );
        assert_eq!(s.entities, before); // Fixture tests never commit transactions.
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(false));
        assert_eq!(home(&s, 1).unwrap()["activities"][0]["activityId"], 50);
        assert!(mutate(&s, 1, "start", &json!({"activityId":51}), at).is_err());
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(true));
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/queue".into(), json!([]));
        assert!(
            home(&s, 1).unwrap()["activities"]
                .as_array()
                .unwrap()
                .is_empty()
        );
    }

    #[test]
    fn self_selected_lessons_prepare_locked_and_start_directly() {
        let mut s = fixture();
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([]));
        let at = Utc::now();
        let view = home(&s, 1).unwrap();
        assert_eq!(view["activities"][0]["activityId"], 51);
        assert!(view["activities"][0]["taskId"].is_null());
        assert_eq!(view["activities"][0]["status"], "selected");
        let prepared = queue_forms(&s, 1, at).unwrap();
        let task = prepared
            .iter()
            .find(|f| f.get("learner-task/activity") == Some(&json!(51)))
            .unwrap();
        assert_eq!(
            task["learner-task/status"],
            kw("learner-task.status/locked")
        );
        assert!(
            !prepared
                .iter()
                .any(|f| f.get("learner-task/activity") == Some(&json!(51))
                    && f.get("learner-task/status") == Some(&kw("learner-task.status/unlocked")))
        );
        let (forms, _) = mutate(&s, 1, "start", &json!({"activityId":51}), at).unwrap();
        let task = forms
            .iter()
            .find(|f| f.get("learner-task/activity") == Some(&json!(51)))
            .unwrap();
        assert_eq!(
            task["learner-task/status"],
            kw("learner-task.status/started")
        );
        assert!(
            !schema::edn(&json!(forms))
                .unwrap()
                .contains("learner-task.status/unlocked")
        );
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/self-directed".into(), json!(false));
        assert!(mutate(&s, 1, "start", &json!({"activityId":51}), at).is_err());
        assert!(
            queue_forms(&s, 1, at)
                .unwrap()
                .iter()
                .any(|f| f.get("learner-task/status") == Some(&kw("learner-task.status/unlocked")))
        );
    }

    #[test]
    fn adding_a_queue_topic_prepares_its_activity_even_when_self_directed_is_off() {
        let mut s = fixture();
        for (key, value) in [
            ("learner/activity", json!([])),
            ("learner/queue", json!([])),
            ("learner/self-directed", json!(false)),
        ] {
            s.entities.get_mut(&1).unwrap().insert(key.into(), value);
        }
        let before = s.entities.clone();
        let at = Utc::now();
        let (forms, _) = mutate(
            &s,
            1,
            "queue-topic",
            &json!({"topicId":6,"selected":true}),
            at,
        )
        .unwrap();
        assert!(forms.contains(&add(json!(1), "learner/queue", json!(6))));
        let prepared = forms
            .iter()
            .find(|f| f.get("learner-task/activity") == Some(&json!(51)))
            .unwrap();
        assert_eq!(
            prepared["learner-task/status"],
            kw("learner-task.status/locked")
        );
        assert!(!forms.iter().any(|f| f.get("task-item/content").is_some()));
        assert_eq!(s.entities, before);
        assert!(
            mutate(
                &s,
                1,
                "queue-topic",
                &json!({"topicId":51,"selected":true}),
                at
            )
            .is_err()
        );
    }

    #[test]
    fn engine_unlocking_and_manual_selection_prepare_independently_without_duplicates() {
        let mut s = fixture();
        let at = Utc::now();
        assert!(queue_forms(&s, 1, at).unwrap().is_empty());
        // An engine-eligible queued lesson can unlock through the engine itself.
        s.entities
            .get_mut(&4)
            .unwrap()
            .insert("module/topics".into(), json!([5, 6]));
        s.entities.insert(
            23,
            json!({"progress/topic":7,"progress/repetitions":1.0})
                .as_object()
                .unwrap()
                .clone(),
        );
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/knowledge-profile".into(), json!([23]));
        assert_eq!(
            queue_forms(&s, 1, at).unwrap(),
            vec![
                cas(
                    &s,
                    81,
                    "learner-task/status",
                    "learner-task.status/unlocked"
                )
                .unwrap()
            ]
        );
        s.entities.get_mut(&81).unwrap().insert(
            "learner-task/status".into(),
            kw("learner-task.status/unlocked"),
        );
        assert!(queue_forms(&s, 1, at).unwrap().is_empty());
        // Explicit selection alone must not maintain a false engine unlock.
        s.entities
            .get_mut(&23)
            .unwrap()
            .insert("progress/repetitions".into(), json!(0.0));
        assert_eq!(
            queue_forms(&s, 1, at).unwrap(),
            vec![cas(&s, 81, "learner-task/status", "learner-task.status/locked").unwrap()]
        );
    }
}

#[cfg(test)]
mod integration {
    use super::*;

    fn commit(
        conn: &Connection,
        endpoint: &str,
        s: &EntitySnapshot,
        forms: Vec<Json>,
        key: &str,
        at: DateTime<Utc>,
    ) -> Result<EntitySnapshot> {
        let tx = TransactionRequest::from_edn(key, schema::edn(&json!(forms))?.as_str())?
            .comparing_basis(s.basis_t)
            .with_tx_instant(at.timestamp_millis());
        let first = conn.transact_socket(endpoint, tx.clone(), Duration::from_secs(30))?;
        let second = conn.transact_socket(endpoint, tx, Duration::from_secs(30))?;
        assert_eq!(
            first.basis_t, second.basis_t,
            "exact retries must replay one commit"
        );
        assert!(second.replayed);
        snapshot(&conn.sync_to(first.basis_t, Duration::from_secs(10))?)
    }

    #[test]
    #[ignore = "requires the local durable writer; creates then removes a temporary integration learner"]
    fn durable_lesson_lifecycle() -> Result<()> {
        let database = std::env::var("EDB_DATABASE").unwrap_or("course-academy-v2".into());
        let endpoint = std::env::var("EDB_ENDPOINT")
            .unwrap_or("/tmp/course-academy-edb-v2/writer.sock".into());
        let conn = Connection::connect_configured(postgres_config_from_env()?, database, 256)?;
        let source = snapshot(&conn.db())?;
        let original = source
            .entities
            .iter()
            .find_map(|(e, r)| {
                (r.get("learner/id").and_then(Json::as_str)
                    == Some("59d5cf13-351c-4114-be19-4c3bb64ee051"))
                .then_some(*e)
            })
            .ok_or("original learner unavailable")?;
        let id = format!("integration-{}", uid()?);
        let c = course(&source, original)?;
        let mut forms = vec![];
        let mut progress = vec![];
        for (index, p) in source
            .refs(original, "learner/knowledge-profile")?
            .iter()
            .enumerate()
        {
            let name = format!("test-progress-{index}");
            progress.push(json!(name));
            forms.push(json!({"db/id":name,"progress/id":uid()?,"progress/topic":source.reference(*p,"progress/topic")?,"progress/repetitions":number(&source,*p,"progress/repetitions")}));
        }
        forms.push(json!({"db/id":"test-learner","learner/id":id,"learner/name":"Temporary learner API integration test","learner/course":c,"learner/self-directed":false,"learner/knowledge-profile":progress,"db/ensure":kw("learner/validate")}));
        let mut s = commit(
            &conn,
            &endpoint,
            &source,
            forms,
            &format!("{id}-setup"),
            Utc::now(),
        )?;
        let l = s
            .entities
            .iter()
            .find_map(|(e, r)| (r.get("learner/id") == Some(&json!(id))).then_some(*e))
            .unwrap();
        eprintln!("Temporary integration learner: {id}");
        let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| -> Result<()> {
            let at = Utc::now();
            let activity = learning::study_candidates(&s, l, c, at)?
                .first()
                .ok_or("no eligible test lesson")?
                .activity;
            let forms = queue_forms(&s, l, at)?;
            assert!(
                !forms.is_empty(),
                "available work needs pending task records"
            );
            s = commit(&conn, &endpoint, &s, forms, &format!("{id}-queue"), at)?;
            let t = task_for(&s, l, activity)?.ok_or("queue did not create task")?;
            assert_eq!(status(&s, t, "learner-task/status")?, "unlocked");
            assert!(
                items(&s, t)?.is_empty(),
                "unlocking must not expose a question"
            );
            assert!(!s.entity(t)?.contains_key("learner-task/elapsed-seconds"));
            assert!(
                queue_forms(&s, l, at)?.is_empty(),
                "unchanged planning must not create tasks or writes"
            );
            let at = Utc::now();
            let (forms, result) = mutate(&s, l, "start", &json!({"activityId":activity}), at)?;
            assert_eq!(result["taskId"].as_u64(), Some(t));
            s = commit(&conn, &endpoint, &s, forms, &format!("{id}-start"), at)?;
            let allocated_base = number(&s, t, "learner-task/xp-base");
            assert_eq!(allocated_base, base_xp::activity_base(&s, activity)? as f64);
            let first = *items(&s, t)?.last().unwrap();
            let at = Utc::now();
            let (forms, _) = mutate(&s, l, "pause", &json!({"taskId":t}), at)?;
            s = commit(&conn, &endpoint, &s, forms, &format!("{id}-pause"), at)?;
            let paused = number(&s, first, "task-item/elapsed-seconds");
            std::thread::sleep(Duration::from_millis(25));
            let at = Utc::now();
            let (forms, _) = mutate(&s, l, "resume", &json!({"taskId":t}), at)?;
            s = commit(&conn, &endpoint, &s, forms, &format!("{id}-resume"), at)?;
            assert_eq!(
                number(&s, first, "task-item/elapsed-seconds"),
                paused,
                "paused wall time must not accrue"
            );
            for n in 0..100 {
                if status(&s, t, "learner-task/status")? == "completed" {
                    break;
                }
                let view = task_json(&s, l, t)?;
                let step = &view["step"];
                let i = step["itemId"].as_u64().unwrap();
                let question = step["kind"] == "question";
                if question && !matches!(step["status"].as_str(), Some("correct" | "incorrect")) {
                    assert!(
                        step.get("solution").is_none(),
                        "unanswered question solution leaked"
                    );
                    assert!(
                        step["fields"]
                            .as_array()
                            .unwrap()
                            .iter()
                            .all(|f| f.get("correctAnswer").is_none()),
                        "unanswered answer key leaked"
                    );
                    assert!(
                        mutate(
                            &s,
                            l,
                            "continue",
                            &json!({"taskId":t,"itemId":i}),
                            Utc::now()
                        )
                        .is_err(),
                        "unanswered question must block continue"
                    );
                    assert!(
                        mutate(
                            &s,
                            l,
                            "answer",
                            &json!({"taskId":t,"itemId":i,"responses":[]}),
                            Utc::now()
                        )
                        .is_err(),
                        "missing answers must be rejected"
                    );
                    let content = s.reference(i, "task-item/content")?;
                    let mut answers = vec![];
                    for f in s.refs(content, "question/answer-fields")? {
                        let correct = s.reference(f, "answer-field/correct")?;
                        answers.push(if status(&s, f, "answer-field/type")? == "blank" {
                            json!({"fieldId":f,"value":text(&s,correct,"answer/value")})
                        } else {
                            json!({"fieldId":f,"choiceId":correct})
                        });
                    }
                    let at = Utc::now();
                    let body = json!({"taskId":t,"itemId":i,"responses":answers});
                    let (forms, _) = mutate(&s, l, "answer", &body, at)?;
                    s = commit(&conn, &endpoint, &s, forms, &format!("{id}-answer-{n}"), at)?;
                    assert_eq!(status(&s, i, "task-item/status")?, "correct");
                    assert!(
                        mutate(&s, l, "answer", &body, Utc::now())?.0.is_empty(),
                        "new request must not credit terminal answer twice"
                    );
                }
                let at = Utc::now();
                let body = json!({"taskId":t,"itemId":i});
                let (forms, _) = mutate(&s, l, "continue", &body, at)?;
                s = commit(
                    &conn,
                    &endpoint,
                    &s,
                    forms,
                    &format!("{id}-continue-{n}"),
                    at,
                )?;
                assert!(
                    mutate(&s, l, "continue", &body, Utc::now())?.0.is_empty(),
                    "old presentation must never advance a new step"
                );
            }
            assert_eq!(status(&s, t, "learner-task/status")?, "completed");
            assert_eq!(
                number(&s, t, "learner-task/xp-earned"),
                learning::lesson_xp(
                    &s,
                    activity,
                    &items(&s, t)?,
                    number(&s, t, "learner-task/xp-base") as i64
                )? as f64
            );
            let chain = items(&s, t)?;
            assert_eq!(
                number(&s, t, "learner-task/elapsed-seconds"),
                chain
                    .iter()
                    .map(|i| number(&s, *i, "task-item/elapsed-seconds"))
                    .sum::<f64>()
            );
            assert!(
                s.optional_ref(l, "learner/performance")?.is_some(),
                "answers must persist overall accuracy"
            );
            let topic = s.reference(activity, "activity/scope")?;
            let p = s
                .refs(l, "learner/knowledge-profile")?
                .into_iter()
                .find(|p| s.reference(*p, "progress/topic").ok() == Some(topic))
                .unwrap();
            assert_eq!(s.entity(p)?.get("progress/learned"), Some(&json!(true)));
            assert!(s.entity(p)?.contains_key("progress/memory-at"));
            assert_eq!(number(&s, t, "learner-task/xp-base"), allocated_base);
            for name in [
                "progress/expected-assessment-accuracy",
                "progress/expected-practice-accuracy",
            ] {
                let forecast = s
                    .entity(p)?
                    .get(name)
                    .and_then(Json::as_f64)
                    .expect("forecast persisted");
                assert!((0.0..=1.0).contains(&forecast));
            }
            eprintln!(
                "durable lesson completed: {} presentations; XP and FIRe persisted",
                chain.len()
            );
            Ok(())
        }))
        .unwrap_or_else(|_| Err("native integration assertion failed".into()));
        if std::env::var("LEARNING_TEST_KEEP").as_deref() == Ok("1") {
            eprintln!("KEEP_TEST_LEARNER={id}");
            return result;
        }
        let fresh = snapshot(&conn.sync()?)?;
        let mut cleanup = vec![];
        for t in fresh.refs(l, "learner/activity")? {
            cleanup.push(json!([kw("db/retractEntity"), t]));
        }
        cleanup.push(json!([kw("db/retractEntity"), l]));
        commit(
            &conn,
            &endpoint,
            &fresh,
            cleanup,
            &format!("{id}-cleanup"),
            Utc::now(),
        )?;
        result
    }
}
