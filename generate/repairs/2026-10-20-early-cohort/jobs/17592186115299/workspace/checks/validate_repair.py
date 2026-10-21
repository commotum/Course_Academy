"""Source replay, independent printed math, native grading and variation witnesses."""
import collections,copy,importlib.util,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('legacy_validation',ROOT/'17592186115299/validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
E=ROOT/'evidence';REPO=Path('/home/jake/Developer/Course_Academy');PY='/home/jake/Developer/Course_Academy/.venv/bin/python'
def dump(name,obj): (E/name).write_text(json.dumps(obj,indent=2)+'\n')
def plain(s):
 s=re.sub(r'\\left\[\\begin\{array\}\{[^}]+\}(.*?)\\end\{array\}\\right\]',lambda m:r'[\begin{aligned}'+m[1]+r'\end{aligned}]',s,flags=re.S)
 return re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',lambda m:r'[\begin{aligned}'+m[1]+r'\end{aligned}]',s,flags=re.S).replace(r'\left(', '(').replace(r'\right)', ')')
def category(s):return 'dependent' if 'consistent dependent' in s else 'independent' if 'independent' in s or 'unique solution' in s else 'inconsistent' if 'inconsistent' in s or 'no solution' in s else 'none'
def mathematical(rec):
 q=rec['question'];m=v.system(q[':question/problem']);kind=v.independent_class(m);assert kind==rec['generation']['classification']
 solution=plain(q[':question/worked-solution']);mm=v.matrices(solution);assert mm[0]==m and mm[1]==m
 assert v.operation_checks(solution)==len(rec['generation']['operations']);assert mm[-1].rref()[0]==m.rref()[0]
 # Every operation and every displayed corresponding equation/substitution is checked by retained independent validator.
 adapted=copy.deepcopy(rec);aq=adapted['question'];aq[':question/worked-solution']=solution
 if aq[':question/answer-fields'][0][':answer-field/type'].endswith('/checkbox'):
  aq[':question/problem']+='\n\n'+'\n'.join(g.ROMAN[i]+'. '+g.WORDS[k] for i,k in enumerate(g.WORDS))
 key=g.correct_for(aq[':question/problem'],m)
 bank=['I only','II only','III only','I and II only','I and III only']
 aq[':question/answer-fields']=[{':answer-field/type':':answer-field.type/radio',':answer-field/correct':[':answer/id',key],':answer-field/choices':[{':answer/id':x,':answer/value':x} for x in bank]}]
 v.validate_record(adapted)
 checks=[];truth=[]
 for i,f in enumerate(q[':question/answer-fields']):
  if f[':answer-field/type'].endswith('/checkbox'):
   expected='true' if category(f[':answer-field/key'])==kind else 'false';truth.append(expected=='true')
  else:expected=g.correct_for(q[':question/problem'],m)
  for a in f[':answer-field/choices']:
   correct=a[':answer/value']==expected
   assert correct==(a[':answer/id']==f[':answer-field/correct'][1]), 'Wrong key in printed question'
   checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if correct else 'rejected','purpose':'Independently solve printed system; test every selectable alternative'})
 if truth:assert sum(truth)==1
 return m,kind,checks

def source_replays():
 qs=json.loads((E/'source-questions.json').read_text());replays=[];report=[]
 clean=lambda s:re.sub(r'\s+','',g.normalize_prose(plain(g.normalize_prose(s))))
 for source in qs:
  name=source[':question/math-academy-id'];n=v.system(source[':question/problem']).cols-1
  r=g.generate('moderate',template=name,parameters={'scales':[1]*n,'translations':[0]*n});mathematical(r);q=r['question']
  assert clean(source[':question/problem'])==clean(q[':question/problem']),name+' prompt'
  if name!='q-32242':assert clean(source[':question/worked-solution'].replace('reduced row echelon form','row echelon form'))==clean(q[':question/worked-solution']),name+' solution'
  sf=sorted(source[':question/answer-fields'],key=lambda f:f[':answer-field/key']);gf=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']);assert len(sf)==len(gf)
  for a,b in zip(sf,gf):
   assert a[':answer-field/key']==b[':answer-field/key']
   assert a[':answer-field/type'][':db/ident']==b[':answer-field/type']
   assert sorted(x[':answer/value'] for x in a[':answer-field/choices'])==sorted(x[':answer/value'] for x in b[':answer-field/choices'])
   assert a[':answer-field/correct'][':answer/value']==next(x[':answer/value'] for x in b[':answer-field/choices'] if x[':answer/id']==b[':answer-field/correct'][1])
  report.append({'source_id':name,'question_id':source[':question/id'],'banks':len(sf),'options':sum(len(f[':answer-field/choices']) for f in sf),'prompt_matched':True,'solution_matched':name not in ['q-32242','q-74638'],'retained_correction':'Unstated R1 negation removed' if name=='q-32242' else 'Echelon stage described as echelon, rather than reduced echelon' if name=='q-74638' else None});replays.append(r)
 dump('source-replays.json',replays);dump('source-replay-report.json',report)
 return replays

def summarize(records):
 groups=collections.defaultdict(lambda:collections.Counter());positions=collections.defaultdict(set);free=set();semantic=set()
 for r in records:
  q=r['question'];m,kind,_=mathematical(r);fs=q[':question/answer-fields'];layout=r['generation']['response_layout'];none=any(f[':answer-field/key']=='None of the above' for f in fs)
  group=f'{m.rows}x{m.cols-1}/{layout}/none={none}';groups[group][kind]+=1
  semantic.add(r['generation']['mathematical_fingerprint'])
  if layout=='checkbox':positions[group].add(next(i for i,f in enumerate(fs) if any(a[':answer/value']=='true' and a[':answer/id']==f[':answer-field/correct'][1] for a in f[':answer-field/choices'])))
  else:
   positions[group].add(next(i for i,a in enumerate(fs[0][':answer-field/choices']) if a[':answer/id']==fs[0][':answer-field/correct'][1]))
  if kind=='dependent':free.add(tuple(i for i in range(m.cols-1) if i not in m[:,:-1].rref()[1]))
 for group,counts in groups.items():
  expected={'dependent','inconsistent'} if group.startswith('2x3') else set(g.WORDS)
  assert set(counts)==expected,(group,counts)
  assert len(positions[group])>1,(group,positions[group])
 return {'semantic_instances':len(semantic),'records':len(records),'classifications_by_visible_group':{k:dict(v) for k,v in groups.items()},'correct_positions':{k:sorted(v) for k,v in positions.items()},'free_variable_positions':[list(t) for t in sorted(free)],'best_constant_classification_by_group':{k:{'successes':max(v.values()),'attempts':sum(v.values()),'uniform_class_baseline':1/len(v)} for k,v in groups.items()}}

def main():
 replays=source_replays();records=[];controlled=[];coverage={}
 for name,t in g.TEMPLATES.items():
  base=g.parse_matrix(t['math_components'][1]);expected={'dependent','inconsistent'} if base.rows<base.cols-1 else set(g.WORDS);seen=set()
  for seed in range(30):
   r=g.generate('moderate',seed,template=name);_,kind,_=mathematical(r);records.append(r);seen.add(kind)
   if seen==expected and seed>=4:break
  assert seen==expected,name;coverage[name]={'cases':sorted(seen),'samples':seed+1,'bank':t['profile']}
  # Vary only the contradiction constant in echelon form, then invert the same operations.
  n=base.cols-1;final=g.sp.zeros(base.rows,n+1);final[0,0]=1;final[0,1]=2;final[0,n]=3
  if n==3:final[0,2]=1
  for constant in [0,1]:
   z=final.copy();z[1,n]=constant
   for op in reversed(t['operations']):
    typ,i,*rest=op
    if typ=='swap':z.row_swap(i,rest[0])
    elif typ=='scale':z[i,:]/=g.sp.Rational(rest[0])
    else:j,c=rest;z[i,:]-=g.sp.Rational(c)*z[j,:]
   params={'matrix':[[str(x) for x in row] for row in z.tolist()],'order':list(g.WORDS)}
   r=g.generate('moderate',0,template=name,parameters=params);_,kind,_=mathematical(r)
   assert kind==('dependent' if constant==0 else 'inconsistent');controlled.append(r)
  # Same system, different category placement: classification preserved, visible key position changes.
  a=controlled[-2];p=copy.deepcopy(a['generation']['parameters']);p['order']=list(reversed(p['order']))
  b=g.generate('moderate',3,template=name,parameters=p);mathematical(b);assert v.system(a['question'][':question/problem'])==v.system(b['question'][':question/problem']);assert a['question'][':question/answer-fields']!=b['question'][':question/answer-fields'];controlled.append(b)
 # Keep a small regression sample for the preserved authored bands, including all outcomes.
 for level in ['easy','hard']:
  seen=set()
  for seed in range(15):
   r=g.generate(level,seed);_,kind,_=mathematical(r);records.append(r);seen.add(kind)
   if seen==set(g.WORDS) and seed>=4:break
  assert seen==set(g.WORDS)
 dump('test-records.json',records);dump('counterfactual-records.json',controlled)
 delivery_records=[r for r in records if r['question'][':question/difficulty'].endswith('/moderate')]
 dump('delivery-input.json',delivery_records)
 before=summarize(delivery_records)
 cmd=[PY,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/'delivery-input.json'),'--source',str(ROOT.parent/'source/source.json'),'--inventory',str(ROOT.parent/'source/inventory.json'),'--difficulty','moderate','--output',str(E/'delivery'),'--math-root','/media/jake/SSD/EDB/math']
 subprocess.run(cmd,check=True)
 accepted=json.loads((E/'delivery/accepted.json').read_text());after=summarize(accepted)
 fixtures=[{'label':str(i),'record':r,'checks':mathematical(r)[2]} for i,r in enumerate(replays+records+controlled+accepted)]
 dump('native-input.json',fixtures)
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'native-input.json'),str(E/'native-report.json')],check=True)
 dump('pedagogical-variation.json',{'passed':True,'before_delivery':before,'after_delivery':after,'per_source_schedule':coverage,'counterfactual_records':len(controlled),'counterfactual':'Only echelon contradiction constant changed, with the same inverse operations, category order and remaining echelon data. Classification, visible key, explanation and native grading change together. Reordering statements preserves the mathematical answer.','fixed_correct_count':'Exactly one of three mutually exclusive and exhaustive categories is true; None always false is a valid logical simplification.','selection_limit':'Offline shared publication filters exercised. Native question_selection.rs chooses eligible fresh IDs by difficulty; it does not inspect category values. Live learner history, dynamic inventory and database collisions were not exercised.','rejection':'Moderate sampler rejects only arithmetic/shape/echelon failures; case coverage measured after these retries. Two-equation three-unknown systems cannot be independent.','commands':['python checks/validate_repair.py','check_delivery.py (exact args in checks/validate_repair.py)','generate/runs/current/check-engine evidence/native-input.json evidence/native-report.json']})
 # Small render set: each response layout, dimensions, all outcomes, authored bands, and a source repair.
 selected=[replays[0],replays[-1]]
 criteria=[('moderate',2,4,'dependent'),('moderate',3,3,'independent'),('moderate',3,3,'inconsistent'),('easy',2,3,None),('hard',3,4,None)]
 for band,rows,cols,kind in criteria:
  selected.append(next(r for r in records if r['question'][':question/difficulty'].endswith('/'+band) and v.system(r['question'][':question/problem']).shape==(rows,cols) and (kind is None or r['generation']['classification']==kind)))
 dump('render-records.json',selected)
 print(json.dumps({'passed':True,'source_replays':len(replays),'sample_records':len(records),'counterfactual_records':len(controlled),'native_cases':len(fixtures),'delivery_accepted':len(accepted),'render_representatives':len(selected)}))
if __name__=='__main__':main()
