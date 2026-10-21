"""Compare every math fragment in source prompts/solutions with replay.
Source q-319350's erroneous LHS is preserved here; served repairs are math-tested separately.
"""
import json,re
from pathlib import Path
import sympy as s
import generator as g

def parts(text):
 result=[]
 for m in re.finditer(r'\$\$([\s\S]*?)\$\$|\$([^$]*)\$',text):
  z=(m[1] if m[1] is not None else m[2]).strip().rstrip('.')
  z=z.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  for row in z.split(r'\\'):
   for side in row.replace('&','').split('='):
    side=side.strip().rstrip('.').replace(r'\,','').rstrip(' +')
    if side:result.append(g.parse(side,{'u':s.Function('u')(g.X),'v':s.Function('v')(g.X)}))
 return result
replays=json.loads(Path('evidence/source-replay.json').read_text());report=[];count=0
for r in replays:
 t=r['generation']['template'];q=r['question'];raw=g.QUESTIONS[t];n=0
 for k in [':question/problem',':question/worked-solution']:
  if k in raw:
   a,b=parts(raw[k]),parts(q[k]);assert len(a)==len(b),(t,k,len(a),len(b))
   for x,y in zip(a,b):assert s.trigsimp(s.simplify(x-y))==0,(t,k,x,y)
   n+=len(a)
 # Nonmathematical prose and placeholder layout remain the source's literal prose.
 def prose(z):return re.sub(r'\s+',' ',re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$','<MATH>',z)).strip()
 for k in [':question/problem',':question/worked-solution']:
  if k in raw:assert prose(raw[k])==prose(q[k]),(t,k,'prose/layout')
 report.append({'source_id':t,'compared_math_fragments':n,'prose_and_placeholder_layout_match':True});count+=n
out={'passed':True,'sources':len(report),'math_fragments':count,'cases':report,'source_error':'q-319350 first LHS incorrectly names e^x sec x; preserved only in raw evidence, corrected in all served solutions.','response_fidelity':'Every supplied field type and complete bank retained in raw replay; q-71004 has no source fields and is repaired with one full-derivative blank for served records.'}
Path('evidence/source-fidelity.json').write_text(json.dumps(out,indent=2));print('source fidelity',len(report),'cases,',count,'math fragments, PASS')
