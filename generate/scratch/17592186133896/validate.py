#!/usr/bin/env python3
"""Independent displayed-math, exact replay, complete integral and native grader QA."""
import concurrent.futures,importlib.util,json,math,re,subprocess,sys,hashlib,platform,tempfile
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('green',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def bound(s):
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 s=s.replace(' ','').replace(r'\pi','pi').replace('π','pi')
 s=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',s)
 s=s.replace('{','(').replace('}',')')
 return parse_expr(s,local_dict={'pi':sp.pi},transformations=standard_transformations+(implicit_multiplication_application,))

def display_data(r):
 q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 curve=re.search('⟨(.*?)⟩',prompt)[1].replace(r'\,','').split(',')
 x,y=[g.parse_math(z) for z in curve]
 interval=re.search(r'for \$t.*?\[(.*?)\]',prompt)[1]
 lo,hi=[bound(z) for z in interval.split(',')]
 field='P' if '$P(x,y)=-y$' in prompt else 'Q'
 sign=-1 if 'negatively oriented' in prompt else 1
 dx,dy=sp.diff(x,g.t),sp.diff(y,g.t)
 expected=sign*((-y*dx) if field=='P' else x*dy)
 derivative=re.search('⟨(.*?)⟩',sol)[1].replace(r'\,','').split(',')
 assert sp.trigsimp(g.parse_math(derivative[0])-dx)==0
 assert sp.trigsimp(g.parse_math(derivative[1])-dy)==0
 assert sp.simplify(x.subs(g.t,lo)-x.subs(g.t,hi))==0
 assert sp.simplify(y.subs(g.t,lo)-y.subs(g.t,hi))==0
 signed_area=g.integral_value(x*dy,(lo,hi))
 assert float(sp.N(signed_area))*sign>0
 # Read BOTH actual displayed parametric substitution and final collection.
 last=sol[sol.rfind(r'\begin{aligned}'):]
 expressions=re.findall(r'\}([^{]*?)\\,dt',last)
 # Source-shaped bounds use nested braces; read via a brace-balanced walker.
 starts=list(re.finditer(r'\{\\int \}|\\int(?=_)',last)); rows=[]
 for match in starts:
  text=last[match.end():];pos=0
  for token in ['_','^']:
   assert text[pos]==token
   pos+=1
   if text[pos]=='{':
    depth=1;pos+=1
    while depth:
     if text[pos]=='{':depth+=1
     elif text[pos]=='}':depth-=1
     pos+=1
   else:
    pos+=1
  end=text.find(r'\,',pos)
  # Product exponential factors can themselves contain a spacing \,.
  ends=[j for suffix in (r'\,dt',r'\,\mathrm{d}t') if (j:=text.find(suffix,pos))>=0]
  assert ends
  rows.append(text[pos:min(ends)])
 assert len(rows)==2,(r['generation']['template'],rows)
 for row in rows:assert sp.trigsimp(g.parse_math(row)-expected)==0,(row,expected)
 return expected,(lo,hi),x,y,sign

def formatting(r):
 q=r['question']; assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['generation']['learner_eligible']
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
  assert text.count('$')%2==0
  assert not re.search(r'(?<!\\)\\\s*&',text),'collapsed aligned row separator'
  for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S):
   if block.count('&')>1:assert chr(92)*2 in block,'missing TeX aligned row breaks'
  depth=0
  for ch in text:
   if ch=='{':depth+=1
   elif ch=='}':depth-=1
   assert depth>=0
  assert depth==0
  assert 'AAAAAAA' not in text and '@@' not in text and '--' not in text and '+-' not in text
 assert len(q[':question/answer-fields'])==1
 assert q[':question/answer-fields'][0][':answer-field/type']==':answer-field.type/radio'

def verify(r):
 formatting(r);expected,domain,x,y,sign=display_data(r)
 f=r['question'][':question/answer-fields'][0];choices=f[':answer-field/choices'];assert len(choices)==5
 expr=[g.parse_math(a[':answer/value']) for a in choices]
 good=[i for i,e in enumerate(expr) if sp.trigsimp(e-expected)==0]
 assert len(good)==1
 assert choices[good[0]][':answer/id']==f[':answer-field/correct'][1]
 iv=[g.integral_value(e,domain) for e in expr]
 assert all(not g.equivalent_scalar(iv[i],iv[j]) for i in range(5) for j in range(i))
 # Plot data are read back and checked against actual displayed coordinates.
 plots=r['generation']['plots'];data=json.loads(Path(plots['data']).read_text())
 assert data['orientation']==sign
 assert [bound(s) for s in data['domain']]==list(domain)
 for arrow in data['arrows']:
  assert arrow['t_start']<arrow['t_end']
  for key,tk in [('start','t_start'),('end','t_end')]:
   target=[float(z.subs(g.t,arrow[tk])) for z in (x,y)]
   assert all(abs(a-b)<1e-10 for a,b in zip(target,arrow[key]))
 assert max(abs(float(x.subs(g.t,tv))-xv) for tv,xv in zip(data['samples']['t'][::100],data['samples']['x'][::100]))<1e-10
 assert max(abs(float(y.subs(g.t,tv))-yv) for tv,yv in zip(data['samples']['t'][::100],data['samples']['y'][::100]))<1e-10
 return [str(v) for v in iv]


def main():
 cases=json.loads((ROOT/'source-cases.json').read_text());source_results=[];raw=[]
 choices_matched=correct_matched=solution_matched=prompt_matched=fields_matched=0
 for case in cases:
  r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);raw.append(r)
  q=r['question'];source=g.QUESTIONS[case['source_id']]
  assert q[':question/problem']==source[':question/problem'];prompt_matched+=1
  assert (':question/worked-solution' in q)==(':question/worked-solution' in source)
  if ':question/worked-solution' in source:
   assert q[':question/worked-solution']==source[':question/worked-solution'];solution_matched+=1
  assert (':question/difficulty' in q)==(':question/difficulty' in source)
  assert len(q[':question/answer-fields'])==len(source[':question/answer-fields'])
  collisions=[]
  for i,(f,sf) in enumerate(zip(q[':question/answer-fields'],source[':question/answer-fields'])):
   assert f[':answer-field/key']==sf[':answer-field/key'] and f[':answer-field/type']==sf[':answer-field/type'][':db/ident'];fields_matched+=1
   vals=sorted(a[':answer/value'] for a in f[':answer-field/choices']);sv=sorted(a[':answer/value'] for a in sf[':answer-field/choices']);assert vals==sv;choices_matched+=len(vals)
   assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
   if ':answer-field/correct' in sf:
    value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert value==sf[':answer-field/correct'][':answer/value'];correct_matched+=1
   expressions=[g.parse_math(a[':answer/value']) for a in f[':answer-field/choices']]
   domain=g.mathematical_data(case['template'],case['parameters'])['domain'];integrals=[g.integral_value(e,domain) for e in expressions]
   pairs=[{'values':[f[':answer-field/choices'][i][':answer/value'],f[':answer-field/choices'][j][':answer/value']],'integral':str(integrals[i])} for i in range(5) for j in range(i) if g.equivalent_scalar(integrals[i],integrals[j])]
   collisions.append({'field_index':i,'complete_integral_collisions':pairs})
  source_results.append({'source_id':case['source_id'],'prompt_exact':True,'solution_exact':':question/worked-solution' in source,'correct_designations_matched':sum(':answer-field/correct' in f for f in source[':question/answer-fields']),'bank_exact':True,'raw_learner_eligible':False,'full_value_findings':collisions})
 records=[];math_results=[];changed_raw=[]
 for template,(level,sid,params) in g.TEMPLATES.items():
  if template=='exp_ccw':continue  # current moderate evidence supersedes historical inferred hard
  for seed in [31,43]:
   r=g.generate(level,seed,template=template);iv=verify(r);records.append(r);math_results.append({'template':template,'seed':seed,'integral_values':iv})
   p=r['generation']['parameters'];other=g.generate(level,seed+100,template=template,parameters=p)
   assert other['question'][':question/id']==r['question'][':question/id']
   assert other['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
 # Exercise documented coefficient and power boundary workloads explicitly.
 boundaries=[('easy','circle_cw',{'a':20,'b':20}),('moderate','ellipse_ccw',{'a':12,'b':1}),('hard','power',{'a':6,'b':1,'m':3}),('hard','power',{'a':2,'b':6,'m':7}),('hard','exp_cw',{'a':1,'b':6}),('hard','double_sine',{'a':6,'b':1}),('hard','double_cos',{'a':1,'b':6})]
 for level,template,p in boundaries:
  r=g.generate(level,1001,template=template,parameters=p);iv=verify(r);records.append(r);math_results.append({'template':template,'boundary_parameters':p,'integral_values':iv})
 # Normalized evidence profile exists publicly but is never learner-eligible.
 for case in cases:
  r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile='observed')
  assert not r['generation']['learner_eligible']
  assert len(r['question'][':question/answer-fields'])==1
 # Changed-parameter public raw replays preserve bank and whole solution masks.
 for case in cases:
  p=dict(case['parameters']);p['a']=2 if p['a']!=2 else 3;p['b']=4
  r=g.generate(case['level'],19,template=case['template'],parameters=p,profile='observed_raw')
  assert r['generation']['parameters']==p
  changed_raw.append(r)
 # Strict explicit bounds and authored bank collision rejection.
 invalid=[('hard','ellipse_cw',{'a':3,'b':3}),('moderate','ellipse_ccw',{'a':13,'b':1}),('easy','circle_cw',{'a':21,'b':21}),('moderate','ellipse_ccw',{'a':3,'b':3}),('hard','power',{'a':2,'b':3,'m':4}),('hard','exp_cw',{'a':2,'b':1})]
 for level,template,p in invalid:
  try:g.generate(level,template=template,parameters=p)
  except ValueError:pass
  else:raise AssertionError('invalid input accepted')
 # Meaningful task dedup: equal product scales across ellipse shapes and profiles.
 r1=g.generate_moderate(template='ellipse_ccw',parameters={'a':2,'b':6})
 r2=g.generate_moderate(template='ellipse_ccw',parameters={'a':3,'b':4})
 assert r1['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
 assert r1['question'][':question/id']!=r2['question'][':question/id']
 # Fresh concurrent asset writes use private unique temporary paths.
 concurrent_parent=ROOT/'concurrent-plots';concurrent_parent.mkdir(exist_ok=True)
 concurrent_dir=Path(tempfile.mkdtemp(prefix='qa-',dir=concurrent_parent))
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  args=[('ellipse_ccw',{'a':4,'b':5}),('ellipse_ccw',{'a':4,'b':5}),('double_cos',{'a':3,'b':2})]
  result=list(pool.map(lambda pair:g.render_plots(*pair,output_dir=concurrent_dir),args))
 assert result[0]==result[1] and result[0]!=result[2]
 assert not list(concurrent_dir.glob('render-*'))
 for path in result:assert Path(path['prompt']).exists() and Path(path['data']).exists()
 engine=[]
 for r in records:
  f=r['question'][':question/answer-fields'][0];checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio selection; displayed math checked independently'} for a in f[':answer-field/choices']]
  engine.append({'label':r['generation']['template']+':'+str(r['generation']['seed']),'record':r,'checks':checks})
 (ROOT/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
 binary=ROOT/'reference/native/check-engine'
 subprocess.run([str(binary),str(ROOT/'engine-input.json'),str(ROOT/'engine.json')],check=True)
 native=json.loads((ROOT/'engine.json').read_text())
 report={'passed':True,'version':g.VERSION,'source_provenance':{k:v for k,v in g.SOURCE.items() if k!='record'},'source_coverage':{'questions':8,'prompt_exact':prompt_matched,'existing_solutions_exact':solution_matched,'existing_solutions_total':7,'fields_exact':fields_matched,'fields_total':9,'displayed_choices_exact':choices_matched,'displayed_choices_total':45,'correct_designations_exact':correct_matched,'correct_designations_total':7,'absent_correct_refs_retained':2,'absent_difficulty_retained':1,'absent_solution_retained':1},'source_results':source_results,'generated_records_checked':len(records),'levels':['easy','moderate','hard'],'generated_math_results':math_results,'grading':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks'],'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest()},'runtime':{'python':platform.python_version(),'sympy':sp.__version__,'matplotlib':__import__('matplotlib').__version__},'generator_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'current_evidence_addendum':'reference/current-classification.md','suspended_normal_templates':['exp_ccw'],'authored_scope':'easy clockwise circles; outer positive scales and odd powers 3,5,7. Full operation bank authored for unique definite-integral values.','unresolved_findings':['Historical q-42221 raw replay lacks correct/solution/difficulty. Current source repaired it and rates it moderate; authored hard sampling is suspended.','Raw q-42238 duplicate legacy field retained only in evidence profile.','Ambiguous complete-integral source banks are evidence-only; full-value collisions reported per field.'],'database_writes':0}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 (ROOT/'review.json').write_text(json.dumps({'original_replays':raw,'generated_evidence_variants':changed_raw,'generated_variants':records},indent=2,ensure_ascii=False)+'\n')
 md='# Green’s theorem area setup: original evidence and generated variants\n\nRaw originals preserve the captured banks and missing attributes; they are evidence-only. Generated variants use a complete authored bank whose full integral values are pairwise unequal. Correctness, repair and fidelity are counted separately in validation.json.\n\n'
 for r in raw:
  md+='### Original '+r['generation']['source_id']+' — raw evidence\n\n'+g.markdown(r)+'\n'
 for r in changed_raw:
  md+='### Generated changed-parameter evidence — source bank '+r['generation']['source_id']+' (learner-ineligible)\n\n'+g.markdown(r)+'\n'
 for r in records:
  md+='### Generated variant — '+r['question'][':question/difficulty'].split('/')[-1]+'\n\n'+g.markdown(r)+'\n'
 (ROOT/'review.md').write_text(md)
 print(json.dumps(report['source_coverage']),len(records),'generated records verified')
if __name__=='__main__':main()
