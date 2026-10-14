"""One-time extraction of source numeric atoms into explicitly annotated semantic roles.
Slots are parsed inside complete prompt/solution components, never global replacements.
Every literal exponent and widget-key digit is marked separately from variable roles.
"""
import json,re
from pathlib import Path
H=Path(__file__).parent
S=json.loads((H/'source.json').read_text())['record'][':knowledge-point/questions']
# Ordered digit-token roles for each prompt and each numeric-bearing solution line.
R={
'q-17373':(['n','d','t'],[]),
'q-17395':(['b','c','t'],[]),
'q-101723':(['a','c','b','t'],[['a','c','b'],['t'],['t','a','c','b','t','a','t','c','t','b','a','t','c/t','b']]),
'q-340014':(['a',':2','c','t',':1'],[['a',':2','c','a',':2','c','a',':2','c',':1','2*a','c'],['t'],['t','2*a','c','t','2*a','t','c','t','answer']]),
'q-340022':(['a','c','b','t',':1'],[['a','c','b','a','c','b','a',':1','c','b','b','a','c','b','b'],['t'],['t','a','c','b','b','t','a','t','c','b','b','t','a','t','c*b**t','b']]),
'q-340109':(['a','c','b','t',':1'],[['a','c','b','a','c','b','a','c',':1','b','a','c','b'],['t'],['t','a','c','b','t','a','t','c','t','b','a','t','c/t','b']]),
'q-70897':(['a','b','b','t'],[['a','b','b','b'],['t'],['t','a','b','b','b','t','a','t','b','b','t','b','a/t','b','b**t','b']]),
'q-101726':(['a','k','c','b',':1','b'],[['a','k','c','b','a','k','c','b','a','k','c','b','a',':0','c',':1','b','a','c','b'],[':1','b'],[':1','b','a','c','b',':1','b','a','c',':1','b','b','a','c','answer']]),
'q-17371':(['a','c',':2','k','t'],[['a','c',':2','k','a','c',':2','k','a','c',':2','k','a',':1','2*c','k','a','2*c','k'],['t'],['t','a','2*c','k','t','a','t','2*c','t','k','a/t','2*c*t','k','answer']]),
'q-340024':(['a',':3','c','b','t',':1'],[['a',':3','c','b','a',':3','c','b','a',':3',':2','c',':1','b','3*a',':2','c','b'],['t'],['t','3*a',':2','c','b','t','3*a','t',':2','c','t','b','3*a*t**2','c','t','b']]),
'q-340026':(['a','b','c',':2','k','t',':1'],[['a','b','c',':2','k','a','b','c',':2','k','a',':1','b','c',':2','k','a','b','2*c','k'],['t'],['t','a','b','2*c','k','t','a','t','b','2*c','t','k','a/t','b','2*c*t-k']]),
'q-340110':(['a','c','b','k','t',':1'],[['a','c','b','k','a','c','b','k','a','c',':1','b',':0','a','c','b'],['t'],['t','a','c','b','t','a','t','c','t','b','a','t','c/t','b']]),
'q-70903':(['a',':3','k','t'],[['a',':10',':3',':2'],[':1'],['t','a',':10',':3',':2','t','a','t',':10',':3','t',':2','a/t',':10','3*t**2']])
}
A={
'q-17373':[['d','n'],[':0'],['n','d'],['n','d'],['d','n']],
'q-17395':[[':1','b'],['b','c'],[':0'],['c','b'],[':1','b','c']],
'q-340014':[['answer']],
'q-340022':[['a','t','c*b**t','b']],
'q-340109':[['a','t','c/t','b'],['a','t','c/t','b']],
'q-101726':[['a+1'],['a','c','b'],['answer'],['c','b','k-a'],['a+c-k']],
'q-17371':[['answer'],['a'],['answer'],['a+2*c+k'],['k']],
'q-340024':[['3*a*t**2','c','t','b']],
'q-340026':[['a/t','b','2*c*t-k']],
'q-340110':[['a','t','c/t','b']],
'q-70903':[['a*t',':10','t'],['a/t',':10','3*t**2'],['a/t','t',':10','t'],['a/t',':10','t**2'],['a',':10','t**2']]
}
def mask(s,roles):
 matches=list(re.finditer(r'\d+',s));assert len(matches)==len(roles),(s,len(matches),roles)
 out=[];last=0
 for m,r in zip(matches,roles):out += [s[last:m.start()],m[0] if r.startswith(':') else '@@'+r+'@@'];last=m.end()
 return ''.join(out)+s[last:]
out={}
for q in S:
 sid=q[':question/math-academy-id'];pr,sr=R[sid]
 sol=q.get(':question/worked-solution');lines=[];i=0
 if sol:
  for l in sol.splitlines(keepends=True):
   if re.search(r'\d',l):l=mask(l,sr[i]);i+=1
   lines.append(l)
  assert i==len(sr)
 fields=q.get(':question/answer-fields',[])
 out[sid]={'prompt':mask(q[':question/problem'],pr),'solution':''.join(lines) if sol else None,'answers':[mask(a[':answer/value'],roles) for f in fields for a,roles in zip(f[':answer-field/choices'],A[sid])],'presence':{k:k in q for k in (':question/difficulty',':question/worked-solution',':question/answer-fields')},'correct_present':bool(fields and ':answer-field/correct' in fields[0]),'correct_index':next((i for i,a in enumerate(fields[0][':answer-field/choices'])if a[':answer/id']==fields[0].get(':answer-field/correct',{}).get(':answer/id')),None) if fields else None}
(H/'masks.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
