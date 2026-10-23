import sys,os,json,pathlib,importlib.util,re,hashlib,collections
sys.dont_write_bytecode=True
P=pathlib.Path(__file__).resolve().parent
src=(P/'review_checks.py').read_text(); start=src.index('import sympy as sp'); end=src.index('source=json.load')
exec(src[start:end])
def save(n,o): (P/n).write_text(json.dumps(o,indent=2))
spec=importlib.util.spec_from_file_location('gen',P.parent/'workspace/17592186096613.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
pairs=[p for p in json.load(open(P/'counterfactuals.json')) if p['profile']!='quotient-denominator']
pairs.append({'profile':'quotient-denominator','before':g.generate_easy(seed=619,profile='quotient',parameters=dict(n=1,d=4,k=0)), 'relevant_after':g.generate_easy(seed=619,profile='quotient',parameters=dict(n=1,d=5,k=0)), 'irrelevant_after':g.generate_easy(seed=620,profile='quotient',parameters=dict(n=1,d=4,k=0))})
save('counterfactuals.json',pairs)
records=json.load(open(P/'batch.json'))+[r for pair in pairs for k,r in pair.items() if k!='profile']
save('render-records.json',records)
cases=json.load(open(P/'grader-input.json'))
for r in [pairs[-1][k] for k in ['before','relevant_after','irrelevant_after']]+json.load(open(P/'delivery-batch/accepted.json'))+json.load(open(P/'historical-records.json')):
 t=target(r);f=field(r);checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if sp.simplify(parse(a[':answer/value'])-t)==0 else 'rejected','purpose':'Independent visible-prompt derivative'} for a in f[':answer-field/choices']]
 else:
  checks=[{'submitted':v,'expected':e,'purpose':'Equivalent or plausible incorrect expression'} for v,e in [(sp.latex(t),'accepted'),(str(t),'accepted'),(str(t).replace('/x','*x^(-1)'),'accepted'),('0','rejected'),(str(-t),'rejected'),(str(t*x),'rejected')]]
 cases.append({'label':'supplement-'+r['question'][':question/id'],'record':r,'checks':checks})
save('grader-combined-input.json',cases)
# Inspect every new-family solution equality, using differentiation of its visible expression.
rows=[]
for r in records+json.load(open(P/'author-regression/focused-samples.json'))[:26]:
 t=target(r);sol=r['question'][':question/worked-solution'];block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[-1]
 rr=[]
 for row in block.split(r'\\'):
  val=row.split('=')[-1].strip().rstrip('.')
  val=val.replace(r'\left','').replace(r'\right','').replace(r'\frac{\text{d}}{\text{d}x}','D')
  # Reuse independent parser with D mapped to log's derivative before numeric simplification.
  val=val.replace(r'D(\ln x)',r'\frac{1}{x}')
  if 'D(' in val:
   val=re.sub(r'D\((.*)\)',lambda m: sp.latex(sp.diff(parse(m[1]),x)),val)
  rr.append(sp.simplify(parse(val)-t)==0)
 rows.append({'id':r['question'][':question/id'],'rows':rr,'solution':sol})
save('solution-row-diagnostic.json',[v for v in rows if not all(v['rows'])]); assert all(all(v['rows']) for v in rows)
save('solution-rows.json',rows)
# Directed invalid quotient domains and collision boundaries must reject, with nearby allowed values.
rej=[]
for n,d,k in [(1,1,0),(0,4,0),(2,4,0),(1,13,0),(1,4,1),(-1,2,0),(1,12,0)]:
 try:r=g.generate_easy(seed=619,profile='quotient',parameters=dict(n=n,d=d,k=k));ok=True
 except ValueError as e:ok=False
 assert ok==((n,d,k) in [(-1,2,0),(1,12,0)])
 rej.append({'parameters':dict(n=n,d=d,k=k),'accepted':ok})
save('quotient-boundaries.json',{'seed':619,'cases':rej,'domain_rule':'22 signed unit fractions: numerator ±1, denominator 2..12; complete bank uniqueness rejects denominator 1.'})
save('repair-verification.json',{'finding':'6bbaf15dc6703e79f686','independent_prior_failure':'original-failure.json','independent_current_pass':'repaired-gap.json','retained_check_fails_old':'retained-regression-original.log','retained_check_passes_current':'retained-regression.log','retained_preflight':'../repair-preflight.json','solution_row_checks':len(rows),'counterfactual_pairs':len(pairs)})
(P/'session-state.md').write_text('Source replay and targeted mathematics complete. Prior counterexample and retained author regression fail old package, pass current. Delivery retains 5/5 batch and 21/26 independent samples. Native grading and UI render pending. Package unchanged so far.\n')
print(json.dumps({'solution_records':len(rows),'native_cases':len(cases),'render_records':len(records)}))
