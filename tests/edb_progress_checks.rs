//! Progress validation must remain local even when many records change together.
use edb_core::{
    Database, EntityRef, Keyword, NativeRegistry, RuntimeValue, SpeculationLimits, Symbol,
    TransactionExecutionOptions, Value,
};
use std::{error::Error, fmt::Write};

fn state_fields(topic: &str, policy: u64) -> String {
    format!(
        r#":progress/topic {topic}
        :progress/repetitions 0.0 :progress/memory 0.0
        :progress/memory-at #inst "2026-09-26T00:00:00.000Z"
        :progress/interval-days 1.0 :progress/assessment-accuracy 0.5
        :progress/practice-accuracy 0.5 :progress/assessment-mass 0.0
        :progress/practice-mass 0.0 :progress/learned false :progress/policy {policy}"#
    )
}

pub fn check(db: &Database, learner: u64, state: u64, topic: u64) -> Result<(), Box<dyn Error>> {
    let policy_attr = db.entid(&Keyword::new("progress", "policy")).unwrap() as u32;
    let policy = match db.values(state, policy_attr).as_slice() {
        [Value::Ref(policy)] => *policy,
        other => panic!("Expected policy reference, got {other:?}"),
    };
    for forms in [
        format!(
            "[[:db/retract {learner} :learner/knowledge-profile {state}] \
             [:db/add {policy} :learner/knowledge-profile {state}] \
             {{:db/id {state} :db/ensure :progress/validate}}]"
        ),
        format!("[{{:db/id {state} :progress/topic {policy} :db/ensure :progress/validate}}]"),
        format!(
            "[{{:learner/id \"second-owner\" :learner/knowledge-profile {state}}} \
             {{:db/id {state} :db/ensure :progress/validate}}]"
        ),
    ] {
        assert_eq!(
            super::transact(db, &forms, 3000).unwrap_err().code,
            "transaction/entity-predicate"
        );
    }
    // The callback itself requires identity, independently of the entity spec's
    // required-attribute list (native callers may invoke the callback directly).
    let missing_id = super::transact(db, &format!("[[:db/retract {state} :progress/id]]"), 3000)?;
    assert!(!super::progress::valid_progress(
        &missing_id.db_after.database_value(),
        state
    )?);

    // Another learner's progress for the same shared topic is valid.
    let shared_topic = super::transact(
        db,
        &format!(
            r#"[{{:db/id "other-state" :progress/id "other-topic-state" {}
                 :db/ensure :progress/validate}}
                {{:learner/id "other-topic-learner" :learner/knowledge-profile "other-state"
                 :db/ensure :learner/validate}}
                {{:db/id {state} :db/ensure :progress/validate}}]"#,
            state_fields(&topic.to_string(), policy)
        ),
        3000,
    )?;
    // Even a malformed candidate with multiple owners must count as a
    // duplicate if any owner is this learner; progress-only ensure catches it.
    assert_eq!(
        super::transact(
            &shared_topic.db_after,
            &format!(
                r#"[[:db/add {learner} :learner/knowledge-profile [:progress/id "other-topic-state"]]
                    {{:db/id {state} :db/ensure :progress/validate}}]"#
            ),
            3001,
        )
        .unwrap_err()
        .code,
        "transaction/entity-predicate"
    );

    // A progress ensure covers that record; learner ensure covers siblings.
    let malformed_sibling = super::transact(
        db,
        &format!(
            r#"[{{:db/id "incomplete-sibling" :progress/id "incomplete-sibling"}}
                {{:db/id {learner} :learner/knowledge-profile "incomplete-sibling"}}]"#
        ),
        3000,
    )?;
    super::transact(
        &malformed_sibling.db_after,
        &format!("[{{:db/id {state} :db/ensure :progress/validate}}]"),
        3001,
    )?;
    assert_eq!(
        super::transact(
            &malformed_sibling.db_after,
            &format!("[{{:db/id {learner} :db/ensure :learner/validate}}]"),
            3001,
        )
        .unwrap_err()
        .code,
        "transaction/entity-predicate"
    );

    check_batch_read_budget(db, policy)
}

fn check_batch_read_budget(db: &Database, policy: u64) -> Result<(), Box<dyn Error>> {
    const PROFILE_SIZE: usize = 2_000;
    const CHANGED: usize = 152;
    let mut fixture = String::from("[");
    for i in 0..PROFILE_SIZE {
        write!(
            fixture,
            r#"{{:db/id "budget-topic-{i}" :topic/id #uuid "b3d88ca6-d319-409b-bdb2-{i:012x}"}}
               {{:db/id "budget-state-{i}" :progress/id "budget-state-{i}" {}}}"#,
            state_fields(&format!("\"budget-topic-{i}\""), policy)
        )?;
    }
    fixture.push_str(
        r#"{:db/id "budget-learner" :learner/id "budget-learner" :learner/knowledge-profile ["#,
    );
    for i in 0..PROFILE_SIZE {
        write!(fixture, "\"budget-state-{i}\" ")?;
    }
    fixture.push_str("] :db/ensure :learner/validate}]");
    let fixture = super::transact(db, &fixture, 3000)?;
    let mut updates = String::from("[");
    for i in 0..CHANGED {
        write!(
            updates,
            r#"{{:db/id {} :progress/memory 0.75 :db/ensure :progress/validate}}"#,
            fixture.tempids[&format!("budget-state-{i}")]
        )?;
    }
    write!(
        updates,
        "{{:db/id {} :db/ensure :learner/validate}}]",
        fixture.tempids["budget-learner"]
    )?;
    let mut registry = NativeRegistry::builder();
    registry.entity_predicate(
        Symbol::new("course-academy.progress", "valid-profile?"),
        |db, entity, control| {
            control.check(1)?;
            Ok(RuntimeValue::Scalar(Value::Bool(
                super::progress::valid_profile(db, entity)?,
            )))
        },
    )?;
    registry.entity_predicate(
        Symbol::new("course-academy.progress", "valid-progress?"),
        |db, entity, control| {
            control.check(1)?;
            Ok(RuntimeValue::Scalar(Value::Bool(
                super::progress::valid_progress(db, entity)?,
            )))
        },
    )?;
    let report = fixture
        .db_after
        .database_value()
        .with_forms_with_execution_options(
            &edb_core::edn_transaction::read_edn_transaction(&updates)?,
            3001,
            EntityRef::Id(edb_core::DB_SOURCE_SYSTEM),
            SpeculationLimits {
                // Well below the production 1M datom/64 MiB limit. Repeating
                // full-profile validation exhausts even the production limit.
                max_read_datoms: 50_000,
                max_read_bytes: 8 * 1024 * 1024,
                ..Default::default()
            },
            &TransactionExecutionOptions {
                native: registry.build(),
                ..Default::default()
            },
        )?;
    let memory_attr = db.entid(&Keyword::new("progress", "memory")).unwrap() as u32;
    for i in 0..CHANGED {
        assert_eq!(
            report
                .db_after
                .values(fixture.tempids[&format!("budget-state-{i}")], memory_attr,)?,
            vec![Value::Double(0.75)]
        );
    }
    println!(
        "PASS {CHANGED} progress updates plus full validation of a {PROFILE_SIZE}-record profile within 50,000 read datoms / 8 MiB."
    );
    Ok(())
}
