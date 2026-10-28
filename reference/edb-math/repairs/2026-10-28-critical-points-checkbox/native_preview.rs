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

fn usage() -> SemanticError {
    SemanticError::incorrect("cli/preview-usage", "usage: native-preview with --database NAME --file PATH --source IDENT")
}

fn arguments(raw: &[String]) -> Result<BTreeMap<String, String>, SemanticError> {
    if raw.first().map(String::as_str) != Some("with") || raw.len() != 7 {
        return Err(usage());
    }
    let mut values = BTreeMap::new();
    for pair in raw[1..].chunks_exact(2) {
        if !["--database", "--file", "--source"].contains(&pair[0].as_str())
            || pair[1].is_empty() || values.insert(pair[0].clone(), pair[1].clone()).is_some() {
            return Err(usage());
        }
    }
    Ok(values)
}

fn run() -> Result<(), Box<dyn std::error::Error>> {
    let args = arguments(&std::env::args().skip(1).collect::<Vec<_>>())?;
    let mut input: Box<dyn Read> = if args["--file"] == "-" {
        Box::new(std::io::stdin())
    } else {
        Box::new(std::fs::File::open(&args["--file"])?)
    };
    let mut text = String::new();
    input.by_ref().take(16 * 1024 * 1024 + 1).read_to_string(&mut text)?;
    if text.len() > 16 * 1024 * 1024 {
        return Err(SemanticError::incorrect("cli/preview-input-size", "EDN input exceeds 16 MiB").into());
    }
    let forms = edb_core::edn_transaction::read_edn_transaction(&text)?;
    let source = EntityRef::from_edn(&args["--source"])?;
    let connection = Connection::connect_configured(postgres_config_from_env()?, &args["--database"], 256)?;
    let db = connection.db();
    let at = i64::try_from(SystemTime::now().duration_since(UNIX_EPOCH)?.as_millis())?;
    let report = db.with_forms_with_execution_options(
        &forms, at, source, Default::default(),
        &TransactionExecutionOptions { native: registry()?, ..Default::default() },
    )?;
    let EdnValue::Map(mut fields) = transaction_report_to_edn(
        report.db_before.basis_t(), report.db_after.basis_t(), &report.tx_data, &report.tempids,
    )? else { unreachable!("transaction report is a map") };
    fields.push((edn_keyword("edb", "committed"), EdnValue::Bool(false)));
    fields.push((edn_keyword("edb", "speculative"), EdnValue::Bool(true)));
    let directory=std::path::Path::new(&args["--file"]).parent().ok_or("transaction directory")?;
    for (ids,pattern,output) in [("question-ids.txt","question-pull.edn","preview-questions.edn"),("retained-ids.txt","retained-pull.edn","preview-retained.edn")] {
        let pattern=edb_core::edn_pull::parse_pull_edn(&std::fs::read_to_string(directory.join(pattern))?)?;
        let mut values=vec![];
        for line in std::fs::read_to_string(directory.join(ids))?.lines(){
            if line.trim().is_empty(){continue}
            let eid=line.parse::<u64>()?;
            let value=report.db_after.pull(&pattern,eid)?;
            values.push(edb_core::edn_value::query_value_to_edn(&value)?);
        }
        std::fs::write(directory.join(output),write_edn(&EdnValue::Vector(values))?+"\n")?;
    }
    println!("{}", write_edn(&EdnValue::Map(fields))?);
    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            if let Some(error) = error.downcast_ref::<SemanticError>() {
                eprintln!("ERROR category={:?} code={}", error.category, error.code);
                if error.code.starts_with("cli/") { eprintln!("{}", error.message); }
            } else {
                eprintln!("ERROR code=preview/io");
            }
            ExitCode::FAILURE
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn only_noncommitting_preview_arguments_are_accepted() {
        let args = ["with", "--database", "math", "--file", "-", "--source", ":org/Math-Academy"]
            .map(String::from);
        assert_eq!(arguments(&args).unwrap()["--source"], ":org/Math-Academy");
        for command in ["transact", "transactor", "create", "status"] {
            let mut invalid = args.clone(); invalid[0] = command.into();
            assert!(arguments(&invalid).is_err());
        }
        let mut invalid = args.clone(); invalid[3] = "--database".into();
        assert!(arguments(&invalid).is_err());
    }
}
