//! Actual in-memory practice validation; no EDB access, attempts, or progress.
use course_academy_engine::{learning,schema::{EntitySnapshot,Record}};
use serde_json::{Value,json};
use std::{fs,collections::BTreeMap,error::Error};
fn main()->Result<(),Box<dyn Error>> {
 let a:Vec<_>=std::env::args().skip(1).collect();let input:Value=serde_json::from_str(&fs::read_to_string(&a[0])?)?;
 let entities:BTreeMap<u64,Record>=serde_json::from_value(input["entities"].clone())?;
 let s=EntitySnapshot::new(entities.clone(),input["basis"].as_u64().unwrap())?;let mut reports=vec![];
 for q in input["questions"].as_array().unwrap(){let id=q.as_u64().unwrap();
  let before=learning::validate_response_question(&s,id).err();
  let all=s.refs(id,"question/answer-fields")?;let mut retained=vec![];let mut detached=vec![];
  for f in &all {if s.optional_ref(*f,"answer-field/correct")?.is_some(){retained.push(*f)}else{detached.push(*f)}}
  let cleanup=if retained.len()==1 && all.len()==2 {
   let mut simulated=entities.clone();simulated.get_mut(&id).unwrap().insert("question/answer-fields".into(),json!(retained));
   let proposed=EntitySnapshot::new(simulated,0)?;
   Some(json!({"retained_field":retained[0],"detached_field":detached[0],"validation_error":learning::validate_response_question(&proposed,id).err()}))
  }else{None};
  reports.push(json!({"question":id,"current_validation_error":before,"simulated_cleanup":cleanup}));
 }
 let(mut accepted,mut rejected)=(0,0);let mut proposals=vec![];
 for p in input["proposals"].as_array().unwrap(){
  let q=p["question"].as_u64().unwrap();let field=p["field"].as_u64().unwrap();let correct=p["correct"].as_u64().unwrap();
  let mut simulated=entities.clone();simulated.get_mut(&q).unwrap().insert("question/answer-fields".into(),json!([field]));
  simulated.get_mut(&field).unwrap().insert("answer-field/correct".into(),json!(correct));
  let proposed=EntitySnapshot::new(simulated,0)?;learning::validate_response_question(&proposed,q)?;
  for a in proposed.refs(field,"answer-field/choices")?{
   let actual=learning::grade_field(&proposed,q,field,&a.to_string())?;
   if actual!=(a==correct){return Err("grader disagreed with independently derived key".into())}
   if actual{accepted+=1}else{rejected+=1}
  }
  proposals.push(json!({"question":q,"retained_field":field,"correct_answer":correct,"simulated_only":true,"validation_passed":true}));
 }
 fs::write(&a[1],serde_json::to_string_pretty(&json!({"entry_point":"learning::validate_response_question and learning::grade_field","database_writes":0,"records":reports,"in_memory_proposals":proposals,"accepted_checks":accepted,"rejected_checks":rejected}))?+"\n")?;Ok(())
}
