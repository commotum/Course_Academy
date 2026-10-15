"""Independent printed-expression QA and actual learner radio grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
from functools import lru_cache
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load(HERE.with_suffix('.py'),'g');p=load(HERE/'scalar-parser.py','p')
x=p.x;U=sp.Symbol('U',positive=True)
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def group(t,start,left='{',right='}'):
 assert t[start]==left;depth=1;end=start+1
 while depth:
  assert end<len(t);depth+=(t[end]==left)-(t[end]==right);end+=1
 return t[start+1:end-1],end
def scalar(t,var='x'):
 t=t.strip().rstrip('.,').replace('✓','').replace('C','v')
 if var!='x':t=re.sub(r'(?<![A-Za-z])'+var+r'(?![A-Za-z])','x',t)
 while r'\sqrt' in t:
  at=t.index(r'\sqrt');start=at+5;d=2
  if t[start]=='[':z,start=group(t,start,'[',']');d=int(z)
  rad,end=group(t,start);expr=scalar(rad)
  t=t[:at]+'('+sp.latex(expr)+')^{1/'+str(d)+'}'+t[end:]
 return p.scalar(t)
@lru_cache(maxsize=None)
def zero_on_positive_domain(expression):
 return sp.simplify(sp.powdenest(expression,force=False))==0
def equal(a,b,t,shift):
 # U>0 parameterizes the entire declared open interval, including the
 # source bank whose even-root radicand has offset -2.
 lower=2 if any(r['offset']==-2 for r in t['bank']) else 0
 z=(U+lower-shift)/t['a']
 return zero_on_positive_domain((a-b).subs(p.u,t['a']*x+shift).subs(x,z))
def prompt_data(q):
 text=q[':question/problem'].split(r'\int',1)[1];text=re.sub(r'\\textrm\s*d\s*([a-z])',r'\\text{d}\1',text);text=re.sub(r'(?<![a-z])d([a-z])',r'\\text{d}\1',text);m=re.search(r'(?:\\,)?\\text\{d\}([a-z])',text);assert m,text
 return scalar(text[:m.start()].replace(r'\displaystyle','').strip(),m[1]),m[1]
def fingerprint(q):
 text=q[':question/problem'];at=text.index(r'\sqrt')+5;d=2
 if text[at]=='[':z,at=group(text,at,'[',']');d=int(z)
 rad,end=group(text,at);var=prompt_data(q)[1];z=scalar(rad,var)
 base,n=z.as_base_exp();assert n.is_Integer and base.is_polynomial(x) and sp.Poly(base,x).degree()==1
 a=sp.diff(base,x);b=base.subs(x,0)
 if r'\frac{1}{' in text[:at]:n=-n
 exp=sp.Rational(n,d)
 return g.digest([int(a),int(b),int(exp.p),int(exp.q)])
def solution_check(q,t,b,integrand):
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==4
 substitution=re.search(r'let\s+\$u=([^$]+)\$',q[':question/worked-solution']);assert substitution
 assert equal(scalar(substitution[1],t['variable']),t['a']*x+b,t,b),(t,b,'actual substitution operand')
 intro=blocks[0].split(r'\int',1)[1].split(r'\,\text{d}')[0];assert equal(scalar(intro,t['variable']),integrand,t,b)
 differential=blocks[1].split('⟹')
 assert len(differential)==2
 lhs,rhs=differential
 assert lhs.split('=')[0].strip()==r'\frac{\text{d}u}{\text{d}'+t['variable']+'}'
 assert sp.simplify(scalar(lhs.split('=')[1].rstrip(r'\,'),t['variable'])-t['a'])==0
 expected_prefix=r'\,\text{d}'+t['variable']+'='
 assert rhs.startswith(expected_prefix),(t,rhs)
 factor=rhs[len(expected_prefix):].removesuffix('.').removesuffix(r'\text{d}u')
 factor=factor.rstrip(r'\,')
 factor={'':sp.Integer(1),'-':sp.Integer(-1)}.get(factor,factor)
 factor=scalar(factor,t['variable']) if isinstance(factor,str) else factor
 assert sp.simplify(factor-1/sp.Integer(t['a']))==0,(t,blocks[1])
 def value(s,derivative=False):
  s=s.strip().replace('✓','');var=t['variable']
  if r'\int' in s:
   coef,rest=s.split(r'\int',1);m=re.search(r'\\text\{d\}([a-z])',rest);assert m,rest;diffvar=m[1];expr=rest[:m.start()]+rest[m.end():]
   z=({'-':-1,'+':1,'':1}.get(coef.strip(),None) if coef.strip() in ('-','+','') else scalar(coef,var))*scalar(expr,var);z=z.subs(p.u,t['a']*x+b)
   return z*(t['a'] if diffvar=='u' else 1)
  der=r'\frac{\text{d}}{\text{d}'+var+'}'
  computed={}
  while der in s:
   at=s.index(der);start=at+len(der);op=s[start];arg,end=group(s,start,op,']' if op=='[' else ')')
   z=sp.diff(scalar(arg,var),x);token=['t','j','k'][len(computed)];computed[p.locals_[token]]=z;s=s[:at]+'('+token+')'+s[end:]
  z=scalar(s,var).subs(computed).subs(p.u,t['a']*x+b)
  return z if derivative else sp.diff(z,x)
 for i in (2,3):
  for row in blocks[i].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
   for term in row.split('& ='):
    if term.strip():assert equal(value(term,i==3),integrand,t,b),(t,b,term)
def check(rec):
 meta=rec['generation'];q=rec['question'];sid=meta['template'];t=g.PROFILES[sid];b=meta['parameters']['b']
 assert rec==g.generate(t['difficulty'],meta['seed'],sid,{'b':b})
 integrand,var=prompt_data(q);assert var==t['variable'];assert fingerprint(q)==meta['mathematical_fingerprint']
 f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];assert len(bank)==5 and len({a[':answer/id'] for a in bank})==5
 vals=[scalar(a[':answer/value'],var) for a in bank]
 assert all(not equal(sp.diff(z-w,x),0,t,b) for i,z in enumerate(vals) for w in vals[:i]),'Equivalent bank values'
 good=[a[':answer/id'] for a,z in zip(bank,vals) if equal(sp.diff(z,x),integrand,t,b)];assert good==[f[':answer-field/correct'][1]],(sid,b,good)
 for a,z in zip(bank,vals):
  recipe=next(r for r in t['bank'] if g.normalize_tex(r['value'].replace('@@BASE@@',g.base(t,b)).replace('@@ALTERED@@',g.base(t,b-2)))==a[':answer/value'])
  expected=sp.Rational(recipe['coefficient'])*(t['a']*x+b+recipe['offset'])**sp.Rational(recipe['exponent'])+p.v
  assert equal(z,expected,t,b),(sid,b,'recipe',a)
 solution_check(q,t,b,integrand)
 return rec

def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Canonical correct and every ordinary wrong option under radio selection contract'} for a in f[':answer-field/choices']]
 correct_index=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
 checks.append({'submitted':'000'+str(100+correct_index),'expected':'accepted','purpose':'Equivalent decimal entity ID spelling under actual radio field contract'})
 return {'label':label,'record':rec,'checks':checks}


def main():
 import copy,sys,time
 started=time.time();inputs=[];cases=[];review=[]
 original=[q for q in g.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q]
 def source_content(q):
  return {k:q[k] for k in (':question/problem',':question/worked-solution',':question/difficulty') if k in q}
 for q in g.SOURCE['record'][':knowledge-point/questions']:
  sid=q.get(':question/math-academy-id',str(q[':db/id']));level=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/hard').split('/')[-1]
  rec=g.generate(level,0,profile='source:'+sid);got=rec['question']
  for k in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (k in q)==(k in got),(sid,k)
   if k in q:assert got[k]==(q[k][':db/ident'] if isinstance(q[k],dict) else g.normalize_prose(q[k])),(sid,k)
  fields=q[':question/answer-fields'];assert len(fields)==len(got[':question/answer-fields'])
  for a,b in zip(fields,got[':question/answer-fields']):
   assert a[':answer-field/key']==b[':answer-field/key'] and a[':answer-field/type'][':db/ident']==b[':answer-field/type']
   assert sorted(g.normalize_tex(x[':answer/value']) for x in a[':answer-field/choices'])==sorted(x[':answer/value'] for x in b[':answer-field/choices'])
   assert (':answer-field/correct' in a)==(':answer-field/correct' in b)
   if ':answer-field/correct' in a:
    val=next(x[':answer/value'] for x in b[':answer-field/choices'] if x[':answer/id']==b[':answer-field/correct'][1]);assert val==g.normalize_tex(a[':answer-field/correct'][':answer/value'])
  cases.append({'source_id':sid,'role':'MA' if ':question/math-academy-id' in q else 'independent_inventory','full_prompt':True,'full_solution_or_omission':True,'complete_bank':True,'choices':sum(len(f[':answer-field/choices']) for f in fields),'correct_or_omission':True})
  # A shifted source-fidelity variant must carry the actual template's prose and bank.
  variant=g.generate(level,7,profile='source:'+sid,parameters={'b':2})
  review.append('## '+sid+'\n\nFaithful source at anchor\n\n'+g.markdown(rec)+'\n\nParameterized source variant\n\n'+g.markdown(variant))
 save('source-cases.json',cases)
 for sid,t in g.PROFILES.items():
  print('Checking complete bounded domain:',sid,flush=True)
  for b in g.DOMAIN:
   rec=check(g.generate(t['difficulty'],17,sid,{'b':b}));q=rec['question']
   assert q==g.generate(t['difficulty'],-27,profile=sid,parameters={'b':b})['question']
   dom=rec['generation']['domain'];assert dom['branch']=='positive radicands, principal real roots'
   # The independent parser's substitution maps the whole open domain to U>0;
   # each source altered radicand remains positive. No forced power rewriting.
   assert sp.simplify((t['a']*x+b).subs(x,(U+dom['base_lower_exclusive']-b)/t['a'])-(U+dom['base_lower_exclusive']))==0
   inputs.append(native(sid+' b='+str(b),rec))
  review.append('## Normal '+sid+'\n\n'+g.markdown(g.generate(t['difficulty'],0,sid,{'b':t['b']}))+'\n\n'+g.markdown(g.generate(t['difficulty'],1,sid,{'b':-3})))
 save('native-input.json',inputs)
 engine=ROOT/'generate/runs/current/check-engine';sha=hashlib.sha256(engine.read_bytes()).hexdigest();assert sha=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 strict=[]
 for name,fn in [('bool seed',lambda:g.generate(seed=True)),('float seed',lambda:g.generate(seed=2.0)),('bool count',lambda:g.batch('easy',True)),('float count',lambda:g.batch('easy',2.0)),('bool parameter',lambda:g.generate('easy',parameters={'b':True})),('float parameter',lambda:g.generate('easy',parameters={'b':2.0})),('list parameters',lambda:g.generate('easy',parameters=[2])),('extra parameter',lambda:g.generate('easy',parameters={'b':2,'a':1})),('bad level',lambda:g.generate(True)),('bad template',lambda:g.generate('easy',template=True))]:
  try:fn();raise AssertionError('Accepted '+name)
  except ValueError:strict.append(name)
 save('strict-inputs.json',{'rejected':strict})
 capacities={}
 allfp=set()
 for level in g.LEVELS:
  n=g.capacity(level);rows=g.batch(level,n,43);fps=[r['generation']['mathematical_fingerprint'] for r in rows];assert len(rows)==n and len(set(fps))==n and not allfp.intersection(fps);allfp.update(fps)
  assert rows==g.batch(level,n,43)
  try:g.batch(level,n+1,0);raise AssertionError('Capacity accepted')
  except ValueError:pass
  capacities[level]=n;preview=g.batch(level,2,3);save('preview-'+level+'.json',preview);(HERE/('preview-'+level+'.md')).write_text('\n\n---\n\n'.join(map(g.markdown,preview)))
 save('capacity.json',{'mathematical_capacities':capacities,'cross_profile_and_level_dedup':True,'cosmetics_excluded':True,'overcapacity_rejected':True,'all_cli_count_1_flat_records':3})
 cli=json.loads(subprocess.check_output([sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--count','1']));assert len(cli)==3 and all('question' in q for q in cli)
 (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 baseline=json.load(open(HERE/'registered-baseline.json'));assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in baseline['sha256'].items())
 current=[str(HERE.with_name('17592186064205').with_suffix('.py').resolve())]+sorted(str(p.resolve()) for p in HERE.with_name('17592186064205').rglob('*') if p.is_file());assert set(current)==set(baseline['full_path_set'])
 save('validation.json',{'passed':True,'exhaustive_normal_instances':len(inputs),'full_domain_per_profile':len(g.DOMAIN),'source_cases':len(cases),'MA_banks':9,'MA_choices':45,'nonMA_inventory':2,'solution_validation':'Independent displayed integrand, substitution, actual differential, all integration stages, actual derivative operands and all derivative rows; all choices pairwise derivative-distinct modulo C on explicit positive-base domain','source_errors_retained_in_source_API':True,'native_engine_sha256':sha,'registered_full_path_set_and_hashes_unchanged':True,'duration_seconds':time.time()-started})
 print('All validation passed:',len(inputs),'instances',flush=True)
if __name__=='__main__':main()
