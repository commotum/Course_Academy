"""Small affected-check sample: supplied source replay, displayed math and controls.
No database writes, services, or mutations of runtime package files.
"""
import collections,hashlib,importlib.util,json,math,os,pathlib,re,sys
sys.dont_write_bytecode=True
W=pathlib.Path(__file__).resolve().parents[1];E=W/'evidence';E.mkdir(exist_ok=True)
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(E/'assets')
os.environ['PYTHONDONTWRITEBYTECODE']='1'
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
G=module('generator',W/'17592186172040.py');old=module('prompt_checks',W/'checks/prompt_witness.py')
def save(name,value):(E/name).write_text(json.dumps(value,indent=2)+'\n')
def field(r):return r['question'][':question/answer-fields'][0]
def key(r):
 f=field(r);return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
source=json.loads((W.parent/'source/source.json').read_text());replays=[];replay_results=[]
for q in source['material']['kp'][':knowledge-point/questions']:
 profile=q[':question/math-academy-id'];level='moderate' if 'could be' in q[':question/problem'] else 'hard'
 r=G.generate(level,seed=91,profile=profile);replays.append(r);sf=q[':question/answer-fields'][0]
 assert sorted(a[':answer/value'] for a in field(r)[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
 assert r['question'][':question/problem']==q[':question/problem']
 if ':question/worked-solution' in q:assert r['question'][':question/worked-solution']==q[':question/worked-solution']
 if ':answer-field/correct' in sf:assert key(r)[':answer/value']==sf[':answer-field/correct'][':answer/value']
 replay_results.append({'profile':profile,'source_question_id':q[':question/id'],'matched_options':5,'total_options':5,'prompt_exact':True,'solution_exact':True if ':question/worked-solution' in q else None,'designation_exact':True if ':answer-field/correct' in sf else None,'source_difficulty':q.get(':question/difficulty'),'authored_completion':':answer-field/correct' not in sf})
save('source-replay-records.json',replays);save('source-replay-results.json',replay_results)
p={'a':1,'b':1,'c':0,'px':1,'py':1,'orientation':'y','single':'linear'}
sample=[];controls=[]
for t in G.TEMPLATES['moderate']:
 changes=[p,{**p,'a':-1},{**p,**({'orientation':'x'} if t=='possible_mixed' else {'px':2,'py':2} if t=='possible_product' else {'a':2})}]
 rs=[G.generate('moderate',seed=91+i,template=t,parameters=ps) for i,ps in enumerate(changes)];sample+=rs
 base=rs[0];relevant=G.generate('moderate',seed=91,template=t,parameters=changes[1])
 irrelevant=G.generate('moderate',seed=91,template=t,parameters={**p,'single':'exp'})
 assert base['question']==irrelevant['question']
 assert key(base)[':answer/value']!=key(relevant)[':answer/value']
 assert base['question'][':question/problem']!=relevant['question'][':question/problem']
 assert base['question'][':question/worked-solution']!=relevant['question'][':question/worked-solution']
 controls.extend([base,relevant,irrelevant]);
 controls_info={'irrelevant_slot':'single','relevant_slot':'a sign'}
# Direction changes only the outlier; four both-variable options remain fixed.
x=G.generate('hard',seed=91,template='impossible_x',parameters=p);y=G.generate('hard',seed=91,template='impossible_y',parameters=p)
assert len(set(a[':answer/value'] for a in field(x)[':answer-field/choices']) & set(a[':answer/value'] for a in field(y)[':answer-field/choices']))==4
assert key(x)[':answer/value']!=key(y)[':answer/value'];controls.extend([x,y]);sample.extend([x,y,G.generate('easy',seed=91,template='possible_linear',parameters=p)])
save('small-sample.json',sample);save('controlled-records.json',controls)
batch=[G.generate('moderate',seed=801239+i) for i in range(5)];save('batch.json',batch)
# Numeric dependence witness is derived from serialized plot data actually sent
# to the renderer. The independent prompt parser comes from retained validation.
math_results=[]
for r in sample+controls+batch:
 f=field(r);possible='could be' in r['question'][':question/problem'];matches=[];image_checks=[]
 rhs=old.load_rhs(r['question'][':question/problem']) if possible else None
 for a in f[':answer-field/choices']:
  path=pathlib.Path(a[':answer/value']);data=json.loads(path.with_suffix('.json').read_text());pts=data['points'];by_x=collections.defaultdict(list);by_y=collections.defaultdict(list)
  for xx,yy,m in pts:by_x[xx].append(m);by_y[yy].append(m)
  # x-dependence means some horizontal row changes; y-dependence means
  # some vertical column changes. Exceptional axes do not erase dependence.
  varies_x=any(max(v)-min(v)>1e-8 for v in by_y.values());varies_y=any(max(v)-min(v)>1e-8 for v in by_x.values())
  qualifies=(varies_x and varies_y)==possible
  if qualifies:matches.append(a[':answer/id'])
  if qualifies and possible:
   # Scalar substitution into the expression parsed from the actual prompt.
   for xx,yy,m in pts[::17]:
    predicted=float(rhs.subs({G.X:xx,G.Y:yy}));assert math.isclose(m,predicted,rel_tol=1e-10,abs_tol=1e-10)
  assert path.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
  image_checks.append({'choice_id':a[':answer/id'],'varies_x':varies_x,'varies_y':varies_y,'qualifies':qualifies})
 assert matches==[f[':answer-field/correct'][1]],(r['generation']['template'],matches)
 guide=re.findall(r'!\[\]\((.*?)\)',r['question'][':question/worked-solution'])[-1]
 gs=json.loads(pathlib.Path(guide).with_suffix('.json').read_text());ks=json.loads(pathlib.Path(key(r)[':answer/value']).with_suffix('.json').read_text());assert gs['points']==ks['points']
 math_results.append({'question_id':r['question'][':question/id'],'template':r['generation']['template'],'images':image_checks,'guide_matches_key':True})
save('math-results.json',math_results)
# Old boundary/cold-source behavior is preserved; no broader sampler redesign.
invalid=[{'parameters':{**p,'a':0}},{'template':'possible_linear'},{'field_type':'checkbox'},{'profile':'q-98229'}]
for args in invalid:
 try:G.generate('moderate',seed=801239,**args)
 except ValueError:pass
 else:raise AssertionError(('invalid explicit inputs accepted',args))
assert G.generate('moderate',seed=801239)==batch[0]
canonical=G.generate('easy',seed=991,profile='e-8507')
all_records=replays+sample+controls+batch+[canonical]+json.loads((E/'cold-records.json').read_text())
# Batch native grading all choices together; mathematical keys were checked above.
grader=[]
for i,r in enumerate(all_records):
 f=field(r);grader.append({'label':str(i)+'/'+r['generation']['bank_profile'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete bank single-choice test'} for a in f[':answer-field/choices']]})
save('grader-input.json',grader)
save('render-records.json',[canonical,sample[5],x])
save('counterfactual-results.json',{'moderate':{'templates':G.TEMPLATES['moderate'],'relevant_sign_changes':3,'prompt_key_worked_guide_changed':True,'irrelevant_single_shape_preserves_question':True},'hard':{'changed_outlier_direction':'x to y','background_options_held_fixed':4,'key_and_worked_guide_changed':True},'invalid_cases_rejected':len(invalid),'determinism':True})
# Inspection of the captured inventory; do not manufacture generated source rows.
inventory=json.loads((W.parent/'source/inventory.json').read_text());srcids={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
rows=[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':q[':question/id'] in srcids,'generation_attributes':[k for k in q if 'generat' in k.lower()]} for q in inventory['questions']]
assert all(r['original_source'] and not r['generation_attributes'] for r in rows)
save('affected-inventory.json',{'affected_questions':[]})
save('inventory-review.json',{'basis':inventory['basis'],'rows':rows,'conclusion':'All eight captured questions are original source records, without generation metadata. Verified no stored generated instances to implicate in either retained finding; runtime dependency and missing canonical API defects concern generator behavior. Original sources are not relabeled. Live inventory is untested.'})
print('PASS: 8 practice banks (40 options), 12 small sample records, controlled pairs, 5 requested batch records;',len(grader),'native grader cases prepared')
