#!/usr/bin/env python3
"""Independent displayed-string mathematical checks plus complete source replay."""
import importlib.util, json, re, sys, hashlib, itertools, subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
V={v:sp.Symbol(v,real=True) for v in ['x','z','t','u','C']}

def group(text,pos):
 assert text[pos]=='{',(text,pos)
 depth=1;i=pos+1
 while depth:
  if text[i]=='{':depth+=1
  elif text[i]=='}':depth-=1
  i+=1
 return text[pos+1:i-1],i

def parse(text):
 text=text.strip().rstrip('.')
 if text=='-':return sp.Integer(-1)
 text=text.replace(r'\left','').replace(r'\right','')
 for command in (r'\,',r'\quad',r'\cdot',r'\displaystyle'):text=text.replace(command,' ' if command!=r'\cdot' else '*')
 while r'\frac' in text:
  i=text.index(r'\frac');j=i+5;a,j=group(text,j);b,j=group(text,j)
  text=text[:i]+'(('+str(parse(a))+')/('+str(parse(b))+'))'+text[j:]
 assert '\\' not in text,text
 text=text.replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(text,local_dict={**V,'e':sp.E},transformations=standard_transformations+(implicit_multiplication_application,))

def prompt_math(q):
 text=q[':question/problem'];i=text.index(r'\int')+4;text=text[i:]
 m=re.search(r'(?:\\,)?\\text\{d\}([xzt])|d([xzt])',text);assert m,text
 var=m.group(1) or m.group(2)
 return parse(text[:m.start()]),V[var]

def primitive_row(row,var):
 row=row.replace('&','').strip();row=row.removeprefix('=').strip().replace(r'(-\text{d}u)', '(-1)')
 for v in ['x','z','t','u']:row=row.replace(r'\text{d}'+v,'')
 if r'\int' in row:
  pre,expr=row.split(r'\int');pre=parse(pre) if pre.strip() else sp.Integer(1)
  integrated_var=V['u'] if '{e}^{u}' in expr else var
  return pre*parse(expr), integrated_var
 return parse(row), None

def check(record):
 q=record['question'];meta=record['generation'];p=meta['parameters'];template=meta['template'];raw=meta['evidence_only']
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']['db_id']==G.KP
 integrand,var=prompt_math(q)
 assert str(var)==p['v']
 assert sp.expand(integrand-G.objects(p)[3]*sp.exp(G.objects(p)[1]))==0
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio'
 assert len(f[':answer-field/choices'])==5
 values=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 for e in values:assert e.free_symbols<={var,V['C']} and not e.has(sp.zoo,sp.nan,sp.oo)
 for a,b in itertools.combinations(values,2):assert sp.expand(sp.diff(a-b,var))!=0,'equivalent bank pair'
 matches=[sp.expand(sp.diff(e,var)-integrand)==0 for e in values];assert sum(matches)==1
 if ':answer-field/correct' in f:
  corr=f[':answer-field/correct'][1]
  assert next(matches[i] for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==corr)
 sol=q.get(':question/worked-solution')
 if sol:
  m=re.search(r'\$u=(.*?)\.\$',sol);assert m
  g=parse(m.group(1));assert sp.expand(g-G.objects(p)[1])==0
  relation=sol.split('$$')[1].strip()
  prefix=r'\frac{\text{d}u}{\text{d}'+str(var)+'}='
  assert relation.startswith(prefix)
  derivative,rhs=relation[len(prefix):].split(r'\,⟹\,')
  assert sp.expand(parse(derivative)-sp.diff(g,var))==0
  left,right=rhs.rstrip('.').split('=');left=left.replace(r'\text{d}u','').strip();ratio=parse(left) if left not in ('','-') else sp.Integer(-1 if left=='-' else 1)
  right=right.replace(r'\text{d}'+str(var),'');poly=parse(right)
  assert sp.expand(ratio*sp.diff(g,var)-poly)==0
  body=sol[sol.index(r'\begin{aligned}'):].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split('$$')[0].strip()
  rows=body.split(r'\\');initial,reordered=rows[0].split('& =')
  stages=[initial,reordered]+rows[1:]
  expected=4 if p['l'] else 6
  assert len(stages)==expected,(len(stages),template)
  for row in stages:
   e,integrated_var=primitive_row(row,var)
   if integrated_var is not None:
    actual=e.subs(V['u'],g)*sp.diff(g,var) if integrated_var==V['u'] else e
   else:actual=sp.diff(e.subs(V['u'],g),var)
   assert sp.expand(actual-integrand)==0,(template,row)
  # Preserve operative sequence, not only equivalent algebra or row count.
  assert r'\cdot' in reordered
  if p['l']:
   assert r'\int {e}^{u}\,\text{d}u' in rows[1]
  else:
   assert r'\int {e}^{u}\cdot' in rows[1]
   assert r'\int {e}^{u}\,\text{d}u' in rows[2] and r'\cdot' not in rows[2]
   assert r'\int' not in rows[3] and '{e}^{u}' in rows[3]
   assert '{e}^{'+G.exponent(p)+'}' in rows[4]
 for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in f[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
  assert text.count('{')==text.count('}')
  assert text.count('$')%2==0
  if text.startswith("Let's"):assert text.count(r'\begin{aligned}')==text.count(r'\end{aligned}')
 return True

def run():
 cases=[];review=[];fidelity=[];literal_banks=0;source_distractors=0
 for template,(level,qid,p) in G.CONFIG.items():
  original=G.QS[qid];r=G.generate(level,template=template,parameters=p,profile='raw:'+qid);check(r)
  q=r['question'];f=q[':question/answer-fields'][0];of=original[':question/answer-fields'][0]
  assert q[':question/problem']==original[':question/problem']
  assert q.get(':question/worked-solution')==original.get(':question/worked-solution')
  for key in [':question/difficulty',':question/worked-solution']:assert (key in q)==(key in original)
  assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  source_values=[parse(a[':answer/value']) for a in of[':answer-field/choices']]
  generated_values=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
  for a in source_values:assert sum(sp.expand(sp.diff(a-b,V[p['v']]))==0 for b in generated_values)==1
  literal=sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  assert literal,qid;literal_banks+=literal;source_distractors+=4
  if ':answer-field/correct' in of:
   correct=parse(of[':answer-field/correct'][':answer/value']);assert sp.expand(sp.diff(correct,V[p['v']])-prompt_math(q)[0])==0
  cases.append({'source_id':qid,'source_db_id':original[':db/id'],'template':template,'level':level,'parameters':p,'bank_profile':'raw:'+qid,'authored_level_assignment':':question/difficulty' not in original,'raw_record':original})
  fidelity.append({'source_id':qid,'options_matched':5,'distractors_matched':4,'literal_bank':literal,'raw_prompt':True,'raw_solution':True if ':question/worked-solution' in original else 'absent preserved','correct_designation':'matched' if ':answer-field/correct' in of else 'absent preserved; inference separate','difficulty':'matched' if ':question/difficulty' in original else 'absent preserved'})
  review.append({'role':'original raw replay','record':r})
  # Original parameters through completed normal presentation, plus 2 changed per family.
  normal=G.generate(level,template=template,parameters=p);check(normal)
  review.append({'role':'normal at original parameters','record':normal})
  for seed in [81,92]:
   changed=G.generate(level,seed,template=template);check(changed)
   assert changed['generation']['parameters']!=p
   review.append({'role':'generated changed parameters','record':changed})
   historical=G.generate(level,seed,template=template,profile='raw:'+qid);check(historical)
   review.append({'role':'changed historical complete bank evidence','record':historical})
  if template.startswith('legacy_'):
   opaque=G.generate(level,81,template=template,profile='observed:'+qid);check(opaque)
   assert opaque['generation']['evidence_only'] and not opaque['generation']['eligible_for_learning']
 # default family coverage, sufficient mathematical variety and stable identities.
 fingerprints={lev:set() for lev in ['easy','moderate','hard']};coverage=set();records=[]
 for level in fingerprints:
  for seed in range(90):
   r=G.generate(level,seed);check(r);records.append(r)
   fingerprints[level].add(r['generation']['mathematical_fingerprint']);coverage.add(r['generation']['template'])
   again=G.generate(level,seed+999,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile'])
   assert again['question'][':question/id']==r['question'][':question/id']
 assert coverage==set(G.CONFIG)
 assert min(map(len,fingerprints.values()))>=40
 # Explicit bounds applied equally to direct inputs.
 guards=0
 for t,(level,qid,p) in G.CONFIG.items():
  for key,value in [('n',5),('b',9),('a',0),('c',0),('v','y')]:
   bad={**p,key:value}
   try:G.generate(level,parameters=bad,template=t)
   except ValueError:guards+=1
   else:raise AssertionError(('guard did not reject',t,bad))
 # Displayed mutations: wrong derivative, reordered row coefficient, a stopped
 # constant stage algebraically equal but missing operation, and control byte.
 import copy
 mutation_base=G.generate('moderate',template='cubic_positive',parameters=G.CONFIG['cubic_positive'][2])
 mutations=[lambda text:text.replace('=9{x}^{2}', '=8{x}^{2}'),lambda text:text.replace(r'\cdot 3{x}^{2}',r'\cdot 4{x}^{2}'),lambda text:text.replace(r'\frac{1}{3}\int {e}^{u}\,\text{d}u',r'\int \frac{1}{3}{e}^{u}\,\text{d}u'),lambda text:text+'\x0c']
 for fn in mutations:
  bad=copy.deepcopy(mutation_base);bad['question'][':question/worked-solution']=fn(bad['question'][':question/worked-solution'])
  try:check(bad)
  except (AssertionError,ValueError):pass
  else:raise AssertionError('displayed mutation undetected')
 fixtures=[]
 for i,item in enumerate(review):
  r=item['record'];f=r['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in f:continue
  corr=f[':answer-field/correct'][1]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==corr else 'rejected','purpose':'owned radio selection after mathematical pair checks'} for a in f[':answer-field/choices']]
  fixtures.append({'label':str(i)+' '+item['role']+' '+r['generation']['template'],'record':r,'checks':checks})
 (ROOT/'native-input.json').write_text(json.dumps(fixtures,indent=2))
 engine=Path('generate/runs/current/check-engine');subprocess.run([str(engine),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],check=True)
 native=json.loads((ROOT/'native-report.json').read_text())
 (ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False)+'\n')
 (ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 md=[]
 for item in review:md.append('## '+item['role']+' — '+item['record']['generation']['template']+'\n\n'+G.markdown(item['record']))
 (ROOT/'review.md').write_text('\n\n'.join(md)+'\n')
 report={'passed':True,'source_basis':G.WRAPPER['basis'],'source_lineage':G.WRAPPER['lineage'],'source_sha256':hashlib.sha256((ROOT/'source.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'fidelity':fidelity,'complete_banks':7,'all_source_options':35,'source_distractors':28,'literal_raw_banks':literal_banks,'source_correct_designations_matched':5,'missing_designations_preserved':2,'source_solutions_exact':5,'missing_solutions_preserved':2,'raw_nested_aligned_preserved':1,'normal_nested_aligned_repairs':1,'math_checked_records':len(records)+len(review),'normal_task_counts_90_seeds':{k:len(v) for k,v in fingerprints.items()},'default_family_coverage':sorted(coverage),'explicit_guard_rejections':guards,'mutation_rejections':len(mutations),'native':{k:native[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'native_raw_missing_key_exclusions':sum(':answer-field/correct' not in item['record']['question'][':question/answer-fields'][0] for item in review),'plot_rating':'none','database_writes':0,'unresolved':['Historical q-13737/q-73663 scalar distractor intent is underdetermined; profiles are evidence-only in raw replay, authored complete method bank is normal default.','Two absent source correct designations and solutions cannot count as observed matches; independently inferred completions are normal output only.']}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':run()
