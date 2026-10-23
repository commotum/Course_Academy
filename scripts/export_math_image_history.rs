//! Read retained history for an explicit entity set at the audit's exact basis.
//! No writer is opened; output is a JSONL stream of string/keyword assertions.
use edb_core::{Connection, IndexPrefix, Value, postgres_config_from_env};
use serde_json::json;
use std::{error::Error, fs::File, io::{BufWriter, Write}, collections::BTreeMap};

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<_> = std::env::args().collect();
    if args.len() != 6 { return Err("usage: export_math_image_history DATABASE BASIS IDS.json OUTPUT.jsonl".into()); }
    let ids: Vec<u64> = serde_json::from_reader(File::open(&args[4])?)?;
    let basis: u64 = args[3].parse()?;
    let conn = Connection::connect_configured_with_cache_limits(postgres_config_from_env()?, args[1].clone(), 2048, 64 * 1024 * 1024)?;
    // args[2] is the literal --as-of, making accidental argument swaps fail.
    if args[2] != "--as-of" { return Err("--as-of is required".into()); }
    let db = conn.sync()?.as_of(basis);
    let history = db.clone().history();
    let mut out = BufWriter::new(File::create(&args[5])?);
    let mut count = 0;
    let mut transactions = BTreeMap::new();
    for eid in &ids {
        for d in history.collect_datoms_with_prefix(&IndexPrefix::Eavt {entity:*eid,attribute:None,value:None})? {
            let a = db.schema().attribute(d.attribute)?.ident.qualified_name();
            let v = match d.value {Value::String(v)=>json!(v), Value::Keyword(v)=>json!(v.qualified_name()), _=>continue};
            serde_json::to_writer(&mut out,&json!({"e":d.entity,"a":a,"v":v,"tx":d.tx,"t":edb_core::tx_to_t(d.tx)?,"source":d.source,"added":d.added}))?;
            out.write_all(b"\n")?;
            transactions.insert(d.tx, ());
            count += 1;
        }
    }
    out.flush()?;
    let attr = db.schema().resolve_ident(&edb_core::Keyword::new("db","txInstant")).ok_or("missing txInstant")?;
    let mut instants = BTreeMap::new();
    for tx in transactions.keys() {
        for d in db.collect_datoms_with_prefix(&IndexPrefix::Eavt {entity:*tx,attribute:Some(attr),value:None})? {
            if let Value::Instant(at)=d.value {instants.insert(*tx,at);}
        }
    }
    std::fs::write(std::path::Path::new(&args[5]).with_extension("transactions.json"),serde_json::to_vec_pretty(&instants)?)?;
    println!("Read {count} retained historical facts for {} entities through basis {basis}",ids.len());
    Ok(())
}
