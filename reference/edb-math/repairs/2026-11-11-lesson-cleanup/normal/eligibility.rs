use course_academy_engine::{learning,schema::{EntitySnapshot,Record}};
use serde_json::{Value,json};
use std::{collections::BTreeMap,fs,error::Error};
fn main()->Result<(),Box<dyn Error>>{
 let a:Vec<_>=std::env::args().skip(1).collect();let input:Value=serde_json::from_slice(&fs::read(&a[0])?)?;
 let entities:BTreeMap<u64,Record>=input["entities"].as_object().unwrap().iter().map(|(k,v)|(k.parse().unwrap(),v.as_object().unwrap().clone())).collect();
 let basis=input["basis"].as_u64().unwrap();let snapshot=EntitySnapshot::new(entities,basis)?;let mut rows=vec![];
 for q in input["questions"].as_array().unwrap(){let id=q.as_u64().unwrap();let result=learning::validate_practice_question(&snapshot,id);rows.push(json!({"entity":id,"eligible":result.is_ok(),"reason":result.err()}));}
 fs::write(&a[1],serde_json::to_string_pretty(&json!({"basis":basis,"database_writes":0,"entry_point":"learning::validate_practice_question","questions":rows}))?+"\n")?;Ok(())
}
