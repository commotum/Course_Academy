//! Formal expressions used in two-function differential-operator proofs.
//!
//! Derivatives are independent jet coordinates, not quotients of letters d.
//! Operator applications are uninterpreted atoms: this does not assume the
//! linearity that the learner is being asked to establish.
use super::Context;
use crate::Result;
use regex::Regex;

fn replace(source: String, pattern: &str, value: &str) -> String {
    Regex::new(pattern).unwrap().replace_all(&source, value).into_owned()
}

fn indexed_functions(source: &str) -> bool {
    ["y_1", "y_2", "y_{1}", "y_{2}", "y}_{1}", "y}_{2}"]
        .iter().any(|part| source.contains(part))
}

fn normalize(source: &str) -> Result<String> {
    if source.len() > 4096 { return Err("formal expression exceeds 4096 bytes".into()); }
    let mut s = source.replace('′', "'").replace('″', "''").replace('−', "-");
    for wrapper in [r"\text{d}", r"\mathrm{d}", r"\textrm{d}"] { s = s.replace(wrapper, "d"); }
    s = s.replace(r"\dfrac", r"\frac").replace(r"\tfrac", r"\frac")
        .replace(r"\left", "").replace(r"\right", "")
        .replace(r"\cdot", "*").replace(r"\times", "*")
        .replace(r"\neq", "≠").replace(r"\ne", "≠").replace("!=", "≠")
        .replace(r"\prime", "'");
    for space in [r"\,", r"\;", r"\:", r"\!", r"\quad", r"\qquad"] { s = s.replace(space, ""); }
    s.retain(|c| !c.is_whitespace());
    for _ in 0..3 { s = replace(s, r"\{([abdyx])\}", "$1"); }
    s = replace(s, r"_\{([12])\}", "_$1");
    s = replace(s, r"\^\{([12])\}", "^$1");
    s = replace(s, r"y('+)_(1|2)", "y_$2$1");
    s = replace(s, r"y_([12])\^\{('+?)\}", "y_$1$2");
    s = replace(s, r"y_([12])\(x\)", "y_$1");
    if Regex::new(r"y_(?:[3-9]|[12][0-9])").unwrap().is_match(&s) {
        return Err("formal proof uses the specified functions y_1 and y_2".into());
    }
    // Reject user-supplied atom names before introducing private coordinates.
    // Otherwise typing p could impersonate the private atom for y_1'.
    let vocabulary = s.replace(r"\frac", "");
    if vocabulary.chars().any(|c| c.is_alphabetic() && !"abdyxDL".contains(c)) {
        return Err("unsupported formal differential-operator notation".into());
    }
    for (index, plain, first, second) in [(1, "u", "p", "r"), (2, "v", "q", "s")] {
        s = s.replace(&format!(r"\frac{{d^2y_{index}}}{{dx^2}}"), second)
            .replace(&format!(r"\frac{{dy_{index}}}{{dx}}"), first)
            .replace(&format!("y_{index}''"), second)
            .replace(&format!("y_{index}'"), first)
            .replace(&format!("y_{index}"), plain);
    }
    if s.chars().any(|c| "dy".contains(c)) {
        return Err("unsupported derivative; use derivatives of y_1 or y_2 with respect to x".into());
    }
    Ok(s)
}

#[derive(Default)]
struct Applications(Vec<(char, String, char)>);

impl Applications {
    fn rewrite(&mut self, source: &str, context: Context, depth: usize) -> Result<String> {
        if depth > 8 { return Err("operator application nesting exceeds 8".into()); }
        let mut out = String::new();
        let mut offset = 0;
        while offset < source.len() {
            let ch = source[offset..].chars().next().unwrap();
            if matches!(ch, 'D' | 'L') {
                let start = offset + 1;
                if !source[start..].starts_with('(') { return Err("operator requires an argument".into()); }
                let mut level = 1;
                let mut end = None;
                for (i, c) in source[start + 1..].char_indices() {
                    if c == '(' { level += 1; }
                    if c == ')' { level -= 1; }
                    if level == 0 { end = Some(start + 1 + i); break; }
                }
                let end = end.ok_or("unclosed operator argument")?;
                let argument = self.rewrite(&source[start + 1..end], context, depth + 1)?;
                super::compare(&argument, &argument, context)?;
                let mut found = None;
                for (name, other, atom) in &self.0 {
                    if *name == ch && super::compare(&argument, other, context)? {
                        found = Some(*atom); break;
                    }
                }
                let atom = if let Some(atom) = found { atom } else {
                    let atom = "cdfghjklmnotwz".chars().nth(self.0.len())
                        .ok_or("too many distinct formal operator applications")?;
                    self.0.push((ch, argument, atom)); atom
                };
                out.push(atom);
                offset = end + 1;
            } else {
                out.push(ch); offset += ch.len_utf8();
            }
        }
        Ok(out)
    }
}

fn relation(source: &str) -> Result<Option<(&str, char, &str)>> {
    let mut depth = 0;
    let mut result = None;
    for (i, c) in source.char_indices() {
        match c {
            '(' | '{' => depth += 1,
            ')' | '}' => depth -= 1,
            '=' | '≠' if depth == 0 => {
                if result.is_some() { return Err("one comparison is required per proof blank".into()); }
                result = Some((&source[..i], c, &source[i + c.len_utf8()..]));
            }
            _ => {}
        }
        if depth < 0 { return Err("unbalanced formal expression".into()); }
    }
    if depth != 0 { return Err("unbalanced formal expression".into()); }
    Ok(result)
}

pub(super) fn compare(a: &str, b: &str, context: Context) -> Option<Result<bool>> {
    if !indexed_functions(b) || !(b.contains(r"\frac") || b.contains("L(") || b.contains("D(")
        || b.contains(r"L\left(") || b.contains(r"D\left(")) { return None; }
    Some((|| {
        let (a, b) = (normalize(a)?, normalize(b)?);
        let mut applications = Applications::default();
        // Canonical applications define private atoms first; entered spellings
        // share an atom only after their arguments are proved equivalent.
        let b = applications.rewrite(&b, context, 0)?;
        let a = applications.rewrite(&a, context, 0)?;
        match (relation(&a)?, relation(&b)?) {
            (None, None) => super::compare(&a, &b, context),
            (Some((al, op, ar)), Some((bl, expected, br))) if op == expected => {
                Ok((super::compare(al, bl, context)? && super::compare(ar, br, context)?)
                    || (super::compare(al, br, context)? && super::compare(ar, bl, context)?))
            }
            _ => Ok(false),
        }
    })())
}

#[cfg(test)]
mod tests {
    use super::*;
    fn cmp(a: &str, b: &str) -> Result<bool> { compare(a, b, Context::default()).unwrap() }

    #[test]
    fn derivative_notations_are_independent_jet_coordinates() {
        let key = r"{a}^{2}{\left(\frac{\text{d}{y}_{1}}{\text{d}x}\right)}^{2}+{b}^{2}{\left(\frac{\text{d}{y}_{2}}{\text{d}x}\right)}^{2}";
        assert_eq!(cmp("b^2(y_2')^2+a^2(y_1')^2", key), Ok(true));
        assert_eq!(cmp("a^2(y'_1)^2+b^2(y'_2)^2", key), Ok(true));
        assert_eq!(cmp("a^2*y_1^2/x^2+b^2*y_2^2/x^2", key), Ok(false));
        assert_eq!(cmp("(a*y_1'+b*y_2')^2", key), Ok(false));
        assert!(cmp("a^2*p^2+b^2*q^2", key).is_err());
        let second = r"a\frac{{\text{d}}^{2}{y}_{1}}{\text{d}{x}^{2}}+b\frac{{\text{d}}^{2}{y}_{2}}{\text{d}{x}^{2}}";
        assert_eq!(cmp("b*y_2''+a*y_1''", second), Ok(true));
        assert_eq!(cmp("a*y_1'+b*y_2'", second), Ok(false));
    }

    #[test]
    fn operator_conditions_do_not_assume_linearity() {
        let key = r"L(a{y}_{1}+b{y}_{2})=aL({y}_{1})+bL({y}_{2})";
        assert_eq!(cmp("bL(y_2)+aL(y_1)=L(by_2+ay_1)", key), Ok(true));
        assert_eq!(cmp("L(ay_1+by_2)=L(y_1)+L(y_2)", key), Ok(false));
        assert_eq!(cmp("L(ay_1*by_2)=abL(y_1)*L(y_2)", key), Ok(false));
        assert_eq!(cmp(r"L(ay_1+by_2)\ne aL(y_1)+bL(y_2)", key), Ok(false));
        assert!(cmp("c=ad+bf", key).is_err());
        let inequality = r"D(a{y}_{1}+b{y}_{2})\ne aD({y}_{1})+bD({y}_{2})";
        assert_eq!(cmp(r"aD(y_1)+bD(y_2)\neq D(by_2+ay_1)", inequality), Ok(true));
        assert_eq!(cmp("D(ay_1+by_2)=aD(y_1)+bD(y_2)", inequality), Ok(false));
    }

    #[test]
    fn ordinary_answers_keep_the_existing_comparison_path() {
        assert!(compare("x+x", "2x", Context::default()).is_none());
        assert!(compare("y_1+y_2", "y_2+y_1", Context::default()).is_none());
        assert!(cmp("L(ay_1+by_2", "L(ay_1+by_2)=aL(y_1)+bL(y_2)").is_err());
    }
}
