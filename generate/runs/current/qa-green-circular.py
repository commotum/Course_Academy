"""Root pointwise missing-integrand criterion, full source banks/stages/plots."""
import re,json,hashlib,importlib.util,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186176024;D=ROOT/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);sys.modules[name]=m;z.loader.exec_module(m);return m
base=load(R/'qa-parametric-scalar-line.py','scalarbase');p=base.p;x,y=p.p.x,p.p.y;r,theta=p.p.u,p.p.v
C={k:0 for k in ('records','cross_partials','cartesian_curl_rows','polar_rows','complete_choices','whole_banks','circle_equations','plot_sidecars','raw_prompts','raw_solutions','raw_choices','literal_raw_choices','raw_banks','raw_designations','raw_missing_designations','raw_missing_ratings')}
def scalar(raw):
 raw=raw.replace('θ',r'\theta').replace(r'\theta','v');raw=re.sub(r'\\[A-Za-z]+|r',lambda m:'u' if m[0]=='r' else m[0],raw);return base.scalar(raw)
def equal(a,b):return base.equal(a,b)
def prompt(q):
 txt=q[':question/problem'];bs=p.blocks(txt);vec=re.search(r'F\(x,\s*y\)\s*=\s*⟨(.*?)⟩',txt)
 if vec:P,Q=[scalar(v) for v in vec[1].replace(r'\,','').split(',')]
 else:
  line=next(b for b in bs if '∮' in b and 'dx' in b);line=line.split('=',1)[0].strip();body=re.sub(r'^.*?∮\}?_(?:\{C\}|C|\(C\))','',line);P,tail=re.split(r'\\,?\s*dx|dx',body,maxsplit=1);Q=re.sub(r'\\,?\s*dy|dy','',tail).strip().removeprefix('+');P,Q=scalar(P),scalar(Q)
 circle=next(b for b in bs if re.match(r'(?:\{x\}|x)(?:\^\{?2\}?|²)\s*\+',b));lhs,n=circle.split('=',1);assert equal(scalar(lhs),x*x+y*y);rad=s.sqrt(scalar(n));assert rad>0
 assert 'counterclockwise' in txt and 'pointwise' in txt;C['circle_equations']+=1
 return P,Q,rad

def audits(q,family):
 P,Q,rad=prompt(q);py=s.diff(P,y);qx=s.diff(Q,x);curl=s.simplify(qx-py);pol=s.trigsimp(curl.subs({x:r*s.cos(theta),y:r*s.sin(theta)},simultaneous=True));answer=s.expand_trig(pol*r);sol=q[':question/worked-solution'].replace(r'\partial ','∂').replace(r'\iint_D','{∬}_{D}').replace(r'\iint_\Delta','{∬}_{Δ}')
 start_partials=C['cross_partials']
 for fn,axis,raw in re.findall(r'\\frac\{∂([PQ])\}\{∂([xy])\}=(.*?)(?=,\\,|\.\\end|\$)',sol):
  assert (fn,axis) in (('P','y'),('Q','x'));assert equal(scalar(raw),py if fn=='P' else qx);C['cross_partials']+=1
 # Actual source prose definitions must match the independently read prompt.
 for fn,body in re.findall(r'\$([PQ])\(x,y\)=(.*?)\$',sol):assert equal(scalar(body.rstrip(',')),P if fn=='P' else Q)
 stage_roles=[]
 for block in p.blocks(sol):
  if r'\begin{aligned}' not in block:
   if family!='unrated_cross' or '∬' not in block or 'f(' in block:continue
   rows=['&='+rhs for rhs in block.split('=')[1:]]
  else:
   body=block.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0];rows=body.split(chr(92)*2)
  for row in rows:
   if '=' not in row:continue
   raw=row.split('=',1)[1].replace('&','').strip().rstrip('.,');raw=raw.replace(r'\int_0',r'\int_{0}')
   if re.match(r'\{∬\}_\{D\}',raw):
    expr=re.sub(r'^\{∬\}_\{D\}','',raw);expr=re.split(r'\\(?:text|mathrm)\{d\}A|dA',expr)[0].rstrip().removesuffix(r'\,')
    if '∂' in expr:
     expr=expr.replace(r'\frac{∂Q}{∂x}','('+s.latex(qx)+')').replace(r'\frac{∂P}{∂y}','('+s.latex(py)+')')
    assert equal(scalar(expr),curl),(family,'curl',expr,curl);C['cartesian_curl_rows']+=1;stage_roles.append('curl')
   elif re.match(r'\{∬\}_\{Δ\}',raw):
    expr=re.sub(r'^\{∬\}_\{Δ\}','',raw);expr=re.split(r'\\(?:text|mathrm)\{d\}r|dr',expr)[0].rstrip().removesuffix(r'\,');assert equal(scalar(expr),answer),(family,'polar',expr,answer);C['polar_rows']+=1;stage_roles.append('polar')
   elif r'\int' in raw:
    # Formal empty box is prompt-only; solution final concrete integrand/bounds.
    starts=list(re.finditer(r'(?:\{\\int \}|\\int)_',raw));assert len(starts)==2
    def groupat(pos):return p.group(raw,pos)
    vals=[];pos=0
    for m in starts:
     a,j=groupat(m.end());assert raw[j]=='^';b,j=groupat(j+1);vals.extend([scalar(a),scalar(b)]);pos=j
    assert vals==[0,2*s.pi,0,rad];expr=re.split(r'\\(?:text|mathrm)\{d\}r|dr',raw[pos:])[0].strip().removesuffix(r'\,');assert equal(scalar(expr),answer);C['polar_rows']+=1;stage_roles.append('polar')
 assert C['cross_partials']-start_partials==2 and stage_roles
 f=q[':question/answer-fields'][0];vs=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vs)==5 and all(not equal(v,w) for i,v in enumerate(vs) for w in vs[:i]);assert next(a[':answer/id'] for a in f[':answer-field/choices'] if equal(scalar(a[':answer/value']),answer))==f[':answer-field/correct'][1]
 for path in re.findall(r'!\[[^]]*\]\(([^)]+)\)',sol):
  path=Path(path);assert path.exists();side=json.loads(path.with_suffix('.json').read_text());assert side['radius']==rad and side['orientation']=='counterclockwise' and side['equal_aspect'];assert hashlib.sha256(path.read_bytes()).hexdigest()==side['sha256'];C['plot_sidecars']+=1
 C['records']+=1;C['complete_choices']+=5;C['whole_banks']+=1;return stage_roles

def raw(g):
 qs={q[':question/math-academy-id']:q for q in json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions']}
 for case in json.loads((D/'source-cases.json').read_text()):
  old=qs[case['source_id']];q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];assert q[':question/problem']==old[':question/problem'];C['raw_prompts']+=1
  for attr in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (attr in q)==(attr in old)
  if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution'];C['raw_solutions']+=1
  if ':question/difficulty' in old:assert q[':question/difficulty']==old[':question/difficulty'][':db/ident']
  else:C['raw_missing_ratings']+=1
  f,f0=q[':question/answer-fields'][0],old[':question/answer-fields'][0];assert f[':answer-field/type']==f0[':answer-field/type'][':db/ident'] and f[':answer-field/key']==f0[':answer-field/key'];actual=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
  for v in f0[':answer-field/choices']:assert sum(equal(scalar(v[':answer/value']),a) for a in actual)==1;C['raw_choices']+=1;C['literal_raw_choices']+=sum(a[':answer/value']==v[':answer/value'] for a in f[':answer-field/choices'])
  assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
  if ':answer-field/correct' in f0:assert equal(scalar(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])),scalar(f0[':answer-field/correct'][':answer/value']));C['raw_designations']+=1
  else:C['raw_missing_designations']+=1
  C['raw_banks']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'green_circular_generator');raw(g);records=json.loads((R/f'qa/{K}-sampled.json').read_text());roles={}
 for fam,(lv,*_) in g.CONFIG.items():records.append(g.generate(lv,template=fam,seed=883))
 for rec in records:
  fam=rec['generation']['template'];seq=audits(rec['question'],fam);assert fam not in roles or roles[fam]==seq;roles[fam]=seq
 report=dict(status='passed',readback=C,operative_sequences=roles,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
