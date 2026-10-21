//! One-connection, read-only fixed-basis Pulls and indexed incoming-use census.
use edb_core::{Connection,DatabaseValue,IndexPrefix,Keyword,Value,postgres_config_from_env};
use edb_core::edn::{EdnValue,read_edn,write_edn};
use edb_core::edn_pull::parse_pull_edn;
use edb_core::edn_value::query_value_to_edn;
use std::{collections::BTreeSet,error::Error,fs,path::Path};

fn references(db:&DatabaseValue,entity:u64,attribute:u32)->Result<Vec<u64>,Box<dyn Error>> {
    let mut refs=vec![];
    for row in db.prefix_cursor(&IndexPrefix::Eavt{entity,attribute:Some(attribute),value:None})? {
        if let Value::Ref(id)=row?.value {refs.push(id);}
    }
    Ok(refs)
}

fn main()->Result<(),Box<dyn Error>> {
    let args:Vec<_>=std::env::args().skip(1).collect();
    if args.len()!=2 {return Err("usage: refresh DIRECTORY AS_OF_BASIS".into())}
    let directory=Path::new(&args[0]);let pinned:u64=args[1].parse()?;
    let connection=Connection::connect_configured(postgres_config_from_env()?,"math",256)?;
    let current=connection.db();let connection_basis=current.basis_t();if connection_basis<pinned{return Err("Requested basis is unavailable".into())}
    let db=current.as_of(pinned);
    let EdnValue::Vector(groups)=read_edn(&fs::read_to_string(directory.join("native-pulls.edn"))?)? else {return Err("native-pulls.edn must be vector".into())};
    let mut qids=BTreeSet::new();let mut group_counts=vec![];
    for group in groups {
        let EdnValue::Vector(parts)=group else {return Err("Pull group must be vector".into())};
        let [EdnValue::String(name),EdnValue::String(pattern),EdnValue::Vector(ids)]=parts.as_slice() else {return Err("Pull group must be [name pattern ids]".into())};
        if name.is_empty() || !name.chars().all(|c|c.is_ascii_alphanumeric()||c=='-'){return Err("Unsafe Pull output name".into())}
        let pattern=parse_pull_edn(pattern)?;let mut rows=vec![];
        for id in ids {
            let EdnValue::Long(id)=id else{return Err("Entity ID must be integer".into())};let id=u64::try_from(*id)?;
            let pulled=query_value_to_edn(&db.pull(&pattern,id)?)?;
            if let EdnValue::Map(fields)=&pulled {
                if fields.iter().any(|(key,_)|matches!(key,EdnValue::Keyword(k) if k==&Keyword::new("question","id"))){qids.insert(id);}
            }
            rows.push(pulled);
        }
        fs::write(directory.join(format!("capture-{name}.edn")),write_edn(&EdnValue::Vector(rows))?+"\n")?;
        group_counts.push(format!("\"{name}\":{}",ids.len()));
        println!("Captured {name}: {}",ids.len());
    }
    let question_fields=db.entid(&Keyword::new("question","answer-fields")).ok_or("Missing question/answer-fields")? as u32;
    let field_choices=db.entid(&Keyword::new("answer-field","choices")).ok_or("Missing answer-field/choices")? as u32;
    let mut targets=qids.clone();let mut field_count=0;let mut answer_count=0;
    for q in &qids {
        for field in references(&db,*q,question_fields)? {
            if targets.insert(field){field_count+=1;}
            for answer in references(&db,field,field_choices)? {if targets.insert(answer){answer_count+=1;}}
        }
    }
    let mut incoming=vec![];
    for target in &targets {
        for row in db.prefix_cursor(&IndexPrefix::Vaet{value:Value::Ref(*target),attribute:None,entity:None})? {
            let d=row?;
            // The third cell is an entity ID, known to be reference-typed by VAET.
            incoming.push(EdnValue::Vector(vec![EdnValue::Long(d.entity as i64),EdnValue::Long(d.attribute as i64),
                EdnValue::Long(*target as i64),EdnValue::Long(d.tx as i64),EdnValue::Long(d.source as i64),EdnValue::Bool(d.added)]));
        }
    }
    let count=incoming.len();
    fs::write(directory.join("incoming.edn"),write_edn(&EdnValue::Vector(incoming))?+"\n")?;
    fs::write(directory.join("incoming-targets.edn"),write_edn(&EdnValue::Vector(targets.into_iter().map(|v|EdnValue::Long(v as i64)).collect()))?+"\n")?;
    fs::write(directory.join("refresh-complete.json"),format!("{{\"basis\":{pinned},\"connection_basis\":{connection_basis},\"groups\":{{{}}},\"questions\":{},\"fields\":{field_count},\"answers\":{answer_count},\"incoming_datoms\":{count},\"completed_to_end\":true,\"database_writes\":0}}\n",group_counts.join(","),qids.len()))?;
    println!("Incoming references: {count}; no database writes");Ok(())
}
