// Read-only counterfactual replay; appended to the exact learning API source.
const REPAIR_LEARNER: u64 = 17592186045416;
const BAD_ITEM: u64 = 17592186576280;


fn dynamic_ids(s: &EntitySnapshot) -> Result<BTreeSet<u64>> {
    let mut ids: BTreeSet<_> = s.refs(REPAIR_LEARNER, "learner/knowledge-profile")?.into_iter().collect();
    ids.extend(s.optional_ref(REPAIR_LEARNER, "learner/performance")?);
    Ok(ids)
}

fn dynamic_records(s: &EntitySnapshot, ids: &BTreeSet<u64>) -> BTreeMap<u64,Record> {
    ids.iter().filter_map(|id| s.entities.get(id).map(|record| (*id, record.clone()))).collect()
}

fn apply_credit_forms(s: &mut EntitySnapshot, forms: &[Json], identities: &BTreeMap<String,u64>) -> Result<()> {
    let mut temps=BTreeMap::new();
    for form in forms {
        if let Some(map)=form.as_object() {
            if let Some(temp)=map["db/id"].as_str() {
                let identity=map.get("progress/id").and_then(Json::as_str).ok_or("Only new progress records may use a tempid")?;
                temps.insert(temp.to_owned(),*identities.get(identity).ok_or("New progress identity absent from observed history")?);
            }
        }
    }

    let normalize = |v:&Json| -> Result<Json> {
        Ok(if v.get("$instant").is_some() {
            json!({"$instant":schema::parse_instant(v)?.timestamp_millis()})
        } else {v.clone()})
    };
    let mut changed = BTreeMap::new();
    for form in forms {
        if let Some(map) = form.as_object() {
            let eid = map["db/id"].as_u64().or_else(||map["db/id"].as_str().and_then(|t|temps.get(t).copied())).ok_or("Unknown entity during credit replay")?;
            let record = changed.entry(eid).or_insert_with(||s.entities.get(&eid).cloned().unwrap_or_default());
            for (attr,v) in map {
                if !matches!(attr.as_str(),"db/id"|"db/ensure") {
                    if attr=="learner/activity" {return Err("Unexpected task membership change during replay".into());}
                    if attr=="learner/knowledge-profile" {
                        if eid!=REPAIR_LEARNER {return Err("Another learner's membership changed".into());}
                        let mut links=record.get(attr).and_then(Json::as_array).cloned().unwrap_or_default();
                        for link in v.as_array().ok_or("Profile links must be an array")? {
                            let target=link.as_u64().or_else(||link.as_str().and_then(|t|temps.get(t).copied())).ok_or("Unknown profile tempid")?;
                            if !links.contains(&json!(target)) {links.push(json!(target));}
                        }
                        links.sort_by_key(|id|id.as_u64());
                        record.insert(attr.clone(),json!(links));
                    } else {record.insert(attr.clone(),normalize(v)?);}
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
    let bad_events=current.status_history.iter().filter(|h| h.entity==BAD_ITEM && h.attribute=="task-item/status")
        .filter(|h| current.ident(&h.value).ok().as_deref()==Some("task-item.status/correct")).collect::<Vec<_>>();
    if bad_events.len()!=1 {return Err("Expected exactly one correct event for bad item".into());}
    let bad_t=bad_events[0].t;
    let mut control=snapshot(&db.clone().as_of(bad_t-1))?;
    let mut omitted=control.clone();
    let ids=dynamic_ids(&current)?;
    let initial_ids=dynamic_ids(&control)?;
    if !initial_ids.is_subset(&ids) {return Err("A learner profile was removed since bad event".into());}
    let identities=current.entities.with_attribute("progress/id").into_iter().map(|id|Ok((current.entity(id)?["progress/id"].as_str().ok_or("Invalid progress identity")?.to_owned(),id))).collect::<Result<BTreeMap<_,_>>>()?;
    let mut control_links=control.refs(REPAIR_LEARNER,"learner/knowledge-profile")?.into_iter().collect::<BTreeSet<_>>();
    let initial=dynamic_records(&control,&ids);
    let history=db.clone().history();
    let mut changes: BTreeMap<u64,Vec<(u64,String,Json,bool)>>=BTreeMap::new();
    for &entity in &ids {
        for d in history.collect_datoms_with_prefix(&IndexPrefix::Eavt {entity,attribute:None,value:None})? {
            let t=edb_core::tx_to_t(d.tx)?;
            if t<bad_t {continue;}
            let attr=db.schema().attribute(d.attribute)?.ident.qualified_name();
            changes.entry(t).or_default().push((entity,attr,value(&d.value)?,d.added));
        }
    }
    let profile_attr=db.schema().resolve_ident(&edb_core::Keyword::new("learner","knowledge-profile")).ok_or("Missing profile schema")?;
    for d in history.collect_datoms_with_prefix(&IndexPrefix::Eavt {entity:REPAIR_LEARNER,attribute:Some(profile_attr),value:None})? {
        let t=edb_core::tx_to_t(d.tx)?;
        if t>=bad_t {changes.entry(t).or_default().push((REPAIR_LEARNER,"learner/knowledge-profile".into(),value(&d.value)?,d.added));}
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
                if entity==REPAIR_LEARNER {if !control_links.remove(&v.as_u64().ok_or("Profile ref required")?) {return Err("Membership retraction mismatch".into());} continue;}
                let record=actual.get_mut(&entity).ok_or("Unexpected new progress entity")?;
                if record.get(attr)!=Some(v) {return Err(format!("Historical retraction mismatch at {t}: {entity} {attr}").into());}
                record.remove(attr);
            }
        }
        for &(entity,ref attr,ref v,added) in datoms {
            if added {
                if entity==REPAIR_LEARNER {if !control_links.insert(v.as_u64().ok_or("Profile ref required")?) {return Err("Membership assertion mismatch".into());} continue;}
                actual.entry(entity).or_default().insert(attr.clone(),v.clone());
            }
        }
        apply_credit_forms(&mut control,&forms,&identities)?;
        if control.refs(REPAIR_LEARNER,"learner/knowledge-profile")?.into_iter().collect::<BTreeSet<_>>()!=control_links {return Err("Native control profile membership mismatch".into());}
        let predicted=dynamic_records(&control,&ids);
        if predicted!=actual {
            let mismatch=ids.iter().filter(|id|predicted.get(id)!=actual.get(id)).map(|id|json!({"id":id,"predicted":predicted.get(id),"actual":actual.get(id)})).collect::<Vec<_>>();
            std::fs::write(dir.join("control-mismatch.json"),serde_json::to_string_pretty(&json!({"basis":t,"mismatch":mismatch}))?)?;
            return Err(format!("Native control replay mismatched original transaction {t}").into());
        }
        let removed=h.entity==BAD_ITEM;
        if removed && t!=bad_t {return Err("Bad item transaction changed".into());}
        if !removed {
            let corrected=learning::credit(&omitted,REPAIR_LEARNER,activity,Some(question),correct,false,&event_id,at)?;
            apply_credit_forms(&mut omitted,&corrected,&identities)?;
        }
        let changed=datoms.iter().map(|(e,_,_,_)|*e).collect::<BTreeSet<_>>();
        events.push(json!({"basis":t,"item":h.entity,"task":task,"activity":activity,"question":question,"correct":correct,"at":h.at,"removed":removed,"controlMatched":true,"changedEntities":changed}));
    }
    if events.iter().filter(|e|e["removed"]==true).count()!=1 {return Err("Replay did not remove exactly one event".into());}
    if dynamic_records(&control,&ids)!=dynamic_records(&current,&ids) || dynamic_ids(&control)?!=dynamic_ids(&current)? {return Err("Control replay does not equal current learner state".into());}
    let before=dynamic_records(&current,&ids);
    let after=dynamic_records(&omitted,&ids);
    let mut forms=vec![];
    let mut changed=vec![];
    let mut detached_profiles=vec![];
    for &eid in &ids {
        let old=&before[&eid];
        let Some(new)=after.get(&eid) else {
            if initial_ids.contains(&eid) || !old.contains_key("progress/id") {return Err("Only a profile created by the omitted event may disappear".into());}
            if dynamic_ids(&omitted)?.contains(&eid) {return Err("Missing profile is still owned in counterfactual".into());}
            forms.push(json!([kw("db/retract"),REPAIR_LEARNER,kw("learner/knowledge-profile"),eid]));
            detached_profiles.push(eid);
            continue;
        };
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
    if !detached_profiles.is_empty() {forms.push(json!([kw("db/ensure"),REPAIR_LEARNER,kw("learner/validate")]));}
    let audit=json!({"detachedProfiles":detached_profiles,"archivedProfileRecordsRetained":true,"basis":db.basis_t(),"badBasis":bad_t,"badItem":BAD_ITEM,"learner":REPAIR_LEARNER,"nativeControlMatchedEveryTransaction":true,"nativeControlEqualsCurrent":true,"retentionEvents":0,"events":events,"changes":changed,"formCount":forms.len(),"dynamicEntityCount":ids.len()});
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
