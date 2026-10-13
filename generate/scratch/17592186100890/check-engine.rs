//! In-memory checks through the actual grade_field entry point; no EDB access.
use course_academy_engine::{learning, schema::{EntitySnapshot, Record}};
use serde_json::{Value, json};
use std::{collections::BTreeMap, error::Error, fs};

fn record(value: Value) -> Record { value.as_object().unwrap().clone() }

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.len() != 2 { return Err("check-engine INPUT.json REPORT.json".into()); }
    let input: Value = serde_json::from_str(&fs::read_to_string(&args[0])?)?;
    let mut reports = vec![];
    let mut accepted = 0;
    let mut rejected = 0;
    let mut limitations = 0;
    for item in input.as_array().ok_or("expected records array")? {
        let q = &item["record"]["question"];
        let field = &q[":question/answer-fields"][0];
        let mut entities = BTreeMap::new();
        for (index, name) in ["answer-field.type/radio", "answer-field.type/blank", "answer.type/math"].iter().enumerate() {
            entities.insert(index as u64 + 1, record(json!({"db/ident":name})));
        }
        let mut answer_ids = vec![];
        let correct_uuid = field[":answer-field/correct"][1].as_str().ok_or("correct ref")?;
        let mut correct = None;
        for (index, answer) in field[":answer-field/choices"].as_array().ok_or("choices")?.iter().enumerate() {
            let id = 100 + index as u64; // Fixture-local IDs, never live entity IDs.
            answer_ids.push(id);
            if answer[":answer/id"] == correct_uuid { correct = Some(id); }
            entities.insert(id, record(json!({"answer/type":"answer.type/math", "answer/value":answer[":answer/value"]})));
        }
        let correct = correct.ok_or("canonical must belong to its field")?;
        entities.insert(10, record(json!({"question/id":"generator-fixture", "question/problem":q[":question/problem"], "question/answer-fields":[20]})));
        entities.insert(11, record(json!({"knowledge-point/title":item["record"]["knowledge_point"]["title"], "knowledge-point/questions":[10]})));
        entities.insert(20, record(json!({"answer-field/key":field[":answer-field/key"],
            "answer-field/type":field[":answer-field/type"].as_str().unwrap().trim_start_matches(':'),
            "answer-field/choices":answer_ids, "answer-field/correct":correct})));
        let snapshot = EntitySnapshot::new(entities, 0)?;
        let mut checks = vec![];
        for check in item["checks"].as_array().ok_or("checks")? {
            let result = learning::grade_field(&snapshot, 10, 20, check["submitted"].as_str().ok_or("submission")?);
            let outcome = match result {
                Ok(true) => "accepted", Ok(false) => "rejected", Err(_) => "unresolved"
            };
            let expected = check["expected"].as_str().ok_or("expected")?;
            if outcome != expected {
                return Err(format!("{}: {} expected {}, got {} ({:?})", item["label"], check["submitted"], expected, outcome, result).into());
            }
            match outcome { "accepted" => accepted += 1, "rejected" => rejected += 1, _ => limitations += 1 }
            checks.push(json!({"submitted":check["submitted"], "outcome":outcome,
                              "reason":result.err(), "purpose":check["purpose"]}));
        }
        reports.push(json!({"label":item["label"], "template":item["record"]["generation"]["template"], "checks":checks}));
    }
    fs::write(&args[1], serde_json::to_string_pretty(&json!({"database_writes":0,
        "entry_point":"course_academy_engine::learning::grade_field", "records":reports,
        "accepted_checks":accepted,"rejected_checks":rejected,"documented_unresolved_checks":limitations}))? + "\n")?;
    println!("Real grade_field checks: {} accepted, {} rejected, {} documented unresolved; database writes: 0", accepted,rejected,limitations);
    Ok(())
}
