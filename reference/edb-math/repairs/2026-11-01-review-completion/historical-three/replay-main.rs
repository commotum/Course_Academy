const RETENTION:&[&str]=&["progress/learned","progress/repetitions","progress/memory","progress/memory-at","progress/interval-days"];
fn audit_record(db:&DatabaseValue,id:u64)->Result<Record>{
    let mut row=Record::new();
    for d in db.collect_datoms_with_prefix(&IndexPrefix::Eavt{entity:id,attribute:None,value:None})?{
        let a=db.schema().attribute(d.attribute)?;let name=a.ident.qualified_name();
        if name.starts_with("db/"){continue;}
        let v=value(&d.value)?;
        if a.cardinality==Cardinality::Many{row.entry(name).or_insert(json!([])).as_array_mut().unwrap().push(v);}else{row.insert(name,v);}
    }Ok(row)
}
fn replay_credit(s:&EntitySnapshot,after:&DatabaseValue,l:u64,journal:&Json,override_pass:Option<bool>)->Result<Vec<Json>>{
    let body=&journal["input"];let task=required(body,"taskId")?;let a=s.reference(task,"learner-task/activity")?;
    let at=DateTime::from_timestamp_millis(journal["at"].as_i64().ok_or("missing original event time")?).unwrap();
    match body["action"].as_str().ok_or("missing action")?{
        "answer"=>{let item=required(body,"itemId")?;let q=s.reference(item,"task-item/content")?;let row=audit_record(after,item)?;let outcome=s.ident(row.get("task-item/status").ok_or("missing after answer status")?)?;
            if !matches!(outcome.as_str(),"task-item.status/correct"|"task-item.status/incorrect"){return Err("answer has no recorded submitted outcome".into());}
            Ok(learning::credit(s,l,a,Some(q),outcome.ends_with("/correct"),false,&format!("item-{item}"),at)?)},
        "continue"=>{let row=audit_record(after,task)?;let state=s.ident(row.get("learner-task/status").ok_or("missing terminal status")?)?;
            if !matches!(state.as_str(),"learner-task.status/completed"|"learner-task.status/failed"){return Err("continue is not a terminal retention event".into());}
            Ok(learning::credit(s,l,a,None,override_pass.unwrap_or(state.ends_with("/completed")),true,&format!("task-{task}"),at)?)},
        "submit"|"expire"=>{if retrieval::kind(s,a)?!="assessment"{return Err("unclassified non-assessment submit/expire".into());}
            let mut results=vec![];
            for item in items(s,task)?{let old=status(s,item,"task-item/status")?;if matches!(old.as_str(),"correct"|"incorrect"){continue;}
                let row=audit_record(after,item)?;let state=s.ident(row.get("task-item/status").ok_or("missing after assessment status")?)?;
                if matches!(state.as_str(),"task-item.status/correct"|"task-item.status/incorrect"){results.push((s.reference(item,"task-item/content")?,state.ends_with("/correct")));}}
            Ok(retrieval::assessment_credit(s,l,&results,&format!("assessment-{task}"),at)?)},
        other=>Err(format!("unclassified semantic event {other}").into())
    }
}
fn apply_progress(record:&mut Record,forms:&[Json],topic:u64){
    for form in forms{if form.get("progress/topic")==Some(&json!(topic)){for (a,v) in form.as_object().unwrap(){if a.starts_with("progress/"){record.insert(a.clone(),v.clone());}}}}
}
fn replay_main()->Result<()>{
    let out=PathBuf::from("/tmp/course-academy-review-rule-replay-output");std::fs::create_dir_all(&out)?;
    let manifest:Json=serde_json::from_slice(&std::fs::read("/tmp/course-academy-review-rule-replay-manifest.json")?)?;
    let conn=Connection::connect_configured(postgres_config_from_env()?,"math",256)?;let db=conn.db();
    let current=snapshot(&db)?;let l=current.entities.with_attribute("learner/id").into_iter().find(|id|current.entities[id]["learner/id"]=="59d5cf13-351c-4114-be19-4c3bb64ee051").ok_or("learner missing")?;
    let mut reports=vec![];let mut all_forms=vec![];let mut capture_cache:Option<(u64,EntitySnapshot)>=None;let mut capture_verified=false;
    for (task_text,entry) in manifest.as_object().unwrap(){
        let task=task_text.parse::<u64>()?;
        let completed_path=out.join(format!("task-{task}.json"));
        if completed_path.exists(){let previous:Json=serde_json::from_slice(&std::fs::read(&completed_path)?)?;
            let mut unchanged=previous["currentBasis"]==db.basis_t();
            for row in previous["rows"].as_array().unwrap(){let actual=current.entity(row["progress"].as_u64().unwrap())?;for(a,v)in row["actual"].as_object().unwrap(){if !same_domain(v,actual.get(a).unwrap_or(&Json::Null)){unchanged=false;}}}
            if unchanged{all_forms.extend(previous["forms"].as_array().unwrap().iter().cloned());reports.push(previous);eprintln!("reused fully verified case {task}");continue;}
        }
        let progress_ids=entry["progressIds"].as_array().unwrap().iter().map(|v|v.as_u64().unwrap()).collect::<BTreeSet<_>>();
        let topics=progress_ids.iter().map(|id|Ok((*id,current.reference(*id,"progress/topic")?))).collect::<Result<BTreeMap<_,_>>>()?;
        let mut events=vec![json!({"basis":entry["basis"],"path":entry["journal"],"originalCorrection":true})];events.extend(entry["laterWrites"].as_array().unwrap().iter().cloned());
        events.sort_by_key(|event|event["basis"].as_u64().unwrap());events.dedup_by_key(|event|event["basis"].as_u64().unwrap());
        let mut corrected=BTreeMap::<u64,Record>::new();let mut control=BTreeMap::<u64,Record>::new();let mut trace=vec![];let mut covered=BTreeSet::new();
        for event in events{
            let basis=event["basis"].as_u64().unwrap();covered.insert(basis+1);
            let journal:Json=serde_json::from_slice(&std::fs::read(event["path"].as_str().unwrap())?)?;
            if journal["basis"]!=basis||journal["source"]!="application/ca-engine"{return Err("journal provenance mismatch".into());}
            let before_db=db.clone().as_of(basis);let after_db=db.clone().as_of(basis+1);
            let started=Instant::now();let mut before=if let Some((from,mut previous))=capture_cache.take(){
                replay_capture(&db,from,basis,&mut previous)?;
                if !capture_verified {
                    let full=snapshot(&before_db)?;
                    if serde_json::to_value(&previous.status_history)?!=serde_json::to_value(&full.status_history)?||previous.entities!=full.entities{return Err(format!("incremental/full historical capture mismatch {from}->{basis}").into());}
                    capture_verified=true;eprintln!("incremental/full exact records+clock parity verified {from}->{basis}");
                }
                previous
            }else{snapshot(&before_db)?};eprintln!("captured task={task} before={basis} elapsed={:.3}s",started.elapsed().as_secs_f64());
            let mut actual_before=BTreeMap::new();let mut actual_after=BTreeMap::new();
            for &progress in &progress_ids {
                let row=before.entity(progress)?.clone();
                if let Some(previous)=control.get(&progress){for &a in RETENTION{if !same_domain(previous.get(a).unwrap_or(&Json::Null),row.get(a).unwrap_or(&Json::Null)){return Err(format!("unexplained intermediate retention write task={task} progress={progress} before={basis} attr={a}").into());}}}
                actual_before.insert(progress,row);actual_after.insert(progress,audit_record(&after_db,progress)?);
            }
            let mut baseline=replay_credit(&before,&after_db,l,&journal,None)?;
            if event["originalCorrection"]==true {
                // These October20 attempts predate October28's failed-review
                // memory refresh. Reproduce their actual historical policy.
                let at=DateTime::from_timestamp_millis(journal["at"].as_i64().unwrap()).unwrap();
                let mut capture=before.clone();let complete=before.refs(l,"learner/knowledge-profile")?.into_iter().filter(|id|["progress/repetitions","progress/memory","progress/memory-at","progress/interval-days","progress/learned","progress/assessment-accuracy","progress/practice-accuracy","progress/assessment-mass","progress/practice-mass"].iter().all(|a|before.entities[id].contains_key(*a))).collect::<Vec<_>>();
                capture.entities.get_mut(&l).unwrap().insert("learner/knowledge-profile".into(),json!(complete));
                let loaded=schema::load_runtime(capture,l,before.entities.with_attribute("policy/id")[0])?;let mut engine=loaded.engine.clone();engine.policy.failed_review_refresh_fraction=0.0;
                let activity=before.reference(task,"learner-task/activity")?;let target=before.reference(activity,"activity/scope")?;
                engine.apply_retention(course_academy_engine::core::Event{id:format!("historical-failure-{task}"),learner:loaded.learner.clone(),topic:loaded.topic_eid_to_id[&target].clone(),at:schema::timestamp_days(at),passed:false,kind:"review".into(),..Default::default()})?;
                for form in &mut baseline {if let Some(topic)=form.get("progress/topic").and_then(Json::as_u64){if let Some(state)=engine.states.get(&loaded.learner).and_then(|states|states.get(&loaded.topic_eid_to_id[&topic])){form["progress/memory"]=json!(state.memory);}}}
            }
            let mut old=actual_before.clone();let mut mismatches=vec![];
            for (&progress,row) in &mut old {
                apply_progress(row,&baseline,topics[&progress]);
                for (a,v) in row.iter(){if a.starts_with("progress/")&&!same_domain(v,actual_after[&progress].get(a).unwrap_or(&Json::Null)){mismatches.push(json!({"progress":progress,"attribute":a,"canonical":v,"recorded":actual_after[&progress].get(a)}));}}
            }
            if !mismatches.is_empty(){let report=json!({"task":task,"basis":basis,"blocker":"unchanged canonical replay differs from recorded result","mismatches":mismatches});std::fs::write(out.join(format!("blocked-{task}-{basis}.json")),serde_json::to_vec_pretty(&report)?)?;return Err(format!("unchanged replay mismatch task={task} basis={basis}").into());}
            control=old.clone();
            let mut replacements=BTreeMap::new();
            for (&progress,previous) in &corrected{let mut row=actual_before[&progress].clone();for &a in RETENTION{if let Some(v)=previous.get(a){row.insert(a.into(),v.clone());}else{row.remove(a);}}replacements.insert(progress,row);}
            before.replace_records(replacements,before.basis_t)?;
            let changed=replay_credit(&before,&after_db,l,&journal,(event["originalCorrection"]==true).then_some(true))?;
            let mut desired=BTreeMap::new();
            for &progress in &progress_ids {
                let mut row=before.entity(progress)?.clone();apply_progress(&mut row,&changed,topics[&progress]);
                for (a,v) in &row{if a.contains("accuracy")||a.ends_with("-mass"){if !same_domain(v,actual_after[&progress].get(a).unwrap_or(&Json::Null)){return Err(format!("replay would change factual answer evidence task={task} basis={basis} progress={progress} attr={a}").into());}}}
                desired.insert(progress,row);
            }
            trace.push(json!({"beforeBasis":basis,"afterBasis":basis+1,"at":journal["at"],"action":journal["input"]["action"],"eventTask":journal["input"]["taskId"],"journal":event["path"],"correctedTerminal":event["originalCorrection"]==true,"controlReproduced":true,"historicalFailureRefreshDisabled":event["originalCorrection"]==true,"control":old,"corrected":desired,"seconds":started.elapsed().as_secs_f64()}));
            corrected=desired;
            before.replace_records(actual_before,before.basis_t)?;capture_cache=Some((basis,before));
            eprintln!("replay task={task} basis={basis} action={} verified elapsed={:.3}s",journal["input"]["action"],started.elapsed().as_secs_f64());
        }
        let mut forms=vec![];let mut final_rows=vec![];
        let attr_ids=RETENTION.iter().map(|a|{let(ns,name)=a.split_once('/').unwrap();db.schema().resolve_ident(&Keyword::new(ns,name)).ok_or_else(||format!("missing attr {a}"))}).collect::<std::result::Result<BTreeSet<_>,_>>()?;
        for &progress in &progress_ids {
            let old=&control[&progress];let desired=&corrected[&progress];let actual=current.entity(progress)?;
            for &a in RETENTION{if !same_domain(old.get(a).unwrap_or(&Json::Null),actual.get(a).unwrap_or(&Json::Null)){return Err(format!("control does not reproduce current retention task={task} progress={progress} attr={a}").into());}}
            for d in db.clone().history().collect_datoms_with_prefix(&IndexPrefix::Eavt{entity:progress,attribute:None,value:None})?{let t=edb_core::tx_to_t(d.tx)?;if t>entry["basis"].as_u64().unwrap()&&attr_ids.contains(&d.attribute)&&!covered.contains(&t){return Err(format!("unclassified retention datom task={task} progress={progress} t={t}").into());}}
            let start=forms.len();for &a in RETENTION{let from=actual.get(a).cloned().unwrap_or(Json::Null);let to=desired.get(a).cloned().unwrap_or(Json::Null);if !same_domain(&from,&to){forms.push(json!([kw("db/cas"),progress,kw(a),from,to]));}}
            if forms.len()>start{forms.push(json!([kw("db/ensure"),progress,kw("progress/validate")]));}
            final_rows.push(json!({"progress":progress,"topic":topics[&progress],"actual":actual,"desired":desired}));
        }
        all_forms.extend(forms.clone());
        reports.push(json!({"task":task,"currentBasis":db.basis_t(),"controlMatchesCurrent":true,"allLaterRetentionWritesClassified":true,"rows":final_rows,"trace":trace,"forms":forms}));
        std::fs::write(out.join(format!("task-{task}.json")),serde_json::to_vec_pretty(reports.last().unwrap())?)?;
    }
    std::fs::write(out.join("report.json"),serde_json::to_vec_pretty(&json!({"committed":false,"durableWrites":0,"basis":db.basis_t(),"cases":reports,"forms":all_forms}))?)?;
    std::fs::write(out.join("retention-only.edn"),schema::edn(&json!(all_forms))?)?;
    println!("Replay verified {} cases at basis{}; no writes; {}",reports.len(),db.basis_t(),out.display());Ok(())
}
fn main(){if let Err(error)=replay_main(){eprintln!("Replay audit failed: {error}");std::process::exit(1);}}
