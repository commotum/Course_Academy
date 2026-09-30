//! Behavioral checks run by validate_fire_schema.rs against the installed schema.
use super::{configuration, transact};
use edb_core::{Database, EntityRef, Keyword, TxForm, TxFunctions, TxOp, Value};
use std::error::Error;

pub fn check(db: &Database, topic: u64, input_basis: u64) -> Result<(), Box<dyn Error>> {
    let policy = r#"[:policy/id #uuid "b3d88ca6-d319-409b-bdb1-000000000003"]"#;
    let reject = |text: &str| {
        edb_core::edn_transaction::read_edn_transaction(text).expect("valid EDN test transaction");
        assert!(
            transact(db, text, 2200).is_err(),
            "Expected rejection: {text}"
        );
    };
    // Each mutation runs on an isolated speculative branch; no policy writer is exercised.
    for change in [
        ":policy/base-half-life-days 0.0",
        ":policy/interval-growth 1.0",
        ":policy/maximum-half-life-days 0.5",
        ":policy/review-threshold 1.0",
        ":policy/initial-accuracy 1.0",
        ":policy/accuracy-update-rate 1.1",
        ":policy/minimum-speed 1.1",
        ":policy/maximum-speed 0.9",
        ":policy/maximum-failure-multiplier 0.9",
        ":policy/overdue-failure-slope -1.0",
        ":policy/early-practice-discount-power 0.0",
        ":policy/future-horizon-days -1.0",
        ":policy/retention-update-order :answer-field.type/radio",
        ":policy/gate-slow-implicit \"true\"",
    ] {
        reject(&format!(
            "[{{:db/id {policy} {change} :db/ensure :policy/validate}}]"
        ));
    }
    reject(&format!(
        r#"[[:db/retract {policy} :policy/accuracy-update-rate 0.2]
        {{:db/id {policy} :db/ensure :policy/validate}}]"#
    ));
    assert!(transact(db, &format!("[{{:db/id {policy} :policy/retention-update-order :policy.retention-update/add-before-decay :db/ensure :policy/validate}}]"), 2200).is_ok());

    for invalid in [-0.1, 1.1] {
        reject(&format!(
            "[{{:db/id {topic} :topic/difficulty {invalid} :db/ensure :topic/difficulty-validate}}]"
        ));
    }
    assert!(
        transact(
            db,
            &format!(
                "[{{:db/id {topic} :topic/difficulty 0.9 :db/ensure :topic/difficulty-validate}}]"
            ),
            2200
        )
        .is_ok()
    );
    // EDB's EDN reader does not expose nonfinite literals; exercise native values.
    let mut functions = TxFunctions::new();
    configuration::register_configuration_predicates(&mut functions);
    for (ns, name, entity, spec) in [
        (
            "policy",
            "speed-exponent",
            EntityRef::Lookup {
                attribute: db.entid(&Keyword::new("policy", "id")).unwrap() as u32,
                value: Value::Uuid(0xb3d88ca6d319409bbdb1000000000003),
            },
            "validate",
        ),
        (
            "topic",
            "difficulty",
            EntityRef::Id(topic),
            "difficulty-validate",
        ),
    ] {
        for invalid in [f64::NAN, f64::INFINITY, f64::NEG_INFINITY] {
            let forms = [
                TxForm::Op(TxOp::Add {
                    entity: entity.clone(),
                    attribute: db.entid(&Keyword::new(ns, name)).unwrap() as u32,
                    value: Value::Double(invalid).into(),
                }),
                TxForm::Op(TxOp::Ensure {
                    entity: entity.clone(),
                    spec: EntityRef::Ident(Keyword::new(ns, spec)),
                }),
            ];
            assert!(db.with_forms(&forms, &functions, 2200).is_err());
        }
    }

    // A complete curriculum topic can still have no difficulty estimate.
    let unknown = r#"[{:db/id "kp" :knowledge-point/id #uuid "b3d88ca6-d319-409b-bdb1-000000000006"}
        {:topic/id #uuid "b3d88ca6-d319-409b-bdb1-000000000005" :topic/title "Uncalibrated topic"
         :topic/knowledge-points ["kp"] :db/ensure :topic/validate}]"#;
    assert!(transact(db, unknown, 2200).is_ok());
    assert!(
        transact(
            db,
            &unknown.replace(":topic/title", ":topic/difficulty 0.8 :topic/title"),
            2200
        )
        .is_ok()
    );

    // History recovers the earlier estimate independently of later updates.
    let updated = transact(
        db,
        &format!(
            "[{{:db/id {topic} :topic/difficulty 0.8 :db/ensure :topic/difficulty-validate}}]"
        ),
        2200,
    )?
    .db_after;
    let attr = updated.entid(&Keyword::new("topic", "difficulty")).unwrap() as u32;
    assert_eq!(updated.values(topic, attr), vec![&Value::Double(0.8)]);
    let previous = updated.database_value().as_of(input_basis);
    assert_eq!(previous.values(topic, attr)?, vec![Value::Double(0.75)]);
    assert!(configuration::valid_topic_difficulty(&previous, topic)?);
    println!(
        "PASS typed policies reject invalid enums, missing settings, nonfinite values and inconsistent bounds; topic estimates preserve unknown values and reject invalid ranges; basis T retrieves the original difficulty after later updates."
    );
    Ok(())
}
