//! Check actual committed KP eligibility and saved grading with the current engine.
use course_academy_engine::{learning,inventory,assessment_sampling,schema::{EntitySnapshot,Record}};
use serde_json::{Value,json};
use std::{collections::{BTreeMap,BTreeSet},error::Error,fs};
fn main()->Result<(),Box<dyn Error>>{
 let args:Vec<_>=std::env::args().skip(1).collect();let input:Value=serde_json::from_str(&fs::read_to_string(&args[0])?)?;
 let records:BTreeMap<u64,Record>=input["entities"].as_object().unwrap().iter().map(|(k,v)|(k.parse().unwrap(),v.as_object().unwrap().clone())).collect();let s=EntitySnapshot::new(records,0)?;
 let kp=input["kp"].as_u64().unwrap();let wanted:BTreeSet<_>=input["expected_fresh"].as_array().unwrap().iter().map(|v|v.as_u64().unwrap()).collect();
 let actual:BTreeSet<_>=inventory::practice_pool(&s,&[kp],&BTreeSet::new())?.into_iter().collect();assert_eq!(actual,wanted);
 let assessment:BTreeSet<_>=assessment_sampling::pool(&s,&[kp],&BTreeSet::new())?.into_iter().collect();assert_eq!(assessment,wanted);
 for q in input["retired"].as_array().unwrap(){assert!(learning::validate_practice_question(&s,q.as_u64().unwrap()).is_err());}
 for saved in input["saved"].as_array().unwrap(){let responses:BTreeMap<_,_>=saved["responses"].as_object().unwrap().iter().map(|(k,v)|(k.parse::<u64>().unwrap(),v.as_str().unwrap().to_string())).collect();assert!(learning::grade(&s,saved["question"].as_u64().unwrap(),&responses)?);}
 let report=json!({"passed":true,"fresh_inventory_ids":actual,"fresh_assessment_ids":assessment,"retired_questions_rejected":input["retired"],"saved_attempts_still_grade_correct":input["saved"].as_array().unwrap().len()});fs::write(&args[1],serde_json::to_string_pretty(&report)?+"\n")?;println!("{report}");Ok(())
}
