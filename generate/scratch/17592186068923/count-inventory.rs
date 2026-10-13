//! Read-only counts using the application's real pool/unavailable policies.
use course_academy_engine::{assessment_sampling,learning,schema::{EntitySnapshot,Record}};
use serde_json::{Value,json};
use std::{collections::BTreeMap,error::Error,fs};
fn main()->Result<(),Box<dyn Error>>{
 let a:Vec<_>=std::env::args().skip(1).collect();
 let v:Value=serde_json::from_str(&fs::read_to_string(&a[0])?)?;
 let entities:BTreeMap<u64,Record>=serde_json::from_value(v["entities"].clone())?;
 let mut s=EntitySnapshot::new(entities,v["basis_t"].as_u64().ok_or("basis")?)?;
 s.status_history=serde_json::from_value(v["status_history"].clone())?;
 let l=s.entities.iter().find(|(_,r)|r.get("learner/id").and_then(Value::as_str)==Some("59d5cf13-351c-4114-be19-4c3bb64ee051")).ok_or("learner")?.0;
 let unavailable=learning::unavailable_questions(&s,*l)?;
 let qs=assessment_sampling::pool(&s,&[17592186068923],&unavailable)?;
 let counts:Vec<_>=(0..3).map(|b|qs.iter().filter(|q|assessment_sampling::band(&s,**q).ok().flatten()==Some(b)).count()).collect();
 let result=json!({"basis":s.basis_t,"knowledgePoint":17592186068923u64,"available":{"easy":counts[0],"moderate":counts[1],"hard":counts[2]},"available_question_eids":qs,"policy":"assessment_sampling::pool and learning::unavailable_questions; canonical, unrated, incomplete, served/reserved excluded","database_writes":0});
 fs::write(&a[1],serde_json::to_string_pretty(&result)?+"\n")?;println!("{}",result);Ok(())
}
