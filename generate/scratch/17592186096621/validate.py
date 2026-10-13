"""Independent displayed expressions, full source-bank replay and real grader."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from math_parser import scalar
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def eq(a,b):return s.trigsimp(s.expand(s.together(a-b).as_numer_denom()[0]))==0
def correct(field):
 return str(field[':answer-field/correct'][':answer/id']) if isinstance(field[':answer-field/correct'],dict) else field[':answer-field/correct'][1]
def function_and_point(q):
 p=q[':question/problem'];text=p[p.index('=')+1:];f=scalar(text[:text.index('$')].strip().rstrip(','))
 point=None
 if 'slope of the tangent' in p:
  text=p[p.rindex('$x=')+3:];point=scalar(text[:text.index('$')])
 return f,point
def question_math(q):
 f,t=function_and_point(q);X=next(iter(f.free_symbols))
 target=s.diff(f,X);target=target if t is None else target.subs(X,t)
 field=q[':question/answer-fields'][0];values=[scalar(a[':answer/value']) for a in field[':answer-field/choices']]
 valid=[eq(a,target) for a in values];assert sum(valid)==1,(q[':question/problem'],target,values)
 assert str(field[':answer-field/choices'][valid.index(True)][':answer/id'])==correct(field)
 assert all(not eq(a,b) for i,a in enumerate(values) for b in values[:i])
 return f,t,target

def solution_steps(rec):
 q=rec['question'];f,t,target=question_math(q);X=g.X;level=q[':question/difficulty'].split('/')[-1]
 displays=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
 count=0
 for index,display in enumerate(displays):
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',display)
  for row in text.split(r'\\'):
   rhs=row.split('&=')[1].strip().rstrip('.')
   if 'prime' in rhs:continue # first two formal quotient-rule/substitution rows
   value=scalar(rhs);expected=target if index==1 else s.diff(f,X)
   assert eq(value,expected),(rhs,expected,value);count+=1
 assert len(displays)==(2 if level=='moderate' else 1) and count==({'easy':4,'moderate':6,'hard':2}[level])
 # Derivative markers in formal rows and explicit function decomposition.
 assert r'\frac{u^{\prime}(x)\cdot v(x)-u(x)\cdot v^{\prime}(x)}{[v(x)]^{2}}' in q[':question/worked-solution']
 return count

def check(rec):
 assert rec['knowledge_point']['db_id']==g.KP_ID and rec['knowledge_point']['id']==g.KP_UUID
 m=rec['generation'];q=rec['question'];level=q[':question/difficulty'].split('/')[-1]
 assert rec==g.generate(level,m['seed'],m['template'],m['parameters'],m['profile'])
 question_math(q);solution_steps(rec)
 assert g.fingerprint(q)==m['mathematical_fingerprint']
 f=q[':question/answer-fields'][0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 ids=[q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]
 assert len(set(ids))==len(ids)
 for value in ids:uuid.UUID(value)
 for text in (q[':question/problem'],q[':question/worked-solution']):
  assert text.count('$')%2==0 and text.count('{')==text.count('}')
 return True

def source_normal(q):
 q=copy.deepcopy(q)
 q[':question/id']=str(q[':question/id'])
 if ':question/difficulty' in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q.get(':question/answer-fields',[]):
  f[':answer-field/id']=str(f[':answer-field/id']);f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
  for a in f[':answer-field/choices']:
   a[':answer/id']=str(a[':answer/id']);a[':answer/type']=a[':answer/type'][':db/ident']
 return q

def native(label,rec):
 checks=[]
 for i,f in enumerate(rec['question'][':question/answer-fields']):
  if f[':answer-field/type']==':answer-field.type/radio':
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct(f) else 'rejected','purpose':'Every choice through actual ID-selection grader'} for a in f[':answer-field/choices'])
  else:
   value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct(f))
   checks.extend([{'field_index':i,'submitted':value,'expected':'accepted','purpose':'Canonical blank answer'},{'field_index':i,'submitted':'('+value+')','expected':'accepted','purpose':'Equivalent parentheses'},{'field_index':i,'submitted':'0','expected':'rejected','purpose':'Incorrect zero'}])
 return {'label':label,'record':rec,'checks':checks}

def main():
 sources={q[':question/math-academy-id']:q for q in g.KP[':knowledge-point/questions']}
 banks=[]
 for mid,(level,c) in g.DATA.items():
  rec=g.generate(level,100,mid,{'c':c},'observed');check(rec)
  q=source_normal(sources[mid]);question_math(q)
  a=q[':question/answer-fields'][0];b=rec['question'][':question/answer-fields'][0]
  mapping=[]
  for choice in a[':answer-field/choices']:
   matches=[v for v in b[':answer-field/choices'] if eq(scalar(choice[':answer/value']),scalar(v[':answer/value']))]
   assert len(matches)==1
   assert (choice[':answer/id']==correct(a))==(matches[0][':answer/id']==correct(b))
   mapping.append({'source_id':choice[':answer/id'],'source_value':choice[':answer/value'],'generated_value':matches[0][':answer/value'],'matched':True})
  assert len(a[':answer-field/choices'])==len(b[':answer-field/choices'])==5
  banks.append({'source':mid,'complete_bank':True,'choices_matched':5,'distractors_matched':4,'mapping':mapping})
 save('source-replay.json',{'supported_banks_matched':2,'supported_banks_total':2,'distractors_matched':8,'distractors_total':8,'unimplemented_banks_not_claimed_faithful':['q-17921','q-47999','q-47943','q-47998','q-48504'],'banks':banks})
 records=[g.generate(level,c,parameters={'c':c}) for level in ('easy','moderate') for c in range(1,21)]+[g.generate('hard',a*10+b,parameters={'a':a,'b':b}) for a in range(1,4) for b in range(1,4)]
 for rec in records:check(rec)
 assert len({r['generation']['mathematical_fingerprint'] for r in records})==49
 for rec in records:
  other=g.generate(rec['question'][':question/difficulty'].split('/')[-1],999,parameters=rec['generation']['parameters'])
  assert other['question'][':question/id']==rec['question'][':question/id'] and other['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
 cases=[];usable=[];excluded=[]
 for mid,source in sources.items():
  if mid in ('q-17921','q-47999'):excluded.append({'source':mid,'reason':'Unrated; no canonical answer or worked solution'});continue
  if mid=='q-9908':excluded.append({'source':mid,'reason':'No answer field'});continue
  if mid in ('q-167328','q-167782'):excluded.append({'source':mid,'reason':'Prompt omits definitions of f,h; second template has broken fraction table'});continue
  q=source_normal(source);question_math(q)
  rec={'knowledge_point':{'title':g.KP[':knowledge-point/title']},'question':q,'generation':{'template':mid}}
  cases.append(native(mid,rec));usable.append(mid)
 cases.extend(native(r['question'][':question/id'],r) for r in records)
 save('native-input.json',cases)
 subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 save('previews.json',records)
 save('source-validation.json',{'mathematically_and_natively_validated_sources':usable,'excluded_sources':excluded})
 hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'math_parser.py',HERE/'source.json',HERE/'source.edn',HERE/'source-replay.json',HERE/'native-report.json',HERE/'previews.json')}
 save('validation.json',{'passed':True,'distinct_tasks':49,'by_level':{'easy':20,'moderate':20,'hard':9},'complete_source_banks':'2/2','source_distractors':'8/8','all_displayed_evaluated_solution_steps_checked':True,'deterministic_replay':True,'identity_ignores_choice_order_and_seed':True,'real_grader_entry_point':'course_academy_engine::learning::grade_field','hashes':hashes,'dependencies':{'sympy':s.__version__},'fidelity_limits':'Two observed profiles (q-2385 and q-48507) and one explicitly authored hard operation profile supported; normalized notation and equivalent simplified solution rows, unchanged quotient-rule sequence; other source families are excluded from generator support, not deleted.'})
 print(json.dumps({'passed':True,'records':49,'usable_sources':usable,'excluded_sources':excluded},indent=2))
if __name__=='__main__':main()
