"""One-off evidence extraction; complete mathematical spans become named slots."""
import json,re
from pathlib import Path
import sympy as s
D=Path(__file__).parent
qs=json.load(open(D/'source.json'))['record'][':knowledge-point/questions']
x=s.Symbol('x')
def expr(t):
 t=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',t)
 return s.sympify(t)
def vector(t):
 if t.startswith('⟨'):return list(map(expr,t[1:-1].split(','))), 'angle'
 if t.startswith('['):return list(map(expr,t[len('[\\begin{aligned}'):-len('\\end{aligned}]')].split(' \\\\ '))), 'column'
 t=t.replace('-', '+-')
 a=[s.S(0)]*3
 for term in t.split('+'):
  if term:
   idx='ijk'.index(term[-1]);c=term[:-1];a[idx]=expr('1' if c=='' else '-1' if c=='-' else c)
 return a,'basis'
out=[];cases=[]
for q in qs:
 prompt=q[':question/problem'];sol=q[':question/worked-solution']
 m=re.match(r'Let \$([a-z])=(.*?)\$ and \$([a-z])=(.*?)\.\$',prompt)
 assert m,prompt
 n1,v1,n2,v2=m.groups();p,layout=vector(v1);v,layout2=vector(v2);assert layout==layout2
 dot=s.expand(sum(a*b for a,b in zip(p,v)));A=dot.coeff(x);B=dot.subs(x,0);correct=-B/A
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
 assert len(blocks)==2
 rows=blocks[0].split(' \\\\  & =');assert len(rows)==3
 reduced=rows[2][:-1] # terminal period
 const_first=reduced.find('x')>0 and re.match(r'^-?\d+[+-]',reduced) is not None
 # source first unknown term reduction can be constant-first even with positive coefficient.
 if reduced.startswith('-2+2x') or reduced.startswith('-20+2x') or reduced.startswith('-6+2x'):const_first=True
 sr=blocks[1].split(' \\\\ ')
 has_dot=sr[0].startswith(n1+r'\cdot') or sr[0].startswith('p'+r'\cdot')
 intermediate=len(sr)==(4 if has_dot else 3)
 promptmask=prompt[:m.start(2)]+'@V1@'+prompt[m.end(2):m.start(4)]+'@V2@'+prompt[m.end(4):]
 solmask=sol.replace(blocks[0],'@DOTBLOCK@').replace(blocks[1],'@SOLVEBLOCK@')
 # Numeric original row =-2+6+4x has already evaluated products, preserve its sequence.
 evaluated='\\cdot' not in rows[1]
 f=q[':question/answer-fields'][0];vals=[a[':answer/value'] for a in f[':answer-field/choices']]
 cfg={'template':q[':question/math-academy-id'],'source_id':q[':db/id'],'source_uuid':q[':question/id'],'names':[n1,n2],'layout':layout,'parameters':{'p':list(map(str,p)),'q':list(map(str,v))},'prompt_mask':promptmask,'solution_mask':solmask,'formal_row':rows[0],'constant_first':bool(const_first),'intermediate':intermediate,'has_dot':has_dot,'evaluated_products':evaluated,'field_type':f[':answer-field/type'][':db/ident'].split('/')[-1],'field_key':f[':answer-field/key'],'bank_values':vals,'historical_ratios':list(map(lambda t:str(expr(t)/correct),vals)) if correct else None,'original_correct':str(correct),'solution_alias_error':q[':db/id']==17592186292830,'raw_question_keys':list(q)}
 out.append(cfg);cases.append({'source_id':q[':db/id'],'source_math_academy_id':cfg['template'],'template':cfg['template'],'level':'moderate','parameters':cfg['parameters'],'profile':'observed:'+cfg['template']})
(D/'recipes.json').write_text(json.dumps(out,indent=2)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
print(len(out),'extracted')
