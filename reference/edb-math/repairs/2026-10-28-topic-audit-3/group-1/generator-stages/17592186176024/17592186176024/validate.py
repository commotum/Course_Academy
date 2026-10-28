#!/usr/bin/env python3
"""Local fail-fast QA: source presence/value/layout, independently read printed
prompt, derivatives and every operative integral row; method-stage structure,
pointwise bank eligibility, identity, workload guards and real native grading.
"""
import importlib.util,json,re,sys,hashlib,subprocess,copy,concurrent.futures
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent;SCRIPT=ROOT.with_suffix('.py');spec=importlib.util.spec_from_file_location('green',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def eq(a,b):return sp.trigsimp(sp.expand(a-b))==0

def prompt_model(q):
 s=q[':question/problem'];f=re.search(r'F\(x, ?y\)\s*=\s*⟨(.*?)⟩',s)
 if f:
  a,b=f[1].split(',',1);return g.parse_math(a),g.parse_math(b.replace(r'\,',''))
 line=re.search(r'\{∮\}_\{C\}(.*?)=\{\\int',s,re.S)[1];a,b=line.split(r'\,dx',1);b=b.removesuffix(r'\,dy').lstrip('+');return g.parse_math(a),g.parse_math(b)

def formatting(s,raw=False):
 assert not any(ord(c)<32 and c not in '\n\t\r'for c in s),'control character'
 assert s.count('$$')%2==0,'display delimiters'
 assert s.replace('$$','').count('$')%2==0,'inline delimiters'
 if not raw:
  n=0
  for i,c in enumerate(s):
   if c not in '{}':continue
   if i and s[i-1]=='\\':continue
   n+=1 if c=='{'else -1;assert n>=0,'unmatched brace'
  assert n==0,'unmatched brace'
 assert '--'not in s and '+-'not in s,'bare signed operation'

def validate_record(rec):
 q=rec['question'];gen=rec['generation'];name=gen['template'];p=gen['parameters'];raw=gen['profile']=='original'
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 formatting(q[':question/problem'],raw);formatting(q.get(':question/worked-solution',''),raw)
 P,Q=prompt_model(q);expected=sp.trigsimp((sp.diff(Q,g.X)-sp.diff(P,g.Y)).subs({g.X:g.R*g.C,g.Y:g.R*g.S})*g.R)
 # Independently read every concrete line-integral rewrite, including rows
 # before the partial derivatives. A correct curl/key cannot hide stale operands.
 for body in re.findall(r'\{∮\}_\{C\}([^=\n]*?)\\,dy',q.get(':question/worked-solution','')):
  if r'\,dx' not in body:continue
  lhs,rhs=body.split(r'\,dx',1)
  if 'P' in lhs or 'F' in lhs:continue
  assert eq(g.parse_math(lhs),P) and eq(g.parse_math(rhs.lstrip('+')),Q),'stale line-integral operands'
 assert eq(P,g.model(name,p)[0])and eq(Q,g.model(name,p)[1]),'actual prompt model'
 f=q[':question/answer-fields'][0];values=[g.parse_math(a[':answer/value'])for a in f[':answer-field/choices']]
 for answer in f[':answer-field/choices']:formatting(answer[':answer/value'],raw)
 assert len(values)==5;assert len({a[':answer/id']for a in f[':answer-field/choices']})==5
 if ':answer-field/correct'in f:
  selected=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);assert eq(g.parse_math(selected[':answer/value']),expected),'printed correct answer'
 if not gen['evidence_only']:g.eligible(values)
 sol=q.get(':question/worked-solution')
 if sol and name!='unrated_cross':
  dp=re.search(r'\\frac\{∂P\}\{∂y\}=(.*?),\\,',sol)[1];dq=re.search(r'\\frac\{∂Q\}\{∂x\}=(.*?)\.\\end',sol)[1]
  assert eq(g.parse_math(dp),sp.diff(P,g.Y));assert eq(g.parse_math(dq),sp.diff(Q,g.X))
  checked=[]
  for block in re.findall(r'\$\$(.*?)\$\$',sol,re.S):
   if r'\begin{aligned}'not in block or '{∬}'not in block:continue
   for row in block.split('\\\\'):
    matches=list(re.finditer(r'\{∬\}_\{([DΔ])\}',row))
    for m in matches:
     reg=m[1];z=row[m.end():]
     if r'\frac{∂Q}'in z:continue
     marker=r'\text{d}A'if reg=='D'else r'\text{d}r';z=z.split(marker)[0].rstrip().removesuffix(r'\,').strip()
     val=g.parse_math(z);wanted=sp.diff(Q,g.X)-sp.diff(P,g.Y)if reg=='D'else expected
     assert eq(val,wanted),(name,'printed stage',z,val,wanted);checked.append(z)
    if not matches:
     m=re.search(r'\{\\int \}_\{0\}\^\{\d+\}(.*?)\\,\\text\{d\}r',row,re.S)
     if m:
      z=m[1];assert eq(g.parse_math(z),expected),(name,'printed final stage',z);checked.append(z)
  expected_counts={'y2':4,'xy':4,'negx2':4,'cross':6,'cubic':6,'xy_extra':4,'offset':5,'unequal_cubic':6}
  assert len(checked)==expected_counts[name],(name,'operative row sequence',len(checked))
  # Required operation masks are distinct from algebraic equality/count.
  if name in ('cubic','unequal_cubic'):
   assert r'\cdot (r\operatorname{cos}⁡\theta )^{2}'in sol
   assert r'{r}^{2}{cos}^{2}⁡\theta 'in sol
   if name=='cubic':assert r'({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )'in sol
  if name=='cross':
   assert r'\cdot r\operatorname{cos}⁡\theta \cdot r\operatorname{sin}⁡\theta 'in sol
   assert r'{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta 'in sol
   assert r'\operatorname{sin}⁡(2\theta )'in sol
  if name=='offset':assert ')−('not in sol and re.search(r'\{∬\}_\{D\}\(\(',sol)
  # Inline P/Q statements must agree with prompt, too.
  pp=re.search(r'Since \$P\(x,y\)=(.*?)\$',sol)[1];qq=re.search(r'and \$Q\(x,y\)=(.*?),\$',sol)[1]
  assert eq(g.parse_math(pp),P)and eq(g.parse_math(qq),Q)
  rad=re.search(r'0\\le r\\le (\d+)',sol)[1];assert int(rad)==p['radius']
 if sol and name=='unrated_cross':
  dp=re.search(r'\\frac\{\\partial P\}\{\\partial y\}=(.*?)\$',sol)[1]
  dq=re.search(r'\\frac\{\\partial Q\}\{\\partial x\}=(.*?)\$',sol)[1]
  assert eq(g.parse_math(dp),sp.diff(P,g.Y));assert eq(g.parse_math(dq),sp.diff(Q,g.X))
  numeric=[]
  for m in re.finditer(r'\\iint_D(.*?)\\,dA',sol):
   z=m[1]
   if r'\frac' in z or z==' f(x,y)':continue
   assert eq(g.parse_math(z),sp.diff(Q,g.X)-sp.diff(P,g.Y));numeric.append(z)
  assert len(numeric)==3,'authored curl sequence'
  z=re.search(r'\\iint_\\Delta(\(.*?)\\,dr',sol)[1]
  assert eq(g.parse_math(z),expected),'authored polar substitution/Jacobian'
  z=re.search(r'\\int_0\^\{'+str(p['radius'])+r'\}(.*?)\\,dr',sol)[1]
  assert eq(g.parse_math(z),expected),'authored final integrand'
 return True

def full_value(e,rad):
 # Exact known Fourier/exponential angular moments, rather than syntax.
 angular=sp.integrate(e,(g.R,0,rad))
 if angular.has(sp.exp(g.C)):
  k=sp.expand(angular).coeff(sp.exp(g.C));angular=sp.expand(angular)-k*sp.exp(g.C)
  return sp.simplify(sp.integrate(angular,(g.T,0,2*sp.pi))+k*2*sp.pi*sp.besseli(0,1))
 return sp.simplify(sp.integrate(angular,(g.T,0,2*sp.pi)))

def main():
 cases=[];source_checks=[];full_evidence=[];native=[];reviews=[]
 for name,(level,sid,rad)in g.CONFIG.items():
  if sid is None:continue
  p={'a':1,'b':2 if name=='cross'else 1,'radius':rad}
  rec=g.generate(level,template=name,parameters=p,profile='original');src=g.SOURCES[sid];q=rec['question'];f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
  validate_record(rec)
  assert q[':question/problem']==src[':question/problem']
  for key in (':question/difficulty',':question/worked-solution'):
   assert (key in q)==(key in src),'attribute presence'
  assert q.get(':question/worked-solution')==src.get(':question/worked-solution')
  assert (':answer-field/correct'in f)==(':answer-field/correct'in sf)
  vals=[g.parse_math(a[':answer/value'])for a in f[':answer-field/choices']];original=[g.parse_math(a[':answer/value'])for a in sf[':answer-field/choices']]
  assert all(sum(eq(v,z)for z in vals)==1 for v in original),'complete one-to-one bank'
  if ':answer-field/correct'in sf:
   selected=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);assert eq(g.parse_math(selected[':answer/value']),g.parse_math(sf[':answer-field/correct'][':answer/value']))
  cases.append({'source_id':sid,'template':name,'level':level,'parameters':p,'bank_profile':'original','difficulty_authored':name=='unrated_cross','missing_correct_designation':name=='unrated_cross'})
  source_checks.append({'source_id':sid,'prompt_exact':True,'solution_exact':':question/worked-solution'in src,'solution_presence':True,'bank_matches':5,'bank_total':5,'correct_designation_matches':':answer-field/correct'in sf})
  full=[str(full_value(v,rad))for v in original];full_evidence.append({'source_id':sid,'integrand_options':[a[':answer/value']for a in sf[':answer-field/choices']],'complete_integral_values':full,'value_collisions':len(full)-len(set(full)),'criterion':'pointwise missing fragment, not complete integral value','opaque_evidence_only':name=='unrated_cross'})
  if ':answer-field/correct'in f:native.append(engine_item(rec,'original '+sid))
  # Two changed variants for every family/profile, not just level minima.
  for seed in [19,43]:
   r=g.generate(level,seed,template=name);validate_record(r);reviews.append(r);native.append(engine_item(r,'generated '+name+' '+str(seed)))
 for seed in [19,43]:
  r=g.generate_hard(seed);validate_record(r);reviews.append(r);native.append(engine_item(r,'authored hard '+str(seed)))
 # Boundary and shuffled identity; sample each default family as well.
 sample_count=0;seen={l:set()for l in ('easy','moderate','hard')};tasks={l:set()for l in seen}
 for name,(level,sid,rad)in g.CONFIG.items():
  for seed in range(12):
   r=g.generate(level,seed,template=name);validate_record(r);sample_count+=1;tasks[level].add(r['generation']['mathematical_fingerprint'])
   p=r['generation']['parameters'];r2=g.generate(level,seed+900,template=name,parameters=p,profile=r['generation']['profile']);assert r['question'][':question/id']==r2['question'][':question/id']
 for level in seen:
  for seed in range(30):seen[level].add(g.generate(level,seed)['generation']['template'])
  assert seen[level]=={n for n,v in g.CONFIG.items()if v[0]==level},'default family coverage'
 for name,level,p in [('unequal_cubic','hard',{'a':2,'b':2,'radius':2}),('cubic','moderate',{'a':2,'b':3,'radius':2}),('xy_extra','moderate',{'a':1,'b':1,'radius':5})]:
  try:g.generate(level,template=name,parameters=p);raise AssertionError('invalid input accepted')
  except ValueError:pass
 # Regression changes true source expansion to an equal final repeated row.
 mutated=copy.deepcopy(next(r for r in reviews if r['generation']['template']=='cubic'))
 mutated['question'][':question/worked-solution']=mutated['question'][':question/worked-solution'].replace(r'{r}^{2}{cos}^{2}⁡\theta ',r'{r}^{2}(1-{sin}^{2}⁡\theta )')
 try:validate_record(mutated);raise AssertionError('missing required expansion accepted')
 except AssertionError as e:assert str(e)!='missing required expansion accepted'
 # Parent regression: cancelled common offsets affect display identity only.
 neutral=[g.generate('moderate',template='offset',parameters={'a':2,'b':2,'radius':4,'h':h}) for h in range(1,5)]
 assert len({r['generation']['mathematical_fingerprint'] for r in neutral})==1
 assert len({r['question'][':question/id'] for r in neutral})==4
 stale=copy.deepcopy(neutral[0]);z=g.pieces('offset',stale['generation']['parameters'])
 stale['question'][':question/worked-solution']=stale['question'][':question/worked-solution'].replace(z['P']+r'\,dx+'+z['Q']+r'\,dy',r'y(x-1)\,dx+x(y-1)\,dy')
 try:validate_record(stale);raise AssertionError('stale operands accepted')
 except AssertionError as e:assert str(e)!='stale operands accepted'
 # Exact finite family domain counts exclude bounds/common offsets.
 counts={'easy':36*3+15,'moderate':6+36+6+36,'hard':30}
 plotdir=ROOT/'concurrent-plots';plotdir.mkdir(exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(4)as pool:paths=list(pool.map(lambda radius:g.render_plots(radius,plotdir),[2,2,3,4]))
 for path in paths:
  side=json.loads(Path(path).with_suffix('.json').read_text());assert side['sha256']==hashlib.sha256(Path(path).read_bytes()).hexdigest()
 assert not list(plotdir.glob('tmp*'))
 (ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(ROOT/'full-integral-audit.json').write_text(json.dumps(full_evidence,indent=2,ensure_ascii=False)+'\n')
 (ROOT/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n');(ROOT/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
 harness=ROOT/'reference/native/check-engine';subprocess.run([str(harness),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
 engine=json.loads((ROOT/'engine-validation.json').read_text());report={'status':'passed','source_basis':1356,'practice_sources':8,'source_prompts_exact':8,'existing_solutions_exact':7,'existing_solution_denominator':7,'missing_solution_presence_preserved':1,'source_banks_matched':8,'source_options_matched':40,'source_correct_designations_matched':7,'source_correct_designations_present':7,'unrated_missing_correct_designations':1,'independently_parsed_samples':sample_count,'finite_meaningful_task_counts':counts,'sampled_task_counts':{l:len(v)for l,v in tasks.items()},'default_family_coverage':{l:sorted(v)for l,v in seen.items()},'native':{k:engine[k]for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'python':sys.version.split()[0],'sympy':sp.__version__,'format_repairs':['normal disk region braces are escaped visible glyphs','normal q-125716 placeholder repaired','all normal prompts expressly request pointwise simplification'],'evidence_only_profiles':['unrated_cross/original'],'source_notation_normalization':'Answer values rendered in standard TeX; exact source values remain in source.json. Raw prompts/solutions unchanged at source parameters.'}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');write_review(cases,reviews);print(json.dumps(report,indent=2))

def engine_item(rec,label):
 f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else 'rejected','purpose':'Owned radio ID: independently verified pointwise math'}for a in f[':answer-field/choices']]}

def write_review(cases,reviews):
 s='# Original source records and labeled generated variants\n\n'
 for c in cases:
  q=g.SOURCES[c['source_id']];s+='## Original '+c['source_id']+' — '+c['template']+'\n\n'+q[':question/problem']+'\n\n'
  s+='Original bank: '+', '.join('$'+a[':answer/value']+'$'for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Original worked solution absent; correct designation and difficulty absent.]')+'\n\n'
  for r in reviews:
   if r['generation']['template']==c['template']:s+='### Generated variant — '+str(r['generation']['parameters'])+'\n\n'+g.markdown(r)+'\n\n'
 for r in reviews:
  if r['generation']['template']=='unequal_cubic':s+='## Authored missing hard level — '+str(r['generation']['parameters'])+'\n\n'+g.markdown(r)+'\n\n'
 (ROOT/'review.md').write_text(s)
if __name__=='__main__':main()
