//! Generic in-memory grading checks through the real application; never accesses EDB.
use course_academy_engine::{learning, schema::{EntitySnapshot, Record}};
use serde_json::{Value, json};
use std::{collections::BTreeMap, error::Error, fs};
fn record(v: Value)->Record {v.as_object().unwrap().clone()}
fn main()->Result<(),Box<dyn Error>> {
 let args:Vec<_>=std::env::args().skip(1).collect();
 if args.len()!=2{return Err("check-engine INPUT.json REPORT.json".into())}
 let input:Value=serde_json::from_str(&fs::read_to_string(&args[0])?)?;
 let(mut accepted,mut rejected,mut unresolved)=(0,0,0);let mut reports=vec![];
 for item in input.as_array().ok_or("records array required")? {
  let q=&item["record"]["question"];let fields=q[":question/answer-fields"].as_array().ok_or("fields required")?;
  let mut entities=BTreeMap::new();let mut maps=vec![];let mut field_ids=vec![];let mut next_answer=100u64;
  let mut enum_names=std::collections::BTreeSet::new();
  for f in fields {enum_names.insert(f[":answer-field/type"].as_str().ok_or("field enum")?.trim_start_matches(':').to_owned());
   for a in f[":answer-field/choices"].as_array().ok_or("choices")?{enum_names.insert(a[":answer/type"].as_str().ok_or("answer enum")?.trim_start_matches(':').to_owned());}}
  for(i,name)in enum_names.into_iter().enumerate(){if i>=19{return Err("too many fixture enums".into())}entities.insert(i as u64+1,record(json!({"db/ident":name})));}

  for(i,f)in fields.iter().enumerate(){
   let field_id=20+i as u64;field_ids.push(field_id);let mut ids=vec![];let mut by_uuid=BTreeMap::new();let mut correct=None;
   let correct_uuid=f[":answer-field/correct"].get(1).and_then(Value::as_str).ok_or("correct lookup ref required")?;
   for a in f[":answer-field/choices"].as_array().ok_or("choices required")?{
    let id=next_answer;next_answer+=1;ids.push(id);
    let uuid=a[":answer/id"].as_str().ok_or("answer UUID required")?;
    if by_uuid.insert(uuid.to_owned(),id).is_some(){return Err("duplicate answer UUID".into())}
    if uuid==correct_uuid{correct=Some(id)}
    entities.insert(id,record(json!({"answer/type":a[":answer/type"].as_str().ok_or("answer type required")?.trim_start_matches(':'),"answer/value":a[":answer/value"]})));
   }
   let correct=correct.ok_or("correct answer must belong to its field")?;
   entities.insert(field_id,record(json!({"answer-field/key":f[":answer-field/key"],"answer-field/type":f[":answer-field/type"].as_str().ok_or("field type required")?.trim_start_matches(':'),"answer-field/choices":ids,"answer-field/correct":correct})));
   maps.push(by_uuid);
  }
  entities.insert(10,record(json!({"question/id":"batch-generator-fixture","question/problem":q[":question/problem"],"question/answer-fields":field_ids})));
  entities.insert(11,record(json!({"knowledge-point/title":item["record"]["knowledge_point"]["title"],"knowledge-point/questions":[10]})));
  let snapshot=EntitySnapshot::new(entities,0)?;
  let result=learning::validate_practice_question(&snapshot,10);
  let usable=result.is_ok();

  reports.push(json!({"label":item["label"],"question_id":q[":question/id"],"usable":usable,"reason":result.err()}));
 }
 fs::write(&args[1],serde_json::to_string_pretty(&json!({"database_writes":0,"entry_point":"course_academy_engine::learning::validate_practice_question","records":reports}))?+"\n")?;
 Ok(())
}
