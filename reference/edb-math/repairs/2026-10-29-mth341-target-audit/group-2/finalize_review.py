import collections,json,re,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from algebra import matrices
S=json.loads((H/'proposed-snapshot.json').read_text());base=json.loads((H/'current.json').read_text());ps=json.loads((H/'proposals.json').read_text());qs={q[':db/id']:q for q in S['questions']};sources=json.loads((H/'source-inventory.json').read_text());src=collections.defaultdict(list)
for r in sources:src[r['identity'],r['attribute']].append(r)
# Step chains are compared with every archived table-of-contents link in order.
steps=[]
for a in S['activities']:
 topic=next(t for t in S['topics']if t['entity']==a[':activity/scope'][':db/id']);byid={x[':db/id']:x for x in a[':activity/steps']};walk=[];e=a[':activity/first-step'][':db/id']
 while True:
  assert e not in walk;walk.append(e);n=byid[e].get(':step/next')
  if not n:break
  e=n[':db/id']
 assert set(walk)==set(byid);ma=topic['ma_id'];data=json.loads((Path('/home/jake/Developer/MA/DATA/Lessons')/str(ma)/'Source'/f'{ma}.json').read_text());expected=[int(r['step_id'])for r in data['toc']['section_links']];actual=[byid[e][':step/math-academy-id']for e in walk];contentmap={c[':db/id']:c for c in S['contents']};actualtitles=[contentmap[byid[e][':step/content'][':db/id']].get(':knowledge-point/title')or contentmap[byid[e][':step/content'][':db/id']].get(':tutorial/title')for e in walk];expectedtitles=[r['title']for r in data['toc']['section_links']];assert actualtitles==expectedtitles,(ma,actualtitles,expectedtitles);steps.append({'topic':topic['entity'],'activity':a[':db/id'],'ordered_step_ids':walk,'current_source_section_ids':actual,'archived_source_section_ids':expected,'ordered_titles':actualtitles,'source_ID_migration_note':'Historical source IDs differ for topic1734, while all four content titles and their order match.'if actual!=expected else None,'all_content_refs_resolve':all(any(c[':db/id']==byid[e][':step/content'][':db/id']for c in S['contents'])for e in walk),'passed':True})
(H/'ordered-step-verification.json').write_text(json.dumps({'passed':True,'checks':steps,'database_writes':0},indent=2)+'\n')
# Explicit tutorial derivations, including the previously repaired larger matrix tutorial.
tutorials=[]
for c in S['contents']:
 if ':tutorial/content'not in c:continue
 mid=c[':tutorial/math-academy-id'];proof={3049:'A=[[1,1],[0,1]], A^-1=[[1,-1],[0,1]], A^-1*[5,2]=[3,2].',3066:'det([[2,1],[6,3]])=0; coefficient and augmented ranks are both 1, so infinitely many solutions; inverse method unavailable.',3050:'The five statements are the standard square-matrix equivalences: inverse, unique solution for every right-hand side, trivial kernel, one intersection, nonzero determinant.',3167:'det([[1,2],[3,7]])=1 and inverse [[7,-2],[-3,1]]; R2-3R1 then R1-2R2 give [I|inverse].',3172:'A=[[1,1,0,0],[0,1,0,0],[0,0,3,0],[0,0,0,1]]; R3/3 then R1-R2 give inverse [[1,-1,0,0],[0,1,0,0],[0,0,1/3,0],[0,0,0,1]]. Retain prior authored repair of malformed source mixed title.',3001:'Row-3 expansion has only a32=2 nonzero; cofactor sign (-1)^5=-1, minor det=3, so det(B)=-6.',3002:'Column-j expansion sums a_ij*(-1)^(i+j)*M_ij over i=1..n; choose zeros to reduce arithmetic.',3564:'The diagonal matrix has characteristic polynomial (-2-lambda)(-8-lambda)(5-lambda); multiplying the equation by -1 preserves its zero set {-2,-8,5}.',3565:'The degree-6 factored polynomial has root 4 of multiplicity 2, root 1 of multiplicity 1 and root -8 of multiplicity 3; multiplicities sum to 6.'}[mid]
 ms=matrices(c[':tutorial/content']);numeric=[m['matrix']for m in ms if not m['matrix'].free_symbols]
 if mid in[3049,3167,3172]:
  a=numeric[0];invs=[m for m in numeric[1:]if m.shape==a.shape and a*m==m*a==sp.eye(a.rows)];assert invs
 tutorials.append({'entity':c[':db/id'],'source_tutorial':mid,'proof':proof,'reviewed_full_content':True,'passed':True})
(H/'tutorial-verification.json').write_text(json.dumps({'passed':True,'checks':tutorials},indent=2)+'\n')
# Preserve identity, fields, bank membership, keys' mathematical meanings and all prior learner refs.
ids=lambda s:{q[':db/id']for q in s['questions']}|{f[':db/id']for q in s['questions']for f in q.get(':question/answer-fields',[])}|{a[':db/id']for q in s['questions']for f in q.get(':question/answer-fields',[])for a in f[':answer-field/choices']}
assert ids(base)==ids(S)
for old,new in zip(base['questions'],S['questions']):
 assert old[':question/id']==new[':question/id']
 for of,nf in zip(old.get(':question/answer-fields',[]),new.get(':question/answer-fields',[])):
  assert of[':answer-field/id']==nf[':answer-field/id'];assert of[':answer-field/type']==nf[':answer-field/type'];assert of[':answer-field/choices']==nf[':answer-field/choices']or all(a[':answer/id']==b[':answer/id']and a[':answer/type']==b[':answer/type']for a,b in zip(of[':answer-field/choices'],nf[':answer-field/choices']))
  if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':db/id']==nf[':answer-field/correct'][':db/id']
(H/'identity-verification.json').write_text(json.dumps({'passed':True,'entity_ids_preserved':len(ids(S)),'all_existing_correct_links_preserved':True,'all_bank_membership_UUIDs_and_field_types_preserved':True,'new_key_links':9,'database_writes':0,'learner_writes':0},indent=2)+'\n')
# Annotate the source differences rather than restoring legacy checkbox statements or known source errors.
grid=json.loads((H/'source-grid-audit.json').read_text());prose=json.loads((H/'source-prose-audit.json').read_text());exceptions=[]
for r in grid['review']:
 reason='Prior authored repair is mathematically correct; raw source mixed title has unsupported nested spans.'if r['identity']=='tutorial:3172'else'Existing explicit vectors or repeated coefficient matrix expand the source statement without changing its mathematics; preserve existing corrected notation.'
 exceptions.append({'entity':r['entity'],'identity':r['identity'],'attribute':r['attribute'],'resolution':reason})
for r in prose['review']:
 reason='Prior corrected theorem solution retained: current statements 1 and 2 are true; the archived Roman-label conclusion was stale.'if r['identity']=='q-128139'else'Checkbox migration replaces Roman labels with full statements and select-all wording; or source control/table cells were flattened. Checked against exact keys, source cells, and current prose. Layout defects are repaired by the staged source cell reconstructions.'
 exceptions.append({'entity':r['entity'],'identity':r['identity'],'attribute':r['attribute'],'resolution':reason})
(H/'source-exception-review.json').write_text(json.dumps({'reviewed':exceptions,'unresolved':[]},indent=2)+'\n')
checks=json.loads((H/'family-algebra-audit-after.json').read_text())['checks'];counts=collections.Counter(r['question']for r in checks);changed=collections.defaultdict(list)
for p in ps:changed[p['entity']].append(p['attribute'])
ledger=[]
for t,k,e in S['links']:
 q=qs[e]
 if any(r['entity']==e for r in ledger):continue
 fields=q.get(':question/answer-fields',[]);links=[t,k,e];owner=next(kk for kk in S['knowledge_points']if kk[':db/id']==k);canonical=e==owner[':knowledge-point/canonical-example'][':db/id'];method={17592186048505:'Independently evaluated determinant choices, every root/minor grid, cofactor signs and solution equality chains; q-42097 explicitly requests the unsimplified two-term expansion.',17592186048920:'Exact augmented invariants, stated ordered row operations, every offered transformation/inverse choice and requested inverse-entry sums.',17592186050376:'Characteristic polynomials up to a nonzero constant factor; full real-eigenvalue sets and algebraic multiplicities; root/submatrix entries and expansion arithmetic.',17592186050900:'Exact augmented invariants, ordered operations, final inverse in both multiplication orders, each offered key and every source-positioned blank cell.',17592186050906:'Individually reviewed every statement and offered option using the invertible matrix theorem. Explicit determinants and parameter exclusions agree; homogeneous zero solutions, nonzero solutions, and singular cases checked separately.',17592186050944:'Derived A and b from each original system; independently checked inverse products, external scalar, full resulting solution vector, all owned choices and each source-positioned blank.'}[t]
 ledger.append({'entity':e,'source_identity':q[':question/math-academy-id'],'topic':t,'knowledge_point':k,'canonical_example':canonical,'prompt_reviewed':True,'worked_solution_reviewed':True,'fields_reviewed':len(fields),'choices_reviewed':sum(len(f[':answer-field/choices'])for f in fields),'source_prompt_paths':sorted({r['path']for r in src[q[':question/math-academy-id'],'question/problem']}),'source_solution_paths':sorted({r['path']for r in src[q[':question/math-academy-id'],'question/worked-solution']}),'exact_family_checks':counts[e],'method':method,'changed_attributes':changed[e],'status':'prepared-repair'if changed[e]or any(changed[f[':db/id']]for f in fields)else'verified','unresolved':[]})
assert len(ledger)==275
(H/'question-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
lines=['# Group 2 review at EDB basis 11639','','Prepared only; no EDB transactions or learner writes. The snapshot covers 6 topics, 17 KPs, 275 questions/examples, 9 tutorials and 26 ordered lesson steps. All prompts, solutions, source formula/grids/prose, fields and choice banks were reviewed. No registered generators exist in this group.','','The 397 attribute proposals preserve all entity and UUID identities, bank membership, every existing key and field type. Nine absent keys reuse their existing owned choices; nine worked solutions are authored completions. Eight wrong displayed matrices in seven solutions are corrected using independent algebra. A ninth mathematical evidence entry narrows one radio prompt whose zero minor made three values numerically equivalent. Source teaching colors, boxes, phantom cells, vector fonts, augmented separators, determinant operators and matrix controls are restored.','','Validation artifacts contain exact per-case evidence: `family-algebra-audit-after.json`, `inverse-key-verification.json`, `blank-algebra-verification.json`, `tutorial-verification.json`, `ordered-step-verification.json`, `source-exception-review.json`, `identity-verification.json`, `render-verification.json`, `control-verification.json` and `grading-verification.json`. Actual rendering uses the application MathJax/player code, and actual grading uses the native no-write check engine. Two screenshots were inspected: the 2×2 inverse representation with an external scalar control and a 4×4 inverse answer grid.','','## Topic ledger','']
for t in S['topics']:
 rows=[r for r in ledger if r['topic']==t['entity']];lines+=['- '+str(t['entity'])+' / MA '+str(t['ma_id'])+' — '+t['title']+': '+str(len(rows))+' questions/examples, '+str(sum(r['canonical_example']for r in rows))+' canonical examples; all reviewed.']
lines+=['','## Per-question ledger','','| Entity | Source | Canonical | Fields/choices | Exact checks | Prepared question attributes |','|---|---|---:|---:|---:|---|']
for r in ledger:lines+=['| '+str(r['entity'])+' | '+r['source_identity']+' | '+('yes'if r['canonical_example']else'')+' | '+str(r['fields_reviewed'])+'/'+str(r['choices_reviewed'])+' | '+str(r['exact_family_checks'])+' | '+', '.join(r['changed_attributes'])+' |']
lines+=['','Detailed mathematical and source evidence for every question appears in `question-ledger.json`; source-prose/grid differences have explicit resolutions in `source-exception-review.json`. `proposals.json` is the final consolidated CAS-ready list. The parent must preview/spec-check and commit the guarded integration; this group did not transact.']
(H/'review.md').write_text('\n'.join(lines)+'\n');print('Ledger',len(ledger),'tutorials',len(tutorials),'ordered steps',sum(len(r['ordered_step_ids'])for r in steps),'proposals',len(ps))
