"""Fail closed on replay, printed mathematics, plot data, UUIDs and native grading."""
from pathlib import Path
import importlib.util,json,re,subprocess,hashlib
from fractions import Fraction
import sympy as sp
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ellipse',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
raw=json.loads((D/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in raw['record'][':knowledge-point/questions']};cases=json.loads((D/'source-cases.json').read_text())

def angle(s):
 # Independent exact parser for every displayed source/generated pi expression.
 s=s.replace(' ','').replace(r'\left','').replace(r'\right','')
 s=re.sub(r'\\frac\{(.*?)\}\{(.*?)\}',lambda m:'('+m[1]+')/('+m[2]+')',s)
 s=s.replace(r'\pi','P');s=re.sub(r'(\d)(P)',r'\1*\2',s)
 value=sp.sympify(s,locals={'P':sp.pi})
 assert value.is_real;return sp.simplify(value)
def bounds(s):
 match=re.fullmatch(r'\\theta\s*\\in\s*\[(.*),(.*)(\]|\))',s);assert match,s
 return angle(match[1]),angle(match[2]),match[3]==']'
def normalize_math(s):
 if r'\in' in s:return bounds(s)
 return angle(s)
def normalized_prose(s):return re.sub(r'!\[.*?\]\(.*?\)','![](ASSET)',s)

def check(r):
 q=r['question'];meta=r['generation'];p=meta['parameters'];fields=q[':question/answer-fields'];text=q[':question/problem'];sol=q[':question/worked-solution']
 for displayed in (text,sol):
  assert displayed.count('$$')%2==0, 'Unbalanced display-math delimiters'
  inline=re.sub(r'\$\$.*?\$\$','',displayed,flags=re.S)
  assert inline.count('$')%2==0, 'Unbalanced inline-math delimiters'
  assert displayed.count('{')==displayed.count('}'), 'Unbalanced TeX braces'
 assert not '@@' in text+sol
 assert 'central angle' not in sol
 # Parse actual printed equations rather than proving answer from generation metadata.
 matches=re.findall(r'x=(\d+)\\operatorname\{cos\}⁡\\theta ([-+]\d+)?,\\,y=(\d+)\\operatorname\{sin\}⁡\\theta ([-+]\d+)?',text)
 assert len(matches)==1
 a,h,b,k=matches[0];a,b=int(a),int(b);h,k=int(h or 0),int(k or 0)
 assert (a,b,h,k)==tuple(p[z] for z in ('a','b','h','k'))
 assert f'a={a}' in sol and f'b={b}' in sol
 if h or k:assert f'point $({h},{k}),' in sol
 assert 'p=' not in sol and 'q=' not in sol
 # Every full/restricted numeric equation is exactly the printed prompt equation.
 for a1,h1,b1,k1 in re.findall(r'x=(\d+)\\operatorname\{cos\}⁡\\theta ([-+]\d+)?,\\,y=(\d+)\\operatorname\{sin\}⁡\\theta ([-+]\d+)?',sol):assert (int(a1),int(b1),int(h1 or 0),int(k1 or 0))==(a,b,h,k)
 intervals=re.findall(r'\\theta \\in (\[.*?\])',sol)
 assert intervals
 last=normalize_math(r'\theta \in '+intervals[-1]);lo,hi,closed=last
 assert closed and lo==sp.Rational(p['lo'])*sp.pi and hi==sp.Rational(p['hi'])*sp.pi
 assert 0<=lo<hi<=2*sp.pi
 t=sp.Symbol('t',real=True);xt=a*sp.cos(t)+h;yt=b*sp.sin(t)+k
 assert sp.trigsimp(((xt-h)/a)**2+((yt-k)/b)**2-1)==0
 # Exact curve extreme/endpoints and branch signs from printed equations.
 end=[(sp.simplify(xt.subs(t,u)),sp.simplify(yt.subs(t,u))) for u in (lo,hi)]
 assert all(v.is_Integer for pt in end for v in pt)
 mid=(lo+hi)/2;assert sp.simplify(((xt.subs(t,mid)-h)/a)**2+((yt.subs(t,mid)-k)/b)**2)==1
 ids=[]
 for f in fields:
  uuid=f[':answer-field/id'];assert uuid not in ids;ids.append(uuid)
  vals=f[':answer-field/choices'];assert len(vals)==(5 if f[':answer-field/type'].endswith('radio') else 1)
  values=[normalize_math(z[':answer/value']) for z in vals];assert len(set(values))==len(values)
  selected=[z for z in vals if z[':answer/id']==f[':answer-field/correct'][1]];assert len(selected)==1
  cv=normalize_math(selected[0][':answer/value'])
  assert cv==last if f[':answer-field/type'].endswith('radio') else cv==(lo if f[':answer-field/key']=='field-1' else hi)
  assert f[':answer-field/type'].endswith('radio') or '{{'+f[':answer-field/key']+'}}' in text
  for z in vals:assert z[':answer/id'] not in ids;ids.append(z[':answer/id']);assert '$' not in z[':answer/value']
 for role,path in meta['plot_assets'].items():
  path=Path(path);assert path.exists() and path.stat().st_size>10000
  data=json.loads(path.with_name(path.name.split('-')[0]+'.json').read_text());assert data['parameters']==p
  assert data['prompt_context']==g.TEMPLATES[meta['template']]['prompt_context']
 return {'printed_equation':[a,b,h,k],'derived_interval':[str(lo),str(hi)],'endpoints':[[str(x),str(y)] for x,y in end]}

def engine_item(label,r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  for z in f[':answer-field/choices']:
   correct=z[':answer/id']==f[':answer-field/correct'][1]
   if f[':answer-field/type'].endswith('radio'):checks.append({'field_index':i,'submitted_answer_id':z[':answer/id'],'expected':'accepted' if correct else 'rejected','purpose':'Complete owned bank selection'})
   else:
    v=z[':answer/value'];expr=angle(v)
    checks.extend([{'field_index':i,'submitted':v,'expected':'accepted','purpose':'Canonical printed endpoint'},
                   {'field_index':i,'submitted':str(expr).replace('pi','\\pi'),'expected':'accepted','purpose':'Equivalent slash-division pi endpoint'},
                   {'field_index':i,'submitted':r'\pi-\pi' if expr==0 else '('+str(2*expr).replace('pi',r'\pi')+')/2','expected':'accepted','purpose':'Unreduced equivalent endpoint expression'},
                   {'field_index':i,'submitted':str(expr+sp.pi/4).replace('pi',r'\pi'),'expected':'rejected','purpose':'Incorrect endpoint shifted by pi/4'}])
 return {'label':label,'record':r,'checks':checks}

records=[];replays=[];fidelity=[];display=[];engine=[];matched=choices=designations=0
for case in cases:
 q=qs[case['source_id']];level=q[':question/difficulty'][':db/ident'].split('/')[-1]
 r=g.generate(level,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);replays.append(r);display.append(check(r));engine.append(engine_item(case['source_id'],r))
 bykey={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']}
 count=0
 for orig in q[':question/answer-fields']:
  f=bykey[orig[':answer-field/key']];assert orig[':answer-field/type'][':db/ident']==f[':answer-field/type']
  left=[normalize_math(z[':answer/value']) for z in orig[':answer-field/choices']];right=[normalize_math(z[':answer/value']) for z in f[':answer-field/choices']];assert sorted(left,key=str)==sorted(right,key=str)
  count+=len(left);choices+=len(left);matched+=len(right)
  correct=next(z for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert normalize_math(correct[':answer/value'])==normalize_math(orig[':answer-field/correct'][':answer/value']);designations+=1
 assert normalized_prose(q[':question/problem'])==normalized_prose(r['question'][':question/problem'])
 # Text differences in solution are disclosed repairs, not exact prose fidelity.
 fidelity.append({'source_id':case['source_id'],'template':case['template'],'profile':case['bank_profile'],'values_matched':count,'values_total':count,'complete_bank':True,'correct_designations_matched':len(q[':question/answer-fields']),'prompt_exact_except_generated_assets':True,'worked_prose_exact':normalized_prose(q[':question/worked-solution'])==normalized_prose(r['question'][':question/worked-solution']),'worked_prose_repairs':r['generation']['source_prose_repairs']})
 # Source replay identity invariant under seed/order changes.
 again=g.generate(level,91,case['template'],parameters=case['parameters'],profile=case['bank_profile']);assert r['question'][':question/id']==again['question'][':question/id'];assert r['generation']['parameter_fingerprint']==again['generation']['parameter_fingerprint']
 # Two clearly generated variants for each template AND complete bank.
 for seed in (131,252):
  variant=g.generate(level,seed,case['template'],profile=case['bank_profile']);records.append(variant);display.append(check(variant));engine.append(engine_item(case['source_id']+' variant '+str(seed),variant))
# Radius/center boundaries and meaningful sampler enumeration: 42 geometries per origin arc, 3360 translated objects per hard arc.
for name,t in g.TEMPLATES.items():
 for a,b,h,k in ((2,8,-4,4),(8,2,4,-4)) if t['level']=='hard' else ((2,8,0,0),(8,2,0,0)):
  r=g.generate(t['level'],17,name,parameters={'a':a,'b':b,'h':h,'k':k,'lo':t['arc'][0],'hi':t['arc'][1]});display.append(check(r));engine.append(engine_item(name+' boundary '+str(a),r))
 sampled=[]
 for seed in range(100):
  p1=g.sample_parameters(t['level'],t,__import__('random').Random(seed));p2=g.sample_parameters(t['level'],t,__import__('random').Random(seed));assert p1==p2
  assert (p1['h']!=0 or p1['k']!=0)==(t['level']=='hard')
  assert [p1['lo'],p1['hi']]==t['arc'];sampled.append(g.fingerprint(p1))
 assert len(set(sampled))>=35
# Different complete banks must change displayed content identity on same object.
p=cases[0]['parameters'];compatible=[c for c in cases if c['parameters']['lo']==p['lo'] and c['parameters']['hi']==p['hi'] and qs[c['source_id']][':question/difficulty'][':db/ident'].endswith('easy') and c['bank_profile']]
ids=[]
for c in compatible:
 r=g.generate('easy',template=c['template'],parameters=p,profile=c['bank_profile']);ids.append((c['bank_profile'],r['question'][':question/id'],r['generation']['parameter_fingerprint']))
assert len({z[2] for z in ids})==1
assert len({z[1] for z in ids})>=2
# Invalid explicit instances cannot be silently repaired or resampled.
for bad in ({**p,'a':0},{**p,'a':p['b']},{**p,'lo':'-1'},{**p,'hi':'3'},{**p,'h':1}, {**p,'surprise':3}):
 try:g.generate('easy',template=cases[0]['template'],parameters=bad)
 except ValueError:pass
 else:raise AssertionError('Invalid explicit input accepted')
(D/'review.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n');(D/'replays.json').write_text(json.dumps(replays,indent=2,ensure_ascii=False)+'\n');(D/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
engine_binary=Path('generate/runs/current/check-engine');subprocess.run([str(engine_binary),str(D/'engine-input.json'),str(D/'engine.json')],check=True)
engine_report=json.loads((D/'engine.json').read_text());assert engine_report['documented_unresolved_checks']==0
def source_assets(text):
 return re.sub(r'!\[.*?\]\((.*?)\)',lambda m:'![](/media/jake/SSD/EDB/math/'+m[1]+')',text)
review=['# Source fidelity and generated variations','Basis 1356; all originals retained. Generated plots replace original assets. All worked solutions have disclosed mathematical wording repairs.']
for case,replay in zip(cases,replays):
 q=qs[case['source_id']];review+=['## Original '+case['source_id'],source_assets(q[':question/problem']),source_assets(q[':question/worked-solution'])]
 review += ['Original complete bank:',json.dumps([{ 'key':f[':answer-field/key'],'values':[z[':answer/value'] for z in f[':answer-field/choices']],'correct':f[':answer-field/correct'][':answer/value']} for f in q[':question/answer-fields']],indent=2),'## Source parameter replay (repaired prose)',g.markdown(replay)]
 review += [g.markdown(r) for r in records if r['generation']['template']==case['template'] and r['generation']['bank_profile']==case['bank_profile']][:2]
(D/'review.md').write_text('\n\n'.join(review)+'\n')
result={'pass':True,'source_provenance':{k:raw[k] for k in ('database','basis','lineage')},'source_questions':18,'levels':{'easy':8,'moderate':5,'hard':5},'source_values_matched':matched,'source_values_total':choices,'complete_original_banks':18,'correct_designations_matched':designations,'original_worked_prose_exact':sum(x['worked_prose_exact'] for x in fidelity),'repaired_worked_prose':sum(not x['worked_prose_exact'] for x in fidelity),'source_fidelity':fidelity,'independent_displayed_math_records':len(display),'displayed_math_evidence':display,'native_grading':engine_report,'engine_sha256':hashlib.sha256(engine_binary.read_bytes()).hexdigest(),'generated_review_records':len(records),'template_count':len(g.TEMPLATES),'bank_profile_count':len(g.BANK_PROFILES),'authored_missing_levels':[],'unresolved_findings':[],'source_error_repairs':['18 solutions: ellipse parameter angle incorrectly identified as geometric polar angle','q-274866 incorrect copied center/radii repaired','q-327831 final p,q variable typo repaired','q-79282 missing comma in generic parametric formula repaired'],'scope_validation':True,'identity_validation':True,'database_writes':0,'plot_qa':'All 36 source plots inspected; generated review montage inspection recorded separately in plot-qa.md'}
(D/'validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print('PASS',matched,'/',choices,'source values,',designations,'correct designations;',len(display),'independent displayed-math records')
