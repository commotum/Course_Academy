"""Independent actual-prompt, complete-bank and ordered-stage polar-chain audit."""
import importlib.util,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=R.parents[2]/f'generate/scratch/{K}'
direction={17592186124594:'forward',17592186124595:'inverse',17592186124596:'cylindrical'}[K]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('independent_polar_reader',R/'polar-chain-parser.py');g=module('reviewed_polar_generator',D.with_suffix('.py'))
counts={'printed_instances':0,'source_banks':0,'source_values':0,'source_existing_refs':0,'source_missing_refs_derived':0,'source_function_and_target_matches':0,'source_prose_and_stage_sequences':0,'source_raw_exact_solutions':0,'source_label_repaired_solutions':0}
def check(r):
 q=r['question'];details=p.question(q[':question/problem'],direction);fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio';vs=[p.scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vs)==5
 good=[p.equal(v,details[5]) for v in vs];selected=[i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]]
 assert len(selected)==1 and good[selected[0]] and sum(good)==1,(q,good)
 assert not [(i,j) for i,v in enumerate(vs) for j,w in enumerate(vs[:i]) if p.equal(v,w)],(q,vs)
 c=p.stages(q[':question/worked-solution'],details,direction)
 for key,n in c.items():counts[key]=counts.get(key,0)+n
 counts['printed_instances']+=1;return q,details,c
def mask(text):return re.sub(r'\s+',' ',p.MATH.sub('$MATH$',text)).strip()
def repair(qid,text):
 if qid=='q-94999':text=text.replace('∂g','∂h')
 if qid in ('q-95113','q-95116'):
  # Only the mislabeled first converted Cartesian partial, not its RHS.
  anchor='Writing the above results';before,after=text.split(anchor,1);after=after.replace(r'\frac{∂'+('g' if qid=='q-95113' else 'w')+r'}{∂y}',r'\frac{∂'+('g' if qid=='q-95113' else 'w')+r'}{∂x}',1);text=before+anchor+after
 if qid=='q-165282':
  # Last answer row is a y derivative; preceding coordinate partials are correct.
  pos=text.rfind('Then,');assert pos>=0;text=text[:pos]+text[pos:].replace(r'\frac{∂h}{∂x}',r'\frac{∂h}{∂y}')
 if qid=='q-95172':text=text.replace(r'\frac{∂v}{∂y}\cdot \frac{∂v}{∂\theta }',r'\frac{∂v}{∂y}\cdot \frac{∂y}{∂\theta }')
 return text
sources={key:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] for key in (q[':question/math-academy-id'],q[':db/id'])}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];difficulty=case.get('difficulty') or case.get('level') or case.get('authored_level_assignment') or old.get(':question/difficulty',{}).get(':db/ident','').rsplit('/',1)[-1];assert difficulty
 r=g.generate(difficulty,template=case['template'],parameters=case['parameters'],profile=case.get('profile',case.get('bank_profile')));q,details,c=check(r)
 od=p.question(old[':question/problem'],direction);assert od[0]==details[0] and od[2]==details[2] and p.equal(od[1],details[1]);counts['source_function_and_target_matches']+=1
 of=old[':question/answer-fields'][case.get('raw_field_index',0)];nf=q[':question/answer-fields'][0];vs=[p.scalar(a[':answer/value']) for a in nf[':answer-field/choices']]
 for a in of[':answer-field/choices']:
  matches=[i for i,v in enumerate(vs) if p.equal(v,p.scalar(a[':answer/value']))];assert matches,(case,a);vs.pop(matches[0]);counts['source_values']+=1
 assert not vs;counts['source_banks']+=1
 selected=next(p.scalar(a[':answer/value']) for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1])
 if of.get(':answer-field/correct'):assert p.equal(selected,p.scalar(of[':answer-field/correct'][':answer/value']));counts['source_existing_refs']+=1
 else:counts['source_missing_refs_derived']+=1
 if old.get(':question/worked-solution'):
  raw=old[':question/worked-solution'];fixed=repair(old[':question/math-academy-id'],raw);new=q[':question/worked-solution'];assert mask(raw)==mask(new),(case,mask(raw),mask(new));sc,ss=p.stages(fixed,od,direction,sequence=True);nc,ns=p.stages(new,details,direction,sequence=True);assert sc==c==nc and len(ss)==len(ns)
  for (a,b),(x,y) in zip(ss,ns):assert p.equal(a,x) and p.equal(b,y),(case,a,b,x,y)
  counts['source_prose_and_stage_sequences']+=1;counts['source_raw_exact_solutions']+=int(raw==new);counts['source_label_repaired_solutions']+=int(raw!=fixed)
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
