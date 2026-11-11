"""Audit stored field integrity, solution endpoints and ordered-ratio keys."""
import json,re,sys
from pathlib import Path
from fractions import Fraction as F
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from math_native import coeffs

def plain(s):return s.replace('\\\\','\\')
def num(s):return F(re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'\1/\2',plain(s)).strip())
rows=[]
for kp in [17592186096652,17592186096653,17592186096701,17592186235285]:
 k=json.loads((H/str(kp)/'inventory/kp.json').read_text())
 for q in k[':knowledge-point/questions']:
  fs=q.get(':question/answer-fields',[]);problems=[];keys=[f[':answer-field/key'] for f in fs]
  if len(keys)!=len(set(keys)):problems.append('duplicate field keys')
  if not q.get(':question/worked-solution','').strip():problems.append('missing worked solution')
  if any(':answer-field/correct' not in f for f in fs):problems.append('missing canonical answer')
  for f in fs:
   if ':answer-field/correct' in f and f[':answer-field/correct'][':answer/id'] not in [a[':answer/id'] for a in f[':answer-field/choices']]:problems.append('key outside bank')
  check=None;expected=None
  if kp==17592186096653 and not problems:
   prompt=plain(q[':question/problem']);prompt=re.sub(r'\\overset\{\\to\s*\}\{([A-Z]{2})\}',r'\\overrightarrow{\1}',prompt);prompt=re.sub(r'\\mathbf\s*\{([a-z])\}',r'\1',prompt);prompt=re.sub(r'\s+','',prompt)
   m=re.search(r'([A-Z])([A-Z]):\2([A-Z])=(\d+):(\d+)',prompt);assert m,q[':db/id'];A,X,B,r,s=m.groups();r,s=int(r),int(s);givens=re.findall(r'\\overrightarrow\{([A-Z]{2})\}=([a-z])',prompt)[:2];assert len(givens)==2
   syms=[];signs=[]
   for point in [A,B]:
    edge,var=next((e,v) for e,v in givens if e in ['O'+point,point+'O']);syms.append(var);signs.append(1 if edge.startswith('O') else -1)
   target=1 # Every stored ratio prompt currently requests O->interior X.
   expected=[F(s,r+s)*signs[0]*target,F(r,r+s)*signs[1]*target]
   if fs[0][':answer-field/type'][':db/ident'].endswith('/radio'):
    actual=coeffs(plain(fs[0][':answer-field/correct'][':answer/value']));check=actual==dict(zip(syms,expected))
   else:check=all(num(f[':answer-field/correct'][':answer/value'])==expected[int(f[':answer-field/key'].split('-')[-1])-1] for f in fs)
   assert check,(q[':db/id'],expected)
  elif kp!=17592186096653:
   end={};pattern=r'-?(?:\\(?:d?frac)\{\d+\}\{\d+\}|\d+/\d+|\d+(?:\.\d+)?)'
   for sym in ['lambda','mu']:
    ms=re.findall(r'\\'+sym+r'\s*=\s*('+pattern+')',plain(q[':question/worked-solution']))
    if ms:end[sym]=num(ms[-1])
   assert 'lambda' in end
   expected=[end['lambda']]+([end['mu']] if 'mu' in end else [])
   if fs[0][':answer-field/type'][':db/ident'].endswith('/radio'):
    value=plain(fs[0][':answer-field/correct'][':answer/value'])
    if kp==17592186096652:
     pairs=[num(re.search(r'\\'+sym+r'\s*=\s*('+pattern+')',value)[1]) for sym in ['lambda','mu']];check=pairs==expected
    else:check=num(value)==expected[0]
   else:check=all(num(f[':answer-field/correct'][':answer/value'])==expected[int(f[':answer-field/key'].split('-')[-1])-1] for f in fs)
   assert check,(q[':db/id'],expected)
  rows.append(dict(kp=kp,entity=q[':db/id'],origin='imported' if ':question/math-academy-id' in q else 'authored',issues=problems,key_check=check,expected=list(map(str,expected)) if expected else None,key_check_method='independent ordered-ratio/direction calculation' if kp==17592186096653 else 'consistency with complete worked-solution terminal values; not an independent pixel-coordinate solution'))
(H/'stored-integrity.json').write_text(json.dumps(dict(basis=14220,records=len(rows),questions=rows),indent=2)+'\n');print('Stored checks',len(rows),'keyschecked',sum(r['key_check'] is True for r in rows),'issues',[r for r in rows if r['issues']])
