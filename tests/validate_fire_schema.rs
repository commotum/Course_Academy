// Run from the repository root; requires the local EDB edb_core build.
use edb_core::{Database, Keyword, SemanticError, TxFunctions, TxReport, Value};
#[path = "../engine/edb/configuration.rs"]
mod configuration;
mod edb_activity_checks;
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
    let mut schema_count = 0usize;
    for dir in [
        "schema/data",
        "schema/content",
        "schema/learner",
        "schema/engine",
    ] {
        let mut paths = fs::read_dir(root.join(dir))?
            .filter_map(Result::ok)
            .map(|e| e.path())
            .filter(|p| p.extension().is_some_and(|e| e == "edn"))
            // Review drafts live beside the current content schemas but are not installed.
            .filter(|p| {
                p.file_name()
                    .and_then(|n| n.to_str())
                    .is_none_or(|n| !n.starts_with("proposed-"))
            })
            // Seed transactions are applied after schema installation.
            .filter(|p| {
                let seed_files = [
                    "1-2-sequences.edn",
                    "2-3-courses.edn",
                    "2-4-self-directed-course.edn",
                    "3-2-units.edn",
                    "3-3-course-units.edn",
                    "4-2-modules.edn",
                    "4-3-unit-modules.edn",
                    "5-3-topics.edn",
                    "5-4-module-topics.edn",
                    "5-5-prerequisites.edn",
                ];
                p.file_name()
                    .and_then(|n| n.to_str())
                    .is_none_or(|n| !seed_files.contains(&n))
            })
            .collect::<Vec<_>>();
        paths.sort();
        for path in paths {
            db = transact(&db, &fs::read_to_string(&path)?, clock)
                .map_err(|e| format!("{}: {e}", path.display()))?
                .db_after;
            clock += 1;
            schema_count += 1;
        }
    }
    let fixture = r#"[
 {:db/id "advanced" :topic/id #uuid "b3d88ca6-d319-409b-bdb1-000000000001" :topic/title "Illustrative advanced topic" :topic/encompasses ["edge"]}
 {:db/id "component" :topic/id #uuid "b3d88ca6-d319-409b-bdb1-000000000002" :topic/title "Illustrative component topic" :topic/next ["advanced"]}
 {:db/id "learner" :learner/id "schema-check-learner"
  :learner/performance "performance"
  :learner/knowledge-profile ["state" "unlearned-state"]
  :db/ensure :learner/validate}
 {:db/id "performance"
  :performance/assessment-accuracy 0.8 :performance/practice-accuracy 0.9
  :performance/assessment-mass 0.0 :performance/practice-mass 4.0
  :db/ensure :performance/validate}
 {:db/id "policy" :policy/id #uuid "b3d88ca6-d319-409b-bdb1-000000000003"
  :policy/base-half-life-days 1.0 :policy/interval-growth 2.0 :policy/maximum-half-life-days 36500.0
  :policy/review-threshold 0.5 :policy/initial-retention 1.0 :policy/early-practice-discount-power 1.0
  :policy/initial-accuracy 0.8 :policy/accuracy-update-rate 0.2 :policy/speed-exponent 2.0
  :policy/minimum-speed 0.25 :policy/maximum-speed 4.0
  :policy/overdue-failure-slope 1.0 :policy/maximum-failure-multiplier 4.0
  :policy/gate-slow-implicit true :policy/retention-update-order :policy.retention-update/decay-before-add
  :policy/future-horizon-days 7.0 :db/ensure :policy/validate}
 {:db/id "edge" :encompassing/topic "component" :encompassing/weight 0.0
  :encompassing/rationale "Illustrative explicit zero coverage for schema validation." :db/ensure :encompassing/validate}
 {:db/id "advanced" :topic/difficulty 0.75 :db/ensure :topic/difficulty-validate}
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
    let learner = find_string(&db, "learner", "id", "schema-check-learner");
    let performance_attr = db.entid(&Keyword::new("learner", "performance")).unwrap() as u32;
    let performance = match db.values(learner, performance_attr).as_slice() {
        [Value::Ref(id)] => *id,
        other => panic!("Expected one performance component, got {other:?}"),
    };
    let performance_owners = db.datoms_with_prefix(&edb_core::IndexPrefix::Vaet {
        value: Value::Ref(performance),
        attribute: Some(performance_attr),
        entity: None,
    })?;
    assert_eq!(performance_owners.len(), 1);
    assert_eq!(performance_owners[0].entity, learner);
    let missing_performance_value = r#"[{:performance/assessment-accuracy 0.8
      :performance/practice-accuracy 0.9 :performance/assessment-mass 0.0
      :db/ensure :performance/validate}]"#;
    assert_eq!(
        transact(&db, missing_performance_value, 2050)
            .unwrap_err()
            .code,
        "transaction/entity-spec"
    );
    let topicattr = db.entid(&Keyword::new("progress", "topic")).unwrap() as u32;
    let topic = match db.values(state, topicattr).first().unwrap() {
        Value::Ref(id) => *id,
        other => panic!("Unexpected ref {other:?}"),
    };
    let input_basis = db.basis_t();
    edb_configuration_checks::check(&db, topic, input_basis)?;
    let state_count = db
        .datoms(edb_core::View::Current, edb_core::IndexOrder::Eavt)
        .iter()
        .filter(|d| d.attribute == idattr && d.added)
        .count();
    let update =
        format!(r#"[{{:db/id {state} :progress/memory 0.75 :db/ensure :progress/validate}}]"#);
    db = transact(&db, &update, 2500)?.db_after;
    assert_eq!(
        state_count,
        db.datoms(edb_core::View::Current, edb_core::IndexOrder::Eavt)
            .iter()
            .filter(|d| d.attribute == idattr && d.added)
            .count()
    );
    db = transact(
        &db,
        r#"[{:learner/id "schema-check-other" :db/ensure :learner/validate}]"#,
        2600,
    )?
    .db_after;
    let wrong_type = format!(r#"[{{:db/id {state} :progress/learned "true"}}]"#);
    assert!(transact(&db, &wrong_type, 3000).is_err());
    for invalid in [
        ":progress/repetitions -0.1",
        ":progress/memory -0.1",
        ":progress/interval-days 0.0",
        ":progress/assessment-accuracy 1.1",
        ":progress/practice-accuracy -0.1",
        ":progress/assessment-mass -0.1",
        ":progress/practice-mass -0.1",
    ] {
        assert!(
            transact(
                &db,
                &format!("[{{:db/id {state} {invalid} :db/ensure :progress/validate}}]"),
                3000
            )
            .is_err()
        );
    }
    assert!(
        transact(
            &db,
            &format!("[{{:db/id {state} :progress/memory 1.5 :db/ensure :progress/validate}}]"),
            3000
        )
        .is_ok()
    );
    assert!(
        transact(
            &db,
            &format!("[{{:db/id {state} :progress/policy {topic} :db/ensure :progress/validate}}]"),
            3000
        )
        .is_err()
    );
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
  {{:db/id {learner} :learner/knowledge-profile "duplicate" :db/ensure :learner/validate}}]"#
    );
    assert!(transact(&db, &duplicate, 3000).is_err());
    let shared = format!(
        r#"[{{:learner/id "shared-owner" :learner/knowledge-profile {state} :db/ensure :learner/validate}}]"#
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
    let other = find_string(&db, "learner", "id", "schema-check-other");
    let transfer = format!(
        r#"[[:db/retract {learner} :learner/knowledge-profile {state}]
  {{:db/id {learner} :db/ensure :learner/validate}}
  {{:db/id {other} :learner/knowledge-profile {state} :db/ensure :learner/validate}}
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
    for name in [
        "assessment-accuracy",
        "practice-accuracy",
        "assessment-mass",
        "practice-mass",
    ] {
        let attr = db.entid(&Keyword::new("performance", name)).unwrap() as u32;
        assert!(!db.values(performance, attr).is_empty());
        assert!(removed.values(performance, attr).is_empty());
    }
    let topicidattr = db.entid(&Keyword::new("topic", "id")).unwrap() as u32;
    assert!(!removed.values(topic, topicidattr).is_empty());
    edb_activity_checks::check(&db)?;
    println!(
        "PASS all {schema_count} current schemas install; policy/difficulty/progress predicates, single-owner topic progress, identity-preserving writes, required fields, component deletion and history checks pass."
    );
    println!(
        "Scope: in-memory native EDB transaction/CAS validation and Rust-generated EDN. Durable writer basis-conflict/idempotency behavior is not exercised without a running transactor."
    );
    Ok(())
}
