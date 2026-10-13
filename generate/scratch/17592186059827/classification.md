# Classification

Database math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Exact title: **Translating Between Half-Open Intervals and Inequalities**. The capture has two practice questions, neither rated. Neither contains a correct lookup ref or worked solution. Each has one `selection` radio field and five math choices. No fields are missing or duplicated. Radio prompts require no placeholder. The canonical example is teaching context and is not counted as practice coverage.

| Source | Template | Bank profile | Original rating | Authored replay assignment | Plot |
|---|---|---|---|---|---|
| q-1253 | inequality_to_interval | observed_1253_raw | absent | easy | none |
| q-25754 | interval_to_inequality | observed_25754_raw | absent | hard | none |

There are two observed prompt/value families, two observed complete bank profiles, and zero observed rated families at any level. Every generated level is an authored design claim. All levels retain the same two endpoint-inclusion decisions and radio layout. Easy uses nonnegative integer bounds; moderate uses a negative lower bound and rational bounds with a noninteger present; hard uses a negative lower bound and at least one irrational square-root bound. These are independent same-skill instances, without solving inequalities or algebraically simplifying surds. Neither translating to a graph nor a union/unbounded interval is added.

The actual linked lesson route is 60770 Introduction → 60782 Closed Intervals tutorial → 60771 open interval KP59826 → 60775 closed interval KP59829 → 60772 Half-Open tutorial → 60773 this KP59827 → 60774 number-line KP59828. This order follows first-step/next rather than Pull collection order. The earlier open KP provides the strict-comparison/parenthesis correspondence, and the preceding half-open tutorial adds the independent included endpoint. The canonical example uses `(-4,sqrt(2)]`, so signed surds are already within this KP. Topic prerequisites are Compound Inequalities (2310), Surds (2204), and Simplifying Expressions With Surds (3709). They support rational/surd reading; they do not justify adding algebraic inequality solving. Number-line translation belongs to sibling59828 and is excluded.

The original local MA lesson `/home/jake/Developer/MA/DATA/Lessons/239/Source/239.json` confirms both multiple-choice widgets, five choices each, their prompts and equivalent complete banks; it contains no key or worked solution for these questions either. Relevant excerpts are saved in authoritative-widget.json. No plot assets occur in either practice item or this canonical example. Lesson tutorial graphs belong to context only; no extraction/rendering is required for this generator.

Source omissions are preserved by public raw profiles, not hidden by replacing captured data. Normal profiles add an independently established key and authored canonical-anchored worked solution plus an authored rating. Observed key and solution fidelity denominators are both zero; preservation of their absence is separately tested 2/2. Source answer/field UUIDs and nested enum maps are converted to the documented local review representation; identifiers are generated deterministically and field-owned. No database writes occur.

Completed observed profiles obey the same authored level bounds as defaults and explicit inputs. Only raw unrated evidence may replay an endpoint form outside a requested level, because it carries no difficulty label or learning eligibility.
