//! Generic in-memory grading checks through the real application; never accesses EDB.
use course_academy_engine::{learning, schema::{EntitySnapshot, Record}};
use serde_json::{Value, json};
use std::{collections::BTreeMap, error::Error, fs};
fn record(v: Value)->Record {v.as_object().unwrap().clone()}
// Publisher records allow either a keyword string or a pulled :db/ident map.
fn enum_name(value: &Value) -> Result<&str, Box<dyn Error>> {
 let ident = value.as_str().or_else(|| value.get(":db/ident").and_then(Value::as_str))
  .ok_or("enum keyword string or :db/ident map required")?;
 Ok(ident.trim_start_matches(':'))
}
fn main()->Result<(),Box<dyn Error>> {
 let args:Vec<_>=std::env::args().skip(1).collect();
 if args.len()!=2{return Err("check-engine INPUT.json REPORT.json".into())}
 let input:Value=serde_json::from_str(&fs::read_to_string(&args[0])?)?;
 let(mut accepted,mut rejected,mut unresolved)=(0,0,0);let mut reports=vec![];
 for item in input.as_array().ok_or("records array required")? {
  let q=&item["record"]["question"];let fields=q[":question/answer-fields"].as_array().ok_or("fields required")?;
  let mut entities=BTreeMap::new();let mut maps=vec![];let mut field_ids=vec![];let mut next_answer=100u64;
  let mut enum_names=std::collections::BTreeSet::new();
  for f in fields {enum_names.insert(enum_name(&f[":answer-field/type"])?.to_owned());
   for a in f[":answer-field/choices"].as_array().ok_or("choices")?{enum_names.insert(enum_name(&a[":answer/type"])?.to_owned());}}
  for(i,name)in enum_names.into_iter().enumerate(){if i>=19{return Err("too many fixture enums".into())}entities.insert(i as u64+1,record(json!({"db/ident":name})));}

  for(i,f)in fields.iter().enumerate(){
   let field_id=20+i as u64;field_ids.push(field_id);let mut ids=vec![];let mut by_uuid=BTreeMap::new();let mut correct=None;
   let correct_uuid=f[":answer-field/correct"].get(1).and_then(Value::as_str).ok_or("correct lookup ref required")?;
   for a in f[":answer-field/choices"].as_array().ok_or("choices required")?{
    let id=next_answer;next_answer+=1;ids.push(id);
    let uuid=a[":answer/id"].as_str().ok_or("answer UUID required")?;
    if by_uuid.insert(uuid.to_owned(),id).is_some(){return Err("duplicate answer UUID".into())}
    if uuid==correct_uuid{correct=Some(id)}
    entities.insert(id,record(json!({"answer/type":enum_name(&a[":answer/type"])?,"answer/value":a[":answer/value"]})));
   }
   let correct=correct.ok_or("correct answer must belong to its field")?;
   entities.insert(field_id,record(json!({"answer-field/key":f[":answer-field/key"],"answer-field/type":enum_name(&f[":answer-field/type"])?,"answer-field/choices":ids,"answer-field/correct":correct})));
   maps.push(by_uuid);
  }
  entities.insert(10,record(json!({"question/id":"batch-generator-fixture","question/problem":q[":question/problem"],"question/answer-fields":field_ids})));
  entities.insert(11,record(json!({"knowledge-point/title":item["record"]["knowledge_point"]["title"],"knowledge-point/questions":[10]})));
  let snapshot=EntitySnapshot::new(entities,0)?;let mut checks=vec![];
  for check in item["checks"].as_array().ok_or("checks required")?{
   let i=check["field_index"].as_u64().unwrap_or(0)as usize;
   if i>=fields.len(){return Err("field_index out of range".into())}
   let submitted=if let Some(uuid)=check["submitted_answer_id"].as_str(){maps[i].get(uuid).ok_or("selected UUID not in field")?.to_string()}
    else{check["submitted"].as_str().ok_or("submission required")?.to_owned()};
   let result=learning::grade_field(&snapshot,10,field_ids[i],&submitted);
   let outcome=match &result{Ok(true)=>"accepted",Ok(false)=>"rejected",Err(_)=>"unresolved"};
   let expected=check["expected"].as_str().ok_or("expected result required")?;
   if outcome!=expected{return Err(format!("{} field {}: {:?} expected {}, got {} ({:?})",item["label"],i,submitted,expected,outcome,result).into())}
   match outcome{"accepted"=>accepted+=1,"rejected"=>rejected+=1,_=>unresolved+=1}
   checks.push(json!({"field_index":i,"submitted":submitted,"outcome":outcome,"reason":result.err(),"purpose":check["purpose"]}));
  }
  reports.push(json!({"label":item["label"],"template":item["record"]["generation"]["template"],"checks":checks}));
 }
 fs::write(&args[1],serde_json::to_string_pretty(&json!({"database_writes":0,"entry_point":"course_academy_engine::learning::grade_field","records":reports,"accepted_checks":accepted,"rejected_checks":rejected,"documented_unresolved_checks":unresolved}))?+"\n")?;
 println!("Native grading: {accepted} accepted, {rejected} rejected, {unresolved} explicitly unresolved; no database operations.");Ok(())
}

#[cfg(test)]
mod tests {
 use super::*;
 #[test]
 fn enum_representations_agree() {
  for name in [":answer-field.type/radio", ":answer-field.type/blank", ":answer.type/math", ":answer.type/text"] {
   assert_eq!(enum_name(&json!(name)).unwrap(), enum_name(&json!({":db/ident": name})).unwrap());
   assert_eq!(enum_name(&json!(name)).unwrap(), name.trim_start_matches(':'));
  }
 }
 #[test]
 fn malformed_enum_maps_fail() {
  for value in [json!(null), json!({}), json!({":db/ident": 3})] {
   assert!(enum_name(&value).is_err());
  }
 }
}
