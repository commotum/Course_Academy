"""Read displayed equations independently and exercise native radio grading."""
import importlib.util,itertools,json,re,subprocess,sys,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('standard_form',HERE.with_suffix('.py'));p=module('independent_scalar',ROOT/'generate/runs/current/ode-scalar-parser.py');s=g.s
MATH=re.compile(r'\$\$(.*?)\$\$',re.S)
def strip_annotation(t):
 for tag in ('_{⏟}','_{P(x)}','_{Q(x)}'):t=t.replace(tag,'')
 # Underbrace is presentation only. Retain its grouped mathematical argument.
 t=t.replace(r'\underbrace','')
 return t
def expression(t):
 t=re.sub(r'\\(?:dfrac|frac)\s*\{\\(?:textrm|text)\{d\}y\}\s*\{\\(?:textrm|text)\{d\}x\}', 'z', strip_annotation(t)).replace(r'\frac{\text{d}y}{\text{d}x}','z').replace(r'\frac{dy}{dx}','z')
 return p.scalar(t).subs(p.z,g.D)
def equation(t):
 t=t.replace('&','').strip().rstrip('.,').removesuffix(r'\,')
 l,r=t.split('=');return expression(l),expression(r)
def same(a,b):return s.simplify(s.trigsimp(a-b))==0
def equivalent(a,b):return same(g.normalized(a),g.normalized(b))
def fingerprint(q):
 block=re.sub(r'(?:,|\\,|\s)*[xy]\\ne.*','',MATH.findall(q[':question/problem'])[0].split(r'\,,')[0])
 e=equation(block);r=g.normalized(e);P=s.expand(r).coeff(g.y);Q=-r.subs({g.D:0,g.y:0})
 t=None
 for sid,q0 in g.SOURCES.items():
  if str(q.get(':question/id'))==q0[':question/id']:t=sid
 canonical=g.REC[':knowledge-point/canonical-example']
 if str(q.get(':question/id'))==canonical[':question/id']:
  # Canonical only: determine normalized equation directly; its domain is real.
  domain='real x,y'
 else:
  # Domain is a mathematical restriction, inferred from the actual derivative
  # coefficient and rational terms; never a template/seed identity.
  L,R=e;coeff=s.expand(L-R).coeff(g.D)
  if coeff.has(s.cos) and not coeff.has(g.y):
   arg=next(iter(coeff.atoms(s.cos))).args[0];domain='cos('+str(arg).replace(' ','')+') != 0'
  elif (L-R).has(s.cot):domain='sin(x) != 0'
  elif (L-R).has(1/g.x):domain='x != 0'
  elif coeff.has(g.y):domain='y != 0'
  else:domain='real x,y'
 return g.semantic(P,Q,domain)
def native(rec):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':rec['question'][':question/id'],'record':rec,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Source-shaped complete radio bank'} for a in f[':answer-field/choices']]}
def check(rec):
 meta=rec['generation'];level=rec['question'][':question/difficulty'].split('/')[-1]
 assert level in g.LEVELS and meta['template'] in g.FAMILIES[level]
 replay=g.generate(level,meta['seed'],meta['template'],meta['parameters'],meta['bank_profile']);expected=json.loads(json.dumps(rec));expected['generation'].pop('inventory_fingerprint',None);assert replay==expected
 q=rec['question'];prompt=equation(MATH.findall(q[':question/problem'])[0].split(r'\,,')[0]);P=s.expand(g.normalized(prompt)).coeff(g.y);Q=-g.normalized(prompt).subs({g.D:0,g.y:0})
 fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];answers=[equation(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(answers)==5 and len({a[':answer/id'] for a in f[':answer-field/choices']})==5
 good=[g.standard(a) and equivalent(a,prompt) for a in answers];correct=[a[':answer/id']==f[':answer-field/correct'][1] for a in f[':answer-field/choices']]
 assert sum(good)==1 and good==correct
 # Ensure distinct displayed forms even for legitimate equivalent rearrangements.
 assert not any(same(a[0],b[0]) and same(a[1],b[1]) for a,b in itertools.combinations(answers,2))
 blocks=MATH.findall(q[':question/worked-solution']);alignment=next(b for b in blocks if r'\begin{aligned}' in b)
 rows=alignment.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}')[0].split(r'\\')
 assert len(rows)==len(g.data(meta['template'],meta['parameters'])['stages'])
 for row in rows:assert equivalent(equation(row),prompt),(meta,row)
 final=q[':question/worked-solution'].split('Now, the equation',1)[1]
 cp=re.search(r'\$P\(x\)=(.*?)\$',final)[1];cq=re.search(r'\$Q\(x\)=(.*?)\.\$',final)[1]
 assert same(expression(cp),P) and same(expression(cq),Q)
 assert meta['mathematical_fingerprint']==g.semantic(P,Q,meta['domains'])
 return len(rows)
def main():
 report={'source_basis':g.RAW['basis'],'lineage':g.RAW['lineage'],'source_fidelity':{'complete_banks':0,'matched_distractors':0,'total_distractors':0,'banks':[],'excluded_fields':[]},'validation':{}}
 records=[];reviews=[];rows=0
 for t,q in g.SOURCES.items():
  level='hard' if t=='q-16401' else 'easy';r=g.generate(level,template=t,parameters=g.ORIGINAL[t]);rows+=check(r)
  prompt=equation(re.sub(r'(?:,|\\,|\s)*[xy]\\ne.*', '', MATH.findall(q[':question/problem'])[0]));assert equivalent(prompt,equation(MATH.findall(r['question'][':question/problem'])[0].split(r'\,,')[0]))
  for f in q[':question/answer-fields']:
   complete=':answer-field/correct' in f
   old=[equation(a[':answer/value']) for a in f[':answer-field/choices']];new=[equation(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
   matches=[]
   for i,a in enumerate(old):
    candidates=[j for j,b in enumerate(new) if same(a[0],b[0]) and same(a[1],b[1]) and equivalent(a,b)]
    assert len(candidates)==1,(t,f[':db/id'],a,candidates);matches.append(candidates[0])
   assert len(set(matches))==len(old)==len(new)==5
   if complete:
    oc=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id']);assert matches[oc]==g.data(t,g.ORIGINAL[t])['correct']
    report['source_fidelity']['complete_banks']+=1;report['source_fidelity']['matched_distractors']+=4;report['source_fidelity']['total_distractors']+=4
   else:report['source_fidelity']['excluded_fields'].append({'source_id':t,'field_db_id':f[':db/id'],'reason':'Missing correct reference and duplicate selection key; original preserved, omitted from generated response layout','matched_options':5})
   report['source_fidelity']['banks'].append({'source_id':t,'field_db_id':f[':db/id'],'options_matched':5,'complete':complete,'missing':[],'extra':[]})
  # Independently check every original worked-solution equation too.
  aligned=q[':question/worked-solution'].split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
  for row in aligned.split(r'\\'):assert equivalent(equation(row),prompt),(t,row)
  records.append(r);reviews.append('## '+t+'\n\nOriginal:\n\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\nReplayed:\n\n'+g.markdown(r))
 # Parameter boundaries and multiple changed parameters for every complete bank.
 for level,templates in g.FAMILIES.items():
  for t in templates:
   endpoints=[dict(zip(g.ORIGINAL[t],v)) for v in itertools.product(*[(2,5) if t=='q-16400' and k=='a' else (1,5) if t=='q-16400' and k in ('b','c') else (1,8) if t=='q-16400' else (1,6) if k in ('a','n') else (1,4) if t=='q-16401' else (2,8) if t=='q-79699' else (1,8) for k in g.ORIGINAL[t]])]
   for par in endpoints:
    r=g.generate(level,template=t,parameters=par);rows+=check(r);records.append(r)
   for seed in range(4):
    r=g.generate(level,seed,template=t);rows+=check(r);records.append(r)
   reviews.append('## Changed '+t+'\n\n'+g.markdown(records[-1]))
   try:g.generate(level,template=t,parameters={k:0 for k in g.ORIGINAL[t]})
   except ValueError:pass
   else:raise AssertionError('Out-of-domain parameters accepted')
 try:g.generate('moderate')
 except ValueError:pass
 else:raise AssertionError('Unsupported band accepted')
 # Same mathematical task cannot count twice from dependent scaling, seed or IDs.
 a=g.generate('hard',5,parameters={'a':2,'b':2,'n':2});b=g.generate('hard',99,parameters={'a':4,'b':1,'n':2})
 assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 input_path=HERE/'native-input.json';input_path.write_text(json.dumps([native(r) for r in records],indent=2))
 subprocess.run([str(HERE/'check-current-engine'),str(input_path),str(HERE/'native-report.json')],check=True)
 native_report=json.loads((HERE/'native-report.json').read_text());assert native_report['documented_unresolved_checks']==0
 report['validation']={'instances':len(records),'independently_parsed_solution_rows':rows,'all_source_solution_rows_checked':True,'all_supported_profiles_exercised':True,'invalid_parameter_rejection':True,'scaling_alias_rejection':True,'seed_replay':True,'complete_equation_and_standard_form_eligibility_checked':True}
 report['fidelity_notes']=['Source instructional prose and ordered operations preserved. SymPy normalizes mathematical notation and grouping; exact byte/notation fidelity is not claimed. Explicit domains added where division requires them. Empty source math blocks omitted.','The missing-correct duplicate field in q-16400 is evidence only; the other complete field is the supported five-choice bank.','q-16396 and q-79697 wrong-answer transformations have opaque intent. Explicit generalized expressions are labeled hypotheses in extraction; original bank replay matches all values.']
 report['native_engine']=native_report;report['native_engine_sha256']=hashlib.sha256((HERE/'check-current-engine').read_bytes()).hexdigest();report['pass']=True
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(HERE/'review.md').write_text('# Original and generated review\n\n'+'\n\n---\n\n'.join(reviews)+'\n')
 print(json.dumps({'pass':True,'instances':len(records),'source_complete_banks':report['source_fidelity']['complete_banks'],'source_distractors':report['source_fidelity']['matched_distractors'],'solution_rows':rows}))
if __name__=='__main__':main()
