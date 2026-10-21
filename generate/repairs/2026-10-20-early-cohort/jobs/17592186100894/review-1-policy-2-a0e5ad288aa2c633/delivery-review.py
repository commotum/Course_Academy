from auditlib import *
import collections, shutil

samples=json.load(open(E/'samples.json')); batch=json.load(open(E/'batch.json'))
def cue(r):
 opts=field(r)[':answer-field/choices']; cand=[a for a in opts if ('\\ln' in a[':answer/value'] or '\\operatorname{ln}' in a[':answer/value']) and '\\pi' not in a[':answer/value']]
 return len(cand)==1 and cand[0][':answer/id']==field(r)[':answer-field/correct'][1]
def measure(rs):
 ts=[r for r in rs if r['generation']['template']=='q-104065']; return {'total':len(rs),'templates':dict(collections.Counter(r['generation']['template'] for r in rs)),'trig':len(ts),'trig_constants':dict(collections.Counter(r['generation']['parameters'].get('c') for r in ts)),'trig_coefficients':dict(collections.Counter(str(r['generation']['parameters'].get('a')) for r in ts)),'key_with_pi':sum('\\pi' in correct(r) for r in ts),'old_cue_correct':sum(cue(r) for r in ts),'old_cue_total':len(ts)}
stage={}
for label,rs,level in [('batch',batch,'easy'),('easy',[r for r in samples if g.level(r['generation']['template'])=='easy'],'easy'),('moderate',[r for r in samples if g.level(r['generation']['template'])=='moderate'],'moderate')]:
 save('delivery-'+label+'-input.json',rs)
 cmd=[sys.executable,str(ROOT/'generate/pipeline/check_delivery.py'),'--input',str(E/('delivery-'+label+'-input.json')),'--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),'--difficulty',level,'--output',str(E/('delivery-'+label)),'--asset-root',str(E),'--math-root','/media/jake/SSD/EDB/math']
 p=subprocess.run(cmd,capture_output=True,text=True);(E/('delivery-'+label+'-console.txt')).write_text(p.stdout+p.stderr)
 stage[label]={'command':cmd,'exit':p.returncode,'raw':measure(rs),'accepted':measure(json.load(open(E/('delivery-'+label+'/accepted.json')))) if p.returncode==0 else None}
save('delivery-stages.json',stage)

# Reconfirm original source/missing-profile counterexamples using prior isolated package.
prev=JOB/'review-0-policy-2-bbeaf16048b2bfc2'; oldpath=prev/'relocated/17592186100894.py'
spec=importlib.util.spec_from_file_location('old_gen',oldpath);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
oldr=old.generate('easy',847003,'q-104065',{'h':1});current=g.generate('easy',847003,'q-104065',{'h':1})
save('before-after-shortcut-records.json',[oldr,current]);missing=[]
for mid in ('q-128199','q-126765'):
 try:old.generate(g.level(mid),493711,mid,{'h':1});missing.append({'template':mid,'old_rejected':False})
 except Exception as exc:missing.append({'template':mid,'old_rejected':True,'message':str(exc),'current_supported':mid in g.MODELS})
save('retained-finding-witnesses.json',{'old_symbol_cue_success':cue(oldr),'current_exact_case_cue_success':cue(current),'missing_profile_before_after':missing,'old_native_failure':'prior-strict-failure.txt; independently authored strict input now rerun against current harness in grader-input.json','preflight':'preflight-inspection.json'})

# Probe repaired trigonometric bank within coefficient/constant subgroups.
trig=[r for r in samples if r['generation']['template']=='q-104065']
probes=[]
groups={'all trig':trig}
for a in (2,4,6):groups['coefficient '+str(a)]=[r for r in trig if r['generation']['parameters'].get('a')==a]
for c in ('-pi^2','-1','0','1','pi^2'):groups['constant '+c]=[r for r in trig if r['generation']['parameters'].get('c')==c]
for name,rs in groups.items():
 for strategy in ('unique logarithm without pi','shortest expression','first stored option','lowest x-square coefficient','highest x-square coefficient','unique integer constant'):
  wins=0;applies=0;pred=[]
  for r in rs:
   opts=field(r)[':answer-field/choices'];h=r['generation']['parameters']['h'];j=next(i for i,a in enumerate(opts) if a[':answer/id']==field(r)[':answer-field/correct'][1]); candidates=[]
   if strategy=='unique logarithm without pi':candidates=[i for i,a in enumerate(opts) if '\\pi' not in a[':answer/value']]
   elif strategy=='first stored option':candidates=[0]
   elif strategy=='shortest expression':
    lens=[len(a[':answer/value']) for a in opts];candidates=[i for i,n in enumerate(lens) if n==min(lens)]
   else:
    values=[explicit(r,a[':answer/value'])-S.log(S.sin(x-h)) for a in opts];coeff=[S.expand(v).coeff(x,2) for v in values]
    if strategy=='lowest x-square coefficient':candidates=[i for i,c in enumerate(coeff) if c==min(coeff)]
    elif strategy=='highest x-square coefficient':candidates=[i for i,c in enumerate(coeff) if c==max(coeff)]
    elif strategy=='unique integer constant':candidates=[i for i,v in enumerate(values) if simplify(v.subs(x,h)).is_integer]
   if len(candidates)==1:applies+=1;wins+=candidates[0]==j
   pred.append({'qid':r['question'][':question/id'],'candidates':candidates,'correct_index':j})
  probes.append({'subgroup':name,'strategy':strategy,'correct':wins,'total':len(rs),'unique_applications':applies,'baseline':0.2,'predictions':pred})
save('shortcut-results.json',{'probes':probes,'delivery':stage,'note':'No unique candidate is a failure to answer, not an omitted trial. Stored option position is further randomized by actual UI. Perfect small subgroups require mathematical inspection; not every observed correlation is a structural rule.'})

# Captured inventory and learner selection rules, conditioned on easy band.
inv=json.load(open(JOB/'source/inventory.json'));qs=inv['questions'];sourceids={q[':question/id'] for q in json.load(open(JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions']}
generated=[q for q in qs if any('generat' in k for k in q)]
save('inventory-audit.json',{'basis':inv['basis'],'count':len(qs),'generated_count':len(generated),'all_original_source_ids':all(q[':question/id'] in sourceids for q in qs),'result':'Examined captured inventory; no generated records. Original source questions not labeled generated. No affected generated stored instance exists in this captured inventory; future/live inventory not queried.'})
save('affected-inventory.json',{'affected_questions':[]})
accepted=json.load(open(E/'delivery-batch/accepted.json'));base=max(q[':db/id'] for q in qs)+1
pool=sorted([(q[':db/id'],'source',q[':question/id']) for q in qs if q[':question/difficulty'][':db/ident'].endswith('/easy')]+[(base+i,r['generation']['template'],r['question'][':question/id']) for i,r in enumerate(accepted)])
draws=[]
for i in range(128):
 seed='independent-revision-'+str(i);d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/2**53;chosen=pool[int(u*len(pool))];draws.append({'seed':seed,'selected':chosen})
save('selection.json',{'source':'engine/rust/question_selection.rs select()/seen_before_task; ui/learning.js choiceOrder','basis':inv['basis'],'assumptions':['Fresh usable captured easy sources plus accepted batch; positive easy band weight, conditioned on drawing easy.','New entity IDs are sorted proxies; exact live history and policy weights unavailable.','No-policy fallback returns first candidate; configured weighted selection samples uniformly within chosen band.'], 'pool':pool,'draws':draws,'counts':dict(collections.Counter(d['selected'][1] for d in draws)),'result':'All five accepted batch records have support under fresh configured easy-band selection. Freshness can remove records, but does not change their banks or mathematical decisions. UI hashes choice IDs and task-item IDs; stored position is not a stable displayed cue.'})
print(json.dumps({'stages':stage,'original_counterexamples':json.load(open(E/'retained-finding-witnesses.json')),'inventory_generated':len(generated),'perfect_probes':[(p['subgroup'],p['strategy'],p['correct'],p['total']) for p in probes if p['correct']==p['total']]}))
