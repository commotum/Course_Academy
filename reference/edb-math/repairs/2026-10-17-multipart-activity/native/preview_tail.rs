// Appended to a temporary copy of learning_api.rs by build.py; no durable writes.
#[path = "REPO_ROOT/engine/edb/answer_fields.rs"]
mod repair_answer_fields;
#[path = "REPO_ROOT/engine/edb/configuration.rs"]
mod repair_configuration;
#[path = "REPO_ROOT/engine/edb/progress.rs"]
mod repair_progress;

fn repair_registry() -> Result<edb_core::NativeRegistry> {
    type Predicate = fn(&DatabaseValue, u64) -> std::result::Result<bool, edb_core::SemanticError>;
    let mut builder = edb_core::NativeRegistry::builder();
    for (namespace, name, predicate) in [
        ("course-academy.topic", "valid-difficulty?", repair_configuration::valid_topic_difficulty as Predicate),
        ("course-academy.policy", "valid?", repair_configuration::valid_policy as Predicate),
        ("course-academy.progress", "valid-profile?", repair_progress::valid_profile as Predicate),
        ("course-academy.progress", "valid-progress?", repair_progress::valid_progress as Predicate),
        ("course-academy.answer-field", "valid?", repair_answer_fields::valid_field as Predicate),
    ] {
        builder.entity_predicate(edb_core::Symbol::new(namespace, name), move |db, entity, control| {
            control.check(1)?;
            Ok(edb_core::RuntimeValue::Scalar(Value::Bool(predicate(db, entity)?)))
        })?;
    }
    Ok(builder.build())
}

fn repair_with(db: &DatabaseValue, forms: &[Json], source: EntityRef, at: i64) -> Result<DatabaseValue> {
    Ok(db.with_forms_with_execution_options(
        &edb_core::edn_transaction::read_edn_transaction(&schema::edn(&json!(forms))?)?,
        at, source, Default::default(),
        &edb_core::TransactionExecutionOptions {native: repair_registry()?, ..Default::default()},
    )?.db_after)
}

fn repair_result<T: serde::Serialize, E: std::fmt::Display>(result: std::result::Result<T, E>) -> Json {
    match result { Ok(v) => json!({"ok":true,"value":v}), Err(e) => json!({"ok":false,"error":e.to_string()}) }
}

fn repair_position(p: learning::Position) -> Json {
    json!({"next":p.next,"passed":p.passed,"failed":p.failed,"shortage":p.shortage,"deferred":p.deferred})
}

fn repair_view(s: &EntitySnapshot, input: &Json) -> Result<Json> {
    let learner = required(input, "learner")?;
    let mut tasks = vec![];
    for task in input["tasks"].as_array().ok_or("tasks list required")? {
        let task = task.as_u64().ok_or("task ID required")?;
        let activity = s.reference(task, "learner-task/activity")?;
        let chain = items(s, task)?;
        tasks.push(json!({
            "task":task,"activity":activity,"record":s.entity(task)?,
            "chain":chain.iter().map(|item| -> Result<Json> {
                let content=s.reference(*item,"task-item/content")?;
                Ok(json!({"item":item,"content":content,"record":s.entity(*item)?,
                    "isMultistepQuestion":s.is_multistep_question(content)?,"isExample":s.is_example(content)}))
            }).collect::<Result<Vec<_>>>()?,
            "taskJson":repair_result(task_json(s,learner,task)),
            "position":repair_result(learning::continuation_state(s,activity,&chain,false,false).map(repair_position)),
            "practiceState":repair_result(practice_state(s,activity,&chain).map(repair_position)),
            "deferredResumeStep":repair_result(learning::deferred_resume_step(s,activity,&chain)),
        }));
    }
    let profiles=input["profiles"].as_array().ok_or("profiles list required")?.iter().map(|id| -> Result<Json> {
        let id=id.as_u64().ok_or("profile ID required")?;Ok(json!({"id":id,"record":s.entity(id)?}))
    }).collect::<Result<Vec<_>>>()?;
    Ok(json!({"basis":s.basis_t,"tasks":tasks,"profiles":profiles}))
}

fn repair_run() -> Result<()> {
    let args:Vec<_>=std::env::args().skip(1).collect();
    if args.len()!=4 {return Err("usage: preview DIRECTORY SOURCE_IDENT EXPECTED_BASIS INPUT_JSON".into());}
    let dir=std::path::Path::new(&args[0]);
    let source=EntityRef::from_edn(&args[1])?;
    let basis:u64=args[2].parse()?;
    let input:Json=serde_json::from_str(&std::fs::read_to_string(&args[3])?)?;
    let connection=Connection::connect_configured(postgres_config_from_env()?,"math",256)?;
    let db=connection.db();
    if db.basis_t()!=basis {return Err(format!("Current basis {} != prepared {basis}; no preview or write",db.basis_t()).into());}
    let before=snapshot(&db)?;
    std::fs::write(dir.join("api-preview-before.json"),serde_json::to_string_pretty(&repair_view(&before,&input)?)?+"\n")?;
    let forms=edb_core::edn_transaction::read_edn_transaction(&std::fs::read_to_string(dir.join("transaction.edn"))?)?;
    let at=Utc::now().timestamp_millis();
    let report=db.with_forms_with_execution_options(&forms,at,source.clone(),Default::default(),
        &edb_core::TransactionExecutionOptions {native:repair_registry()?,..Default::default()})?;
    let after=snapshot(&report.db_after)?;
    std::fs::write(dir.join("api-preview-after.json"),serde_json::to_string_pretty(&repair_view(&after,&input)?)?+"\n")?;
    let learner=required(&input,"learner")?;
    let mut scenarios=vec![];
    for task in input["tasks"].as_array().unwrap() {
        let task=task.as_u64().unwrap();
        let scenario=(|| -> Result<Json> {
            let (resume_forms,resume_result)=mutate(&after,learner,"resume",&json!({"taskId":task}),DateTime::from_timestamp_millis(at+1).unwrap())?;
            let resumed_db=repair_with(&report.db_after,&resume_forms,source.clone(),at+1)?;
            let resumed=snapshot(&resumed_db)?;
            let item=*items(&resumed,task)?.last().ok_or("No current presentation after resume")?;
            let (continue_forms,continue_result)=mutate(&resumed,learner,"continue",&json!({"taskId":task,"itemId":item}),DateTime::from_timestamp_millis(at+2).unwrap())?;
            let continued_db=repair_with(&resumed_db,&continue_forms,source.clone(),at+2)?;
            let continued=snapshot(&continued_db)?;
            let next=*items(&continued,task)?.last().ok_or("No presentation after continue")?;
            let question=continued.reference(next,"task-item/content")?;
            learning::validate_practice_question(&continued,question)?;
            if before.refs(task,"learner-task/items")?.contains(&next) {return Err("Continue did not create fresh practice".into());}
            Ok(json!({"task":task,"resumeForms":resume_forms,"resumeResult":resume_result,
                "continueForms":continue_forms,"continueResult":continue_result,"nextItem":next,"nextQuestion":question,
                "nextQuestionIsMultistep":continued.is_multistep_question(question)?,
                "nextQuestionWasPreviouslyUnavailable":learning::unavailable_questions(&after,learner)?.contains(&question),
                "taskJson":task_json(&continued,learner,task)?}))
        })();
        scenarios.push(json!({"task":task,"preview":repair_result(scenario)}));
    }
    std::fs::write(dir.join("api-preview-resume-continue.json"),serde_json::to_string_pretty(&json!({"committed":false,"speculative":true,"scenarios":scenarios}))?+"\n")?;
    println!("{}",json!({"committed":false,"speculative":true,"basisBefore":basis,"basisAfter":after.basis_t,"tasks":input["tasks"],"allResumeContinuePassed":scenarios.iter().all(|s|s["preview"]["ok"]==true)}));
    Ok(())
}

fn main() {
    if let Err(error)=repair_run(){eprintln!("{error}");std::process::exit(1);}
}
