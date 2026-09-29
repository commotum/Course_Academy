use course_academy_engine::{Result, graph_snapshots, history, live_history, replay, wire};
use serde_json::{Value, json};
use std::{
    fs,
    io::{self, BufRead, Read},
    path::Path,
};

fn read_json(path: Option<&String>) -> Result<Value> {
    let mut text = String::new();
    if let Some(p) = path.filter(|p| p.as_str() != "-") {
        text = fs::read_to_string(p).map_err(|e| e.to_string())?;
    } else {
        io::stdin()
            .read_to_string(&mut text)
            .map_err(|e| e.to_string())?;
    }
    serde_json::from_str(&text).map_err(|e| e.to_string())
}
fn run() -> Result<()> {
    let mut args: Vec<String> = std::env::args().skip(1).collect();
    if args.is_empty() || args[0] == "--help" {
        println!(
            "fire demo [--output FILE]\nfire replay FILE [--output FILE]\nfire request [FILE|-] [--output FILE]\nfire batch  # one JSON request per stdin line\nfire history [--progress FILE] [--observations FILE] [--profile FILE] [--catalog FILE] [--output FILE] [--replay-output FILE]\nfire live-history [--capture FILE] [--progress FILE] [--prior FILE] [--catalog-root PATH] [--output FILE]\nfire graph-snapshots --ma-root PATH [--progress FILE] [--without-git] [--output FILE]"
        );
        return Ok(());
    }
    let output = if let Some(i) = args.iter().position(|a| a == "--output") {
        if i + 1 >= args.len() || args[i + 1].starts_with("--") {
            return Err("--output requires path".into());
        }
        let path = args.remove(i + 1);
        args.remove(i);
        Some(path)
    } else {
        None
    };
    let allowed: &[&str] = match args[0].as_str() {
        "demo" | "replay" | "request" | "batch" => &[],
        "history" => &[
            "--progress",
            "--observations",
            "--profile",
            "--catalog",
            "--replay-output",
        ],
        "live-history" => &["--capture", "--progress", "--prior", "--catalog-root"],
        "graph-snapshots" => &["--ma-root", "--progress", "--without-git"],
        command => return Err(format!("unknown command {command}")),
    };
    let mut seen = std::collections::BTreeSet::new();
    let mut i = 1;
    while i < args.len() {
        let argument = &args[i];
        if argument.starts_with("--") {
            if !allowed.contains(&argument.as_str()) || !seen.insert(argument) {
                return Err(format!("unknown or repeated option {argument}"));
            }
            if argument != "--without-git" {
                i += 1;
                if args.get(i).is_none_or(|v| v.starts_with("--")) {
                    return Err(format!("{argument} requires a value"));
                }
            }
        } else if !matches!(args[0].as_str(), "replay" | "request") || i != 1 {
            return Err(format!("unexpected argument {argument}"));
        }
        i += 1;
    }
    if args[0] == "batch" && output.is_some() {
        return Err("batch writes one result per stdout line; --output is unsupported".into());
    }
    if args[0] == "batch" {
        for line in io::stdin().lock().lines() {
            let line = line.map_err(|e| e.to_string())?;
            let result = serde_json::from_str::<Value>(&line)
                .map_err(|e| e.to_string())
                .and_then(|v| wire::execute(&v));
            println!(
                "{}",
                match result {
                    Ok(v) => json!({"ok":v}),
                    Err(e) => json!({"error":e}),
                }
            );
        }
        return Ok(());
    }
    let option = |name: &str| -> Result<Option<&str>> {
        match args.iter().position(|a| a == name) {
            Some(i) => Ok(Some(
                args.get(i + 1)
                    .filter(|s| !s.starts_with("--"))
                    .ok_or_else(|| format!("{name} requires value"))?,
            )),
            None => Ok(None),
        }
    };
    let value = match args[0].as_str() {
        "request" => wire::execute(&read_json(args.get(1))?)?,
        "demo" => replay::demo()?,
        "replay" => replay::replay(read_json(Some(
            args.get(1).ok_or("replay requires input file")?,
        ))?)?,
        "graph-snapshots" => graph_snapshots::build_graph_audit(
            Path::new(option("--ma-root")?.ok_or("--ma-root required")?),
            Path::new(option("--progress")?.unwrap_or("reference/progress.csv")),
            !args.iter().any(|s| s == "--without-git"),
        )?,
        "history" => {
            let audit = history::build_audit(
                Path::new(option("--progress")?.unwrap_or("reference/progress.csv")),
                Path::new(
                    option("--observations")?
                        .unwrap_or("reference/mathacademy-xp-observations.json"),
                ),
                option("--profile")?.map(Path::new),
                option("--catalog")?.map(Path::new),
            )?;
            if let Some(path) = option("--replay-output")? {
                write_json(path, &history::run_history_scenarios(&audit)?)?;
            }
            audit
        }
        "live-history" => live_history::build_live_audit(
            Path::new(
                option("--capture")?.unwrap_or("reference/fire-live-observations-2026-09-26.json"),
            ),
            Path::new(option("--progress")?.unwrap_or("reference/progress.csv")),
            Path::new(option("--prior")?.unwrap_or("reference/mathacademy-xp-observations.json")),
            option("--catalog-root")?.map(Path::new),
        )?,
        _ => return Err(format!("unknown command {}", args[0])),
    };
    let payload = serde_json::to_string_pretty(&value).map_err(|e| e.to_string())? + "\n";
    if let Some(path) = output {
        if let Some(parent) = Path::new(&path)
            .parent()
            .filter(|p| !p.as_os_str().is_empty())
        {
            fs::create_dir_all(parent).map_err(|e| e.to_string())?;
        }
        fs::write(path, payload).map_err(|e| e.to_string())?;
    } else {
        print!("{payload}");
    }
    Ok(())
}
fn write_json(path: &str, value: &Value) -> Result<()> {
    if let Some(parent) = Path::new(path)
        .parent()
        .filter(|p| !p.as_os_str().is_empty())
    {
        fs::create_dir_all(parent).map_err(|e| e.to_string())?;
    }
    fs::write(
        path,
        serde_json::to_string_pretty(value).map_err(|e| e.to_string())? + "\n",
    )
    .map_err(|e| e.to_string())
}
fn main() {
    if let Err(error) = run() {
        eprintln!("{error}");
        std::process::exit(1);
    }
}
