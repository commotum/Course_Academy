//! Application stopping, exact XP candidates, and diagnostic placement.
//! These local policies are separate from FIRe retention and persistence.
use crate::Result;
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet, VecDeque};

/// None denotes an explicit skip of a presented question.
pub type Outcome = Option<bool>;

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct PracticeDecision {
    pub status: String,
    pub attempted: usize,
    pub correct: usize,
    pub streak: usize,
}
impl PracticeDecision {
    pub fn complete(&self) -> bool {
        self.status != "continue"
    }
    pub fn passed(&self) -> Option<bool> {
        self.complete().then_some(self.status == "passed")
    }
}

fn practice_prefix(outcomes: &[Outcome], required_streak: usize) -> Result<PracticeDecision> {
    let mut decision = PracticeDecision {
        status: "continue".into(),
        attempted: 0,
        correct: 0,
        streak: 0,
    };
    for outcome in outcomes {
        if decision.complete() {
            return Err("outcomes continue beyond the first terminal prefix".into());
        }
        decision.attempted += 1;
        if *outcome == Some(true) {
            decision.correct += 1;
            decision.streak += 1;
        } else {
            decision.streak = 0;
        }
        decision.status = if decision.streak >= required_streak {
            "passed"
        } else if decision.attempted == 5 {
            "failed"
        } else {
            "continue"
        }
        .into();
    }
    Ok(decision)
}
pub fn evaluate_kp_prefix(outcomes: &[Outcome]) -> Result<PracticeDecision> {
    practice_prefix(outcomes, 2)
}
pub fn evaluate_review_prefix(outcomes: &[Outcome]) -> Result<PracticeDecision> {
    practice_prefix(outcomes, 3)
}

/// Convert numeric inputs to an exact rational. Floats use their decimal
/// representation, matching Python Fraction(str(value)), not their binary ratio.
pub trait ExactNumber {
    fn exact(self) -> Result<BigRational>;
}
impl ExactNumber for BigRational {
    fn exact(self) -> Result<BigRational> {
        Ok(self)
    }
}
impl ExactNumber for &BigRational {
    fn exact(self) -> Result<BigRational> {
        Ok(self.clone())
    }
}
impl ExactNumber for BigInt {
    fn exact(self) -> Result<BigRational> {
        Ok(BigRational::from_integer(self))
    }
}
impl ExactNumber for &BigInt {
    fn exact(self) -> Result<BigRational> {
        Ok(BigRational::from_integer(self.clone()))
    }
}
macro_rules! exact_integer { ($($t:ty),*) => {$(impl ExactNumber for $t {
    fn exact(self) -> Result<BigRational> { Ok(BigRational::from_integer(BigInt::from(self))) }
})*}; }
exact_integer!(
    i8, i16, i32, i64, i128, isize, u8, u16, u32, u64, u128, usize
);
impl ExactNumber for f64 {
    fn exact(self) -> Result<BigRational> {
        if !self.is_finite() {
            return Err("value must be a finite number".into());
        }
        decimal_number(&self.to_string())
    }
}

/// Explicit parser for decimal inputs such as arbitrary precision Decimal.
pub fn decimal_number(value: &str) -> Result<BigRational> {
    let invalid = || "value must be a finite number".to_string();
    let (mantissa, exponent) = match value.find(['e', 'E']) {
        Some(at) => (
            &value[..at],
            value[at + 1..].parse::<i32>().map_err(|_| invalid())?,
        ),
        None => (value, 0),
    };
    let fraction_len = mantissa.split_once('.').map_or(0, |(_, tail)| tail.len());
    let digits = mantissa.replace('.', "");
    if mantissa.chars().filter(|c| *c == '.').count() > 1 {
        return Err(invalid());
    }
    let numerator = digits.parse::<BigInt>().map_err(|_| invalid())?;
    let scale = i64::try_from(fraction_len).map_err(|_| invalid())? - i64::from(exponent);
    let power: u32 = scale.unsigned_abs().try_into().map_err(|_| invalid())?;
    let factor = BigInt::from(10).pow(power);
    Ok(if scale >= 0 {
        BigRational::new(numerator, factor)
    } else {
        BigRational::from_integer(numerator * factor)
    })
}

/// floor(x + 1/2), including ties toward positive infinity for negative XP.
pub fn round_half_up(value: impl ExactNumber) -> Result<BigInt> {
    let shifted = value.exact()? + BigRational::new(1.into(), 2.into());
    let mut quotient = shifted.numer() / shifted.denom();
    if shifted.is_negative() && !(shifted.numer() % shifted.denom()).is_zero() {
        quotient -= 1;
    }
    Ok(quotient)
}
fn xp_inputs(base: impl ExactNumber, outcomes: &[Outcome]) -> Result<BigRational> {
    let base = base.exact()?;
    if base.is_negative() {
        return Err("base XP must be nonnegative".into());
    }
    if outcomes.is_empty() {
        return Err("XP requires at least one presented question".into());
    }
    Ok(base)
}
fn accuracy(outcomes: &[Outcome]) -> BigRational {
    BigRational::new(
        outcomes.iter().filter(|v| **v == Some(true)).count().into(),
        outcomes.len().into(),
    )
}
pub fn assessment_xp_candidate(base: impl ExactNumber, outcomes: &[Outcome]) -> Result<BigInt> {
    let baseline = xp_inputs(base, outcomes)?;
    let award = round_half_up(
        baseline
            * BigRational::new(6.into(), 5.into())
            * (accuracy(outcomes) - BigRational::new(7.into(), 20.into()))
            / BigRational::new(13.into(), 20.into()),
    )?;
    Ok(award.max(BigInt::zero()))
}
pub fn multistep_xp_candidate(base: impl ExactNumber, outcomes: &[Outcome]) -> Result<BigInt> {
    let baseline = xp_inputs(base, outcomes)?;
    round_half_up(
        baseline * (BigRational::new(9.into(), 4.into()) * accuracy(outcomes) - BigRational::one()),
    )
}
pub fn lesson_xp_candidate(
    base: impl ExactNumber,
    outcomes: &[Outcome],
    award: Option<BigInt>,
) -> Result<BigInt> {
    let baseline = xp_inputs(base, outcomes)?;
    if let Some(award) = award {
        return Ok(award);
    }
    if !outcomes.iter().all(|v| *v == Some(true)) {
        return Err("partial lesson XP is unresolved; supply an explicit award".into());
    }
    round_half_up(baseline * BigRational::new(5.into(), 4.into()))
}
pub fn review_xp_candidate(
    base: impl ExactNumber,
    outcomes: &[Outcome],
    award: Option<BigInt>,
) -> Result<BigInt> {
    let baseline = xp_inputs(base, outcomes)?;
    if let Some(award) = award {
        return Ok(award);
    }
    if !outcomes.iter().all(|v| *v == Some(true)) {
        return Err("partial review XP is unresolved; supply an explicit award".into());
    }
    round_half_up(baseline + BigRational::from_integer(2.into()))
}

/// Signed placement evidence on a prerequisite DAG. Each answer contributes
/// once to each reachable topic; negative evidence travels toward descendants.
#[derive(Clone, Debug)]
pub struct DiagnosticBalance {
    down: BTreeMap<String, BTreeSet<String>>,
    up: BTreeMap<String, BTreeSet<String>>,
    pub skip_policy: String,
    balances: BTreeMap<String, f64>,
}
impl DiagnosticBalance {
    pub fn new(prerequisites: BTreeMap<String, Vec<String>>, skip_policy: &str) -> Result<Self> {
        if !matches!(skip_policy, "negative" | "neutral") {
            return Err("skip_policy must explicitly be negative or neutral".into());
        }
        let mut down = BTreeMap::new();
        let mut topics = BTreeSet::new();
        for (topic, parents) in prerequisites {
            if topic.is_empty() || parents.iter().any(String::is_empty) {
                return Err("topic IDs must be nonempty strings".into());
            }
            let parent_set: BTreeSet<_> = parents.iter().cloned().collect();
            if parent_set.len() != parents.len() {
                return Err("duplicate prerequisite edge".into());
            }
            topics.insert(topic.clone());
            topics.extend(parents);
            down.insert(topic, parent_set);
        }
        for topic in &topics {
            down.entry(topic.clone()).or_insert_with(BTreeSet::new);
        }
        let mut up: BTreeMap<_, BTreeSet<String>> = topics
            .iter()
            .map(|t| (t.clone(), BTreeSet::new()))
            .collect();
        for (topic, parents) in &down {
            for parent in parents {
                up.get_mut(parent).unwrap().insert(topic.clone());
            }
        }
        let mut remaining: BTreeMap<_, _> =
            down.iter().map(|(t, p)| (t.clone(), p.len())).collect();
        let mut ready: VecDeque<_> = remaining
            .iter()
            .filter(|(_, n)| **n == 0)
            .map(|(t, _)| t.clone())
            .collect();
        let mut visited = 0;
        while let Some(topic) = ready.pop_front() {
            visited += 1;
            for child in &up[&topic] {
                let count = remaining.get_mut(child).unwrap();
                *count -= 1;
                if *count == 0 {
                    ready.push_back(child.clone());
                }
            }
        }
        if visited != topics.len() {
            return Err("diagnostic prerequisites must be acyclic".into());
        }
        Ok(Self {
            down,
            up,
            skip_policy: skip_policy.into(),
            balances: topics.into_iter().map(|t| (t, 0.0)).collect(),
        })
    }
    pub fn apply(
        &mut self,
        topic: &str,
        outcome: Outcome,
        weight: f64,
    ) -> Result<BTreeMap<String, f64>> {
        if topic.is_empty() {
            return Err("topic IDs must be nonempty strings".into());
        }
        if !self.balances.contains_key(topic) {
            return Err("topic is outside the diagnostic graph".into());
        }
        if !weight.is_finite() || weight <= 0.0 || weight > 1.0 {
            return Err("weight must satisfy 0 < weight <= 1".into());
        }
        if outcome != Some(true) && weight != 1.0 {
            return Err("reduced diagnostic weights apply only to correct answers".into());
        }
        if outcome.is_none() && self.skip_policy == "neutral" {
            return Ok(BTreeMap::new());
        }
        let graph = if outcome == Some(true) {
            &self.down
        } else {
            &self.up
        };
        let mut reached = BTreeSet::new();
        let mut pending = vec![topic.to_string()];
        while let Some(current) = pending.pop() {
            if reached.insert(current.clone()) {
                pending.extend(graph[&current].iter().cloned());
            }
        }
        let delta = if outcome == Some(true) { weight } else { -1.0 };
        if reached
            .iter()
            .any(|t| !(self.balances[t] + delta).is_finite())
        {
            return Err("diagnostic balance overflow".into());
        }
        let changes = reached
            .into_iter()
            .map(|t| (t, delta))
            .collect::<BTreeMap<_, _>>();
        for (target, delta) in &changes {
            *self.balances.get_mut(target).unwrap() += delta;
        }
        Ok(changes)
    }
    pub fn snapshot(&self) -> BTreeMap<String, f64> {
        self.balances.clone()
    }
    pub fn positive_repetitions(&self) -> BTreeMap<String, f64> {
        self.balances
            .iter()
            .filter(|(_, b)| **b > 0.0)
            .map(|(t, b)| (t.clone(), *b))
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn stopping_and_skip_order() {
        assert_eq!(evaluate_kp_prefix(&[]).unwrap().passed(), None);
        assert_eq!(
            evaluate_kp_prefix(&[Some(true), None, Some(true)])
                .unwrap()
                .streak,
            1
        );
        assert_eq!(
            evaluate_kp_prefix(&[Some(true), Some(false), Some(true), Some(true)])
                .unwrap()
                .passed(),
            Some(true)
        );
        assert_eq!(
            evaluate_review_prefix(&[Some(false), Some(false), Some(true), Some(true), Some(true)])
                .unwrap()
                .passed(),
            Some(true)
        );
        assert_eq!(
            evaluate_review_prefix(&[Some(true), Some(true), Some(false), Some(false), Some(true)])
                .unwrap()
                .passed(),
            Some(false)
        );
        assert!(evaluate_kp_prefix(&[Some(true), Some(true), Some(false)]).is_err());
        assert!(evaluate_review_prefix(&[Some(true); 4]).is_err());
        assert!(evaluate_kp_prefix(&[Some(false); 6]).is_err());
    }
    #[test]
    fn exact_awards_and_rounding() {
        assert_eq!(round_half_up(-2.5).unwrap(), BigInt::from(-2));
        assert_eq!(
            round_half_up(BigRational::new((-8).into(), 3.into())).unwrap(),
            BigInt::from(-3)
        );
        assert_eq!(
            round_half_up(decimal_number("1e40").unwrap() + BigRational::new(1.into(), 2.into()))
                .unwrap(),
            BigInt::from(10).pow(40) + 1
        );
        for (base, correct, count, award) in [
            (15, 7, 10, 10),
            (15, 5, 8, 8),
            (15, 7, 9, 12),
            (15, 10, 11, 15),
            (13, 7, 7, 16),
            (15, 8, 8, 18),
            (13, 7, 8, 13),
            (11, 2, 8, 0),
            (15, 8, 12, 9),
            (12, 11, 11, 14),
            (11, 6, 9, 6),
            (12, 4, 9, 2),
        ] {
            let outcomes: Vec<_> = (0..count).map(|i| Some(i < correct)).collect();
            assert_eq!(
                assessment_xp_candidate(base, &outcomes).unwrap(),
                BigInt::from(award)
            );
        }
        for (base, correct, count, award) in [
            (10, 7, 7, 13),
            (10, 5, 7, 6),
            (15, 8, 10, 12),
            (7, 5, 9, 2),
            (14, 7, 9, 11),
            (7, 7, 8, 7),
        ] {
            let outcomes: Vec<_> = (0..count).map(|i| Some(i < correct)).collect();
            assert_eq!(
                multistep_xp_candidate(base, &outcomes).unwrap(),
                BigInt::from(award)
            );
        }
        assert_eq!(
            multistep_xp_candidate(7, &[None]).unwrap(),
            BigInt::from(-7)
        );
        assert_eq!(
            lesson_xp_candidate(16, &[Some(true); 8], None).unwrap(),
            BigInt::from(20)
        );
        assert_eq!(
            review_xp_candidate(7, &[Some(true); 3], None).unwrap(),
            BigInt::from(9)
        );
        assert!(lesson_xp_candidate(7, &[Some(false)], None).is_err());
        assert_eq!(
            lesson_xp_candidate(7, &[Some(false)], Some((-1).into())).unwrap(),
            BigInt::from(-1)
        );
        assert!(assessment_xp_candidate(-1, &[Some(true)]).is_err());
        assert!(assessment_xp_candidate(f64::NAN, &[Some(true)]).is_err());
        assert!(review_xp_candidate(1, &[], None).is_err());
    }
    fn diamond(policy: &str) -> DiagnosticBalance {
        DiagnosticBalance::new(
            BTreeMap::from([
                ("advanced".into(), vec!["left".into(), "right".into()]),
                ("left".into(), vec!["basic".into()]),
                ("right".into(), vec!["basic".into()]),
                ("unrelated".into(), vec![]),
            ]),
            policy,
        )
        .unwrap()
    }
    #[test]
    fn diagnostic_direction_deduplication_weights_and_atomic_errors() {
        let mut d = diamond("negative");
        assert_eq!(d.apply("advanced", Some(true), 1.0).unwrap().len(), 4);
        d.apply("basic", Some(false), 1.0).unwrap();
        assert!(d.positive_repetitions().is_empty());
        d.apply("advanced", Some(true), 0.25).unwrap();
        d.apply("right", Some(true), 1.0).unwrap();
        assert_eq!(d.snapshot()["basic"], 1.25);
        d.apply("left", Some(false), 1.0).unwrap();
        assert_eq!(d.snapshot()["advanced"], -0.75);
        let before = d.snapshot();
        for (topic, outcome, weight) in [
            ("unknown", Some(true), 1.0),
            ("basic", Some(true), 0.0),
            ("basic", Some(true), f64::NAN),
            ("basic", Some(false), 0.5),
            ("basic", None, 0.5),
        ] {
            assert!(d.apply(topic, outcome, weight).is_err());
            assert_eq!(d.snapshot(), before);
        }
        let mut neutral = diamond("neutral");
        assert!(neutral.apply("left", None, 1.0).unwrap().is_empty());
        assert!(neutral.snapshot().values().all(|v| *v == 0.0));
        assert!(
            DiagnosticBalance::new(BTreeMap::from([("A".into(), vec!["A".into()])]), "negative")
                .is_err()
        );
        assert!(
            DiagnosticBalance::new(
                BTreeMap::from([("A".into(), vec!["B".into(), "B".into()])]),
                "negative"
            )
            .is_err()
        );
    }
}
