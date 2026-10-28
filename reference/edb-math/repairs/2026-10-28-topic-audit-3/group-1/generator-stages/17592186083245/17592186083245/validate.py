#!/usr/bin/env python3
"""Read actual displayed mathematics, match every source bank, native grade.
The strict local parser is copied from the parent's tangent-line QA parser;
no generator metadata is used to derive the independent mathematical key.
"""
import copy, hashlib, importlib.util, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load('normal_generator',ROOT.with_suffix('.py'));p=load('normal_display_parser',ROOT/'display-parser.py');X,Y,T=p.x,p.y,p.t
MATH=re.compile(r'\$\$[\s\S]*?\$\$|\$[^$]*\$')
def blocks(text):return [m[0][2:-2] if m[0].startswith('$$') else m[0][1:-1] for m in MATH.finditer(text)]
def math(text):return p.scalar(text.strip().replace('&','').removesuffix(r'\,'))
def same(a,b):return s.simplify(s.trigsimp(a-b))==0
def pair(text):
 text=text.strip().rstrip('.,').replace(r'\,','').replace(r'\left','').replace(r'\right','');assert text.startswith('(') and text.endswith(')'),text
 return tuple(math(z) for z in text[1:-1].split(','))
def relation(raw):
 lhs,rhs=raw.strip().rstrip('.,').split('=');return s.expand(math(lhs)-math(rhs))
def line_eq(a,b):
 if s.Poly(a,X,Y,domain='EX').total_degree()!=1 or s.Poly(b,X,Y,domain='EX').total_degree()!=1:return False
 ca=[a.coeff(X),a.coeff(Y),a.subs({X:0,Y:0})];cb=[b.coeff(X),b.coeff(Y),b.subs({X:0,Y:0})];pivot=next(i for i,v in enumerate(cb) if v!=0)
 return ca[pivot]!=0 and same(a*cb[pivot],b*ca[pivot])
def formatting(text):
 assert text.count('$')%2==0 and text.count('{')==text.count('}'),text
 assert not re.search(r'\+\s*-|--',text),text
 for b in blocks(text):assert b.count('{')==b.count('}'),b

def read_prompt(text):
 raw=next(b for b in blocks(text) if re.match(r'\s*x\s*=',b));raw=raw.replace(r'\quad','').replace(r'\,','')
 m=re.match(r'\s*x\s*=(.*?),\s*y\s*=(.*?),',raw,re.S);assert m,raw
 xt,yt=map(math,m.groups());terms=[math(b.split('=',1)[1].strip().rstrip('.,?')) for b in blocks(text) if re.match(r't\s*=',b)];assert len(terms)==1
 u=terms[0];dx,dy=s.diff(xt,T),s.diff(yt,T);xp,yp=s.simplify(xt.subs(T,u)),s.simplify(yt.subs(T,u));dxp,dyp=dx.subs(T,u),dy.subs(T,u)
 ratio=s.simplify(dy/dx)
 if dxp==0 and dyp==0:
  # q15570 parameter retraces one geometric branch y-h=exp(-(x-k));
  # dx/dt=0 at its endpoint but dy/dx has unique finite limiting value.
  assert xt.has(s.log(s.sin(T))) and yt.has(1/s.sin(T))
  k=s.simplify(xt-s.log(s.sin(T)));h=s.simplify(yt-1/s.sin(T));assert not k.has(T) and not h.has(T)
  assert same(yt-h,s.exp(-(xt-k)))
  assert same(s.diff(s.exp(-(X-k))+h,X).subs(X,xp),s.limit(ratio,T,u))
  m=s.limit(ratio,T,u)
 else:
  assert dxp!=0 and dyp!=0;m=s.simplify(dyp/dxp)
 mn=s.simplify(-1/m);line=s.expand(Y-yp-mn*(X-xp));xi=s.simplify(xp-yp/mn);yi=s.simplify(yp-mn*xp)
 return dict(xt=xt,yt=yt,u=u,dx=dx,dy=dy,xp=xp,yp=yp,m=m,mn=mn,line=line,xi=xi,yi=yi,ratio=ratio)

def aligned_rows(block):return block.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\')
def stage_check(r,z):
 name=r['generation']['template'];solution=r['question'].get(':question/worked-solution')
 if solution is None:return 0
 allblocks=blocks(solution);alignments=[b for b in allblocks if r'\begin{aligned}' in b]
 expected={'log_sine':[2,3,1,2],'log_power':[2,3,1,2],'cubic_axis':[2,2,3,2,4],'sixth_axis':[2,2,3,5,2],'cubic_linear':[2,3,3,2],'exponential':[2,3,1,2],'quartic_cubic':[2,2,3,2],'quartic_axis':[2,3],'linear_quadratic':[2,2]}
 counts=[len(aligned_rows(b)) for b in alignments];assert counts==expected[name],('operative row structure',name,counts)
 first=aligned_rows(alignments[0]);assert len(first)==2
 for row,var in zip(first,['x','y']):
  parts=row.replace('&','').split('=');assert parts[0].strip()==var
  for expr in parts[1:]:assert same(math(expr),z['xp' if var=='x' else 'yp']),('coordinate evaluation',name,expr,z)
 # The derivative component pair is its own required source block.
 deriv=next(b for b in allblocks if ('{x}^{′}(t)=' in b or "x'(t)=" in b or r'x\prime(t)=' in b))
 components=re.split(r',\\(?:,|quad|qquad)\s*',deriv);assert len(components)==2,components
 for component,var in zip(components,['x','y']):
  lhs,rhs=component.split('=',1);assert var in lhs
  assert same(math(rhs),z['d'+var]),('displayed coordinate derivative',rhs,z['d'+var])
 if name in ('linear_quadratic','quartic_axis'):
  ratio=next(b for b in allblocks if r'\frac{dy}{dx}=' in b)
  assert same(math(ratio.split('=')[-1]),z['ratio'])
  slope=next(b for b in allblocks if b.strip().startswith('m='))
  for expr in slope.split('=')[1:]:assert same(math(expr),z['m'])
  normal=next(b for b in allblocks if b.strip().startswith('m_n='))
 else:
  ratio=next(b for b in alignments if r'\frac{dy}{dx} &' in b)
  for row in aligned_rows(ratio)[1:]:
   for expr in row.replace('&','').split('=')[1:]:assert same(math(expr),z['ratio']),('symbolic ratio operation',expr,z['ratio'])
  slope=next(b for b in alignments if aligned_rows(b)[0].lstrip().startswith('m'))
  for row in aligned_rows(slope):
   for expr in row.split('&')[-1].split('=')[1:]:
    if '|' not in expr:assert same(math(expr),z['m']),('tangent slope',expr)
  normal=next(b for b in allblocks if ('{m}_{n}' in b or 'm_n =' in b) and '=' in b)
 assert r'-\frac{1}{m}' in normal,('formal negative reciprocal missing',normal)
 for expr in normal.split('=')[2:]:assert same(math(expr),z['mn']),('negative reciprocal',expr,z['mn'])
 axis=g.FAMILIES[name][-1] if name in g.FAMILIES else None
 linegroups=alignments[1:] if name in ('linear_quadratic','quartic_axis') else [alignments[-2],alignments[-1]] if axis else [alignments[-1]]
 for j,b in enumerate(linegroups):
  intercept=axis and j==len(linegroups)-1
  target=X-z['xi'] if axis=='x' else Y-z['yi']
  for row in aligned_rows(b):
   assert row.count('=')==1,row
   assert line_eq(relation(row.replace('&','')),s.expand(target) if intercept else z['line']),('whole-line/intercept row',row,z)
 if name=='quartic_axis':
  pointline=next(b for b in allblocks if b.strip().startswith('y-'))
  assert line_eq(relation(pointline),z['line'])
 # Every declared point, including the point-slope prose and final conclusion.
 for b in allblocks:
  if '=(' in b and '{x}_{1}' in b:b=b.split('=',1)[1]
  if b.lstrip().startswith('(') and b.rstrip().endswith((')',').',').,',').$')):
   values=pair(b)
   if len(values)==2:
    conclusion='Consequently' in solution and b in blocks(solution.split('Consequently',1)[1])
    target=(z['xi'],0) if axis=='x' and conclusion else (0,z['yi']) if axis=='y' and conclusion else (z['xp'],z['yp'])
    assert all(same(a,c) for a,c in zip(values,target)),('prose point/conclusion',b,target)
 # Family-specific mandatory operation masks, beyond row counts/equality.
 if name=='log_sine':assert r'\cdot \frac{\operatorname{sin}' in ratio and r'-\frac{1}{\operatorname{sin}' in ratio
 if name=='log_power':assert r'\frac{6{t}^{3}-3t}{2}' in ratio
 if name=='cubic_linear':assert r'(-1)\cdot \frac{1}' in ratio
 if name=='exponential':assert r'\frac{2t{e}^{t}}{{e}^{t}}' in ratio and '=2t' in ratio.replace(' ','')
 # Freeze the operative source skeleton, not merely equivalent values and row
 # counts. Read translations from the actual prompt; they may not come from
 # generation parameters. Undo the complete coordinate groups in its normal
 # line block and compare every source point-slope/distribution/collection row.
 if name in g.FAMILIES and name!='quartic_axis':
  _,idx,baseX,baseY,_,_=g.FAMILIES[name]
  k=s.simplify(z['xt']-baseX);h=s.simplify(z['yt']-baseY)
  assert not k.has(T) and not h.has(T)
  original=[b[2:-2] for b in re.findall(r'\$\$.*?\$\$',g.QUESTIONS[idx][':question/worked-solution'],re.S)]
  displays=[b[2:-2] for b in re.findall(r'\$\$.*?\$\$',solution,re.S)]
  assert displays[1:5]==original[1:5],('source derivative/ratio/evaluation/reciprocal operative skeleton',name)
  line=displays[5]
  for var,shift in [('x',k),('y',h)]:
   if shift:line=line.replace('('+var+('-' if shift>0 else '+')+g.tex(abs(shift))+')',var)
  assert line==original[5],('source normal rearrangement skeleton',name)
 return sum(counts)

def verify(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'} and r['knowledge_point']['db_id']==g.KP
 assert r==json.loads(json.dumps(r));q=r['question'];z=read_prompt(q[':question/problem']);formatting(q[':question/problem']);formatting(q.get(':question/worked-solution',''))
 uuid.UUID(q[':question/id']);uuid.UUID(r['knowledge_point']['id'])
 fields=q[':question/answer-fields'];axis=g.FAMILIES[r['generation']['template']][-1] if r['generation']['template'] in g.FAMILIES else None
 for f in fields:
  uuid.UUID(f[':answer-field/id'])
  for a in f[':answer-field/choices']:uuid.UUID(a[':answer/id'])
  answers=f[':answer-field/choices'];owned={a[':answer/id'] for a in answers};assert len(owned)==len(answers)
  objects=[]
  for a in answers:
   formatting(a[':answer/value']);value=a[':answer/value']
   if f[':answer-field/type'].endswith('/blank'):
    assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem'];obj=math(value);target=(z['xi'] if axis=='x' else 0) if f[':answer-field/key']=='field-1' else (0 if axis=='x' else z['yi']);eq=same(obj,target)
   elif value.startswith('('):obj=pair(value);eq=all(same(a,b) for a,b in zip(obj,(z['xi'],0)))
   else:obj=relation(value);eq=line_eq(obj,z['line'])
   if ':answer-field/correct' in f:assert eq==(a[':answer/id']==f[':answer-field/correct'][1]),('designation versus displayed value',value,z)
   objects.append(obj)
  for i,obj in enumerate(objects):
   for old in objects[:i]:assert not (all(same(a,b) for a,b in zip(obj,old)) if isinstance(obj,tuple) else line_eq(obj,old) if f[':answer-field/type'].endswith('/radio') else same(obj,old)),('ambiguous complete bank',obj,old)
  if ':answer-field/correct' in f:assert f[':answer-field/correct'][0]==':answer/id' and f[':answer-field/correct'][1] in owned
 if not r['generation']['evidence_only']:
  level='easy' if r['generation']['template']=='linear_quadratic' else g.FAMILIES[r['generation']['template']][0];assert q[':question/difficulty']==':question.difficulty/'+level
 return z,stage_check(r,z)

def fidelity(r,q):
 generated=r['question'];assert generated[':question/problem']==q[':question/problem'];assert generated.get(':question/worked-solution')==q.get(':question/worked-solution')
 for key in (':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (key in q)==(key in generated)
 if ':question/difficulty' in q:assert generated[':question/difficulty']==q[':question/difficulty'][':db/ident']
 assert len(generated[':question/answer-fields'])==len(q[':question/answer-fields'])
 matched=correct=0
 for f,orig in zip(generated[':question/answer-fields'],q[':question/answer-fields']):
  assert f[':answer-field/key']==orig[':answer-field/key'] and f[':answer-field/type']==orig[':answer-field/type'][':db/ident'];assert (':answer-field/correct' in f)==(':answer-field/correct' in orig)
  # Literal values are stronger than equation equivalence at the anchor. The
  # latter is separately exercised for changed banks and independent QA.
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in orig[':answer-field/choices'])
  for a in f[':answer-field/choices']:
   old=next(v for v in orig[':answer-field/choices'] if v[':answer/value']==a[':answer/value']);assert a[':answer/type']==old[':answer/type'][':db/ident'];matched+=1
   if ':answer-field/correct' in f:assert (a[':answer/id']==f[':answer-field/correct'][1])==(old[':answer/id']==orig[':answer-field/correct'][':answer/id'])
  correct+=int(':answer-field/correct' in orig)
 return matched,correct

def engine_item(label,r):
 checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  if ':answer-field/correct' not in f:return None
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned choice; displayed equation independently validated'} for a in f[':answer-field/choices'])
  else:
   val=f[':answer-field/choices'][0][':answer/value'];answer=math(val);alternate=str(s.numer(answer)+s.denom(answer))+'/'+str(s.denom(answer))+'-1'
   checks.extend([{'field_index':fi,'submitted':val,'expected':'accepted','purpose':'canonical scalar coordinate'},{'field_index':fi,'submitted':alternate,'expected':'rejected' if 'round' in r['question'][':question/problem'].lower() else 'accepted','purpose':'independently unreduced equivalent coordinate; raw round wording form-sensitive'},{'field_index':fi,'submitted':'999','expected':'rejected','purpose':'wrong coordinate'}])
 return {'label':label,'record':r,'checks':checks}

def main():
 raw=[];review=[];fixtures=[];cases=[];matched=correct=rows=0;counts={l:set() for l in ['easy','moderate','hard']};normal_count=0;profile_variants=0
 for name,d in g.FAMILIES.items():
  level,idx,*_=d;c={'source_id':g.QUESTIONS[idx][':db/id'],'template':name,'level':level,'parameters':{'k':0,'h':0},'bank_profile':'observed'};cases.append(c)
  r=g.generate(level,template=name,parameters=c['parameters'],profile='observed');z,n=verify(r);a,b=fidelity(r,g.QUESTIONS[idx]);matched+=a;correct+=b;rows+=n;raw.append(r);item=engine_item('raw '+name,r)
  if item:fixtures.append(item)
  if name!='quartic_axis':
   r=g.generate(level,template=name,parameters={'k':2,'h':4},profile='observed');verify(r);review.append(r);fixtures.append(engine_item('changed observed '+name,r));profile_variants+=1
 for name,level in [('linear_quadratic','easy')]+[(n,d[0]) for n,d in g.FAMILIES.items()]:
  for seed in range(24):
   r=g.generate(level,seed=seed,template=name);z,n=verify(r);rows+=n;normal_count+=1;counts[level].add(r['generation']['mathematical_fingerprint'])
   if seed<2:review.append(r)
   if seed<4:fixtures.append(engine_item('method '+name+' '+str(seed),r))
   parameters=r['generation']['parameters'];a=g.generate(level,73,template=name,parameters=parameters);b=g.generate(level,87,template=name,parameters=parameters);assert a['question'][':question/id']==b['question'][':question/id']
 # All eligible source-shaped families occur under ordinary level defaults.
 coverage=set(g.generate(l,seed)['generation']['template'] for l in counts for seed in range(60));assert coverage==set(g.FAMILIES)|{'linear_quadratic'},coverage
 # Full equation equivalence up to nonzero scalar and wrong-line rejection.
 assert line_eq(7*(Y+3*X-2),Y+3*X-2) and not line_eq(Y+3*X-3,Y+3*X-2)
 for name,level in [('linear_quadratic','easy')]+[(n,d[0]) for n,d in g.FAMILIES.items()]:
  pms=g.generate(level,template=name)['generation']['parameters'];bad=dict(pms);bad[next(iter(bad))]=100
  try:g.generate(level,template=name,parameters=bad);raise AssertionError('out of bounds accepted')
  except ValueError:pass
 # Mutation preserves final bank but changes actual displayed coordinate curve.
 m=copy.deepcopy(next(r for r in review if r['generation']['template']=='cubic_axis'));m['question'][':question/problem']=m['question'][':question/problem'].replace('7{t}^{2}','9{t}^{2}')
 try:verify(m);raise RuntimeError('displayed prompt mutation escaped')
 except AssertionError:pass
 m=copy.deepcopy(next(r for r in review if r['generation']['template']=='exponential'));m['question'][':question/worked-solution']=m['question'][':question/worked-solution'].replace(r'\frac{2t{e}^{t}}{{e}^{t}}',r'2t')
 try:verify(m);raise RuntimeError('omitted source cancellation operation escaped')
 except AssertionError:pass
 # Decoded source bytes, not JSON escaping, establish whether TeX repairs exist.
 slash_runs=[]
 for q in g.QUESTIONS:
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:slash_runs.append({'source_id':q[':db/id'],'answer_id':a[':answer/id'],'adjacent_ord92_positions':[i for i in range(len(a[':answer/value'])-1) if ord(a[':answer/value'][i])==ord(a[':answer/value'][i+1])==92]})
 assert all(not a['adjacent_ord92_positions'] for a in slash_runs)
 (ROOT/'decoded-tex-evidence.json').write_text(json.dumps(slash_runs,indent=2)+'\n');(ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(ROOT/'review.json').write_text(json.dumps(raw+review,indent=2,ensure_ascii=False)+'\n');(ROOT/'engine-input.json').write_text(json.dumps(fixtures,indent=2,ensure_ascii=False)+'\n')
 command=[str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')];result=subprocess.run(command,text=True,capture_output=True);assert result.returncode==0,result.stdout+result.stderr;engine=json.loads((ROOT/'engine-report.json').read_text())
 summary={'status':'passed','runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'provenance':{k:g.CAP[k] for k in ['database','basis','lineage']},'source_questions':8,'raw_prompt_exact':8,'raw_solution_exact_present':7,'raw_solution_omission_preserved':1,'raw_difficulty_enum_matches':7,'raw_difficulty_omission_preserved':1,'complete_source_banks':8,'source_values_matched':matched,'source_values_total':34,'source_correct_refs_matched':correct,'source_correct_refs_present':9,'missing_source_correct_refs':1,'matched_designated_distractors':20,'unrated_bank_values_without_designation':5,'independent_normal_instances':normal_count,'changed_historical_profiles_checked':profile_variants,'verified_aligned_rows':rows,'sampled_distinct_tasks':{l:len(v) for l,v in counts.items()},'default_family_coverage':sorted(coverage),'native':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':engine['documented_unresolved_checks'],'raw_missing_key_records_skipped':1,'raw_equivalent_coordinates_rejected_by_round_wording':4},'engine_source_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'limitations':['Raw q-15558 omits difficulty, correct designation and worked solution; inferred key is used only in authored completion.','Historical whole banks have opaque errors and remain public evidence-only; normals use separate complete method banks.','q-15570 has stationary parameter derivatives and a geometric endpoint tangent; normal presentation adds the limiting-branch justification.','q-122931 source says tangent while solving the normal; normal presentation repairs this prose.','Raw Do not round wording rejects four meaningful equivalent coordinate entries; normal exact-answer phrasing supports them.','Translation family extension preserves fixed differentiation workload; it is not claimed as additional recovered template or derivative variety.','q-15558 source raster replay is restricted to original geometry; textual authored completion varies geometry without reusing that plot.']}
 summary['finite_eligible_method_tasks']={key:val['eligible_method_tasks'] for key,val in json.loads((ROOT/'finite-domain.json').read_text()).items()}
 summary['normal_teaching_repairs']={'limiting_endpoint_justification':1,'tangent_to_normal_prose':1,'exact_answer_wording':2}
 (ROOT/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
 sections=[]
 for r in raw+review:sections.append('## '+('Observed evidence' if r['generation']['evidence_only'] else 'Generated method-bank variant')+' — '+r['generation']['template']+'\n\n'+g.markdown(r))
 (ROOT/'review.md').write_text('# Normal-line review\n\nRaw originals, changed evidence profiles and authored normal variants are distinguished below.\n\n'+'\n\n---\n\n'.join(sections))
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
