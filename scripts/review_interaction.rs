//! Fast, read-only review feedback and ordered background persistence.
use super::*;
use course_academy_engine::activities;

fn review(s:&EntitySnapshot,l:u64,body:&Json)->Result<(u64,u64,Vec<learning::LessonStep>)>{
    let t=required(body,"taskId")?;owned(s,l,t)?;
    let a=s.reference(t,"learner-task/activity")?;
    if retrieval::kind(s,a)?!="review" {return Err("Fast interaction requires a review".into());}
    let steps=learning::lesson_steps(s,a)?;
    if steps.len()!=5 {return Err("A review must reserve five fresh questions".into());}
    Ok((t,a,steps))
}

pub(super) fn read(s:&EntitySnapshot,l:u64,body:&Json)->Result<Json>{
    let (t,_,steps)=review(s,l,body)?;
    if body["action"]=="review-session" {
        let view=task_json(s,l,t)?;
        let mut periods=vec![];
        if let Some(i)=view["step"]["itemId"].as_u64(){
            let saved=s.refs(i,"task-item/working-periods")?;
            if !saved.is_empty(){
                for p in saved {periods.push(json!({"id":s.entity(p)?["working-period/id"]["$uuid"],"start":schema::parse_instant(&s.entity(p)?["working-period/started-at"])?.timestamp_millis(),"end":s.entity(p)?.get("working-period/ended-at").map(schema::parse_instant).transpose()?.map(|v|v.timestamp_millis())}));}
            }else{
                let events=timing::history(s,i,"task-item/status")?;
                if events.first().is_none_or(|(_,v)|v!="task-item.status/started"){return Err("Historical review timing requires synchronous continuation".into());}
                let cutoff=s.entity(i)?.get("task-item/working-ended-at").map(schema::parse_instant).transpose()?.map(|at|at.timestamp_millis());
                for (index,(at,state)) in events.iter().enumerate(){
                    let start=at.timestamp_millis();
                    if state!="task-item.status/started" || cutoff.is_some_and(|end|start>=end){continue;}
                    let end=events.get(index+1).map(|v|v.0.timestamp_millis()).map(|end|end.min(cutoff.unwrap_or(end)));
                    periods.push(json!({"id":uid()?,"start":start,"end":end}));
                }
            }
        }
        periods.sort_by_key(|p|p["start"].as_i64());
        let cards=steps.iter().map(|st|content_step_json(s,&steps,st.content,None,"started",Some(0.))).collect::<Result<Vec<_>>>()?;
        return Ok(json!({"view":view,"steps":cards,"periods":periods}));
    }
    if body["action"]=="review-decision" {
        let outcomes=body["outcomes"].as_array().ok_or("Review outcomes required")?.iter().map(|v|match v.as_str(){Some("correct")=>Ok(Some(true)),Some("incorrect")=>Ok(Some(false)),Some("skipped")=>Ok(None),_=>Err("Invalid review outcome".into())}).collect::<Result<Vec<_>>>()?;
        if outcomes.is_empty()||outcomes.len()>5{return Err("Invalid review prefix".into());}
        let decision=activities::evaluate_review_prefix(&outcomes)?;
        let xp=activities::earned_xp("review",number(s,t,"learner-task/xp-base") as i64,decision.correct,decision.attempted,outcomes.last().copied().flatten())?;
        return Ok(json!({"complete":decision.complete(),"passed":decision.passed(),"xp":xp.to_string().parse::<i64>()?}));
    }
    let q=required(body,"questionId")?;
    if !steps.iter().any(|st|st.content==q){return Err("Question is not reserved by this review".into());}
    if body["action"]=="review-skip" {return Ok(json!({"step":content_step_json(s,&steps,q,None,"skipped",Some(0.))?}));}
    let fields=s.refs(q,"question/answer-fields")?;
    let responses=body["responses"].as_array().ok_or("Responses required")?;
    let mut submitted=BTreeMap::new();
    for r in responses{
        let f=required(r,"fieldId")?;
        if !fields.contains(&f)||submitted.contains_key(&f){return Err("Each answer field must appear exactly once".into());}
        let v=if status(s,f,"answer-field/type")?=="blank"{r["value"].as_str().ok_or("Blank response needs text")?.to_owned()}else{required(r,"choiceId")?.to_string()};
        submitted.insert(f,v);
    }
    if submitted.len()!=fields.len(){return Err("Answer every current question field before submitting".into());}
    let correct=learning::grade(s,q,&submitted)?;
    let state=if correct{"correct"}else{"incorrect"};
    let mut step=content_step_json(s,&steps,q,None,state,Some(0.))?;
    for field in step["fields"].as_array_mut().unwrap(){
        let f=field["id"].as_u64().unwrap();let r=responses.iter().find(|r|r["fieldId"]==f).unwrap();
        let mut response=if status(s,f,"answer-field/type")?=="blank"{json!({"value":r["value"],"type":status(s,s.reference(f,"answer-field/correct")?,"answer/type")?})}else{let a=required(r,"choiceId")?;json!({"id":a,"choiceId":a,"value":text(s,a,"answer/value"),"type":status(s,a,"answer/type")?,"feedback":text(s,a,"answer/feedback")})};
        response["grade"]=json!(if learning::grade_field(s,q,f,&submitted[&f])?{"correct"}else{"incorrect"});
        field["response"]=response;field["grade"]=field["response"]["grade"].clone();
    }
    Ok(json!({"step":step}))
}

pub(super) fn persist(app:&mut Application,body:&Json)->Result<Json>{
    let mut op=body["operation"].clone();
    let (t,_,_)=review(&app.snapshot,app.learner_eid,&op)?;
    let q=required(&op["_queuedReview"],"questionId")?;
    let item=items(&app.snapshot,t)?.into_iter().find(|i|app.snapshot.optional_ref(*i,"task-item/content").ok().flatten()==Some(q)).ok_or("Queued review presentation is not available yet")?;
    op["itemId"]=json!(item);op["_deferQueue"]=json!(true);
    app.process(&op)
}

fn close_other_clocks(s:&EntitySnapshot,body:&Json,at:DateTime<Utc>,forms:&mut Vec<Json>)->Result<()>{
    let queued=body.get("_queuedReview").is_some();
    let selected=body["itemId"].as_u64();
    let transitions=forms.iter().filter(|f|f.get(0)==Some(&kw("db/cas"))&&f.get(2)==Some(&kw("task-item/status")))
        .filter_map(|f|Some((f[1].as_u64()?,f[4].clone()))).collect::<Vec<_>>();
    for (item,next) in transitions {
        if queued&&Some(item)==selected{continue;}
        let periods=s.refs(item,"task-item/working-periods")?;
        if periods.is_empty(){continue;}
        let before=status(s,item,"task-item/status")?;
        let after=s.ident(&next)?;
        if before=="started" && after!="task-item.status/started" {
            for period in periods {
                if !s.entity(period)?.contains_key("working-period/ended-at"){
                    let end=if body["action"]=="answer"&&Some(item)==selected{body["submittedAt"].as_i64().unwrap_or(at.timestamp_millis())}else{at.timestamp_millis()};
                    forms.push(json!([kw("db/cas"),period,kw("working-period/ended-at"),null,{"$instant":end}]));
                }
            }
        }else if before=="paused" && after=="task-item.status/started" {
            let id=format!("clock-resume-{item}");
            forms.push(json!({"db/id":id,"working-period/id":{"$uuid":uid()?},"working-period/started-at":{"$instant":at.timestamp_millis()}}));
            forms.push(add(json!(item),"task-item/working-periods",json!(id)));
        }
    }
    Ok(())
}

pub(super) fn attach_periods(s:&EntitySnapshot,l:u64,body:&Json,at:DateTime<Utc>,forms:&mut Vec<Json>)->Result<()>{
    close_other_clocks(s,body,at,forms)?;
    let Some(queued)=body.get("_queuedReview")else{return Ok(())};
    let (t,_,_)=review(s,l,body)?;
    let action=body["action"].as_str().unwrap_or("");
    let target=if action=="continue" && forms.iter().any(|v|v.get("db/id")==Some(&json!("new-item"))){json!("new-item")}else{json!(required(body,"itemId")?)};
    if let Some(expected)=queued["expectedStatus"].as_str(){
        let projected=forms.iter().find(|f|f.get(0)==Some(&kw("db/cas"))&&f.get(1)==Some(&json!(required(body,"itemId").unwrap_or(0)))&&f.get(2)==Some(&kw("task-item/status"))).and_then(|f|f.get(4));
        if projected!=Some(&kw(&format!("task-item.status/{expected}"))){return Err("Review answer changed before saving; queued answer retained".into());}
    }
    if action=="continue" && queued.get("nextQuestionId").is_some(){
        let actual=forms.iter().find(|f|f.get("db/id")==Some(&json!("new-item"))).and_then(|f|f.get("task-item/content")).cloned().unwrap_or(Json::Null);
        if actual!=queued["nextQuestionId"]{return Err("Review route changed before saving; queued work retained".into());}
        if let Some(expected)=queued["expectedTaskStatus"].as_str(){
            let actual=forms.iter().find(|f|f.get(0)==Some(&kw("db/cas"))&&f.get(1)==Some(&json!(t))&&f.get(2)==Some(&kw("learner-task/status"))).and_then(|f|f.get(4)).cloned().unwrap_or(kw(&format!("learner-task.status/{}",status(s,t,"learner-task/status").unwrap_or_default())));
            if actual!=kw(&format!("learner-task.status/{expected}")){return Err("Review stopping rule changed before saving; queued work retained".into());}
        }
    }
    let periods=queued["periods"].as_array().ok_or("Queued working periods required")?;
    let at=Utc::now().timestamp_millis();let mut last=None;let mut open=false;
    for (n,p) in periods.iter().enumerate(){
        let start=p["start"].as_i64().ok_or("Invalid working period start")?;
        let end=p["end"].as_i64();
        if start>at||end.is_some_and(|end|end<start||end>at)||last.is_some_and(|end|start<end)||open{return Err("Invalid queued working periods".into());}
        open=end.is_none();last=end;
        let key=format!("working-{n}");let id=p["id"].as_str().ok_or("Working period identity required")?;
        let mut record=json!({"db/id":key,"working-period/id":{"$uuid":id},"working-period/started-at":{"$instant":start}});
        if let Some(end)=end{record["working-period/ended-at"]=json!({"$instant":end});}
        forms.push(record);forms.push(add(target.clone(),"task-item/working-periods",json!(key)));
    }
    // Duration is server-measured from the acknowledged work intervals; database
    // status timestamps may lag several queued steps and cannot time the work.
    if action!="continue"{
        let elapsed=periods.iter().map(|p|(p["end"].as_i64().unwrap_or(at)-p["start"].as_i64().unwrap()) as f64/1000.).sum::<f64>();
        forms.retain(|f|!(f.get(2)==Some(&kw("task-item/elapsed-seconds"))&&f.get(1)==Some(&target))&&!(f.get(2)==Some(&kw("learner-task/elapsed-seconds"))&&f.get(1)==Some(&json!(t))));
        forms.push(add(target.clone(),"task-item/elapsed-seconds",json!(elapsed)));
        let total=items(s,t)?.into_iter().map(|i|if target==json!(i){elapsed}else{number(s,i,"task-item/elapsed-seconds")}).sum::<f64>();
        forms.push(add(json!(t),"learner-task/elapsed-seconds",json!(total)));
    }
    Ok(())
}
