//! Read-only current application inventory predicates; no writer, jobs or attempts.
use course_academy_engine::{schema::{self,EntitySnapshot,Record},learning,inventory,assessment_sampling};
use edb_core::{Cardinality,DatabaseValue,Datom,IndexPrefix,Keyword,Peer,Value,postgres_config_from_env};
use serde_json::{Value as Json,json};
use std::{collections::{BTreeMap,BTreeSet},env,error::Error,fs};
type Result<T>=std::result::Result<T,Box<dyn Error>>;
fn uuid(v:u128)->String {let s=format!("{v:032x}");format!("{}-{}-{}-{}-{}",&s[..8],&s[8..12],&s[12..16],&s[16..20],&s[20..])}
fn value(v:&Value)->Result<Json>{Ok(match v {
 Value::String(v)|Value::Uri(v)=>json!(v),Value::Long(v)=>json!(v),Value::Double(v)=>json!(v),Value::Float(v)=>json!(v),Value::Bool(v)=>json!(v),Value::Ref(v)=>json!(v),Value::Keyword(v)=>schema::keyword(&v.qualified_name()),Value::Uuid(v)=>json!({"$uuid":uuid(*v)}),Value::Instant(v)=>json!({"$instant":v}),_=>return Err("Unsupported domain value".into())})}
fn add(db:&DatabaseValue,records:&mut BTreeMap<u64,Record>,d:Datom)->Result<()> {
 let a=db.schema().attribute(d.attribute)?;let name=a.ident.qualified_name();let v=value(&d.value)?;
 let r=records.entry(d.entity).or_default();
 if a.cardinality==Cardinality::Many {let values=r.entry(name).or_insert(json!([])).as_array_mut().unwrap();if !values.contains(&v){values.push(v);}}
 else{r.insert(name,v);} Ok(())
}
fn entity(db:&DatabaseValue,records:&mut BTreeMap<u64,Record>,e:u64)->Result<()> {
 for d in db.collect_datoms_with_prefix(&IndexPrefix::Eavt{entity:e,attribute:None,value:None})? {add(db,records,d)?;}Ok(())
}
fn refs(records:&BTreeMap<u64,Record>,e:u64,a:&str)->Vec<u64>{match records.get(&e).and_then(|r|r.get(a)){Some(Json::Array(v))=>v.iter().filter_map(Json::as_u64).collect(),Some(v)=>v.as_u64().into_iter().collect(),None=>vec![]}}
fn main()->Result<()> {
 let args:Vec<_>=env::args().skip(1).collect();let input:Json=serde_json::from_str(&fs::read_to_string(&args[0])?)?;
 let learner=input["learner"].as_u64().ok_or("learner missing")?;let topic=input["topic"].as_u64().ok_or("topic missing")?;
 let current=Peer::connect_configured(&postgres_config_from_env()?,input["database"].as_str().ok_or("database missing")?,512)?.db();
 let lineage=current.snapshot_reference()?.key().lineage_id().to_string();assert_eq!(input["lineage"].as_str(),Some(lineage.as_str()));
 let basis=input["basis"].as_u64().unwrap_or(current.basis_t());let db=current.as_of(basis);let mut records=BTreeMap::new();
 // Only this topic and this learner's own history. Every database access has
 // a fixed entity or an exact selected-question reverse-reference prefix.
 entity(&db,&mut records,topic)?;let kps=refs(&records,topic,"topic/knowledge-points");
 let mut selected_questions=BTreeSet::new();
 for &kp in &kps {
  entity(&db,&mut records,kp)?;
  for g in refs(&records,kp,"knowledge-point/question-generator"){entity(&db,&mut records,g)?;}
  for q in refs(&records,kp,"knowledge-point/questions") {
   selected_questions.insert(q);
   entity(&db,&mut records,q)?;
   for f in refs(&records,q,"question/answer-fields") {
    entity(&db,&mut records,f)?;
    for a in refs(&records,f,"answer-field/choices"){entity(&db,&mut records,a)?;}
   }
  }
 }
 // Capture all owners of the selected questions, so canonical exclusions and
 // the symbolic grader's KP-title context are exact within this lesson bank.
 for q in selected_questions {
  for name in ["knowledge-point/canonical-example","knowledge-point/questions"] {
   let (ns,n)=name.split_once('/').unwrap();let a=db.schema().resolve_ident(&Keyword::new(ns,n)).ok_or("missing attribute")?;
   for d in db.collect_datoms_with_prefix(&IndexPrefix::Vaet{value:Value::Ref(q),attribute:Some(a),entity:None})? {let owner=d.entity;add(&db,&mut records,d)?;if !records[&owner].contains_key("knowledge-point/title"){let title=db.schema().resolve_ident(&Keyword::new("knowledge-point","title")).ok_or("missing title")?;for d in db.collect_datoms_with_prefix(&IndexPrefix::Eavt{entity:owner,attribute:Some(title),value:None})? {add(&db,&mut records,d)?;}}}
  }
 }
 entity(&db,&mut records,learner)?;
 let tasks=refs(&records,learner,"learner/activity");let mut history_items=0;
 for task in tasks.iter().copied() {
  entity(&db,&mut records,task)?;
  for item in refs(&records,task,"learner-task/items") {
   history_items+=1;let a=db.schema().resolve_ident(&Keyword::new("task-item","content")).ok_or("missing item content")?;
   records.entry(item).or_default();for d in db.collect_datoms_with_prefix(&IndexPrefix::Eavt{entity:item,attribute:Some(a),value:None})? {add(&db,&mut records,d)?;}
  }
  for status in refs(&records,task,"learner-task/status"){entity(&db,&mut records,status)?;}
  let status=refs(&records,task,"learner-task/status").first().and_then(|e|records.get(e)).and_then(|r|r.get("db/ident")).and_then(|v|v.get("$keyword")).and_then(Json::as_str).unwrap_or("").to_owned();
  if status.ends_with("/started")||status.ends_with("/paused") {
   for activity in refs(&records,task,"learner-task/activity") {
    entity(&db,&mut records,activity)?;
    for token in refs(&records,activity,"activity/type"){entity(&db,&mut records,token)?;}
    for step in refs(&records,activity,"activity/steps") {entity(&db,&mut records,step)?;for content in refs(&records,step,"step/content"){records.entry(content).or_default();}}
   }
  }
 }
 let token_ids:BTreeSet<_>=records.values().flat_map(|r|["answer/type","answer-field/type","question/difficulty"].into_iter().filter_map(|a|r.get(a).and_then(Json::as_u64))).collect();
 for token in token_ids{entity(&db,&mut records,token)?;}
 let contents:Vec<_>=records.values().filter_map(|r|r.get("task-item/content").and_then(Json::as_u64)).collect();
 for e in contents{records.entry(e).or_default();}
 let s=EntitySnapshot::new(records,basis)?;let seen=learning::unavailable_questions(&s,learner)?;let mut rows=vec![];
 for &kp in &kps {
  let members=s.refs(kp,"knowledge-point/questions")?;let usable=inventory::practice_pool(&s,&[kp],&BTreeSet::new())?;let fresh=inventory::practice_pool(&s,&[kp],&seen)?;
  let mut counts=BTreeMap::from([("easy",0),("moderate",0),("hard",0),("unrated",0)]);
  for &q in &fresh{let b=assessment_sampling::band(&s,q)?.map(|b|["easy","moderate","hard"][b]).unwrap_or("unrated");*counts.get_mut(b).unwrap()+=1;}
  let invalid:Vec<_>=members.iter().filter(|q|!usable.contains(q)).map(|q|json!({"question":q,"reason":if s.is_example(*q){"canonical example".to_owned()}else{learning::validate_response_question(&s,*q).err().map(|e|e.to_string()).unwrap_or("ungraded free response".into())}})).collect();
  let generator=s.optional_ref(kp,"knowledge-point/question-generator")?;
  rows.push(json!({"knowledgePoint":kp,"title":s.entity(kp)?.get("knowledge-point/title"),"practice_members":members.len(),"usable_total":usable.len(),"available_total":fresh.len(),"available_by_band":counts,"shortage_to_lesson":5usize.saturating_sub(fresh.len()),"fresh_question_ids":fresh,"unavailable_question_ids":members.iter().filter(|q|seen.contains(q)).collect::<Vec<_>>(),"invalid_questions":invalid,"generator":generator,"generator_script":generator.and_then(|g|s.entity(g).ok()?.get("question-generator/script").cloned())}));
 }
 let result=json!({"basis":basis,"lineage":lineage,"topic":topic,"learner":learner,"lesson_ready":inventory::lesson_ready(&s,&kps,&seen)?,"lesson_shortages":inventory::lesson_shortages(&s,&kps,&seen)?,"knowledge_points":rows,"read_scope":{"lesson_kps":kps.len(),"own_learner_tasks":tasks.len(),"own_history_items":history_items,"projection_entities":s.entities.len(),"global_attribute_scans":0},"entry_points":["learning::unavailable_questions","inventory::practice_pool","inventory::lesson_shortages","inventory::lesson_ready"],"database_writes":0,"learner_attempts_created":0});
 fs::write(&args[1],serde_json::to_string_pretty(&result)?+"\n")?;println!("{}",serde_json::to_string_pretty(&result)?);Ok(())
}
