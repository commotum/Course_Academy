//! Saved graph colors are observations, never recovered FIRe state.
use crate::Result;
use chrono::{DateTime, SecondsFormat, Utc};
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use std::{
    collections::{BTreeMap, BTreeSet},
    fs,
    io::Read,
    path::{Path, PathBuf},
    process::{Command, Stdio},
    time::{Duration, Instant},
};

const COLORS: [(&str, &str); 7] = [
    ("rgb(210, 231, 249)", "numeric-case-1"),
    ("rgb(165, 207, 243)", "numeric-case-2"),
    ("rgb(120, 182, 237)", "numeric-case-3"),
    ("rgb(74, 158, 232)", "numeric-case-4"),
    ("rgb(29, 134, 226)", "numeric-case-5"),
    (
        "rgb(23, 107, 181)",
        "truthy-default-not-numeric-1-through-5",
    ),
    ("rgb(242, 242, 242)", "gray-no-numeric-constraint"),
];
fn source(path: &Path) -> Result<Value> {
    Ok(
        json!({"path":path.to_string_lossy(),"sha256":format!("{:x}",Sha256::digest(fs::read(path).map_err(|e|e.to_string())?))}),
    )
}
fn text<'a>(v: &'a Value, k: &str) -> Result<&'a str> {
    v[k].as_str().ok_or_else(|| format!("missing string {k}"))
}
fn timestamp(v: &Value) -> Result<i64> {
    v.as_i64()
        .or_else(|| v.as_str().and_then(|s| s.parse().ok()))
        .ok_or("invalid timestamp".into())
}
fn utc(v: &Value) -> Result<String> {
    Ok(DateTime::<Utc>::from_timestamp(timestamp(v)?, 0)
        .ok_or("invalid timestamp")?
        .to_rfc3339_opts(SecondsFormat::Secs, false))
}
fn numeric_sort(values: impl IntoIterator<Item = String>) -> Result<Vec<String>> {
    let mut a: Vec<_> = values
        .into_iter()
        .map(|v| Ok((v.parse::<u64>().map_err(|_| "numeric topic required")?, v)))
        .collect::<Result<_>>()?;
    a.sort();
    Ok(a.into_iter().map(|(_, v)| v).collect())
}
pub fn parse_saved_graph(path: &Path) -> Result<Value> {
    let data = fs::read_to_string(path).map_err(|e| e.to_string())?;
    let doc = roxmltree::Document::parse(&data).map_err(|e| e.to_string())?;
    let root = doc.root_element();
    let mut nodes = vec![];
    let mut seen = BTreeSet::new();
    let mut compatible = root.attribute("id") == Some("graph");
    for node in root.descendants().filter(|n| {
        n.attribute("class")
            .is_some_and(|v| v.split_whitespace().any(|s| s == "node"))
    }) {
        let title = node
            .children()
            .filter(|n| n.is_element())
            .find(|n| n.tag_name().name() == "title")
            .ok_or("Missing node title/ellipse")?;
        let ellipse = node
            .children()
            .filter(|n| n.is_element())
            .find(|n| n.tag_name().name() == "ellipse")
            .ok_or("Missing node title/ellipse")?;
        let topic = title.text().unwrap_or("").trim();
        if topic.is_empty() || !topic.chars().all(|c| c.is_ascii_digit()) {
            return Err("Nonnumeric graph topic ID".into());
        }
        if !seen.insert(topic) {
            return Err("Duplicate topic ID inside graph".into());
        }
        let fill = ellipse.attribute("fill");
        let category = COLORS
            .iter()
            .find(|(c, _)| Some(*c) == fill)
            .map(|(_, s)| *s)
            .unwrap_or("unrecognized-color");
        compatible &=
            ellipse.attribute("stroke-width") == Some("0") && category != "unrecognized-color";
        nodes.push(json!({"topic_id":topic,"fill":fill,"stroke_width":ellipse.attribute("stroke-width"),"legacy_display_category":category}));
    }
    Ok(
        json!({"source":source(path)?,"root_id":root.attribute("id"),"legacy_renderer_compatible":compatible,"node_count":nodes.len(),"nodes":nodes}),
    )
}
fn git_command(repo: &Path, args: &[&str], relative: &Path) -> Result<String> {
    let mut child = Command::new("git")
        .arg("-C")
        .arg(repo)
        .args(args)
        .arg("--")
        .arg(relative)
        .stdout(Stdio::piped())
        .stderr(Stdio::null())
        .spawn()
        .map_err(|e| e.to_string())?;
    let started = Instant::now();
    loop {
        if let Some(status) = child.try_wait().map_err(|e| e.to_string())? {
            if !status.success() {
                return Err("git provenance command failed".into());
            }
            let mut out = String::new();
            child
                .stdout
                .take()
                .unwrap()
                .read_to_string(&mut out)
                .map_err(|e| e.to_string())?;
            return Ok(out.trim().into());
        }
        if started.elapsed() > Duration::from_secs(15) {
            let _ = child.kill();
            let _ = child.wait();
            return Err("git provenance timeout".into());
        }
        std::thread::sleep(Duration::from_millis(25));
    }
}
fn provenance(repo: &Path, path: &Path) -> Value {
    let inner = || -> Result<Value> {
        let relative = path.strip_prefix(repo).map_err(|e| e.to_string())?;
        let value = git_command(repo, &["log", "-1", "--format=%H|%aI|%cI"], relative)?;
        let changed = git_command(repo, &["diff", "--name-only", "HEAD"], relative)?;
        let fields: Vec<_> = value.split('|').collect();
        Ok(if fields.len() == 3 {
            json!({"last_path_commit":fields[0],"author_time":fields[1],"committer_time":fields[2],"working_tree_differs_from_head":!changed.is_empty()})
        } else {
            json!({"tracked_commit":null})
        })
    };
    inner().unwrap_or_else(|e| json!({"unavailable":e}))
}
fn graph_paths(dir: &Path, out: &mut Vec<PathBuf>) -> Result<()> {
    if !dir.exists() {
        return Ok(());
    }
    for e in fs::read_dir(dir).map_err(|e| e.to_string())? {
        let e = e.map_err(|e| e.to_string())?;
        let p = e.path();
        if e.file_type().map_err(|e| e.to_string())?.is_dir() {
            graph_paths(&p, out)?;
        } else if p
            .file_name()
            .and_then(|v| v.to_str())
            .is_some_and(|n| n.starts_with("Graph-") && n.ends_with(".html"))
        {
            out.push(p);
        }
    }
    Ok(())
}
pub fn build_graph_audit(ma_root: &Path, progress: &Path, include_git: bool) -> Result<Value> {
    let log =
        ma_root.join("PIPELINE/Math-Academy/0-Ingest/1-Course-Source/_course_progress_state.jsonl");
    let script = log.with_file_name("course-source.py");
    let logs: Vec<Value> = fs::read_to_string(&log)
        .map_err(|e| e.to_string())?
        .lines()
        .filter(|s| !s.trim().is_empty())
        .map(|s| serde_json::from_str(s).map_err(|e| e.to_string()))
        .collect::<Result<_>>()?;
    let mut completions: BTreeMap<String, Vec<&Value>> = BTreeMap::new();
    let mut starts: BTreeMap<String, Vec<&Value>> = BTreeMap::new();
    let identity = |v: &Value| {
        v.as_str()
            .map(str::to_owned)
            .unwrap_or_else(|| v.to_string())
    };
    for r in &logs {
        match r["status"].as_str() {
            Some("started") => starts.entry(identity(&r["course_id"])).or_default().push(r),
            Some("completed") => {
                if let Some(p) = r["graph_html_path"].as_str().filter(|p| !p.is_empty()) {
                    completions.entry(p.into()).or_default().push(r);
                }
            }
            _ => {}
        }
    }
    let mut paths = vec![];
    graph_paths(&ma_root.join("COURSES/Math-Academy"), &mut paths)?;
    paths.sort();
    let mut graphs = vec![];
    let mut colors: BTreeMap<String, usize> = BTreeMap::new();
    let mut categories: BTreeMap<String, usize> = BTreeMap::new();
    let mut topic_colors: BTreeMap<String, BTreeSet<String>> = BTreeMap::new();
    let mut topic_categories: BTreeMap<String, BTreeSet<String>> = BTreeMap::new();
    let mut capture_times = vec![];
    for path in paths {
        let mut graph = parse_saved_graph(&path)?;
        let rows = completions
            .get(path.to_str().ok_or("non UTF-8 path")?)
            .cloned()
            .unwrap_or_default();
        let latest = rows
            .iter()
            .max_by_key(|r| timestamp(&r["ts"]).unwrap_or(i64::MIN));
        let mut bounds = Value::Null;
        let mut course = Value::Null;
        let mut name = Value::Null;
        if let Some(row) = latest {
            let completed = utc(&row["ts"])?;
            capture_times.push(completed.clone());
            let id = identity(&row["course_id"]);
            course = json!(id);
            name = row["name"].clone();
            let start = starts
                .get(&id)
                .into_iter()
                .flatten()
                .filter(|s| {
                    timestamp(&s["ts"]).unwrap_or(i64::MAX)
                        <= timestamp(&row["ts"]).unwrap_or(i64::MIN)
                })
                .max_by_key(|s| timestamp(&s["ts"]).unwrap_or(i64::MIN));
            bounds = json!({"last_started_utc":start.map(|r|utc(&r["ts"])).transpose()?,"completed_utc":completed});
        }
        for node in graph["nodes"].as_array().unwrap() {
            let topic = text(node, "topic_id")?;
            let fill = node["fill"].as_str().unwrap_or("null");
            let category = text(node, "legacy_display_category")?;
            *colors.entry(fill.into()).or_default() += 1;
            *categories.entry(category.into()).or_default() += 1;
            topic_colors
                .entry(topic.into())
                .or_default()
                .insert(fill.into());
            topic_categories
                .entry(topic.into())
                .or_default()
                .insert(category.into());
        }
        let m = graph.as_object_mut().unwrap();
        m.insert("course_id".into(), course);
        m.insert("course_name".into(), name);
        m.insert("capture_log_completion_records".into(), json!(rows.len()));
        m.insert("capture_log_bounds".into(), bounds);
        m.insert("learner_id".into(), Value::Null);
        m.insert(
            "git".into(),
            if include_git {
                provenance(ma_root, &path)
            } else {
                Value::Null
            },
        );
        graphs.push(graph);
    }
    let mut reader = csv::Reader::from_path(progress).map_err(|e| e.to_string())?;
    let history: Vec<BTreeMap<String, String>> = reader
        .deserialize()
        .map(|r| r.map_err(|e| e.to_string()))
        .collect::<Result<_>>()?;
    let history_topics: BTreeSet<_> = history
        .iter()
        .filter_map(|r| r.get("topic-id").filter(|s| !s.is_empty()).cloned())
        .collect();
    let overlap = numeric_sort(
        history_topics
            .iter()
            .filter(|s| topic_colors.contains_key(*s))
            .cloned(),
    )?;
    let conflicting = numeric_sort(
        topic_colors
            .iter()
            .filter(|(_, s)| s.len() > 1)
            .map(|(t, _)| t.clone()),
    )?;
    let logged: Vec<String> = completions
        .values()
        .flatten()
        .map(|r| utc(&r["ts"]))
        .collect::<Result<_>>()?;
    let history_overlap:Vec<Value>=overlap.iter().map(|t|json!({"topic_id":t,"fills":topic_colors[t],"conditional_display_categories":topic_categories[t],"history_task_ids":history.iter().filter(|r|r.get("topic-id")==Some(t)).map(|r|r.get("task-id")).collect::<Vec<_>>()})).collect();
    Ok(
        json!({"schema_version":1,"sources":{"progress":source(progress)?,"capture_log":source(&log)?,"capture_script":source(&script)?,"public_renderer_assets":{
        "legacy":{"url":"https://mathacademy.com/js/knowledge-graph.js","sha256":"9faf1eee0a0ee09c7e66c4da4db791088ab44ade2af23d317631d5bb71c90c79"},"newer":{"url":"https://mathacademy.com/js/student-knowledge-graph.js","sha256":"094e279fd063cc926db7a583ab6a693fe519349bd5406a0cc2ac8cd1c2a351cb"}},"public_renderer_retrieved_date":"2026-09-26"},
        "summary":{"saved_graphs":graphs.len(),"node_occurrences":graphs.iter().map(|g|g["node_count"].as_u64().unwrap()).sum::<u64>(),"unique_topic_ids":topic_colors.len(),"legacy_compatible_graphs":graphs.iter().filter(|g|g["legacy_renderer_compatible"]==true).count(),"color_counts":colors,"conditional_display_category_counts":categories,"conflicting_color_topic_count":conflicting.len(),"history_topic_overlap_count":overlap.len(),"history_topics_with_conflicting_colors":numeric_sort(conflicting.iter().filter(|t|history_topics.contains(*t)).cloned())?,"first_capture_log_completion_utc":capture_times.iter().min(),"last_capture_log_completion_utc":capture_times.iter().max(),"all_logged_graph_completion_records":logged.len(),"earliest_completion_including_overwritten_paths_utc":logged.iter().min(),"verified_numeric_fire_states":0,"verified_fire_transitions":0},
        "interpretation":{
            "observed":"Node topic IDs and exact fill colors in per-course saved HTML; capture-log times and Git commit provenance.",
            "conditional_mapping":"Palette, #graph root and zero stroke widths match the legacy public renderer. Numeric-case-1..5 refer only to numeric switch cases of its topic.repetition display field, conditional on that historical renderer being used.",
            "default_caveat":"Dark default does not mean >=6: every truthy value unequal to numeric 1..5, including fractions or strings, reaches default. Gray supplies no numeric repetition constraint.",
            "state_caveat":"April capture renderer version, learner identity and server mapping between display repetition and FIRe repNum/stability are not recorded. The newer renderer uses a different stability-to-HSL mapping and must not be inverted on these legacy colors.",
            "course_caveat":"Capture script switches active course before loading /learn and saving #graph. Cross-course differences are preserved, not reconciled into a single learner state or treated as before/after transitions.",
            "time_caveat":"Started/completed times bound the logging operation, not an authenticated answer or state timestamp; Git dates corroborate file provenance, not exact capture time. History completion times have no verified zone."},
        "conflicting_color_topic_ids":conflicting,"history_overlap":history_overlap,"graphs":graphs}),
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn colors_do_not_become_retention() {
        let path = std::env::temp_dir().join(format!("fire-graph-{}.html", std::process::id()));
        for (root, color, category, compatible) in [
            (
                "graph",
                "rgb(23, 107, 181)",
                "truthy-default-not-numeric-1-through-5",
                true,
            ),
            ("graph", "rgb(165, 207, 243)", "numeric-case-2", true),
            (
                "knowledgeGraph",
                "hsl(208, 77%, 80%)",
                "unrecognized-color",
                false,
            ),
            (
                "graph",
                "rgb(242, 242, 242)",
                "gray-no-numeric-constraint",
                true,
            ),
        ] {
            fs::write(&path, format!(r#"<div id="{root}"><svg><g class="node"><title>42</title><ellipse fill="{color}" stroke-width="0"/></g></svg></div>"#)).unwrap();
            let result = parse_saved_graph(&path).unwrap();
            assert_eq!(result["nodes"][0]["legacy_display_category"], category);
            assert_eq!(result["legacy_renderer_compatible"], compatible);
            assert!(result["nodes"][0].get("repetitions").is_none());
        }
        fs::write(&path,r#"<svg><g class="node"><title>42</title><ellipse/></g><g class="node"><title>42</title><ellipse/></g></svg>"#).unwrap();
        assert!(parse_saved_graph(&path).is_err());
        fs::remove_file(path).unwrap();
    }

    #[test]
    fn retained_graph_audit_preserves_conflicts_and_unknown_state() {
        let audit: Value =
            serde_json::from_str(include_str!("fixtures/graph-snapshot-observations.json"))
                .unwrap();
        for (key, expected) in [
            ("saved_graphs", 31),
            ("node_occurrences", 6627),
            ("conflicting_color_topic_count", 217),
            ("history_topic_overlap_count", 129),
            ("verified_numeric_fire_states", 0),
        ] {
            assert_eq!(audit["summary"][key], expected, "{key}");
        }
    }
}
