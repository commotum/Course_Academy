//! Current-schema activity ownership and Rust -> native EDB transaction checks.
use super::transact;
use course_academy_engine::{
    runtime::{ActivityRules, CompletionOptions, complete_item, expire_task, transition_item},
    schema::{EntitySnapshot, load_runtime, parse_instant},
};
use edb_core::{Cardinality, Database, IndexOrder, Keyword, TransactionRequest, Value, View};
use std::{collections::BTreeMap, error::Error};

fn attr(db: &Database, ns: &str, name: &str) -> u32 {
    db.entid(&Keyword::new(ns, name)).unwrap() as u32
}
fn find(db: &Database, ns: &str, name: &str, value: Value) -> u64 {
    let a = attr(db, ns, name);
    db.datoms(View::Current, IndexOrder::Eavt)
        .iter()
        .find(|d| d.attribute == a && d.value == value && d.added)
        .unwrap()
        .entity
}
fn json(value: &Value) -> String {
    match value {
        Value::String(v) => format!("{v:?}"),
        Value::Keyword(v) => format!("{:?}", v.qualified_name()),
        Value::Uuid(v) => format!("\"{v:032x}\""),
        Value::Ref(v) => v.to_string(),
        Value::Long(v) | Value::Instant(v) => v.to_string(),
        Value::Double(v) => format!("{v:?}"),
        Value::Bool(v) => v.to_string(),
        other => panic!("unexpected fixture value {other:?}"),
    }
}
// Capture actual native values and cardinalities; no assumed EID allocation and
// the native fixture must expose unsupported attributes directly.
fn capture(db: &Database) -> String {
    let mut entities: BTreeMap<u64, BTreeMap<String, (bool, Vec<String>)>> = BTreeMap::new();
    for d in db.datoms(View::Current, IndexOrder::Eavt) {
        if !d.added {
            continue;
        }
        let attribute = db.schema().attribute(d.attribute).unwrap();
        let name = attribute.ident.qualified_name();
        if (name.starts_with("db/") || name.starts_with("db.")) && name != "db/ident" {
            continue;
        }
        let entry = entities
            .entry(d.entity)
            .or_default()
            .entry(name)
            .or_insert((attribute.cardinality == Cardinality::Many, Vec::new()));
        entry.1.push(json(&d.value));
    }
    let maps: Vec<String> = entities
        .iter()
        .map(|(eid, record)| {
            let fields: Vec<String> = record
                .iter()
                .map(|(name, (many, values))| {
                    format!(
                        "{name:?}:{}",
                        if *many {
                            format!("[{}]", values.join(","))
                        } else {
                            values[0].clone()
                        }
                    )
                })
                .collect();
            format!("\"{eid}\":{{{}}}", fields.join(","))
        })
        .collect();
    let tx_instant = attr(db, "db", "txInstant");
    let mut history = Vec::new();
    for d in db.datoms(View::History, IndexOrder::Eavt) {
        let name = db
            .schema()
            .attribute(d.attribute)
            .unwrap()
            .ident
            .qualified_name();
        if !d.added || !matches!(name.as_str(), "learner-task/status" | "task-item/status") {
            continue;
        }
        let at = db.values(d.tx, tx_instant);
        let [Value::Instant(at)] = at.as_slice() else {
            panic!("status transaction {} has no timestamp", d.tx);
        };
        let Value::Ref(value) = d.value else {
            panic!("status history must contain enum references");
        };
        let t = edb_core::tx_to_t(d.tx).unwrap();
        history.push((
            t,
            d.entity,
            name.clone(),
            format!(
                "{{\"entity\":{},\"attribute\":{name:?},\"value\":{value},\"t\":{t},\"at\":{at}}}",
                d.entity
            ),
        ));
    }
    history.sort_by(|a, b| (&a.0, &a.1, &a.2).cmp(&(&b.0, &b.1, &b.2)));
    format!(
        "{{\"basis_t\":{},\"entities\":{{{}}},\"status_history\":[{}]}}",
        db.basis_t(),
        maps.join(","),
        history
            .into_iter()
            .map(|(_, _, _, value)| value)
            .collect::<Vec<_>>()
            .join(",")
    )
}

pub fn check(base: &Database) -> Result<(), Box<dyn Error>> {
    let fixture = r#"[
     {:db/id "q" :question/id #uuid "00000000-0000-4000-8000-000000000020"
      :question/problem "Select 2."
      :question/answer-fields ["field"] :db/ensure :question/validate}
     {:db/id "field" :answer-field/id #uuid "00000000-0000-4000-8000-000000000021"
      :answer-field/key "selection" :answer-field/type :answer-field.type/radio
      :answer-field/choices ["right" "wrong"]
      :answer-field/correct "right" :db/ensure :answer-field/validate}
     {:db/id "right" :answer/id #uuid "00000000-0000-4000-8000-000000000022"
      :answer/type :answer.type/math :answer/value "2" :db/ensure :answer/validate}
     {:db/id "wrong" :answer/id #uuid "00000000-0000-4000-8000-000000000023"
      :answer/type :answer.type/math :answer/value "3" :db/ensure :answer/validate}
     {:db/id "example" :question/id #uuid "00000000-0000-4000-8000-000000000030"
      :question/problem "Recognize 2."
      :question/worked-solution "Two is written 2." :db/ensure :question/validate}
     {:db/id "kp" :knowledge-point/id #uuid "00000000-0000-4000-8000-000000000031"
      :knowledge-point/title "Recognize two" :knowledge-point/canonical-example "example"
      :knowledge-point/questions ["q"] :db/ensure :knowledge-point/validate}
     {:db/id [:topic/id #uuid "b3d88ca6-d319-409b-bdb1-000000000001"]
      :topic/knowledge-points ["kp"] :db/ensure :topic/validate}
     {:db/id "review" :assessment/id #uuid "00000000-0000-4000-8000-000000000024"
      :assessment/title "Native one-question assessment"
      :assessment/questions ["q"] :db/ensure :assessment/validate}
     {:db/id "task" :learner-task/id #uuid "00000000-0000-4000-8000-000000000025"
      :learner-task/activity "review" :learner-task/status :learner-task.status/started
      :learner-task/items ["item"] :db/ensure :learner-task/validate}
     {:db/id "item" :task-item/id #uuid "00000000-0000-4000-8000-000000000026"
      :task-item/content "q" :task-item/status :task-item.status/started :db/ensure :task-item/validate}
     {:db/id [:learner/id "schema-check-learner"] :learner/activity ["task"] :db/ensure :learner/validate}
    ]"#;
    let started_at = parse_instant(&"2026-09-28T00:00:00Z".into())?.timestamp_millis();
    let db = transact(base, fixture, started_at)?.db_after;
    let learner = find(
        &db,
        "learner",
        "id",
        Value::String("schema-check-learner".into()),
    );
    let policy = find(
        &db,
        "policy",
        "id",
        Value::Uuid(0xb3d88ca6d319409bbdb1000000000003),
    );
    let item = find(
        &db,
        "task-item",
        "id",
        Value::Uuid(0x00000000000040008000000000000026),
    );
    let task = find(
        &db,
        "learner-task",
        "id",
        Value::Uuid(0x00000000000040008000000000000025),
    );
    let answer = find(
        &db,
        "answer",
        "id",
        Value::Uuid(0x00000000000040008000000000000022),
    );
    // The database history, not a supplied duration or domain timestamp, is
    // the timing source: work one second, pause three, then work one more.
    let db = transact(
        &db,
        &format!(
            "[[:db/add {item} :task-item/status :task-item.status/paused] \
          [:db/add {task} :learner-task/status :learner-task.status/paused]]"
        ),
        started_at + 1000,
    )?
    .db_after;
    let db = transact(
        &db,
        &format!(
            "[[:db/add {item} :task-item/status :task-item.status/started] \
          [:db/add {task} :learner-task/status :learner-task.status/started]]"
        ),
        started_at + 4000,
    )?
    .db_after;
    let snapshot = EntitySnapshot::from_json_str(&capture(&db))?;
    let loaded = load_runtime(snapshot, learner, policy)?;
    let advanced = find(
        &db,
        "topic",
        "id",
        Value::Uuid(0xb3d88ca6d319409bbdb1000000000001),
    );
    let prerequisite = find(
        &db,
        "topic",
        "id",
        Value::Uuid(0xb3d88ca6d319409bbdb1000000000002),
    );
    assert_eq!(
        loaded.snapshot.refs(prerequisite, "topic/next")?,
        vec![advanced]
    );
    assert_eq!(
        loaded.snapshot.owners(advanced, "topic/next")?,
        vec![prerequisite]
    );
    assert_eq!(
        loaded.engine.neighborhoods[&loaded.topic_eid_to_id[&advanced]],
        vec![loaded.topic_eid_to_id[&prerequisite].clone()]
    );
    assert!(
        !loaded
            .engine
            .neighborhoods
            .contains_key(&loaded.topic_eid_to_id[&prerequisite])
    );
    let incoming = db.datoms_with_prefix(&edb_core::IndexPrefix::Vaet {
        value: Value::Ref(advanced),
        attribute: Some(attr(&db, "topic", "next")),
        entity: None,
    })?;
    assert_eq!(incoming.len(), 1);
    assert_eq!(incoming[0].entity, prerequisite);
    let at = started_at + 5000;
    let mut options = CompletionOptions::new(parse_instant(&at.into())?);
    options.result = Some(true);
    options.response_refs = vec![answer.into()];
    let completion = complete_item(&loaded, item, options)?;
    assert!(completion.delivery.complete);
    let plan = completion.transaction;
    let key = &plan.request_key;
    let basis = plan.compare_basis_t;
    let edn = &plan.edn;
    let request = TransactionRequest::from_edn(key, edn)?.comparing_basis(basis);
    assert_eq!(request.compare_basis_t, Some(db.basis_t()));
    assert!(request.request_key.starts_with("complete-item-"));
    // with_forms checks transaction/CAS semantics; it is not the durable writer.
    // The native transactor-selected instant must match the plan's event time.
    assert_eq!(
        transact(&db, edn, at + 10_000).unwrap_err().code,
        "transaction/tx-instant-mismatch"
    );
    let after = transact(&db, edn, at)?.db_after;
    assert_eq!(
        after.values(item, attr(&after, "task-item", "elapsed-seconds")),
        vec![&Value::Double(2.0)]
    );
    assert_eq!(
        after.values(item, attr(&after, "task-item", "responses")),
        vec![&Value::Ref(answer)]
    );
    assert_eq!(
        after.values(task, attr(&after, "learner-task", "elapsed-seconds")),
        vec![&Value::Double(2.0)]
    );
    assert_eq!(
        after.values(item, attr(&after, "task-item", "status")),
        vec![&Value::Ref(
            after
                .entid(&Keyword::new("task-item.status", "correct"))
                .unwrap()
        )]
    );
    assert_eq!(
        transact(&after, edn, at).unwrap_err().code,
        "transaction/cas-failed",
        "the item status CAS must reject a second fresh application"
    );
    let state = find(
        &after,
        "progress",
        "id",
        Value::String("schema-check-state".into()),
    );
    assert_eq!(
        after.values(state, attr(&after, "progress", "practice-mass")),
        vec![&Value::Double(4.0)]
    );
    assert_eq!(
        after.values(state, attr(&after, "progress", "assessment-mass")),
        vec![&Value::Double(1.0)]
    );
    assert_eq!(
        after
            .values(state, attr(&after, "progress", "last-direct-at"))
            .len(),
        1
    );
    let performance = match after.values(learner, attr(&after, "learner", "performance"))[0] {
        Value::Ref(eid) => *eid,
        _ => panic!("performance ref required"),
    };
    assert_eq!(
        after.values(performance, attr(&after, "performance", "assessment-mass")),
        vec![&Value::Double(1.0)]
    );
    assert_eq!(
        after.values(performance, attr(&after, "performance", "practice-mass")),
        vec![&Value::Double(4.0)]
    );
    assert_eq!(
        after.values(task, attr(&after, "learner-task", "status")),
        vec![&Value::Ref(
            after
                .entid(&Keyword::new("learner-task.status", "completed"))
                .unwrap()
        )]
    );
    let completion_history = capture(&after);
    assert!(completion_history.contains(&format!("\"at\":{at}")));
    let final_snapshot = EntitySnapshot::from_json_str(&completion_history)?;
    let final_loaded = load_runtime(final_snapshot, learner, policy)?;
    let mut repeated = CompletionOptions::new(parse_instant(&at.into())?);
    repeated.result = Some(true);
    assert!(complete_item(&final_loaded, item, repeated).is_err());

    // Pausing the activity must not extend an assessment's wall-clock limit.
    // No answer/result is invented for the unfinished question on expiry.
    let question = find(
        &after,
        "question",
        "id",
        Value::Uuid(0x00000000000040008000000000000020),
    );
    let timer_start = at + 1000;
    let timer_fixture = format!(
        r#"[
      {{:db/id "timed-assessment" :assessment/id #uuid "00000000-0000-4000-8000-000000000040"
        :assessment/title "Native expiry check" :assessment/questions [{question}]
        :assessment/time-limit-seconds 3.0 :db/ensure :assessment/validate}}
      {{:db/id "timed-task" :learner-task/id #uuid "00000000-0000-4000-8000-000000000041"
        :learner-task/activity "timed-assessment" :learner-task/status :learner-task.status/started
        :learner-task/items ["timed-item"] :db/ensure :learner-task/validate}}
      {{:db/id "timed-item" :task-item/id #uuid "00000000-0000-4000-8000-000000000042"
        :task-item/content {question} :task-item/status :task-item.status/started :db/ensure :task-item/validate}}
      [:db/add {learner} :learner/activity "timed-task"]
    ]"#
    );
    let timer_db = transact(&after, &timer_fixture, timer_start)?.db_after;
    let timed_task = find(
        &timer_db,
        "learner-task",
        "id",
        Value::Uuid(0x00000000000040008000000000000041),
    );
    let timed_item = find(
        &timer_db,
        "task-item",
        "id",
        Value::Uuid(0x00000000000040008000000000000042),
    );
    let timer_loaded = load_runtime(
        EntitySnapshot::from_json_str(&capture(&timer_db))?,
        learner,
        policy,
    )?;
    let pause_at = timer_start + 1000;
    let pause = transition_item(
        &timer_loaded,
        timed_item,
        "paused",
        parse_instant(&pause_at.into())?,
    )?;
    let timer_db = transact(&timer_db, &pause.edn, pause_at)?.db_after;
    assert_eq!(
        timer_db.values(timed_item, attr(&timer_db, "task-item", "elapsed-seconds")),
        vec![&Value::Double(1.0)]
    );
    assert_eq!(
        transact(&timer_db, &pause.edn, pause_at).unwrap_err().code,
        "transaction/cas-failed"
    );
    let timer_db = transact(
        &timer_db,
        &format!("[[:db/add {timed_task} :learner-task/status :learner-task.status/paused]]"),
        pause_at,
    )?
    .db_after;
    let timed_loaded = load_runtime(
        EntitySnapshot::from_json_str(&capture(&timer_db))?,
        learner,
        policy,
    )?;
    assert!(
        expire_task(
            &timed_loaded,
            timed_task,
            parse_instant(&(timer_start + 2000).into())?,
            None,
            ActivityRules::default()
        )
        .is_err()
    );
    let expiry_at = timer_start + 3000;
    let expiry = expire_task(
        &timed_loaded,
        timed_task,
        parse_instant(&expiry_at.into())?,
        None,
        ActivityRules::default(),
    )?;
    let expired = transact(&timer_db, &expiry.transaction.edn, expiry_at)?.db_after;
    assert_eq!(
        expired.values(
            timed_task,
            attr(&expired, "learner-task", "elapsed-seconds")
        ),
        vec![&Value::Double(1.0)]
    );
    assert_eq!(
        expired.values(timed_task, attr(&expired, "learner-task", "status")),
        vec![&Value::Ref(
            expired
                .entid(&Keyword::new("learner-task.status", "completed"))
                .unwrap()
        )]
    );
    assert_eq!(
        expired.values(timed_item, attr(&expired, "task-item", "status")),
        vec![&Value::Ref(
            expired
                .entid(&Keyword::new("task-item.status", "paused"))
                .unwrap()
        )]
    );
    assert!(
        expired
            .values(timed_item, attr(&expired, "task-item", "responses"))
            .is_empty()
    );
    assert_eq!(
        transact(&expired, &expiry.transaction.edn, expiry_at)
            .unwrap_err()
            .code,
        "transaction/cas-failed"
    );

    let deleted = transact(
        &after,
        &format!("[[:db.fn/retractEntity {task}]]"),
        at + 100,
    )?
    .db_after;
    assert!(
        deleted
            .values(item, attr(&deleted, "task-item", "id"))
            .is_empty()
    );
    assert_eq!(
        deleted.values(answer, attr(&deleted, "answer", "id")).len(),
        1
    );
    println!(
        "PASS actual EDB status history -> Rust automatic assessment completion -> native request EDN, pause/resume elapsed totals, exact basis field, status CAS, progress/global update, stable answer refs and component lifecycle."
    );
    Ok(())
}
