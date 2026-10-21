//! Read-only forecasting inputs. No scheduler preparation or transaction plans.
use super::*;

// Only relationships, prices and learner evidence; never export question prose.
const ATTRIBUTES: &[&str] = &[
    "topic/id", "topic/title", "topic/next", "topic/knowledge-points",
    "knowledge-point/key-prerequisites", "course/id", "course/code", "course/title",
    "course/units", "unit/modules", "module/topics", "learner/id",
    "learner/targets", "learner/queue", "learner/assignments", "learner/activity",
    "learner/knowledge-profile", "learner/daily-xp-goal", "activity/id", "activity/type",
    "activity/scope", "activity/course", "activity/due", "activity/steps",
    "activity/expected-seconds", "step/content", "multistep/steps",
    "assigned-problem/content", "assigned-problem/topic-coverage", "progress/topic",
    "progress/repetitions", "progress/learned", "learner-task/activity",
    "learner-task/status", "learner-task/xp-base", "learner-task/xp-earned",
    "learner-task/finished-at", "learner-task/elapsed-seconds",
];

pub(super) struct Capture {
    data: Json,
    timing: EntitySnapshot,
    learner: u64,
}

fn attr(db: &DatabaseValue, name: &str) -> Option<u32> {
    let (ns, n) = name.split_once('/')?;
    db.schema().resolve_ident(&Keyword::new(ns, n))
}

// Uncached lessons use exactly the existing engine estimator. Load only their
// content closure, rather than capturing the entire question bank for a price.
fn load_estimator_content(db: &DatabaseValue, entities: &mut BTreeMap<u64, Record>, activity: u64) -> Result<()> {
    let mut pending = BTreeSet::from([activity]);
    if let Some(a) = attr(db, "policy/id") {
        pending.extend(db.collect_datoms_with_prefix(&IndexPrefix::Aevt { attribute:a, entity:None, value:None })?.iter().map(|d|d.entity));
    }
    let mut loaded = BTreeSet::new();
    while let Some(e) = pending.pop_first() {
        if !loaded.insert(e) { continue; }
        let r = page_reader::record(db,e)?;
        for edge in ["activity/steps", "activity/first-step", "step/content", "step/next",
            "knowledge-point/questions", "knowledge-point/canonical-example", "question/answer-fields",
            "policy/question-selection-weights"] {
            pending.extend(page_reader::references(&r,edge));
        }
        for v in r.values().flat_map(|v| match v { Json::Array(v)=>v.iter().collect::<Vec<_>>(),v=>vec![v] }) {
            if let Some((id,ident))=v.as_u64().and_then(|id|db.ident(id).map(|ident|(id,ident))) {
                entities.entry(id).or_default().insert("db/ident".into(),kw(&ident.qualified_name()));
            }
        }
        entities.entry(e).or_default().extend(r);
    }
    Ok(())
}

pub(super) fn capture(db: &DatabaseValue, learner_id: &str) -> Result<Capture> {
    let (timing,learner)=page_reader::capture_stats(db,learner_id)?;
    let mut records=BTreeMap::<u64,Record>::new();
    let mut histories=BTreeMap::<u64,Vec<Json>>::new();
    let mut entities=BTreeMap::<u64,Record>::new();
    let mut instants=BTreeMap::new();
    if let Some(a)=attr(db,"db/txInstant") {
        for d in db.collect_datoms_with_prefix(&IndexPrefix::Aevt {attribute:a,entity:None,value:None})? {
            if let Value::Instant(at)=d.value { instants.insert(edb_core::tx_to_t(d.entity)?,at); }
        }
    }
    // Keep this learner's current and past owned tasks/progress. Other learners'
    // private evidence is not needed for the shared graph projection.
    let mut owned=BTreeSet::from([learner]);
    for name in ["learner/activity","learner/knowledge-profile"] {
        if let Some(a)=attr(db,name) {
            for d in db.clone().history().collect_datoms_with_prefix(&IndexPrefix::Eavt {entity:learner,attribute:Some(a),value:None})? {
                if let Value::Ref(id)=d.value {owned.insert(id);}
            }
        }
    }
    for &name in ATTRIBUTES {
        let Some(a)=attr(db,name) else {continue};
        let private=name.starts_with("learner/") || name.starts_with("learner-task/") || name.starts_with("progress/");
        for d in db.collect_datoms_with_prefix(&IndexPrefix::Aevt {attribute:a,entity:None,value:None})? {
            if private && !owned.contains(&d.entity) {continue;}
            let v=value(&d.value)?;
            let values=records.entry(d.entity).or_default().entry(name).or_insert(json!([])).as_array_mut().unwrap();
            if !values.contains(&v) {values.push(v.clone());}
            let r=entities.entry(d.entity).or_default();
            if db.schema().attribute(a)?.cardinality==Cardinality::Many {
                let values=r.entry(name).or_insert(json!([])).as_array_mut().unwrap();
                if !values.contains(&v) {values.push(v);}
            } else {r.insert(name.into(),v);}
        }
        for d in db.clone().history().collect_datoms_with_prefix(&IndexPrefix::Aevt {attribute:a,entity:None,value:None})? {
            if private && !owned.contains(&d.entity) {continue;}
            let t=edb_core::tx_to_t(d.tx)?;
            histories.entry(t).or_default().push(json!([d.entity,name,value(&d.value)?,d.added]));
        }
    }
    let mut enums=BTreeMap::new();
    for name in ["activity.type/lesson","activity.type/review","activity.type/assessment",
        "activity.type/assignment","activity.type/diagnostic","learner-task.status/locked",
        "learner-task.status/unlocked","learner-task.status/started","learner-task.status/paused",
        "learner-task.status/completed","learner-task.status/failed"] {
        let (ns,n)=name.split_once('/').unwrap();
        if let Some(e)=db.entid(&Keyword::new(ns,n)) {
            enums.insert(e,name);
            entities.entry(e).or_default().insert("db/ident".into(),kw(name));
        }
    }
    let known=learning::known_preparation_topics(&EntitySnapshot::new(entities.clone(),db.basis_t())?,learner)?;
    let lessons:Vec<_>=entities.iter().filter_map(|(&e,r)| {
        r.get("activity/type").and_then(Json::as_u64).and_then(|id|enums.get(&id))
            .is_some_and(|kind|*kind=="activity.type/lesson").then_some(e)
    }).collect();
    let mut prices=BTreeMap::new();
    for e in lessons {
        if !entities[&e].contains_key("activity/expected-seconds") {load_estimator_content(db,&mut entities,e)?;}
        let s=EntitySnapshot::new(entities.clone(),db.basis_t())?;
        prices.insert(e,match base_xp::activity_base(&s,e) {
            Ok(base)=>json!({"baseXp":base}),Err(error)=>json!({"baseXp":null,"reason":error}),
        });
    }
    let history=histories.into_iter().map(|(t,changes)| {
        Ok(json!({"t":t,"at":instants.get(&t).ok_or("Missing forecast history transaction date")?,"changes":changes}))
    }).collect::<Result<Vec<_>>>()?;
    Ok(Capture {data:json!({"basis":db.basis_t(),"learnerId":learner,"records":records,
        "enums":enums,"history":history,"lessonBases":prices,"knownTopics":known}),timing,learner})
}

pub(super) fn read(capture: &Capture, body: &Json, now: DateTime<Utc>) -> Result<Json> {
    let stats=study_stats::summary(&capture.timing,capture.learner,body,now)?;
    let mut data=capture.data.clone();
    data["capturedAt"]=json!(now.to_rfc3339());
    data["timing"]=stats;
    // Preserve the engine's dating semantics: an undated import has no recent
    // completion date. Original recovered dates remain authoritative.
    let mut dates=BTreeMap::new();
    let mut first_observed=None;
    for event in &capture.timing.status_history {
        if event.attribute!="learner-task/status" {continue;}
        let at=schema::parse_instant(&event.at)?;
        if at>now {continue;}
        first_observed=Some(first_observed.map_or(at,|old:DateTime<Utc>|old.min(at)));
        if matches!(capture.timing.ident(&event.value)?.as_str(),"learner-task.status/completed"|"learner-task.status/failed") {
            let started=capture.timing.status_history.iter().any(|h|h.entity==event.entity && h.attribute=="learner-task/status" && capture.timing.ident(&h.value).ok().as_deref()==Some("learner-task.status/started"));
            if started || capture.timing.entities[&event.entity].contains_key("learner-task/finished-at") {
                let finished=timing::task_finished_at(&capture.timing,event.entity,at)?;
                dates.insert(event.entity,finished.timestamp_millis());
                first_observed=Some(first_observed.unwrap().min(finished));
            }
        }
    }
    data["finishedAt"]=json!(dates);
    data["firstObservedAt"]=json!(first_observed.map(|at|at.timestamp_millis()));
    Ok(data)
}
