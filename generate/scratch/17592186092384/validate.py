"""Independent rendered-question checks plus the actual application grader."""
import hashlib, importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('normal_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x',real=True)
def expression(text):
 text=text.replace('\\\\','\\').replace('\\left','').replace('\\right','').replace('\\,','')
 def group(s,i):
  assert s[i]=='{';depth=1;j=i+1
  while depth:
   if s[j]=='{':depth+=1
   if s[j]=='}':depth-=1
   j+=1
  return s[i+1:j-1],j
 def convert(s):
  out='';i=0
  while i<len(s):
   if s.startswith('\\frac',i) or s.startswith('\\dfrac',i):
    i+=len('\\dfrac') if s.startswith('\\dfrac',i) else len('\\frac');a,i=group(s,i);b,i=group(s,i);out+='(('+convert(a)+')/('+convert(b)+'))'
   elif s.startswith('\\sqrt',i):
    a,i=group(s,i+5);out+='sqrt('+convert(a)+')'
   elif s[i]=='{':a,i=group(s,i);out+='('+convert(a)+')'
   elif s[i]=='^':out+='**';i+=1
   else:out+=s[i];i+=1
  return out
 return parse_expr(convert(text),local_dict={'x':x,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
def parsed(q):
 f=expression(re.search(r'\$y\s*=\s*(.*?)\$',q[':question/problem'])[1])
 ptext=re.search(r'at the point \$\((.*?)\)',q[':question/problem'])[1];px,py=ptext.split(',');p=expression(px);y=expression(py)
 assert sp.simplify(f.subs(x,p)-y)==0,'Point not on curve'
 slope=sp.simplify(sp.diff(f,x).subs(x,p));assert slope.is_finite and slope!=0
 return f,p,y,slope,sp.simplify(-1/slope)
def parse_question(q):
 f,p,_,_,_=parsed(q);return g.fingerprint_expr(f,p)
def solution_check(q):
 f,p,y,m,a=parsed(q)
 assert q.get(':question/worked-solution') and len(q.get(':question/answer-fields',[]))==1
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
 assert len(blocks)==3,'Expected derivative, evaluation and reciprocal blocks'
 rhs=[]
 for block in blocks:
  value=block.rsplit('=',1)[1].replace(r'\end{aligned}','').replace(r'\,','').strip().rstrip('.')
  rhs.append(expression(value))
 assert sp.simplify(sp.powdenest(sp.diff(f,x)-rhs[0],force=True))==0,'Wrong displayed derivative'
 assert sp.simplify(m-rhs[1])==0,'Wrong displayed tangent slope'
 assert sp.simplify(a-rhs[2])==0,'Wrong displayed normal slope' 
 field=q[':question/answer-fields'][0];correct=field[':answer-field/correct'];cid=correct[':answer/id'] if isinstance(correct,dict) else correct[1]
 choices=field[':answer-field/choices'];vals=[expression(c[':answer/value']) for c in choices]
 assert len(set(vals))==len(vals)
 assert [c[':answer/id'] for c,v in zip(choices,vals) if sp.simplify(v-a)==0]==[cid]
 assert all(c[':answer/type']==':answer.type/math' or c[':answer/type'][':db/ident']==':answer.type/math' for c in choices)
 return f,p,m,a
def independent(rec):
 f,p,m,a=solution_check(rec['question']);meta=rec['generation'];mid=meta['template'];s=meta['parameters']['scale']
 assert s in range(1,13) and meta['version']==g.VERSION
 assert meta['parameter_fingerprint']==g.fingerprint_expr(f,p)
 # Exact deterministic replay checks all presentation, fields and identities.
 assert rec==g.generate_profile(mid,s,meta['seed'])
 return True
def checks(rec):
 _,_,_,a=solution_check(rec['question']);field=rec['question'][':question/answer-fields'][0]
 if field[':answer-field/type']==':answer-field.type/radio':return [{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'Every complete bank option'} for c in field[':answer-field/choices']]
 return [{'submitted':sp.latex(a),'expected':'accepted','purpose':'Canonical math'}, {'submitted':str(a),'expected':'accepted','purpose':'Equivalent rational notation'}, {'submitted':f'({a.p}*2)/({a.q}*2)','expected':'accepted','purpose':'Equivalent exact expression'}, {'submitted':str(a+1),'expected':'rejected','purpose':'Incorrect offset'}, {'submitted':str(-a),'expected':'rejected','purpose':'Incorrect sign'}]
def main():
 evidence=[];preview=[]
 for mid in g.SPECS:
  original=g.ROWS[mid];r=g.generate_profile(mid,1);independent(r)
  field=original[':question/answer-fields'][0];observed=[expression(c[':answer/value']) for c in field[':answer-field/choices']];generated=[expression(c[':answer/value']) for c in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  assert sorted(map(str,observed))==sorted(map(str,generated))
  assert original[':question/problem']==r['question'][':question/problem'] and original[':question/worked-solution']==r['question'][':question/worked-solution']
  solution_check(original)
  evidence.append({'source':mid,'options_matched':len(observed),'options_total':len(observed),'complete_bank':True,'prompt_and_solution_exact':True,'correct_designation_verified':True,'point_verified':True})
  for s in range(1,13):
   try:r=g.generate_profile(mid,s)
   except ValueError:continue
   independent(r);preview.append(r)
 (HERE/'reference/native-validation-input.json').write_text(json.dumps([{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in preview],indent=2))
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'reference/native-validation-input.json'),str(HERE/'reference/native-validation-report.json')],check=True)
 report=json.loads((HERE/'reference/native-validation-report.json').read_text());assert report['documented_unresolved_checks']==0
 result={'status':'pass','source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'source_replay':evidence,'complete_banks':len(evidence),'matched_options':sum(e['options_matched'] for e in evidence),'generated_validated':len(preview),'distinct_tasks':len({g.fingerprint_expr(*parsed(r['question'])[:2]) for r in preview}),'native_grader':'course_academy_engine::learning::grade_field','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json']}}
 (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
 (HERE/'preview.json').write_text(json.dumps(preview,indent=2)+'\n')
 (HERE/'review.md').write_text('\n\n'.join('## '+r['generation']['template']+' scale '+str(r['generation']['parameters']['scale'])+'\n\n'+r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in preview if r['generation']['parameters']['scale'] in (1,2,12)))
 print(json.dumps(result))
if __name__=='__main__':main()
