"""Root independently audits scalar graph integrals, not generator metadata."""
import importlib.util,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_scalar_graph_readback',R/'scalar-line-parser.py');g=module('scalar_graph_generator_under_review',D.with_suffix('.py'))
counts={'printed_instances':0,'source_banks':0,'source_values':0,'source_existing_refs':0,'source_missing_refs_derived':0,'source_function_curve_and_bounds':0,'source_full_prose_and_stage_sequences':0,'source_raw_exact_solutions':0,'source_teaching_repairs':0}
def check(r):
 q=r['question'];details=p.prompt(q[':question/problem']);c,answer=p.stages(q[':question/worked-solution'],details,with_value=True);assert answer is not None
 for key,n in c.items():counts[key]=counts.get(key,0)+n
 fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio';choices=f[':answer-field/choices'];vs=[p.scalar(a[':answer/value']) for a in choices];assert len(vs)==5
 good=[p.equal(v,answer) for v in vs];selected=[i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1]];assert len(selected)==1 and sum(good)==1 and good[selected[0]],(q,answer,good)
 assert not [(i,j) for i,v in enumerate(vs) for j,w in enumerate(vs[:i]) if p.equal(v,w)],(q,vs)
 counts['printed_instances']+=1;return q,details,c
def mask(text):return re.sub(r'\s+',' ',p.p.MATH.sub('$MATH$',text)).strip()
sources={key:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] for key in (q[':question/math-academy-id'],q[':db/id'])}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];level=case.get('difficulty') or case.get('level') or old.get(':question/difficulty',{}).get(':db/ident','').rsplit('/',1)[-1];r=g.generate(level,template=case['template'],parameters=case['parameters'],profile=case.get('profile',case.get('bank_profile')));q,details,c=check(r);od=p.prompt(old[':question/problem']);assert p.equal(od[0],details[0]) and p.equal(od[1],details[1]) and all(p.equal(a,b) for a,b in zip(od[3],details[3]));counts['source_function_curve_and_bounds']+=1
 of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0];vs=[p.scalar(a[':answer/value']) for a in nf[':answer-field/choices']]
 for a in of[':answer-field/choices']:
  matches=[i for i,v in enumerate(vs) if p.equal(v,p.scalar(a[':answer/value']))];assert matches,(case['source_id'],a);vs.pop(matches[0]);counts['source_values']+=1
 assert not vs;counts['source_banks']+=1
 selected=next(p.scalar(a[':answer/value']) for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1])
 if of.get(':answer-field/correct'):assert p.equal(selected,p.scalar(of[':answer-field/correct'][':answer/value']));counts['source_existing_refs']+=1
 else:counts['source_missing_refs_derived']+=1
 if old.get(':question/worked-solution'):
  raw=old[':question/worked-solution'];fixed=raw.replace(r'{r}^{′}(u)',r'{r}^{′}(t)').replace('t-(t-4))','t-(t-4)')
  if old[':question/math-academy-id']=='q-76480':fixed=fixed.replace(r'3{x}^{5}{y}^{2}',r'\frac{4{y}^{2}}{{x}^{3}}')
  assert mask(raw)==mask(q[':question/worked-solution']);assert p.stages(fixed,od)==c;counts['source_full_prose_and_stage_sequences']+=1;counts['source_raw_exact_solutions']+=int(raw==q[':question/worked-solution']);counts['source_teaching_repairs']+=int(raw!=fixed)
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
