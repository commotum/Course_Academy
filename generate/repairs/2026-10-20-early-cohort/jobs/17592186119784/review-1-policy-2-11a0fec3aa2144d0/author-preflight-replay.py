#!/usr/bin/env python3
"""Executable retained regressions. Offline, no runtime file mutations."""
import sys
sys.dont_write_bytecode=True
import json,pathlib,importlib.util,re,collections
P=pathlib.Path(__import__('os').environ['REVIEW_PACKAGE'])
sys.path.insert(0,str(P))
spec=importlib.util.spec_from_file_location('current_generator',P/'17592186119784.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
E=pathlib.Path(__import__('os').environ['REVIEW_AUTHOR_EVIDENCE']);E.mkdir(exist_ok=True)
def save(name,x):(E/name).write_text(json.dumps(x,indent=2))
def matrix(text):
 s=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)[1]
 return [[int(x.strip()) for x in row.split('&')] for row in s.split(r'\\')]
def selected(f):
 return next(a[':answer/value']=='true' for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def ordinary(r):return [selected(f) for f in r['question'][':question/answer-fields'] if f[':answer-field/key']!='None of the above']
def evaluate(m,key):
 expr=re.search(r'\$(.*?)\$',key)[1];e=re.sub(r'[{}\s]','',expr);name=re.search('[A-E]',e)[0];e=e.replace(name,'M')
 n=len(m);t=[[m[j][i] for j in range(n)] for i in range(n)]
 if e=='M':b=m
 elif e=='M^T':b=t
 elif e in ('M^T+M','M+M^T'):b=[[m[i][j]+t[i][j] for j in range(n)] for i in range(n)]
 elif e=='M-M^T':b=[[m[i][j]-t[i][j] for j in range(n)] for i in range(n)]
 elif e=='M^T-M':b=[[t[i][j]-m[i][j] for j in range(n)] for i in range(n)]
 else:raise AssertionError(e)
 region=[(i,j) for i in range(n) for j in range(n) if (i>j if 'upper triangular' in key else i<j if 'lower triangular' in key else i!=j)]
 return all(b[i][j]==0 for i,j in region),b

def audit(r):
 q=r['question'];m=matrix(q[':question/problem']);vs=[]
 solution=q[':question/worked-solution']
 stages=re.findall(r'- (\$.*?\$ is (?:upper triangular|lower triangular|diagonal)): \*\*(true|false)\*\*\.(.*?)(?=\n\n- |\Z)',solution,re.S)
 for f in q[':question/answer-fields']:
  if f[':answer-field/key']=='None of the above':continue
  good,b=evaluate(m,f[':answer-field/key']);assert selected(f)==good
  vs.append(good)
  if not r['generation']['evidence_only']:
   stage=next(s for s in stages if s[0]+'.'==f[':answer-field/key'])
   assert stage[1]==str(good).lower() and matrix(stage[2])==b
   if not good:
    witness=re.search(r'row (\d+), column (\d+) is \$(-?\d+)',stage[2]);i,j,v=map(int,witness.groups());assert b[i-1][j-1]==v and v!=0
 none=[f for f in q[':question/answer-fields'] if f[':answer-field/key']=='None of the above']
 if none:assert selected(none[0])== (not any(vs))
 assert any(selected(f) for f in q[':question/answer-fields'])
 return vs

def controls(sid):
 n=len(g.TEMPLATES[sid]['source_matrix']);base=[[i+1 if i==j else 0 for j in range(n)] for i in range(n)]
 import copy
 cases=[]
 for kind in ['diagonal','upper','lower','neither','symmetric','skew']:
  m=copy.deepcopy(base)
  if kind in ('upper','neither','symmetric','skew'):m[0][-1]=2
  if kind in ('lower','neither','symmetric'):m[-1][0]=2 if kind=='symmetric' else 3
  if kind=='skew':m[-1][0]=-2
  cases.append((kind,m))
 return cases

def main():
 # Exact prior rejection: actual generated visible keys, not metadata.
 a=g.generate('moderate',101,'q-42091',parameters={'matrix':[[4,0,0],[1,1,0],[0,0,3]]})
 b=g.generate('moderate',101,'q-42091',parameters={'matrix':[[4,0,0],[0,1,0],[0,0,3]]})
 assert audit(a)==[False,True,True] and audit(b)==[True,True,True]
 save('exact-counterexample.json',[a,b])
 contract=json.loads((E/'source-contract.json').read_text())
 assert g.SOURCE['record']==contract
 assert len(contract[':knowledge-point/questions'])==12
 replay=[];records=[];coverage={};graders=[]
 for sid,t in g.TEMPLATES.items():
  if sid!='direct-properties':
   r=g.generate(t['level'],101,sid,profile='source-replay');q=g.QS[sid];rq=r['question'];audit(r)
   assert rq[':question/problem']==q[':question/problem'] and rq[':question/worked-solution']==q[':question/worked-solution']
   assert rq.get(':question/difficulty')==g.enum(q.get(':question/difficulty'))
   assert [(f[':answer-field/key'],[a[':answer/value'] for a in f[':answer-field/choices']],selected(f)) for f in rq[':question/answer-fields']]==[(f[':answer-field/key'],[a[':answer/value'] for a in f[':answer-field/choices']],f[':answer-field/correct'][':answer/value']=='true') for f in q[':question/answer-fields']]
   replay.append(r)
  n=len(t['source_matrix']);boundary=[[0]*n for _ in range(n)];boundary[0][0]=-8;boundary[-1][-1]=8
  audit(g.generate(t['level'],0,sid,parameters={'matrix':boundary}))
  try:g.generate(t['level'],0,sid,parameters={'matrix':[[9]*n for _ in range(n)]})
  except ValueError:pass
  else:raise AssertionError('Out-of-range matrix accepted')
  patterns=set();rs=[]
  for case,m in controls(sid):
   r=g.generate(t['level'],101,sid,parameters={'matrix':m});patterns.add(tuple(audit(r)));rs.append(r);records.append(r)
   # Diagonal entries are irrelevant; preserve every field verdict.
   changed=[row[:] for row in m]
   for i in range(len(m)):changed[i][i]=0
   irrelevant=g.generate(t['level'],101,sid,parameters={'matrix':changed});assert ordinary(irrelevant)==ordinary(r);audit(irrelevant)
  assert len(patterns)==(5 if t['level']=='hard' else 4),(sid,patterns)
  # Ordinary position and correct-selection count cannot identify the subset.
  by_count=collections.defaultdict(set)
  for r in rs:by_count[sum(selected(f) for f in r['question'][':question/answer-fields'])].add(tuple(ordinary(r)))
  assert any(len(v)>1 for v in by_count.values())
  sampled=[]
  for seed in range(8):
   r=g.generate(t['level'],seed,sid);sampled.append(tuple(audit(r)))
  assert len(set(sampled))>1,(sid,sampled)
  coverage[sid]={'level':t['level'],'controlled_truth_patterns':[list(v) for v in sorted(patterns)],'seeded_truth_patterns':[list(v) for v in sorted(set(sampled))]}
  # Real native checks cover every changed region/cancellation outcome.
  for r in rs:
   checks=[]
   for i,f in enumerate(r['question'][':question/answer-fields']):
    correct=selected(f)
    for a in f[':answer-field/choices']:
     checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if (a[':answer/value']=='true')==correct else 'rejected','purpose':'independent visible-matrix region arithmetic'})
   graders.append({'label':sid,'record':r,'checks':checks})
 save('source-replay.json',replay);save('controlled-records.json',records);save('coverage.json',coverage);save('grader-input.json',graders)
 fresh=[g.generate(level,4077425948+i) for level in ('moderate','hard') for i in range(5)]
 for r in fresh:audit(r)
 save('fresh-records.json',fresh)
 for level in ('moderate','hard'):save(level+'-records.json',[r for r in records+fresh if r['generation']['level']==level])
 save('render-records.json',[records[1],records[3],next(r for r in records if r['generation']['template']=='q-126474' and ordinary(r)==[False,False,True]),records[4]])
 print(json.dumps({'replay':len(replay),'controlled':len(records),'seeded':8*len(coverage),'exact_counterexample':'passed','profiles_per_template':{s:len(c['controlled_truth_patterns']) for s,c in coverage.items()}}))
if __name__=='__main__':main()
