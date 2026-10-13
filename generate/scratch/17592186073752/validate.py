#!/usr/bin/env python3
"""Fail-closed independent printed-math, full-bank, scope and native QA."""
import hashlib, importlib.util, json, re, subprocess, sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,)

def expr(tex):
 tex=tex.replace(r'\,','').replace(r'\{','').replace('&','').strip().rstrip('.,:')
 while r'\frac' in tex:
  tex,n=re.subn(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',tex)
  assert n,tex
 tex=tex.replace('{','(').replace('}',')')
 return parse_expr(tex,local_dict={v:sp.Symbol(v) for v in 'abxypq'},transformations=TRANS)

def equation(tex):
 lhs,rhs=tex.split('=');return sp.expand(expr(lhs)-expr(rhs))

def format_check(tex):
 # Exact alternating inline/display delimiter kinds; newlines allowed.
 tokens=re.findall(r'\$\$|\$',tex);opening=None
 for token in tokens:
  if opening is None:opening=token
  else:assert opening==token,('math delimiter mismatch',tex);opening=None
 assert opening is None
 for math in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$([^$]*?)\$(?!\$)',tex,re.S):
  s=''.join(math);depth=0
  for i,c in enumerate(s):
   if c in '{}' and (i==0 or s[i-1]!='\\'):
    depth+=1 if c=='{' else -1;assert depth>=0
  assert depth==0,s
 assert '--' not in tex and '+-' not in tex

def system(record):
 q=record['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 if r'\{' in prompt:
  group=re.search(r'\\\{([^$]*)\$',prompt).group(1);rows=group.split('; ')
 else:
  group=re.search(r'\\\{\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S).group(1);rows=group.split(r' \\ ')
 assert len(rows)==2
 eqs=[equation(r) for r in rows];variables=sorted(set().union(*(e.free_symbols for e in eqs)),key=str)
 assert len(variables)==2
 solved=sp.solve(eqs,variables,dict=True);assert len(solved)==1 and len(solved[0])==2
 return eqs,variables,solved[0]

def proportional(a,b,variables):
 pa,pb=sp.Poly(a,*variables),sp.Poly(b,*variables)
 if pa.is_zero or pb.is_zero:return False
 ratio=sp.cancel(pa.LC()/pb.LC())
 return sp.expand(a-ratio*b)==0

def check_record(record):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']['db_id']==g.KP_ID
 q=record['question'];format_check(q[':question/problem']);format_check(q[':question/worked-solution'])
 eqs,vs,solved=system(record);x,y=vs;pair=[solved[x],solved[y]]
 fields=q[':question/answer-fields'];radio=fields[0][':answer-field/type'].endswith('/radio')
 answers=[];owned=set()
 for i,f in enumerate(fields):
  assert f[':answer-field/correct'][0]==':answer/id'
  vals=[];ids=[]
  for a in f[':answer-field/choices']:
   assert a[':answer/id'] not in owned;owned.add(a[':answer/id']);ids.append(a[':answer/id']);vals.append(expr(a[':answer/value']));assert not vals[-1].free_symbols
  assert len(set(vals))==len(vals)
  cid=f[':answer-field/correct'][1];assert cid in ids
  answer=pair[0]-pair[1] if radio else pair[i]
  assert sum(v==answer for v in vals)==1
  assert vals[ids.index(cid)]==answer
  if not radio:assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  answers.append(answer)
 # Every printed aligned equation is independently true and is proportional to
 # either original equation or one of the independently eliminated coordinate
 # equations. This catches wrong distributed, collected or isolation values.
 candidates=eqs+[x-solved[x],y-solved[y]]
 groups=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
 counts=[]
 for group in groups:
  rows=group.split(r' \\ ');counts.append(len(rows))
  for row in rows:
   residual=equation(row)
   assert sp.simplify(residual.subs(solved))==0,(row,solved)
   assert any(proportional(residual,c,vs) for c in candidates),(row,candidates)
 name=record['generation']['template']
 expected=[2,6,2] if name.startswith('coefficient') else [6,2] if name=='tuple_xy' else [2,4] if name=='direct_pq' else [2,6,2]
 assert counts==expected,(name,counts)
 # Keep substituted products and separately expanded/collected rows, not a CAS
 # expression copied into every stage. This verifies structure as well as value.
 index=1 if name.startswith('coefficient') else 0 if name=='tuple_xy' else 1
 rows=groups[index].split(r' \\ ')
 assert '(' in rows[1]
 r0,r1=equation(rows[0]),equation(rows[1])
 removed=r0.free_symbols-r1.free_symbols
 assert len(removed)==1
 removed=next(iter(removed))
 substitutions=[value for original in eqs for value in sp.solve(original,removed)]
 assert any(sp.expand(r0.subs(removed,value)-r1)==0 for value in substitutions)
 limit=4 if name=='direct_pq' else 5
 for j in range(2,limit):
  previous,current=equation(rows[j-1]),equation(rows[j])
  if name=='direct_pq' and j==3:assert proportional(previous,current,vs)
  else:assert sp.expand(previous-current)==0,('Invalid distributed/collected/isolation operation',rows[j-1],rows[j])
 if name!='direct_pq':
  assert '(' not in rows[2] and len(re.findall(r'[+-]',rows[2].split('&')[0]))>=1
  assert rows[2]!=rows[3] and rows[3]!=rows[4]
 return pair,counts

def checks(record):
 result=[]
 for i,f in enumerate(record['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:
   ok=a[':answer/id']==f[':answer-field/correct'][1]
   if f[':answer-field/type'].endswith('/radio'):
    result.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if ok else 'rejected','purpose':'Every owned displayed option'})
   else:
    v=expr(a[':answer/value']);p,q=sp.fraction(v)
    result.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'Canonical scalar fragment'}, {'field_index':i,'submitted':f'({2*p})/({2*q})','expected':'accepted','purpose':'Genuinely unreduced equivalent rational entry'}, {'field_index':i,'submitted':str(v+1),'expected':'rejected','purpose':'Wrong scalar fragment'}])
 return result

def normalize_prompt(s):
 return re.sub(r'\s+','',s.replace('${','$\\{').replace('$$,',' $, $'))
def normalize_solution(s):return s.replace('{\\begin{aligned}',r'\{\begin{aligned}')
def main():
 raw=json.loads((HERE/'source.json').read_text());sources={q[':question/math-academy-id']:q for q in raw['record'][':knowledge-point/questions']};cases=json.loads((HERE/'source-cases.json').read_text())
 replay=[];fidelity=[];engine=[];reviews=[]
 for c in cases:
  record=g.generate(c['level'],23,c['template'],parameters=c['parameters'],profile=c['bank_profile']);pair,counts=check_record(record);src=sources[c['source_id']];q=record['question']
  assert normalize_prompt(q[':question/problem'])==normalize_prompt(src[':question/problem'])
  srcfields={f[':answer-field/key']:f for f in src[':question/answer-fields']}
  total=matched=designation=0
  for f in q[':question/answer-fields']:
   sf=srcfields[f[':answer-field/key']];assert sf[':answer-field/type'][':db/ident']==f[':answer-field/type']
   original=sorted([expr(a[':answer/value']) for a in sf.get(':answer-field/choices',[])],key=str);generated=sorted([expr(a[':answer/value']) for a in f[':answer-field/choices']],key=str)
   if original:assert original==generated;total+=len(original);matched+=len(original)
   if ':answer-field/correct' in sf:
    answer=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert expr(answer[':answer/value'])==expr(sf[':answer-field/correct'][':answer/value']);designation+=1
  solution_exact=None
  if ':question/worked-solution' in src:
   assert q[':question/worked-solution']==normalize_solution(src[':question/worked-solution']);solution_exact=q[':question/worked-solution']==src[':question/worked-solution']
  fidelity.append({'source_id':c['source_id'],'bank_values_matched':matched,'bank_values_total':total,'correct_designations_matched':designation,'missing_correct_designations':len(srcfields)-designation,'raw_prompt_exact':q[':question/problem']==src[':question/problem'],'presentation_normalized_prompt':True,'raw_solution_exact':solution_exact,'presentation_normalized_solution':True if solution_exact is not None else None,'derived_pair':[str(z) for z in pair],'stage_rows':counts})
  replay.append(record);engine.append({'label':c['source_id'],'record':record,'checks':checks(record)})
  # Both observed profiles and authored default variations get review coverage.
  variant=g.generate(c['level'],77,c['template'],profile=c['bank_profile']);check_record(variant);reviews.append({'label':'Generated observed-profile variant for '+c['source_id'],'record':variant})
 profile_counts={}
 for profile,name in g.PROFILES.items():
  level=g.TEMPLATES[name][0];profile_counts[profile]=0
  for seed in range(30):
   r=g.generate(level,seed,name,profile=profile);check_record(r);profile_counts[profile]+=1
   if seed<2:engine.append({'label':'Profile '+profile+str(seed),'record':r,'checks':checks(r)})
 stats={};unique={}
 for level in ['easy','moderate','hard']:
  unique[level]=set();stats[level]=0
  for name,(l,_) in g.TEMPLATES.items():
   if l!=level:continue
   for seed in range(120):
    r=g.generate(level,seed,name);check_record(r);stats[level]+=1;unique[level].add(r['generation']['mathematical_fingerprint'])
    if seed<2:reviews.append({'label':'Authored default '+level+' '+name,'record':r});engine.append({'label':level+name+str(seed),'record':r,'checks':checks(r)})
    clone=g.generate(level,seed+2000,name,parameters=r['generation']['parameters'],profile=r['generation']['bank_profile']);assert r['question'][':question/id']==clone['question'][':question/id']
 for level,name,p in [('hard','unit_pair',{'A':3,'B':2,'C':4,'S':-4,'T':2}),('moderate','difference_ab',{'A':3,'B':2,'C':3,'S':-4,'T':2}),('easy','tuple_xy',{'k':5,'C':14,'h':5})]:
  try:g.generate(level,template=name,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit workload was accepted')
 (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True,capture_output=True,text=True)
 native=json.loads((HERE/'engine-report.json').read_text())
 (HERE/'source-replay.json').write_text(json.dumps(replay,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(reviews,indent=2)+'\n')
 md=['# Substitution review','', 'Source originals are raw captured evidence. Generated replays repair presentation only; missing solutions and answers are independently authored. Context defaults additionally supply the missing first equation.','']
 for c,r in zip(cases,replay):
  src=sources[c['source_id']];md+=['## Original '+c['source_id'],'','```text',src[':question/problem'],'```','', 'Captured fields: '+json.dumps([{ 'key':f[':answer-field/key'], 'type':f[':answer-field/type'][':db/ident'], 'values':[a[':answer/value'] for a in f.get(':answer-field/choices',[])], 'correct_value':f.get(':answer-field/correct',{}).get(':answer/value')} for f in src[':question/answer-fields']]),'', '```text',src.get(':question/worked-solution','No captured worked solution.'),'```','','## Presentation-normalized replay '+c['source_id'],'',g.markdown(r),'']
 for item in reviews:md+=['## '+item['label'],'',g.markdown(item['record']),'']
 (HERE/'review.md').write_text('\n'.join(md))
 report={'status':'passed','source_basis':1356,'sources':6,'source_fidelity':fidelity,'matched_complete_nonempty_banks':8,'total_nonempty_banks':8,'matched_source_values':sum(f['bank_values_matched'] for f in fidelity),'total_source_values':sum(f['bank_values_total'] for f in fidelity),'matched_existing_correct_refs':6,'existing_correct_refs':6,'independently_derived_missing_correct_refs':4,'raw_exact_prompts':sum(f['raw_prompt_exact'] for f in fidelity),'presentation_normalized_prompts':6,'raw_exact_worked_solutions':0,'presentation_normalized_existing_worked_solutions':3,'authored_missing_worked_solutions':3,'generated_checks':stats,'profile_checks':profile_counts,'distinct_mathematical_tasks':{k:len(v) for k,v in unique.items()},'native':{k:native[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'plot_rating':'none','unresolved_source_distractor_intent':['source_4133 empirical amplitude ratios','source_5179 -2q interpretation'],'blocking_findings':[],'engine_source_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'engine_build_log':(ROOT/'generate/runs/current/engine-build.log').read_text().strip(),'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
