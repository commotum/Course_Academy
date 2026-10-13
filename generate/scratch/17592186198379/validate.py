#!/usr/bin/env python3
"""Fail-closed printed-math, complete-bank, source sequence and native-grade audit."""
import importlib.util,itertools,json,hashlib,re,subprocess,sys
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('flux',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sys.path.insert(0,str(ROOT));from math_parser import scalar

def same(a,b):
 diff=s.simplify(a-b)
 if diff!=0 and any(v.is_Pow and v.exp.q==2 for v in s.preorder_traversal(diff)):
  xp,yp=s.symbols('xp yp',positive=True);diff=s.simplify(diff.subs({g.x:xp,g.y:yp}))
 assert diff==0,(a,b)
def strip_blocks(text):return re.split(r'\$\$\n.*?\n\$\$',text,flags=re.S)
def blocks(text):return re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S)
def read_vec(text):
 raw=re.search(r'\\left\\langle (.*?)\\right\\rangle',text).group(1);return [scalar(v) for v in raw.split(r',\,')]
def validate_record(r):
 q=r['question'];md=q[':question/problem'];p=r['generation']['parameters'];k=r['generation']['template'];profile=r['generation']['profile']
 F=read_vec(blocks(md)[0]);gt=scalar(re.search(r'\$z=(.*?)\$',md).group(1));dom=re.search(r' for \$(.*?)\\le x\\le (.*?)\$ and \$(.*?)\\le y\\le (.*?)\.\$',md)
 b=[scalar(a) for a in dom.groups()];x,y,z=g.x,g.y,g.z
 ru=s.Matrix([1,0,s.diff(gt,x)]);rv=s.Matrix([0,1,s.diff(gt,y)]);normal=ru.cross(rv)
 sub=[v.subs(z,gt) for v in F];h=s.simplify(s.Matrix(sub).dot(normal))
 # Real positive rectangle permits the radical simplifications printed by the source.
 if k=='q-161541':
  xp,yp=s.symbols('xp yp',positive=True);h=s.simplify(h.subs({x:xp,y:yp})).subs({xp:x,yp:y})
 ans=s.integrate(s.integrate(h,(y,b[2],b[3])),(x,b[0],b[1]))
 if not r['generation']['quarantined_source_domain']:
  width=b[3]-b[2];assert all(s.N(width.subs(x,b[0]+(b[1]-b[0])*s.Rational(i,4)))>=0 for i in range(5)),('Invalid geometric domain',b)
 else:assert k=='q-161481' and profile=='observed_q-161481'
 solblocks=blocks(q[':question/worked-solution']);deriv=solblocks[1]
 drows=deriv.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')
 for row,v in zip(drows,[x,y]):same(scalar(row.rsplit('=',1)[1]),s.diff(gt,v))
 substitution=solblocks[-2];under=re.findall(r'\\underbrace\{(.*?)\}_\{[PQR]\}',substitution)
 assert len(under)==3
 for a,v in zip(under,sub):same(scalar(a),v)
 rows=solblocks[-1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')
 stages=g.STAGES[k] if k!='easy_affine' else ['formula','dot','distributed','iterated','primitive_y','evaluated_y','primitive_x','evaluated_x','answer']
 assert len(rows)==len(stages)
 for stage,row in zip(stages,rows):
  rhs=row.split(' & =',1)[1]
  if stage in ['dot','distributed','simplified']:
   expr=rhs.split(r'\left(',1)[1].rsplit(r'\right)',1)[0];same(scalar(expr),h)
  elif stage=='iterated':
   bounds=re.findall(r'\\int_\{(.*?)\}\^\{(.*?)\}',rhs);assert len(bounds)==2
   for actual,expect in zip([bounds[0][0],bounds[0][1],bounds[1][0],bounds[1][1]],b):same(scalar(actual),expect)
   same(scalar(rhs.split(r'\left(',1)[1].rsplit(r'\right)',1)[0]),h)
  elif stage=='primitive_y':
   expr=scalar(rhs.split(r'\left[',1)[1].split(r'\right]',1)[0]);same(s.diff(expr,y),h)
  elif stage in ['evaluated_y','simplified_y']:
   expr=scalar(rhs.split(r'\left(',1)[1].rsplit(r'\right)',1)[0]);same(expr,s.integrate(h,(y,b[2],b[3])))
  elif stage=='primitive_x':
   expr=scalar(rhs.split(r'\left[',1)[1].split(r'\right]',1)[0]);same(s.diff(expr,x),s.integrate(h,(y,b[2],b[3])))
  elif stage in ['evaluated_x','answer']:same(scalar(rhs),ans)
 fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio';assert f[':answer-field/key']=='selection'
 choices=f[':answer-field/choices'];assert len(choices)==5
 parsed=[scalar(a[':answer/value']) for a in choices];correct=f[':answer-field/correct'][1]
 assert sum(s.simplify(v-ans)==0 for v in parsed)==1
 for a,v in zip(choices,parsed):assert (a[':answer/id']==correct)==(s.simplify(v-ans)==0)
 assert all(not g.eq(a,b) for i,a in enumerate(parsed) for b in parsed[:i])
 # Each authored error value is independently recomputed from the printed dot-product inputs.
 if not profile.startswith('observed_'):
  raw_terms=[-sub[0]*s.diff(gt,x),-sub[1]*s.diff(gt,y),sub[2]]
  if k=='q-161541':
   xp,yp=s.symbols('xp yp',positive=True);raw_terms=[s.simplify(t.subs({x:xp,y:yp})).subs({xp:x,yp:y}) for t in raw_terms]
  raw_terms=[s.trigsimp(s.simplify(t)) for t in raw_terms]
  A,B,C=[s.integrate(s.integrate(t,(y,b[2],b[3])),(x,b[0],b[1])) for t in raw_terms]
  ops={'correct':ans,'opposite':-ans,'flip_P':-A+B+C,'flip_Q':A-B+C,'omit_R':A+B,'omit_P':B+C,'R_only':C,'positive_sum':-A-B+C}
  if 'P_only' in g.DEFAULT_BANKS[profile]:ops['P_only']=g.integral(sub[0],b)
  if 'Q_only' in g.DEFAULT_BANKS[profile]:ops['Q_only']=g.integral(sub[1],b)
  for key in g.DEFAULT_BANKS[profile]:assert sum(g.eq(v,ops[key]) for v in parsed)==1,(key,parsed,ops[key])
 for text in [md,q[':question/worked-solution']]:
  assert text.count('$')%2==0
  depth=0
  for c in text:
   if c=='{':depth+=1
   if c=='}':depth-=1;assert depth>=0
  assert depth==0
 return ans

def main():
 stage_spec=importlib.util.spec_from_file_location('stage_audit',ROOT/'source-stage-audit.py');sa=importlib.util.module_from_spec(stage_spec);stage_spec.loader.exec_module(sa);source_stage_reports=[]
 cases=[];records=[];review=[];banks=[];source_matched=0;source_choices=0;native=[];prose=0;stage_rows=0
 for k,src in g.SOURCES.items():
  print('Source',k,flush=True);source_stage_reports.append(sa.audit(g,src))
  p={'p':1,'q':1,'r':1};profile='observed_'+k;r=g.generate(g.LEVELS[k],template=k,parameters=p,profile=profile);ans=validate_record(r);records.append(r)
  f=src[':question/answer-fields'][0];aorig=f[':answer-field/choices'];gen=r['question'][':question/answer-fields'][0][':answer-field/choices']
  mapping=[]
  # Try flux-method operation candidates BEFORE describing remaining values as opaque.
  m=g.model(k,p,profile);ABC=[g.integral(t,m['b']) for t in m['terms']];candidate_ops={str(c):sum(c[i]*ABC[i] for i in range(3)) for c in itertools.product([-1,0,1,2],repeat=3)}
  for a in aorig:
   value=scalar(a[':answer/value']);matches=[b for b in gen if g.eq(value,scalar(b[':answer/value']))];assert len(matches)==1
   orig_correct=a[':answer/id']==f[':answer-field/correct'][':answer/id'];matched_correct=matches[0][':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1];assert orig_correct==matched_correct
   index=next(i for i,v in enumerate(g.OBSERVED[k]) if g.eq(value,s.sympify(v)))
   mapping.append({'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'correct':orig_correct,'recipe':'p*('+g.OBSERVED[k][index]+')','mathematical_operation_candidates':[op for op,v in candidate_ops.items() if g.eq(v,value)],'interpretation':'correct flux' if orig_correct else 'underidentified: uniform-scaling observed expression shape only; not default'})
   source_choices+=1
  source_matched+=1
  parts=strip_blocks(src[':question/worked-solution']);assert parts==strip_blocks(r['question'][':question/worked-solution']);prose+=1
  bs=blocks(src[':question/worked-solution']);gs=blocks(r['question'][':question/worked-solution']);assert len(bs)==len(gs)
  for a,b in zip(bs,gs):assert len(a.split(r' \\ '))==len(b.split(r' \\ ')),(k,a,b)
  stage_rows+=len(bs[-1].split(r' \\ '))
  cases.append({'source_id':k,'source_question_id':src[':question/id'],'template':k,'parameters':p,'bank_profile':profile,'level':g.LEVELS[k]});banks.append({'source_id':k,'choices':mapping})
  review.append('## Original '+k+'\n\n'+src[':question/problem']+'\n\n'+ '\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][':answer/id'] else '') for a in aorig)+'\n\n'+src[':question/worked-solution'])
  review.append('### Generated observed-profile replay '+k+(' — QUARANTINED formal integral; original geometric domain is empty' if k=='q-161481' else ' — first substitution vector repaired' if k=='q-161552' else '')+'\n\n'+g.markdown(r))
  # A changed uniform coefficient sample exercises every explicit observed bank profile.
  scaled=g.generate(g.LEVELS[k],template=k,parameters={'p':2,'q':2,'r':2},profile=profile);validate_record(scaled);records.append(scaled);review.append('### Generated variant of observed bank '+k+' (uniform scaling; error intent unresolved'+('; QUARANTINED formal integral' if k=='q-161481' else '')+')\n\n'+g.markdown(scaled))
 for level in ['easy','moderate','hard']:
  for k,t in g.TEMPLATES.items():
   if t['level']!=level:continue
   for seed in [27,53]:
    print('Default',k,seed,flush=True);r=g.generate(level,seed,template=k);validate_record(r);records.append(r);review.append('### Generated authored default '+level+' '+k+' seed '+str(seed)+'\n\n'+g.markdown(r))
 # Stable presentation identity across random option orders.
 for r in records:
  a=r['generation'];r2=g.generate(r['question'][':question/difficulty'].split('/')[-1],999,template=a['template'],parameters=a['parameters'],profile=a['profile']);assert r2['question'][':question/id']==r['question'][':question/id'];assert r2['generation']['mathematical_fingerprint']==a['mathematical_fingerprint']
  f=r['question'][':question/answer-fields'][0];native.append({'label':a['template']+' '+a['profile']+' '+str(a['seed']),'record':r,'checks':[{'submitted_answer_id':v[':answer/id'],'expected':'accepted' if v[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native radio ownership and designation'} for v in f[':answer-field/choices']]})
 for level,k,p in [('easy','easy_affine',{'a':-3,'b':1,'c':0,'u':1,'v':1,'w':0,'X':1,'Y':1}),('moderate','q-160888',{'p':-4,'q':1,'r':1}),('hard','q-161553',{'p':1,'q':4,'r':1})]:
  try:g.generate(level,template=k,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Explicit bounds bypass')
 (ROOT/'source-stage-audit.json').write_text(json.dumps(source_stage_reports,indent=2));(ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2));(ROOT/'bank-mapping.json').write_text(json.dumps(banks,indent=2));(ROOT/'review.json').write_text(json.dumps(records,indent=2));(ROOT/'review.md').write_text('\n\n'.join(review));(ROOT/'native-input.json').write_text(json.dumps(native))
 engine=Path('generate/runs/current/check-engine');subprocess.run([str(engine),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],check=True)
 report={'passed':True,'sources':12,'source_complete_banks_matched':source_matched,'source_options_matched':source_choices,'source_correct_refs_matched':12,'source_prose_sequence_matched':prose,'source_final_math_rows':stage_rows,'source_solution_notation':'standard LaTeX normalization; same block and row counts, mathematical operations','source_solution_supported_repairs':{'q-161552':'first substitution third component 2xz → 2x(y+z)'},'source_geometric_correctness':{'passed':11,'quarantined':1,'source_id':'q-161481','reason':'reversed y bounds define no geometric interior; original bank matches formal oriented integral only'},'normal_generated_domain_correctness':'all passed; q-161481 swaps y bounds','generated_records_checked':len(records),'authored_easy_records':2,'native_checks':sum(len(n['checks']) for n in native),'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'unresolved_observed_error_intent':'wrong scalar options are underidentified; explicit uniformly-scaled expression profiles retained; default banks have independently tested method operations','source_provenance':{k:g.SOURCE[k] for k in ['database','basis','lineage']},'database_writes':0}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
