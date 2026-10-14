"""Independent polynomial substitution, complete source bank replay and native grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('circle',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def check(r):
 q=r['question'];m=r['generation'];p=m['parameters'];radius,h,k=[sp.sympify(p[a]) for a in ('r','h','k')]
 assert radius>0 and g.fingerprint(q)=='|'.join(map(str,(radius,h,k)))==m['mathematical_fingerprint']
 assert r==g.generate(q[':question/difficulty'].split('/')[-1],m['seed'],m['template'],p,m['replay'])
 fs=q[':question/answer-fields'];sol=q[':question/worked-solution'];expected=sp.expand((g.x-h)**2+(g.y-k)**2-radius**2)
 final=re.search(r'Therefore the Cartesian equation is \$(.*?)\.\$',sol)[1];assert sp.expand(g.polynomial(final)-expected)==0
 seen={q[':question/id']}
 for i,f in enumerate(fs):
  assert f[':answer-field/id'] not in seen;seen.add(f[':answer-field/id'])
  assert f[':answer-field/key']==('selection' if len(fs)==1 else 'field-'+str(i+1))
  choices=f[':answer-field/choices'];correct=[a for a in choices if a[':answer/id']==f[':answer-field/correct'][1]];assert len(correct)==1
  for a in choices:assert a[':answer/id'] not in seen;seen.add(a[':answer/id'])
  if len(fs)==1:
   assert len(choices)==5;polys=[g.polynomial(a[':answer/value']) for a in choices];assert len(set(polys))==5
   assert sum(sp.expand(v-expected)==0 for v in polys)==1 and sp.expand(g.polynomial(correct[0][':answer/value'])-expected)==0
   assert sp.trigsimp(expected.subs({g.x:radius*sp.cos(g.theta)+h,g.y:radius*sp.sin(g.theta)+k}))==0
   # Independently refute each distractor at a point of the circle (finite sample sufficient for degree 2 trig polynomial).
   for a,poly in zip(choices,polys):
    vals=[sp.simplify(poly.subs({g.x:radius*sp.cos(t)+h,g.y:radius*sp.sin(t)+k})) for t in (0,sp.pi/2,sp.pi,3*sp.pi/2,sp.pi/4)]
    assert all(v==0 for v in vals) if a==correct[0] else any(v!=0 for v in vals)
  else:assert len(choices)==1 and g.parse_math(correct[0][':answer/value'])==(abs(h),abs(k),radius**2)[i]
 assert sol.count('By squaring')==2 if len(fs)==1 and h==k==0 else sol.count('By isolating')==2
 assert 'Adding the two equations' in sol and r'\cos^2\theta+\sin^2\theta' in sol
 # Check every displayed intermediate equality by substituting the rendered circle data.
 def expression(text):
  text=text.strip().rstrip('.')
  for name in ('cos','sin'):
   text=text.replace('\\'+name+r'^2\theta','('+name+'(theta))^2').replace('\\'+name+r'\theta',name+'(theta)')
  from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
  text=text.replace(r'\frac',r'\frac')
  for _ in range(5):text=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',text)
  text=text.replace('{','(').replace('}',')').replace('^','**')
  return parse_expr(text,local_dict={'x':g.x,'y':g.y,'theta':g.theta,'cos':sp.cos,'sin':sp.sin},transformations=standard_transformations+(implicit_multiplication_application,))
 for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol):
  lhs=None
  for row in block.split(r'\\'):
   left,right=row.split('&=')
   if left:lhs=expression(left)
   assert lhs is not None
   difference=(lhs-expression(right)).subs({g.x:radius*sp.cos(g.theta)+h,g.y:radius*sp.sin(g.theta)+k})
   assert sp.trigsimp(sp.expand(difference))==0,(m['template'],row,difference)
 return r
def native(label,r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   checks += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each complete radio option'} for a in f[':answer-field/choices']]
  else:
   v=g.parse_math(f[':answer-field/choices'][0][':answer/value']);checks += [{'field_index':i,'submitted':z,'expected':expected,'purpose':purpose} for z,expected,purpose in [(g.tex(v),'accepted','canonical fragment'),(str(v),'accepted','equivalent rational'),(str(v+1),'rejected','wrong fragment')]]
 return {'label':label,'record':r,'checks':checks}
def main():
 samples=[];inputs=[];replays=[];mapping=[];coverage={};review=[]
 for t in g.TEMPLATES:
  source=g.SOURCES[t];spec=g.SPECS[t];assert g.fingerprint(source)=='|'.join(str(sp.sympify(spec[a])) for a in ('r','h','k'));r=check(g.generate(spec['difficulty'],0,t,g.original(t),True));sf=sorted(source[':question/answer-fields'],key=lambda f:f[':answer-field/key']);gf=r['question'][':question/answer-fields'];bank=[]
  for a,b in zip(sf,gf):
   original=[g.polynomial(v[':answer/value']) if len(sf)==1 else g.parse_math(v[':answer/value']) for v in a[':answer-field/choices']]
   generated=[g.polynomial(v[':answer/value']) if len(gf)==1 else g.parse_math(v[':answer/value']) for v in b[':answer-field/choices']]
   assert len(original)==len(generated) and set(original)==set(generated),(t,original,generated)
   ac=a[':answer-field/correct'][':answer/value'];bc=next(z[':answer/value'] for z in b[':answer-field/choices'] if z[':answer/id']==b[':answer-field/correct'][1]);assert (g.polynomial(ac)==g.polynomial(bc) if len(sf)==1 else g.parse_math(ac)==g.parse_math(bc))
   for v in a[':answer-field/choices']:
    obj=g.polynomial(v[':answer/value']) if len(sf)==1 else g.parse_math(v[':answer/value']);idx=generated.index(obj)
    recipe=list(map(str,g.recipes(spec['profile'],*[sp.sympify(spec[z]) for z in ('r','h','k')])[idx])) if len(sf)==1 else ['abs(h)','abs(k)','r^2'][int(a[':answer-field/key'].split('-')[-1])-1]
    mapping.append({'source':t,'source_db_id':source[':db/id'],'field':a[':answer-field/key'],'source_answer_uuid':v[':answer/id'],'value':v[':answer/value'],'profile':spec['profile'],'recipe_at_original':recipe,'recipe_index':idx,'complete_value_reproduced':True});bank.append(v)
  replays.append({'source':t,'profile':spec['profile'],'matched_choices':len(bank),'total_choices':len(bank),'matched_distractors':len(bank)-len(sf),'complete_bank_match':True,'correct_designations_match':True,'field_layout_match':True})
  inputs.append(native('replay-'+t,r));review.append('## '+t+' source\n\n'+source[':question/problem']+'\n\n'+source[':question/worked-solution']+'\n\n## Replay\n\n'+g.markdown(r))
  c={key:set() for key in ('r','h','k','fingerprints')}
  for seed in range(20):
   r=check(g.generate(spec['difficulty'],seed,t));samples.append(r);inputs.append(native(t+'-'+str(seed),r))
   for key in ('r','h','k'):c[key].add(r['generation']['parameters'][key])
   c['fingerprints'].add(g.fingerprint(r['question']));assert r['question']==g.generate(spec['difficulty'],seed+1000,t,r['generation']['parameters'])['question']
  assert len(c['r'])>1
  for key in ('h','k'):assert len(c[key])>1 if sp.sympify(spec[key])!=0 else c[key]=={'0'}
  coverage[t]={key:sorted(vals) for key,vals in c.items()};review.append('## Sample\n\n'+g.markdown(r))
 # Changed centre with radius and remaining centre held constant, checking all rendered references and key.
 t=next(t for t in g.TEMPLATES if g.SPECS[t]['profile']=='blank');p=g.original(t);a=check(g.generate('hard',0,t,p));p['h']='-7/2';b=check(g.generate('hard',0,t,p));assert a['generation']['parameters']['r']==b['generation']['parameters']['r'] and a['generation']['parameters']['k']==b['generation']['parameters']['k'];assert g.fingerprint(a['question'])!=g.fingerprint(b['question']);inputs += [native('changed-centre-before',a),native('changed-centre-after',b)]
 # No seed, profile or order can make the same geometric question fresh.
 assert a['question']==g.generate('hard',999,t,a['generation']['parameters'])['question'];cq=dict(a['question']);cq[':question/answer-fields']=list(reversed(cq[':question/answer-fields']));assert g.fingerprint(cq)==g.fingerprint(a['question'])
 try:g.batch('easy',5,0)
 except ValueError:pass
 else:raise AssertionError('Unsupported easy accepted')
 save('source-choice-mapping.json',mapping);save('source-replay.json',{'passed':True,'basis':g.S['basis'],'complete_banks_matched':len(replays),'complete_banks_total':len(replays),'matched_choices':sum(z['matched_choices'] for z in replays),'matched_distractors':sum(z['matched_distractors'] for z in replays),'missing_or_extra_options':[],'profiles':replays,'excluded_sources':g.EXCLUDED})
 save('native-input.json',inputs);subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 save('previews.json',samples);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'supported_levels':list(g.SUPPORTED_LEVELS),'unsupported_levels':['easy'],'sample_count':len(samples),'source_banks':len(replays),'source_fidelity':'Complete mathematical banks, keys, field layouts, prompt structure and ordered solution stages preserved. TeX normalized; theorem wording corrected from theorem to identity. Replays do not copy literals.','actual_grading':'All radio options and canonical/equivalent/wrong entries for all blanks through learning::grade_field; zero unresolved','mathematics':'Exact polynomial normalization, substitution into parametrization, distractor counterexamples, blank keys; parsed rendered final equations and givens','coverage':coverage,'changed_centre_checked':True,'distinctness':'radius and centre; ignores field style, choices, seed and identity','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'source-specs.json')}})
 print('Validated',len(replays),'source banks and',len(samples),'sampled variants.')
if __name__=='__main__':main()
