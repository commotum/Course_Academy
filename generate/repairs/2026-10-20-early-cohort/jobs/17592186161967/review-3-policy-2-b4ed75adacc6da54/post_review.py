import ast,collections,hashlib,importlib.util,json,pathlib,sys
sys.dont_write_bytecode=True
from helpers import check,mats,ops
ROOT=pathlib.Path(__file__).resolve().parent;JOB=ROOT.parent;PKG=JOB/'workspace'
s=importlib.util.spec_from_file_location('subject',PKG/'17592186161967.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
a=ast.parse((ROOT/'review.py').read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in ['bank','analyze','metrics']],type_ignores=[]),'analysis-functions','exec'))
def save(n,x):(ROOT/n).write_text(json.dumps(x,indent=2)+'\n')
def probes(rr):
 details=[]
 for r in rr:
  z=analyze(r);correct=z['correct_pair'];extra=z['extra'];bb=bank(r);ci=check(r)
  z['same_sign']=[extra[d]*correct[d]>0 for d in (0,1)]
  z['cross_sign']=correct[0]*correct[1]>0
  z['first_mode']=collections.Counter(v[0] for v in bb).most_common(1)[0][0]==correct[0]
  details.append(z)
 groups={}
 for shape in ['all','unit-first','unit-second','swap']:
  vv=[d for d in details if shape=='all' or d['shape']==shape]
  if not vv:continue
  groups[shape]={'total':len(vv),'same_sign':[sum(v['same_sign'][d] for v in vv) for d in (0,1)],'opposite_sign':[sum(not v['same_sign'][d] for v in vv) for d in (0,1)],'same_as_other':sum(v['cross_sign'] for v in vv),'first_mode':sum(v['first_mode'] for v in vv),'correct_sign_pairs':sorted(set(tuple(k>0 for k in v['correct_pair']) for v in vv)),'positions':dict(collections.Counter(v['correct_index'] for v in vv))}
 return {'groups':groups,'details':details}
allprobes={};cases=json.load(open('grader-input.json'));selection={}
for n in ['batch','fresh','fresh-batches']:
 path=f'delivery-{n}/accepted.json';rr=json.load(open(path));before=json.load(open('batch.json' if n=='batch' else 'fresh-samples.json' if n=='fresh' else 'fresh-batches.json'))
 allprobes[n]={'before':probes(before),'after':probes(rr),'delivery':json.load(open(f'delivery-{n}/delivery.json'))}
 draws=[]
 for i in range(32):
  seed=f'independent-review-3-{i}';d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();ix=int(((int.from_bytes(d[8:16],'big')>>11)/(1<<53))*len(rr));z=analyze(rr[ix]);draws.append({'seed':seed,'rank':ix,'question_id':z['id'],'retained_shortcut_success':z['success']})
 selection[n]={'eligible_count':len(rr),'draws':draws,'retained_shortcut_successes':sum(v['retained_shortcut_success'] for v in draws),'uniform_easy_pool_probes':probes(rr)['groups']}
 for i,r in enumerate(rr):
  ci=check(r);f=r['question'][':question/answer-fields'][0]
  cs=[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if j==ci else 'rejected','purpose':'Full-row arithmetic after publication normalization'} for j,c in enumerate(f[':answer-field/choices'])]
  z=analyze(r);cs.append({'submitted_answer_id':z['guess_id'],'expected':'accepted' if z['success'] else 'rejected','purpose':'Actual retained partial-reasoning shortcut after delivery'})
  cases.append({'label':n+'-delivered-'+str(i),'record':r,'checks':cs})
# Explicit stale-response assertions for relevant and irrelevant counterfactuals.
pairs=json.load(open('counterfactual-records.json'));oldpair=bank(pairs[0])[check(pairs[0])]
for i in (0,1,2):
 r=pairs[i];idx=bank(r).index(oldpair);choice=r['question'][':question/answer-fields'][0][':answer-field/choices'][idx]
 cases.append({'label':'controlled-old-response-'+str(i),'record':r,'checks':[{'submitted_answer_id':choice[':answer/id'],'expected':'rejected' if i==1 else 'accepted','purpose':'Old operation pair must be rejected on relevant sign change and preserved on irrelevant non-target entry change'}]})
save('post-delivery-shortcuts.json',allprobes);save('all-grader-input.json',cases)
selection['basis']=5580;selection['rule']='Read engine/rust/question_selection.rs: fresh usable candidates deduplicated and sorted by entity ID; positive easy weight selects uniformly within all-easy pool via SHA256 bytes 8:16. Empty history modeled. No configured weights selects first remaining entity; zero easy weight excludes this rated pool.'
selection['limitations']=['New entity IDs and live learner history are not captured; rank uses accepted-file order. Equal within-band probabilities and support do not depend on that order.','All five runner candidates remain eligible under positive easy weight. After prior-answer exclusion, some cases can naturally be absent for an individual learner. No claim that every short learner session contains every sign case.','No publication preparation exists; actual shared read-only delivery used captured inventory. Original sources coexist with generated additions.']
save('selection.json',selection)
save('retained-finding-results.json',{'findings':[{'id':'d02e8980f26ead535fe5','author_old':'author-old-frequency.log: retained 36-case failure persists','author_current':'author-current-check.log: pass; 9/36 frequency successes, 52 identical-bank groups','independent_old':'retained-old.log: 36/36','independent_current':'retained-current.log: 9/36'},{'id':'79a24ab401bd284df93a','author_old':'author-old-batch.log: unit-first uniform sign cue','author_current':'author-current-batch.log: 5 delivered survivors and 54 small-sample records pass','independent_old':'retained-batch-old.json: 5/5 shortcut success','independent_current':'retained-batch-current.json: 2/5 shortcut success'}],'preflight_inspected':True,'control_origin':'Unmodified preserved previous review relocated generators; author checks copied and input paths adapted under current evidence root.'})
(ROOT/'session-state.md').write_text('Independent arithmetic and all source replays passed; batch 5/5 and fresh CLI 26/26 survive delivery. Both retained regressions reproduce failures on old code and pass current code. Post-delivery and selection probes saved. Native grader input assembled, rendering inspection in progress.\n')
print(json.dumps({'native_cases':len(cases),'native_checks':sum(len(x['checks']) for x in cases),'post_delivery':{n:{'counts':(x['delivery']['input_count'],x['delivery']['accepted_count']),'groups':x['after']['groups']} for n,x in allprobes.items()}},default=str))
