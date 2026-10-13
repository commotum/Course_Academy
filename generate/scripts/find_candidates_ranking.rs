//! Minimal captured projection for the engine's ranking and availability rules.
use super::*;
use course_academy_engine::{assessment_sampling, learning, schema::{EntitySnapshot, Record}};
use edb_core::{Cardinality, IndexPrefix};

fn value(v: &Value) -> Result<Json> {
    Ok(match v {
        Value::String(v) | Value::Uri(v) => json!(v),
        Value::Long(v) => json!(v),
        Value::Double(v) => json!(v),
        Value::Float(v) => json!(v),
        Value::Bool(v) => json!(v),
        Value::Ref(v) => json!(v),
        Value::Keyword(v) => json!({"$keyword":v.qualified_name()}),
        Value::Uuid(v) => {
            let s = format!("{v:032x}");
            json!({"$uuid":format!("{}-{}-{}-{}-{}",&s[..8],&s[8..12],&s[12..16],&s[16..20],&s[20..])})
        }
        Value::Instant(v) => json!({"$instant":v}),
        _ => return Err("unsupported ranking value".into()),
    })
}
fn insert(db: &DatabaseValue, records: &mut BTreeMap<u64, Record>, d: &edb_core::Datom) -> Result<()> {
    let a = db.schema().attribute(d.attribute)?;
    let name = a.ident.qualified_name();
    if (name.starts_with("db/") || name.starts_with("db.")) && name != "db/ident" { return Ok(()); }
    let v = value(&d.value)?;
    let row = records.entry(d.entity).or_default();
    if a.cardinality == Cardinality::Many {
        let values = row.entry(name).or_insert(json!([])).as_array_mut().unwrap();
        if !values.contains(&v) { values.push(v); }
    } else { row.insert(name, v); }
    if let Value::Ref(child) = &d.value { records.entry(*child).or_default(); }
    Ok(())
}
fn refs(records: &BTreeMap<u64, Record>, entity: u64, attr: &str) -> Vec<u64> {
    match records.get(&entity).and_then(|r| r.get(attr)) {
        Some(Json::Array(v)) => v.iter().filter_map(Json::as_u64).collect(),
        Some(v) => v.as_u64().into_iter().collect(),
        None => vec![],
    }
}

pub(super) fn annotate(db: &DatabaseValue, learner: u64, now: i64, topics: &mut Json) -> Result<()> {
    if topics.as_array().ok_or("topics array missing")?.is_empty() { return Ok(()); }
    let mut records = BTreeMap::new();
    // Bounded attribute reads for curriculum support; never scan all questions.
    for name in ["db/ident", "topic/id", "topic/next", "topic/knowledge-points",
                 "knowledge-point/key-prerequisites", "knowledge-point/canonical-example",
                 "policy/id", "policy/review-threshold"] {
        let (ns, attr) = name.split_once('/').unwrap();
        if let Some(a) = db.schema().resolve_ident(&Keyword::new(ns, attr)) {
            for d in db.collect_datoms_with_prefix(&IndexPrefix::Aevt { attribute:a, entity:None, value:None })? {
                insert(db, &mut records, &d)?;
            }
        }
    }
    let selected_kps: BTreeSet<u64> = topics.as_array().unwrap().iter()
        .flat_map(|t| t["knowledge_points"].as_array().unwrap()).map(|k| eid(&k["db/id"]))
        .collect::<Result<_>>()?;
    let mut pending = BTreeSet::from([learner]);
    pending.extend(selected_kps.iter().copied());
    let mut visited = BTreeSet::new();
    let mut selected_since = BTreeMap::<(u64, String), i64>::new();
    while let Some(e) = pending.pop_first() {
        if !visited.insert(e) { continue; }
        records.entry(e).or_default();
        for d in db.collect_datoms_with_prefix(&IndexPrefix::Eavt { entity:e, attribute:None, value:None })? {
            let name = db.schema().attribute(d.attribute)?.ident.qualified_name();
            if e == learner && matches!(name.as_str(), "learner/queue" | "learner/targets") {
                if let Value::Ref(topic) = &d.value {
                    for stamp in db.values(d.tx, edb_core::DB_TX_INSTANT as u32)? {
                        if let Value::Instant(ms) = stamp {
                            selected_since.entry((*topic, name.clone())).and_modify(|t| *t=(*t).min(ms)).or_insert(ms);
                        }
                    }
                }
            }
            insert(db, &mut records, &d)?;
        }
        for attr in ["learner/activity", "learner/knowledge-profile", "learner/assignments",
                     "learner-task/activity", "learner-task/items", "activity/steps", "step/content",
                     "task-item/content", "assigned-problem/content", "multistep/steps",
                     "question/answer-fields", "answer-field/choices", "answer-field/correct"] {
            pending.extend(refs(&records, e, attr));
        }
        if selected_kps.contains(&e) {
            pending.extend(refs(&records, e, "knowledge-point/questions"));
            pending.extend(refs(&records, e, "knowledge-point/canonical-example"));
        }
    }
    let s = EntitySnapshot::new(records, db.basis_t()).map_err(|e| format!("ranking projection: {e}"))?;
    let at = DateTime::<Utc>::from_timestamp_millis(now).ok_or("invalid ranking time")?;
    let priorities = learning::inventory_priorities(&s, learner, at)?;
    let unavailable = learning::unavailable_questions(&s, learner)?;
    let queued: BTreeSet<_> = s.refs(learner, "learner/queue")?.into_iter().collect();
    let targeted: BTreeSet<_> = s.refs(learner, "learner/targets")?.into_iter().collect();
    let bands = ["easy", "moderate", "hard"];
    let inventory = |kps: &[u64]| -> Result<Json> {
        let qs = assessment_sampling::pool(&s, kps, &unavailable)?;
        let mut counts = [0usize;3];
        let mut supported = BTreeSet::new();
        for &kp in kps {
            for q in s.refs(kp, "knowledge-point/questions")?.into_iter()
                .chain(s.optional_ref(kp, "knowledge-point/canonical-example")?) {
                if let Some(band) = assessment_sampling::band(&s,q)? { supported.insert(band); }
            }
        }
        for q in qs { counts[assessment_sampling::band(&s,q)?.unwrap()] += 1; }
        Ok(json!({"available": {"easy":counts[0],"moderate":counts[1],"hard":counts[2]},
            "supported_difficulties":supported.into_iter().map(|b|bands[b]).collect::<Vec<_>>()}))
    };
    for t in topics.as_array_mut().unwrap() {
        let topic = eid(&t["db/id"])?;
        let priority = &priorities[&topic];
        let needed = priority.ongoing || t["triggers"].as_array().unwrap().iter()
            .any(|tr| matches!(tr["reason"].as_str(),Some("assigned" | "scheduler-selected")));
        let state = if needed { "needed-now" } else if queued.contains(&topic) { "queued" }
            else if targeted.contains(&topic) || priority.target_count > 0 { "target-related" } else { "unlocked" };
        let mut score = priority.priority;
        for task in s.refs(learner,"learner/activity")? {
            let status = s.entity(task)?.get("learner-task/status").map(|v|s.ident(v)).transpose()?;
            if !matches!(status.as_deref(),Some("learner-task.status/locked" | "learner-task.status/unlocked" | "learner-task.status/started" | "learner-task.status/paused")) { continue; }
            let activity = s.reference(task,"learner-task/activity")?;
            if s.optional_ref(activity,"activity/scope")? == Some(topic)
                || t["triggers"].as_array().unwrap().iter().any(|tr|tr["task"].as_u64()==Some(task)) {
                if let Some(stored) = s.entity(task)?.get("learner-task/priority").and_then(Json::as_f64) { score=score.max(stored); }
            }
        }
        t["activity_state"] = json!(state);
        t["engine_priority"] = json!(score);
        t["assignment_due"] = json!(priority.due.map(|d| d.to_rfc3339()));
        let mut waiting = selected_since.get(&(topic, if state=="queued" { "learner/queue" } else { "learner/targets" }.into())).copied();
        if needed {
            waiting = None;
            for trigger in t["triggers"].as_array().unwrap() {
                if let Some(task) = trigger["task"].as_u64() {
                    if let Some(at) = s.entity(task)?.get("learner-task/offered-at") {
                        let ms = course_academy_engine::schema::parse_instant(at)?.timestamp_millis();
                        waiting = Some(waiting.map_or(ms, |old|old.min(ms)));
                    }
                }
            }
        }
        t["waiting_since"] = json!(waiting.and_then(DateTime::<Utc>::from_timestamp_millis).map(|d|d.to_rfc3339()));
        let kps: Vec<_> = t["knowledge_points"].as_array().unwrap().iter()
            .map(|kp| eid(&kp["db/id"])).collect::<Result<_>>()?;
        t["topic_inventory"] = inventory(&kps)?;
        for kp in t["knowledge_points"].as_array_mut().unwrap() {
            kp["inventory"] = inventory(&[eid(&kp["db/id"]) ?])?;
        }
    }
    Ok(())
}
