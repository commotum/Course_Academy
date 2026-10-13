//! Noncommitting capture previews with the application's native schema checks.
#[path = "/home/jake/Developer/Course_Academy/engine/edb/answer_fields.rs"]
mod answer_fields;
#[path = "/home/jake/Developer/Course_Academy/engine/edb/configuration.rs"]
mod configuration;
#[path = "/home/jake/Developer/Course_Academy/engine/edb/progress.rs"]
mod progress;

use edb_core::edn::{EdnValue, write_edn};
use edb_core::edn_value::{edn_keyword, transaction_report_to_edn};
use edb_core::{
    Connection, DatabaseValue, EntityRef, NativeRegistry, RuntimeValue, SemanticError, Symbol,
    TransactionExecutionOptions, Value, postgres_config_from_env,
};
use std::{collections::BTreeMap, io::Read, process::ExitCode, time::{SystemTime, UNIX_EPOCH}};

fn registry() -> Result<NativeRegistry, SemanticError> {
    type Predicate = fn(&DatabaseValue, u64) -> Result<bool, SemanticError>;
    let mut builder = NativeRegistry::builder();
    for (namespace, name, predicate) in [
        ("course-academy.topic", "valid-difficulty?", configuration::valid_topic_difficulty as Predicate),
        ("course-academy.policy", "valid?", configuration::valid_policy as Predicate),
        ("course-academy.progress", "valid-profile?", progress::valid_profile as Predicate),
        ("course-academy.progress", "valid-progress?", progress::valid_progress as Predicate),
        ("course-academy.answer-field", "valid?", answer_fields::valid_field as Predicate),
    ] {
        builder.entity_predicate(Symbol::new(namespace, name), move |db, entity, control| {
            control.check(1)?;
            Ok(RuntimeValue::Scalar(Value::Bool(predicate(db, entity)?)))
        })?;
    }
    Ok(builder.build())
}


use std::io::Write;
fn run() -> Result<(), Box<dyn std::error::Error>> {
 let args:Vec<_>=std::env::args().skip(1).collect();
 if args.len()!=3{return Err("held-preview OUTPUT_DIR SOURCE_IDENT BATCH_COUNT".into())}
 let out=std::path::Path::new(&args[0]);let source=EntityRef::from_edn(&args[1])?;
 let connection=Connection::connect_configured(postgres_config_from_env()?,"math",256)?;
 let mut db=connection.db();
 println!("CAPTURED_BASIS {}",db.basis_t());std::io::stdout().flush()?;
 let mut signal=String::new();std::io::stdin().read_line(&mut signal)?;
 if signal.trim()!="PREVIEW"{return Err("expected PREVIEW after preparation; no writes performed".into())}
 for number in 1..=args[2].parse::<usize>()? {
  let directory=out.join(format!("batch-{number:02}"));
  let text=std::fs::read_to_string(directory.join("transaction.edn"))?;
  if text.len()>16*1024*1024{return Err("transaction exceeds EDN input bound".into())}
  let forms=edb_core::edn_transaction::read_edn_transaction(&text)?;
  let at=i64::try_from(SystemTime::now().duration_since(UNIX_EPOCH)?.as_millis())?;
  let report=db.with_forms_with_execution_options(&forms,at,source.clone(),Default::default(),&TransactionExecutionOptions{native:registry()?,..Default::default()})?;
  let EdnValue::Map(mut fields)=transaction_report_to_edn(report.db_before.basis_t(),report.db_after.basis_t(),&report.tx_data,&report.tempids)? else{unreachable!()};
  fields.push((edn_keyword("edb","committed"),EdnValue::Bool(false)));
  fields.push((edn_keyword("edb","speculative"),EdnValue::Bool(true)));
  std::fs::write(directory.join("preview.edn"),write_edn(&EdnValue::Map(fields))?+"\n")?;
  db=report.db_after;
  println!("PREVIEWED_BATCH {number}");std::io::stdout().flush()?;
 }
 Ok(())
}
fn main()->ExitCode{match run(){Ok(())=>ExitCode::SUCCESS,Err(error)=>{eprintln!("Noncommitting preview failed: {error}");ExitCode::FAILURE}}}
