#!/usr/bin/env python3
"""Independent visible-content checks, source replay and focused regressions."""
import importlib.util,json,re,subprocess,sys,collections,tempfile,shutil
from pathlib import Path
import sympy as sp
W=Path(__file__).resolve().parents[1]; E=W/'evidence';E.mkdir(exist_ok=True)
REPO=Path('/home/jake/Developer/Course_Academy'); PY=sys.executable
spec=importlib.util.spec_from_file_location('generator',W/'17592186059770.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,obj): (E/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')
def scalar(t):
 t=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1/\2)',t.strip())
 assert re.fullmatch(r'[\d()*/+ .-]+',t),t
 return sp.Rational(sp.sympify(t))
def matrix(t):
 m=re.search(r'\\begin\{(?:bmatrix|array)\}(?:\{[c|]+\})?(.*?)\\end\{(?:bmatrix|array)\}',t,re.S);assert m,t
 rows=[[scalar(c) for c in row.split('&')] for row in m[1].split(r'\\')]
 assert len({len(r) for r in rows})==1
 return tuple(tuple(r) for r in rows)
def expr(t):
 t=re.sub(r'\{x\}_\{(\d)\}',r'X\1',t.replace('&',''))
 assert re.fullmatch(r'[a-zAX\d+ .-]+',t),t
 t=re.sub(r'(?<=\d)(?=[a-zAX])','*',t)
 names={n:sp.Symbol(n) for n in ['a','b','c','p','q','u','v','X1','X2','X3']}
 return sp.expand(sp.sympify(t,locals=names))
def equations(t):
 m=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',t,re.S);assert m,t
 return [expr(row.split('=')[0])-expr(row.split('=')[1]) for row in m[1].split(r'\\')]
def witness(record):
 q=record['question'];text=q[':question/problem'];es=equations(text)
 names=['X1','X2','X3'] if '{x}_{3}' in text else ['X1','X2'] if '{x}_{1}' in text else ['p','q'] if re.search(r'\bp|\dp',text) else ['u','v'] if re.search(r'\bu|\du',text) else ['a','b','c']
 syms=[sp.Symbol(n) for n in names];A=[];rhs=[]
 for e in es:
  row=[e.coeff(s) for s in syms];constant=e.subs(dict.fromkeys(syms,0))
  assert sp.expand(e-sum(v*s for v,s in zip(row,syms))-constant)==0
  A.append(row);rhs.append(-constant)
 target=tuple(tuple(row) if 'coefficient matrix' in text else tuple(row+[v]) for row,v in zip(A,rhs))
 f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
 assert len(choices)==5 and len({a[':answer/id'] for a in choices})==5
 values=[matrix(a[':answer/value']) for a in choices]
 assert len(set(values))==5 and values.count(target)==1
 assert next(matrix(a[':answer/value']) for a in choices if a[':answer/id']==correct)==target
 sm=re.findall(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}|\\left\[\\begin\{array\}.*?\\end\{array\}\\right\]',q[':question/worked-solution'],re.S)
 assert matrix(sm[0])==tuple(tuple(r) for r in A)
 assert matrix(sm[-1])==target
 if ':question.difficulty/moderate'==q[':question/difficulty']:assert equations(q[':question/worked-solution'])==es
 else:assert 'already organized' in q[':question/worked-solution'] and len(A)==2 and len(A[0])==2
 return target

def shortcut_report(records):
 groups=collections.defaultdict(list)
 for r in records:groups[r['generation']['bank_profile']].append(r)
 report={}
 for profile,rs in groups.items():
  outcomes=collections.defaultdict(list);positions=[];signs=[]
  for r in rs:
   target=witness(r);f=r['question'][':question/answer-fields'][0];vals=[matrix(a[':answer/value']) for a in f[':answer-field/choices']];pos=vals.index(target);positions.append(pos);signs.append(tuple(int(sp.sign(x)) for row in target for x in row))
   # Fixed positional strategies and content-only predicates: no prompt inspection.
   for j in range(5):outcomes['choice_position_'+str(j)].append(j==pos)
   for predicate in ['shape_2x3','most_zeros','fewest_negatives','most_negatives','largest_abs_sum','smallest_abs_sum']:
    def score(m):
     flat=[x for row in m for x in row]
     return {'shape_2x3':int(len(m)==2 and len(m[0])==3),'most_zeros':flat.count(0),'fewest_negatives':-sum(int(bool(x<0)) for x in flat),'most_negatives':sum(int(bool(x<0)) for x in flat),'largest_abs_sum':sum(abs(x) for x in flat),'smallest_abs_sum':-sum(abs(x) for x in flat)}[predicate]
    scores=[score(m) for m in vals];picks=[j for j,s in enumerate(scores) if s==max(scores)]
    outcomes[predicate].append(pos in picks and len(picks)==1)
   for cell in [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)]:
    # Is copying this same displayed cell sufficient every time?
    picks=[j for j,m in enumerate(vals) if len(m)==len(target) and len(m[0])==len(target[0]) and m[cell[0]][cell[1]]==target[cell[0]][cell[1]]]
    outcomes[f'match_prompt_cell_{cell}'].append(len(picks)==1 and picks[0]==pos)
    for sign in [-1,0,1]:
     picks=[j for j,m in enumerate(vals) if cell[0]<len(m) and cell[1]<len(m[0]) and sp.sign(m[cell[0]][cell[1]])==sign]
     outcomes[f'sign_at_{cell}_{sign}'].append(len(picks)==1 and pos==picks[0])
  assert len(set(positions))>=4,(profile,positions)
  assert len(set(signs))>=4,(profile,'fixed decision signs')
  assert all(not all(v) for v in outcomes.values()),(profile,'perfect incidental predictor')
  report[profile]={'records':len(rs),'correct_positions':dict(collections.Counter(positions)),'target_sign_patterns':len(set(signs)),'probes':{k:{'unique_correct':sum(v),'attempts':len(v)} for k,v in outcomes.items()},'baseline_fixed_random_position':0.2}
 return report

def main():
 # Regression for latest feedback: invoke the exact failed interface, inspect output.
 cmd=[PY,str(W/'17592186059770.py'),'--difficulty','easy','--count','5','--seed','0','--format','json']
 run=subprocess.run(cmd,text=True,capture_output=True);assert run.returncode==0,run.stderr
 latest=json.loads(run.stdout);assert len(latest)==5
 for r in latest:assert r['question'][':question/difficulty']==':question.difficulty/easy';witness(r)
 save('latest-failure-regression.json',{'command':cmd,'exit_code':run.returncode,'records':len(latest),'independent_visible_checks':'passed'})
 source=json.loads((W/'../source/source.json').read_text());qs={q.get(':question/math-academy-id'):q for q in source['material']['kp'][':knowledge-point/questions']}
 replay=[];fidelity=[];controls=[];pool=[]
 for profile,(values,names) in g.EASY_SOURCES.items():
  p=dict(zip('abcdef',values));r=g.generate('easy',profile=profile,parameters=p);replay.append(r);witness(r)
  for key in p:
   for value in (-p[key],9 if p[key]!=9 else 1):
    changed={**p,key:value}
    try:r2=g.generate('easy',profile=profile,parameters=changed)
    except ValueError:
     changed[key]=-9 if value>0 else 9;r2=g.generate('easy',profile=profile,parameters=changed)
    t=witness(r2);assert t!=witness(r);controls.append(r2)
  for seed in range(24):
   r2=g.generate('easy',seed,profile=profile);assert r2==g.generate('easy',seed,profile=profile);witness(r2);pool.append(r2)
 for template,profile in g.TEMPLATES.items():
  r=g.generate('moderate',template=template,parameters=g.SOURCE_PARAMETERS[template]);witness(r);replay.append(r)
  for seed in range(12):r2=g.generate('moderate',seed,template=template);witness(r2);pool.append(r2)
 for r in replay:
  profile=r['generation']['bank_profile'];s=qs[profile];sf=s[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0]
  original=[matrix(a[':answer/value']) for a in sf[':answer-field/choices']];made=[matrix(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(original)==len(made)==5 and set(original)==set(made),profile
  assert matrix(sf[':answer-field/correct'][':answer/value'])==witness(r)
  assert equations(s[':question/problem'])==equations(r['question'][':question/problem'])
  # Operative prose must replay; TeX whitespace/unit coefficient normalization may differ.
  prose=lambda t:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$','',t,flags=re.S)).strip()
  assert prose(s[':question/worked-solution'])==prose(r['question'][':question/worked-solution']),profile
  fidelity.append({'profile':profile,'source_id':s[':question/id'],'complete_bank':'5/5','distractors':'4/4','solution_prose':'matched','equations':'matched'})
 # Irrelevant presentation: changing shuffle seed preserves bank/mathematical response.
 for r in replay:
  kw={'profile':r['generation']['bank_profile'],'parameters':r['generation']['parameters']}
  if r['question'][':question/difficulty'].endswith('/moderate'):kw['template']=r['generation']['template']
  r2=g.generate(r['question'][':question/difficulty'].split('/')[-1],999,**kw)
  assert witness(r2)==witness(r)
 # Coefficient RHS is mathematically irrelevant; explicit control must preserve target.
 p={**g.SOURCE_PARAMETERS['coefficient'],'e':-5};r=g.generate('moderate',template='coefficient',parameters=p);witness(r);assert witness(r)==witness(replay[-2]);controls.append(r)
 save('source-replay.json',replay);save('fidelity.json',fidelity);save('controlled-records.json',controls)
 save('sample-records.json',[r for r in pool if r['question'][':question/difficulty'].endswith('/easy')])
 save('moderate-records.json',[r for r in pool if r['question'][':question/difficulty'].endswith('/moderate')])
 save('pedagogical-variation-before.json',shortcut_report(pool))
 save('learner-request.json',latest)
 # Check all choices; correctness expectation comes from visible-equation witness.
 cases=[]
 for r in replay+controls+pool:
  target=witness(r);f=r['question'][':question/answer-fields'][0]
  cases.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if matrix(a[':answer/value'])==target else 'rejected','purpose':'independent visible equation matrix'} for a in f[':answer-field/choices']]})
 save('native-input.json',cases)
 run=subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'native-input.json'),str(E/'native-report.json')],text=True,capture_output=True);assert run.returncode==0,run.stdout+run.stderr
 # Runtime closure: copy exactly manifest files into a fresh directory.
 manifest=json.loads((W/'package.json').read_text())
 with tempfile.TemporaryDirectory(prefix='ca-generator-') as tmp:
  root=Path(tmp)
  for name in manifest['files']:
   dest=root/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/name,dest)
  result=subprocess.run([PY,str(root/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','0','--format','json'],cwd=root,text=True,capture_output=True)
  assert result.returncode==0,result.stderr
  assert json.loads(result.stdout)==latest
 save('validation-summary.json',{'status':'passed','source_banks':len(fidelity),'source_distractors':4*len(fidelity),'controlled_records':len(controls),'sample_records':len(pool),'native_cases':len(cases),'native_checks':5*len(cases),'relocation':'passed','feedback':'easy runtime mismatch repaired','history_finding_ids':[]})
 print((E/'validation-summary.json').read_text())
if __name__=='__main__':main()
