//! Read a captured application projection with the actual inventory predicates.
use course_academy_engine::{schema::EntitySnapshot,learning,assessment_sampling};
use serde_json::{Value,json};
use std::{error::Error,fs};
fn main()->Result<(),Box<dyn Error>> {
 let args:Vec<_>=std::env::args().skip(1).collect();
 let value:Value=serde_json::from_str(&fs::read_to_string(&args[0])?)?;
 let s=EntitySnapshot::from_json(&value)?;
 let l=s.entities.iter().find(|(_,r)|r.get("learner/id").and_then(Value::as_str)==Some("59d5cf13-351c-4114-be19-4c3bb64ee051")).ok_or("Learner missing")?.0;
 let kp=17592186184172;
 let unavailable=learning::unavailable_questions(&s,*l)?;
 let pool=assessment_sampling::pool(&s,&[kp],&unavailable)?;
 let mut counts=[0usize;3];
 for q in &pool {counts[assessment_sampling::band(&s,*q)?.ok_or("Unrated pool member")?]+=1;}
 let out=json!({"basis":s.basis_t,"knowledgePoint":kp,"available_by_level":{"easy":counts[0],"moderate":counts[1],"hard":counts[2]},"available_questions":pool,"practice_members":s.refs(kp,"knowledge-point/questions")?,"excluded_seen_or_reserved":s.refs(kp,"knowledge-point/questions")?.iter().filter(|q|unavailable.contains(q)).collect::<Vec<_>>(),"entry_points":["learning::unavailable_questions","assessment_sampling::pool","assessment_sampling::band"]});
 fs::write(&args[1],serde_json::to_string_pretty(&out)?+"\n")?;Ok(())
}
