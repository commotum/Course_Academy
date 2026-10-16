from pathlib import Path
import collections,json,importlib.util,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('source_audit',HERE/'audit.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
rows=json.loads((HERE/'matches.json').read_text());lessons=json.loads((HERE/'affected-lessons.json').read_text());summary=json.loads((HERE/'comparison-summary.json').read_text())
strict=[r for r in rows if r['reason']=='missing_matrices' and len(a.current_matrices(r['currentText']))==1 and len(r['sourceMatrices'])>1]
(HERE/'first-matrix-only.json').write_text(json.dumps(strict,indent=2))
bylesson=collections.defaultdict(list)
for row in strict:bylesson[(row['lessonId'],row['lessonTitle'])].append(row)
repaired={17592186088890,17592186087503}
rootcause=Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py')
lines=['# Compound-math import-loss audit — October 15, 2026','',
'Original lesson HTML preserves complete compound equations, but the legacy extractor often selected only the first nested MathML fragment. This can remove matrix operands, names, operators, or most of a non-matrix formula. The issue precedes the current Markdown renderer.','',
f'Scanned **{summary["sourceFilesScanned"]:,} original lesson HTML captures**. Found {summary["sourceCandidates"]:,} candidate formula occurrences across {summary["candidateLessons"]} lessons, and read {summary["currentRecordsRead"]:,} matching current database records at **EDB basis 2832**. No source scan errors occurred.','',
'## Direct first-matrix-only losses','',
f'**{len(strict)} content attributes in {len(bylesson)} lessons** have the same particularly clear signature as the reported examples: the original formula contains multiple matrices, while the corresponding current problem/tutorial/solution contains only one matrix, matching the first source matrix. This is a conservative subset of the broader results, not a complete list of all import damage.','',
'| Lesson | Source topic | Affected attributes | Database entities | Original source evidence |','| --- | ---: | ---: | --- | --- |']
for (topic,title),items in sorted(bylesson.items(),key=lambda item:item[0][1]):
 first=items[0];entities=', '.join('`'+str(e)+'`' for e in sorted({r['entity'] for r in items}))
 source=f'[{first["domId"]}]({first["sourceFile"]}:{first["line"]})'
 lines.append(f'| {title} | {topic} | {len(items)} | {entities} | {source} |')
lines+=['','[Detailed first-matrix-only evidence](first-matrix-only.json) records the original matrices, missing matrices and labels, source lines, current text, and exact database entity/attribute.','',
'## Broader source-loss matches','',
f'The automated comparison flagged **{summary["patternMatchedAttributes"]} attributes in {summary["patternMatchedEntities"]} content records across {summary["patternMatchedLessons"]} lessons**. These matches include the direct cases above. Treat the full list as a review queue: formula normalization and later content revisions can require judgment. The audit does not claim that every broader match has been manually checked.','',
'| Signature | Matched attributes |','| --- | ---: |',
f'| Source matrices absent from the current attribute | {summary["reasons"]["missing_matrices"]} |',
f'| Matrix values found, but source assignment labels absent | {summary["reasons"]["missing_matrix_labels"]} |',
f'| An isolated first MathML fragment appears instead of the complete compound formula | {summary["reasons"]["truncated_compound_formula"]} |','',
'Non-matrix spot checks confirm the same loss mechanism:','',
'- **Directrices of Ellipses** (`17592186093469`): the complete focus/directrix set definition became a display containing only `P`.',
'- **Solving Geometric Series Problems Using Exponential Equations and Inequalities** (`17592186093398`): the underbraced sum inequality became only `N`.',
'- **Multiplying Two-Digit Decimals** (`17592186056062`): the annotated decimal placement example became only `2`.','',
f'Another **{summary["candidateOccurrencesNeedingReview"]:,} source formula occurrences** could not be confidently compared automatically. Unsupported MathML and legitimate rendering differences stay in [needs-review.json](needs-review.json). The scan also identified {summary["candidateOccurrencesAlreadyComplete"]} candidate occurrences whose required matrices/formulas were already present. A clean result for a particular occurrence does not certify the entire lesson.','',
'## Reported items repaired during this session','',
'| Reported entity | Content changed | Result |','| --- | --- | --- |',
'| `17592186100992` | Canonical example `17592186100687`, MA e-4379 | Restored A/B/C definitions from the source; verified at basis 2831. |',
'| `17592186088890` | Tutorial 2982 | Restored the missing 2×2 zero matrix and 3×3 square matrix. |',
'| `17592186087696` | Canonical example `17592186087503`, MA e-4391 | Restored U/W/Z definitions from the source. |',
'| `17592186403293` | Question q-68727 | Stacked W/X/Y vertically; matrix values preserved. |','',
'The last three text repairs committed together at **basis 2843**, after the audit snapshot. Therefore, two content records in the snapshot’s match list are now repaired (`17592186088890` and `17592186087503`). The remaining snapshot queue has 363 records / 366 matched attributes across the same 201 lessons. No answer entities, field identities, grades, attempts, XP, or learner history were changed. Nine live-app DOM checks at 893, 375, and 320px verified the three reported repairs, without screenshots or learner submissions.','',
'## Cause and scope','',
f'The legacy [extract_math_from_node()]({rootcause}:532) calls `node.find("mjx-assistive-mml")`, finds the first descendant, and returns its MathML before reading the outer SVG title. In a title such as `A = [matrix], B = [matrix]`, that descendant represents only the first matrix. The outer equation still exists in the original HTML.','',
'This audit targets that specific import failure. It does not certify unrelated Markdown tables, image extraction, blank placement, or every possible equation conversion. It also does not apply an unreviewed bulk rewrite to the broader match list. Original source files remain unchanged.','',
'## All lessons with automated matches','',
'The following counts are matched attributes, not counts of questions. Tutorial content and worked solutions can also be affected. Entity IDs support direct review in the app.','',
'| Lesson | Source topic | Matched attributes | Content entity IDs |','| --- | ---: | ---: | --- |']
for lesson in sorted(lessons,key=lambda l:l['title']):
 entities=', '.join('`'+str(e)+'`'+(' (repaired)' if e in repaired else '') for e in lesson['entities'])
 lines.append(f'| {lesson["title"]} | {lesson["id"]} | {lesson["affectedAttributes"]} | {entities} |')
lines+=['','Machine-readable evidence: [matches](matches.json), [lesson index](affected-lessons.json), [source candidates](source-candidates.json), [scan summary](scan-summary.json), [comparison summary](comparison-summary.json). All database projections and source/input query templates are retained alongside this report.','']
(HERE/'README.md').write_text('\n'.join(lines))
summary.update({'directFirstMatrixOnlyAttributes':len(strict),'directFirstMatrixOnlyLessons':len(bylesson),'reportedRepairsAtBasis':2843,'remainingMatchedRecordsAfterReportedRepairs':363,'remainingMatchedAttributesAfterReportedRepairs':366})
(HERE/'comparison-summary.json').write_text(json.dumps(summary,indent=2))
print('Report:',HERE/'README.md');print('Direct matrix-loss lessons:',len(bylesson),'broader matched lessons:',len(lessons))
