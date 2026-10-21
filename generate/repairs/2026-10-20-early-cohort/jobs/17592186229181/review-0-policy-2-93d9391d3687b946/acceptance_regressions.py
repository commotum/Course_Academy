"""Strict independent regressions: exit nonzero on the demonstrated generator defects.
Run with the context Python; optional first argument is an alternate package root.
"""
import sys
sys.dont_write_bytecode=True
import pathlib,importlib.util,json,re,collections,ast
import sympy as sp
ROOT=pathlib.Path(__file__).resolve().parent
PKG=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'workspace'
manifest=json.load(open(PKG/'package.json')); spec=importlib.util.spec_from_file_location('candidate',PKG/manifest['entrypoint']);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
tree=ast.parse((ROOT/'review_checks.py').read_text())
for n in tree.body:
 if isinstance(n,ast.FunctionDef) and n.name in ['key','ex','shortcut'] or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EX' for t in n.targets):exec(compile(ast.Module(body=[n],type_ignores=[]),'<independent review helpers>','exec'))
cases=[]
def test(label,fn):
 try:fn();cases.append({'test':label,'passed':True})
 except Exception as e:cases.append({'test':label,'passed':False,'exception':type(e).__name__,'failure':str(e)})
def no_bank_only_answer():
 r=m.generate('easy',81031); q=r['question'];pick=shortcut(q)
 assert pick!=key(q), 'Seed 81031: prompt-free repeated-constant/modal-initial-value strategy selects the correct UUID '+str(pick)
test('minimal prompt-free shortcut',no_bank_only_answer)
s=json.load(open(ROOT.parent/'source/source.json'))
for source in s['material']['kp'][':knowledge-point/questions']:
 def replay_current(q=source):
  sid=q[':db/id'];level='moderate' if 'rounded' in q[':question/problem'] else 'easy';r=m.generate(level,61829,template='source_'+str(sid));rq=r['question']
  for field in [':question/worked-solution',':question/difficulty']:
   assert (field in rq)==(field in q),str(sid)+' current source attribute presence mismatch: '+field
  assert bool(key(rq))==bool(key(q)),str(sid)+' current source correct-link presence differs'
  normalize=lambda x:re.sub(r'\s+','',x).replace('{e}','e')
  banks=lambda x:sorted(normalize(a[':answer/value']) for a in x[':question/answer-fields'][0][':answer-field/choices'])
  assert banks(rq)==banks(q),str(sid)+' complete bank differs beyond harmless whitespace and e bracing'
 test('current source '+source[':question/id'],replay_current)
report={'package':str(PKG),'cases':cases,'passed':all(x['passed'] for x in cases),'command':f'{sys.executable} {ROOT}/acceptance_regressions.py {PKG}'}
(ROOT/'acceptance-regressions.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'failures':[x for x in cases if not x['passed']]},indent=2))
raise SystemExit(0 if report['passed'] else 1)
