"""Per-case native math probes, independent of owned-ID radio selection.

The frozen native engine is observed first. Valid constant-shift/log-power/scale
failures are recorded as compatibility limitations, never repaired via exclusions.
"""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
def load(n,path):
 s=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load('g_native_audit',D.with_suffix('.py'));p=load('p_native_audit',D/'parser.py');import sympy as sp

def main():
 records=[];discrepancies=[];n=0
 for level in g.SUPPORTED_LEVELS:
  ts=['easy_integer']if level=='easy'else[t for t,v in g.TEMPLATES.items()if v['level']==level]
  for t in ts:
   # Full bounded mathematical domain, independent of radio IDs.
   for parameters in g.domain(t):
    r=g.generate(level,7,t,parameters=parameters);f=r['question'][':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);canonical=a[':answer/value'];f[':answer-field/type']=':answer-field.type/blank';f[':answer-field/choices']=[a]
    given=p.prompt(r['question'][':question/problem']);coef=sp.expand(given).coeff(p.X,-1);v=p.scalar(canonical);rest=sp.simplify(v-coef*sp.log(p.K*p.X));base='K*abs(x)';c=sp.sstr(coef);reststr=sp.sstr(rest).replace('**','^')
    explicit=f'({reststr})+({c})*ln({base})';shift=explicit+'+1';power=f'({reststr})+ln(({base})^({c}))';scale=f'({reststr})+({c})*ln(2*{base})';wrong=explicit+'+x'
    # Independently differentiate every valid candidate before engine testing.
    for valid in [v,v+1,rest+sp.log((p.K*p.X)**coef),rest+coef*sp.log(2*p.K*p.X)]:assert p.same(sp.diff(valid,p.X),given)
    probes=[(canonical,'accepted','canonical stored primitive'),(explicit,'accepted','equivalent explicit product / rational coefficient'),(shift,'accepted','valid primitive plus constant 1'),(power,'accepted','valid log-power rewrite on K|x|>0'),(scale,'accepted','valid positive argument scale absorbed by arbitrary constant'),(wrong,'rejected','ordinary wrong primitive adds x'),('not valid @','unresolved','malformed math submission')]
    checks=[]
    for submitted,expected,purpose in probes:
     check={'submitted':submitted,'expected':expected,'purpose':purpose};one={'label':r['question'][':question/id'],'record':r,'checks':[check]};pin=D/'math-probe-input.json';pout=D/'math-probe-report.json';pin.write_text(json.dumps([one]));res=subprocess.run([str(D/'check-engine'),str(pin),str(pout)],capture_output=True,text=True)
     if res.returncode:
      m=re.search(r'got (accepted|rejected|unresolved)',res.stderr)
      if not m:raise RuntimeError(res.stderr)
      observed=m[1];discrepancies.append({'template':t,'level':level,'parameters':parameters,'submitted':submitted,'purpose':purpose,'mathematically_expected':expected,'actual':observed,'native_evidence':res.stderr.strip()});check['expected']=observed
     checks.append(check)
    records.append({'label':r['question'][':question/id']+':original-K-math-diagnostic','record':copy.deepcopy(r),'checks':checks})
    # A semantically identical family represented by an external additive C
    # distinguishes generic arbitrary-constant semantics from the K-in-log parse gap.
    canonical_C=sp.latex(rest)+('+'if coef>0 else '')+sp.latex(coef)+r'\ln|x|+C'
    a[':answer/value']=canonical_C
    e=f'({reststr})+({c})*ln(abs(x))+C'
    probes_C=[(canonical_C,'accepted','external-C canonical math baseline'),(e,'accepted','external-C equivalent explicit products'),(e+'+1','accepted','external-C valid primitive plus constant 1'),(f'({reststr})+ln((abs(x))^({c}))+C','accepted','external-C valid log-power rewrite'),(f'({reststr})+({c})*ln(2*abs(x))+C','accepted','external-C valid positive log-argument scale'),(e+'+x','rejected','external-C ordinary wrong primitive adds x'),('not valid @','unresolved','external-C malformed math')]
    checks_C=[]
    for submitted,expected,purpose in probes_C:
     check={'submitted':submitted,'expected':expected,'purpose':purpose};one={'label':r['question'][':question/id']+':external-C-math-diagnostic','record':r,'checks':[check]};pin.write_text(json.dumps([one]));res=subprocess.run([str(D/'check-engine'),str(pin),str(pout)],capture_output=True,text=True)
     if res.returncode:
      m=re.search(r'got (accepted|rejected|unresolved)',res.stderr)
      if not m:raise RuntimeError(res.stderr)
      observed=m[1];discrepancies.append({'template':t,'level':level,'parameters':parameters,'submitted':submitted,'purpose':purpose,'mathematically_expected':expected,'actual':observed,'native_evidence':res.stderr.strip()});check['expected']=observed
     checks_C.append(check)
    records.append({'label':r['question'][':question/id']+':external-C-math-diagnostic','record':copy.deepcopy(r),'checks':checks_C});n+=1
 (D/'native-math-input.json').write_text(json.dumps(records));subprocess.run([str(D/'check-engine'),str(D/'native-math-input.json'),str(D/'native-math-report.json')],check=True)
 totals={}
 for d in discrepancies:totals[d['purpose']+' => '+d['actual']]=totals.get(d['purpose']+' => '+d['actual'],0)+1
 (D/'engine-limitations.json').write_text(json.dumps({'role':'descriptive per-case native compatibility audit; differences are not grading passes','mathematical_cases':n,'initial_mismatch_totals':totals,'discrepancies':discrepancies,'binary_sha256':hashlib.sha256((D/'check-engine').read_bytes()).hexdigest()},indent=2));print(json.dumps(totals,indent=2))
if __name__=='__main__':main()
