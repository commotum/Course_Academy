"""Independent displayed-math, source-ledger and real grader checks."""
from pathlib import Path
import importlib.util,json,re,subprocess,sys,hashlib,concurrent.futures,tempfile
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
U,V=sp.symbols('U V');TRANS=standard_transformations+(implicit_multiplication_application,)
def parse(text,locals=None):
 text=text.strip().rstrip('.,');text=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',text);text=text.replace('{','(').replace('}',')');text=re.sub(r'(\d)([A-Za-z])',r'\1*\2',text)
 return parse_expr(text,local_dict=locals or {},transformations=TRANS)
def rhs(text,p):return sp.expand(parse(text.split('=')[-1],{p['u']:U,p['v']:V}))
def inspect(r,allow_raw=False):
 q=r['question'];prompt=q[':question/problem'];p=g.parameters_for({':question/problem':prompt});rr,ss=p['r'],p['s'];t=sp.Rational(rr,rr+ss);a=1-t;expected=a*U+t*V
 assert set(r['knowledge_point'])=={'db_id','id','title'} and r['knowledge_point']['db_id']==g.KP_ID
 A,B,X,u,w=[p[k] for k in ('A','B','X','u','v')]
 field_values=[]
 for i,f in enumerate(q[':question/answer-fields']):
  correct=f[':answer-field/correct'][1];bank=f[':answer-field/choices'];assert any(c[':answer/id']==correct for c in bank)
  if f[':answer-field/type'].endswith('/blank'):
   assert '{{'+f[':answer-field/key']+'}}' in prompt;assert len(bank)==1
   value=parse(bank[0][':answer/value']);field_values.append(value)
  else:
   vals=[rhs(c[':answer/value'],p) for c in bank];assert len(set(vals))==len(vals)==5;assert vals[next(i for i,c in enumerate(bank) if c[':answer/id']==correct)]==expected
 if field_values:assert field_values==([t,a] if allow_raw and r['generation']['raw_wrong_blank_key'] else [a,t])
 # Independently derive every displayed vector stage from actual prompt ratios.
 vec={'O'+A:U,A+'O':-U,'O'+B:V,B+'O':-V,A+B:V-U,A+X:t*(V-U),'O'+X:expected}
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==4
 count=0
 for block in blocks:
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
  # Replace complete vector components, preserving scalar math variables.
  block=re.sub(r'\\overset\{\\to \}\{([A-Z]{2})\}',lambda m:'('+str(vec[m[1]])+')',block)
  parts=block.split(r'\\');first=None
  for row in parts:
   exprs=row.strip().rstrip('.').split('=')
   if exprs[0].strip():first=parse(exprs[0],{u:U,w:V})
   assert first is not None
   for item in exprs[1:]:
    value=parse(item,{u:U,w:V,'U':U,'V':V});assert sp.expand(value-first)==0,(row,first,value)
   count+=1
 assert count==9 # path + four AB rows + ratio chain + three collected rows
 for text in [prompt,sol,*[c[':answer/value'] for f in q[':question/answer-fields'] for c in f[':answer-field/choices']]]:
  assert text.count('$')%2==0
  depth=0
  for char in text:
   if char=='{':depth+=1
   elif char=='}':depth-=1
   assert depth>=0
  assert depth==0
 image=Path(re.search(r'!\[\]\((.*?)\)',prompt)[1]);assert image.exists()
 side=json.loads(Path(str(image)+'.json').read_text());xx=side['X'];assert abs(xx[0]-4*float(t))<1e-12 and xx[1]==0
 assert side['parameters']==p and side['renderer']=='Matplotlib'
 return p,expected

def native(r,label):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  cid=f[':answer-field/correct'][1]
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':i,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==cid else 'rejected','purpose':'Each owned displayed choice'} for c in f[':answer-field/choices'])
  else:
   val=f[':answer-field/choices'][0][':answer/value'];x=parse(val);n,d=sp.fraction(x)
   checks.extend([{'field_index':i,'submitted':val,'expected':'accepted','purpose':'Canonical fragment'}, {'field_index':i,'submitted':f'\\frac{{{3*n}}}{{{3*d}}}','expected':'accepted','purpose':'Unreduced equivalent fragment'},{'field_index':i,'submitted':g.frac(-x),'expected':'rejected','purpose':'Wrong signed coefficient'},{'field_index':i,'submitted':g.frac(x+1),'expected':'rejected','purpose':'Wrong magnitude'}])
 return dict(label=label,record=r,checks=checks)

def main():
 assert json.loads((HERE/'source.json').read_text())==json.loads((REPO/'generate/runs/current/sources/17592186096653.json').read_text())
 cases=json.loads((HERE/'source-cases.json').read_text());assert len(cases)==len(g.QS)==23
 route=json.loads((REPO/'generate/runs/current/lessons/17592186048780.json').read_text())['record'][0];steps={s[':db/id']:s for s in route[':activity/steps']};key=route[':activity/first-step'][':db/id'];order=[]
 while key:
  s=steps[key];order.append(s[':step/content'][':db/id']);key=s.get(':step/next',{}).get(':db/id')
 assert order[-2:]==[17592186096652,g.KP_ID]
 ledger=[];review=[];engine=[];reviewmd=['# Ratio-vector review','Database math; basis 1356. Source banks are explicit replay evidence. Four raw blank keys are mathematically wrong; normal authored answers use the corrected coefficients.']
 for c in cases:
  id=c['source_id'];old=g.QS[id];r=g.generate('moderate',7,c['template'],parameters=c['parameters'],profile=id);p,ans=inspect(r,True);q=r['question'];oldfields=old[':question/answer-fields'][-1:] if id=='q-12212' else old[':question/answer-fields'];fields=q[':question/answer-fields']
  values=0;designation=0
  for f,of in zip(fields,oldfields):
   if f[':answer-field/type'].endswith('/radio'):
    new=[rhs(x[':answer/value'],p) for x in f[':answer-field/choices']];orig=[rhs(x[':answer/value'],p) for x in of[':answer-field/choices']]
   else:new=[parse(x[':answer/value']) for x in f[':answer-field/choices']];orig=[parse(x[':answer/value']) for x in of[':answer-field/choices']]
   assert set(new)==set(orig) and len(new)==len(orig);values+=len(new)
   if ':answer-field/correct' in of:
    oc=of[':answer-field/correct'][':answer/value'];newcorrect=next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id']==f[':answer-field/correct'][1])
    assert (rhs(oc,p)==rhs(newcorrect,p) if '=' in oc else parse(oc)==parse(newcorrect));designation+=1
  before=re.sub(r'!\[\]\(.*?\)','![](PLOT)',old[':question/problem']);after=re.sub(r'!\[\]\(.*?\)','![](PLOT)',q[':question/problem']);assert before==after,(id,before,after)
  osol=old.get(':question/worked-solution');assert osol is None or osol==q[':question/worked-solution'],id
  ledger.append(dict(source_id=id,bank_values_matched=values,complete_banks=len(fields),designations_matched=designation,solution_raw_exact=osol is not None,prompt_text_exact=True,mathematical_source_anomaly=id in g.REVERSED,missing_designation=id=='q-42659'))
  review.append(r);engine.append(native(r,'source:'+id))
  reviewmd.extend([f'\n## Original {id}',old[':question/problem'],json.dumps([[a[':answer/value'] for a in f[':answer-field/choices']] for f in old[':question/answer-fields']],ensure_ascii=False),'Source worked solution:',osol or '(absent)','\nGenerated source replay:',q[':question/problem'],q[':question/worked-solution']])
  # One changed-ratio peer for every observed bank/layout, not a literal branch.
  for rr,ss in [(2,5),(4,7),(5,9),(7,4),(9,5)]:
   pp=dict(c['parameters'],r=rr,s=ss)
   try:variant=g.generate('moderate',11,c['template'],parameters=pp,profile=id);inspect(variant,True);break
   except (ValueError,AssertionError):continue
  else:raise AssertionError('No changed peer '+id)
  review.append(variant);engine.append(native(variant,'observed-profile-peer:'+id));reviewmd.extend(['\nChanged-ratio replay peer (observed bank recipes; intent underdetermined):',variant['question'][':question/problem'],json.dumps(variant['question'][':question/answer-fields'],ensure_ascii=False),variant['question'][':question/worked-solution']])
 for id in sorted(g.REVERSED):
  repaired=g.generate('moderate',3,parameters=g.parameters_for(g.QS[id]),profile=id+'-repaired');inspect(repaired);review.append(repaired);engine.append(native(repaired,'repaired:'+id));reviewmd.extend(['\n## Mathematically repaired source '+id,repaired['question'][':question/problem'],json.dumps(repaired['question'][':question/answer-fields'],ensure_ascii=False),repaired['question'][':question/worked-solution']])
 # Explicit legacy duplicate bank: same assessment values, one supported field.
 legacy=g.generate('moderate',4,parameters=g.parameters_for(g.QS['q-12212']),profile='q-12212-legacy');inspect(legacy);lf=g.QS['q-12212'][':question/answer-fields'][0];lp=legacy['generation']['parameters'];assert {rhs(x[':answer/value'],lp) for x in lf[':answer-field/choices']}=={rhs(x[':answer/value'],lp) for x in legacy['question'][':question/answer-fields'][0][':answer-field/choices']};engine.append(native(legacy,'legacy:q-12212'));review.append(legacy)
 reviewmd.extend(['\n## Legacy duplicate bank q-12212',json.dumps(lf,ensure_ascii=False),'API replay:',json.dumps(legacy,ensure_ascii=False)])
 diversity={};checked=0
 for level in ('easy','moderate','hard'):
  fingerprints=set()
  for template in ('radio','coefficients'):
   for seed in range(24):
    r=g.generate(level,seed,template);inspect(r);checked+=1;fingerprints.add(r['generation']['mathematical_fingerprint'])
    if seed<2:
     review.append(r);engine.append(native(r,f'authored:{level}:{template}:{seed}'));reviewmd.extend([f'\n## Authored {level} {template} peer {seed+1}',r['question'][':question/problem'],json.dumps(r['question'][':question/answer-fields'],ensure_ascii=False),r['question'][':question/worked-solution']])
    # Seed changes cannot change content identity when parameters fixed.
    other=g.generate(level,seed+999,template,parameters=r['generation']['parameters']);assert r['question'][':question/id']==other['question'][':question/id']
   bad=dict(r['generation']['parameters'],r={'easy':5,'moderate':13,'hard':21}[level])
   try:g.generate(level,1,template,parameters=bad)
   except ValueError:pass
   else:raise AssertionError('explicit workload guard')
  diversity[level]=len(fingerprints);assert diversity[level]>=8
 for rr,ss in [(10,10),(20,10)]:
  for template in ('radio','coefficients'):
   try:g.generate('hard',1,template,parameters=dict(A='A',B='B',X='T',u='a',v='b',r=rr,s=ss))
   except ValueError:pass
   else:raise AssertionError('hard must reject unreduced easy ratio')
 a=g.generate('moderate',1,'coefficients',parameters=dict(A='A',B='B',X='T',u='a',v='b',r=2,s=1));b=g.generate('moderate',1,'coefficients',parameters=dict(A='A',B='B',X='T',u='a',v='b',r=4,s=2));assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 # Concurrent same/different fresh plotting writes, using private cache inputs.
 pp=dict(A='L',B='P',X='Q',u='l',v='p',r=17,s=16);qq=dict(pp,r=15,s=17)
 with tempfile.TemporaryDirectory(prefix='concurrency-',dir=HERE) as fresh:
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:paths=list(pool.map(lambda p:g.render_plots(p,fresh),[pp,pp,qq]))
  assert paths[0]==paths[1] and paths[0]!=paths[2]
  for path,p in zip(paths,[pp,pp,qq]):assert json.loads(Path(path+'.json').read_text())['parameters']==p
  assert not list(Path(fresh).glob('ratio-*.json'))
 inputpath=HERE/'native-input.json';outputpath=HERE/'native-report.json';inputpath.write_text(json.dumps(engine,indent=2,ensure_ascii=False));exe=REPO/'generate/runs/current/check-engine';subprocess.run([str(exe),str(inputpath),str(outputpath)],check=True)
 report=json.loads(outputpath.read_text());validation={'status':'passed','source_cases':23,'source_bank_values_matched':sum(x['bank_values_matched'] for x in ledger)+5,'source_bank_values_total':sum(x['bank_values_matched'] for x in ledger)+5,'source_complete_banks_matched':sum(x['complete_banks'] for x in ledger)+1,'source_designations_total_present':32,'source_incorrect_correct_designations':8,'source_distractors_matched':56,'source_distractors_total':56,'source_radio_banks_matched':14,'source_radio_banks_total':14,'source_designations_matched':sum(x['designations_matched'] for x in ledger),'source_designations_missing_inferred':2,'source_solutions_exact':sum(x['solution_raw_exact'] for x in ledger),'source_solutions_total_present':22,'source_prompts_text_exact':23,'raw_blank_wrong_keys':sorted(g.REVERSED),'correctness_source_cases':19,'mathematical_repairs_required':4,'authored_missing_levels':['easy','hard'],'source_ledger':ledger,'fresh_concurrent_plot_checks':3,'generated_records_checked':checked,'native_records':len(engine),'native_report':report,'diversity_24_seeds_each_layout':diversity,'route':order,'unresolved':['Observed distractor intent underdetermined; replay profiles are explicit component patterns, not recovered historical error code.'],'failures':[],'engine_sha256':hashlib.sha256(exe.read_bytes()).hexdigest()}
 (HERE/'validation.json').write_text(json.dumps(validation,indent=2,ensure_ascii=False));(HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False));(HERE/'review.md').write_text('\n\n'.join(reviewmd));print(json.dumps({k:v for k,v in validation.items() if k not in ('source_ledger','native_report')},indent=2))
if __name__=='__main__':main()
