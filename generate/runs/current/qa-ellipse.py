"""Parent exact fields and visual source arcs, plus printed ellipse geometry."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186152190;D=R.parents[2]/f'generate/scratch/{K}'
z=importlib.util.spec_from_file_location('parent_ellipse',D.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
ARCS={'q-78682':('0','1/2'),'q-79278':('1','2'),'q-106400':('0','1'),'q-106402':('0','1/2'),'q-106403':('1','3/2'),'q-106404':('1/2','3/2'),'q-106711':('3/2','2'),'q-274866':('0','1/2'),'q-327822':('0','1/2'),'q-327828':('0','1/2'),'q-327831':('3/2','2'),'q-327835':('0','1'),'q-327847':('0','1/2'),'q-328327':('1/2','3/2'),'q-79273':('0','1'),'q-79275':('0','1'),'q-79280':('0','1/2'),'q-79282':('0','1')}
def angle(v):
 v=v.replace(' ','').replace(r'\pi','P');v=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'(\1)/(\2)',v);v=re.sub(r'(\d)P',r'\1*P',v);return s.simplify(s.sympify(v,locals={'P':s.pi}))
def domain(v):
 m=re.search(r'\[(.*?),(.*?)(\]|\))',v);assert m,v
 return angle(m[1]),angle(m[2]),m[3]==']'
def eqs(v):
 pattern=r'x=(\d+)\\operatorname\{cos\}⁡\\theta\s*([-+]\d+)?,\\,y=(\d+)\\operatorname\{sin\}⁡\\theta\s*([-+]\d+)?'
 return [(int(a),int(b),int(h or 0),int(k or 0)) for a,h,b,k in re.findall(pattern,v)]
def norm(v):return re.sub(r'!\[.*?\]\([^)]*\)','![](PLOT)',v)
def prose(v):
 v=re.sub(r'we associate the parameter .*?(?=\n\n)', 'ANGLE SENTENCE.',v,flags=re.S)
 v=re.sub(r'we again interpret .*?(?= On the quarter-arc)', 'ANGLE SENTENCE.',v,flags=re.S)
 v=re.sub(r'!\[.*?\]\([^)]*\)','PLOT',v);v=re.sub(r'\$\$.*?\$\$','DISPLAY',v,flags=re.S);v=re.sub(r'\$[^$]*\$','INLINE',v)
 # One documented repaired teaching sentence; remaining prose must persist.
 v=re.sub(r'we associate the parameter .*?\.', 'ANGLE SENTENCE.',v)
 return re.sub(r'\s+',' ',v).strip()
counts={'source_questions':0,'source_radio_banks':0,'source_values':0,'source_blank_fragments':0,'source_correct_refs':0,'exact_source_prompts_except_assets':0,'unmodified_prose_outside_repaired_sentence':0,'independently_visual_source_domains':0,'printed_curve_records':0}
def check(r,bounds):
 q=r['question'];equations=eqs(q[':question/problem']);assert len(equations)==1;a,b,h,k=equations[0];assert a>0 and b>0 and a!=b
 lo,hi=[s.Rational(v)*s.pi for v in bounds];assert 0<=lo<hi<=2*s.pi
 shown=eqs(q[':question/worked-solution']);assert shown==[equations[0],equations[0]]
 assert q[':question/worked-solution'].count('$')%2==0,('unbalanced math delimiters',q[':question/worked-solution'])
 assert 'central angle' not in q[':question/worked-solution'];assert 'unit circle' in q[':question/worked-solution']
 t=s.Symbol('t',real=True);xt=h+a*s.cos(t);yt=k+b*s.sin(t);assert s.trigsimp(((xt-h)/a)**2+((yt-k)/b)**2)==1
 fs=q[':question/answer-fields']
 for f in fs:
  selected=next(v for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1])
  if f[':answer-field/type'].endswith('/radio'):
   values=[domain(v[':answer/value']) for v in f[':answer-field/choices']];assert len(values)==len(set(values))==5;assert values.count((lo,hi,True))==1;assert domain(selected[':answer/value'])==(lo,hi,True)
  else:assert angle(selected[':answer/value'])==(lo if f[':answer-field/key']=='field-1' else hi)
 for path in r['generation']['plot_assets'].values():
  path=Path(path);spec=json.loads(path.with_name(path.name.split('-')[0]+'.json').read_text());p=spec['parameters'];assert (p['a'],p['b'],p['h'],p['k'])==(a,b,h,k);assert [s.Rational(p[v])*s.pi for v in ('lo','hi')]==[lo,hi]
 counts['printed_curve_records']+=1
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=qs[c['source_id']];level=old[':question/difficulty'][':db/ident'].split('/')[-1];r=g.generate(level,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];check(r,ARCS[c['source_id']]);counts['independently_visual_source_domains']+=1
 assert norm(old[':question/problem'])==norm(q[':question/problem']);counts['exact_source_prompts_except_assets']+=1
 assert prose(old[':question/worked-solution'])==prose(q[':question/worked-solution']),(c['source_id'],prose(old[':question/worked-solution']),prose(q[':question/worked-solution']));counts['unmodified_prose_outside_repaired_sentence']+=1
 bykey={f[':answer-field/key']:f for f in q[':question/answer-fields']}
 for of in old[':question/answer-fields']:
  f=bykey[of[':answer-field/key']];radio=f[':answer-field/type'].endswith('/radio');parse=domain if radio else angle
  assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted([parse(v[':answer/value']) for v in f[':answer-field/choices']],key=str)==sorted([parse(v[':answer/value']) for v in of[':answer-field/choices']],key=str)
  selected=next(v for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1]);assert parse(selected[':answer/value'])==parse(of[':answer-field/correct'][':answer/value']);counts['source_correct_refs']+=1
  counts['source_values']+=len(f[':answer-field/choices'])
  if radio:counts['source_radio_banks']+=1
  else:counts['source_blank_fragments']+=1
 counts['source_questions']+=1
records=json.loads((D/'review.json').read_text())+[x['record'] for x in json.loads((D/'engine-input.json').read_text())];seen=set()
for r in records:
 if r['question'][':question/id'] in seen:continue
 seen.add(r['question'][':question/id']);p=r['generation']['parameters'];check(r,[p['lo'],p['hi']])
counts['distinct_review_and_boundary_records']=len(seen);counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
