"""Independently parse rendered matrices and row operations, replay every source bank."""
import copy,hashlib,importlib.util,json,re,subprocess,uuid,itertools
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=int)+'\n')
def fingerprint(q):return g.fingerprint(q[':question/problem'] if isinstance(q,dict) else q)
def solution_check(q):
 A,B=g.matrices(q[':question/problem'])[:2];p=g.source_parameters(q);pivot=p['pivot'];targets=[r for r in range(3) if r!=pivot]
 fields=q[':question/answer-fields'];assert len(fields)==1,'Duplicate fields are ungradable'
 f=fields[0];assert f[':answer-field/key']=='selection';t=f[':answer-field/type'];assert (t.get(':db/ident') if isinstance(t,dict) else t)==':answer-field.type/radio'
 values=[]
 for a in f[':answer-field/choices']:
  ops=g.operations(a[':answer/value']);assert len(ops)==2 and [r for r,_,_ in ops]==targets and all(piv==pivot for _,piv,_ in ops)
  values.append(tuple(k for _,_,k in ops))
 correct=tuple(p['ks'][r] for r in targets);assert len(values)==5 and len(set(values))==5 and values.count(correct)==1
 # Check each complete option as actual simultaneous row transformations.
 for coeff in values:
  trial=A.copy()
  for r,k in zip(targets,coeff):trial[r,:]=A[r,:]+k*A[pivot,:]
  assert (trial==B)==(coeff==correct)
 cr=f[':answer-field/correct'];cid=str(cr[':answer/id']) if isinstance(cr,dict) else cr[1];assert str(f[':answer-field/choices'][values.index(correct)][':answer/id'])==cid
 stages=g.matrices(q[':question/worked-solution']);assert len(stages)==3 and stages[0]==A
 current=A.copy()
 for r,stage in zip(targets,stages[1:]):
  current[r,:]=current[r,:]+p['ks'][r]*current[pivot,:];assert stage==current,'Incorrect displayed intermediate matrix'
 assert current==B
 solution=q[':question/worked-solution'];assert str(pivot+1)+str(p['column']+1) in solution
 direction=('above' if pivot==2 else 'below' if pivot==0 else 'above and below');assert 'entries '+direction+' ' in solution
 if r'\xrightarrow' in solution:
  ops=g.operations(solution);assert ops==[(r,pivot,p['ks'][r]) for r in targets]*2,'Stale target/operation references'
 for text in [q[':question/problem'],solution]+[a[':answer/value'] for a in f[':answer-field/choices']]:assert text.count('{')==text.count('}') and text.count('$')%2==0
 return p

def independent(r):
 q=r['question'];m=r['generation'];assert r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['id']==g.KP_UUID
 assert q[':question/difficulty']==':question.difficulty/easy'
 p=solution_check(q);assert p==m['parameters']
 assert fingerprint(q)==m['parameter_fingerprint']
 assert r==g.generate('easy',m['seed'],bank_profile=m['bank_profile'],parameters=m['parameters'])
 ids=[q[':question/id']]+[f[':answer-field/id'] for f in q[':question/answer-fields']]+[a[':answer/id'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']];assert len(ids)==len(set(ids));[uuid.UUID(i) for i in ids]
def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every radio option through application grader'} for a in f[':answer-field/choices']]
def main():
 replay=[];records=[];review=[];extraction=[]
 for profile,q in g.SOURCES.items():
  p=g.ORIGINAL[profile];targets=[r for r in range(3) if r!=p['pivot']];a,b=[p['ks'][r] for r in targets];bank=g.recipes(profile,a,b)
  mapped=[]
  for f in q[':question/answer-fields']:
   source_bank=[tuple(k for _,_,k in g.operations(x[':answer/value'])) for x in f[':answer-field/choices']]
   assert sorted(source_bank)==sorted(bank) and len(set(bank))==5,(profile,source_bank,bank)
   if ':answer-field/correct' in f:assert tuple(k for _,_,k in g.operations(f[':answer-field/correct'][':answer/value']))==(a,b)
   replay.append({'source':profile,'field_id':f[':answer-field/id'],'complete_bank':True,'matched':5,'total':5,'matched_distractors':4,'total_distractors':4,'correct_pair':[a,b],'key_present':':answer-field/correct' in f,'missing_options':[],'extra_options':[]})
   mapped.extend({'field_id':f[':answer-field/id'],'source_answer_id':x[':answer/id'],'source_value':x[':answer/value'],'coefficient_pair':source_bank[i],'recipe_index':bank.index(source_bank[i]),'reproduces_complete_value':True} for i,x in enumerate(f[':answer-field/choices']))
  r=g.generate(bank_profile=profile,parameters=p);independent(r);records.append(r)
  completed=copy.deepcopy(q);completed[':question/answer-fields']=[f for f in q[':question/answer-fields'] if ':answer-field/correct' in f];solution_check(completed)
  extraction.append({'source':profile,'difficulty':'easy','template':'row-zero-3x3','parameters':p,'pivot_value':p['A'][p['pivot']][p['column']],'choice_profile':profile,'choice_mapping':mapped,'prompt':q[':question/problem'],'solution':q[':question/worked-solution'],'field_count':len(q[':question/answer-fields']),'duplicate_fields_preserved':len(q[':question/answer-fields'])>1})
  review.append('## '+profile+' original\n\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\nReplay\n\n'+g.markdown(r))
 variants=g.batch('easy',600,20261014)
 for r in variants:independent(r)
 records+=variants
 coverage={slot:sorted({r['generation']['parameters'][slot] for r in variants}) for slot in ('pivot','column')}
 assert all(coverage[k]==list(range(3)) for k in coverage)
 combos={(r['generation']['parameters']['pivot'],r['generation']['parameters']['column']) for r in variants};assert len(combos)==9
 assert set(r['generation']['bank_profile'] for r in variants)==set(g.PROFILES)
 # All signed coefficient/pivot bounds for each source bank. Collision rejection is explicit.
 bounded=[];rejections=0
 for profile in g.PROFILES:
  for p,c,pv,a,b in itertools.product(range(3),range(3),[-3,-2,-1,1,2,3],[-9,-2,-1,1,2,9],[-9,-2,-1,1,2,9]):
   bank=g.recipes(profile,a,b)
   if len(set(bank))!=5:rejections+=1;continue
   A=[[7,-4,5],[3,8,-6],[-5,4,9]];targets=[r for r in range(3) if r!=p];A[p][c]=pv
   ks=[0,0,0]
   for r,k in zip(targets,[a,b]):A[r][c]=-k*pv;ks[r]=k
   s=g.generate(bank_profile=profile,parameters={'A':A,'pivot':p,'column':c,'ks':ks});solution_check(s['question']);bounded.append((profile,p,c,pv,a,b))
 # Same A, changed pivot or eliminated column: changed relation, all references recomputed.
 fixed=[[1,1,5],[1,2,2],[2,3,4]];changed=[]
 for p,c in [(0,0),(1,0),(0,1)]:
  ks=[-fixed[r][c]//fixed[p][c] if r!=p else 0 for r in range(3)]
  s=g.generate(bank_profile='q-91163',parameters={'A':fixed,'pivot':p,'column':c,'ks':ks});independent(s);changed.append(s);records.append(s)
 for s in changed[1:]:
  broken=copy.deepcopy(s);broken['question'][':question/worked-solution']=changed[0]['question'][':question/worked-solution']
  try:solution_check(broken['question'])
  except AssertionError:pass
  else:raise AssertionError('Stale target references passed')
 review.append('## Changed pivot/column, A held constant\n\n'+'\n\n'.join(g.markdown(r) for r in changed))
 for band in ('moderate','hard'):
  try:g.generate(band)
  except ValueError:pass
  else:raise AssertionError('Unsupported level accepted')
 a=g.generate(seed=1,parameters=g.ORIGINAL[g.PROFILES[0]],bank_profile=g.PROFILES[0]);b=g.generate(seed=2,parameters=g.ORIGINAL[g.PROFILES[0]],bank_profile=g.PROFILES[0]);assert a['question']==b['question']
 save('engine-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records]);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 save('source-bank-replay.json',replay);save('source-extraction.json',extraction);save('slot-coverage.json',{'slots':coverage,'pivot_column_combinations':len(combos),'eligible_combinations':9,'profile_coverage':list(g.PROFILES),'bounded_valid_cases':len(bounded),'bounded_bank_collisions_rejected':rejections,'stale_target_negative_controls':2});save('validated-previews.json',records);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'status':'pass','basis':json.loads((HERE/'source.json').read_text())['basis'],'source_fidelity':{'complete_banks':len(replay),'complete_options':len(replay)*5,'distractors':len(replay)*4,'source_solution_sequences_checked':10,'source_notation':'Normalized R braces/spacing; operation pairs compared exactly; preserved three matrix stages and solution sentences','missing_original_fields':'Duplicate/missing keys preserved and excluded from inventory'},'mathematics':{'instances_checked':len(records),'bounded_cases':len(bounded),'all_9_target_role_combinations':True},'grading':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':0},'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',ROOT/'generate/runs/current/check-engine']}})
if __name__=='__main__':main()
