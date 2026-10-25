//! Typed set answers: finite sets and Euclidean spaces with finitely many holes.
//! An unsupported representation remains unresolved; scalar equivalence is
//! delegated to the existing exact grader, including its domain checks.
use crate::Result;

#[derive(Debug)]
enum Member {
    Scalar(String),
    Point(Vec<String>),
}
#[derive(Debug)]
enum Set {
    Finite(Vec<Member>),
    Space(usize, Vec<Member>),
}

fn compact(value: &str) -> String {
    value
        .trim()
        .trim_matches('$')
        .replace("\\left", "")
        .replace("\\right", "")
        .replace("\\lbrace", "\\{")
        .replace("\\rbrace", "\\}")
        .replace("\\,", "")
        .replace("\\;", "")
        .replace("\\!", "")
        .replace("\\quad", "")
        .replace("\\qquad", "")
        .replace('−', "-")
        .chars()
        .filter(|c| !c.is_whitespace())
        .collect()
}
fn parts(value: &str) -> Option<Vec<&str>> {
    let mut stack = Vec::new();
    let mut out = Vec::new();
    let mut start = 0;
    for (i, c) in value.char_indices() {
        match c {
            '(' | '{' | '[' => stack.push(c),
            ')' | '}' | ']' => {
                let expected = match c {
                    ')' => '(',
                    '}' => '{',
                    _ => '[',
                };
                if stack.pop() != Some(expected) {
                    return None;
                }
            }
            ',' if stack.is_empty() => {
                out.push(&value[start..i]);
                start = i + 1;
            }
            _ => {}
        }
    }
    if !stack.is_empty() {
        return None;
    }
    out.push(&value[start..]);
    if out.iter().any(|s| s.is_empty()) {
        None
    } else {
        Some(out)
    }
}
fn finite(value: &str, plain: bool) -> Option<Vec<Member>> {
    if value == "\\emptyset" || value == "\\varnothing" {
        return Some(vec![]);
    }
    let body = value
        .strip_prefix("\\{")
        .and_then(|s| s.strip_suffix("\\}"))
        .or_else(|| {
            plain
                .then(|| value.strip_prefix('{')?.strip_suffix('}'))
                .flatten()
        })?;
    if body.is_empty() {
        return Some(vec![]);
    }
    parts(body)?
        .into_iter()
        .map(|s| {
            if let Some(body) = s.strip_prefix('(').and_then(|s| s.strip_suffix(')')) {
                Some(Member::Point(
                    parts(body)?.into_iter().map(str::to_owned).collect(),
                ))
            } else {
                Some(Member::Scalar(s.to_owned()))
            }
        })
        .collect()
}
fn parse(value: &str, plain: bool) -> Option<Set> {
    let value = compact(value);
    if let Some(members) = finite(&value, plain) {
        return Some(Set::Finite(members));
    }
    let (base, holes) = ["\\setminus", "\\smallsetminus", "\\backslash"]
        .into_iter()
        .find_map(|separator| value.split_once(separator))
        .map_or((value.as_str(), None), |(b, h)| (b, Some(h)));
    let real = base
        .strip_prefix("\\mathbb{R}")
        .or_else(|| base.strip_prefix("\\mathbbR"))
        .or_else(|| base.strip_prefix('ℝ'))
        .or_else(|| plain.then(|| base.strip_prefix('R')).flatten())?;
    let power = real.strip_prefix('^')?;
    let power = power
        .strip_prefix('{')
        .and_then(|s| s.strip_suffix('}'))
        .unwrap_or(power);
    if !power.bytes().all(|c| c.is_ascii_digit()) {
        return None;
    }
    let dimension = power.parse::<usize>().ok()?;
    if dimension == 0 || dimension > 64 {
        return None;
    }
    Some(Set::Space(
        dimension,
        match holes {
            Some(h) => finite(h, true)?,
            None => vec![],
        },
    ))
}
fn member_eq(
    a: &Member,
    b: &Member,
    scalar: &mut impl FnMut(&str, &str) -> Result<bool>,
) -> Result<bool> {
    match (a, b) {
        (Member::Scalar(a), Member::Scalar(b)) => scalar(a, b),
        (Member::Point(a), Member::Point(b)) if a.len() == b.len() => {
            for (a, b) in a.iter().zip(b) {
                if !scalar(a, b)? {
                    return Ok(false);
                }
            }
            Ok(true)
        }
        _ => Ok(false),
    }
}
fn same_members(
    a: &[Member],
    b: &[Member],
    scalar: &mut impl FnMut(&str, &str) -> Result<bool>,
) -> Result<bool> {
    for (left, right) in [(a, b), (b, a)] {
        for x in left {
            let mut found = false;
            let mut unresolved = None;
            for y in right {
                match member_eq(x, y, scalar) {
                    Ok(true) => {
                        found = true;
                        break;
                    }
                    Ok(false) => {}
                    Err(e) => unresolved = Some(e),
                }
            }
            if !found {
                if let Some(e) = unresolved {
                    return Err(e);
                }
                return Ok(false);
            }
        }
    }
    Ok(true)
}
fn points(
    members: Vec<Member>,
    dimension: usize,
    scalar: &mut impl FnMut(&str, &str) -> Result<bool>,
) -> Result<Vec<Member>> {
    members
        .into_iter()
        .map(|m| match m {
            Member::Point(v) if v.len() == dimension => Ok(Member::Point(v)),
            Member::Scalar(v) if scalar(&v, "0")? => Ok(Member::Point(vec!["0".into(); dimension])),
            _ => Err("excluded points must have the space's dimension".into()),
        })
        .collect()
}
pub(crate) fn compare(
    actual: &str,
    expected: &str,
    mut scalar: impl FnMut(&str, &str) -> Result<bool>,
) -> Option<Result<bool>> {
    let expected = parse(expected, false)?;
    Some((|| {
        let actual = parse(actual, true).ok_or("unsupported set answer notation")?;
        match (actual, expected) {
            (Set::Finite(a), Set::Finite(b)) => same_members(&a, &b, &mut scalar),
            (Set::Space(n, a), Set::Space(m, b)) if n == m => {
                let a = points(a, n, &mut scalar)?;
                let b = points(b, m, &mut scalar)?;
                same_members(&a, &b, &mut scalar)
            }
            _ => Ok(false),
        }
    })())
}

#[cfg(test)]
mod tests {
    use crate::{learning::compare_math_in_context, symbolic::Context};
    fn compare(a: &str, b: &str) -> crate::Result<bool> {
        compare_math_in_context(
            a,
            b,
            "Find the domain or possible values.",
            Context::default(),
        )
    }
    #[test]
    fn euclidean_domains_preserve_dimension_and_holes() {
        assert_eq!(compare(r"\mathbb{R}^{2}", r"\mathbb R^2"), Ok(true));
        assert_eq!(
            compare(
                r"R^2\setminus\left\{(0,0)\right\}",
                r"\mathbb R^2\setminus\{(0,0)\}"
            ),
            Ok(true)
        );
        assert_eq!(
            compare(r"ℝ^2\backslash\{0\}", r"\mathbb R^2\setminus\{(0,0)\}"),
            Ok(true)
        );
        assert_eq!(compare(r"\mathbb R^3", r"\mathbb R^2"), Ok(false));
        assert_eq!(
            compare(r"\mathbb R^2", r"\mathbb R^2\setminus\{(0,0)\}"),
            Ok(false)
        );
        assert_eq!(
            compare(
                r"\mathbb R^2\setminus\{(0,1)\}",
                r"\mathbb R^2\setminus\{(0,0)\}"
            ),
            Ok(false)
        );
        assert!(
            compare(
                r"\mathbb R^2\setminus\{(0,0,0)\}",
                r"\mathbb R^2\setminus\{(0,0)\}"
            )
            .is_err()
        );
    }
    #[test]
    fn finite_sets_ignore_order_and_repetition_but_not_values_or_point_order() {
        assert_eq!(compare(r"\{1,-1,1\}", r"\{-1,1\}"), Ok(true));
        assert_eq!(compare(r"{2/2,-1}", r"\{-1,1\}"), Ok(true));
        assert_eq!(compare(r"\{1\}", r"\{-1,1\}"), Ok(false));
        assert_eq!(compare(r"\{-1,0,1\}", r"\{-1,1\}"), Ok(false));
        assert_eq!(compare(r"\{(0,1)\}", r"\{(1,0)\}"), Ok(false));
        assert_eq!(compare(r"\emptyset", r"\{\}"), Ok(true));
        assert!(compare(r"\{-1,\}", r"\{-1,1\}").is_err());
    }
    #[test]
    fn scalar_math_and_unsupported_sets_do_not_gain_string_equality() {
        assert_eq!(compare("1+1", "2"), Ok(true));
        assert!(compare(r"\mathbb Q^2", r"\mathbb R^2").is_err());
        assert!(compare(r"\{x:x>0\}", r"\{x:x>0\}").is_err());
    }
}
