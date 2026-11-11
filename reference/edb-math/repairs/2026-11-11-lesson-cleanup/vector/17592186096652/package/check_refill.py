"""Package-bound actual survivor checks: exact math, no supplied path, own-tip labels."""
import argparse,hashlib,json,os,re,tempfile
from pathlib import Path
from fractions import Fraction as F
import generator

def enum(x):return x.get(':db/ident') if isinstance(x,dict) else x
def answer_id(x):return x[-1] if isinstance(x,list) else x.get(':answer/id') if isinstance(x,dict) else x

def fingerprint(q):
 result={k:q[k] for k in [':question/problem',':question/requires-calculator'] if k in q};fields=[]
 for f in q[':question/answer-fields']:
  a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==answer_id(f[':answer-field/correct']))
  row={':answer-field/key':f[':answer-field/key'],':answer-field/type':enum(f[':answer-field/type']),':answer-field/correct':{':answer/type':enum(a[':answer/type']),':answer/value':a[':answer/value']}}
  if enum(f[':answer-field/type']) not in [':answer-field.type/blank',':answer-field.type/free']:row[':answer-field/choices']=sorted([{':answer/type':enum(a[':answer/type']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:json.dumps(a,sort_keys=True))
  fields.append(row)
 result[':question/answer-fields']=sorted(fields,key=lambda f:f[':answer-field/key'])
 return hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def number(x):
 x=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'\1/\2',x.replace('$','').strip())
 return F(x)
def coeffs(text):
 text=text.split('=')[-1];text=re.sub(r'\\mathbf\s*\{([a-z])\}',r'\1',text);text=re.sub(r'\\mathbf\s+([a-z])',r'\1',text);text=text.replace(' ','').strip('$.,')
 pattern=r'([+-]?)(\\(?:d?frac)\{\d+\}\{\d+\}|\d+(?:\.\d+)?(?:/\d+)?)?([a-z])';found=list(re.finditer(pattern,text));assert ''.join(m[0] for m in found)==text,text
 return {m[3]:(-1 if m[1]=='-' else 1)*number(m[2] or '1') for m in found}
def solve(a,b,c):
 a,b,c=[list(map(F,v)) for v in [a,b,c]];det=a[0]*b[1]-a[1]*b[0];assert det
 return [(c[0]*b[1]-c[1]*b[0])/det,(a[0]*c[1]-a[1]*c[0])/det]
def expected(kp,rec):
 g=rec['generation'];q=rec['question'];p=g.get('parameters',g.get('instance'));prompt=q[':question/problem']
 if kp==17592186096652:
  values=solve(p['u'],p['v'],p['target']);assert values==[F(p['a']),F(p['b'])]
  assert r'\mathbf{c}=\lambda\mathbf{a}+\mu\mathbf{b}' in prompt
  assert not re.search(r'route|dashed|O\\to|\\overrightarrow\{[AX]C\}',prompt)
  return values
 if kp==17592186096653:
  m=re.search(r'([A-Z])([A-Z]):\2([A-Z])=(\d+):(\d+)',prompt);assert m
  A,X,B,r,s=m.groups();r,s=int(r),int(s);assert (A,B,X,r,s)==tuple(p[k] for k in ['A','B','X','r','s'])
  givens=re.findall(r'\\overrightarrow\{([A-Z]{2})\}=([a-z])',prompt)[:2];assert len(givens)==2
  signs=[]
  for (edge,name),point,var in zip(givens,[A,B],[p['u'],p['v']]):
   assert name==var;signs.append(1 if edge=='O'+point else -1 if edge==point+'O' else None)
  assert None not in signs
  requested=re.search(r'Express \$\\overrightarrow\{([A-Z]{2})\}',prompt)[1];target=1 if requested=='O'+X else -1 if requested==X+'O' else None;assert target
  return [F(s,r+s)*signs[0]*target,F(r,r+s)*signs[1]*target]
 if kp==17592186096701:
  values=solve(p['a'],p['b'],p['c']);known='b' if p['unknown']=='a' else 'a';assert values[['a','b'].index(known)]==F(p['known'])
  assert values[['a','b'].index(p['unknown'])]==F(p['scalar'])
  # Check every stored intermediate displacement independently.
  origin=[F(p['known'])*F(x) for x in p[known]];assert origin==list(map(F,p['p']))
  assert [F(c)-o for c,o in zip(p['c'],origin)]==list(map(F,p['residual']))
  return [values[['a','b'].index(p['unknown'])]]
 if kp==17592186235285:
  a,b=list(map(F,p['a'])),list(map(F,p['b']));c=[F(p['k'])*b[i]-F(p['r'])*a[i] for i in (0,1)];return [solve(a,b,c)[0]]

CHECK_IDS=['vector-geometry-and-endpoints', 'independent-two-blank-task', 'target-provenance', 'endpoint-label-association']

def check(r,out):

 import check_prior
 check_prior.assess(r)
 kp=generator.KP['db_id'];q=r['question'];g=r['generation'];p=g.get('instance',g.get('parameters'));values=expected(kp,r);prompt=q[':question/problem'];solution=q[':question/worked-solution']
 assert not re.search(r'compare its legs|following the drawn|path is drawn|OX.?=.?.?OA|AB.?=.?.?b',prompt,re.I),'Prompt supplies assessed route'
 assert not set(map(str,g.get('source_ids',[]))) & {'q-275128','17592186292807','17592186097046','17592186097240'}
 checks=[];fields=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key'])
 for i,f in enumerate(fields):
  correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==answer_id(f[':answer-field/correct']))
  if kp==17592186096653 and enum(f[':answer-field/type'])==':answer-field.type/radio':
   assert coeffs(correct[':answer/value'])=={p['u']:values[0],p['v']:values[1]}
   assert not re.search(r'\\overrightarrow\{O'+p['X']+r'\}=\\overrightarrow\{O'+p['A'],prompt),'Prompt supplies endpoint path'
  else:
   value=values[i] if len(values)>1 else values[0];assert number(correct[':answer/value'])==value,'Key disagrees with independent exact math'
   if enum(f[':answer-field/type'])==':answer-field.type/blank':
    fi=q[':question/answer-fields'].index(f)
    checks.extend([dict(field_index=fi,submitted=f'{2*value.numerator}/{2*value.denominator}',expected='accepted',control='equivalent',purpose='Independent exact rational with no reduction requirement'),dict(field_index=fi,submitted=str(-value),expected='rejected',control='wrong',purpose='Opposite nonzero signed coefficient')])
 if kp in [17592186096652,17592186096701]:
  os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(out)
  if kp==17592186096652:
   from diagram import render
   files={}
   for role in ['prompt','solution']:
    path=out/(role+'.png');render(p,path,role=='solution');files[role]=path
  else:
   exact=generator.instance(p['a'],p['b'],p['unknown'],p['known'],p['scalar'],p['profile'])
   files={role:out/generator.diagram(exact,role=='solution',out) for role in ['prompt','solution']}
  for role,text in [('prompt',prompt),('solution',solution)]:
   refs=re.findall(r'!\[[^]]*\]\(([^)]+)\)',text);assert len(refs)==1
   sha=hashlib.sha256(files[role].read_bytes()).hexdigest();assert refs[0].endswith(files[role].name) or refs[0]==f'images/{sha[:2]}/{sha}.png','Incorrect diagram role or changed geometry/renderer'
   witness=json.loads(files[role].with_suffix('.json').read_text());labels=witness['labels'];assert {x['symbol'] for x in labels}=={'a','b','c'}
   points={'a':p['u'],'b':p['v'],'c':p['target']} if kp==17592186096652 else {k:p[k] for k in ['a','b','c']}
   for label in labels:
    assert list(map(F,label['arrow_endpoint']))==list(map(F,points[label['symbol']])),'Callout bound to wrong arrow'
    assert list(map(F,label['leader_xy']))==list(map(F,points[label['symbol']])),'Leader misses own endpoint'
    assert label['font_points']>=17 and label['score']<1000,'Unreadable or colliding callout'
 return checks

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--records',required=True);ap.add_argument('--inventory',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();rows=json.loads(Path(a.records).read_text());native=[]
 with tempfile.TemporaryDirectory(prefix='vector-reviewed-refill-') as temporary:
  for i,r in enumerate(rows):
   d=Path(temporary)/str(i);d.mkdir();checks=check(r,d)
   if checks:native.append(dict(fingerprint=fingerprint(r['question']),checks=checks))
 covered=sorted(fingerprint(r['question']) for r in rows)
 Path(a.output).write_text(json.dumps(dict(status='passed',checked_fingerprints=covered,check_results=[dict(id=x,status='passed',checked_fingerprints=covered) for x in CHECK_IDS],native_checks=native),indent=2)+'\n')
