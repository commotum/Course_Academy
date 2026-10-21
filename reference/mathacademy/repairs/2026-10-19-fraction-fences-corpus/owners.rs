//! Resolve a bounded set of candidate answer owners from one immutable value.
use edb_core::{IndexOrder, Peer, Value, postgres_config_from_env};
use serde_json::{Value as Json, json};
use std::{collections::{BTreeMap,BTreeSet},error::Error,fs,path::PathBuf};
fn main()->Result<(),Box<dyn Error>>{
    let args:Vec<_>=std::env::args().skip(1).collect();let dir=PathBuf::from(&args[0]);let basis:u64=args[1].parse()?;
    let candidates:Vec<Json>=serde_json::from_str(&fs::read_to_string(dir.join("candidate-changes.json"))?)?;
    let wanted:BTreeSet<u64>=candidates.iter().filter(|c|c["attribute"].as_str().unwrap().starts_with(":answer/")).map(|c|c["entity"].as_u64().unwrap()).collect();
    let db=Peer::connect_configured(&postgres_config_from_env()?,"math",256)?.db().as_of(basis);
    let mut types=BTreeMap::new();let mut memberships=BTreeSet::new();let mut questions:BTreeMap<u64,BTreeSet<u64>>=BTreeMap::new();
    for d in db.collect_datoms(IndexOrder::Eavt)?{
        let Some(attr)=db.ident(d.attribute as u64) else{continue};let Value::Ref(target)=d.value else{continue};
        match attr.qualified_name().as_str(){
            "answer/type" if wanted.contains(&d.entity)=>{types.insert(d.entity,target);},
            "answer-field/choices"|"answer-field/correct" if wanted.contains(&target)=>{memberships.insert((target,d.entity));},
            "question/answer-fields"=>{questions.entry(target).or_default().insert(d.entity);},
            _=>{}
        }
    }
    let types:Vec<_>=types.into_iter().map(|(e,t)|json!([{":db/id":e,":answer/type":{":db/id":t,":db/ident":format!(":{}",db.ident(t).unwrap().qualified_name())}}])).collect();
    let owners:Vec<_>=memberships.into_iter().flat_map(|(a,f)|questions.get(&f).into_iter().flatten().map(move|q|[a,*q,f])).collect();
    fs::write(dir.join("answer-types.json"),serde_json::to_vec_pretty(&types)?)?;fs::write(dir.join("answer-owners.json"),serde_json::to_vec_pretty(&owners)?)?;
    println!("Resolved {} candidate answer types and {} owner links at basis {basis}",types.len(),owners.len());Ok(())
}
