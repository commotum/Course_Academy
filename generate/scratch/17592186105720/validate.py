"""Independent parsing, two-branch calculus, exhaustive banks and native grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from math_parser import expression,prompt_integrand,branches,derivative_residual,X,C,K
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2,default=str)+'\n')
def parse(problem):return g.fingerprint_expression(prompt_integrand(problem))
def bank_check(q):
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection'
 kind=f[':answer-field/type'];kind=kind[':db/ident'] if isinstance(kind,dict) else kind;assert kind==':answer-field.type/radio'
 aa=f[':answer-field/choices'];assert len(aa)==5
 cid=f[':answer-field/correct'];cid=str(cid[':answer/id']) if isinstance(cid,dict) else cid[1]
 integrand=prompt_integrand(q[':question/problem']);values=[expression(a[':answer/value']) for a in aa]
 for val in values:
  assert all(sp.simplify(sp.im(sp.expand_complex(b)))==0 for b in branches(val)), 'Choice undefined over a real branch'
 valid=[derivative_residual(v,integrand)==[0,0] and sp.diff(v,K)!=0 for v in values]
 assert sum(valid)==1 and str(aa[valid.index(True)][':answer/id'])==cid,('Incorrect key',valid)
 for i,v in enumerate(values):
  for w in values[:i]:
   assert derivative_residual(v-w,sp.Integer(0))!=[0,0],'Equivalent antiderivative families'
 return integrand
def integral_expression(text):
 text=text.strip().rstrip('.,')
 text=re.sub(r'\\int\s*(?:\\,\s*)?\\text\{d\}x','(1)',text)
 text=text.replace(r'\int','').replace(r'\text{d}x','').replace(r'\,','')
 return expression(text)
def solution_check(q):
 integrand=bank_check(q);displays=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S);assert len(displays)==2
 count=0
 for display in displays:
  display=re.sub(r'\\(?:begin|end)\{aligned\}','',display)
  for line in display.split(r'\\'):
   left,right=line.replace('&','').split('=');right=right.strip().rstrip('.,')
   if left.strip():assert sp.simplify(integral_expression(left)-integrand)==0
   if r'\int' in right:assert sp.simplify(integral_expression(right)-integrand)==0,right
   else:
    val=expression(right);assert derivative_residual(val,integrand)==[0,0],right
    assert sp.diff(val,C)!=0 or sp.diff(val,K)!=0,'Arbitrary constant missing'
   count+=1
 # The displayed final result must equal the keyed answer at the same K.
 f=q[':question/answer-fields'][0];cid=f[':answer-field/correct'];cid=str(cid[':answer/id']) if isinstance(cid,dict) else cid[1]
 correct=next(a for a in f[':answer-field/choices'] if str(a[':answer/id'])==cid)
 assert branches(expression(right)-expression(correct[':answer/value']))==[0,0]
 return count
def independent(r):
 m=r['generation'];q=r['question'];assert r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['id']==g.KP_UUID
 level=q[':question/difficulty'].split('/')[-1];assert r==g.generate(level,m['seed'],m['template'],m['parameters'],m['bank_profile'])
 assert parse(q[':question/problem'])==m['parameter_fingerprint'];steps=solution_check(q)
 f=q[':question/answer-fields'][0];ids=[q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']];assert len(set(ids))==len(ids)
 for u in ids:uuid.UUID(u)
 for text in [q[':question/problem'],q[':question/worked-solution']]:assert text.count('$')%2==0 and text.count('{')==text.count('}')
 assert '@@' not in json.dumps(r)
 return steps
def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned radio choice through actual grade_field'} for a in f[':answer-field/choices']]
def main():
 source=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 rows=[];replays=[];review=[];steps=0
 for mid,t in g.TEMPLATES.items():
  r=g.generate(t['level'],0,mid,t['parameters']);q=qs[mid];f=q[':question/answer-fields'][0]
  solution_check(q)
  assert g.clean(q[':question/problem'])==r['question'][':question/problem'];assert g.clean(q[':question/worked-solution'])==r['question'][':question/worked-solution']
  original=[expression(a[':answer/value']) for a in f[':answer-field/choices']];rendered=[expression(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  assert all(sum(branches(a-b)==[0,0] for b in rendered)==1 for a in original)
  assert g.clean(f[':answer-field/correct'][':answer/value'])==r['question'][':question/answer-fields'][0][':answer-field/choices'][t['correct_index']][':answer/value']
  replays.append({'source':mid,'complete_bank':True,'matched_options':5,'total_options':5,'matched_distractors':4,'total_distractors':4,'missing':[],'extra':[],'notation':'Log commands normalized; source sentences and full solution sequence retained.'})
  review.append('## '+mid+' original\n\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\n### Replay\n\n'+g.markdown(r))
  for p in g.domain(t['kind']):
   rec=g.generate(t['level'],123,mid,p);steps+=independent(rec);assert rec['question']==g.generate(t['level'],99,mid,p)['question'];rows.append(rec)
  variant=g.generate(t['level'],17,mid,next(p for p in g.domain(t['kind']) if p!=t['parameters']));review.append('### Changed parameters\n\n'+g.markdown(variant))
 # Explicit negative controls cover source exclusions and frozen boundaries.
 negatives=0
 for mid in ['q-103603','q-49067']:
  try:bank_check(qs[mid])
  except (AssertionError,ValueError,KeyError):negatives+=1
  else:raise AssertionError('Source defect was missed: '+mid)
 for level,mid,p in [('easy',None,None),('hard','q-103375',{'n':2}),('moderate','q-15717',{'n':3}),('moderate','q-15710',{'n':32}),('hard','q-103375',{'n':True})]:
  try:g.generate(level,template=mid,parameters=p)
  except ValueError:negatives+=1
  else:raise AssertionError('Invalid parameter accepted')
 corrupted=copy.deepcopy(rows[0]);f=corrupted['question'][':question/answer-fields'][0];f[':answer-field/choices'][g.TEMPLATES[corrupted['generation']['template']]['correct_index']][':answer/value']='x+K'
 try:bank_check(corrupted['question'])
 except AssertionError:negatives+=1
 else:raise AssertionError('Corrupt answer accepted')
 save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(rows)])
 subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 save('source-cases.json',replays);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 files=[HERE.with_suffix('.py'),HERE/'templates.json',HERE/'source.json',Path(__file__),HERE/'math_parser.py',HERE/'check-engine']
 save('validation.json',{'status':'pass','source_basis':source['basis'],'complete_source_banks':len(replays),'supported_source_banks':5,'excluded_source_banks':['q-49096','q-103603','q-49067'],'matched_distractors':20,'total_supported_distractors':20,'exhaustive_profile_parameter_cases':len(rows),'checked_solution_lines':steps,'negative_controls':negatives,'native_grading':engine['entry_point'],'accepted_checks':engine['accepted_checks'],'rejected_checks':engine['rejected_checks'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}})
 print(json.dumps(json.loads((HERE/'validation.json').read_text())|{'hashes':'retained'}))
if __name__=='__main__':main()
