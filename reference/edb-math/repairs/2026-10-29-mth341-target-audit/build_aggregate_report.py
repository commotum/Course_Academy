"""Build review documentation only; no database access or mutations."""
import json,collections
from pathlib import Path
H=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text())
inv=read(H/'inventory.json');skip=read(H/'skip-coverage-verification.json');skipby={x['topic']:x for x in skip['checks']};groups={};topicgroups={};ownership={};allproposals=[];classification=[]
for name in['group-1','group-2','group-3']:
 D=H/name;s=read(D/'current.json');ps=read(D/'proposals.json');groups[name]={'snapshot':s,'proposals':ps,'commit':read(H/('commit-'+name)/'verification.json')}
 for t in s['topics']:topicgroups[t['entity']]=name
 for t,k,q in s['links']:ownership[q]=t
 for q in s['questions']:
  tid=ownership[q[':db/id']]
  for f in q.get(':question/answer-fields',[]):
   ownership[f[':db/id']]=tid
   for a in f[':answer-field/choices']:ownership[a[':db/id']]=tid
 for t,a,st,c in s['steps']:ownership[c]=t
 for p in ps:allproposals.append({'group':name,**p})
# Disjoint precedence: authored completion, source-error correction, source-math restoration,
# then source/presentation/control restoration. A field may also carry typography changes.
completion=set();source_error=set();math_restore=set();evidence={}
for name,g in groups.items():
 for p in g['proposals']:
  key=(p['entity'],p['attribute'])
  if p['before']is None and p['attribute']in['answer-field/correct','question/worked-solution']:completion.add(key)
for p in read(H/'group-1/mathematical-corrections.json'):source_error.add((p['entity'],p['attribute']))
for p in read(H/'group-1/scalar-versus-set-restorations.json'):
 key=(p['entity'],p['attribute']);math_restore.add(key);source_error.discard(key)
for e in read(H/'group-2/mathematical-correction-evidence.json'):source_error.add((e['question'],'question/problem'if e['question']==17592186370926 else'question/worked-solution'))
for eid in[17592186304926,17592186660905]:
 for a in['question/problem','question/worked-solution']:source_error.add((eid,a))
for eid in[17592186193876,17592186205256]:source_error.add((eid,'tutorial/content'))
for eid in[17592186204221,17592186204222,17592186204223]:math_restore.add((eid,'question/problem'))
word=read(H/'group-3-wording-delta/proposals.json');wordkeys={(p['entity'],p['attribute'])for p in word};source_error.update(wordkeys)
final_attributes=allproposals+ [{'group':'group-3',**p}for p in word if (p['entity'],p['attribute'])not in{(x['entity'],x['attribute'])for x in allproposals}]
assert len(final_attributes)==1339
for p in final_attributes:
 key=(p['entity'],p['attribute']);cat='authored-completion'if key in completion else'authored-source-mathematical-correction'if key in source_error else'source-mathematics-restoration'if key in math_restore else'source-presentation-and-control-restoration';classification.append({'group':p['group'],'entity':p['entity'],'attribute':p['attribute'],'category':cat,'also_has_later_wording_delta':key in wordkeys})
assert len(allproposals)==1338 and len({(p['entity'],p['attribute'])for p in allproposals})==1338
counts=collections.Counter(r['category']for r in classification);assert counts=={'authored-completion':68,'authored-source-mathematical-correction':35,'source-mathematics-restoration':6,'source-presentation-and-control-restoration':1230},counts
ledger=[]
for t in inv['topics']:
 eid=t[':db/id'];decision=next(d for d in inv['decisions']if d['topic']==eid);ids=sorted({q for tt,k,q in inv['links']if tt==eid});g=topicgroups.get(eid);row={'topic':eid,'title':t[':topic/title'],'source_topic':t[':topic/math-academy-id'],'questions_examples':len(ids),'knowledge_points':len(t[':topic/knowledge-points']),'question_ids':ids,'review_basis_t':11639,'prior_completed_audits':decision['prior_completed_audits'],'scope_decision_reasons':decision['reasons']}
 if g:
  commit=groups[g]['commit'];ps=[p for p in allproposals if ownership[p['entity']]==eid];row.update(action='fresh-full-review',group=g,content_status='committed-and-exact-readback-verified',content_commit_basis_t=commit['basis_t'],primary_attribute_changes=len(ps),final_change_categories=dict(collections.Counter(r['category']for r in classification if ownership[r['entity']]==eid)),report=g+'/review.md',individual_question_ledger=g+('/question-source-review-ledger.json'if g=='group-1'else'/review.md'if g=='group-2'else'/review-ledger.json'),final_global_verification='pending')
 else:
  prev=skipby[eid];row.update(action='reuse-prior-completed-full-review',coverage_status='prior-completion-evidence-and-unchanged-question-pool-verified',pool_comparison=prev,report=str(Path(prev['prior_audit'])/next(a['report']for a in decision['prior_completed_audits']if a['directory']==prev['prior_audit'])),full_topic_reaudited_this_run=False)
 if eid==17592186050178:row['narrow_delta']={'question':17592186106149,'identity':'q-20966','type':'duplicate-radio-control ownership repair only','basis_t':11658,'active_field':17592186401847,'retained_detached_field':17592186102770,'proof':'skipped-delta/proof.json','native_grading':'skipped-delta/grading-verification.json','rendering':'skipped-delta/render-verification.json','controls':'skipped-delta/control-verification.json','original_solution_and_choices_unchanged':True}
 if g=='group-3':row['later_wording_delta_basis_t']=11666 if any(ownership[e]==eid for e,a in wordkeys)else None
 ledger.append(row)
assert len(ledger)==50 and sum(r['action']=='fresh-full-review'for r in ledger)==19
final=H/'final-live-verification.json';global_status=read(final)if final.exists()else None
if global_status and global_status.get('passed'):
 for r in ledger:
  if r['action']=='fresh-full-review':r['final_global_verification']={'passed':True,'path':'final-live-verification.json','basis_t':global_status.get('basis_t')}
summary={'scope_basis_t':11639,'requested_topics':50,'freshly_reviewed_topics':19,'reused_completed_topics':31,'fresh_questions_examples':944,'reused_questions_examples':1938,'all_requested_questions_examples':2882,'fresh_tutorials':35,'fresh_ordered_steps':94,'primary_scalar_writes':1338,'wording_followup_scalar_writes':4,'distinct_final_changed_attributes':1339,'duplicate_membership_retractions':5,'classification_by_distinct_final_attribute':dict(counts),'source_identified_fresh_records':905,'archived_source_found':904,'missing_original_prompt':['q-105109'],'generated_fresh_records_without_MA_source':39,'commit_bases':{'duplicates':11658,'group-2':11662,'group-3':11663,'group-1':11664,'generator_successor':11665,'exterior_wording':11666},'global_final_verification':global_status or'pending','authored_correction_protection':read(H/'reconciliation-protection-verification.json')if(H/'reconciliation-protection-verification.json').exists()else{'registry':read(H/'authored-reconciliation-verification.json'),'tutorial_guard':'tutorial-source-guard-verification.json','actual_question_importer_smoke':'pending parent'}}
(H/'topic-coverage-ledger.json').write_text(json.dumps({'summary':summary,'topics':ledger},indent=2)+'\n');(H/'correction-classification-ledger.json').write_text(json.dumps({'classification_precedence':['authored-completion','authored-source-mathematical-correction','source-mathematics-restoration','source-presentation-and-control-restoration'],'distinct_final_attribute_counts':dict(counts),'wording_followups_on_already_changed_attributes':3,'new_attribute_from_wording_followup':1,'entries':classification},indent=2)+'\n')
report='''# MTH 341 target quality pass

The content repairs and generator successor are committed. Nineteen topics received a fresh full review; prior completed reviews were reused for the other 31 after verifying their current question/example pools against the completed audit evidence. One of those 31 also received a narrow duplicate-radio-control repair. **This does not claim a new full review of all 50 topics.**

The fresh review covers **944 questions/examples, 35 tutorials and 94 ordered lesson steps**. The full requested scope contains 2,882 questions/examples. Every one of the 50 topic decisions, its prior evidence or new group report, question IDs and commit status appears in [topic-coverage-ledger.json](topic-coverage-ledger.json).

## What changed

The pass completed **32 missing worked solutions and 36 missing correct links**, reusing existing owned answers. It corrected wrong displayed matrices, cofactor and row-operation signs, scalar-versus-set regressions, ambiguous response forms, geometric plane constraints and cross-product dimensionality. It restored source colors, fonts, boxes, operators, set fences, augmented separators, complete controls and source-equivalent formula layouts. Source diagrams were preserved.

The source-error corrections include a plane question whose original wording admitted two choices, a cross-product question whose source supplied two-dimensional outputs, missing tutorial theorem conditions, and a zero-polynomial degree claim. The four exterior-ellipse explanations were clarified in a separate follow-up: the chosen test point is outside the ellipse and inside the shaded exterior region. These mathematical/editorial corrections are marked as locally authored; they are not claimed to reproduce original Math Academy wording.

There are **1,339 distinct changed attributes**. A disjoint classification, with mathematical changes taking precedence over typography on the same field, is retained in [correction-classification-ledger.json](correction-classification-ledger.json):

| Final attribute category | Count |
|---|---:|
| Authored completions: 32 solutions + 36 correct links | 68 |
| Independently proved source mathematical/explanatory corrections | 35 |
| Mathematical restoration to source: scalar/set choices and × operators | 6 |
| Source presentation, layout and control restoration | 1,230 |

The primary batches wrote 1,338 attributes; the four later wording writes updated three already changed solutions and one previously unchanged canonical solution, giving 1,342 scalar write operations on 1,339 distinct final attributes. Five duplicate question→field links were retracted separately. The detached fields and their 25 answers were retained as entities, and the parent verified zero retained learner-response usage before retraction. Existing active answer banks, valid keys, entity/UUID identities and learner history were preserved except the explicitly evidenced scalar/set source restorations.

## Coverage and verification

| Fresh review | Questions/examples | Evidence |
|---|---:|---|
| Group 1: seven vector-space, span, null-space and theorem topics | 346 | [Review](group-1/review.md), [question ledger](group-1/question-source-review-ledger.json) |
| Group 2: six determinant, inverse and characteristic-equation topics | 275 | [Review and per-question ledger](group-2/review.md) |
| Group 3: six geometric subspace, plane, region and cross-product topics | 323 | [Review](group-3/review.md), [question ledger](group-3/review-ledger.json) |

Independent exact algebra, full choice-bank checks, row-operation transitions, canonical examples, tutorials and geometric constraints support the repairs. Geometry review inspected the complete diagrams, coordinate domains, orientation, shading, and solid/dashed boundary inclusion. Actual rendering used the application's player functions, CSS, MathJax and MathLive. The fresh questions passed **8,496 width/feedback control cases**, with additional focused follow-up cases. Native grading on all **885 gradable fresh questions** accepted 1,370 correct responses and rejected 3,628 wrong responses, with no unresolved checks. Group reports retain the exact fixtures and scope of each check rather than treating rendering or parser success as proof of mathematics.

The parent preserved and decoded **127 distinct source images** in 254 desktop/mobile checks. Group 3's final controls also have zero horizontal/content overflows at 760, 390 and 320 px. The other groups' reports record their own geometry checks and do not claim that every long source formula fits without horizontal scrolling.

For the reused topic *Solving 3×3 Singular Systems of Equations Using Gaussian Elimination*, the new q-20966 delta is limited to its duplicated radio ownership. Its archived source has one five-choice radio widget. Independent affine-solution and full-bank proofs establish `x=-1+y-4z`, with two independent null directions, and preserve the existing key. The projected single-control record passes native grading (one correct/four wrong), seven strict-render fragments and nine control cases. See [proof](skipped-delta/proof.json). The full topic's earlier completed review remains the coverage basis.

## Generator and commit record

One immutable successor repairs five explicit source-replay paths in the recognition generator. It preserves the original script/source/helper evidence bytes, updates changed generated identities, and marks the output as authored source-error repair. Eleven fresh records and the other eleven replay paths remain byte-identical. The installed registered CLI passed the five corrected replays, eleven unchanged fresh outputs, package-byte checks, and rejection of unsupported moderate/hard bands. Four other scoped generator references remained unchanged. The two Group 3 cross-product generators additionally passed 512 all-band samples, independent algebra, relocation comparisons, native grading and actual rendering; no successor was needed for them.

| Confirmed transaction | Basis |
|---|---:|
| Five duplicate ownership retractions | 11658 |
| Group 2 content | 11662 |
| Group 3 content | 11663 |
| Group 1 content | 11664 |
| Immutable generator publication/reference | 11665 |
| Four authored exterior-wording follow-ups | 11666 |

Each content batch has exact readback and exact-reviewed-datom verification in its commit directory. The generator's installed-reference/bytes result is [installed-generator-verification.json](installed-generator-verification.json).

## Limits and remaining verification

Archived originals were found for **904 of 905 source-identified fresh records**. No retained original prompt was found for q-105109; its stored dot-product givens, complete bank and unique answer were independently checked. The other **39 fresh records are generated questions without original Math Academy pages** and were reviewed as authored/generated content. Historical/canonical source selectors include `.exampleExplanation` and hashed history captures.

The 31 reused topics rely on their recorded completed audits and unchanged-pool comparison; their full content was not silently re-reviewed in this run. All 50 topics also received the parent's current structural sweep for missing solutions/keys, owned answers, duplicate keys and mathematical blank types. Numerical parsers and browser checks supplement the individual proofs; they do not establish every theorem or diagram interpretation by themselves. No learner attempts, timing, exposure, XP or progress records were created for testing.

**Final global committed-state verification: PENDING parent verifier.**

**Authored-correction reconciliation/protection verification: PENDING parent verification.**
'''
if global_status and global_status.get('passed'):report=report.replace('**Final global committed-state verification: PENDING parent verifier.**','**Final global committed-state verification: PASSED.** See [final-live-verification.json](final-live-verification.json).')
if(H/'reconciliation-protection-verification.json').exists()and read(H/'reconciliation-protection-verification.json').get('passed'):report=report.replace('**Authored-correction reconciliation/protection verification: PENDING parent verification.**','**Authored-correction reconciliation/protection verification: PASSED.** [Registry](authored-reconciliation-verification.json), [actual importer proof](reconciliation-protection-verification.json), [tutorial source guards](tutorial-source-guard-verification.json).')
else:report=report.replace('**Authored-correction reconciliation/protection verification: PENDING parent verification.**','Authored provenance is registered for62questions (198attribute evidence records), including exact complete-bank guards for the two scalar/set repairs. All18Codex-attributed tutorial changes use the existing separately-attributed source guard; its existing actual pipeline branch test passes. **Actual question-importer smoke verification: PENDING parent.**')
(H/'REPORT.md').write_text(report);(H/'aggregate-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print('Wrote aggregate REPORT.md, 50-topic coverage ledger, and 1339-attribute correction-classification ledger; final verifier/protection status explicit.')
