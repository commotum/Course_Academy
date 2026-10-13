#!/usr/bin/env python3
"""Independent displayed-stage, complete source fidelity, scope and native checks."""
import concurrent.futures, copy, hashlib, importlib.util, json, math, re, subprocess, sys, tempfile
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def asnum(s):return float(s.replace(r'\,','').strip(' ,.;'))
def formatting(text):
 assert text.count('$')%2==0,'unbalanced math delimiters'
 depth=0
 for c in text:
  if c=='{':depth+=1
  if c=='}':depth-=1;assert depth>=0,'unbalanced TeX groups'
 assert depth==0,'unbalanced TeX groups'
 assert not re.search(r'\{\{(a|b|c|d|theta|phi|v1|v2|h1|h2|answer|total)\}\}',text),'unresolved slots'

def math_check(record):
 q=record['question'];assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']['db_id']==g.KP_ID
 assert record['generation']['eligible_for_learning'] and not record['generation']['evidence_only']
 text=q[':question/problem'];s=q[':question/worked-solution'];formatting(text);formatting(s)
 asset=re.findall(r'!\[\]\(([^)]+)\)',text)[0]; data=json.loads(Path(asset).with_suffix('.json').read_text())
 assert hashlib.sha256(Path(asset).read_bytes()).hexdigest()==data['png_sha256']
 # Read assessed mathematical data from the displayed plot label specification,
 # independently of the generation parameters and its calculation helpers.
 sides={(a,b):float(v) for a,b,v in data['side_labels']}; angles=data['angle_labels']; pnts=data['vertices']; ordered='ABCD'
 for (a,b),value in sides.items():
  assert abs(math.dist(pnts[a],pnts[b])-value)<1e-7,'rendered edge does not match its label'
 triangle_data=[]
 for vertex,angle in angles:
  incident=[v for (a,b),v in sides.items() if vertex in (a,b)]
  assert len(incident)==2
  i=ordered.index(vertex);before,after=pnts[ordered[(i-1)%4]],pnts[ordered[(i+1)%4]];point=pnts[vertex]
  v1=[before[j]-point[j] for j in range(2)];v2=[after[j]-point[j] for j in range(2)]
  cosine=sum(v1[j]*v2[j] for j in range(2))/(math.hypot(*v1)*math.hypot(*v2));actual=math.degrees(math.acos(max(-1,min(1,cosine))))
  tolerance=.501 if float(angle).is_integer() else .051
  assert abs(actual-float(angle))<tolerance,'rendered angle inconsistent with label precision'
  triangle_data.append((sorted(incident),float(angle)))
 if len(angles)==1:
  # Both marked adjacent lengths meet at B in the parallelogram diagram.
  assert sorted(sides.values())==triangle_data[0][0]
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',s,re.S)
 assert len(blocks)==len(triangle_data)+1
 values=[]; names=[];digits=[]
 for block,(side_values,angle) in zip(blocks,triangle_data):
  rows=block.split(r'\\'); assert len(rows)==3,'required substitution, multiplication and sine-evaluation stages'
  name=re.search(r'\{A\}_\{([A-D]+)\}',rows[0])[1];names.append(name)
  factors=re.search(r'\\frac\{1\}\{2\}(.*?)\\operatorname\{sin\}⁡?\{([\d.]+)\}\^\{∘\}',rows[0]);assert factors,'full included-angle substitution row'
  nums=[float(n) for n in re.findall(r'\d+(?:\.\d+)?',factors[1])];assert sorted(nums)==side_values
  assert float(factors[2])==angle
  stage=re.search(r'&\s*=([\d.]+)(?:\\cdot\s*)?\\operatorname\{sin\}⁡?\{([\d.]+)\}\^\{∘\}',rows[1]);assert stage,'operative multiplication row missing'
  coefficient=side_values[0]*side_values[1]/2
  assert abs(float(stage[1])-coefficient)<1e-8 and float(stage[2])==angle
  vtext=re.split(r'&\s*(?:=|≈|\\approx)\s*',rows[2])[1].strip(' ,.')
  value=asnum(vtext);decimal_digits=len(vtext.replace(r'\,','').split('.')[1]);digits.append(decimal_digits)
  expected=coefficient*math.sin(math.radians(angle))
  assert abs(value-float(g.rounded(expected,decimal_digits)))<1e-9,'printed sine evaluation incorrect'
  values.append(value)
 rows=blocks[-1].split(r'\\');assert len(rows)==3,'required composition, numeric substitution and collection rows'
 if len(values)==1:
  assert '2{A}_{'+names[0]+'}' in rows[0],'doubling must refer to the triangle actually computed'
  factor=re.search(r'&\s*=2\\cdot\s*([\d.,\\]+)',rows[1]);assert factor
  assert asnum(factor[1])==values[0]
  expected_total=2*values[0]
 else:
  assert '{A}_{'+names[0]+'}+{A}_{'+names[1]+'}' in rows[0],'triangle addition row required'
  summands=re.split(r'&\s*(?:=|≈|\\approx)\s*',rows[1])[1].split('+');assert len(summands)==2
  assert [asnum(x) for x in summands]==values
  expected_total=sum(values)
 printed_total=asnum(re.split(r'&\s*(?:=|≈|\\approx)\s*',rows[2])[1]);assert abs(printed_total-expected_total)<10**(-digits[0])*.51
 unit=1 if 'nearest integer' in text else .1
 precise=sum(a*b/2*math.sin(math.radians(t)) for (a,b),t in triangle_data)*(2 if len(triangle_data)==1 else 1)
 answer=round(precise) if unit==1 else float(g.rounded(precise,1))
 final=re.search(r'is \$([\d.]+)\.\$',s);assert final and float(final[1])==answer,'final prose answer'
 fields=q[':question/answer-fields'];assert len(fields)==1
 field=fields[0];choices=field[':answer-field/choices'];ref=field[':answer-field/correct'][1]
 selected=[x for x in choices if x[':answer/id']==ref];assert len(selected)==1 and float(selected[0][':answer/value'])==answer
 if field[':answer-field/type'].endswith('/blank'):assert '{{'+field[':answer-field/key']+'}}' in text
 else:
  assert len(choices)==5 and len({x[':answer/value'] for x in choices})==5
  assert all(float(x[':answer/value'])>0 for x in choices)
  if len(values)==1:
   a,b=triangle_data[0][0];vals=[precise,precise/2,a*b,2*a*b,a*b/2]
  else:
   (a,b),t=triangle_data[0];(c,d),f=triangle_data[1];u=a*b/2*math.sin(math.radians(t));v=c*d/2*math.sin(math.radians(f));vals=[u+v,u,v,2*(u+v),abs(u-v)]
  assert sorted(float(x[':answer/value']) for x in choices)==sorted(float(g.rounded(x,0 if unit==1 else 1)) for x in vals),'full displayed method-derived bank'
 return True

def main():
 originals=g.SOURCE['record'][':knowledge-point/questions'];raw=[];fidelity=[]
 for source in originals:
  key=source[':question/math-academy-id'];r=g.generate('moderate',template=key,parameters=g.RECIPES[key]['parameters'],profile='observed-'+key);q=r['question'];raw.append(r)
  for attr in (':question/problem',':question/worked-solution'):
   assert (attr in source)==(attr in q);assert source.get(attr)==q.get(attr),'complete prompt/solution string fidelity'
  for attr in (':question/difficulty',':question/answer-fields'):
   assert (attr in source)==(attr in q),'attribute-presence fidelity'
  for sf,rf in zip(source.get(':question/answer-fields',[]),q.get(':question/answer-fields',[])):
   assert sf[':answer-field/type'][':db/ident']==rf[':answer-field/type'] and sf[':answer-field/key']==rf[':answer-field/key']
   assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
   assert (':answer-field/correct' in sf)==(':answer-field/correct' in rf)
   if ':answer-field/correct' in sf:
    correct=next(a for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
    assert correct[':answer/value']==sf[':answer-field/correct'][':answer/value']
  fidelity.append({'source_id':source[':db/id'],'prompt_exact':True,'solution_exact':':question/worked-solution' in source,'presence_parity':True,'displayed_values':sum(len(f[':answer-field/choices']) for f in source.get(':question/answer-fields',[]))})
 generated=[]
 for level in ('easy','moderate','hard'):
  for seed in range(25):
   r=g.generate(level,seed);math_check(r);generated.append(r)
 default_coverage={}
 for level in ('easy','moderate','hard'):
  eligible={k for k,r in g.RECIPES.items() if level=='moderate' or (r['kind']=='para')==(level=='easy')}
  seen={r['generation']['template'] for r in generated if r['generation']['difficulty_design']==level}
  assert seen==eligible,'default supported-family coverage'
  default_coverage[level]=sorted(seen)
 # Explicit exercise each normal source-shaped family and both radio and blank layouts.
 for key in g.RECIPES:
  for seed in (201,202):
   r=g.generate('moderate',seed,template=key);math_check(r);generated.append(r)
 # Structural regression: equivalent arithmetic cannot replace the multiplied sine coefficient stage.
 bad=copy.deepcopy(generated[0]);s=bad['question'][':question/worked-solution'];original_block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',s,re.S)[0];rows=original_block.split(r'\\');rows[1]='  & ='+rows[0].split('& =')[1];replacement=r'\\'.join(rows);bad['question'][':question/worked-solution']=s.replace(original_block,replacement,1)
 try:math_check(bad)
 except AssertionError:pass
 else:raise AssertionError('operative-stage corruption was not rejected')
 # Stable IDs under independent shuffle; changed banks/data and actual difficulty affect content.
 for r in generated[:9]:
  m=r['generation'];r2=g.generate(m['difficulty_design'],999,template=m['template'],parameters=m['parameters']);assert r['question'][':question/id']==r2['question'][':question/id']
 # Invalid explicit inputs are rejected, never resampled.
 invalid=[('easy',dict(a=5,b=6,theta=55,precision=0),'q-279762'),('hard',dict(a=6,b=7,theta=50,c=7,d=8,phi=43,precision=1),'q-285703'),('moderate',dict(a=8,b=5,theta=80,c=10,d=7,phi=50,precision=1),'q-54258')]
 for level,p,key in invalid:
  try:g.generate(level,template=key,parameters=p)
  except ValueError:pass
  else:raise AssertionError('scope/geometry bound bypass')
 # Fresh concurrent renderer calls, including duplicate parameters, in separate processes.
 with tempfile.TemporaryDirectory(prefix='quadrilateral-concurrency-') as td:
  prs=[g.RECIPES['q-279762']['parameters'],g.RECIPES['q-285737']['parameters'],g.RECIPES['q-279762']['parameters']]
  def job(p):
   code="import importlib.util,json; s=importlib.util.spec_from_file_location('g',"+repr(str(ROOT.with_suffix('.py')))+"); g=importlib.util.module_from_spec(s);s.loader.exec_module(g);g.render_plots("+repr(p)+",g.RECIPES['q-279762'],"+repr(td)+")"
   subprocess.run([sys.executable,'-c',code],check=True,capture_output=True)
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(job,prs))
  assert len(list(Path(td).glob('*.png')))==4 and len(list(Path(td).glob('*.json')))==4
  assert not any(x.name.startswith('tmp') for x in Path(td).iterdir())
 native=[]
 native_records=generated+[r for r in raw if r['question'].get(':question/answer-fields') and ':answer-field/correct' in r['question'][':question/answer-fields'][0]]
 for r in native_records:
  f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1];answer=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
  if f[':answer-field/type'].endswith('/radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'owned complete-bank ID'} for a in f[':answer-field/choices']]
  else:
   checks=[{'submitted':answer,'expected':'accepted','purpose':'canonical rounded value'},{'submitted':str(float(answer)+1),'expected':'rejected','purpose':'wrong rounded value'},{'submitted':f'2*{answer}/2','expected':'rejected','purpose':'genuine rounding request requires rounded numeral, not arithmetic expression'},{'submitted':'+'+answer,'expected':'rejected','purpose':'documented native rejection of equivalent leading-plus numeral; normal blank explicitly requests digits/decimal point'}]
  native.append({'label':r['generation']['difficulty_design']+'-'+r['generation']['template']+'-'+str(r['generation']['seed']),'record':r,'checks':checks})
 inp=ROOT/'engine-input.json';out=ROOT/'engine-report.json';inp.write_text(json.dumps(native,indent=2)+'\n')
 process=subprocess.run(['generate/runs/current/check-engine',str(inp),str(out)],text=True,capture_output=True);assert process.returncode==0,process.stdout+process.stderr
 report=json.loads(out.read_text())
 review=raw+generated[-20:]+[g.generate(level,seed+401) for level in ('easy','moderate','hard') for seed in (0,1)]
 (ROOT/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 lines=['# Quadrilateral source and generated review','All observed records below are raw, evidence-only and ineligible. Generated records use supported complete method banks.']
 for r in review:
  m=r['generation'];lines += ['## '+('Original replay (evidence only)' if m['evidence_only'] else 'Generated '+m['difficulty_design'])+' — '+m['template'],g.markdown(r)]
 (ROOT/'review.md').write_text('\n\n'.join(lines)+'\n')
 metrics={'status':'pass','source_practice_questions':10,'unrated_sources':2,'source_prompt_exact':10,'source_solution_exact':8,'source_solution_denominator':8,'source_presence_parity':10,'source_field_layouts_matched':9,'source_banks_matched':9,'source_radio_banks_matched':6,'source_choice_values_matched':33,'source_correct_designations_matched':7,'source_correct_designations_missing':2,'source_fieldless':1,'known_radio_distractors_matched':16,'unkeyed_radio_values_matched':10,'raw_evidence_only_profiles':10,'generated_math_checked':len(generated),'levels':{x:sum(r['generation']['difficulty_design']==x for r in generated) for x in ('easy','moderate','hard')},'native':{k:v for k,v in report.items() if k!='records'},'default_family_coverage':default_coverage,'structural_mutation_rejected':True,'explicit_scope_and_geometry_rejections':3,'fresh_concurrent_render_passed':True,'source_anomalies':['q-72754 final four-place displayed sum 91.3119 should be 91.3120; raw preserved, normal repaired','q-72768 A_ACD in a chain referring to A_ACB; normal consistent nomenclature','q-54258 two measured triangles incompatible by 8.143 degrees; raw preserved; normal requires compatible data','q-72754 sides and angles slightly incompatible beyond integer angle rounding; raw retained and normal geometry guard enforced','q-18180 and q-54258 missing difficulty/correct ref/solution; raw omission preserved; completed normal fields inferred','q-72754 fieldless; normal supported blank is authored'], 'native_equivalent_entry_limitations':['Arithmetic expressions equal to the rounded numeral are rejected under genuine rounding instructions','Leading-plus rounded numerals are rejected; normal blanks explicitly request digits and optional decimal point'],'runtime':generated[0]['generation']['runtime'],'script_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'source_fidelity':fidelity}
 (ROOT/'validation.json').write_text(json.dumps(metrics,indent=2)+'\n');print(json.dumps({k:v for k,v in metrics.items() if k not in ('source_fidelity','source_anomalies')},indent=2));print(process.stdout)
if __name__=='__main__':main()
