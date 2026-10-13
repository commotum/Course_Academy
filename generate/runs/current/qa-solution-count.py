"""Parent classification from complete printed lines plus every actual elimination stage."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186073776
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'qa-elimination-solution.py','countparentparser');x,y=p.letters['x'],p.letters['y'];CATEGORIES=('no solutions','infinitely many solutions','a single solution')
def scalar(raw):return p.scalar(raw)
def equation(raw):return p.equation(raw)
def task(q):
 raw=re.search(r'\$([^$]*)\$',q[':question/problem']);assert raw;parts=raw[1].replace(r'\{','').lstrip('{').split(';');assert len(parts)==2;eqs=list(map(equation,parts));coeffs=[(s.expand(L-R).coeff(x),s.expand(L-R).coeff(y),-s.expand(L-R).subs({x:0,y:0})) for L,R in eqs];A=s.Matrix([row[:2] for row in coeffs]);B=A.row_join(s.Matrix([row[2] for row in coeffs]));answer=CATEGORIES[0] if A.rank()<B.rank() else CATEGORIES[2] if A.rank()==2 else CATEGORIES[1];return coeffs,answer
def raw(g):
 original=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];C=dict(prompts=0,fields=0,values=0,unrated=0,missing_keys=0,missing_solutions=0)
 for case in json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text()):
  old=next(q for q in original if str(case['source_id']) in map(str,(q[':db/id'],q[':question/id'],q[':question/math-academy-id'])));q=g.generate(case.get('level',case.get('authored_level')),template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile')))['question'];assert q[':question/problem']==old[':question/problem'];C['prompts']+=1
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in old)
  C['unrated']+=(':question/difficulty' not in old);C['missing_solutions']+=(':question/worked-solution' not in old);assert len(q[':question/answer-fields'])==len(old[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],old[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);assert all(a[':answer/type']==':answer.type/text' for a in f[':answer-field/choices']);C['fields']+=1;C['values']+=len(f[':answer-field/choices']);C['missing_keys']+=(':answer-field/correct' not in f0)
 return C
def check():
 g=load(ROOT/f'generate/scratch/{K}.py','countgenerator');source=raw(g);rs=json.loads((R/f'qa/{K}-sampled.json').read_text());C=dict(records=0,rearranged_equations=0,annotated_operations=0,transformed_equations=0,ordered_constant_components=0,collected_statements=0,substitution_stages=0,whole_banks=0,choices=0,branches={v:0 for v in CATEGORIES})
 for r in rs:
  q=r['question'];rows,answer=task(q);a,b,c=rows[0];d,e,f=rows[1];row=0 if abs(a)<=abs(d) else 1;m=-[a,d][1-row]/[a,d][row];assert m.q==1;level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':assert abs(m)==1 and max(abs(a),abs(b),abs(d),abs(e))<=5
  else:assert 2<=abs(m)<=4
  sol=q[':question/worked-solution'];bs=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);hard=level=='hard'
  if hard:
   assert re.search(r'(?<!\d)y',q[':question/problem']) and c!=0 and f!=0 and abs(b)==1 and 2<=abs(e)<=4;block=bs.pop(0).replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\');assert len(block)==2
   for z,(A,B,D) in zip(block,rows):assert equation(z)==(A*x+B*y,D);C['rearranged_equations']+=1
  marked=bs.pop(0).replace(r'\{','').split(';');assert len(marked)==2
  for i,z in enumerate(marked):
   if i==row:
    match=re.fullmatch(r'\s*(.*?)\s*\\mid\s*\\mid\s*\\cdot\s*\((-?\d+)\)\s*',z);assert match and s.Integer(match[2])==m;z=match[1];C['annotated_operations']+=1
   A,B,D=rows[i];assert equation(z)==(A*x+B*y,D)
  transformed=[tuple(s.expand(v*m) for v in row0) if i==row else row0 for i,row0 in enumerate(rows)];S=sum(z[1] for z in transformed);T=sum(z[2] for z in transformed);stage=bs.pop(0).replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\');assert len(stage)==(4 if S==0 else 5)
  for z,(A,B,D) in zip(stage[:2],transformed):assert equation(z)==(A*x+B*y,D);C['transformed_equations']+=1
  L,R0=stage[2].split('=',1);assert scalar(L)==S*y;numbers=[scalar(v) for v in re.findall(r'[+-]?\d+',re.sub(r'\s+','',R0))];assert numbers==[z[2] for z in transformed];C['ordered_constant_components']+=2;assert equation(stage[3])==(S*y,T);C['collected_statements']+=1
  if S==0:
   assert not bs and answer==(CATEGORIES[1] if T==0 else CATEGORIES[0]);assert ('*always true*' if T==0 else '*always false*') in sol and '*'+answer+'*' in sol
  else:
   Y=T/S;X=(c-b*Y)/a;assert equation(stage[4])==(y,Y);sub=bs.pop(0).replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\');assert len(sub)==3 and not bs
   assert equation(sub[0])==(a*x+b*Y,c);assert equation(sub[1])==(a*x,c-b*Y);assert equation(sub[2])==(x,X);C['substitution_stages']+=3
   assert answer==CATEGORIES[2];end=re.search(r'\*a single solution\*, \$\((.*?)\)\$',sol);assert end and p.pair('('+end[1]+')')==(X,Y);assert all(s.simplify(A*X+B*Y-D)==0 for A,B,D in rows)
  field=q[':question/answer-fields'][0];assert field[':answer-field/type']==':answer-field.type/select' and field[':answer-field/key']=='field-1';vals=[z[':answer/value'] for z in field[':answer-field/choices']];assert len(vals)==3 and set(vals)==set(CATEGORIES)
  for a0 in field[':answer-field/choices']:assert (a0[':answer/value']==answer)==(a0[':answer/id']==field[':answer-field/correct'][1]);C['choices']+=1
  C['whole_banks']+=1;C['branches'][answer]+=1;C['records']+=1
 assert all(C['branches'].values());out=dict(status='passed',kp_id=K,source=source,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
