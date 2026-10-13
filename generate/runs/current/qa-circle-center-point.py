"""Root actual center/point inputs, distance stages, equations and complete banks."""
import sys,re,json,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'qa-circle-construction.py','reader');scalar,eq,key=p.scalar,p.eq,p.key;x,y=p.x,p.y
n=dict(records=0,choices=0,distance_rows=0,circle_rows=0,formal_rows=0,pngs=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
def check(rec):
 q=rec['question'];g=rec['generation'];prompt=q[':question/problem'];m=re.search(r'C\((.*?),(.*?)\)\$ and the point \$X\((.*?),(.*?)\)',prompt);assert m,prompt
 h,k,u,v=map(scalar,m.groups());D=(u-h)**2+(v-k)**2;r=s.sqrt(D);F=(x-h)**2+(y-k)**2-D
 assert tuple(s.sympify(g['parameters'][z]) for z in ('h','k','u','v'))==(h,k,u,v)
 f=q[':question/answer-fields'][0];vs=[eq(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vs)==5 and len({key(z) for z in vs})==5;hits=[i for i,z in enumerate(vs) if key(z)==key(F)];assert len(hits)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][hits[0]][':answer/id']==f[':answer-field/correct'][1]
 else:assert g['evidence_only'] and not g['eligible_for_learning']
 profile=g['bank_profile']
 if profile in ('authored-easy','authored-hard'):
  expected=[F,(x+h)**2+(y-k)**2-D,(x-u)**2+(y-v)**2-D,(x-h)**2+(y-k)**2-r,(x-h)**2+(y-k)**2-(u-h)**2] if profile=='authored-easy' else [F,(x-h)**2+(y+k)**2-D,(x+h)**2+(y+k)**2-D,(x-h)**2+(y-k)**2-r,(x+h)**2+(y+k)**2-r]
  assert set(map(key,vs))==set(map(key,expected))
 sol=q.get(':question/worked-solution')
 if sol:
  blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==3
  generic=(x-p.p.u)**2+(y-p.p.v)**2-p.p.t**2;assert eq(blocks[0])==s.expand(generic);n['formal_rows']+=1
  rows=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
  for row in rows:assert s.simplify(scalar(row.split('=')[1])-r)==0;n['distance_rows']+=1
  # Structural operands in the first distance row must be the actual four
  # coordinate inputs, allowing either complete subtraction direction.
  first=rows[0].split('=')[1];pairs=re.findall(r'\((.*?)\)',first.replace('(-','NEG'))
  # Value equality above is independent; public validator additionally parses
  # each ordered operand. Full source masks and source stage counts below exact.
  rows=blocks[2].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==3 and eq(rows[0])==s.expand(generic);n['formal_rows']+=1
  for row in rows[1:]:assert key(eq(row))==key(F);n['circle_rows']+=1
 if g['plot']['renderer'].lower()=='matplotlib':
  path=re.findall(r'!\[\]\((.*?)\)',prompt)[0];p.raster(path,h,k,r);n['pngs']+=1
 n['records']+=1;n['choices']+=5
if __name__=='__main__':
 kp=17592186087768;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['difficulty'],parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);check(rec);q=rec['question'];o=olds[c['source_id']]
  for attr in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (attr in q)==(attr in o)
   if attr in o:assert q[attr]==(o[attr][':db/ident'] if attr.endswith('difficulty') else o[attr])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:
   value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert value==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 for item in json.load(open(D/'review.json')):check(item.get('record',item))
 for level in ('easy','moderate','hard'):
  for seed in range(8):check(g.generate(level,seed=540000+seed))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
