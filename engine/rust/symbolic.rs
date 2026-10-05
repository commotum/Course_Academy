//! Bounded exact algebra for entered answers. This is deliberately not a CAS.
//!
//! Rational functions over named variables and supported function atoms use
//! BigRational coefficients. Root, imaginary-unit, and trig relations are
//! exact. Domain obligations survive cancellation. No floating point or
//! numerical samples are used to accept an answer.
use crate::{Result, activities::decimal_number};
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use num_traits::{One, Signed, ToPrimitive, Zero};
use std::collections::{BTreeMap, BTreeSet};

const MAX_TERMS: usize = 128;
const MAX_POWER: u32 = 64;
const MAX_WORK: usize = 100_000;
const MAX_BITS: u64 = 16_384;
const MAX_STRUCTURE: usize = 4_096;

#[derive(Clone, Copy, Debug, Default)]
pub struct Context {
    /// Sigma indices and vector basis labels use i as a formal symbol.
    pub symbolic_i: bool,
    /// Sequence/sigma indices n, k, j, and i are integers in these prompts.
    pub integer_indices: bool,
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
enum Atom {
    Variable(String),
    Pi,
    E,
    I,
    Root(u8, Box<Poly>),
    Function(String, Box<Value>),
    Power(Box<Value>, Box<Value>),
}
type Mono = BTreeMap<Atom, u16>;
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
struct Poly(BTreeMap<Mono, Q>);
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
struct Value {
    num: Poly,
    den: Poly,
}
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
enum Condition {
    Nonzero(Poly),
    Nonnegative(Value),
    Positive(Value),
}
#[derive(Clone, Debug, PartialEq, Eq)]
enum Answer {
    Special(String),
    Expression(Value, BTreeSet<Condition>),
}

impl Poly {
    fn bounded_structure(&self) -> bool {
        fn poly(p: &Poly, left: &mut usize, depth: usize) -> bool {
            if depth > 64 {
                return false;
            }
            for m in p.0.keys() {
                for a in m.keys() {
                    if *left == 0 {
                        return false;
                    }
                    *left -= 1;
                    let ok = match a {
                        Atom::Root(_, p) => poly(p, left, depth + 1),
                        Atom::Function(_, v) => value(v, left, depth + 1),
                        Atom::Power(a, b) => value(a, left, depth + 1) && value(b, left, depth + 1),
                        _ => true,
                    };
                    if !ok {
                        return false;
                    }
                }
            }
            true
        }
        fn value(v: &Value, left: &mut usize, depth: usize) -> bool {
            poly(&v.num, left, depth) && poly(&v.den, left, depth)
        }
        let mut left = MAX_STRUCTURE;
        poly(self, &mut left, 0)
    }
    fn number(q: Q) -> Self {
        Self(if q.is_zero() {
            BTreeMap::new()
        } else {
            BTreeMap::from([(Mono::new(), q)])
        })
    }
    fn integer(n: i64) -> Self {
        Self::number(Q::from_integer(n.into()))
    }
    fn atom(a: Atom) -> Self {
        Self(BTreeMap::from([(BTreeMap::from([(a, 1)]), Q::one())]))
    }
    fn constant(&self) -> Option<Q> {
        if self.0.is_empty() {
            return Some(Q::zero());
        }
        if self.0.len() == 1 {
            let (m, c) = self.0.first_key_value()?;
            if m.is_empty() {
                return Some(c.clone());
            }
        }
        None
    }
    fn is_zero(&self) -> bool {
        self.0.is_empty()
    }
    fn scale(&self, c: &Q) -> Self {
        if c.is_zero() {
            return Self::integer(0);
        }
        Self(self.0.iter().map(|(m, v)| (m.clone(), v * c)).collect())
    }
    fn monic(&self) -> Self {
        match self.0.first_key_value() {
            Some((_, c)) => self.scale(&c.recip()),
            None => self.clone(),
        }
    }
    fn nonnegative(&self) -> bool {
        self.0.iter().all(|(m, c)| {
            c.is_positive()
                && m.iter().all(|(a, p)| {
                    p % 2 == 0
                        || matches!(a, Atom::E | Atom::Pi)
                        || matches!(a, Atom::Root(n, _) if n % 2 == 0)
                        || matches!(a, Atom::Function(n, _) if n == "exp" || n == "abs")
                })
        })
    }
    fn positive(&self) -> bool {
        self.nonnegative()
            && self.0.iter().any(|(m, c)| {
                c.is_positive()
                    && m.keys().all(|a| {
                        matches!(a, Atom::E | Atom::Pi)
                            || matches!(a, Atom::Function(n,_) if n == "exp")
                    })
            })
    }
    fn rational_variables_only(&self) -> bool {
        self.0
            .keys()
            .all(|m| m.keys().all(|a| matches!(a, Atom::Variable(_) | Atom::I)))
    }
    fn interval(&self) -> Option<(Q, Q)> {
        self.interval_at(None)
    }
    fn interval_at(&self, sample: Option<i64>) -> Option<(Q, Q)> {
        if self.0.len() > 16
            || self.0.iter().any(|(m, c)| {
                m.values().copied().sum::<u16>() > 32
                    || c.numer().bits().max(c.denom().bits()) > 256
            })
        {
            return None;
        }
        let mut lo = Q::zero();
        let mut hi = Q::zero();
        for (m, c) in &self.0 {
            let mut interval = (c.clone(), c.clone());
            for (a, e) in m {
                let bounds = match a {
                    Atom::Pi => (Q::from_integer(3.into()), Q::from_integer(4.into())),
                    Atom::E => (Q::from_integer(2.into()), Q::from_integer(3.into())),
                    Atom::I => return None,
                    Atom::Variable(name) => {
                        let n = sample?;
                        // Distinct values prevent x-y from vanishing at every
                        // witness. These are exact substitutions, not floats.
                        let offset = name.bytes().map(u64::from).sum::<u64>() % 7;
                        let v = Q::from_integer((n + offset as i64).into());
                        (v.clone(), v)
                    }
                    Atom::Function(name, arg) => {
                        let (l, h) = arg.interval_at(sample)?;
                        function_interval(name, &l, &h)?
                    }
                    Atom::Power(base, exponent) => {
                        let (l, h) = base.interval_at(sample)?;
                        let (a, b) = exponent.interval_at(sample)?;
                        if a != b || !a.is_integer() {
                            return None;
                        }
                        let n = a.to_integer().to_i32()?;
                        if n.unsigned_abs() > 64 || (n <= 0 && l <= Q::zero() && h >= Q::zero()) {
                            return None;
                        }
                        let mut powers = vec![l.pow(n), h.pow(n)];
                        if n > 0 && n % 2 == 0 && l <= Q::zero() && h >= Q::zero() {
                            powers.push(Q::zero());
                        }
                        (powers.iter().min()?.clone(), powers.iter().max()?.clone())
                    }
                    Atom::Root(n, p) => {
                        let (l, h) = p.interval_at(sample)?;
                        (root_bounds(&l, *n)?.0, root_bounds(&h, *n)?.1)
                    }
                };
                for _ in 0..*e {
                    interval = interval_mul(&interval, &bounds);
                }
                if interval.0.numer().bits().max(interval.0.denom().bits()) > MAX_BITS
                    || interval.1.numer().bits().max(interval.1.denom().bits()) > MAX_BITS
                {
                    return None;
                }
            }
            lo += interval.0;
            hi += interval.1;
        }
        Some((lo, hi))
    }
}
fn root_bounds(v: &Q, n: u8) -> Option<(Q, Q)> {
    if v.numer().bits().max(v.denom().bits()) > 128 {
        return None;
    }
    if v.is_negative() {
        if n % 2 == 0 {
            return None;
        }
        let (l, h) = root_bounds(&-v, n)?;
        return Some((-h, -l));
    }
    let mut l = Q::zero();
    let mut h = v.clone().max(Q::one());
    for _ in 0..24 {
        let mid = (&l + &h) / Q::from_integer(2.into());
        if mid.pow(i32::from(n)) <= *v {
            l = mid;
        } else {
            h = mid;
        }
    }
    Some((l, h))
}
fn log_bounds(x: &Q) -> Option<(Q, Q)> {
    if !x.is_positive() || x.numer().bits().max(x.denom().bits()) > 128 {
        return None;
    }
    let t = (x - Q::one()) / (x + Q::one());
    if t.abs() > Q::new(9.into(), 10.into()) {
        return None;
    }
    let square = &t * &t;
    let mut power = t.clone();
    let mut sum = Q::zero();
    for k in 0..24 {
        sum += &power / Q::from_integer((2 * k + 1).into());
        power *= &square;
    }
    sum *= Q::from_integer(2.into());
    let remainder = Q::from_integer(2.into()) * power.abs()
        / (Q::from_integer(49.into()) * (Q::one() - square));
    Some((&sum - &remainder, sum + remainder))
}
fn trig_bounds(name: &str, x: &Q) -> Option<(Q, Q)> {
    if x.abs() > Q::from_integer(16.into()) || x.numer().bits().max(x.denom().bits()) > 128 {
        return None;
    }
    let cosine = name == "cos";
    let mut term = if cosine { Q::one() } else { x.clone() };
    let mut sum = term.clone();
    // Taylor's theorem: derivatives of real sine/cosine have absolute value
    // at most one. The next-degree absolute term bounds the remainder.
    let mut degree = if cosine { 0 } else { 1 };
    for _ in 0..39 {
        term *= -x * x / Q::from_integer(((degree + 1) * (degree + 2)).into());
        sum += &term;
        degree += 2;
    }
    let remainder = term.abs() * x.abs() / Q::from_integer((degree + 1).into());
    Some((&sum - &remainder, sum + remainder))
}
fn exp_bounds(x: &Q) -> Option<(Q, Q)> {
    if x.abs() > Q::from_integer(16.into()) || x.numer().bits().max(x.denom().bits()) > 128 {
        return None;
    }
    let mut sum = Q::one();
    let mut term = Q::one();
    for k in 1..=80 {
        term *= x / Q::from_integer(k.into());
        sum += &term;
    }
    // Taylor remainder <= e^|x| * |x|^81/81!. Use e < 3.
    let factor = Q::from_integer(BigInt::from(3).pow(x.abs().ceil().to_integer().to_u32()?));
    let remainder = term.abs() * x.abs() / Q::from_integer(81.into()) * factor;
    Some((&sum - &remainder, sum + remainder))
}
fn function_interval(name: &str, l: &Q, h: &Q) -> Option<(Q, Q)> {
    match name {
        "ln" => Some((log_bounds(l)?.0, log_bounds(h)?.1)),
        "exp" => Some((exp_bounds(l)?.0, exp_bounds(h)?.1)),
        "sin" | "cos" => {
            let mid = (l + h) / Q::from_integer(2.into());
            let radius = (h - l) / Q::from_integer(2.into());
            let (a, b) = trig_bounds(name, &mid)?;
            Some((a - radius.clone(), b + radius))
        }
        "abs" => {
            let min = if l <= &Q::zero() && h >= &Q::zero() {
                Q::zero()
            } else {
                l.abs().min(h.abs())
            };
            Some((min, l.abs().max(h.abs())))
        }
        _ => None,
    }
}
fn interval_mul(a: &(Q, Q), b: &(Q, Q)) -> (Q, Q) {
    let products = [&a.0 * &b.0, &a.0 * &b.1, &a.1 * &b.0, &a.1 * &b.1];
    (
        products.iter().min().unwrap().clone(),
        products.iter().max().unwrap().clone(),
    )
}
impl Value {
    fn number(q: Q) -> Self {
        Self {
            num: Poly::number(q),
            den: Poly::integer(1),
        }
    }
    fn integer(n: i64) -> Self {
        Self::number(Q::from_integer(n.into()))
    }
    fn atom(a: Atom) -> Self {
        Self {
            num: Poly::atom(a),
            den: Poly::integer(1),
        }
    }
    fn constant(&self) -> Option<Q> {
        Some(self.num.constant()? / self.den.constant()?)
    }
    fn is_zero(&self) -> bool {
        self.num.is_zero()
    }
    fn neg(&self) -> Self {
        Self {
            num: self.num.scale(&Q::from_integer((-1).into())),
            den: self.den.clone(),
        }
    }
    fn interval_at(&self, sample: Option<i64>) -> Option<(Q, Q)> {
        let a = self.num.interval_at(sample)?;
        let (l, h) = self.den.interval_at(sample)?;
        if l <= Q::zero() && h >= Q::zero() {
            return None;
        }
        Some(interval_mul(&a, &(h.recip(), l.recip())))
    }
}

struct Algebra {
    work: usize,
    depth: usize,
    conditions: BTreeSet<Condition>,
    context: Context,
}
impl Algebra {
    fn spend(&mut self, n: usize) -> Result<()> {
        self.work = self.work.saturating_add(n);
        if self.work > MAX_WORK {
            return Err("symbolic comparison exceeds its work limit".into());
        }
        Ok(())
    }
    fn check(&mut self, p: Poly) -> Result<Poly> {
        self.spend(p.0.len() + 1)?;
        if p.0.len() > MAX_TERMS
            || !p.bounded_structure()
            || p.0.iter().any(|(m, c)| {
                m.values().map(|v| usize::from(*v)).sum::<usize>() > 256
                    || c.numer().bits().max(c.denom().bits()) > MAX_BITS
            })
        {
            return Err("symbolic expression exceeds its size limit".into());
        }
        Ok(p)
    }
    fn padd(&mut self, a: &Poly, b: &Poly) -> Result<Poly> {
        self.spend(a.0.len() + b.0.len())?;
        let mut out = a.0.clone();
        for (m, c) in &b.0 {
            let v = out.entry(m.clone()).or_insert_with(Q::zero);
            *v += c;
            if v.is_zero() {
                out.remove(m);
            }
        }
        self.check(Poly(out))
    }
    fn relation(&mut self, a: &Atom) -> Result<Option<(u16, Poly)>> {
        Ok(match a {
            Atom::I => Some((2, Poly::integer(-1))),
            Atom::Root(n, p) => Some((u16::from(*n), *p.clone())),
            Atom::Function(n, x) if n == "cos" => {
                let sin = Poly::atom(Atom::Function("sin".into(), x.clone()));
                let sin2 = self.pmul(&sin, &sin)?.scale(&Q::from_integer((-1).into()));
                Some((2, self.padd(&Poly::integer(1), &sin2)?))
            }
            Atom::Function(n, x) if n == "abs" && x.den == Poly::integer(1) => {
                Some((2, self.pmul(&x.num, &x.num)?))
            }
            _ => None,
        })
    }
    fn reduce_term(&mut self, m: Mono, c: Q) -> Result<Poly> {
        self.spend(1)?;
        if self.depth >= 64 {
            return Err("symbolic expansion exceeds its depth limit".into());
        }
        for (a, e) in &m {
            let degree = match a {
                Atom::I => 2,
                Atom::Root(n, _) => u16::from(*n),
                Atom::Function(n, _) if n == "cos" || n == "abs" => 2,
                _ => continue,
            };
            if *e < degree {
                continue;
            }
            let Some((degree, p)) = self.relation(a)? else {
                continue;
            };
            let mut rest = m.clone();
            if *e == degree {
                rest.remove(a);
            } else {
                rest.insert(a.clone(), e - degree);
            }
            self.depth += 1;
            let result = self.pmul(&Poly(BTreeMap::from([(rest, c)])), &p);
            self.depth -= 1;
            return result;
        }
        self.check(
            Poly::number(c.clone())
                .0
                .into_iter()
                .map(|(_, v)| (m.clone(), v))
                .collect::<BTreeMap<_, _>>()
                .into(),
        )
    }
    fn pmul(&mut self, a: &Poly, b: &Poly) -> Result<Poly> {
        self.spend(a.0.len().saturating_mul(b.0.len()))?;
        let mut out = Poly::integer(0);
        for (ma, ca) in &a.0 {
            for (mb, cb) in &b.0 {
                let mut m = ma.clone();
                for (atom, e) in mb {
                    let v = m.entry(atom.clone()).or_insert(0);
                    *v = v.checked_add(*e).ok_or("symbolic power exceeds limit")?;
                }
                let term = self.reduce_term(m, ca * cb)?;
                out = self.padd(&out, &term)?;
            }
        }
        Ok(out)
    }
    fn ppow(&mut self, p: &Poly, n: u32) -> Result<Poly> {
        if n > MAX_POWER {
            return Err("symbolic power exceeds 64".into());
        }
        let mut out = Poly::integer(1);
        for _ in 0..n {
            out = self.pmul(&out, p)?;
        }
        Ok(out)
    }
    fn value(&mut self, num: Poly, den: Poly) -> Result<Value> {
        if den.is_zero() {
            return Err("division by zero".into());
        }
        let mut num = self.check(num)?;
        let mut den = self.check(den)?;
        if num.is_zero() {
            return Ok(Value::integer(0));
        }
        if num == den {
            return Ok(Value::integer(1));
        }
        // Remove a shared monomial; domain obligations were recorded earlier.
        let mut common = num.0.first_key_value().unwrap().0.clone();
        for m in num.0.keys().chain(den.0.keys()) {
            common.retain(|a, e| {
                *e = (*e).min(*m.get(a).unwrap_or(&0));
                *e > 0
            });
        }
        if !common.is_empty() {
            let strip = |p: Poly| {
                Poly(
                    p.0.into_iter()
                        .map(|(mut m, c)| {
                            for (a, e) in &common {
                                let v = m.get_mut(a).unwrap();
                                *v -= e;
                                if *v == 0 {
                                    m.remove(a);
                                }
                            }
                            (m, c)
                        })
                        .collect(),
                )
            };
            num = strip(num);
            den = strip(den);
        }
        let factor = den.0.first_key_value().unwrap().1.recip();
        Ok(Value {
            num: self.check(num.scale(&factor))?,
            den: self.check(den.scale(&factor))?,
        })
    }
    fn add(&mut self, a: &Value, b: &Value) -> Result<Value> {
        let l = self.pmul(&a.num, &b.den)?;
        let r = self.pmul(&b.num, &a.den)?;
        let num = self.padd(&l, &r)?;
        let den = self.pmul(&a.den, &b.den)?;
        self.value(num, den)
    }
    fn mul(&mut self, a: &Value, b: &Value) -> Result<Value> {
        let num = self.pmul(&a.num, &b.num)?;
        let den = self.pmul(&a.den, &b.den)?;
        self.value(num, den)
    }
    fn nonzero(&mut self, p: &Poly) -> Result<()> {
        if p.is_zero() {
            return Err("division by zero".into());
        }
        if p.constant().is_some()
            || p.positive()
            || p.scale(&Q::from_integer((-1).into())).positive()
        {
            return Ok(());
        }
        if p.interval()
            .is_some_and(|(lo, hi)| lo.is_positive() || hi.is_negative())
        {
            return Ok(());
        }
        if p.0.len() == 1 {
            for a in p.0.first_key_value().unwrap().0.keys() {
                match a {
                    Atom::E | Atom::Pi | Atom::I => {}
                    Atom::Root(_, r) => self.nonzero(r)?,
                    Atom::Function(n, _) if n == "exp" => {}
                    Atom::Function(n, _) if n == "cos" => {
                        let (_, square) = self.relation(a)?.unwrap();
                        self.nonzero(&square)?;
                    }
                    Atom::Function(n, x) if n == "abs" => self.nonzero(&x.num)?,
                    _ => {
                        self.conditions
                            .insert(Condition::Nonzero(Poly::atom(a.clone()).monic()));
                    }
                }
            }
        } else {
            self.conditions.insert(Condition::Nonzero(p.monic()));
        }
        Ok(())
    }
    fn sign_condition(&mut self, v: &Value, positive: bool) -> Result<()> {
        if let Some(c) = v.constant() {
            if c.is_negative() || (positive && c.is_zero()) {
                return Err("expression is outside its real domain".into());
            }
            return Ok(());
        }
        if v.den.positive()
            && (if positive {
                v.num.positive()
            } else {
                v.num.nonnegative()
            })
        {
            return Ok(());
        }
        if v.den.positive() && v.num.scale(&Q::from_integer((-1).into())).positive() {
            return Err("expression is outside its real domain".into());
        }
        self.conditions.insert(if positive {
            Condition::Positive(v.clone())
        } else {
            Condition::Nonnegative(v.clone())
        });
        Ok(())
    }
    fn div(&mut self, a: &Value, b: &Value) -> Result<Value> {
        self.nonzero(&b.num)?;
        let num = self.pmul(&a.num, &b.den)?;
        let den = self.pmul(&a.den, &b.num)?;
        self.value(num, den)
    }
    fn integer_power(&mut self, v: &Value, n: i32) -> Result<Value> {
        if n.unsigned_abs() > MAX_POWER {
            return Err("symbolic power exceeds 64".into());
        }
        if n <= 0 {
            self.nonzero(&v.num)?;
        }
        let num = self.ppow(&v.num, n.unsigned_abs())?;
        let den = self.ppow(&v.den, n.unsigned_abs())?;
        if n < 0 {
            self.value(den, num)
        } else {
            self.value(num, den)
        }
    }
    fn root_integer(&mut self, n: BigInt, degree: u8) -> Result<Value> {
        if n.is_negative() {
            if degree % 2 == 0 {
                return Err("negative real radicand".into());
            }
            return Ok(self.root_integer(-n, degree)?.neg());
        }
        if n.is_zero() {
            return Ok(Value::integer(0));
        }
        // Trial factoring is deliberately bounded; large unfactored radicands
        // stay unsupported rather than spending unbounded CPU.
        let mut n = n.to_u64().ok_or("radicand exceeds factoring range")?;
        if n > 1_000_000_000_000 {
            return Err("radicand exceeds factoring range".into());
        }
        let mut outside = BigInt::one();
        let mut factors = vec![];
        let mut prime = 2_u64;
        while prime <= n / prime {
            self.spend(1)?;
            let mut count = 0_u32;
            while n % prime == 0 {
                n /= prime;
                count += 1;
            }
            outside *= BigInt::from(prime).pow(count / u32::from(degree));
            if count % u32::from(degree) > 0 {
                factors.push((prime, count % u32::from(degree)));
            }
            prime += if prime == 2 { 1 } else { 2 };
        }
        if n > 1 {
            factors.push((n, 1));
        }
        let mut result = Value::number(Q::from_integer(outside));
        for (prime, power) in factors {
            let atom = Value::atom(Atom::Root(
                degree,
                Box::new(Poly::number(Q::from_integer(prime.into()))),
            ));
            let factor = self.integer_power(&atom, power as i32)?;
            result = self.mul(&result, &factor)?;
        }
        Ok(result)
    }
    fn root(&mut self, v: &Value, degree: u8) -> Result<Value> {
        if !(2..=8).contains(&degree) {
            return Err("only roots of degree 2 through 8 are supported".into());
        }
        if let Some(c) = v.constant() {
            let n = self.root_integer(c.numer().clone(), degree)?;
            let d = self.root_integer(c.denom().clone(), degree)?;
            return self.div(&n, &d);
        }
        if v.den != Poly::integer(1) {
            return Err("root of a symbolic quotient is unsupported".into());
        }
        // A power of one variable can use a common root atom (x^(4/3), etc.).
        if v.num.0.len() == 1 {
            let (m, c) = v.num.0.first_key_value().unwrap();
            if m.len() == 1 && c.is_one() {
                let (atom, exponent) = m.first_key_value().unwrap();
                if matches!(atom, Atom::Variable(_)) {
                    if degree % 2 == 0 && exponent % 2 == 0 {
                        let a = Value::atom(atom.clone());
                        let abs = self.function("abs", &a)?;
                        if exponent % u16::from(degree) == 0 {
                            return self
                                .integer_power(&abs, i32::from(exponent / u16::from(degree)));
                        }
                    } else if *exponent > 1 {
                        let r = self.root(&Value::atom(atom.clone()), degree)?;
                        return self.integer_power(&r, i32::from(*exponent));
                    }
                }
            }
        }
        if degree % 2 == 0 {
            self.sign_condition(v, false)?;
        }
        Ok(Value::atom(Atom::Root(degree, Box::new(v.num.clone()))))
    }
    fn power(&mut self, a: &Value, b: &Value) -> Result<Value> {
        if let Some(c) = b.constant() {
            if c.is_integer() {
                let n = c.to_integer().to_i32().ok_or("power exceeds range")?;
                return self.integer_power(a, n);
            }
            let degree = c
                .denom()
                .to_u8()
                .ok_or("fractional power exceeds root range")?;
            let n = c.numer().to_i32().ok_or("fractional power exceeds range")?;
            let root = self.root(a, degree)?;
            return self.integer_power(&root, n);
        }
        let integer_exponent=self.context.integer_indices && b.den==Poly::integer(1)
            && b.num.0.iter().all(|(m,c)|c.is_integer()&&m.keys().all(|a|matches!(a,Atom::Variable(n) if ["n","k","j","i"].contains(&n.as_str()))));
        if !integer_exponent {
            self.sign_condition(a, true)?;
        } else {
            self.nonzero(&a.num)?;
        }
        if *a == Value::atom(Atom::E) {
            return self.function("exp", b);
        }
        Ok(Value::atom(Atom::Power(
            Box::new(a.clone()),
            Box::new(b.clone()),
        )))
    }
    fn function(&mut self, name: &str, x: &Value) -> Result<Value> {
        match name {
            "sqrt" => return self.root(x, 2),
            "cbrt" => return self.root(x, 3),
            "sec" | "csc" | "cot" | "tan" => {
                let denominator = self.function(
                    if name == "sec" || name == "tan" {
                        "cos"
                    } else {
                        "sin"
                    },
                    x,
                )?;
                let numerator = if name == "tan" {
                    self.function("sin", x)?
                } else if name == "cot" {
                    self.function("cos", x)?
                } else {
                    Value::integer(1)
                };
                return self.div(&numerator, &denominator);
            }
            "ln" => {
                self.sign_condition(x, true)?;
                if *x == Value::integer(1) {
                    return Ok(Value::integer(0));
                }
                if *x == Value::atom(Atom::E) {
                    return Ok(Value::integer(1));
                }
            }
            "exp" => {
                if let Some(c) = x.constant().filter(Q::is_integer) {
                    let n = c.to_integer().to_i32().ok_or("exponential exceeds range")?;
                    return self.integer_power(&Value::atom(Atom::E), n);
                }
                if x.den == Poly::integer(1)
                    && x.num.0.values().all(|c| {
                        c.is_integer()
                            && c.to_integer()
                                .to_i32()
                                .is_some_and(|n| n.unsigned_abs() <= 64)
                    })
                {
                    let mut result = Value::integer(1);
                    for (m, c) in &x.num.0 {
                        let base = if m.is_empty() {
                            Value::atom(Atom::E)
                        } else {
                            Value::atom(Atom::Function(
                                "exp".into(),
                                Box::new(Value {
                                    num: Poly(BTreeMap::from([(m.clone(), Q::one())])),
                                    den: Poly::integer(1),
                                }),
                            ))
                        };
                        let power = self.integer_power(&base, c.to_integer().to_i32().unwrap())?;
                        result = self.mul(&result, &power)?;
                    }
                    return Ok(result);
                }
            }
            "abs" => {
                if let Some(c) = x.constant() {
                    return Ok(Value::number(c.abs()));
                }
                if x.num.nonnegative() && x.den.positive() {
                    return Ok(x.clone());
                }
            }
            "sin" | "cos" => {
                if x.is_zero() {
                    return Ok(Value::integer(if name == "sin" { 0 } else { 1 }));
                }
                if let Some(angle) = pi_multiple(x) {
                    return self.special_trig(name, angle);
                }
            }
            _ => return Err(format!("unsupported function: {name}")),
        }
        // Odd/even symmetry; choose the argument with positive leading term.
        if matches!(name, "sin" | "cos" | "abs")
            && x.num
                .0
                .first_key_value()
                .is_some_and(|(_, c)| c.is_negative())
        {
            let y = x.neg();
            let f = self.function(name, &y)?;
            return Ok(if name == "sin" { f.neg() } else { f });
        }
        Ok(Value::atom(Atom::Function(
            name.into(),
            Box::new(x.clone()),
        )))
    }
    fn special_trig(&mut self, name: &str, mut angle: Q) -> Result<Value> {
        if name == "cos" {
            angle += Q::new(1.into(), 2.into());
        }
        let two = Q::from_integer(2.into());
        angle = angle.clone() - Q::from_integer((angle.clone() / &two).floor().to_integer()) * &two;
        let mut sign = 1;
        if angle > Q::one() {
            angle -= Q::one();
            sign = -1;
        }
        if angle > Q::new(1.into(), 2.into()) {
            angle = Q::one() - angle;
        }
        let v = if angle.is_zero() {
            Value::integer(0)
        } else if angle == Q::new(1.into(), 6.into()) {
            Value::number(Q::new(1.into(), 2.into()))
        } else if angle == Q::new(1.into(), 4.into()) || angle == Q::new(1.into(), 3.into()) {
            let n = if angle == Q::new(1.into(), 4.into()) {
                2
            } else {
                3
            };
            let r = self.root(&Value::integer(n), 2)?;
            self.div(&r, &Value::integer(2))?
        } else if angle == Q::new(1.into(), 2.into()) {
            Value::integer(1)
        } else {
            let f = Value::atom(Atom::Function(
                "sin".into(),
                Box::new(Value {
                    num: Poly::atom(Atom::Pi).scale(&angle),
                    den: Poly::integer(1),
                }),
            ));
            return Ok(if sign < 0 { f.neg() } else { f });
        };
        Ok(if sign < 0 { v.neg() } else { v })
    }
    fn eval(&mut self, ast: &Ast) -> Result<Value> {
        self.spend(1)?;
        match ast {
            Ast::Number(s) => Ok(Value::number(decimal_number(s)?)),
            Ast::Symbol(s) => Ok(Value::atom(match s.as_str() {
                "pi" => Atom::Pi,
                "e" => Atom::E,
                "i" if !self.context.symbolic_i => Atom::I,
                _ => Atom::Variable(s.clone()),
            })),
            Ast::Neg(a) => Ok(self.eval(a)?.neg()),
            Ast::Binary(op, a, b) => {
                let a = self.eval(a)?;
                let b = self.eval(b)?;
                match op {
                    '+' => self.add(&a, &b),
                    '-' => self.add(&a, &b.neg()),
                    '*' => self.mul(&a, &b),
                    '/' => self.div(&a, &b),
                    '^' => self.power(&a, &b),
                    _ => Err("unsupported operation".into()),
                }
            }
            Ast::Function(name, a) => {
                let a = self.eval(a)?;
                self.function(name, &a)
            }
            Ast::Root(n, a) => {
                let a = self.eval(a)?;
                self.root(&a, *n)
            }
        }
    }
}
impl From<BTreeMap<Mono, Q>> for Poly {
    fn from(p: BTreeMap<Mono, Q>) -> Self {
        Self(p)
    }
}
fn pi_multiple(v: &Value) -> Option<Q> {
    if v.den != Poly::integer(1) || v.num.0.len() != 1 {
        return None;
    }
    let (m, c) = v.num.0.first_key_value()?;
    (m == &BTreeMap::from([(Atom::Pi, 1)])).then(|| c.clone())
}

#[derive(Debug)]
enum Ast {
    Number(String),
    Symbol(String),
    Neg(Box<Ast>),
    Binary(char, Box<Ast>, Box<Ast>),
    Function(String, Box<Ast>),
    Root(u8, Box<Ast>),
}
#[derive(Clone, Debug, PartialEq, Eq)]
enum Token {
    Number(String),
    Word(String),
    Command(String),
    Mark(char),
}
fn lex(source: &str) -> Result<Vec<Token>> {
    if source.len() > 4096 {
        return Err("math input exceeds 4096 bytes".into());
    }
    let mut source = source.to_owned();
    for name in ["sin", "cos", "tan", "sec", "csc", "cot", "ln", "log"] {
        source = source.replace(&format!("\\operatorname{{{name}}}"), &format!(" {name} "));
        source = source.replace(&format!("\\mathrm{{{name}}}"), &format!(" {name} "));
        source = source.replace(&format!("{{{name}}}"), &format!(" {name} "));
    }
    let chars: Vec<_> = source.chars().collect();
    let mut at = 0;
    let mut tokens = vec![];
    while at < chars.len() {
        let c = chars[at];
        at += 1;
        if c.is_whitespace() || c == '$' {
            continue;
        }
        if c == '\\' {
            let start = at;
            while at < chars.len() && chars[at].is_ascii_alphabetic() {
                at += 1;
            }
            let word: String = chars[start..at].iter().collect();
            if word.is_empty() {
                if at < chars.len() && ",;! ()[]".contains(chars[at]) {
                    at += 1;
                    continue;
                }
                return Err("unsupported TeX escape".into());
            }
            match word.as_str() {
                "left" | "right" | "displaystyle" | "textstyle" => {}
                "cdot" | "times" => tokens.push(Token::Mark('*')),
                "div" => tokens.push(Token::Mark('/')),
                "dfrac" | "tfrac" => tokens.push(Token::Command("frac".into())),
                _ => tokens.push(Token::Command(word)),
            }
        } else if c.is_ascii_digit() || c == '.' {
            let start = at - 1;
            while at < chars.len() && (chars[at].is_ascii_digit() || chars[at] == '.') {
                at += 1;
            }
            if at < chars.len() && matches!(chars[at], 'e' | 'E') {
                let exp = at;
                let mut end = at + 1;
                if end < chars.len() && matches!(chars[end], '+' | '-') {
                    end += 1;
                }
                let digits = end;
                while end < chars.len() && chars[end].is_ascii_digit() {
                    end += 1;
                }
                if end > digits {
                    at = end;
                } else {
                    at = exp;
                }
            }
            let word: String = chars[start..at].iter().collect();
            if word.len() > 256 {
                return Err("numeric literal exceeds 256 bytes".into());
            }
            if let Some((_, exp)) = word.split_once(['e', 'E']) {
                if exp
                    .parse::<i32>()
                    .ok()
                    .is_none_or(|e| e.unsigned_abs() > 64)
                {
                    return Err("decimal exponent exceeds 64".into());
                }
            }
            decimal_number(&word)?;
            tokens.push(Token::Number(word));
        } else if c.is_alphabetic() {
            let start = at - 1;
            while at < chars.len() && chars[at].is_alphabetic() {
                at += 1;
            }
            let word: String = chars[start..at].iter().collect();
            if matches!(
                word.as_str(),
                "pi" | "sin"
                    | "cos"
                    | "tan"
                    | "sec"
                    | "csc"
                    | "cot"
                    | "ln"
                    | "log"
                    | "exp"
                    | "abs"
                    | "sqrt"
                    | "cbrt"
            ) {
                tokens.push(Token::Word(word));
            } else if word.chars().count() > 2 {
                tokens.push(Token::Command(word));
            } else {
                for c in word.chars() {
                    tokens.push(Token::Word(match c {
                        'π' => "pi".into(),
                        _ => c.to_string(),
                    }));
                }
            }
        } else {
            tokens.push(match c {
                '−' => Token::Mark('-'),
                '×' | '·' => Token::Mark('*'),
                '÷' => Token::Mark('/'),
                '√' => Token::Word("sqrt".into()),
                _ => Token::Mark(c),
            });
        }
        if tokens.len() > 512 {
            return Err("math input exceeds 512 tokens".into());
        }
    }
    Ok(tokens)
}
struct Parser {
    tokens: Vec<Token>,
    at: usize,
    depth: usize,
}
impl Parser {
    fn peek(&self) -> Option<&Token> {
        self.tokens.get(self.at)
    }
    fn take(&mut self) -> Result<Token> {
        let t = self.peek().cloned().ok_or("incomplete expression")?;
        self.at += 1;
        Ok(t)
    }
    fn mark(&mut self, c: char) -> bool {
        if self.peek() == Some(&Token::Mark(c)) {
            self.at += 1;
            true
        } else {
            false
        }
    }
    fn nested(&mut self, call: impl FnOnce(&mut Self) -> Result<Ast>) -> Result<Ast> {
        if self.depth >= 64 {
            return Err("math input exceeds 64 nesting levels".into());
        }
        self.depth += 1;
        let r = call(self);
        self.depth -= 1;
        r
    }
    fn sum(&mut self) -> Result<Ast> {
        let mut a = self.product()?;
        loop {
            let op = if self.mark('+') {
                '+'
            } else if self.mark('-') {
                '-'
            } else {
                break;
            };
            a = Ast::Binary(op, Box::new(a), Box::new(self.product()?));
        }
        Ok(a)
    }
    fn product(&mut self) -> Result<Ast> {
        let mut a = self.signed()?;
        loop {
            let op = if self.mark('*') {
                '*'
            } else if self.mark('/') {
                '/'
            } else if matches!(
                self.peek(),
                Some(
                    Token::Number(_) | Token::Word(_) | Token::Command(_) | Token::Mark('(' | '{')
                )
            ) {
                '*'
            } else {
                break;
            };
            a = Ast::Binary(op, Box::new(a), Box::new(self.signed()?));
        }
        Ok(a)
    }
    fn signed(&mut self) -> Result<Ast> {
        if self.mark('-') {
            return self.nested(|p| Ok(Ast::Neg(Box::new(p.signed()?))));
        }
        if self.mark('+') {
            return self.nested(Self::signed);
        }
        self.power()
    }
    fn power(&mut self) -> Result<Ast> {
        let mut a = self.atom()?;
        if self.mark('^') {
            a = Ast::Binary('^', Box::new(a), Box::new(self.nested(Self::signed)?));
        }
        if self.mark('%') {
            a = Ast::Binary('/', Box::new(a), Box::new(Ast::Number("100".into())));
        }
        Ok(a)
    }
    fn group_or_tex_atom(&mut self) -> Result<Ast> {
        // In TeX, an unbraced fraction argument is one character, not a whole
        // multi-digit numeric token: \frac38 means 3/8.
        if let Some(Token::Number(n)) = self.peek().cloned() {
            if n.len() > 1 && n.chars().all(|c| c.is_ascii_digit()) {
                self.tokens[self.at] = Token::Number(n[1..].into());
                return Ok(Ast::Number(n[..1].into()));
            }
        }
        self.nested(Self::atom)
    }
    fn function(&mut self, mut name: String) -> Result<Ast> {
        let mut base = None;
        let mut power = None;
        if self.mark('_') {
            base = Some(self.group_or_tex_atom()?);
        }
        if self.mark('^') {
            power = Some(self.group_or_tex_atom()?);
        }
        // Grouped arguments stop at their close. Ungrouped arguments consume
        // one signed power; write sin(2*x) for a product argument.
        let arg = if matches!(self.peek(), Some(Token::Mark('(' | '{'))) {
            self.nested(Self::atom)?
        } else {
            let mut arg = self.nested(Self::signed)?;
            loop {
                let variable = match self.peek() {
                    Some(Token::Number(_)) => true,
                    Some(Token::Word(n)) => n.chars().count() == 1 || n == "pi",
                    Some(Token::Command(n)) => {
                        ["pi", "theta", "alpha", "beta", "gamma", "phi", "lambda"]
                            .contains(&n.as_str())
                    }
                    _ => false,
                };
                if !variable {
                    break;
                }
                arg = Ast::Binary('*', Box::new(arg), Box::new(self.nested(Self::signed)?));
            }
            arg
        };
        if name == "log" {
            name = "ln".into();
            if base.is_none() {
                base = Some(Ast::Number("10".into()));
            }
        }
        let mut out = Ast::Function(name.clone(), Box::new(arg));
        if let Some(base) = base {
            if name != "ln" {
                return Err("only logarithms accept a base".into());
            }
            out = Ast::Binary(
                '/',
                Box::new(out),
                Box::new(Ast::Function("ln".into(), Box::new(base))),
            );
        }
        if let Some(power) = power {
            out = Ast::Binary('^', Box::new(out), Box::new(power));
        }
        Ok(out)
    }
    fn atom(&mut self) -> Result<Ast> {
        match self.take()? {
            Token::Number(n) => Ok(Ast::Number(n)),
            Token::Mark(open @ ('(' | '{')) => {
                let a = self.nested(Self::sum)?;
                if !self.mark(if open == '(' { ')' } else { '}' }) {
                    return Err("unclosed group".into());
                }
                Ok(a)
            }
            Token::Word(n) | Token::Command(n)
                if matches!(
                    n.as_str(),
                    "sin"
                        | "cos"
                        | "tan"
                        | "sec"
                        | "csc"
                        | "cot"
                        | "ln"
                        | "log"
                        | "exp"
                        | "abs"
                        | "cbrt"
                ) =>
            {
                self.function(n)
            }
            token @ (Token::Word(_) | Token::Command(_)) if matches!(&token,Token::Word(n)|Token::Command(n) if n=="sqrt") =>
            {
                let tex = matches!(token, Token::Command(_));
                let mut degree = 2;
                if self.mark('[') {
                    let Token::Number(n) = self.take()? else {
                        return Err("root degree must be an integer".into());
                    };
                    degree = n.parse().map_err(|_| "unsupported root degree")?;
                    if !self.mark(']') {
                        return Err("unclosed root degree".into());
                    }
                }
                let arg = if tex {
                    self.group_or_tex_atom()?
                } else {
                    self.nested(Self::atom)?
                };
                Ok(Ast::Root(degree, Box::new(arg)))
            }
            Token::Command(n) if n == "frac" => {
                let a = self.group_or_tex_atom()?;
                let b = self.group_or_tex_atom()?;
                Ok(Ast::Binary('/', Box::new(a), Box::new(b)))
            }
            Token::Command(n) if n == "operatorname" || n == "mathrm" => {
                if !self.mark('{') {
                    return Err("operator name needs braces".into());
                }
                let mut name = String::new();
                while !self.mark('}') {
                    match self.take()? {
                        Token::Word(w) => name.push_str(&w),
                        _ => return Err("invalid operator name".into()),
                    }
                }
                if name == "i" {
                    return Ok(Ast::Symbol(name));
                }
                self.function(name)
            }
            Token::Command(n)
                if matches!(
                    n.as_str(),
                    "pi" | "theta" | "alpha" | "beta" | "gamma" | "phi" | "lambda"
                ) =>
            {
                Ok(Ast::Symbol(
                    match n.as_str() {
                        "theta" => "θ",
                        "alpha" => "α",
                        "beta" => "β",
                        "gamma" => "γ",
                        "phi" => "φ",
                        "lambda" => "λ",
                        _ => "pi",
                    }
                    .into(),
                ))
            }
            Token::Word(n) => {
                if ["f", "g", "h"].contains(&n.as_str()) && self.peek() == Some(&Token::Mark('(')) {
                    return Err(
                        "unspecified function calls are unsupported; use * for multiplication"
                            .into(),
                    );
                }
                Ok(Ast::Symbol(n))
            }
            Token::Mark('|') => {
                let a = self.nested(Self::sum)?;
                if !self.mark('|') {
                    return Err("unclosed absolute value".into());
                }
                Ok(Ast::Function("abs".into(), Box::new(a)))
            }
            _ => Err("unsupported mathematical notation".into()),
        }
    }
}

fn special(source: &str) -> Option<String> {
    let s = source
        .trim()
        .trim_matches('$')
        .replace("\\left", "")
        .replace("\\right", "")
        .replace("\\text", "")
        .replace("\\mathrm", "")
        .replace(['{', '}'], "")
        .split_whitespace()
        .collect::<String>()
        .to_lowercase()
        .replace('−', "-");
    Some(
        match s.as_str() {
            "dne" | "doesnotexist" => "DNE",
            "∞" | "+∞" | "\\infty" | "+\\infty" | "infinity" | "+infinity" => "infinity",
            "-∞" | "-\\infty" | "-infinity" => "-infinity",
            "<" => "<",
            ">" => ">",
            "≤" | "<=" | "\\le" | "\\leq" => "<=",
            "≥" | ">=" | "\\ge" | "\\geq" => ">=",
            "=" => "=",
            "≠" | "!=" | "\\ne" | "\\neq" => "!=",
            _ => return None,
        }
        .into(),
    )
}
fn parse(source: &str, context: Context) -> Result<Answer> {
    if source.len() > 4096 || source.trim().is_empty() {
        return Err("empty or oversized mathematical answer".into());
    }
    if let Some(s) = special(source) {
        return Ok(Answer::Special(s));
    }
    let mut parser = Parser {
        tokens: lex(source)?,
        at: 0,
        depth: 0,
    };
    let ast = parser.sum()?;
    if parser.at != parser.tokens.len() {
        return Err("unconsumed mathematical notation".into());
    }
    let mut algebra = Algebra {
        work: 0,
        depth: 0,
        conditions: BTreeSet::new(),
        context,
    };
    let value = algebra.eval(&ast)?;
    algebra.check(value.num.clone())?;
    algebra.check(value.den.clone())?;
    // Positive implies both nonnegative and nonzero; canonicalize this common
    // intersection so equivalent root/log spellings compare consistently.
    let mut conditions = algebra.conditions;
    let nonnegative: Vec<_> = conditions
        .iter()
        .filter_map(|c| {
            if let Condition::Nonnegative(v) = c {
                Some(v.clone())
            } else {
                None
            }
        })
        .collect();
    for v in nonnegative {
        if conditions.contains(&Condition::Nonzero(v.num.monic())) {
            conditions.remove(&Condition::Nonnegative(v.clone()));
            conditions.remove(&Condition::Nonzero(v.num.monic()));
            conditions.insert(Condition::Positive(v));
        }
    }
    let positive: Vec<_> = conditions
        .iter()
        .filter_map(|c| {
            if let Condition::Positive(v) = c {
                Some(v.clone())
            } else {
                None
            }
        })
        .collect();
    for v in positive {
        conditions.remove(&Condition::Nonnegative(v.clone()));
        conditions.remove(&Condition::Nonzero(v.num.monic()));
    }
    Ok(Answer::Expression(value, conditions))
}

/// Whether a canonical answer has a bounded, supported representation.
pub fn supports(source: &str, context: Context) -> bool {
    parse(source, context).is_ok()
}

/// True is proved by exact normal forms. A nonzero rational polynomial proves
/// false. Unresolved transcendental identities or differing domains return an
/// error so the caller cannot turn a limitation into a learner failure.
pub fn compare(a: &str, b: &str, context: Context) -> Result<bool> {
    let a = parse(a, context)?;
    let b = parse(b, context)?;
    match (a, b) {
        (Answer::Special(a), Answer::Special(b)) => Ok(a == b),
        (Answer::Special(_), Answer::Expression(..))
        | (Answer::Expression(..), Answer::Special(_)) => Ok(false),
        (Answer::Expression(a, ca), Answer::Expression(b, cb)) => {
            if ca != cb {
                return Err("answer comparison has unresolved domain differences".into());
            }
            let mut algebra = Algebra {
                work: 0,
                depth: 0,
                conditions: BTreeSet::new(),
                context,
            };
            let l = algebra.pmul(&a.num, &b.den)?;
            let r = algebra.pmul(&b.num, &a.den)?;
            let diff = algebra.padd(&l, &r.scale(&Q::from_integer((-1).into())))?;
            if diff.is_zero() {
                return Ok(true);
            }
            if diff.rational_variables_only() {
                return Ok(false);
            }
            if diff
                .interval()
                .is_some_and(|(lo, hi)| lo.is_positive() || hi.is_negative())
            {
                return Ok(false);
            }
            for sample in [-4, -2, 0, 1, 3] {
                if !ca.iter().all(|c| condition_at(c, sample)) {
                    continue;
                }
                if diff
                    .interval_at(Some(sample))
                    .is_some_and(|(lo, hi)| lo.is_positive() || hi.is_negative())
                {
                    return Ok(false);
                }
            }
            Err("symbolic equivalence is not established by the supported rules".into())
        }
    }
}
fn condition_at(c: &Condition, sample: i64) -> bool {
    match c {
        Condition::Nonzero(p) => p
            .interval_at(Some(sample))
            .is_some_and(|(l, h)| l.is_positive() || h.is_negative()),
        Condition::Nonnegative(v) => v
            .interval_at(Some(sample))
            .is_some_and(|(l, _)| !l.is_negative()),
        Condition::Positive(v) => v
            .interval_at(Some(sample))
            .is_some_and(|(l, _)| l.is_positive()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn eq(a: &str, b: &str) {
        assert_eq!(compare(a, b, Context::default()), Ok(true), "{a} != {b}");
    }
    #[test]
    fn exact_polynomial_and_rational_equivalence() {
        for (a, b) in [
            ("x+x", "2x"),
            ("7b", "b*7"),
            ("400a+20b", "20(20a+b)"),
            ("x^2-5x-50", "(x-10)(x+5)"),
            ("k(3-k)", "3k-k^2"),
            ("-11/x", "-11x^{-1}"),
            ("2/(x^2+1)^2", "2/(x^4+2x^2+1)"),
            ("-x^2", "-(x*x)"),
            ("1/3+1/6", "1/2"),
            ("\\frac38", "0.375"),
            ("\\frac1{3}", "1/3"),
            ("1e-3", ".001"),
            ("25%", "1/4"),
        ] {
            eq(a, b);
        }
        for (a, b) in [
            ("7b", "8b"),
            ("9007199254740992", "9007199254740993"),
            ("0.00000000000000001x", "0"),
            ("-x^2", "x^2"),
        ] {
            assert_eq!(compare(a, b, Context::default()), Ok(false));
        }
    }
    #[test]
    fn roots_and_functions() {
        for (a, b) in [
            ("2\\sqrt{10}", "\\sqrt{40}"),
            ("1/\\sqrt{3}", "\\sqrt{3}/3"),
            ("(sqrt(6)-sqrt(2))/4", "1/(sqrt(6)+sqrt(2))"),
            ("3sqrt(3)/(sqrt(3)-1)", "(9+3sqrt(3))/2"),
            ("sin(x)^2+cos(x)^2", "1"),
            ("csc(x)", "1/sin(x)"),
            ("sin(-x)", "-sin(x)"),
            ("cos(-x)", "cos(x)"),
            ("\\sin(\\pi/6)", "1/2"),
            ("cos(pi/3)", "1/2"),
            ("8i", "4i+4i"),
            ("i^2", "-1"),
            ("\\operatorname{ln}4", "ln(4)"),
            ("e^x", "exp(x)"),
        ] {
            eq(a, b);
        }
    }
    #[test]
    fn domains_limits_and_unknown_identities_are_explicit() {
        for (a, b) in [("x/x", "1"), ("sqrt(x)^2", "x"), ("ln(x)", "ln(x+1)")] {
            assert!(compare(a, b, Context::default()).is_err());
        }
        for a in [
            "0*(1/0)",
            "ln(-1)",
            "sqrt(-1)",
            "2^9999999",
            "1e9999999",
            "foo(x)",
            "ln(-x^2-1)",
            "sqrt(-x^2-1)",
            "(x+y+z)^64",
        ] {
            assert!(!supports(a, Context::default()), "{a}");
        }
        eq("\\infty", "∞");
        eq("\\le", "<=");
        eq("DNE", "\\text{DNE}");
        assert_eq!(compare("∞", "-∞", Context::default()), Ok(false));
        assert_eq!(
            compare(
                "i^2",
                "-1",
                Context {
                    symbolic_i: true,
                    ..Context::default()
                }
            ),
            Ok(false)
        );
        assert!(!supports(&"(".repeat(1000), Context::default()));
        let mut nested = "x".to_owned();
        for _ in 0..20 {
            nested = format!("ln(({nested}+1)^7)");
        }
        assert!(!supports(&nested, Context::default()));
    }
    #[test]
    fn captured_answers_and_independent_correctness_cases() {
        let fixtures: serde_json::Value = serde_json::from_str(include_str!(
            "../../reference/symbolic-grader-2026-10-05/cases.json"
        ))
        .unwrap();
        for case in fixtures["cases"].as_array().unwrap() {
            let context = Context {
                symbolic_i: case["symbolic_i"].as_bool().unwrap_or(false),
                integer_indices: case["integer_indices"].as_bool().unwrap_or(false),
            };
            let actual = compare(
                case["canonical"].as_str().unwrap(),
                case["submitted"].as_str().unwrap(),
                context,
            );
            match case["expected"].as_str().unwrap() {
                "equivalent" => assert_eq!(actual, Ok(true), "{case}"),
                "different" => assert_eq!(actual, Ok(false), "{case}"),
                "unsupported" => assert!(actual.is_err(), "{case}: {actual:?}"),
                _ => panic!("invalid expected result"),
            }
        }
    }
}
