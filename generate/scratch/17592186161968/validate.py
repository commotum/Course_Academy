"""Independent rendered matrix, option and solution checks plus real application grader."""
import copy,hashlib,importlib.util,json,re,subprocess,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=int)+'\n')
def fingerprint(q):return g.fingerprint(q[':question/problem'] if isinstance(q,dict) else q)
def solution_check(q):
 A,B=g.matrices(q[':question/problem'])[:2];p=g.source_parameters(q);pivot=p['pivot'];cols=[c for c in range(3) if c!=pivot]
 fields=q[':question/answer-fields'];assert len(fields)==1,'Duplicate field keys are ungradable'
 f=fields[0];assert f[':answer-field/key']=='selection';t=f[':answer-field/type'];assert (t.get(':db/ident') if isinstance(t,dict) else t)==':answer-field.type/radio'
 values=[]
 for a in f[':answer-field/choices']:
  ops=g.operations(a[':answer/value']);assert len(ops)==2 and [c for c,_,_ in ops]==cols and all(piv==pivot for _,piv,_ in ops)
  result=A.copy()
  for c,piv,k in ops:result[:,c]=result[:,c]+k*result[:,piv]
  values.append((tuple(k for _,_,k in ops),result==B))
 assert len(values)==5 and len(set(v[0] for v in values))==5 and sum(v[1] for v in values)==1
 cr=f[':answer-field/correct'];cid=str(cr[':answer/id']) if isinstance(cr,dict) else cr[1];assert str(f[':answer-field/choices'][[v[1] for v in values].index(True)][':answer/id'])==cid
 stages=g.matrices(q[':question/worked-solution']);assert len(stages)==3 and stages[0]==A
 current=A.copy()
 for c,stage in zip(cols,stages[1:]):
  current[:,c]=current[:,c]+p['ks'][c]*current[:,pivot];assert stage==current,'Incorrect displayed intermediate matrix'
 assert current==B
 solution=q[':question/worked-solution'];assert str(p['row']+1)+str(pivot+1) in solution
 ops=g.operations(solution);assert ops==[(c,pivot,p['ks'][c]) for c in cols]*2,'Stale target/operation references'
 for text in [q[':question/problem'],solution]+[a[':answer/value'] for a in f[':answer-field/choices']]:assert text.count('{')==text.count('}') and text.count('$')%2==0
 return p

def independent(r):
 q=r['question'];m=r['generation'];assert r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['id']==g.KP_UUID
 assert q[':question/difficulty']==':question.difficulty/easy'
 p=solution_check(q);assert p==m['parameters'];assert fingerprint(q)==m['parameter_fingerprint']
 assert r==g.generate('easy',m['seed'],bank_profile=m['bank_profile'],parameters=m['parameters'])
 ids=[q[':question/id']]+[f[':answer-field/id'] for f in q[':question/answer-fields']]+[a[':answer/id'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']];assert len(ids)==len(set(ids));[uuid.UUID(i) for i in ids]
def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every option through actual learner grader'} for a in f[':answer-field/choices']]
def main():
 replay=[];records=[];review=[];components=[]
 for profile,q in g.SOURCES.items():
  p=g.ORIGINAL[profile];cols=[c for c in range(3) if c!=p['pivot']];a,b=[p['ks'][c] for c in cols];bank=g.recipes(profile,a,b)
  for f in q[':question/answer-fields']:
   source_bank=[tuple(k for _,_,k in g.operations(x[':answer/value'])) for x in f[':answer-field/choices']]
   assert sorted(source_bank)==sorted(bank) and len(set(bank))==5,(profile,source_bank,bank)
   if ':answer-field/correct' in f:assert tuple(k for _,_,k in g.operations(f[':answer-field/correct'][':answer/value']))==(a,b)
   replay.append({'source':profile,'field_id':str(f[':answer-field/id']),'complete_bank':True,'matched':5,'total':5,'matched_distractors':4,'total_distractors':4,'correct_pair':[a,b],'key_present':':answer-field/correct' in f,'missing_options':[],'extra_options':[]})
   components.append({'source':profile,'field_id':str(f[':answer-field/id']),'parameters':p,'correct_pair':[a,b],'options':[{'source_answer':str(x[':answer/id']),'exact_value':x[':answer/value'],'recipe_index':bank.index(coeff),'evaluated_recipe':coeff} for x,coeff in zip(f[':answer-field/choices'],source_bank)]})
  r=g.generate(bank_profile=profile,parameters=p);independent(r);records.append(r)
  corrected=copy.deepcopy(q);corrected[':question/answer-fields']=[f for f in corrected[':question/answer-fields'] if ':answer-field/correct' in f]
  if profile=='q-91187':
   try:solution_check(corrected)
   except AssertionError:pass
   else:raise AssertionError('Known source error undetected')
   corrected[':question/worked-solution']=corrected[':question/worked-solution'].replace(r'${C}_{1}:={C}_{1}-{C}_{2}',r'${C}_{2}:={C}_{2}-{C}_{1}')
  solution_check(corrected)
  review.append('## '+profile+' original\n\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\nReplay (corrected when source error recorded)\n\n'+g.markdown(r))
 variants=g.batch('easy',450,20261014)
 for r in variants:independent(r)
 records+=variants
 coverage={slot:sorted({r['generation']['parameters'][slot] for r in variants}) for slot in ('row','pivot')}
 combinations={(r['generation']['parameters']['row'],r['generation']['parameters']['pivot']) for r in variants};assert len(combinations)==9
 assert set(r['generation']['bank_profile'] for r in variants)==set(g.PROFILES)
 # Same mathematical A, same zero row; change retained pivot and both requested column roles.
 changed=[]
 A=[[2,-2,6],[1,7,-2],[3,-1,5]]
 for p in (0,1):
  params={'A':A,'row':0,'pivot':p,'ks':[int(-A[0][c]/A[0][p]) if c!=p else 0 for c in range(3)]}
  r=g.generate(bank_profile='q-130609',parameters=params);independent(r);changed.append(r);records.append(r)
 broken=copy.deepcopy(changed[1]);broken['question'][':question/worked-solution']=changed[0]['question'][':question/worked-solution']
 try:solution_check(broken['question'])
 except AssertionError:pass
 else:raise AssertionError('Stale target references passed')
 review.append('## Changed pivot with A held constant\n\n'+'\n\n'.join(g.markdown(r) for r in changed))
 for band in ('moderate','hard'):
  try:g.generate(band)
  except ValueError:pass
  else:raise AssertionError('Unsupported level accepted')
 a=g.generate(seed=1,parameters=g.ORIGINAL[g.PROFILES[0]],bank_profile=g.PROFILES[0]);b=g.generate(seed=2,parameters=g.ORIGINAL[g.PROFILES[0]],bank_profile=g.PROFILES[0]);assert a['question']==b['question']
 save('engine-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records]);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 save('source-components.json',components);save('source-bank-replay.json',replay);save('slot-coverage.json',{'slots':coverage,'row_pivot_combinations':len(combinations),'eligible_combinations':9,'profile_coverage':list(g.PROFILES),'changed_pivot_fixed_A_negative_control':True});save('validated-previews.json',records);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'status':'pass','basis':json.loads((HERE/'source.json').read_text())['basis'],'source_fidelity':{'complete_banks':len(replay),'complete_options':len(replay)*5,'distractors':len(replay)*4,'source_solution_sequences_checked':9,'source_errors':['q-91187 conclusion reverses C2:=C2-C1 to C1:=C1-C2; generated conclusion corrected from matrix stages'],'ungradable_sources':['q-42917 duplicate selection field, one without key; preserved and excluded']},'mathematics':{'instances_checked':len(records),'matrix_stages_checked':len(records)*3,'all_9_target_role_combinations':True},'grading':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':0},'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',ROOT/'generate/runs/current/check-engine']}})
if __name__=='__main__':main()
