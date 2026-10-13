"""Parent checks printed other-base formula applications and full banks."""
import importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186096612;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_other_base_readback',R/'exponential-readback.py');g=module('reviewed_other_base_generator',D.with_suffix('.py'))
counts=dict(printed_instances=0,complete_values=0,source_banks=0,source_values=0,source_existing_refs=0,source_missing_refs_derived=0,source_raw_solution_matches=0,source_prompts_exact=0,raw_formal_operator_repair_instances=0,legacy_wrong_blank_alias_instances=0)
def value(raw):return p.scalar(raw.split('=',1)[-1])
def check(r):
 q=r['question'];meta=r['generation'];name,F,point=p.function_and_point(q[':question/problem']);exponentials=[]
 for node in p.s.preorder_traversal(F):
  if isinstance(node,p.s.Pow) and node.exp.has(p.x):assert node.exp==p.x and node.base.is_number and node.base>1;exponentials.append(node)
  elif node.func==p.s.exp:assert node.args[0]==p.x
 assert exponentials and p.s.expand(F-sum(F.coeff(v)*v for v in exponentials)-F.coeff(p.s.exp(p.x))*p.s.exp(p.x)).is_polynomial(p.x)
 if meta['template']=='two_bases_rate':assert len(exponentials)==2 and point in (-2,-1,1,2)
 df=p.s.diff(F,p.x);expected=df if point is None else df.subs(p.x,point);f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 vals=[value(v[':answer/value']) for v in f[':answer-field/choices']];good=[p.p.equal(v,expected) for v in vals]
 if f[':answer-field/type']==':answer-field.type/radio':
  assert sum(good)==1
  for n,A in enumerate(vals):
   for B in vals[:n]:assert not p.p.equal(A,B),(q,A,B)
 else:
  assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  if meta['template']=='cubic_rate_blank' and meta['profile'] in ('observed','raw_source'):
   assert len(vals)==2 and sum(good)==1 and any(p.p.equal(v,df) for v in vals);counts['legacy_wrong_blank_alias_instances']+=1
  else:assert all(good)
 assert good[next(n for n,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])]
 worked=q[':question/worked-solution']
 if meta['profile'] in ('observed','raw_source') and meta['template']=='natural_rate_radio':
  assert worked.count(r'\frac{\text{d}y}{\text{d}x}')==2;worked=worked.replace(r'\frac{\text{d}y}{\text{d}x}',r'\frac{\text{d}}{\text{d}x}');counts['raw_formal_operator_repair_instances']+=1
 else:assert r'\frac{\text{d}y}{\text{d}x}' not in worked
 stages=p.stages(worked,F,point);assert stages['derivative_rows']>=4 and stages['operator_rows']>=2;assert (stages['evaluation_rows']>=3)==(point is not None)
 for key,n in stages.items():counts[key]=counts.get(key,0)+n
 counts['printed_instances']+=1;counts['complete_values']+=len(vals);return q
sources={key:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] for key in (q[':question/math-academy-id'],q[':db/id'],q[':question/id'])}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['profile']);q=check(r);of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
 assert q[':question/problem']==old[':question/problem'];counts['source_prompts_exact']+=1
 remaining=[value(a[':answer/value']) for a in nf[':answer-field/choices']]
 for a in of[':answer-field/choices']:
  A=value(a[':answer/value']);index=next(k for k,B in enumerate(remaining) if p.p.equal(A,B));remaining.pop(index)
 assert not remaining
 if of.get(':answer-field/correct'):
  A=value(of[':answer-field/correct'][':answer/value']);B=value(next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]));assert p.p.equal(A,B);counts['source_existing_refs']+=1
 else:counts['source_missing_refs_derived']+=1
 if old.get(':question/worked-solution'):assert old[':question/worked-solution']==q[':question/worked-solution'];counts['source_raw_solution_matches']+=1
 counts['source_banks']+=1;counts['source_values']+=len(of[':answer-field/choices'])
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['source_formal_operator_error']='q-17388 two dy/dx used as d/dx';counts['source_wrong_blank_alias']='q-340280 full derivative is not scalar slope';counts['source_widget_duplicate']='q-11732 five historic UI slots correspond to four unique captured EDB values';counts['database_writes']=0
(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
