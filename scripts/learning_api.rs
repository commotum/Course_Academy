//! Local learner application boundary: immutable EDB reads and guarded durable writes.
mod activity_history;
mod review_interaction;
mod study_stats;
mod forecast_reader;
mod assignment_interaction;
mod assignment_reader;
mod developer_preview;
mod page_reader;
mod quiz_labels;
use quiz_labels::QuizLabels;
#[cfg(test)]
#[path = "../engine/edb/answer_fields.rs"]
mod preview_answer_fields;
#[cfg(test)]
#[allow(dead_code)]
#[path = "../engine/edb/configuration.rs"]
mod preview_configuration;
#[cfg(test)]
#[allow(dead_code)]
#[path = "../engine/edb/progress.rs"]
mod preview_progress;
#[cfg(test)]
mod retrieval_tests;

use chrono::{DateTime, Utc};
use course_academy_engine::{
    base_xp, learning, retrieval,
    schema::{self, EntitySnapshot, Record, StatusAssertion},
    timing,
};
use edb_core::{
    Cardinality, Connection, DatabaseValue, EntityRef, IndexOrder, IndexPrefix, Keyword,
    SnapshotReference, TimePoint, TransactionRequest, Value, postgres_config_from_env,
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
const ENGINE_SOURCE: &str = "application/ca-engine";

fn engine_source() -> EntityRef {
    EntityRef::Ident(Keyword::new("application", "ca-engine"))
}

fn saved_request_source(saved: &Json, learner: u64) -> Result<EntityRef> {
    match saved.get("source") {
        Some(Json::String(source)) if source == ENGINE_SOURCE => Ok(engine_source()),
        // The request source participates in exact-retry identity. Preserve
        // the original source for journals created before engine attribution.
        None => Ok(EntityRef::Id(learner)),
        _ => Err("Saved request has an unsupported transaction source".into()),
    }
}

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
    s.focused_mode = course_academy_engine::study_mode::FOCUSED_MODE;
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
    home_cache: Option<(Instant, Duration, Json, bool)>,
    inventory_cache: Option<(Instant, Duration, Json)>,
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
            .with_attribute("learner/id")
            .into_iter()
            .find(|eid| {
                snapshot.entities[eid]
                    .get("learner/id")
                    .and_then(Json::as_str)
                    == Some(&learner)
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
            inventory_cache: None,
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
                let mut status_changed=false;
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
                        if matches!(name.as_str(),"task-item/status"|"learner-task/status") {status_changed=true;}
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
                // Ordinary queue, target, and content edits do not alter clock
                // history. noHistory attributes still require a fresh read,
                // since maintenance can remove assertions between commits.
                let retained_history=["task-item/status","learner-task/status"].iter().all(|name|{
                    let (ns,n)=name.split_once('/').unwrap();
                    db.schema().resolve_ident(&Keyword::new(ns,n))
                        .and_then(|id|db.schema().attribute(id).ok())
                        .is_some_and(|attribute|!attribute.no_history)
                });
                if status_changed || !retained_history {refresh_history(&db, &mut self.snapshot)?;}
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
        self.inventory_cache = None;
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

    fn handle(&mut self, mut body: Json) -> Result<Json> {
        let started = Instant::now();
        self.adopt(self.conn.sync()?)?;
        trace("sync", started);
        let focused = body.as_object_mut().and_then(|body| body.remove("_focusedMode"))
            .map(|value| value.as_bool().ok_or("Focused mode must be a boolean"))
            .transpose()?.unwrap_or(course_academy_engine::study_mode::FOCUSED_MODE);
        if self.snapshot.focused_mode != focused {
            self.snapshot.focused_mode = focused;
            self.home_cache = None;
            self.inventory_cache = None;
        }
        let action = body["action"].as_str().ok_or("Action required")?;
        if action=="inventory" {
            if let Some((at,lifetime,result))=&self.inventory_cache {
                if at.elapsed()<*lifetime {return Ok(result.clone());}
            }
            let started=Instant::now();
            let now=Utc::now();
            let lifetime=course_academy_engine::scheduling::lifecycle(&self.snapshot,self.learner_eid)
                .map(|history|inventory_cache_duration(self.home_lifetime(),history.mastered.values().copied(),now))
                .unwrap_or(Duration::ZERO);
            let result=self.process(&body)?;
            self.inventory_cache=Some((started,lifetime,result.clone()));
            trace(action,started);
            return Ok(result);
        }
        // Readiness decays without commits. Cache only until the next known
        // retention boundary, with a one-minute upper bound. Mutations always
        // compute eligibility against the new captured value and current time.
        if action == "home" {
            if let Some(result) = self.cached_home(false) {
                return Ok(result);
            }
        }
        let started = Instant::now();
        let home_lifetime = if matches!(action, "home" | "queue") {
            self.home_lifetime()
        } else {
            Duration::ZERO
        };
        // A queue cache hit must keep its original expiry. The scheduler polls
        // every 30 seconds; renewing on each hit could hide time-based changes.
        let reusable_cache = self.home_cache.as_ref().and_then(|(at, lifetime, _, prepared)| {
            (action == "queue" && *prepared && at.elapsed() < *lifetime).then_some(*at)
        });
        let result = self.process(&body)?;
        let reused_cache = reusable_cache.is_some_and(|previous| {
            self.home_cache.as_ref().is_some_and(|(at, _, _, _)| *at == previous)
        });
        if matches!(action, "home" | "queue") && !reused_cache {
            self.home_cache = Some((started, home_lifetime, result.clone(), action == "queue"));
        }
        trace(action, started);
        Ok(result)
    }

    fn cached_home(&self, prepared: bool) -> Option<Json> {
        self.home_cache
            .as_ref()
            .and_then(|(at, lifetime, result, queue_prepared)| {
                (at.elapsed() < *lifetime && (!prepared || *queue_prepared)).then(|| result.clone())
            })
    }

    fn home_lifetime(&self) -> Duration {
        home_cache_duration(&self.snapshot, self.learner_eid, Utc::now())
    }
}

fn home_cache_duration(snapshot: &EntitySnapshot, learner: u64, at: DateTime<Utc>) -> Duration {
    let now = schema::timestamp_days(at);
    let mut seconds: f64 = 60.0;
    // A failed/malformed estimate disables caching; home() supplies its
    // ordinary validation error instead of hiding it behind stale output.
    let Ok(progress) = snapshot.refs(learner, "learner/knowledge-profile")
    else {
        return Duration::ZERO;
    };
    for progress in progress {
        let Ok(record) = snapshot.entity(progress) else {
            return Duration::ZERO;
        };
        if record.get("progress/learned") != Some(&json!(true)) {
            continue;
        }
        let boundary = (|| -> Option<(f64, f64)> {
            let memory = record.get("progress/memory")?.as_f64()?;
            let interval = record.get("progress/interval-days")?.as_f64()?;
            let at = schema::instant_days(record.get("progress/memory-at")?).ok()?;
            let policy = snapshot.eid(record.get("progress/policy")?).ok()?;
            let threshold = snapshot.entity(policy)
                .ok()?
                .get("policy/review-threshold")?
                .as_f64()?;
            if !memory.is_finite()
                || memory < 0.0
                || !interval.is_finite()
                || interval <= 0.0
                || !threshold.is_finite()
                || threshold <= 0.0
            {
                return None;
            }
            // Zero memory is valid and already due. It has no future
            // decay crossing, but a future observation still matters.
            Some((at, if memory == 0.0 { at } else { at + interval * (memory / threshold).log2() }))
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
    if let Ok(tasks) = snapshot.refs(learner, "learner/activity") {
        for task in tasks {
            if let Ok(Some(remaining)) = retrieval::remaining(snapshot, task, at)
            {
                seconds = seconds.min((remaining - 0.002).max(0.0));
            }
        }
    }
    // Assessment topics become eligible after 48 hours even with no commit.
    let Ok(history) = course_academy_engine::scheduling::lifecycle(snapshot, learner) else {
        return Duration::ZERO;
    };
    for learned in history.mastered.values() {
        let boundary = *learned + chrono::Duration::hours(48);
        if boundary >= at {
            seconds = seconds.min(((boundary - at).num_milliseconds() as f64 / 1000.0 - 0.002).max(0.0));
        }
    }
    Duration::from_secs_f64(seconds)
}

fn inventory_cache_duration(review_lifetime:Duration, mastered:impl Iterator<Item=DateTime<Utc>>, now:DateTime<Utc>) -> Duration {
    let mut seconds=review_lifetime.as_secs_f64().min(10.0);
    for learned in mastered {
        let boundary=learned+chrono::Duration::hours(48);
        if boundary>=now {
            seconds=seconds.min(((boundary-now).num_milliseconds() as f64/1000.0-0.002).max(0.0));
        }
    }
    Duration::from_secs_f64(seconds)
}

fn trace(stage: &str, started: Instant) {
    if std::env::var_os("LEARNING_TRACE").is_some() || started.elapsed()>Duration::from_millis(250) || matches!(stage,"grade"|"plan"|"durable-write-and-open-receipt"|"observe-commit") {
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
    for activity in s.owners(topic, "activity/scope")? {
        if status(s, activity, "activity/type")? == "lesson"
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
            let finished_at = timing::task_finished_at(s,task,timing::status_at(s, task, "learner-task/status")?)?;
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

fn check_lesson_retry(s: &EntitySnapshot, l: u64, activity: u64) -> Result<()> {
    if retrieval::kind(s, activity)? != "lesson" { return Ok(()); }
    let h = course_academy_engine::scheduling::lifecycle(s, l)?;
    if let Some(topic) = s.optional_ref(activity, "activity/scope")? {
        if h.lesson_blocked(s, topic)? {
            return Err("Complete the prerequisite repairs before retrying this lesson".into());
        }
        if let Some(task) = task_for(s, l, activity)? {
            if !s.refs(task, "learner-task/remediation-for")?.is_empty() && !h.retry_ready(topic) {
                return Err("Complete five other successful practice activities before this required lesson retry".into());
            }
        }
    }
    Ok(())
}

// Shared by actual starts and the read-only menu check. Supply is counted from
// the resident immutable snapshot, including seen and reserved questions.
fn check_activity_start(s: &EntitySnapshot, l: u64, activity: u64,
    selected_topic: Option<u64>, at: DateTime<Utc>) -> Result<()> {
    if retrieval::kind(s, activity)? == "lesson" {
        let topic = s.reference(activity, "activity/scope")?;
        let shortages = course_academy_engine::inventory::lesson_shortages(
            s, &s.refs(topic, "topic/knowledge-points")?, &learning::unavailable_questions(s, l)?)?;
        if !shortages.is_empty() {
            let details = shortages.into_iter().map(|(kp, count)|format!("{} has {count} (needs {} more)",
                text(s, kp, "knowledge-point/title"), 5-count)).collect::<Vec<_>>().join("; ");
            return Err(format!("Lesson needs at least five fresh, gradable questions per skill: {details}").into());
        }
    }
    // A manually selected review need not be due yet. Its route still uses
    // the regular fresh-question reservation and review grading policies.
    if retrieval::kind(s, activity)? == "review"
        && selected_topic.is_some_and(|topic| s.optional_ref(activity, "activity/scope").ok().flatten() == Some(topic))
        && retrieval::fresh(s, l, activity)? { return Ok(()); }
    let candidates = if let Some(topic) = selected_topic {
        learning::selected_topic_candidates(s, l, course(s, l)?, topic, at)?
    } else {
        learning::study_candidates(s, l, course(s, l)?, at)?
    };
    if !candidates.iter().any(|p| p.activity == activity) {
        return Err("Activity is not eligible or its content is unavailable".into());
    }
    Ok(())
}

// The menu and the mutation use the same immutable review plan. Checking an
// action never creates a definition, reserves questions, or changes an attempt.
enum TopicReviewPlan {
    Existing { task: u64, activity: u64, state: String },
    New(retrieval::Definition),
}

fn topic_review_plan(s: &EntitySnapshot, l: u64, topic: u64, at: DateTime<Utc>) -> Result<TopicReviewPlan> {
    if !s.entity(topic)?.contains_key("topic/id") { return Err("Review requires a topic entity ID".into()); }
    let mut existing = vec![];
    for task in s.refs(l, "learner/activity")? {
        let activity = s.reference(task, "learner-task/activity")?;
        if retrieval::kind(s, activity)? != "review" || s.optional_ref(activity, "activity/scope")? != Some(topic) { continue; }
        let state = status(s, task, "learner-task/status")?;
        if matches!(state.as_str(), "started" | "paused") {
            existing.push((0, task, activity, state));
        } else if matches!(state.as_str(), "locked" | "unlocked") && retrieval::fresh(s, l, activity)? {
            existing.push((1, task, activity, state));
        }
    }
    existing.sort();
    // Required queue work is a recommendation, not a lock on an explicitly
    // selected review. Keep eligibility and content checks local to this topic.
    if let Some((_, task, activity, state)) = existing.into_iter().next() {
        // Resume/start have their own continuation and freshness checks too.
        // Validate their plan here so an enabled action matches its mutation.
        let action = if state == "paused" { "resume" } else { "start" };
        mutate_with_selection(s, l, action, &json!({"taskId":task,"activityId":activity}), at, Some(topic))?;
        return Ok(TopicReviewPlan::Existing { task, activity, state });
    }
    Ok(TopicReviewPlan::New(retrieval::selected_review(s, l, topic)?))
}

fn topic_study_availability(s: &EntitySnapshot, l: u64, topic: u64, at: DateTime<Utc>) -> Json {
    let check = || -> Result<(bool, bool)> {
        let activity = topic_lesson(s, topic)?;
        check_lesson_retry(s, l, activity)?;
        let existing = task_for(s, l, activity)?;
        if existing.is_none() && !retrieval::relearn_topics(s, l)?.contains(&topic)
            && completed_task_for(s, l, activity)?.is_some() { return Ok((false, true)); }
        if let Some(task) = existing {
            match status(s, task, "learner-task/status")?.as_str() {
                "started" => return Ok((true, false)),
                "paused" => {
                    let chain = items(s, task)?;
                    chain.last().ok_or("Task has no presentation")?;
                    learning::continuation_state(s, activity, &chain, false, false)?;
                    return Ok((true, false));
                }
                _ => {}
            }
        }
        check_activity_start(s, l, activity, Some(topic), at)?;
        learning::first_content(s, activity, l)?.ok_or("Lesson has no available content")?;
        Ok((false, false))
    };
    let mut view = match check() {
        Ok((resumable, completed)) => json!({"basis":s.basis_t,"topicId":topic,"available":true,"resumable":resumable,"completed":completed}),
        Err(error) => json!({"basis":s.basis_t,"topicId":topic,"available":false,"resumable":false,"completed":false,"reason":error.to_string()}),
    };
    view["review"] = match topic_review_plan(s, l, topic, at) {
        Ok(TopicReviewPlan::Existing { state, .. }) => json!({"available":true,"resumable":matches!(state.as_str(),"started"|"paused")}),
        Ok(TopicReviewPlan::New(_)) => json!({"available":true,"resumable":false}),
        Err(error) => json!({"available":false,"resumable":false,"reason":error.to_string()}),
    };
    view
}
fn learner_json(s: &EntitySnapshot, l: u64) -> Json {
    json!({"id":text(s,l,"learner/id"),"name":text(s,l,"learner/name"),
        "focusedMode":s.focused_mode,
        "dailyXpGoal":s.entities.get(&l).and_then(|r|r.get("learner/daily-xp-goal")),
        "selfDirected":s.entities.get(&l).and_then(|r|r.get("learner/self-directed")).and_then(Json::as_bool).unwrap_or(false),
        "targets":s.refs(l,"learner/targets").unwrap_or_default(),
        "queue":s.refs(l,"learner/queue").unwrap_or_default()})
}
fn course_json(s: &EntitySnapshot, l: u64) -> Result<Json> {
    let Some(c) = s.optional_ref(l, "learner/course")? else {
        return Ok(Json::Null);
    };
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
        .with_attribute("course/id")
        .into_iter()
        .filter_map(|course| {
            let record = &s.entities[&course];
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
            if !matches!(
                status(s, activity, "activity/type")?.as_str(),
                "lesson" | "review" | "assessment"
            ) {
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
    home_with_candidates(s, l, None)
}

fn home_with_candidates(
    s: &EntitySnapshot,
    l: u64,
    candidates: Option<Vec<learning::PlannedActivity>>,
) -> Result<Json> {
    let Some(c) = s.optional_ref(l, "learner/course")? else {
        return Ok(json!({
            "basis": s.basis_t, "learner": learner_json(s, l), "course": null,
            "activities": [], "waitingActivities": [], "needsCourseSelection": true,
            "queueDescription": "Choose a course in your profile to begin studying.",
            "practiceNotice": "",
        }));
    };
    let self_directed = learner_json(s, l)["selfDirected"] == true;
    let candidates = match candidates {
        Some(candidates) => candidates,
        None => learning::study_candidates(s, l, c, Utc::now())?,
    };
    let mut activities = vec![];
    let quiz_labels = QuizLabels::capture(s, l)?;
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
        activities.push(json!({"activityId":a,"title":quiz_labels.title(s,a,task)?,"type":status(s,a,"activity/type")?,"taskId":task,"status":state,
            "priority":candidate.priority,"reason":candidate.reason,"targetCount":candidate.target_count,
            "targetTopics":candidate.target_topics,"progress":progress,
            "xpBase":if retrieval::kind(s,a)? == "assessment" { Some(match task.and_then(|t|s.entities[&t].get("learner-task/xp-base")).and_then(Json::as_i64) {Some(base)=>base,None=>base_xp::duration_base(expected)?}) } else { None },
            "expectedSeconds":if expected>0.0{Some(expected)}else{None}}));
        if activities.len() == course_academy_engine::scheduling::STUDY_QUEUE_LIMIT {
            break;
        }
    }
    let mut waiting = vec![];
    let layers = learning::topic_layers(s)?;
    for t in s.refs(l, "learner/activity")? {
        if status(s, t, "learner-task/status")? != "paused" {
            continue;
        }
        let a = s.reference(t, "learner-task/activity")?;
        if status(s, a, "activity/type")? != "lesson" {
            continue;
        }
        let topic = s.reference(a, "activity/scope")?;
        if !learning::topic_in_study_focus(s, l, topic)? { continue; }
        if layers.get(&topic).is_none_or(|&layer| layer + 1 < learning::MIN_STUDY_LAYER) {
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
        json!({"basis":s.basis_t,"learner":learner_json(s,l),"course":course_json(s,l)?,"activities":activities,"waitingActivities":waiting,"assessmentStatus":course_academy_engine::inventory::assessment_status(s,l,Utc::now())?,"queueDescription":"Assessments need five previously unassessed topics learned at least 48 hours ago. They become available at 120 practice XP and required at 150. Ordinary reviews are optional; required remediation takes precedence.","practiceNotice":"Each skill has at most five questions. Two correct answers in a row advance to the next step; two incorrect answers or skips in a row fail the lesson. After five questions without either streak, continue to the next step. If fresh questions run out sooner, you can continue and return to unfinished practice later."}),
    )
}

/// Prepare selected and recommended work without recording a presentation or clock.
/// Self-directed selections get a prepared locked task, preserving engine eligibility.
/// The caller journals this transaction and submits it with an exact basis guard.
fn queue_forms(s: &EntitySnapshot, l: u64, at: DateTime<Utc>) -> Result<Vec<Json>> {
    Ok(queue_preparation(s, l, at)?.0)
}

fn definition_forms(
    s: &EntitySnapshot,
    definition: &retrieval::Definition,
    activity: &str,
    course: Option<u64>,
) -> Result<Vec<Json>> {
    if definition.questions.is_empty() {
        return Err("Cannot prepare an empty retrieval activity".into());
    }
    let mut forms = vec![];
    let step_ids: Vec<_> = (0..definition.questions.len())
        .map(|slot| format!("{activity}-step-{slot}"))
        .collect();
    let mut record = json!({"db/id":activity,"activity/id":{"$uuid":uid()?},"activity/title":definition.title,
        "activity/type":kw(&format!("activity.type/{}",definition.kind)),
        "activity/steps":step_ids,"activity/first-step":step_ids[0],"activity/expected-seconds":definition.expected_seconds,
        "db/ensure":kw("activity/validate")});
    if let Some(topic) = definition.topic {
        record["activity/scope"] = json!(topic);
    }
    if definition.kind == "assessment" {
        record["activity/time-limit-seconds"] = json!(retrieval::ASSESSMENT_SECONDS);
    } else {
        record["activity/course"] = json!(course.ok_or("A review requires a course")?);
    }
    forms.push(record);
    for (slot, question) in definition.questions.iter().enumerate() {
        let mut record = json!({"db/id":step_ids[slot],"step/id":{"$uuid":uid()?},"step/content":question,"step/expected-seconds":if definition.kind=="assessment" {course_academy_engine::assessment_sampling::seconds(s,*question)?}else{90.0},"db/ensure":kw("step/validate")});
        if let Some(next) = step_ids.get(slot + 1) {
            record["step/next"] = json!(next);
        }
        forms.push(record);
    }
    Ok(forms)
}

fn queue_preparation(
    s: &EntitySnapshot,
    l: u64,
    at: DateTime<Utc>,
) -> Result<(Vec<Json>, Vec<learning::PlannedActivity>)> {
    // Repair older accidental opens before planning so their paused state no
    // longer puts them ahead of the learner's actual selections.
    let resets = reset_unstarted_lessons(s, l)?;
    if !resets.is_empty() {
        return Ok((resets, vec![]));
    }
    let Some(c) = s.optional_ref(l, "learner/course")? else {
        return Ok((vec![], vec![]));
    };
    let queued = learning::queue_candidates(s, l, c, at)?;
    let engine = learning::engine_candidates(s, l, c, at)?;
    let mut plan = BTreeMap::new();
    for candidate in queued.iter().cloned() {
        plan.insert(candidate.activity, (candidate, false));
    }
    for candidate in engine.iter().cloned() {
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
    let mut prepared_lessons = BTreeSet::new();
    let layers = learning::topic_layers(s)?;
    let study_topic = |topic: u64| layers.get(&topic)
        .is_some_and(|&layer| layer + 1 >= learning::MIN_STUDY_LAYER);
    let lifecycle = course_academy_engine::scheduling::lifecycle(s, l)?;
    for (&activity, &task) in &pending {
        if !matches!(
            status(s, task, "learner-task/status")?.as_str(),
            "locked" | "unlocked"
        ) {
            continue;
        }
        if let Some(topic) = s.optional_ref(activity, "activity/scope")? {
            let kind = retrieval::kind(s, activity)?;
            for (&(origin, t), required_kind) in &lifecycle.repairs {
                if t == topic
                    && required_kind == &kind
                    && !s
                        .refs(task, "learner-task/remediation-for")?
                        .contains(&origin)
                    && (kind == "lesson" || retrieval::fresh(s, l, activity)?)
                {
                    forms.push(add(
                        json!(task),
                        "learner-task/remediation-for",
                        json!(origin),
                    ));
                }
            }
        }
    }

    for task in s.refs(l, "learner/activity")? {
        if retrieval::remaining(s, task, at)? == Some(0.0) {
            forms.extend(mutate(s, l, "expire", &json!({"taskId":task}), at)?.0);
        }
    }
    for (index, definition) in retrieval::schedule(s, l, c, at)?.into_iter().enumerate() {
        let assessment_followup = definition.remediation_for.iter()
            .any(|origin| lifecycle.assessment_origin(s, *origin).unwrap_or(false));
        if definition.kind != "assessment" && !assessment_followup
            && (definition.topic.is_some_and(|topic| !study_topic(topic))
                || definition.questions.iter().any(|q| !s.topic_for_question(*q).is_ok_and(&study_topic)))
        {
            continue;
        }
        let task = format!("retrieval-task-{index}");
        if let Some(activity) = definition.existing_activity {
            prepared_lessons.insert(activity);
            if !pending.contains_key(&activity) {
                forms.push(json!({"db/id":task,"learner-task/id":{"$uuid":uid()?},"learner-task/activity":activity,"learner-task/status":kw("learner-task.status/unlocked"),"learner-task/priority":definition.priority,"learner-task/remediation-for":definition.remediation_for,"db/ensure":kw("learner-task/validate")}));
                forms.push(add(json!(l), "learner/activity", json!(task)));
            }
            continue;
        }
        let activity = format!("retrieval-activity-{index}");
        forms.extend(definition_forms(s, &definition, &activity, Some(c))?);
        if let Some(original) = definition.retake_of {
            if let Some(existing) = s.refs(l, "learner/activity")?.into_iter().find(|t| {
                s.optional_ref(*t, "learner-task/retake-of").ok().flatten() == Some(original)
                    && matches!(
                        status(s, *t, "learner-task/status").ok().as_deref(),
                        Some("locked" | "unlocked")
                    )
            }) {
                forms.push(add(
                    json!(existing),
                    "learner-task/activity",
                    json!(activity),
                ));
                forms.push(add(
                    json!(existing),
                    "learner-task/priority",
                    json!(definition.priority),
                ));
                if status(s, existing, "learner-task/status")? == "locked" {
                    forms.push(cas(
                        s,
                        existing,
                        "learner-task/status",
                        "learner-task.status/unlocked",
                    )?);
                }
                continue;
            }
        }
        let task = format!("retrieval-task-{index}");
        forms.push(json!({"db/id":task,"learner-task/id":{"$uuid":uid()?},"learner-task/activity":activity,
            "learner-task/status":kw("learner-task.status/unlocked"),"learner-task/priority":definition.priority,"db/ensure":kw("learner-task/validate")}));
        if !definition.remediation_for.is_empty() {
            for origin in definition.remediation_for {
                forms.push(add(
                    json!(task),
                    "learner-task/remediation-for",
                    json!(origin),
                ));
            }
        }
        if let Some(original) = definition.retake_of {
            forms.push(add(json!(task), "learner-task/retake-of", json!(original)));
        }
        forms.push(add(json!(l), "learner/activity", json!(task)));
    }
    let mut eligible = BTreeSet::new();
    let unavailable = learning::unavailable_questions(s, l)?;
    for (_, (candidate, engine_eligible)) in plan {
        let activity = candidate.activity;
        if retrieval::kind(s, activity)? == "lesson"
            && !pending.get(&activity).is_some_and(|t| {
                matches!(
                    status(s, *t, "learner-task/status").ok().as_deref(),
                    Some("started" | "paused")
                )
            })
            && !course_academy_engine::inventory::lesson_ready(
                s,
                &s.refs(candidate.topic, "topic/knowledge-points")?,
                &unavailable,
            )?
        {
            continue;
        }
        eligible.insert(activity);
        if prepared_lessons.contains(&activity) {
            continue;
        }
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
    let candidates = if s.entity(l)?.get("learner/self-directed") == Some(&json!(true)) {
        queued
    } else {
        engine
    };
    Ok((forms, candidates))
}
fn reset_unstarted_lessons(s: &EntitySnapshot, learner: u64) -> Result<Vec<Json>> {
    let mut forms = vec![];
    for task in s.refs(learner, "learner/activity")? {
        if status(s, task, "learner-task/status")? == "paused"
            && learning::lesson_has_no_progress(s, task)?
        {
            forms.push(cas(s, task, "learner-task/status", "learner-task.status/locked")?);
            forms.push(add(json!(task), "learner-task/priority", json!(0.0)));
        }
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

// Presentation-only field result. Reuse the engine's symbolic comparison rather
// than guessing correctness from the displayed strings in JavaScript.
fn attach_field_grade(s: &EntitySnapshot, question: u64, id: u64, field: &mut Json) {
    let submitted = if field["type"] == "blank" {
        field["response"]["value"].as_str().map(str::to_owned)
    } else if field["type"] == "free" {
        None
    } else {
        field["response"]["choiceId"]
            .as_u64()
            .map(|id| id.to_string())
    };
    if let Some(correct) =
        submitted.and_then(|value| learning::grade_field(s, question, id, &value).ok())
    {
        field["grade"] = json!(if correct { "correct" } else { "incorrect" });
    }
}

// Use the displayed content's source ID, never an authored placement or topic ID.
fn content_math_academy_id(record: &Record) -> Option<String> {
    record
        .get(if record.contains_key("tutorial/id") {
            "tutorial/math-academy-id"
        } else {
            "question/math-academy-id"
        })
        .and_then(|value| {
            value
                .as_str()
                .map(str::to_owned)
                .or_else(|| value.as_u64().map(|id| id.to_string()))
        })
}

fn knowledge_point_identity(s: &EntitySnapshot, content: u64) -> Result<Option<Json>> {
    let record = s.entity(content)?;
    Ok(record.contains_key("knowledge-point/id").then(|| {
        json!({
            "id": content,
            "title": text(s, content, "knowledge-point/title"),
        })
    }))
}

// Saved multipart presentations retain their original shared context even
// though fresh standalone practice excludes those parts. Recover the stored
// setup through reverse containment in this snapshot and its cached indexes.
fn question_markdown(s: &EntitySnapshot, question: u64) -> Result<String> {
    fn contexts(
        s: &EntitySnapshot,
        content: u64,
        ancestors: &mut BTreeSet<u64>,
    ) -> Result<BTreeSet<Vec<String>>> {
        if ancestors.len() >= 32 || !ancestors.insert(content) {
            return Err("Question context nesting must be acyclic and at most 32 levels deep".into());
        }
        let mut paths = BTreeSet::new();
        for step in s.owners(content, "step/content")? {
            for parent in s.owners(step, "multistep/steps")? {
                let context = text(s, parent, "multistep/context");
                for mut path in contexts(s, parent, ancestors)? {
                    if !context.trim().is_empty() {
                        path.push(context.trim().to_owned());
                    }
                    paths.insert(path);
                }
            }
        }
        for wrapper in s.owners(content, "assigned-problem/content")? {
            paths.extend(contexts(s, wrapper, ancestors)?);
        }
        ancestors.remove(&content);
        if paths.is_empty() {
            paths.insert(vec![]);
        }
        Ok(paths)
    }
    let problem = text(s, question, "question/problem");
    let mut paths = contexts(s, question, &mut BTreeSet::new())?;
    if paths.len() > 1 {
        paths.remove(&vec![]);
    }
    if paths.len() > 1 {
        return Err("Question has multiple different shared setups".into());
    }
    let mut parts: Vec<_> = paths.into_iter().next().unwrap_or_default().into_iter()
        .filter(|context| !problem.contains(context))
        .collect();
    parts.push(problem);
    Ok(parts.join("\n\n"))
}

fn task_step_json(
    s: &EntitySnapshot,
    steps: &[learning::LessonStep],
    i: u64,
    at: DateTime<Utc>,
) -> Result<Json> {
    task_step_json_with_elapsed(s, steps, i, Some(timing::elapsed(s, i, at)?))
}

fn task_step_json_with_elapsed(
    s: &EntitySnapshot,
    steps: &[learning::LessonStep],
    i: u64,
    elapsed: Option<f64>,
) -> Result<Json> {
    let content = s.reference(i, "task-item/content")?;
    let state = status(s, i, "task-item/status")?;
    content_step_json(s, steps, content, Some(i), &state, elapsed)
}

/// Render a question independently of whether it has a saved presentation.
/// Completed quizzes also review reserved questions the learner never opened.
fn content_step_json(
    s: &EntitySnapshot,
    steps: &[learning::LessonStep],
    content: u64,
    item: Option<u64>,
    state: &str,
    elapsed: Option<f64>,
) -> Result<Json> {
    let e = s.entity(content)?;
    let responses = item.map(|i| s.refs(i, "task-item/responses")).transpose()?.unwrap_or_default();
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
        if !matches!(kind.as_str(), "blank" | "free") {
            for ch in s.refs(f, "answer-field/choices")? {
                choices.push(json!({"id":ch,"type":status(s,ch,"answer/type")?,"value":text(s,ch,"answer/value")}));
            }
        }
        let mut field =
            json!({"id":f,"key":text(s,f,"answer-field/key"),"type":kind,"choices":choices});
        if kind == "blank" {
            field["answerType"] = json!(
                s.optional_ref(f, "answer-field/correct")?
                    .map(|correct| status(s, correct, "answer/type"))
                    .transpose()?
            );
        }
        if terminal || !responses.is_empty() {
            let selected = responses.iter().copied().find(|ch| {
                s.refs(f, "answer-field/choices")
                    .unwrap_or_default()
                    .contains(ch)
            });
            if let Some(ch) = selected {
                field["response"] = json!({"id":ch,"choiceId":ch,"type":status(s,ch,"answer/type")?,"value":text(s,ch,"answer/value"),"feedback":text(s,ch,"answer/feedback")});
            }
            if terminal {
                if let Some(correct) = s.optional_ref(f, "answer-field/correct")? {
                    field["correctAnswer"] = json!({"id":correct,"type":status(s,correct,"answer/type")?,"value":text(s,correct,"answer/value")});
                }
            }
        }
        if matches!(state, "correct" | "incorrect") {
            attach_field_grade(s, content, f, &mut field);
        }
        fields.push(field);
    }
    let markdown = if tutorial { text(s, content, "tutorial/content") } else { question_markdown(s, content)? };
    let mut step = json!({"itemId":item,"contentId":content,"kind":if tutorial{"tutorial"}else if example{"example"}else{"question"},"title":title,"markdown":markdown,"fields":fields,"status":state,"canContinue":tutorial||example||terminal,"requiresCalculator":e.get("question/requires-calculator"),"elapsedSeconds":elapsed});
    step["stepId"] = json!(authored.map(|(_, entry)| entry.step.to_string()));
    step["mathAcademyId"] = json!(content_math_academy_id(e));
    if let Some((_, entry)) = authored {
        step["knowledgePoint"] = json!(knowledge_point_identity(s, entry.content)?);
    }
    if reveal {
        step["solution"] = json!(text(s, content, "question/worked-solution"));
    }
    Ok(step)
}

fn assessment_result_step(
    s: &EntitySnapshot, steps: &[learning::LessonStep], content: u64,
    item: Option<u64>, at: DateTime<Utc>,
) -> Result<Json> {
    let recorded = item.map(|i| status(s, i, "task-item/status")).transpose()?;
    let unanswered = !matches!(recorded.as_deref(), Some("correct" | "incorrect"));
    let elapsed = item.map(|i| timing::elapsed(s, i, at)).transpose()?;
    // This is feedback for the finalized quiz, not a fabricated grading event.
    let mut step = content_step_json(s, steps, content, item,
        if unanswered { "incorrect" } else { recorded.as_deref().unwrap() }, elapsed)?;
    step["unanswered"] = json!(unanswered);
    if item.is_none() {
        step["reviewKey"] = json!(format!("assessment-question-{content}"));
    }
    Ok(step)
}

fn hide_assessment_feedback(step: &mut Json) {
    if matches!(
        step["status"].as_str(),
        Some("correct" | "incorrect" | "skipped")
    ) {
        step["status"] = json!("submitted");
    }
    if let Some(record) = step.as_object_mut() {
        record.remove("solution");
        record.remove("feedback");
    }
    if let Some(fields) = step["fields"].as_array_mut() {
        for field in fields {
            field.as_object_mut().unwrap().remove("correctAnswer");
            field.as_object_mut().unwrap().remove("grade");
            if let Some(response) = field["response"].as_object_mut() {
                response.remove("feedback");
            }
        }
    }
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
    let title = if retrieval::kind(s, a)? == "assessment" {
        QuizLabels::capture(s, l)?.title(s, a, Some(t))?
    } else { text(s, a, "activity/title") };
    let chain = items(s, t)?;
    let at = Utc::now();
    let steps = learning::lesson_steps(s, a)?;
    let progress = lesson_progress(s, &steps, &chain)?;
    let active = s
        .optional_ref(t, "learner-task/active-item")?
        .or_else(|| chain.last().copied());
    let mut step = active
        .as_ref()
        .map(|&i| task_step_json(s, &steps, i, at))
        .transpose()?
        .unwrap_or(Json::Null);
    let assessment = retrieval::kind(s, a)? == "assessment";
    let hide_feedback = assessment && !matches!(task_state.as_str(), "completed" | "failed");
    if assessment && !hide_feedback {
        if let Some(item) = active {
            step = assessment_result_step(s, &steps, s.reference(item, "task-item/content")?, Some(item), at)?;
        }
    }
    if hide_feedback && !step.is_null() {
        hide_assessment_feedback(&mut step);
    }
    let history = if include_history && assessment && !hide_feedback {
        let presentations: BTreeMap<_, _> = chain.iter().map(|&i|
            s.reference(i, "task-item/content").map(|content| (content, i))).collect::<std::result::Result<_, _>>()?;
        let mut history = vec![];
        for (index, entry) in steps.iter().enumerate() {
            let item = presentations.get(&entry.content).copied();
            if item.is_some() && item == active { continue; }
            history.push(json!({"order":index + 1,"number":index + 1,"total":steps.len(),
                "step":assessment_result_step(s, &steps, entry.content, item, at)?}));
        }
        history
    } else if include_history {
        chain
            .iter()
            .filter(|i| Some(**i) != active)
            .enumerate()
            .map(|(index, &i)| {
                let mut step = task_step_json(s, &steps, i, at)?;
                if hide_feedback {
                    hide_assessment_feedback(&mut step);
                }
                let number = authored_step(&steps, s.reference(i, "task-item/content")?)
                    .map(|(index, _)| index + 1)
                    .unwrap_or(1);
                Ok(json!({"order":index + 1,"number":number,"total":steps.len(),"step":step}))
            })
            .collect::<Result<Vec<Json>>>()?
    } else {
        vec![]
    };
    let mut view = json!({"basis":s.basis_t,"taskId":t,"activityId":a,"type":retrieval::kind(s,a)?,"learner":learner_json(s,l),"course":course_json(s,l)?,"title":title,"status":task_state,"xp":number(s,t,"learner-task/xp-earned"),"xpBase":number(s,t,"learner-task/xp-base"),"elapsedSeconds":if matches!(task_state.as_str(),"unlocked"|"locked"){number(s,t,"learner-task/elapsed-seconds")}else{timing::task_elapsed(s,t,at)?},"step":step,"progress":progress});
    if retrieval::kind(s, a)? == "review" {
        if let Some(topic) = s.optional_ref(a, "activity/scope")? {
            if let Some(id) = s.entity(topic)?.get("topic/id").and_then(|v| v.get("$uuid")) {
                view["reviewTopic"] = json!({"id":topic,"uuid":id,"title":text(s,topic,"topic/title")});
            }
        }
    }
    if assessment {
        let remaining = retrieval::remaining(s, t, at)?;
        view["remainingSeconds"] = json!(remaining);
        view["questions"]=json!(steps.iter().enumerate().map(|(index,st)|{
            let item=chain.iter().find(|i|s.optional_ref(**i,"task-item/content").ok().flatten()==Some(st.content)).copied();
            json!({"number":index+1,"questionId":st.content,"itemId":item,"answered":item.is_some_and(|i|!s.refs(i,"task-item/responses").unwrap_or_default().is_empty()),"active":item==active})
        }).collect::<Vec<_>>());
        view["progress"]["stepNumber"] = json!(
            step.get("contentId")
                .and_then(Json::as_u64)
                .and_then(|q| steps.iter().position(|st| st.content == q))
                .map(|n| n + 1)
        );
        view["expired"] = json!(remaining == Some(0.0));
        if !hide_feedback {
            let correct = chain
                .iter()
                .filter(|i| status(s, **i, "task-item/status").ok().as_deref() == Some("correct"))
                .count();
            let answered = chain
                .iter()
                .filter(|i| {
                    matches!(
                        status(s, **i, "task-item/status").ok().as_deref(),
                        Some("correct" | "incorrect")
                    )
                })
                .count();
            view["assessmentScore"] =
                json!({"correct":correct,"total":steps.len(),"unanswered":steps.len()-answered});
        }
        view["timeLimitSeconds"] = json!(number(s, a, "activity/time-limit-seconds"));
    }
    let practice = practice_state(s, a, &chain);
    if practice.is_err()
        && chain
            .iter()
            .any(|i| s.entities[i].contains_key("task-item/deferred-step"))
    {
        return Err(practice.err().unwrap());
    }
    if let Ok(practice) = practice {
        // The final answer still needs its Continue transition to pause the
        // attempt. Showing the waiting screen earlier hides that transition,
        // and Resume on an already started task cannot resume deferred work.
        let awaiting = task_state == "paused"
            && practice.next.is_none()
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
    matches!(action, "continue" | "submit" | "expire")
        && matches!(task_state, "completed" | "failed")
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
    transition_with_elapsed(s,t,i,state,elapsed,forms)
}

fn transition_with_elapsed(s:&EntitySnapshot,t:u64,i:u64,state:&str,elapsed:f64,forms:&mut Vec<Json>)->Result<()> {
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
fn assessment_drafts(s: &EntitySnapshot, item: u64) -> Result<BTreeMap<u64, String>> {
    let q = s.reference(item, "task-item/content")?;
    let responses = s.refs(item, "task-item/responses")?;
    let mut out = BTreeMap::new();
    for field in s.refs(q, "question/answer-fields")? {
        let choices = s.refs(field, "answer-field/choices")?;
        if let Some(&answer) = responses.iter().find(|answer| choices.contains(answer)) {
            out.insert(
                field,
                if matches!(
                    status(s, field, "answer-field/type")?.as_str(),
                    "blank" | "free"
                ) {
                    text(s, answer, "answer/value")
                } else {
                    answer.to_string()
                },
            );
        }
    }
    Ok(out)
}
fn save_assessment_draft(
    s: &EntitySnapshot,
    item: u64,
    responses: &Json,
    forms: &mut Vec<Json>,
) -> Result<()> {
    let q = s.reference(item, "task-item/content")?;
    let fields = s.refs(q, "question/answer-fields")?;
    let mut submitted = BTreeSet::new();
    let old: BTreeSet<_> = s.refs(item, "task-item/responses")?.into_iter().collect();
    let mut retained = BTreeSet::new();
    for r in responses.as_array().ok_or("responses must be a list")? {
        let f = required(r, "fieldId")?;
        if !fields.contains(&f) || !submitted.insert(f) {
            return Err("Draft fields must be distinct and belong to this question".into());
        }
        let kind = status(s, f, "answer-field/type")?;
        let choices = s.refs(f, "answer-field/choices")?;
        let response = if matches!(kind.as_str(), "blank" | "free") {
            let v = r["value"]
                .as_str()
                .ok_or("Entered response requires a string")?;
            if v.len() > 16000 {
                return Err("Response is too long".into());
            }
            if v.trim().is_empty() {
                continue;
            }
            let type_id = s.reference(s.reference(f, "answer-field/correct")?, "answer/type")?;
            if let Some(ch) = choices.into_iter().find(|ch| {
                text(s, *ch, "answer/value") == v
                    && s.reference(*ch, "answer/type").ok() == Some(type_id)
            }) {
                json!(ch)
            } else {
                let key = format!("draft-{item}-{f}");
                forms.push(json!({"db/id":key,"answer/id":{"$uuid":uid()?},"answer/type":type_id,"answer/value":v,"db/ensure":kw("answer/validate")}));
                forms.push(add(json!(f), "answer-field/choices", json!(key)));
                json!(key)
            }
        } else {
            let Some(ch) = r["choiceId"].as_u64() else {
                continue;
            };
            if !choices.contains(&ch) {
                return Err("Choice does not belong to this field".into());
            }
            json!(ch)
        };
        if response.as_u64().is_some_and(|r| old.contains(&r)) {
            retained.insert(response.as_u64().unwrap());
        } else {
            forms.push(add(json!(item), "task-item/responses", response));
        }
    }
    for removed in old.difference(&retained) {
        forms.push(json!([
            kw("db/retract"),
            item,
            kw("task-item/responses"),
            removed
        ]));
    }
    Ok(())
}
fn assessment_mutate(
    s: &EntitySnapshot,
    l: u64,
    t: u64,
    action: &str,
    body: &Json,
    at: DateTime<Utc>,
) -> Result<(Vec<Json>, Json)> {
    let a = s.reference(t, "learner-task/activity")?;
    let st = status(s, t, "learner-task/status")?;
    let chain = items(s, t)?;
    retrieval::position(s, a, &chain)?;
    let active = s
        .optional_ref(t, "learner-task/active-item")?
        .or_else(|| chain.last().copied())
        .ok_or("Assessment has no active presentation")?;
    if !chain.contains(&active) {
        return Err("Active assessment item does not belong to its task".into());
    }
    let expired = retrieval::remaining(s, t, at)? == Some(0.0);
    let mut forms = vec![];
    if matches!(st.as_str(), "completed" | "failed") {
        return Ok((forms, json!({"taskId":t})));
    }
    if matches!(action, "submit" | "expire") {
        if action == "expire" && !expired {
            return Err("Assessment has not reached its deadline".into());
        }
        if action == "submit" && expired {
            return Err("Assessment deadline has elapsed".into());
        }
        if !matches!(st.as_str(), "started" | "paused") {
            return Err("Start the assessment before submitting".into());
        }
        // Submission can include the current draft; grade it in a prospective
        // snapshot while publishing its saved answers in the same transaction.
        let mut prospective = s.clone();
        if let Some(responses) = body.get("responses") {
            if action == "submit" {
                save_assessment_draft(s, active, responses, &mut forms)?;
                let q = s.reference(active, "task-item/content")?;
                let mut submitted = BTreeMap::new();
                for r in responses.as_array().ok_or("responses must be a list")? {
                    if let Some(f) = r["fieldId"].as_u64() {
                        if let Some(v) = r["value"].as_str().filter(|v| !v.trim().is_empty()) {
                            submitted.insert(f, v.to_owned());
                        } else if let Some(v) = r["choiceId"].as_u64() {
                            submitted.insert(f, v.to_string());
                        }
                    }
                }
                let _ = q;
                // Explicit submitted values avoid resolving transaction tempids.
                prospective
                    .entities
                    .get_mut(&active)
                    .unwrap()
                    .insert("draft-final-values".into(), json!(submitted));
            }
        }
        let mut results = vec![];
        let mut correct = 0;
        let mut elapsed = 0.0;
        for &item in &chain {
            let q = s.reference(item, "task-item/content")?;
            let draft = if let Some(v) = prospective.entities[&item].get("draft-final-values") {
                serde_json::from_value::<BTreeMap<u64, String>>(v.clone())?
            } else {
                assessment_drafts(s, item)?
            };
            let fields = s.refs(q, "question/answer-fields")?;
            let complete = fields.iter().all(|f| draft.contains_key(f)) && !fields.is_empty();
            let item_state = status(s, item, "task-item/status")?;
            let measured_at = if expired {
                timing::task_started(s, t)?
                    + chrono::Duration::milliseconds(
                        (number(s, a, "activity/time-limit-seconds") * 1000.0) as i64,
                    )
            } else {
                at
            };
            let seconds = timing::elapsed(s, item, measured_at)?;
            elapsed += seconds;
            if matches!(item_state.as_str(), "correct" | "incorrect") {
                // Legacy partially submitted attempts retain their recorded results.
                correct += usize::from(item_state == "correct");
                continue;
            }
            if complete {
                let passed = learning::grade(s, q, &draft)?;
                correct += usize::from(passed);
                results.push((q, passed));
                forms.push(cas(
                    s,
                    item,
                    "task-item/status",
                    if passed {
                        "task-item.status/correct"
                    } else {
                        "task-item.status/incorrect"
                    },
                )?);
            } else if item_state == "started" {
                forms.push(cas(s, item, "task-item/status", "task-item.status/paused")?);
            }
            forms.push(add(
                json!(item),
                "task-item/elapsed-seconds",
                json!(seconds),
            ));
        }
        let total = learning::lesson_steps(s, a)?.len();
        let xp = course_academy_engine::activities::earned_xp(
            "assessment",
            number(s, t, "learner-task/xp-base") as i64,
            correct,
            total,
            None,
        )?;
        forms.push(add(
            json!(t),
            "learner-task/elapsed-seconds",
            json!(elapsed),
        ));
        forms.push(add(
            json!(t),
            "learner-task/xp-earned",
            json!(xp.to_string().parse::<i64>()?),
        ));
        forms.push(cas(
            s,
            t,
            "learner-task/status",
            "learner-task.status/completed",
        )?);
        forms.extend(retrieval::assessment_credit(
            s,
            l,
            &results,
            &format!("assessment-{t}"),
            at,
        )?);
        return Ok((forms, json!({"taskId":t})));
    }
    if expired && action != "pause" {
        return Err("Assessment deadline has elapsed".into());
    }
    if matches!(action, "pause" | "resume") {
        if action == "pause" && !expired && st == "started" {
            if let Some(responses) = body.get("responses").filter(|v| !v.is_null()) {
                save_assessment_draft(s, active, responses, &mut forms)?;
            }
        }
        let target = if action == "pause" {
            "paused"
        } else {
            "started"
        };
        if st == target {
            return Ok((forms, json!({"taskId":t})));
        }
        if action == "resume" {
            pause_other_lessons(s, l, Some(t), at, &mut forms)?;
        }
        transition(s, t, active, target, at, &mut forms)?;
        forms.push(cas(
            s,
            t,
            "learner-task/status",
            &format!("learner-task.status/{target}"),
        )?);
        return Ok((forms, json!({"taskId":t})));
    }
    if st != "started" {
        return Err("Resume the lesson before continuing".into());
    }
    if action == "draft" || action == "navigate" {
        if body
            .get("itemId")
            .and_then(Json::as_u64)
            .is_some_and(|i| i != active)
        {
            return Err(
                "Draft belongs to a different active question; refresh before editing".into(),
            );
        }
        if let Some(responses) = body.get("responses") {
            save_assessment_draft(s, active, responses, &mut forms)?;
        }
        if action == "navigate" {
            let q = required(body, "questionId")?;
            if !learning::lesson_steps(s, a)?
                .iter()
                .any(|st| st.content == q)
            {
                return Err("Question is outside the reserved assessment".into());
            }
            if s.reference(active, "task-item/content")? != q {
                if status(s, active, "task-item/status")? == "started" {
                    transition(s, t, active, "paused", at, &mut forms)?;
                }
                if let Some(&item) = chain
                    .iter()
                    .find(|i| s.optional_ref(**i, "task-item/content").ok().flatten() == Some(q))
                {
                    if status(s, item, "task-item/status")? == "paused" {
                        forms.push(cas(
                            s,
                            item,
                            "task-item/status",
                            "task-item.status/started",
                        )?);
                    }
                    forms.push(add(json!(t), "learner-task/active-item", json!(item)));
                } else {
                    // Reserved legacy routes may predate practice eligibility
                    // rules. Saved presentations remain usable; new ones must
                    // still be standalone questions.
                    learning::validate_practice_question(s, q)?;
                    append_item(json!(t), chain.last().copied(), q, &mut forms)?;
                    forms.push(add(json!(t), "learner-task/active-item", json!("new-item")));
                }
            }
        }
        return Ok((forms, json!({"taskId":t})));
    }
    Err("Assessment answers are drafts until whole-assessment Submit or expiry".into())
}

fn mutate(
    s: &EntitySnapshot,
    l: u64,
    action: &str,
    body: &Json,
    at: DateTime<Utc>,
) -> Result<(Vec<Json>, Json)> {
    mutate_with_selection(s, l, action, body, at, None)
}

fn mutate_with_selection(
    s: &EntitySnapshot,
    l: u64,
    action: &str,
    body: &Json,
    at: DateTime<Utc>,
    selected_topic: Option<u64>,
) -> Result<(Vec<Json>, Json)> {
    if matches!(
        action,
        "start" | "resume" | "study-topic" | "assignment-focus" | "assignment-answer"
    ) {
        let requested = body["activityId"]
            .as_u64()
            .or_else(|| {
                body["taskId"]
                    .as_u64()
                    .and_then(|t| s.reference(t, "learner-task/activity").ok())
            })
            .or_else(|| {
                body["topicId"]
                    .as_u64()
                    .and_then(|t| topic_lesson(s, t).ok())
            });
        // Explicit topic study is independent of queue priority. Resuming a
        // lesson or review must preserve that choice after leaving the page.
        let explicit_study = selected_topic.is_some()
            || action == "study-topic"
            || (action == "resume"
                && requested.is_some_and(|activity| {
                    matches!(retrieval::kind(s, activity).ok().as_deref(), Some("lesson" | "review"))
                }));
        if !explicit_study {
            let plan = learning::study_candidates(s, l, course(s, l)?, at)?;
            let gated = plan.iter().any(|p| p.priority >= 11000.0);
            if gated && requested.is_none_or(|a| !plan.iter().any(|p| p.activity == a)) {
                return Err("Complete the required activity before starting unrelated study".into());
            }
        }
        if let Some(a) = requested {
            check_lesson_retry(s, l, a)?;
        }
    }
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
    if action == "daily-xp-goal" {
        let goal = body["dailyXpGoal"].as_i64().filter(|n| *n > 0 && *n <= 9_007_199_254_740_991)
            .ok_or("Daily XP goal must be a positive whole number")?;
        forms.push(json!([kw("db/cas"), l, kw("learner/daily-xp-goal"), s.entity(l)?.get("learner/daily-xp-goal").cloned().unwrap_or(Json::Null), goal]));
        return Ok((forms, json!({"goal":true})));
    }
    if action == "profile-settings" {
        let requested = body["courseId"].as_str().ok_or("courseId is required")?;
        let selected = s
            .entities
            .with_attribute("course/id")
            .into_iter()
            .find(|id| {
                s.entities[id]
                    .get("course/id")
                    .and_then(|v| v.get("$uuid"))
                    .and_then(Json::as_str)
                    == Some(requested)
            })
            .ok_or("Selected course does not exist")?;
        let directed = body["selfDirected"]
            .as_bool()
            .ok_or("selfDirected must be a boolean")?;
        let old_directed = learner_json(s, l)["selfDirected"] == true;
        if s.optional_ref(l, "learner/course")? != Some(selected) || old_directed != directed {
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
    if action == "regenerate-assessment" {
        let activity = required(body, "activityId")?;
        let task = task_for(s, l, activity)?.ok_or("No unfinished assessment belongs to this learner")?;
        owned(s, l, task)?;
        if retrieval::kind(s, activity)? != "assessment"
            || s.optional_ref(task, "learner-task/retake-of")?.is_some()
        {
            return Err("Only an ordinary assessment can be regenerated".into());
        }
        let task_state = status(s, task, "learner-task/status")?;
        let previously_started = s.status_history.iter().any(|event| {
            event.entity == task && event.attribute == "learner-task/status"
                && s.ident(&event.value).ok().is_some_and(|state|
                    !matches!(state.as_str(), "learner-task.status/locked" | "learner-task.status/unlocked"))
        });
        if !matches!(task_state.as_str(), "locked" | "unlocked")
            || previously_started || !items(s, task)?.is_empty()
            || s.optional_ref(task, "learner-task/active-item")?.is_some()
            || number(s, task, "learner-task/elapsed-seconds") != 0.0
            || s.entity(task)?.contains_key("learner-task/xp-earned")
            || s.entity(task)?.contains_key("learner-task/finished-at")
        {
            return Err("Only a never-started assessment can be regenerated".into());
        }
        let pools = retrieval::assessment_pools(s, l, at)?;
        let definition = retrieval::assessment_definition(s, l, at)?
            .ok_or("Assessment needs five eligible topics not previously assessed")?;
        let replacement = "regenerated-assessment";
        forms.extend(definition_forms(s, &definition, replacement, None)?);
        // Preserve the previous immutable route and atomically move this unstarted task.
        forms.push(json!([kw("db/cas"),task,kw("learner-task/activity"),activity,replacement]));
        forms.push(add(json!(task), "learner-task/xp-base", json!(base_xp::duration_base(definition.expected_seconds)?)));
        forms.push(json!([kw("db/ensure"),task,kw("learner-task/validate")]));
        return Ok((forms, json!({"taskId":task,"regeneration":{
            "previousActivityId":activity,"eligibleTopicIds":pools.keys().collect::<Vec<_>>(),
            "eligibleTopicCount":pools.len(),"questionCount":definition.questions.len(),
            "expectedSeconds":definition.expected_seconds
        }})));
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
    if action == "review-topic" {
        let topic = required(body, "topicId")?;
        let definition = match topic_review_plan(s, l, topic, at)? {
            TopicReviewPlan::Existing { task, activity, state } => {
                return match state.as_str() {
                    "started" => Ok((forms, json!({"taskId":task}))),
                    "paused" => mutate_with_selection(s, l, "resume", &json!({"taskId":task}), at, Some(topic)),
                    _ => mutate_with_selection(s, l, "start", &json!({"activityId":activity}), at, Some(topic)),
                };
            }
            TopicReviewPlan::New(definition) => definition,
        };
        pause_other_lessons(s, l, None, at, &mut forms)?;
        forms.extend(definition_forms(s, &definition, "review-activity", Some(course(s, l)?))?);
        let id = uid()?;
        forms.push(json!({"db/id":"new-task","learner-task/id":{"$uuid":id},"learner-task/activity":"review-activity",
            "learner-task/status":kw("learner-task.status/started"),"learner-task/priority":definition.priority,
            "learner-task/elapsed-seconds":0.0,"learner-task/xp-base":base_xp::duration_base(definition.expected_seconds)?,
            "learner-task/xp-earned":0,"learner-task/remediation-for":definition.remediation_for,"db/ensure":kw("learner-task/validate")}));
        forms.push(add(json!(l), "learner/activity", json!("new-task")));
        append_item(json!("new-task"), None, definition.questions[0], &mut forms)?;
        return Ok((forms, json!({"taskUuid":id})));
    }
    if action == "study-topic" {
        let topic = required(body, "topicId")?;
        let activity = topic_lesson(s, topic)?;
        // A finished lesson is available for review through its saved attempt.
        // Keep unfinished attempts resumable and never regrade completed work.
        if task_for(s, l, activity)?.is_none() && !retrieval::relearn_topics(s, l)?.contains(&topic)
        {
            if let Some(task) = completed_task_for(s, l, activity)? {
                return Ok((forms, json!({"taskId":task})));
            }
        }
        // Explicit study uses the manual selection rules without persisting a
        // queue membership, preference change, or engine unlock. Starting and
        // resuming still use the same guarded, replayable lesson lifecycle.
        return mutate_with_selection(s, l, "start", &json!({"activityId":activity}), at, Some(topic));
    }
    if action == "start" {
        let a = required(body, "activityId")?;
        if retrieval::kind(s, a)? == "assessment"
            && !(number(s, a, "activity/time-limit-seconds").is_finite()
                && number(s, a, "activity/time-limit-seconds") > 0.0)
        {
            return Err("Assessment requires a positive wall-clock time limit".into());
        }
        let existing = task_for(s, l, a)?;
        if let Some(task) = existing {
            if retrieval::remaining(s, task, at)? == Some(0.0) {
                return mutate(s, l, "expire", &json!({"taskId":task}), at);
            }
            match status(s, task, "learner-task/status")?.as_str() {
                "paused" => return mutate_with_selection(s, l, "resume", &json!({"taskId":task}), at, selected_topic),
                "started" => {
                    pause_other_lessons(s, l, Some(task), at, &mut forms)?;
                    return Ok((forms, json!({"taskId":task})));
                }
                _ => {}
            }
        }
        check_activity_start(s, l, a, selected_topic, at)?;
        if let Some(t) = existing {
            let state = status(s, t, "learner-task/status")?;
            if matches!(state.as_str(), "locked" | "unlocked") {
                pause_other_lessons(s, l, Some(t), at, &mut forms)?;
                let chain = items(s, t)?;
                if !chain.is_empty() && !learning::lesson_has_no_progress(s, t)? {
                    return Err("An unstarted task cannot contain completed work".into());
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
                if let Some(&item) = chain.last() {
                    // Reuse the saved presentation and its timing checkpoint.
                    transition(s, t, item, "started", at, &mut forms)?;
                } else {
                    let content = learning::first_content(s, a, l)?.ok_or("Lesson has no available content")?;
                    append_item(json!(t), None, content, &mut forms)?;
                }
                if retrieval::kind(s, a)? == "assessment" {
                    forms.push(add(json!(t), "learner-task/active-item", json!("new-item")));
                }
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
        if retrieval::kind(s, a)? == "assessment" {
            forms.push(add(
                json!("new-task"),
                "learner-task/active-item",
                json!("new-item"),
            ));
        }
        return Ok((forms, json!({"taskUuid":id})));
    }
    let t = required(body, "taskId")?;
    owned(s, l, t)?;
    let a = s.reference(t, "learner-task/activity")?;
    if status(s, a, "activity/type")? == "assignment" {
        return Err("Use the assignment question controls for this task".into());
    }
    let state = status(s, t, "learner-task/status")?;
    if retrieval::kind(s, a)? == "lesson" && matches!(state.as_str(), "locked" | "unlocked") {
        if action == "pause" {
            return Ok((forms, json!({"taskId":t})));
        }
        if action == "resume" {
            return mutate_with_selection(s, l, "start", &json!({"activityId":a}), at, selected_topic.or(s.optional_ref(a, "activity/scope")?));
        }
    }
    if retrieval::kind(s, a)? == "assessment" {
        return assessment_mutate(s, l, t, action, body, at);
    }
    let chain = items(s, t)?;
    if retrieval::supported(s, a)? {
        retrieval::position(s, a, &chain)?;
    }
    let i = *chain.last().ok_or("Task has no presentation")?;
    let item_state = status(s, i, "task-item/status")?;
    let content = s.reference(i, "task-item/content")?;
    let terminal = timing::terminal(&format!("task-item.status/{item_state}"));
    let assessment_remaining = retrieval::remaining(s, t, at)?;
    if action == "expire" {
        if matches!(state.as_str(), "completed" | "failed") {
            return Ok((forms, json!({"taskId":t})));
        }
        if assessment_remaining != Some(0.0) {
            return Err("Assessment has not reached its deadline".into());
        }
        // Unanswered/unpresented questions affect the score denominator only.
        // They are never converted into fabricated wrong-answer observations.
        if item_state == "started" {
            transition(s, t, i, "paused", at, &mut forms)?;
        }
        forms.push(cas(
            s,
            t,
            "learner-task/status",
            "learner-task.status/completed",
        )?);
        forms.push(add(
            json!(t),
            "learner-task/xp-earned",
            json!(retrieval::xp(
                s,
                a,
                &chain,
                number(s, t, "learner-task/xp-base") as i64
            )?),
        ));
        return Ok((forms, json!({"taskId":t})));
    }
    if assessment_remaining == Some(0.0) && action != "pause" {
        return Err("Assessment deadline has elapsed".into());
    }
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
        let reset = action == "pause" && learning::lesson_has_no_progress(s, t)?;
        if state == target && !reset || matches!(state.as_str(), "completed" | "failed") {
            return Ok((forms, json!({"taskId":t})));
        }
        if !matches!(state.as_str(), "started" | "paused") {
            return Err("Task cannot change running state".into());
        }
        if !terminal && item_state != target {
            transition(s, t, i, target, at, &mut forms)?;
        }
        forms.push(cas(
            s,
            t,
            "learner-task/status",
            &format!("learner-task.status/{}", if reset { "locked" } else { target }),
        )?);
        if reset {
            forms.push(add(json!(t), "learner-task/priority", json!(0.0)));
        }
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
        if action == "skip" {
            if !retrieval::supported(s, a)? || instruction {
                return Err("Skip is available only for retrieval questions".into());
            }
            if !terminal {
                transition(s, t, i, "skipped", at, &mut forms)?;
            }
        } else if action == "answer" {
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
                    let type_id =
                        s.reference(s.reference(f, "answer-field/correct")?, "answer/type")?;
                    let existing = choices.into_iter().find(|ch| {
                        text(s, *ch, "answer/value") == v
                            && s.reference(*ch, "answer/type").ok() == Some(type_id)
                    });
                    let response = if let Some(ch) = existing {
                        json!(ch)
                    } else {
                        let key = format!("response-{f}");
                        forms.push(json!({"db/id":key,"answer/id":{"$uuid":uid()?},"answer/type":type_id,"answer/value":v,"db/ensure":kw("answer/validate")}));
                        forms.push(add(json!(f), "answer-field/choices", json!(key)));
                        forms.push(json!([kw("db/ensure"), f, kw("answer-field/validate")]));
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
            let grading=Instant::now();
            let correct = learning::grade(s, content, &submitted)?;
            trace("grade",grading);
            for response in response_refs {
                forms.push(add(json!(i), "task-item/responses", response));
            }
            let answered_state=if correct {"correct"}else{"incorrect"};
            if let Some(millis)=body["submittedAt"].as_i64().filter(|_|body.get("_queuedReview").is_none()) {
                let until=DateTime::from_timestamp_millis(millis).ok_or("Invalid submission instant")?;
                let elapsed=timing::elapsed_until(s,i,at,until)?;
                transition_with_elapsed(s,t,i,answered_state,elapsed,&mut forms)?;
                forms.push(add(json!(i),"task-item/working-ended-at",json!({"$instant":millis})));
            }else {
                transition(s,t,i,answered_state,at,&mut forms)?;
            }
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
                if s.entity(next)?.contains_key("question/id") && !s.is_example(next) {
                    learning::validate_practice_question(s, next)?;
                }
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
    fn record_queue_offer(&mut self, mut view: Json, request: &str) -> Result<Json> {
        let l = self.learner_eid;
        let journal = PathBuf::from(std::env::var("LEARNING_REQUEST_DIR")?)
            .join(format!("{}-{request}-offers.json", self.learner));
        let saved = if journal.exists() {
            serde_json::from_slice::<Json>(&std::fs::read(&journal)?)?
        } else {
            let s = &self.snapshot;
            let h = course_academy_engine::scheduling::lifecycle(s, l)?;
            let at = Utc::now();
            let mut forms = vec![];
            for activity in view["activities"]
                .as_array()
                .ok_or("Queue activities must be a list")?
            {
                if activity["type"] != "lesson" {
                    continue;
                }
                let Some(task) = activity["taskId"].as_u64() else {
                    continue;
                };
                if !s.refs(task, "learner-task/remediation-for")?.is_empty() {
                    continue;
                }
                let previous = s
                    .entity(task)?
                    .get("learner-task/offered-at")
                    .and_then(|v| schema::parse_instant(v).ok());
                if previous.is_none()
                    || h.finished.iter().any(|f| {
                        f.kind == "review"
                            && f.at > previous.unwrap()
                            && s.refs(f.task, "learner-task/remediation-for")
                                .unwrap_or_default()
                                .is_empty()
                    })
                {
                    forms.push(add(
                        json!(task),
                        "learner-task/offered-at",
                        json!({"$instant":at.to_rfc3339()}),
                    ));
                }
            }
            if forms.is_empty() {
                return Ok(view);
            }
            let saved = json!({"edn":schema::edn(&json!(forms))?,"basis":s.basis_t,"at":at.timestamp_millis(),"source":ENGINE_SOURCE,"view":view});
            let staging = journal.with_extension("tmp");
            let mut file = std::fs::File::create(&staging)?;
            file.write_all(&serde_json::to_vec(&saved)?)?;
            file.sync_all()?;
            std::fs::rename(staging, &journal)?;
            std::fs::File::open(journal.parent().unwrap())?.sync_all()?;
            saved
        };
        let tx = TransactionRequest::from_edn(
            format!("learning-{}-{request}-offers", self.learner),
            saved["edn"].as_str().unwrap(),
            saved_request_source(&saved, l)?,
        )?
        .comparing_basis(saved["basis"].as_u64().unwrap())
        .with_tx_instant(saved["at"].as_i64().unwrap());
        let committed = self
            .conn
            .transact_socket(&self.endpoint, tx, Duration::from_secs(30))?;
        let db = self
            .conn
            .sync_to(committed.basis_t, Duration::from_secs(10))?;
        self.adopt(db)?;
        view = saved["view"].clone();
        view["basis"] = json!(self.snapshot.basis_t);
        Ok(view)
    }

    fn process(&mut self, body: &Json) -> Result<Json> {
        let action = body["action"].as_str().ok_or("Action required")?;
        if body["action"] == "persist-review" { return review_interaction::persist(self,body); }
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
                .with_attribute("learner/id")
                .into_iter()
                .find(|eid| {
                    s.entities[eid].get("learner/id").and_then(Json::as_str) == Some(learner)
                })
                .ok_or("Learner not found")?;
        }
        let l = self.learner_eid;
        if matches!(action,"review-session"|"review-grade"|"review-skip"|"review-decision") {return review_interaction::read(s,l,body);}
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
        if action == "inventory" {
            return Ok(
                json!({"basis":s.basis_t,"lineage":self.reference.key().lineage_id().to_string(),"assessmentStatus":course_academy_engine::inventory::assessment_status(s,l,Utc::now())?,"qualifyingTopics":course_academy_engine::inventory::triggers(s,l,Utc::now())?.keys().copied().collect::<Vec<_>>(),"jobs":course_academy_engine::inventory::requests(s,l,Utc::now())?}),
            );
        }
        if action == "home" {
            return home(&s, l);
        }
        if action == "profile" {
            return profile_json(s, l);
        }
        if action == "topic-study-availability" {
            return Ok(topic_study_availability(s, l, required(body, "topicId")?, Utc::now()));
        }
        if action == "learner" {
            return Ok(json!({"basis":s.basis_t,"learner":learner_json(s,l)}));
        }
        if action == "activity-history" {
            return activity_history::list(s, l, body);
        }
        if action == "activity-history-detail" {
            return activity_history::detail(s, l, required(body, "taskId")?);
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
                    && s.len() <= 128
                    && s.chars().all(|c| c.is_ascii_alphanumeric() || c == '-')
            })
            .ok_or("A stable requestId is required")?;
        let journal = PathBuf::from(std::env::var("LEARNING_REQUEST_DIR")?)
            .join(format!("{learner}-{request}.json"));
        let cached_queue = if action == "queue"
            && reset_unstarted_lessons(s, l)?.is_empty()
        {
            self.cached_home(true)
        } else {
            None
        };
        let mut planned_candidates = None;
        let saved: Json = if journal.exists() {
            let saved: Json = serde_json::from_slice(&std::fs::read(&journal)?)?;
            if saved["input"] != *body {
                return Err("requestId was already used for a different request".into());
            }
            saved
        } else {
            let at = Utc::now();
            let planning = Instant::now();
            let (mut forms, result) = if action == "queue" {
                let forms = if cached_queue.is_some() {
                    vec![]
                } else {
                    let (mut forms, candidates) = queue_preparation(s, l, at)?;
                    if body["background"] == true {
                        forms.retain(|f| f.get(2) != Some(&kw("learner-task/offered-at")));
                    }
                    if forms.is_empty() {
                        planned_candidates = Some(candidates);
                    }
                    forms
                };
                let expired = s
                    .refs(l, "learner/activity")?
                    .into_iter()
                    .any(|t| retrieval::remaining(s, t, at).ok().flatten() == Some(0.0));
                (forms, json!({"queue":true,"expired":expired,"resetUnstarted":!reset_unstarted_lessons(s,l)?.is_empty()}))
            } else {
                mutate(&s, l, action, &body, at)?
            };
            review_interaction::attach_periods(s,l,body,&mut forms)?;
            trace("plan", planning);
            let saved = json!({"input":body,"edn":schema::edn(&json!(forms))?,"basis":s.basis_t,"at":at.timestamp_millis(),"result":result,"empty":forms.is_empty(),"source":ENGINE_SOURCE});
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
                saved_request_source(&saved, l)?,
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
        if matches!(action, "target" | "queue-topic" | "daily-xp-goal") {
            return Ok(json!({"basis":s.basis_t,"learner":learner_json(s,l)}));
        }
        if action == "queue" {
            if result["resetUnstarted"] == true {
                let mut next = body.clone();
                next["requestId"] = json!(format!("{request}-unstarted"));
                return self.process(&next);
            }
            if result["expired"] == true {
                let mut next = body.clone();
                next["requestId"] = json!(format!("{request}-expiry"));
                return self.process(&next);
            }
            if saved["empty"] == true {
                if let Some(view) = cached_queue {
                    return if body["background"] == true { Ok(view) } else { self.record_queue_offer(view, request) };
                }
            }
            let view = home_with_candidates(s, l, planned_candidates)?;
            return if body["background"] == true {
                Ok(view)
            } else {
                self.record_queue_offer(view, request)
            };
        }
        let t = if let Some(t) = result["taskId"].as_u64() {
            t
        } else {
            let id = result["taskUuid"].as_str().ok_or("Missing task result")?;
            s.entities
                .with_attribute("learner-task/id")
                .into_iter()
                .find(|e| s.entities[e].get("learner-task/id") == Some(&json!({"$uuid":id})))
                .ok_or("Committed task unavailable")?
        };
        // Task evidence commits first. Intermediate steps return immediately;
        // completion refreshes availability with a separate replayable request.
        let queue_error =
            if body["_deferQueue"] != true && needs_queue_refresh(action, &status(&self.snapshot, t, "learner-task/status")?) {
                let request = format!("queue-after-{l}-{}", self.snapshot.basis_t);
                // Retain the freshly computed home at its new basis. Calling
                // process directly discarded it and forced Home to plan again.
                self.handle(json!({"action":"queue","background":true,"requestId":request}))
                    .err()
            } else {
                None
            };
        let mut view = task_json_view(
            &self.snapshot,
            l,
            t,
            matches!(action, "start" | "study-topic" | "review-topic" | "resume")
                || retrieval::kind(
                    &self.snapshot,
                    self.snapshot.reference(t, "learner-task/activity")?,
                )? == "assessment"
                    && matches!(
                        status(&self.snapshot, t, "learner-task/status")?.as_str(),
                        "completed" | "failed"
                    ),
        )?;
        if action == "regenerate-assessment" {
            view["regeneration"] = saved["result"]["regeneration"].clone();
        }
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
            let mut code = if error.to_string() == "Assessment deadline has elapsed" {
                "assessment-expired"
            } else if error.to_string().starts_with("Lesson needs at least five fresh, gradable questions per skill:") {
                "lesson-supply-shortage"
            } else if error.to_string() == "Resume the lesson before continuing" {
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
    if endpoint == "--pages" && serve {
        return page_reader::serve(database, learner);
    }
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
    fn inventory_cache_expires_before_review_and_assessment_eligibility_boundaries() {
        let now=Utc::now();
        let before=now-chrono::Duration::hours(48)+chrono::Duration::seconds(3);
        let past=now-chrono::Duration::hours(49);
        assert_eq!(inventory_cache_duration(Duration::from_secs(60),[past].into_iter(),now),Duration::from_secs(10));
        let boundary=inventory_cache_duration(Duration::from_secs(60),[before].into_iter(),now);
        assert!(boundary.as_secs_f64()>2.99 && boundary.as_secs_f64()<3.0);
        assert_eq!(inventory_cache_duration(Duration::from_secs(1),[before].into_iter(),now),Duration::from_secs(1));
        assert_eq!(inventory_cache_duration(Duration::ZERO,[past].into_iter(),now),Duration::ZERO);
        assert_eq!(inventory_cache_duration(Duration::from_secs(60),[now-chrono::Duration::hours(48)].into_iter(),now),Duration::ZERO);
    }

    #[test]
    fn home_cache_accepts_zero_memory_and_expires_before_retention_changes() {
        let now = Utc::now();
        let records = BTreeMap::from([
            (1, json!({"learner/knowledge-profile":[2]}).as_object().unwrap().clone()),
            (2, json!({"progress/learned":true,"progress/policy":3,"progress/memory":0.0,
                "progress/memory-at":schema::instant_value(now-chrono::Duration::days(1)),
                "progress/interval-days":1.0}).as_object().unwrap().clone()),
            (3, json!({"policy/review-threshold":0.5}).as_object().unwrap().clone()),
        ]);
        let mut s = EntitySnapshot::new(records, 42).unwrap();
        assert_eq!(home_cache_duration(&s, 1, now), Duration::from_secs(60));
        s.entities.get_mut(&2).unwrap().insert("progress/memory".into(), json!(1.0));
        s.entities.get_mut(&2).unwrap().insert("progress/memory-at".into(), schema::instant_value(now-chrono::Duration::days(1)+chrono::Duration::seconds(3)));
        let lifetime = home_cache_duration(&s, 1, now).as_secs_f64();
        assert!(lifetime > 2.99 && lifetime < 3.0, "{lifetime}");
        // A future observation is also an eligibility boundary for zero memory.
        s.entities.get_mut(&2).unwrap().insert("progress/memory".into(), json!(0.0));
        s.entities.get_mut(&2).unwrap().insert("progress/memory-at".into(), schema::instant_value(now+chrono::Duration::seconds(3)));
        let lifetime = home_cache_duration(&s, 1, now).as_secs_f64();
        assert!(lifetime > 2.99 && lifetime < 3.0, "{lifetime}");
        s.entities.get_mut(&2).unwrap().insert("progress/memory".into(), json!(-1.0));
        assert_eq!(home_cache_duration(&s, 1, now), Duration::ZERO);
    }

    #[test]
    fn request_journals_preserve_their_source_across_exact_retries() {
        assert!(matches!(
            saved_request_source(&json!({"source":ENGINE_SOURCE}), 42).unwrap(),
            EntityRef::Ident(ident) if ident.qualified_name() == ENGINE_SOURCE
        ));
        assert!(matches!(
            saved_request_source(&json!({"edn":"[]"}), 42).unwrap(),
            EntityRef::Id(42)
        ));
        assert!(saved_request_source(&json!({"source":"person/other"}), 42).is_err());
    }

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
        let prefixed = json!({"question/id":"q", "question/math-academy-id":"q-456"});
        assert_eq!(
            content_math_academy_id(prefixed.as_object().unwrap()).as_deref(),
            Some("q-456")
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

    #[test]
    #[ignore = "read-only admission check against the configured live database"]
    fn live_lesson_admission_without_recording() -> Result<()> {
        let topic=std::env::var("LESSON_TEST_TOPIC")?.parse::<u64>()?;
        let database=std::env::var("EDB_DATABASE")?;
        let learner=std::env::var("LESSON_TEST_LEARNER")?;
        let app=Application::connect(database,learner,std::env::var("EDB_ENDPOINT")?)?;
        let s=&app.snapshot;
        let unavailable=learning::unavailable_questions(s,app.learner_eid)?;
        let kps=s.refs(topic,"topic/knowledge-points")?;
        assert!(course_academy_engine::inventory::lesson_ready(s,&kps,&unavailable)?);
        let (forms,result)=mutate(s,app.learner_eid,"study-topic",&json!({"topicId":topic}),Utc::now())?;
        assert!(!forms.is_empty() || result.get("taskId").is_some());
        println!("Topic {topic} can start at basis {}; {} proposed forms, no writes",s.basis_t,forms.len());
        Ok(())
    }

    #[test]
    fn saved_questions_and_items_include_their_shared_function() -> Result<()> {
        let s = EntitySnapshot::new(BTreeMap::from([
            (1, json!({"question/id":"part","question/problem":"Calculate $f'(x)$.\n\n$f'(x)={{field-1}}$"}).as_object().unwrap().clone()),
            (2, json!({"step/content":1}).as_object().unwrap().clone()),
            (3, json!({"multistep/context":"Consider $f(x)=-x^3-3x^2+24x-7$.","multistep/steps":[2]}).as_object().unwrap().clone()),
            (4, json!({"task-item/content":1,"task-item/status":5}).as_object().unwrap().clone()),
            (5, json!({"db/ident":kw("task-item.status/started")}).as_object().unwrap().clone()),
        ]), 10)?;
        let before = s.entities.clone();
        let expected = "Consider $f(x)=-x^3-3x^2+24x-7$.\n\nCalculate $f'(x)$.\n\n$f'(x)={{field-1}}$";
        assert_eq!(question_markdown(&s, 1)?, expected);
        assert_eq!(task_step_json_with_elapsed(&s, &[], 4, None)?["markdown"], expected);
        assert_eq!(s.entities, before);
        Ok(())
    }

    #[test]
    fn shared_question_setup_is_ordered_deduplicated_and_never_guessed() -> Result<()> {
        let mut s = EntitySnapshot::new(BTreeMap::from([
            (1, json!({"question/problem":"Calculate the derivative."}).as_object().unwrap().clone()),
            (2, json!({"step/content":1}).as_object().unwrap().clone()),
            (3, json!({"multistep/context":"Inner setup.","multistep/steps":[2]}).as_object().unwrap().clone()),
            (4, json!({"step/content":3}).as_object().unwrap().clone()),
            (5, json!({"multistep/context":"Outer setup.","multistep/steps":[4]}).as_object().unwrap().clone()),
        ]), 10)?;
        assert_eq!(question_markdown(&s, 1)?, "Outer setup.\n\nInner setup.\n\nCalculate the derivative.");
        s.entities.insert(1, json!({"question/problem":"Outer setup.\n\nInner setup.\n\nCalculate the derivative."}).as_object().unwrap().clone());
        assert_eq!(question_markdown(&s, 1)?, "Outer setup.\n\nInner setup.\n\nCalculate the derivative.");
        s.entities.insert(6, json!({"multistep/context":"Different function.","multistep/steps":[2]}).as_object().unwrap().clone());
        assert!(question_markdown(&s, 1).unwrap_err().to_string().contains("different shared setups"));
        s.entities.remove(&6);
        s.entities.insert(7, json!({"step/content":5}).as_object().unwrap().clone());
        s.entities.get_mut(&3).unwrap().insert("multistep/steps".into(), json!([2,7]));
        assert!(question_markdown(&s, 1).unwrap_err().to_string().contains("acyclic"));
        Ok(())
    }

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
            "activity.type/review",
        ]
        .iter()
        .enumerate()
        {
            records.insert(
                1000 + index as u64,
                json!({"db/ident":kw(ident)}).as_object().unwrap().clone(),
            );
        }
        // Keep the selection fixtures at L30+; the cutoff has its own boundary tests.
        for topic in 90000..90029 {
            let next = if topic == 90028 { vec![5,7] } else { vec![topic + 1] };
            records.insert(topic, json!({"topic/id":format!("foundation-{topic}"),"topic/next":next}).as_object().unwrap().clone());
        }
        records.insert(90029, json!({"progress/topic":90028,"progress/repetitions":1.0}).as_object().unwrap().clone());
        records.get_mut(&1).unwrap().insert("learner/knowledge-profile".into(),json!([90029]));
        let mut snapshot = EntitySnapshot::new(records, 42).unwrap();
        // This fixture represents an already prepared queue. Keep its stored
        // priority current while tests below exercise no-op preparation.
        for candidate in learning::queue_candidates(&snapshot, 1, 2, Utc::now()).unwrap() {
            let tasks = snapshot.owners(candidate.activity, "learner-task/activity").unwrap();
            for task in tasks {
                snapshot.entities.get_mut(&task).unwrap()
                    .insert("learner-task/priority".into(), json!(candidate.priority));
            }
        }
        snapshot
    }

    #[test]
    fn review_task_exposes_its_topic_reference_without_a_live_lesson() {
        let mut s = fixture();
        assert!(task_json(&s, 1, 81).unwrap().get("reviewTopic").is_none());
        s.entities.get_mut(&51).unwrap().insert("activity/type".into(), json!("activity.type/review"));
        s.entities.get_mut(&6).unwrap().insert("topic/id".into(), json!({"$uuid":"00000000-0000-0000-0000-000000000006"}));
        s.entities.get_mut(&6).unwrap().insert("topic/knowledge-points".into(), json!([72]));
        s.entities.insert(72, json!({"knowledge-point/id":"review-bank","knowledge-point/questions":[71]}).as_object().unwrap().clone());
        let s = EntitySnapshot::new(s.entities.into(), 42).unwrap();
        let view = task_json(&s, 1, 81).unwrap();
        assert_eq!(view["reviewTopic"]["id"], 6);
        assert_eq!(view["reviewTopic"]["uuid"], "00000000-0000-0000-0000-000000000006");
        assert_eq!(view["activityId"], 51);
    }

    #[test]
    #[ignore = "read-only performance measurement against the configured database"]
    fn profile_study_home_reads() -> Result<()> {
        let mut app = Application::connect(std::env::var("EDB_DATABASE")?, std::env::var("PAGE_TEST_LEARNER")?, std::env::var("EDB_ENDPOINT").unwrap_or_default())?;
        let s = &app.snapshot;
        let l = app.learner_eid;
        eprintln!("Profile home basis={} entities={} cache-lifetime={:?}", s.basis_t, s.entities.len(), app.home_lifetime());
        let c = s.reference(l, "learner/course")?;
        macro_rules! measure {
            ($label:literal, $expression:expr) => {{
                let started = Instant::now();
                let value = $expression?;
                eprintln!("Profile component {}: {:.3} ms", $label, started.elapsed().as_secs_f64()*1000.);
                value
            }};
        }
        measure!("queue candidates", learning::queue_candidates(s, l, c, Utc::now()));
        measure!("engine candidates", learning::engine_candidates(s, l, c, Utc::now()));
        measure!("retrieval schedule", retrieval::schedule(s, l, c, Utc::now()));
        measure!("topic layers", learning::topic_layers(s));
        measure!("unavailable questions", learning::unavailable_questions(s, l));
        measure!("lifecycle", course_academy_engine::scheduling::lifecycle(s, l));
        measure!("assessment status", course_academy_engine::inventory::assessment_status(s, l, Utc::now()));
        for run in 0..3 {
            let started = Instant::now();
            let (forms, candidates) = queue_preparation(s, l, Utc::now())?;
            eprintln!("Profile home run={run} preparation={:.3} ms speculative-forms={} candidates={}", started.elapsed().as_secs_f64()*1000., forms.len(), candidates.len());
            let started = Instant::now();
            let view = home_with_candidates(s, l, None)?;
            eprintln!("Profile home run={run} repeated-planning={:.3} ms bytes={}", started.elapsed().as_secs_f64()*1000., serde_json::to_vec(&view)?.len());
            let started = Instant::now();
            let _view = home_with_candidates(s, l, Some(candidates))?;
            eprintln!("Profile home run={run} reused-planning={:.3} ms", started.elapsed().as_secs_f64()*1000.);
        }
        let view = home(&app.snapshot, l)?;
        app.home_cache = Some((Instant::now(), app.home_lifetime(), view, true));
        for run in 0..5 {
            let started = Instant::now();
            let view = app.handle(json!({"action":"home"}))?;
            eprintln!("Profile cached home run={run} elapsed={:.3} ms bytes={}", started.elapsed().as_secs_f64()*1000., serde_json::to_vec(&view)?.len());
        }
        // Simulate learner writes only in this held projection. Exercise the
        // same replacement/invalidation path without committing to live EDB.
        let task = app.snapshot.refs(l, "learner/activity")?[0];
        for run in 0..3 {
            let mut record = app.snapshot.entity(task)?.clone();
            let elapsed = record.get("learner-task/elapsed-seconds").and_then(Json::as_f64).unwrap_or(0.0);
            record.insert("learner-task/elapsed-seconds".into(), json!(elapsed + 1.0));
            app.snapshot.replace_records(BTreeMap::from([(task, record)]), app.snapshot.basis_t + 1)?;
            app.home_cache = None;
            let started = Instant::now();
            let (forms, candidates) = queue_preparation(&app.snapshot, l, Utc::now())?;
            let view = home_with_candidates(&app.snapshot, l, Some(candidates))?;
            eprintln!("Profile rebuild after learner update run={run} elapsed={:.3} ms speculative-forms={} bytes={}", started.elapsed().as_secs_f64()*1000., forms.len(), serde_json::to_vec(&view)?.len());
        }
        Ok(())
    }

    #[test]
    #[ignore = "read-only performance measurement against the configured database"]
    fn profile_study_now_reads() -> Result<()> {
        let app = Application::connect(
            std::env::var("EDB_DATABASE")?,
            std::env::var("PAGE_TEST_LEARNER")?,
            std::env::var("EDB_ENDPOINT").unwrap_or_default(),
        )?;
        let s = &app.snapshot;
        let l = app.learner_eid;
        eprintln!("Profile basis={} entities={} status_events={}", s.basis_t, s.entities.len(), s.status_history.len());
        let started = Instant::now();
        let mut copy = s.clone();
        eprintln!("Profile snapshot-clone: {:.3} ms", started.elapsed().as_secs_f64()*1000.);
        let db = app.conn.db();
        let started = Instant::now();
        refresh_history(&db, &mut copy)?;
        eprintln!("Profile status-history-refresh: {:.3} ms", started.elapsed().as_secs_f64()*1000.);
        let topics: Vec<u64> = std::env::var("LEARNING_PROFILE_TOPICS")?
            .split(',').map(str::parse).collect::<std::result::Result<_, _>>()?;
        for topic in topics {
            let activity = topic_lesson(s, topic)?;
            for run in 0..2 {
                let started = Instant::now();
                let result = mutate(s, l, "study-topic", &json!({"topicId":topic}), Utc::now());
                eprintln!("Profile study-now topic={} title={} run={} planning={:.3} ms outcome={}", topic,
                    text(s,activity,"activity/title"),run,started.elapsed().as_secs_f64()*1000.,
                    match &result {Ok((forms,_))=>format!("{} speculative forms",forms.len()),Err(error)=>error.to_string()});
                if let Ok((_, result)) = result {
                    if let Some(task) = result["taskId"].as_u64() {
                        let started = Instant::now();
                        let view = task_json(s, l, task)?;
                        eprintln!("Profile task-response: {:.3} ms bytes={}", started.elapsed().as_secs_f64()*1000.,serde_json::to_vec(&view)?.len());
                    }
                }
            }
        }
        Ok(())
    }

    fn usable_small_bank_fixture() -> EntitySnapshot {
        let mut s=fixture();
        for (id,band) in [(1100,"easy"),(1101,"moderate"),(1102,"hard")] {
            s.entities.insert(id,json!({"db/ident":kw(&format!("question.difficulty/{band}"))}).as_object().unwrap().clone());
        }
        let template=s.entities[&71].clone();
        for (q,band) in [(71,1100),(74,1100),(75,1101),(76,1101),(77,1102)] {
            let mut row=template.clone();
            row.insert("question/id".into(),json!(format!("question-{q}")));
            row.insert("question/difficulty".into(),json!(band));
            s.entities.insert(q,row);
        }
        s.entities.insert(72,json!({"knowledge-point/id":"skill","knowledge-point/title":"Small skill bank",
            "knowledge-point/canonical-example":73,"knowledge-point/questions":[71,74,75,76,77]}).as_object().unwrap().clone());
        s.entities.insert(73,json!({"question/id":"example","question/problem":"Find x.","question/worked-solution":"x=2"}).as_object().unwrap().clone());
        s.entities.get_mut(&6).unwrap().insert("topic/knowledge-points".into(),json!([72]));
        s.entities.get_mut(&61).unwrap().insert("step/content".into(),json!(72));
        EntitySnapshot::new(s.entities.into(),s.basis_t).unwrap()
    }

    #[test]
    fn study_now_and_queue_allow_five_total_questions_without_full_band_reserves() {
        let s=usable_small_bank_fixture();
        assert!(!course_academy_engine::inventory::ready(&s,&[72],&BTreeSet::new(),true).unwrap());
        let (forms,result)=mutate(&s,1,"study-topic",&json!({"topicId":6}),Utc::now()).unwrap();
        assert_eq!(result["taskId"],81);
        assert!(forms.contains(&cas(&s,81,"learner-task/status","learner-task.status/started").unwrap()));
        let (_,plan)=queue_preparation(&s,1,Utc::now()).unwrap();
        assert!(plan.iter().any(|p|p.activity==51));
    }

    #[test]
    fn focused_mode_keeps_topic_menu_checks_and_manual_lesson_resume_independent() {
        let mut s = usable_small_bank_fixture();
        let at = Utc::now();
        let normal = topic_study_availability(&s, 1, 6, at);
        s.focused_mode = true;
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(), json!([5]));
        let focused = topic_study_availability(&s, 1, 6, at);
        assert_eq!(focused, normal);
        assert_eq!(focused["available"], true);
        for (action, body) in [("study-topic", json!({"topicId":6})),
            ("resume", json!({"taskId":81}))] {
            assert!(mutate(&s, 1, action, &body, at).is_ok(), "{action}");
        }
        // Feed eligibility stays narrow, and manual content checks still apply.
        assert!(!learning::study_candidates(&s, 1, 2, at).unwrap().iter().any(|p| p.topic == 6));
        s.entities.get_mut(&72).unwrap().insert("knowledge-point/questions".into(),json!([71,74,75,76]));
        let unavailable = topic_study_availability(&s, 1, 6, at);
        assert_eq!(unavailable["available"], false);
        assert!(unavailable["reason"].as_str().unwrap().contains("has 4 (needs 1 more)"));
    }

    #[test]
    fn study_now_names_a_real_total_supply_shortage() {
        let mut s=usable_small_bank_fixture();
        s.entities.get_mut(&72).unwrap().insert("knowledge-point/questions".into(),json!([71,74,75,76]));
        let error=mutate(&s,1,"study-topic",&json!({"topicId":6}),Utc::now()).unwrap_err();
        assert!(error.to_string().contains("Small skill bank has 4 (needs 1 more)"));
        assert_eq!(envelope(Err(error))["code"],"lesson-supply-shortage");
    }

    #[test]
    fn topic_menu_availability_uses_start_rules_without_mutating_the_snapshot() {
        let at = Utc::now();
        let mut s = usable_small_bank_fixture();
        let before = s.entities.clone();
        assert_eq!(topic_study_availability(&s, 1, 6, at)["available"], true);
        assert_eq!(s.entities, before);
        // One exhausted or invalid question makes a five-question skill bank unusable.
        s.entities.get_mut(&72).unwrap().insert("knowledge-point/questions".into(), json!([71,74,75,76]));
        let view = topic_study_availability(&s, 1, 6, at);
        assert_eq!(view["available"], false);
        assert!(view["reason"].as_str().unwrap().contains("has 4 (needs 1 more)"));
        assert!(mutate(&s, 1, "study-topic", &json!({"topicId":6}), at).is_err());
        let mut s = usable_small_bank_fixture();
        s.entities.get_mut(&90).unwrap().remove("answer-field/correct");
        assert_eq!(topic_study_availability(&s, 1, 6, at)["available"], false);
        for topic in [2, 7, 999] {
            assert_eq!(topic_study_availability(&s, 1, topic, at)["available"], false);
        }
        let s = fixture();
        assert_eq!(topic_study_availability(&s, 1, 6, at)["available"], true);
    }

    #[test]
    fn topic_menu_distinguishes_completed_lessons_from_resumable_study() {
        let mut s = fixture();
        s.entities.insert(2000, json!({"db/ident":kw("learner-task.status/completed")}).as_object().unwrap().clone());
        s.entities.get_mut(&81).unwrap().insert("learner-task/status".into(), json!(2000));
        let mut s = EntitySnapshot::new(s.entities.into(), s.basis_t).unwrap();
        s.status_history.push(StatusAssertion { entity: 81, attribute: "learner-task/status".into(), value: kw("learner-task.status/completed"), t: 42, at: json!({"$instant":1000}) });
        let at = Utc::now();
        let view = topic_study_availability(&s, 1, 6, at);
        assert_eq!(view["available"], true);
        assert_eq!(view["completed"], true);
        assert_eq!(view["resumable"], false);
        let (forms, result) = mutate(&s, 1, "study-topic", &json!({"topicId":6}), at).unwrap();
        assert!(forms.is_empty());
        assert_eq!(result["taskId"], 81);
    }

    #[test]
    fn learner_without_a_course_can_browse_and_select_their_first_course() {
        let mut s = fixture();
        s.entities.get_mut(&1).unwrap().remove("learner/course");
        let before = s.entities.clone();
        let view = home(&s, 1).unwrap();
        assert!(view["course"].is_null());
        assert_eq!(view["needsCourseSelection"], true);
        assert_eq!(view["activities"], json!([]));
        let profile = profile_json(&s, 1).unwrap();
        assert!(profile["course"].is_null());
        assert_eq!(profile["courses"].as_array().unwrap().len(), 1);
        assert!(queue_forms(&s, 1, Utc::now()).unwrap().is_empty());
        let (forms, _) = mutate(
            &s,
            1,
            "profile-settings",
            &json!({"courseId":"00000000-0000-0000-0000-000000000002","selfDirected":false}),
            Utc::now(),
        )
        .unwrap();
        assert!(forms.contains(&json!([kw("db/add"), 1, kw("learner/course"), 2])));
        assert_eq!(s.entities, before);
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
        s = EntitySnapshot::new(s.entities.into(), 42).unwrap();
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
        assert!(entry["step"]["fields"][0].get("presentation").is_none());
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
        s = EntitySnapshot::new(s.entities.clone().into(), s.basis_t).unwrap();
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
        for (t, entity, attribute, value) in [
            (1, 81, "learner-task/status", "learner-task.status/started"),
            (2, 95, "task-item/status", "task-item.status/completed"),
            (3, 96, "task-item/status", "task-item.status/correct"),
            (4, 97, "task-item/status", "task-item.status/completed"),
        ] {
            s.status_history.push(StatusAssertion {
                entity,
                attribute: attribute.into(),
                value: kw(value),
                t,
                at: json!({"$instant":t * 1000}),
            });
        }
        // Deferred work must not hide the last presentation or its Next button
        // before Continue has actually paused the attempt.
        let view = task_json(&s, 1, 81).unwrap();
        assert_eq!(view["awaitingQuestions"], false);
        assert_eq!(view["canResumePractice"], false);
        assert_eq!(view["step"]["itemId"], 97);
        assert_eq!(view["deferredSteps"][0]["stepId"], 61);
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
        s.status_history.push(StatusAssertion {
            entity: 81,
            attribute: "learner-task/status".into(),
            value: kw("learner-task.status/paused"),
            t: 5,
            at: json!({"$instant":5000}),
        });
        let view = task_json(&s, 1, 81).unwrap();
        assert_eq!(view["awaitingQuestions"], true);
        assert_eq!(view["canResumePractice"], false);
        assert_eq!(view["elapsedSeconds"], 3.0);
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
        assert_eq!(task_json(&s, 1, 81).unwrap()["canResumePractice"], true);
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/queue".into(), json!([]));
        let dashboard = home(&s, 1).unwrap();
        assert_eq!(dashboard["activities"].as_array().unwrap().len(), 1);
        assert_eq!(dashboard["activities"][0]["taskId"], 81);
        assert_eq!(dashboard["activities"][0]["status"], "paused");
        assert!(
            dashboard["waitingActivities"]
                .as_array()
                .unwrap()
                .is_empty()
        );
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
        assert_eq!(topic_study_availability(&s, 1, 6, at)["available"], true);
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
        s = EntitySnapshot::new(s.entities.into(), 42).unwrap();
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
        let cloned_task = s.entity(81).unwrap().clone();
        s.entities.insert(83, cloned_task);
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
        s = EntitySnapshot::new(s.entities.into(), 42).unwrap();
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
        let cloned_activity = s.entity(51).unwrap().clone();
        s.entities.insert(52, cloned_activity);
        assert!(
            topic_lesson(&s, 6)
                .unwrap_err()
                .to_string()
                .contains("ambiguous")
        );
    }

    #[test]
    fn self_directed_home_and_preparation_preserve_unselected_started_and_paused_lessons() {
        for state in ["started", "paused"] {
            let mut s = fixture();
            s.entities.insert(95, json!({"task-item/content":70,"task-item/status":"task-item.status/correct"}).as_object().unwrap().clone());
            s.entities.get_mut(&80).unwrap().insert("learner-task/items".into(), json!([95]));
            s.entities.get_mut(&80).unwrap().insert(
                "learner-task/status".into(),
                kw(&format!("learner-task.status/{state}")),
            );
            let before = s.entities.clone();
            let view = home(&s, 1).unwrap();
            assert_eq!(view["activities"][0]["activityId"], 50);
            assert_eq!(view["activities"][0]["taskId"], 80);
            assert_eq!(view["activities"][0]["status"], state);
            assert_eq!(view["activities"][0]["reason"], "Continue your lesson");
            assert_eq!(view["activities"][1]["activityId"], 51);
            let (forms, candidates) = queue_preparation(&s, 1, Utc::now()).unwrap();
            assert!(forms.iter().all(|form| {
                form.as_array()
                    .is_some_and(|parts| parts.get(2) == Some(&kw("learner-task/priority")))
            }));
            assert_eq!(home_with_candidates(&s, 1, Some(candidates)).unwrap(), view);
            assert_eq!(s.entities, before);
            s.entities
                .get_mut(&1)
                .unwrap()
                .insert("learner/queue".into(), json!([]));
            assert_eq!(
                home(&s, 1).unwrap()["activities"].as_array().unwrap().len(),
                1
            );
        }
    }

    #[test]
    fn prepared_queue_candidates_render_the_same_home_in_both_study_modes() {
        for directed in [false, true] {
            let mut s = fixture();
            s.entities
                .get_mut(&1)
                .unwrap()
                .insert("learner/self-directed".into(), json!(directed));
            let (forms, candidates) = queue_preparation(&s, 1, Utc::now()).unwrap();
            assert!(forms.is_empty());
            assert_eq!(
                home_with_candidates(&s, 1, Some(candidates)).unwrap(),
                home(&s, 1).unwrap()
            );
        }
    }

    #[test]
    fn study_home_and_preparation_exclude_topics_below_l30_in_both_modes() {
        let mut s = fixture();
        // Removing the foundation chain puts the course and selected topics
        // below L30, including their already prepared tasks.
        s.entities.get_mut(&90028).unwrap().insert("topic/next".into(),json!([]));
        for self_directed in [true,false] {
            s.entities.get_mut(&1).unwrap().insert("learner/self-directed".into(),json!(self_directed));
            let view = home(&s,1).unwrap();
            assert!(view["activities"].as_array().unwrap().is_empty());
            assert!(view["waitingActivities"].as_array().unwrap().is_empty());
            let (_,candidates) = queue_preparation(&s,1,Utc::now()).unwrap();
            assert!(candidates.is_empty());
            assert!(check_activity_start(&s,1,51,None,Utc::now()).is_err());
        }
    }

    #[test]
    fn study_skips_band_one_with_false_learned_flag_and_serves_the_next_new_lesson() {
        let mut s = fixture();
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(),json!([5]));
        s.entities.insert(96,json!({"progress/topic":6,"progress/repetitions":1.0,
            "progress/learned":false}).as_object().unwrap().clone());
        s.entities.get_mut(&1).unwrap().insert("learner/knowledge-profile".into(),json!([90029,96]));
        let before = s.entities.clone();
        let at = Utc::now();
        let view = home(&s,1).unwrap();
        assert_eq!(view["activities"].as_array().unwrap().len(),1);
        assert_eq!(view["activities"][0]["activityId"],50);
        let (_, candidates) = queue_preparation(&s,1,at).unwrap();
        assert_eq!(candidates.iter().map(|p|p.activity).collect::<Vec<_>>(),[50]);
        assert!(check_activity_start(&s,1,50,None,at).is_ok());
        assert!(check_activity_start(&s,1,51,None,at).is_err());
        // Manual study and the learner's recorded progress remain untouched.
        assert!(check_activity_start(&s,1,51,Some(6),at).is_ok());
        assert_eq!(s.entities,before);
    }

    #[test]
    fn bounded_scope_home_preparation_and_start_skip_shortages_without_mastery_gates() {
        let mut s = fixture();
        // A <- B <- C <- D: C is the depth-two entry point, even though D is
        // unlearned. B has no question supply; it must not hold up A either.
        // The second selected branch has its own unavailable earlier lesson.
        for (topic, next, available) in [
            (106, vec![], true), (107, vec![106], false),
            (108, vec![107], true), (109, vec![108], true),
            (116, vec![], true), (117, vec![116], false),
        ] {
            let activity = 2000 + topic;
            let step = 3000 + topic;
            let question = 4000 + topic;
            let kp = 5000 + topic;
            s.entities.insert(topic, json!({"topic/id":format!("topic-{topic}"),
                "topic/next":next,"topic/knowledge-points":[kp]}).as_object().unwrap().clone());
            s.entities.insert(activity, json!({"activity/id":format!("lesson-{topic}"),
                "activity/type":"activity.type/lesson","activity/scope":topic,
                "activity/title":format!("Lesson {topic}"),"activity/expected-seconds":720.0,
                "activity/steps":[step],"activity/first-step":step}).as_object().unwrap().clone());
            s.entities.insert(step, json!({"step/content":question}).as_object().unwrap().clone());
            let mut record = s.entities[&71].clone();
            record.insert("question/id".into(),json!(format!("fixed-{topic}")));
            s.entities.insert(question,record);
            let mut questions = vec![];
            if available {
                for i in 0..5 {
                    let q = 6000 + topic * 10 + i;
                    let mut record = s.entities[&71].clone();
                    record.insert("question/id".into(),json!(format!("practice-{q}")));
                    s.entities.insert(q,record);
                    questions.push(q);
                }
            }
            s.entities.insert(kp,json!({"knowledge-point/id":format!("skill-{kp}"),
                "knowledge-point/questions":questions}).as_object().unwrap().clone());
        }
        s.entities.get_mut(&90028).unwrap().insert("topic/next".into(),json!([5,7,109,117]));
        s.entities.get_mut(&1).unwrap().insert("learner/targets".into(),json!([106]));
        s.entities.get_mut(&1).unwrap().insert("learner/queue".into(),json!([116]));
        let before = s.entities.clone();
        let at = Utc::now();
        let expected = BTreeSet::from([2106,2108,2116]);
        let view = home(&s,1).unwrap();
        let ids = |view: &Json| view["activities"].as_array().unwrap().iter()
            .map(|card|card["activityId"].as_u64().unwrap()).collect::<BTreeSet<_>>();
        assert_eq!(ids(&view),expected);
        assert_eq!(ids(&developer_preview::home(&s,1).unwrap()),expected);
        let (forms,candidates)=queue_preparation(&s,1,at).unwrap();
        assert_eq!(candidates.iter().map(|p|p.activity).collect::<BTreeSet<_>>(),expected);
        assert_eq!(ids(&home_with_candidates(&s,1,Some(candidates)).unwrap()),expected);
        for activity in expected {
            assert!(forms.iter().any(|form|form.get("learner-task/activity")==Some(&json!(activity))));
            check_activity_start(&s,1,activity,None,at).unwrap();
            let (starts,_)=mutate(&s,1,"start",&json!({"activityId":activity}),at).unwrap();
            assert!(starts.iter().any(|form|form.get("learner-task/activity")==Some(&json!(activity))
                && form.get("learner-task/status")==Some(&kw("learner-task.status/started"))));
        }
        for unavailable in [2107,2117,2109] {
            assert!(check_activity_start(&s,1,unavailable,None,at).is_err());
            assert!(!forms.iter().any(|form|form.get("learner-task/activity")==Some(&json!(unavailable))));
        }
        assert_eq!(s.entities,before,"read and speculative start checks never commit learner changes");
        // Explicit Study Now remains able to choose D; switching to course mode
        // still offers the independent course lesson, not the scoped lessons.
        check_activity_start(&s,1,2109,Some(109),at).unwrap();
        s.entities.get_mut(&1).unwrap().insert("learner/self-directed".into(),json!(false));
        assert_eq!(ids(&home(&s,1).unwrap()),BTreeSet::from([50]));
        assert!(check_activity_start(&s,1,2108,None,at).is_err());
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
        let selected_priority = s.entities[&81]["learner-task/priority"].clone();
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
            .insert("learner/knowledge-profile".into(), json!([23,90029]));
        assert_eq!(
            queue_forms(&s, 1, at).unwrap(),
            vec![
                cas(
                    &s,
                    81,
                    "learner-task/status",
                    "learner-task.status/unlocked"
                )
                .unwrap(),
                add(json!(81), "learner-task/priority", json!(1.0)),
            ]
        );
        s.entities.get_mut(&81).unwrap().insert(
            "learner-task/status".into(),
            kw("learner-task.status/unlocked"),
        );
        s.entities.get_mut(&81).unwrap().insert("learner-task/priority".into(), json!(1.0));
        assert!(queue_forms(&s, 1, at).unwrap().is_empty());
        // Explicit selection alone must not maintain a false engine unlock.
        s.entities
            .get_mut(&23)
            .unwrap()
            .insert("progress/repetitions".into(), json!(0.0));
        assert_eq!(
            queue_forms(&s, 1, at).unwrap(),
            vec![cas(&s, 81, "learner-task/status", "learner-task.status/locked").unwrap(),
                add(json!(81), "learner-task/priority", selected_priority)]
        );
    }
}

#[cfg(test)]
mod integration {
    use super::*;

    fn preview_with(
        db: &DatabaseValue,
        transaction: &str,
        at: i64,
        source: EntityRef,
    ) -> Result<edb_core::SpeculativeTransactionReport> {
        let mut registry = edb_core::NativeRegistry::builder();
        type Predicate =
            fn(&DatabaseValue, u64) -> std::result::Result<bool, edb_core::SemanticError>;
        for (namespace, name, predicate) in [
            (
                "course-academy.topic",
                "valid-difficulty?",
                preview_configuration::valid_topic_difficulty as Predicate,
            ),
            (
                "course-academy.policy",
                "valid?",
                preview_configuration::valid_policy as Predicate,
            ),
            (
                "course-academy.progress",
                "valid-profile?",
                preview_progress::valid_profile as Predicate,
            ),
            (
                "course-academy.progress",
                "valid-progress?",
                preview_progress::valid_progress as Predicate,
            ),
            (
                "course-academy.answer-field",
                "valid?",
                preview_answer_fields::valid_field as Predicate,
            ),
        ] {
            registry.entity_predicate(
                edb_core::Symbol::new(namespace, name),
                move |db, entity, control| {
                    control.check(1)?;
                    Ok(edb_core::RuntimeValue::Scalar(Value::Bool(predicate(
                        db, entity,
                    )?)))
                },
            )?;
        }
        Ok(db.with_forms_with_execution_options(
            &edb_core::edn_transaction::read_edn_transaction(transaction)?,
            at,
            source,
            edb_core::SpeculationLimits::default(),
            &edb_core::TransactionExecutionOptions {
                native: registry.build(),
                ..Default::default()
            },
        )?)
    }

    #[test]
    #[ignore = "reads live math and previews a migration manifest or transaction without durable writes"]
    fn preview_history_migration() -> Result<()> {
        let (input_path, manifest) =
            if let Some(path) = std::env::var_os("LEARNING_HISTORY_MIGRATION_MANIFEST") {
                let path = PathBuf::from(path);
                let manifest: Json = serde_json::from_slice(&std::fs::read(&path)?)?;
                (path, manifest)
            } else {
                let path = PathBuf::from(std::env::var("LEARNING_HISTORY_MIGRATION_TX")?)
                    .canonicalize()?;
                let intent: Json =
                    serde_json::from_slice(&std::fs::read(path.with_file_name("intent.json"))?)?;
                let manifest = json!({
                    "destination_basis":intent["destination_basis"],
                    "transactions":[{"file":path,"source":intent["source"],
                        "source_eid":intent["source_eid"],"sha256":intent["transaction_sha256"]}],
                });
                (path, manifest)
            };
        let expected_basis = manifest["destination_basis"]
            .as_u64()
            .ok_or("migration manifest is missing destination_basis")?;
        let stages = manifest["transactions"]
            .as_array()
            .filter(|stages| !stages.is_empty())
            .ok_or("migration manifest must contain ordered transactions")?;
        let config = if std::env::var_os("EDB_POSTGRES_URL").is_some() {
            postgres_config_from_env()?
        } else {
            edb_core::PostgresConnectionConfig::parse(
                "host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'",
            )?
        };
        let database = std::env::var("EDB_DATABASE").unwrap_or("math".into());
        let conn = Connection::connect_configured(config, database, 256)?;
        let base = conn.db();
        assert_eq!(
            base.basis_t(),
            expected_basis,
            "migration destination advanced; prepare a fresh transaction before previewing"
        );
        let before = snapshot(&base)?;
        let learner = before
            .entities
            .iter()
            .find_map(|(&eid, record)| {
                (record.get("learner/id").and_then(Json::as_str)
                    == Some("59d5cf13-351c-4114-be19-4c3bb64ee051"))
                .then_some(eid)
            })
            .ok_or("migration learner is unavailable")?;
        let prior_tasks: BTreeSet<_> = before
            .refs(learner, "learner/activity")?
            .into_iter()
            .collect();
        let engine_source_eid = before
            .entities
            .iter()
            .find_map(|(&eid, record)| {
                (record.get("db/ident") == Some(&kw(ENGINE_SOURCE))).then_some(eid)
            })
            .ok_or("application/ca-engine source is not registered")?;
        let mut migrated = base.clone();
        let mut stage_reports = vec![];
        let preview_at = Utc::now().timestamp_millis();
        let mut all_engine_source = true;
        let mut introduced_facts = Vec::<edb_core::Datom>::new();
        let mut all_added = true;
        for (index, stage) in stages.iter().enumerate() {
            let file = stage["file"]
                .as_str()
                .ok_or("migration stage is missing file")?;
            let path = input_path
                .parent()
                .ok_or("migration input has no parent directory")?
                .join(file);
            let transaction = std::fs::read_to_string(&path)?;
            let source_name = stage["source"]
                .as_str()
                .ok_or("migration stage is missing source")?
                .trim_start_matches(':');
            let (namespace, name) = source_name
                .split_once('/')
                .ok_or("migration source must be a qualified ident")?;
            let source_ident = Keyword::new(namespace, name);
            let source = migrated
                .entid(&source_ident)
                .ok_or_else(|| format!("migration source {source_name} is not registered"))?;
            if let Some(expected) = stage.get("source_eid").filter(|value| !value.is_null()) {
                assert_eq!(
                    Some(source),
                    expected.as_u64(),
                    "migration stage {index} source ident does not match its recorded EID"
                );
            } else {
                assert!(
                    base.entid(&source_ident).is_none()
                        && introduced_facts.iter().any(|fact| {
                            fact.entity == source
                                && fact.value == Value::Keyword(source_ident.clone())
                                && migrated.schema().attribute(fact.attribute).is_ok_and(
                                    |attribute| attribute.ident == Keyword::new("db", "ident"),
                                )
                        }),
                    "migration stage {index} may omit source_eid only for a source ident introduced by an earlier stage"
                );
            }
            let preview = preview_with(
                &migrated,
                &transaction,
                preview_at,
                EntityRef::Ident(source_ident),
            )?;
            let allowed_retractions: BTreeSet<String> = stage
                .get("allow_retractions")
                .map(|value| {
                    value
                        .as_array()
                        .ok_or("allow_retractions must be an attribute list")?
                        .iter()
                        .map(|attribute| {
                            attribute
                                .as_str()
                                .map(|name| name.trim_start_matches(':').to_owned())
                                .ok_or("allowed retraction attribute must be an ident")
                        })
                        .collect::<std::result::Result<_, _>>()
                })
                .transpose()?
                .unwrap_or_default();
            assert!(
                allowed_retractions.is_empty()
                    || (source == engine_source_eid
                        && allowed_retractions
                            .iter()
                            .all(|name| name.starts_with("progress/"))),
                "only an engine stage may replace explicitly allowed imported progress attributes"
            );
            assert!(
                preview.tx_data.iter().all(|datom| datom.source == source),
                "migration stage {index} must attribute facts to its declared source"
            );
            let mut retractions = vec![];
            for datom in preview.tx_data.iter().filter(|datom| !datom.added) {
                let attribute = preview.db_before.schema().attribute(datom.attribute)?;
                let name = attribute.ident.qualified_name();
                assert!(
                    allowed_retractions.contains(&name),
                    "migration stage {index} retracts undeclared attribute {name}"
                );
                let earlier = introduced_facts
                    .iter()
                    .rev()
                    .find(|earlier| {
                        earlier.entity == datom.entity
                            && earlier.attribute == datom.attribute
                            && earlier.value == datom.value
                    })
                    .ok_or_else(|| {
                        format!(
                            "migration stage {index} would retract a preexisting fact on {} {name}",
                            datom.entity
                        )
                    })?;
                retractions.push(json!({
                    "entity":datom.entity,"attribute":format!(":{name}"),"value":value(&datom.value)?,
                    "asserted_source_eid":earlier.source,"retraction_source_eid":datom.source,
                }));
            }
            all_added &= retractions.is_empty();
            introduced_facts.extend(preview.tx_data.iter().filter(|datom| datom.added).cloned());
            all_engine_source &= source == engine_source_eid;
            stage_reports.push(json!({
                "index":index,"file":file,"source":format!(":{source_name}"),"source_eid":source,
                "sha256":stage["sha256"],"destination_basis":preview.db_before.basis_t(),
                "preview_basis":preview.db_after.basis_t(),
                "added_datoms":preview.tx_data.iter().filter(|datom| datom.added).count(),
                "all_added":retractions.is_empty(),"allowed_retractions":retractions,
                "preexisting_facts_unchanged":true,"declared_source_validated":true,"native_predicates_validated":true,
            }));
            migrated = preview.db_after;
        }
        let s = snapshot(&migrated)?;
        let tasks: Vec<_> = s
            .refs(learner, "learner/activity")?
            .into_iter()
            .filter(|task| !prior_tasks.contains(task))
            .collect();
        assert_eq!(
            tasks.len(),
            10,
            "migration must introduce the ten selected lesson tasks"
        );
        profile_json(&s, learner)?;
        home(&s, learner)?;
        assert_eq!(s.refs(learner, "learner/knowledge-profile")?.len(), 1041);
        let (mut completed, mut paused, mut answered, mut response_refs, mut rendered_responses) =
            (0, 0, 0, 0, 0);
        let (mut correct, mut incorrect, mut total_seconds, mut total_xp) = (0, 0, 0.0, 0.0);
        let at = Utc::now();
        let mut task_reports = vec![];
        for task in tasks {
            let activity = s.reference(task, "learner-task/activity")?;
            assert_eq!(status(&s, activity, "activity/type")?, "lesson");
            let state = status(&s, task, "learner-task/status")?;
            match state.as_str() {
                "completed" => completed += 1,
                "paused" => paused += 1,
                _ => {
                    return Err(
                        format!("migrated task {task} has unexpected status {state}").into(),
                    );
                }
            }
            let view = task_json(&s, learner, task).map_err(|error| {
                format!(
                    "render migrated task {task} ({}): {error}",
                    text(&s, activity, "activity/title")
                )
            })?;
            let chain = items(&s, task)?;
            practice_state(&s, activity, &chain).map_err(|error| {
                format!("migrated task {task} does not match its lesson definition: {error}")
            })?;
            assert_eq!(
                view["history"]
                    .as_array()
                    .ok_or("task history missing")?
                    .len()
                    + 1,
                chain.len()
            );
            let saved = s
                .entity(task)?
                .get("learner-task/elapsed-seconds")
                .and_then(Json::as_f64)
                .ok_or("migrated task has no saved elapsed time")?;
            total_seconds += saved;
            total_xp += number(&s, task, "learner-task/xp-earned");
            let mut item_total = 0.0;
            for item in chain {
                let elapsed = s
                    .entity(item)?
                    .get("task-item/elapsed-seconds")
                    .and_then(Json::as_f64)
                    .ok_or("migrated item has no saved elapsed time")?;
                assert!(
                    (timing::elapsed(&s, item, at)? - elapsed).abs() < 1e-6,
                    "imported item {item} must retain its saved duration"
                );
                item_total += elapsed;
                let responses = s.refs(item, "task-item/responses")?;
                answered += usize::from(!responses.is_empty());
                response_refs += responses.len();
                if !responses.is_empty() {
                    match status(&s, item, "task-item/status")?.as_str() {
                        "correct" => correct += 1,
                        "incorrect" => incorrect += 1,
                        _ => return Err("a migrated answer has a non-graded status".into()),
                    }
                }
            }
            assert!(
                (saved - item_total).abs() < 1e-6,
                "task {task} saved time must equal item totals"
            );
            assert!((timing::task_elapsed(&s, task, at)? - saved).abs() < 1e-6);
            assert!(
                (view["elapsedSeconds"]
                    .as_f64()
                    .ok_or("rendered duration missing")?
                    - saved)
                    .abs()
                    < 1e-6
            );
            for step in view["history"]
                .as_array()
                .unwrap()
                .iter()
                .map(|entry| &entry["step"])
                .chain(std::iter::once(&view["step"]))
            {
                rendered_responses += step["fields"]
                    .as_array()
                    .ok_or("rendered answer fields missing")?
                    .iter()
                    .filter(|field| field.get("response").is_some())
                    .count();
            }
            if state == "paused" {
                let resumed_at = Utc::now();
                let (forms, _) = mutate(&s, learner, "resume", &json!({"taskId":task}), resumed_at)
                    .map_err(|error| {
                        format!(
                            "resume migrated task {task} ({}): {error}",
                            text(&s, activity, "activity/title")
                        )
                    })?;
                if forms.is_empty() {
                    eprintln!("Task {task} remains paused pending fresh practice questions");
                } else {
                    let resumed = preview_with(
                        &migrated,
                        &schema::edn(&json!(forms))?,
                        resumed_at.timestamp_millis(),
                        engine_source(),
                    )?;
                    assert!(
                        resumed
                            .tx_data
                            .iter()
                            .all(|datom| datom.source == engine_source_eid),
                        "resuming imported work must be attributed to the application engine"
                    );
                    let resumed_snapshot = snapshot(&resumed.db_after)?;
                    assert_eq!(
                        status(&resumed_snapshot, task, "learner-task/status")?,
                        "started"
                    );
                    task_json(&resumed_snapshot, learner, task)
                        .map_err(|error| format!("render resumed task {task}: {error}"))?;
                }
            }
            eprintln!(
                "Previewed {state} task {task}: {}",
                text(&s, activity, "activity/title")
            );
            task_reports.push(
                json!({"task_id":task,"status":state,"title":text(&s,activity,"activity/title"),
                "elapsed_seconds":saved,"rendered":true,"lesson_route_validated":true,
                "resume_validated":state == "paused"}),
            );
        }
        assert_eq!((completed, paused), (4, 6));
        assert_eq!(
            answered, 44,
            "all saved answer submissions must be retained"
        );
        assert_eq!((correct, incorrect), (40, 4));
        assert_eq!(total_xp, 37.0);
        assert!((total_seconds - 8344.367).abs() < 1e-6);
        assert_eq!(
            rendered_responses, response_refs,
            "every saved response must be visible in task history"
        );
        eprintln!(
            "Read-only migration preview: {completed} completed, {paused} paused, {answered} answered items, {rendered_responses} rendered field responses"
        );
        let report_path = std::env::var_os("LEARNING_HISTORY_MIGRATION_REPORT")
            .map(PathBuf::from)
            .unwrap_or_else(|| input_path.with_file_name("application-preview.json"));
        std::fs::write(
            report_path,
            serde_json::to_vec_pretty(&json!({
                "committed":false,"speculative":true,"status":"passed","destination_basis":before.basis_t,
                "preview_basis":s.basis_t,"durable_writes":0,"stages":stage_reports,
                "all_added":all_added,"preexisting_facts_unchanged":true,
                "all_engine_source":all_engine_source,"declared_sources_validated":true,
                "native_predicates_validated":true,"resume_source":format!(":{ENGINE_SOURCE}"),
                "profile_rendered":true,"home_rendered":true,
                "completed_tasks":completed,"paused_tasks":paused,"answered_items":answered,
                "progress_records":1041,"correct_items":correct,"incorrect_items":incorrect,
                "elapsed_seconds":total_seconds,"xp_earned":total_xp,
                "response_refs":response_refs,"rendered_responses":rendered_responses,"tasks":task_reports,
            }))?,
        )?;
        Ok(())
    }

    pub(super) fn commit(
        conn: &Connection,
        endpoint: &str,
        s: &EntitySnapshot,
        forms: Vec<Json>,
        key: &str,
        at: DateTime<Utc>,
    ) -> Result<EntitySnapshot> {
        let source = s
            .entities
            .iter()
            .find_map(|(&eid, record)| {
                (record.get("db/ident") == Some(&kw(ENGINE_SOURCE))).then_some(eid)
            })
            .ok_or("application/ca-engine source is not registered")?;
        let tx = TransactionRequest::from_edn(
            key,
            schema::edn(&json!(forms))?.as_str(),
            engine_source(),
        )?
        .comparing_basis(s.basis_t)
        .with_tx_instant(at.timestamp_millis());
        let first = conn.transact_socket(endpoint, tx.clone(), Duration::from_secs(30))?;
        let second = conn.transact_socket(endpoint, tx, Duration::from_secs(30))?;
        assert_eq!(
            first.basis_t, second.basis_t,
            "exact retries must replay one commit"
        );
        assert!(second.replayed);
        for report in [first.report?, second.report?] {
            assert!(
                report.tx_data.iter().all(|datom| datom.source == source),
                "every committed fact must retain the application engine's provenance"
            );
        }
        snapshot(&conn.sync_to(first.basis_t, Duration::from_secs(10))?)
    }

    #[test]
    #[ignore = "requires the local durable writer; creates then removes a temporary integration learner"]
    fn durable_lesson_lifecycle() -> Result<()> {
        let database = std::env::var("EDB_DATABASE").unwrap_or("math".into());
        let endpoint = std::env::var("EDB_ENDPOINT").unwrap_or("/tmp/edb-math/writer.sock".into());
        let conn = Connection::connect_configured(postgres_config_from_env()?, database, 256)?;
        let (mut s, l, nonce) = super::retrieval_tests::durable_fixture(&conn, &endpoint, false)?;
        let id = s.entities[&l]["learner/id"].as_str().unwrap().to_string();
        let c = course(&s, l)?;
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
        super::retrieval_tests::durable_cleanup(&conn, &endpoint, l, &nonce)?;
        result
    }
}
