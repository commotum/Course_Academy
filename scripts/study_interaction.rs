//! Local study projections. Only the existing guarded process path can commit.
//! The outbox stores a small record overlay and the original operation before
//! acknowledging it. Provisional entity IDs never cross the EDB write boundary.
use super::*;
use edb_core::ValueType;
const LOCAL_ID: u64 = 4_000_000_000_000_000;
pub(super) struct Projection {
    snapshot: EntitySnapshot,
    touched: BTreeSet<u64>,
    fingerprint: String,
}


fn attr<'a>(db: &'a DatabaseValue, name: &str) -> Result<&'a edb_core::Attribute> {
    let (ns,n)=name.split_once('/').ok_or("Invalid attribute")?;
    let id=db.schema().resolve_ident(&Keyword::new(ns,n)).ok_or("Unknown study attribute")?;
    Ok(db.schema().attribute(id)?)
}
fn ident(v:&Json)->Result<&str>{v.get("$keyword").and_then(Json::as_str).or_else(||v.as_str()).ok_or("Expected keyword".into())}
fn resolve(s:&EntitySnapshot, ids:&BTreeMap<String,u64>, v:&Json)->Result<u64>{
    if let Some(id)=v.as_u64(){return Ok(id)}
    if let Some(name)=v.as_str(){return ids.get(name).copied().ok_or_else(||format!("Unresolved local entity {name}").into())}
    let name=ident(v)?;
    s.entities.with_attribute("db/ident").into_iter().find(|id|s.entities[id].get("db/ident").is_some_and(|v|s.ident(v).ok().as_deref()==Some(name))).ok_or_else(||format!("Unknown local ident {name}").into())
}
fn canonical(s:&EntitySnapshot,db:&DatabaseValue,ids:&BTreeMap<String,u64>,a:&str,v:&Json)->Result<Json>{
    if attr(db,a)?.value_type==ValueType::Ref {Ok(json!(resolve(s,ids,v)?))}else{Ok(v.clone())}
}
fn collect_ids(s:&EntitySnapshot, forms:&[Json])->Result<BTreeMap<String,u64>>{
    let mut ids=BTreeMap::new();
    let mut next=LOCAL_ID.checked_add(s.basis_t.checked_mul(65536).ok_or("Study basis exhausted")?).ok_or("Study basis exhausted")?;
    for form in forms {
        if let Some(name)=form.get("db/id").and_then(Json::as_str){
            if !ids.contains_key(name){
                // Unique identities upsert in EDB. Mirror that for resumed clocks
                // and progress maps rather than creating duplicate local records.
                let existing=form.as_object().unwrap().iter().filter(|(a,_)|a.ends_with("/id")).find_map(|(a,v)|s.entities.with_attribute(a).into_iter().find(|id|s.entities[id].get(a)==Some(v)));
                ids.insert(name.into(),existing.unwrap_or_else(||{let id=next;next+=1;id}));
            }
        }
    }
    Ok(ids)
}
fn apply_in_place(s:&mut EntitySnapshot,db:&DatabaseValue,forms:&[Json],at:DateTime<Utc>)->Result<BTreeMap<String,u64>>{
    let ids=collect_ids(s,forms)?;
    let mut changed=BTreeMap::<(u64,String),Vec<Json>>::new();
    let mut retractions=vec![];
    for form in forms {
        if let Some(map)=form.as_object(){
            let id=resolve(s,&ids,&map["db/id"])?;
            for (a,v) in map {
                if matches!(a.as_str(),"db/id"|"db/ensure"){continue;}
                let values=if attr(db,a)?.cardinality==Cardinality::Many{v.as_array().ok_or("Many attribute needs values")?.clone()}else{vec![v.clone()]};
                for v in values{changed.entry((id,a.clone())).or_default().push(canonical(s,db,&ids,a,&v)?);}
            }
        } else {
            let f=form.as_array().ok_or("Study transaction form required")?;
            let op=ident(&f[0])?;
            if op=="db/ensure"{continue;}
            let id=resolve(s,&ids,&f[1])?;
            let a=ident(&f[2])?.to_owned();
            if op=="db/retract" {
                retractions.push((id,a.clone(),f.get(3).map(|v|canonical(s,db,&ids,&a,v)).transpose()?));
            }else if op=="db/add"||op=="db/cas" {
                if op=="db/cas"{
                    let old=if f[3].is_null(){Json::Null}else{canonical(s,db,&ids,&a,&f[3])?};
                    if s.entities.get(&id).and_then(|e|e.get(&a)).unwrap_or(&Json::Null)!=&old{return Err("Study precondition changed".into());}
                }
                let v=canonical(s,db,&ids,&a,&f[if op=="db/cas"{4}else{3}])?;
                changed.entry((id,a)).or_default().push(v);
            }else{return Err(format!("Unsupported local study transaction {op}").into())}
        }
    }
    let mut replacements=BTreeMap::<u64,Record>::new();
    let mut history=vec![];
    for (id,a,v) in retractions {
        let e=replacements.entry(id).or_insert_with(||s.entities.get(&id).cloned().unwrap_or_default());
        if let Some(v)=v {
            if attr(db,&a)?.cardinality==Cardinality::Many {if let Some(values)=e.get_mut(&a).and_then(Json::as_array_mut){values.retain(|value|*value!=v);}}
            else if e.get(&a)==Some(&v){e.remove(&a);}
        }else{e.remove(&a);}
    }
    for ((id,a),values) in changed {
        let many=attr(db,&a)?.cardinality==Cardinality::Many;
        let e=replacements.entry(id).or_insert_with(||s.entities.get(&id).cloned().unwrap_or_default());
        if many {
            let current=e.entry(a.clone()).or_insert(json!([])).as_array_mut().ok_or("Expected many values")?;
            for v in values{if !current.contains(&v){current.push(v);}}
            current.sort_by_key(|v|v.to_string());
        }else{
            if values.iter().any(|v|*v!=values[0]){return Err("Conflicting local cardinality-one values".into());}
            let v=values[0].clone();
            if matches!(a.as_str(),"task-item/status"|"learner-task/status")&&e.get(&a)!=Some(&v){history.push(StatusAssertion{entity:id,attribute:a.clone(),value:v.clone(),t:s.basis_t+1,at:json!({"$instant":at.timestamp_millis()})});}
            e.insert(a,v);
        }
    }
    s.replace_records(replacements,s.basis_t+1)?;
    s.status_history.extend(history);
    Ok(ids)
}
pub(super) fn apply(s:&EntitySnapshot,db:&DatabaseValue,forms:&[Json],at:DateTime<Utc>)->Result<(EntitySnapshot,BTreeMap<String,u64>)>{
    let mut out=s.clone();
    let ids=apply_in_place(&mut out,db,forms,at)?;
    Ok((out,ids))
}

fn overlay(base:&EntitySnapshot,delta:&Json)->Result<EntitySnapshot>{
    let mut s=base.clone();
    if delta.is_null(){return Ok(s)}
    let records:BTreeMap<u64,Record>=serde_json::from_value(delta["entities"].clone())?;
    let replaced=records.keys().copied().collect::<BTreeSet<_>>();
    for (id,e) in records{s.entities.insert(id,e);}
    s.status_history.retain(|h|!replaced.contains(&h.entity));
    s.status_history.extend(serde_json::from_value::<Vec<StatusAssertion>>(delta["history"].clone())?);
    s.basis_t=s.basis_t.max(delta["basis"].as_u64().ok_or("Study overlay basis required")?);
    let mut result=EntitySnapshot::new(s.entities.into(),s.basis_t)?;
    result.status_history=s.status_history;result.focused_mode=base.focused_mode;
    Ok(result)
}
fn delta(s:&EntitySnapshot,touched:&BTreeSet<u64>)->Json{
    let records=touched.iter().filter_map(|id|s.entities.get(id).map(|e|(*id,e))).collect::<BTreeMap<_,_>>();
    let history=s.status_history.iter().filter(|h|touched.contains(&h.entity)).collect::<Vec<_>>();
    json!({"entities":records,"history":history,"basis":s.basis_t})
}

fn identity(s:&EntitySnapshot,id:u64)->Result<Json>{
    let e=s.entity(id)?;
    for a in ["learner-task/id","task-item/id","activity/id","answer/id","working-period/id","progress/id","step/id"]{if let Some(v)=e.get(a){return Ok(json!({"attribute":a,"value":v}));}}
    Err(format!("Provisional study reference {id} has no stable identity: {}",json!(e)).into())
}
fn lookup(s:&EntitySnapshot,key:&Json)->Result<u64>{
    let a=key["attribute"].as_str().ok_or("Stable study identity required")?;
    s.entities.with_attribute(a).into_iter().find(|id|s.entities[id].get(a)==Some(&key["value"])).ok_or_else(||"Queued presentation is not available yet".into())
}
fn task(s:&EntitySnapshot,result:&Json)->Result<Option<u64>>{
    if let Some(id)=result["taskId"].as_u64(){return Ok(Some(id))}
    if let Some(id)=result["taskUuid"].as_str(){return Ok(Some(lookup(s,&json!({"attribute":"learner-task/id","value":{"$uuid":id}}))?))}
    Ok(None)
}
fn view(s:&EntitySnapshot,l:u64,action:&str,result:&Json)->Result<Json>{
    if action=="profile-settings"{return profile_json(s,l)}
    if let Some(id)=result["assignmentId"].as_str(){return assignment_reader::detail(s,l,id)}
    if matches!(action,"target"|"queue-topic"|"daily-xp-goal"){return Ok(json!({"basis":s.basis_t,"learner":learner_json(s,l)}))}
    if action=="queue"{return home(s,l)}
    let t=task(s,result)?.ok_or("Missing local task result")?;
    task_json(s,l,t)
}
fn promise(view:&Json)->Json{
    json!({"type":view["type"],"status":view["status"],"contentId":view["step"]["contentId"],"stepStatus":view["step"]["status"],"xp":view["xp"],"assignmentId":view["assignmentId"]})
}
fn generated(forms:&[Json])->Json{
    let mut values=serde_json::Map::new();
    for f in forms{if let Some(name)=f.get("db/id").and_then(Json::as_str){for (a,v) in f.as_object().unwrap(){if a.ends_with("/id"){values.insert(format!("{name}|{a}"),v.clone());}}}}
    Json::Object(values)
}
fn reuse_ids(forms:&mut[Json],ids:&Json){
    for f in forms{if let Some(name)=f.get("db/id").and_then(Json::as_str).map(str::to_owned){for (a,v) in f.as_object_mut().unwrap(){if let Some(saved)=ids.get(format!("{name}|{a}")){*v=saved.clone();}}}}
}
/// Convert status transitions to explicit logical work intervals. Their times
/// survive delayed EDB transactions and restarts, including starts and switches.
pub(super) fn clocks(s:&EntitySnapshot,db:&DatabaseValue,forms:&mut Vec<Json>,at:DateTime<Utc>)->Result<()> {
    let ids=collect_ids(s,forms)?;
    let transitions=forms.iter().filter_map(|f|{
        if let Some(e)=f.as_object(){Some((e.get("db/id")?.clone(),e.get("task-item/status")?.clone()))}
        else{let a=f.as_array()?;if ident(a.get(2)?).ok()?=="task-item/status"{Some((a.get(1)?.clone(),a.get(if ident(&a[0]).ok()?=="db/cas"{4}else{3})?.clone()))}else{None}}
    }).collect::<Vec<_>>();
    for (target,next) in transitions {
        let item=resolve(s,&ids,&target)?;let next=ident(&next)?.split('/').next_back().unwrap();
        let prior=s.entities.get(&item).map(|_|status(s,item,"task-item/status")).transpose()?;
        if prior.as_deref()==Some(next){continue;}
        let existing=if s.entities.contains_key(&item){s.refs(item,"task-item/working-periods")?}else{vec![]};
        if existing.is_empty()&&prior.is_some(){
            let elapsed=timing::elapsed(s,item,at)?;
            if elapsed>0. {
                let key=format!("study-clock-{item}-prior");
                forms.push(json!({"db/id":key,"working-period/id":{"$uuid":uid()?},"working-period/started-at":{"$instant":at.timestamp_millis()-(elapsed*1000.).round() as i64},"working-period/ended-at":{"$instant":at.timestamp_millis()}}));
                forms.push(add(target.clone(),"task-item/working-periods",json!(key)));
            }
        }
        if next!="started" {
            for period in existing {if !s.entity(period)?.contains_key("working-period/ended-at"){forms.push(json!([kw("db/cas"),period,kw("working-period/ended-at"),null,{"$instant":at.timestamp_millis()}]));}}
        }else{
            let key=format!("study-clock-{item}-open");
            forms.push(json!({"db/id":key,"working-period/id":{"$uuid":uid()?},"working-period/started-at":{"$instant":at.timestamp_millis()}}));
            forms.push(add(target,"task-item/working-periods",json!(key)));
        }
    }
    let _=db;Ok(())
}

pub(super) fn project(app:&mut Application,body:&Json)->Result<Json>{
    let (response,projection)=project_value(&app.snapshot,&app.conn.db(),app.learner_eid,app.study_projection.take(),body)?;
    app.study_projection=Some(projection);
    Ok(response)
}
pub(super) fn project_value(base:&EntitySnapshot,db:&DatabaseValue,learner:u64,prior:Option<Projection>,body:&Json)->Result<(Json,Projection)>{
    let fingerprint=course_academy_engine::core::fingerprint(&body["overlay"]);
    let mut projection=match prior {
        Some(p) if p.fingerprint==fingerprint => p,
        _ => Projection{snapshot:overlay(base,&body["overlay"])?,touched:body["overlay"]["entities"].as_object().map(|m|m.keys().filter_map(|k|k.parse().ok()).collect()).unwrap_or_default(),fingerprint},
    };
    let s=&mut projection.snapshot;
    if let Some(focused)=body["operation"]["_focusedMode"].as_bool(){s.focused_mode=focused;}
    let op=&body["operation"];let action=op["action"].as_str().ok_or("Action required")?;
    let millis=body["receivedAt"].as_i64().ok_or("Study receipt instant required")?;
    let at=DateTime::from_timestamp_millis(millis).ok_or("Invalid receipt instant")?;
    let (mut forms,result)=mutate(&s,learner,action,op,at)?;
    clocks(&s,db,&mut forms,at)?;
    // Resolve the pre-operation synthetic references before applying new data.
    let mut refs=serde_json::Map::new();
    for key in ["taskId","itemId","activityId","questionId"]{if let Some(id)=op[key].as_u64().filter(|id|*id>=LOCAL_ID){refs.insert(key.into(),identity(s,id)?);}}
    let ids=apply_in_place(s,db,&forms,at)?;
    let after=&projection.snapshot;
    let output=view(after,learner,action,&result)?;
    let mut clock_forms=vec![];
    for f in &forms{
        let clock=f.as_object().is_some_and(|e|e.contains_key("working-period/id"))||f.get(2).and_then(|v|ident(v).ok()).is_some_and(|a|matches!(a,"task-item/working-periods"|"working-period/ended-at"|"task-item/elapsed-seconds"|"learner-task/elapsed-seconds"|"task-item/working-ended-at"));
        if clock{clock_forms.push(f.clone());}
    }
    // References inside admitted clock forms are resolved by identity at replay.
    let mut clock_refs=serde_json::Map::new();
    for f in &clock_forms{if let Some(id)=f.get(1).and_then(Json::as_u64).filter(|id|*id>=LOCAL_ID){clock_refs.insert(id.to_string(),identity(after,id)?);}}
    let mut operation=op.clone();operation["_deferQueue"]=json!(true);
    operation["_queuedStudy"]=json!({"refs":refs,"clockRefs":clock_refs,"clocks":clock_forms,"generated":generated(&forms),"locals":ids.values().map(|id|Ok((id.to_string(),identity(after,*id)?))).collect::<Result<BTreeMap<_,_>>>()?,"expected":promise(&output),"at":millis});
    let mut changed_tasks=BTreeSet::new();
    for form in &forms {
        let target=form.get("db/id").or_else(||form.get(1));
        if let Some(target)=target {
            if let Ok(id)=resolve(after,&ids,target) {
                projection.touched.insert(id);
                if after.entities.get(&id).is_some_and(|e|e.contains_key("learner-task/id")){changed_tasks.insert(id);}
                for owner in after.owners(id,"learner-task/items")?{changed_tasks.insert(owner);}
            }
        }
    }
    if let Some(task)=task(after,&result)?{changed_tasks.insert(task);}
    let mut views=serde_json::Map::new();
    for t in changed_tasks {
        if let Ok(v)=task_json(after,learner,t){views.insert(t.to_string(),v);}
    }
    let overlay=delta(after,&projection.touched);
    projection.fingerprint=course_academy_engine::core::fingerprint(&overlay);
    let response=json!({"view":output,"views":views,"overlay":overlay,"operation":operation});
    Ok((response,projection))
}

/// Recompute read-dependent credit at the current durable basis; retain the
/// admitted grade/route and identities. Only a confirmed CAS/basis rejection
/// permits the outbox to choose a new database attempt key.
pub(super) fn prepare(s:&EntitySnapshot,db:&DatabaseValue,l:u64,body:&Json,forms:&mut Vec<Json>,result:&mut Json,at:DateTime<Utc>)->Result<()> {
    let Some(queued)=body.get("_queuedStudy")else{return Ok(())};
    reuse_ids(forms,&queued["generated"]);
    if let Some(id)=queued["generated"]["new-task|learner-task/id"]["$uuid"].as_str(){if result.get("taskUuid").is_some(){result["taskUuid"]=json!(id);}}
    forms.retain(|f|!f.get(2).and_then(|v|ident(v).ok()).is_some_and(|a|matches!(a,"task-item/working-periods"|"working-period/ended-at"|"task-item/elapsed-seconds"|"learner-task/elapsed-seconds"|"task-item/working-ended-at")));
    for f in queued["clocks"].as_array().ok_or("Queued study clocks required")?{
        let mut f=f.clone();
        if let Some(id)=f.get(1).and_then(Json::as_u64).filter(|id|*id>=LOCAL_ID){f[1]=json!(lookup(s,&queued["clockRefs"][id.to_string()])?);}
        forms.push(f);
    }
    // Clock tempid names include provisional entity IDs, but UUID identity is
    // stable and all new references stay local to this exact transaction.
    let (after,_)=apply(s,db,forms,at)?;
    let actual=promise(&view(&after,l,body["action"].as_str().unwrap_or(""),result)?);
    if actual!=queued["expected"]{return Err("Study content or outcome changed before saving; accepted work retained".into());}
    Ok(())
}
pub(super) fn bind(s:&EntitySnapshot,operation:&Json)->Result<Json>{
    let mut op=operation.clone();
    let refs=op["_queuedStudy"]["refs"].as_object().ok_or("Queued study references required")?.clone();
    for (key,value) in refs{op[key]=json!(lookup(s,&value)?);}
    Ok(op)
}
pub(super) fn persist(app:&mut Application,body:&Json)->Result<Json>{
    let op=bind(&app.snapshot,&body["operation"])?;
    let value=app.process(&op)?;
    let mut aliases=serde_json::Map::new();
    for (local,key) in op["_queuedStudy"]["locals"].as_object().ok_or("Queued study identities required")? {
        aliases.insert(local.clone(),json!(lookup(&app.snapshot,key)?));
    }
    Ok(json!({"view":value,"aliases":aliases}))
}

pub(super) fn read(app:&mut Application,body:&Json)->Result<Json>{
    let fingerprint=course_academy_engine::core::fingerprint(&body["overlay"]);
    if app.study_projection.as_ref().is_none_or(|p|p.fingerprint!=fingerprint){
        app.study_projection=Some(Projection{snapshot:overlay(&app.snapshot,&body["overlay"])?,touched:BTreeSet::new(),fingerprint});
    }
    let s=&app.study_projection.as_ref().unwrap().snapshot;
    let l=app.learner_eid;let op=&body["operation"];
    match op["action"].as_str().ok_or("Study read action required")? {
        "home"|"queue"=>home(s,l),
        "task"=>{let t=required(op,"taskId")?;owned(s,l,t)?;task_json(s,l,t)},
        "profile"=>profile_json(s,l),
        "learner"=>Ok(json!({"basis":s.basis_t,"learner":learner_json(s,l)})),
        "assignments"=>assignment_reader::list(s,l),
        "assignment"=>assignment_reader::detail(s,l,op["assignmentId"].as_str().ok_or("Assignment required")?),
        "activity-history"=>activity_history::list(s,l,op),
        "activity-history-detail"=>activity_history::detail(s,l,required(op,"taskId")?),
        "study-stats"=>study_stats::summary(s,l,op,Utc::now()),
        "topic-study-availability"=>Ok(topic_study_availability(s,l,required(op,"topicId")?,Utc::now())),
        _=>Err("Unsupported local study read".into()),
    }
}
