fn final_batch_audit()->Result<()> {
    let out=PathBuf::from("/tmp/course-academy-review-rule-final-batch");
    let replay:Json=serde_json::from_slice(&std::fs::read("/tmp/course-academy-review-rule-replay-output/report.json")?)?;
    if replay["committed"]!=false||replay["durableWrites"]!=0{return Err("unexpected replay report kind".into());}
    let mut app=Application::connect("math".into(),"59d5cf13-351c-4114-be19-4c3bb64ee051".into(),"/tmp/edb-math/writer.sock".into())?;
    let db=app.conn.sync()?;app.adopt(db.clone())?;
    let current=&app.snapshot;
    let engine_id=db.entid(&Keyword::new("application","ca-engine")).ok_or("missing engine attribution")?;
    let mut forms=replay["forms"].as_array().ok_or("missing retention forms")?.clone();
    let expected_tasks=BTreeSet::from([17592186639386u64,17592186654853u64,17592186653076u64]);
    let mut observed_tasks=BTreeSet::new();let mut progress_ids=BTreeSet::new();let mut original_times=vec![];
    let changes=forms.iter().filter_map(|f|Some((f.get(1)?.as_u64()?,f.get(2)?.get("$keyword")?.as_str()?.to_owned()))).collect::<BTreeSet<_>>();
    let mut guarded_fields=0;
    for case in replay["cases"].as_array().ok_or("missing replay cases")? {
        let task=case["task"].as_u64().ok_or("missing repaired task")?;
        if !observed_tasks.insert(task)||!expected_tasks.contains(&task)||case["controlMatchesCurrent"]!=true||case["allLaterRetentionWritesClassified"]!=true{return Err("incomplete or duplicate control replay".into());}
        for row in case["rows"].as_array().ok_or("missing progress rows")? {
            let progress=row["progress"].as_u64().ok_or("missing progress ID")?;
            if !progress_ids.insert(progress){return Err("overlapping independent progress rows require joint replay".into());}
            let actual=current.entity(progress)?;
            let captured=row["actual"].as_object().ok_or("missing captured factual row")?;
            for (a,v) in captured {
                if a.starts_with("progress/")&&!same_domain(v,actual.get(a).unwrap_or(&Json::Null)){return Err(format!("replay checkpoint stale progress={progress} attr={a}").into());}
            }
            for (a,v) in actual {
                if a.starts_with("progress/")&&!captured.contains_key(a){return Err("factual progress fields added after replay checkpoint".into());}
                if a.starts_with("progress/")&&!changes.contains(&(progress,a.clone())){forms.push(json!([kw("db/cas"),progress,kw(a),v,v]));guarded_fields+=1;}
            }
            if !forms.iter().any(|f|f.get(0)==Some(&kw("db/ensure"))&&f.get(1)==Some(&json!(progress))){forms.push(json!([kw("db/ensure"),progress,kw("progress/validate")]));}
        }
        if status(current,task,"learner-task/status")?!="failed"||current.entity(task)?.contains_key("learner-task/math-academy-id"){return Err("task is no longer a failed local attempt".into());}
        owned(current,app.learner_eid,task)?;
        let activity=current.reference(task,"learner-task/activity")?;
        if retrieval::kind(current,activity)?!="review"{return Err("repair target is not a review".into());}
        let chain=items(current,task)?;
        if chain.len()!=5{return Err("historical repair must preserve exactly five observed presentations".into());}
        let original=case["trace"].as_array().unwrap().iter().find(|event|event["correctedTerminal"]==true).ok_or("missing corrected original terminal")?;
        let original_at=original["at"].as_i64().ok_or("missing original finish time")?;
        let original_t=original["afterBasis"].as_u64().unwrap();
        let status_attr=db.schema().resolve_ident(&Keyword::new("learner-task","status")).unwrap();
        let terminal=db.clone().history().collect_datoms_with_prefix(&IndexPrefix::Eavt{entity:task,attribute:Some(status_attr),value:None})?.into_iter().find(|d|d.added&&edb_core::tx_to_t(d.tx).ok()==Some(original_t)).ok_or("original terminal attribution not retained")?;
        if terminal.source!=engine_id||current.ident(&value(&terminal.value)?)?!="learner-task.status/failed"{return Err("original outcome is not controller-attributed failure".into());}
        let instant_attr=db.schema().resolve_ident(&Keyword::new("db","txInstant")).unwrap();
        let tx_at=db.collect_datoms_with_prefix(&IndexPrefix::Eavt{entity:terminal.tx,attribute:Some(instant_attr),value:None})?.into_iter().find_map(|d|if let Value::Instant(v)=d.value{Some(v)}else{None}).ok_or("original transaction instant missing")?;
        if tx_at!=original_at{return Err("original journal/transaction finish time mismatch".into());}
        forms.push(json!([kw("db/cas"),task,kw("learner-task/status"),current.entities[&task]["learner-task/status"],kw("learner-task.status/completed")]));
        for a in ["learner-task/id","learner-task/activity","learner-task/xp-base","learner-task/xp-earned","learner-task/elapsed-seconds"]{if let Some(v)=current.entities[&task].get(a){forms.push(json!([kw("db/cas"),task,kw(a),v,v]));}}
        let finished=current.entities[&task].get("learner-task/finished-at").cloned().unwrap_or(Json::Null);
        if !finished.is_null()&&schema::parse_instant(&finished)?.timestamp_millis()!=original_at{return Err("existing finish date conflicts with original terminal".into());}
        forms.push(json!([kw("db/cas"),task,kw("learner-task/finished-at"),finished,{"$instant":original_at}]));
        for item in chain {
            let state=status(current,item,"task-item/status")?;
            if !matches!(state.as_str(),"correct"|"incorrect"|"skipped"){return Err("historical question outcome changed".into());}
            for a in ["task-item/id","task-item/status","task-item/content","task-item/elapsed-seconds"]{if let Some(v)=current.entities[&item].get(a){forms.push(json!([kw("db/cas"),item,kw(a),v,v]));}}
        }
        forms.push(json!([kw("db/ensure"),task,kw("learner-task/validate")]));
        original_times.push(json!({"task":task,"originalTerminalT":original_t,"originalFinishedAt":original_at,"xpBase":current.entities[&task].get("learner-task/xp-base"),"xpEarned":current.entities[&task].get("learner-task/xp-earned")}));
    }
    if observed_tasks!=expected_tasks||progress_ids!=BTreeSet::from([17592186408518u64,17592186409322u64,17592186408414u64,17592186408572u64,17592186408335u64]){return Err("historical batch is incomplete".into());}
    let edn=schema::edn(&json!(forms))?;
    let preview=audit_preview(&db,&edn)?;
    let allowed=BTreeSet::from(["db/txInstant","progress/learned","progress/repetitions","progress/memory","progress/memory-at","progress/interval-days","learner-task/status","learner-task/finished-at"]);
    let mut preview_datoms=vec![];
    for d in &preview.tx_data {
        let name=db.schema().attribute(d.attribute)?.ident.qualified_name();
        if d.source!=engine_id||!allowed.contains(name.as_str()){return Err(format!("preview changes protected state {name}").into());}
        if name.starts_with("progress/")&&!progress_ids.contains(&d.entity){return Err("preview touched progress outside replay union".into());}
        if name.starts_with("learner-task/")&&!expected_tasks.contains(&d.entity){return Err("preview touched unrelated task".into());}
        preview_datoms.push(json!({"entity":d.entity,"attribute":name,"value":value(&d.value)?,"source":d.source,"added":d.added}));
    }
    for case in replay["cases"].as_array().unwrap() {
        for row in case["rows"].as_array().unwrap() {
            let progress=row["progress"].as_u64().unwrap();
            let mut actual_after=Record::new();
            for d in preview.db_after.collect_datoms_with_prefix(&IndexPrefix::Eavt{entity:progress,attribute:None,value:None})? {let name=db.schema().attribute(d.attribute)?.ident.qualified_name();if name.starts_with("progress/"){actual_after.insert(name,value(&d.value)?);}}
            for (a,v) in row["desired"].as_object().unwrap() {if a.starts_with("progress/")&&!same_domain(v,actual_after.get(a).unwrap_or(&Json::Null)){return Err(format!("preview does not equal canonical replay progress={progress} attr={a}").into());}}
        }
    }
    let key=format!("review-five-success-historical-v1-{}",&course_academy_engine::core::fingerprint(&json!({"basis":db.basis_t(),"source":ENGINE_SOURCE,"forms":forms}))[..24]);
    let report=json!({"ready":true,"committed":false,"durableWrites":0,"basis":db.basis_t(),"replayBasis":replay["basis"],"source":ENGINE_SOURCE,"sourceEntity":engine_id,"requestKey":key,"progressRows":progress_ids,"tasks":observed_tasks,"originalFinishTimesAndPreservedXp":original_times,"allControlReplaysMatch":true,"allActualProgressFieldsRecheckedAndGuarded":true,"additionalFactualSelfGuards":guarded_fields,"allFiveObservedItemsPreserved":true,"previewDatoms":preview_datoms,"formCount":forms.len(),"forms":forms});
    std::fs::write(out.join("transaction.edn"),edn)?;
    std::fs::write(out.join("ready.json"),serde_json::to_vec_pretty(&report)?)?;
    std::fs::write(out.join("native-preview.json"),serde_json::to_vec_pretty(&json!({"committed":false,"dbBefore":db.basis_t(),"speculativeAfter":preview.db_after.basis_t(),"source":ENGINE_SOURCE,"sourceEntity":engine_id,"datoms":preview_datoms}))?)?;
    println!("{}",json!({"ready":true,"basis":db.basis_t(),"tasks":observed_tasks,"progressRows":progress_ids,"previewDatoms":preview.tx_data.len(),"out":out}));Ok(())
}
fn main(){if let Err(error)=final_batch_audit(){eprintln!("Final batch audit failed: {error}");std::process::exit(1);}}
