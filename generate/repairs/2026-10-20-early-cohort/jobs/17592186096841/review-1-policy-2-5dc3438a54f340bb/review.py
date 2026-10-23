import sys,os,json,re,hashlib,importlib.util,platform,subprocess,shutil
from pathlib import Path
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
ROOT=Path('/home/jake/Developer/Course_Academy');E=Path(__file__).resolve().parent;W=E.parent/'workspace'
sys.path.insert(0,str(W))
import generator as g
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
x,t=s.symbols('x t')
def save(name,obj): (E/name).write_text(json.dumps(obj,indent=2,default=str))
def read(name):return json.loads((E/name).read_text())
def parse(v):
 v=v.replace('\\\\','\\').replace('\\left','').replace('\\right','').replace(',','').replace('y=','')
 v=v.replace('{)}',')')
 v=re.sub(r'\^\{([^{}]+)\}',r'^(\1)',v)
 while '\\frac' in v:
  m=re.search(r'\\(?:d?frac)\{([^{}]*)\}\{([^{}]*)\}',v)
  if not m:raise ValueError(v)
  v=v[:m.start()]+'(('+m[1]+')/('+m[2]+'))'+v[m.end():]
 v=re.sub(r'\^\{([^{}]+)\}',r'^(\1)',v).replace('{','').replace('}','')
 return parse_expr(v,local_dict={'x':x,'t':t}, transformations=standard_transformations+(convert_xor,implicit_multiplication_application))
def expected(q):
 p=q[':question/problem']
 if 'f(x)=' in p.replace(' ',''):
  f=re.search(r'f\(x\)\s*=\s*(.*?)\$',p)[1].rstrip('.,');v=x
 else:f=re.search(r'\[([^\]]+)\]',p)[1];v=t
 f=parse(f);d=s.diff(f,v)
 point=re.search(r'point\s*\$\(([-\d]+),([^)]*)\)',p)
 if point:
  z=int(point[1]);y=parse(point[2]);assert s.expand(f.subs(v,z)-y)==0
  return s.expand(d.subs(v,z)*v+y-d.subs(v,z)*z) if 'equation' in p else d.subs(v,z)
 return s.expand(d)
def correct(q):
 f=q[':question/answer-fields'][0];c=f[':answer-field/correct'];cid=c[1] if isinstance(c,list) else c[':answer/id']
 return next(a for a in f[':answer-field/choices'] if a[':answer/id']==cid)
def check_record(r):
 q=r['question'];e=expected(q);f=q[':question/answer-fields'][0];vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 matches=[a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if s.expand(v-e)==0]
 return {'id':q[':question/id'],'template':r['generation']['template'],'expected':str(e),'key_correct':s.expand(parse(correct(q)[':answer/value'])-e)==0,'unique_correct':len(matches)==1,'distinct':len({str(s.expand(v)) for v in vals})==len(vals)}
def make_grading(r,label):
 q=r['question'];f=q[':question/answer-fields'][0];e=expected(q)
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if s.expand(parse(a[':answer/value'])-e)==0 else 'rejected','purpose':'independently differentiated displayed prompt'} for a in f[':answer-field/choices']]
 else:
  checks=[{'submitted':v,'expected':out,'purpose':purpose} for v,out,purpose in [(correct(q)[':answer/value'],'accepted','displayed factored form'),(s.sstr(s.expand(e)).replace('**','^'),'accepted','expanded polynomial'),(s.sstr(s.factor(e)).replace('**','^'),'accepted','alternative factored expression'),(s.sstr(s.expand(e+1)).replace('**','^'),'rejected','off-by-one polynomial'),('0','accepted' if e==0 else 'rejected','zero response')]]
 return {'label':label,'record':r,'checks':checks}
def main():
 save('package-before.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in W.iterdir() if p.is_file()})
 records=[]
 for name,info in g.TEMPLATES.items():
  for seed in range(82901,82913):records.append(g.generate(info[0],seed,template=name))
 save('samples-independent.json',records)
 save('samples-easy.json',[r for r in records if r['question'][':question/difficulty'].endswith('/easy')])
 batch=json.loads((E.parent/'samples.json').read_text());save('batch.json',batch)
 source=json.loads((E.parent/'source/source.json').read_text());sq={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']}
 cases=list(g.SOURCE_CASES)+[('q-132770','quadratic_derivative',dict(a=1,b=3,n=2),None),('q-132994','quadratic_derivative',dict(a=1,b=1,n=3),None)]
 replay=[];results=[]
 for sid,name,p,prof in cases:
  r=g.generate(g.TEMPLATES[name][0],551,template=name,parameters=p,profile=prof);replay.append(r)
  orig=sq[sid];f=orig[':question/answer-fields'][0]
  original_values=[str(s.expand(parse(a[':answer/value']))) for a in f[':answer-field/choices']]
  generated_values=[str(s.expand(parse(a[':answer/value']))) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  results.append({'source_id':orig[':question/id'],'source_ma':sid,'record_id':r['question'][':question/id'],'bank_equal':sorted(original_values)==sorted(generated_values),'original_values':original_values,'generated_values':generated_values,'note':'q-340690 removes incorrect historical blank alternative; q-48625 inferred missing solution and correct link; quadratic solution corrects h/F notation.'})
 save('source-replays.json',replay);save('source-replay-results.json',results)
 # Relevant: hold all except coefficient / exponent / evaluation point fixed. Irrelevant: reorder affine inner terms.
 specs=[('base','easy','affine_blank',dict(a=2,b=3,n=3)),('coefficient','easy','affine_blank',dict(a=-2,b=3,n=3)),('power','easy','affine_blank',dict(a=2,b=3,n=4)),('point0','moderate','affine_slope',dict(a=2,b=1,n=4,z=0)),('point1','moderate','affine_slope',dict(a=2,b=1,n=4,z=1)),('tangent0','hard','tangent_blank',dict(a=2,b=1,n=4,z=0)),('tangent1','hard','tangent_blank',dict(a=2,b=1,n=4,z=1)),('order1','easy','affine_constant_radio',dict(a=2,b=3,n=3)),('order2','easy','affine_variable_radio',dict(a=2,b=3,n=3))]
 pairs=[g.generate(l,4401,template=n,parameters=p) for _,l,n,p in specs];save('counterfactual-records.json',pairs)
 checks=[check_record(r) for r in records+batch+replay+pairs];save('math-results.json',checks)
 native=[make_grading(r,'record-'+str(i)) for i,r in enumerate(batch+replay+pairs+[next(r for r in records if r['generation']['template']==n) for n in g.TEMPLATES])]
 # Old response must fail after relevant change; order-only keeps same mathematical response.
 for ia,ib in [(0,1),(0,2),(3,4),(5,6)]:
  native.append({'label':'counterfactual-cross-'+str(ia)+'-'+str(ib),'record':pairs[ib],'checks':[{'submitted':str(expected(pairs[ia]['question'])).replace('**','^'),'expected':'rejected','purpose':'old answer is stale after relevant change'}]})
 save('grader-input.json',native)
 render=batch+pairs+[next(r for r in records if r['generation']['template']==n) for n in g.TEMPLATES if not n.startswith('affine_')]
 save('render-records.json',render)
 save('scope-results.json',{'templates':{n:{'difficulty':v[0],'type':v[1],'source':v[2],'family':v[3]} for n,v in g.TEMPLATES.items()},'sample_count':len(records),'observations':'Powers of polynomial only; requested easy samples have affine inner polynomial. Higher families retain source slope/tangent operations. Canonical e-181 inner 3*x^4+x^3 cannot be generated: quartic always a*x^4+b*x.'})
 save('runtime.json',{'python':platform.python_version(),'sympy':s.__version__,'mpmath':__import__('mpmath').__version__})
 print('sample count',len(records),'math failures',[c for c in checks if not all(c[k] for k in ('key_correct','unique_correct','distinct'))]);print('source bank exceptions',[(r['source_ma'],r['bank_equal']) for r in results if not r['bank_equal']])
 (E/'session-state.md').write_text('Independent source analysis complete. Package read only. 120 fresh stratified samples, exact batch, 12 source replay cases, 9 controlled records saved. Prompt-derived SymPy checks completed. Native grading/render/delivery next.\n')
if __name__=='__main__':main()
