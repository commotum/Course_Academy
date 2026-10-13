# Complete choice-bank extraction

KP `17592186100890`; basis `1356`; version `trig-cartesian-guide-draft-4`.

All 56 incorrect choices are accounted for in 14 complete profiles; the 13 prompt/field/solution templates are unchanged. Each profile is selected before sampling, and all four recipes must remain distinct and incorrect. Formulas and eligibility conditions are explicit draft generalizations of the observed values, not recovered authoring code or proven diagnoses. Sources provide no option feedback.

Symbols: `a`, `b` are the supplied coefficients; `h`, `k` are the x/y offsets where present. Inputs use exact integers; output uses exact rational expressions and radicals.

The option-level [ledger](choice-extraction.json) retains source field/answer IDs, original values and positions, parameter dictionaries, recipe formulas, and replay results. The [fidelity report](source-bank-fidelity.json) compares complete equations, including nonzero constant rescaling, and preserves correct designations.

## sin_shift_exchange

Template: `ellipse_sin_radio`. Source: `q-15751`. Observed parameters: `{"a": 2, "b": 5, "h": -1, "k": 4}`.

Unequal positive scales; both offsets nonzero.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| ${(\frac{x-1}{2})}^{2}+{(\frac{y+4}{5})}^{2}=1$ | `(k + y)**2/b**2 + (h + x)**2/a**2 = 1` | `reverse_both_offsets` |
| ${(\frac{x+4}{5})}^{2}+{(\frac{y-1}{2})}^{2}=1$ | `(k + x)**2/b**2 + (h + y)**2/a**2 = 1` | `exchange_scales_and_offsets_keep_x_sign` |
| ${(\frac{x+4}{5})}^{2}+{(\frac{y+1}{2})}^{2}=1$ | `(k + x)**2/b**2 + (-h + y)**2/a**2 = 1` | `exchange_scales_and_offsets_reverse_y_sign` |
| ${(\frac{x-1}{2})}^{2}+{(\frac{y-4}{5})}^{2}=1$ | `(-k + y)**2/b**2 + (h + x)**2/a**2 = 1` | `reverse_x_offset` |

## sin_unit_y_shift

Template: `ellipse_sin_radio`. Source: `q-102680`. Observed parameters: `{"a": 1, "b": 1, "h": 0, "k": -5}`.

Unit scales; h=0 and k<0.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| $(x+5)^{2}+(y+5)^{2}=1$ | `(-k + x)**2 + (-k + y)**2 = 1` | `apply_y_offset_to_both_coordinates` |
| $(x-5)^{2}+{y}^{2}=1$ | `y**2 + (k + x)**2 = 1` | `move_offset_to_x_with_reversed_sign` |
| ${x}^{2}+(y-5)^{2}=1$ | `x**2 + (k + y)**2 = 1` | `reverse_y_offset` |
| ${x}^{2}+5{y}^{2}=1$ | `-k*y**2 + x**2 = 1` | `replace_y_offset_with_coefficient` |

## sin_compound_scale_offset

Template: `ellipse_sin_radio`. Source: `q-102682`. Observed parameters: `{"a": 5, "b": 3, "h": 3, "k": -2}`.

Positive scales; both offsets nonzero; whole-bank distinctness is checked.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| ${(\frac{x-3}{2})}^{2}+{(\frac{y+5}{3})}^{2}=1$ | `(-h + x)**2/k**2 + (a + y)**2/b**2 = 1` | `use_y_offset_as_x_scale_and_x_scale_as_y_offset` |
| ${(\frac{x+2}{5})}^{2}+{(\frac{y-3}{3})}^{2}=1$ | `(-h + y)**2/b**2 + (-k + x)**2/a**2 = 1` | `exchange_offsets` |
| ${(\frac{x-3}{2})}^{2}+{(\frac{y+2}{5})}^{2}=1$ | `(-h + x)**2/k**2 + (-k + y)**2/a**2 = 1` | `use_y_offset_as_x_scale_and_exchange_y_scale` |
| ${(\frac{x-5}{3})}^{2}+{(\frac{y+3}{2})}^{2}=1$ | `(h + y)**2/k**2 + (-a + x)**2/h**2 = 1` | `exchange_scale_offset_roles_in_both_coordinates` |

## sin_unit_x_shift_identity

Template: `ellipse_sin_radio`. Source: `q-15657`. Observed parameters: `{"a": 1, "b": 1, "h": -3, "k": 0}`.

Unit scales; h<=-2 and k=0.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| ${x}^{2}+(y-3)^{2}=1$ | `x**2 + (h + y)**2 = 1` | `move_x_offset_to_y_with_reversed_sign` |
| $3{x}^{2}+{y}^{2}=1$ | `-h*x**2 + y**2 = 1` | `replace_x_offset_with_coefficient` |
| ${x}^{2}+{y}^{2}=3$ | `x**2 + y**2 = -h` | `move_x_offset_to_identity_constant` |
| $(x-3)^{2}+(y-3)^{2}=3$ | `(h + x)**2 + (h + y)**2 = -h` | `reverse_and_duplicate_offset_and_change_constant` |

## cos_identity_scale

Template: `ellipse_cos_radio`. Source: `q-15752`. Observed parameters: `{"a": 2, "b": 3, "h": 0, "k": 0}`.

Unequal positive scales; offsets may be zero or nonzero.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| ${(\frac{y}{2})}^{2}-{(\frac{x}{3})}^{2}=2\pi $ | `-(-h + x)**2/b**2 + (-k + y)**2/a**2 = 2*pi` | `exchange_scales_subtract_and_use_interval_constant` |
| $-{(\frac{y}{3})}^{2}+{(\frac{x}{2})}^{2}=1$ | `-(-k + y)**2/b**2 + (-h + x)**2/a**2 = 1` | `subtract_y_identity_term` |
| ${x}^{2}+{y}^{2}=6$ | `(-h + x)**2 + (-k + y)**2 = a*b` | `omit_scales_and_use_product_as_constant` |
| ${(\frac{y}{2})}^{2}-{(\frac{x}{3})}^{2}=1$ | `-(-h + x)**2/b**2 + (-k + y)**2/a**2 = 1` | `exchange_scales_and_subtract` |

## cos_unit_shift_identity

Template: `ellipse_cos_radio`. Source: `q-15679`. Observed parameters: `{"a": 1, "b": 1, "h": -2, "k": 3}`.

Unit scales; h<0 and k>=2.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| $(y-3)^{2}+{x}^{2}=1$ | `x**2 + (-k + y)**2 = 1` | `omit_x_offset` |
| $(y-2)^{2}+(x-3)^{2}=1$ | `(h + y)**2 + (-k + x)**2 = 1` | `exchange_offsets_and_reverse_x_sign` |
| $(y+3)^{2}+(x+2)^{2}=3$ | `(-h + x)**2 + (k + y)**2 = k` | `reverse_y_offset_and_change_constant` |
| ${y}^{2}+(x+3)^{2}=3$ | `y**2 + (k + x)**2 = k` | `omit_y_offset_shift_x_by_y_offset_and_change_constant` |

## tan_sec_source

Template: `tan_sec_radio`. Source: `q-102677`. Observed parameters: `{"a": 2, "b": 1}`.

a>=2; b=1.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| ${y}^{2}={(\frac{x}{2})}^{2}-1$ | `y**2 = -1 + x**2/a**2` | `reverse_identity_constant` |
| ${y}^{2}={(\frac{2}{x})}^{2}+1$ | `y**2 = a**2/x**2 + 1` | `invert_coordinate_ratio` |
| ${y}^{2}={x}^{2}+2$ | `y**2 = a + x**2` | `omit_scale_and_use_it_as_constant` |
| ${y}^{2}=1-{(\frac{x}{2})}^{2}$ | `y**2 = 1 - x**2/a**2` | `reverse_squared_term` |

## cot_csc_source

Template: `cot_csc_radio`. Source: `q-15761`. Observed parameters: `{"a": 3, "b": 1}`.

a>=3; b=1; a=2 would duplicate two options.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| ${y}^{2}=1+{x}^{2}$ | `y**2 = x**2 + 1` | `omit_coordinate_scale` |
| ${y}^{2}=1-{(\frac{x}{3})}^{2}$ | `y**2 = 1 - x**2/a**2` | `reverse_squared_term` |
| ${y}^{2}=1-3{x}^{2}$ | `y**2 = -a*x**2 + 1` | `use_scale_as_coefficient_and_reverse_sign` |
| ${y}^{2}=1+{(\frac{x}{2})}^{2}$ | `y**2 = x**2/(a - 1)**2 + 1` | `use_scale_minus_one` |

## cos_tan_source

Template: `cos_tan_radio`. Source: `q-102687`. Observed parameters: `{"a": 1, "b": 1}`.

Positive coefficients; sampling uses a,b in 1..4; source coefficients are both one.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| $y=\frac{\sqrt{1-{x}^{2}}}{2x}$ | `y = b*sqrt(a**2 - x**2)/(2*x)` | `double_denominator` |
| $y=\frac{1-{x}^{2}}{2x}$ | `y = a*b*(1 - x**2/a**2)/(2*x)` | `omit_root_and_double_denominator` |
| $y=\sqrt{1-{x}^{2}}$ | `y = b*sqrt(1 - x**2/a**2)` | `omit_tangent_denominator` |
| $y=\frac{1-{x}^{2}}{x}$ | `y = a*b*(1 - x**2/a**2)/x` | `omit_root` |

## sin_tan_source

Template: `sin_tan_radio`. Source: `q-15759`. Observed parameters: `{"a": 1, "b": 1}`.

Positive coefficients; sampling uses a,b in 1..4; source coefficients are both one.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| $y=\frac{4x}{\sqrt{1+{x}^{2}}}$ | `y = 4*b*x/sqrt(a**2 + x**2)` | `alter_factor_and_radical_sign` |
| $y=\frac{x}{\sqrt{{x}^{2}-4}}$ | `y = b*x/sqrt(-4*a**2 + x**2)` | `reverse_radical_sign_and_alter_constant` |
| $y=\frac{2x}{\sqrt{2+{x}^{2}}}$ | `y = 2*b*x/sqrt(2*a**2 + x**2)` | `alter_factor_and_radical_constant` |
| $y=\frac{2x}{\sqrt{{x}^{2}-1}}$ | `y = 2*b*x/sqrt(-a**2 + x**2)` | `reverse_radical_sign_and_double_factor` |

## sin_double_factored_source

Template: `sin_double_factored_radio`. Source: `q-24378`. Observed parameters: `{"a": 2, "b": 3}`.

Positive a; b>=2.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| $y=1-\frac{{x}^{2}}{4}$ | `y = 1 - x**2/a**2` | `omit_y_scale_and_double_angle_factor` |
| $y=3(1+\frac{{x}^{2}}{4})$ | `y = b*(1 + x**2/a**2)` | `reverse_sign_and_omit_double_angle_factor` |
| $y=2(1+\frac{{x}^{2}}{4})$ | `y = (1 + x**2/a**2)*(b - 1)` | `alter_outer_scale_sign_and_double_angle_factor` |
| $y=1-\frac{{x}^{2}}{2}$ | `y = 1 - 2*x**2/a**2` | `omit_y_scale` |

## sin_double_expanded_source

Template: `sin_double_expanded_radio`. Source: `q-24576`. Observed parameters: `{"a": 6, "b": -5}`.

Positive a; negative b.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| $y=1+\frac{5{x}^{2}}{6}$ | `y = 1 - b*x**2/a` | `alter_constant_and_unsquare_scale` |
| $y=5+{x}^{2}$ | `y = -b + x**2` | `reverse_constant_and_omit_quadratic_scale` |
| $y=-18+\frac{{x}^{2}}{5}$ | `y = -a**2/2 - x**2/b` | `exchange_constant_and_denominator_roles` |
| $y=\frac{1}{5}-{x}^{2}$ | `y = -x**2 - 1/b` | `reciprocate_constant_and_omit_scale` |

## cos_double_positive_source

Template: `cos_double_radio`. Source: `q-24574`. Observed parameters: `{"a": 4, "b": 2}`.

Positive a and b.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| $y=3(\frac{{x}^{2}}{5}-1)$ | `y = (b + 1)*(x**2/(a + 1) - 1)` | `alter_outer_scale_and_use_scale_plus_one` |
| $y=\frac{{x}^{2}}{4}+1$ | `y = 1 + x**2/a` | `use_unsquared_scale_and_reverse_constant` |
| $y=3{x}^{2}+8$ | `y = a*b + x**2*(b + 1)` | `alter_quadratic_coefficient_and_use_scale_product_as_constant` |
| $y=1-\frac{{x}^{2}}{8}$ | `y = 1 - 2*x**2/a**2` | `reverse_identity_and_omit_outer_scale` |

## cos_double_negative_source

Template: `cos_double_radio`. Source: `q-24575`. Observed parameters: `{"a": -3, "b": 4}`.

Negative a; positive b.

| Original incorrect value | Parameterized equation | Recipe interpretation (inferred) |
|---|---|---|
| $y=\frac{{x}^{2}}{9}-1$ | `y = -1 + x**2/a**2` | `omit_outer_scale_and_double_angle_factor` |
| $y=1+\frac{{x}^{2}}{6}$ | `y = 1 - x**2/(2*a)` | `use_twice_signed_scale_and_reverse_constant` |
| $y=1-\frac{{x}^{2}}{9}$ | `y = 1 - x**2/a**2` | `reverse_identity_and_omit_double_angle_factor` |
| $y=7(\frac{{x}^{2}}{9}+1)$ | `y = (1 + x**2/a**2)*(-a + b)` | `use_scale_difference_reverse_constant_and_omit_double_angle_factor` |

