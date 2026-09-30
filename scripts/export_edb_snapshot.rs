//! Export domain facts from an offline EDB backup as lossless EDN-valued JSONL.
//!
//! Build this small standalone program against the local edb-core and serde_json
//! rlibs. It never opens a writer or changes the backup repository.

use edb_core::edn::write_edn;
use edb_core::edn_value::value_to_edn;
use edb_core::{BackupConnection, IndexOrder, Value};
use serde_json::{json, to_writer};
use std::collections::BTreeMap;
use std::env;
use std::error::Error;
use std::fs::{self, File};
use std::io::{BufWriter, Write};
use std::path::PathBuf;

fn uuid_string(value: u128) -> String {
    let hex = format!("{value:032x}");
    format!("{}-{}-{}-{}-{}", &hex[..8], &hex[8..12], &hex[12..16], &hex[16..20], &hex[20..])
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args_os().skip(1);
    let backup = PathBuf::from(args.next().ok_or("usage: export_edb_snapshot BACKUP_DIR OUTPUT.jsonl")?);
    let output = PathBuf::from(args.next().ok_or("usage: export_edb_snapshot BACKUP_DIR OUTPUT.jsonl")?);
    if args.next().is_some() {
        return Err("usage: export_edb_snapshot BACKUP_DIR OUTPUT.jsonl".into());
    }
    let manifest = output.with_extension("manifest.json");
    let staging = output.with_extension("jsonl.tmp");
    let connection = BackupConnection::open(&backup)?;
    let db = connection.db();
    let basis_t = db.basis_t();
    let datoms = db.collect_datoms(IndexOrder::Eavt)?;
    let mut writer = BufWriter::new(File::create(&staging)?);
    let mut counts = BTreeMap::<String, usize>::new();
    let mut exported = 0usize;
    let mut skipped_builtin = 0usize;
    for datom in datoms {
        let attr = db
            .ident(datom.attribute as u64)
            .ok_or_else(|| format!("attribute {} has no ident", datom.attribute))?;
        let name = attr.qualified_name();
        if attr.namespace.as_deref().is_some_and(|ns| ns == "db" || ns.starts_with("db.")) {
            skipped_builtin += 1;
            continue;
        }
        let value_edn = write_edn(&value_to_edn(&datom.value)?)?;
        let ref_eid = match &datom.value {
            Value::Ref(target) => Some(*target),
            _ => None,
        };
        let ref_ident = ref_eid.and_then(|eid| db.ident(eid)).map(|ident| ident.qualified_name());
        let raw_string = match &datom.value {
            Value::String(value) => Some(value.as_str()),
            _ => None,
        };
        let uuid = match &datom.value {
            Value::Uuid(value) => Some(uuid_string(*value)),
            _ => None,
        };
        to_writer(
            &mut writer,
            &json!({
                "e": datom.entity,
                "a": name,
                "value_edn": value_edn,
                "ref_eid": ref_eid,
                "ref_ident": ref_ident,
                "raw_string": raw_string,
                "uuid": uuid,
            }),
        )?;
        writer.write_all(b"\n")?;
        *counts.entry(name).or_default() += 1;
        exported += 1;
    }
    writer.flush()?;
    fs::rename(staging, &output)?;
    fs::write(
        &manifest,
        serde_json::to_vec_pretty(&json!({
            "backup": backup,
            "basis_t": basis_t,
            "domain_datoms": exported,
            "skipped_builtin_datoms": skipped_builtin,
            "attribute_counts": counts,
        }))?,
    )?;
    println!("exported {exported} domain datoms at basis {basis_t} to {}", output.display());
    Ok(())
}
