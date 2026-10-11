//! Read-only chained speculation. There are no durable-write API calls.
//! Usage: sequential-preview DATABASE EXPECTED_BASIS OUTDIR SOURCE FILE [SOURCE FILE ...]
//!        [--repeat-immediate] [--query QUERY.edn INPUTS.edn] [--pull PATTERN.edn IDENTIFIERS.edn]
//! Immediate repeats branch from each stage's db-after, then are discarded before the next stage.
//! Query inputs are non-source :in arguments. Only the default $ database source is supported.
//! Pull identifiers are an EDN vector. DATABASE=:memory uses an in-memory bootstrap for smoke checks.
use edb_core::edn::{read_edn, write_edn, EdnValue};
use edb_core::edn_pull::{entity_identifier_from_edn, parse_pull_edn};
use edb_core::edn_query::{parse_query_edn, EdnQueryArgument, EdnQueryInput};
use edb_core::edn_value::{edn_keyword, query_value_to_edn, transaction_report_to_edn};
use edb_core::{Database, DatabaseValue, EntityRef, Peer, PullControl, QueryControl,
    QuerySourceValue, SpeculativeTransactionReport, DB_TX_INSTANT, postgres_config_from_env};
use std::{error::Error, fs, path::Path, time::{Duration, SystemTime, UNIX_EPOCH}};
type Result<T> = std::result::Result<T, Box<dyn Error>>;

struct Step { source: String, file: String, text: String }

fn read(path: &str) -> Result<String> {
    if fs::metadata(path)?.len() > 16 * 1024 * 1024 { return Err("Input exceeds 16 MiB".into()); }
    Ok(fs::read_to_string(path)?)
}
fn save(out: &Path, name: &str, value: &EdnValue) -> Result<()> {
    fs::write(out.join(name), format!("{}\n", write_edn(value)?))?;
    Ok(())
}
fn k(name: &str) -> EdnValue { edn_keyword("preview", name) }
fn n(value: u64) -> Result<EdnValue> { Ok(EdnValue::Long(i64::try_from(value)?)) }

fn save_report(out: &Path, label: &str, report: &SpeculativeTransactionReport,
               source: &str) -> Result<EdnValue> {
    let identifier = entity_identifier_from_edn(&read_edn(source)?)?;
    let source_id = report.db_after.resolve_entity_identifier(&identifier)?
        .ok_or("Transaction source is absent from speculative db-after")?;
    if report.tx_data.iter().any(|d| d.source != source_id) {
        return Err("Speculative datom has unexpected attribution".into());
    }
    let instants = report.tx_data.iter().filter(|d| d.attribute == DB_TX_INSTANT as u32).count();
    if instants != 1 { return Err("Expected exactly one transaction instant".into()); }
    let material = report.tx_data.len() - instants;
    let mut value = transaction_report_to_edn(report.db_before.basis_t(),
        report.db_after.basis_t(), &report.tx_data, &report.tempids)?;
    let EdnValue::Map(fields) = &mut value else { unreachable!() };
    fields.extend([
        (edn_keyword("edb", "committed"), EdnValue::Bool(false)),
        (edn_keyword("edb", "speculative"), EdnValue::Bool(true)),
    ]);
    save(out, &format!("{label}-preview.edn"), &value)?;
    println!("{label}: speculative {} -> {}; {} datoms ({} material); source {source} ({source_id})",
        report.db_before.basis_t(), report.db_after.basis_t(), report.tx_data.len(), material);
    Ok(EdnValue::Map(vec![
        (k("label"), EdnValue::String(label.into())),
        (k("source"), read_edn(source)?),
        (k("source-id"), n(source_id)?),
        (k("basis-before"), n(report.db_before.basis_t())?),
        (k("basis-after"), n(report.db_after.basis_t())?),
        (k("datoms"), n(report.tx_data.len() as u64)?),
        (k("material-datoms"), n(material as u64)?),
    ]))
}

fn query(db: &DatabaseValue, query_file: &str, inputs_file: &str) -> Result<EdnValue> {
    let query = parse_query_edn(&read(query_file)?)?;
    let EdnValue::Vector(inputs) = read_edn(&read(inputs_file)?)? else {
        return Err("Query inputs must be a vector".into());
    };
    let mut inputs = inputs.into_iter();
    let mut arguments = Vec::new();
    for input in &query.inputs {
        match input {
            EdnQueryInput::Source(name) if name == "$" => arguments.push(
                EdnQueryArgument::Source(QuerySourceValue::Database(db.clone()))),
            EdnQueryInput::Source(_) => return Err("Only the default $ query source is supported".into()),
            _ => arguments.push(EdnQueryArgument::Data(inputs.next().ok_or("Too few query inputs")?)),
        }
    }
    if inputs.next().is_some() { return Err("Too many query inputs".into()); }
    let bound = query.bind(&arguments)?;
    let control = QueryControl { timeout: Some(Duration::from_secs(30)), ..Default::default() };
    let report = bound.execute(&control, None)?;
    Ok(bound.result_to_edn(&report.result)?)
}
fn pulls(db: &DatabaseValue, pattern_file: &str, identifiers_file: &str) -> Result<EdnValue> {
    let pattern = parse_pull_edn(&read(pattern_file)?)?;
    let EdnValue::Vector(identifiers) = read_edn(&read(identifiers_file)?)? else {
        return Err("Pull identifiers must be a vector".into());
    };
    let control = PullControl { max_depth: 32, max_entities: 100_000, ..Default::default() };
    let mut results = Vec::new();
    for raw in identifiers {
        let identifier = entity_identifier_from_edn(&raw)?;
        if db.resolve_entity_identifier(&identifier)?.is_none() {
            return Err(format!("Expected pull entity absent: {}", write_edn(&raw)?).into());
        }
        let result = db.pull_with_control(&pattern, identifier, &control)?;
        results.push(EdnValue::Vector(vec![raw, query_value_to_edn(&result)?]));
    }
    Ok(EdnValue::Vector(results))
}

fn run() -> Result<()> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.len() < 5 { return Err("Usage: sequential-preview DATABASE EXPECTED_BASIS OUTDIR SOURCE FILE [SOURCE FILE ...] [--repeat-immediate] [--query QUERY.edn INPUTS.edn] [--pull PATTERN.edn IDENTIFIERS.edn]".into()); }
    let expected: u64 = args[1].parse()?;
    let out = Path::new(&args[2]);
    let mut steps = Vec::new();
    let mut queries = Vec::new();
    let mut pull_specs = Vec::new();
    let mut repeat_immediate = false;
    let mut i = 3;
    while i < args.len() {
        match args[i].as_str() {
            "--repeat-immediate" => {
                repeat_immediate = true;
                i += 1;
            }
            "--query" | "--pull" => {
                if i + 2 >= args.len() { return Err("Read check requires two file paths".into()); }
                let pair = (args[i + 1].clone(), args[i + 2].clone());
                read_edn(&read(&pair.0)?)?;
                read_edn(&read(&pair.1)?)?;
                if args[i] == "--query" { queries.push(pair); } else { pull_specs.push(pair); }
                i += 3;
            }
            source => {
                if i + 1 >= args.len() { return Err("Each source needs a transaction file".into()); }
                EntityRef::from_edn(source)?;
                let file = args[i + 1].clone();
                let text = read(&file)?;
                edb_core::edn_transaction::read_edn_transaction(&text)?;
                steps.push(Step { source: source.into(), file, text });
                i += 2;
            }
        }
    }
    if steps.is_empty() { return Err("At least one speculative step is required".into()); }
    // Peer and with_edn have no writer startup/submission. No endpoint or token is accepted.
    let config = if args[0] == ":memory" { None } else { Some(postgres_config_from_env()?) };
    let mut db = match &config {
        Some(config) => Peer::connect_configured(config, &args[0], 128)?.db(),
        None => Database::bootstrap()?.database_value(),
    };
    if db.basis_t() != expected {
        return Err(format!("Stale preparation basis: expected {expected}, found {}", db.basis_t()).into());
    }
    let captured = db.clone();
    let now = i64::try_from(SystemTime::now().duration_since(UNIX_EPOCH)?.as_millis())?;
    let instant = now.max(db.last_tx_instant().unwrap_or(now));
    fs::create_dir_all(out)?;
    let mut summaries = Vec::new();
    let mut repeats = Vec::new();
    for (i, step) in steps.iter().enumerate() {
        let report = db.with_edn(&step.text, instant, EntityRef::from_edn(&step.source)?)?;
        let mut summary = save_report(out, &format!("stage{}", i + 1), &report, &step.source)?;
        let EdnValue::Map(fields) = &mut summary else { unreachable!() };
        fields.push((k("file"), EdnValue::String(step.file.clone())));
        summaries.push(summary);
        if repeat_immediate {
            let repeated = report.db_after.with_edn(
                &step.text, instant, EntityRef::from_edn(&step.source)?)?;
            repeats.push(save_report(out, &format!("repeat-stage{}", i + 1), &repeated, &step.source)?);
            if repeated.tx_data.iter().any(|d| d.attribute != DB_TX_INSTANT as u32) {
                return Err(format!("Immediate repeat stage {} produced material datoms; inspect repeat report", i + 1).into());
            }
        }
        // Continue the original chain; a repeat is an independent discarded branch.
        db = report.db_after;
    }
    let final_basis = db.basis_t();
    let mut query_results = Vec::new();
    for (i, (q, inputs)) in queries.iter().enumerate() {
        let result = query(&db, q, inputs)?;
        save(out, &format!("final-query{}.edn", i + 1), &result)?;
        query_results.push(result);
    }
    let mut pull_results = Vec::new();
    for (i, (p, identifiers)) in pull_specs.iter().enumerate() {
        let result = pulls(&db, p, identifiers)?;
        save(out, &format!("final-pull{}.edn", i + 1), &result)?;
        pull_results.push(result);
    }
    // Default mode repeats all forms on the final branch. Immediate mode has already
    // checked each stage before any later revision could supersede its assertions.
    if !repeat_immediate {
        for (i, step) in steps.iter().enumerate() {
            let report = db.with_edn(&step.text, instant, EntityRef::from_edn(&step.source)?)?;
            repeats.push(save_report(out, &format!("repeat-stage{}", i + 1), &report, &step.source)?);
            if report.tx_data.iter().any(|d| d.attribute != DB_TX_INSTANT as u32) {
                return Err(format!("Repeat stage {} produced material datoms; inspect repeat report", i + 1).into());
            }
            db = report.db_after;
        }
        for ((q, inputs), original) in queries.iter().zip(query_results) {
            if query(&db, q, inputs)? != original { return Err("Final query changed after repeat".into()); }
        }
        for ((p, identifiers), original) in pull_specs.iter().zip(pull_results) {
            if pulls(&db, p, identifiers)? != original { return Err("Final pull changed after repeat".into()); }
        }
    }
    let live_after = match &config {
        Some(config) => Peer::connect_configured(config, &args[0], 128)?.db().basis_t(),
        None => captured.basis_t(),
    };
    save(out, "manifest.edn", &EdnValue::Map(vec![
        (k("database"), EdnValue::String(args[0].clone())),
        (k("durable-basis-before"), n(expected)?),
        (k("durable-basis-after"), n(live_after)?),
        (k("speculative-basis-after"), n(final_basis)?),
        (k("tx-instant-millis"), EdnValue::Long(instant)),
        (k("repeat-mode"), EdnValue::String(if repeat_immediate { "immediate" } else { "final-chain" }.into())),
        (k("stages"), EdnValue::Vector(summaries)),
        (k("repeats"), EdnValue::Vector(repeats)),
        (k("queries-checked"), n(queries.len() as u64)?),
        (k("pulls-checked"), n(pull_specs.len() as u64)?),
        (k("database-writes"), EdnValue::Long(0)),
        (edn_keyword("edb", "committed"), EdnValue::Bool(false)),
        (edn_keyword("edb", "speculative"), EdnValue::Bool(true)),
    ]))?;
    if live_after != expected {
        return Err(format!("Concurrent durable change: {expected} -> {live_after}; refresh preview before submission").into());
    }
    println!("Live basis unchanged at {live_after}; {} stages validated; repeats produced no material datoms; database writes: 0", steps.len());
    Ok(())
}
fn main() {
    if let Err(error) = run() { eprintln!("Read-only speculative preview failed: {error}"); std::process::exit(1); }
}
