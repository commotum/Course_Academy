//! Read-only check of the captured, scoped inventory through the actual pool.
use course_academy_engine::{assessment_sampling, schema::{EntitySnapshot, Record}};
use serde_json::{Value,json};
use std::{collections::{BTreeMap,BTreeSet},error::Error,fs};
fn main()->Result<(),Box<dyn Error>> {
 let args:Vec<_>=std::env::args().skip(1).collect();
 let data:Value=serde_json::from_str(&fs::read_to_string(&args[0])?)?;
 let entities:BTreeMap<u64,Record>=data["entities"].as_object().unwrap().iter()
   .map(|(key,v)|(key.parse().unwrap(),v.as_object().unwrap().clone())).collect();
 let snapshot=EntitySnapshot::new(entities,data["basis_t"].as_u64().unwrap())?;
 let seen:BTreeSet<u64>=data["seen"].as_array().unwrap().iter().map(|x|x.as_u64().unwrap()).collect();
 let pool=assessment_sampling::pool(&snapshot,&[data["knowledge_point"].as_u64().unwrap()],&seen)?;
 let mut bands=BTreeMap::<String,Vec<u64>>::new();
 for q in pool { let band=assessment_sampling::band(&snapshot,q)?.unwrap();
   bands.entry(["easy","moderate","hard"][band].into()).or_default().push(q); }
 let report=json!({"basis":snapshot.basis_t,"entry_point":"assessment_sampling::pool","available_ids_by_level":bands,"excluded_unavailable":seen,"database_writes":0});
 fs::write(&args[1],serde_json::to_string_pretty(&report)?+"\n")?;
 println!("{}",report);Ok(())
}
