//! Captured demand, graph order and engine priority for generator ranking.
use super::*;
use course_academy_engine::{
    assessment_sampling, learning,
    schema::{EntitySnapshot, Record},
};
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
fn insert(
    db: &DatabaseValue,
    records: &mut BTreeMap<u64, Record>,
    d: &edb_core::Datom,
) -> Result<()> {
    let a = db.schema().attribute(d.attribute)?;
    let name = a.ident.qualified_name();
    if (name.starts_with("db/") || name.starts_with("db.")) && name != "db/ident" {
        return Ok(());
    }
    let v = value(&d.value)?;
    let row = records.entry(d.entity).or_default();
    if a.cardinality == Cardinality::Many {
        let values = row.entry(name).or_insert(json!([])).as_array_mut().unwrap();
        if !values.contains(&v) {
            values.push(v);
        }
    } else {
        row.insert(name, v);
    }
    if let Value::Ref(child) = &d.value {
        records.entry(*child).or_default();
    }
    Ok(())
}
fn refs(records: &BTreeMap<u64, Record>, entity: u64, attr: &str) -> Vec<u64> {
    match records.get(&entity).and_then(|r| r.get(attr)) {
        Some(Json::Array(v)) => v.iter().filter_map(Json::as_u64).collect(),
        Some(v) => v.as_u64().into_iter().collect(),
        None => vec![],
    }
}

/// Distinct selected goals supported by a topic, including a selected topic
/// itself. Topic edges and KP key prerequisites both carry support; repeated
/// selection memberships and multiple graph paths never increase the count.
fn selected_support(s: &EntitySnapshot, selected: &BTreeSet<u64>) -> Result<BTreeMap<u64, usize>> {
    let mut prerequisites = BTreeMap::<u64, BTreeSet<u64>>::new();
    for topic in s.entities.with_attribute("topic/id") {
        for next in s.refs(topic, "topic/next")? {
            prerequisites.entry(next).or_default().insert(topic);
        }
        for kp in s.refs(topic, "topic/knowledge-points")? {
            prerequisites
                .entry(topic)
                .or_default()
                .extend(s.refs(kp, "knowledge-point/key-prerequisites")?);
        }
    }
    let mut support = BTreeMap::new();
    for &goal in selected {
        let mut visited = BTreeSet::new();
        let mut pending = vec![goal];
        while let Some(topic) = pending.pop() {
            if !visited.insert(topic) {
                continue;
            }
            *support.entry(topic).or_insert(0) += 1;
            pending.extend(prerequisites.get(&topic).into_iter().flatten());
        }
    }
    Ok(support)
}

fn review_dates(s: &EntitySnapshot, learner: u64) -> Result<BTreeMap<u64, i64>> {
    let mut dates = BTreeMap::<u64, i64>::new();
    for progress in s.refs(learner, "learner/knowledge-profile")? {
        let row = s.entity(progress)?;
        if row.get("progress/learned") != Some(&json!(true)) {
            continue;
        }
        let (Some(memory), Some(interval), Some(anchor), Some(policy)) = (
            row.get("progress/memory").and_then(Json::as_f64),
            row.get("progress/interval-days").and_then(Json::as_f64),
            row.get("progress/memory-at"),
            s.optional_ref(progress, "progress/policy")?,
        ) else {
            continue;
        };
        let Some(threshold) = s
            .entity(policy)?
            .get("policy/review-threshold")
            .and_then(Json::as_f64)
        else {
            continue;
        };
        // Match the review-due exponential decay; memory already below the
        // threshold is due at its observation, never before that observation.
        let anchor = course_academy_engine::schema::parse_instant(anchor)?.timestamp_millis();
        review_due(memory, anchor, interval, threshold, anchor)?;
        let days = if memory <= threshold {
            0.0
        } else {
            interval * (memory / threshold).log2()
        };
        let due = anchor.saturating_add((days * 86_400_000.0).round() as i64);
        let topic = s.reference(progress, "progress/topic")?;
        dates
            .entry(topic)
            .and_modify(|old| *old = (*old).min(due))
            .or_insert(due);
    }
    Ok(dates)
}

pub(super) fn annotate(
    db: &DatabaseValue,
    learner: u64,
    now: i64,
    topics: &mut Json,
) -> Result<()> {
    if topics.as_array().ok_or("topics array missing")?.is_empty() {
        return Ok(());
    }
    let mut records = BTreeMap::new();
    // Bounded attribute reads for curriculum support; never scan all questions.
    for name in [
        "db/ident",
        "topic/id",
        "topic/next",
        "topic/knowledge-points",
        "knowledge-point/key-prerequisites",
        "knowledge-point/canonical-example",
        "policy/id",
        "policy/review-threshold",
    ] {
        let (ns, attr) = name.split_once('/').unwrap();
        if let Some(a) = db.schema().resolve_ident(&Keyword::new(ns, attr)) {
            for d in db.collect_datoms_with_prefix(&IndexPrefix::Aevt {
                attribute: a,
                entity: None,
                value: None,
            })? {
                insert(db, &mut records, &d)?;
            }
        }
    }
    let selected_kps: BTreeSet<u64> = topics
        .as_array()
        .unwrap()
        .iter()
        .flat_map(|t| t["knowledge_points"].as_array().unwrap())
        .map(|k| eid(&k["db/id"]))
        .collect::<Result<_>>()?;
    let mut pending = BTreeSet::from([learner]);
    pending.extend(selected_kps.iter().copied());
    let mut visited = BTreeSet::new();
    let mut selected_since = BTreeMap::<(u64, String), i64>::new();
    let mut terminal_at = BTreeMap::<u64, i64>::new();
    while let Some(e) = pending.pop_first() {
        if !visited.insert(e) {
            continue;
        }
        records.entry(e).or_default();
        for d in db.collect_datoms_with_prefix(&IndexPrefix::Eavt {
            entity: e,
            attribute: None,
            value: None,
        })? {
            let name = db.schema().attribute(d.attribute)?.ident.qualified_name();
            if e == learner && matches!(name.as_str(), "learner/queue" | "learner/targets") {
                if let Value::Ref(topic) = &d.value {
                    for stamp in db.values(d.tx, edb_core::DB_TX_INSTANT as u32)? {
                        if let Value::Instant(ms) = stamp {
                            selected_since
                                .entry((*topic, name.clone()))
                                .and_modify(|t| *t = (*t).min(ms))
                                .or_insert(ms);
                        }
                    }
                }
            }
            if name == "learner-task/status" {
                for stamp in db.values(d.tx, edb_core::DB_TX_INSTANT as u32)? {
                    if let Value::Instant(ms) = stamp {
                        terminal_at.insert(e, ms);
                    }
                }
            }
            insert(db, &mut records, &d)?;
        }
        for attr in [
            "learner/activity",
            "learner/knowledge-profile",
            "learner/assignments",
            "learner-task/activity",
            "learner-task/items",
            "activity/steps",
            "step/content",
            "task-item/content",
            "assigned-problem/content",
            "multistep/steps",
            "question/answer-fields",
            "answer-field/choices",
            "answer-field/correct",
        ] {
            pending.extend(refs(&records, e, attr));
        }
        if selected_kps.contains(&e) {
            pending.extend(refs(&records, e, "knowledge-point/questions"));
            pending.extend(refs(&records, e, "knowledge-point/canonical-example"));
        }
    }
    let s = EntitySnapshot::new(records, db.basis_t())
        .map_err(|e| format!("ranking projection: {e}"))?;
    let at = DateTime::<Utc>::from_timestamp_millis(now).ok_or("invalid ranking time")?;
    let priorities = learning::inventory_priorities(&s, learner, at)?;
    let unavailable = learning::unavailable_questions(&s, learner)?;
    let queued: BTreeSet<_> = s.refs(learner, "learner/queue")?.into_iter().collect();
    let targeted: BTreeSet<_> = s.refs(learner, "learner/targets")?.into_iter().collect();
    let selected = queued.union(&targeted).copied().collect();
    let support = selected_support(&s, &selected)?;
    let layers = learning::topic_layers(&s)?;
    let review_dates = review_dates(&s, learner)?;
    let mut learned_now = BTreeMap::new();
    for progress in s.refs(learner, "learner/knowledge-profile")? {
        let row = s.entity(progress)?;
        let learned = row
            .get("progress/learned")
            .and_then(Json::as_bool)
            .unwrap_or_else(|| {
                row.get("progress/repetitions")
                    .and_then(Json::as_f64)
                    .unwrap_or(0.0)
                    > 0.0
            });
        learned_now.insert(s.reference(progress, "progress/topic")?, learned);
    }
    let mut reviewed = BTreeSet::new();
    let mut completed_lessons = BTreeSet::new();
    let mut first_studied = BTreeMap::<u64, i64>::new();
    for task in s.refs(learner, "learner/activity")? {
        if s.entity(task)?
            .get("learner-task/status")
            .map(|v| s.ident(v))
            .transpose()?
            .as_deref()
            != Some("learner-task.status/completed")
        {
            continue;
        }
        let activity = s.reference(task, "learner-task/activity")?;
        let Some(topic) = s.optional_ref(activity, "activity/scope")? else {
            continue;
        };
        let kind = s
            .entity(activity)?
            .get("activity/type")
            .map(|v| s.ident(v))
            .transpose()?;
        if kind.as_deref() == Some("activity.type/review") {
            reviewed.insert(topic);
        }
        if kind.as_deref() == Some("activity.type/lesson") {
            completed_lessons.insert(topic);
            let finished = s
                .entity(task)?
                .get("learner-task/finished-at")
                .map(course_academy_engine::schema::parse_instant)
                .transpose()?
                .map(|at| at.timestamp_millis())
                .or_else(|| terminal_at.get(&task).copied());
            if let Some(finished) = finished {
                first_studied
                    .entry(topic)
                    .and_modify(|at| *at = (*at).min(finished))
                    .or_insert(finished);
            }
        }
    }
    let bands = ["easy", "moderate", "hard"];
    let inventory = |kps: &[u64]| -> Result<Json> {
        let qs = assessment_sampling::pool(&s, kps, &unavailable)?;
        let ordinary: BTreeSet<_> = kps
            .iter()
            .map(|kp| s.refs(*kp, "knowledge-point/questions"))
            .collect::<std::result::Result<Vec<_>, _>>()?
            .into_iter()
            .flatten()
            .collect();
        let total = ordinary
            .into_iter()
            .filter(|q| {
                !unavailable.contains(q)
                    && !s.is_example(*q)
                    && learning::validate_response_question(&s, *q).is_ok()
                    && learning::has_free_fields(&s, *q).ok() == Some(false)
            })
            .count();
        let mut counts = [0usize; 3];
        let mut supported = BTreeSet::new();
        for &kp in kps {
            for q in s
                .refs(kp, "knowledge-point/questions")?
                .into_iter()
                .chain(s.optional_ref(kp, "knowledge-point/canonical-example")?)
            {
                if let Some(band) = assessment_sampling::band(&s, q)? {
                    supported.insert(band);
                }
            }
        }
        for q in qs {
            counts[assessment_sampling::band(&s, q)?.unwrap()] += 1;
        }
        let rated = counts.iter().sum::<usize>();
        Ok(
            json!({"available": {"easy":counts[0],"moderate":counts[1],"hard":counts[2]},
            "available_total":total,"rated_total":rated,"unrated_total":total-rated,
            "supported_difficulties":supported.into_iter().map(|b|bands[b]).collect::<Vec<_>>()}),
        )
    };
    for t in topics.as_array_mut().unwrap() {
        let topic = eid(&t["db/id"])?;
        let priority = &priorities[&topic];
        // Selected-only discovery deliberately skips the broader studied-topic
        // eligibility pass. Recover history from the already captured learner
        // facts so its selected topics retain the same demand metadata.
        t["studied"] = json!(
            t["studied"] == true
                || learned_now.get(&topic) == Some(&true)
                || completed_lessons.contains(&topic)
        );
        if t["studied"] == true
            && !t["urgency_groups"]
                .as_array()
                .unwrap()
                .contains(&json!("studied"))
        {
            t["urgency_groups"]
                .as_array_mut()
                .unwrap()
                .push(json!("studied"));
            t["urgency_value"] = json!(t["urgency_value"].as_u64().unwrap_or(0).max(5));
        }
        let currently_learned = learned_now
            .get(&topic)
            .copied()
            .unwrap_or(t["studied"] == true);
        let selected_prerequisite = t["urgency_groups"]
            .as_array()
            .unwrap()
            .iter()
            .any(|g| g == "selected-prerequisite");
        let current_need = t["triggers"].as_array().unwrap().iter().any(|tr| {
            !matches!(
                tr["reason"].as_str(),
                Some("learner/queue" | "learner/targets")
            )
        });
        let relevance = if queued.contains(&topic) || targeted.contains(&topic) {
            1u8
        } else if selected_prerequisite {
            2
        } else if current_need {
            3
        } else {
            4
        };
        t["relevance_tier"] = json!(relevance);
        t["topic_layer"] = json!(layers[&topic]);
        t["selected_support_count"] = json!(support.get(&topic).copied().unwrap_or(0));
        t["completed_local_lesson"] = json!(completed_lessons.contains(&topic));
        t["review_due_at"] = json!(
            review_dates
                .get(&topic)
                .and_then(|ms| DateTime::<Utc>::from_timestamp_millis(*ms))
                .map(|at| at.to_rfc3339())
        );
        t["reviewed"] = json!(reviewed.contains(&topic));
        t["first_studied_at"] = json!(
            first_studied
                .get(&topic)
                .and_then(|at| DateTime::<Utc>::from_timestamp_millis(*at))
                .map(|at| at.to_rfc3339())
        );
        let mut upcoming = vec![];
        for trigger in t["triggers"].as_array().unwrap() {
            let kind = trigger["activity_type"].as_str().unwrap();
            let reason = trigger["reason"].as_str().unwrap();
            let tier = if let Some(task) = trigger["task"].as_u64() {
                let state = s
                    .entity(task)?
                    .get("learner-task/status")
                    .map(|v| s.ident(v))
                    .transpose()?;
                match state.as_deref() {
                    Some("learner-task.status/started" | "learner-task.status/paused") => 0,
                    Some("learner-task.status/unlocked") => 1,
                    _ => 3,
                }
            } else if reason == "scheduler-selected" {
                1
            } else if reason == "review-due" {
                2
            } else {
                continue;
            };
            upcoming.push((
                tier,
                match kind {
                    "lesson" => 0,
                    "review" => 1,
                    _ => 2,
                },
                kind.to_owned(),
            ));
        }
        upcoming.sort();
        t["next_activity"] = json!(
            upcoming
                .first()
                .map(|(_, _, kind)| kind.as_str())
                .unwrap_or(if currently_learned {
                    if reviewed.contains(&topic) {
                        "assessment"
                    } else {
                        "review"
                    }
                } else {
                    "lesson"
                })
        );
        let mut demands = BTreeMap::<String, u8>::new();
        let mut demand = |kind: &str, tier: u8| {
            demands
                .entry(kind.to_owned())
                .and_modify(|old| *old = (*old).min(tier))
                .or_insert(tier);
        };
        let next_activity = t["next_activity"].as_str().unwrap();
        // Historical study/review alone does not establish an upcoming
        // assessment. Actual assessment triggers below supply their own tier.
        demand(
            next_activity,
            if next_activity == "assessment" {
                4
            } else {
                relevance
            },
        );
        if queued.contains(&topic)
            || (targeted.contains(&topic) && !completed_lessons.contains(&topic))
            || (selected_prerequisite && !currently_learned)
        {
            demand("lesson", relevance);
        }
        for trigger in t["triggers"].as_array().unwrap() {
            let reason = trigger["reason"].as_str().unwrap();
            if matches!(reason, "learner/queue" | "learner/targets") {
                continue;
            }
            let mut immediate = reason == "scheduler-selected";
            if let Some(task) = trigger["task"].as_u64() {
                let row = s.entity(task)?;
                let status = row
                    .get("learner-task/status")
                    .map(|v| s.ident(v))
                    .transpose()?;
                immediate |= matches!(
                    status.as_deref(),
                    Some("learner-task.status/started" | "learner-task.status/paused")
                ) || row.contains_key("learner-task/remediation-for")
                    || row
                        .get("learner-task/priority")
                        .and_then(Json::as_f64)
                        .is_some_and(|n| n >= 12000.0);
            }
            demand(
                trigger["activity_type"].as_str().unwrap(),
                if immediate { 0 } else { relevance.min(3) },
            );
        }
        t["activity_demands"] = json!(demands.into_iter().map(|(activity_type, relevance_tier)|
            json!({"activity_type":activity_type, "relevance_tier":relevance_tier})).collect::<Vec<_>>());
        let needed = priority.ongoing
            || t["activity_demands"]
                .as_array()
                .unwrap()
                .iter()
                .any(|d| d["relevance_tier"] == 0)
            || t["triggers"].as_array().unwrap().iter().any(|tr| {
                matches!(
                    tr["reason"].as_str(),
                    Some("assigned" | "scheduler-selected")
                )
            });
        let state = if needed {
            "needed-now"
        } else if queued.contains(&topic) {
            "queued"
        } else if targeted.contains(&topic) || priority.target_count > 0 {
            "target-related"
        } else {
            "unlocked"
        };
        let mut score = priority.priority;
        for task in s.refs(learner, "learner/activity")? {
            let status = s
                .entity(task)?
                .get("learner-task/status")
                .map(|v| s.ident(v))
                .transpose()?;
            if !matches!(
                status.as_deref(),
                Some(
                    "learner-task.status/locked"
                        | "learner-task.status/unlocked"
                        | "learner-task.status/started"
                        | "learner-task.status/paused"
                )
            ) {
                continue;
            }
            let activity = s.reference(task, "learner-task/activity")?;
            if s.optional_ref(activity, "activity/scope")? == Some(topic)
                || t["triggers"]
                    .as_array()
                    .unwrap()
                    .iter()
                    .any(|tr| tr["task"].as_u64() == Some(task))
            {
                if let Some(stored) = s
                    .entity(task)?
                    .get("learner-task/priority")
                    .and_then(Json::as_f64)
                {
                    score = score.max(stored);
                }
            }
        }
        t["activity_state"] = json!(state);
        t["engine_priority"] = json!(score);
        t["assignment_due"] = json!(priority.due.map(|d| d.to_rfc3339()));
        let mut waiting = selected_since
            .get(&(
                topic,
                if state == "queued" {
                    "learner/queue"
                } else {
                    "learner/targets"
                }
                .into(),
            ))
            .copied();
        if needed {
            waiting = None;
            for trigger in t["triggers"].as_array().unwrap() {
                if let Some(task) = trigger["task"].as_u64() {
                    if let Some(at) = s.entity(task)?.get("learner-task/offered-at") {
                        let ms =
                            course_academy_engine::schema::parse_instant(at)?.timestamp_millis();
                        waiting = Some(waiting.map_or(ms, |old| old.min(ms)));
                    }
                }
            }
        }
        t["waiting_since"] = json!(
            waiting
                .and_then(DateTime::<Utc>::from_timestamp_millis)
                .map(|d| d.to_rfc3339())
        );
        let kps: Vec<_> = t["knowledge_points"]
            .as_array()
            .unwrap()
            .iter()
            .map(|kp| eid(&kp["db/id"]))
            .collect::<Result<_>>()?;
        t["topic_inventory"] = inventory(&kps)?;
        for kp in t["knowledge_points"].as_array_mut().unwrap() {
            kp["inventory"] = inventory(&[eid(&kp["db/id"])?])?;
        }
    }
    Ok(())
}
