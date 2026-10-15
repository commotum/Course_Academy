"""Independent exact polynomial integration and rendered-value/engine checks."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,t=g.x,g.y,g.t

def parse(value):
 value=value.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace('⁡','').replace(r'\operatorname{ln}3','log(3)')
 value=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',value)
 value=re.sub(r'\\log\{\(\s*(\d+)\s*\)\}',r'log(\1)',value)
 while r'\frac' in value:
  previous=value;value=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',value)
  assert previous!=value,value
 value=value.replace('{','(').replace('}',')')
 return parse_expr(value,local_dict={'x':x,'y':y,'t':t,'e':s.E,'E':s.E,'log':s.log,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def direct_integral(p,q,curve):
 a,b,lo,hi=map(s.sympify,curve)
 integrand=s.expand(p.subs({x:a,y:b},simultaneous=True)*s.diff(a,t)+q.subs({x:a,y:b},simultaneous=True)*s.diff(b,t))
 # Independent power-rule summation, including the source's half powers.
 result=0
 for term in s.Add.make_args(integrand):
  coefficient,degree=term.as_coeff_exponent(t)
  assert not coefficient.has(t) and degree!=-1
  result+=coefficient*(hi**(degree+1)-lo**(degree+1))/(degree+1)
 return s.simplify(result)

def independent(r):
 meta=r['generation'];template=meta['template'];scale=meta['parameters']['scale'];d=g.DATA[template];p,q=scale*s.sympify(d[0]),scale*s.sympify(d[1]);known=d[4]
 i1=direct_integral(p,q,d[2]);i2=direct_integral(p,q,d[3]);total=s.simplify(i1+i2)
 assert total==scale*s.sympify(d[6]),template
 question=r['question'];prompt=question[':question/problem'];solution=question[':question/worked-solution']
 assert question[':question/difficulty']==':question.difficulty/'+d[-1]
 assert g.KP_ID==r['knowledge_point']['db_id']
 # Independently read the supplied integral and whole rendered vector field.
 given=re.search(r'Given that .*?=(.*?),?\$',prompt)[1]
 assert s.simplify(parse(given)-(i1 if known==1 else i2))==0,(template,given)
 field=prompt.split('F(x,y)=')[1].split('$')[0].rstrip(',')
 parts=field.split(r'\,i');assert len(parts)==2
 pp=parse(parts[0]);qq=parse(parts[1][1:-len(r'\,j')]) if parts[1] else s.Integer(0)
 assert s.simplify(pp-p)==s.simplify(qq-q)==0,(template,field)
 f=question[':question/answer-fields'][0];assert len(question[':question/answer-fields'])==1
 assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 choices=f[':answer-field/choices'];assert len(choices)==5
 values=[parse(a[':answer/value']) for a in choices]
 expected=[scale*s.sympify(v) for v in d[5]]
 assert all(sum(s.simplify(a-b)==0 for b in values)==1 for a in expected)
 assert all(sum(s.simplify(a-b)==0 for b in values)==1 for a in values)
 correct=next(a for a in choices if a[':answer/id']==f[':answer-field/correct'][1]);assert s.simplify(parse(correct[':answer/value'])-total)==0
 assert all('$' not in a[':answer/value'] for a in choices)
 for z in (prompt,solution):assert z.count('$')%2==0 and z.count('{')==z.count('}')
 if scale!=1:
  j=3-known;a,b,lo,hi=map(s.sympify,d[3] if known==1 else d[2]);u=p.subs({x:a,y:b},simultaneous=True);v=q.subs({x:a,y:b},simultaneous=True);dot=s.expand(u*s.diff(a,t)+v*s.diff(b,t))
  rendered=re.search(r'\$\$F\(r_\d\(t\)\)=\((.*?)\)\\,i\+\((.*?)\)\\,j\.\$\$',solution)
  assert rendered and s.simplify(parse(rendered[1])-u)==s.simplify(parse(rendered[2])-v)==0
  derivative=re.search(r"\$\$r_\d'\(t\)=\((.*?)\)\\,i\+\((.*?)\)\\,j\.\$\$",solution)
  assert derivative and s.simplify(parse(derivative[1])-s.diff(a,t))==s.simplify(parse(derivative[2])-s.diff(b,t))==0
  line=solution.split('We can now compute the dot product:')[1].split('Finally')[0]
  assert s.simplify(parse(line.rsplit('=',1)[1].split('.$$')[0])-dot)==0
  final=solution.rsplit('=',1)[1].split('.$$')[0];assert s.simplify(parse(final)-total)==0
  if template=='q-77250':lo,hi=hi,lo;assert 'same path travelled from $B$ to $A$' in solution and r'\int_{-C_2}' in solution
  assert f'with $t$ running from ${g.tex(lo)}$ to ${g.tex(hi)}$' in solution
  assert f'r_{j}(t)=({g.tex(a)})\\,i+({g.tex(b)})\\,j' in solution
 return total

def checks(r):
 independent(r);f=r['question'][':question/answer-fields'][0]
 return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each source-profile radio option'} for a in f[':answer-field/choices']]

def main():
 records=[];replay=[];mapping=[]
 for template,src in g.SOURCES.items():
  level=g.DATA[template][-1];r=g.generate(level,template=template,parameters={'scale':1});independent(r)
  assert r['question'][':question/problem']==src[':question/problem'] and r['question'][':question/worked-solution']==src[':question/worked-solution']
  sf=src[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0]
  assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
  assert sf[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  replay.append({'source':template,'complete_bank':'5/5','distractors':'4/4','correct_designation':True,'exact_prompt_and_solution':True})
  for a in sf[':answer-field/choices']:
   expr=parse(a[':answer/value']);mapping.append({'source':template,'field':'selection','profile':'observed-scaled:'+template,'source_answer':a[':answer/id'],'original':a[':answer/value'],'base_expression':str(expr),'recipe':'scale * ('+str(expr)+')','complete_value_replay':True,'interpretation':'observed expression; error mechanism unresolved' if a[':answer/id']!=sf[':answer-field/correct'][':answer/id'] else 'exact integral sum'})
  records.append(r)
  for scale in g.SCALES:
   r=g.generate(level,template=template,parameters={'scale':scale});independent(r);records.append(r)
 assert len({r['generation']['mathematical_signature'] for r in records})==160
 for level in g.SUPPORTED_LEVELS:
  seen={g.generate(level,seed)['generation']['template'] for seed in range(150)}
  assert seen=={k for k,d in g.DATA.items() if d[-1]==level}
 # Hold every geometric datum constant and change scale: rendered key and field
 # must both change. Deliberately mutate a key and given value to test detection.
 r=g.generate('hard',template='q-77244',parameters={'scale':2});r2=g.generate('hard',template='q-77244',parameters={'scale':3});independent(r2)
 assert independent(r)!=independent(r2)
 bad=copy.deepcopy(r2);f=bad['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
 for broken in [bad,{**r2,'question':{**r2['question'],':question/problem':r['question'][':question/problem']}}]:
  try:independent(broken)
  except AssertionError:pass
  else:raise AssertionError('stale rendered key/value survived')
 input_data=[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records]
 (HERE/'engine-input.json').write_text(json.dumps(input_data));subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 report={'status':'pass','source_basis':g.SNAPSHOT['basis'],'source_replays':replay,'source_distractors':'40/40','source_complete_banks':'10/10','exact_independent_records':160,'native':json.loads((HERE/'engine-report.json').read_text()),'slot_coverage':{'scale':list(g.SCALES),'families':list(g.DATA),'fixed_paths_and_requested_integral':True},'stale_value_mutations_rejected':2,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2));(HERE/'source-choice-mapping.json').write_text(json.dumps(mapping,indent=2))
 review=[g.generate(level,template=template,parameters={'scale':scale}) for level,template in [('moderate','q-39342'),('moderate','q-77182'),('hard','q-77244'),('hard','q-77258')] for scale in [1,-2,3]]
 (HERE/'review.json').write_text(json.dumps(review,indent=2));(HERE/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in review))
 print(json.dumps({k:v for k,v in report.items() if k!='native'},indent=2))
if __name__=='__main__':main()
