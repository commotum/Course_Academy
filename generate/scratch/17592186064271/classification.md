# Classification at math basis 1356

Database math, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Raw provenance is retained in source.json. The KP is **Determining the Units of a Derivative**, owning topic 296 / db 17592186048835, Interpreting the Meaning of the Derivative in Context. Its key prerequisite is Selecting Units for Rates of Change (2231).

The first-step/next chain in the captured lesson is Introduction → this Units KP → Interpreting the Derivative of a Function → Interpreting the Derivative in a Given Context → Determining a Rate of Change → Relating a Derivative to a Rate of Change. This order is obtained by following refs, not the Pull collection order. Introduction and canonical rocket example teach `[dependent quantity] / [independent quantity]`, displaying unit declarations, the change-ratio explanation, the unit quotient, and a prose conclusion.

| Template | Practice source | Captured difficulty | Local replay level | Fields / complete bank | Plots |
| --- | --- | --- | --- | --- | --- |
| farmer | q-48557 | unrated | hard, authored workload assignment | one radio, five text choices; missing correct ref; invalid original bank | none |
| pail | q-48613 | unrated | easy, authored workload assignment | one radio, five text choices; missing correct ref | none |
| website | q-110040 | easy | easy | no captured field; authored five-text radio repair | none |
| reward | q-72091 | easy | easy | no captured field; authored five-text radio repair | none |
| cupcake | q-110037 | easy | easy | one radio, five text choices | none |
| milk | q-110038 | easy | easy | one radio, five text choices | none |
| battery | q-110042 | easy | easy | one radio, five text choices | none |
| currency | q-72092 | easy | easy | one radio, five text choices | none |
| coffee | q-48611 | easy | easy | one radio, five text choices | none |

There are nine observed contextual Markdown/value templates and seven observed complete choice banks. Different context/solution prose keeps the templates separate although the assessed operation is shared. Seven source questions have explicit easy labels; neither moderate nor hard has a captured explicit label. The farmer's compound input units warrant an authored hard assignment consistent with the hard extension, rather than inventing an observed difficulty. There are no images in the nine practice sources and no new plots; steps 5/7 require no renderer.

## Repairs and limits

The authoritative original lesson widget snapshot `/home/jake/Developer/MA/DATA/Lessons/296/Source/296.json` confirms both older banks, including the farmer's `p dollars per ton`. Relevant widgets, original layout, and provenance are preserved in authoritative-widgets.json. The missing farmer/pail correct refs cannot count as matched original designations. The derivations determine their values independently.

For the farmer, tons/(dollars/ton) is tons²/dollar, absent from all five original options. Normal output changes **only** `tons per dollar` to `squared tons per dollar`. The four remaining displayed choices remain exact. The raw_observed API profile preserves all five original strings and intentionally has no correct ref; it is invalid evidence, not a normal learner question. Missing source solution is authored using the lesson's four-stage operator narrative. Pail retains all original strings, infers cubic centimeters/second and supplies the same authored solution sequence.

Website/reward fields are absent, and the available older authoritative lesson snapshot contains neither widget. Their five-option radio fields and bank profiles are expressly authored repairs, not recovered source fields. A single derivative-unit response demand matches every valid neighboring source; no extra assessment is added. Website prompt declares **visits**, while source solution says **visitors**. Normal output changes visitors to visits; observed profile preserves the raw solution exactly and is marked as raw teaching evidence in review/validation. Its repaired field always answers visits/hour.

## Authored missing-level bounds

Easy retains direct dependent/input unit identification in the observed context shapes, including cubic volume and different named time units. No unit conversion calculation is requested. Whole named units are parameterized with explicit context-appropriate finite domains in templates.json, including gram/kilogram and liter/milliliter source distractor distinctions.

Moderate `non_time_power` uses a squared or cubic length quantity per item/package/ticket/cupcake count, extending the observed pail's powered unit labels and cupcake's non-time count input. Each question has exactly one powered label and one count input; all sixteen parameter combinations require the same quotient recognition. The authored difficulty label is a design choice, not a claim of recovered MA labels. No artificial progression, numeric functions, or differentiation is introduced.

Hard `price_rate` extends the observed unrated farmer to quantity / (currency / same quantity). It has exactly one compound input unit and one cancellation/inversion: quantity²/currency. Quantity is ton, kilogram, liter, meter, item, package, ticket, or cupcake; currency is dollar or euro. Sixteen authored combinations use the same operation and workload. No conversion, numerical rate interpretation, second derivative, or inverse derivative is required. The corrected farmer fits exactly this workload.

This narrow categorical skill has finite meaningful variety. The validator exhausts the advertised domains, records distinct mathematical fingerprints, and does not inflate counts using symbols, seeds, option order, bank profiles, or incidental story wording. Observed currency stays one unit pair; other contexts vary named scale labels or independently measured units. Different physical units are compared with exact scale as well as dimensions.
