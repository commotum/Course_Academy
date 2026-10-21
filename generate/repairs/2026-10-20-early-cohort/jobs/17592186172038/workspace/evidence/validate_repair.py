import os,json,math,random,subprocess,copy,hashlib,shutil,sys
from fractions import Fraction as F
from pathlib import Path
from verify_record import g,check
from probe_banks import probes
W=Path(__file__).resolve().parents[1]; E=W/'evidence'; AS=E/'assets';AS.mkdir(exist_ok=True)
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(AS)
REPO=Path('/home/jake/Developer/Course_Academy');SOURCE=REPO/'generate/repairs/2026-10-20-early-cohort/jobs/17592186172038/source'
def save(name,data): (E/name).write_text(json.dumps(data,indent=2)+'\n')
def field(r):return r['question'][':question/answer-fields'][0]
def correct_geometry(r):
 f=field(r);a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);return r['generation']['choice_geometry'][a[':answer/value']]
def independent(t,p):
 a=F(p['a']);b=F(p.get('b',1));d=F(p.get('d',1));out=[]
 for x,y in p['points']:
  x,y=F(x),F(y)
  out.append({'constant_product':lambda:a-b*x*y,'quadratic_linear':lambda:a*x*x-b*y,'rational_square':lambda:a*y*y/x,'two_quadratic':lambda:a*x*x-b*y*y,'affine_fraction':lambda:(a*x+b*y)/d,'affine':lambda:a*x+b*y}[t]())
 return list(map(str,out))
def verify(r):
 check(r);m=r['generation'];assert independent(m['template'],m['parameters'])==m['exact_slopes']==correct_geometry(r)
 return r
supplied=json.loads((SOURCE/'source.json').read_text());rawqs={q[':question/math-academy-id']:q for q in supplied['material']['kp'][':knowledge-point/questions']}
raster=json.loads((W/'17592186172038/source-raster.json').read_text());source_records=[];source_results=[]
for sid,(t,p,_) in g.PROFILES.items():
 r=verify(g.generate('easy',profile=sid,parameters=p));source_records.append(r);q=rawqs[sid]
 assert r['question'][':question/problem']==q[':question/problem']
 _,bank=g.banks(t,p,sid);observed=[v for v in raster if v['source_id']==sid];byasset={v['asset']:v for v in observed}
 assert set(byasset)=={a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']}
 for row,v in zip(bank,observed):
  for exact,approx in zip(row,v['raster_slopes']):assert approx=='inf' if exact==g.sp.oo else abs(math.atan(float(exact))-math.atan(approx))<.06
 correct=q[':question/answer-fields'][0].get(':answer-field/correct');ci=bank.index(g.banks(t,p,sid)[0])
 if correct:assert correct[':answer/value']==observed[ci]['asset']
 if ':question/worked-solution' in q:
  import re
  normalize=lambda s:re.sub(r'!\[\]\([^)]*\)','<PLOT>',re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}','<ROWS>',s,flags=re.S))
  assert normalize(q[':question/worked-solution'])==normalize(r['question'][':question/worked-solution'])
 source_results.append({'source_id':sid,'options_matched':5,'distractors_matched':4,'stored_correct_match':bool(correct),'missing_fields_authored':not bool(correct),'difficulty_source':q.get(':question/difficulty')})
save('source-replays.json',source_records);save('source-replay.json',{'complete_banks':7,'options':35,'distractors':28,'observed_keys':5,'inferred_keys':2,'cases':source_results,'source_raster':'../17592186172038/source-raster.json','visual_inspection':'All seven existing source contact sheets viewed during this repair; source raster evidence retained.'})
print('Source replay: 7 banks, 35 options, 5 observed and 2 inferred keys',flush=True)
records=[];counter=[];rejection={}
for ti,t in enumerate(g.TEMPLATES):
 base=verify(g.generate('easy',120+ti,template=t));records.append(base);p=base['generation']['parameters']
 # Change signs of all coefficients: negate f while retaining all point coordinates.
 n=copy.deepcopy(p)
 for k in ('a','b'):
  if k in n:n[k]=str(-F(n[k]))
 neg=verify(g.generate('easy',120+ti,template=t,parameters=n));records.append(neg)
 assert neg['generation']['exact_slopes']==[str(-F(v)) for v in base['generation']['exact_slopes']]
 assert correct_geometry(base)!=correct_geometry(neg)
 # Change just one assessed point, maintaining two coordinates and the equation.
 changed=None;index=ti%3
 for pt in [[x,y] for x in range(-4,5) for y in range(-4,5) if t!='rational_square' or x!=0]:
  n=copy.deepcopy(p);n['points'][index]=pt
  try:
   g.validate_parameters('easy',t,n);s,b=g.banks(t,n,'authored')
   if str(s[index])==base['generation']['exact_slopes'][index]:continue
   changed=verify(g.generate('easy',120+ti,template=t,parameters=n));break
  except ValueError:continue
 assert changed;records.append(changed)
 assert all(base['generation']['exact_slopes'][j]==changed['generation']['exact_slopes'][j] for j in range(3) if j!=index)
 # Presentation-only seed reorders complete choices without changing their math.
 presentation=verify(g.generate('easy',980+ti,template=t,parameters=p));records.append(presentation)
 assert base['question'][':question/id']==presentation['question'][':question/id'];assert correct_geometry(base)==correct_geometry(presentation)
 counter.append({'template':t,'base_id':base['question'][':question/id'],'negated_equation_id':neg['question'][':question/id'],'changed_point_id':changed['question'][':question/id'],'changed_index':index,'before':p,'after':changed['generation']['parameters'],'before_slopes':correct_geometry(base),'negated_slopes':correct_geometry(neg),'after_slopes':correct_geometry(changed),'irrelevant_seed_preserves_geometry':True})
 # Additional ordinary instances exercise position/zero/sign cases after rejection.
 for seed in range(3):records.append(verify(g.generate('easy',200+seed,template=t)))
 rng=random.Random(90210);accepted=0;attempts=0
 for _ in range(40):
  attempts+=1;sample=g.sample('easy',t,rng)
  try:g.validate_parameters('easy',t,sample);g.banks(t,sample,'authored');accepted+=1
  except ValueError:pass
 rejection[t]={'raw_attempts':attempts,'valid_banks':accepted,'whole_bank_rejected':attempts-accepted}
# Replay every observed bank at changed values, not only source literals.
profile_results=[]
for sid,(t,_,_) in g.PROFILES.items():
 r=verify(g.generate('easy',31,profile=sid));records.append(r);profile_results.append({'profile':sid,'parameters':r['generation']['parameters'],'checked':True})
# y^2 ignores y's sign: a valid simplification, while point centers must change.
p={'a':-1,'points':[[-1,-2],[2,-2],[2,2]]}
a=verify(g.generate('easy',parameters=p,template='rational_square'))
p2=copy.deepcopy(p);p2['points'][0][1]=2
b=verify(g.generate('easy',parameters=p2,template='rational_square'));assert a['generation']['exact_slopes']==b['generation']['exact_slopes'];records.extend([a,b])
invalid=[('rational_square',{'a':1,'points':[[0,1],[1,2],[2,3]]}),('affine',{'a':1,'b':2,'points':[[1,1],[1,1],[2,2]]}),('affine',{'a':1,'b':2,'points':[[5,1],[1,2],[2,3]]}),('affine',{'a':1,'b':2,'points':[[-1,-1],[0,0],[1,1]]})]
for t,p in invalid:
 try:g.generate('easy',template=t,parameters=p)
 except ValueError:pass
 else:raise AssertionError('Expected invalid domain or whole bank rejection')
# Native grading: all five choices in one batched process, including controls.
cases=[]
for i,r in enumerate(source_records+records):
 f=field(r);cases.append({'label':str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete bank / controlled response'} for c in f[':answer-field/choices']]})
save('engine-input.json',cases);save('generated.json',records);save('counterfactuals.json',counter)
subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'engine-input.json'),str(E/'engine-report.json')],check=True)
# Shared delivery filter handles exact duplicate presentation variants and inventory.
subprocess.run([sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/'generated.json'),'--source',str(SOURCE/'source.json'),'--inventory',str(SOURCE/'inventory.json'),'--difficulty','easy','--output',str(E/'delivery'),'--asset-root',str(AS),'--math-root','/media/jake/SSD/EDB/math'],check=True)
accepted=json.loads((E/'delivery/accepted.json').read_text())
# Delivery changes image paths; recover geometry from exact image bytes, independently of choice IDs.
geometry={hashlib.sha256((AS/path).read_bytes()).hexdigest():values for r in records for path,values in r['generation']['choice_geometry'].items()}
for r in accepted:
 for c in field(r)[':answer-field/choices']:
  path=c[':answer/value'];h=Path(path).stem;assert h in geometry
  r['generation']['choice_geometry'][path]=geometry[h]
variation={'raw':probes(records),'delivered':probes(accepted),'rejection':rejection,'counterfactuals':counter,'source_profile_generalization':profile_results,'semantic_instances_raw':len({r['generation']['mathematical_fingerprint'] for r in records}),'semantic_instances_delivered':len({r['generation']['mathematical_fingerprint'] for r in accepted}),'baseline':'Uniform radio choice is 0.2; tied cue strategies split their vote. No tested cue is reliable within any equation form. Small delivered samples are coverage checks, not statistical proof. Larger 40-per-form pure-bank probes are bank-probes-before.json.','selection_limits':'Read question_selection.rs: selects fresh usable candidates by difficulty then a uniform within-band index, or smallest entity with no configured policy. Captured inventory delivery exercised; live learner history, policy and future entity IDs unavailable. No database writes.'}
save('pedagogical-variation.json',variation)
# Representative UI: six normal forms plus replay with vertical distractors.
render_records=[next(r for r in records if r['generation']['template']==t) for t in g.TEMPLATES]+[source_records[3]]
save('render-records.json',render_records)
save('validation.json',{'passed':True,'source_complete_banks':7,'source_options':35,'records_checked':len(cases),'native_checks':sum(len(c['checks']) for c in cases),'explicit_invalid_cases':len(invalid),'counterfactual_pairs':len(counter),'delivered':len(accepted),'fidelity':'complete source bank orientations, prompt and available solution prose/sequence replayed; notation and asset rendering normalized; two source keys inferred','correctness':'Fractions oracle, independent displayed TeX parser, three substitutions and rendered segment endpoints','grading':'native grade_field on all five choices including controlled cases','variation':'within-template probes before/after shared filtering; sign and point counterfactuals; presentation and y-sign invariance','runtime_closure':'4 declared files; relocation check pending'})
print('Checked records',len(cases),'native responses',sum(len(c['checks']) for c in cases),'delivered',len(accepted),flush=True)
