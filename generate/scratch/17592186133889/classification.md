# Classification — KP 17592186133889

Captured database math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Fourteen practice questions: seven easy, seven moderate, no hard. Canonical e-9489 is curricular evidence, not a fifteenth practice question.

| Difficulty | Observed fields | Extracted source templates/banks | Plot rating |

|---|---|---|---|

| Easy | Five radio, two blank | 7 templates, 5 complete radio banks | none |

| Moderate | Seven radio | 7 templates, 7 complete radio banks | none |

| Hard | None observed; authored radio/blank | 2 authored equal-level templates | none |

Each source has an explicit parameterized scale-mask recipe. We retain separate rows when formal inputs, collection stages, evaluation stages or blank layouts differ. Uniform scale is a component parameter, but these evidence recipes do not claim recovery of distractor intent. Normal generation selects separately authored eligible banks.

| Source | Difficulty | Field | Prompt components | Original correct |

|---|---|---|---|---|

| q-105555 | easy | radio | $\operatorname{ln}⁡(xy), -y\operatorname{cos}⁡x, y{z}^{3}$ | $\frac{1}{x}-\operatorname{cos}⁡x+3y{z}^{2}$ |

| q-41839 | moderate | radio | $xyz, {e}^{-y}\operatorname{cos}⁡\pi x, {e}^{-y}\operatorname{sin}⁡\pi z+2xz$ | $\pi +3$ |

| q-168615 | easy | blank | ${z}^{2}, 2xy, x{y}^{2}$ | $2x$ |

| q-123176 | easy | radio | ${e}^{x}\operatorname{sin}⁡yz, xyz, 2$ | ${e}^{x}\operatorname{sin}⁡yz+xz$ |

| q-123179 | easy | radio | $(2x+3y-4z)^{2}, (2x+3y-4z)^{2}, (2x+3y-4z)^{2}$ | $4x+6y-8z$ |

| q-123200 | moderate | radio | $(x-y)^{3}, (y+z)^{3}, (x+z)^{3}$ | $96$ |

| q-131176 | easy | radio | $2xy{z}^{2}, x{e}^{y}, y{z}^{3}$ | $5y{z}^{2}+x{e}^{y}$ |

| q-131178 | moderate | radio | $xz\operatorname{cos}⁡y, y{x}^{2}, x{z}^{2}{e}^{y}$ | $-5$ |

| q-131179 | moderate | radio | $x(y{e}^{z}+\operatorname{ln}⁡y), xy{e}^{z}, z(x+1)$ | $4$ |

| q-168624 | easy | blank | $0, 0, -xy-2{z}^{2}$ | $-4z$ |

| q-123192 | moderate | radio | ${x}^{2}yz, x{y}^{2}z, xy{z}^{2}$ | $24$ |

| q-41837 | easy | radio | ${e}^{xz}\operatorname{cos}⁡y, 0, \operatorname{ln}⁡yz$ | $z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{z}$ |

| q-105559 | moderate | radio | $\operatorname{cos}⁡\pi x, y\operatorname{sin}⁡\pi y, {e}^{2z}$ | $2-\pi $ |

| q-123196 | moderate | radio | $(x+y)^{2}, (y+z)^{2}, (x+z)^{2}$ | $-8$ |

## Source anomalies and repairs

q-168615 and q-168624 contain the response line and matching field-1 placeholder but omit the vector declaration. Their worked-solution formal operator rows identify respectively F=⟨z²,2xy,xy²⟩ and G=⟨0,0,-xy-2z²⟩. The public source_* recipes preserve raw prompt strings and are evidence_only, eligible_for_learning=false. Public easy templates zero_terms and axial prepend those complete declarations with parameterized scale, retain the original blank shape and solution sequence, and are supported_presentation_repair, eligible_for_learning=true. These are two supported prompt repairs, separate from exact raw replay counts.

q-123179 begins its explanation with F=P+Qj+Rk: the i after P is missing. This prose typo remains in raw evidence. Normal shared_square output uses the common correct P i+Q j+R k opening. It is one prose repair, separate from the two incomplete prompt repairs; no mathematical value or source correct designation needs repair.

All 14 source difficulty labels and correct references are present. No missing-label inference or missing-correct designation is counted as a match. The local original MA lesson 2131 Source/2131.json confirms the 3D lesson narrative and canonical example but does not contain the later q-168615/q-168624 widgets; component repair therefore relies on captured ordered derivative inputs and independent mathematical checking, not a claim that an unavailable widget was inspected.
