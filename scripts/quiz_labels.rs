//! Learner-specific quiz names, derived without changing authored activities.
use super::*;

pub(super) struct QuizLabels {
    titles: BTreeMap<u64, String>,
    next: usize,
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> EntitySnapshot {
        let mut records = BTreeMap::new();
        for (id, record) in [
            (
                1,
                json!({"learner/id":"mine","learner/activity":[40,30,20,10,60]}),
            ),
            (2, json!({"learner/id":"other","learner/activity":[99]})),
            (
                100,
                json!({"activity/type":"activity.type/assessment","activity/title":"Practice assessment"}),
            ),
            (
                101,
                json!({"activity/type":"activity.type/assessment","activity/title":"Optional assessment retake"}),
            ),
            (
                102,
                json!({"activity/type":"activity.type/assessment","activity/title":"Practice assessment"}),
            ),
            (
                103,
                json!({"activity/type":"activity.type/assessment","activity/title":"Practice assessment"}),
            ),
            (
                104,
                json!({"activity/type":"activity.type/lesson","activity/title":"A lesson"}),
            ),
            (
                30,
                json!({"learner-task/activity":100,"learner-task/status":"learner-task.status/completed"}),
            ),
            (
                20,
                json!({"learner-task/activity":101,"learner-task/status":"learner-task.status/completed","learner-task/retake-of":30}),
            ),
            (
                10,
                json!({"learner-task/activity":102,"learner-task/status":"learner-task.status/completed"}),
            ),
            (
                40,
                json!({"learner-task/activity":103,"learner-task/status":"learner-task.status/unlocked"}),
            ),
            (
                60,
                json!({"learner-task/activity":104,"learner-task/status":"learner-task.status/completed"}),
            ),
            (
                99,
                json!({"learner-task/activity":100,"learner-task/status":"learner-task.status/completed"}),
            ),
        ] {
            records.insert(id, record.as_object().unwrap().clone());
        }
        for (i, name) in [
            "activity.type/assessment",
            "activity.type/lesson",
            "learner-task.status/completed",
            "learner-task.status/started",
            "learner-task.status/unlocked",
        ]
        .iter()
        .enumerate()
        {
            records.insert(
                1000 + i as u64,
                json!({"db/ident":kw(name)}).as_object().unwrap().clone(),
            );
        }
        let mut s = EntitySnapshot::new(records, 100).unwrap();
        for (task, seconds, state) in [
            (99, 1, "started"),
            (30, 10, "started"),
            (20, 20, "started"),
            (10, 30, "started"),
            (30, 60, "started"),
            (10, 70, "completed"),
            (20, 80, "completed"),
            (30, 90, "completed"),
        ] {
            s.status_history.push(StatusAssertion {
                entity: task,
                attribute: "learner-task/status".into(),
                value: kw(&format!("learner-task.status/{state}")),
                t: seconds,
                at: schema::instant_value(DateTime::from_timestamp(seconds as i64, 0).unwrap()),
            });
        }
        s
    }

    #[test]
    fn quizzes_follow_first_start_and_retakes_keep_the_original_number() -> Result<()> {
        let s = fixture();
        let before = json!({"entities":s.entities,"history":s.status_history,"basis":s.basis_t});
        let labels = QuizLabels::capture(&s, 1)?;
        assert_eq!(labels.title(&s, 100, Some(30))?, "Quiz 1");
        assert_eq!(labels.title(&s, 101, Some(20))?, "Retake Quiz 1");
        assert_eq!(labels.title(&s, 102, Some(10))?, "Quiz 2");
        assert_eq!(labels.title(&s, 103, Some(40))?, "Quiz 3");
        assert_eq!(labels.title(&s, 104, Some(60))?, "A lesson");
        assert_eq!(
            QuizLabels::capture(&s, 2)?.title(&s, 100, Some(99))?,
            "Quiz 1"
        );
        assert_eq!(
            json!({"entities":s.entities,"history":s.status_history,"basis":s.basis_t}),
            before
        );
        Ok(())
    }

    #[test]
    fn prepared_quizzes_do_not_advance_numbering_and_preview_uses_the_same_title() -> Result<()> {
        let mut s = fixture();
        s.entities
            .get_mut(&1)
            .unwrap()
            .insert("learner/activity".into(), json!([30, 20, 40]));
        let labels = QuizLabels::capture(&s, 1)?;
        assert_eq!(labels.title(&s, 103, Some(40))?, "Quiz 2");
        assert_eq!(labels.title(&s, 103, None)?, "Quiz 2");
        assert_eq!(labels.title(&s, 101, None)?, "Retake Quiz 1");
        Ok(())
    }

    #[test]
    fn imported_dates_and_history_pagination_preserve_the_same_numbers() -> Result<()> {
        let mut s = fixture();
        s.entities.get_mut(&10).unwrap().insert(
            "learner-task/finished-at".into(),
            schema::instant_value(DateTime::from_timestamp(5, 0).unwrap()),
        );
        let labels = QuizLabels::capture(&s, 1)?;
        assert_eq!(labels.title(&s, 102, Some(10))?, "Quiz 1");
        assert_eq!(labels.title(&s, 100, Some(30))?, "Quiz 2");
        assert_eq!(labels.title(&s, 101, Some(20))?, "Retake Quiz 2");
        let history = activity_history::list(&s, 1, &json!({}))?;
        let entries = history["activities"].as_array().unwrap();
        assert_eq!(
            entries.iter().find(|entry| entry["taskId"] == 20).unwrap()["title"],
            "Retake Quiz 2"
        );
        let later_page = activity_history::list(&s, 1, &json!({"beforeTaskId":20}))?;
        assert_eq!(later_page["activities"][0]["title"], "Quiz 1");
        Ok(())
    }
}

impl QuizLabels {
    pub(super) fn capture(s: &EntitySnapshot, learner: u64) -> Result<Self> {
        let mut assessments = BTreeSet::new();
        let mut originals = BTreeSet::new();
        let mut retakes = BTreeMap::new();
        for task in s.refs(learner, "learner/activity")? {
            let activity = s.reference(task, "learner-task/activity")?;
            if retrieval::kind(s, activity)? != "assessment" {
                continue;
            }
            assessments.insert(task);
            if let Some(original) = s.optional_ref(task, "learner-task/retake-of")? {
                retakes.insert(task, original);
            } else if matches!(
                status(s, task, "learner-task/status")?.as_str(),
                "started" | "paused" | "completed" | "failed"
            ) {
                originals.insert(task);
            }
        }
        // One pass over resident history for all of this learner's quizzes.
        // Preparation and retakes do not consume a new quiz number.
        if assessments.is_empty() {
            return Ok(Self {
                titles: BTreeMap::new(),
                next: 1,
            });
        }
        let mut first_seen = BTreeMap::new();
        let mut first_started = BTreeMap::new();
        for event in &s.status_history {
            if event.attribute != "learner-task/status" || !assessments.contains(&event.entity) {
                continue;
            }
            let at = schema::parse_instant(&event.at)?;
            first_seen.entry(event.entity).or_insert(at);
            if s.ident(&event.value)? == "learner-task.status/started" {
                first_started.entry(event.entity).or_insert(at);
                if !retakes.contains_key(&event.entity) {
                    originals.insert(event.entity);
                }
            }
        }
        let mut dated = vec![];
        for task in originals {
            let imported = s
                .entity(task)?
                .get("learner-task/finished-at")
                .map(schema::parse_instant)
                .transpose()?;
            let at = imported
                .or(first_started.get(&task).copied())
                .or(first_seen.get(&task).copied());
            dated.push((at, task));
        }
        dated.sort();
        let numbers: BTreeMap<_, _> = dated
            .into_iter()
            .enumerate()
            .map(|(i, (_, task))| (task, i + 1))
            .collect();
        let next = numbers.len() + 1;
        let mut titles = BTreeMap::new();
        for task in assessments {
            let mut original = task;
            let mut visited = BTreeSet::new();
            while let Some(parent) = retakes.get(&original) {
                if !visited.insert(original) {
                    return Err("Cyclic quiz retake references".into());
                }
                original = *parent;
            }
            let number = numbers.get(&original).copied().unwrap_or(next);
            titles.insert(
                task,
                if retakes.contains_key(&task) {
                    format!("Retake Quiz {number}")
                } else {
                    format!("Quiz {number}")
                },
            );
        }
        Ok(Self { titles, next })
    }

    pub(super) fn title(
        &self,
        s: &EntitySnapshot,
        activity: u64,
        task: Option<u64>,
    ) -> Result<String> {
        if retrieval::kind(s, activity)? != "assessment" {
            return Ok(text(s, activity, "activity/title"));
        }
        if let Some(title) = task.and_then(|task| self.titles.get(&task)) {
            return Ok(title.clone());
        }
        // An inspection may select an activity before looking up its saved task.
        for task in s.owners(activity, "learner-task/activity")? {
            if let Some(title) = self.titles.get(&task) {
                return Ok(title.clone());
            }
        }
        Ok(format!("Quiz {}", self.next))
    }
}
