//! Task-scoped CAS-only submission through the configured application writer.
//! Every mutation is an exact field CAS; entity specs validate current db-after.
use edb_core::{Connection, EntityRef, SemanticError, TransactionRequest, postgres_config_from_env};
use edb_core::edn::{EdnValue, write_edn};
use edb_core::edn_value::{edn_keyword, transaction_report_to_edn};
use std::{collections::BTreeMap, error::Error, process::ExitCode, time::Duration};

fn arguments(raw: &[String]) -> Result<BTreeMap<String, String>, SemanticError> {
    let required = ["--database", "--file", "--endpoint", "--request-key", "--source", "--timeout-ms"];
    let usage = || SemanticError::incorrect("cli/submit-usage", "native-submit requires one complete saved transact request");
    if raw.first().map(String::as_str) != Some("transact") || raw.len() != 13 {
        return Err(usage());
    }
    let mut result = BTreeMap::new();
    for pair in raw[1..].chunks_exact(2) {
        if !required.contains(&pair[0].as_str()) || pair[1].is_empty()
            || result.insert(pair[0].clone(), pair[1].clone()).is_some() {
            return Err(usage());
        }
    }
    Ok(result)
}

fn run() -> Result<(), Box<dyn Error>> {
    let a = arguments(&std::env::args().skip(1).collect::<Vec<_>>())?;
    let text = std::fs::read_to_string(&a["--file"])?;
    if text.len() > 16 * 1024 * 1024 {
        return Err(SemanticError::incorrect("cli/submit-input-size", "EDN input exceeds 16 MiB").into());
    }
    // Match the stock CLI's EDN request representation. Do not rewrite forms,
    // regenerate IDs, supply a new instant, or change a saved basis guard.
    let request = TransactionRequest::from_edn(&a["--request-key"], &text,
        EntityRef::from_edn(&a["--source"])?)?;
    let connection = Connection::connect_configured(postgres_config_from_env()?, &a["--database"], 128)?;
    let commit = connection.transact_socket(&a["--endpoint"], request,
        Duration::from_millis(a["--timeout-ms"].parse()?))?;
    // Retain confirmation even if the local report cannot be opened/formatted.
    let mut fields = vec![
        (edn_keyword("edb", "committed"), EdnValue::Bool(true)),
        (edn_keyword("edb", "basis-t"), EdnValue::Long(commit.basis_t as i64)),
        (edn_keyword("edb", "replayed"), EdnValue::Bool(commit.replayed)),
        (edn_keyword("edb", "tx-hash"), EdnValue::String(commit.tx_hash.iter().map(|b| format!("{b:02x}")).collect())),
    ];
    let report = commit.report.and_then(|r| transaction_report_to_edn(
        r.db_before.basis_t(), r.db_after.basis_t(), &r.tx_data, &r.tempids));
    match report {
        Ok(EdnValue::Map(m)) => fields.extend(m),
        Err(e) => fields.push((edn_keyword("edb", "report-error"), EdnValue::String(e.code.into()))),
        _ => unreachable!("transaction report is a map"),
    }
    println!("{}", write_edn(&EdnValue::Map(fields))?);
    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            if let Some(e) = error.downcast_ref::<SemanticError>() {
                eprintln!("ERROR category={:?} code={}", e.category, e.code);
                if let Some(code) = e.details.get("remote_code") {
                    // Codes are safe diagnostic labels; arbitrary messages and
                    // other details can contain transaction data or credentials.
                    if code.len() <= 128 && code.chars().all(|c| c.is_ascii_alphanumeric() || "/._-".contains(c)) {
                        eprintln!("remote_code={code}");
                    }
                }
            } else {
                eprintln!("ERROR code=submit/local-error");
            }
            ExitCode::FAILURE
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn only_complete_saved_submission_is_accepted() {
        let a = ["transact", "--database", "math", "--file", "/saved.edn", "--endpoint", "/writer.sock",
            "--request-key", "saved-key", "--basis", "42", "--source", ":org/Math-Academy", "--timeout-ms", "180000"].map(String::from);
        assert_eq!(arguments(&a).unwrap()["--request-key"], "saved-key");
        let mut b = a.clone(); b[0] = "with".into(); assert!(arguments(&b).is_err());
        let mut b = a.clone(); b[3] = "--database".into(); assert!(arguments(&b).is_err());
        assert!(arguments(&a[..13]).is_err());
    }
}
