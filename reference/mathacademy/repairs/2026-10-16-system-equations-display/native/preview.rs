//! Read-only speculative transaction and before/after Pulls from one native value.
#[path = "/home/jake/Developer/Course_Academy/engine/edb/answer_fields.rs"]
mod answer_fields;
#[path = "/home/jake/Developer/Course_Academy/engine/edb/configuration.rs"]
mod configuration;
#[path = "/home/jake/Developer/Course_Academy/engine/edb/progress.rs"]
mod progress;
use edb_core::edn::{EdnValue, read_edn, write_edn};
use edb_core::edn_pull::parse_pull_edn;
use edb_core::edn_value::{edn_keyword, query_value_to_edn, transaction_report_to_edn};
use edb_core::{Connection, DatabaseValue, EntityRef, NativeRegistry, RuntimeValue,
    SemanticError, Symbol, TransactionExecutionOptions, Value, postgres_config_from_env};
use std::{error::Error, fs, path::Path, time::{SystemTime, UNIX_EPOCH}};

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

// native-pulls.edn: [["questions" "[* ...]" [123 456]] ...]
fn pulls(db: &DatabaseValue, directory: &Path, stage: &str) -> Result<(), Box<dyn Error>> {
    let EdnValue::Vector(groups) = read_edn(&fs::read_to_string(directory.join("native-pulls.edn"))?)? else {
        return Err("native-pulls.edn must be a vector".into());
    };
    for group in groups {
        let EdnValue::Vector(parts) = group else { return Err("Pull group must be vector".into()); };
        let [EdnValue::String(name), EdnValue::String(pattern), EdnValue::Vector(ids)] = parts.as_slice() else {
            return Err("Pull group must contain name, pattern text and entity IDs".into());
        };
        if name.is_empty() || !name.chars().all(|c| c.is_ascii_alphanumeric() || c == '-') {
            return Err("Unsafe Pull output name".into());
        }
        let pattern = parse_pull_edn(pattern)?;
        let mut values = Vec::new();
        for id in ids {
            let EdnValue::Long(id) = id else { return Err("Pull entity ID must be integer".into()); };
            let id = u64::try_from(*id)?;
            values.push(query_value_to_edn(&db.pull(&pattern, id)?)?);
        }
        fs::write(directory.join(format!("preview-{name}-{stage}.edn")),
            write_edn(&EdnValue::Vector(values))? + "\n")?;
    }
    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.len() != 3 { return Err("usage: preview DIRECTORY SOURCE_IDENT EXPECTED_BASIS".into()); }
    let directory = Path::new(&args[0]);
    let source = EntityRef::from_edn(&args[1])?;
    let expected: u64 = args[2].parse()?;
    let connection = Connection::connect_configured(postgres_config_from_env()?, "math", 256)?;
    let db = connection.db();
    if db.basis_t() != expected {
        return Err(format!("Current basis {} differs from prepared {expected}; no preview or write", db.basis_t()).into());
    }
    let text = fs::read_to_string(directory.join("transaction.edn"))?;
    if text.len() > 16 * 1024 * 1024 { return Err("Transaction input exceeds 16 MiB".into()); }
    let forms = edb_core::edn_transaction::read_edn_transaction(&text)?;
    let at = i64::try_from(SystemTime::now().duration_since(UNIX_EPOCH)?.as_millis())?;
    let report = db.with_forms_with_execution_options(&forms, at, source,
        Default::default(), &TransactionExecutionOptions { native: registry()?, ..Default::default() })?;
    pulls(&report.db_before, directory, "before")?;
    pulls(&report.db_after, directory, "after")?;
    let EdnValue::Map(mut fields) = transaction_report_to_edn(report.db_before.basis_t(),
        report.db_after.basis_t(), &report.tx_data, &report.tempids)? else { unreachable!() };
    fields.push((edn_keyword("edb", "committed"), EdnValue::Bool(false)));
    fields.push((edn_keyword("edb", "speculative"), EdnValue::Bool(true)));
    println!("{}", write_edn(&EdnValue::Map(fields))?);
    Ok(())
}
