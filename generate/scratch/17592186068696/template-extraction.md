# Template extraction (four stages)

## 1. Specific originals

The complete question records are retained in `source.json`. `source-bank-map.json` lists each field and every choice, source UUID, answer type, exact decoded string and coordinate/image recipe. `source-cases.json` maps all 17 originals to public replay calls. List questions show one source graph and ask for every break, with two or three integer x coordinates. Their fixed solution first describes the breaks using the pencil criterion, then gives the same coordinate set in a Therefore sentence. Image-selection questions state one integer target and offer five complete plots. Their fixed solution identifies a break/jump/asymptote at that same target, optionally shows a highlighted plot, and states that the other plots are continuous. Blank questions ask for one coordinate or two in ascending order; the solution uses the canonical pencil-criterion sentence. Their graph widgets were not captured in the frozen prompt.

The list graph at q-48080 has a vertical asymptote at -2 and jump at 0. q-48090 has a displaced hole at 1, asymptote at 2 and jump at 4. q-104021 has an asymptote at -2, jump at 1 and asymptote at 3. q-104020 has a jump at 0 and displaced hole at 2. q-104023 has a jump at -2 and displaced hole at 0. q-48087 has a displaced hole at -2 and asymptote at 2. q-104025 has a displaced hole at -1 and jump at 2. q-48088 has an unfilled hole at -3 and one-sided asymptote at 0. Image-selection correct plots show, respectively: displaced hole at -3 (q104040); asymptote at 1 (q48074); asymptote at -1 with a separately assigned filled value (q48076); jump at -2 (q104036); displaced hole at 1 (q48038). Every other plotted option is connected, including nondifferentiable corners; corners are not breaks. Vertical y values are not labelled in these practice rasters and are not asserted to have exact formulas.

## 2. Shared pattern and purpose

Read the graph's open/filled points, disconnected branches and vertical asymptotes to identify x coordinates where the plotted function breaks. The response is a coordinate set, fieldwise coordinate fragments, or selection of one entire graph. No mathematical formula is supplied or inferred for assessment. A connected corner, oscillation or turning point does not create a discontinuity.

## 3. Component/option mapping

Each source radio bank is retained as an explicit `observed:q-ID` profile. Scalar/text choices are complete coordinate sets, transformed by the same injective horizontal affine map as the graph. This is a defensible geometric recipe for the displayed object; the original distractor intent is often underdetermined. No claim of recovered psychological error intent is made. Plotted choices use their own branch and marker recipe; none borrow the correct graph's geometry. Legacy banks, raw whitespace and missing attributes remain public evidence.

Normal list banks are separately labelled authored operations, chosen together before parameters: for two breaks {a,b}, use {a,b}, {a}, {b}, {a,c}, {b,c}, with c=b+1; for three breaks {a,b,c}, use the full set, each two-element omission, and the middle point alone. These represent omission of a visible break or inclusion of a neighbouring continuous coordinate. The complete bank is rejected on any set collision; individual choices are never replaced. Normal image-selection banks retain the five observed graph roles. Blank fields retain their observed single-coordinate answer shape and ascending-order layout.

## 4. Stable backbone and slots

The source prompt, full worked-solution prose and sentence/stage order are masks rather than literal returned payloads. Eligible numeric atoms lie only inside complete coordinate math components. A symmetric ± component becomes a complete two-coordinate expression when shifted. Graph references are replaced as complete asset components. Every source recipe supports x↦s x+h, s∈{1,2}, integer h∈[-3,3]; all graphs in a plotted bank use the same affine map. These slots change actual graph coordinates, stated targets, all bank coordinate values and both introductory/concluding solution coordinates together. Vertical shape is preserved; no new function operator is introduced. All explicit inputs obey the same domain guards. At identity parameters, raw replay uses the exact original paths because the geometry is unchanged; at changed parameters Matplotlib renders the independently extracted branches/markers.

Normal easy samples all 17 source-shaped family profiles and all four response layouts. The blank-widget repair supplies a clearly authored discontinuous graph because the original missing widget cannot be recovered from local MA lesson 462. The fieldless source receives an explicitly authored five-choice coordinate-set field. The legacy duplicate field is retained only in raw evidence; normal practice uses one valid field. Normal solutions retain each source's actual operative prose; source selection solutions that say “shown below” but omit a picture receive their own correct graph at that exact stage.

Authored moderate/hard use the source list prompt and full two-sentence solution backbone. Both show a displaced hole, a jump and an asymptote. Their three coordinates are ordered within [-4,4], integer or half-integer, straddle zero, and are separated by at least 1.5. Moderate requires exactly one half-integer and labelled 0.5 grid increments; hard requires exactly two half-integers, labelled unit increments and one connected corner. Vertical reflection is an eligible orientation, not an extra mathematical-task count. Complete finite domains contain **99 easy**, **114 moderate** and **99 hard** meaningful tasks. Easy counts unify radio and blank coordinate-set layouts and deduplicate shared profiles; vertical reflections do not inflate these counts. Neither level admits the other's workload. The moderate/hard level labels remain explicit design claims.

Mathematical fingerprints unify equivalent coordinate-set tasks across radio/blank layouts and include the assessed coordinates and scale-reading workload; graph-selection remains its separate assessed criterion; they exclude seed, option order, vertical reflection, variable aliases and bank profiles. Content identity separately includes actual difficulty, prompt, fixed solution and complete displayed bank. Fixed parameters preserve IDs under shuffling; different visible banks change IDs.

## Source anomalies and fidelity denominators

- q48080 retains two fields with key `selection`; the first has no correct designation. The second is the authoritative active field (also corroborated by the plotted graph and solution). Raw replay preserves both banks and the omission; normal has one supported field. Native grading uses an explicitly labelled active-widget fixture adapter for the raw legacy record; it does not mutate public replay or count the missing designation as matched.
- q104021 lacks `:question/answer-fields` entirely. Raw replay omits the key. Normal adds an authored field with independently verified {-2,1,3}.
- q131299/q131334/q131482/q131483 lack their plotted widget in the captured prompt. Local MA lesson 462 contains none of these q IDs/assets. Raw evidence remains ineligible, even though its numeric answer grade fixtures work. Supplied plots and whitespace cleanup are authored presentation repairs, not recovered original widgets.
- Several raw math choices contain two adjacent decoded backslashes before `pm`. This was verified by testing decoded substring membership and counting ord(92) runs, not by interpreting JSON serialization. q48087's nested correct value has one slash while its actual choice has two, but its correct UUID selects that choice. Raw choice spelling and designation are preserved; normal authored set strings avoid this malformed TeX. Source correctness and raw formatting are not conflated.

Verified raw denominators: **17/17 complete prompts and full worked solutions**, **19/19 field banks**, **71/71 displayed choices**, **18/18 present correct designations**. The one absent designation, one absent fields attribute and four omitted widgets are preserved and separately reported. DB numeric IDs and original MA IDs are provenance, not reused identities for newly generated records. Runtime UUID/enum normalization and lookup-ref representation follow the established local generator format.


## Current checkbox source supplement (basis 2230)

Seven current prompts append “Select all that apply” and Roman-labelled scalar
x-coordinate candidates to the original graph-reading prompt. Each candidate
owns a two-value text bank `{true,false}`; its key is true exactly when the
candidate coordinate belongs to the graph's independently read break set.
This is a separate current response layout, not a recovered historical radio
distractor recipe. Every current candidate, field, Boolean choice and correct
designation is retained in the live EDN capture; the independent validator parses
the Roman labels and coordinates and checks each complete Boolean bank against
open markers and vertical asymptotes. The source's worked-solution sequence and
full original wording remain unchanged. The seven profiles are q-48080, q-48090,
q-104020, q-104023, q-48087, q-104025 and q-48088. Their respective candidate
counts are 3, 3, 3, 3, 5, 4 and 5.

This replenishment executes the frozen generator's already validated moderate
and hard authored coordinate-set radio templates. Those templates and their
complete subset-bank recipes remain explicitly authored extensions with the
previously reviewed same-method scope and difficulty guards; they do not claim
fidelity to the newer checkbox layout. Every new coordinate triple is distinct
and includes noninteger coordinates absent from the easy source tasks.
