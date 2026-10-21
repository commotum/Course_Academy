const REPAIR_LEARNER: u64 = 17592186045416;
const BAD_ITEM: u64 = 17592186649259;
const TASK: u64 = 17592186627939;
const REVIEW: u64 = 17592186649970;

fn dynamic_ids(s: &EntitySnapshot) -> Result<BTreeSet<u64>> {
    let mut ids: BTreeSet<_> = s.refs(REPAIR_LEARNER,"learner/knowledge-profile")?.into_iter().collect();
    ids.extend(s.optional_ref(REPAIR_LEARNER,"learner/performance")?);
    Ok(ids)
}
fn dynamic_records(s: &EntitySnapshot, ids: &BTreeSet<u64>) -> BTreeMap<u64,Record> {
    ids.iter().filter_map(|id|s.entities.get(id).map(|r|(*id,r.clone()))).collect()
}

fn apply_credit(s: &mut EntitySnapshot, forms: &[Json], identities: &BTreeMap<String,u64>) -> Result<()> {
    let mut temps=BTreeMap::new();
    for f in forms {
        if let Some(m)=f.as_object() {
            if let Some(temp)=m["db/id"].as_str() {
                let key=m.get("progress/id").and_then(Json::as_str).ok_or("Unexpected tempid")?;
                temps.insert(temp.to_owned(),*identities.get(key).ok_or("Unknown progress identity")?);
            }
        }
    }
    let mut changed=BTreeMap::new();
    for f in forms {
        if let Some(m)=f.as_object() {
            let eid=m["db/id"].as_u64().or_else(||m["db/id"].as_str().and_then(|t|temps.get(t).copied())).ok_or("Unknown entity")?;
            let record=changed.entry(eid).or_insert_with(||s.entities.get(&eid).cloned().unwrap_or_default());
            for (attr,v) in m {
                if matches!(attr.as_str(),"db/id"|"db/ensure") {continue;}
                let v=if v.get("$instant").is_some() {json!({"$instant":schema::parse_instant(v)?.timestamp_millis()})} else {v.clone()};
                if attr=="learner/knowledge-profile" {
                    let mut links=record.get(attr).and_then(Json::as_array).cloned().unwrap_or_default();
                    for link in v.as_array().ok_or("Expected links")? {
                        let id=link.as_u64().or_else(||link.as_str().and_then(|t|temps.get(t).copied())).ok_or("Unknown link")?;
                        if !links.contains(&json!(id)) {links.push(json!(id));}
                    }
                    links.sort_by_key(Json::as_u64);record.insert(attr.clone(),json!(links));
                } else {record.insert(attr.clone(),v);}
            }
        } else {
            let a=f.as_array().ok_or("Expected form")?;
            if a[0]!=kw("db/retract") {return Err("Unexpected credit operation".into());}
            let eid=a[1].as_u64().ok_or("Expected entity")?;
            let attr=a[2]["$keyword"].as_str().ok_or("Expected attribute")?;
            let r=changed.entry(eid).or_insert_with(||s.entities[&eid].clone());
            r.remove(attr);
        }
    }
    s.replace_records(changed,s.basis_t)?;
    Ok(())
}

fn correction(dir: &std::path::Path) -> Result<()> {
    let conn=Connection::connect_configured(postgres_config_from_env()?,"math",512)?;
    let db=conn.db();let current=snapshot(&db)?;
    let events=current.status_history.iter().filter(|h| h.entity==TASK && h.attribute=="learner-task/status" && current.ident(&h.value).ok().as_deref()==Some("learner-task.status/completed")).collect::<Vec<_>>();
    if events.len()!=1 {return Err("Expected one assessment completion".into());}
    let h=events[0];let before=snapshot(&db.clone().as_of(h.t-1))?;
    let post=snapshot(&db.clone().as_of(h.t))?;
    let ids=dynamic_ids(&current)?;
    if dynamic_records(&post,&ids)!=dynamic_records(&current,&ids) || dynamic_ids(&post)?!=ids {
        return Err("Learner state changed after assessment; replay subsequent events before correcting".into());
    }
    let identities=current.entities.with_attribute("progress/id").into_iter().map(|id|Ok((current.entity(id)?["progress/id"].as_str().ok_or("Invalid progress identity")?.to_owned(),id))).collect::<Result<BTreeMap<_,_>>>()?;
    let activity=current.reference(TASK,"learner-task/activity")?;
    let chain=items(&current,TASK)?;
    let mut original=vec![];let mut repaired=vec![];
    for &item in &chain {
        let old=status(&before,item,"task-item/status")?;
        if matches!(old.as_str(),"correct"|"incorrect") {continue;}
        let st=status(&current,item,"task-item/status")?;
        if !matches!(st.as_str(),"correct"|"incorrect") {return Err("Expected all assessment questions answered".into());}
        let q=current.reference(item,"task-item/content")?;
        original.push((q,st=="correct"));repaired.push((q,st=="correct" || item==BAD_ITEM));
    }
    if original.len()!=9 || original.iter().filter(|(_,v)|!*v).count()!=1 || repaired.iter().any(|(_,v)|!*v) {return Err("Unexpected assessment outcomes".into());}
    let at=schema::parse_instant(&h.at)?;let event=format!("assessment-{TASK}");
    let control_forms=retrieval::assessment_credit(&before,REPAIR_LEARNER,&original,&event,at)?;
    let fixed_forms=retrieval::assessment_credit(&before,REPAIR_LEARNER,&repaired,&event,at)?;
    let mut control=before.clone();apply_credit(&mut control,&control_forms,&identities)?;
    if dynamic_records(&control,&ids)!=dynamic_records(&post,&ids) || dynamic_ids(&control)?!=ids {
        std::fs::write(dir.join("mismatch.json"),serde_json::to_string_pretty(&json!({"predicted":dynamic_records(&control,&ids),"observed":dynamic_records(&post,&ids)}))?)?;
        return Err("Native control does not reproduce assessment learner state".into());
    }
    let mut fixed=before.clone();apply_credit(&mut fixed,&fixed_forms,&identities)?;
    if dynamic_ids(&fixed)?!=ids {return Err("Unexpected corrected profile membership change".into());}
    let old=dynamic_records(&current,&ids);let new=dynamic_records(&fixed,&ids);
    let mut forms=vec![];let mut changes=vec![];
    for (&id,record) in &old {
        let repaired=&new[&id];
        for attr in record.keys().chain(repaired.keys()).collect::<BTreeSet<_>>() {
            if record.get(attr)==repaired.get(attr) {continue;}
            if let Some(v)=repaired.get(attr) {forms.push(json!([kw("db/cas"),id,kw(attr),record.get(attr),v]));}
            else {forms.push(json!([kw("db/retract"),id,kw(attr),record[attr]]));}
            changes.push(json!({"entity":id,"attribute":attr,"before":record.get(attr),"after":repaired.get(attr)}));
        }
        if record!=repaired {forms.push(json!([kw("db/ensure"),id,kw(if record.contains_key("progress/id") {"progress/validate"}else{"performance/validate"})]));}
    }
    let base=current.entity(TASK)?["learner-task/xp-base"].as_i64().ok_or("Missing XP base")?;
    let xp=course_academy_engine::activities::earned_xp("assessment",base,chain.len(),chain.len(),None)?.to_string().parse::<i64>()?;
    let lifecycle=course_academy_engine::scheduling::lifecycle(&current,REPAIR_LEARNER)?;
    let audit=json!({"basis":db.basis_t(),"gradeBasis":h.t,"gradedAt":h.at,"task":TASK,"item":BAD_ITEM,"controlMatchesObserved":true,"noSubsequentLearnerStateChanges":true,"xpBefore":current.entity(TASK)?["learner-task/xp-earned"],"xpAfter":xp,"originalResults":original,"correctedResults":repaired,"dynamicChanges":changes,"originalRepairs":lifecycle.repairs.iter().map(|((o,t),k)|json!({"origin":o,"topic":t,"kind":k})).collect::<Vec<_>>()});
    std::fs::write(dir.join("dynamic-forms.edn"),schema::edn(&json!(forms))?+"\n")?;
    std::fs::write(dir.join("dynamic-before.json"),serde_json::to_string_pretty(&old)?+"\n")?;
    std::fs::write(dir.join("dynamic-after.json"),serde_json::to_string_pretty(&new)?+"\n")?;
    std::fs::write(dir.join("correction-audit.json"),serde_json::to_string_pretty(&audit)?+"\n")?;
    println!("{}",json!({"basis":db.basis_t(),"gradeBasis":h.t,"changedAttributes":changes.len(),"xpAfter":xp,"controlMatches":true}));
    Ok(())
}

#[path = "REPO_ROOT/engine/edb/answer_fields.rs"] mod repair_answer_fields;
#[path = "REPO_ROOT/engine/edb/configuration.rs"] mod repair_configuration;
#[path = "REPO_ROOT/engine/edb/progress.rs"] mod repair_progress;
fn repair_registry() -> Result<edb_core::NativeRegistry> {
    type Predicate=fn(&DatabaseValue,u64)->std::result::Result<bool,edb_core::SemanticError>;
    let mut builder=edb_core::NativeRegistry::builder();
    for (ns,name,predicate) in [
        ("course-academy.topic","valid-difficulty?",repair_configuration::valid_topic_difficulty as Predicate),
        ("course-academy.policy","valid?",repair_configuration::valid_policy as Predicate),
        ("course-academy.progress","valid-profile?",repair_progress::valid_profile as Predicate),
        ("course-academy.progress","valid-progress?",repair_progress::valid_progress as Predicate),
        ("course-academy.answer-field","valid?",repair_answer_fields::valid_field as Predicate)] {
        builder.entity_predicate(edb_core::Symbol::new(ns,name),move |db,e,c| {c.check(1)?;Ok(edb_core::RuntimeValue::Scalar(Value::Bool(predicate(db,e)?)))})?;
    }
    Ok(builder.build())
}
fn preview_repair(dir: &std::path::Path) -> Result<()> {
    let plan:Json=serde_json::from_str(&std::fs::read_to_string(dir.join("plan.json"))?)?;
    let conn=Connection::connect_configured(postgres_config_from_env()?,"math",512)?;
    let db=conn.db();
    if db.basis_t()!=plan["basis"].as_u64().ok_or("Missing basis")? {return Err("Stale repair basis".into());}
    let forms=edb_core::edn_transaction::read_edn_transaction(&std::fs::read_to_string(dir.join("transaction.edn"))?)?;
    let report=db.with_forms_with_execution_options(&forms,Utc::now().timestamp_millis(),engine_source(),Default::default(),&edb_core::TransactionExecutionOptions{native:repair_registry()?,..Default::default()})?;
    let s=snapshot(&report.db_after)?;
    let field=s.refs(s.reference(BAD_ITEM,"task-item/content")?,"question/answer-fields")?[0];
    let answer=s.reference(field,"answer-field/correct")?;
    if s.refs(BAD_ITEM,"task-item/responses")?!=vec![answer] {return Err("Response/key mismatch".into());}
    let draft=BTreeMap::from([(field,answer.to_string())]);
    if !learning::grade(&s,s.reference(BAD_ITEM,"task-item/content")?,&draft)? {return Err("Repaired response rejected by actual grader".into());}
    if status(&s,BAD_ITEM,"task-item/status")?!="correct" {return Err("Incorrect repaired status".into());}
    let chain=items(&s,TASK)?;
    if retrieval::xp(&s,s.reference(TASK,"learner-task/activity")?,&chain,15)?!=18 || s.entity(TASK)?["learner-task/xp-earned"]!=json!(18) {return Err("Full-mark XP mismatch".into());}
    let lifecycle=course_academy_engine::scheduling::lifecycle(&s,REPAIR_LEARNER)?;
    if lifecycle.repairs.contains_key(&(TASK,17592186048980)) || s.refs(REPAIR_LEARNER,"learner/activity")?.contains(&REVIEW) {return Err("Review obligation remains".into());}
    let expected:Json=serde_json::from_str(&std::fs::read_to_string(dir.parent().unwrap().join("native/dynamic-after.json"))?)?;
    if serde_json::to_value(dynamic_records(&s,&dynamic_ids(&s)?))?!=expected {return Err("Speculative learner state differs from native counterfactual".into());}
    let result=json!({"passed":true,"basisBefore":db.basis_t(),"correctResponse":answer,"correctValue":s.entity(answer)?["answer/value"],"xp":18,"reviewRemoved":true,"nativeGraderAccepted":true,"dynamicCounterfactualMatched":true,"taskJson":task_json(&s,REPAIR_LEARNER,TASK)?});
    std::fs::write(dir.join("application-preview.json"),serde_json::to_string_pretty(&result)?+"\n")?;
    println!("{}",json!({"passed":true,"xp":18,"reviewRemoved":true,"nativeGraderAccepted":true,"dynamicCounterfactualMatched":true}));
    Ok(())
}
fn main() {
    let args:Vec<_>=std::env::args().skip(1).collect();
    let (mode,path)=if args.len()==2 { (args[0].as_str(),args[1].as_str()) } else {("calculate",args.first().expect("directory required").as_str())};
    let dir=std::path::Path::new(path);
    let result=if mode=="preview" {preview_repair(dir)}else{correction(dir)};
    if let Err(e)=result {eprintln!("{e}");std::process::exit(1);}
}
