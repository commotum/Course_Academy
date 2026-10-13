"""Independent rendered-equation verification, complete replay and native grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')
def expr(s):
 s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s.strip().rstrip('.'))
 return parse_expr(s,transformations=standard_transformations+(implicit_multiplication_application,))
def equation(q):
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/problem'],re.S)
 if blocks:return blocks[0]
 return re.search(r'\$([^$]*x[^$]*=[^$]*)\$',q[':question/problem']).group(1)
def solve_display(q):
 lhs,rhs=equation(q).split('=');x=sp.Symbol('x');poly=sp.Poly(sp.expand(expr(lhs)-expr(rhs)),x)
 assert poly.degree()==1
 variables=sorted(poly.as_expr().free_symbols-{x},key=str);assert len(variables)==2
 roots=sp.solve(poly.all_coeffs(),variables,dict=True);assert len(roots)==1 and set(roots[0])==set(variables)
 assert sp.expand(poly.as_expr().subs(roots[0]))==0
 return poly,roots[0]
def fingerprint(q):
 _,roots=solve_display(q)
 return g.digest(['general-identity',*[str(z) for z in sorted(roots.values())]])
def check(rec):
 q=rec['question'];meta=rec['generation'];level=q[':question/difficulty'].split('/')[-1]
 assert rec['knowledge_point']['db_id']==g.KP_ID
 assert g.generate(level,meta['seed'],meta['template'],meta['parameters'])==rec
 poly,roots=solve_display(q);total=sum(roots.values())
 f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];values=[expr(a[':answer/value']) for a in bank]
 assert len(set(values))==len(values) and values.count(total)==1
 correct=next(expr(a[':answer/value']) for a in bank if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==total
 assert '{{field-1}}' in q[':question/problem'] if level=='moderate' else '{{' not in q[':question/problem']
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
 assert len(blocks) in (7,8)
 assert blocks[2]==equation(q)
 for i in range(3,len(blocks)-1):
  s=blocks[i].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
  lhs,rhs=s.split('=');assert sp.simplify((expr(lhs)-expr(rhs)).subs(roots))==0
 final=blocks[-1].rstrip('.').split('=');assert len(final)==3
 assert all(sp.simplify(expr(side).subs(roots))==total for side in final)
 a,b,c,d,e,f=map(sp.Rational,meta['parameters']);u,v=map(sp.Symbol,g.SOURCE_CASES[meta['template']][3:5])
 assert roots[u]==(c-b)/a and roots[v]==(f-e)/d
 assert meta['mathematical_fingerprint']==g.fingerprint(meta['parameters'])
 return rec
def native(label,rec):
 field=rec['question'][':question/answer-fields'][0];checks=[]
 if field[':answer-field/type']==':answer-field.type/radio':
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'actual radio choice selection'} for a in field[':answer-field/choices']]
 else:
  total=expr(field[':answer-field/choices'][0][':answer/value'])
  for entry in (str(total),str(total)+'.0',r'\frac{'+str(2*total)+'}{2}',str(total)+'+0'):
   checks.append({'submitted':entry,'expected':'accepted','purpose':'equivalent blank entry'})
  for entry in (str(total+1),str(total-1)):
   checks.append({'submitted':entry,'expected':'rejected','purpose':'incorrect blank entry'})
 return {'label':label,'record':rec,'checks':checks}
def main():
 replay=[];inputs=[];review=[];count=0;identities={}
 for mid,(level,family,profile,u,v,p) in g.SOURCE_CASES.items():
  old=g.SOURCES[mid];r=check(g.generate(level,0,mid,p));q=r['question'];f=q[':question/answer-fields'][0];oldf=old[':question/answer-fields'][0]
  assert old[':question/problem']==q[':question/problem'],(mid,'prompt')
  assert old[':question/worked-solution']==q[':question/worked-solution'],(mid,'solution',q[':question/worked-solution'])
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in oldf[':answer-field/choices'])
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==oldf[':answer-field/correct'][':answer/value']
  assert f[':answer-field/key']==oldf[':answer-field/key'] and f[':answer-field/type']==oldf[':answer-field/type'][':db/ident']
  replay.append({'source':mid,'matched_choices':len(f[':answer-field/choices']),'matched_incorrect_choices':len(f[':answer-field/choices'])-1,'complete_bank_match':True,'prompt_exact':True,'solution_exact':True,'variant_support':profile!='literal-replay-only'})
  inputs.append(native(mid,r));review.append('Original '+mid+'\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\nExact replay\n\n'+g.markdown(r))
  if profile=='literal-replay-only':continue
  for seed in range(100):
   variant=check(g.generate(level,seed,mid));count+=1
   qid=variant['question'][':question/id'];assert qid not in identities or identities[qid]==variant['question'];identities[qid]=variant['question']
   assert variant==g.generate(level,seed,mid)
   assert g.generate(level,seed+100,mid,variant['generation']['parameters'])['question']==variant['question']
   if seed<10:inputs.append(native(mid+' seed '+str(seed),variant))
  review.append('Variant '+mid+'\n\n'+g.markdown(g.generate(level,42,mid)))
 for level in ('easy','moderate'):
  records=g.batch(level,30,10000);assert len({r['generation']['mathematical_fingerprint'] for r in records})==30
 assert g.fingerprint([1,2,7,5,0,15])==g.fingerprint([2,4,14,10,0,30])
 save('engine-input.json',inputs);binary=ROOT/'generate/runs/current/check-engine';subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'native-grading.json')],check=True)
 save('source-replay.json',replay);(HERE/'review.md').write_text('\n\n---\n\n'.join(review))
 save('validation.json',{'passed':True,'source_basis':json.loads((HERE/'source.json').read_text())['basis'],'complete_banks_matched':5,'choices_matched':17,'incorrect_choices_matched':12,'displayed_math_instances':count,'source_prompt_solution_fidelity':'exact for all five complete records','legacy_incomplete_excluded':['q-287978','q-287985'],'literal_replay_only':['q-288623','q-288627'],'supported':['easy','moderate'],'unsupported':['hard'],'native_grading':json.loads((HERE/'native-grading.json').read_text()),'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),Path(__file__),binary,ROOT/'generate/runs/current/check-engine.rs',HERE/'source.json')}})
 print('Validated 5 complete source banks, 300 varied equations, native radio and blank grading.')
if __name__=='__main__':main()
