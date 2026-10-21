//! Read-only exhaustive literal brace-accent history census through a pinned basis.
use edb_core::edn::{EdnValue, write_edn};
use edb_core::{Connection, IndexPrefix, Keyword, Value, postgres_config_from_env};
use std::{collections::BTreeSet, error::Error, fs, path::Path};

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.len()!=2 {return Err("usage: history DIRECTORY AS_OF_BASIS".into());}
    let dir=Path::new(&args[0]);let pinned:u64=args[1].parse()?;
    let conn=Connection::connect_configured(postgres_config_from_env()?,"math",256)?;
    let current=conn.db();let basis=current.basis_t();
    if basis<pinned {return Err("Current basis older than requested pinned basis".into());}
    let db=current.history().as_of(pinned);
    let needles=["⏟","⏞","︷","︸"];
    for (ns,name,aid) in [("tutorial","content",1064u32),("question","problem",1071),("question","worked-solution",1074),("answer","value",1080),("answer","feedback",1081),("multistep","context",1085)] {
        if db.entid(&Keyword::new(ns,name))!=Some(aid as u64) {return Err("Unexpected attribute identity".into());}
        let mut count=0u64;let mut bytes=0u64;let mut entities=BTreeSet::new();let mut matched=Vec::new();let mut counts=[0u64;4];let mut adds=0u64;let mut retracts=0u64;let mut matching_entities=BTreeSet::new();
        for row in db.prefix_cursor(&IndexPrefix::Aevt{attribute:aid,entity:None,value:None})? {
            let d=row?;
            if d.attribute!=aid {return Err("Unexpected visible datom in attribute prefix".into());}
            let Value::String(value)=d.value else{return Err("Nonstring content attribute".into());};
            count+=1;bytes+=value.len() as u64;entities.insert(d.entity);
            let mut hit=false;
            for (i,needle) in needles.iter().enumerate(){if value.contains(needle){counts[i]+=1;hit=true;}}
            if hit {
                if d.added {adds+=1;}else{retracts+=1;}
                matching_entities.insert(d.entity);
                matched.push(EdnValue::Vector(vec![EdnValue::Long(d.entity as i64),EdnValue::Long(aid as i64),EdnValue::String(value),EdnValue::Long(d.tx as i64),EdnValue::Long(d.source as i64),EdnValue::Bool(d.added)]));
            }
        }
        let stem=format!("history-{ns}-{name}");
        fs::write(dir.join(format!("{stem}.edn")),write_edn(&EdnValue::Vector(matched.clone()))?+"\n")?;
        let stats=format!("{{\"database\":\"math\",\"captured_current_basis\":{basis},\"as_of_basis\":{pinned},\"attribute\":\":{ns}/{name}\",\"attribute_id\":{aid},\"history_datoms\":{count},\"distinct_entities\":{},\"utf8_value_bytes\":{bytes},\"matching_rows\":{},\"matching_entities\":{},\"matching_adds\":{adds},\"matching_retracts\":{retracts},\"needle_match_counts\":{:?},\"completed_to_end\":true,\"database_writes\":0}}\n",entities.len(),matched.len(),matching_entities.len(),counts);
        fs::write(dir.join(format!("{stem}-stats.json")),&stats)?;print!("{stats}");
    }
    Ok(())
}
