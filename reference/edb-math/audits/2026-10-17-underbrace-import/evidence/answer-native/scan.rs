//! Read-only exhaustive current :answer/value census at a pinned EDB basis.
//! Uses streaming AEVT prefix iteration to avoid Datalog materialization limits.
use edb_core::edn::{EdnValue, write_edn};
use edb_core::{Connection, IndexPrefix, Keyword, Value, postgres_config_from_env};
use std::{collections::BTreeSet, error::Error, fs, path::Path};

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.len()!=2 { return Err("usage: scan DIRECTORY AS_OF_BASIS".into()); }
    let dir=Path::new(&args[0]); let pinned:u64=args[1].parse()?;
    let conn=Connection::connect_configured(postgres_config_from_env()?, "math", 256)?;
    let current=conn.db();
    if current.basis_t()<pinned {return Err("Current basis is older than requested pinned basis".into());}
    let current_basis=current.basis_t();
    let db=current.as_of(pinned);
    let aid=u32::try_from(db.entid(&Keyword::new("answer","value")).ok_or("No :answer/value attribute")?)?;
    if aid!=1080 {return Err("Unexpected attribute ID".into());}
    let needles=["⏟","⏞","︷","︸",r"\underbrace",r"\overbrace"];
    let prefix=IndexPrefix::Aevt {attribute:aid,entity:None,value:None};
    let mut count=0u64;let mut bytes=0u64;let mut entities=BTreeSet::new();let mut matched=Vec::new();
    let mut counts=[0u64;6];let mut max_bytes=0u64;
    for row in db.prefix_cursor(&prefix)? {
        let d=row?;
        if d.attribute!=aid || !d.added {return Err("Unexpected visible datom in attribute prefix".into());}
        let Value::String(value)=d.value else{return Err("Nonstring :answer/value".into());};
        count+=1;entities.insert(d.entity);bytes+=value.len() as u64;max_bytes=max_bytes.max(value.len() as u64);
        let mut hit=false;
        for (i,needle) in needles.iter().enumerate() {if value.contains(needle) {counts[i]+=1;hit=true;}}
        if hit {matched.push(EdnValue::Vector(vec![EdnValue::Long(d.entity as i64),EdnValue::String(value),EdnValue::Long(d.tx as i64),EdnValue::Long(d.source as i64)]));}
    }
    fs::write(dir.join("matches.edn"),write_edn(&EdnValue::Vector(matched.clone()))?+"\n")?;
    let stats=format!("{{\"database\":\"math\",\"captured_current_basis\":{current_basis},\"as_of_basis\":{pinned},\"attribute\":\":answer/value\",\"attribute_id\":{aid},\"current_datoms\":{count},\"distinct_entities\":{},\"utf8_value_bytes\":{bytes},\"max_value_bytes\":{max_bytes},\"matching_rows\":{},\"needle_match_counts\":{:?},\"completed_to_end\":true,\"database_writes\":0}}\n",entities.len(),matched.len(),counts);
    fs::write(dir.join("stats.json"),&stats)?;
    print!("{stats}");Ok(())
}
