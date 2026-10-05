//! Run the current native grader against prepared content, without a database.
use course_academy_engine::{learning, schema::{EntitySnapshot, Record}};
use serde_json::{json, Value};
use std::{collections::BTreeMap, error::Error, fs};

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.len() != 2 { return Err("usage: validate_historical_question_readiness QUESTIONS.json REPORT.json".into()); }
    let source: Value = serde_json::from_str(&fs::read_to_string(&args[0])?)?;
    let mut reports = vec![];
    for q in source["questions"].as_array().ok_or("questions required")? {
        let mut entities = BTreeMap::<u64, Record>::new();
        for (i, name) in ["answer-field.type/blank", "answer-field.type/radio", "answer-field.type/select",
                          "answer.type/math", "answer.type/text", "answer.type/image"].iter().enumerate() {
            entities.insert(i as u64 + 1, json!({"db/ident":name}).as_object().unwrap().clone());
        }
        let mut canonical = BTreeMap::new();
        let mut wrong = BTreeMap::new();
        let mut field_ids = vec![];
        let mut alternate_choices = vec![];
        let mut next = 20;
        for f in q["answer_fields"].as_array().ok_or("answer fields required")? {
            let field_id = next; next += 1;
            let mut choices = vec![];
            let mut correct = None;
            for c in f["choices"].as_array().ok_or("choices required")? {
                let eid = next; next += 1;
                choices.push(eid);
                if c["value"] == f["correct_value"] { correct = Some(eid); }
                entities.insert(eid, json!({"answer/type":format!("answer.type/{}",c["type"].as_str().unwrap()),
                    "answer/value":c["value"]}).as_object().unwrap().clone());
            }
            let correct = correct.ok_or("missing canonical answer")?;
            let is_blank = f["type"] == "blank";
            let response = if is_blank { f["correct_value"].as_str().unwrap().to_owned() } else { correct.to_string() };
            canonical.insert(field_id, response.clone());
            wrong.insert(field_id, if is_blank { format!("{response} [incorrect]") } else {
                choices.iter().find(|c| **c != correct).ok_or("no distractor")?.to_string()
            });
            if !is_blank {
                alternate_choices.extend(choices.iter().filter(|c| **c != correct)
                    .map(|c| (field_id, c.to_string())));
            }
            entities.insert(field_id, json!({"answer-field/key":f["key"],
                "answer-field/type":format!("answer-field.type/{}",f["type"].as_str().unwrap()),
                "answer-field/choices":choices,"answer-field/correct":correct}).as_object().unwrap().clone());
            field_ids.push(field_id);
        }
        entities.insert(10, json!({"question/id":"prepared-content-check", "question/problem":q["problem"],
            "question/answer-fields":field_ids}).as_object().unwrap().clone());
        let snapshot = EntitySnapshot::new(entities, 0)?;
        let result = learning::grade(&snapshot, 10, &canonical);
        let (accepted, error) = match result {
            Ok(true) => {
                if learning::grade(&snapshot, 10, &wrong)? { return Err("wrong response graded correct".into()); }
                for (field_id, response) in alternate_choices {
                    let mut attempt = canonical.clone();
                    attempt.insert(field_id, response);
                    if learning::grade(&snapshot, 10, &attempt)? {
                        return Err("an authored distractor graded correct".into());
                    }
                }
                (true, None)
            }
            Ok(false) => return Err("canonical response graded incorrect".into()),
            Err(message) => (false, Some(message)),
        };
        reports.push(json!({"math_academy_id":q["math_academy_id"],"accepted_by_current_grader":accepted,"reason":error}));
    }
    let ready = reports.iter().filter(|q| q["accepted_by_current_grader"] == true).count();
    let report = json!({"question_count":reports.len(),"current_engine_ready_count":ready,
        "needs_symbolic_grader_count":reports.len()-ready,"database_writes":0,"questions":reports});
    fs::write(&args[1], serde_json::to_string_pretty(&report)? + "\n")?;
    println!("{}", json!({"checked":report["question_count"],"current_engine_ready":ready,
        "needs_symbolic_grader":report["needs_symbolic_grader_count"]}));
    Ok(())
}
