"""Read printed instances, source replay, target roles, and native learner grading."""
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def fingerprint(q):return g.signature(q)
def result(q):
 M=g.matrices(q[':question/problem'])
 return M[0]*M[1] if 'X+Y' in q[':question/problem'] else g.evaluate(g.expression(q),dict(zip('ABC',M[:3])))
def solution_check(q):
 R=result(q);fields=q[':question/answer-fields'];assert len({f[':answer-field/key'] for f in fields})==len(fields)
 assert q.get(':question/worked-solution') and g.matrices(q[':question/worked-solution'])[-1]==R,'Final worked matrix does not equal expanded matrix products'
 printed={}
 if 'X+Y' in q[':question/problem']:printed={'field-'+str(i+1):list(divmod(i,2)) for i in range(4)}
 else:
  printed=g.targets(q,R)
  rows=[x for x in q[':question/problem'].splitlines() if x.startswith('|') and '---' not in x]
  if rows:
   for i,row in enumerate(rows):
    for j,c in enumerate(row.split('|')[3:6]):
     if '{{' not in c:assert g.scalar(c.strip().strip('$'))==R[i,j],('Stale supplied entry',i,j)
 for f in fields:
  cr=f.get(':answer-field/correct');assert cr,'Missing canonical answer'
  cid=str(cr[':answer/id']) if isinstance(cr,dict) else cr[1]
  answers=f[':answer-field/choices'];correct=[a for a in answers if str(a[':answer/id'])==cid];assert len(correct)==1
  typ=f[':answer-field/type'];typ=typ.get(':db/ident') if isinstance(typ,dict) else typ
  if typ.endswith('/radio'):
   bank=[g.matrices(a[':answer/value'])[0] for a in answers];assert len(bank)==5 and len(set(tuple(v) for v in bank))==5
   assert g.matrices(correct[0][':answer/value'])[0]==R and bank.count(R)==1
  else:assert g.scalar(correct[0][':answer/value'])==R[tuple(printed[f[':answer-field/key']])]
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in fields for a in f[':answer-field/choices']]:assert text.count('{')==text.count('}') and text.count('$')%2==0
 return R

def independent(rec):
 q=rec['question'];m=rec['generation'];assert rec['knowledge_point']['db_id']==g.KP_ID
 solution_check(q);assert fingerprint(q)==m['parameter_fingerprint']
 assert rec==g.generate(q[':question/difficulty'].split('/')[-1],m['seed'],bank_profile=m['template'],parameters=m['parameters'])
def checks(r):
 out=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   out += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every source-bank option'} for a in f[':answer-field/choices']]
  else:
   value=f[':answer-field/choices'][0][':answer/value'];v=g.scalar(value)
   out += [{'field_index':i,'submitted':t,'expected':expect,'purpose':'Blank equivalence or incorrect value'} for t,expect in [(value,'accepted'),('('+value+')+0','accepted'),(g.s.latex(v+1),'rejected')]]
 return out

def main():
 records=[];replays=[];review=[];coverage={};components=[]
 for profile,q in g.SOURCES.items():
  level=q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1]
  if level not in g.SUPPORTED_LEVELS:
   components.append({'source':profile,'excluded':'Unrated, absent canonical answer and worked solution; preserved'});continue
  base=g.source_data(profile);params={'matrices':[[[str(v) for v in row] for row in M.tolist()] for M in base],'targets':{} if len(q[':question/answer-fields'])==1 else g.targets(q,result(q))}
  if profile=='q-138783':params['targets']={'field-'+str(i+1):list(divmod(i,2)) for i in range(4)}
  replay=g.generate(level,0,bank_profile=profile,parameters=params);independent(replay);solution_check(q)
  matched=total=0
  for f in q[':question/answer-fields']:
   rf=next(z for z in replay['question'][':question/answer-fields'] if z[':answer-field/key']==f[':answer-field/key'])
   math=lambda a:tuple(g.matrices(a[':answer/value'])[0]) if rf[':answer-field/type'].endswith('/radio') else g.scalar(a[':answer/value'])
   orig=[math(a) for a in f[':answer-field/choices']];new=[math(a) for a in rf[':answer-field/choices']];assert sorted(map(str,orig))==sorted(map(str,new)),profile
   matched+=len(orig);total+=len(orig)
  replays.append({'source':profile,'matched_options':matched,'total_options':total,'complete_bank':True,'missing':[],'extra':[],'matched_distractors':4 if len(q[':question/answer-fields'])==1 else 0})
  records.append(replay);variants=[]
  for seed in range(30):
   try:r=g.generate(level,seed,bank_profile=profile);independent(r)
   except AssertionError as error:
    if str(error)=='Colliding bank':continue
    raise
   variants.append(r);records.append(r)
  assert len(variants)>=10
  coverage[profile]={'instances':len(variants),'distinct_mathematical_tasks':len({fingerprint(r['question']) for r in variants}),'target_positions':{f[':answer-field/key']:sorted({tuple(r['generation']['parameters']['targets'][f[':answer-field/key']]) for r in variants}) for f in q[':question/answer-fields'] if not f[':answer-field/type'][':db/ident'].endswith('/radio')}}
  # Changed targets with all supplied matrices held constant. Verify rendered keys,
  # known table entries and solutions; an old key at a different-valued cell fails.
  if params['targets'] and profile!='q-138783':
   base_variant=variants[0];p=copy.deepcopy(base_variant['generation']['parameters']);R=result(base_variant['question']);taken={tuple(pos) for pos in p['targets'].values()};changed=False
   for key,pos in p['targets'].items():
    options=[(i,j) for i in range(3) for j in range(3) if (i,j) not in taken and g.category(R[i,j])==g.category(R[tuple(pos)]) and R[i,j]!=R[tuple(pos)]]
    if options:p['targets'][key]=list(options[0]);changed=True;break
   if changed:
    r=g.generate(level,base_variant['generation']['seed'],bank_profile=profile,parameters=p);independent(r)
    broken=copy.deepcopy(r);broken['question'][':question/answer-fields']=base_variant['question'][':question/answer-fields']
    try:solution_check(broken['question'])
    except AssertionError:coverage[profile]['stale_key_negative_control']=True
    else:raise AssertionError('Stale target accepted')
    review.append('Changed targets, fixed matrices:\n\n'+base_variant['question'][':question/problem']+'\n\n'+r['question'][':question/problem']);records.append(r)
  review.append('## '+profile+' original\n\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\nGenerated variant\n\n'+variants[0]['question'][':question/problem']+'\n\n'+variants[0]['question'][':question/worked-solution'])
  components.append({'source':profile,'level':level,'expression':'XZ+YZ' if profile=='q-138783' else g.expression(q),'fields':[{ 'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'original_correct':f[':answer-field/correct'][':answer/value']} for f in q[':question/answer-fields']], 'original_parameters':params})
 save('engine-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records])
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 save('source-bank-replay.json',replays);save('source-components.json',components);save('slot-coverage.json',coverage);save('validated-previews.json',records[:15]);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'status':'pass','basis':json.loads((HERE/'source.json').read_text())['basis'],'source_fidelity':{'complete_banks':len(replays),'matched_options':sum(r['matched_options'] for r in replays),'missing':0,'extra':0,'all_rated_source_keys_and_worked_results_checked':True,'notation':'Source prose and stages retained; matrix whitespace normalized, table markup normalized'},'mathematics':{'instances':len(records),'exact_expanded_matrix_products':True,'all_source_templates':True},'grading':engine,'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',ROOT/'generate/runs/current/check-engine']}})
if __name__=='__main__':main()
