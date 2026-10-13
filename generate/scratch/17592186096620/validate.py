#!/usr/bin/env python3
"""Check displayed mathematics, full source banks, response grading and replay."""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from math_parser import parse,function,fingerprint,X,K
spec=importlib.util.spec_from_file_location('quotients',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name,value):
 (HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')

def equal(a,b):return sp.cancel(a-b)==0

def solution_rows(solution):
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
 if len(blocks)!=2:raise ValueError('Expected derivative and quotient blocks')
 deriv=re.split(r'\\\\',blocks[0])
 derivatives=[parse(row.split('&=',1)[1]) for row in deriv]
 rows=[row.split('&=',1)[1] for row in re.split(r'\\\\',blocks[1])]
 return derivatives,rows

def independent(rec):
 q=rec['question'];f=function(q[':question/problem']);answer=sp.cancel(sp.diff(f,X))
 # Independent displayed u,v also establish the original function and domain.
 solution=q[':question/worked-solution']
 u=parse(re.search(r'\$u\(x\)=(.*?)\$',solution).group(1))
 v=parse(re.search(r'\$v\(x\)=(.*?)\$',solution).group(1))
 assert equal(u/v,f)
 deriv,rows=solution_rows(solution)
 assert equal(deriv[0],sp.diff(u,X)) and equal(deriv[1],sp.diff(v,X))
 for row in rows:
  for key,value in [(r'u^{\prime}(x)',deriv[0]),(r'v^{\prime}(x)',deriv[1]),('u(x)',u),('v(x)',v)]:
   row=row.replace(key,'('+sp.sstr(value)+')')
  row=row.replace('[','(').replace(']',')')
  assert equal(parse(row),answer),row
 field=q[':question/answer-fields'][0]
 correct_id=field[':answer-field/correct'][1]
 values=[parse(a[':answer/value']) for a in field[':answer-field/choices']]
 assert sum(equal(z,answer) for z in values)==1
 assert all(not equal(z,y) for i,z in enumerate(values) for y in values[:i])
 assert next(a[':answer/id'] for a,z in zip(field[':answer-field/choices'],values) if equal(z,answer))==correct_id
 assert field[':answer-field/key']==('selection' if field[':answer-field/type'].endswith('/radio') else 'field-1')
 if field[':answer-field/type'].endswith('/blank'):
  assert len(values)==1 and '{{field-1}}' in q[':question/problem']
 else:assert len(values)==5
 for value in [q[':question/id'],field[':answer-field/id']]+[a[':answer/id'] for a in field[':answer-field/choices']]:uuid.UUID(value)
 for text in (q[':question/problem'],solution):
  assert text.count('$')%2==0 and text.count('{')==text.count('}')
  assert not any(x in text for x in ('+-','--','-+'))
 assert fingerprint(q)==rec['generation']['math_fingerprint']
 return len(rows)+2

def ordered(q):
 q=copy.deepcopy(q)
 for field in q[':question/answer-fields']:field[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
 return q

def validate(rec):
 assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 metadata=rec['generation'];assert metadata['version']==g.VERSION
 expected=g.generate(rec['question'][':question/difficulty'].split('/')[-1],metadata['seed'],metadata['template'],parameters=metadata['parameters'],profile=metadata['profile'])
 assert ordered(rec['question'])==ordered(expected['question'])
 assert rec['generation']==expected['generation']
 return independent(rec)

def checks(rec):
 f=rec['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every field-owned choice through native grader'} for a in f[':answer-field/choices']]
 value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
 correct=parse(value)
 # Independently expanded numerator and denominator provide a noncanonical
 # equivalent, including symbolic constants, to test actual mathematical grading.
 num,den=sp.fraction(correct)
 equivalent=('('+sp.sstr(sp.expand(num))+')/('+sp.sstr(sp.expand(den))+')').replace('**','^')
 return [{'submitted':value,'expected':'accepted','purpose':'Canonical fragment'},
  {'submitted':equivalent,'expected':'accepted','purpose':'Equivalent expanded rational expression'},
  {'submitted':sp.sstr(correct+1).replace('**','^'),'expected':'rejected','purpose':'Incorrect answer'},
  {'submitted':sp.sstr(-correct).replace('**','^'),'expected':'rejected','purpose':'Reversed quotient-rule subtraction'}]

def build_engine():
 source=ROOT/'generate/runs/current/check-engine.rs'
 libs={name:max((ROOT/'target/release/deps').glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name in ('course_academy_engine','serde_json')}
 output=HERE/'check-engine'
 cmd=['rustc','--edition=2024','-O',str(source)]
 for name,path in libs.items():cmd+=['--extern',name+'='+str(path)]
 cmd+=['-L','dependency='+str(ROOT/'target/release/deps'),'-L','dependency='+str(ROOT.parent/'EDB/target/release/deps'),'-o',str(output)]
 subprocess.run(cmd,check=True)
 save('engine-build.json',{'command':cmd,'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,output,*libs.values()]}})
 return output

def main():
 qs={q[':question/math-academy-id']:q for q in g.RAW['kp'][':knowledge-point/questions']}
 records=[];source_reports=[];reviews=[];steps=0
 for mid,t in g.TEMPLATES.items():
  rec=g.generate('easy',0,mid,parameters=t['parameters']);steps+=validate(rec);records.append(rec)
  q=qs[mid];fields=q.get(':question/answer-fields',[])
  bank_report={'source':mid,'profile':t['profile'],'extension':t.get('extension'),'source_rated_easy':q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/easy','missing_options':[],'extra_options':[]}
  if fields:
   original=[parse(a[':answer/value']) for a in fields[0][':answer-field/choices']]
   rendered=[parse(a[':answer/value']) for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]
   assert len(original)==len(rendered)
   for z in original:assert sum(equal(z,y) for y in rendered)==1
   correct=fields[0].get(':answer-field/correct')
   if correct:assert equal(parse(correct[':answer/value']),sp.diff(function(rec['question'][':question/problem']),X))
   bank_report.update(matched_values=len(original),total_values=len(original),matched_distractors=len(original)-1,total_distractors=len(original)-1,correct_designation='captured' if correct else 'independently computed; original missing')
  else:bank_report.update(matched_values=0,total_values=0,answer_shape_fidelity='Unavailable; explicitly authored blank extension')
  # Source final rows are checked separately from normalized render formatting.
  solution=q.get(':question/worked-solution','')
  if solution:
   final=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)[-1]
   rhs=re.split(r'\\\\',final)[-1].split('&',1)[-1].lstrip().lstrip('=').strip().rstrip('.')
   assert equal(parse(rhs),sp.diff(function(rec['question'][':question/problem']),X))
   bank_report['source_final_solution_verified']=True
  source_reports.append(bank_report)
  reviews.append('## '+mid+' original\n\n'+q[':question/problem']+'\n\n'+solution+'\n\nOriginal bank: '+json.dumps([a[':answer/value'] for f in fields for a in f[':answer-field/choices']])+'\n\n### Generated source-parameter replay\n\n'+g.markdown(rec))
  for seed in range(12):
   r=g.generate('easy',seed+30,mid);steps+=validate(r);records.append(r)
   again=g.generate('easy',999,mid,parameters=r['generation']['parameters'])
   assert ordered(r['question'])==ordered(again['question'])
  # Explicit signed, zero-shift and endpoint cases, preserving constraints.
  for key in t['parameters']:
   for value in (-12,0,12):
    p=dict(t['parameters']);p[key]=value
    try:r=g.generate('easy',0,mid,parameters=p)
    except ValueError:continue
    steps+=validate(r);records.append(r)
  reviews.append('### Changed-parameter variant\n\n'+g.markdown(g.generate('easy',34,mid)))
 for r in g.batch('easy',100,827):steps+=validate(r);records.append(r)
 assert len({r['generation']['math_fingerprint'] for r in g.batch('easy',100,827)})==100
 negative=0
 for level,p,profile in [('hard',None,None),('moderate',None,None),('easy',{'c':0,'a':4,'b':-9},None),('easy',{'c':True,'a':4,'b':-9},None),('easy',{'c':-2,'a':13,'b':-9},None),('easy',None,'invented')]:
  try:g.generate(level,template='q-11955',parameters=p,profile=profile)
  except ValueError:negative+=1
  else:raise AssertionError('Invalid input accepted')
 for mode in ('prompt','answer','solution'):
  r=copy.deepcopy(records[0]);q=r['question']
  if mode=='prompt':q[':question/problem']=q[':question/problem'].replace(r'\frac{-2}',r'\frac{-3}')
  elif mode=='answer':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='999'
  else:q[':question/worked-solution']=q[':question/worked-solution'].replace('u^{\\prime}(x)&=0','u^{\\prime}(x)&=1')
  try:independent(r)
  except (ValueError,AssertionError):negative+=1
  else:raise AssertionError('Corruption accepted: '+mode)
 binary=build_engine()
 save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)])
 subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 save('source-replay.json',source_reports)
 save('previews.json',g.batch('easy',12,440))
 (HERE/'review.md').write_text('\n\n---\n\n'.join(reviews)+'\n')
 report={'passed':True,'source_basis':g.RAW['basis'],'supported_levels':['easy'],'templates':len(g.TEMPLATES),'source_banks':{'matched':sum(bool(r['total_values']) for r in source_reports),'total':sum(bool(r['total_values']) for r in source_reports),'matched_values':sum(r['matched_values'] for r in source_reports),'total_values':sum(r['total_values'] for r in source_reports),'matched_distractors':sum(r.get('matched_distractors',0) for r in source_reports),'total_distractors':sum(r.get('total_distractors',0) for r in source_reports),'missing_options':[],'extra_options':[]},'correctness':{'records':len(records),'displayed_solution_rows':steps,'negative_controls':negative,'distinct_batch':100},'fidelity':{'mathematical_banks':'Complete observed banks reproduced; sparse radio recipes marked algebraic patterns rather than inferred misconceptions.','prose':'Shared original quotient-rule prose retained.','notation_layout':'Normalized TeX and whitespace; original solution stages retained. q-11966 has authored solution. Missing definitions and fields are labeled extensions; no exact text fidelity claim.'},'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')}}
 save('validation.json',report)
 print(json.dumps(report))

if __name__=='__main__':main()
