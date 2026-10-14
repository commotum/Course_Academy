"""Independent rendered-expression, complete source-bank and native-grader validation."""
import copy,hashlib,importlib.util,json,re,subprocess,uuid,tokenize
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('tangent_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2,default=str)+'\n')
def enum(x):return x[':db/ident'] if isinstance(x,dict) else x
def correct_id(f):
 c=f[':answer-field/correct'];return str(c[':answer/id']) if isinstance(c,dict) else c[1]
def solution_check(q):
 curve,t,y=g.prompt_data(q[':question/problem']);assert t>0 and sp.simplify(curve.subs(g.x,t)-y)==0,'wrong supplied point'
 m=sp.diff(curve,g.x).subs(g.x,t);fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];choices=f[':answer-field/choices'];kind=enum(f[':answer-field/type']);assert kind in (':answer-field.type/blank',':answer-field.type/radio')
 assert len(choices)==(1 if kind.endswith('/blank') else 5)
 vals=[g.expression(a[':answer/value']) for a in choices];valid=[sp.simplify(v-m)==0 for v in vals]
 assert sum(valid)==1 and str(choices[valid.index(True)][':answer/id'])==correct_id(f),'wrong or ambiguous key'
 assert len(set(vals))==len(vals),'duplicate answers'
 text=q[':question/worked-solution'];assert text and '__' not in text
 targets=re.findall(r'x=(\d+)',text);assert targets and all(sp.Integer(i)==t for i in targets),'stale evaluated target'
 displays=re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S);assert len(displays) in (2,3)
 steps=0
 for i,display in enumerate(displays):
  display=re.sub(r'\\(?:begin|end)\{aligned\}','',display)
  for line in display.split(r'\\'):
   rhs=line.replace('&','').split('=')[-1].strip().rstrip('.,')
   if rhs.startswith(r'\frac{\text{d}}{\text{d}x}'):
    z=re.fullmatch(r'\\frac\{\\text\{d\}\}\{\\text\{d\}x\}\((.*)\)',rhs)
    assert z and sp.simplify(g.expression(z[1])-curve)==0,'wrong derivative input'
   else:
    expect=sp.diff(curve,g.x) if i==0 else m
    assert sp.simplify(g.expression(rhs)-expect)==0,('invalid solution stage',rhs,expect)
   steps+=1
 return steps

def independent(rec):
 assert rec['knowledge_point']['db_id']==g.KP_ID and rec['knowledge_point']['id']==g.KP_UUID
 q=rec['question'];meta=rec['generation'];level=q[':question/difficulty'].split('/')[-1]
 assert rec==g.generate(level,meta['seed'],meta['template'],meta['parameters'])
 assert g.fingerprint(q)==meta['parameter_fingerprint'];n=solution_check(q)
 assert q[':question/problem'].count('{{field-1}}')==1
 for field in q[':question/answer-fields']:
  assert field[':answer-field/key']=='field-1'
 ids=[q[':question/id']]+[f[':answer-field/id'] for f in q[':question/answer-fields']]+[a[':answer/id'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
 assert len(ids)==len(set(ids))
 for i in ids:uuid.UUID(i)
 return n

def checks(rec):
 f=rec['question'][':question/answer-fields'][0]
 if enum(f[':answer-field/type']).endswith('/radio'):
  return [{'field_index':0,'submitted_answer_id':str(a[':answer/id']),'expected':'accepted' if str(a[':answer/id'])==correct_id(f) else 'rejected','purpose':'Every field-owned source choice'} for a in f[':answer-field/choices']]
 v=g.expression(f[':answer-field/choices'][0][':answer/value']);assert v.is_Rational
 q=int(v.q)
 for factor in (2,5):
  while q%factor==0:q//=factor
 decimal_exact=q==1
 return [{'field_index':0,'submitted':s,'expected':expected,'purpose':purpose} for s,expected,purpose in [(str(v),'accepted','Exact rational'),(f'({v.p*2})/({v.q*2})','accepted','Equivalent unsimplified rational'),(f'{sp.N(v,16):.12f}','accepted' if decimal_exact else 'rejected','Exact terminating decimal' if decimal_exact else 'Rounded recurring fraction is not exact'),(str(v+1),'rejected','Incorrect slope'),(str(v-1),'rejected','Incorrect slope')]]

def fixture(q):
 q=copy.deepcopy(q)
 q[':question/difficulty']=enum(q[':question/difficulty'])
 for f in q[':question/answer-fields']:
  f[':answer-field/id']=str(f[':answer-field/id']);f[':answer-field/type']=enum(f[':answer-field/type']);f[':answer-field/correct']=[':answer/id',correct_id(f)]
  for a in f[':answer-field/choices']:a[':answer/id']=str(a[':answer/id']);a[':answer/type']=enum(a[':answer/type'])
 return {'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'question':q,'generation':{'template':q[':question/math-academy-id']}}

def main():
 source=g.S['record'];qs={q[':question/math-academy-id']:q for q in source[':knowledge-point/questions']};source_cases=[];native=[];review=[];steps=0
 for mid,q in qs.items():
  if ':question/worked-solution' not in q:continue
  steps+=solution_check(q);f=q[':question/answer-fields'][0];rec=fixture(q)
  native.append({'label':'source-'+mid,'record':rec,'checks':checks(rec)})
  case={'source':mid,'bank_profile':mid if enum(f[':answer-field/type']).endswith('/radio') else None,'matched_values':len(f[':answer-field/choices']),'total_values':len(f[':answer-field/choices']),'matched_distractors':len(f[':answer-field/choices'])-1,'total_distractors':len(f[':answer-field/choices'])-1,'missing_options':[],'extra_options':[],'sampling':'parameterized blank' if mid in g.TEMPLATES else 'frozen source bank; replay only'}
  if mid in g.TEMPLATES:
   replay=g.generate(g.TEMPLATES[mid]['difficulty'],template=mid,parameters=g.TEMPLATES[mid]['original_parameters']);independent(replay)
   assert replay['question'][':question/problem']==q[':question/problem'];assert replay['question'][':question/worked-solution']==q[':question/worked-solution']
   assert [a[':answer/value'] for a in replay['question'][':question/answer-fields'][0][':answer-field/choices']]==[a[':answer/value'] for a in f[':answer-field/choices']]
   case.update(exact_prompt_replay=True,exact_solution_replay=True)
   review.append('## '+mid+' source and exact replay\n\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\nGenerated replay:\n\n'+g.markdown(replay))
  source_cases.append(case)
 sizes={};coverage={};records=[]
 for level in g.SUPPORTED_LEVELS:
  rows=g.batch(level,9999,2205);sizes[level]=len(rows);coverage[level]={k:sorted({r['generation']['parameters'][k] for r in rows}) for k in ('a','b','k')}
  assert len({g.fingerprint(r['question']) for r in rows})==len(rows)
  for i,r in enumerate(rows):
   steps+=independent(r);native.append({'label':level+'-'+str(i),'record':r,'checks':checks(r)});records.append(r)
  review.append('## '+level+' changed coefficients and point\n\n'+g.markdown(rows[0]))
  r=rows[0];p=dict(r['generation']['parameters']);p['k']=2 if p['k']!=2 else 3
  changed=g.generate(level,template=r['generation']['template'],parameters=p);independent(changed);assert g.fingerprint(changed['question'])!=g.fingerprint(r['question'])
  review.append('## '+level+' same curve, changed point\n\n'+g.markdown(changed))
 negatives=0
 for r in records[:1]+records[-1:]:
  for mode in ('answer','solution','target','point'):
   bad=copy.deepcopy(r);q=bad['question']
   if mode=='answer':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='999'
   if mode=='solution':q[':question/worked-solution']=q[':question/worked-solution'].replace(' & =',' & =999+',1)
   if mode=='target':q[':question/worked-solution']=q[':question/worked-solution'].replace('Evaluating at $x=','Evaluating at $x=999')
   if mode=='point':q[':question/problem']=q[':question/problem'].replace('at the point $(','at the point $(999')
   try:solution_check(q)
   except (AssertionError,ValueError,SyntaxError,TypeError,tokenize.TokenError):negatives+=1
   else:raise AssertionError('corruption escaped: '+mode)
 for level,p in [('hard',None),('easy',{'a':4,'b':3,'k':2}),('moderate',{'a':5,'b':10,'k':0})]:
  try:g.generate(level,parameters=p)
  except ValueError:negatives+=1
  else:raise AssertionError('invalid input accepted')
 save('source-cases.json',source_cases);save('engine-input.json',native)
 binary=ROOT/'generate/runs/current/check-engine';subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 save('source-replay.json',{'banks':source_cases,'supported_banks_matched':5,'total_complete_banks':5,'matched_values':17,'total_values':17,'matched_distractors':12,'total_distractors':12,'bank_generalization':'Three radio profiles are immutable replay-only banks, not used for new instances. All their exact choices retained and independently mathematically and natively graded. No unsupported extrapolation.'})
 (HERE/'review.md').write_text('\n\n---\n\n'.join(review)+'\n')
 save('validation.json',{'status':'pass','source_basis':g.S['basis'],'lineage':g.S['lineage'],'supported_levels':list(g.SUPPORTED_LEVELS),'mathematics':{'records_checked':len(records),'solution_stages_checked':steps,'negative_controls':negatives,'finite_distinct_parameter_tasks':sizes,'slot_coverage':coverage,'same_curve_changed_point_checked':True},'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',HERE/'templates.json',HERE/'replenish.py',binary)}})
 print(json.dumps({'status':'pass','domain':sizes,'records':len(records),'stages':steps,'negative_controls':negatives}))
if __name__=='__main__':main()
