//! Read the explorer's small attribute projection from one immutable EDB basis.
//! This peer never opens a transactor or writes database facts.

use edb_core::{
    DatabaseValue, IndexPrefix, Keyword, Peer, SemanticError, SnapshotKey, Value,
    postgres_config_from_env,
};
use serde_json::{Value as Json, json};
use std::collections::{BTreeMap, BTreeSet};
use std::error::Error;
use std::io::{BufRead, Write};

mod topic_reader;

type Result<T> = std::result::Result<T, Box<dyn Error>>;
type Facts = BTreeMap<u64, BTreeMap<&'static str, Vec<Value>>>;

fn values<'a>(facts: &'a Facts, eid: u64, attr: &str) -> &'a [Value] {
    facts
        .get(&eid)
        .and_then(|e| e.get(attr))
        .map(Vec::as_slice)
        .unwrap_or(&[])
}

fn scalar<'a>(facts: &'a Facts, eid: u64, attr: &str) -> Option<&'a Value> {
    values(facts, eid, attr).first()
}

fn refs(facts: &Facts, eid: u64, attr: &str) -> Vec<u64> {
    values(facts, eid, attr)
        .iter()
        .filter_map(|v| match v {
            Value::Ref(id) => Some(*id),
            _ => None,
        })
        .collect()
}

fn text(facts: &Facts, eid: u64, attr: &str) -> Option<String> {
    match scalar(facts, eid, attr) {
        Some(Value::String(s)) => Some(s.clone()),
        _ => None,
    }
}

fn uuid(facts: &Facts, eid: u64, attr: &str) -> Option<String> {
    match scalar(facts, eid, attr) {
        Some(Value::Uuid(value)) => {
            let hex = format!("{value:032x}");
            Some(format!(
                "{}-{}-{}-{}-{}",
                &hex[..8],
                &hex[8..12],
                &hex[12..16],
                &hex[16..20],
                &hex[20..]
            ))
        }
        _ => None,
    }
}

fn project(db: &DatabaseValue) -> Result<Facts> {
    let mut facts = Facts::new();
    for attr in [
        "topic/id",
        "topic/title",
        "topic/math-academy-id",
        "topic/next",
        "course/id",
        "course/title",
        "course/code",
        "course/level",
        "course/units",
        "unit/modules",
        "module/topics",
        "learner/id",
        "learner/name",
        "learner/course",
        "learner/knowledge-profile",
        "progress/topic",
        "progress/repetitions",
    ] {
        let (ns, name) = attr.split_once('/').unwrap();
        let Some(attribute) = db.schema().resolve_ident(&Keyword::new(ns, name)) else {
            // Optional schema additions may not yet be installed.
            if matches!(
                attr,
                "course/level" | "course/code" | "topic/math-academy-id"
            ) {
                continue;
            }
            return Err(format!("Missing schema attribute {attr}").into());
        };
        for datom in db.collect_datoms_with_prefix(&IndexPrefix::Aevt {
            attribute,
            entity: None,
            value: None,
        })? {
            facts
                .entry(datom.entity)
                .or_default()
                .entry(attr)
                .or_default()
                .push(datom.value);
        }
    }
    Ok(facts)
}

fn graph(db: &DatabaseValue, learner_id: &str) -> Result<Json> {
    let facts = project(db)?;
    let learner_eid = facts
        .keys()
        .copied()
        .find(|eid| text(&facts, *eid, "learner/id").as_deref() == Some(learner_id))
        .ok_or("Learner not found")?;
    let topic_ids: BTreeSet<_> = facts
        .keys()
        .copied()
        .filter(|eid| scalar(&facts, *eid, "topic/id").is_some())
        .collect();
    // JavaScript numbers must represent graph identifiers exactly.
    if topic_ids.iter().any(|eid| *eid > 9_007_199_254_740_991) {
        return Err("Topic entity ID exceeds JavaScript safe integer range".into());
    }
    let mut nodes = Vec::new();
    let mut links = Vec::new();
    for eid in &topic_ids {
        let mut node = json!({
            "id": eid,
            "name": text(&facts, *eid, "topic/title").unwrap_or_else(|| format!("Untitled topic {eid}")),
            "uuid": uuid(&facts, *eid, "topic/id"),
        });
        if let Some(Value::Long(id)) = scalar(&facts, *eid, "topic/math-academy-id") {
            node["mathAcademyId"] = json!(id);
        }
        nodes.push(node);
        for target in refs(&facts, *eid, "topic/next") {
            if !topic_ids.contains(&target) {
                return Err("A topic/next edge references an entity without topic/id".into());
            }
            links.push(json!({"source": eid, "target": target}));
        }
    }
    let mut courses = Vec::new();
    for eid in facts.keys().copied() {
        let Some(id) = uuid(&facts, eid, "course/id") else {
            continue;
        };
        let mut membership = BTreeSet::new();
        for unit in refs(&facts, eid, "course/units") {
            for module in refs(&facts, unit, "unit/modules") {
                for topic in refs(&facts, module, "module/topics") {
                    if !topic_ids.contains(&topic) {
                        return Err(
                            "Course membership references an entity without topic/id".into()
                        );
                    }
                    membership.insert(topic);
                }
            }
        }
        let level = refs(&facts, eid, "course/level")
            .first()
            .and_then(|eid| db.ident(*eid))
            .map(|ident| ident.qualified_name());
        courses.push(json!({
            "id": id,
            "title": text(&facts, eid, "course/title").unwrap_or_else(|| format!("Untitled course {eid}")),
            "level": level,
            "code": text(&facts, eid, "course/code"),
            "topicIds": membership,
        }));
    }
    courses.sort_by(|a, b| {
        a["title"]
            .as_str()
            .cmp(&b["title"].as_str())
            .then_with(|| a["id"].as_str().cmp(&b["id"].as_str()))
    });
    let mut repetitions = BTreeMap::new();
    for progress in refs(&facts, learner_eid, "learner/knowledge-profile") {
        let Some(Value::Ref(topic)) = scalar(&facts, progress, "progress/topic") else {
            continue;
        };
        let count = match scalar(&facts, progress, "progress/repetitions") {
            Some(Value::Double(n)) => *n,
            Some(Value::Long(n)) => *n as f64,
            None => continue, // Unknown repetitions stay absent, never inferred.
            _ => return Err("Repetitions must be numeric".into()),
        };
        if !count.is_finite() || count < 0.0 {
            return Err("Repetitions must be finite and nonnegative".into());
        }
        if !topic_ids.contains(topic) {
            return Err("Progress references an entity without topic/id".into());
        }
        if repetitions.insert(topic.to_string(), count).is_some() {
            return Err("Learner has duplicate progress records for one topic".into());
        }
    }
    let course_id = refs(&facts, learner_eid, "learner/course")
        .first()
        .and_then(|eid| uuid(&facts, *eid, "course/id"));
    Ok(json!({
        "basis": db.basis_t(), "courses": courses, "nodes": nodes, "links": links,
        "learner": {"id": learner_id, "name": text(&facts, learner_eid, "learner/name"), "courseId": course_id},
        "repetitions": repetitions,
    }))
}

fn course_facts(db: &DatabaseValue) -> Result<Facts> {
    // Keep the graph's existing projection and cold-read cost unchanged. Course
    // requests read only curriculum metadata and the learner's current profile.
    let mut facts = project(db)?;
    for attr in [
        "course/math-academy-id",
        "course/description",
        "course/overview",
        "course/outcomes",
        "course/next",
        "course-outcome/id",
        "course-outcome/index",
        "course-outcome/category",
        "course-outcome/text",
        "unit/id",
        "unit/title",
        "unit/next",
        "module/id",
        "module/title",
        "module/next",
        "sequence/id",
        "sequence/title",
        "sequence/courses",
        "progress/learned",
    ] {
        let (ns, name) = attr.split_once('/').unwrap();
        let Some(attribute) = db.schema().resolve_ident(&Keyword::new(ns, name)) else {
            // Metadata and newer optional schema may not yet be installed.
            continue;
        };
        for datom in db.collect_datoms_with_prefix(&IndexPrefix::Aevt {
            attribute,
            entity: None,
            value: None,
        })? {
            facts
                .entry(datom.entity)
                .or_default()
                .entry(attr)
                .or_default()
                .push(datom.value);
        }
    }
    Ok(facts)
}

fn long(facts: &Facts, eid: u64, attr: &str) -> Option<i64> {
    match scalar(facts, eid, attr) {
        Some(Value::Long(value)) => Some(*value),
        _ => None,
    }
}

fn required_uuid(facts: &Facts, eid: u64, attr: &str) -> Result<String> {
    uuid(facts, eid, attr)
        .ok_or_else(|| format!("Curriculum membership references an entity without {attr}").into())
}

fn title(facts: &Facts, eid: u64, kind: &str) -> String {
    text(facts, eid, &format!("{kind}/title")).unwrap_or_else(|| format!("Untitled {kind} {eid}"))
}

fn ordered_members(facts: &Facts, members: Vec<u64>, kind: &str) -> Result<Vec<u64>> {
    let members: BTreeSet<_> = members.into_iter().collect();
    let next_attr = format!("{kind}/next");
    let id_attr = format!("{kind}/id");
    let sort_key = |eid| (title(facts, eid, kind), uuid(facts, eid, &id_attr), eid);
    let mut indegree: BTreeMap<_, usize> = members.iter().map(|eid| (*eid, 0)).collect();
    let mut edges = BTreeMap::new();
    for eid in &members {
        let next: BTreeSet<_> = refs(facts, *eid, &next_attr)
            .into_iter()
            .filter(|target| members.contains(target))
            .collect();
        for target in &next {
            *indegree.get_mut(target).unwrap() += 1;
        }
        edges.insert(*eid, next);
    }
    // Membership is unordered. Honor only explicit next edges within this
    // subset; independent branches use a stable title/identity tie break.
    let mut ready: BTreeSet<_> = indegree
        .iter()
        .filter(|(_, degree)| **degree == 0)
        .map(|(eid, _)| sort_key(*eid))
        .collect();
    let mut ordered = Vec::with_capacity(members.len());
    while let Some((_, _, eid)) = ready.pop_first() {
        ordered.push(eid);
        for target in &edges[&eid] {
            let degree = indegree.get_mut(target).unwrap();
            *degree -= 1;
            if *degree == 0 {
                ready.insert(sort_key(*target));
            }
        }
    }
    if ordered.len() != members.len() {
        return Err(format!("Curriculum {next_attr} contains a cycle").into());
    }
    Ok(ordered)
}

type TopicProgress = BTreeMap<u64, (Option<f64>, Option<bool>)>;

fn course_progress(facts: &Facts, learner_eid: u64) -> Result<TopicProgress> {
    let mut progress = BTreeMap::new();
    for eid in refs(facts, learner_eid, "learner/knowledge-profile") {
        let Some(Value::Ref(topic)) = scalar(facts, eid, "progress/topic") else {
            continue;
        };
        required_uuid(facts, *topic, "topic/id")?;
        let repetitions = match scalar(facts, eid, "progress/repetitions") {
            Some(Value::Double(value)) => Some(*value),
            Some(Value::Long(value)) => Some(*value as f64),
            None => None,
            _ => return Err("Repetitions must be numeric".into()),
        };
        if repetitions.is_some_and(|value| !value.is_finite() || value < 0.0) {
            return Err("Repetitions must be finite and nonnegative".into());
        }
        let learned = match scalar(facts, eid, "progress/learned") {
            Some(Value::Bool(value)) => Some(*value),
            None => None,
            _ => return Err("Learned progress must be boolean".into()),
        };
        if progress.insert(*topic, (repetitions, learned)).is_some() {
            return Err("Learner has duplicate progress records for one topic".into());
        }
    }
    Ok(progress)
}

fn course_completion(facts: &Facts, course_eid: u64, progress: &TopicProgress) -> (usize, usize) {
    let mut topics = BTreeSet::new();
    for unit in refs(facts, course_eid, "course/units") {
        for module in refs(facts, unit, "unit/modules") {
            topics.extend(refs(facts, module, "module/topics"));
        }
    }
    let completed = topics
        .iter()
        .filter(|topic| {
            progress
                .get(topic)
                .and_then(|(repetitions, _)| *repetitions)
                .is_some_and(|repetitions| repetitions >= 6.0)
        })
        .count();
    (completed, topics.len())
}

fn course(db: &DatabaseValue, learner_id: &str, selector: Option<&str>) -> Result<Option<Json>> {
    let facts = course_facts(db)?;
    let learner_eid = facts
        .keys()
        .copied()
        .find(|eid| text(&facts, *eid, "learner/id").as_deref() == Some(learner_id))
        .ok_or("Learner not found")?;
    let learner_course = refs(&facts, learner_eid, "learner/course").first().copied();
    let course_eid = match selector {
        Some(selector) => {
            let academy_id = selector.parse::<i64>().ok();
            facts.keys().copied().find(|eid| {
                uuid(&facts, *eid, "course/id").is_some_and(|id| {
                    id.eq_ignore_ascii_case(selector)
                        || academy_id.is_some_and(|id| {
                            long(&facts, *eid, "course/math-academy-id") == Some(id)
                        })
                })
            })
        }
        None => learner_course.filter(|eid| uuid(&facts, *eid, "course/id").is_some()),
    };
    let Some(course_eid) = course_eid else {
        return Ok(None);
    };
    let progress = course_progress(&facts, learner_eid)?;
    let mut units = Vec::new();
    for unit in ordered_members(&facts, refs(&facts, course_eid, "course/units"), "unit")? {
        let mut modules = Vec::new();
        for module in ordered_members(&facts, refs(&facts, unit, "unit/modules"), "module")? {
            let mut topics = Vec::new();
            for topic in ordered_members(&facts, refs(&facts, module, "module/topics"), "topic")? {
                if topic > 9_007_199_254_740_991 {
                    return Err("Topic entity ID exceeds JavaScript safe integer range".into());
                }
                let (repetitions, learned) = progress.get(&topic).copied().unwrap_or((None, None));
                topics.push(json!({
                    "id": topic,
                    "uuid": required_uuid(&facts, topic, "topic/id")?,
                    "title": title(&facts, topic, "topic"),
                    "mathAcademyId": long(&facts, topic, "topic/math-academy-id"),
                    "repetitions": repetitions,
                    "learned": learned,
                }));
            }
            modules.push(json!({
                "id": required_uuid(&facts, module, "module/id")?,
                "title": title(&facts, module, "module"),
                "topics": topics,
            }));
        }
        units.push(json!({
            "id": required_uuid(&facts, unit, "unit/id")?,
            "title": title(&facts, unit, "unit"),
            "modules": modules,
        }));
    }
    let mut outcome_ids = refs(&facts, course_eid, "course/outcomes");
    outcome_ids.sort_by_key(|eid| {
        (
            long(&facts, *eid, "course-outcome/index").unwrap_or(i64::MAX),
            uuid(&facts, *eid, "course-outcome/id"),
            *eid,
        )
    });
    outcome_ids.dedup();
    let outcomes = outcome_ids
        .into_iter()
        .map(|eid| -> Result<Json> {
            Ok(json!({
                "id": required_uuid(&facts, eid, "course-outcome/id")?,
                "index": long(&facts, eid, "course-outcome/index"),
                "category": text(&facts, eid, "course-outcome/category"),
                "text": text(&facts, eid, "course-outcome/text"),
            }))
        })
        .collect::<Result<Vec<_>>>()?;
    let mut sequence_ids: Vec<_> = facts
        .keys()
        .copied()
        .filter(|eid| uuid(&facts, *eid, "sequence/id").is_some())
        .collect();
    sequence_ids.sort_by_key(|eid| {
        (
            title(&facts, *eid, "sequence"),
            uuid(&facts, *eid, "sequence/id"),
            *eid,
        )
    });
    let mut sequences = Vec::new();
    let mut completions = BTreeMap::new();
    for sequence in sequence_ids {
        let courses =
            ordered_members(&facts, refs(&facts, sequence, "sequence/courses"), "course")?
                .into_iter()
                .map(|eid| -> Result<Json> {
                    let (completed, total) = *completions
                        .entry(eid)
                        .or_insert_with(|| course_completion(&facts, eid, &progress));
                    Ok(json!({
                        "id": required_uuid(&facts, eid, "course/id")?,
                        "title": title(&facts, eid, "course"),
                        "completion": {"completed": completed, "total": total},
                    }))
                })
                .collect::<Result<Vec<_>>>()?;
        sequences.push(json!({
            "id": required_uuid(&facts, sequence, "sequence/id")?,
            "title": title(&facts, sequence, "sequence"),
            "courses": courses,
        }));
    }
    let level = refs(&facts, course_eid, "course/level")
        .first()
        .and_then(|eid| db.ident(*eid))
        .map(|ident| ident.qualified_name());
    Ok(Some(json!({
        "basis": db.basis_t(),
        "learner": {
            "id": learner_id,
            "name": text(&facts, learner_eid, "learner/name"),
            "courseId": learner_course.and_then(|eid| uuid(&facts, eid, "course/id")),
        },
        "course": {
            "id": required_uuid(&facts, course_eid, "course/id")?,
            "title": title(&facts, course_eid, "course"),
            "code": text(&facts, course_eid, "course/code"),
            "level": level,
            "mathAcademyId": long(&facts, course_eid, "course/math-academy-id"),
            "description": text(&facts, course_eid, "course/description"),
            "overview": text(&facts, course_eid, "course/overview"),
            "outcomes": outcomes,
            "units": units,
        },
        "sequences": sequences,
    })))
}

fn serve(peer: &Peer, learner_id: &str) -> Result<()> {
    // This process serves one fixed learner. SnapshotKey includes the lineage
    // and excision generation/frontier, not merely a transaction number.
    // We read current facts only: noHistory consolidation or physical indexing
    // cannot change this projection at an unchanged logical snapshot.
    let mut cached_key: Option<SnapshotKey> = None;
    let mut cached_graph: Option<Vec<u8>> = None;
    let mut cached_courses: BTreeMap<String, Vec<u8>> = BTreeMap::new();
    let mut cached_topics: BTreeMap<String, Vec<u8>> = BTreeMap::new();
    const MAX_CACHED_COURSES: usize = 16;
    const MAX_CACHED_TOPICS: usize = 24;
    let stdin = std::io::stdin();
    let mut stdout = std::io::BufWriter::new(std::io::stdout().lock());
    for line in stdin.lock().lines() {
        let line = line?;
        let response = (|| -> Result<()> {
            let request: Json = serde_json::from_str(&line)?;
            if !request.is_object() {
                return Err("Expected a JSON object".into());
            }
            // Always authenticate/capture the latest durable head before cache
            // lookup. Failure is an error, never permission to serve stale data.
            // The long-lived peer also retains its bounded decoded-block cache.
            let db = peer.sync()?;
            let key = db.snapshot_key()?;
            if cached_key.as_ref().is_none_or(|previous| *previous != key) {
                cached_key = Some(key);
                cached_graph = None;
                cached_courses.clear();
                cached_topics.clear();
            }
            if request.get("action").and_then(Json::as_str) == Some("topic") {
                let selector =
                    match request.get("topicId") {
                        Some(Json::String(value)) if !value.is_empty() && value.len() <= 128 => {
                            value.as_str()
                        }
                        _ => return Err(
                            "Topic identifier must be a nonempty UUID or Math Academy ID string"
                                .into(),
                        ),
                    };
                if !cached_topics.contains_key(selector) {
                    let envelope = match topic_reader::topic(&db, learner_id, selector)? {
                        Some(data) => json!({"ok": true, "data": data}),
                        None => {
                            json!({"ok": false, "error": "Topic not found.", "code": "not-found"})
                        }
                    };
                    if cached_topics.len() >= MAX_CACHED_TOPICS {
                        cached_topics.pop_first();
                    }
                    cached_topics.insert(selector.to_string(), serde_json::to_vec(&envelope)?);
                }
                stdout.write_all(&cached_topics[selector])?;
            } else if request.get("action").and_then(Json::as_str) == Some("course") {
                let selector =
                    match request.get("courseId") {
                        None | Some(Json::Null) => None,
                        Some(Json::String(value)) if !value.is_empty() && value.len() <= 128 => {
                            Some(value.as_str())
                        }
                        _ => return Err(
                            "Course identifier must be a nonempty UUID or Math Academy ID string"
                                .into(),
                        ),
                    };
                let cache_id = selector.unwrap_or("");
                if !cached_courses.contains_key(cache_id) {
                    let envelope = match course(&db, learner_id, selector)? {
                        Some(data) => json!({"ok": true, "data": data}),
                        None => {
                            json!({"ok": false, "error": "Course not found.", "code": "not-found"})
                        }
                    };
                    if cached_courses.len() >= MAX_CACHED_COURSES {
                        cached_courses.pop_first();
                    }
                    cached_courses.insert(cache_id.to_string(), serde_json::to_vec(&envelope)?);
                }
                stdout.write_all(&cached_courses[cache_id])?;
            } else {
                if cached_graph.is_none() {
                    let data = graph(&db, learner_id)?;
                    cached_graph = Some(serde_json::to_vec(&json!({"ok": true, "data": data}))?);
                }
                stdout.write_all(cached_graph.as_ref().unwrap())?;
            }
            Ok(())
        })();
        match response {
            Ok(()) => (),
            Err(error) => {
                report_error(error.as_ref());
                stdout.write_all(b"{\"ok\":false,\"error\":\"The knowledge graph is temporarily unavailable.\",\"code\":\"unavailable\"}")?;
            }
        }
        stdout.write_all(b"\n")?;
        stdout.flush()?;
    }
    Ok(())
}

fn run() -> Result<()> {
    let mut args = std::env::args().skip(1);
    let usage = "usage: graph_explorer_reader DATABASE LEARNER_ID [--serve]";
    let database = args.next().ok_or(usage)?;
    let learner_id = args.next().ok_or(usage)?;
    let serve_requests = match args.next().as_deref() {
        None => false,
        Some("--serve") => true,
        _ => return Err(usage.into()),
    };
    if args.next().is_some() {
        return Err(usage.into());
    }
    let peer = Peer::connect_configured(&postgres_config_from_env()?, database, 256)?;
    if serve_requests {
        serve(&peer, &learner_id)
    } else {
        serde_json::to_writer(std::io::stdout().lock(), &graph(&peer.db(), &learner_id)?)?;
        Ok(())
    }
}

fn report_error(error: &(dyn Error + 'static)) {
    if let Some(error) = error.downcast_ref::<SemanticError>() {
        // Connection strings and private database values stay out of diagnostics.
        eprintln!(
            "EDB read failed: category={:?} code={}",
            error.category, error.code
        );
    } else {
        eprintln!("Graph read failed: {error}");
    }
}

fn main() {
    if let Err(error) = run() {
        report_error(error.as_ref());
        std::process::exit(1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fact(facts: &mut Facts, eid: u64, attr: &'static str, value: Value) {
        facts
            .entry(eid)
            .or_default()
            .entry(attr)
            .or_default()
            .push(value);
    }

    #[test]
    fn order_honors_dependencies_and_stable_ties_within_membership() {
        let mut facts = Facts::new();
        for (eid, name) in [
            (1, "Z prerequisite"),
            (2, "A dependent"),
            (3, "B independent"),
        ] {
            fact(&mut facts, eid, "topic/title", Value::String(name.into()));
            fact(&mut facts, eid, "topic/id", Value::Uuid(eid as u128));
        }
        fact(&mut facts, 1, "topic/next", Value::Ref(2));
        // Edges crossing this module boundary do not add phantom members.
        fact(&mut facts, 3, "topic/next", Value::Ref(99));
        fact(&mut facts, 99, "topic/next", Value::Ref(3));
        assert_eq!(
            ordered_members(&facts, vec![2, 3, 1, 2], "topic").unwrap(),
            vec![3, 1, 2]
        );
        assert_eq!(
            ordered_members(&facts, vec![1, 2, 3], "topic").unwrap(),
            vec![3, 1, 2]
        );
    }

    #[test]
    fn cyclic_navigation_is_not_presented_as_a_valid_order() {
        let mut facts = Facts::new();
        fact(&mut facts, 1, "unit/next", Value::Ref(2));
        fact(&mut facts, 2, "unit/next", Value::Ref(1));
        assert!(ordered_members(&facts, vec![1, 2], "unit").is_err());
    }

    #[test]
    fn partial_progress_preserves_unknown_distinct_from_zero_and_false() {
        let mut facts = Facts::new();
        for (topic, record) in [(1, 11), (2, 12)] {
            fact(&mut facts, topic, "topic/id", Value::Uuid(topic as u128));
            fact(&mut facts, record, "progress/topic", Value::Ref(topic));
            fact(
                &mut facts,
                20,
                "learner/knowledge-profile",
                Value::Ref(record),
            );
        }
        fact(&mut facts, 11, "progress/repetitions", Value::Double(0.0));
        fact(&mut facts, 11, "progress/learned", Value::Bool(false));
        let progress = course_progress(&facts, 20).unwrap();
        assert_eq!(progress[&1], (Some(0.0), Some(false)));
        assert_eq!(progress[&2], (None, None));
    }

    #[test]
    fn course_completion_counts_unique_topics_at_the_raw_repetition_threshold() {
        let mut facts = Facts::new();
        for unit in [10, 11] {
            fact(&mut facts, 1, "course/units", Value::Ref(unit));
        }
        for (unit, module) in [(10, 20), (10, 21), (11, 21)] {
            fact(&mut facts, unit, "unit/modules", Value::Ref(module));
        }
        for (module, topic) in [
            (20, 101), (20, 102), (21, 101), (21, 103), (21, 104), (21, 105),
        ] {
            fact(&mut facts, module, "module/topics", Value::Ref(topic));
        }
        let progress = BTreeMap::from([
            (101, (Some(6.0), Some(false))),
            (102, (Some(7.0), None)),
            (103, (Some(5.99), Some(true))),
            (104, (None, Some(true))),
            (999, (Some(6.0), Some(true))),
        ]);
        assert_eq!(course_completion(&facts, 1, &progress), (2, 5));
        assert_eq!(course_completion(&facts, 2, &progress), (0, 0));
    }
}
