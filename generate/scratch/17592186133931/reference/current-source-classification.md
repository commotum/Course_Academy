# Current evidence — math basis 2723

Lineage: `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The exact current KP pull is retained in `initial/kp.edn`. This supplements the frozen basis-1356 extraction without rewriting captured source evidence.

The live pool has 13 source questions, all moderate: twelve five-choice scalar math radios and one context-dependent integrand math blank. The original ten full-flux families remain supported by the existing generator. The previously incomplete `q-162412` now has a moderate label, correct answer 2, and a complete solution; all live facts are preserved. The incomplete preceding premise for blank `q-168617` remains unresolved, so that question is excluded from our validated reserve.

Two added source families have no plots:

| Source entity | Pattern and supplied data | Stages and answer bank |
|---|---|---|
| 17592186537908 (`q-162603`) | Outward rectangular-box flux, F=(y sqrt(x), z-x, y³), x in [1,4], y in [0,1], z in [1,2]. Positive x keeps all partials continuous. | Three held partials yield y/(2 sqrt(x)); three separated integrals; sqrt(x), y²/2 and width endpoints; flux 1/2. Bank: 5/2, 4, 3/2, 3, 1/2 (correct). |
| 17592186537916 (`q-162598`) | Outward rectangular-box flux, F=(z³, 2xz cos(y), xy²), x in [0,1], y in [0,pi], z in [2,4]. | Three held partials yield -2xz sin(y); separate 2x, -sin(y), z; primitives x², cos(y), z²/2; endpoints 1, -2, 6; flux -12. Bank: 6, -12 (correct), -6, -8, 16. |

Both originals have been independently differentiated, integrated, and checked against their keys, every integration equation stage, and actual learner grading. They count as original practice if fresh and unreserved. Their new field/solution families and source banks remain outside normal generation: the source-bank intentions cannot be established from one scalar bank. This is a bounded variant-family capability exception, not an unsupported moderate level and not a claim that these banks have parameterized replay. No new distractor profile is invented for them. Their exact raw values and worked solutions are retained in `initial/kp.edn`, with audit records in `current-source-audit.json`.

The existing validated sampler provides 32 easy, 4,715 moderate, and 100 hard semantic tasks. Easy and hard retain their documented authored tutorial/canonical anchors and fixed workloads. No plot renderer is required. The source solution for repaired q-162412 groups its final endpoint arithmetic differently from the frozen generator; the live-source audit evaluates those equations directly rather than requiring the old row layout. These source differences do not change the generator's supported structures or identities.
