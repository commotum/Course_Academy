"""Independent displayed-math, complete fidelity, domain, identity and native QA."""
import importlib.util,json,re,subprocess,hashlib
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('general_identity',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=sp.Symbol('x');TRANS=standard_transformations+(implicit_multiplication_application,)
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def expr(s):
 s=s.strip().rstrip('.,').replace('&','').replace(r'\,','').replace(r'\quad','')
 while r'\frac' in s:
  n=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
  assert n!=s,s;s=n
 assert '\\' not in s,s
 s=re.sub(r'(?<=\d)(?=[a-zA-Z])','*',s)
 return sp.expand(parse_expr(s,local_dict={'x':X},transformations=TRANS))
def equation(s):
 l,r=s.split('=');return sp.expand(expr(l)-expr(r))
def math_blocks(s):return re.findall(r'\$\$\n(.*?)\n\$\$',s,re.S)
def actual_equation(q):
 blocks=math_blocks(q[':question/problem'])
 return blocks[0] if blocks else re.search(r'\$([^$]*x[^$]*=[^$]+)\$',q[':question/problem']).group(1)
def audit(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 q=rec['question'];meta=rec['generation'];raw=meta['profile'].startswith('raw:');missing=raw and meta['template'] in ('q-287978','q-287985')
 eq=actual_equation(q);res=equation(eq);symbols=sorted(res.free_symbols-{X},key=str);assert len(symbols)==2
 coefficient=res.coeff(X);constant=res.subs(X,0)
 # Solve from displayed x-coefficient and constant, independently of metadata.
 roots=sp.solve([coefficient,constant],symbols);assert len(roots)==2
 values={str(k):v for k,v in roots.items()};total=sum(roots.values())
 left,right=map(expr,eq.split('='));lc,rc=left.coeff(X),right.coeff(X);lk,rk=left.subs(X,0),right.subs(X,0)
 u=next(s for s in symbols if lc.has(s));v=next(s for s in symbols if lk.has(s))
 actual=[lc.coeff(u),lc.subs(u,0),rc,lk.coeff(v),lk.subs(v,0),rk]
 expected=g.fingerprint(actual)
 assert meta['mathematical_fingerprint']==expected
 f=q[':question/answer-fields'][0];bank=f.get(':answer-field/choices',[]);parsed=[expr(a[':answer/value']) for a in bank]
 assert len(set(parsed))==len(parsed)
 if missing:
  assert ':question/worked-solution' not in q and ':question/difficulty' not in q and ':answer-field/correct' not in f
  if bank:assert total in parsed
 else:
  assert parsed.count(total)==1
  if not raw:
   a,b,c,d,e,z=list(map(g.rat,meta['parameters'].values()));U,V=(c-b)/a,(z-e)/d
   expected_bank={'method-sum':[total,U,V,c+z,U-V],'method-components':[total,c/a+V,U+z/d,a*(c-b)+V,U+d*(z-e)],'blank':[total]}[meta['profile']]
   assert set(parsed)==set(expected_bank)
  correct=next(a for a in bank if a[':answer/id']==f[':answer-field/correct'][1]);assert expr(correct[':answer/value'])==total
  solution=q[':question/worked-solution'];blocks=math_blocks(solution);assert len(blocks) in (7,8)
  assert equation(blocks[2])==res
  for block in blocks[3:-1]:
   block=re.sub(r'\\begin\{aligned\}|\\end\{aligned\}','',block)
   assert sp.simplify(equation(block).subs(roots))==0,block
  chain=blocks[-1].rstrip('.').split('=');assert all(sp.simplify(expr(term).subs(roots)-total)==0 for term in chain),chain
  assert all(str(s) in solution for s in symbols)
  # Every displayed root in final prose matches the actual prompt.
  prose=re.search(r'Finally, since \$(.*?)\$ and \$(.*?)\$,? we have',solution)
  assert prose
  for s in prose.groups():assert equation(s).subs(roots)==0
 for obj,key in [(q,':question/id'),(f,':answer-field/id')]+[(a,':answer/id') for a in bank]:g.uuid.UUID(obj[key])
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in bank]:
  assert text.count('$')%2==0 and text.count('$$')%2==0
  depth=0
  for char in text:
   depth+=int(char=='{')-int(char=='}');assert depth>=0
  assert depth==0
  assert '+-' not in text and '--' not in text
 return total

def native(rec,label):
 checks=[]
 for i,f in enumerate(rec['question'][':question/answer-fields']):
  if ':answer-field/correct' not in f:return None
  if f[':answer-field/type'].endswith('/radio'):
   checks += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'whole displayed bank'} for a in f[':answer-field/choices']]
  else:
   value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);n=expr(value)
   equiv='('+str(n.p*2)+')/('+str(n.q*2)+')'
   checks += [{'field_index':i,'submitted':entry,'expected':expect,'purpose':purpose} for entry,expect,purpose in [(value,'accepted','canonical exact value'),(equiv,'accepted','independently unreduced rational'),(str(n+1),'rejected','incorrect value')]]
 return {'label':label,'record':rec,'checks':checks}

def main():
 source=json.loads((ROOT/'generate/runs/current/sources/17592186110721.json').read_text());save('source.json',source)
 fidelity=[];cases=[];review=[];engine=[];byte_audit=[];normal=[];counts={};positions=set()
 for mid,(level,u,v,p) in g.SOURCE_CASES.items():
  original=g.SOURCES[mid];profile='raw:'+mid;rec=g.generate(level,parameters=p,template=mid,profile=profile);audit(rec);q=rec['question'];f=q[':question/answer-fields'][0];of=original[':question/answer-fields'][0]
  assert q[':question/problem']==original[':question/problem'],mid
  assert q.get(':question/worked-solution')==original.get(':question/worked-solution'),mid
  assert (':question/difficulty' in q)==(':question/difficulty' in original)
  assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
  ov=[a[':answer/value'] for a in of.get(':answer-field/choices',[])];rv=[a[':answer/value'] for a in f.get(':answer-field/choices',[])]
  assert sorted(ov)==sorted(rv),(mid,ov,rv)
  assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  cases.append({'source_id':mid,'level':level,'template':mid,'parameters':rec['generation']['parameters'],'bank_profile':profile})
  fidelity.append({'source_id':mid,'prompt_exact':True,'solution_exact':':question/worked-solution' in original,'solution_omission_exact':':question/worked-solution' not in original,'field_shape_exact':True,'choices_matched':len(ov),'correct_designation_matched':':answer-field/correct' in original,'designation_omission_exact':':answer-field/correct' not in original})
  byte_audit.append({'source_id':mid,'choice_double_backslash_runs':[value.count(chr(92)*2) for value in ov]})
  review.append({'label':'Observed source and parameterized raw replay '+mid,'original':original,'record':rec})
  n=native(rec,'source '+mid)
  if n:engine.append(n)
  raw_variant=g.generate(level,23,template=mid,profile=profile);audit(raw_variant);review.append({'label':'Changed-parameter evidence-only observed bank '+mid,'record':raw_variant})
  variant=g.generate(level,100,template=mid);audit(variant);review.append({'label':'Normal authored bank/completion variant '+mid,'record':variant});engine.append(native(variant,'variant '+mid))
 for level in ('easy','moderate','hard'):
  fps=set();n=0
  for template in g.TEMPLATES[level]:
   for kind,profile in [('radio','method-sum'),('blank','blank')]+([('radio','method-components')] if level=='hard' else []):
    for seed in range(80):
     rec=g.generate(level,seed,template=template,field_type=kind,profile=profile);audit(rec);n+=1;fps.add(rec['generation']['mathematical_fingerprint'])
     assert rec==g.generate(level,seed,template=template,field_type=kind,profile=profile)
     other=g.generate(level,seed+91,template=template,field_type=kind,profile=profile,parameters=rec['generation']['parameters']);assert rec['question'][':question/id']==other['question'][':question/id']
     assert rec['generation']['mathematical_fingerprint']==other['generation']['mathematical_fingerprint']
     if kind=='radio':
      f=rec['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
     if seed<2:review.append({'label':f'Generated {level}/{template}/{profile}/{seed}','record':rec});engine.append(native(rec,f'{level}/{template}/{profile}/{seed}'))
     if seed<10:normal.append(rec)
  counts[level]={'tested':n,'distinct_mathematical_tasks_in_test':len(fps)}
 assert positions==set(range(5)),positions
 # Explicit out-of-bounds, removed hard workload and colliding whole banks.
 rejected=0
 for level,template,p,profile in [('hard','affine-pair',[1,1,3,2,1,4],'blank'),('hard','affine-pair',[2,2,4,2,2,4],'blank'),('moderate','q-288583',[7,0,14,-1,1,4],'blank'),('easy','q-288622',[1,2,4,2,0,4],'method-sum')]:
  try:g.generate(level,template=template,parameters=p,profile=profile,field_type='blank' if profile=='blank' else 'radio')
  except ValueError:rejected+=1
  else:raise AssertionError('invalid explicit object was accepted')
 # Bank/layout differences change presentation ID while retaining task identity.
 p={'a':'2','b':'3','c':'8','d':'-3','e':'2','f':'-5'}
 a=g.generate_hard(template='affine-pair',parameters=p,field_type='radio',profile='method-sum');b=g.generate_hard(template='affine-pair',parameters=p,field_type='blank',profile='blank');audit(a);audit(b)
 assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id']
 save('source-cases.json',cases);save('source-replay.json',fidelity);save('review.json',review);save('engine-input.json',engine);save('normal-samples.json',normal)
 binary=ROOT/'generate/runs/current/check-engine';subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'native-grading.json')],check=True)
 report={'status':'passed private validation; awaiting independent parent QA','basis':source['basis'],'lineage':source['lineage'],'source_questions':7,'raw_prompt_exact':7,'raw_full_solution_exact':5,'raw_solution_omissions_exact':2,'complete_populated_banks_matched':6,'complete_populated_banks_available':6,'source_radio_banks_matched':4,'source_blank_answer_fragments_matched':2,'source_empty_bank_omissions_exact':1,'source_field_layouts_matched':7,'source_choice_values_matched':sum(r['choices_matched'] for r in fidelity),'source_correct_designations_matched':5,'source_correct_designations_missing':2,'authored_missing_level':'hard','normal_counts':counts,'native_report':'native-grading.json','native_binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'invalid_explicit_objects_rejected':rejected,'radio_positions':sorted(positions),'source_byte_audit':byte_audit,'limitations':['Scalar observed wrong-operation intent is underdetermined; raw complete profiles are explicit and ineligible for normal practice.','Two unrated questions have missing solutions/designations; normal answers and levels are authored completions, never counted as observed matches.','No observed hard difficulty; hard scope is an authored design claim.']}
 save('validation.json',report)
 md=['# Review — KP 17592186110721','Captured math basis 1356. Observed records and authored variants are labeled separately.']
 for item in review:
  md+=['## '+item['label']]
  if 'original' in item:
   md+=['### Original',item['original'][':question/problem'],item['original'].get(':question/worked-solution','[Captured source omits solution.]'),'Original bank: '+', '.join(a[':answer/value'] for f in item['original'][':question/answer-fields'] for a in f.get(':answer-field/choices',[]))]
  md+=['### Generated',g.markdown(item['record'])]
 (HERE/'review.md').write_text('\n\n'.join(md)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
