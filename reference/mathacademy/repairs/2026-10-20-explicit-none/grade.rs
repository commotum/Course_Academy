//! Exhaustively check every historical checkbox subset, its explicit None mapping,
//! empty submissions, contradictory selections, and fresh-practice eligibility.
use course_academy_engine::{learning,schema::{EntitySnapshot,Record}};
use serde_json::{Value,json};
use std::{collections::BTreeMap,error::Error,fs};
fn obj(v:Value)->Record{v.as_object().unwrap().clone()}
fn id(v:&Value)->u64{v[":db/id"].as_u64().unwrap()}
fn main()->Result<(),Box<dyn Error>>{
 let args:Vec<_>=std::env::args().skip(1).collect();let data:Value=serde_json::from_str(&fs::read_to_string(&args[0])?)?;
 let mut count=0;let mut masks=0;let mut flips=0;
 for q in data["questions"].as_array().unwrap(){
  let mut records=BTreeMap::new();records.insert(1,obj(json!({"db/ident":"answer-field.type/checkbox"})));records.insert(2,obj(json!({"db/ident":"answer.type/text"})));
  let fields=q[":question/answer-fields"].as_array().unwrap();let mut fids=vec![];let mut canonical=BTreeMap::new();let mut banks=vec![];
  for f in fields{
   let fid=id(f);let mut choices=vec![];let mut bank=BTreeMap::new();
   for a in f[":answer-field/choices"].as_array().unwrap(){let aid=id(a);choices.push(aid);bank.insert(a[":answer/value"].as_str().unwrap().to_string(),aid);records.insert(aid,obj(json!({"answer/type":"answer.type/text","answer/value":a[":answer/value"]})));}
   let correct=id(&f[":answer-field/correct"]);canonical.insert(fid,correct.to_string());fids.push(fid);
   records.insert(fid,obj(json!({"answer-field/key":f[":answer-field/key"],"answer-field/type":"answer-field.type/checkbox","answer-field/choices":choices,"answer-field/correct":correct})));
   banks.push((fid,bank));
  }
  let qid=id(q);records.insert(qid,obj(json!({"question/id":q[":question/id"],"question/problem":q[":question/problem"],"question/answer-fields":fids})));
  records.insert(3,obj(json!({"knowledge-point/title":"Source None restoration","knowledge-point/questions":[qid]})));
  let snapshot=EntitySnapshot::new(records,0)?;learning::validate_practice_question(&snapshot,qid)?;assert!(learning::grade(&snapshot,qid,&canonical)?);
  let none_id=data["none_field_ids"][qid.to_string()].as_u64().unwrap();let ordinary:Vec<_>=banks.iter().filter(|(fid,_)|*fid!=none_id).collect();assert!(ordinary.len()<=10);
  for mask in 0..1u64<<ordinary.len(){
   let mut response=BTreeMap::new();let mut expected=true;
   for (i,(fid,bank))in ordinary.iter().enumerate(){let val=if mask&(1<<i)!=0{"true"}else{"false"};let aid=bank[val];response.insert(*fid,aid.to_string());expected&=canonical[fid]==aid.to_string();}
   let none_bank=&banks.iter().find(|(fid,_)|*fid==none_id).unwrap().1;
   response.insert(none_id,none_bank[if mask==0{"true"}else{"false"}].to_string());
   assert_eq!(learning::grade(&snapshot,qid,&response)?,expected,"mapped historical subset changed for {qid} mask {mask}");masks+=1;
   if mask!=0{response.insert(none_id,none_bank["true"].to_string());assert!(!learning::grade(&snapshot,qid,&response)?,"contradictory None accepted");}
  }
  for (fid,bank)in &banks{let mut response=canonical.clone();let alternate=bank.values().find(|a|a.to_string()!=canonical[fid]).unwrap();response.insert(*fid,alternate.to_string());assert!(!learning::grade(&snapshot,qid,&response)?);flips+=1;}
  let unchecked:BTreeMap<_,_>=banks.iter().map(|(fid,bank)|(*fid,bank["false"].to_string())).collect();assert!(!learning::grade(&snapshot,qid,&unchecked)?);
  count+=1;
 }
 let report=json!({"passed":true,"questions":count,"historical_subsets_checked":masks,"single_checkbox_flips_rejected":flips,"all_unchecked_and_contradictory_none_rejected":true,"all_fresh_practice_eligible":true,"database_writes":0});fs::write(&args[1],serde_json::to_string_pretty(&report)?+"\n")?;println!("{report}");Ok(())
}
