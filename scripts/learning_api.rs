//! Local learner application boundary: immutable EDB reads and guarded durable writes.
mod assignment_reader;
mod assignment_interaction;
mod developer_preview;

use chrono::{DateTime, Utc};
use course_academy_engine::{
    learning,
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
fn owned(s: &EntitySnapshot, learner: u64, task: u64) -> Result<()> {
    if s.owners(task, "learner/activity")? != vec![learner] {
        return Err("Task does not belong to this learner".into());
    }
    Ok(())
}
fn items(s: &EntitySnapshot, task: u64) -> Result<Vec<u64>> {
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
fn course(s: &EntitySnapshot, l: u64) -> Result<u64> {
    Ok(s.reference(l, "learner/course")?)
}
fn learner_json(s: &EntitySnapshot, l: u64) -> Json {
    json!({"id":text(s,l,"learner/id"),"name":text(s,l,"learner/name"),
        "selfDirected":s.entities.get(&l).and_then(|r|r.get("learner/self-directed")).and_then(Json::as_bool).unwrap_or(false),
        "targets":s.refs(l,"learner/targets").unwrap_or_default()})
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
    groups.sort_by(|a, b| a["title"].as_str().cmp(&b["title"].as_str()).then_with(|| a["id"].as_str().cmp(&b["id"].as_str())));
    Ok(groups)
}
fn profile_json(s: &EntitySnapshot, l: u64) -> Result<Json> {
    let mut courses: Vec<_> = s.entities.iter().filter_map(|(_, record)| {
        let id = record.get("course/id")?.get("$uuid")?.as_str()?;
        let title = record.get("course/title")?.as_str()?;
        Some(json!({"id":id,"title":title}))
    }).collect();
    courses.sort_by(|a, b| a["title"].as_str().cmp(&b["title"].as_str()));
    Ok(json!({"learner":learner_json(s,l),"course":course_json(s,l)?,"courses":courses}))
}
fn another_started_task(s: &EntitySnapshot, learner: u64, current: Option<u64>) -> Result<bool> {
    for task in s.refs(learner, "learner/activity")? {
        if Some(task) != current && status(s, task, "learner-task/status")? == "started" {
            return Ok(true);
        }
    }
    Ok(false)
}
fn home(s: &EntitySnapshot, l: u64) -> Result<Json> {
    let c = course(s, l)?;
    let candidates = learning::plan_candidates(s, l, c, Utc::now())?;
    let mut activities = vec![];
    for candidate in candidates {
        let a = candidate.activity;
        let Some(task) = task_for(s, l, a)? else { continue };
        let state = status(s, task, "learner-task/status")?;
        if state == "locked" { continue; }
        let expected = number(s, a, "activity/expected-seconds");
        let expected = if expected > 0.0 { expected } else {
            s.refs(a, "activity/steps")?.into_iter().map(|step| number(s, step, "step/expected-seconds")).sum()
        };
        let progress = if matches!(state.as_str(), "started" | "paused") {
            lesson_progress(s, &learning::lesson_steps(s, a)?, &items(s, task)?)?
        } else {
            Json::Null
        };
        activities.push(json!({"activityId":a,"title":text(s,a,"activity/title"),"type":"lesson","taskId":task,"status":state,
            "priority":number(s,task,"learner-task/priority"),"reason":candidate.reason,"targetCount":candidate.target_count,
            "targetTopics":candidate.target_topics,"progress":progress,"expectedSeconds":if expected>0.0{Some(expected)}else{None}}));
        if activities.len() == 5 { break; }
    }
    Ok(
        json!({"basis":s.basis_t,"learner":learner_json(s,l),"course":course_json(s,l)?,"activities":activities,"queueDescription":"Ready activities prioritized by current work, study targets, assignment deadlines, and prerequisite readiness.","practiceNotice":"Each skill needs two correct answers in a row, with up to five questions. If fresh questions run out, more content is needed and the lesson remains unfinished."}),
    )
}

/// Materialize available work without recording any presentation or starting a clock.
/// The caller journals this transaction and submits it with an exact basis guard.
fn queue_forms(s: &EntitySnapshot, l: u64, at: DateTime<Utc>) -> Result<Vec<Json>> {
    let plan = learning::plan_candidates(s, l, course(s, l)?, at)?;
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
            "completed" | "failed" => { terminal_assignments.insert(activity); }
            _ => return Err("Unknown task status".into()),
        }
    }
    let mut forms = vec![];
    let mut eligible = BTreeSet::new();
    for candidate in plan {
        let activity = candidate.activity;
        eligible.insert(activity);
        let priority = candidate.priority;
        if !priority.is_finite() { return Err("Task priority must be finite".into()); }
        if let Some(&task) = pending.get(&activity) {
            if status(s, task, "learner-task/status")? == "locked" {
                forms.push(cas(s, task, "learner-task/status", "learner-task.status/unlocked")?);
            }
            if s.entity(task)?.get("learner-task/priority").and_then(Json::as_f64) != Some(priority) {
                forms.push(add(json!(task), "learner-task/priority", json!(priority)));
            }
        } else {
            let temp = format!("queue-task-{activity}");
            forms.push(json!({"db/id":temp,"learner-task/id":{"$uuid":uid()?},"learner-task/activity":activity,
                "learner-task/status":kw("learner-task.status/unlocked"),"learner-task/priority":priority,"db/ensure":kw("learner-task/validate")}));
            forms.push(add(json!(l), "learner/activity", json!(temp)));
        }
    }
    for (&activity, &task) in &pending {
        let state = status(s, task, "learner-task/status")?;
        if eligible.contains(&activity) || matches!(state.as_str(), "started" | "paused") { continue; }
        if state == "unlocked" {
            forms.push(cas(s, task, "learner-task/status", "learner-task.status/locked")?);
        }
        if number(s, task, "learner-task/priority") != 0.0 {
            forms.push(add(json!(task), "learner-task/priority", json!(0.0)));
        }
    }
    // Assigned activities get a record immediately. Unsupported players remain
    // locked; their mapped topics can still prioritize runnable preparation lessons.
    for activity in s.refs(l, "learner/assignments")? {
        if !s.entity(activity)?.contains_key("activity/id")
            || status(s, activity, "activity/type")? != "assignment" {
            return Err("Learner assignments must reference assignment activities".into());
        }
        if pending.contains_key(&activity) || terminal_assignments.contains(&activity) || eligible.contains(&activity) { continue; }
        let temp = format!("queue-assignment-{activity}");
        forms.push(json!({"db/id":temp,"learner-task/id":{"$uuid":uid()?},"learner-task/activity":activity,
            "learner-task/status":kw("learner-task.status/locked"),"learner-task/priority":0.0,"db/ensure":kw("learner-task/validate")}));
        forms.push(add(json!(l), "learner/activity", json!(temp)));
    }
    Ok(forms)
}
fn authored_step(steps: &[learning::LessonStep], content: u64) -> Option<(usize, &learning::LessonStep)> {
    steps.iter().enumerate().find(|(_, entry)| {
        entry.content == content
            || entry.example == Some(content)
            || entry.questions.contains(&content)
    })
}

/// Presentations within an adaptive skill share one authored step. Study and
/// the player report the same position rather than counting practice questions.
fn lesson_progress(s: &EntitySnapshot, steps: &[learning::LessonStep], chain: &[u64]) -> Result<Json> {
    let step_number = if let Some(&item) = chain.last() {
        authored_step(steps, s.reference(item, "task-item/content")?)
            .map(|(index, _)| index + 1)
            .unwrap_or(1)
    } else {
        1
    };
    Ok(json!({"stepNumber":step_number,"totalSteps":steps.len(),"presented":chain.len(),
        "answered":chain.iter().filter(|i|matches!(status(s,**i,"task-item/status").as_deref(),Ok("correct"|"incorrect"))).count()}))
}

fn task_json(s: &EntitySnapshot, l: u64, t: u64) -> Result<Json> {
    owned(s, l, t)?;
    let a = s.reference(t, "learner-task/activity")?;
    let task_state = status(s, t, "learner-task/status")?;
    let chain = items(s, t)?;
    let at = Utc::now();
    let steps = learning::lesson_steps(s, a)?;
    let progress = lesson_progress(s, &steps, &chain)?;
    let mut step = Json::Null;
    if let Some(&i) = chain.last() {
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
        } else if let Some((_, entry)) =
            authored.filter(|(_, entry)| entry.kind == "knowledge-point")
        {
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
            let mut field =
                json!({"id":f,"key":text(s,f,"answer-field/key"),"type":kind,"choices":choices});
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
        step = json!({"itemId":i,"contentId":content,"kind":if tutorial{"tutorial"}else if example{"example"}else{"question"},"title":title,"markdown":text(s,content,if tutorial{"tutorial/content"}else{"question/problem"}),"fields":fields,"status":state,"canContinue":tutorial||example||terminal,"requiresCalculator":e.get("question/requires-calculator"),"elapsedSeconds":timing::elapsed(s,i,at)?});
        step["stepId"] = json!(authored.map(|(_, entry)| entry.step.to_string()));
        if reveal {
            step["solution"] = json!(text(s, content, "question/worked-solution"));
        }
    }
    Ok(
        json!({"basis":s.basis_t,"taskId":t,"activityId":a,"learner":learner_json(s,l),"course":course_json(s,l)?,"title":text(s,a,"activity/title"),"status":task_state,"xp":number(s,t,"learner-task/xp-earned"),"xpBase":number(s,t,"learner-task/xp-base"),"elapsedSeconds":if matches!(task_state.as_str(),"unlocked"|"locked"){number(s,t,"learner-task/elapsed-seconds")}else{timing::task_elapsed(s,t,at)?},"step":step,"progress":progress}),
    )
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
    if action.starts_with("assignment-") || (action == "pause" && body["taskId"].as_u64().is_some_and(|task| {
        s.optional_ref(task, "learner-task/activity").ok().flatten().is_some_and(|activity| {
            matches!(status(s, activity, "activity/type").as_deref(), Ok("assignment"))
        })
    })) {
        return assignment_interaction::mutate(s, l, action, body, at);
    }
    let mut forms = vec![];
    if action == "profile-settings" {
        let requested = body["courseId"].as_str().ok_or("courseId is required")?;
        let selected = s.entities.iter().find_map(|(id, record)| {
            (record.get("course/id").and_then(|v| v.get("$uuid")).and_then(Json::as_str) == Some(requested)).then_some(*id)
        }).ok_or("Selected course does not exist")?;
        let directed = body["selfDirected"].as_bool().ok_or("selfDirected must be a boolean")?;
        let old_directed = learner_json(s, l)["selfDirected"] == true;
        if course(s, l)? != selected || old_directed != directed {
            // Pause and change settings in the same transaction so no activity
            // continues timing against the previous study selection.
            for task in s.refs(l, "learner/activity")? {
                if status(s, task, "learner-task/status")? == "started" {
                    forms.extend(mutate(s, l, "pause", &json!({"taskId":task}), at)?.0);
                }
            }
            forms.push(json!([kw("db/add"),l,kw("learner/course"),selected]));
            forms.push(json!([kw("db/add"),l,kw("learner/self-directed"),directed]));
        }
        return Ok((forms, json!({"profile":true})));
    }
    if action == "queue" {
        return Ok((queue_forms(s, l, at)?, json!({"queue":true})));
    }
    if action == "target" {
        if s.entity(l)?.get("learner/self-directed").and_then(Json::as_bool) != Some(true) {
            return Err("Self-directed study is not enabled for this learner".into());
        }
        let topic = required(body, "topicId")?;
        if !s.entity(topic)?.contains_key("topic/id") {
            return Err("A study target must reference a topic".into());
        }
        let selected = body["selected"].as_bool().ok_or("selected must be a boolean")?;
        let mut targets: BTreeSet<_> = s.refs(l, "learner/targets")?.into_iter().collect();
        let changed = if selected { targets.insert(topic) } else { targets.remove(&topic) };
        if changed {
            forms.push(json!([kw(if selected {"db/add"} else {"db/retract"}),l,kw("learner/targets"),topic]));
        }
        let mut prospective = s.clone();
        prospective.entities.get_mut(&l).unwrap().insert("learner/targets".into(), json!(targets));
        forms.extend(queue_forms(&prospective, l, at)?);
        return Ok((forms, json!({"targets":true})));
    }
    if action == "start" {
        let a = required(body, "activityId")?;
        if !learning::candidates(s, l, course(s, l)?)?.contains(&a) {
            return Err("Activity is not eligible or its content is unavailable".into());
        }
        if let Some(t) = task_for(s, l, a)? {
            let state = status(s, t, "learner-task/status")?;
            if state == "paused" {
                return mutate(s, l, "resume", &json!({"taskId":t}), at);
            }
            if matches!(state.as_str(), "locked" | "unlocked") {
                if another_started_task(s, l, Some(t))? || timing::active_item(s, l)?.is_some() {
                    return Err("Pause the current lesson before starting another".into());
                }
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
                    let expected = number(s, a, "activity/expected-seconds");
                    forms.push(add(
                        json!(t),
                        "learner-task/xp-base",
                        json!(if expected > 0.0 {
                            (expected / 60.0).round().max(1.0) as i64
                        } else {
                            12
                        }),
                    ));
                }
                let content =
                    learning::first_content(s, a, l)?.ok_or("Lesson has no available content")?;
                append_item(json!(t), None, content, &mut forms)?;
            }
            return Ok((forms, json!({"taskId":t})));
        }
        if timing::active_item(s, l)?.is_some() || another_started_task(s, l, None)? {
            return Err("Pause the current lesson before starting another".into());
        }
        let id = uid()?;
        let expected = number(s, a, "activity/expected-seconds");
        let xp_base = if expected > 0.0 {
            (expected / 60.0).round().max(1.0) as i64
        } else {
            12
        };
        forms.push(json!({"db/id":"new-task","learner-task/id":{"$uuid":id},"learner-task/activity":a,"learner-task/status":kw("learner-task.status/started"),"learner-task/priority":1.0,"learner-task/elapsed-seconds":0.0,"learner-task/xp-base":xp_base,"learner-task/xp-earned":0,"db/ensure":kw("learner-task/validate")}));
        forms.push(add(json!(l), "learner/activity", json!("new-task")));
        let content =
            learning::first_content(s, a, l)?.ok_or("Lesson has no available content")?;
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
    if matches!(action, "pause" | "resume") {
        let target = if action == "pause" {
            "paused"
        } else {
            "started"
        };
        if state == target || matches!(state.as_str(), "completed" | "failed") {
            return Ok((forms, json!({"taskId":t})));
        }
        if !matches!(state.as_str(), "started" | "paused") {
            return Err("Task cannot change running state".into());
        }
        if action == "resume"
            && (timing::active_item(s, l)?.is_some() || another_started_task(s, l, Some(t))?)
        {
            return Err("Pause the current lesson before resuming another".into());
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
        let instruction =
            e.contains_key("tutorial/id") || s.is_example(content);
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
            let (next, passed, xp) = learning::continuation(
                s,
                a,
                &chain,
                !terminal,
                number(s, t, "learner-task/xp-base") as i64,
            )?;
            if let Some(next) = next {
                append_item(json!(t), Some(i), next, &mut forms)?;
            } else {
                forms.push(cas(
                    s,
                    t,
                    "learner-task/status",
                    if passed {
                        "learner-task.status/completed"
                    } else {
                        "learner-task.status/failed"
                    },
                )?);
                forms.push(add(json!(t), "learner-task/xp-earned", json!(xp)));
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
            return assignment_reader::detail_mode(&s, l, body["assignmentId"].as_str().ok_or("Assignment ID required")?, body["preview"] == true);
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
        if action == "target" {
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
        // Task evidence commits first. Refresh derived availability immediately,
        // using its own replayable request so queue maintenance cannot duplicate credit.
        let request = format!("queue-after-{l}-{}", self.snapshot.basis_t);
        let queue_error = self.process(&json!({"action":"queue","requestId":request})).err();
        let mut view = task_json(&self.snapshot, l, t)?;
        if let Some(error) = queue_error {
            eprintln!("Queue refresh postponed after saved task: {error}");
            view["queueNotice"] = json!("Your work is saved. Refresh the home page to update available activities.");
        }
        Ok(view)
    }
}

fn envelope(result: Result<Json>) -> Json {
    match result {
        Ok(data) => json!({"ok":true,"data":data}),
        Err(error) => {
            eprintln!("Learning API: {error}");
            let mut code = "validation";
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
    fn saved_position_uses_authored_steps_even_with_multiple_practice_presentations() {
        let steps = vec![
            learning::LessonStep { step: 10, content: 100, kind: "tutorial".into(), example: None, questions: vec![] },
            learning::LessonStep { step: 20, content: 200, kind: "knowledge-point".into(), example: Some(201), questions: vec![202, 203] },
            learning::LessonStep { step: 30, content: 300, kind: "tutorial".into(), example: None, questions: vec![] },
            learning::LessonStep { step: 40, content: 400, kind: "tutorial".into(), example: None, questions: vec![] },
        ];
        let records: BTreeMap<_, _> = [
            (100, json!({})), (200, json!({})), (201, json!({})),
            (202, json!({})), (203, json!({})), (300, json!({})), (400, json!({})),
            (900, json!({"db/ident":kw("task-item.status/correct")})),
            (901, json!({"db/ident":kw("task-item.status/paused")})),
            (1, json!({"task-item/content":100,"task-item/status":900})),
            (2, json!({"task-item/content":201,"task-item/status":900})),
            (3, json!({"task-item/content":202,"task-item/status":900})),
            (4, json!({"task-item/content":203,"task-item/status":900})),
            (5, json!({"task-item/content":300,"task-item/status":901})),
        ].into_iter().map(|(id, record)| (id, record.as_object().unwrap().clone())).collect();
        let s = EntitySnapshot::new(records, 42).unwrap();
        let before = s.entities.clone();
        for chain in [&[1, 2][..], &[1, 2, 3][..], &[1, 2, 3, 4][..]] {
            let progress = lesson_progress(&s, &steps, chain).unwrap();
            assert_eq!(progress["stepNumber"], 2);
            assert_eq!(progress["totalSteps"], 4);
        }
        let halfway = lesson_progress(&s, &steps, &[1, 2, 3, 4, 5]).unwrap();
        assert_eq!(halfway, json!({"stepNumber":3,"totalSteps":4,"presented":5,"answered":4}));
        assert_eq!(lesson_progress(&s, &steps, &[]).unwrap()["stepNumber"], 1);
        assert_eq!(lesson_progress(&s, &steps, &[1]).unwrap()["stepNumber"], 1);
        assert_eq!(authored_step(&steps, 200).unwrap().0, 1);
        assert_eq!(s.entities, before);
        assert_eq!(s.basis_t, 42);
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
        forms.push(json!({"db/id":"test-learner","learner/id":id,"learner/name":"Temporary learner API integration test","learner/course":c,"learner/self-directed":true,"learner/knowledge-profile":progress,"db/ensure":kw("learner/validate")}));
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
            let activity = *learning::candidates(&s, l, c)?
                .first()
                .ok_or("no eligible test lesson")?;
            let at = Utc::now();
            let forms = queue_forms(&s, l, at)?;
            assert!(!forms.is_empty(), "available work needs pending task records");
            s = commit(&conn, &endpoint, &s, forms, &format!("{id}-queue"), at)?;
            let t = task_for(&s, l, activity)?.ok_or("queue did not create task")?;
            assert_eq!(status(&s, t, "learner-task/status")?, "unlocked");
            assert!(items(&s, t)?.is_empty(), "unlocking must not expose a question");
            assert!(!s.entity(t)?.contains_key("learner-task/elapsed-seconds"));
            assert!(queue_forms(&s, l, at)?.is_empty(), "unchanged planning must not create tasks or writes");
            let topic = s.reference(activity, "activity/scope")?;
            let baseline = number(&s, t, "learner-task/priority");
            let pending = s.refs(l, "learner/activity")?;
            let target = json!({"topicId":topic,"selected":true});
            let (forms, _) = mutate(&s, l, "target", &target, at)?;
            s = commit(&conn, &endpoint, &s, forms, &format!("{id}-target"), at)?;
            assert_eq!(s.refs(l, "learner/targets")?, vec![topic]);
            assert_eq!(s.refs(l, "learner/activity")?, pending);
            assert!(number(&s, t, "learner-task/priority") > baseline);
            assert!(mutate(&s, l, "target", &target, at)?.0.is_empty());
            assert!(mutate(&s, l, "target", &json!({"topicId":c,"selected":true}), at).is_err());
            let (forms, _) = mutate(&s, l, "target", &json!({"topicId":topic,"selected":false}), at)?;
            s = commit(&conn, &endpoint, &s, forms, &format!("{id}-untarget"), at)?;
            assert!(s.refs(l, "learner/targets")?.is_empty());
            assert_eq!(number(&s, t, "learner-task/priority"), baseline);
            assert_eq!(task_for(&s, l, activity)?, Some(t));
            let at = Utc::now();
            let (forms, result) = mutate(&s, l, "start", &json!({"activityId":activity}), at)?;
            assert_eq!(result["taskId"].as_u64(), Some(t));
            s = commit(&conn, &endpoint, &s, forms, &format!("{id}-start"), at)?;
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
