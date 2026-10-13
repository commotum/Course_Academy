"""Fail-closed displayed-math, source fidelity, identity and native grading QA."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('ranges_generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
C,S,X,Y=sp.symbols('C S x y',real=True)

def write(n,x):(ROOT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def expression(t):
 t=t.replace('⁡','').replace(r'\theta','θ')
 t=re.sub(r'\\operatorname\{(cos|sin)\}',lambda m:'C' if m[1]=='cos' else 'S',t)
 t=t.replace(r'\cos','C').replace(r'\sin','S').replace('θ','')
 frac=re.compile(r'\\frac\{([^{}]*)\}\{([^{}]*)\}')
 while r'\frac' in t:
  n=frac.sub(lambda m:'(('+m[1]+')/('+m[2]+'))',t)
  assert n!=t,('bad fraction',t);t=n
 t=t.strip().removesuffix('.')
 assert re.fullmatch(r'[0-9CSxy()+*/.\s-]+',t),('unsupported math',t)
 return parse_expr(t,local_dict={'C':C,'S':S,'x':X,'y':Y},transformations=standard_transformations+(implicit_multiplication_application,),evaluate=True)

def ranges(t):
 t=t.replace(r'\,','').replace(' ','').replace(r'\leq',r'\le')
 chunks=t.split(',');assert len(chunks)==2,t
 answer=[]
 for var,chunk in zip('xy',chunks):
  lhs,mid,rhs=chunk.split(r'\le');assert mid==var
  answer += [expression(lhs),expression(rhs)]
 return tuple(answer)

def readback(r):
 q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 normalized=prompt.replace('θ',r'\theta').replace('π',r'\pi')
 m=re.search(r'x\s*=([^,]+),.*?y\s*=([^,]+),',normalized,re.S);assert m,prompt
 xx,yy=expression(m[1]),expression(m[2]);assert xx.free_symbols<={C} and yy.free_symbols<={S}
 domain=re.sub(r'\s|\\,','',normalized)
 assert r'0\le\theta<2\pi' in domain
 p=g.parse_parameters(r['generation']['parameters'])
 assert sp.expand(xx)==p['a']*C+p['h'] and sp.expand(yy)==p['b']*S+p['k']
 endpoints=[]
 for f,t in [(xx,C),(yy,S)]:
  vals=[f.subs(t,v) for v in [-1,1]];endpoints.extend([min(vals),max(vals)])
 expected=tuple(endpoints)
 # Every displayed bound in every aligned row is a full sharp range (also
 # verifies distributed translations and negative-scale inequality reversal).
 row_counts=[]
 for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S):
  lines=block.split(r'\\');row_counts.append(len(lines))
  for line in lines:
   line=re.sub(r'\\text\{[^{}]*\}','',line).replace('&','')
   rev=r'\ge' in line;parts=line.split(r'\ge' if rev else r'\le');assert len(parts)==3,line
   lo,mid,hi=map(expression,parts)
   mid=mid.subs({X:xx,Y:yy})
   vals=[mid.subs({C:v,S:w}) for v in [-1,1] for w in [-1,1]]
   assert lo==(max(vals) if rev else min(vals)) and hi==(min(vals) if rev else max(vals)),line
 for inline in re.findall(r'\$([^$]*)\$',sol):
  if r'\le' in inline and ('x' in inline or 'y' in inline):
   a,b,c=inline.split(r'\le');f=expression(b).subs({X:xx,Y:yy});vals=[f.subs({C:v,S:w}) for v in [-1,1] for w in [-1,1]]
   assert expression(a)==min(vals) and expression(c)==max(vals)
 sid=r['generation']['template']
 if sid!='hard-rational' and sid!='q-70341':
  orig=g.SOURCES[sid][':question/worked-solution']
  assert row_counts==[len(b.split(r'\\')) for b in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',orig,re.S)]
 if sid=='hard-rational':assert row_counts==[5,5],row_counts
 for text in (prompt,sol):
  assert text.count('$')%2==0
  assert text.count('{')==text.count('}')
 fields=q[':question/answer-fields'];identities=[]
 if fields[0][':answer-field/type'].endswith('/radio'):
  f=fields[0];vals=[ranges(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(vals)==5 and len(set(vals))==5 and vals.count(expected)==1
  a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert ranges(a[':answer/value'])==expected
 else:
  assert len(fields)==6
  for f in fields:
   i=int(f[':answer-field/key'].split('-')[1])-1;a=f[':answer-field/choices'][0]
   assert f[':answer-field/correct']==[':answer/id',a[':answer/id']]
   if i in (1,4):assert a[':answer/value'].strip()==r'\le'
   else:assert expression(a[':answer/value'])==expected[{0:0,2:1,3:2,5:3}[i]]
  assert set(re.findall(r'\{\{(field-\d)\}\}',prompt))=={f[':answer-field/key'] for f in fields}
 for f in fields:
  ids=[a[':answer/id'] for a in f[':answer-field/choices']];assert len(set(ids))==len(ids)
  assert f[':answer-field/correct'][1] in ids;identities+=ids
 assert len(set(identities))==len(identities)
 return expected

def engine_item(r,label):
 checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   checks += [{'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio option'} for a in f[':answer-field/choices']]
  else:
   val=f[':answer-field/choices'][0][':answer/value'];sign=val.strip()==r'\le'
   # Standalone inequality fragments are form answers; numeric endpoint blanks
   # additionally test an unreduced exact fraction as a meaningful equivalent.
   checks.append({'field_index':fi,'submitted':val,'expected':'accepted','purpose':'canonical source-shaped fragment'})
   if sign:
    checks.append({'field_index':fi,'submitted':r'\leq','expected':'accepted','purpose':'equivalent inequality fragment'})
   if not sign:
    z=expression(val);num,den=sp.fraction(z);eq=str(2*num)+'/'+str(2*den)
    checks.append({'field_index':fi,'submitted':eq,'expected':'accepted','purpose':'unreduced exact numeric endpoint'})
   checks.append({'field_index':fi,'submitted':r'\ge' if sign else str(expression(val)+1),'expected':'rejected','purpose':'wrong inequality sign' if sign else 'wrong endpoint'})
 return {'label':label,'record':r,'checks':checks}

def main():
 cases=[];coverage=[];engine=[];review=[];reviewmd=['# Trigonometric parametric ranges: source and generated review','', 'All generated variants are labeled. Raw snapshots remain unchanged.']
 distractors=0;sourcevalues=0;sourcefields=0;designations=0
 for sid,old in g.SOURCES.items():
  spec=g.TEMPLATES[sid];p=dict(zip('abhk',g.PARAMS[sid]));profile='observed:'+sid if spec['kind']=='radio' else None
  case={'source_id':sid,'template':sid,'level':spec['level'],'parameters':p,'bank_profile':profile};cases.append(case)
  r=g.generate(spec['level'],template=sid,parameters=p,profile=profile);readback(r);engine.append(engine_item(r,'source:'+sid));new=r['question']
  assert new[':question/problem']==old[':question/problem']
  if sid!='q-70341':assert new[':question/worked-solution']==old[':question/worked-solution']
  for of in old[':question/answer-fields']:
   nf=next(f for f in new[':question/answer-fields'] if f[':answer-field/key']==of[':answer-field/key']);assert nf[':answer-field/type']==of[':answer-field/type'][':db/ident']
   if spec['kind']=='radio':
    ov=[ranges(a[':answer/value']) for a in of[':answer-field/choices']];nv=[ranges(a[':answer/value']) for a in nf[':answer-field/choices']];assert sorted(ov)==sorted(nv)
    sourcevalues+=5;distractors+=4
   else:
    ov=of[':answer-field/choices'][0][':answer/value'];nv=nf[':answer-field/choices'][0][':answer/value'];assert ov.strip()==nv.strip() or expression(ov)==expression(nv);sourcevalues+=1
   sourcefields+=1
   if ':answer-field/correct' in of:
    nv=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);ov=of[':answer-field/correct'][':answer/value'];assert (ranges(nv)==ranges(ov) if spec['kind']=='radio' else nv.strip()==ov.strip() or expression(nv)==expression(ov));designations+=1
  coverage.append({'source_id':sid,'bank_values_matched':True,'prompt_exact':True,'solution_exact':True if sid!='q-70341' else None,'correct_designation_matched':True if sid!='q-70341' else None,'inferred_correct':sid=='q-70341'})
  reviewmd += ['', '## Original '+sid+' ('+('unrated; authored moderate assignment' if sid=='q-70341' else spec['level'])+')','',old[':question/problem'],'','Original fields/bank:',json.dumps(old[':question/answer-fields'],indent=2,ensure_ascii=False),'','Original worked solution:',old.get(':question/worked-solution','**Absent in capture.**'),'','### Source replay (generated at original parameters)',g.markdown(r)]
  # Show observed bank variant AND default authored bank for each radio.
  for prof in ([profile,'authored:full-period'] if profile else [None]):
   v=g.generate(spec['level'],seed=42,template=sid,profile=prof);readback(v);review.append(v);engine.append(engine_item(v,'variant:'+sid+':'+str(prof)))
   reviewmd += ['','### Generated variant — '+str(prof or 'blank'),g.markdown(v)]
 for level in ['easy','moderate','hard']:
  for seed in range(2):
   r=g.generate(level,seed+1000);readback(r);review.append(r);engine.append(engine_item(r,'level:'+level+str(seed)));reviewmd += ['', '## Generated '+level+' example '+str(seed+1),g.markdown(r)]
 # Exercise every template/profile, rather than only whichever random template
 # is selected, and verify seeds/order cannot alter fixed-parameter identity.
 counts={};fingerprints={l:set() for l in ('easy','moderate','hard')}
 for name,spec in g.TEMPLATES.items():
  profiles=['authored:full-period','observed:'+name] if spec['kind']=='radio' else [None]
  for prof in profiles:
   for seed in range(24):
    r=g.generate(spec['level'],seed,template=name,profile=prof);readback(r);p=r['generation']['parameters'];r2=g.generate(spec['level'],999,template=name,parameters=p,profile=prof)
    assert r['question'][':question/id']==r2['question'][':question/id'];assert r['generation']['parameter_fingerprint']==r2['generation']['parameter_fingerprint']
    fingerprints[spec['level']].add(r['generation']['parameter_fingerprint'])
   counts[name+':'+str(prof)]=24
 # All invalid explicit parameters must fail, never be silently resampled.
 invalid=[('hard-rational',{'a':'-3/2','b':'-5/2','h':'1/2','k':'3/2'}),('hard-rational',{'a':'-2','b':'-5/3','h':'1/2','k':'3/4'}),('hard-rational',{'a':'-3/2','b':'-5/3','h':'0','k':'3/4'}),('q-16201',{'a':'4','b':'4','h':'0','k':'0'})]
 for name,p in invalid:
  try:g.generate(g.TEMPLATES[name]['level'],template=name,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('invalid accepted',name,p))
 # Equivalent mathematical tasks across presentation recipes share fingerprint.
 z={'a':4,'b':2,'h':0,'k':0};a=g.generate('easy',template='q-16201',parameters=z);b=g.generate('easy',template='q-276258',parameters=z)
 assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id']
 # Prove actual displayed mathematics is audited independently from metadata.
 for which in ('prompt','stage','choice','blank'):
  r=g.generate('easy',template='q-16201' if which=='choice' else 'q-276258',parameters={'a':4,'b':2,'h':0,'k':0});r=copy.deepcopy(r)
  if which=='prompt':r['question'][':question/problem']=r['question'][':question/problem'].replace('x=4','x=5',1)
  elif which=='stage':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('-4 &', '-5 &',1)
  elif which=='choice':
   fs=r['question'][':question/answer-fields'][0];fs[':answer-field/choices'][1][':answer/value']=fs[':answer-field/choices'][0][':answer/value']
  else:r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='123'
  try:readback(r)
  except AssertionError:pass
  else:raise AssertionError(('display corruption escaped validator',which))
 write('source-cases.json',cases);write('review.json',review);(ROOT/'review.md').write_text('\n\n'.join(reviewmd)+'\n');write('engine-input.json',engine)
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
 native=json.loads((ROOT/'engine-report.json').read_text());assert native['documented_unresolved_checks']==0
 write('validation.json',{'passed':True,'version':g.VERSION,'source_coverage':coverage,'practice_sources':16,'source_fields_matched':sourcefields,'source_values_matched':sourcevalues,'source_radio_banks_matched':8,'source_distractors_matched':distractors,'correct_designations_matched':designations,'correct_designations_missing':1,'source_solutions_exact':15,'source_solutions_absent':1,'authored_unrated_solution':1,'authored_hard_template':1,'sample_counts':counts,'distinct_assessed_tasks':{l:len(s) for l,s in fingerprints.items()},'native':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':0,'binary_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest()},'database_writes':0})
 print('PASS: all 16 source banks/fields, 15 available exact solutions, sampled displayed mathematics, scope/identity and native grading.')
if __name__=='__main__':main()
