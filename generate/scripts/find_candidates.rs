//! Read-only trigger discovery. All queries and the captured log share one DB value.
use chrono::{DateTime, Utc};
use edb_core::edn::{EdnValue, write_edn};
use edb_core::edn_query::{EdnQueryArgument, parse_query_edn};
use edb_core::{
    Connection, DatabaseValue, Keyword, QueryControl, QuerySourceValue, TimePoint, Value,
    postgres_config_from_env,
};
use serde_json::{Value as Json, json};
use std::{
    collections::{BTreeMap, BTreeSet},
    error::Error,
    io::Read,
    time::Duration,
};
type Result<T> = std::result::Result<T, Box<dyn Error>>;
const SELECTED: &str = include_str!("queries/selected-topics.edn");
const PENDING: &str = include_str!("queries/pending-activities.edn");
const PENDING_TOPICS: &str = include_str!("queries/pending-topics.edn");
const PENDING_CONTENT: &str = include_str!("queries/pending-content.edn");
const RETAKE_CONTENT: &str = include_str!("queries/retake-content.edn");
const CONTENT_TOPICS: [&str; 3] = [
    include_str!("queries/kp-content-topics.edn"),
    include_str!("queries/question-content-topics.edn"),
    include_str!("queries/example-content-topics.edn"),
];
const REVIEWS: &str = include_str!("queries/review-state.edn");
const CHANGED: &str = include_str!("queries/changed-activities.edn");
const TOPICS: &str = include_str!("queries/topics.edn");
const KPS: &str = include_str!("queries/knowledge-points.edn");

#[cfg(test)]
mod find_candidates_tests;
mod find_candidates_ranking;

fn json_value(v: &EdnValue) -> Result<Json> {
    Ok(match v {
        EdnValue::Nil => Json::Null,
        EdnValue::Bool(v) => json!(v),
        EdnValue::Long(v) => json!(v),
        EdnValue::Double(v) => json!(v),
        EdnValue::String(v) => json!(v),
        EdnValue::Keyword(v) => json!(v.qualified_name()),
        EdnValue::Tagged(_, v) => json_value(v)?,
        EdnValue::Vector(v) | EdnValue::List(v) | EdnValue::Set(v) => {
            Json::Array(v.iter().map(json_value).collect::<Result<_>>()?)
        }
        EdnValue::Map(v) => {
            let mut map = serde_json::Map::new();
            for (key, value) in v {
                let key = json_value(key)?;
                map.insert(
                    key.as_str().ok_or("non-string output key")?.into(),
                    json_value(value)?,
                );
            }
            Json::Object(map)
        }
        _ => return Err(format!("unsupported query output: {}", write_edn(v)?).into()),
    })
}

fn query(db: &DatabaseValue, text: &str, inputs: Vec<EdnValue>) -> Result<Vec<Vec<Json>>> {
    let mut args = vec![EdnQueryArgument::Source(QuerySourceValue::Database(
        db.clone(),
    ))];
    args.extend(inputs.into_iter().map(EdnQueryArgument::Data));
    let bound = parse_query_edn(text)?.bind(&args)?;
    let control = QueryControl {
        timeout: Some(Duration::from_secs(30)),
        max_work: 5_000_000,
        max_intermediate_rows: 100_000,
        max_result_rows: 100_000,
        max_value_bytes: 64 * 1024 * 1024,
        ..Default::default()
    };
    let result = bound
        .execute(&control, None)
        .map_err(|error| format!("{}: {error}", text.lines().next().unwrap_or("query")))?;
    if std::env::var_os("GENERATE_QUERY_STATS").is_some() {
        eprintln!(
            "{} rows={} work={} seeks={} datoms={} value_bytes={}",
            text.lines().next().unwrap_or("query"),
            result.stats.rows_produced,
            result.stats.work,
            result.stats.index_seeks,
            result.stats.datoms_examined,
            result.stats.allocated_value_bytes
        );
    }
    Ok(serde_json::from_value(json_value(
        &bound.result_to_edn(&result.result)?,
    )?)?)
}
fn eid(v: &Json) -> Result<u64> {
    v.as_u64().ok_or_else(|| "expected entity ID".into())
}
fn input_eid(v: u64) -> Result<EdnValue> {
    Ok(EdnValue::Tagged(
        edb_core::Symbol::new("edb", "ref"),
        Box::new(EdnValue::Long(i64::try_from(v)?)),
    ))
}
fn ids(v: &BTreeSet<u64>) -> Result<EdnValue> {
    Ok(EdnValue::Vector(
        v.iter().map(|v| input_eid(*v)).collect::<Result<_>>()?,
    ))
}

#[derive(Default)]
struct Changes {
    selections: BTreeSet<(u64, String)>,
    tasks: BTreeSet<u64>,
    activities: BTreeSet<u64>,
    steps: BTreeSet<u64>,
}
impl Changes {
    fn observe(
        &mut self,
        learner: u64,
        entity: u64,
        attribute: &str,
        value: &Value,
        added: bool,
        unlocked: u64,
        locked: u64,
    ) {
        if !added {
            return;
        }
        match (attribute, value) {
            ("learner/queue" | "learner/targets", Value::Ref(topic)) if entity == learner => {
                self.selections.insert((*topic, attribute.into()));
            }
            ("learner/activity", Value::Ref(task)) if entity == learner => {
                self.tasks.insert(*task);
            }
            ("learner-task/status", Value::Ref(state))
                if *state == unlocked || *state == locked =>
            {
                self.tasks.insert(entity);
            }
            ("learner-task/activity" | "learner-task/retake-of", _) => {
                self.tasks.insert(entity);
            }
            ("activity/scope" | "activity/steps" | "activity/type", _) => {
                self.activities.insert(entity);
            }
            ("step/content", _) => {
                self.steps.insert(entity);
            }
            _ => {}
        }
    }
}

fn review_due(memory: f64, anchor: i64, interval: f64, threshold: f64, now: i64) -> Result<bool> {
    if !memory.is_finite()
        || memory < 0.0
        || !interval.is_finite()
        || interval <= 0.0
        || !threshold.is_finite()
        || threshold <= 0.0
    {
        return Err("invalid operational review state".into());
    }
    let elapsed = (now as f64 - anchor as f64) / 86_400_000.0;
    Ok(elapsed >= 0.0 && memory * 2.0_f64.powf(-elapsed / interval) <= threshold + 1e-12)
}

fn candidates(
    db: &DatabaseValue,
    learner: u64,
    now: i64,
    changes: Option<&Changes>,
    scheduler_topics: &BTreeSet<u64>,
    scheduler_kind: &str,
) -> Result<Json> {
    let mut triggers: BTreeMap<u64, BTreeSet<(String, String, Option<u64>)>> = BTreeMap::new();
    let mut add = |topic, reason: &str, kind: &str, task| {
        triggers
            .entry(topic)
            .or_default()
            .insert((reason.into(), kind.into(), task));
    };
    let selections = EdnValue::Vector(vec![
        EdnValue::Keyword(Keyword::new("learner", "queue")),
        EdnValue::Keyword(Keyword::new("learner", "targets")),
    ]);
    for row in query(db, SELECTED, vec![input_eid(learner)?, selections])? {
        let topic = eid(&row[0])?;
        let reason = row[1].as_str().ok_or("selection ident missing")?;
        if changes.is_none_or(|c| c.selections.contains(&(topic, reason.into()))) {
            add(topic, reason, "lesson", None);
        }
    }
    let mut pending = vec![];
    for row in query(db, PENDING, vec![input_eid(learner)?])? {
        let task = eid(&row[0])?;
        let activity = eid(&row[1])?;
        if changes.is_none_or(|c| c.tasks.contains(&task) || c.activities.contains(&activity)) {
            pending.push(EdnValue::Vector(vec![
                input_eid(task)?,
                input_eid(activity)?,
                EdnValue::String(row[2].as_str().ok_or("activity kind missing")?.into()),
                EdnValue::String(row[3].as_str().ok_or("activity state missing")?.into()),
            ]));
        }
    }
    let mut pending_topics = if pending.is_empty() {
        vec![]
    } else {
        query(db, PENDING_TOPICS, vec![EdnValue::Vector(pending.clone())])?
    };
    // Lessons/reviews have a required topic scope. Only assessments need
    // content-based topic discovery; avoid reverse catalog joins for tutorials
    // and worked examples in ordinary lesson routes.
    let assessment_pending: Vec<_> = pending
        .iter()
        .filter(|row| {
            matches!(row, EdnValue::Vector(values) if values.get(2) ==
            Some(&EdnValue::String("activity.type/assessment".into())))
        })
        .cloned()
        .collect();
    if !assessment_pending.is_empty() {
        let mut contents: BTreeMap<u64, Vec<Vec<Json>>> = BTreeMap::new();
        for text in [PENDING_CONTENT, RETAKE_CONTENT] {
            for row in query(db, text, vec![EdnValue::Vector(assessment_pending.clone())])? {
                contents.entry(eid(&row[0])?).or_default().push(row);
            }
        }
        let content_ids = contents.keys().copied().collect();
        if !contents.is_empty() {
            for text in CONTENT_TOPICS {
                for row in query(db, text, vec![ids(&content_ids)?])? {
                    for content in &contents[&eid(&row[1])?] {
                        let mut mapped = content.clone();
                        mapped[0] = row[0].clone();
                        pending_topics.push(mapped);
                    }
                }
            }
        }
    }
    for row in pending_topics {
        let topic = eid(&row[0])?;
        let task = eid(&row[2])?;
        let activity = eid(&row[3])?;
        let kind = row[1]
            .as_str()
            .ok_or("activity kind missing")?
            .strip_prefix("activity.type/")
            .ok_or("unexpected activity kind")?;
        if changes.is_none_or(|c| c.tasks.contains(&task) || c.activities.contains(&activity)) {
            add(
                topic,
                if kind == "lesson" {
                    "unlocked"
                } else {
                    "assigned"
                },
                kind,
                Some(task),
            );
        }
    }
    for row in query(db, REVIEWS, vec![input_eid(learner)?])? {
        let anchor = DateTime::parse_from_rfc3339(row[2].as_str().ok_or("memory anchor missing")?)?
            .timestamp_millis();
        if review_due(
            row[1].as_f64().ok_or("memory missing")?,
            anchor,
            row[3].as_f64().ok_or("interval missing")?,
            row[4].as_f64().ok_or("threshold missing")?,
            now,
        )? {
            add(eid(&row[0])?, "review-due", "review", None);
        }
    }
    for topic in scheduler_topics {
        add(*topic, "scheduler-selected", scheduler_kind, None);
    }
    let selected: BTreeSet<_> = triggers.keys().copied().collect();
    let mut records = BTreeMap::new();
    if !selected.is_empty() {
        for row in query(db, TOPICS, vec![ids(&selected)?])? {
            let topic = eid(&row[0])?;
            let mut record = row[1].clone();
            record["triggers"] = json!(triggers[&topic].iter().map(|(reason, kind, task)|
                json!({"reason":reason,"activity_type":kind,"task":task})).collect::<Vec<_>>());
            record["knowledge_points"] = json!([]);
            records.insert(topic, record);
        }
        if !scheduler_topics
            .iter()
            .all(|topic| records.contains_key(topic))
        {
            return Err("selected entity is not an existing topic".into());
        }
        for row in query(db, KPS, vec![ids(&selected)?])? {
            let mut kp = row[1].clone();
            let generator = kp
                .get("knowledge-point/question-generator")
                .and_then(|g| g.get("db/id"))
                .cloned();
            kp["has_generator"] = json!(generator.is_some());
            kp["generator_entity"] = generator.unwrap_or(Json::Null);
            records.get_mut(&eid(&row[0])?).ok_or("KP topic missing")?["knowledge_points"]
                .as_array_mut()
                .ok_or("KP array missing")?
                .push(kp);
        }
        for record in records.values_mut() {
            record["knowledge_points"]
                .as_array_mut()
                .unwrap()
                .sort_by_key(|k| k["db/id"].as_u64());
        }
    }
    Ok(json!(records.into_values().collect::<Vec<_>>()))
}

fn main() -> Result<()> {
    let mut text = String::new();
    std::io::stdin().read_to_string(&mut text)?;
    let request: Json = serde_json::from_str(&text)?;
    let database = request["database"].as_str().ok_or("database required")?;
    let learner_id = request["learner"].as_str().ok_or("learner required")?;
    let conn = Connection::connect_configured_with_cache_limits(
        postgres_config_from_env()?,
        database,
        512,
        32 * 1024 * 1024,
    )?;
    let db = conn.sync()?;
    let reference = db.snapshot_reference()?;
    let lineage = reference.key().lineage_id().to_string();
    let basis = db.basis_t();
    let rows = query(
        &db,
        "[:find ?l :in $ ?id :where [?l :learner/id ?id]]",
        vec![EdnValue::String(learner_id.into())],
    )?;
    if rows.len() != 1 {
        return Err("expected exactly one matching learner".into());
    }
    let learner = eid(&rows[0][0])?;
    let now = match request["at"].as_str() {
        Some(at) => DateTime::parse_from_rfc3339(at)?.timestamp_millis(),
        None => Utc::now().timestamp_millis(),
    };
    let mut changes = None;
    if let Some(after) = request["after_basis"].as_u64() {
        if request["lineage"].as_str() != Some(&lineage) {
            return Err("cursor lineage mismatch".into());
        }
        if after > basis {
            return Err("cursor is ahead of database basis".into());
        }
        let mut found = Changes::default();
        let unlocked = db
            .entid(&Keyword::new("learner-task.status", "unlocked"))
            .ok_or("unlocked enum missing")?;
        let locked = db
            .entid(&Keyword::new("learner-task.status", "locked"))
            .ok_or("locked enum missing")?;
        let mut expected = after + 1;
        for tx in db
            .log_value()?
            .tx_range(Some(TimePoint::T(after + 1)), Some(TimePoint::T(basis + 1)))?
        {
            let tx = tx?;
            if tx.t != expected {
                return Err("log gap; run a full discovery before advancing cursor".into());
            }
            expected += 1;
            for d in tx.data {
                let attribute = db.schema().attribute(d.attribute)?.ident.qualified_name();
                found.observe(
                    learner, d.entity, &attribute, &d.value, d.added, unlocked, locked,
                );
            }
        }
        if expected != basis + 1 {
            return Err("log gap; run a full discovery before advancing cursor".into());
        }
        if !found.steps.is_empty() {
            for row in query(&db, CHANGED, vec![ids(&found.steps)?])? {
                found.activities.insert(eid(&row[0])?);
            }
        }
        changes = Some(found);
    }
    let topics = request["topics"]
        .as_array()
        .ok_or("topics array required")?
        .iter()
        .map(eid)
        .collect::<Result<BTreeSet<_>>>()?;
    let kind = request["activity_type"].as_str().unwrap_or("assessment");
    if !matches!(kind, "lesson" | "review" | "assessment") {
        return Err("unsupported activity type".into());
    }
    let mut candidates = candidates(&db, learner, now, changes.as_ref(), &topics, kind)?;
    find_candidates_ranking::annotate(&db, learner, now, &mut candidates)?;
    println!(
        "{}",
        serde_json::to_string_pretty(&json!({"database":database,"learner":learner_id,
        "basis":basis,"cursor":{"lineage":lineage,"basis":basis},"at":DateTime::<Utc>::from_timestamp_millis(now),
        "topics":candidates}))?
    );
    Ok(())
}
