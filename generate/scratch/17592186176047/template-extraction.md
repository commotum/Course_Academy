# Template extraction (four stages)

Basis/lineage are preserved in `source.json`. The complete raw source evidence is separate from `recipes.json` (parameterized masks), `source-cases.json` (explicit public API replay inputs), and `review.md` (originals/replays/changed variants).

## 1. Specific observations

q-27015/q-27021 use numbered statements, Unicode π inside TeX fractions, a five-option text radio and no original solution/key. They contain interval claims `[-π,π]`/`[-1,0]` and general families with step π or 2π. q-103230 uses hyphen bullets and invisible Unicode function application in `cos⁡x`; its solution groups II and III into one shared range/output explanation. q-103233 uses three bullets and three separate verdicts; its false claim `π/2+2nπ` names only a proper subset of the zeros. q-27009/q-70667 use Roman-numbered prose and local intercept/extremum statements; q-27009’s raster includes horizontal extrema guides. q-70666 mixes a false general maximum family, a true negative-angle zero, and an incorrect symmetric range.

q-167631 contains five independent math blanks in the order of domain lower/upper endpoints, range lower/upper endpoints, and period. Captured EDB collection order is field-3, field-5, field-2, field-4, field-1; keys and placeholders identify their actual display roles. The prompt's long whitespace layout is preserved exactly in observed replay. Its displayed function and raster are sine, despite the owning cosine KP. This mislink does not change the validity of the five source answer values.

## 2. Shared mathematical pattern

Determine which three proposed properties of the unit cosine graph are true, then select the complete true-statement subset from an owned text radio bank. A pointwise zero/extremum claim is tested by exact cosine evaluation; a range/output claim is tested against `[-1,1]`; a general zero/extrema claim must describe the **entire** relevant input set. A family consisting only of every second zero does not qualify as “the zeros,” even though every point it lists is a zero. The separate five-blank template supplies domain/range endpoint fragments and period. The untransformed graph stays fixed under claim changes.

## 3. Complete component and bank mapping

Every source option is a **categorical subset recipe**, independently parsed from its displayed Roman labels. No scalar fit or uncertain error operation is required: `I and III only` means select exactly truth positions 1 and 3. These are alternative outcomes of the same assessed truth operation, not learner-facing distractor diagnoses.

| Profile | Complete displayed source bank (order immaterial) | Correct computed outcome |
|---|---|---|
| observed-q-27015 | III only; II only; II and III only; I only; I and III only | II only (original designation absent) |
| observed-q-27021 | II and III only; II only; I only; III only; I and II only | I only (original designation absent) |
| observed-q-103230 | I only; I and III only; I, II, and III; II and III only; III only | I only |
| observed-q-103233 | I and II only; I and III only; III only; II only; II and III only | II only |
| observed-q-27009 | I only; I and III only; III only; II only; II and III only | I only |
| observed-q-70666 | I and III only; I only; II only; II and III only; III only | II only |
| observed-q-70667 | I and II only; II and III only; II only; I and III only; I only | I and II only |

The q-167631 mapping is field-1 → domain lower `-\infty `; field-2 → domain upper `\infty `; field-3 → range lower `-1`; field-4 → range upper `1`; field-5 → period `2\pi `. Each field owns exactly one math answer, and its source whitespace is preserved in replay. All five placeholders occur in the original prompt. Raw API replay is mathematically correct for its actual displayed sine, but the sine content is an explicit curriculum mislink, not silently accepted as normal cosine generation.

In `recipes.json`, every prompt and available worked solution is a reusable mask. Slot definitions identify a **complete mathematical component**, its kind (angle/family/interval/number), and source notation style. Every masked component is reconstructed from exact rational parameters through `angle`, `family`, `interval`, or `numtex`; no branch returns a literal original payload or uses an answer lookup table. q-167631's finite function/plot slot is shared by raw sine replay and supported cosine repair. Fixed wording and all worked-solution stages remain in the masks.

## 4. Reusable masks, guards and computations

The seven observed radio templates have explicit slot dictionaries in `source-cases.json` and the implementation. Angle slots stay within familiar half/integer multiples in `[-2π,2π]`; family slots are one of six distinct complete input sets (offset reduced modulo step); output claims stay at `±3/2` or `±2`; incorrect intervals are the supported symmetric bounds 2/3/π or `[-1,0]`. All source-slot guard checks apply to explicit calls as well as sampled calls. The computed truth vector must equal the captured solution's fixed verdict pattern; otherwise the whole input is rejected. Thus shared source explanations remain correct under changed parameters. We infer only categorical recipe semantics, not the historical authoring algorithm.

Source-local solution masks preserve grouped verdicts, canonical corrective families and source point/intercept sentences. Both source replay and changed-parameter output are validated: original complete prompt, bank values, field keys/types, correct values and full solution text; changed output’s actual printed claims are parsed independently and compared with its categorical correct answer and solution verdicts. The two missing solutions use the common plot opening, “Let's go through each statement,” three independent verdicts and supported explanations. They are authored solutions with no exact-source denominator.

Authored default catalogs choose their **whole** five-member bank before assembly: the correct subset plus four fixed, deterministically ranked wrong categorical subsets of the eight possible truth outcomes. Complete banks are labeled authored. No member is patched from a first-valid pool; duplicate/missing correct outcomes reject the instance. Correct identities are recorded before seeded choice shuffling. One fixed worked solution accompanies the question, independent of the chosen error.

The easy/moderate/hard catalog bounds are enforced by membership, not loose generic coefficient guards. Hard contains three general-family claims in every instance; moderate contains one zero, one maximum family and one range; easy contains three distinct local landmarks. Every catalog member has equal workload within its level. The exact generator’s public API supports each source case through normal `generate(...)`, including the original sine replay profile. The canonical mathematical fingerprint contains semantic claims normalized modulo family step/local cosine period, excluding presentation aliases, bank choice and seed. Content identity includes version, actual prompt, fixed solution and complete displayed bank. Reordering radio answers changes neither identity.

## Repairs and limitations

- q-27015/q-27021: original EDB and original MA lesson widget (3557/Source/3557.json, questions 27015/27021) both lack explanations/keys. Independently verified correct outcomes are II only / I only; supported solutions and moderate assignment are explicitly authored. Original absent designations remain missing.
- q-167631: sine content is kept in observed replay; normal q-167631 uses cosine with the matching graph. Its domain/range/period fragments remain unchanged mathematically. No slash anomaly exists; byte inspection confirms single TeX slashes.
- No source mathematical error was found in the six available correct designations or their worked mathematics. The semantic set-completeness interpretation is supported by canonical e-11002’s false `nπ` minimum claim and the Introduction’s full-family formulas.
- These catalogs are finite. Equivalent integer shifts, variable aliases and incorrect coefficient magnitudes are not used to claim endless conceptual diversity. Source recovery does not imply original sampling algorithms or observed easy/hard labels.

Incorrect symmetric range bounds 2, 3 and π are incidental magnitudes in a truth-classification task: their lower/upper endpoint positions are identical relative to [-1,1], so they share a mathematical fingerprint. Similarly, output magnitudes outside the range share the below/above classification fingerprint. Their actual displayed values still affect complete content identity and source-bank fidelity.
