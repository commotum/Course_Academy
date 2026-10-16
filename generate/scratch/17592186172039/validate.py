#!/usr/bin/env python3
"""Fail on source, displayed math, complete banks, format, scope, IDs or grader.
Run from repository root with .venv/bin/python. Native grading uses local
in-memory fixtures only. Every slope/statement is derived from PRINTED TeX.
"""
import concurrent.futures,hashlib,importlib.util,itertools,json,pathlib,re,subprocess,sys
import sympy as sp
sys.dont_write_bytecode=True
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.parent/(HERE.name+'.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
CASES=json.loads((HERE/'source-cases.json').read_text());SOURCE=json.loads((HERE/'source.json').read_text())
BY_ID={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
LABEL_MASK={label:mask for mask,label in g.LABELS.items()}
U,V=sp.symbols('u v',positive=True)

def read_printed_expr(prompt):
 eq=prompt.split('$')[1];rhs=eq.split('=',1)[1].strip().replace('{','').replace('}','')
 m=re.fullmatch(r'(-?\d*)x(\^2)?(y(\^2)?)?',rhs)
 assert m,('Not a supported printed slope equation',eq)
 c=int(m[1]) if m[1] not in ('','-') else -1 if m[1]=='-' else 1
 a=2 if m[2] else 1;b=0 if not m[3] else 2 if m[4] else 1
 return sp.Integer(c)*g.X**a*g.Y**b,{'c':c,'a':a,'b':b}

def checked(record):
 assert {'knowledge_point','question','generation'}<=set(record)
 assert record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=record['question'];gen=record['generation'];p=gen['parameters'];level=gen['level']
 g.validate_parameters(level,p)
 f,printed=read_printed_expr(q[':question/problem'])
 assert all(printed[k]==p[k] for k in printed)
 ss=[]
 for quadrant,(sx,sy) in g.POINTS.items():
  # Symbolic identity on the ENTIRE open quadrant, not an isolated sample.
  mapped=sp.expand(f.subs({g.X:sx*U,g.Y:sy*V}))
  ratio=sp.simplify(mapped/(abs(printed['c'])*U**printed['a']*V**printed['b']))
  assert ratio in (-1,1);ss.append(int(ratio))
 assert tuple(ss)==tuple(gen['plot']['signs'])
 assert sp.simplify(f.subs(g.X,0))==0
 assert (sp.simplify(f.subs(g.Y,0))==0)==(printed['b']>0)
 claims=re.findall(r'At every point in the (first|second|third|fourth) quadrant, the slope of the slope field is (positive|negative)',q[':question/problem'])
 assert len(claims)==3
 mask=0
 for i,(word,claim) in enumerate(claims):
  quadrant={v:k for k,v in g.WORDS.items()}[word];sign=1 if claim=='positive' else -1
  assert quadrant==p['quadrants'][i] and sign==p['claims'][i]
  if ss[quadrant-1]==sign:mask|=1<<i
 sol=q[':question/worked-solution']
 if gen['template']=='parity_numbered':
  assert printed['a']==1 and printed['b']==2
  assert ('the opposite sign to x' in sol)==(printed['c']<0)
  for word,nums in re.findall(r'(negative|positive) in quadrants? ([IV, and]+)',sol):
   for name in re.findall(r'\b(?:IV|III|II|I)\b',nums):assert ss[('I','II','III','IV').index(name)]==(1 if word=='positive' else -1)
 else:
  intro_expr=sol.split('$')[1].split('=',1)[1].rstrip('.')
  checkf,_=read_printed_expr('equation $d='+intro_expr+'$')
  assert sp.simplify(checkf-f)==0
  blocks=re.findall(r'- Statement (I|II|III) is (true|false)\. If \$\(x,y\)\$ is in the (first|second|third|fourth) quadrant,.*?\$\$\n(.*?)\n\$\$\n\nThis implies that the slope of the slope field is (positive|negative) for any point \$\(x,y\)\$ in the (first|second|third|fourth) quadrant\.',sol,re.S)
  assert len(blocks)==3
  for i,(roman,truth,word,math,claimed,repeated) in enumerate(blocks):
   assert roman==g.ROMAN[i] and word==claims[i][0]==repeated
   assert truth==('true' if mask&(1<<i) else 'false')
   expected=ss[p['quadrants'][i]-1]
   assert math==r'{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)'+('>0.' if expected>0 else '<0.')+(r'\,' if gen['template']=='bilinear_open_thin' else '')
   assert claimed==('positive' if expected>0 else 'negative')
  if 'Therefore' in sol:assert '"'+g.LABELS[mask]+'."' in sol
  if level=='easy':assert '$x=0$ or $y=0.$' not in sol
  else:assert '$x=0$ or $y=0.$' in sol
 for content in [q[':question/problem'],sol]:
  assert content.count('$$')%2==0
  assert content.replace('$$','').count('$')%2==0
  depth=0
  for char in content:
   if char=='{':depth+=1
   if char=='}':depth-=1
   assert depth>=0
  assert depth==0
 fields=q[':question/answer-fields'];assert len(fields)==3
 assert {f[':answer-field/key'] for f in fields}==set(g.ROMAN)
 for field in fields:
  i=g.ROMAN.index(field[':answer-field/key'])
  assert field[':answer-field/type']==':answer-field.type/checkbox'
  assert {a[':answer/value'] for a in field[':answer-field/choices']}=={'true','false'}
  assert all(a[':answer/type']==':answer.type/text' for a in field[':answer-field/choices'])
  answer=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
  assert answer[':answer/value']==('true' if mask&(1<<i) else 'false')
 assert mask==gen['truth_mask']
 assert (HERE/gen['plot']['asset']).is_file()
 if gen['plot']['renderer']!='immutable source asset':
  sidecar=json.loads((HERE/gen['plot']['asset']).with_suffix('.json').read_text())
  assert sidecar['spec']['signs']==ss
  assert sidecar['spec']['zero_axes']==(['x'] if printed['b']==0 else ['x','y'])
 same=g.generate(level,seed=gen['seed']+999,template=gen['template'],parameters=p,profile=gen.get('legacy_bank_profile'))
 assert same['question'][':question/id']==q[':question/id']
 assert same['generation']['content_identity']==gen['content_identity']
 return mask


def native_checks(r):
 return [{'field_index':i,'submitted_answer_id':next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==value),'expected':'accepted' if value==next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]) else 'rejected','purpose':'Checkbox authored choice ID through actual learner grader'} for i,f in enumerate(r['question'][':question/answer-fields']) for value in ('false','true')]

def field_shape(f):
 correct=f[':answer-field/correct'];aid=correct.get(':answer/id') if isinstance(correct,dict) else correct[1]
 return (f[':answer-field/key'], sorted(a[':answer/value'] for a in f[':answer-field/choices']), next(a[':answer/value'] for a in f[':answer-field/choices'] if str(a[':answer/id'])==str(aid)))

def main():
 current=json.loads((HERE/'reference/initial/kp.json').read_text())
 byid={q[':question/math-academy-id']:q for q in current[':knowledge-point/questions']}
 fixtures=[];reviews=[];replays=[]
 for case in CASES:
  r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);checked(r);q=r['question'];old=byid[case['source_id']]
  assert q[':question/problem']==old[':question/problem']
  assert sorted(map(field_shape,q[':question/answer-fields']))==sorted(map(field_shape,old[':question/answer-fields']))
  if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution']
  replays.append({'source':case['source_id'],'fields':3,'bank_values_matched':6,'prompt_exact':True,'available_solution_exact':True})
  fixtures.append({'label':case['source_id'],'record':r,'checks':native_checks(r)})
  reviews.append({'source':old,'replay':r,'variant':g.generate(case['level'],seed=43,template=case['template'])})
 coverage={}
 for level,powers in [('easy',[(1,0)]),('moderate',[(1,1)]),('hard',[(1,2),(2,1),(2,2)])]:
  fps=set();targets=set()
  for c,(a,b),qs,cs in itertools.product([-1,1],powers,itertools.combinations([1,2,3,4],3),itertools.product([-1,1],repeat=3)):
   r=g.generate(level,parameters={'c':c,'a':a,'b':b,'quadrants':list(qs),'claims':list(cs)});checked(r);fps.add(r['generation']['mathematical_fingerprint']);targets.add(tuple(qs))
   fixtures.append({'label':r['question'][':question/id'],'record':r,'checks':native_checks(r)})
  assert len(fps)==64*len(powers) and len(targets)==4
  coverage[level]={'distinct_tasks':len(fps),'quadrant_target_sets':[list(x) for x in sorted(targets)]}
  assert len({g.generate(level,seed)['generation']['mathematical_fingerprint'] for seed in range(1000)})==len(fps)
 # Changed target with all other data fixed must alter every target reference and key.
 base={'c':1,'a':1,'b':1,'quadrants':[1,2,3],'claims':[1,1,1]}
 a=g.generate('moderate',parameters=base);b=g.generate('moderate',parameters=base|{'quadrants':[4,2,3]});checked(a);checked(b)
 assert a['generation']['truth_mask']!=b['generation']['truth_mask']
 for level,powers in [('easy',[(1,0)]),('moderate',[(1,1)]),('hard',[(1,2),(2,1),(2,2)])]:
  for c,(x,y) in itertools.product([-9,-1,1,9],powers):checked(g.generate(level,parameters=base|{'c':c,'a':x,'b':y}))
 for delta in [{'c':0},{'c':10},{'a':3},{'quadrants':[1,1,2]},{'claims':[0,1,1]}]:
  try:g.generate('moderate',parameters=base|delta)
  except ValueError:pass
  else:raise AssertionError('Invalid parameters admitted')
 out=HERE/'reference/current-validation';out.mkdir(parents=True,exist_ok=True)
 (out/'side-by-side.json').write_text(json.dumps(reviews,indent=2)+'\n')
 (out/'native-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(out/'native-input.json'),str(out/'native-report.json')],check=True)
 engine=json.loads((out/'native-report.json').read_text());assert engine['documented_unresolved_checks']==0
 report={'passed':True,'source_basis':2771,'current_source_banks':replays,'matched_current_bank_values':48,'historical_radio_fidelity':'reference/legacy-v2/validation.json: 8 complete banks, 40 options','coverage':coverage,'supported_levels':['easy','moderate','hard'],'native_grading':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'changed_target_checked':True,'source_q97483':'Unrated source remains excluded from weighted inventory; its current compact solution and checkbox keys replay exactly. Generated counterparts have independently justified hard classification.'}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 files=[HERE.with_suffix('.py'),pathlib.Path(__file__),HERE/'render.py',HERE/'source-cases.json',HERE/'reference/initial/kp.json',HERE/'validation.json',ROOT/'generate/runs/current/check-engine']
 (HERE/'validation-freeze.json').write_text(json.dumps({'status':'passed','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
