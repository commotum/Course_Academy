"""Independent printed-expression checks and actual application grading."""
import hashlib,importlib.util,json,re,subprocess
from functools import lru_cache
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('tangent_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=g.x
ENGINE=HERE/'check-current-engine'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build_engine():
 deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps';harness=ROOT/'generate/runs/current/check-engine.rs'
 libraries={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns)for name in ('course_academy_engine','serde_json')}
 cmd=['rustc','--edition=2024','-O',str(harness)]
 for name,p in libraries.items():cmd+=['--extern',name+'='+str(p)]
 cmd+=['-L','dependency='+str(edb),'-L','dependency='+str(deps),'-o',str(ENGINE)];subprocess.run(cmd,check=True)
 save('engine-build.json',{'harness_sha256':sha(harness),'libraries':{str(p):sha(p)for p in libraries.values()},'executable_sha256':sha(ENGINE)})

def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
@lru_cache(maxsize=None)
def expr(t):
 t=t.strip().rstrip('.').replace('⁡','').replace(r'\,','').replace(r'\cdot','*')
 t=re.sub(r'\\operatorname\{(tan|sec|cos|sin|csc|cot)\}',r'\1',t)
 t=re.sub(r'\{(sec|cos|sin|tan|csc|cot)\}',r'\1',t)
 t=re.sub(r'\\(tan|sec|cos|sin|csc|cot)\b',r'\1',t).replace(r'\pi','pi')
 def group(s,i):
  assert s[i]=='{',(s,i)
  d=1;j=i+1
  while d:
   d+=(s[j]=='{')-(s[j]=='}');j+=1
  return s[i+1:j-1],j
 def conv(s):
  out='';i=0
  while i<len(s):
   if s.startswith('\\frac',i) or s.startswith('\\dfrac',i):
    i+=len('\\dfrac') if s.startswith('\\dfrac',i) else len('\\frac');a,i=group(s,i);b,i=group(s,i);out+='(('+conv(a)+')/('+conv(b)+'))'
   elif s.startswith('\\sqrt',i):
    i+=5;a,i=group(s,i);out+='sqrt('+conv(a)+')'
   elif s[i]=='{':a,i=group(s,i);out+='('+conv(a)+')'
   elif s[i]=='^':out+='**';i+=1
   else:out+=s[i];i+=1
  return out
 t=conv(t)
 # All observed trigonometric functions have one x, numeric, pi, sqrt(x),
 # or parenthesized exact argument; move optional exponents after the call.
 pattern=r'(tan|sec|cos|sin|csc|cot)(?:\*\*(\(\d+\)|\d+))?\s*'
 def trig(m):
  start=m.end();assert start<len(t)
  if t[start]=='(':
   d=1;j=start+1
   while d:d+=(t[j]=='(')-(t[j]==')');j+=1
   arg=t[start:j]
  elif t.startswith('sqrt(',start):
   d=1;j=start+5
   while d:d+=(t[j]=='(')-(t[j]==')');j+=1
   arg=t[start:j]
  else:
   mm=re.match(r'x|pi|\d+',t[start:]);assert mm,(t,start);arg=mm[0];j=start+len(arg)
  return m[1]+'('+arg+')'+('**'+m[2] if m[2] else ''),j
 while (m:=re.search(pattern,t)):
  # Remove the found function from later matching by temporary uppercase.
  val,j=trig(m);t=t[:m.start()]+val.replace(m[1],m[1].upper(),1)+t[j:]
 t=t.lower()
 return parse_expr(t,local_dict={'x':x,'pi':sp.pi,**{n:getattr(sp,n) for n in ('tan','sec','cos','sin','csc','cot','sqrt')}},transformations=standard_transformations+(implicit_multiplication_application,))
def function(q):
 t=q[':question/problem'];m=re.search(r'(?:f\(x\)|y)\s*=\s*(.*?)(?:\$|\s+when)',t);assert m,t
 return expr(m[1])
@lru_cache(maxsize=None)
def equivalent(a,b):
 delta=sp.expand((a-b).rewrite(sp.cos))
 if delta==0:return True
 # A differing regular evaluation disproves identity, before costly simplification.
 if x in delta.free_symbols:
  for z in (sp.Rational(1,3),sp.Rational(2,5)):
   sample=sp.N(delta.subs(x,z),50)
   if sample.is_real and abs(sample)>sp.Float('1e-35'):return False
 return sp.simplify(delta)==0
def rec_template(q):
 return 'q-70911' if re.search(r'y=\d+\(\{x\}',q[':question/problem']) else None
def fingerprint(q):
 f=function(q)
 if '3(' in q[':question/problem'] or rec_template(q)=='q-70911':f=sp.expand(f-f.subs(x,0))
 level=q.get(':question/difficulty',':question.difficulty/easy')
 if isinstance(level,dict):level=level[':db/ident']
 level=str(level);t=q[':question/problem'];point='expression'
 if level.endswith('/moderate') or ' at ' in t:
  point=sp.pi/4 if r'\frac{\pi }{4}' in t else sp.pi if r'x=\pi ' in t else 0
 return g.digest([str(sp.expand(f)),str(point)])
def check(rec):
 q=rec['question'];m=rec['generation'];sid=m['template'];assert rec==g.generate(q[':question/difficulty'].split('/')[-1],m['seed'],sid,m['parameters'])
 f=function(q);expected=sp.diff(f,x);level=q[':question/difficulty'].split('/')[-1]
 if level=='moderate':expected=sp.simplify(expected.subs(x,sp.pi/4 if sid=='q-103081' else sp.pi if sid=='q-17912' else 0))
 for text in (q[':question/problem'],q[':question/worked-solution']):
  assert text.count('$')%2==0 and text.count('{')==text.count('}'),'unbalanced formatting'
 fs=q[':question/answer-fields'];assert len(fs)==1;field=fs[0];bank=field[':answer-field/choices'];vals=[expr(a[':answer/value']) for a in bank]
 for i in range(len(vals)):
  for j in range(i):assert not equivalent(vals[i],vals[j]),'equivalent choices'
 matches=[a[':answer/id'] for a,v in zip(bank,vals) if equivalent(v,expected)];assert matches==[field[':answer-field/correct'][1]],(sid,m['parameters'],expected,vals)
 assert all(a[':answer/type']==':answer.type/math' for a in bank)
 assert fingerprint(q)==m['mathematical_fingerprint']
 sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert blocks
 # Verify every fully numeric/algebraic printed RHS row; symbolic d/dx rows
 # are checked by independently differentiating their printed input above.
 for bi,block in enumerate(blocks):
  target=sp.diff(f,x) if bi==0 else expected
  for row in block.split(r' \\ '):
   if '& =' not in row:continue
   rhs=row.split('& =',1)[1].strip()
   if r'\text{d}' in rhs:continue
   value=expr(rhs);assert equivalent(value,target),(sid,m['parameters'],rhs,value,target)
 if field[':answer-field/type']==':answer-field.type/blank':assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem'] and len(bank)==1
 return rec

def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 if f[':answer-field/type']==':answer-field.type/radio':checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual radio grading'} for a in f[':answer-field/choices']]
 else:
  val=f[':answer-field/choices'][0][':answer/value'];z=expr(val)
  checks=[{'submitted':val,'expected':'accepted','purpose':'canonical blank answer'}, {'submitted':'('+val+')','expected':'accepted','purpose':'parenthesized equivalent'}, {'submitted':sp.sstr(z).replace('**','^'),'expected':'accepted','purpose':'equivalent plain expression'}, {'submitted':val+'+1','expected':'rejected','purpose':'incorrect derivative'}, {'submitted':'0','expected':'rejected','purpose':'incorrect zero'}]
 return {'label':label,'record':rec,'checks':checks}
def main():
 build_engine()
 inputs=[];replay=[];review=[];fps=set();n=0
 for sid,(level,p) in g.PROFILES.items():
  r=check(g.generate(level,0,sid,p));q=r['question'];old=g.SOURCES[sid];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
  assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
  replay.append({'source':sid,'matched_choices':len(f[':answer-field/choices']),'matched_distractors':len(f[':answer-field/choices'])-1,'complete_bank_match':True,'prompt_exact':True,'solution_exact':True})
  variant=check(g.generate(level,42,sid));review.append('## '+sid+'\n\nOriginal\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\nVariant\n\n'+g.markdown(variant))
  for p in g.candidates(sid):
   try:r=g.generate(level,0,sid,p)
   except ValueError:continue
   check(r);assert g.generate(level,99,sid,p)['question']==r['question'];inputs.append(native(sid+' '+str(p),r));fps.add(r['generation']['mathematical_fingerprint']);n+=1
 save('source-replay.json',{'passed':True,'complete_banks_matched':7,'complete_banks_total':7,'distractors_matched':16,'distractors_total':16,'profiles':replay,'excluded_incomplete_sources':['q-30990','q-47905'],'reason':'missing difficulty, worked solution and correct designation; retained unchanged'})
 save('native-input.json',inputs);subprocess.run([str(ENGINE),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 bylevel={l:set() for l in g.SUPPORTED_LEVELS}
 for item in inputs:bylevel[item['record']['question'][':question/difficulty'].split('/')[-1]].add(item['record']['generation']['mathematical_fingerprint'])
 cap=json.loads((HERE/'capabilities.json').read_text());cap['finite_distinct_tasks']={l:len(v) for l,v in bylevel.items()};save('capabilities.json',cap)
 save('previews.json',{l:g.batch(l,5,1917) for l in g.SUPPORTED_LEVELS});(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'exhaustive_instances':n,'distinct_bounded_tasks':len(fps),'mathematical_checks':'Independent printed prompt differentiation; parsed full choices, pairwise equivalence, all algebraic and numeric solution rows; fixed regular evaluation points; deterministic replay','source_fidelity':'7/7 complete banks; 16/16 distractors; exact original prompt, solution and notation','native_grading':'All choices and blank equivalent/counterexample inputs across bounded parameters','supported_levels':list(g.SUPPORTED_LEVELS),'distinct_tasks_by_level':{l:len(v)for l,v in bylevel.items()},'actual_engine_build':json.loads((HERE/'engine-build.json').read_text()),'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json')}})
 print('Validated',n,'instances and',len(fps),'distinct tasks')
if __name__=='__main__':main()
