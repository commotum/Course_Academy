"""Independent coordinate/ratio math and native right/wrong/equivalent controls."""
import argparse,json,re,subprocess,sys
from pathlib import Path
from fractions import Fraction as F
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import answer_id,enum

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

def main():
 ap=argparse.ArgumentParser();ap.add_argument('kp',type=int);ns=ap.parse_args();d=H/str(ns.kp);cases=[];ledger=[]
 for path in sorted((d/'samples').glob('*/*/delivery/accepted.json')):
  for i,rec in enumerate(json.loads(path.read_text())):
   vals=expected(ns.kp,rec);checks=[];q=rec['question'];fs=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key'])
   if ns.kp==17592186096653 and enum(fs[0][':answer-field/type'])==':answer-field.type/radio':
    p=rec['generation']['parameters'];target={p['u']:vals[0],p['v']:vals[1]};assert coeffs(next(a for a in fs[0][':answer-field/choices'] if a[':answer/id']==answer_id(fs[0][':answer-field/correct']))[':answer/value'])==target
   else:
    for f,value in zip(fs,vals):assert number(next(a for a in f[':answer-field/choices'] if a[':answer/id']==answer_id(f[':answer-field/correct']))[':answer/value'])==value
   for fi,f in enumerate(q[':question/answer-fields']):
    if enum(f[':answer-field/type'])==':answer-field.type/radio':
     for a in f[':answer-field/choices']:checks.append(dict(field_index=fi,submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==answer_id(f[':answer-field/correct']) else 'rejected',purpose='Actual offered choice; exact independently derived coefficients'))
    else:
     value=vals[int(f[':answer-field/key'].split('-')[-1])-1] if len(vals)>1 else vals[0]
     checks.extend([dict(field_index=fi,submitted=str(value),expected='accepted',purpose='Independent exact coordinate or ordered-ratio calculation'),dict(field_index=fi,submitted=f'{value.numerator*2}/{value.denominator*2}',expected='accepted',purpose='Equivalent unreduced rational, with no simplest-form restriction'),dict(field_index=fi,submitted=str(-value),expected='rejected',purpose='Wrong direction/sign'),dict(field_index=fi,submitted=str(value+1),expected='rejected',purpose='Wrong magnitude near miss')])
   label=str(path.relative_to(d))+':'+str(i);cases.append(dict(label=label,record=rec,checks=checks));ledger.append(dict(label=label,expected=list(map(str,vals)),parameters=rec['generation'].get('parameters',rec['generation'].get('instance')),question_uuid=q[':question/id']))
 (d/'math-checks.json').write_text(json.dumps(dict(passed=True,records=len(cases),checks=ledger,method='Independent 2x2 determinant solve or parse displayed ordered ratio/directions; metadata geometry is the actual renderer input, not pixel-digitized reconstruction.'),indent=2)+'\n')
 # Split by difficulty so each bounded native report is independently recoverable.
 for band in ['easy','moderate','hard']:
  subset=[c for c in cases if enum(c['record']['question'][':question/difficulty']).endswith('/'+band)];out=d/'native'/band;out.mkdir(parents=True,exist_ok=True);(out/'input.json').write_text(json.dumps(subset,indent=2)+'\n');run=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(out/'input.json'),str(out/'report.json')],capture_output=True,text=True,timeout=180);(out/'stderr.txt').write_text(run.stderr);print(ns.kp,band,run.returncode,run.stdout.strip(),run.stderr[-1000:],flush=True)
  if run.returncode:raise SystemExit(run.returncode)
if __name__=='__main__':main()
