// Run from the repository root; requires the local EDB edb_core build.
use edb_core::{Database, Keyword, SemanticError, TxFunctions, TxReport, Value};
#[path = "../engine/edb/configuration.rs"]
mod configuration;
mod edb_configuration_checks;
#[path = "../engine/edb/progress.rs"]
mod progress;
fn transact(db: &Database, text: &str, at: i64) -> Result<TxReport, SemanticError> {
    let mut functions = TxFunctions::new();
    progress::register_progress_predicates(&mut functions);
    configuration::register_configuration_predicates(&mut functions);
    db.with_forms(
        &edb_core::edn_transaction::read_edn_transaction(text)?,
        &functions,
        at,
    )
}
use std::{error::Error, fs};
fn main() -> Result<(), Box<dyn Error>> {
    let root = std::env::current_dir()?;
    let mut db = Database::bootstrap()?;
    let mut clock = 1000i64;
    for dir in ["schema-v2/data", "schema-v2/content", "schema-v2/fire"] {
        let mut paths = fs::read_dir(root.join(dir))?
            .filter_map(Result::ok)
            .map(|e| e.path())
            .filter(|p| p.extension().is_some_and(|e| e == "edn"))
            .collect::<Vec<_>>();
        paths.sort();
        for path in paths {
            db = transact(&db, &fs::read_to_string(&path)?, clock)
                .map_err(|e| format!("{}: {e}", path.display()))?
                .db_after;
            clock += 1;
        }
    }
    let fixture = r#"[
 {:db/id "advanced" :topic/id #uuid "b3d88ca6-d319-409b-bdb1-000000000001" :topic/title "Illustrative advanced topic" :topic/encompasses ["edge"]}
 {:db/id "component" :topic/id #uuid "b3d88ca6-d319-409b-bdb1-000000000002" :topic/title "Illustrative component topic"}
 {:db/id "learner" :fire-learner/id "schema-check-learner"
  :fire-learner/assessment-accuracy 0.8 :fire-learner/practice-accuracy 0.9
  :fire-learner/assessment-mass 0.0 :fire-learner/practice-mass 4.0
  :learner/knowledge-profile ["state" "unlearned-state"]
  :db/ensure [:fire-learner/validate :fire-learner/ability-validate]}
 {:db/id "policy" :policy/id #uuid "b3d88ca6-d319-409b-bdb1-000000000003"
  :policy/name "Schema validation configuration" :policy/algorithm :policy.algorithm/fire-v1
  :policy/base-half-life-days 1.0 :policy/interval-growth 2.0 :policy/maximum-half-life-days 36500.0
  :policy/review-threshold 0.5 :policy/initial-retention 1.0 :policy/early-practice-discount-power 1.0
  :policy/initial-accuracy 0.8 :policy/accuracy-update-rate 0.2 :policy/speed-exponent 2.0
  :policy/minimum-speed 0.25 :policy/maximum-speed 4.0
  :policy/overdue-failure-slope 1.0 :policy/maximum-failure-multiplier 4.0
  :policy/gate-slow-implicit true :policy/retention-update-order :policy.retention-update/decay-before-add
  :policy/future-horizon-days 7.0 :db/ensure :policy/validate}
 {:db/id "edge" :encompassing/topic "component" :encompassing/weight 0.0
  :encompassing/rationale "Illustrative explicit zero coverage for schema validation." :db/ensure :encompassing/validate}
 {:db/id "advanced" :topic/difficulty 0.75 :topic/difficulty-method :difficulty.method/assessment-data
  :topic/assessment-correct 3 :topic/assessment-total 4 :topic/assessment-cohort "Illustrative schema fixture"
  :topic/assessment-through #inst "2026-09-26T00:00:00.000Z" :db/ensure :topic/difficulty-validate}
 {:db/id "event" :fire-event/id "schema-check-event" :fire-event/learner "learner" :fire-event/at #inst "2026-09-26T00:00:00.000Z"
  :fire-event/topic "advanced" :fire-event/kind "review" :fire-event/passed true :fire-event/assessment false :fire-event/quality 1.5
  :fire-event/learned false :fire-event/question-results-edn "[true true true true]" :fire-event/source "direct" :db/ensure :fire-event/validate}
 {:db/id "state" :progress/id "schema-check-state" :progress/topic "advanced"
  :progress/repetitions 1.5 :progress/memory 1.0 :progress/memory-at #inst "2026-09-26T00:00:00.000Z"
  :progress/interval-days 2.8284271247461903 :progress/assessment-accuracy 0.8 :progress/practice-accuracy 0.8
  :progress/assessment-mass 0.0 :progress/practice-mass 4.0
  :progress/learned true :progress/policy "policy" :db/ensure :progress/validate}
 {:db/id "unlearned-state" :progress/id "schema-check-unlearned" :progress/topic "component"
  :progress/repetitions 0.0 :progress/memory 0.0 :progress/memory-at #inst "2026-09-26T00:00:00.000Z"
  :progress/interval-days 1.0 :progress/assessment-accuracy 0.4 :progress/practice-accuracy 0.6
  :progress/assessment-mass 2.0 :progress/practice-mass 3.0
  :progress/learned false :progress/policy "policy" :db/ensure :progress/validate}
 ]"#;
    db = transact(&db, fixture, 2000)?.db_after;
    let idattr = db.entid(&Keyword::new("progress", "id")).unwrap() as u32;
    let state = db
        .datoms(edb_core::View::Current, edb_core::IndexOrder::Eavt)
        .iter()
        .find(|d| {
            d.attribute == idattr
                && d.value == Value::String("schema-check-state".into())
                && d.added
        })
        .unwrap()
        .entity;
    let find_string = |database: &Database, ns: &str, name: &str, value: &str| {
        let attr = database.entid(&Keyword::new(ns, name)).unwrap() as u32;
        database
            .datoms(edb_core::View::Current, edb_core::IndexOrder::Eavt)
            .iter()
            .find(|d| d.attribute == attr && d.value == Value::String(value.into()) && d.added)
            .unwrap()
            .entity
    };
    let learner = find_string(&db, "fire-learner", "id", "schema-check-learner");
    let topicattr = db.entid(&Keyword::new("progress", "topic")).unwrap() as u32;
    let topic = match db.values(state, topicattr).first().unwrap() {
        Value::Ref(id) => *id,
        other => panic!("Unexpected ref {other:?}"),
    };
    let event = find_string(&db, "fire-event", "id", "schema-check-event");
    let input_basis = db.basis_t();
    let receipt = r#"[ {:fire-application/id "schema-check-application" :fire-application/event EVENT_ID :fire-application/event-hash "schema-test-payload" :fire-application/policy [:policy/id #uuid "b3d88ca6-d319-409b-bdb1-000000000003"]
  :fire-application/basis-t BASIS_T :fire-application/input-state-edn "{}"
  :fire-application/applied-at #inst "2026-09-26T00:00:01.000Z"
  :fire-application/updates [{:fire-update/topic [:topic/id #uuid "b3d88ca6-d319-409b-bdb1-000000000001"]
    :fire-update/trace-edn "{:direct true :raw_delta 1.0 :before {:repetitions 0.5} :after {:repetitions 1.5}}" :db/ensure :fire-update/validate}]
  :db/ensure :fire-application/validate}
]"#.replace("BASIS_T", &input_basis.to_string()).replace("EVENT_ID", &event.to_string());
    db = transact(&db, &receipt, 2100)?.db_after;
    let application = find_string(&db, "fire-application", "id", "schema-check-application");
    let basis_attr = db
        .entid(&Keyword::new("fire-application", "basis-t"))
        .unwrap() as u32;
    assert_eq!(
        db.values(application, basis_attr),
        vec![&Value::Long(input_basis as i64)]
    );
    edb_configuration_checks::check(&db, topic, input_basis)?;
    let eventkeyattr = db.entid(&Keyword::new("fire-event", "key")).unwrap() as u32;
    assert_eq!(db.values(event, eventkeyattr).len(), 1);
    let state_count = db
        .datoms(edb_core::View::Current, edb_core::IndexOrder::Eavt)
        .iter()
        .filter(|d| d.attribute == idattr && d.added)
        .count();
    let update = format!(
        r#"[{{:db/id [:progress/id "schema-check-state"] :progress/memory 0.75 :db/ensure :progress/validate}}
  {{:db/id [:fire-event/key [{learner} "schema-check-event"]] :fire-event/quality 1.5 :db/ensure :fire-event/validate}}]"#
    );
    db = transact(&db, &update, 2500)?.db_after;
    assert_eq!(
        state_count,
        db.datoms(edb_core::View::Current, edb_core::IndexOrder::Eavt)
            .iter()
            .filter(|d| d.attribute == idattr && d.added)
            .count()
    );
    assert_eq!(
        event,
        find_string(&db, "fire-event", "id", "schema-check-event")
    );
    let second_learner = r#"[
  {:db/id "other" :fire-learner/id "schema-check-other" :db/ensure :fire-learner/validate}
  {:fire-event/id "schema-check-event" :fire-event/learner "other" :fire-event/at #inst "2026-09-26T00:00:00.000Z"
   :fire-event/topic [:topic/id #uuid "b3d88ca6-d319-409b-bdb1-000000000001"] :fire-event/kind "review"
   :fire-event/passed false :fire-event/assessment true :fire-event/quality 1.5 :fire-event/learned false
   :fire-event/question-results-edn "[false true]" :fire-event/source "direct" :db/ensure :fire-event/validate}]"#;
    db = transact(&db, second_learner, 2600)?.db_after;
    let duplicate_event =
        format!(r#"[{{:fire-event/id "schema-check-event" :fire-event/learner {learner}}}]"#);
    assert!(transact(&db, &duplicate_event, 3000).is_err());
    let wrong_type = format!(r#"[{{:db/id {event} :fire-event/passed "true"}}]"#);
    assert!(transact(&db, &wrong_type, 3000).is_err());
    let wrong_cardinality = format!(r#"[{{:db/id {state} :progress/repetitions [1.0 2.0]}}]"#);
    assert!(transact(&db, &wrong_cardinality, 3000).is_err());
    let missing = r#"[{:progress/id "incomplete" :db/ensure :progress/validate}]"#;
    assert_eq!(
        transact(&db, missing, 3000).unwrap_err().code,
        "transaction/entity-spec"
    );
    let duplicate = format!(
        r#"[
  {{:db/id "duplicate" :progress/id "duplicate" :progress/topic {topic}}}
  {{:db/id {learner} :learner/knowledge-profile "duplicate" :db/ensure :fire-learner/validate}}]"#
    );
    assert!(transact(&db, &duplicate, 3000).is_err());
    let shared = format!(
        r#"[{{:fire-learner/id "shared-owner" :learner/knowledge-profile {state} :db/ensure :fire-learner/validate}}]"#
    );
    assert!(transact(&db, &shared, 3000).is_err());
    let changed = format!(
        r#"[{{:db/id [:progress/id "schema-check-unlearned"] :progress/topic {topic} :db/ensure :progress/validate}}]"#
    );
    assert!(transact(&db, &changed, 3000).is_err());
    let detached = format!(
        r#"[[:db/retract {learner} :learner/knowledge-profile {state}]
  {{:db/id {state} :db/ensure :progress/validate}}]"#
    );
    assert!(transact(&db, &detached, 3000).is_err());
    let other = find_string(&db, "fire-learner", "id", "schema-check-other");
    let transfer = format!(
        r#"[[:db/retract {learner} :learner/knowledge-profile {state}]
  {{:db/id {learner} :db/ensure :fire-learner/validate}}
  {{:db/id {other} :learner/knowledge-profile {state} :db/ensure :fire-learner/validate}}
  {{:db/id {state} :db/ensure :progress/validate}}]"#
    );
    assert!(transact(&db, &transfer, 3000).is_ok());
    let profileattr = db
        .entid(&Keyword::new("learner", "knowledge-profile"))
        .unwrap() as u32;
    let owners = db.datoms_with_prefix(&edb_core::IndexPrefix::Vaet {
        value: Value::Ref(state),
        attribute: Some(profileattr),
        entity: None,
    })?;
    assert_eq!(owners.len(), 1);
    assert_eq!(owners[0].entity, learner);
    let removed = transact(&db, &format!("[[:db.fn/retractEntity {learner}]]"), 3100)?.db_after;
    assert!(removed.values(state, idattr).is_empty());
    let topicidattr = db.entid(&Keyword::new("topic", "id")).unwrap() as u32;
    assert!(!removed.values(topic, topicidattr).is_empty());
    println!("PASS all current content and FIRe schemas install; required-attribute specs accept topic-owned encompassing/difficulty/global ability/event/application/state fixtures, explicit zero coverage, optional rationale, quality 1.5 and unlearned ability.");
    println!("PASS progress updates preserve identity; reverse ownership resolves; duplicate topics, shared owners, orphaned records and duplicate-producing topic changes are rejected. Learner deletion cascades to progress and preserves shared topics. Event identity/type/cardinality checks pass.");
    println!("Scope: native EDB schema, policy and difficulty predicates, ownership and history semantics. Engine equations and embedded receipt payloads are checked separately.");
    Ok(())
}
