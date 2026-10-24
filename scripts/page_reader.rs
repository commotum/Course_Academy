//! Small read-only list projections, independent of scheduler/write admission.
use super::*;

fn attribute(db: &DatabaseValue, name: &str) -> Result<u32> {
    let (ns, name) = name.split_once('/').ok_or("Invalid attribute")?;
    Ok(db
        .schema()
        .resolve_ident(&Keyword::new(ns, name))
        .ok_or("Missing page schema")?)
}

pub(super) fn record(db: &DatabaseValue, entity: u64) -> Result<Record> {
    let mut record = Record::new();
    for d in db.collect_datoms_with_prefix(&IndexPrefix::Eavt {
        entity,
        attribute: None,
        value: None,
    })? {
        let a = db.schema().attribute(d.attribute)?;
        let name = a.ident.qualified_name();
        if name.starts_with("db/") || name.starts_with("db.") {
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
    Ok(record)
}

pub(super) fn references(record: &Record, name: &str) -> Vec<u64> {
    match record.get(name) {
        Some(Json::Array(values)) => values.iter().filter_map(Json::as_u64).collect(),
        Some(value) => value.as_u64().into_iter().collect(),
        None => vec![],
    }
}

fn capture(db: &DatabaseValue, learner: &str, assignments: bool) -> Result<(EntitySnapshot, u64)> {
    let learner = db
        .collect_datoms_with_prefix(&IndexPrefix::Avet {
            attribute: attribute(db, "learner/id")?,
            value: Some(Value::String(learner.into())),
            entity: None,
        })?
        .first()
        .ok_or("Learner not found")?
        .entity;
    let mut entities = BTreeMap::new();
    let mut pending = BTreeSet::from([learner]);
    // Past assertions can refer to statuses absent from current records.
    for (ns, names) in [
        (
            "learner-task.status",
            &[
                "locked",
                "unlocked",
                "started",
                "paused",
                "completed",
                "failed",
            ][..],
        ),
        (
            "task-item.status",
            &[
                "started",
                "paused",
                "completed",
                "skipped",
                "correct",
                "incorrect",
            ][..],
        ),
    ] {
        for name in names {
            let ident = Keyword::new(ns, *name);
            let id = db.entid(&ident).ok_or("Missing status ident")?;
            entities
                .entry(id)
                .or_insert_with(Record::new)
                .insert("db/ident".into(), kw(&ident.qualified_name()));
        }
    }
    // Keep the complete canonical-example classification without fetching the
    // question bank. EntitySnapshot uses these facts to distinguish examples.
    for d in db.collect_datoms_with_prefix(&IndexPrefix::Aevt {
        attribute: attribute(db, "knowledge-point/canonical-example")?,
        entity: None,
        value: None,
    })? {
        entities
            .entry(d.entity)
            .or_insert_with(Record::new)
            .insert("knowledge-point/canonical-example".into(), value(&d.value)?);
    }
    if assignments {
        for d in db.collect_datoms_with_prefix(&IndexPrefix::Aevt {
            attribute: attribute(db, "course-group/id")?,
            entity: None,
            value: None,
        })? {
            pending.insert(d.entity);
        }
    }
    let mut loaded = BTreeSet::new();
    while let Some(entity) = pending.pop_first() {
        if !loaded.insert(entity) {
            continue;
        }
        let record = record(db, entity)?;
        // Enum identities are already resident in this captured DB dictionary.
        // Add them directly rather than fetching enum entities one at a time.
        for v in record.values().flat_map(|v| match v {
            Json::Array(v) => v.iter().collect::<Vec<_>>(),
            v => vec![v],
        }) {
            if let Some((id, ident)) = v
                .as_u64()
                .and_then(|id| db.ident(id).map(|ident| (id, ident)))
            {
                entities
                    .entry(id)
                    .or_insert_with(Record::new)
                    .insert("db/ident".into(), kw(&ident.qualified_name()));
            }
        }
        let edges: &[&str] = if entity == learner {
            if assignments {
                &[
                    "learner/assignments",
                    "learner/activity",
                    "learner/course",
                    "learner/targets",
                    "learner/queue",
                ]
            } else {
                &[
                    "learner/activity",
                    "learner/course",
                    "learner/targets",
                    "learner/queue",
                ]
            }
        } else if record.contains_key("learner-task/activity") {
            if assignments {
                &["learner-task/activity"]
            } else {
                &["learner-task/activity", "learner-task/items"]
            }
        } else if record.contains_key("activity/id") {
            if assignments
                && record
                    .get("activity/type")
                    .and_then(Json::as_u64)
                    .and_then(|id| db.ident(id))
                    .is_some_and(|ident| ident.qualified_name() == "activity.type/assignment")
            {
                &["activity/course", "activity/steps", "activity/first-step"]
            } else {
                &["activity/course"]
            }
        } else if record.contains_key("task-item/content") {
            &["task-item/content"]
        } else if assignments && record.contains_key("step/id") {
            &["step/content", "step/next"]
        } else if assignments && record.contains_key("assigned-problem/id") {
            &[
                "assigned-problem/content",
                "assigned-problem/topic-coverage",
            ]
        } else if assignments && record.contains_key("multistep/id") {
            &["multistep/steps", "multistep/first-step"]
        } else if assignments && record.contains_key("course-group/id") {
            &["course-group/courses"]
        } else {
            &[]
        };
        for edge in edges {
            pending.extend(references(&record, edge));
        }
        entities
            .entry(entity)
            .or_insert_with(Record::new)
            .extend(record);
    }
    let mut s = EntitySnapshot::new(entities, db.basis_t())?;
    refresh_history(db, &mut s)?;
    Ok((s, learner))
}

pub(super) fn capture_stats(db: &DatabaseValue, learner: &str) -> Result<(EntitySnapshot,u64)> {
    let learner = db.collect_datoms_with_prefix(&IndexPrefix::Avet {
        attribute:attribute(db,"learner/id")?, value:Some(Value::String(learner.into())),entity:None,
    })?.first().ok_or("Learner not found")?.entity;
    let mut entities=BTreeMap::from([(learner,record(db,learner)?)]);
    for task in references(&entities[&learner],"learner/activity") {
        let task_record=record(db,task)?;
        for item in references(&task_record,"learner-task/items") { entities.insert(item,record(db,item)?); }
        // Activity totals use completed attempts, never inferred repetitions.
        let completed=task_record.get("learner-task/status").and_then(Json::as_u64).and_then(|id|db.ident(id))
            .is_some_and(|ident|ident.qualified_name()=="learner-task.status/completed");
        for activity in references(&task_record,"learner-task/activity").into_iter().filter(|_|completed) {
            if !entities.contains_key(&activity) { entities.insert(activity,record(db,activity)?); }
            for topic in references(&entities[&activity],"activity/scope") {
                if !entities.contains_key(&topic) { entities.insert(topic,record(db,topic)?); }
            }
        }
        entities.insert(task,task_record);
    }
    for (ns,names) in [("learner-task.status",&["locked","unlocked","started","paused","completed","failed"][..]),
        ("task-item.status",&["started","paused","completed","skipped","correct","incorrect"][..]),
        ("activity.type",&["lesson","review","assessment","diagnostic","assignment"][..])] {
        for name in names {
            let ident=Keyword::new(ns,*name);
            entities.insert(db.entid(&ident).ok_or("Missing status ident")?,Record::from_iter([("db/ident".into(),kw(&ident.qualified_name()))]));
        }
    }
    let mut snapshot=EntitySnapshot::new(entities,db.basis_t())?;
    refresh_history(db,&mut snapshot)?;
    Ok((snapshot,learner))
}

pub(super) fn serve(database: String, learner: String) -> Result<bool> {
    let conn = Connection::connect_configured_with_cache_limits(
        postgres_config_from_env()?,
        database,
        512,
        16 * 1024 * 1024,
    )?;
    let mut cache: BTreeMap<bool, (SnapshotReference, EntitySnapshot, u64)> = BTreeMap::new();
    let mut stats_cache: Option<(SnapshotReference,EntitySnapshot,u64)> = None;
    let mut forecast_cache: Option<(SnapshotReference,forecast_reader::Capture)> = None;
    let stdin = std::io::stdin();
    let stdout = std::io::stdout();
    let mut output = stdout.lock();
    for line in stdin.lock().lines() {
        let result = (|| -> Result<Json> {
            let body: Json = serde_json::from_str(&line?)?;
            let stats = body["action"] == "study-stats";
            let forecast = body["action"] == "forecast-inputs";
            let assignments = match body["action"].as_str() {
                Some("assignments") => true,
                Some("activity-history"|"study-stats"|"forecast-inputs") => false,
                _ => return Err("Page reader accepts only read-only list actions".into()),
            };
            let started = Instant::now();
            let db = conn.sync()?;
            let reference = db.snapshot_reference()?;
            if forecast {
                if forecast_cache.as_ref().is_none_or(|(old,_)|*old!=reference) {
                    forecast_cache=Some((reference,forecast_reader::capture(&db,&learner)?));
                }
                return forecast_reader::read(&forecast_cache.as_ref().unwrap().1,&body,Utc::now());
            }
            if stats {
                if stats_cache.as_ref().is_none_or(|(old,_,_)|*old!=reference) {
                    let (s,learner)=capture_stats(&db,&learner)?;
                    stats_cache=Some((reference,s,learner));
                }
                let (_,s,learner)=stats_cache.as_ref().unwrap();
                return study_stats::summary(s,*learner,&body,Utc::now());
            }
            if cache
                .get(&assignments)
                .is_none_or(|(old, _, _)| *old != reference)
            {
                let (s, learner) = capture(&db, &learner, assignments)?;
                cache.insert(assignments, (reference, s, learner));
            }
            let (_, s, learner) = &cache[&assignments];
            let result = if assignments {
                assignment_reader::list(s, *learner)
            } else {
                activity_history::list(s, *learner, &body)
            };
            trace("page-list", started);
            result
        })();
        serde_json::to_writer(&mut output, &envelope(result))?;
        output.write_all(b"\n")?;
        output.flush()?;
    }
    Ok(true)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    #[ignore = "read-only comparison against configured database"]
    fn page_projection_matches_full_database() -> Result<()> {
        let conn = Connection::connect_configured(
            postgres_config_from_env()?,
            std::env::var("EDB_DATABASE")?,
            2048,
        )?;
        let db = conn.db();
        let learner = std::env::var("PAGE_TEST_LEARNER")?;
        let full = snapshot(&db)?;
        for assignments in [false, true] {
            let (small, eid) = capture(&db, &learner, assignments)?;
            assert!(small.entities.len() < full.entities.len());
            if assignments {
                assert_eq!(
                    assignment_reader::list(&small, eid)?,
                    assignment_reader::list(&full, eid)?
                );
            } else {
                assert_eq!(
                    activity_history::list(&small, eid, &json!({}))?,
                    activity_history::list(&full, eid, &json!({}))?
                );
            }
        }
        let started=Instant::now();
        let (small,eid)=capture_stats(&db,&learner)?;
        let at=Utc::now();
        let day=86_400_000i64;
        let first=at.timestamp_millis()/day*day-6*day;
        let body=json!({"dayStarts":(0..8).map(|i|first+i*day).collect::<Vec<_>>()});
        assert_eq!(study_stats::summary(&small,eid,&body,at)?,study_stats::summary(&full,eid,&body,at)?);
        assert!(small.entities.len()<full.entities.len());
        eprintln!("Stats projection: {} entities vs {} full, {:.1} ms",small.entities.len(),full.entities.len(),started.elapsed().as_secs_f64()*1000.);
        Ok(())
    }
}
