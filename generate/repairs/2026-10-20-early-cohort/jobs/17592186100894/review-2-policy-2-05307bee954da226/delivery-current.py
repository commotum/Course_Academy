from auditlib import *
from collections import Counter,defaultdict
samples=json.load(open(E/'samples.json')); batch=json.load(open(E/'batch.json'))
def measures(rs):
 ts=[r for r in rs if r['generation']['template']=='q-104065']
 return {'total':len(rs),'templates':dict(Counter(r['generation']['template'] for r in rs)),'trig':len(ts),'constants':dict(Counter(r['generation']['parameters'].get('c') for r in ts)),'coefficients':dict(Counter(str(r['generation']['parameters'].get('a')) for r in ts)),'key_pi':sum('\\pi' in correct(r) for r in ts),'key_no_pi':sum('\\pi' not in correct(r) for r in ts)}
stages={}
for name,rs,level in [('batch',batch,'easy'),('easy',[r for r in samples if r['question'][':question/difficulty'].endswith('/easy')],'easy'),('moderate',[r for r in samples if r['question'][':question/difficulty'].endswith('/moderate')],'moderate')]:
 save('delivery-'+name+'-input.json',rs)
 cmd=[sys.executable,str(ROOT/'generate/pipeline/check_delivery.py'),'--input',str(E/('delivery-'+name+'-input.json')),'--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),'--difficulty',level,'--output',str(E/('delivery-'+name)),'--asset-root',str(E),'--math-root','/media/jake/SSD/EDB/math']
 p=subprocess.run(cmd,capture_output=True,text=True);(E/('delivery-'+name+'-console.txt')).write_text(p.stdout+p.stderr)
 assert p.returncode==0,p.stderr+p.stdout
 accepted=json.load(open(E/('delivery-'+name+'/accepted.json')))
 stages[name]={'command':cmd,'exit':p.returncode,'raw':measures(rs),'accepted':measures(accepted)}
save('delivery-stages.json',stages)
# Predict only from displayed bank properties, never use correct UUID to choose.
def probe(rs,name):
 out=[]
 groups={'all changed trig':[r for r in rs if r['generation']['template']=='q-104065']}
 for bank in range(15):groups['fixed visible bank '+str(bank)]=[r for r in groups['all changed trig'] if r['generation']['parameters'].get('bank')==bank]
 groups['pure pi² initial ordinate']=[r for r in groups['all changed trig'] if simplify(prompt_data(r)[1][1]/S.pi**2).is_Rational is True]
 for group,rr in groups.items():
  if not rr:continue
  for strategy in ['unique log without pi','previous shortest repeated coefficient','shortest option','longest option','stored first option','singleton coefficient']:
   wins=0;chosen=0;details=[]
   for r in rr:
    opts=field(r)[':answer-field/choices'];_,(x0,y0)=prompt_data(r);h=simplify(x0-S.pi/2)
    co=[S.expand(explicit(r,a[':answer/value'])-S.log(S.sin(x-h))).coeff(x,2) for a in opts];counts=Counter(co);inds=[]
    if strategy=='unique log without pi':inds=[i for i,a in enumerate(opts) if '\\ln' in a[':answer/value'] and '\\pi' not in a[':answer/value']]
    if strategy=='previous shortest repeated coefficient':
     reps=[v for v,n in counts.items() if n>1]
     if simplify(y0/S.pi**2).is_Rational is True and len(reps)==1:
      same=[i for i,v in enumerate(co) if v==reps[0]];ln=min(len(opts[i][':answer/value']) for i in same);inds=[i for i in same if len(opts[i][':answer/value'])==ln]
    if strategy=='shortest option':inds=[min(range(len(opts)),key=lambda i:len(opts[i][':answer/value']))]
    if strategy=='longest option':inds=[max(range(len(opts)),key=lambda i:len(opts[i][':answer/value']))]
    if strategy=='stored first option':inds=[0]
    if strategy=='singleton coefficient':inds=[i for i,v in enumerate(co) if counts[v]==1]
    prediction=opts[inds[0]][':answer/id'] if len(inds)==1 else None
    chosen+=prediction is not None;win=prediction==field(r)[':answer-field/correct'][1];wins+=win
    details.append({'question_id':r['question'][':question/id'],'candidates':inds,'success':win})
   out.append({'stage':name,'subgroup':group,'strategy':strategy,'correct':wins,'total':len(rr),'applications':chosen,'baseline':0.2,'details':details})
 return out
raw=json.load(open(E/'role-records.json'));accepted=json.load(open(E/'delivery-easy/accepted.json'))
signatures={(r['generation']['seed'],json.dumps(r['generation']['parameters'],sort_keys=True)) for r in raw};delroles=[r for r in accepted if (r['generation']['seed'],json.dumps(r['generation']['parameters'],sort_keys=True)) in signatures]
probes=probe(raw,'raw roles')+probe(delroles,'delivered roles')
# A fixed whole bank admits every answer, with order held fixed. This is stronger
# than merely observing randomized correct positions across different banks.
coverage=[]
for stage,rs in [('raw',raw),('delivered',delroles)]:
 bybank=defaultdict(list)
 for r in rs:bybank[tuple(a[':answer/value'] for a in field(r)[':answer-field/choices'])].append(r)
 for bank,group in bybank.items():
  keys=Counter(correct(r) for r in group)
  coverage.append({'stage':stage,'bank':list(bank),'roles':len(group),'all_values_can_win':set(keys)==set(bank),'key_counts':dict(keys)})
 assert len(bybank)==15 and all(set(correct(r) for r in rr)==set(bb) for bb,rr in bybank.items())
save('shortcut-results.json',{'probes':probes,'fixed_bank_coverage':coverage,'delivery_role_count':len(delroles),'interpretation':'Whole-bank cues succeed at random baseline on fixed-bank controls. Old unique repeated-coefficient subgroup is absent: two coefficients now repeat. Pure pi² subgroup retains every role. Coefficient matching to ODE followed by IC substitution is intended mathematics, not an incidental cue.','exact_batch':{'records':len(batch),'templates':dict(Counter(r['generation']['template'] for r in batch)),'trig_count':sum(r['generation']['template']=='q-104065' for r in batch),'assessment':'No trigonometric item in actual batch. Four displayed blank families; two translated q-355546 instances are useful modest numerical practice, not a complete mastery pool. Sine fragment requires integration; fixed zero or copy-IC does not solve the five delivered tasks. Valid sine constant-shift entries fail native grading (separate finding).'}})
# Captured inventory: inspect identity AND generation provenance, do not mark sources generated.
inv=json.load(open(JOB/'source/inventory.json'));qs=inv['questions'];sourceids={q[':question/id'] for q in json.load(open(JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions']}
generated=[q for q in qs if any('generat' in k for k in q)]
assert not generated and all(q[':question/id'] in sourceids for q in qs)
save('inventory-audit.json',{'basis':inv['basis'],'records':len(qs),'generated_records':len(generated),'all_ids_are_original_sources':True,'question_keys':sorted(set(k for q in qs for k in q)),'finding':'Sine arbitrary-C scaffold grading','tested_absence':'Captured inventory contains only the 26 original source questions. No generated question has generation metadata to reproduce; none affected as a stored generated instance. The original sine source is not relabeled generated.','limitations':'Live post-capture inventory and learner histories unavailable; not queried.'})
save('affected-inventory.json',{'affected_questions':[]})
# Faithful read-only easy-band selection under explicit fresh-pool assumptions.
acc=json.load(open(E/'delivery-batch/accepted.json'));base=max(q[':db/id'] for q in qs)+1
pool=sorted([(q[':db/id'],'source',q[':question/id']) for q in qs if q[':question/difficulty'][':db/ident'].endswith('/easy')]+[(base+i,r['generation']['template'],r['question'][':question/id']) for i,r in enumerate(acc)])
draws=[]
for i in range(128):
 seed='independent-review2-'+str(i);d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/2**53;draws.append({'seed':seed,'selected':pool[int(u*len(pool))]})
save('selection.json',{'implementation':'engine/rust/question_selection.rs select, weights and seen_before_task read directly','implementation_sha256':hashlib.sha256((ROOT/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'inventory_basis':inv['basis'],'pool':pool,'draws':draws,'counts':dict(Counter(d['selected'][1] for d in draws)),'assumptions':['All captured easy sources and accepted batch fresh and usable; synthetic sorted new entity IDs.','Conditioned on a configured positive easy weight; native choice uses digest bytes 8..16 for a uniform draw within that band.','No-policy fallback chooses first entity; zero-weight easy band excludes every easy candidate; prior history can remove items but cannot change their mathematical keys.'],'stage_conclusion':'All accepted batch items have positive support when fresh under positive easy weight. Same for each delivered role profile if prepared instead. No role-sensitive rejection/resampling exists in generator: direct finite selection then return; CLI samples distinct template/shift candidates, independent uniform role within selected bank.','limits':'Exact live entity IDs, task seeds, weights and histories are not in captured input. Conditional reproduction and rule inspection, not a claim of an actual live learner draw.'})
publication=JOB/'publication/preparation.json'
save('publication-status.json',{'exists':publication.exists(),'basis':'Actual shared check_delivery.py against captured inventory and exact runner batch','publication_summary':({'keys':list(json.load(open(publication)).keys())} if publication.exists() else None),'writes':'Only evidence directory output; no publish or database call.'})
print('delivery', {k:(v['raw']['total'],v['accepted']['total']) for k,v in stages.items()},'roles',len(delroles),'inventory generated',len(generated))
