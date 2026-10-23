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
    fn interval_at(&self, sample: Option<&Q>) -> Option<(Q, Q)> {
        if self.0.len() > 16
            || self.0.iter().any(|(m, c)| {
                m.values().map(|e| u32::from(*e)).sum::<u32>() > 4 * MAX_POWER
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
                    Atom::E => exp_bounds(&Q::one())?,
                    Atom::I => return None,
                    Atom::Variable(name) => {
                        let n = sample?;
                        // Distinct values prevent x-y from vanishing at every
                        // witness. These are exact substitutions, not floats.
                        let offset = name.bytes().map(u64::from).sum::<u64>() % 7;
                        let v = n + Q::from_integer(offset.into());
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
// Outward dyadic rounding bounds intermediate exact Taylor fractions while
// retaining about 64 significant bits across large and small magnitudes.
fn bounded_endpoints(v: &Q) -> Option<(Q, Q)> {
    if v.numer().bits().max(v.denom().bits()) > MAX_BITS {
        return None;
    }
    let magnitude_bits = v.abs().ceil().to_integer().bits() as i32;
    let shift = (64 - magnitude_bits).clamp(-256, 64);
    let scale = if shift >= 0 {
        Q::from_integer(BigInt::one() << shift as usize)
    } else {
        Q::new(BigInt::one(), BigInt::one() << (-shift) as usize)
    };
    let scaled = v * &scale;
    Some((Q::from_integer(scaled.floor().to_integer()) / &scale,
          Q::from_integer(scaled.ceil().to_integer()) / &scale))
}
fn root_bounds(v: &Q, n: u8) -> Option<(Q, Q)> {
    if v.numer().bits().max(v.denom().bits()) > 128 {
        if v.numer().bits().max(v.denom().bits()) > MAX_BITS {
            return None;
        }
        let (lower, upper) = bounded_endpoints(v)?;
        if lower.numer().bits().max(upper.numer().bits()) > 128 {
            return None;
        }
        return Some((root_bounds(&lower, n)?.0, root_bounds(&upper, n)?.1));
    }
    if v.is_negative() {
        if n % 2 == 0 {
            return None;
        }
        let (l, h) = root_bounds(&-v, n)?;
        return Some((-h, -l));
    }
    let mut l = Q::zero();
    // Start within a power of two of the root, rather than the radicand.
    // A fixed bisection budget must also resolve large exponential radicands.
    let bits = v.numer().bits().saturating_sub(v.denom().bits()) + 1;
    let exponent = bits.div_ceil(u64::from(n)) + 1;
    let mut h = Q::from_integer(BigInt::one() << exponent as usize);
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
    if !x.is_positive() || x.numer().bits().max(x.denom().bits()) > MAX_BITS {
        return None;
    }
    if x.numer().bits().max(x.denom().bits()) > 128 {
        // Composed interval functions (notably ln(c-exp(u))) receive exact
        // Taylor endpoints with large denominators. Round OUTWARDS before
        // applying the bounded log series. Monotonicity preserves the proof;
        // these witnesses can only reject unequal answers, never accept one.
        let (lower, upper) = bounded_endpoints(x)?;
        if !lower.is_positive() || upper.numer().bits() > 128 {
            return None;
        }
        return Some((log_bounds(&lower)?.0, log_bounds(&upper)?.1));
    }
    // ln(x) = ln(reduced) + exponent*ln(2). Exact power-of-two reduction
    // keeps the atanh series rapidly convergent for every supported positive
    // rational, including large arguments and their reciprocals.
    let two = Q::from_integer(2.into());
    let mut reduced = x.clone();
    let mut exponent = 0i32;
    while reduced > two {
        reduced /= &two;
        exponent += 1;
    }
    while reduced < Q::one() {
        reduced *= &two;
        exponent -= 1;
    }
    let (lo, hi) = reduced_log_bounds(&reduced);
    if exponent == 0 {
        return Some((lo, hi));
    }
    static LOG_TWO: std::sync::OnceLock<(Q, Q)> = std::sync::OnceLock::new();
    let (two_lo, two_hi) = LOG_TWO.get_or_init(|| reduced_log_bounds(&Q::from_integer(2.into())));
    let scale = Q::from_integer(exponent.into());
    let (shift_lo, shift_hi) = if exponent > 0 {
        (two_lo * &scale, two_hi * &scale)
    } else {
        (two_hi * &scale, two_lo * &scale)
    };
    Some((lo + shift_lo, hi + shift_hi))
}
fn reduced_log_bounds(x: &Q) -> (Q, Q) {
    debug_assert!(*x >= Q::one() && *x <= Q::from_integer(2.into()));
    let t = (x - Q::one()) / (x + Q::one());
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
    (&sum - &remainder, sum + remainder)
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
    if x.abs() > Q::from_integer(128.into()) || x.numer().bits().max(x.denom().bits()) > 128 {
        return None;
    }
    if x.is_negative() {
        let (lo, hi) = exp_bounds(&-x)?;
        return Some((hi.recip(), lo.recip()));
    }
    if x > &Q::one() {
        // exp(x)=exp(x/2)^2. Round each positive interval outwards
        // so composition remains bounded without an arbitrary small-x cutoff.
        let (lo, hi) = exp_bounds(&(x / Q::from_integer(2.into())))?;
        return Some((bounded_endpoints(&(&lo * &lo))?.0,
                     bounded_endpoints(&(&hi * &hi))?.1));
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
    Some((bounded_endpoints(&(&sum - &remainder))?.0,
          bounded_endpoints(&(sum + remainder))?.1))
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
    fn interval_at(&self, sample: Option<&Q>) -> Option<(Q, Q)> {
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
    nonzero_power_bases: BTreeMap<Poly, Poly>,
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
    fn reduce_term(&mut self, mut m: Mono, c: Q) -> Result<Poly> {
        self.spend(1)?;
        if self.depth >= 64 {
            return Err("symbolic expansion exceeds its depth limit".into());
        }
        // Products of positive real roots of e add their rational exponents.
        // This also keeps split exp constants consistent with a single exp(q).
        // Stay within the existing root-degree bound and leave other radicands
        // alone: combining arbitrary real roots would need sign conditions.
        let e_roots: Vec<_> = m.iter().filter_map(|(a, n)| match a {
            Atom::Root(d, p) if **p == Poly::atom(Atom::E) => Some((a.clone(), *d, *n)),
            _ => None,
        }).collect();
        if e_roots.len() > 1 {
            let exponent = e_roots.iter().fold(Q::zero(), |q, (_, d, n)| {
                q + Q::new((*n).into(), (*d).into())
            });
            if let Some(degree) = exponent.denom().to_u8().filter(|d| *d <= 8) {
                for (a, _, _) in e_roots { m.remove(&a); }
                let whole = exponent.to_integer().to_u16().ok_or("symbolic power exceeds limit")?;
                if whole > 0 {
                    let n = m.entry(Atom::E).or_insert(0);
                    *n = n.checked_add(whole).ok_or("symbolic power exceeds limit")?;
                }
                let remainder = (exponent.numer() % exponent.denom()).to_u16().unwrap();
                if remainder > 0 {
                    m.insert(Atom::Root(degree, Box::new(Poly::atom(Atom::E))), remainder);
                }
            }
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
        // p^n != 0 iff p != 0. Keep the exact construction available after
        // expansion when it reduces the polynomial degree of a domain guard.
        let degree = |p: &Poly| {
            p.0.keys()
                .map(|m| m.values().map(|e| usize::from(*e)).sum::<usize>())
                .max()
                .unwrap_or(0)
        };
        if n > 1 && degree(&out) > degree(p) {
            self.nonzero_power_bases.insert(out.monic(), p.monic());
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
        self.spend(p.0.len() + 1)?;
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
        let power_key = p.monic();
        if let Some(base) = self.nonzero_power_bases.remove(&power_key) {
            // A root's own relation can lead back to this polynomial. Hide
            // this hint while resolving it, so that path retains the direct
            // polynomial guard instead of following a provenance cycle.
            let result = self.nonzero(&base);
            self.nonzero_power_bases.insert(power_key, base);
            return result;
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
            // Expansion can turn u*sqrt(u) into several terms. Its nonzero
            // condition still requires both factors, just as sqrt(u)^(-3)
            // requires u != 0. Retain the residual factor's guard as well.
            let mut common = p.0.first_key_value().unwrap().0.clone();
            for m in p.0.keys() {
                common.retain(|a, e| {
                    *e = (*e).min(*m.get(a).unwrap_or(&0));
                    *e > 0
                });
            }
            if !common.is_empty() {
                self.nonzero(&Poly(BTreeMap::from([(common.clone(), Q::one())])))?;
                let rest = Poly(p.0.iter().map(|(m, c)| {
                    let mut m = m.clone();
                    for (a, e) in &common {
                        let remaining = m[a] - e;
                        if remaining == 0 {
                            m.remove(a);
                        } else {
                            m.insert(a.clone(), remaining);
                        }
                    }
                    (m, c.clone())
                }).collect());
                return self.nonzero(&rest);
            }
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
            // For positive d, principal real roots satisfy root(n/d) =
            // root(n)/root(d), including when d contains exponential atoms.
            // Odd roots permit either sign. Keep the original nonzero/domain
            // obligations; do not split even roots over an unknown-sign d.
            if degree % 2 == 0 && !v.den.positive() {
                return Err("even root quotient needs a provably positive denominator".into());
            }
            let numerator = self.root(&Value { num: v.num.clone(), den: Poly::integer(1) }, degree)?;
            let denominator = self.root(&Value { num: v.den.clone(), den: Poly::integer(1) }, degree)?;
            return self.div(&numerator, &denominator);
        }
        // Give positive rational multiples the same root atom and domain
        // guard: root(c*p) = root(c)*root(p) for c > 0. Use the magnitude
        // of the leading coefficient so a negative sign stays INSIDE an
        // even root. Bound the new factoring work; larger coefficients keep
        // their existing opaque-root representation.
        let coefficient = v.num.0.first_key_value().unwrap().1.abs();
        if !coefficient.is_one()
            && coefficient.numer() <= &BigInt::from(1_000_000)
            && coefficient.denom() <= &BigInt::from(1_000_000)
        {
            let outside = self.root(&Value::number(coefficient.clone()), degree)?;
            let normalized = self.value(v.num.scale(&coefficient.recip()), Poly::integer(1))?;
            let inside = self.root(&normalized, degree)?;
            return self.mul(&outside, &inside);
        }
        // A power of one variable can use a common root atom (x^(4/3), etc.).
        if v.num.0.len() == 1 {
            let (m, c) = v.num.0.first_key_value().unwrap();
            if m.len() == 1 && c.is_one() {
                let (atom, exponent) = m.first_key_value().unwrap();
                // Positive constants have no even-root sign ambiguity. Reduce
                // the exponent fraction so sqrt(e^3) and e^(3/2), including
                // reducible forms such as fourth_root(e^2), share root atoms.
                if matches!(atom, Atom::E | Atom::Pi) && *exponent > 1 {
                    return self.power(
                        &Value::atom(atom.clone()),
                        &Value::number(Q::new((*exponent).into(), degree.into())),
                    );
                }
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
                // Positive rational constants have an exact logarithm sum.
                // Bound trial division; any remaining factor stays opaque.
                // This never expands ln(x*y) for symbolic, possibly negative
                // factors, whose real domains would need additional guards.
                if let Some(c) = x.constant()
                    && let (Some(n), Some(d)) = (c.numer().to_u64(), c.denom().to_u64())
                    && n <= 1_000_000_000_000 && d <= 1_000_000_000_000
                {
                    let mut factors = BTreeMap::<u64, i32>::new();
                    for (mut remaining, sign) in [(n, 1), (d, -1)] {
                        let mut prime = 2;
                        while prime <= remaining / prime && prime <= 10_000 {
                            self.spend(1)?;
                            while remaining % prime == 0 {
                                *factors.entry(prime).or_default() += sign;
                                remaining /= prime;
                            }
                            prime += if prime == 2 { 1 } else { 2 };
                        }
                        if remaining > 1 {
                            *factors.entry(remaining).or_default() += sign;
                        }
                    }
                    let mut sum = Value::integer(0);
                    for (factor, exponent) in factors {
                        let atom = Value::atom(Atom::Function("ln".into(),
                            Box::new(Value::number(Q::from_integer(factor.into())))));
                        let term = self.mul(&Value::integer(exponent.into()), &atom)?;
                        sum = self.add(&sum, &term)?;
                    }
                    return Ok(sum);
                }
            }
            "exp" => {
                // exp(-u) is the reciprocal of exp(u) for every supported real
                // argument, including rational coefficients. Orient by the
                // leading term so opaque exponential atoms share this identity.
                // Conditions introduced while evaluating u remain in force.
                if x.num.0.first_key_value().is_some_and(|(_, c)| c.is_negative()) {
                    let positive = self.function("exp", &x.neg())?;
                    return self.div(&Value::integer(1), &positive);
                }
                if let Some(c) = x.constant()
                    && (c.is_integer() || c.denom() <= &BigInt::from(8))
                {
                    // exp(q) and e^q denote the same positive real number.
                    // Share the exact rational-power representation, including
                    // root atoms, instead of retaining an opaque exp(q) atom.
                    // Larger root degrees keep the existing opaque exp form.
                    return self.power(&Value::atom(Atom::E), &Value::number(c));
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
    fn eval_root(&mut self, degree: u8, ast: &Ast) -> Result<Value> {
        if !(2..=8).contains(&degree) {
            return Err("only roots of degree 2 through 8 are supported".into());
        }
        if let Ast::Binary('^', base, exponent) = ast {
            let base = self.eval(base)?;
            let exponent = self.eval(exponent)?;
            if let Some(n) = exponent.constant().filter(Q::is_integer)
                .and_then(|c| c.to_integer().to_i32())
                .filter(|n| *n > 1 && n % 2 == 1 && *n <= MAX_POWER as i32)
            {
                // For odd n, root(u^n) = root(u)^n on the same real domain.
                // Apply before expanding u^n, so both the root atom and its
                // domain obligations retain the compound base u.
                return self.power(&base, &Value::number(Q::new(n.into(), degree.into())));
            }
            let powered = self.power(&base, &exponent)?;
            return self.root(&powered, degree);
        }
        let value = self.eval(ast)?;
        self.root(&value, degree)
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
                if name == "sqrt" || name == "cbrt" {
                    return self.eval_root(if name == "sqrt" { 2 } else { 3 }, a);
                }
                let a = self.eval(a)?;
                self.function(name, &a)
            }
            Ast::Root(n, a) => self.eval_root(*n, a),
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
        let mut a = self.implicit_product()?;
        loop {
            let op = if self.mark('*') {
                '*'
            } else if self.mark('/') {
                '/'
            } else {
                break;
            };
            a = Ast::Binary(op, Box::new(a), Box::new(self.implicit_product()?));
        }
        Ok(a)
    }
    fn implicit_product(&mut self) -> Result<Ast> {
        // Typed algebra treats an adjacent product as one slash denominator:
        // 11/4x means 11/(4x). Explicit multiplication remains left associative;
        // (11/4)x and 11/4*x still mean (11/4)*x. TeX fractions keep their groups.
        let mut a = self.signed()?;
        while matches!(self.peek(), Some(Token::Number(_) | Token::Word(_) |
            Token::Command(_) | Token::Mark('(' | '{'))) {
            a = Ast::Binary('*', Box::new(a), Box::new(self.signed()?));
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
        nonzero_power_bases: BTreeMap::new(),
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

/// Compare the expression before an explicitly displayed arbitrary +C.
/// An exact, variable-free real difference is absorbed by that constant.
/// Domain restrictions must still match; this does not prove identities by
/// numerical sampling or turn ordinary expression equality into family equality.
pub fn compare_up_to_constant(a: &str, b: &str, context: Context) -> Result<bool> {
    fn constant_poly(p: &Poly) -> bool {
        p.0.keys().all(|mono| mono.keys().all(|atom| match atom {
            Atom::Pi | Atom::E => true,
            Atom::Root(_, p) => constant_poly(p),
            Atom::Function(_, v) => constant_value(v),
            Atom::Power(base, exponent) => constant_value(base) && constant_value(exponent),
            Atom::Variable(_) | Atom::I => false,
        }))
    }
    fn constant_value(v: &Value) -> bool {
        constant_poly(&v.num) && constant_poly(&v.den)
    }
    if let (Answer::Expression(av, ac), Answer::Expression(bv, bc)) =
        (parse(a, context)?, parse(b, context)?)
    {
        let mut algebra = Algebra {
            work: 0, depth: 0, conditions: BTreeSet::new(),
            nonzero_power_bases: BTreeMap::new(), context,
        };
        let difference = algebra.add(&av, &bv.neg())?;
        if constant_value(&difference) {
            if ac != bc {
                return Err("antiderivative comparison has unresolved domain differences".into());
            }
            return Ok(true);
        }
        // Literal inequality is insufficient here: a nonzero constant is a
        // valid family difference. Two disjoint exact interval evaluations
        // instead prove that the difference actually varies. As with ordinary
        // comparison, samples can reject; they can never establish acceptance.
        let mut intervals: Vec<(Q, Q)> = vec![];
        for sample in counterexample_samples() {
            if !ac.iter().chain(bc.iter()).all(|c| condition_at(c, &sample)) {
                continue;
            }
            if let Some((lo, hi)) = difference.interval_at(Some(&sample)) {
                if intervals.iter().any(|(a, b)| hi < *a || lo > *b) {
                    return Ok(false);
                }
                intervals.push((lo, hi));
            }
        }
        return Err("constant antiderivative difference is not established by the supported rules".into());
    }
    compare(a, b, context)
}

/// True is proved by exact normal forms. A nonzero rational polynomial proves
/// false. A counterexample must be valid in both domains. Unresolved identities
/// or domain equivalence return an error rather than a learner failure.
pub fn compare(a: &str, b: &str, context: Context) -> Result<bool> {
    let a = parse(a, context)?;
    let b = parse(b, context)?;
    match (a, b) {
        (Answer::Special(a), Answer::Special(b)) => Ok(a == b),
        (Answer::Special(_), Answer::Expression(..))
        | (Answer::Expression(..), Answer::Special(_)) => Ok(false),
        (Answer::Expression(a, ca), Answer::Expression(b, cb)) => {
            let mut algebra = Algebra {
                work: 0,
                depth: 0,
                conditions: BTreeSet::new(),
                nonzero_power_bases: BTreeMap::new(),
                context,
            };
            let l = algebra.pmul(&a.num, &b.den)?;
            let r = algebra.pmul(&b.num, &a.den)?;
            let diff = algebra.padd(&l, &r.scale(&Q::from_integer((-1).into())))?;
            if diff.is_zero() {
                if ca != cb {
                    return Err("answer comparison has unresolved domain differences".into());
                }
                return Ok(true);
            }
            // A counterexample valid in BOTH domains proves inequality even
            // when their restrictions differ. Never cancel away domain guards.
            if ca != cb {
                for sample in counterexample_samples() {
                    if ca.iter().chain(cb.iter()).all(|c| condition_at(c, &sample))
                        && diff.interval_at(Some(&sample)).is_some_and(|(lo, hi)|
                            lo.is_positive() || hi.is_negative()) {
                        return Ok(false);
                    }
                }
                return Err("answer comparison has unresolved domain differences".into());
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
            for sample in counterexample_samples() {
                if !ca.iter().all(|c| condition_at(c, &sample)) {
                    continue;
                }
                if diff
                    .interval_at(Some(&sample))
                    .is_some_and(|(lo, hi)| lo.is_positive() || hi.is_negative())
                {
                    return Ok(false);
                }
            }
            Err("symbolic equivalence is not established by the supported rules".into())
        }
    }
}
fn counterexample_samples() -> impl Iterator<Item = Q> {
    // Include exact fractional witnesses inside bounded radical domains.
    // Substitutions prove inequality only; equality still needs a normal form.
    [-4, -2, 0, 1, 3].into_iter().map(|n| Q::from_integer(n.into()))
        .chain((-16..=8).filter(|n| n % 2 != 0).map(|n| Q::new(n.into(), 2.into())))
}
fn condition_at(c: &Condition, sample: &Q) -> bool {
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
    #[test]
    fn ivp_symbolic_roots_and_composed_log_intervals() {
        use super::{compare, Context};
        for (a, b) in [
            ("sqrt(2*exp(2*(x-1)^2)-1)", "(2*exp(2*(x-1)^2)-1)^(1/2)"),
            ("sqrt((x^2+1)/exp(x))", "sqrt(x^2+1)/sqrt(exp(x))"),
            ("ln(5/4-exp(-(x-1)))", "ln((5-4*exp(1-x))/4)"),
            ("ln(2-exp(-(x-1)))", "ln((8-4*exp(1-x))/4)"),
        ] {
            assert_eq!(compare(a, b, Context::default()), Ok(true), "{a} vs {b}");
        }
        for a in ["sqrt(2*exp(2*(x-1)^2)-1)", "sqrt(2*exp(2*(x-4)^2)-1)", "sqrt(2*exp(2*(x+4)^2)-1)", "ln(5/4-exp(-(x-1)))", "ln(2-exp(-(x-1)))"] {
            assert_eq!(compare(a, "0", Context::default()), Ok(false), "{a}");
            assert_eq!(compare("0", a, Context::default()), Ok(false), "{a}");
        }
        assert_eq!(compare("sqrt((x^2+1)/exp(x))", "-sqrt((x^2+1)/exp(x))", Context::default()), Ok(false));
        // Equal values with lost domains must still fail closed.
        assert!(compare("sqrt(x)^2", "x", Context::default()).is_err());
        assert!(compare("sqrt(1/x)", "1/sqrt(x)", Context::default()).is_err());
    }

    #[test]
    fn reciprocal_exponentials_preserve_arguments_and_domains() {
        for (a, b) in [
            ("1/e^{0.03t}", "e^{-0.03t}"),
            ("1/exp(3t/100)", "exp(-3t/100)"),
            ("exp(-x/7-2/3)", "1/exp(x/7+2/3)"),
            ("exp(-sin(x)/3)", "1/exp(sin(x)/3)"),
            ("exp(-1/x)", "1/exp(1/x)"),
            ("exp(-2x)", "1/exp(2x)"),
        ] {
            eq(a, b);
            eq(b, a);
        }
        for (a, b) in [
            ("1/e^{0.03t}", "e^{0.03t}"),
            ("1/e^{0.03t}", "e^{-0.04t}"),
            ("2/e^{0.03t}", "e^{-0.03t}"),
            ("exp(-x/7-2/3)", "1/exp(x/7)"),
        ] {
            assert_eq!(compare(a, b, Context::default()), Ok(false), "{a} vs {b}");
        }
        assert!(compare("exp(-x/x)", "exp(-1)", Context::default()).is_err());
        assert!(!supports("exp(-1/0)", Context::default()));
    }
    #[test]
    fn antiderivative_families_preserve_domain_and_nonconstant_terms() {
        use super::{compare, compare_up_to_constant, Context};
        let canonical = "t^7/7+5*t";
        for value in ["t^7/7+5*t+1", "5*t+t^7/7-3/2", "t^7/7+5*t+pi", "t^7/7+5*t+ln(2)"] {
            assert_eq!(compare_up_to_constant(value, canonical, Context::default()), Ok(true));
            assert_eq!(compare(value, canonical, Context::default()), Ok(false));
        }
        for wrong in ["t^7/6+5*t+1", "t^7/7+6*t+1", "t^7/7+5*t+t^2", "1"] {
            assert_eq!(compare_up_to_constant(wrong, canonical, Context::default()), Ok(false));
        }
        assert!(compare_up_to_constant("t^7/7+5*t+t/t", canonical, Context::default()).is_err());
        assert_eq!(compare_up_to_constant("ln(t)+3", "ln(t)", Context::default()), Ok(true));
        assert!(compare_up_to_constant("ln(t^2)/2+3", "ln(t)", Context::default()).is_err());
        assert_eq!(compare_up_to_constant("0", "ln(t)", Context::default()), Ok(false));
        assert_eq!(compare_up_to_constant("0", "1/sqrt(t)", Context::default()), Ok(false));
    }
    #[test]
    fn rational_logarithm_identities_preserve_grading_and_domains() {
        for (a, b) in [
            ("ln(4)", "2ln(2)"), ("ln(72)", "3ln(2)+2ln(3)"),
            ("ln(4/9)", "2ln(2)-2ln(3)"), ("ln(1/8)", "-3ln(2)"),
            ("4^x*ln(4)*sin(x)", "2*4^x*ln(2)*sin(x)"),
            ("4^x/(x*ln(4))", "4^x/(2x*ln(2))"),
            ("-15x^2*ln(4)", "-30x^2*ln(2)"),
        ] {
            eq(a, b);
            eq(b, a);
        }
        for (a, b) in [("ln(4)", "ln(2)"), ("-15x^2*ln(4)", "30x^2*ln(2)"),
                       ("4^x/(x*ln(4))", "4^x/(x*ln(2))")] {
            assert_eq!(compare(a, b, Context::default()), Ok(false));
        }
        assert!(!supports("ln(-4)", Context::default()));
        assert!(!supports("ln(0)", Context::default()));
        assert!(compare("ln(x^2)", "2ln(x)", Context::default()).is_err());
        assert!(compare("ln(4)*x/x", "2ln(2)", Context::default()).is_err());
    }
    #[test]
    fn fractional_counterexamples_reject_wrong_radical_answers() {
        for (a, b) in [("-x/sqrt(1-x^2)", "0"),
                       ("-x/sqrt(1-x^2)", "x/sqrt(1-x^2)"),
                       ("sqrt(1-x^2)", "0")] {
            assert_eq!(compare(a, b, Context::default()), Ok(false));
            assert_eq!(compare(b, a, Context::default()), Ok(false));
        }
        assert!(compare("sqrt(1-x^2)^2", "1-x^2", Context::default()).is_err());
        assert!(compare("x/x", "1", Context::default()).is_err());
    }
    #[test]
    fn natural_log_equation_answers_reject_wrong_values_beyond_old_bounds() {
        for rhs in [2, 19, 20, 21, 30, 128, 1000] {
            let canonical = format!("(4-ln({rhs}))/5");
            for equivalent in [format!("(ln({rhs})-4)/(-5)"), format!("4/5-ln({rhs})/5")] {
                assert_eq!(compare(&canonical, &equivalent, Context::default()), Ok(true));
            }
            for wrong in ["0".to_owned(), rhs.to_string(), format!("ln({rhs})-4")] {
                assert_eq!(compare(&canonical, &wrong, Context::default()), Ok(false), "{canonical} versus {wrong}");
                assert_eq!(compare(&wrong, &canonical, Context::default()), Ok(false));
            }
        }
        for (a, b) in [("ln(21)", "ln(22)"), ("ln(1/21)", "0"),
                       ("ln(1/1000)", "-1"), ("ln(1000)", "1")] {
            assert_eq!(compare(a, b, Context::default()), Ok(false), "{a} versus {b}");
        }
        assert!(compare("ln(x)/ln(x)", "1", Context::default()).is_err());
        assert!(!supports("ln(-21)", Context::default()));
    }

    #[test]
    fn reduced_logarithm_intervals_enclose_known_bounds() {
        let q = |n: i64, d: i64| Q::new(n.into(), d.into());
        for (x, lower, upper) in [(q(21,1),q(3044,1000),q(3045,1000)),
                                 (q(1,21),q(-3045,1000),q(-3044,1000)),
                                 (q(1000,1),q(6907,1000),q(6908,1000)),
                                 (q(1,1000),q(-6908,1000),q(-6907,1000))] {
            let (lo, hi) = log_bounds(&x).unwrap();
            assert!(lower < lo && lo < hi && hi < upper);
        }
        assert_eq!(log_bounds(&Q::one()), Some((Q::zero(), Q::zero())));
        assert!(log_bounds(&Q::zero()).is_none());
        assert!(log_bounds(&q(-1,1)).is_none());
        assert!(log_bounds(&Q::from_integer(BigInt::one() << 129)).is_none());
    }
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
    fn typed_slash_denominators_and_domain_counterexamples() {
        eq("11/4x", "\\frac{11}{4x}");
        eq("11/(4x)", "\\frac{11}{4x}");
        eq("-7/3x", "-\\frac{7}{3x}");
        eq("-7/(3x)", "-\\frac{7}{3x}");
        eq("(11/4)x", "\\frac{11}{4}x");
        eq("11/4*x", "\\frac{11}{4}x");
        assert_eq!(compare("(11/4)x", "11/(4x)", Context::default()), Ok(false));
        assert_eq!(compare("0", "11/(4x)", Context::default()), Ok(false));
        assert!(compare("x/x", "1", Context::default()).is_err());
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
    fn fractional_exp_constants_share_exact_power_form() {
        for q in ["0", "1", "-2", "1/2", "-1/2", "3/2", "2/4", "1/3", "-2/3", "5/4", "1/5", "5/6", "1/7", "7/8"] {
            let exponential = format!("exp({q})");
            let power = format!("e^({q})");
            eq(&exponential, &power);
            eq(&power, &exponential);
        }
        for (a, b) in [
            ("exp(1/2)", "sqrt(e)"),
            ("exp(3/2)", "sqrt(e^3)"),
            ("exp(-1/2)*exp(1/2)", "1"),
            ("exp(1/2)*exp(1/3)", "e^(5/6)"),
            ("8/(5*sqrt(5)*exp(1/2))", "8*sqrt(5)/(25*e^(1/2))"),
        ] {
            eq(a, b);
        }
        for wrong in ["-e^(1/2)", "2*e^(1/2)", "e^(-1/2)", "e^(1/3)"] {
            assert_eq!(compare("exp(1/2)", wrong, Context::default()), Ok(false));
        }
        assert!(supports("exp(1/100)", Context::default()));
        assert!(!supports("exp(1/0)", Context::default()));
        assert!(compare("exp((x/x)/2)", "e^(1/2)", Context::default()).is_err());
    }
    #[test]
    fn roots_of_positive_constant_powers_share_rational_power_form() {
        eq(r"\frac{\sqrt{e^3}}{3}", r"\frac{e^{\frac{3}{2}}}{3}");
        for base in ["e", "pi"] {
            for degree in 2..=8 {
                for exponent in 1..=8 {
                    let radical = format!(r"\sqrt[{degree}]{{{base}^{exponent}}}");
                    let power = format!("{base}^({exponent}/{degree})");
                    eq(&radical, &power);
                    eq(&power, &radical);
                }
            }
        }
        for wrong in ["-e^(3/2)/3", "2e^(3/2)/3"] {
            assert_eq!(compare("sqrt(e^3)/3", wrong, Context::default()), Ok(false));
        }
        assert!(!supports("sqrt(-e^3)", Context::default()));
        assert_eq!(compare("sqrt(x^2)", "x", Context::default()), Ok(false));
        assert!(compare("sqrt(x)^2", "x", Context::default()).is_err());
        assert!(compare("sqrt(e^3)*(x/x)", "e^(3/2)", Context::default()).is_err());
    }
    #[test]
    fn roots_of_compound_odd_powers_preserve_domains() {
        for (a, b) in [
            (r"-\left(2x+7\right)^{-\frac32}", r"-\frac{1}{\sqrt{(2x+7)^3}}"),
            ("sqrt((2x+7)^3)", "(2x+7)^(3/2)"),
            ("1/sqrt((x-2)^5)", "(x-2)^(-5/2)"),
            ("sqrt((x^2+1)^3)", "(x^2+1)^(3/2)"),
            ("sqrt((1-x)^3)", "(1-x)^(3/2)"),
            (r"\sqrt[4]{(2x-1)^3}", "(2x-1)^(3/4)"),
            ("cbrt((x+1)^3)", "x+1"),
            ("1/((x+1)*sqrt(x+1))", "(x+1)^(-3/2)"),
        ] {
            eq(a, b);
            eq(b, a);
        }
        for (a, b) in [
            ("-1/sqrt((2x+7)^3)", "(2x+7)^(-3/2)"),
            ("sqrt((x+1)^2)", "x+1"),
        ] {
            assert_eq!(compare(a, b, Context::default()), Ok(false), "{a} == {b}");
        }
        for (a, b) in [
            ("sqrt((x+1)^3)^2", "(x+1)^3"),
            ("sqrt((x+1)^3)/sqrt((x+1)^3)", "1"),
            ("(x*sqrt(x+1))/(x*sqrt(x+1))", "sqrt(x+1)/sqrt(x+1)"),
            ("sqrt((x/x)^3)", "1"),
            ("1/(sqrt(x^2-1)^2)", "1/(x^2-1)"),
            ("sqrt(x^2-1)^2/sqrt(x^2-1)^2", "1"),
            ("sqrt(((x+1)/x)^3)", "((x+1)/x)^(3/2)"),
        ] {
            assert!(compare(a, b, Context::default()).is_err(), "{a} == {b}");
        }
        assert!(!supports("sqrt((-x^2-1)^3)", Context::default()));
        assert!(!supports("sqrt((x+1)^65)", Context::default()));
    }
    #[test]
    fn rational_scaling_of_symbolic_radicands_is_exact() {
        for (a, b) in [
            (
                "2\\sqrt{1+\\frac{x^2}{9}}",
                "\\sqrt{4+\\frac{4x^2}{9}}",
            ),
            ("sqrt(4x)", "2sqrt(x)"),
            ("sqrt(x/9)", "sqrt(x)/3"),
            ("sqrt(18+9x^2)", "3sqrt(2+x^2)"),
            ("sqrt(4-4x)", "2sqrt(1-x)"),
            ("sqrt(-4x)", "2sqrt(-x)"),
            ("sqrt(4x^2)", "2abs(x)"),
            ("sqrt(4x^6)", "2abs(x)^3"),
            ("cbrt(8x)", "2cbrt(x)"),
            ("\\sqrt[4]{16x}", "2\\sqrt[4]{x}"),
            ("sqrt(4x)^2", "4sqrt(x)^2"),
            ("1/sqrt(4x)", "1/(2sqrt(x))"),
        ] {
            eq(a, b);
            eq(b, a);
        }
        for scale in 1..=8 {
            for denominator in 1..=8 {
                let a = format!("{scale}sqrt(1+x^2/{})", denominator * denominator);
                let b = format!(
                    "sqrt({}+{}*x^2/{})",
                    scale * scale,
                    scale * scale,
                    denominator * denominator
                );
                eq(&a, &b);
            }
        }
        // Coefficients beyond the new factoring bound remain supported as
        // opaque roots; normalizing must not narrow the previous parser.
        assert!(supports("sqrt(1000003+x^2)", Context::default()));
    }
    #[test]
    fn radicand_scaling_preserves_signs_and_domain_obligations() {
        for (a, b) in [
            ("sqrt(4+4x^2/9)", "-2sqrt(1+x^2/9)"),
            ("sqrt(4x^2)", "2x"),
            ("sqrt(4+4x^2/9)", "sqrt(4+x^2/9)"),
        ] {
            assert_eq!(compare(a, b, Context::default()), Ok(false), "{a} == {b}");
        }
        for (a, b) in [
            ("sqrt(-4x)", "-2sqrt(x)"),
            ("sqrt(4x)^2", "4x"),
            ("sqrt(4x/x)", "2"),
            ("sqrt(4x)/sqrt(4x)", "1"),
        ] {
            assert!(compare(a, b, Context::default()).is_err(), "{a} == {b}");
        }
        assert!(!supports("sqrt(-4-4x^2)", Context::default()));
    }
    #[test]
    fn domains_limits_and_unknown_identities_are_explicit() {
        for (a, b) in [("x/x", "1"), ("sqrt(x)^2", "x")] {
            assert!(compare(a, b, Context::default()).is_err());
        }
        assert_eq!(compare("ln(x)", "ln(x+1)", Context::default()), Ok(false));
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
