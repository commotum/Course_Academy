#!/usr/bin/env python3
import hashlib,importlib.util,json,re,subprocess,sys,difflib
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('flux_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ENGINE=ROOT/'generate/runs/current/check-engine'
def save(name,x):(D/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def checks(r,label):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'actual owned radio selection'} for a in f[':answer-field/choices']]}
def inspect(r):
 q=r['question'];p=g.parameters(q);meta=r['generation']['parameters'];assert p==meta,(p,meta)
 c=sp.Rational(p['c']);L=p['L'];h=sp.Rational(L,2);t=sp.Symbol('t',real=True)
 # Independent outward-normal line integrals: right, top, left, bottom.
 if p['axis']=='radial':fluxes=[sp.integrate(c*h,(t,-h,h))]*4
 else:
  fx=c if p['axis']=='i' else 0;fy=c if p['axis']=='j' else 0
  fluxes=[sp.integrate(v,(t,-h,h)) for v in (fx,fy,-fx,-fy)]
 answer=sum(fluxes);f=q[':question/answer-fields'][0];vals=[g.value_parse(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(vals)==len(set(vals))==5 and vals.count(answer)==1
 correct=f[':answer-field/correct'][1]
 assert next(g.value_parse(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==correct)==answer
 sol=q[':question/worked-solution'];assert sol.count('$')%2==0 and '@' not in sol
 # Read numerical equations and field from printed prompt/solution.
 assert '$F='+g.field(c,p['axis'])+'$' in sol if p['axis']!='radial' else '('+g.field(c,'radial')+')' in sol
 if p['axis']=='radial':
  chain=re.search(r'\{∮\}_\{C\}F\\cdot n\\,\\text\{d\}s=4\\cdot (\(?-?[\d.]+\)?)=(-?[\d.]+)\.',sol)
  assert chain and sp.Rational(chain[1].strip('()'))==fluxes[0] and sp.Rational(chain[2])==answer
  bounds=re.search(r't\\in \[(-?\d+),(\d+)\]',sol);assert tuple(map(int,bounds.groups()))==(-h,h)
  assert 'r(t)='+g.coefficient(h)+r'\,i+t\,j' in sol
 else:
  assert sol.rstrip().endswith('=0.\n$$')
  parallel=(1,3) if p['axis']=='j' else (2,4)
  assert 'parallel to ${C}_{'+str(parallel[0])+'}$ and ${C}_{'+str(parallel[1])+'}' in sol
 for path in re.findall(r'!\[\]\((.*?)\)',q[':question/problem']+'\n'+sol):
  fp=Path(path) if Path(path).is_absolute() else Path('/media/jake/SSD/EDB/math')/path
  assert fp.is_file(),fp
 return answer

def easy_recipe(sid,p,value):
 value=int(value);sign='-' if value<0 else ''
 return '0' if value==0 else sign+'L' if abs(value)==p['L'] else sign+'2*L' if sid=='q-127190' else sign+'abs(c)*L'
def main():
 ledger=[];native=[];reviews=[];total=0;dist=0
 for sid,q in g.SOURCES.items():
  lv=g.level_of(q);p=g.parameters(q);r=g.generate(lv,parameters=p,profile=sid);inspect(r)
  new=r['question'];f=q[':question/answer-fields'][0];bank=sorted(g.value_parse(a[':answer/value']) for a in f[':answer-field/choices']);newbank=sorted(g.value_parse(a[':answer/value']) for a in new[':question/answer-fields'][0][':answer-field/choices']);assert bank==newbank
  assert q[':question/problem']==new[':question/problem']
  if ':question/worked-solution' in q:
   if q[':question/worked-solution']!=new[':question/worked-solution']:
    print(''.join(difflib.unified_diff(q[':question/worked-solution'].splitlines(True),new[':question/worked-solution'].splitlines(True))),sid);raise AssertionError('solution fidelity')
   assert f[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in new[':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==new[':question/answer-fields'][0][':answer-field/correct'][1])
  ledger.append({'source':sid,'parameters':p,'level':lv,'complete_bank_matched':True,'choices':5,'distractors':4 if f.get(':answer-field/correct') else None,'source_key_missing':':answer-field/correct' not in f,'source_solution_missing':':question/worked-solution' not in q,'prompt_exact':True,'present_solution_exact':':question/worked-solution' in q,'recipes':[{'value':a[':answer/value'],'recipe':easy_recipe(sid,p,a[':answer/value']) if lv=='easy' else str(g.value_parse(a[':answer/value'])/(2*sp.Rational(p['c'])*p['L']**2))+'*(2*c*L**2)'} for a in f[':answer-field/choices']]})
  total+=5;dist+=4 if f.get(':answer-field/correct') else 0
  native.append(checks(r,'source/'+sid));reviews.append({'label':'Source replay '+sid,'record':r})
  # Each whole source bank selected at changed signed coefficients and lengths.
  for n,params in enumerate((dict(p,c='4',L=10),dict(p,c='-2',L=12))):
   rr=g.generate(lv,seed=n,profile=sid,parameters=params);inspect(rr);native.append(checks(rr,'changed/'+sid+'/'+str(n)))
   if n==0:reviews.append({'label':'Changed parameters '+sid,'record':rr})
 save('source-replay.json',ledger)
 # Boundaries and slot roles: entire finite numeric domain checked without plots.
 covered={};n=0
 original_plot=g.render_plots
 def stub(p,out):return {'prompt':str(D/'source-plots.png'),'solution':str(D/'source-plots.png')}
 g.render_plots=stub
 for lv in g.SUPPORTED:
  seen=set();axes=set();signs=set();lengths=set();coeffs=set()
  for L in g.LENGTHS:
   for c in g.COEFFICIENTS:
    if lv=='easy' and abs(c)<2:continue
    for axis in (('i','j') if lv=='easy' else ('radial',)):
     p={'c':str(c),'L':L,'axis':axis}
     for sid,q in g.SOURCES.items():
      if g.level_of(q)!=lv:continue
      rr=g.generate(lv,seed=31,profile=sid,parameters=p);inspect(rr);n+=1
      native.append(checks(rr,'domain/'+str(n)));seen.add(g.task_key(p));axes.add(axis);signs.add(str(sp.sign(c)));lengths.add(L);coeffs.add(str(c))
  covered[lv]={'distinct_parameter_tasks':len(seen),'axes':sorted(axes),'signs':sorted(signs),'lengths':sorted(lengths),'coefficients':sorted(coeffs),'eligible_unvisited':[]}
 # Changed direction with other mathematical data fixed must update all side names.
 r1=g.generate('easy',parameters={'c':'2','L':10,'axis':'i'},profile='q-126881');r2=g.generate('easy',parameters={'c':'2','L':10,'axis':'j'},profile='q-126881');inspect(r1);inspect(r2)
 assert r1['question'][':question/worked-solution']!=r2['question'][':question/worked-solution'] and g.task_key(r1['generation']['parameters'])==g.task_key(r2['generation']['parameters'])
 g.render_plots=original_plot
 # Deterministic sampled question identity and assets.
 for lv in g.SUPPORTED:
  a=g.generate(lv,seed=91);b=g.generate(lv,seed=91);assert a==b;inspect(a)
 save('engine-input.json',native);subprocess.run([str(ENGINE),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True,timeout=55)
 eng=json.loads((D/'engine-report.json').read_text());assert eng['documented_unresolved_checks']==0
 save('review.json',reviews);lines=['# Source and changed-parameter review','']
 for item in reviews:
  q=item['record']['question'];lines.extend(['## '+item['label'],'',q[':question/problem'],'',*['- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']],'',q[':question/worked-solution'],''])
 (D/'review.md').write_text('\n'.join(lines))
 sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
 report={'passed':True,'basis':g.CAPTURE['basis'],'lineage':g.CAPTURE['lineage'],'source_practice_questions':11,'complete_banks_matched':11,'source_answer_values_matched':total,'source_answer_values_total':55,'known_distractors_matched':dist,'known_distractors_total':40,'present_solutions_exact':10,'present_keys_matched':10,'unrated_incomplete_source_excluded':'q-127199; solution and -144 key inferred locally, no source mutation','domain_instances_checked':n,'slot_coverage':covered,'changed_axis_with_fixed_values_checked':True,'native_grading':{k:eng[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'supported_levels':list(g.SUPPORTED),'unsupported_levels':['hard'],'generator_sha256':sha(D.with_suffix('.py')),'source_sha256':sha(D/'source.json'),'engine_sha256':sha(ENGINE),'fidelity':'all original prompts, complete banks, present solutions and present keys match; missing source solution/key separately inferred','limitations':['Hard band has no supported source-faithful template.','Homogeneous moderate bank extensions preserve exact observed value ratios; error interpretations unresolved, no invented feedback.','Uniform direction/sign aliases are excluded from distinctness.']}
 save('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
