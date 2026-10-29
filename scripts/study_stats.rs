//! Calendar summaries from owned task evidence; no question or curriculum scan.
use super::*;

#[derive(Default)]
struct ActivityTotals {
    lessons: usize,
    reviews: usize,
    knowledge_points: BTreeSet<u64>,
}

impl ActivityTotals {
    fn record(&mut self, s: &EntitySnapshot, task: u64) -> Result<()> {
        if status(s,task,"learner-task/status")? != "completed" { return Ok(()); }
        if let Some(activity)=s.optional_ref(task,"learner-task/activity")? {
            match status(s,activity,"activity/type")?.as_str() {
                "lesson" => {
                    self.lessons+=1;
                    if let Some(topic)=s.optional_ref(activity,"activity/scope")? {
                        self.knowledge_points.extend(page_reader::references(s.entity(topic)?,"topic/knowledge-points"));
                    }
                }
                "review" => self.reviews+=1,
                _ => {},
            }
        }
        Ok(())
    }

    fn json(&self) -> Json {
        json!({"lessons":self.lessons,"knowledgePoints":self.knowledge_points.len(),"reviews":self.reviews})
    }
}

pub(super) fn summary(s: &EntitySnapshot, learner: u64, body: &Json, now: DateTime<Utc>) -> Result<Json> {
    // The browser supplies local midnights as instants, including DST changes.
    let starts = body["dayStarts"].as_array().ok_or("Local day boundaries are required")?
        .iter().map(|v| v.as_i64().filter(|v| DateTime::from_timestamp_millis(*v).is_some()).ok_or_else(|| "Invalid day boundary".into()))
        .collect::<Result<Vec<_>>>()?;
    if starts.len() != 8 || starts.windows(2).any(|w| !(22*3_600_000..=26*3_600_000).contains(&(w[1]-w[0]))) {
        return Err("Provide eight consecutive local day boundaries".into());
    }
    let tasks: BTreeSet<_> = s.refs(learner, "learner/activity")?.into_iter().collect();
    // Lifetime XP includes recorded imported awards even when their original
    // dates are unknown. Count each owned finished attempt exactly once.
    let mut total_xp=0.;
    let mut missing_xp=0usize;
    let mut activity_totals=ActivityTotals::default();
    for task in &tasks {
        if !matches!(status(s,*task,"learner-task/status")?.as_str(),"completed"|"failed") { continue; }
        if let Some(earned)=s.entity(*task)?.get("learner-task/xp-earned").and_then(Json::as_f64).filter(|v|v.is_finite()) { total_xp+=earned; }
        else { missing_xp+=1; }
        activity_totals.record(s,*task)?;
    }
    let mut item_ids = BTreeSet::new();
    for task in &tasks { item_ids.extend(s.refs(*task, "learner-task/items")?); }
    let cutoffs=item_ids.iter().filter_map(|item|s.entities[item].get("task-item/working-ended-at").map(|v|schema::parse_instant(v).map(|at|(*item,at.timestamp_millis())))).collect::<std::result::Result<BTreeMap<_,_>,String>>()?;
    let mut xp = [0.;7];
    let mut seconds = [0.;7];
    let mut completed = [0u64;7];
    let mut daily_activities: [ActivityTotals;7] = std::array::from_fn(|_| ActivityTotals::default());
    let mut task_starts = BTreeSet::new();
    let mut finished = BTreeMap::new();
    let mut running = BTreeMap::<u64,i64>::new();
    let add_interval = |seconds: &mut [f64;7], start: i64, end: i64| {
        let end = end.min(now.timestamp_millis());
        for day in 0..7 {
            seconds[day] += (end.min(starts[day+1])-start.max(starts[day])).max(0) as f64 / 1000.;
        }
    };
    let mut interval_items=BTreeSet::new();
    for item in &item_ids {
        let periods=s.refs(*item,"task-item/working-periods")?;
        if periods.is_empty(){continue;}
        interval_items.insert(*item);
        for period in periods {
            let e=s.entity(period)?;
            let start=schema::parse_instant(e.get("working-period/started-at").ok_or("Working period needs a start")?)?.timestamp_millis();
            let end=e.get("working-period/ended-at").map(schema::parse_instant).transpose()?.map(|at|at.timestamp_millis()).unwrap_or(now.timestamp_millis());
            add_interval(&mut seconds,start,end);
        }
    }
    for event in &s.status_history {
        let at = schema::parse_instant(&event.at)?.timestamp_millis();
        if at > now.timestamp_millis() { continue; }
        if event.attribute == "learner-task/status" && tasks.contains(&event.entity) {
            let state = s.ident(&event.value)?;
            if state == "learner-task.status/started" { task_starts.insert(event.entity); }
            if matches!(state.as_str(),"learner-task.status/completed"|"learner-task.status/failed") { finished.insert(event.entity, at); }
        } else if event.attribute == "task-item/status" && item_ids.contains(&event.entity) && !interval_items.contains(&event.entity) {
            if let Some(start) = running.remove(&event.entity) { add_interval(&mut seconds,start,at.min(cutoffs.get(&event.entity).copied().unwrap_or(at))); }
            if s.ident(&event.value)? == "task-item.status/started" { running.insert(event.entity,at); }
        }
    }
    for start in running.into_values() { add_interval(&mut seconds,start,now.timestamp_millis()); }
    for (task, at) in finished {
        // An import's recording date is not its original completion date. A
        // recovered source date dates the XP without inventing a local start.
        if !matches!(status(s,task,"learner-task/status")?.as_str(),"completed"|"failed") { continue; }
        if !task_starts.contains(&task) && !s.entity(task)?.contains_key("learner-task/finished-at") { continue; }
        let at = timing::task_finished_at(s,task,DateTime::from_timestamp_millis(at).ok_or("invalid completion date")?)?.timestamp_millis();
        if let Some(day) = starts.windows(2).position(|w| at >= w[0] && at < w[1]) {
            xp[day] += s.entity(task)?.get("learner-task/xp-earned").and_then(Json::as_f64).filter(|x| x.is_finite()).unwrap_or(0.);
            completed[day] += 1;
            daily_activities[day].record(s,task)?;
        }
    }
    let days: Vec<_> = (0..7).map(|i| json!({"start":starts[i],"earnedXp":xp[i],"workingSeconds":seconds[i],"completedActivities":completed[i],"activityTotals":daily_activities[i].json()})).collect();
    Ok(json!({"basis":s.basis_t,"dailyXpGoal":s.entity(learner)?.get("learner/daily-xp-goal"),"days":days,"earnedXp":xp.iter().sum::<f64>(),"totalEarnedXp":total_xp,"totalXpMissing":missing_xp,"workingSeconds":seconds.iter().sum::<f64>(),
        "activityTotals":activity_totals.json()}))
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn activity_totals_use_completed_attempts_and_deduplicate_their_knowledge_points() -> Result<()> {
        let records=BTreeMap::from_iter([
            (1,json!({"learner/id":"test","learner/activity":[2,3,4,5,6,7,8,9,2],"learner/knowledge-profile":[900]})),
            (2,json!({"learner-task/status":11,"learner-task/activity":100})),
            (3,json!({"learner-task/status":11,"learner-task/activity":100})),
            (4,json!({"learner-task/status":11,"learner-task/activity":101})),
            (5,json!({"learner-task/status":12,"learner-task/activity":101})),
            (6,json!({"learner-task/status":13,"learner-task/activity":102})),
            (7,json!({"learner-task/status":11,"learner-task/activity":103})),
            (8,json!({"learner-task/status":11,"learner-task/activity":100})),
            (9,json!({"learner-task/status":11,"learner-task/activity":101,"learner-task/finished-at":{"$instant":86_399_999}})),
            (10,json!({"learner-task/status":11,"learner-task/activity":102})),
            (11,json!({"db/ident":kw("learner-task.status/completed")})),
            (12,json!({"db/ident":kw("learner-task.status/failed")})),
            (13,json!({"db/ident":kw("learner-task.status/paused")})),
            (14,json!({"db/ident":kw("learner-task.status/started")})),
            (20,json!({"db/ident":kw("activity.type/lesson")})),
            (21,json!({"db/ident":kw("activity.type/review")})),
            (22,json!({"db/ident":kw("activity.type/assignment")})),
            (100,json!({"activity/type":20,"activity/scope":200})),
            (101,json!({"activity/type":21,"activity/scope":201})),
            (102,json!({"activity/type":20,"activity/scope":202})),
            (103,json!({"activity/type":22})),
            (200,json!({"topic/knowledge-points":[300,301]})),
            (201,json!({"topic/knowledge-points":[302]})),
            (202,json!({"topic/knowledge-points":[303]})),
            (203,json!({"topic/knowledge-points":[304,305]})),
            (900,json!({"progress/topic":203,"progress/repetitions":6,"progress/learned":true})),
        ].into_iter().map(|(id,value)|(id,value.as_object().unwrap().clone())));
        let mut s=EntitySnapshot::new(records,1)?;
        let before=s.entities.clone();
        let day=86_400_000i64;
        // Imported task 2 has no original completion date. Task 3 crosses
        // midnight; task 9 has a recovered date before its import was recorded.
        for (task, at, state) in [(2,day,11),(3,day,11),(4,day-1,11),(5,day,12),
            (6,day,11),(7,day,11),(8,day+1,11),(9,day,11),(10,day,11)] {
            if task != 2 {
                s.status_history.push(course_academy_engine::schema::StatusAssertion{
                    t:s.status_history.len() as u64+1,entity:task,attribute:"learner-task/status".into(),value:json!(14),at:json!({"$instant":day-1000})});
            }
            s.status_history.push(course_academy_engine::schema::StatusAssertion{
                t:s.status_history.len() as u64+1,entity:task,attribute:"learner-task/status".into(),value:json!(state),at:json!({"$instant":at})});
        }
        let result=summary(&s,1,&json!({"dayStarts":(0..8).map(|i|i*day).collect::<Vec<_>>()}),DateTime::from_timestamp_millis(day+1000).unwrap())?;
        assert_eq!(result["activityTotals"],json!({"lessons":3,"knowledgePoints":2,"reviews":2}));
        assert_eq!(result["days"][0]["activityTotals"],json!({"lessons":0,"knowledgePoints":0,"reviews":2}));
        assert_eq!(result["days"][1]["activityTotals"],json!({"lessons":2,"knowledgePoints":2,"reviews":0}));
        assert_eq!(result["days"][2]["activityTotals"],json!({"lessons":0,"knowledgePoints":0,"reviews":0}));
        assert_eq!(s.entities,before);
        Ok(())
    }
    #[test]
    fn goal_changes_validate_positive_integers_and_only_change_the_preference() -> Result<()> {
        let mut s=EntitySnapshot::new(BTreeMap::from([(1,json!({"learner/id":"test"}).as_object().unwrap().clone())]),1)?;
        for goal in [json!(0),json!(-1),json!(1.5),json!("200"),Json::Null] {
            assert!(mutate(&s,1,"daily-xp-goal",&json!({"dailyXpGoal":goal}),Utc::now()).is_err());
        }
        let (forms,result)=mutate(&s,1,"daily-xp-goal",&json!({"dailyXpGoal":200}),Utc::now())?;
        assert_eq!(forms,vec![json!([kw("db/cas"),1,kw("learner/daily-xp-goal"),null,200])]);
        assert_eq!(result,json!({"goal":true}));
        s.entities.get_mut(&1).unwrap().insert("learner/daily-xp-goal".into(),json!(200));
        let (forms,_)=mutate(&s,1,"daily-xp-goal",&json!({"dailyXpGoal":300}),Utc::now())?;
        assert_eq!(forms,vec![json!([kw("db/cas"),1,kw("learner/daily-xp-goal"),200,300])]);
        assert_eq!(s.entities[&1]["learner/daily-xp-goal"],200);
        Ok(())
    }
    #[test]
    fn local_days_split_work_exclude_pauses_and_do_not_date_imports_as_new_work() -> Result<()> {
        let day=86_400_000i64;
        let mut records=BTreeMap::new();
        for (id,record) in [(1,json!({"learner/id":"test","learner/daily-xp-goal":200,"learner/activity":[2,3,4,6]})),
            (2,json!({"learner-task/id":"task","learner-task/items":[5],"learner-task/status":11,"learner-task/xp-earned":9})),
            (3,json!({"learner-task/id":"import","learner-task/status":11,"learner-task/xp-earned":1000})),
            (4,json!({"learner-task/id":"foreign-clock","learner-task/status":10})),
            (5,json!({"task-item/id":"item","task-item/status":14})),
            (6,json!({"learner-task/id":"active","learner-task/items":[7],"learner-task/status":10})),
            (7,json!({"task-item/id":"active-item","task-item/status":12})),
            (10,json!({"db/ident":kw("learner-task.status/started")})),(11,json!({"db/ident":kw("learner-task.status/completed")})),
            (12,json!({"db/ident":kw("task-item.status/started")})),(13,json!({"db/ident":kw("task-item.status/paused")})),(14,json!({"db/ident":kw("task-item.status/correct")}))] {
            records.insert(id,record.as_object().unwrap().clone());
        }
        let mut s=EntitySnapshot::new(records,20)?;
        for (t,entity,attribute,value,at) in [(1,2,"learner-task/status",10,day-10_000),(2,5,"task-item/status",12,day-10_000),
            (3,5,"task-item/status",13,day+20_000),(4,5,"task-item/status",12,day+60_000),(5,5,"task-item/status",14,day+90_000),
            (6,2,"learner-task/status",11,day+90_000),(7,3,"learner-task/status",11,day+90_000),
            (8,7,"task-item/status",12,day+100_000)] {
            s.status_history.push(course_academy_engine::schema::StatusAssertion{t,entity,attribute:attribute.into(),value:json!(value),at:json!({"$instant":at})});
        }
        let before=s.entities.clone();
        let body=json!({"dayStarts":(0..8).map(|i|i*day).collect::<Vec<_>>()});
        let result=summary(&s,1,&body,DateTime::from_timestamp_millis(day+110_000).unwrap())?;
        assert_eq!(result["dailyXpGoal"],200);
        assert_eq!(result["days"][0]["workingSeconds"],10.);
        assert_eq!(result["days"][1]["workingSeconds"],60.);
        assert_eq!(result["days"][1]["earnedXp"],9.);
        assert_eq!(result["earnedXp"],9.);
        assert_eq!(result["totalEarnedXp"],1009.);
        assert_eq!(result["totalXpMissing"],0);
        assert_eq!(result["days"][1]["completedActivities"],1);
        assert_eq!(s.entities,before);
        s.entities.get_mut(&3).unwrap().insert("learner-task/finished-at".into(),json!({"$instant":day-1000}));
        let recovered=summary(&s,1,&body,DateTime::from_timestamp_millis(day+110_000).unwrap())?;
        assert_eq!(recovered["days"][0]["earnedXp"],1000.);
        assert_eq!(recovered["days"][0]["completedActivities"],1);
        assert_eq!(recovered["days"][1]["earnedXp"],9.);
        assert_eq!(recovered["totalEarnedXp"],1009.);
        s.entities.get_mut(&3).unwrap().remove("learner-task/finished-at");
        s.entities.get_mut(&5).unwrap().insert("task-item/working-ended-at".into(),json!({"$instant":day+80_000}));
        let stopped=summary(&s,1,&body,DateTime::from_timestamp_millis(day+110_000).unwrap())?;
        assert_eq!(stopped["days"][1]["workingSeconds"],50.);
        s.entities.get_mut(&2).unwrap().insert("learner-task/xp-earned".into(),json!(-9));
        s.entities.get_mut(&3).unwrap().remove("learner-task/xp-earned");
        let penalties=summary(&s,1,&body,DateTime::from_timestamp_millis(day+110_000).unwrap())?;
        assert_eq!(penalties["earnedXp"],-9.);
        assert_eq!(penalties["totalEarnedXp"],-9.);
        assert_eq!(penalties["totalXpMissing"],1);
        let mut dst:Vec<_>=(0..8).map(|i|i*day).collect();
        for at in &mut dst[2..] { *at-=3_600_000; }
        assert!(summary(&s,1,&json!({"dayStarts":dst}),Utc::now()).is_ok());
        assert!(summary(&s,1,&json!({"dayStarts":[0,1]}),Utc::now()).is_err());
        Ok(())
    }
}
