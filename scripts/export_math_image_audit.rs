//! Read-only export for the math-image import audit. Never connects to a writer.
//! Build against the application's EDB and serde_json release libraries.
use edb_core::{Connection, IndexOrder, Value, postgres_config_from_env};
use serde_json::json;
use std::{collections::BTreeMap, error::Error, fs::File, io::{BufWriter, Write}};

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<_> = std::env::args().collect();
    if args.len() != 3 { return Err("usage: export_math_image_audit DATABASE OUTPUT.jsonl".into()); }
    let conn = Connection::connect_configured_with_cache_limits(
        postgres_config_from_env()?, args[1].clone(), 2048, 64 * 1024 * 1024)?;
    let db = conn.sync()?;
    let mut out = BufWriter::new(File::create(&args[2])?);
    let mut counts = BTreeMap::<String, usize>::new();
    let mut exported = 0usize;
    for d in db.collect_datoms(IndexOrder::Eavt)? {
        let a = db.schema().attribute(d.attribute)?.ident.qualified_name();
        if (a.starts_with("db/") || a.starts_with("db.")) && a != "db/ident" { continue; }
        *counts.entry(a.clone()).or_default() += 1;
        // Every domain string is examined, including answer values, titles,
        // feedback and newer content types. References retain ownership context.
        let value = match d.value {
            Value::String(v) | Value::Uri(v) => json!(v),
            Value::Ref(v) => json!(v),
            Value::Keyword(v) => json!(format!(":{}", v.qualified_name())),
            Value::Long(v) => json!(v),
            Value::Uuid(v) => json!(format!("{:08x}-{:04x}-{:04x}-{:04x}-{:012x}",
                v >> 96, (v >> 80) & 0xffff, (v >> 64) & 0xffff, (v >> 48) & 0xffff, v & 0xffffffffffff)),
            _ => continue,
        };
        serde_json::to_writer(&mut out, &json!({"e":d.entity,"a":a,"v":value,
            "tx":d.tx,"t":edb_core::tx_to_t(d.tx)?,"source":d.source}))?;
        out.write_all(b"\n")?;
        exported += 1;
    }
    out.flush()?;
    let manifest = std::path::Path::new(&args[2]).with_extension("manifest.json");
    std::fs::write(manifest, serde_json::to_vec_pretty(&json!({
        "database":args[1],"basis_t":db.basis_t(),"exported_datoms":exported,
        "domain_attribute_counts":counts,"export":"current strings, refs, UUIDs, longs and keywords"}))?)?;
    println!("Exported {exported} current facts at basis {}", db.basis_t());
    Ok(())
}
