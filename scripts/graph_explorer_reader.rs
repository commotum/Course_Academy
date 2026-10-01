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

fn serve(peer: &Peer, learner_id: &str) -> Result<()> {
    // This process serves one fixed learner and one fixed projection. SnapshotKey
    // therefore supplies the remaining result-cache identity. It includes the
    // lineage and excision generation/frontier, not merely a transaction number.
    // We read current facts only: noHistory consolidation or physical indexing
    // cannot change this projection at an unchanged logical snapshot.
    let mut cached: Option<(SnapshotKey, Vec<u8>)> = None;
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
            if cached.as_ref().is_none_or(|(previous, _)| *previous != key) {
                let data = graph(&db, learner_id)?;
                cached = Some((key, serde_json::to_vec(&json!({"ok": true, "data": data}))?));
            }
            Ok(())
        })();
        match response {
            Ok(()) => stdout.write_all(&cached.as_ref().unwrap().1)?,
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
