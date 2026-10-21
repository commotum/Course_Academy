import sys,json,pathlib,importlib.util,collections,hashlib
sys.dont_write_bytecode=True
from independent_math import *
E=pathlib.Path(__file__).resolve().parent;P=E.parent/'workspace';sys.path.insert(0,str(P))
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def dump(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
g=load(P/'17592186115241.py','current')
prior=E.parent/'review-1-policy-2-64575e53a5a82ae1';old=load(prior/'relocated/17592186115241.py','prior')
def frac(r):
 cs=field(r)[':answer-field/choices'];a=[c for c in cs if '\\frac' in c[':answer/value']];return {'fraction_choices':len(a),'shortcut_correct':len(a)==1 and a[0][':answer/id']==correct(r)}
before=old.generate_easy(seed=71381,profile='q-32244');after=g.generate_easy(seed=71381,profile='q-32244')
assert frac(before)['shortcut_correct'];assert not frac(after)['shortcut_correct']
checks=[]
for fname in ['checks/validate_repair.py','checks/rational_support.py']:
 h=hashlib.sha256((P/fname).read_bytes()).hexdigest();pf=json.load(open(E.parent/'repair-preflight.json'));ref=next(x for x in pf['checks'] if x['script']==fname);assert ref['sha256']==h
 checks.append({'script':fname,'hash_matches_preflight':True,'sha256':h})
dump('fraction-repair-verification.json',{'command':str(sys.executable)+' -B changed_probes.py','prior_package_binding':'88f8e004aec0258b99a46635c01a49f6a0d6a23ce6470a62b47397679ab0afa2','before':{'record':before,'probe':frac(before)},'after':{'record':after,'probe':frac(after)},'preflight_scripts':checks})
# New tests only for the apparent perfect equal-coordinate cue and underrepresented free-y case.
controls=[g.generate_easy(seed=s,template='authored_easy_'+case) for case in ['equal_coordinates','free_y'] for s in range(83210,83222)]
dump('cue-control-records.json',controls)
rows=[]
for r in json.load(open(E/'source-shortcut-records.json'))+controls:
 M=system(r['question'][':question/problem']);piv=M.rref()[1];fc=next(j for j in range(M.cols-1) if j not in piv);t=v[fc];cs=field(r)[':answer-field/choices'];vv=[vec(c[':answer/value']) for c in cs];ki=next(i for i,c in enumerate(cs) if c[':answer/id']==correct(r))
 feats={
 'absolute_intercept':[sum(abs(e.subs(t,0)) for e in x) for x in vv],
 'absolute_slope':[sum(abs(sp.diff(e,t)) for e in x) for x in vv],
 'fraction_count':[c[':answer/value'].count('\\frac') for c in cs],
 'text_length':[len(c[':answer/value']) for c in cs],
 'first_intercept':[x[0].subs(t,0) for x in vv]}
 sig=[tuple((int(x[j].subs(t,0).q),int(sp.diff(x[j],t).q)) for j in piv) for x in vv]
 assert len(set(sig))==1,('notation distinguishes key',sig)
 outcomes={}
 for f,scores in feats.items():
  for direction,extreme in [('min',min(scores)),('max',max(scores))]:
   ix=[i for i,x in enumerate(scores) if x==extreme]
   if len(ix)==1:outcomes[f+'_'+direction]={'selected_position':ix[0]+1,'correct':ix[0]==ki}
 rows.append({'id':r['question'][':question/id'],'seed':r['generation']['seed'],'template':r['generation']['template'],'key_position':ki+1,'notation_signature':str(sig[0]),'outcomes':outcomes,'math':mathcheck(r)})
summary={}
for template in sorted(set(x['template'] for x in rows)):
 rs=[x for x in rows if x['template']==template];counts={}
 for row in rs:
  for cue,out in row['outcomes'].items():
   z=counts.setdefault(cue,{'correct':0,'total':0});z['total']+=1;z['correct']+=out['correct']
 summary[template]={'count':len(rs),'key_positions':dict(collections.Counter(str(x['key_position']) for x in rs)),'cues':counts}
dump('changed-probe-results.json',{'command':str(sys.executable)+' -B changed_probes.py','rows':rows,'summary':summary,'controls_seeds':[83210,83221],'control_templates':['authored_easy_equal_coordinates','authored_easy_free_y']})
print(json.dumps({'fraction_repair':{'before':frac(before),'after':frac(after)},'control_count':len(controls),'conditional_summary':summary},indent=2))
