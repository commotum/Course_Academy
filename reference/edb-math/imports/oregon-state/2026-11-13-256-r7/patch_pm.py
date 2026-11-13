from pathlib import Path
p=Path('/home/jake/Developer/Course_Academy/engine/rust/symbolic.rs');s=p.read_text();Path('/tmp/rec7-review/symbolic-before.rs').write_text(s)
a=s.index('fn plus_minus(source: &str)');b=s.index('/// Whether a canonical answer',a)
s=s[:a]+r'''// One plus/minus token denotes two branches, including inside a fraction.
// Multiple independent signs remain unsupported rather than growing an
// unbounded set or guessing whether the signs are correlated.
fn plus_minus_branches(source: &str) -> Result<Option<[String; 2]>> {
    let source = source.trim();
    let mut signs = source.match_indices('±').map(|(i, s)| (i, s.len()))
        .chain(source.match_indices(r"\pm").filter(|(i, token)|
            !source[i + token.len()..].starts_with(|c: char| c.is_ascii_alphabetic()))
            .map(|(i, token)| (i, token.len())));
    let Some((i, len)) = signs.next() else { return Ok(None); };
    if signs.next().is_some() { return Err("multiple plus/minus signs are unsupported".into()); }
    let (before, after) = (&source[..i], &source[i + len..]);
    if i == 0 {
        // Preserve the established leading-sign convention: ±(the remainder).
        return Ok(Some([after.trim().to_owned(), format!("-({after})")]));
    }
    Ok(Some([format!("{before}+{after}"), format!("{before}-{after}")]))
}

''' +s[b:]
s=s.replace('Ok(None) => parse(plus_minus(source).unwrap_or(source), context).is_ok(),','''Ok(None) => match plus_minus_branches(source) {
            Ok(Some(branches)) => branches.iter().all(|branch| parse(branch, context).is_ok()),
            Ok(None) => parse(source, context).is_ok(),
            Err(_) => false,
        },''')
a=s.index('    // A leading plus/minus denotes two possible values.');b=s.index('    compare_single(a, b, context)',a)
s=s[:a]+r'''    if let (None, None) = (plus_minus_branches(a)?, plus_minus_branches(b)?) {
        return compare_single(a, b, context);
    }
    let aa = plus_minus_branches(a)?.unwrap_or_else(|| [a.to_owned(), a.to_owned()]);
    let bb = plus_minus_branches(b)?.unwrap_or_else(|| [b.to_owned(), b.to_owned()]);
    // Validate all branches before comparing: malformed notation must never
    // become a learner failure just because another branch differs.
    for branch in aa.iter().chain(bb.iter()) { parse(branch, context)?; }
    let both = |left: Result<bool>, right: Result<bool>| match (left, right) {
        (Ok(false), _) | (_, Ok(false)) => Ok(false),
        (Ok(true), Ok(true)) => Ok(true),
        (Err(error), _) | (_, Err(error)) => Err(error),
    };
    let direct = both(compare_single(&aa[0], &bb[0], context), compare_single(&aa[1], &bb[1], context));
    let swapped = both(compare_single(&aa[0], &bb[1], context), compare_single(&aa[1], &bb[0], context));
    // Either bijection proves equality of the two possible values. Treat a
    // scalar as a repeated pair so a single root cannot pass for two roots.
    match (direct, swapped) {
        (Ok(true), _) | (_, Ok(true)) => Ok(true),
        (Ok(false), Ok(false)) => Ok(false),
        (Err(error), _) | (_, Err(error)) => Err(error),
    }
''' +s[b+len('    compare_single(a, b, context)\n'):]
a=s.index('    #[test]\n    fn fractional_counterexamples_reject_wrong_radical_answers()')
s=s[:a]+r'''    #[test]
    fn embedded_plus_minus_preserves_both_quadratic_roots() {
        let answer = r"\frac{5\pm\sqrt{17}}{4}";
        assert!(supports(answer, Context::default()));
        for same in [answer, r"\frac54\pm\frac{\sqrt{17}}4", "(5±sqrt(17))/4"] {
            eq(answer, same);
            eq(same, answer);
        }
        for wrong in ["0", "(5+sqrt(17))/4", "(5-sqrt(17))/4", r"\frac{5\pm\sqrt{17}}{2}"] {
            assert_eq!(compare(answer, wrong, Context::default()), Ok(false));
            assert_eq!(compare(wrong, answer, Context::default()), Ok(false));
        }
        eq(r"2\pm0", "2");
        assert!(!supports(r"1\pm2\pm3", Context::default()));
        assert!(compare(r"1\pm unknown(x)", "0", Context::default()).is_err());
        assert!(compare(r"(5\pm\sqrt{17})x/(4x)", answer, Context::default()).is_err());
    }

''' +s[a:]
p.write_text(s)
print('Added bounded two-branch support for embedded plus/minus notation; preserved prior edits.')
