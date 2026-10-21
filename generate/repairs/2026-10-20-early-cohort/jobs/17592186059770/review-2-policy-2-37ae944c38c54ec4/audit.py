import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,re,hashlib,subprocess,importlib.util,shutil,collections,itertools
from pathlib import Path
import sympy as sp
E=Path(__file__).resolve().parent
J=E.parent;W=J/'workspace';R=Path('/home/jake/Developer/Course_Academy');PY=R/'.venv/bin/python'
sys.dont_write_bytecode=True

def save(n,x):
 (E/n).parent.mkdir(parents=True,exist_ok=True);(E/n).write_text(json.dumps(x,indent=2,default=str))
def load(n):return json.load(open(n))
def module(p):
 spec=importlib.util.spec_from_file_location('subject',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def texnum(t):
 t=t.strip();t=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',t);return sp.sympify(t)
def mat(t):
 body=re.search(r'\\begin\{(?:array|bmatrix)\}(?:\{[c|]+\})?(.*?)\\end\{',t,re.S)[1]
 return [[texnum(t) for t in row.split('&')] for row in body.split('\\\\')]
def expressions(t,names):
 t=t.replace(' ','').replace('&','')
 for i,n in enumerate(names):t=t.replace(n,f'V{i}')
 t=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',t)
 t=re.sub(r'(?<=[0-9)])(?=V)', '*', t)
 return sp.sympify(t,locals={f'V{i}':sp.Symbol(f'V{i}') for i in range(len(names))})
def visible(q):
 text=q[':question/problem'];body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)[1]
 names=sorted(set(re.findall(r'\{x\}_\{\d+\}|(?<![a-zA-Z])[a-dmnpquv](?![a-zA-Z])',body)))
 A=[];rhs=[]
 for row in body.split('\\\\'):
  l,r=row.split('&=');expr=sp.expand(expressions(l,names)-expressions(r,names))
  syms=[sp.Symbol(f'V{i}') for i in range(len(names))]
  A.append([expr.coeff(v) for v in syms]);rhs.append(-expr.subs(dict.fromkeys(syms,0)))
 return A if 'coefficient matrix' in text.split('\n')[0] else [a+[b] for a,b in zip(A,rhs)]
def qcheck(r):
 q=r['question'];expected=visible(q);f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];key=f[':answer-field/correct'][1]
 parsed=[mat(a[':answer/value']) for a in cs];hits=[i for i,x in enumerate(parsed) if x==expected]
 assert len(hits)==1,(q[':question/id'],'nonunique math',hits,expected)
 assert cs[hits[0]][':answer/id']==key,('bad key',q)
 solution=q[':question/worked-solution'];last=re.findall(r'\\begin\{(?:array|bmatrix)\}.*?\\end\{(?:array|bmatrix)\}',solution,re.S)[-1]
 assert mat(last)==expected,('bad solution',q)
 return {'id':q[':question/id'],'expected':expected,'correct_index':hits[0]}

def command(args):
 p=subprocess.run([str(x) for x in args],text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 return {'command':[str(x) for x in args],'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}

def main():
 hashes={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};save('package-before.json',hashes)
 g=module(W/'17592186059770.py');source=load(J/'source/source.json');qs=source['material']['kp'][':knowledge-point/questions'];by_ma={q[':question/math-academy-id']:q for q in qs}
 replay=[];records=[]
 for profile,(p,names) in g.EASY_SOURCES.items():
  x=g.generate('easy',9031,parameters=dict(zip('abcdef',p)),profile=profile);sq=by_ma[profile];qcheck(x)
  source_bank=[mat(a[':answer/value']) for a in sq[':question/answer-fields'][0][':answer-field/choices']]
  generated=[mat(a[':answer/value']) for a in x['question'][':question/answer-fields'][0][':answer-field/choices']]
  assert sorted(map(str,source_bank))==sorted(map(str,generated));assert visible(sq)==visible(x['question'])
  replay.append({'profile':profile,'source_id':sq[':question/id'],'bank_match':True,'math_match':True});records.append(x)
 for template,profile in g.TEMPLATES.items():
  x=g.generate('moderate',9031,template,parameters=g.SOURCE_PARAMETERS[template]);sq=by_ma[profile];qcheck(x)
  a=[mat(z[':answer/value']) for z in sq[':question/answer-fields'][0][':answer-field/choices']];b=[mat(z[':answer/value']) for z in x['question'][':question/answer-fields'][0][':answer-field/choices']]
  assert sorted(map(str,a))==sorted(map(str,b));assert visible(sq)==visible(x['question']);replay.append({'profile':profile,'source_id':sq[':question/id'],'bank_match':True,'math_match':True});records.append(x)
 save('source-replay-records.json',records);save('source-replay.json',{'tested':replay,'unsupported':[q[':question/id'] for q in qs if q[':question/math-academy-id'] not in list(g.EASY_SOURCES)+list(g.TEMPLATES.values())],'gaps':load(E/'source-analysis.json')['source_gaps']})
 # Fresh bounded sample: profile/orientation combinations and independent seeds, no reliance on metadata for math.
 sample=[g.generate('easy',seed,profile=p,bank_orientation=o) for p in g.EASY_SOURCES for o in ['identity','row_swap','column_swap','both'] for seed in range(830017,830019)]
 moderate=[g.generate('moderate',seed,template=t) for t in g.TEMPLATES for seed in range(947123,947125)]
 batch=load(J/'samples.json');save('batch.json',batch);save('sample.json',sample);save('moderate.json',moderate)
 checks=[qcheck(r) for r in sample+moderate+batch];save('math.json',{'checked':len(checks),'results':checks})
 # Same complete bank, changed intended response; all eligible easy targets across profiles.
 controlled=[];pairs=[]
 for profile in g.EASY_SOURCES:
  p=dict(zip('abcdef',[2,3,5,7,8,9]));base=g.generate('easy',731,parameters=p,profile=profile)
  eligible=[z['recipe'] for z in base['generation']['recipes'] if len(z['matrix'])==2 and len(z['matrix'][0])==3]
  family=[g.generate('easy',731,parameters=p,profile=profile,target_recipe=t) for t in eligible]
  banks=[sorted(a[':answer/value'] for a in x['question'][':question/answer-fields'][0][':answer-field/choices']) for x in family]
  assert all(b==banks[0] for b in banks);assert len({x['question'][':question/problem'] for x in family})==len(family)
  for x in family:qcheck(x)
  start=len(controlled);controlled+=family;pairs.append({'profile':profile,'kind':'relevant','indices':list(range(start,len(controlled))),'result':'fixed bank, distinct prompts and correct matrices'})
 # Irrelevant seed only changes choice order; pin all mathematical parameters and target.
 base=g.generate('easy',731,parameters=dict(zip('abcdef',[2,3,5,7,8,9])),profile='q-129137');other=g.generate('easy',732,parameters=dict(zip('abcdef',[2,3,5,7,8,9])),profile='q-129137')
 assert base['question'][':question/problem']==other['question'][':question/problem'];assert visible(base['question'])==visible(other['question']);assert base['question'][':question/worked-solution']==other['question'][':question/worked-solution'];assert base['question'][':question/answer-fields'][0][':answer-field/choices']!=other['question'][':question/answer-fields'][0][':answer-field/choices']
 controlled += [base,other];pairs.append({'kind':'irrelevant','indices':[len(controlled)-2,len(controlled)-1],'result':'choice order changed; prompt, matrix and explanation preserved'})
 save('controlled.json',controlled);save('counterfactuals.json',pairs)
 native=[]
 for n,r in enumerate(records+sample+moderate+batch+controlled):
  f=r['question'][':question/answer-fields'][0];expected=visible(r['question']);native.append({'label':f'independent-{n}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if mat(a[':answer/value'])==expected else 'rejected','purpose':'visible equations independently parsed; exact requested matrix'} for a in f[':answer-field/choices']]})
 save('native-input.json',native)
 native_run=command([R/'generate/runs/current/check-engine',E/'native-input.json',E/'native-report.json']);save('native-run.json',native_run)
 # Explicit invalid input, deterministic replay and standalone manifest closure relocation.
 runtime={'python':sys.version.split()[0],'packages':{'sympy':sp.__version__}};manifest=load(W/'package.json');assert manifest['dependencies']==runtime
 dest=E/'relocated';dest.mkdir(exist_ok=True)
 for name in manifest['files']:shutil.copy2(W/name,dest/name)
 args=['--difficulty','easy','--count','5','--seed','78319','--format','json'];a=command([PY,W/manifest['entrypoint'],*args]);b=command([PY,dest/manifest['entrypoint'],*args]);assert a['exit']==b['exit']==0;assert json.loads(a['stdout'])==json.loads(b['stdout'])
 boundary=[]
 for profile in g.EASY_SOURCES:
  for v in [1,-1,9,-9]:
   p=dict(zip('abcdef',[v,2,-3,4,-5,6]));x=g.generate('easy',301,profile=profile,parameters=p);qcheck(x);boundary.append(x)
 save('boundary.json',boundary)
 rejection=[]
 for args in [['--difficulty','hard'],['--count','0'],['--difficulty','easy','--parameters',json.dumps(dict(zip('abcdef',[0,2,3,4,5,6])))]]:
  c=command([PY,W/manifest['entrypoint'],*args]);assert c['exit']!=0;rejection.append(c)
 # Verify earlier defect on retained failing implementation, avoiding author checks that write into package.
 old=E/'legacy';old.mkdir(exist_ok=True);shutil.copy2(W/'evidence/legacy/17592186059770.py',old/'17592186059770.py');(old/'17592186059770').mkdir(exist_ok=True);shutil.copy2(W/'evidence/legacy/17592186059770/source.json',old/'17592186059770/source.json')
 before=command([PY,old/'17592186059770.py','--difficulty','easy','--count','5','--seed','0','--format','json']);after=command([PY,W/manifest['entrypoint'],'--difficulty','easy','--count','5','--seed','0','--format','json']);assert before['exit']!=0;assert after['exit']==0
 save('regression.json',{'history':'legacy_packaging_or_sampling','preflight':'absent','failing':before,'current':after})
 save('packaging.json',{'runtime':runtime,'manifest':manifest,'relocation':a['stdout']==b['stdout'],'determinism':a['stdout']==command([PY,W/manifest['entrypoint'],*args])['stdout'] if False else json.loads(a['stdout'])==json.loads(command([PY,W/manifest['entrypoint'],'--difficulty','easy','--count','5','--seed','78319','--format','json'])['stdout']),'rejections':rejection,'boundary_records':'boundary.json','no_assets':'generator only emits JSON/Markdown; no external output'})
 print(json.dumps({'source_replay':len(records),'sample':len(sample),'moderate':len(moderate),'batch':len(batch),'controlled':len(controlled),'math':len(checks),'native_exit':native_run['exit'],'legacy_exit':before['exit'],'current_exit':after['exit']}))
if __name__=='__main__':main()
