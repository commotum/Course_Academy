#!/usr/bin/env python3
"""Fail on source fidelity, independently displayed math, structure or native grade errors."""
import hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from math_parser import x,A,alpha,beta,Y,YC,YP,DC,DP,scalar,eq,displays,rows,equal
S=json.loads((ROOT/'source.json').read_text());sources=S['record'][':knowledge-point/questions'];cases=json.loads((ROOT/'source-cases.json').read_text())

def structure(text):
 assert not any(ord(c)<32 and c not in '\n\t' for c in text),('Control character',text)
 assert not any(z in text for z in ['+-','--',r'\\alpha',r'\\beta']),('Bad TeX sign/command',text)
 st=[]
 for ch in text:
  if ch=='{':st.append(ch)
  if ch=='}':assert st;st.pop()
 assert not st
 rem=re.sub(r'\$\$.*?\$\$','',text,flags=re.S);assert rem.count('$')%2==0
 assert text.count('$$')%2==0

def read_prompt(text):
 math=displays(text)
 if not math:math=re.findall(r'\$([^$]*)\$',text)
 first=math[0];ode,ic=first.split(',',1);lhs,rhs=ode.split('=',1)
 lhs=lhs.replace('{y}^{′}','').replace('y^{′}','');coefficient=scalar(lhs);assert not coefficient.free_symbols- {Y};h=-coefficient.coeff(Y);assert equal(coefficient,-h*Y)
 forcing=scalar(rhs);v=s.Integer(re.search(r'y\(0\)\s*=\s*(-?\d+)',ic)[1])
 companion=re.search(r'has the complementary solution \$(.*?)\$',text)[1];_,comp=eq(companion)
 assert equal(comp,A*s.exp(h*x))
 return h,forcing,v,comp

def validate_record(r,level):
 assert set(r['knowledge_point'])=={'db_id','id','title'} and r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/blank';assert len(f[':answer-field/choices']) in (1,2)
 for z in (q[':question/id'],f[':answer-field/id'],f[':answer-field/choices'][0][':answer/id']):uuid.UUID(z)
 assert f[':answer-field/correct']==[':answer/id',f[':answer-field/choices'][-1][':answer/id']]
 assert '{{field-1}}' in q[':question/problem'];structure(q[':question/problem']);structure(q[':question/worked-solution']);structure(f[':answer-field/choices'][0][':answer/value'])
 h,forcing,v,comp=read_prompt(q[':question/problem']);b=displays(q[':question/worked-solution']);hard=level=='hard'
 assert len(b)==(12 if hard else 10),(len(b),r['generation'])
 left,right=eq(b[0]);assert equal((left-right).subs({DC:s.diff(comp,x),YC:comp}),0)
 left,right=eq(b[1]);assert left==YC and equal(right,comp)
 left,trial=eq(b[2]);assert left==YP
 terms=s.Add.make_args(forcing);assert len(terms)==(2 if hard else 1)
 resonance=[]
 for z in terms:
  expo=[a for a in s.Mul.make_args(z) if a.func==s.exp];assert len(expo)==1;resonance.append(equal(expo[0],s.exp(h*x)))
 if level=='easy':assert not any(resonance)
 if level=='moderate':assert all(resonance)
 if hard:assert sum(resonance) in (0,1)
 derivative=s.diff(trial,x);dr=rows(b[3]);assert len(dr)==(4 if (any(resonance)) else (2 if hard else 1))
 if len(dr)>1:
  assert dr[0].split('=',1)[1].count('^{′}')==1,('Missing formal derivative',dr)
 if len(dr)==4:
  assert dr[1].split('=',1)[1].count('^{′}')==1,('Missing component formal derivative',dr)
  assert dr[2].split('=',1)[1].count('^{′}')==0 and re.search(r'\\alpha \([^)]*\{e\}',dr[2]),('Missing product-rule component row',dr)
  assert r'\alpha (1' in dr[3],('Missing collected product derivative',dr)
 for row in dr:
  if row.split('=',1)[0].replace('&','').strip():left,right=eq(row);assert left==DP
  else:right=scalar(row.split('=',1)[1])
  assert equal(right,derivative),('Displayed derivative',row,right,derivative)
 residual=s.expand(derivative-h*trial)
 sr=rows(b[4]);equation_rows=sr if hard else sr[:-1]
 assert len(equation_rows)==(3 if hard or level=='moderate' or not r['generation']['bank_profile'] or not g.PROFILES[r['generation']['source_id']].get('compact') else 2)
 assert 'alpha' in equation_rows[0]
 if not (r['generation']['source_id'] and g.PROFILES[r['generation']['source_id']].get('compact')):
  assert '(' in equation_rows[0] and ')' in equation_rows[0],('Missing full substituted components',equation_rows)
 if len(equation_rows)==3:
  assert '(' in equation_rows[1] and ')' in equation_rows[1],('Missing coefficient-distribution operation',equation_rows)
 for row in equation_rows:
  left,right=eq(row);assert equal(left,residual) and equal(right,forcing),('Displayed substitution',row,left,residual,right,forcing)
 if hard:
  raw=re.split(r'\\qquad',b[5].replace(r'\,',''));solved=re.split(r'\\qquad',b[6]);values={}
  for item,z in zip(solved,(alpha,beta)):
   left,right=eq(item.strip().lstrip(','));assert left==z;values[z]=right
  for item in raw:
   left,right=eq(item.strip().lstrip(','));assert equal(left.subs(values),right)
  offset=2
 else:
  left,right=eq(sr[-1]);assert left==alpha;values={alpha:right};offset=0
 assert equal(residual.subs(values),forcing)
 left,part=eq(b[5+offset]);assert left==YP and equal(part,trial.subs(values));assert equal(s.diff(part,x)-h*part,forcing)
 left,right=eq(b[6+offset]);assert left==Y and equal(right,YC+YP)
 left,general=eq(b[7+offset]);assert left==Y and equal(general,comp+part) and equal(s.diff(general,x)-h*general,forcing)
 initialrows=rows(b[8+offset]);assert len(initialrows)==2
 left,right=eq(initialrows[0]);assert equal(left,general.subs(x,0)) and equal(right,v)
 left,constant=eq(initialrows[1]);assert left==A and equal(general.subs({A:constant,x:0}),v)
 left,final=eq(b[9+offset]);assert left==Y and equal(final,general.subs(A,constant));assert equal(s.diff(final,x)-h*final,forcing) and equal(final.subs(x,0),v)
 for option in f[':answer-field/choices']:
  answer=scalar(option[':answer/value']);assert equal(answer,final)
 assert '$y(0)='+str(v)+'$' in q[':question/worked-solution']
 return {'homogeneous':1,'trial':1,'derivative_rows':len(dr),'substitution_rows':len(equation_rows),'coefficient_equations':len(values),'particular':1,'general':1,'initial_rows':2,'final_ode_verification':1,'final_initial_verification':1}

def native_item(label,r):
 canonical=r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'];a=scalar(canonical)
 # Factor or regroup the actual expression, retaining a truly distinct spelling.
 h,_,_,_=read_prompt(r['question'][':question/problem'])
 inner=s.expand(s.powsimp(a*s.exp(-h*x),force=True))
 equivalent='('+s.latex(s.exp(h*x))+')('+s.latex(inner)+')'
 assert equivalent!=canonical and equal(scalar(equivalent),a)
 bank_checks=[{'submitted':option[':answer/value'],'expected':'accepted','purpose':'additional original equivalent bank entry'} for option in r['question'][':question/answer-fields'][0][':answer-field/choices'][1:]]
 return {'label':label,'record':r,'checks':bank_checks+[{'submitted':canonical,'expected':'accepted','purpose':'canonical exact expression'},{'submitted':equivalent,'expected':'accepted','purpose':'algebraically equivalent expression factoring out the homogeneous exponential'},{'submitted':canonical+'+1','expected':'rejected','purpose':'wrong initial constant and ODE residual'}]}
def exp_tex(k):return 'e^{'+str(k)+'x}'

def main():
 summary={'database':'math','basis':1356,'lineage':S['lineage'],'source_questions':len(sources),'raw_prompt_exact':0,'raw_solution_exact':0,'available_solutions':13,'raw_field_shape_exact':0,'raw_answer_strings_exact':0,'available_answers':15,'complete_banks_matched':0,'available_banks':13,'correct_designations_matched':0,'available_designations':13,'missing_raw_answers':2,'authored_missing_completions':0,'presentation_repairs':0,'mathematical_repairs':0,'decoded_doubled_command_slashes':0}
 review=[];native=[];checks=[]
 byid={q[':question/math-academy-id']:q for q in sources}
 for c in cases:
  src=byid[c['source_id']];r=g.generate(c['level'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];sf=src[':question/answer-fields'][0];gf=q[':question/answer-fields'][0]
  assert q[':question/problem']==src[':question/problem'];summary['raw_prompt_exact']+=1
  assert q.get(':question/worked-solution')==src.get(':question/worked-solution')
  if ':question/worked-solution' in src:summary['raw_solution_exact']+=1
  # Schema-neutral comparison of the complete original field shape, never inventing absent refs.
  for key in (':answer-field/type',':answer-field/key'):
   sv=sf[key].get(':db/ident') if isinstance(sf[key],dict) else sf[key];assert sv==gf[key]
  assert (':answer-field/correct' in sf)==(':answer-field/correct' in gf);assert (':answer-field/choices' in sf)==(':answer-field/choices' in gf);summary['raw_field_shape_exact']+=1
  if ':answer-field/choices' in sf:
   sv=[a[':answer/value'] for a in sf[':answer-field/choices']];gv=[a[':answer/value'] for a in gf[':answer-field/choices']];assert sv==gv;assert all(equal(scalar(a),scalar(b)) for a,b in zip(sv,gv));summary['raw_answer_strings_exact']+=len(gv);summary['complete_banks_matched']+=1
   source_correct=next(i for i,a in enumerate(sf[':answer-field/choices']) if a[':answer/id']==sf[':answer-field/correct'][':answer/id']);generated_correct=next(i for i,a in enumerate(gf[':answer-field/choices']) if a[':answer/id']==gf[':answer-field/correct'][1]);assert source_correct==generated_correct;summary['correct_designations_matched']+=1
  review.append({'label':'Original raw '+c['source_id'],'record':r})
  normal=g.generate(c['level'],parameters=c['parameters'],profile=c['source_id']);checks.append(validate_record(normal,c['level']));native.append(native_item(c['source_id'],normal))
  if ':answer-field/correct' not in sf:summary['authored_missing_completions']+=1;review.append({'label':'Authored missing-source completion '+c['source_id'],'record':normal})
  for seed in (211,907):
   variant=g.generate(c['level'],seed=seed,profile=c['source_id']);checks.append(validate_record(variant,c['level']));review.append({'label':'Generated profile variant '+c['source_id']+' seed '+str(seed),'record':variant});native.append(native_item(c['source_id']+'-'+str(seed),variant))
 for t,level in g.TEMPLATES.items():
  for seed in range(40):
   r=g.generate(level,seed=seed,template=t);checks.append(validate_record(r,level));r2=g.generate(level,seed=seed+999,template=t,parameters=r['generation']['parameters']);assert r['question']==r2['question'];assert r['generation']['content_identity']==r2['generation']['content_identity']
   if seed<2:review.append({'label':'Generated authored/default '+level+' '+t+' '+str(seed),'record':r});native.append(native_item(t+'-'+str(seed),r))
 # Explicit invalid calls must fail rather than mutating or resampling.
 bad=[('easy','nonresonant',dict(h=2,k=2,f=3,v=1)),('moderate','resonant',dict(h=2,k=3,f=3,v=1)),('hard','mixed',dict(h=2,k=2,k2=2,f=3,f2=4,v=1)),('hard','two_nonresonant',dict(h=2,k=3,k2=4,f=13,f2=4,v=1)),('moderate','resonant',dict(h=-7,k=-7,f=3,v=1)),('easy','nonresonant',dict(h=2,k=3,f=0,v=1))]
 for level,t,p in bad:
  try:g.generate(level,template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('Invalid accepted',level,t,p))
 # Separate fingerprint canonicalizes forcing-term order; presentation remains separate.
 p=dict(h=2,k=3,k2=-1,f=4,f2=-2,v=3);r1=g.generate('hard',template='two_nonresonant',parameters=p);r2=g.generate('hard',template='two_nonresonant',parameters=dict(h=2,k=-1,k2=3,f=-2,f2=4,v=3));assert r1['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint'];assert r1['question'][':question/id']!=r2['question'][':question/id']
 for src in sources:
  text=src.get(':question/worked-solution','');assert r'\\alpha' not in text and r'\\begin' not in text
 (ROOT/'native-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n');engine=ROOT.parents[1]/'runs/current/check-engine';subprocess.run([str(engine),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],check=True)
 report=json.loads((ROOT/'native-report.json').read_text());summary.update(status='passed',generated_stage_checks=len(checks),stages={k:sum(c[k] for c in checks) for k in checks[0]},invalid_explicit_cases_rejected=len(bad),native_accepted=report['accepted_checks'],native_rejected=report['rejected_checks'],native_unresolved=report['documented_unresolved_checks'],native_engine_sha256=hashlib.sha256(engine.read_bytes()).hexdigest(),generator_version=g.VERSION,generator_sha256=hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),plots='none',raw_missing_designations_not_counted_as_matches=2)
 (ROOT/'validation.json').write_text(json.dumps(summary,indent=2)+'\n');(ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n');(ROOT/'review.md').write_text('# Exponential IVP review\n\nRaw originals retain absent fields/solutions. Generated records are explicitly labeled. No plots.\n\n'+'\n\n---\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in review))
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
