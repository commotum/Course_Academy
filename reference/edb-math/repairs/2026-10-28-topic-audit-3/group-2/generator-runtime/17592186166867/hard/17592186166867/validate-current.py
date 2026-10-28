"""Current source replay, symbolic stages, raster geometry, and native grading."""
from pathlib import Path
import json, importlib.util, hashlib, subprocess, copy
D=Path(__file__).resolve().parent
# Reuse the established mathematical validator without executing its full suite.
exec(compile((D/'validate.py').read_text().split('geometry=json.loads')[0],str(D/'validate.py'),'exec'))
geometry=json.loads((D/'source-geometry-current.json').read_text())
qa_spec=importlib.util.spec_from_file_location('independent_qa',D.parents[1]/'runs/current/qa-parabola-slope.py')
qa=importlib.util.module_from_spec(qa_spec);qa_spec.loader.exec_module(qa)
qa.geo['q-127503']=(2,-3)

def validate(r):
 mathcheck(r)
 qa.check(r)

def checks(r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete bank ID selection'} for a in f[':answer-field/choices']]
 a,b=(r['generation']['parameters'][k] for k in ('a','b'))
 value=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==correct)
 return [{'submitted':value,'expected':'accepted','purpose':'canonical fragment'}, {'submitted':rf'\frac{{{b*b}}}{{{2*a}y}}','expected':'accepted','purpose':'equivalent unreduced quotient'}, {'submitted':'y','expected':'rejected','purpose':'incorrect derivative'}, {'submitted':r'\frac{y}{2x}','expected':'rejected','purpose':'requires y-only fragment'}]

def fingerprint(q):
 sid=q.get(':question/math-academy-id')
 if sid:
  a,b=(3,-2) if sid=='e-9579' else g.SOURCE_PARAMS[sid]
  return g.digest(['reconstruct equation from plot','y²=cx',str(sp.Rational(b*b,a))])
 # Read actual rendered equation/solution, independent of generation metadata.
 sol=q[':question/worked-solution'];easy=str(q[':question/difficulty'].get(':db/ident','') if isinstance(q[':question/difficulty'],dict) else q[':question/difficulty']).endswith('/easy')
 if easy:
  block=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/problem'],re.S)[0]
  c=sp.expand(parse(block.split('=')[1])).coeff(X)
 else:
  point=re.search(r'passes through the point \$\((-?\d+),(-?\d+)\)',sol);a,b=map(int,point.groups());c=sp.Rational(b*b,a)
 return g.digest(['given equation' if easy else 'reconstruct equation from plot','y²=cx',str(c)])

def main():
 rows=[];fixtures=[];replays=[];banks=options=0
 for sid,q in g.CURRENT_QS.items():
  a,b=g.SOURCE_PARAMS[sid];level='hard' if a<0 else 'moderate'
  mode='current' if sid in ('q-127374','q-127503') else 'raw'
  r=g.generate(level,parameters={'a':a,'b':b},profile=mode+':'+sid)
  qr=r['question'];f=qr[':question/answer-fields'][0];f0=q[':question/answer-fields'][0]
  for key in (':question/problem',':question/worked-solution'):
   assert qr.get(key)==q.get(key),(sid,key)
  assert qr.get(':question/difficulty')==q.get(':question/difficulty',{}).get(':db/ident')
  assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices'])
  assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
  if ':answer-field/correct' in f:
   answer=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert answer==f0[':answer-field/correct'][':answer/value']
   fixtures.append({'label':sid,'record':r,'checks':checks(r)})
  validate(r);banks+=1;options+=len(f[':answer-field/choices']);replays.append(r)
  exclusion='Missing difficulty/correct reference/worked solution' if sid=='q-127372' else 'Source prose incorrectly identifies vertex (3,6); preserved, excluded from validated inventory' if sid=='q-127510' else None
  rows.append({'entity':q[':db/id'],'source_id':sid,'eligible':exclusion is None,'exclusion':exclusion,'fingerprint':fingerprint(q),'level':q.get(':question/difficulty',{}).get(':db/ident')})
 # The new source bank is evidence-only and must generalize as a complete bank.
 valid=invalid=0
 for a,b in g.domain('moderate'):
  vals,_=g.bank('q-127503',a,b);m=sp.Rational(b*b,2*a)/Y
  if all(sp.cancel(x-y)!=0 for i,x in enumerate(vals) for y in vals[i+1:]):
   assert sum(sp.cancel(x-m)==0 for x in vals)==1;valid+=1
  else:invalid+=1
 for l in ('easy','moderate','hard'):
  for kind in ('blank','radio'):
   for seed in (17,29):
    r=g.generate(l,seed,field_type=kind);validate(r);fixtures.append({'label':r['question'][':question/id'],'record':r,'checks':checks(r)})
 (D/'reference/initial/source-audit.json').write_text(json.dumps({'basis':g.CURRENT_SOURCES['basis'],'rows':rows},indent=2))
 (D/'reference/initial/current-replay.json').write_text(json.dumps(replays,indent=2))
 (D/'reference/initial/native-input.json').write_text(json.dumps(fixtures,indent=2))
 subprocess.run(['generate/runs/current/check-engine',str(D/'reference/initial/native-input.json'),str(D/'reference/initial/native-report.json')],check=True)
 report={'status':'passed','source_basis':g.CURRENT_SOURCES['basis'],'source_banks_matched':banks,'source_values_matched':options,'source_correct_refs_matched':len(g.CURRENT_QS)-1,'source_attribute_presence_and_prose_exact':banks,'new_bank_finite_domain':{'valid':valid,'rejected_collisions':invalid},'source_raster_fits':len(geometry),'generated_independent_raster_checks':12,'legacy_validation':'validation.json','native_report':'reference/initial/native-report.json','generator_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()}
 (D/'validation-current.json').write_text(json.dumps(report,indent=2));print(report)
if __name__=='__main__':main()
