from review import *
import collections,re
# Exercise actual normalized delivered batch, not merely raw sampler IDs.
rs=json.loads((E/'delivery-batch/accepted.json').read_text());cases=[]
for i,r in enumerate(rs):
 f=r['question'][':question/answer-fields'][0]
 cases.append({'label':'normalized runner batch '+str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native outcomes after actual publisher normalization and deduplication'} for a in f[':answer-field/choices']]})
dump('delivered-grader-input.json',cases)
p=run('delivered-grader-command.json',[R/'generate/runs/current/check-engine',E/'delivered-grader-input.json',E/'delivered-grader-report.json']);print('delivered grader',p.returncode,p.stdout[-400:]);assert p.returncode==0
# Cold output math: compare actual sidecar points with independently substituted expressions.
# Empirical hard control verifies missing-coordinate invariance rather than invented formulas.
rs=json.loads((E/'current-cold_dependency_probe/cold-records.json').read_text());out=[]
for r in rs:
 f=r['question'][':question/answer-fields'][0];rows=[]
 for a in f[':answer-field/choices']:
  d=json.loads(pathlib.Path(a[':answer/value']).with_suffix('.json').read_text());groups=[collections.defaultdict(list),collections.defaultdict(list)]
  for x,y,m in d['points']:groups[0][y].append(m);groups[1][x].append(m)
  dep=['x' if any(max(v)-min(v)>1e-7 for v in groups[0].values()) else '', 'y' if any(max(v)-min(v)>1e-7 for v in groups[1].values()) else ''];both=''.join(dep)=='xy';qual=both==r['generation']['template'].startswith('possible')
  rows.append({'image':a[':answer/value'],'depends':''.join(dep),'key_matches':qual==(a[':answer/id']==f[':answer-field/correct'][1])})
 assert all(a['key_matches'] for a in rows)
 out.append({'seed':r['generation']['seed'],'template':r['generation']['template'],'profile':r['generation']['bank_profile'],'images':rows})
dump('cold-math-results.json',out)
# Check that answer controls cannot expose the solution's guide style.
rs=json.loads((E/'fresh-records.json').read_text())+json.loads((E/'batch-records.json').read_text());guides=[]
for r in rs:
 for a in r['question'][':question/answer-fields'][0][':answer-field/choices']:
  d=json.loads(pathlib.Path(a[':answer/value']).with_suffix('.json').read_text());guides.append({'question_id':r['question'][':question/id'],'answer_id':a[':answer/id'],'guide':d.get('guide'),'bounds':d['bounds'],'point_count':len(d['points'])})
assert not any(x['guide'] for x in guides)
assert all(x['bounds']==[-2,2,-2,2] and x['point_count']==225 for x in guides)
dump('layout-shortcut-results.json',{'checks':guides,'conclusion':'All 115 fresh/batch answer images are unannotated, with identical bounds and point counts. Renderer uses the same constant segment length, color and line width for all choices; solution guides are not choice cues.'})
shutil.copyfile(J/'review-0-policy-2-4c6625aaf57ad834/canonical-source-bank.png',E/'canonical-source-bank.png')
assert (E/'canonical-source-bank.png').read_bytes()==pathlib.Path('/media/jake/SSD/EDB/math/images/3b/3bd19865d2a1bb6bbb40c57112f269b51a3740d01da2c80b81db4eb84c6766f1.png').read_bytes()
dump('scope-report.json',{'basis':'Independent source account and current implementation diff; all default authored fields remain in x+y, product with integer powers 1 or 2, mixed quadratic, exp(xy) families. Hard variants invert the taught invariance decision.','default_response':'single image radio, five alternatives','canonical_adapter':'Exact source composite and solution; four text panel labels because captured structured response/rating are absent. Explicit replay only, authored easy assignment disclosed. No default family replaced.','gap':'q-96477 lacks key, solution and difficulty; its supplied completion is authored, not a replay claim for absent evidence.','conclusion':'No new learner prerequisites, response operations, integration or added workload demonstrated.'})
dump('retained-findings-review.json',{'preflight':json.loads((J/'repair-preflight.json').read_text()),'cold':{'old_fails':'strict-cold-old.json','current_passes':'strict-cold-current.json','author_check_current':'current-cold_dependency_probe.command.json','caveat':'An initial run against an old cache-bearing package failed the expected output-location assertion, not the original dependency. Strict cold comparison explicitly removes cache and reproduces original PermissionError.'},'canonical':{'old_fails':'old-canonical_replay_probe.command.json','current_passes':'current-canonical_replay_probe/canonical-result.json'},'resolved':['2c2cb894f9ccd977b988','ef9fcb18c9498adb4987']})
dump('package-integrity.json',{'unchanged':hashes(W)==json.loads((E/'package-before.json').read_text()),'file_count':len(hashes(W)),'external_writes':'Review scripts and outputs confined to evidence_root; no publishing or database mutation.'})
assert json.loads((E/'package-integrity.json').read_text())['unchanged']
(E/'session-state.md').write_text('All required test stages completed. Source replay includes seven complete practice banks plus exact canonical four-panel replay; missing q-96477 fields distinguished. Both original failures independently reproduced on old code and resolved on current. Fresh/sample/boundary math, native raw and delivered grading, delivery/selection and actual UI passed. Visual screenshots inspected, including canonical. Next: finalize pedagogical report and result with evidence contract check. Original package unchanged.\n')
