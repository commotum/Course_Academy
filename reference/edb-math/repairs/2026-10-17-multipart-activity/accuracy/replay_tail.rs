// Read-only counterfactual replay; appended to the exact learning API source.
const REPAIR_LEARNER: u64 = 17592186045416;
const BAD_ITEM: u64 = 17592186576138;
const BAD_T: u64 = 3377;

fn dynamic_ids(s: &EntitySnapshot) -> Result<BTreeSet<u64>> {
    let mut ids: BTreeSet<_> = s.refs(REPAIR_LEARNER, "learner/knowledge-profile")?.into_iter().collect();
    ids.extend(s.optional_ref(REPAIR_LEARNER, "learner/performance")?);
    Ok(ids)
}

fn dynamic_records(s: &EntitySnapshot, ids: &BTreeSet<u64>) -> BTreeMap<u64,Record> {
    ids.iter().filter_map(|id| s.entities.get(id).map(|record| (*id, record.clone()))).collect()
}

fn apply_credit_forms(s: &mut EntitySnapshot, forms: &[Json]) -> Result<()> {
    let normalize = |v:&Json| -> Result<Json> {
        Ok(if v.get("$instant").is_some() {
            json!({"$instant":schema::parse_instant(v)?.timestamp_millis()})
        } else {v.clone()})
    };
    let mut changed = BTreeMap::new();
    for form in forms {
        if let Some(map) = form.as_object() {
            let Some(eid) = map["db/id"].as_u64() else {
                return Err(format!("Unexpected new entity during credit replay: {}",map["db/id"]).into());
            };
            let record = changed.entry(eid).or_insert_with(||s.entities[&eid].clone());
            for (attr,v) in map {
                if !matches!(attr.as_str(),"db/id"|"db/ensure") {
                    if matches!(attr.as_str(),"learner/knowledge-profile"|"learner/activity") {
                        return Err("Unexpected membership change during replay".into());
                    }
                    record.insert(attr.clone(),normalize(v)?);
                }
            }
        } else {
            let f = form.as_array().ok_or("Invalid credit form")?;
            if f[0] != kw("db/retract") {return Err("Unexpected non-retract operation".into());}
            let eid = f[1].as_u64().ok_or("Retraction requires existing entity")?;
            let attr = f[2]["$keyword"].as_str().ok_or("Missing retraction attribute")?;
            let record = changed.entry(eid).or_insert_with(||s.entities[&eid].clone());
            if record.get(attr) != Some(&normalize(&f[3])?) {return Err("Retraction did not match existing value".into());}
            record.remove(attr);
        }
    }
    s.replace_records(changed,s.basis_t)?;
    Ok(())
}

fn run_accuracy() -> Result<()> {
    let dir=std::path::PathBuf::from(std::env::args().nth(1).ok_or("output directory required")?);
    let connection=Connection::connect_configured(postgres_config_from_env()?,"math",512)?;
    let db=connection.db();
    let current=snapshot(&db)?;
    let mut control=snapshot(&db.clone().as_of(BAD_T-1))?;
    let mut omitted=control.clone();
    let ids=dynamic_ids(&current)?;
    if ids != dynamic_ids(&control)? {return Err("Learner dynamic entity membership changed since bad event".into());}
    let initial=dynamic_records(&control,&ids);
    let history=db.clone().history();
    let mut changes: BTreeMap<u64,Vec<(u64,String,Json,bool)>>=BTreeMap::new();
    for &entity in &ids {
        for d in history.collect_datoms_with_prefix(&IndexPrefix::Eavt {entity,attribute:None,value:None})? {
            let t=edb_core::tx_to_t(d.tx)?;
            if t<BAD_T {continue;}
            let attr=db.schema().attribute(d.attribute)?.ident.qualified_name();
            changes.entry(t).or_default().push((entity,attr,value(&d.value)?,d.added));
        }
    }
    // The event interpretation must use the same curriculum and policy. A
    // content repair after grading is harmless unless its native input differs.
    for attr in ["policy/id","encompassing/id"] {
        let before=control.entities.with_attribute(attr).into_iter().map(|id|(id,control.entities[&id].clone())).collect::<BTreeMap<_,_>>();
        let after=current.entities.with_attribute(attr).into_iter().map(|id|(id,current.entities[&id].clone())).collect::<BTreeMap<_,_>>();
        if before!=after {return Err(format!("{attr} records changed during replay interval").into());}
    }
    let mut events=vec![];
    for (&t,datoms) in &changes {
        let graded=current.status_history.iter().filter(|h| h.t==t && h.attribute=="task-item/status")
            .filter_map(|h| match current.ident(&h.value).ok().as_deref() {
                Some("task-item.status/correct") => Some((h,true)),
                Some("task-item.status/incorrect") => Some((h,false)),
                _=>None,
            }).filter(|(h,_)| current.owners(h.entity,"learner-task/items").ok()
                .is_some_and(|owners| owners.iter().any(|task| current.refs(REPAIR_LEARNER,"learner/activity").unwrap().contains(task))))
            .collect::<Vec<_>>();
        if graded.len()!=1 {return Err(format!("Dynamic-state transaction {t} has {} graded events; cannot silently replay",graded.len()).into());}
        let (h,correct)=graded[0];
        let task=current.owners(h.entity,"learner-task/items")?[0];
        let activity=current.reference(task,"learner-task/activity")?;
        if retrieval::kind(&current,activity)? != "lesson" {return Err("Expected only lesson accuracy events".into());}
        let question=current.reference(h.entity,"task-item/content")?;
        let at=schema::parse_instant(&h.at)?;
        let event_id=format!("item-{}",h.entity);
        // The historical content inputs are still present in the pre-event
        // snapshot. Both branches execute exactly the same native credit path.
        let forms=learning::credit(&control,REPAIR_LEARNER,activity,Some(question),correct,false,&event_id,at)?;
        let mut actual=dynamic_records(&control,&ids);
        // Retractions happen before assertions for cardinality-one updates.
        for &(entity,ref attr,ref v,added) in datoms {
            if !added {
                let record=actual.get_mut(&entity).ok_or("Unexpected new progress entity")?;
                if record.get(attr)!=Some(v) {return Err(format!("Historical retraction mismatch at {t}: {entity} {attr}").into());}
                record.remove(attr);
            }
        }
        for &(entity,ref attr,ref v,added) in datoms {
            if added {actual.get_mut(&entity).unwrap().insert(attr.clone(),v.clone());}
        }
        apply_credit_forms(&mut control,&forms)?;
        let predicted=dynamic_records(&control,&ids);
        if predicted!=actual {
            let mismatch=ids.iter().filter(|id|predicted.get(id)!=actual.get(id)).map(|id|json!({"id":id,"predicted":predicted.get(id),"actual":actual.get(id)})).collect::<Vec<_>>();
            std::fs::write(dir.join("control-mismatch.json"),serde_json::to_string_pretty(&json!({"basis":t,"mismatch":mismatch}))?)?;
            return Err(format!("Native control replay mismatched original transaction {t}").into());
        }
        let removed=h.entity==BAD_ITEM;
        if removed && t!=BAD_T {return Err("Bad item transaction changed".into());}
        if !removed {
            let corrected=learning::credit(&omitted,REPAIR_LEARNER,activity,Some(question),correct,false,&event_id,at)?;
            apply_credit_forms(&mut omitted,&corrected)?;
        }
        let changed=datoms.iter().map(|(e,_,_,_)|*e).collect::<BTreeSet<_>>();
        events.push(json!({"basis":t,"item":h.entity,"task":task,"activity":activity,"question":question,"correct":correct,"at":h.at,"removed":removed,"controlMatched":true,"changedEntities":changed}));
    }
    if events.iter().filter(|e|e["removed"]==true).count()!=1 {return Err("Replay did not remove exactly one event".into());}
    if dynamic_records(&control,&ids)!=dynamic_records(&current,&ids) {return Err("Control replay does not equal current learner state".into());}
    let before=dynamic_records(&current,&ids);
    let after=dynamic_records(&omitted,&ids);
    let mut forms=vec![];
    let mut changed=vec![];
    for &eid in &ids {
        let old=&before[&eid];let new=&after[&eid];
        if old==new {continue;}
        let attrs=old.keys().chain(new.keys()).collect::<BTreeSet<_>>();
        let mut fields=vec![];
        for attr in attrs {
            if old.get(attr)==new.get(attr) {continue;}
            if !matches!(attr.as_str(),"progress/practice-accuracy"|"progress/practice-mass"|"progress/expected-practice-accuracy"|"progress/last-direct-at"|"performance/practice-accuracy"|"performance/practice-mass") {
                return Err(format!("Unexpected counterfactual effect {eid}/{attr}").into());
            }
            if let Some(v)=new.get(attr) {
                forms.push(json!([kw("db/cas"),eid,kw(attr),old.get(attr),v]));
            } else {
                forms.push(json!([kw("db/retract"),eid,kw(attr),old[attr]]));
            }
            fields.push(json!({"attribute":attr,"before":old.get(attr),"after":new.get(attr)}));
        }
        forms.push(json!([kw("db/ensure"),eid,kw(if old.contains_key("progress/id") {"progress/validate"}else{"performance/validate"})]));
        changed.push(json!({"entity":eid,"fields":fields}));
    }
    let audit=json!({"basis":db.basis_t(),"badBasis":BAD_T,"badItem":BAD_ITEM,"learner":REPAIR_LEARNER,"nativeControlMatchedEveryTransaction":true,"nativeControlEqualsCurrent":true,"retentionEvents":0,"events":events,"changes":changed,"formCount":forms.len(),"dynamicEntityCount":ids.len()});
    std::fs::write(dir.join("accuracy-forms.edn"),schema::edn(&json!(forms))?+"\n")?;
    std::fs::write(dir.join("accuracy-forms.json"),serde_json::to_string_pretty(&forms)?+"\n")?;
    std::fs::write(dir.join("before.json"),serde_json::to_string_pretty(&before)?+"\n")?;
    std::fs::write(dir.join("after.json"),serde_json::to_string_pretty(&after)?+"\n")?;
    std::fs::write(dir.join("initial.json"),serde_json::to_string_pretty(&initial)?+"\n")?;
    std::fs::write(dir.join("audit.json"),serde_json::to_string_pretty(&audit)?+"\n")?;
    println!("{}",serde_json::to_string_pretty(&audit)?);
    Ok(())
}

fn main() {if let Err(e)=run_accuracy() {eprintln!("{e}");std::process::exit(1);}}
