"""Source-driven completeness, full-bank and independent visible-math regression."""
import json, re, sys
from fractions import Fraction
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import generator as g

def save(name,value):
 p=ROOT/'evidence'/name;p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(value,indent=2)+'\n')

def matrices(text):
 return [[[int(v.strip()) for v in row.split('&')] for row in m[2].split(r'\\')] for m in re.finditer(r'\\begin\{(bmatrix|array)\}(?:\{[^}]*\})?(.*?)\\end\{\1\}',text,re.S)]

def system(text):
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)[1];out=[]
 for row in block.split(r'\\'):
  lhs,rhs=row.replace('&','').split('=');coeff=[]
  for v in 'xyz':
   m=re.search(r'([+-]?\d*)'+v,lhs.replace(' ',''));c=m[1] if m else '0';coeff.append(int(c+'1') if c in ('','+','-') else int(c))
  out.append(coeff+[int(rhs.strip().rstrip('.,'))])
 return out

def solve(rows):
 # Fraction-based Gauss-Jordan witness independent of generator/SymPy.
 m=[[Fraction(x) for x in r] for r in rows]
 for col in range(3):
  pivot=next(i for i in range(col,3) if m[i][col]);m[col],m[pivot]=m[pivot],m[col];a=m[col][col];m[col]=[x/a for x in m[col]]
  for i in range(3):
   if i!=col:
    a=m[i][col];m[i]=[x-a*y for x,y in zip(m[i],m[col])]
 return [[int(v) if v.denominator==1 else str(v) for v in row] for row in m]

def triple(value):
 ms=matrices(value)
 if ms:return [r[3] for r in ms[0]]
 if 'langle' in value or '⟨' in value:return list(map(int,re.findall(r'-?\d+',value)))
 return [int(re.search(v+r'\s*=\s*(-?\d+)',value)[1]) for v in 'xyz']

def check(record):
 q=record['question'];initial=system(q[':question/problem']);reduced=solve(initial);target=[row[3] for row in reduced];ms=matrices(q[':question/worked-solution'])
 assert ms[0]==initial and ms[-1]==reduced, 'Displayed solution endpoints'
 ops=re.findall(r'R_\{(\d)\}:=R_\{\d\}([+-])(\d*)R_\{(\d)\}',q[':question/worked-solution']);assert len(ops)==len(ms)-1
 for before,after,(i,sign,n,j) in zip(ms,ms[1:],ops):
  expected=[r[:] for r in before];factor=(int(n) if n else 1)*(1 if sign=='+' else -1);expected[int(i)-1]=[x+factor*y for x,y in zip(before[int(i)-1],before[int(j)-1])];assert expected==after,'Displayed row operation'
 fs=q[':question/answer-fields']
 if fs:
  f=fs[0];bank=[triple(c[':answer/value']) for c in f[':answer-field/choices']];assert len(bank)==5 and len(set(map(tuple,bank)))==5
  correct=[c[':answer/id'] for c,v in zip(f[':answer-field/choices'],bank) if v==target];assert correct==[f[':answer-field/correct'][1]],'Unique independently verified key'
  if not matrices(f[':answer-field/choices'][0][':answer/value']):
   assert triple(q[':question/worked-solution'].split('So, we have the solution ')[1].split(' Or,')[0])==target
 else:
  assert record['generation']['evidence_only'] and not record['generation']['eligible_for_learning']
 return target

def source_regression():
 cases=json.loads((ROOT/'evidence/source-cases.json').read_text());live=ROOT.parent/'source/source.json'
 if live.exists():
  kp=json.loads(live.read_text())['material']['kp'];assert cases==kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']], 'Captured source changed: refresh and explain evidence'
 assert set(g.SOURCE_CASES)=={q[':question/math-academy-id'] for q in cases}, 'Registry must account for every captured case'
 reports=[];records=[]
 for q in cases:
  name=q[':question/math-academy-id'];r=g.generate(difficulty='easy',seed=731,template=name,replay=True);target=check(r);out=r['question'];assert system(q[':question/problem'])==system(out[':question/problem'])
  fs=q.get(':question/answer-fields',[]);outfs=out[':question/answer-fields'];assert len(fs)==len(outfs)
  if fs:
   f=fs[0];got=outfs[0];assert f[':answer-field/type'][':db/ident']==got[':answer-field/type'];assert sorted(triple(c[':answer/value']) for c in f[':answer-field/choices'])==sorted(triple(c[':answer/value']) for c in got[':answer-field/choices'])
   assert sorted(c[':answer/type'][':db/ident'] for c in f[':answer-field/choices'])==sorted(c[':answer/type'] for c in got[':answer-field/choices'])
  # Compare complete observed operative stages, ignoring the captured repeated initial matrix.
  if q.get(':question/worked-solution'):
   stages=[]
   for m in matrices(q[':question/worked-solution']):
    if not stages or stages[-1]!=m:stages.append(m)
   assert stages==matrices(out[':question/worked-solution']), 'Source operative stages changed'
  else:assert name=='q-20589'
  raw=g.SOURCE_CASES[name]['difficulty'];expected=q.get(':question/difficulty',{}).get(':db/ident');assert raw in (expected,expected.rsplit('/',1)[-1] if expected else None)
  reports.append({'profile':name,'source_uuid':q[':question/id'],'solution':target,'complete_bank':bool(fs),'choices_matched':sum(len(f[':answer-field/choices']) for f in fs),'worked_stages_matched':bool(q.get(':question/worked-solution')),'captured_difficulty':expected,'key_inferred':name=='q-20589','key_corrected':name=='q-131590'});records.append(r)
 assert 'e-4709' not in g.PROFILES,'Fieldless canonical example must not enter practice sampler'
 save('source-replay-records.json',records);save('source-replay.json',{'passed':len(reports),'complete_banks':sum(x['complete_bank'] for x in reports),'choices_matched':sum(x['choices_matched'] for x in reports),'cases':reports})
 print(json.dumps({'source_cases':len(reports),'complete_banks':14,'choices_matched':70,'failures':[]}))
 return records
if __name__=='__main__':source_regression()
