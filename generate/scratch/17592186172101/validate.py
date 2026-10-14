"""Read printed fields and rectangles, integrate boundary flux independently."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load('fluxgen',HERE.with_suffix('.py'));parser=load('display_parser',ROOT/'generate/runs/current/vector-math-parser.py')
x,y=parser.x,parser.y

def scalar(s):return parser.scalar(s.replace('\\\\','\\').replace(r'\sqrt[3]{y}',r'y^{\frac{1}{3}}'))
def read(q):
 text=q[':question/problem'].replace(r'\mathbf{F}','F');raw=re.search(r'F\(x,y\)\s*=\s*(?:⟨|\\left\\langle\s*)(.*?)(?:⟩|\\right\\rangle)',text,re.S)[1]
 parts=raw.replace(r'\,','').replace(r'\:','').split(',');assert len(parts)==2,parts
 p,q=map(scalar,parts)
 tail=text.split('through the boundary of the ')[1]
 if 'vertices' in tail:
  vertices=[tuple(map(int,v)) for v in re.findall(r'\((-?\d+),(-?\d+)\)',tail)];assert len(vertices)==4
  xx=sorted({a for a,b in vertices});yy=sorted({b for a,b in vertices});assert len(xx)==len(yy)==2
  assert set(vertices)=={(a,b) for a in xx for b in yy};bounds=(*xx,*yy)
 else:
  m=re.search(r'(-?\d+)\\le x\\le (-?\d+),(-?\d+)\\le y\\le (-?\d+)',tail);assert m;bounds=tuple(map(int,m.groups()))
 return p,q,bounds

def independent(rec):
 q=rec['question'];p,r,b=read(q);a,z,c,d=b;assert a<z and c<d
 div=sp.diff(p,x)+sp.diff(r,y)
 flux=sp.integrate(r.subs(y,d)-r.subs(y,c),(x,a,z))+sp.integrate(p.subs(x,z)-p.subs(x,a),(y,c,d))
 assert sp.simplify(flux-sp.integrate(div,(x,a,z),(y,c,d)))==0
 fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 vals=[scalar(t[':answer/value']) for t in f[':answer-field/choices']];assert len(vals)==5
 assert all(sp.simplify(v-w)!=0 for i,v in enumerate(vals) for w in vals[:i])
 correct=[t[':answer/id'] for t,v in zip(f[':answer-field/choices'],vals) if sp.simplify(v-flux)==0]
 assert correct==[f[':answer-field/correct'][1]],(flux,vals)
 meta=rec['generation'];t=meta['template'];k=meta['parameters']['scale']
 assert g.TEMPLATES[t]==q[':question/difficulty'].split('/')[-1]
 assert b==g.DATA[t][2]
 assert g.mathematical_fingerprint(t,k)==g.digest([str(sp.expand(div)),list(b)])
 if not meta['evidence_only']:
  sol=q[':question/worked-solution'];assert sol.count('$')%2==0 and sol.count('{')==sol.count('}')
  pp=re.search(r'We have that \$P\(x,y\)=(.*?)\$ and \$Q\(x,y\)=(.*?)\.\$',sol);assert pp
  assert sp.simplify(scalar(pp[1])-p)==0 and sp.simplify(scalar(pp[2])-r)==0
  der=re.search(r'\\frac\{\\partial P\}\{\\partial x\}=(.*?),\\qquad\\frac\{\\partial Q\}\{\\partial y\}=(.*?)\.\n',sol);assert der
  assert sp.simplify(scalar(der[1])-sp.diff(p,x))==0 and sp.simplify(scalar(der[2])-sp.diff(r,y))==0
  region=re.search(r'D=\\\{\(x,y\):(-?\d+)\\le x\\le (-?\d+),\\,(-?\d+)\\le y\\le (-?\d+)\\\}',sol);assert tuple(map(int,region.groups()))==b
  rows=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1].split(r'\\')
  assert sp.simplify(scalar(rows[-1].split('&=')[1])-flux)==0
  inner=sp.integrate(div,(x,a,z))
  # Check both printed integrands, both primitives and both endpoint pairs.
  integrand=re.search(r'\\int_\{(-?\d+)\}\^\{(-?\d+)\}\\int_\{(-?\d+)\}\^\{(-?\d+)\}\\left\((.*?)\\right\)',rows[2]);assert tuple(map(int,integrand.groups()[:4]))==(c,d,a,z)
  assert sp.simplify(scalar(integrand[5])-div)==0
  first=re.search(r'\\left\[(.*?)\\right\]_\{x=(-?\d+)\}\^\{x=(-?\d+)\}',rows[3]);assert tuple(map(int,first.groups()[1:]))==(a,z);assert sp.simplify(sp.diff(scalar(first[1]),x)-div)==0
  middle=re.search(r'\\left\((.*?)\\right\)',rows[4]);assert sp.simplify(scalar(middle[1])-inner)==0
  last=re.search(r'\\left\[(.*?)\\right\]_\{(-?\d+)\}\^\{(-?\d+)\}',rows[5]);assert tuple(map(int,last.groups()[1:]))==(c,d);assert sp.simplify(sp.diff(scalar(last[1]),y)-inner)==0
  assert meta['eligible_for_learning'] and t not in g.EXCLUDED
 return flux

def checks(r):
 independent(r);f=r['question'][':question/answer-fields'][0]
 return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Each field-owned radio choice'} for a in f[':answer-field/choices']]

def main():
 records=[];replays=[]
 for t,s in g.SOURCES.items():
  rec=g.generate(g.TEMPLATES[t],template=t,parameters={'scale':1},profile='observed:'+t);independent(rec)
  q=rec['question'];assert q[':question/problem']==s[':question/problem'] and q[':question/worked-solution']==s[':question/worked-solution']
  f=q[':question/answer-fields'][0];sf=s[':question/answer-fields'][0]
  assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in sf[':answer-field/choices']]
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
  replays.append({'source':t,'full_bank_matched':'5/5','incorrect_choices_matched':'4/4','prompt_and_solution_exact':True,'eligible_for_learning':t not in g.EXCLUDED})
  records.append(rec)
  if t not in g.EXCLUDED:
   for k in g.SCALES:
    rec=g.generate(g.TEMPLATES[t],template=t,parameters={'scale':k});independent(rec)
    assert rec['question']==g.generate(g.TEMPLATES[t],seed=999,template=t,parameters={'scale':k})['question'];records.append(rec)
 fingerprints={r['generation']['mathematical_fingerprint'] for r in records if not r['generation']['evidence_only']};assert len(fingerprints)==36
 # Fixed geometry with changed coefficient must update prompt, derivatives, integral and key.
 first=g.generate('hard',template='q-126820',parameters={'scale':2});second=g.generate('hard',template='q-126820',parameters={'scale':3});independent(first);independent(second)
 assert independent(first)!=independent(second)
 stale=copy.deepcopy(second);stale['question'][':question/worked-solution']=first['question'][':question/worked-solution']
 try:independent(stale)
 except AssertionError:pass
 else:raise AssertionError('stale solution undetected')
 engine=[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records]
 (HERE/'engine-input.json').write_text(json.dumps(engine));subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 report={'status':'pass','generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'source_basis':g.SNAPSHOT['basis'],'source_replays':replays,'complete_banks_matched':'10/10','source_distractors_matched':'40/40','boundary_flux_and_divergence_agree':len(records),'normal_distinct_tasks':36,'scale_slot_coverage':list(g.SCALES),'all_bounded_parameters_checked':True,'fixed_geometry_changed_coefficient_stale_solution_rejected':True,'native':json.loads((HERE/'engine-report.json').read_text()),'limitations':['easy unsupported','q-127322 replay only; source C1 hypothesis fails','common scale 2..5; geometry fixed; finite 20 moderate and 16 hard variants','source distractor causes unresolved; exact whole-value common-scaling extension']}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 review=[first,second,g.generate('moderate',template='q-127303',parameters={'scale':2})]
 (HERE/'review.json').write_text(json.dumps(review,indent=2));(HERE/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in review))
 print(json.dumps({k:v for k,v in report.items() if k!='native'},indent=2))
if __name__=='__main__':main()
