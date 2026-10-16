# Classification at EDB basis 2757

Database `math`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`.
KP 17592186179742: Interpreting the Sign of a Line Integral Over a Non-Constant Vector Field.
All 13 practice questions and the canonical example were pulled together, including full fields, banks, keys, solutions, difficulty and asset references (`source.json`, `reference/initial/kp.edn`). No registered generator or supplied `.generated` file existed.

| Difficulty | Fields | Backbone templates | New plots |
|---|---|---|---|
| easy | three checkbox fields I/II/III, or one five-option radio field selection | tangent ellipse/circle; general curve opposing motion; general curve assisting motion | heavy |
| moderate | three checkbox fields I/II/III, or one five-option radio field selection | perpendicular field on ellipse/circle; perpendicular field on segment | heavy |
| hard | no observed fields or source templates | none supported by this bounded implementation | unsupported |

Changed sign assertions and field layouts are recorded separately in `source-mapping.json`; they are not silently merged. Within the ellipse backbones, quarter/half/three-quarter sweeps, axis ratio, orientation and force direction are geometric slots, subject to the observed level restrictions. General-curve tangent alignment need not equal a merely positive/negative dot product; those source backbones stay separate and replay-only.

Source families and every field choice appear in `source-mapping.json`. Choice-bank profiles consist of actual true/false field banks, or the complete radio bank {I only, II only, III only, I and III only, II and III only}. All three radio sources share that complete bank. The canonical example supports the perpendicular-curve interpretation but is never practice inventory.

The 13 sources contain 10 checkbox questions and three radio questions. Their complete banks have 75 values, including 42 incorrect field-level values. No missing fields, missing keys or unresolved source bank values were observed. Source diagrams have no numerical coordinate values; no exact source vector-field formula is claimed. Graphically perpendicular/tangent/assisting/opposing relationships were read alongside both worked-solution diagrams.

The initial native pool has seven easy and six moderate unused, gradable questions and no shown/reserved questions. For replenishment, mathematically equivalent normal-field quarter-circle sources are collapsed, as are the two perpendicular straight segments; four distinct moderate tasks remain. A new normal-field quarter-ellipse supplies the fifth distinct task. This is an explicit stricter deduplication than raw entity counting.
