//! Bounded-output identity inventory at one basis; no writer connection.
use edb_core::{Connection, IndexOrder, Value, postgres_config_from_env};
use edb_core::edn::{write_edn};
use edb_core::edn_value::value_to_edn;
use serde_json::{json, Value as Json};
use std::{collections::BTreeMap, error::Error, fs};

fn uuid(v:u128)->String {format!("{:08x}-{:04x}-{:04x}-{:04x}-{:012x}",v>>96,(v>>80)&0xffff,(v>>64)&0xffff,(v>>48)&0xffff,v&0xffffffffffff)}
fn main()->Result<(),Box<dyn Error>> {
 let args:Vec<_>=std::env::args().collect();if args.len()!=4{return Err("DATABASE BASIS OUTPUT-DIR".into())}
 let basis=args[2].parse::<u64>()?;
 let conn=Connection::connect_configured(postgres_config_from_env()?,&args[1],128)?;
 let db=conn.db().as_of(basis);let mut rows:BTreeMap<u64,serde_json::Map<String,Json>>=BTreeMap::new();let mut owners:BTreeMap<u64,Vec<u64>>=BTreeMap::new();
 for d in db.collect_datoms(IndexOrder::Eavt)? {
  let a=db.ident(d.attribute as u64).ok_or("attribute has no ident")?.qualified_name();
  if a=="knowledge-point/questions" {if let Value::Ref(q)=d.value {owners.entry(q).or_default().push(d.entity);}continue}
  if !["question/id","question/math-academy-id","question/retired"].contains(&a.as_str()){continue}
  let value=match &d.value {Value::Uuid(v)=>json!(uuid(*v)),Value::String(v)=>json!(v),_=>json!(write_edn(&value_to_edn(&d.value)?)?=="true")};
  rows.entry(d.entity).or_default().insert(format!(":{a}"),value);
 }
 let total=rows.values().filter(|r|r.contains_key(":question/id")).count();let mut generated=vec![];
 for (eid,mut row) in rows {if !row.contains_key(":question/id")||row.contains_key(":question/math-academy-id"){continue}row.insert(":db/id".into(),json!(eid));row.insert(":knowledge-point/_questions".into(),json!(owners.remove(&eid).unwrap_or_default().into_iter().map(|k|json!({":db/id":k})).collect::<Vec<_>>()));generated.push(row);}
 fs::write(format!("{}/generated-questions.json",args[3]),serde_json::to_vec_pretty(&generated)?)?;
 fs::write(format!("{}/generated-identity-coverage.json",args[3]),serde_json::to_vec_pretty(&json!({"basis":basis,"all_questions":total,"generated_questions":generated.len(),"complete_native_snapshot":true}))?)?;
 println!("{} questions, {} without imported source IDs at T{}",total,generated.len(),basis);Ok(())
}
