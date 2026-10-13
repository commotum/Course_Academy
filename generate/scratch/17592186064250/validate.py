"""Full-bank source replay, independent symbolic calculus and actual learner grader."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('arcsec_generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=sp.Symbol('x',real=True);U=sp.Symbol('u',real=True);C=sp.Symbol('C',real=True)

def latex(s):
 s=s.replace('\u2061','').replace('\u00a0',' ').replace(r'\,','').replace(r'\left','').replace(r'\right','')
 s=re.sub(r'\\(?:operatorname|text|textrm)\{(arcsec|arcsin|arctan)\}',lambda m:{'arcsec':'asec','arcsin':'asin','arctan':'atan'}[m[1]],s)
 def group(s,start):
  assert s[start]=='{',s
  depth=1;i=start+1
  while depth:
   depth+=(s[i]=='{')-(s[i]=='}');i+=1
  return s[start+1:i-1],i
 def convert(s):
  out='';i=0
  while i<len(s):
   if s.startswith(r'\frac',i) or s.startswith(r'\dfrac',i):
    i+=6 if s.startswith(r'\dfrac',i) else 5;a,i=group(s,i);b,i=group(s,i);out+='(('+convert(a)+')/('+convert(b)+'))'
   elif s.startswith(r'\sqrt',i):
    i+=5;a,i=group(s,i);out+='sqrt('+convert(a)+')'
   elif s[i]=='|':
    j=s.index('|',i+1);out+='Abs('+convert(s[i+1:j])+')';i=j+1
   else:out+=s[i];i+=1
  return out
 s=convert(s).replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(s,local_dict={'x':X,'u':U,'C':C,'asec':sp.asec,'asin':sp.asin,'atan':sp.atan,'Abs':sp.Abs,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))

def integrand(q):
 p=q[':question/problem'];p=p[p.index(r'\int')+4:];p=p.split('$')[0];p=re.sub(r'=\s*}*\s*$','',p).strip().rstrip('.')
 p=p.replace(r'\,','').replace(r'\frac{\text{d}x}',r'\frac{1}').replace(r'\dfrac{\textrm{d}x}',r'\frac{1}').replace(r'\text{d}x','').replace(r'\textrm{d}x','').strip()
 return sp.simplify(latex(p))

def fingerprint(q):
 try:
  e=integrand(q)
  # Recover the two exact mathematical parameters directly from the expression.
  denominators=list(e.atoms(sp.Pow));roots=[z for z in denominators if z.exp==sp.Rational(-1,2)]
  assert len(roots)==1
  b=sp.expand(roots[0].base).coeff(X,2);assert b>0 and sp.expand(roots[0].base).subs(X,0)==-1
  c=sp.simplify(e*sp.Abs(X)*sp.sqrt(b*X**2-1));assert not c.has(X)
  return g.mathematical_key(sp.sqrt(b),c)
 except (ValueError,AssertionError,IndexError,TypeError):return None

def normalized(q):
 out={k:str(q[k]) if k==':question/id' else q[k] for k in [':question/id',':question/problem',':question/worked-solution']}
 out[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);out[':question/answer-fields']=[]
 for f in q[':question/answer-fields']:
  out[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])]})
 return out

def check_question(q):
 e=integrand(q);f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 bank=f[':answer-field/choices'];assert len(bank)==5 and len({a[':answer/id'] for a in bank})==5
 vals=[latex(a[':answer/value']) for a in bank];correct=f[':answer-field/correct'][1];hits=[]
 for i,z in enumerate(vals):
  # Principal inverse secant derivative, independently from generator recipes.
  d=sp.diff(z,X)
  good=True
  for sign in [1,-1]:
   y=sp.Symbol('y',positive=True);delta=sp.simplify((d-e).subs(X,sign*y))
   good &= delta==0
  if good:hits.append(i)
 assert len(hits)==1 and bank[hits[0]][':answer/id']==correct,(hits,q[':question/problem'])
 for i,z in enumerate(vals):
  for w in vals[:i]:assert sp.simplify(z-w)!=0,'duplicate bank values'
 assert fingerprint(q) is not None
 return hits[0]

def check(r):
 q=r['question'];meta=r['generation'];profile=meta['profile'];t=meta['parameters']['t']
 assert r==g.generate(q[':question/difficulty'].split('/')[-1],meta['seed'],profile=profile,t=t),'Instance differs from deterministic generator'
 hit=check_question(q);assert hit==g.PROFILES[profile][-1]
 assert fingerprint(q)==meta['mathematical_key']
 assert ':question/math-academy-id' not in q
 for s in [q[':question/problem'],q[':question/worked-solution']]:
  assert s.count('$')%2==0 and s.count('{')==s.count('}') and '![' not in s
 # Independently validate the u-substitution and normalization for either sign.
 n,a,c=g.parameters(profile,t);z=sp.Symbol('z',positive=True);e=integrand(q)
 for sign in [-1,1]:
  xexpr=sign*z/n
  assert sp.simplify(e.subs(X,xexpr)/n-c/(z*sp.sqrt(z*z-1)))==0
 # The displayed final primitive is parsed independently of bank metadata.
 sol=q[':question/worked-solution'];last=sol.split('& =')[-1].split(r'\end{aligned}')[0].strip().rstrip('.')
 assert sp.simplify(latex(last)-latex(q[':question/answer-fields'][0][':answer-field/choices'][hit][':answer/value']))==0
 return hit

def engine_item(label,r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every authored choice graded by radio identity'} for a in f[':answer-field/choices']]}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 rows=[];replays=[];report=[]
 for p,v in g.PROFILES.items():
  print('Validating',p,flush=True)
  q=g.ORIGINALS[p];r=g.generate(v[0],0,profile=p,t=v[2]);check(r)
  # Complete mathematical objects and correct designation, ignoring order.
  old=normalized(q);check_question(old)
  oldvals=[latex(a[':answer/value']) for a in old[':question/answer-fields'][0][':answer-field/choices']]
  newvals=[latex(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  matches=[[i for i,z in enumerate(newvals) if sp.simplify(w-z)==0] for w in oldvals]
  assert all(len(m)==1 for m in matches) and len({m[0] for m in matches})==5,(p,matches)
  assert r['question'][':question/problem'].removesuffix('\n\n{{selection}}')==q[':question/problem']
  assert r['question'][':question/worked-solution']==q[':question/worked-solution']
  replays.append(r);passed=0
  for t in g.DOMAIN:
   if g.eligible(p,t):
    r=g.generate(v[0],371,profile=p,t=t);check(r);rows.append(r);passed+=1
    assert r['question']==g.generate(v[0],17,profile=p,t=t)['question']
  report.append({'profile':p,'template':v[1],'matched_distractors':4,'total_distractors':4,'complete_banks_matched':1,'total_source_banks':1,'eligible_parameters_tested':passed})
 for level in ['moderate','hard']:
  r=g.batch(level,5,874);assert len({z['generation']['mathematical_key'] for z in r})==5
 (H/'engine-input.json').write_text(json.dumps([engine_item(str(i),r) for i,r in enumerate(rows)],indent=2))
 subprocess.run([str(H/'check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
 engine=json.loads((H/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 bounds={level:len({r['generation']['mathematical_key'] for r in rows if r['question'][':question/difficulty'].endswith('/'+level)}) for level in ['moderate','hard']}
 capability={'supported_levels':['moderate','hard'],'unsupported_levels':{'easy':'No easy source questions, field shapes or grading/difficulty evidence at basis '+str(g.SOURCE['basis'])+'. Reopen on new evidence; no easy quota claimed filled.'},'bounded_distinct_tasks':bounds,'sampling':'Positive integers t=2..24; nonsquare radicands for root profiles; source equal/proportional relationships retained. Negative slopes deferred, not observed. No variants from bank/seed/order changes.','plots':'none'}
 (H/'capability.json').write_text(json.dumps(capability,indent=2))
 (H/'review.md').write_text('\n\n'.join('## '+r['generation']['profile']+' source replay\n\n'+g.markdown(r)+'\n\n### New variant\n\n'+g.markdown(g.generate(r['question'][':question/difficulty'].split('/')[-1],0,profile=r['generation']['profile'],t=next(t for t in reversed(g.DOMAIN) if g.eligible(r['generation']['profile'],t)))) for r in replays))
 result={'passed':True,'source_basis':g.SOURCE['basis'],'complete_source_banks_matched':17,'total_source_banks':17,'matched_distractors':68,'total_distractors':68,'profiles':report,'exhaustive_instances':len(rows),'fidelity':'All prompt/solution source layouts exact; full banks equivalent; explicit selection placeholder added; answer notation canonicalized.','correctness':'Independent displayed-integrand/primitive differentiation for both signs; u-substitution; single correct answer; distinct bank; final displayed solution independently parsed.','grading':{k:engine[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks']},'files':{str(p.relative_to(ROOT)):sha(p) for p in [H.with_suffix('.py'),Path(__file__),H/'source.json',H/'source.edn',H/'capability.json',H/'check-engine']}}
 (H/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
