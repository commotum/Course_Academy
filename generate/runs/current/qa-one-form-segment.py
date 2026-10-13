"""Root checks actual endpoints, every interpolation row, whole choices and pullback stages."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186179728;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('parent_segment_math',R/'one-form-parser.py');g=module('parent_segment_generator',D.with_suffix('.py'))
counts={'printed_instances':0,'source_prompts':0,'raw_exact_solutions':0,'minimally_repaired_solutions':0,'source_banks':0,'source_values':0,'source_designations':0,'endpoint_interpolation_definitions':0,'scalar_bank_values':0}
def value(text):return p.scalar(text.replace('\\\\','\\'))
def check(r):
 q=r['question'];P,Q=p.oneform(q[':question/problem']);path,lim,points,n=p.segment(q[':question/problem'],q[':question/worked-solution']);counts['endpoint_interpolation_definitions']+=n;f=p.evaluate_form(P,Q,path);I=s.integrate(f,(p.t,*lim));field=q[':question/answer-fields'][0];assert len(field[':answer-field/choices'])==5
 values=[value(a[':answer/value']) for a in field[':answer-field/choices']];counts['scalar_bank_values']+=len(values)
 assert all(not p.equivalent(v,w) for i,v in enumerate(values) for w in values[:i]),values
 selected=[v for a,v in zip(field[':answer-field/choices'],values) if a[':answer/id']==field[':answer-field/correct'][1]];assert len(selected)==1 and p.equivalent(selected[0],I),(q[':question/problem'],selected,I)
 for key,n in p.stages(q[':question/worked-solution'],P,Q,path,lim).items():counts[key]=counts.get(key,0)+n
 if r['generation']['origin']=='authored':
  block=next(b for b in p.blocks(q[':question/worked-solution']) if r'\int' in b and '=' in b);rows=re.split(r'\\\\\s*&?\s*=',p.clean(block));F,a,b=p.primitive(rows[-4]);components=rows[-2].replace(r'\left','').replace(r'\right','').strip();upper,j=p.group(components,0);assert components[j]=='-';lower,k=p.group(components,j+1);assert not components[k:].strip()
  def parts(body):
   vals=[];j=0
   while j<len(body):
    raw,k=p.group(body,j);vals.append(p.scalar(raw));j=k
    if j<len(body):assert body[j]=='+';j+=1
   return vals
  terms=[c*p.t**power[0] for power,c in s.Poly(F,p.t).terms()]
  for body,u in ((upper,b),(lower,a)):
   values=parts(body);assert len(values)==len(terms) and all(p.equivalent(v,z.subs(p.t,u)) for v,z in zip(values,terms)),(body,terms,u)
  counts['separate_endpoint_component_rows']=counts.get('separate_endpoint_component_rows',0)+1
 if q[':question/difficulty'].endswith(('/moderate','/hard')):
  assert all(z!=0 for z in points[0]);assert all(z!=0 for z in (s.diff(path[0],p.t),s.diff(path[1],p.t)));assert s.Poly(f,p.t).degree()==3
  assert s.Poly(P,p.x,p.y).total_degree()==3 and s.Poly(Q,p.x,p.y).total_degree()==(3 if q[':question/difficulty'].endswith('/hard') else 2)
 counts['printed_instances']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];r=g.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=check(r);assert q[':question/problem']==old[':question/problem'];counts['source_prompts']+=1
 sol=old[':question/worked-solution'];fixed=sol.replace(r'4[\frac{4}{3}+10]',r'4[\frac{4}{3}+1]');assert q[':question/worked-solution']==fixed,(case['source_id'],q[':question/worked-solution'],fixed);counts['raw_exact_solutions']+=sol==fixed;counts['minimally_repaired_solutions']+=1
 field=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0];remaining=[value(a[':answer/value']) for a in nf[':answer-field/choices']]
 for a in field[':answer-field/choices']:
  matches=[i for i,v in enumerate(remaining) if p.equivalent(v,value(a[':answer/value']))];assert len(matches)==1;remaining.pop(matches[0]);counts['source_values']+=1
 assert not remaining;counts['source_banks']+=1;nc=next(value(a[':answer/value']) for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert p.equivalent(nc,value(field[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
