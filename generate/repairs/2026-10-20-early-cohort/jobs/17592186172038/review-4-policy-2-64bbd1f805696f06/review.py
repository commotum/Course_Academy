import os,sys,json,pathlib,hashlib,copy,collections,math
from audit import g,fields,answer,parse_rhs,independently_check,save,mirror_probe,visible_bank
ROOT=pathlib.Path.cwd();PKG=ROOT.parent/'workspace'
def load(n):return json.loads((ROOT/n).read_text())
def keyindex(r):return next(i for i,a in enumerate(fields(r)[':answer-field/choices']) if a[':answer/id']==fields(r)[':answer-field/correct'][1])
def main():
 save('package-before.json',{str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()})
 import importlib.metadata as md
 save('runtime.json',{'python':sys.version.split()[0],'packages':{v:md.version(v) for v in ['sympy','matplotlib']},'command':sys.argv})
 source=[]
 for i,(prof,(t,p,_)) in enumerate(g.PROFILES.items()):source.append(g.generate('easy',seed=862001+i,template=t,parameters=copy.deepcopy(p),profile=prof))
 source.append(g.generate('easy',seed=862008,template='quadratic_linear',parameters={'a':2,'b':1,'points':[[1,1],[0,1],[1,2]]},profile='q-80494'))
 save('source-replay-records.json',source);save('source-replay-math.json',[independently_check(r) for r in source])
 records=[];attempts=[];orig_sample=g.sample;orig_banks=g.banks
 def sample(l,t,r):
  p=orig_sample(l,t,r);attempts.append({'level':l,'template':t,'parameters':copy.deepcopy(p)});return p
 def banks(t,p,prof,alternatives=None):
  try:out=orig_banks(t,p,prof,alternatives)
  except ValueError as e:
   if attempts:attempts[-1]['outcome']=str(e)
   raise
  if attempts:attempts[-1]['outcome']='accepted bank'
  return out
 g.sample=sample;g.banks=banks
 for ti,t in enumerate(g.TEMPLATES):
  for i in range(4):
   r=g.generate('easy',seed=862100+ti*100+i,template=t);records.append(r)
   print('sample',t,r['generation']['seed'],'attempts',r['generation']['sampling_attempts'],flush=True)
  save('independent-samples.json',records);save('sampling-attempts.json',attempts)
 g.sample=orig_sample;g.banks=orig_banks
 save('math-results.json',[independently_check(r) for r in records])
 # Change only displayed equation within a fixed accepted coefficient bank, preserve all image bytes and order.
 cf=[];relations=[]
 for ti,t in enumerate(g.TEMPLATES):
  base=next(r for r in records if r['generation']['template']==t);bp=base['generation']['bank_parameters'];group=[]
  for p in bp:
   rr=g.generate('easy',seed=863000+ti,template=t,parameters=copy.deepcopy(p),bank_parameters=copy.deepcopy(bp));cf.append(rr);group.append(rr)
  assert len({answer(r)[':answer/value'] for r in group})==5
  assert all([a[':answer/value'] for a in fields(r)[':answer-field/choices']]==[a[':answer/value'] for a in fields(group[0])[':answer-field/choices']] for r in group)
  assert len({r['question'][':question/problem'] for r in group})==5
  assert len({r['question'][':question/worked-solution'] for r in group})==5
  relations.append({'template':t,'seed':863000+ti,'bank_parameters':bp,'question_ids':[r['question'][':question/id'] for r in group],'correct_positions':[keyindex(r)+1 for r in group],'same_order_and_pixels':True,'all_five_roles_observed':True})
 # Irrelevant presentation change: same fixed bank and equation, only random shuffle differs.
 base=cf[0];p=base['generation']['parameters'];bp=base['generation']['bank_parameters']
 irrelevant=g.generate('easy',seed=863199,template=base['generation']['template'],parameters=copy.deepcopy(p),bank_parameters=copy.deepcopy(bp));cf.append(irrelevant)
 assert answer(irrelevant)[':answer/value']==answer(base)[':answer/value']
 assert irrelevant['question'][':question/problem']==base['question'][':question/problem']
 assert irrelevant['question'][':question/worked-solution']==base['question'][':question/worked-solution']
 assert fields(irrelevant)[':answer-field/choices']!=fields(base)[':answer-field/choices']
 # Change one point with the equation fixed and all five coefficient cases fixed.
 t=base['generation']['template'];p2=copy.deepcopy(p);p2['points'][0]=[4,4]
 bp2=[{**copy.deepcopy(q),'points':copy.deepcopy(p2['points'])} for q in bp]
 point=g.generate('easy',seed=863000,template=t,parameters=p2,bank_parameters=bp2);cf.append(point)
 save('counterfactual-records.json',cf);save('counterfactual-math.json',[independently_check(r) for r in cf])
 save('counterfactual-results.json',{'fixed_banks':relations,'irrelevant_shuffle':{'base':base['question'][':question/id'],'after':irrelevant['question'][':question/id'],'same_prompt_solution_correct_pixels':True,'different_choice_order':True},'point_change':{'before':p,'after':p2,'old_slopes':base['generation']['exact_slopes'],'new_slopes':point['generation']['exact_slopes'],'unchanged_last_two':base['generation']['exact_slopes'][1:]==point['generation']['exact_slopes'][1:]}})
 boundary=g.generate('easy',seed=863210,template='affine',parameters={'a':1,'b':2,'points':[[-4,1],[4,-1],[1,4]]});assert boundary==g.generate('easy',seed=863210,template='affine',parameters={'a':1,'b':2,'points':[[-4,1],[4,-1],[1,4]]})
 save('boundary-records.json',[boundary]);save('boundary-results.json',{'deterministic_replay':True,'math':independently_check(boundary)})
 invalid=[('zero denominator','rational_square',{'a':1,'points':[[0,1],[1,2],[2,3]]}),('duplicate coordinates','affine',{'a':1,'b':2,'points':[[1,1],[1,1],[2,2]]}),('all banks collide at y=0','rational_square',{'a':1,'points':[[-1,0],[1,0],[2,0]]}),('outside coordinate guard','affine',{'a':1,'b':1,'points':[[5,1],[1,1],[2,1]]})]
 rej=[]
 for label,t,p in invalid:
  try:g.generate('easy',seed=863300,template=t,parameters=p);rej.append({'case':label,'rejected':False})
  except ValueError as e:rej.append({'case':label,'rejected':True,'error':str(e),'parameters':p,'template':t})
 assert all(r['rejected'] for r in rej);save('generator-rejections.json',rej)
 batch=json.loads((ROOT.parent/'samples.json').read_text());save('runner-batch.json',batch);save('runner-math.json',[independently_check(r) for r in batch])
 allrecords=source+records+cf+batch+[boundary];checks=[];solutions=[]
 for r in allrecords:
  independently_check(r);f=fields(r)
  checks.append({'label':str(r['generation']['seed'])+' '+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'unique match derived from visible equation and segment geometry'} for a in f[':answer-field/choices']]})
  text=r['question'][':question/worked-solution'];aligned=text.split('\\begin{aligned}',1)[1].split('\\end{aligned}',1)[0];parts=aligned.split(' \\\\ ');expr=parse_rhs(r['question'][':question/problem']);out=[]
  assert len(parts)==3
  for line in parts:
   import re
   pt=re.search(r'_\{\((.*?),(.*?)\)\}',line);x=parse_rhs('='+pt[1]);y=parse_rhs('='+pt[2]);expected=expr.subs({g.X:x,g.Y:y});values=[parse_rhs('='+v.rstrip(', .')) for v in line.split('=')[1:]]
   assert all(g.sp.simplify(v-expected)==0 for v in values),(line,values,expected)
   out.append({'line':line,'independent_expected':str(expected),'displayed_values':list(map(str,values))})
  solutions.append({'question_id':r['question'][':question/id'],'rows':out})
 # Every former correct choice from each fixed bank is checked against every new equation by above all-choice cases.
 save('grader-input.json',checks);save('worked-solution-checks.json',solutions)
 save('shortcut-results.json',[mirror_probe(r) for r in records]);save('runner-shortcuts.json',[mirror_probe(r) for r in batch])
 cov=[]
 for t in g.TEMPLATES:
  rr=[r for r in records if r['generation']['template']==t];cov.append({'template':t,'count':len(rr),'seeds':[r['generation']['seed'] for r in rr],'parameters':[r['generation']['parameters'] for r in rr],'slopes':[r['generation']['exact_slopes'] for r in rr],'positions':[keyindex(r)+1 for r in rr]})
 save('coverage-results.json',{'per_template':cov,'attempts':len(attempts),'accepted':len(records),'outcomes':dict(collections.Counter(a['outcome'] for a in attempts))})
 (ROOT/'session-state.md').write_text('Source and sample milestone complete: 8 source replays, 24 fresh samples, 32 controlled records, boundary and 5 runner cases. Exact prompt/image/solution math passed. Grader input ready; execute native grader, delivery, UI, relocation and inventory checks next.\n')
 print('math/solution cases',len(allrecords),'fixed-bank role checks',len(cf),flush=True)
if __name__=='__main__':main()
