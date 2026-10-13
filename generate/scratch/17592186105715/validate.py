"""Full source replay, exact two-branch calculus and actual learner grading."""
import copy,hashlib,importlib.util,json,re,subprocess,uuid
from pathlib import Path
import sympy as sp
from math_parser import expression,prompt_integrand,integral_body,branches,derivative_residual,X,C
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2,default=str)+'\n')
def parse(problem):return g.fingerprint_coefficient(sp.simplify(prompt_integrand(problem)*X))
def bank_check(q):
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection'
 kind=f[':answer-field/type'];kind=kind[':db/ident'] if isinstance(kind,dict) else kind
 assert kind==':answer-field.type/radio'
 aa=f[':answer-field/choices'];assert len(aa)==5
 cid=f[':answer-field/correct'];cid=str(cid[':answer/id']) if isinstance(cid,dict) else cid[1]
 integrand=prompt_integrand(q[':question/problem']);values=[expression(a[':answer/value']) for a in aa]
 valid=[derivative_residual(v,integrand)==[0,0] and sp.simplify(sp.diff(v,C))==1 for v in values]
 assert sum(valid)==1 and str(aa[valid.index(True)][':answer/id'])==cid,('Incorrect key',valid)
 for i,v in enumerate(values):
  for w in values[:i]:
   assert branches(v-w)!=[0,0],'Equivalent distractors'
   if sp.diff(v,C)==1 and sp.diff(w,C)==1:assert derivative_residual(v-w,sp.Integer(0))!=[0,0],'Same antiderivative family'
 return integrand
def solution_check(q):
 integrand=bank_check(q);assert sp.simplify(integrand*X).free_symbols==set()
 displays=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S);assert len(displays)==1
 display=re.sub(r'\\(?:begin|end)\{aligned\}','',displays[0]);count=0;previous=None
 for line in display.split(r'\\'):
  left,right=line.replace('&','').split('=');right=right.strip().rstrip('.,')
  def evaluate(text):
   if r'\int' in text:
    before,body=text.split(r'\int',1);factor=expression(before.strip()) if before.strip() else sp.Integer(1)
    return factor*integral_body(body),False
   return expression(text),True
  if left.strip():previous=evaluate(left)
  assert previous is not None
  cur=evaluate(right)
  if not cur[1]:assert sp.simplify(cur[0]-integrand)==0
  else:
   assert derivative_residual(cur[0],integrand)==[0,0]
   assert sp.simplify(sp.diff(cur[0],C))==1
  if previous[1] and cur[1]:assert branches(cur[0]-previous[0])==[0,0]
  elif not previous[1]:assert sp.simplify(previous[0]-integrand)==0
  previous=cur;count+=1
 assert previous[1]
 return count
def independent(r):
 m=r['generation'];q=r['question'];assert r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['id']==g.KP_UUID
 level=q[':question/difficulty'].split('/')[-1];assert r==g.generate(level,m['seed'],m['template'],m['parameters'],m['bank_profile'])
 assert parse(q[':question/problem'])==m['parameter_fingerprint'];result=solution_check(q)
 f=q[':question/answer-fields'][0];ids=[q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]
 assert len(set(ids))==len(ids)
 for u in ids:uuid.UUID(u)
 for text in [q[':question/problem'],q[':question/worked-solution']]:assert text.count('$')%2==0 and text.count('{')==text.count('}')
 assert '@@' not in json.dumps(r)
 return result
def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned choice through actual grade_field'} for a in f[':answer-field/choices']]
def main():
 source=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 rows=[];replays=[];review=[];steps=0
 for mid,t in g.TEMPLATES.items():
  r=g.generate('easy',0,mid,t['parameters']);q=qs[mid];f=q[':question/answer-fields'][0]
  assert g.clean(q[':question/problem'])==r['question'][':question/problem']
  assert g.clean(q[':question/worked-solution'])==r['question'][':question/worked-solution']
  original=[expression(a[':answer/value']) for a in f[':answer-field/choices']];rendered=[expression(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  assert all(sum(branches(a-b)==[0,0] for b in rendered)==1 for a in original)
  assert g.clean(f[':answer-field/correct'][':answer/value'],True)==r['question'][':question/answer-fields'][0][':answer-field/choices'][t['correct_index']][':answer/value']
  replays.append({'source':mid,'complete_bank':True,'matched_options':5,'total_options':5,'matched_distractors':4,'total_distractors':4,'missing':[],'extra':[],'notation':'Double-escaped answer commands decoded; log normalized to \\ln. Source sentences and step structure retained.'})
  review.append('## '+mid+' original\n\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\n### Replay\n\n'+g.markdown(r))
  for p in g.domain(t['kind']):
   rec=g.generate('easy',123,mid,p);steps+=independent(rec);assert rec['question']==g.generate('easy',99,mid,p)['question'];rows.append(rec)
  variant=g.generate('easy',17,mid,next(p for p in g.domain(t['kind']) if p!=t['parameters']));review.append('### Changed parameters\n\n'+g.markdown(variant))
 negative=0
 for level,mid,p in [('hard',None,None),('moderate',None,None),('easy','q-29831',{'n':3}),('easy','q-49097',{'n':1}),('easy','q-49097',{'n':13}),('easy','q-49097',{'n':True}),('easy','q-29838',{'n':4}),('easy','q-71098',{'a':2,'b':4})]:
  try:g.generate(level,template=mid,parameters=p)
  except ValueError:negative+=1
  else:raise AssertionError('Invalid generation accepted')
 for part in ('answer','solution'):
  r=copy.deepcopy(rows[0]);q=r['question']
  if part=='answer':q[':question/answer-fields'][0][':answer-field/choices'][g.TEMPLATES[r['generation']['template']]['correct_index']][':answer/value']='x+C'
  else:q[':question/worked-solution']=q[':question/worked-solution'].replace('ln','sin')
  try:solution_check(q)
  except (AssertionError,ValueError):negative+=1
  else:raise AssertionError('Corrupted mathematics accepted')
 save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(rows)])
 subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 save('source-cases.json',replays);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 files=[HERE.with_suffix('.py'),HERE/'templates.json',HERE/'source.json',Path(__file__),HERE/'math_parser.py',HERE/'check-engine']
 save('validation.json',{'status':'pass','source_basis':source['basis'],'complete_source_banks':len(replays),'supported_source_banks':4,'excluded_source_banks':['q-29831','q-103369','q-103590'],'matched_distractors':16,'total_supported_distractors':16,'exhaustive_profile_parameter_cases':len(rows),'checked_solution_lines':steps,'negative_controls':negative,'native_grading':engine['entry_point'],'accepted_checks':engine['accepted_checks'],'rejected_checks':engine['rejected_checks'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}})
 print(json.dumps(json.loads((HERE/'validation.json').read_text())|{'hashes':'retained'}))
if __name__=='__main__':main()
