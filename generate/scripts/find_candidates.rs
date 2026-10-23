//! Read-only generator eligibility. All facts and cursor validation share one DB value.
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
const STUDIED: &str = include_str!("queries/studied-topics.edn");
const COMPLETED_LESSONS: &str = include_str!("queries/completed-lesson-topics.edn");

mod find_candidates_ranking;
#[cfg(test)]
mod find_candidates_tests;

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
        pending_states: &[u64],
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
            ("learner-task/status", Value::Ref(state)) if pending_states.contains(state) => {
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

fn direct_neighbors(
    db: &DatabaseValue,
    seeds: &BTreeSet<u64>,
    prerequisites: bool,
) -> Result<BTreeSet<u64>> {
    let attribute = |name: &str| -> Result<u32> {
        let (ns, attr) = name.split_once('/').unwrap();
        db.schema()
            .resolve_ident(&Keyword::new(ns, attr))
            .ok_or_else(|| format!("missing {name}").into())
    };
    let next = attribute("topic/next")?;
    let kps = attribute("topic/knowledge-points")?;
    let keys = attribute("knowledge-point/key-prerequisites")?;
    let identity = attribute("topic/id")?;
    let forward = |entity, attr| -> Result<BTreeSet<u64>> {
        db.values(entity, attr)?
            .into_iter()
            .map(|v| match v {
                Value::Ref(id) => Ok(id),
                _ => Err("curriculum edge must be a reference".into()),
            })
            .collect()
    };
    // These refs are not AVET-indexed. Explicit VAET prefixes avoid an attribute
    // scan for every seed when the query planner chooses a reverse graph join.
    let reverse = |entity, attr| -> Result<BTreeSet<u64>> {
        Ok(db
            .collect_datoms_with_prefix(&edb_core::IndexPrefix::Vaet {
                value: Value::Ref(entity),
                attribute: Some(attr),
                entity: None,
            })?
            .into_iter()
            .map(|d| d.entity)
            .collect())
    };
    let mut neighbors = BTreeSet::new();
    for &topic in seeds {
        if prerequisites {
            neighbors.extend(reverse(topic, next)?);
            for kp in forward(topic, kps)? {
                neighbors.extend(forward(kp, keys)?);
            }
        } else {
            neighbors.extend(forward(topic, next)?);
            for kp in reverse(topic, keys)? {
                neighbors.extend(reverse(kp, kps)?);
            }
        }
    }
    neighbors
        .into_iter()
        .filter_map(|topic| match db.values(topic, identity) {
            Ok(values) if values.is_empty() => None,
            Ok(_) => Some(Ok(topic)),
            Err(error) => Some(Err(error.into())),
        })
        .collect()
}

fn urgency_groups(
    db: &DatabaseValue,
    learner: u64,
    now: i64,
) -> Result<BTreeMap<u64, BTreeSet<(u8, String)>>> {
    let mut groups = BTreeMap::<u64, BTreeSet<(u8, String)>>::new();
    let mut selected = BTreeSet::new();
    let mut descendants_of = BTreeSet::new();
    let selections = EdnValue::Vector(vec![
        EdnValue::Keyword(Keyword::new("learner", "queue")),
        EdnValue::Keyword(Keyword::new("learner", "targets")),
    ]);
    for row in query(db, SELECTED, vec![input_eid(learner)?, selections])? {
        let topic = eid(&row[0])?;
        selected.insert(topic);
        let (value, name) = if row[1] == "learner/targets" {
            (4, "target")
        } else {
            descendants_of.insert(topic);
            (3, "queued")
        };
        groups
            .entry(topic)
            .or_default()
            .insert((value, name.into()));
    }
    // Materialize the learner's small owned sets before joins. An or-join over
    // profiles plus lesson history otherwise expands catalog-wide on real data.
    let owned = |name: &str| -> Result<BTreeSet<u64>> {
        let (ns, attr) = name.split_once('/').unwrap();
        let attr = db
            .schema()
            .resolve_ident(&Keyword::new(ns, attr))
            .ok_or("learner membership attribute missing")?;
        db.values(learner, attr)?
            .into_iter()
            .map(|v| match v {
                Value::Ref(id) => Ok(id),
                _ => Err("learner membership must be a reference".into()),
            })
            .collect()
    };
    let mut studied = BTreeSet::new();
    let mut known_lessons = BTreeSet::new();
    let mut ready = BTreeSet::new();
    let at = DateTime::<Utc>::from_timestamp_millis(now).ok_or("invalid ranking time")?;
    let profiles = owned("learner/knowledge-profile")?;
    if !profiles.is_empty() {
        for row in query(db, STUDIED, vec![ids(&profiles)?])? {
            let record = row[1].as_object().ok_or("progress record missing")?.clone();
            let threshold = row[1]["progress/policy"]["policy/review-threshold"].as_f64();
            if course_academy_engine::learning::progress_ready(&record, threshold, at)? {
                ready.insert(eid(&row[0])?);
            }
            let learned = row[1].get("progress/learned").and_then(Json::as_bool);
            let repetitions = row[1]
                .get("progress/repetitions")
                .and_then(Json::as_f64)
                .unwrap_or(0.0);
            if learned == Some(true) || learned.is_none() && repetitions > 0.0 {
                studied.insert(eid(&row[0])?);
            }
            // New lesson preparation uses the graph's band-one boundary.
            // Keep broad studied/review maintenance on its existing evidence.
            if learned == Some(true) || repetitions >= 1.0 {
                known_lessons.insert(eid(&row[0])?);
            }
        }
    }
    let tasks = owned("learner/activity")?;
    if !tasks.is_empty() {
        for row in query(db, COMPLETED_LESSONS, vec![ids(&tasks)?])? {
            studied.insert(eid(&row[0])?);
            known_lessons.insert(eid(&row[0])?);
        }
    }
    for &topic in &studied {
        descendants_of.insert(topic);
        groups
            .entry(topic)
            .or_default()
            .insert((5, "studied".into()));
    }
    if let Some(scope) = find_candidates_ranking::bounded_lesson_scope(db, learner)? {
        // Ordinary self-directed preparation matches the visible depth-two
        // graph scope, regardless of prerequisite mastery or current stock.
        for topic in scope.difference(&selected).filter(|topic| !known_lessons.contains(topic)) {
            groups
                .entry(*topic)
                .or_default()
                .insert((2, "selected-prerequisite".into()));
        }
    } else {
        // Course mode retains its operational prerequisite preparation.
        let mut visited = selected.clone();
        let mut frontier = selected;
        while !frontier.is_empty() {
            let next: BTreeSet<_> = direct_neighbors(db, &frontier, true)?
                .into_iter()
                .filter(|t| !ready.contains(t) && !visited.contains(t))
                .collect();
            for &topic in &next {
                groups.entry(topic).or_default().insert((2, "selected-prerequisite".into()));
            }
            visited.extend(next.iter().copied());
            frontier = next;
        }
    }
    if !descendants_of.is_empty() {
        for topic in direct_neighbors(db, &descendants_of, false)? {
            groups
                .entry(topic)
                .or_default()
                .insert((1, "studied-or-queued-descendant".into()));
        }
    }
    Ok(groups)
}

fn registered_topics(db: &DatabaseValue) -> Result<BTreeSet<u64>> {
    let attribute = |name: &str| -> Result<u32> {
        let (ns, attr) = name.split_once('/').unwrap();
        db.schema()
            .resolve_ident(&Keyword::new(ns, attr))
            .ok_or_else(|| format!("missing {name}").into())
    };
    let script = attribute("question-generator/script")?;
    let generator = attribute("knowledge-point/question-generator")?;
    let kps = attribute("topic/knowledge-points")?;
    // Only scan the small registered-script attribute. Explicit reverse ref
    // prefixes avoid catalog-wide topic/KP joins and never read question pools.
    let mut topics = BTreeSet::new();
    for registration in db.collect_datoms_with_prefix(&edb_core::IndexPrefix::Aevt {
        attribute: script,
        entity: None,
        value: None,
    })? {
        if !matches!(&registration.value, Value::String(path) if path.starts_with("generators/")) {
            continue;
        }
        for kp in db.collect_datoms_with_prefix(&edb_core::IndexPrefix::Vaet {
            value: Value::Ref(registration.entity),
            attribute: Some(generator),
            entity: None,
        })? {
            for topic in db.collect_datoms_with_prefix(&edb_core::IndexPrefix::Vaet {
                value: Value::Ref(kp.entity),
                attribute: Some(kps),
                entity: None,
            })? {
                topics.insert(topic.entity);
            }
        }
    }
    Ok(topics)
}

#[cfg(test)]
fn candidates(
    db: &DatabaseValue,
    learner: u64,
    now: i64,
    changes: Option<&Changes>,
    scheduler_topics: &BTreeSet<u64>,
    scheduler_kind: &str,
    include_registered: bool,
) -> Result<Json> {
    candidates_scoped(
        db,
        learner,
        now,
        changes,
        scheduler_topics,
        scheduler_kind,
        include_registered,
        false,
    )
}

fn candidates_scoped(
    db: &DatabaseValue,
    learner: u64,
    now: i64,
    _changes: Option<&Changes>,
    scheduler_topics: &BTreeSet<u64>,
    scheduler_kind: &str,
    include_registered: bool,
    selected_only: bool,
) -> Result<Json> {
    // A ranking needs the complete eligible population. A cursor validates the
    // captured lineage/log but must never hide unchanged queue or study facts.
    let selections = EdnValue::Vector(vec![
        EdnValue::Keyword(Keyword::new("learner", "queue")),
        EdnValue::Keyword(Keyword::new("learner", "targets")),
    ]);
    let selection_rows = query(db, SELECTED, vec![input_eid(learner)?, selections])?;
    let direct: BTreeSet<_> = selection_rows
        .iter()
        .map(|row| eid(&row[0]))
        .collect::<Result<_>>()?;
    if selected_only && direct.is_empty() && !include_registered {
        return Ok(json!([]));
    }
    // The primary phase does not enumerate studied topics, prerequisite or
    // downstream banks. Registered packages may still be included for refill
    // maintenance without expanding the population eligible for authoring.
    let mut groups = if selected_only {
        let mut groups = BTreeMap::<u64, BTreeSet<(u8, String)>>::new();
        for row in &selection_rows {
            let membership = if row[1] == "learner/targets" {
                (4, "target")
            } else {
                (3, "queued")
            };
            groups
                .entry(eid(&row[0])?)
                .or_default()
                .insert((membership.0, membership.1.into()));
        }
        groups
    } else {
        urgency_groups(db, learner, now)?
    };
    let mut triggers: BTreeMap<u64, BTreeSet<(String, String, Option<u64>)>> = BTreeMap::new();
    let mut add = |topic, reason: &str, kind: &str, task| {
        if selected_only && !direct.contains(&topic) {
            return;
        }
        triggers
            .entry(topic)
            .or_default()
            .insert((reason.into(), kind.into(), task));
    };
    for row in selection_rows {
        let topic = eid(&row[0])?;
        let reason = row[1].as_str().ok_or("selection ident missing")?;
        add(topic, reason, "lesson", None);
    }
    let mut pending = vec![];
    for row in query(db, PENDING, vec![input_eid(learner)?])? {
        let task = eid(&row[0])?;
        let activity = eid(&row[1])?;
        pending.push(EdnValue::Vector(vec![
            input_eid(task)?,
            input_eid(activity)?,
            EdnValue::String(row[2].as_str().ok_or("activity kind missing")?.into()),
            EdnValue::String(row[3].as_str().ok_or("activity state missing")?.into()),
        ]));
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
        let kind = row[1]
            .as_str()
            .ok_or("activity kind missing")?
            .strip_prefix("activity.type/")
            .ok_or("unexpected activity kind")?;
        add(
            topic,
            if kind == "lesson" {
                row[4]
                    .as_str()
                    .ok_or("activity state missing")?
                    .strip_prefix("learner-task.status/")
                    .ok_or("unexpected activity state")?
            } else {
                "assigned"
            },
            kind,
            Some(task),
        );
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
    // Actual pending and due work is eligible even outside selected curriculum.
    // Selection membership is not itself an immediate obligation.
    for (&topic, reasons) in &triggers {
        for (reason, _, task) in reasons {
            if matches!(reason.as_str(), "learner/queue" | "learner/targets") {
                continue;
            }
            let mut immediate = reason == "scheduler-selected";
            if let Some(task) = task {
                let status = db
                    .schema()
                    .resolve_ident(&Keyword::new("learner-task", "status"))
                    .unwrap();
                let active: BTreeSet<_> = ["started", "paused"]
                    .iter()
                    .filter_map(|state| db.entid(&Keyword::new("learner-task.status", *state)))
                    .collect();
                immediate |= db
                    .values(*task, status)?
                    .iter()
                    .any(|v| matches!(v, Value::Ref(id) if active.contains(id)));
                if let Some(attr) = db
                    .schema()
                    .resolve_ident(&Keyword::new("learner-task", "remediation-for"))
                {
                    immediate |= !db.values(*task, attr)?.is_empty();
                }
                if let Some(attr) = db
                    .schema()
                    .resolve_ident(&Keyword::new("learner-task", "priority"))
                {
                    immediate |= db
                        .values(*task, attr)?
                        .iter()
                        .any(|v| matches!(v, Value::Double(n) if *n >= 12000.0));
                }
            }
            groups.entry(topic).or_default().insert(if immediate {
                (7, "immediate".into())
            } else {
                (6, "current-need".into())
            });
        }
    }
    let mut selected: BTreeSet<_> = groups.keys().copied().collect();
    if include_registered {
        selected.extend(registered_topics(db)?);
    }
    let mut records = BTreeMap::new();
    if !scheduler_topics.is_empty()
        && query(db, TOPICS, vec![ids(scheduler_topics)?])?.len() != scheduler_topics.len()
    {
        return Err("selected entity is not an existing topic".into());
    }
    if !selected.is_empty() {
        for row in query(db, TOPICS, vec![ids(&selected)?])? {
            let topic = eid(&row[0])?;
            let mut record = row[1].clone();
            record["triggers"] =
                json!(triggers.get(&topic).into_iter().flatten().map(|(reason, kind, task)|
                json!({"reason":reason,"activity_type":kind,"task":task})).collect::<Vec<_>>());
            let memberships = groups.get(&topic).cloned().unwrap_or_default();
            record["urgency_groups"] = json!(
                memberships
                    .iter()
                    .rev()
                    .map(|(_, name)| name)
                    .collect::<Vec<_>>()
            );
            record["urgency_value"] = json!(memberships.last().map_or(0, |(value, _)| *value));
            record["studied"] = json!(memberships.iter().any(|(_, name)| name == "studied"));
            record["knowledge_points"] = json!([]);
            records.insert(topic, record);
        }
        for row in query(db, KPS, vec![ids(&selected)?])? {
            let topic = eid(&row[0])?;
            let mut kp = row[1].clone();
            let generator = kp
                .get("knowledge-point/question-generator")
                .and_then(|g| g.get("db/id"))
                .cloned();
            let script = kp
                .get("knowledge-point/question-generator")
                .and_then(|g| g.get("question-generator/script"))
                .and_then(Json::as_str)
                .filter(|s| !s.trim().is_empty())
                .map(str::to_owned);
            // Outside direct selections, the primary pass only inventories
            // immutable registered packages. Unregistered sibling KPs must not
            // enter the ranking/inventory pass merely by sharing a topic.
            if selected_only
                && !direct.contains(&topic)
                && !script
                    .as_ref()
                    .is_some_and(|s| s.starts_with("generators/"))
            {
                continue;
            }
            kp["has_generator"] = json!(script.is_some());
            kp["generator_script"] = json!(script);
            kp["generator_entity"] = generator.unwrap_or(Json::Null);
            records.get_mut(&topic).ok_or("KP topic missing")?["knowledge_points"]
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
        let pending_states = ["unlocked", "locked", "started", "paused"]
            .iter()
            .map(|state| {
                db.entid(&Keyword::new("learner-task.status", *state))
                    .ok_or("pending status enum missing")
            })
            .collect::<std::result::Result<Vec<_>, _>>()?;
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
                    learner,
                    d.entity,
                    &attribute,
                    &d.value,
                    d.added,
                    &pending_states,
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
    let include_registered = match request.get("include_registered") {
        Some(value) => value
            .as_bool()
            .ok_or("include_registered must be a boolean")?,
        None => false,
    };
    let selected_only = match request.get("selected_only") {
        Some(value) => value.as_bool().ok_or("selected_only must be a boolean")?,
        None => false,
    };
    let mut candidates = candidates_scoped(
        &db,
        learner,
        now,
        changes.as_ref(),
        &topics,
        kind,
        include_registered,
        selected_only,
    )?;
    find_candidates_ranking::annotate(&db, learner, now, &mut candidates)?;
    println!(
        "{}",
        serde_json::to_string_pretty(&json!({"database":database,"learner":learner_id,
        "basis":basis,"cursor":{"lineage":lineage,"basis":basis},"at":DateTime::<Utc>::from_timestamp_millis(now),
        "selected_only":selected_only,"topics":candidates}))?
    );
    Ok(())
}
