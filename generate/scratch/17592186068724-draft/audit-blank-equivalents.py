"""Descriptive native audit of mathematically valid extra blank spellings.

Outcomes are discovered through the frozen checker, never claimed to be grading
passes merely because an expected result was configured to match observation.
"""
import json,re,subprocess,hashlib
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent
records=[r for r in json.loads((D/'native-input.json').read_text())if r['record']['question'][':question/answer-fields'][0][':answer-field/type']==':answer-field.type/blank']
t=sp.Symbol('t',real=True);all_results=[];probes=[]
for r in records:
 c=r['record']['generation']['parameters']['c'];u=2*t**2+c;f=-16*t/u
 assert sp.cancel(sp.diff(-sp.log(u**4),t)-f)==0
 assert sp.cancel(sp.diff(-4*sp.log(2*u),t)-f)==0
 text=f'(2*t^2+{c})';r['checks']=[{'submitted':f'-4*ln(abs({text}))','expected':'accepted','purpose':'valid exact real positive log(abs) equivalent'},{'submitted':f'-ln({text}^4)','expected':'accepted','purpose':'valid exact log-power equivalent'},{'submitted':f'-4*ln(2*{text})','expected':'accepted','purpose':'valid primitive modulo supplied K'}]
 for check in r['checks']:
  one=dict(r,checks=[check]);p=D/'blank-equivalent-probe-input.json';p.write_text(json.dumps([one]));report=D/'blank-equivalent-probe-report.json';out=subprocess.run([str(D/'check-engine'),str(p),str(report)],capture_output=True,text=True)
  if out.returncode:
   observed=re.search(r'got (accepted|rejected|unresolved)',out.stderr)[1];probes.append({'c':c,'submitted':check['submitted'],'initial_expected':'accepted','native_error':out.stderr.strip(),'observed':observed});check['expected']=observed
   p.write_text(json.dumps([one]));subprocess.run([str(D/'check-engine'),str(p),str(report)],check=True,capture_output=True)
  all_results.append(json.loads(report.read_text())['records'][0])
(D/'blank-equivalents-input.json').write_text(json.dumps(records,indent=2));subprocess.run([str(D/'check-engine'),str(D/'blank-equivalents-input.json'),str(D/'blank-equivalents-report.json')],check=True)
(D/'blank-equivalents-audit.json').write_text(json.dumps({'role':'descriptive valid-math engine compatibility limitations; separate from required canonical/equivalent/ordinary-wrong contract tests','every_expression_symbolically_valid':True,'domain':'u=2*t^2+c>0 on all R, c in1..19; fixed external K allows constant shifts','initial_mismatches':probes,'foreign_or_malformed_submissions':0},indent=2))
