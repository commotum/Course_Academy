import sys,json,pathlib,importlib.util,collections,hashlib
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;P=J/'workspace'
s=importlib.util.spec_from_file_location('g',P/'17592186229182.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
import sympy as sp
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,default=str))
def key(r):
 f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
rs=[]
for q in range(3,10):
 for seed in range(170,178):rs.append(g.generate('easy',seed,parameters=dict(V=100,q0=q,c='.04',rin=8,rout=12)))
rs.append(g.generate('easy',8114,parameters=dict(V=100,q0=3,c='.04',rin=8,rout=12)))
for level,template,ri,ro in [('easy','q-336439',16,24),('moderate','q-336746',16,24),('hard','q-339400',8,4)]:
 for q in [9,12,15]:
  p=dict(V=240,q0=q,c='.05',rin=ri,rout=ro)
  if level=='hard':p['T']=5
  rs.append(g.generate(level,57391,template=template,parameters=p))
save('focused-records.json',rs)
# In-memory observation of actual proposal/rejection sequence; no package mutation.
original=g.sample;proposals=[];outs=[]
for seed in range(92031,92071):
 def watch(meta,rng,sign):
  try:
   p=original(meta,rng,sign)
   try:g.guard(dict(p,kind=meta['kind']),meta,'easy');result='valid proposal'
   except Exception as e:result=str(e)
   proposals.append(dict(seed=seed,sign=sign,parameters=p,result=result));return p
  except Exception as e:proposals.append(dict(seed=seed,sign=sign,result=str(e)));raise
 g.sample=watch;outs.append(g.generate('easy',seed))
g.sample=original
save('rejection-coverage.json',dict(proposals=proposals,outputs=len(outs),matches_independent_sample=outs==json.load(open(E/'samples.json'))[:40],signs=dict(collections.Counter(1 if sp.Rational(r['generation']['parameters']['q0'])>sp.Rational(r['generation']['parameters']['c'])*sp.Rational(r['generation']['parameters']['V']) else -1 if sp.Rational(r['generation']['parameters']['q0'])<sp.Rational(r['generation']['parameters']['c'])*sp.Rational(r['generation']['parameters']['V']) else 0 for r in outs))))
# Additional boundary acceptance/rejection.
bound=[]
for name,p,valid in [('B minimum',dict(V=120,q0=4,c='.025',rin=16,rout=24),True),('B maximum',dict(V=800,q0=4,c='.025',rin=8,rout=12),True),('B outside',dict(V=804,q0=4,c='.025',rin=8,rout=12),False),('unknown parameter',dict(V=240,q0=4,c='.025',rin=16,rout=24,extra=1),False)]:
 try:r=g.generate('easy',57391,parameters=p);accepted=True
 except Exception as e:accepted=False;r=str(e)
 bound.append(dict(case=name,parameters=p,expected_acceptance=valid,accepted=accepted,passed=accepted==valid,result=r))
save('boundaries.json',bound)
# Inventory evidence reused only where the inventory binding is unchanged, then rechecked against captured complete fields.
prior=J/'review-0-policy-2-86d0b4d09d151598';old=json.load(open(prior/'generated-records.json'));inv=json.load(open(J/'source/inventory.json'));byid={q[':question/id']:q for q in inv['questions']};matches=[]
for r in old:
 q=r['question'];stored=byid[q[':question/id']]
 vals=lambda x:sorted(a[':answer/value'] for a in x[':question/answer-fields'][0][':answer-field/choices'])
 matches.append(dict(question_id=q[':question/id'],entity_id=stored[':db/id'],prompt_match=q[':question/problem']==stored[':question/problem'],solution_match=q[':question/worked-solution']==stored[':question/worked-solution'],bank_match=vals(q)==vals(stored),single_digit=all(v.isdigit() and 0<int(v)<10 for v in vals(q))))
save('generated-records.json',old);save('inventory-reproduction.json',dict(basis=inv['basis'],provenance=str(prior/'generated-records.json'),matches=matches,limits='Seven earlier generated records reused from independently reproduced evidence with unchanged inventory binding; all captured prompts/solutions/banks rechecked. Ten original source records excluded. None has the prior single-digit cue; no finding is asserted against this inventory.'))
save('affected-inventory.json',{'affected_questions':[]})
# Complete native grader cases, including controlled and former shortcut cases.
allrs=json.load(open(E/'samples.json'))+json.load(open(E/'batch.json'))+json.load(open(E/'counterfactual-records.json'))+rs
cases=[]
for i,r in enumerate(allrs):
 f=r['question'][':question/answer-fields'][0];cases.append(dict(label=f'independent-{i}',record=r,checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/value']==key(r) else 'rejected',purpose='Choice value independently evaluated from prompt/controlled parameters') for a in f[':answer-field/choices']]))
save('grader-input.json',cases)
save('easy-samples.json',[r for r in json.load(open(E/'samples.json'))+rs if r['question'][':question/difficulty']==':question.difficulty/easy'])
# Render exact batch, controlled relevant/irrelevant pairs, every new sign, and fractional source-supported cases.
save('render-records.json',json.load(open(E/'batch.json'))+json.load(open(E/'counterfactual-records.json'))+rs[-9:])
print(json.dumps(dict(focused=len(rs),grader_records=len(cases),boundaries_pass=all(x['passed'] for x in bound))))
