"""Parse rendered mathematics independently; replay complete banks; actual grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('matrix_subtract',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def readmatrix(text):
 return sp.Matrix([[sp.sympify(v.strip().replace(r'\,','')) for v in row.split('&')] for row in text.split(r'\\')])
def check(r):
 q=r['question'];m=r['generation'];p=m['parameters'];t=m['template']
 assert r==g.generate('easy',m['seed'],t,p,m['replay'])
 prompt=g.MATRIX.findall(q[':question/problem']);a,b=map(readmatrix,prompt);c=a-b
 assert q[':question/difficulty']==':question.difficulty/easy'
 sol=[readmatrix(s) for s in g.MATRIX.findall(q[':question/worked-solution'])]
 assert sol[0]==a and sol[1]==b and sol[-1]==c and sol[-2]==c
 fs=q[':question/answer-fields'];radio=fs[0][':answer-field/type'].endswith('/radio')
 if radio:
  assert len(fs)==1 and len(fs[0][':answer-field/choices'])==5
  vals=[readmatrix(g.MATRIX.findall(answer[':answer/value'])[0]) for answer in fs[0][':answer-field/choices']]
  assert len(set(tuple(v) for v in vals))==5
  correct=[answer[':answer/id'] for answer,v in zip(fs[0][':answer-field/choices'],vals) if v==c]
  assert correct==[fs[0][':answer-field/correct'][1]]
 else:
  placeholders=re.findall(r'\{\{(field-\d+)\}\}',q[':question/problem']);assert sorted(placeholders)==sorted(f[':answer-field/key'] for f in fs)
  # Read target cells from rendered table, not generator target list.
  rows=[line for line in q[':question/problem'].splitlines() if line.startswith('|') and '---' not in line]
  cellvalues=[]
  for line in rows:
   for cell in line.split('|'):
    cell=cell.strip()
    if cell.startswith('{{') or re.fullmatch(r'\$-?\d+\$',cell):cellvalues.append(cell)
  assert len(cellvalues)==a.rows*a.cols
  answers={f[':answer-field/key']:f[':answer-field/choices'][0] for f in fs}
  for cell,value in zip(cellvalues,list(c)):
   if cell.startswith('{{'):
    answer=answers[cell[2:-2]];assert int(answer[':answer/value'])==value
   else:assert int(cell[1:-1])==value
  for f in fs:assert f[':answer-field/correct'][1]==f[':answer-field/choices'][0][':answer/id']
 assert g.fingerprint(q)==m['mathematical_fingerprint']
 return r
def native(label,r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete radio bank'} for a in f[':answer-field/choices'])
  else:
   n=int(f[':answer-field/choices'][0][':answer/value'])
   checks.extend({'field_index':i,'submitted':text,'expected':expected,'purpose':'actual integer blank equivalence/rejection'} for text,expected in [(str(n),'accepted'),('('+str(n)+')','accepted'),(str(2*n)+'/2','accepted'),(str(n+1),'rejected')])
 return {'label':label,'record':r,'checks':checks}
def main():
 replays=[];inputs=[];mapping=[];review=[];samples=[];coverage={t:set() for t in g.TEMPLATES}
 for t,q in g.SOURCES.items():
  r=check(g.generate('easy',0,t,g.original(t),True));f=q[':question/answer-fields'];rf=r['question'][':question/answer-fields']
  assert r['question'][':question/problem']==q[':question/problem'],t+' prompt'
  if ':question/worked-solution' in q:assert r['question'][':question/worked-solution']==q[':question/worked-solution'],t+' solution'
  total=0;distractors=0
  for sf in f:
   gf=next(x for x in rf if x[':answer-field/key']==sf[':answer-field/key'])
   original=[a[':answer/value'] for a in sf[':answer-field/choices']];generated=[a[':answer/value'] for a in gf[':answer-field/choices']]
   assert sorted(original)==sorted(generated),t+' bank'
   for sa in sf[':answer-field/choices']:
    matches=[a for a in gf[':answer-field/choices'] if a[':answer/value']==sa[':answer/value']];assert len(matches)==1
    iscorrect=matches[0][':answer/id']==gf[':answer-field/correct'][1]
    mapping.append({'source':t,'field':sf[':answer-field/key'],'source_answer_id':sa[':answer/id'],'value':sa[':answer/value'],'profile':t if len(original)>1 else None,'exactly_reproduced':True,'correct_derived':iscorrect});total+=1;distractors+=int(not iscorrect)
   if ':answer-field/correct' in sf:
    ans=next(a for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);assert ans[':answer/value']==sf[':answer-field/correct'][':answer/value']
  replays.append({'source':t,'source_db_id':q[':db/id'],'complete_bank_match':True,'matched_choices':total,'total_choices':total,'matched_distractors':distractors,'total_distractors':distractors,'exact_prompt':True,'exact_solution':':question/worked-solution' in q,'authored_missing_key_solution_rating':':question/worked-solution' not in q})
  inputs.append(native('replay-'+t,r));review.append('## Source '+t+'\n\n'+g.markdown(r))
  for seed in range(40):
   r=check(g.generate('easy',seed,t));assert r['question']==g.generate('easy',seed+999,t,r['generation']['parameters'])['question']
   samples.append(r);inputs.append(native(t+'-'+str(seed),r));coverage[t].update(r['generation']['parameters'].get('targets',range(len(r['generation']['parameters']['a']))))
  review.append('## Variant '+t+'\n\n'+g.markdown(samples[-1]))
 # Changing target cells with all matrix data held constant catches stale prompt/solution/key references.
 p=g.original('q-319625');r0=check(g.generate('easy',0,'q-319625',p));p['targets']=[0,2,3,4,6,7];r1=check(g.generate('easy',0,'q-319625',p));assert g.fingerprint(r0['question'])==g.fingerprint(r1['question']);inputs.extend([native('same-matrix-original-targets',r0),native('same-matrix-changed-targets',r1)])
 assert coverage['q-319625']==set(range(9))
 for t in g.TEMPLATES:
  # Domain ends/zero/equal entries, excluding ambiguous radio banks as required.
  if t.startswith('q-319'):
   n=len(g.original(t)['a']);p={'a':[-12,0,12]*(n//3)+[-12]*(n%3),'b':[12,0,-12]*(n//3)+[12]*(n%3)}
   if t=='q-319625':p['targets']=[0,1,2,3,4,5]
   inputs.append(native('boundaries-'+t,check(g.generate('easy',0,t,p))))
 for level in ('moderate','hard'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('Unsupported band accepted')
 save('source-choice-mapping.json',mapping);save('source-replay.json',{'passed':True,'basis':g.S['basis'],'profiles':replays,'matched_answer_values':sum(x['matched_choices'] for x in replays),'total_answer_values':sum(x['total_choices'] for x in replays),'complete_banks_matched':len(replays),'complete_banks_total':len(replays),'missing_or_extra_options':[],'unresolved_recipe_interpretations':['q-11478 repeated a00-a11 top row','q-11441 repeated a00, repeated c11, c01 replaced by c00','q-69603 compound mixed-cell transformations'],'note':'These exact value transformations are preserved; cognitive explanations are unresolved and never presented to learners.'})
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('previews.json',samples);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'sample_count':len(samples),'templates':7,'mathematics':'Independent rendered matrix subtraction, unique complete banks, rendered cell/key agreement, exact integer boundary checks','grading':'Actual learning::grade_field: all radio options, correct/equivalent/incorrect blank entries; no unresolved checks','coverage':{t:sorted(v) for t,v in coverage.items()},'changed_targets_fixed_matrices_checked':True,'source_fidelity':'All 7 complete banks and prompts; all 5 available solutions and keys exact; missing data authored only on new instances','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json')}})
 print('Validated all seven templates and 280 sampled easy instances')
if __name__=='__main__':main()
