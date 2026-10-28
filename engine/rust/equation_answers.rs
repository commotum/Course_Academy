//! Whole equation answers retain both their equality and their original domain.
//! Exact residuals differing by a nonzero rational scale prove the same relation.
//! Other zero-set equivalences remain unresolved, except classified real circles.
use super::*;

fn sides(source: &str) -> Result<Option<(&str, &str)>> {
    if source.len() > 4096 {
        return Err("oversized mathematical equation".into());
    }
    let mut stack = Vec::new();
    let mut equal = None;
    for (i, c) in source.char_indices() {
        match c {
            '(' => stack.push(')'),
            '[' => stack.push(']'),
            '{' => stack.push('}'),
            ')' | ']' | '}' => {
                if stack.pop() != Some(c) {
                    return Err("unbalanced equation group".into());
                }
            }
            '=' if stack.is_empty() => {
                if equal.replace(i).is_some() {
                    return Err("chained equations are unsupported".into());
                }
            }
            _ => {}
        }
    }
    let Some(i) = equal else {
        return Ok(None);
    };
    let left = source[..i].trim();
    let right = source[i + 1..].trim();
    if !stack.is_empty()
        || left.is_empty()
        || right.is_empty()
        || left.ends_with(['<', '>', '!'])
        || right.starts_with('=')
    {
        return Err("unsupported or incomplete mathematical equation".into());
    }
    Ok(Some((left, right)))
}

fn residual(left: &str, right: &str, context: Context) -> Result<(Poly, BTreeSet<Condition>)> {
    let (Answer::Expression(a, mut domain), Answer::Expression(b, other_domain)) =
        (parse(left, context)?, parse(right, context)?)
    else {
        return Err("equation sides need supported expressions".into());
    };
    domain.extend(other_domain);
    let mut algebra = Algebra {
        work: 0,
        depth: 0,
        conditions: BTreeSet::new(),
        nonzero_power_bases: BTreeMap::new(),
        context,
    };
    let difference = algebra.add(&a, &b.neg())?;
    // Retain every condition introduced by the original sides, even if the
    // residual cancels completely. A denominator must not disappear from a domain.
    domain.extend(algebra.conditions);
    if !difference.num.rational_variables_only() || !difference.den.rational_variables_only() {
        return Err("only rational polynomial equation residuals are supported".into());
    }
    Ok((difference.num.monic(), domain))
}

fn circle(poly: &Poly) -> Option<(Vec<String>, Q, Q, Q)> {
    let variables = poly
        .0
        .keys()
        .flat_map(|m| m.keys())
        .map(|atom| {
            if let Atom::Variable(v) = atom {
                Some(v.clone())
            } else {
                None
            }
        })
        .collect::<Option<BTreeSet<_>>>()?;
    if variables.len() != 2 {
        return None;
    }
    let variables: Vec<_> = variables.into_iter().collect();
    let mut square = [Q::zero(), Q::zero()];
    let mut linear = square.clone();
    let mut constant = Q::zero();
    for (mono, coefficient) in &poly.0 {
        if mono.is_empty() {
            constant += coefficient;
            continue;
        }
        if mono.len() != 1 {
            return None;
        }
        let (Atom::Variable(name), exponent) = mono.first_key_value()? else {
            return None;
        };
        let i = variables.iter().position(|v| v == name)?;
        match exponent {
            1 => linear[i] += coefficient,
            2 => square[i] += coefficient,
            _ => return None,
        }
    }
    if square[0].is_zero() || square[0] != square[1] {
        return None;
    }
    let two_a = Q::from_integer(2.into()) * &square[0];
    let x = -&linear[0] / &two_a;
    let y = -&linear[1] / &two_a;
    let radius_squared = &x * &x + &y * &y - constant / &square[0];
    Some((variables, x, y, radius_squared))
}

pub(super) fn compare(a: &str, b: &str, context: Context) -> Option<Result<bool>> {
    // Operator answers such as "=" and "<=" retain their existing dispatch.
    if special(a).is_some() || special(b).is_some() {
        return None;
    }
    if !a.contains('=') && !b.contains('=') {
        return None;
    }
    Some((|| {
        let (a_sides, b_sides) = (sides(a)?, sides(b)?);
        let (Some((al, ar)), Some((bl, br))) = (a_sides, b_sides) else {
            // Validate both inputs before rejecting their different response
            // shapes. Unsupported notation must remain a grading error.
            for (source, pair) in [(a, a_sides), (b, b_sides)] {
                if let Some((l, r)) = pair {
                    residual(l, r, context)?;
                } else {
                    parse(source, context)?;
                }
            }
            return Ok(false);
        };
        let (pa, ca) = residual(al, ar, context)?;
        let (pb, cb) = residual(bl, br, context)?;
        if ca != cb {
            return Err("equation comparison has unresolved domain differences".into());
        }
        if pa == pb {
            return Ok(true);
        }
        if ca.is_empty() {
            if let (Some(a), Some(b)) = (circle(&pa), circle(&pb)) {
                if a.0 != b.0 {
                    return Err("equation variables differ".into());
                }
                // Negative squared radius means an empty real relation. Other
                // circles are uniquely determined by center and squared radius.
                return Ok(if a.3.is_negative() || b.3.is_negative() {
                    a.3.is_negative() && b.3.is_negative()
                } else {
                    a == b
                });
            }
        }
        // Nonproportional polynomials can have the same zero set (x and x²).
        // Never turn absence of a proof into a learner's incorrect answer.
        Err("equation zero-set equivalence is not established by supported rules".into())
    })())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn circle_equations_accept_rearrangement_expansion_and_scaling() {
        assert!(super::super::supports("(x-3)^2+y^2=9", Context::default()));
        for a in [
            "(x-3)^{2}+{y}^{2}=9",
            "9=y^2+(x-3)^2",
            "x^2-6x+y^2=0",
            "-2x^2+12x-2y^2=0",
        ] {
            assert_eq!(
                super::super::compare(a, "(x-3)^2+y^2=9", Context::default()),
                Ok(true)
            );
        }
        assert_eq!(
            super::super::compare("x^2+y^2-12y=0", "(x-0)^2+(y-6)^2=36", Context::default()),
            Ok(true)
        );
        for a in [
            "(x-4)^2+y^2=9",
            "(x-3)^2+y^2=10",
            "(x-3)^2+y^2=-9",
            "987654321",
        ] {
            assert_eq!(
                super::super::compare(a, "(x-3)^2+y^2=9", Context::default()),
                Ok(false)
            );
        }
    }
    #[test]
    fn equation_comparison_preserves_domains_and_unsupported_shapes() {
        let compare = |a, b| super::super::compare(a, b, Context::default());
        assert!(compare("x/x=1", "1=1").is_err());
        assert!(compare("x^2=0", "x=0").is_err());
        assert!(compare("x=y=1", "x=y").is_err());
        assert!(compare("\\unknown{x}=1", "x=1").is_err());
        assert!(compare("x<=1", "x=1").is_err());
        assert_eq!(compare("x^2+y^2=-1", "x^2+y^2=-2"), Ok(true));
        assert_eq!(compare("=", "="), Ok(true));
        assert_eq!(compare("<=", r"\leq"), Ok(true));
        assert_eq!(compare("!=", r"\ne"), Ok(true));
    }
    #[test]
    fn source_multiplication_glyphs_preserve_exact_radical_answers() {
        for glyph in ["∗", "⋅", "×", "·"] {
            let key = format!("3(2{glyph}{{2}}^{{1/3}}-1)");
            assert_eq!(
                super::super::compare(&key, r"3(2\sqrt[3]{2}-1)", Context::default()),
                Ok(true)
            );
            assert_eq!(
                super::super::compare(&key, r"3(2\sqrt[3]{2}+1)", Context::default()),
                Ok(false)
            );
        }
    }
}
