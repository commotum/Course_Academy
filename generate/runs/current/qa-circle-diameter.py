"""Root diameter/endpoints readback; full equations and ordered solution stages."""
import sys,re,json,importlib.util,hashlib
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'qa-circle-construction.py','readback');x,y=p.x,p.y;scalar,eq,key=p.scalar,p.eq,p.key
n=dict(records=0,choices=0,distance_rows=0,radius_sides=0,midpoint_coordinates=0,circle_rows=0,prose_inputs=0,pngs=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
def point(text):
 a,b=text.split(',');return scalar(a),scalar(b)
def check(rec):
 q=rec['question'];g=rec['generation'];prompt=q[':question/problem']
 matches=re.findall(r'\$\((-?\d+\s*,\s*-?\d+)\)\$',prompt);assert len(matches)==2,prompt
 A,B=map(point,matches);h,k=((A[i]+B[i])/2 for i in (0,1));D=sum((a-b)**2 for a,b in zip(A,B));r=s.sqrt(D)/2;F=(x-h)**2+(y-k)**2-D/4
 assert A!=B and tuple(g['parameters'][z] for z in ('x1','y1','x2','y2'))==A+B
 f=q[':question/answer-fields'][0];vs=[eq(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vs)==5 and len({key(z) for z in vs})==5
 hits=[i for i,z in enumerate(vs) if key(z)==key(F)];assert len(hits)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][hits[0]][':answer/id']==f[':answer-field/correct'][1]
 else:assert g['evidence_only'] and not g['eligible_for_learning']
 if g['bank_profile'] in ('authored_easy','authored_method'):
  expected=[F,(x-h)**2+(y-k)**2-D,(x-h)**2+(y-k)**2-r,(x-A[0])**2+(y-A[1])**2-D/4,(x-B[0])**2+(y-B[1])**2-D/4] if g['bank_profile']=='authored_easy' else [F,(x+h)**2+(y+k)**2-D/4,(x-h)**2+(y-k)**2-D,(x-A[0])**2+(y-A[1])**2-D/4,(x-2*h)**2+(y-2*k)**2-D/4]
  assert set(map(key,vs))==set(map(key,expected))
 sol=q.get(':question/worked-solution')
 if sol:
  blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==5
  generic=(x-p.p.u)**2+(y-p.p.v)**2-p.p.t**2;assert eq(blocks[0])==s.expand(generic)
  rows=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
  for row in rows:assert s.simplify(scalar(row.split('=')[1])-s.sqrt(D))==0;n['distance_rows']+=1
  radius=blocks[2].split('=');assert radius[0]=='r'
  for side in radius[1:]:assert s.simplify(scalar(side.replace('XY',s.latex(s.sqrt(D))))-r)==0;n['radius_sides']+=1
  middle=blocks[3].split('=');assert len(middle)==3
  for tup in middle[1:]:
   xx,yy=point(tup.strip()[1:-1]);assert xx==h and yy==k;n['midpoint_coordinates']+=2
  rows=blocks[4].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==3 and eq(rows[0])==s.expand(generic)
  for row in rows[1:]:assert key(eq(row))==key(F);n['circle_rows']+=1
  matches=re.findall(r'\$(X|Y)\(([^()]*)\)',sol);assert dict((z,point(v)) for z,v in matches)=={'X':A,'Y':B};n['prose_inputs']+=4
  conclusion=re.search(r'circle has radius \$r=(.*?)\$ and center \$\(a,b\)=\((.*?)\)',sol);assert conclusion and scalar(conclusion[1])==r and point(conclusion[2])==(h,k);n['prose_inputs']+=3
 if not g['dependencies']['plot'].get('reused_original'):
  image=re.findall(r'!\[\]\((.*?)\)',prompt)[0];p.raster(image,h,k,r);n['pngs']+=1
 n['records']+=1;n['choices']+=5
if __name__=='__main__':
 kp=17592186087657;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);check(rec);q=rec['question'];o=olds[c['source_id']]
  for attr in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (attr in q)==(attr in o)
   if attr in o:assert q[attr]==(o[attr][':db/ident'] if attr.endswith('difficulty') else o[attr])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:
   value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert value==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 for item in json.load(open(D/'review.json')):check(item['record'])
 for level in ('easy','moderate','hard'):
  for seed in range(7):check(g.generate(level,seed=630000+seed))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
