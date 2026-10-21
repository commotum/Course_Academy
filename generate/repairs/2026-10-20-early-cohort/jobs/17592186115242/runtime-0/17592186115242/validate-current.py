"""Reconcile captured live source banks with the frozen generator's exact replays."""
import hashlib, importlib.util, json, pathlib, re, sys
sys.dont_write_bytecode=True
D=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(D));import validate as v
g=v.g
sys.path.insert(0,str(D.parents[2]/'scripts/question_capture'));from edn import loads
P=D/'reference/replenishment/initial'
x=loads((P/'kp.edn').read_text())[0][0]
sid='q-131725';q=next(q for q in x[':knowledge-point/questions'] if q.get(':question/math-academy-id')==sid)
p=dict(a=2,b=-1,c=3,d=-4,u=1,v=-5,e=-1)
style={'swap':False,'rowop':'plus','negative_coeff_factored':False}
problem=q[':question/problem'].replace(' &=','=')
solution=q[':question/worked-solution'].replace(' &=','=')
solution=re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',lambda m:g.matrix([[c.strip() for c in row.split('&')] for row in m[1].split(r'\\')]),solution,flags=re.S)
comp=g.components(p,style)
for key in ['matrix0','matrix2','rowop','equation1','equation2','pivot_equation','reduced_equation','answer','zero_equation']:
    if comp[key]:
        problem=problem.replace(comp[key],'@@'+key+'@@');solution=solution.replace(comp[key],'@@'+key+'@@')
# Offsets are observed patterns with unresolved error intent, replay-only.
profile={'template':'inconsistent_shift','level':'moderate','parameters':p,'style':style,'problem_mask':problem,'solution_mask':solution,'bank':['t+3','t+1','t','t-2','t-1'],'bank_interpretation':'Observed complete bank: offsets +3,+1,0,-2,-1 from t=7. Error intent unresolved; explicit replay profile, never default.'}
recipes=json.loads((D/'recipes.json').read_text());recipes[sid]=profile
(D/'recipes.json').write_text(json.dumps(recipes,indent=2)+'\n')
cases=json.loads((D/'source-cases.json').read_text());byid={c['source_id']:c for c in cases};byid[sid]={'source_id':sid,'template':profile['template'],'parameters':p,'level':'moderate','bank_profile':sid}
reports=[];native=[]
for source in x[':knowledge-point/questions']:
    sid=source[':question/math-academy-id'];c=byid[sid]
    rec=g.generate(c['level'],seed=33,template=c['template'],parameters=c['parameters'],profile=sid);v.printed_check(rec)
    sf=source[':question/answer-fields'][0];f=rec['question'][':question/answer-fields'][0]
    sourcebank={v.parse(a[':answer/value'].split('=',1)[1]) for a in sf[':answer-field/choices']}
    genbank={v.parse(a[':answer/value'].split('=',1)[1]) for a in f[':answer-field/choices']}
    assert len(sourcebank)==len(genbank)==5 and sourcebank==genbank
    sv=v.parse(sf[':answer-field/correct'][':answer/value'].split('=',1)[1]);gv=v.printed_check(rec);assert sv==gv
    # Printed current source equations independently establish original parameters.
    eqs=v.equations(source[':question/problem']);replay=v.equations(rec['question'][':question/problem']);assert all(v.s.simplify(a-b)==0 for a,b in zip(eqs,replay))
    reports.append({'source':sid,'level':c['level'],'template':c['template'],'profile':sid,'parameters':c['parameters'],'complete_bank':True,'matched_choices':5,'matched_distractors':4,'correct_designation':True,'current_printed_system_matches_replay':True})
    native.append(v.engine_case(sid,rec))
# Changed parameters for new source profile preserve the whole bank, not pooled recipes.
changed=[]
for seed in range(10):
    r=g.generate('moderate',seed=seed+100,profile='q-131725');v.printed_check(r);changed.append(r);native.append(v.engine_case('supplemental-variant-'+str(seed),r))
(P/'current-source-bank-replay.json').write_text(json.dumps({'passed':True,'basis':json.loads((P/'basis.json').read_text())['basis'],'source_questions':len(reports),'matched_banks':len(reports),'matched_choices':5*len(reports),'matched_distractors':4*len(reports),'sources':reports,'plots':'none; displayed mathematics only'},indent=2)+'\n')
(P/'supplemental-variants.json').write_text(json.dumps(changed,indent=2)+'\n');(P/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
print(json.dumps({'passed':True,'current_source_banks':len(reports),'matched_choices':5*len(reports),'matched_distractors':4*len(reports),'changed_profile_instances':len(changed)}))
