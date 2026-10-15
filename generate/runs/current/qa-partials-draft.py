import sys
sys.dont_write_bytecode=True
import json,re,hashlib,copy,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186124639;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
reader=load('parent_partial_point_helpers',R/'qa-partial-point-draft.py');math=reader.math;s=reader.s;p=reader.p;same=reader.same;prose=reader.prose
counts={'records':0,'choices':0,'solution_stages':0,'individual_derivative_operands':0,'source_banks':0,'source_values':0,'source_keys':0,'source_missing_keys':0,'source_prose_sequences':0,'authored_hard_banks':0}
def question(q):
 islands=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$',q[':question/problem'],re.S)
 assert len(islands)==2
 ask,formula=islands;mt=re.search(r'(?:∂|\\partial)\s*([xy])',ask) or re.search(r'_\{?([xy])\}?',ask);assert mt
 return math(formula.split('=',1)[1].rstrip('.,')),getattr(p,mt[1] or mt[2])
def rows(text):
 group=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S);assert group
 out=[]
 for row in group[1].split(chr(92)*2):
  lhs,rhs=row.split('&',1);assert rhs.strip().startswith('=');out.append((lhs.strip(),rhs.strip()[1:].strip()))
 assert len(out)==5
 return out

def check(record):
 q=record['question'];F,var=question(q);C=s.diff(F,var);f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio'
 values=[math(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5
 for i,a in enumerate(values):assert all(not same(a,b) for b in values[:i])
 good=[same(z,C) for z in values];assert sum(good)==1
 if ':answer-field/correct' in f:assert good[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])]
 if ':question/worked-solution' in q:
  text=q[':question/worked-solution'];st=rows(text)
  assert 'with respect to $'+str(var)+',$' in text
  for lhs,rhs in st:assert same(math(rhs),C),(rhs,F,var,C)
  operands=list(math(st[1][1]).atoms(s.Derivative));assert len(operands)==len(s.Add.make_args(F))
  assert all(d.variables==(var,) for d in operands)
  terms=s.Add.make_args(F)
  for d in operands:assert sum(same(d.expr,t) or same(-d.expr,t) for t in terms)==1,(F,d)
  # Extraction must preserve the same differentiation variable and a held-only factor.
  ex=math(st[2][1]);assert len(ex.atoms(s.Derivative))==len(operands)
  counts['individual_derivative_operands']+=len(operands);counts['solution_stages']+=5
  count=reader.individual_stages(F,var,st[1:4]);counts['individual_operative_contributions']=counts.get('individual_operative_contributions',0)+count
 if q.get(':question/difficulty')==':question.difficulty/hard':
  held=p.y if var==p.x else p.x;terms=s.Add.make_args(F);assert len(terms)==3
  funcs=[node.func for node in s.preorder_traversal(F) if node.func in (s.log,s.exp,s.sin,s.atan)]
  assert sorted(str(f) for f in funcs) in (sorted(['log','exp']),sorted(['sin','atan']))
  reciprocal=[t for t in terms if t.as_powers_dict().get(var,s.Integer(0))<0];assert len(reciprocal)==1
  ds=[s.diff(t,var) for t in terms];expected=[C]
  rec=reciprocal[0];Rr=s.diff(rec,var);expected.append(C-2*Rr)
  primitive=[t for t in terms if any(node.func in (s.log,s.sin) for node in s.preorder_traversal(t))];assert len(primitive)==1
  T=primitive[0];expected.append(C-s.diff(T,var)+T)
  expatan=[t for t in terms if any(node.func in (s.exp,s.atan) for node in s.preorder_traversal(t))];assert len(expatan)==1
  E=expatan[0];heldfactor=E.as_independent(var,as_Add=False)[0];expected.append(C-s.diff(E,var)+s.diff(E,var)/held)
  expected.append(s.diff(F,held));assert all(sum(same(a,b) for b in expected)==1 for a in values)
  counts['authored_hard_banks']+=1
 counts['records']+=1;counts['choices']+=5

if __name__=='__main__':
 g=load('parent_partials_generation',D.with_suffix('.py'));source=json.loads((R/'refresh-2026-10-14/sources'/f'{K}.json').read_text());assert source==json.loads((D/'source.json').read_text());originals={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 for case in json.loads((D/'source-cases.json').read_text()):
  old=originals[case['source_id']];r=g.generate(case.get('difficulty',case.get('level')),template=case['template'],parameters=case['parameters'],profile='raw');q=r['question'];check(r)
  oldF,oldvar=question(old);F,var=question(q);assert same(oldF,F) and oldvar==var and prose(old[':question/problem'])==prose(q[':question/problem'])
  of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0];remaining=[math(z[':answer/value']) for z in nf[':answer-field/choices']]
  for z in of[':answer-field/choices']:
   ids=[i for i,a in enumerate(remaining) if same(a,math(z[':answer/value']))];assert len(ids)==1;remaining.pop(ids[0]);counts['source_values']+=1
  assert not remaining;counts['source_banks']+=1
  if ':answer-field/correct' in of:
   ans=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]);assert same(math(ans),math(of[':answer-field/correct'][':answer/value']));counts['source_keys']+=1
  else:assert ':answer-field/correct' not in nf;counts['source_missing_keys']+=1
  assert (':question/worked-solution' in old)==(':question/worked-solution' in q)
  if ':question/worked-solution' in old:
   assert prose(old[':question/worked-solution'])==prose(q[':question/worked-solution'])
   for (_,a),(_,b) in zip(rows(old[':question/worked-solution']),rows(q[':question/worked-solution'])):assert same(math(a),math(b))
   counts['source_prose_sequences']+=1
 samples=json.loads((R/'qa'/f'{K}-sampled.json').read_text())
 for z in samples:check(z)
 # Include both targets at otherwise held mathematical data in every declared family.
 for name,(sid,level,anchor) in g.SPECS.items():
  for target in ('x','y'):
   pars=dict(anchor,target=target);check(g.generate(level,template=name,parameters=pars))
 mutant=copy.deepcopy(samples[0]);text=mutant['question'][':question/worked-solution'];bad=rows(text)[-2][1];mutant['question'][':question/worked-solution']=text.replace(bad,'('+bad+')+1',1);saved=copy.deepcopy(counts)
 try:check(mutant)
 except AssertionError:pass
 else:raise AssertionError('Wrong intermediate derivative survived')
 counts=saved;counts.update(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),unchanged_key_wrong_intermediate_rejected=True,database_writes=0)
 (R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
