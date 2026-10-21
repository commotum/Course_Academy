//! Read-only, fixed-basis Pull groups. Never opens or submits to a writer.
use edb_core::edn::{EdnValue, read_edn, write_edn};
use edb_core::edn_pull::parse_pull_edn;
use edb_core::edn_value::query_value_to_edn;
use edb_core::{Peer, postgres_config_from_env};
use std::{error::Error, fs, path::Path};
fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.len() != 2 { return Err("usage: native_read DIRECTORY BASIS".into()); }
    let dir = Path::new(&args[0]);
    let basis: u64 = args[1].parse()?;
    let db = Peer::connect_configured(&postgres_config_from_env()?, "math", 256)?.db().as_of(basis);
    let EdnValue::Vector(groups) = read_edn(&fs::read_to_string(dir.join("native-pulls.edn"))?)? else { return Err("expected groups".into()); };
    for group in groups {
        let EdnValue::Vector(parts) = group else { return Err("expected group".into()); };
        let [EdnValue::String(name), EdnValue::String(pattern), EdnValue::Vector(ids)] = parts.as_slice() else { return Err("bad group".into()); };
        if name.is_empty() || !name.chars().all(|c| c.is_ascii_alphanumeric() || c == '-') { return Err("bad output name".into()); }
        let pattern = parse_pull_edn(pattern)?;
        let mut values = Vec::new();
        for id in ids {
            let EdnValue::Long(id) = id else { return Err("expected entity id".into()); };
            values.push(query_value_to_edn(&db.pull(&pattern, u64::try_from(*id)?)?)?);
        }
        fs::write(dir.join(format!("{name}.edn")), write_edn(&EdnValue::Vector(values))? + "\n")?;
        println!("{name}: {} entities at basis {basis}", ids.len());
    }
    Ok(())
}
