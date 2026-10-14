"""Rendered-math validation, full bank replay, and actual engine grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('matrix_add',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def readmatrix(text):return sp.Matrix([[sp.sympify(v.strip()) for v in row.split('&')] for row in text.split(r'\\')])
def check(r):
 q=r['question'];m=r['generation'];p=m['parameters'];t=m['template']
 assert r==g.generate('easy',m['seed'],t,p,m['replay'])
 a,b=map(readmatrix,g.MATRIX.findall(q[':question/problem']));c=a+b
 assert q[':question/difficulty']==':question.difficulty/easy' and a.shape==b.shape and a.rows!=a.cols
 sol=[readmatrix(s) for s in g.MATRIX.findall(q[':question/worked-solution'])]
 assert sol[0]==a and sol[1]==b and sol[-1]==c and sol[-2]==c
 fs=q[':question/answer-fields'];radio=fs[0][':answer-field/type'].endswith('/radio')
 if radio:
  assert len(fs)==1 and len(fs[0][':answer-field/choices'])==5
  vals=[readmatrix(g.MATRIX.findall(ans[':answer/value'])[0]) for ans in fs[0][':answer-field/choices']]
  assert len(set(tuple(v) for v in vals))==5
  correct=[ans[':answer/id'] for ans,v in zip(fs[0][':answer-field/choices'],vals) if v==c]
  assert correct==[fs[0][':answer-field/correct'][1]]
 else:
  placeholders=re.findall(r'\{\{(field-\d+)\}\}',q[':question/problem']);assert placeholders==['field-'+str(j+1) for j in range(len(c))]
  assert len(fs)==len(c)==6
  for j,f in enumerate(fs):
   assert f[':answer-field/key']==placeholders[j] and int(f[':answer-field/choices'][0][':answer/value'])==c[j]
   assert f[':answer-field/correct'][1]==f[':answer-field/choices'][0][':answer/id']
 assert g.fingerprint(q)==m['mathematical_fingerprint']
 return r
def native(label,r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete radio bank'} for a in f[':answer-field/choices'])
  else:
   n=int(f[':answer-field/choices'][0][':answer/value'])
   checks.extend({'field_index':i,'submitted':text,'expected':expected,'purpose':'integer blank equivalence/rejection'} for text,expected in [(str(n),'accepted'),('('+str(n)+')','accepted'),(str(2*n)+'/2','accepted'),(str(n+1),'rejected')])
 return {'label':label,'record':r,'checks':checks}
def main():
 replays=[];inputs=[];mapping=[];review=[];samples=[];coverage={t:{'a':set(),'b':set()} for t in g.TEMPLATES}
 for t,q in g.SOURCES.items():
  r=check(g.generate('easy',0,t,g.original(t),True));fs=q[':question/answer-fields'];rf=r['question'][':question/answer-fields']
  assert r['question'][':question/problem']==q[':question/problem'],t+' prompt'
  if ':question/worked-solution' in q:assert r['question'][':question/worked-solution']==q[':question/worked-solution'],t+' solution'
  total=0;distractors=0
  for sf in fs:
   gf=next(x for x in rf if x[':answer-field/key']==sf[':answer-field/key'])
   original=[a[':answer/value'] for a in sf[':answer-field/choices']];generated=[a[':answer/value'] for a in gf[':answer-field/choices']]
   assert sorted(original)==sorted(generated),(t,'bank',original,generated)
   for sa in sf[':answer-field/choices']:
    matches=[a for a in gf[':answer-field/choices'] if a[':answer/value']==sa[':answer/value']];assert len(matches)==1
    iscorrect=matches[0][':answer/id']==gf[':answer-field/correct'][1]
    mapping.append({'source':t,'field':sf[':answer-field/key'],'source_answer_id':sa[':answer/id'],'source_parameters':g.original(t),'value':sa[':answer/value'],'profile':t if len(original)>1 else None,'recipe_index':generated.index(sa[':answer/value']) if len(original)>1 else 'cell-'+sf[':answer-field/key'],'exactly_reproduced':True,'correct_derived':iscorrect});total+=1;distractors+=int(not iscorrect)
   if ':answer-field/correct' in sf:
    ans=next(a for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);assert ans[':answer/value']==sf[':answer-field/correct'][':answer/value']
  replays.append({'source':t,'source_db_id':q[':db/id'],'complete_bank_match':True,'matched_choices':total,'total_choices':total,'matched_distractors':distractors,'total_distractors':distractors,'exact_prompt':True,'exact_solution':':question/worked-solution' in q,'authored_missing_key_solution_rating':':question/worked-solution' not in q})
  inputs.append(native('replay-'+t,r));review.append('## Original '+t+'\n\n'+q[':question/problem']+'\n\n'+q.get(':question/worked-solution','Original solution/key absent; new instance is completed independently.'))
  for seed in range(40):
   r=check(g.generate('easy',seed,t));assert r['question']==g.generate('easy',seed+999,t,r['generation']['parameters'])['question']
   samples.append(r);inputs.append(native(t+'-'+str(seed),r))
   for k in ('a','b'):coverage[t][k].update(r['generation']['parameters'][k])
  review.append('## Variant '+t+'\n\n'+g.markdown(samples[-1]))
  # Exhaust every scalar slot domain with the other operands held at a valid sample.
  base=samples[-1]['generation']['parameters'];boundaries=0;ambiguous=0
  for key in ('a','b'):
   for j in range(6):
    for val in range(-16,17):
     p={k:list(v) for k,v in base.items()};p[key][j]=val
     try:check(g.generate('easy',0,t,p))
     except AssertionError:
      vals=g.bank(t,p);assert vals is not None and len({tuple(v) for v in vals})<5;ambiguous+=1
     else:boundaries+=1
  replays[-1]['slot_domain_validated']=boundaries;replays[-1]['ambiguous_banks_excluded']=ambiguous
 for level in ('moderate','hard'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('Unsupported band accepted')
 assert all(v[k]==set(range(-16,17)) for v in coverage.values() for k in ('a','b'))
 save('source-choice-mapping.json',mapping);save('source-replay.json',{'passed':True,'basis':g.S['basis'],'profiles':replays,'matched_answer_values':sum(x['matched_choices'] for x in replays),'total_answer_values':sum(x['total_choices'] for x in replays),'complete_banks_matched':len(replays),'complete_banks_total':len(replays),'missing_or_extra_options':[],'recipe_interpretation':'Irregular compound errors preserve explicit source residual offsets; underlying cognitive mechanisms unresolved. See extraction and bank() for complete recipes.'})
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('previews.json',samples);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'sample_count':len(samples),'templates':7,'profiles':6,'mathematics':'Independent rendered non-square matrix addition; expanded arithmetic and answer matrices; complete unique banks; six blank cell/key agreement; exhaustive scalar slot perturbations with ambiguity exclusions','grading':'Actual learning::grade_field: all radio options; correct, equivalent and incorrect blank entries; no unresolved checks','coverage':{t:{k:sorted(v) for k,v in slots.items()} for t,slots in coverage.items()},'target_slots':'No variable subset or target position: six entries requested in full. Every operand entry is variable. Matrix orientations fixed per source template.','source_fidelity':'All 7 complete banks/prompts and all 5 available solutions/keys exact. Missing data authored only in new instances.','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json')}})
 print('Validated seven templates and 280 easy variants')
if __name__=='__main__':main()
