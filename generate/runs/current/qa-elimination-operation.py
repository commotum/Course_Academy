"""Parent: actual system, complete paired selection, distributed rows and ordered addition."""
import importlib.util,json,re,hashlib,sys,copy
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
letters={c:s.Symbol(c,real=True) for c in 'xystabuvwz'}
def scalar(raw):
 raw=raw.replace('&','').strip().replace(r'\{','').lstrip('{');assert re.fullmatch(r'[xystabuvwz0-9()\s+*/.\-]+',raw),raw;return s.expand(parse_expr(raw,local_dict=letters,transformations=standard_transformations+(implicit_multiplication_application,)))
def equation(raw):a,b=raw.split('=',1);return scalar(a),scalar(b)
def displayed(q):
 text=q[':question/problem'];body=re.search(r'\n\$(.*?)\$\n',text);assert body;textvar=re.search(r'eliminate the variable \$([xystabuvwz])\$',text);assert textvar;var=letters[textvar[1]];rows=[equation(r) for r in body[1].replace(r'\{','').lstrip('{').split('; ')];assert len(rows)==2;symbols=set().union(*(a.free_symbols for a,b in rows));assert len(symbols)==2 and var in symbols;other=next(v for v in symbols if v!=var);return rows,var,other
def raw(g,k):
 qs=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];C=dict(prompts=0,fields=0,values=0,unrated=0,missing_keys=0,missing_solutions=0)
 for c in json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text()):
  old=next(q for q in qs if str(c['source_id']) in map(str,(q[':db/id'],q[':question/id'],q[':question/math-academy-id'])));q=g.generate(c.get('level','easy'),template=c.get('template'),parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile')))['question'];assert q[':question/problem']==old[':question/problem'];C['prompts']+=1
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in old)
  C['unrated']+=(':question/difficulty' not in old);C['missing_solutions']+=(':question/worked-solution' not in old);assert len(q[':question/answer-fields'])==len(old[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],old[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);assert all(isinstance(a[':answer/type'],str) for a in f[':answer-field/choices']);C['fields']+=1;C['values']+=len(f[':answer-field/choices']);C['missing_keys']+=(':answer-field/correct' not in f0)
 return C
def check(k):
 g=load(ROOT/f'generate/scratch/{k}.py','eliminationoperation'+str(k));src=raw(g,k);rs=json.loads((R/f'qa/{k}-sampled.json').read_text());C=dict(records=0,paired_combinations=0,selected_operations=0,scaled_equations=0,distributed_equation_rows=0,ordered_addition_components=0,collected_equations=0,solution_set_checks=0)
 for r in rs:
  q=r['question'];rows,var,other=displayed(q);fields={f[':answer-field/key']:f for f in q[':question/answer-fields']};rowvalues=[a[':answer/value'] for a in fields['field-1'][':answer-field/choices']];assert set(rowvalues)=={'first','second'};multipliers=[s.Rational(a[':answer/value']) for a in fields['field-2'][':answer-field/choices']];assert len(multipliers)==4 and len(set(multipliers))==4;coeff=[a.coeff(var) for a,b in rows];valid=[(i,m) for i,name in enumerate(('first','second')) for m in multipliers if m*coeff[i]+coeff[1-i]==0];assert len(valid)==1;row,m=valid[0];C['paired_combinations']+=8;C['selected_operations']+=1
  for key,want in (('field-1',('first','second')[row]),('field-2',str(m))):assert next(a[':answer/value'] for a in fields[key][':answer-field/choices'] if a[':answer/id']==fields[key][':answer-field/correct'][1])==want
  n=rows[1-row][0].coeff(other)
  if k==17592186192654:assert set(multipliers)=={m,-m,n,-n}
  else:
   ratio0=abs(m);n0=ratio0-1 if r['generation']['profile']=='difference' else abs(coeff[1-row]);assert set(multipliers)=={m,-m,n0,-n0}
  level=q[':question/difficulty'].split('/')[-1];small=min(map(abs,coeff));big=max(map(abs,coeff));assert (small==1 if level=='easy' else 2<=small<=4);ratio=big/small;assert ratio.is_Integer and (2<=ratio<=7 if level=='easy' else 2<=ratio<=4 if level=='moderate' else 5<=ratio<=7)
  sol=q[':question/worked-solution'];bs=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(bs)==2;scaled=[(s.expand(a*m),s.expand(b*m)) if i==row else (a,b) for i,(a,b) in enumerate(rows)];body=bs[0].replace(r'\{','').split('; ');assert len(body)==2
  for i,bodyrow in enumerate(body):
   if i==row:
    z=re.fullmatch(r'\((.*?)\)\\cdot \((-?\d+)\)',bodyrow);assert z and s.Rational(z[2])==m and equation(z[1])==rows[i];C['scaled_equations']+=1
   else:assert equation(bodyrow)==rows[i]
  stages=bs[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\');assert len(stages)==4
  for stage,want in zip(stages[:2],scaled):assert equation(stage)==want;C['distributed_equation_rows']+=1
  left,right=stages[2].split('=',1);left=re.sub(r'\s+','',left.replace('&',''));right=re.sub(r'\s+','',right);assert left.startswith('(') and left.endswith(')') and right.startswith('(') and right.endswith(')');a,b=(s.expand(v[0]).coeff(other) for v in scaled);expected_coeff=[a,b]
  parts=re.findall(r'([+-]?\d*)'+str(other),left);assert len(parts)==2;got=[s.Integer(1 if v in ('','+') else -1 if v=='-' else v) for v in parts];assert got==expected_coeff,(left,got,expected_coeff);nums=list(map(s.Integer,re.findall(r'[+-]?\d+',right)));assert nums==[v[1] for v in scaled];C['ordered_addition_components']+=4
  collected=(s.expand(sum(v[0] for v in scaled)),s.expand(sum(v[1] for v in scaled)));assert equation(stages[3])==collected and collected[0].coeff(var)==0 and collected[0].coeff(other)!=0;C['collected_equations']+=1
  initial=s.solve([a-b for a,b in rows],(var,other));transformed=s.solve([a-b for a,b in scaled],(var,other));assert initial==transformed and s.simplify((collected[0]-collected[1]).subs(initial))==0;C['solution_set_checks']+=1
  assert re.search(r'first equation is \$'+str(coeff[0])+r'\$',sol) and re.search(r'second equation it is \$'+str(coeff[1])+r'\$',sol);assert not re.search(r'back.substitut|solution to the system',sol,re.I);C['records']+=1
 out=dict(status='passed',kp_id=k,source=src,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
