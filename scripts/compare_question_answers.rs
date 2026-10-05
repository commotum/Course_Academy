//! JSON-lines interface to the engine's exact, error-preserving math comparison.
use course_academy_engine::learning::{compare_math_in_context, comparison_context};
use serde::Deserialize;
use std::io::{self, BufRead, Read, Write};

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Request {
    a: String,
    b: String,
    #[serde(default)]
    prompt: String,
    #[serde(default)]
    kp_titles: Vec<String>,
}

fn response(line: &[u8]) -> serde_json::Value {
    let result = (|| {
        let r: Request = serde_json::from_slice(line).map_err(|e| e.to_string())?;
        if r.a.len() > 4096 || r.b.len() > 4096 {
            return Err("mathematical answer exceeds 4096 bytes".to_owned());
        }
        compare_math_in_context(
            &r.a,
            &r.b,
            &r.prompt,
            comparison_context(&r.prompt, &r.kp_titles),
        )
    })();
    match result {
        Ok(true) => serde_json::json!({"outcome":"equivalent"}),
        Ok(false) => serde_json::json!({"outcome":"different"}),
        Err(reason) => serde_json::json!({"outcome":"unresolved", "reason":reason}),
    }
}

fn main() -> io::Result<()> {
    let mut input = io::stdin().lock();
    let mut output = io::stdout().lock();
    loop {
        let mut line = vec![];
        let count = (&mut input).take(32769).read_until(b'\n', &mut line)?;
        if count == 0 {
            break;
        }
        let reply = if count > 32768 {
            serde_json::json!({"outcome":"unresolved", "reason":"comparison request exceeds 32768 bytes"})
        } else {
            response(&line)
        };
        writeln!(output, "{}", reply)?;
        output.flush()?;
        if count > 32768 {
            break;
        }
    }
    Ok(())
}
