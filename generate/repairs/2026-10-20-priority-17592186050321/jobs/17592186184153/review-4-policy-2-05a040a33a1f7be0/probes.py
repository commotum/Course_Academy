"""Independent changed-rule and retained-counterexample audit. All output stays here."""
import sys
sys.dont_write_bytecode=True
import json,pathlib,random,collections,itertools,importlib.util
from fractions import Fraction as F
from audit_math import *
R=pathlib.Path(__file__).resolve().parent;J=R.parent
sys.path.insert(0,str(J/'workspace'));import generator as G
save=lambda n,v:(R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
load=lambda n:json.loads((R/n).read_text())
def visible(r):
 integ,v=extract(r);x=V[v];rows=[]
 for a in field(r)[':answer-field/choices']:
  val=S.expand(tex(a[':answer/value'])-V['C']);c=val.coeff(x);rest=S.simplify(val-c*x)
  rows.append({'id':a[':answer/id'],'linear':F(str(c)),'power':F(str(rest.subs(x,1))),'length':len(a[':answer/value'])})
 return rows,F(str(S.expand(integ).coeff(x,0)))
def strategies(r):
 rows,k=visible(r);cs=collections.Counter(z['linear'] for z in rows);ps=collections.Counter(z['power'] for z in rows)
 matched=[z for z in rows if z['linear']==k]
 d={'range6':[z for z in rows if abs(z['linear'])<=6],
 'eliminate_singleton':[z for z in rows if cs[z['linear']]>1],
 'choose_singleton':[z for z in rows if cs[z['linear']]==1],
 'min_constant':[z for z in rows if abs(z['linear'])==min(abs(t['linear']) for t in rows)],
 'max_constant':[z for z in rows if abs(z['linear'])==max(abs(t['linear']) for t in rows)],
 'shortest':[z for z in rows if z['length']==min(t['length'] for t in rows)],
 'longest':[z for z in rows if z['length']==max(t['length'] for t in rows)],
 'constant_then_max':[z for z in matched if abs(z['power'])==max(abs(t['power']) for t in matched)],
 'constant_then_min':[z for z in matched if abs(z['power'])==min(abs(t['power']) for t in matched)],
 'constant_then_most':[z for z in matched if ps[z['power']]==max(ps[t['power']] for t in matched)],
 'typography':[z for z in matched if abs(z['power']).numerator==1 and abs(z['power']).denominator<10]}
 d.update({'position'+str(j):[rows[j]] for j in range(5)})
 key=answer(r)[':answer/id'];rng=random.Random('independent-ties-'+r['question'][':question/id'])
 # Empty filters fall back to the full constant-matched row.
 return {cue:{'selected':(z:=rng.choice(pool or matched))['id'],'success':z['id']==key,
             'expected_success':float(F(any(a['id']==key for a in (pool or matched)),len(pool or matched))),
             'baseline':1/len(matched) if cue.startswith('constant_') or cue=='typography' else .2}
         for cue,pool in d.items()}
def probe(records):
 trials=[]
 for j,r in enumerate(records):
  if field(r)[':answer-field/type'].endswith('/blank'):continue
  integ,v=extract(r);exponents=[p for (p,) in []] # grouping derives from visible integrand below
  p=next(t.as_powers_dict().get(V[v],S.Integer(0)) for t in S.Add.make_args(integ) if t.has(V[v]))
  profile='R' if p<0 else 'P'
  trials.append({'index':j,'id':r['question'][':question/id'],'profile':profile,'exponent':str(p),'strategies':strategies(r)})
 summary=[]
 for group in ['radio','P','R']+sorted({t['profile']+':'+t['exponent'] for t in trials}):
  ts=[t for t in trials if group=='radio' or group==t['profile'] or group==t['profile']+':'+t['exponent']]
  for cue in ts[0]['strategies'] if ts else []:
   summary.append({'subgroup':group,'cue':cue,'correct':sum(t['strategies'][cue]['success'] for t in ts),'total':len(ts),
     'tie_averaged_rate':sum(t['strategies'][cue]['expected_success'] for t in ts)/len(ts),
     'baseline':sum(t['strategies'][cue]['baseline'] for t in ts)/len(ts)})
 return {'trials':trials,'summary':summary}

# Exact eligible assignment product for changed role rules, at one same-sign triple.
controls=[]
for profile,n in [('P',n) for n in range(2,7)]+[('R',3),('R',7)]:
 for rank,side,omission in itertools.product(range(3),(-1,1),[(0,1),(1,0),(1,1),(2,0),(2,1)]):
  constants=(1,3,6);k=constants[rank];others=[c for c in constants if c!=k]
  f=next(f for f in G.factor_domain(profile,n) if (f>1)==(side>0))
  r=G.build(G.instance(profile,n,-1,k,'x',True,offset=others[0]-k,second_offset=others[1]-k,factors=[f],omitted_row=omission[0],omitted_col=omission[1]),random.Random(901))
  verify(r);controls.append(r)
save('role-controls.json',controls);exact=probe(controls);save('role-control-results.json',exact)
for row in exact['summary']:
 if ':' not in row['subgroup']:continue
 if row['cue'] in ['range6','eliminate_singleton','choose_singleton','min_constant','max_constant','shortest','longest','constant_then_max','constant_then_min','constant_then_most']:
  assert abs(row['tie_averaged_rate']-row['baseline'])<1e-12,row

# Hold full bank fixed and transfer the correct constant among its three values.
cf=[];pairs=[]
for profile,n in [('P',3),('R',3)]:
 for k in [1,3,6]:
  others=[c for c in [1,3,6] if c!=k]
  f=F(4,3) if profile=='P' else F(1,2)
  i=G.instance(profile,n,1,k,'x',True,offset=others[0]-k,second_offset=others[1]-k,factors=[f],omitted_row=2,omitted_col=1)
  r=G.build(i,random.Random(713));verify(r);cf.append(r)
 # Different omitted row changes the bank; ensure a full common alternative bank by omitting the same absolute constant.
 rs=cf[-3:]
 for r in rs:
  i=r['generation']['parameters']; const=[i['k'],i['k']+i['offset'],i['k']+i['second_offset']];i['omitted_row']=const.index(6);i['omitted_col']=1
  r.update(G.build(i,random.Random(713)));verify(r)
 assert all(set(a[':answer/value'] for a in field(r)[':answer-field/choices'])==set(a[':answer/value'] for a in field(rs[0])[':answer-field/choices']) for r in rs)
 pairs.append({'kind':'relevant','change':profile+' target constant 1 -> 3 -> 6, fixed complete bank','indices':list(range(len(cf)-3,len(cf))),'expected':'same answer bank, changed key and worked answer','passed':True})
# R exponent/sign plus irrelevant order is absent from the earlier small controlled suite.
base=G.instance('R',3,1,3,'x',True,offset=-2,second_offset=3,factors=['1/2'])
for change,delta,kind in [('reciprocal_exponent',{'n':7,'factors':['5/3']},'relevant'),('reciprocal_sign',{'s':-1},'relevant'),('reciprocal_order',{'constant_first':False},'irrelevant')]:
 a=G.build(base,random.Random(81));b=G.build(dict(base,**delta),random.Random(81));verify(a);verify(b);j=len(cf);cf += [a,b]
 same=equal(tex(answer(a)[':answer/value']),tex(answer(b)[':answer/value']));assert same==(kind=='irrelevant')
 pairs.append({'kind':kind,'change':change,'indices':[j,j+1],'expected':'preserved' if kind=='irrelevant' else 'changed','passed':True})
save('additional-counterfactual-records.json',cf);save('additional-counterfactual-results.json',pairs)

# Reproduce all retained failures on the actual historical visible records/modules.
history=load('../repair-history.json');hist=[];old_records=[]
for f in history['findings']:
 d=pathlib.Path(f['review_directory']);fid=f['id']; oldpath=d/'relocated/generator.py'
 spec=importlib.util.spec_from_file_location('old_'+fid,oldpath);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
 if fid=='616fcc41bbddb77320ee':
  rs=[r for r in old.generate(count=240,seed=86184906) if r['generation']['parameters']['profile']=='P' and r['generation']['parameters']['n'] in (4,6)]
  vals=[strategies(r)['typography'] for r in rs];assert all(v['expected_success']==1 for v in vals)
  old_records.append(rs[0]);hist.append({'finding':fid,'failing_records':len(rs),'old_cue_rate':1,'current_check':'role-control-results.json: both coefficient sides, all supported exponents; original typography cue no longer uniquely selects key'})
 elif fid=='d78b77b9fcc4f894d32f':
  rs=[r for r in old.generate(count=480,seed=94172863) if r['generation']['parameters']['profile']=='P' and r['generation']['parameters']['n']==2];vals=[strategies(r)['constant_then_max'] for r in rs]
  wins=sum(v['success'] for v in vals);assert wins/len(vals)>.7
  old_records.append(rs[next(j for j,v in enumerate(vals) if v['success'])]);hist.append({'finding':fid,'failing_records':len(rs),'old_correct':wins,'old_baseline':sum(v['baseline'] for v in vals)/len(vals),'current_check':'role-control-results.json: max and min conditional magnitude rates equal constant-only baseline'})
 elif fid=='5587baea103305eacb69':
  r=old.build(old.instance('P',3,-1,5,'x',True,offset=-2,second_offset=2,factors=['4/3'],omitted_row=1,omitted_col=1));v=strategies(r)['eliminate_singleton'];assert v['expected_success']==.25
  old_records.append(r);hist.append({'finding':fid,'old_expected_success':.25,'baseline':.2,'current_check':'role-control-results.json: all non-key omissions; singleton and non-singleton elimination return chance'})
 elif fid=='562a5aa02e27b7f0deff':
  i=dict(profile='R',n=3,s=-1,k=-5,variable='t',constant_first=False,offset=-3,second_offset=-2,factors=[2],omitted_row=0,omitted_col=1)
  r=old.build(i);assert strategies(r)['range6']['expected_success']==1;old_records.append(r)
  try:G.build(i)
  except ValueError:rejected=True
  else:rejected=False
  assert rejected
  replacement=G.build(G.instance('R',3,-1,-5,'t',False,offset=1,second_offset=2,factors=[2],omitted_row=0,omitted_col=1));verify(replacement)
  save('repaired-range-record.json',[replacement]);assert all(1<=abs(z['linear'])<=6 for z in visible(replacement)[0])
  hist.append({'finding':fid,'old_correct':1,'old_total':1,'current_exact_old_assignment_rejected':True,'same_integrand_supported':True,'replacement':'repaired-range-record.json'})
 else:
  r=G.build(G.instance('B',6,1,5,'t',True));save('constant-shift-record.json',[r]);verify(r)
  old_input=json.loads((d/'additional-grader-input.json').read_text());oldfail=old_input[-1];assert oldfail['checks'][-1]['expected']=='accepted'
  save('historical-constant-shift-input.json',[oldfail]);hist.append({'finding':fid,'historical_failure_log':(d/'additional-grading-run.log').read_text(),'current_native_input':'grader-input.json','independent_math':'diff(t^7/7+5*t+1,t)=t^6+5'})
 for entry in hist[-1:]:entry['historical_module']=str(oldpath)
save('historical-failing-records.json',old_records);save('history-verification.json',hist)
# Exercise all current controls and pairs using real grader, including prior-answer probes.
cases=load('grader-input.json')
for label,rs in [('role control',controls),('additional counterfactual',cf)]:
 for j,r in enumerate(rs):
  cases.append({'label':label+' '+str(j),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==answer(r)[':answer/id'] else 'rejected','purpose':'independently differentiated choice'} for a in field(r)[':answer-field/choices']]})
for pair in pairs:
 rs=[cf[j] for j in pair['indices']];a=rs[0]
 for b in rs[1:]:
  prior=[v for v in field(b)[':answer-field/choices'] if equal(tex(v[':answer/value']),tex(answer(a)[':answer/value']))]
  if prior:cases.append({'label':'prior answer '+pair['change'],'record':b,'checks':[{'submitted_answer_id':prior[0][':answer/id'],'expected':'accepted' if pair['kind']=='irrelevant' else 'rejected'}]})
# Exact historical grader example, with expanded/factored equivalents, shifted constants, wrong derivative.
r=load('constant-shift-record.json')[0];val=tex(answer(r)[':answer/value']);x=V['t']
cases.append({'label':'exact retained blank defect','record':r,'checks':[{'submitted':str(v).replace('**','^'),'expected':'accepted' if equal(S.diff(v,x),S.diff(val,x)) else 'rejected'} for v in [val,val+1,val-3,S.factor(val),val+x,S.diff(val,x)]]})
save('grader-input-final.json',cases)
save('render-records-final.json',load('render-records.json')+cf+[load('repaired-range-record.json')[0],r])
(R/'session-state.md').write_text('Completed independent math/source/runtime checks and exact changed-role controls. Historical failures reproduced from earlier generator snapshots. Current relevant and irrelevant controlled cases saved. Delivery/native grading/UI rendering and final decision evidence pending.\n')
print(json.dumps({'controls':len(controls),'additional_counterfactuals':len(cf),'retained_findings':len(hist),'native_cases':len(cases)}))
