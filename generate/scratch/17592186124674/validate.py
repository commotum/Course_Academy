#!/usr/bin/env python3
"""Independent checks read ACTUAL printed prompt/options/stages, then native radio grading."""
import hashlib, importlib.util, json, re, subprocess, sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
BASE=Path(__file__).resolve().parent;SCRIPT=BASE.with_suffix('.py');ROOT=BASE.parents[2]
spec=importlib.util.spec_from_file_location('growth_model',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
S=sp.Symbol('S');k,a=sp.symbols('k a');TRANS=standard_transformations+(implicit_multiplication_application,)

def math_rhs(tex,symbol):
 tex=tex.strip().rstrip('.,')
 while '\\frac' in tex:
  new=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',tex)
  assert new!=tex,('unsupported printed fraction',tex)
  tex=new
 tex=tex.replace('{'+symbol+'}',symbol).replace('{','(').replace('}',')').replace('^','**')
 tex=tex.replace(symbol,'S')
 # Protect structural independent/dependent variable agreement before normalization.
 assert set(re.findall(r'[A-Za-z]',tex)) <= {'S','k','a'},('wrong displayed variable',tex)
 return sp.expand(parse_expr(tex,local_dict={'S':S,'k':k,'a':a},transformations=TRANS))

def eq(tex,symbol):
 left,right=tex.split('=',1)
 left=left.replace(r'\text{d}','d').replace(r'\textrm d ','d').replace(' ','')
 assert left in (r'\frac{d'+symbol+r'}{dt}',r'\dfrac{d'+symbol+r'}{dt}'),('wrong differential variable',left,symbol)
 return math_rhs(right,symbol)

def formatting(text):
 assert text.count('$')%2==0,('unbalanced math delimiters',text)
 depth=0
 for i,c in enumerate(text):
  if c in '{}':
   if i and text[i-1]=='\\':continue
   depth+=1 if c=='{' else -1
   assert depth>=0,('unbalanced TeX group',text)
 assert depth==0,('unbalanced TeX group',text)
 assert '<<' not in text and '{{' not in text
 assert '--' not in text and '+-' not in text

def printed_check(rec):
 q=rec['question'];p=q[':question/problem'];f=q[':question/answer-fields'][0]
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 assert rec['knowledge_point']['db_id']==g.KP_ID
 symbol=re.search(r'\$([A-Z])\(t\)\$',p).group(1)
 match=re.search(r'(?:maximum.+?is|maximum capacity is) \$(\d+)\$',p)
 assert match,('capacity missing in actual prompt',p)
 A=int(match.group(1));rate_match=re.search(r'rate of increase equals \$(.+?)\$ times',p)
 rate=math_rhs(rate_match.group(1),symbol) if rate_match else k
 expected=sp.expand(rate*(A-S))
 values=[eq(c[':answer/value'],symbol) for c in f[':answer-field/choices']]
 assert len(values)==5
 assert all(sp.simplify(x-y)!=0 for i,x in enumerate(values) for y in values[i+1:]),'ambiguous complete equation bank'
 good=[i for i,x in enumerate(values) if sp.simplify(x-expected)==0];assert len(good)==1
 if ':answer-field/correct' in f:
  correct=f[':answer-field/correct'][1];assert f[':answer-field/choices'][good[0]][':answer/id']==correct
 assert len({c[':answer/id'] for c in f[':answer-field/choices']})==5
 formatting(p)
 for c in f[':answer-field/choices']:formatting(c[':answer/value'])
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];formatting(sol)
  blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==2,'source formal/substitution stages required'
  assert sp.simplify(eq(blocks[0],symbol)-k*(a-S))==0
  assert sp.simplify(eq(blocks[1],symbol)-expected)==0
  assert re.search(r'\$a\s*=\s*'+str(A)+r'(?:\D|$)',sol),'actual numeric capacity assignment must match printed prompt'
  if rate_match:
   rmatch=re.search(r'\$k=(.+?)\$',sol);assert rmatch and math_rhs(rmatch.group(1),symbol)==rate
  assert not any(x in sol for x in ('\\int','e^{-','\\ln','log(','separat')),'modeling-only scope'
  assert sol.index(blocks[0])<sol.index(blocks[1])
 h=g.digest({'version':g.VERSION,'prompt':p,'solution':q.get(':question/worked-solution'),'bank':sorted(c[':answer/value'] for c in f[':answer-field/choices']),'correct':f[':answer-field/choices'][good[0]][':answer/value'] if ':answer-field/correct' in f else None,'difficulty':q.get(':question/difficulty','').split('/')[-1] or None})
 assert h==rec['generation']['content_sha256']
 return good[0]

source=json.loads((BASE/'source.json').read_text());originals={q[':db/id']:q for q in source['record'][':knowledge-point/questions']};cases=json.loads((BASE/'source-cases.json').read_text())
assert len(cases)==len(originals)==11
records=[];review=[];report=[];count={'banks':0,'options':0,'distractors':0,'correct_designations':0,'prompt_exact':0,'solution_exact':0,'solution_absent_parity':0,'missing_designations_preserved':0,'difficulty_presence_parity':0}
for case in cases:
 rec=g.generate(case['level'],seed=7,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=rec['question'];o=originals[case['source_db_id']];of=o[':question/answer-fields'][0];gf=q[':question/answer-fields'][0]
 assert q[':question/problem']==o[':question/problem'];count['prompt_exact']+=1
 assert (':question/difficulty' in q)==(':question/difficulty' in o);count['difficulty_presence_parity']+=1
 if ':question/difficulty' in o:assert q[':question/difficulty']==o[':question/difficulty'][':db/ident']
 assert (':question/worked-solution' in q)==(':question/worked-solution' in o)
 if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];count['solution_exact']+=1
 else:count['solution_absent_parity']+=1
 assert gf[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert gf[':answer-field/key']==of[':answer-field/key']
 assert sorted(c[':answer/value'] for c in gf[':answer-field/choices'])==sorted(c[':answer/value'] for c in of[':answer-field/choices'])
 assert (':answer-field/correct' in gf)==(':answer-field/correct' in of)
 good=printed_check(rec)
 if ':answer-field/correct' in of:
  assert gf[':answer-field/choices'][good][':answer/value']==of[':answer-field/correct'][':answer/value'];count['correct_designations']+=1;records.append(rec)
 else:count['missing_designations_preserved']+=1
 count['banks']+=1;count['options']+=5;count['distractors']+=4
 report.append({'source_id':case['source_id'],'bank':'exact 5/5','prompt':'exact','solution':'exact' if ':question/worked-solution' in o else 'absent preserved','correct':'exact' if ':answer-field/correct' in of else 'absent preserved; independently inferred only in repaired profile'})
 review.append({'label':'ORIGINAL PARAMETERIZED RAW REPLAY '+case['source_id'],'record':rec})
 # Change all meaningful mathematical inputs through normal API, not copy replay.
 params={k:v*2 for k,v in case['parameters'].items()};changed=g.generate('easy',seed=13,template=case['template'],parameters=params,profile=case['bank_profile']);printed_check(changed);review.append({'label':'GENERATED OBSERVED BANK VARIANT '+case['source_id'],'record':changed})
 repaired=g.generate('easy',seed=9,template=case['template'],parameters=case['parameters'],profile=case['bank_profile'].replace('observed_','repaired_'));printed_check(repaired);records.append(repaired)
 review.append({'label':'GENERATED SUPPORTED PRESENTATION/FIELD COMPLETION '+case['source_id'],'record':repaired})
 changed_completed=g.generate('easy',seed=13,template=case['template'],parameters=params,profile=case['bank_profile'].replace('observed_','repaired_'));printed_check(changed_completed);records.append(changed_completed)
# Large bounded normal sample, workload and meaningful bank checks.
normal=[]
for level in ('easy','moderate','hard'):
 for seed in range(150):
  rec=g.generate(level,seed);printed_check(rec);normal.append(rec)
  if seed<3:review.append({'label':'GENERATED AUTHORED '+level.upper()+f' seed={seed}','record':rec});records.append(rec)
  again=g.generate(level,seed+1000,template=rec['generation']['template'],profile=rec['generation']['profile'],parameters=rec['generation']['parameters']);printed_check(again)
  assert again['question'][':question/id']==rec['question'][':question/id'],'seed must not affect content identity'
  assert again['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
# Exhaustive finite rate catalog and explicit workload boundaries.
boundary_count=0
for level,rates in [('moderate',tuple(sp.Integer(i) for i in range(2,7))),('hard',g.RATIONAL_CATALOG)]:
 for rate in rates:
  for capacity in (20,500):
   for initial in (1,capacity-1):
    p={'context':'deer','capacity':capacity,'initial':initial,'numerator':int(rate.p),'denominator':int(rate.q)}
    rec=g.generate(level,seed=97,parameters=p);printed_check(rec);boundary_count+=1
# Identity excludes noise but includes real changes, correct refs own answers.
for level in ('moderate','hard'):
 first=g.generate(level,42);p=first['generation']['parameters'].copy();p['initial']=1 if p['initial']!=1 else 2
 second=g.generate(level,42,parameters=p);assert first['generation']['mathematical_fingerprint']==second['generation']['mathematical_fingerprint'];assert first['question'][':question/id']!=second['question'][':question/id']
assert len({next(i for i,c in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if c[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in normal})>1
invalid=[('easy',{'context':'deer','capacity':0}),('moderate',{'context':'deer','capacity':100,'initial':5,'numerator':1,'denominator':1}),('moderate',{'context':'deer','capacity':100,'initial':5,'numerator':7,'denominator':1}),('hard',{'context':'deer','capacity':100,'initial':5,'numerator':2,'denominator':4}),('hard',{'context':'deer','capacity':100,'initial':5,'numerator':4,'denominator':3}),('hard',{'context':'deer','capacity':501,'initial':5,'numerator':1,'denominator':2}),('moderate',{'context':'deer','capacity':100,'initial':100,'numerator':2,'denominator':1})]
for level,p in invalid:
 try:g.generate(level,parameters=p)
 except ValueError:pass
 else:raise AssertionError(('invalid explicit parameters accepted',level,p))
# Native grade_field for every source's completed model plus every authored review.
engine_input=[]
for j,rec in enumerate(records):
 f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 engine_input.append({'label':f'growth_model_record_{j}','record':rec,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==correct else 'rejected','purpose':'complete radio bank selection'} for c in f[':answer-field/choices']]})
(BASE/'engine-input.json').write_text(json.dumps(engine_input,indent=2,ensure_ascii=False)+'\n')
engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(BASE/'engine-input.json'),str(BASE/'engine-report.json')],check=True)
engine_report=json.loads((BASE/'engine-report.json').read_text())
(BASE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
lines=['# Labeled original/generated review','', 'Raw absent difficulty, solution and designation remain absent. Repaired completion and authored levels are labeled separately.']
for item in review:
 lines+=['','## '+item['label']+' — '+item['record']['question'].get(':question/difficulty','unrated').split('/')[-1],'',g.markdown(item['record']),'','Metadata: `'+json.dumps(item['record']['generation'],ensure_ascii=False)+'`']
(BASE/'review.md').write_text('\n'.join(lines)+'\n')
summary={'status':'pass','source_provenance':{k:v for k,v in source.items() if k!='record'},'source_coverage':{**count,'captured_designated_distractors_matched':36,'inferred_undesignated_distractors_mathematically_checked':8},'source_comparisons':report,'normal_printed_math_records':len(normal),'changed_observed_profiles_checked':11,'explicit_catalog_boundary_records':boundary_count,'native_records':len(engine_input),'native_accepted':engine_report['accepted_checks'],'native_rejected':engine_report['rejected_checks'],'native_unresolved':engine_report['documented_unresolved_checks'],'invalid_explicit_cases_rejected':len(invalid),'authored_levels':['moderate','hard'],'known_limits':['Two raw sources lack correct refs/difficulty/solutions; inferred completions do not count as matched original designations.','Scalar-bank numerical recipes are explicit normalized capacity ratios with unknown historical intent, excluded from authored default sampling.','Factory raw source mixes capacity units and units/day; repaired profile consistently uses units.','Moderate and hard labels are authored coefficient-placement workload claims, not observed labels.'],'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'unresolved_failures':[]}
(BASE/'validation.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ('source_comparisons','known_limits')},indent=2))
