"""Executable retained regressions; read visible records and integrate boundaries.
All output goes to workspace evidence; runtime package files are read-only.
"""
import sys, os, json, importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent; W=E.parent
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(E/'runtime')
os.environ['MPLCONFIGDIR']=str(E/'mpl-cache')
spec=importlib.util.spec_from_file_location('current_generator',W/'17592186129197.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from independent_oracle import s, parse, correct, oracle, probe

def save(name,data): (E/name).write_text(json.dumps(data,indent=2,ensure_ascii=False,default=str)+'\n')
def values(r):return [parse(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
def keyvalue(r):return parse(correct(r['question'])[':answer/value'])
def rank(r):return sum(float(z)<float(keyvalue(r))-1e-10 for z in values(r))
def field_contract(field):
 correct_ref=field.get(':answer-field/correct')
 correct_id=correct_ref.get(':answer/id') if isinstance(correct_ref,dict) else correct_ref[1] if correct_ref else None
 attrs={k:v for k,v in field.items() if k not in [':db/id',':answer-field/id',':answer-field/choices',':answer-field/correct']}
 if isinstance(attrs[':answer-field/type'],dict):attrs[':answer-field/type']=attrs[':answer-field/type'][':db/ident']
 bank=[]
 for a in field[':answer-field/choices']:
  item={k:v for k,v in a.items() if k not in [':db/id',':answer/id']}
  if isinstance(item[':answer/type'],dict):item[':answer/type']=item[':answer/type'][':db/ident']
  bank.append(item)
 return {'attributes':attrs,'bank':sorted(bank,key=lambda a:a[':answer/value']),'correct':next((a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==correct_id),None)}

def source_check():
 # Supplied immutable source is independent of the bundled replay input.
 source=json.loads((W.parent/'source/source.json').read_text());results=[];records=[]
 for q in source['material']['kp'][':knowledge-point/questions']:
  r=g.generate('hard',97,profile='raw:'+q[':question/math-academy-id'],parameters={'scale':1});a=r['question'];records.append(r)
  assert a[':question/problem']==q[':question/problem'], q[':question/id']
  assert a.get(':question/worked-solution')==q.get(':question/worked-solution')
  expected=q.get(':question/difficulty',{}).get(':db/ident')
  assert a.get(':question/difficulty')==expected
  assert [field_contract(f) for f in a[':question/answer-fields']]==[field_contract(f) for f in q[':question/answer-fields']]
  owned=[]
  for f in a[':question/answer-fields']:
   owned.append(f[':answer-field/id']);owned.extend(z[':answer/id'] for z in f[':answer-field/choices'])
   if f.get(':answer-field/correct'):assert f[':answer-field/correct'][1] in [z[':answer/id'] for z in f[':answer-field/choices']]
  assert len(owned)==len(set(owned))
  assert r['generation']['source']['basis']==source['basis']
  results.append({'source':q[':question/id'],'fields':len(a[':question/answer-fields']),'complete_contract_equal':True})
 old=g.generate('hard',97,profile='historical:q-82874',parameters={'scale':1})
 assert len(old['question'][':question/answer-fields'])==2
 save('source-replay-records.json',records);save('source-replay.json',{'current':results,'historical_duplicate_field_preserved':True})
 print('Source regression: 12 current contracts, historical two-field record preserved.')

def shortcut_check():
 records=[];summary=[];counterfactual=[]
 for f,(_,band) in g.FAMILIES.items():
  seed=8191
  base=g.generate(band,seed,template=f)
  targets=[g.generate(band,seed,template=f,parameters=p) for p in base['generation']['bank_parameters']]
  banks=[sorted(map(str,values(r))) for r in targets]
  assert all(bank==banks[0] for bank in banks),f
  assert sorted(rank(r) for r in targets)==[0,1,2,3,4],f
  # One visible bank must support five distinct mathematical answers. This
  # defeats ANY deterministic bank-only predictor, not just signed-pair/median.
  assert len(set(str(keyvalue(r)) for r in targets))==5
  assert len({r['question'][':question/problem'] for r in targets})==5
  for r in targets:assert not probe(r)['success'],f
  positions=[next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==correct(r['question'])[':answer/id']) for r in targets]
  assert set(positions)==set(range(5)),(f,positions)
  normal=[g.generate(band,seed,template=f) for seed in [701,911,1237]]
  records+=targets+normal
  summary.append({'template':f,'same_bank_correct_ranks':[rank(r) for r in targets],'correct_positions':positions,'normal_ranks':[rank(r) for r in normal],'signed_pair_successes':sum(probe(r)['success'] for r in targets+normal)})
  counterfactual.append({'template':f,'records':[r['question'][':question/id'] for r in targets],'same_bank':True,'all_five_answers_required':True})
 exact=[g.generate('easy',8191,template='simple',parameters=p) for p in [{'a':1,'h':1,'k':0},{'a':1,'h':4,'k':0},{'a':8,'h':1,'k':0}]]
 assert not probe(exact[0])['success']
 assert s.simplify(keyvalue(exact[0])-s.Rational(4,3))==0
 assert keyvalue(exact[0])!=keyvalue(exact[1]);assert keyvalue(exact[0])==keyvalue(exact[2])
 records+=exact
 math=[];grader=[]
 for i,r in enumerate(records):
  area=oracle(r['question'])['area'];key=keyvalue(r)
  assert s.simplify(area-key)==0, (i,area,key)
  choices=r['question'][':question/answer-fields'][0][':answer-field/choices']
  vals=values(r)
  assert len(vals)==5 and all(s.simplify(z-w)!=0 for j,z in enumerate(vals) for w in vals[:j])
  final=r['question'][':question/worked-solution'].split('&=')[-1].split(r'\end{aligned}')[0].strip()
  assert s.simplify(parse(final)-area)==0,(i,final,area)
  math.append({'index':i,'id':r['question'][':question/id'],'independent_area':str(area),'key_and_solution_match':True})
  grader.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if s.simplify(parse(a[':answer/value'])-area)==0 else 'rejected','purpose':'Independent integration of printed map and boundaries'} for a in choices]})
 save('samples.json',records);save('shortcut-results.json',summary);save('counterfactual-results.json',counterfactual);save('math.json',math);save('grader-input.json',grader)
 for band in ['easy','moderate','hard']:save('samples-'+band+'.json',[r for r in records if r['question'][':question/difficulty']==':question.difficulty/'+band])
 save('render-records.json',[records[0],next(r for r in records if r['generation']['template']=='hyper_y')])
 print('Shortcut regression: eight common-bank five-target witnesses; 67 independently integrated records; 335 grader cases prepared.')

if __name__=='__main__':
 mode=sys.argv[1] if len(sys.argv)>1 else 'all'
 if mode in ['all','source']:source_check()
 if mode in ['all','shortcut']:shortcut_check()
