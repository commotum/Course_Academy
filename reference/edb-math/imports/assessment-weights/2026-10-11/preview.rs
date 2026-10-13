//! Preview this approved request using the application's existing policy predicate.
#[allow(dead_code)]
#[path = "../../../../../engine/edb/configuration.rs"]
mod configuration;

use edb_core::{
    EntityRef, Keyword, NativeRegistry, Peer, RuntimeValue, Symbol,
    TransactionExecutionOptions, Value, postgres_config_from_env,
};
use edb_core::edn::{EdnValue, write_edn};
use edb_core::edn_transaction::read_edn_transaction;
use edb_core::edn_value::{edn_keyword, transaction_report_to_edn};
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.len() != 2 {
        return Err("usage: preview TRANSACTION.edn BASIS".into());
    }
    let basis: u64 = args[1].parse()?;
    let db = Peer::connect_configured(&postgres_config_from_env()?, "math", 256)?.db();
    if db.basis_t() != basis {
        return Err("database basis changed; do not commit the stale request".into());
    }
    let mut builder = NativeRegistry::builder();
    builder.entity_predicate(Symbol::new("course-academy.policy", "valid?"), |db, entity, control| {
        control.check(1)?;
        Ok(RuntimeValue::Scalar(Value::Bool(configuration::valid_policy(db, entity)?)))
    })?;
    let report = db.with_forms_with_execution_options(
        &read_edn_transaction(&std::fs::read_to_string(&args[0])?)?,
        std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH)?.as_millis().try_into()?,
        EntityRef::Ident(Keyword::new("agent", "gpt-6.1-sol-high")),
        Default::default(),
        &TransactionExecutionOptions { native: builder.build(), ..Default::default() },
    )?;
    let EdnValue::Map(mut fields) = transaction_report_to_edn(
        report.db_before.basis_t(), report.db_after.basis_t(), &report.tx_data, &report.tempids,
    )? else { unreachable!() };
    fields.push((edn_keyword("edb", "committed"), EdnValue::Bool(false)));
    println!("{}", write_edn(&EdnValue::Map(fields))?);
    Ok(())
}
