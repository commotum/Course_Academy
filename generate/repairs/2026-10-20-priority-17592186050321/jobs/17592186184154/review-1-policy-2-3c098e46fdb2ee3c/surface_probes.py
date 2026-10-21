import json,pathlib,collections,re
E=pathlib.Path(__file__).resolve().parent
v=json.load(open(E/'variation-results.json'))
# Reuse only independent parser definitions; do not execute audit orchestration.
import ast
ns={'__file__':str(E/'audit.py')}
tree=ast.parse((E/'audit.py').read_text())
selected=[]
for node in tree.body:
 if isinstance(node,(ast.Import,ast.ImportFrom)) and not (isinstance(node,ast.Import) and any(a.name=='generator' for a in node.names)):selected.append(node)
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['x','C'] for t in node.targets):selected.append(node)
 if isinstance(node,ast.FunctionDef) and node.name in ['tex','parse','field','key']:selected.append(node)
exec(compile(ast.Module(body=selected,type_ignores=[]),'independent-parser-functions','exec'),ns)
parse=ns['parse'];x=ns['x'];key=ns['key'];field=ns['field']
def subgroup(r):
 fam=r['generation']['template'];p=r['question'][':question/problem']
 form=('reciprocal' if r'\sqrt{x}}' in p else 'product') if fam=='radical' else ('den'+re.search(r'\}\{x\^\{(\d+)\}\}',p)[1])
 signs=('+' if r['generation']['parameters']['a']>0 else '-')+('+' if r['generation']['parameters']['b']>0 else '-')
 return fam+'/'+form+'/bank-signs-'+signs
reports={}
for stage,path in [('raw','raw-attempts.json'),('delivered','delivery-sample/accepted.json')]:
 records=json.load(open(E/path));groups=collections.defaultdict(list)
 for r in records:
  if r['generation']['template']=='blank':continue
  groups[r['generation']['template']].append(r);groups[subgroup(r)].append(r)
 results=[]
 for group,rr in groups.items():
  # Choice order is retained in these sampled records; UI may shuffle it again.
  for strategy in ['first','last','shortest','longest','largest-polynomial-exponent','smallest-polynomial-exponent','median-polynomial-coefficient','smallest-polynomial-coefficient','largest-polynomial-coefficient']:
   hit=0
   for r in rr:
    aa=field(r)[':answer-field/choices']
    def stats(a):
     expr=parse(a[':answer/value']);terms=expr.as_ordered_terms();positive=[]
     for term in terms:
      coeff,power=term.as_coeff_exponent(x)
      if power>0:positive.append((power,abs(coeff)))
     return max(positive)
    if strategy=='first':chosen=aa[0]
    elif strategy=='last':chosen=aa[-1]
    elif strategy in ['shortest','longest']:chosen=(min if strategy=='shortest' else max)(aa,key=lambda a:len(a[':answer/value']))
    elif strategy.endswith('exponent'):chosen=(max if strategy.startswith('largest') else min)(aa,key=lambda a:stats(a)[0])
    else:
     ranked=sorted(aa,key=lambda a:stats(a)[1]);chosen=ranked[2 if strategy.startswith('median') else (0 if strategy.startswith('smallest') else -1)]
    hit+=chosen[':answer/id']==key(r)[':answer/id']
   results.append({'cue':'static answer position, length, exponent or coefficient rank','subgroup':group,'scope':'within_template' if '/' not in group else 'other_recognizable_subgroup','strategy':strategy,'correct':hit,'total':len(rr),'baseline':.2,'disposition':'defect' if hit==len(rr) else 'not_predictive','conclusion':f'{hit}/{len(rr)} compared to uniform five-choice baseline 0.20; fixed rank does not consult integrand coefficients/exponents. Small sign subgroups are descriptive and are not proof of absence of other predictors.','sample_refs':[path]})
 for q in results:
  if q['correct']==q['total'] and not ('/den4/' in q['subgroup'] and q['strategy'] in ['largest-polynomial-exponent','smallest-polynomial-coefficient']):
   q['disposition']='unconfirmed_exploratory_hit';q['conclusion']+=' Observed perfect only in this small sample; not asserted as a separate defect and not exhaustively tested.'
 reports[stage]=results
(E/'surface-probes.json').write_text(json.dumps(reports,indent=2)+'\n')
print(json.dumps({'probe_counts':{k:len(a) for k,a in reports.items()},'perfect':{k:[p for p in a if p['correct']==p['total']] for k,a in reports.items()}},indent=2))
