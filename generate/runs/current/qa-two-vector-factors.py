"""Parent checks actual lattice plots, full coefficient banks and solution stages.

Original geometry additionally reviewed in source-diagrams.png (42 source PNGs).
At replay, source path factors are independently read from printed hence rows;
changed geometry is solved from the linked renderer sidecar, never API answers.
"""
import importlib.util,json,re,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186096652;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('two_vector_parent_scalar',R/'ode-scalar-parser.py');g=module('two_vector_generator',D.with_suffix('.py'));s=p.s
counts=dict(instances=0,complete_values=0,source_fields=0,source_values=0,source_refs=0,source_raw_prompts=0,source_normalized_prompts=0,source_solutions=0,source_assets=0,linked_plot_pairs=0,length_rows=0,hence_rows=0,path_rows=0,coefficient_rows=0)
def same(a,b):return s.expand(a-b)==0
def read(raw,basis):
 raw=raw.strip().strip('$').rstrip('.,');pieces=re.split(r'(\\[A-Za-z]+)',raw)
 return p.scalar(''.join(z if z.startswith('\\') else re.sub('[a-z]',lambda m:str(basis[m[0]]) if m[0] in basis else m[0],z) for z in pieces))
def pair(text):
 a=re.search(r'\\lambda\s*=\s*([^$]+)',text);b=re.search(r'\\mu\s*=\s*([^$]+)',text);assert a and b,text
 return p.scalar(a[1]),p.scalar(b[1])
def imagefree(text):return re.sub(r'!\[\]\(.*?\)','![](ASSET)',text)
def check(record):
 q=record['question'];meta=record['generation'];stem=q[':question/problem'];worked=q[':question/worked-solution']
 target,u,v=re.search(r'([a-z])=\\lambda\s*([a-z])\s*\+\\mu\s*([a-z])',stem).groups();bs={u:p.i,v:p.j}
 hence=re.findall(r'Hence,\s*\$\\overset\{\\to\s*\}\{([A-Z]{2})\}=([^$]+)',worked);assert len(hence)==2,(meta,hence)
 terms=[read(rhs,bs) for _,rhs in hence];combo=s.expand(sum(terms));a,b=combo.coeff(p.i),combo.coeff(p.j);assert combo==a*p.i+b*p.j
 refs=re.findall(r'!\[\]\((.*?)\)',stem+worked);assert len(refs)==2 and all(Path(z).is_file() for z in refs)
 if not meta['plot'].get('reused_original'):
  side=[json.loads(Path(z).with_suffix('.json').read_text()) for z in refs];first=side[0];assert side[1]['solution'] and not first['solution'];assert first['grid_increment']==1
  assert all(float(z).is_integer() for k in ('u','v','target','corner') for z in first[k])
  U,V,T,P=[s.Matrix([s.Integer(z) for z in first[k]]) for k in ('u','v','target','corner')];sol=s.Matrix.hstack(U,V).inv()*T;assert same(sol[0],a) and same(sol[1],b)
  assert all(float(z).is_integer() for arr in (U,V,T,P) for z in arr)
  for key in ('u','v','target','corner','names','segments','path_labels','first_index'):assert first[key]==side[1][key]
  n1,n2=first['segments'];assert n1==hence[0][0] and n2==hence[1][0]
  geom=[P,T-P]
  for term,vec,label in zip(terms,geom,first['path_labels']):
   assert all(same(z,0) for z in s.Matrix.hstack(U,V)*s.Matrix([term.coeff(p.i),term.coeff(p.j)])-vec)
   assert same(read(label,bs),term)
  counts['linked_plot_pairs']+=1
 points={hence[0][0][0]:0,hence[0][0][1]:terms[0],hence[1][0][1]:combo};bs[target]=combo
 def vector(raw):
  saved=[]
  def hold(m):saved.append(points[m[1][1]]-points[m[1][0]]);return 'ZZ'+str(len(saved)-1)+'ZZ'
  raw=re.sub(r'\\overset\{\\to\s*\}\{([A-Z]{2})\}',hold,raw)
  pieces=re.split(r'(\\[A-Za-z]+)',raw);raw=''.join(z if z.startswith('\\') else re.sub('[a-z]',lambda m:str(bs[m[0]]) if m[0] in bs else m[0],z) for z in pieces)
  raw=raw.replace(r'\lambda', '('+str(a)+')').replace(r'\mu','('+str(b)+')')
  for n,val in enumerate(saved):raw=raw.replace('ZZ'+str(n)+'ZZ','('+str(val)+')')
  return p.scalar(raw)
 for seg,rhs in hence:
  assert same(vector(r'\overset{\to }{'+seg+'}'),read(rhs,bs));counts['hence_rows']+=1
 lengths=re.findall(r'\$([A-Z]{2})=([^$]*?)\|([a-z])\|\$',worked);assert len(lengths)==2
 for seg,coeff,name in lengths:
  coeff=coeff.replace(r'\cdot','').strip();mag=p.scalar(coeff) if coeff else s.Integer(1);term=vector(r'\overset{\to }{'+seg+'}');unit=bs[name];assert same(term,mag*unit) or same(term,-mag*unit)
  direction=re.search(r'\$\\overset\{\\to\s*\}\{'+seg+r'\}\$([^\n]+)',worked)[1];positive=same(term,mag*unit)
  assert ('same direction' in direction)==positive and ('opposite direction' in direction)!=positive;counts['length_rows']+=1
 for raw in re.findall(r'\$\$(.*?)\$\$',worked,re.S):
  if r'\lambda =' in raw and r'\mu =' in raw and ',' in raw:continue
  raw=re.sub(r'\\(?:begin|end)\{aligned\}','',raw);carry=None
  for row in raw.split(r'\\'):
   parts=row.replace('&','').strip().rstrip('.,').split('=')
   if len(parts)<2:continue
   if not parts[0].strip():parts[0]=carry
   else:carry=parts[0]
   vals=[vector(z) for z in parts];assert all(same(vals[0],z) for z in vals[1:]),(meta,row,vals);counts['path_rows']+=len(vals)-1
 final=re.findall(r'\\(lambda|mu)\s*=\s*(-?\\frac\{\d+\}\{\d+\}|-?\d+(?:\.\d+)?)',worked);assert len(final)>=2
 for name,value in final:assert same(p.scalar(value),a if name=='lambda' else b)
 counts['coefficient_rows']+=len(final)
 for f in q[':question/answer-fields']:
  if f[':answer-field/type'].endswith('/radio'):
   vals=[pair(z[':answer/value']) for z in f[':answer-field/choices']];good=[same(x,a) and same(y,b) for x,y in vals];assert sum(good)==1 and len(set(vals))==len(vals)
  else:
   tail=stem.split('{{'+f[':answer-field/key']+'}}')[0];name=re.findall(r'\\(lambda|mu)',tail)[-1];want=a if name=='lambda' else b;vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];good=[same(z,want) for z in vals];assert all(good)
  correct=next(i for i,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1]);assert good[correct];counts['complete_values']+=len(vals)
 if meta['authored']:
  level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':assert a>0 and b>0 and a.q==b.q==1
  elif level=='moderate':assert a<0 or b<0 or a.q>1 or b.q>1
  else:assert a.q>1 and b.q>1 and max(abs(a),abs(b))<4
 counts['instances']+=1;return q
sources={q[':question/id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=sources[c['source_id']];q=check(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']))
 counts['source_raw_prompts']+=int(imagefree(q[':question/problem'])==imagefree(old[':question/problem']))
 oldprompt=old[':question/problem']
 if c['math_academy_id']=='q-275128':oldprompt=oldprompt.replace('$-\\frac{1}{2}$','{{field-1}}').replace('$-\\frac{5}{2}$','{{field-2}}')
 assert imagefree(q[':question/problem'])==imagefree(oldprompt)
 counts['source_normalized_prompts']+=1
 assert imagefree(q[':question/worked-solution'])==imagefree(old[':question/worked-solution']);counts['source_solutions']+=1
 for f,nf in zip(old[':question/answer-fields'],q[':question/answer-fields']):
  readval=pair if nf[':answer-field/type'].endswith('/radio') else p.scalar;vals=[readval(z[':answer/value']) for z in nf[':answer-field/choices']]
  original=[readval(z[':answer/value']) for z in f[':answer-field/choices']];assert sorted(map(str,vals))==sorted(map(str,original));correct=readval(next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]));assert correct==readval(f[':answer-field/correct'][':answer/value']);counts['source_refs']+=1;counts['source_fields']+=1;counts['source_values']+=len(original)
 for ref in re.findall(r'!\[\]\((.*?)\)',old[':question/problem']+old[':question/worked-solution']):
  copied=next(Path(z) for z in re.findall(r'!\[\]\((.*?)\)',q[':question/problem']+q[':question/worked-solution']) if Path(z).name==Path(ref).name)
  origin=Path('/media/jake/SSD/EDB/math')/ref;assert copied.read_bytes()==origin.read_bytes();counts['source_assets']+=1
for r in json.loads((D/'review.json').read_text()):check(r.get('record',r))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
