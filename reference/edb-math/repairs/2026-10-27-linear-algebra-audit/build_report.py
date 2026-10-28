import collections,json,re
from pathlib import Path
H=Path(__file__).resolve().parent
names=['flagged','group-1','group-2','group-3','group-3/checkbox-repair'];changes=[];commits=[];publications=[]
for name in names:
 changes +=json.loads((H/name/'approved-proposals.json').read_text());commits.append({'batch':name,**json.loads((H/name/'verification.json').read_text())});publications+=json.loads((H/name/'generator-publications.json').read_text())
assert len(changes)==1028 and len(publications)==21
verify=json.loads((H/'final-verification.json').read_text());assert verify['passed']
summary={'scope_basis_t':9047,'topics':38,'question_examples':2306,'practice_questions':2195,'canonical_examples':111,'tutorials':85,'direct_source_question_identities':1185,'source_identified_questions_without_retained_original':579,'generated_questions_without_original_identity':542,'content_and_key_attribute_changes':len(changes),'changed_attribute_entities':len({x['entity']for x in changes}),'changes_by_attribute':dict(collections.Counter(x['attribute']for x in changes)),'authored_missing_solutions':59,'existing_owned_correct_links_completed':61,'duplicate_field_memberships_detached':1,'published_replacement_generators':len(publications),'stored_aligned_prefix_fields_repaired':167,'focused_regression_tests':80,'commits':commits,'duplicate_repair':json.loads((H/'duplicate-field/verification.json').read_text()),'final_verification':verify,'unresolved':[{'question':17592186125167,'source':'q-47586','issue':'Existing bank lacks III only under the standard empty-basis convention; retained source wording is mathematically misleading. No arbitrary key or bank mutation.'}],'source_coverage_limit':'Every scoped record received formatting/render/field review. Exact original-source comparison is limited to retained evidence; generator sampling and targeted independent math checks are not a proof over every possible instance.'}
(H/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
lines=['# Linear algebra import and formatting audit','',f'Completed the requested38-topic audit at captured basis T9047:2,306 question/example records (2,195 practice questions and111 canonical examples) plus85 tutorials. Three agents handled disjoint topic groups; the parent independently repaired the flagged multiplication family and integrated all transactions.','',
'## Results','',
'- Committed1,028 reviewed content/key attribute changes across798 entities, plus one duplicate field-membership retraction. Every batch has native preview, stable request/receipt evidence, exact datom verification and database readback.',
'- Repaired32 tutorial fields,306 problem statements,464 worked-solution fields,108 radio-answer display values and57 checkbox statement labels. Completed61 existing-answer key links and authored59 missing worked solutions. Answer values changed only for reviewed source display notation; existing answer IDs and bank memberships remain intact.',
'- Replaced21 immutable generator packages and verified their registered references. Changes preserve supported mathematical families and answer banks while repairing instructional styling, source notation, layout, or content identities. No generated question records were inserted by the publication batches.',
'- Preserved existing question, field and answer UUIDs and learner history. Detached one redundant radio field from q-42156 while retaining the field, its five choices and all temporal history; reverse-reference review found no learner/task usage.',
'- Added common importer preservation of scoped colors, backgrounds and vector/basis/domain fonts. Added formatter validation/normalization and a UI guard for visible bracketed labels consumed as aligned placement options.80 focused regressions pass.',
'', '## Your flagged multiplication questions','',
'Question17592186642471 was generated. Its generator used plain operand matrices at every stage, losing the row/column focus demonstrated by tutorial17592186101959. Question17592186602424 (q-129497) is source-derived and used a wide imported alignment. Its original capture is unavailable, so its new presentation is documented as an authored repair following the tutorial, rather than a claim of recovered original colors. Both are mathematically correct and now show the active blue row, red column and boxed result entry, with explicit row/column captions and mobile line wrapping. The same convention was applied throughout the conformable-product KP; its generator is replaced.',
'', '## Root causes','',
'Older extraction paths discarded meaningful MathML/font annotations, flattened matrix input tables, or turned visible set braces into TeX grouping braces. Generators then reused incomplete imported templates or built fresh solutions from unstyled matrix/vector constructors. Separately, MathJax silently swallows an initial `[A | I]` after `\\begin{aligned}` as an optional placement argument;167 stored fields needed explicit protection. A third class consists of original source arithmetic/transcription errors: source agreement alone did not validate intermediate matrices or row-operation annotations.',
'', '## Validation and limits','',
'All scoped content and checkbox statement labels were checked with the actual Markdown/MathJax renderer. Changed matrix controls were checked for cell/field mapping and mobile layout; the flagged product solutions and representative source/proposed tutorials were visually inspected. Native grading uses the application engine without creating learner attempts. Independent checks cover source given matrices, targeted products/powers/determinants, Gaussian and inverse intermediate matrices, row-operation annotations, and every authored completion; individual group reports state parser and sampling limits.',
'',
'Original source evidence survives for1,185 question identities and all85 tutorials. Another579 source-identified questions lack a retained original;542 generated questions have no original-source identity. They received structural/render/field review and applicable independent checks, but cannot be certified as exact original-source matches. Inventories and per-group missing-source ledgers make this explicit.',
'',
'**Unresolved:** question17592186125167 (q-47586) has no existing choice matching “III only” under the standard empty-basis convention. Its original statement “Null(A) has no basis” is misleading when Null(A)={0}. The bank and key remain unchanged rather than assigning an incorrect answer. All other active answer fields in scope are keyed after the repairs.',
'', '## Evidence','',
'- `summary.json` and `final-verification.json`: totals, exact final inventory/identity/key verification and commit bases.',
'- `flagged/README.md`: detailed multiplication diagnosis, source distinction and mobile screenshots.',
'- `group-1/README.md`, `group-2/README.md`, `group-3/README.md`: source comparisons, mathematical checks, render/grading results and limitations.',
'- `group-3/checkbox-label-validation-report.json`: all476 checkbox labels and22 additional notation repairs.',
'- Each batch has `approved-proposals.json`, `transaction.edn`, `commit-intent.json`, `receipt.edn`, `verification.json` and exact readback files.',
'- Each generator publication has immutable package/digest evidence, preparation, stable-request receipts and registration readback. A stale speculative preparation was archived and refreshed only before a pending request existed.',
'', '## Requested topics','', '| Entity | Source topic | Lesson |','| --- | --- | --- |']
for t in json.loads((H/'inventory.json').read_text())['topics']:lines.append(f"| {t['entity']} | {t['ma_id']} | {t['title']} |")
report='\n'.join(lines)+'\n'
report=re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[A-Za-z])', ' ', report)
report=re.sub(r':(?=\d)', ': ', report)
(H/'README.md').write_text(report);print('Report written:',len(changes),'attribute changes;',len(publications),'generators.')
