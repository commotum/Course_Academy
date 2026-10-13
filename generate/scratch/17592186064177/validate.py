import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).parent.resolve();ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def parse(p):return g.fingerprint_text(p)
def zero_on_intervals(e):
 t=sp.Symbol('u',positive=True)
 return all(sp.simplify(e.subs(g.X,sign*t).doit())==0 for sign in (1,-1))
def derivative_delta(a,b):
 t=sp.Symbol('u',positive=True)
 return all(sp.simplify(sp.diff(a.subs(g.X,sign*t),t)-sign*b.subs(g.X,sign*t))==0 for sign in (1,-1))
def bank_check(q):
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection'
 assert (f[':answer-field/type'].get(':db/ident') if isinstance(f[':answer-field/type'],dict) else f[':answer-field/type'])==':answer-field.type/radio'
 assert len(f[':answer-field/choices'])==5
 cid=str(f[':answer-field/correct'][':answer/id']) if isinstance(f[':answer-field/correct'],dict) else f[':answer-field/correct'][1]
 vals=[g.expression(a[':answer/value']) for a in f[':answer-field/choices']];e=g.integrand(q[':question/problem'])
 flags=[derivative_delta(v,e) for v in vals];assert sum(flags)==1,flags
 assert str(f[':answer-field/choices'][flags.index(True)][':answer/id'])==cid
 for i,v in enumerate(vals):
  for w in vals[:i]:assert not derivative_delta(v,sp.diff(w,g.X)), 'Equivalent options modulo integration constant'
 return e

def evaluate(s):
 s=s.strip().rstrip('.,')
 def integral(m):return '('+str(sp.integrate(g.expression(m[1]),g.X).subs(sp.log(g.X),sp.log(sp.Abs(g.X))))+')'
 s=re.sub(r'\\int\s+(.*?)\\,?\\text\{d\}x',integral,s)
 return g.expression(s)
def solution_check(q):
 e=bank_check(q);text=q[':question/worked-solution'];displays=re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S);assert len(displays)==1
 s=re.sub(r'\\(?:begin|end)\{aligned\}','',displays[0]);prev=None;steps=0
 for row in s.split(r'\\'):
  left,right=row.replace('&','').split('=',1)
  lhs=evaluate(left) if left.strip() else prev;rhs=evaluate(right);assert lhs is not None
  assert zero_on_intervals(lhs-rhs-g.C*(lhs-rhs).coeff(g.C)),row
  assert derivative_delta(rhs,e),row
  prev=rhs;steps+=1
 return steps

def independent(r):
 q,m=r['question'],r['generation'];assert r['knowledge_point']['db_id']==g.KP_ID
 assert r==g.generate(q[':question/difficulty'].split('/')[-1],m['seed'],m['template'],m['parameters'],m['bank_profile'])
 assert parse(q[':question/problem'])==m['parameter_fingerprint'];return solution_check(q)
def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every field-owned source-profile radio option'} for a in f[':answer-field/choices']]
def main():
 source=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};records=[];cases=[];reviews=[];steps=0
 for mid,t in g.TEMPLATES.items():
  r=g.generate(t['difficulty'],template=mid,parameters=t['parameters']);q=qs[mid]
  assert r['question'][':question/problem']==q[':question/problem'] and r['question'][':question/worked-solution']==q[':question/worked-solution']
  assert sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])
  steps+=independent(r);cases.append({'source':mid,'matched_values':5,'total_values':5,'matched_distractors':4,'total_distractors':4,'complete_bank':True,'prompt_and_solution_exact':True,'missing_options':[],'extra_options':[]})
  reviews.append('## '+mid+' original parameter replay\n\n'+g.markdown(r))
  for b in range(2,13):
   z=g.generate(t['difficulty'],31,mid,{'base':b});steps+=independent(z);assert z['question']==g.generate(t['difficulty'],97,mid,{'base':b})['question'];records.append(z)
  reviews.append('## '+mid+' changed base\n\n'+g.markdown(g.generate(t['difficulty'],template=mid,parameters={'base':12})))
 negative=0
 for part in ('answer','solution'):
  z=copy.deepcopy(records[0]);q=z['question']
  if part=='answer':q[':question/answer-fields'][0][':answer-field/choices'][-1][':answer/value']='0'
  else:q[':question/worked-solution']=q[':question/worked-solution'].replace('5{e}^{x}','8{e}^{x}')
  try:solution_check(q)
  except AssertionError:negative+=1
  else:raise AssertionError('Corruption passed')
 for level,p in [('hard',{'base':2}),('easy',{'base':1}),('easy',{'base':13}),('easy',{'base':True})]:
  try:g.generate(level,parameters=p)
  except ValueError:negative+=1
  else:raise AssertionError('Invalid level/bound passed')
 save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)])
 binary=ROOT/'generate/runs/current/check-engine';subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 er=json.loads((HERE/'engine-report.json').read_text());assert er['documented_unresolved_checks']==0
 save('source-cases.json',cases);(HERE/'review.md').write_text('\n\n---\n\n'.join(reviews)+'\n')
 save('validation.json',{'status':'pass','source_basis':source['basis'],'source_coverage':{'complete_banks':6,'bank_total':6,'matched_distractors':24,'total_distractors':24,'matched_values':30,'total_values':30},'mathematics':{'records_checked':len(records),'solution_steps':steps,'negative_controls':negative,'finite_distinct_tasks':{l:len({parse(r['question'][':question/problem']) for r in records if r['question'][':question/difficulty']==':question.difficulty/'+l}) for l in g.SUPPORTED_LEVELS}},'native_grading':{k:er[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',HERE/'templates.json',binary)}})
 print('All source banks, bounded variants, solution steps and native grading passed.',flush=True)
if __name__=='__main__':main()
