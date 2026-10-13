#!/usr/bin/env python3
"""Independent displayed-math, complete-source, identity and native-grade QA."""
import copy, importlib.util, json, re, subprocess, sys, hashlib
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
g=load('generator_tangent',ROOT.with_suffix('.py'))
p=load('independent_tangent_math_parser',ROOT/'display-parser.py')
X,Y,T=p.x,p.y,p.t
MATH=re.compile(r'\$\$[\s\S]*?\$\$|\$[^$]*\$')
def blocks(text):return [m[0][2:-2] if m[0].startswith('$$') else m[0][1:-1] for m in MATH.finditer(text)]
def math(text):return p.scalar(text.strip().replace('&','').removesuffix(r'\,'))
def same(a,b):return s.simplify(s.trigsimp(a-b))==0
def pair(raw):
 raw=raw.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\,','');assert raw.startswith('(') and raw.endswith(')'),raw
 return tuple(math(z) for z in raw[1:-1].split(','))
def relation(raw):
 a,b=raw.strip().rstrip('.,').split('=');return s.expand(math(a)-math(b))
def line_eq(a,b):
 if s.Poly(a,X,Y,domain='EX').total_degree()!=1 or s.Poly(b,X,Y,domain='EX').total_degree()!=1:return False
 ca=[s.expand(a).coeff(X),s.expand(a).coeff(Y),s.expand(a).subs({X:0,Y:0})];cb=[s.expand(b).coeff(X),s.expand(b).coeff(Y),s.expand(b).subs({X:0,Y:0})]
 pivot=next(i for i,z in enumerate(cb) if z!=0)
 return ca[pivot]!=0 and same(a*cb[pivot],b*ca[pivot])
def read_prompt(prompt):
 components=blocks(prompt);raw=next(q for q in components if re.match(r'\s*x\s*=',q))
 raw=raw.replace(r'\qquad','').replace(r'\quad','').replace(r'\,','')
 match=re.match(r'\s*x\s*=(.*?),\s*y\s*=(.*?),',raw,re.S);assert match,raw
 xt,yt=map(math,match.groups());us=[math(q.split('=',1)[1].strip().rstrip('.,?')) for q in components if re.match(r't\s*=',q)]
 assert len(us)==1,(prompt,us)
 u=us[0];dx,dy=s.diff(xt,T),s.diff(yt,T);xp,yp=s.simplify(xt.subs(T,u)),s.simplify(yt.subs(T,u));dxp,dyp=s.simplify(dx.subs(T,u)),s.simplify(dy.subs(T,u));assert dxp!=0 and dyp!=0
 m=s.simplify(dyp/dxp);line=s.expand(Y-yp-m*(X-xp));yi=s.simplify(yp-m*xp);xi=s.simplify(xp-yp/m)
 return dict(xt=xt,yt=yt,u=u,dx=dx,dy=dy,xp=xp,yp=yp,dxp=dxp,dyp=dyp,m=m,line=line,yi=yi,xi=xi)

def signed_components(raw):
 raw=raw.strip().rstrip('.,').removesuffix(r'\,');depth=0;start=0;pieces=[]
 for i,ch in enumerate(raw):
  if ch in '({':depth+=1
  elif ch in ')}':depth-=1
  elif ch in '+-' and depth==0 and i>start:
   pieces.append(raw[start:i]);start=i
 pieces.append(raw[start:])
 return tuple(math(z) for z in pieces)

def formatting(text):
 assert text.count('$')%2==0,'Odd dollars'
 assert not re.search(r'\+\s*-|--|\\pit\b|\\picos\b',text),('Ambiguous signed factors/TeX command',text)
 # TeX groups, including aligned environments, balanced independently.
 assert text.count('{')==text.count('}'),text
 for b in blocks(text):assert b.count('{')==b.count('}'),b

def stage_check(record,z):
 q=record['question'];name=record['generation']['template'];solution=q.get(':question/worked-solution')
 if solution is None:return {'missing_source_solution':True}
 for target,claim in re.findall(r"point \$\((.*?)\)(\.?|,)\$",solution):
  target=target.split(')=(')[-1]
  assert all(same(a,b) for a,b in zip(pair('('+target+')'),(z['xp'],z['yp'])))
 for raw in re.findall(r'\$m=(.*?)\$',solution):assert same(math(raw),z['m']),raw
 for raw in re.findall(r'\$t\s*=(.*?)\$',solution):assert same(math(raw.strip().rstrip('.,')),z['u']),raw
 alignments=[b for b in blocks(solution) if r'\begin{aligned}' in b]
 expected_rows={'polynomial_radio':[2,2,3,1],'polynomial_blank':[2,2,5,3],'exponential_y_intercept':[2,3,3,1,2],'trig_x_intercept':[2,3,3,1,3],'log_y_intercept':[2,2,2,1,3],'linear_cubic':[2,1],'quintic_radio':[2,1]}
 actual_rows=[len(b.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\')) for b in alignments]
 assert actual_rows==expected_rows[name],('Structural chain',name,actual_rows)
 # Verify displayed coordinate derivatives against actual prompt.
 derivblocks=[b for b in blocks(solution) if ('{x}^{′}(t)=' in b or "x'(t)=" in b)]
 assert len(derivblocks)==1,(name,derivblocks)
 derivative=derivblocks[0]
 pieces=re.split(r',\\(?:,|qquad)\s*',derivative)
 assert len(pieces)==2,pieces
 for piece,var in zip(pieces,['x','y']):
  lhs,rhs=piece.split('=',1);assert var in lhs and '(t)' in lhs
  assert same(math(rhs),z['d'+var]),('Printed derivative',piece,z)
 ratio=z['dy']/z['dx'];checked=0
 for i,group in enumerate(alignments):
  body=group.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
  rows=body.split(r'\\')
  if i==0:
   for row,var in zip(rows,['x','y']):
    components=row.replace('&','').split('=');assert components[0].strip()==var
    reference_components=signed_components(components[1])
    for expr in components[1:]:
     assert same(math(expr),z['xp' if var=='x' else 'yp']),('Coordinate substitution/evaluation',expr,z)
     individual=signed_components(expr)
     if len(individual)==len(reference_components):assert all(same(a,b) for a,b in zip(individual,reference_components)),('Ordered coordinate components',expr,components[1])
   continue
  is_ratio=r'\frac{dy}{dx} &' in body
  is_slope=body.lstrip().startswith('m')
  if is_ratio:
   assert r'\frac{{y}^{′}(t)}{{x}^{′}(t)}' in rows[0],body
   for row in rows[1:]:
    for expr in row.replace('&','').split('=')[1:]:assert same(math(expr),ratio),('Symbolic derivative-ratio stage',expr,ratio)
   if name=='exponential_y_intercept':assert r'\frac{{e}^{t}(' in rows[1] and r'\frac{{e}^{t}(' not in rows[2],body
   if name=='trig_x_intercept':assert '('+r'\frac{1}' in rows[1],body
  elif is_slope:
   for row in rows:
    tail=row.split('&',1)[-1] if '&' in row else row
    for expr in tail.split('=')[1:]:
     if '|' in expr:continue
     assert same(math(expr),z['m']),('Slope substitution/evaluation',expr,z['m'])
  else:
   intercept='intercept' in name and i==len(alignments)-1
   target=(Y-z['yi']) if 'y_intercept' in name else (X-z['xi'])
   for row in rows:
    assert row.count('=')==1,row
    expr=relation(row.replace('&',''))
    assert line_eq(expr,target if intercept else z['line']),('Line/intercept rearrangement',row,target if intercept else z['line'])
  checked+=len(rows)
 # Easy/quintic ratio lives in an unaligned complete block.
 if name in ['linear_cubic','quintic_radio']:
  b=next(b for b in blocks(solution) if r"\frac{y'(t)}{x'(t)}" in b)
  assert same(math(b.split('=')[-1]),ratio),b
 # Concluding math must follow changed point/line/intersection.
 if name=='polynomial_blank':
  concluding=re.search(r'slope-intercept form is \$(.*?)\$',solution);assert concluding and line_eq(relation(concluding[1]),z['line'])
 if 'intercept' in name:
  ending=solution.split('Consequently,',1)[1];coords=next(b for b in blocks(ending) if b.startswith('('))
  vals=pair(coords);correct=(0,z['yi']) if 'y_intercept' in name else (z['xi'],0)
  assert len(vals)==2 and all(same(a,b) for a,b in zip(vals,correct)),('Conclusion',coords,correct)
 return {'rows':sum(actual_rows),'derivative_components':2,'verified_post_coordinate_rows':checked}

def verify_record(r):
 q=r['question'];gen=r['generation'];name=gen['template'];assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r==json.loads(json.dumps(r)), 'JSON-native full equality'
 z=read_prompt(q[':question/problem'])
 formatting(q[':question/problem']);formatting(q.get(':question/worked-solution',''))
 fields=q[':question/answer-fields'];flat=[]
 for f in fields:
  answers=f[':answer-field/choices'];owned={a[':answer/id'] for a in answers};assert len(owned)==len(answers)
  for a in answers:formatting(a[':answer/value'])
  if ':answer-field/correct' in f:assert f[':answer-field/correct'][0]==':answer/id' and f[':answer-field/correct'][1] in owned
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  for a in answers:
   value=a[':answer/value']
   if f[':answer-field/type'].endswith('/radio'):
    obj=pair(value) if value.startswith('(') else relation(value)
    correct=(0,z['yi']) if 'y_intercept' in name else (z['xi'],0) if 'x_intercept' in name else z['line']
    eq=(len(obj)==2 and all(same(u,v) for u,v in zip(obj,correct))) if isinstance(obj,tuple) else line_eq(obj,correct)
    flat.append(obj)
   else:
    obj=math(value);correct=(s.expand(z['m']*(X-z['xp'])+z['yp']) if name=='polynomial_blank' else z['yi'] if f[':answer-field/key']=='field-2' else s.Integer(0));eq=same(obj,correct)
   if ':answer-field/correct' in f:assert eq==(a[':answer/id']==f[':answer-field/correct'][1]),('Displayed option designation',value,obj,correct)
 for i,a in enumerate(flat):
  for b in flat[:i]:assert not (all(same(u,v) for u,v in zip(a,b)) if isinstance(a,tuple) else line_eq(a,b)),('Ambiguous bank',a,b)
 if not gen['evidence_only']:assert gen['eligible_for_learning'] and q[':question/difficulty']==':question.difficulty/'+g.TEMPLATES[name]
 stages=stage_check(r,z)
 return z,stages

def fidelity(r,c):
 original=g.QUESTIONS[c['source_id']];q=r['question']
 for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:
  assert (key in q)==(key in original),('Attribute presence',c['source_id'],key)
 if ':question/difficulty' in original:assert q[':question/difficulty']==original[':question/difficulty'][':db/ident']
 assert q[':question/problem']==original[':question/problem']
 assert q.get(':question/worked-solution')==original.get(':question/worked-solution')
 assert len(q[':question/answer-fields'])==len(original[':question/answer-fields'])
 matched=0;correct=0
 for f,source in zip(q[':question/answer-fields'],original[':question/answer-fields']):
  assert f[':answer-field/key']==source[':answer-field/key'] and f[':answer-field/type']==source[':answer-field/type'][':db/ident']
  assert (':answer-field/correct' in f)==(':answer-field/correct' in source)
  def parsed(value):return pair(value) if value.startswith('(') else relation(value) if '=' in value else math(value)
  def equivalent(a,b):return all(same(u,v) for u,v in zip(a,b)) if isinstance(a,tuple) else line_eq(a,b) if a.has(X,Y) and '=' in source[':answer-field/choices'][0][':answer/value'] else same(a,b)
  originals=list(source[':answer-field/choices'])
  for a in f[':answer-field/choices']:
   matches=[v for v in originals if equivalent(parsed(a[':answer/value']),parsed(v[':answer/value']))];assert len(matches)==1,(a,matches)
   source_answer=matches[0];originals.remove(source_answer);matched+=1
   assert a[':answer/type']==source_answer[':answer/type'][':db/ident']
   if ':answer-field/correct' in f:
    assert (a[':answer/id']==f[':answer-field/correct'][1])==(source_answer[':answer/id']==source[':answer-field/correct'][':answer/id'])
  assert not originals
  correct+=int(':answer-field/correct' in source)
 return matched,correct

def engine_item(label,r,z):
 checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  if ':answer-field/correct' not in f:return None # report missing captured designation; never fake a grading pass
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned choice; mathematical value separately read and validated'})
  else:
   val=f[':answer-field/choices'][0][':answer/value'];checks.append({'field_index':fi,'submitted':val,'expected':'accepted','purpose':'canonical source-shaped fragment'})
   if r['generation']['template']=='polynomial_blank':
    sub=lambda expression:g.tex(expression).replace('t','('+g.tex(z['u'])+')')
    alternate=g.frac(sub(z['dy']),sub(z['dx']))+'('+g.shift('x',z['xp'])+')'+g.plus(z['yp'])
   elif f[':answer-field/key']=='field-1':alternate='1-1'
   else:alternate=g.tex(z['yp'])+'-'+g.frac(str(r['generation']['parameters']['n']+r['generation']['parameters']['k']),str(r['generation']['parameters']['n']+r['generation']['parameters']['k']+1))
   assert same(math(alternate),math(val)),('Equivalent native fixture',alternate,val)
   expected='rejected' if 'round' in r['question'][':question/problem'].lower() else 'accepted'
   checks.append({'field_index':fi,'submitted':alternate,'expected':expected,'purpose':'algebraically equivalent point-slope/subtracted coordinate expression; raw round wording is form-sensitive'})
   checks.append({'field_index':fi,'submitted':'999','expected':'rejected','purpose':'incorrect fragment'})
 return {'label':label,'record':r,'checks':checks}

def main():
 raw_records=[];review=[];fixtures=[];matched=0;correct=0;stage_totals=0;families=set();counts={l:set() for l in ['easy','moderate','hard']}
 for c in g.CASES:
  r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);z,stages=verify_record(r);ma,co=fidelity(r,c);matched+=ma;correct+=co;raw_records.append(r);stage_totals+=stages.get('rows',0)
  item=engine_item('raw '+c['source_id'],r,z)
  if item:fixtures.append(item)
  # Native missing-key limitation gets its independently completed normal counterpart.
  normal=g.generate(c['level'],template=c['template'],parameters=c['parameters']);z,_=verify_record(normal);review.append(normal);fixtures.append(engine_item('normal anchor '+c['template'],normal,z))
 for name,level in g.TEMPLATES.items():
  for seed in range(40):
   r=g.generate(level,seed=seed,template=name);z,stages=verify_record(r);stage_totals+=stages.get('rows',0);counts[level].add(r['generation']['parameter_fingerprint']);families.add(name)
   if seed<2:review.append(r)
   if seed<4:fixtures.append(engine_item('variant '+name+' '+str(seed),r,z))
   pms=r['generation']['parameters'];a=g.generate(level,seed=77,template=name,parameters=pms);b=g.generate(level,seed=178,template=name,parameters=pms)
   assert a['question'][':question/id']==b['question'][':question/id']
   assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
 boundary_cases=[('linear_cubic',{'a':-4,'b':-5,'c':-3,'d':-5,'u':-2}),('polynomial_radio',{'a':3,'b':6,'c':4,'d':-6,'u':-2}),('polynomial_blank',{'a':3,'b':6,'c':4,'d':6,'u':2}),('quintic_radio',{'a':3,'b':4,'c':3,'u':-1}),('exponential_y_intercept',{'a':5,'h':4,'w':3}),('trig_x_intercept',{'a':1,'b':4,'c':3,'h':'-6/5','k':4}),('log_y_intercept',{'n':3,'k':4})]
 for name,parameters in boundary_cases:
  r=g.generate(g.TEMPLATES[name],template=name,parameters=parameters);z,stages=verify_record(r);review.append(r);fixtures.append(engine_item('workload boundary '+name,r,z))
 for level in counts:
  for seed in range(100):families.add(g.generate(level,seed)['generation']['template'])
 assert families==set(g.TEMPLATES),'Default family coverage'
 # Evidence-only profiles must remain genuinely parameterized through public API.
 for c in g.CASES:
  new=dict(c['parameters']);key={'polynomial_radio':'d','polynomial_blank':'d','quintic_radio':'b','exponential_y_intercept':'h','trig_x_intercept':'h','log_y_intercept':'k'}[c['template']]
  new[key]='2/3' if key=='h' and c['template']=='trig_x_intercept' else -6 if c['template']=='polynomial_radio' else 3 if c['template']=='exponential_y_intercept' else new[key]+1
  r=g.generate(c['level'],template=c['template'],parameters=new,profile=c['bank_profile']);verify_record(r)
  assert r['question'][':question/problem']!=g.QUESTIONS[c['source_id']][':question/problem']
  review.append(r)
  item=engine_item('changed raw '+c['source_id'],r,read_prompt(r['question'][':question/problem']))
  if item:fixtures.append(item)
 # Deliberately wrong displayed coefficients and omitted-but-equivalent rows must fail.
 mutation=copy.deepcopy(review[0]);mutation['question'][':question/problem']=mutation['question'][':question/problem'].replace('x=2{t}^{3}','x=3{t}^{3}')
 try:verify_record(mutation);raise RuntimeError('Displayed equation mutation escaped')
 except AssertionError:pass
 mutation=copy.deepcopy(next(r for r in review if r['generation']['template']=='polynomial_blank'))
 mutation['question'][':question/worked-solution']=mutation['question'][':question/worked-solution'].replace(r' \\ y-9 & =x','')
 try:verify_record(mutation);raise RuntimeError('Missing structure mutation escaped')
 except AssertionError:pass
 # Full relation equivalence, rather than separate sides or a UUID-only key.
 assert line_eq(3*(Y-2*X),Y-2*X)
 assert not line_eq(Y-2*X+(X-1)**2,Y-2*X)
 for template,old,new in [('trig_x_intercept',r'\operatorname{sin}⁡(\frac{\pi }{2})',r'\operatorname{cos}⁡(\frac{\pi }{2})'),('exponential_y_intercept',r'3{e}^{3t}',r'4{e}^{3t}')]:
  mutation=copy.deepcopy(next(r for r in review if r['generation']['template']==template))
  mutation['question'][':question/worked-solution']=mutation['question'][':question/worked-solution'].replace(old,new,1)
  try:verify_record(mutation);raise RuntimeError('Derivative/evaluation mutation escaped')
  except AssertionError:pass
 mutation=copy.deepcopy(next(r for r in review if r['generation']['template']=='linear_cubic' and r['generation']['parameters'].get('a')==-4 and r['generation']['parameters'].get('u')==-2))
 mutation['question'][':question/worked-solution']=mutation['question'][':question/worked-solution'].replace('8-5=3','-5+8=3')
 try:verify_record(mutation);raise RuntimeError('Coordinate stage order mutation escaped')
 except AssertionError:pass
 # Explicit level bounds and source shape guard failures.
 for name,level in g.TEMPLATES.items():
  pms=dict(g.generate(level,template=name)['generation']['parameters']);pms[next(iter(pms))]=100
  try:g.generate(level,template=name,parameters=pms);raise RuntimeError('Out-of-bounds accepted')
  except ValueError:pass
 (ROOT/'source-cases.json').write_text(json.dumps(g.CASES,indent=2)+'\n');(ROOT/'review.json').write_text(json.dumps(raw_records+review,indent=2,ensure_ascii=False)+'\n')
 (ROOT/'engine-input.json').write_text(json.dumps(fixtures,indent=2,ensure_ascii=False)+'\n')
 result=subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],text=True,capture_output=True)
 assert result.returncode==0,result.stdout+result.stderr
 engine=json.loads((ROOT/'engine-report.json').read_text())
 summary={'status':'passed','runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'provenance':{k:g.SOURCE[k] for k in ['database','basis','lineage']},'source_questions':6,'source_fields':7,'raw_prompt_exact':6,'raw_worked_solution_exact_present':5,'raw_worked_solution_omission_preserved':1,'difficulty_enum_matches':5,'difficulty_omission_preserved':1,'complete_source_banks':6,'source_values_matched':matched,'source_values_total':23,'source_designated_distractors_matched':12,'source_designated_distractors_total':12,'unrated_bank_values_matched_without_designation':5,'source_correct_refs_matched':correct,'source_correct_refs_total_present':6,'missing_source_correct_refs':1,'independent_variant_checks':280,'explicit_boundary_cases':7,'meaningful_tasks_in_40_seeds_per_family':{l:len(v) for l,v in counts.items()},'verified_solution_rows':stage_totals,'native':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':engine['documented_unresolved_checks'],'skipped_raw_missing_key_records':1,'mathematically_equivalent_raw_entries_rejected_by_round_wording':sum(1 for item in fixtures if 'round' in item['record']['question'][':question/problem'].lower() for check in item['checks'] if 'equivalent' in check['purpose'])},'negative_regressions':['actual displayed curve altered','required source stage omitted','explicit workload bounds','derivative operand altered','familiar-angle evaluation altered','full line relation with spurious quadratic term','ordered coordinate evaluation components swapped'],'plot_generation':'none; practice questions have no plot references','limitations':['Unrated raw question has no captured correct ref, difficulty or worked solution. Mathematical key independently inferred only for normal completed records.','Several source distractor recipes are opaque; public raw profiles use explicit component generalizations and remain ineligible evidence.','Raw Do not round wording rejects equivalent typed entries; normal exact-answer wording accepts them.']}
 (ROOT/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
 (ROOT/'review.md').write_text('# Tangent-line generator review\n\nOriginal capture profiles are evidence only. Normal records explicitly use authored complete operation banks.\n\n'+'\n\n---\n\n'.join(g.markdown(r) for r in raw_records+review))
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
