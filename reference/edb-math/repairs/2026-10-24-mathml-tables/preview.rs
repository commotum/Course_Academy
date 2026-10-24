//! Durable EDB writer with Course Academy's native schema predicates.
#[path = "/home/jake/Developer/Course_Academy/engine/edb/answer_fields.rs"] mod answer_fields;
#[path = "/home/jake/Developer/Course_Academy/engine/edb/configuration.rs"] mod configuration;
#[path = "/home/jake/Developer/Course_Academy/engine/edb/progress.rs"] mod progress;

use edb_core::{
    BackgroundIndexingConfig, LocalTransactionServer, LocalTransportConfig, NativeRegistry,
    RuntimeValue, SemanticError, Symbol, TransactionExecutionOptions, TransactionService,
    TransactionServiceConfig, Value, postgres_config_from_env,
};
use std::{error::Error, io::Write, sync::mpsc, time::Duration};

fn wait_for_stop(stop: &mpsc::Receiver<()>, available: impl Fn() -> bool) -> bool {
    loop {
        if !available() {
            return false;
        }
        match stop.recv_timeout(Duration::from_millis(250)) {
            Ok(()) | Err(mpsc::RecvTimeoutError::Disconnected) => return true,
            Err(mpsc::RecvTimeoutError::Timeout) => {}
        }
    }
}

fn registry() -> Result<NativeRegistry, SemanticError> {
    let mut builder = NativeRegistry::builder();
    builder.entity_predicate(
        Symbol::new("course-academy.topic", "valid-difficulty?"),
        |db, entity, control| {
            control.check(1)?;
            Ok(RuntimeValue::Scalar(Value::Bool(
                configuration::valid_topic_difficulty(db, entity)?,
            )))
        },
    )?;
    builder.entity_predicate(
        Symbol::new("course-academy.policy", "valid?"),
        |db, entity, control| {
            control.check(1)?;
            Ok(RuntimeValue::Scalar(Value::Bool(
                configuration::valid_policy(db, entity)?,
            )))
        },
    )?;
    builder.entity_predicate(
        Symbol::new("course-academy.progress", "valid-profile?"),
        |db, entity, control| {
            control.check(1)?;
            Ok(RuntimeValue::Scalar(Value::Bool(progress::valid_profile(
                db, entity,
            )?)))
        },
    )?;
    builder.entity_predicate(
        Symbol::new("course-academy.progress", "valid-progress?"),
        |db, entity, control| {
            control.check(1)?;
            Ok(RuntimeValue::Scalar(Value::Bool(progress::valid_progress(
                db, entity,
            )?)))
        },
    )?;
    builder.entity_predicate(
        Symbol::new("course-academy.answer-field", "valid?"),
        |db, entity, control| {
            control.check(1)?;
            Ok(RuntimeValue::Scalar(Value::Bool(
                answer_fields::valid_field(db, entity)?,
            )))
        },
    )?;
    Ok(builder.build())
}



fn main() -> Result<(), Box<dyn Error>> {
 let args:Vec<_>=std::env::args().collect();
 let path=&args[1];let changes:serde_json::Value=serde_json::from_str(&std::fs::read_to_string(&args[2])?)?;
 let db=edb_core::Peer::connect_configured(&postgres_config_from_env()?,"math",256)?.db();
 let report=db.with_forms_with_execution_options(
  &edb_core::edn_transaction::read_edn_transaction(&std::fs::read_to_string(path)?)?,
  std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH)?.as_millis() as i64,
  edb_core::EntityRef::Ident(edb_core::Keyword::new("agent","codex")),
  edb_core::SpeculationLimits::default(),
  &TransactionExecutionOptions{native:registry()?,..Default::default()})?;
 let mut comparisons=0;
 for change in changes.as_array().ok_or("fields must be an array")? {
  let eid=change["entity"].as_u64().ok_or("entity required")?;
  let (ns,name)=change["attribute"].as_str().ok_or("attribute required")?.split_once('/').ok_or("attribute syntax")?;
  let attribute=report.db_after.schema().resolve_ident(&edb_core::Keyword::new(ns,name)).ok_or("attribute missing")?;
  let actual=report.db_after.values(eid,attribute)?;
  assert!(matches!(actual.as_slice(),[Value::String(v)] if v==change["after"].as_str().unwrap()));
  comparisons+=1;
 }
 assert!(report.tx_data.iter().all(|d|d.source==17592186576411));
 let proof=serde_json::json!({"committed":false,"native_validation_passed":true,"db_before_t":db.basis_t(),"fields_verified":comparisons,"datoms":report.tx_data.len(),"exact_proposed_values_verified":true});
 std::fs::write(&args[3],serde_json::to_vec_pretty(&proof)?)?;
 println!("{}",proof);
 Ok(())
}
