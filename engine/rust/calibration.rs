//! Replayable, independent assessment/practice accuracy.
//! These update rules are local reconstruction policies, not MA parameters.
use crate::Result;
use serde::{Deserialize, Serialize};

fn number(value: f64, name: &str, high: Option<f64>) -> Result<()> {
    if !value.is_finite() || value < 0.0 || high.is_some_and(|hi| value > hi) {
        return Err(format!("{name} must be finite and within bounds"));
    }
    Ok(())
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(default, deny_unknown_fields)]
pub struct AccuracyEstimate {
    pub assessment_accuracy: f64,
    pub practice_accuracy: f64,
    pub assessment_mass: f64,
    pub practice_mass: f64,
}

impl Default for AccuracyEstimate {
    fn default() -> Self {
        Self::new(0.8)
    }
}

impl AccuracyEstimate {
    pub fn new(prior: f64) -> Self {
        Self {
            assessment_accuracy: prior,
            practice_accuracy: prior,
            assessment_mass: 0.0,
            practice_mass: 0.0,
        }
    }

    pub fn validate(&self) -> Result<()> {
        number(self.assessment_accuracy, "assessment_accuracy", Some(1.0))?;
        number(self.practice_accuracy, "practice_accuracy", Some(1.0))?;
        number(self.assessment_mass, "assessment_mass", None)?;
        number(self.practice_mass, "practice_mass", None)
    }

    pub fn accuracy(&self) -> f64 {
        (self.assessment_accuracy + self.practice_accuracy) / 2.0
    }

    /// Ordered fractional evidence updates one channel, atomically.
    pub fn update(
        &mut self,
        outcomes: &[bool],
        assessment: bool,
        alpha: f64,
        weight: f64,
    ) -> Result<&mut Self> {
        self.validate()?;
        number(alpha, "alpha", Some(1.0))?;
        number(weight, "weight", None)?;
        if alpha == 0.0 {
            return Err("alpha must be positive".into());
        }
        if outcomes.is_empty() || weight == 0.0 {
            return Ok(self);
        }
        let (old_accuracy, old_mass) = if assessment {
            (self.assessment_accuracy, self.assessment_mass)
        } else {
            (self.practice_accuracy, self.practice_mass)
        };
        let mass = old_mass + weight * outcomes.len() as f64;
        number(mass, "updated evidence mass", None)?;
        let step = if alpha == 1.0 {
            1.0
        } else {
            -(weight * (-alpha).ln_1p()).exp_m1()
        };
        let mut accuracy = old_accuracy;
        for &correct in outcomes {
            accuracy = (1.0 - step) * accuracy + step * f64::from(correct);
        }
        number(accuracy, "updated accuracy", Some(1.0))?;
        if assessment {
            self.assessment_accuracy = accuracy;
            self.assessment_mass = mass;
        } else {
            self.practice_accuracy = accuracy;
            self.practice_mass = mass;
        }
        Ok(self)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn channels_are_balanced_and_fractional_updates_compose() {
        let mut ability = AccuracyEstimate::default();
        ability.update(&[true; 100], false, 1.0, 1.0).unwrap();
        ability.update(&[false], true, 1.0, 1.0).unwrap();
        assert_eq!(ability.accuracy(), 0.5);
        assert_eq!(ability.practice_mass, 100.0);
        let mut whole = AccuracyEstimate::default();
        let mut split = whole.clone();
        whole.update(&[false], true, 0.2, 1.0).unwrap();
        split.update(&[false, false], true, 0.2, 0.5).unwrap();
        assert!((whole.assessment_accuracy - split.assessment_accuracy).abs() < 1e-15);
        assert_eq!(whole.assessment_mass, split.assessment_mass);
    }

    #[test]
    fn ordered_updates_are_atomic_and_round_trip() {
        let mut ability = AccuracyEstimate::default();
        ability.update(&[true, false], false, 0.2, 1.0).unwrap();
        assert!((ability.practice_accuracy - 0.672).abs() < 1e-14);
        let before = ability.clone();
        assert!(ability.update(&[true, false], true, 0.2, 1e308).is_err());
        assert_eq!(ability, before);
        assert_eq!(
            ability,
            serde_json::from_str::<AccuracyEstimate>(&serde_json::to_string(&ability).unwrap())
                .unwrap()
        );
    }

}
