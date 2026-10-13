"""Independent printed-expression QA and actual learner radio grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
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
def equal(a,b,t,shift):
 # Positive-base interval supports every bank, including altered radicands.
 z=(U+3-shift)/t['a'];return sp.simplify(sp.powdenest((a-b).subs(p.u,t['a']*x+shift).subs(x,z),force=True))==0
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
 intro=blocks[0].split(r'\int',1)[1].split(r'\,\text{d}')[0];assert equal(scalar(intro,t['variable']),integrand,t,b)
 assert '='+str(t['a'])+r'\,' in blocks[1]
 def value(s,derivative=False):
  s=s.strip().replace('✓','');var=t['variable']
  if r'\int' in s:
   coef,rest=s.split(r'\int',1);m=re.search(r'\\text\{d\}([a-z])',rest);assert m,rest;diffvar=m[1];expr=rest[:m.start()]+rest[m.end():]
   z=(scalar(coef,var) if coef.strip() else 1)*scalar(expr,var);z=z.subs(p.u,t['a']*x+b)
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
 meta=rec['generation'];q=rec['question'];sid=meta['template'];t=g.PROFILES[sid];b=meta['parameters'][0]
 assert rec==g.generate(t['difficulty'],meta['seed'],sid,[b])
 integrand,var=prompt_data(q);assert var==t['variable'];assert fingerprint(q)==meta['mathematical_fingerprint']
 f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];assert len(bank)==5 and len({a[':answer/id'] for a in bank})==5
 vals=[scalar(a[':answer/value'],var) for a in bank]
 assert all(not equal(sp.diff(z-w,x),0,t,b) for i,z in enumerate(vals) for w in vals[:i]),'Equivalent bank values'
 good=[a[':answer/id'] for a,z in zip(bank,vals) if equal(sp.diff(z,x),integrand,t,b)];assert good==[f[':answer-field/correct'][1]]
 for z,r in zip(vals,t['bank']):
  expected=sp.Rational(r['coefficient'])*(t['a']*x+b+r['offset'])**sp.Rational(r['exponent'])+p.v
  assert equal(z,expected,t,b)
 # Real odd-root continuation: explicitly differentiate the real branch at
 # negative radicands using c sign(u)^m |u|^(m/d), excluding zero.
 if t['denominator']%2:
  r=next(r for r in t['bank'] if r['correct']);e=sp.Rational(r['exponent']);n,d=e.p,e.q
  derivative=sp.Rational(r['coefficient'])*e*t['a']*(-1)**(n-1)*U**(e-1)
  assert sp.simplify(derivative-(-1)**t['numerator']*U**sp.Rational(t['numerator'],t['denominator']))==0
 solution_check(q,t,b,integrand)
 return rec
def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual application radio grading'} for a in f[':answer-field/choices']]}
def main():
 old={q[':question/math-academy-id']:q for q in json.loads((HERE/'reference/source.json').read_text())[':knowledge-point/questions']};replay=[];inputs=[];review=[];n=0
 for sid,t in g.PROFILES.items():
  r=check(g.generate(t['difficulty'],0,sid,[t['b']]));q=r['question'];o=old[sid];f=q[':question/answer-fields'][0]
  assert q[':question/problem']==o[':question/problem'];assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in o[':question/answer-fields'][0][':answer-field/choices']]
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==o[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
  expected=o[':question/worked-solution'].replace('final answer in terms of $u$ at the very end','final answer in terms of $'+t['variable']+'$ at the very end')
  if sid=='q-17019':expected=expected.replace('^{3/2}','^{2/3}')
  assert q[':question/worked-solution']==expected
  replay.append({'source':sid,'matched_choices':5,'matched_distractors':4,'complete_bank_match':True,'prompt_exact':True,'solution_exact_after_documented_corrections':True})
  variant=check(g.generate(t['difficulty'],42,sid));review.append('## '+sid+'\n\nOriginal\n\n'+o[':question/problem']+'\n\n'+o[':question/worked-solution']+'\n\nReplay\n\n'+g.markdown(r)+'\n\nVariant\n\n'+g.markdown(variant))
  # Check boundaries, signs, source shifts and deterministic spread per profile.
  for b in sorted(set([-100,-99,-11,-3,-1,1,2,3,11,99,100,t['b']]+[v[0] for v in random_samples(sid)])):
   r=check(g.generate(t['difficulty'],0,sid,[b]));assert g.generate(t['difficulty'],99,sid,[b])['question']==r['question'];inputs.append(native(sid+' '+str(b),r));n+=1
 save('source-replay.json',{'passed':True,'complete_banks_matched':8,'complete_banks_total':8,'distractors_matched':32,'distractors_total':32,'profiles':replay,'excluded_incomplete_sources':['q-49392'],'source_corrections':['q-17019 derivative verification uses 3/2 twice where 2/3 is required','End-variable prose says u but final answer uses original variable']})
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('previews.json',g.batch('moderate',5,1930)+g.batch('hard',5,1930));(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'validated_instances':n,'scope':'Every profile; sampled shifts including both bounds, positive/negative, observed values; every submitted instance revalidated','mathematics':'Independent printed integrand/options/all solution equalities; exact differentiation; positive interval and odd-root negative continuation; bank uniqueness','supported_levels':['moderate','hard'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'contract.json',HERE/'validate.py',HERE/'scalar-parser.py')}})
 print('Validated',n,'instances')
def random_samples(sid):
 import random
 return random.Random(sid).sample(g.candidates(sid),10)
if __name__=='__main__':main()
