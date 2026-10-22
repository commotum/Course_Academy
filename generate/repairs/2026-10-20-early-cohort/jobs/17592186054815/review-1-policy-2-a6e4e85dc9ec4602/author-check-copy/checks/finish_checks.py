"""Delivery-stage cue audit, relocation, and read-only captured-inventory account."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,subprocess,shutil,platform,re
from collections import Counter,defaultdict
W=Path(__file__).resolve().parent.parent;E=W/'evidence'
from oracle import mask,target,enum,correct_value,verify,subset

def save(name,obj): (E/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def semantic_value(e):
    from fractions import Fraction
    from math import isqrt
    t=re.search(r'\$([^$]+)\$',e)[1];t=re.sub(r'\s+','',t)
    sg=-1 if t.startswith('-') else 1;t=t.lstrip('-')
    if '\\pi' in t:
        m=re.search(r'\\frac\{\\pi\}\{(\d+)\}',t)
        return ('pi',Fraction(sg,int(m[1]) if m else 1))
    m=re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',t)
    if m:
        coef=sg*int(m[1] or 1);b=int(m[2])
        if isqrt(b)**2==b:return ('rational',Fraction(coef*isqrt(b)))
        factor=next(n for n in range(isqrt(b),0,-1) if b%(n*n)==0)
        return ('root',coef*factor,b//(factor*factor))
    m=re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}',t)
    return ('rational',Fraction(sg*int(m[1]),int(m[2])) if m else sg*Fraction(t))

def metrics(rs):
    groups=defaultdict(list)
    semantic=set()
    for r in rs:
        q=r['question'];t=target(q);mode=enum(q[':question/answer-fields'][0][':answer-field/type']).split('/')[-1]
        groups[''.join((t[0],'0' if t[1] else '',t[2]))+'/'+mode].append(r)
        from oracle import entries
        semantic.add((t,tuple(semantic_value(e) for e in entries(q))))
    out={}
    for key,rr in groups.items():
        masks=[mask(r) for r in rr];n=len(rr);freq=Counter(masks)
        probes={f'fixed_subset_{m}':{'successes':freq[m],'attempts':n} for m in range(16)}
        # Every ordinary position must sometimes qualify and sometimes fail.
        assert all({bool(m&(1<<i)) for m in masks}=={False,True} for i in range(4)),key
        assert len(set(masks))>1,key
        counts=Counter(m.bit_count() for m in masks)
        result={'n':n,'masks':dict(sorted(freq.items())),'correct_number_counts':dict(sorted(counts.items())),
                'fixed_subset_probes':probes,'complete_subset_uniform_baseline':1/16,
                'empirical_best_fixed_subset':max(freq.values())/n}
        if key.endswith('/radio'):
            correct_positions=[];cue_hits=Counter();attempts=Counter()
            for r,m in zip(rr,masks):
                f=r['question'][':question/answer-fields'][0]
                ms=[subset(a[':answer/value']) for a in f[':answer-field/choices']]
                ci=ms.index(m);correct_positions.append(ci)
                for cue in (0,15):
                    name='choose_explicit_subset_'+str(cue)+'_when_offered'
                    if cue in ms:
                        attempts[name]+=1;cue_hits[name]+=int(m==cue)
                for name,pos in [('first',0),('last',4),('fewest_members',min(range(5),key=lambda i:ms[i].bit_count())),('most_members',max(range(5),key=lambda i:ms[i].bit_count()))]:
                    attempts[name]+=1;cue_hits[name]+=int(pos==ci)
            assert len(set(correct_positions))>1,key
            result['radio_positions']=dict(Counter(correct_positions));result['radio_choice_baseline']=1/5
            result['radio_cue_probes']={k:{'successes':cue_hits[k],'attempts':attempts[k]} for k in attempts}
            assert all(cue_hits[k]<attempts[k] for k in attempts), (key,result['radio_cue_probes'])
        out[key]=result
    return {'records':len(rs),'semantic_instances_ignoring_response_and_bank':len(semantic),'groups':out}
raw=json.loads((E/'delivery-input.json').read_text());accepted=json.loads((E/'delivery/accepted.json').read_text())
before=metrics(raw);after=metrics(accepted)
assert before==after
save('pedagogical-variation.json',{'passed':True,'before_delivery':before,'after_delivery':after,
    'counterfactual_evidence':'counterfactual-records.json; masks [5,7,9,8,1,5] under both response contracts. Relevant class/zero/target changes alter keys; within-class fraction change preserves subset.',
    'generation_rejection':'Sampler selects target/mask/response, then each number from compatible class/sign/form groups excluding already used exact semantic values. No post-sampling answer-dependent filtering; no rejection in tested explicit masks. Source-backed explicit None admits empty ordinary subsets without an empty correct checkbox selection.',
    'normal_sampling':'28 fresh sequential instances seed 1442108295, including both response contracts and all seven targets. Controlled masks supplement fresh sampling; counts are coverage, not quotas.',
    'selection_limits':'Actual shared check_delivery examines captured inventory, difficulty and deduplication. question_selection.rs selects difficulty band then an item from fresh usable candidates; all current items are easy. Learner seen-question history, policy weights, reservations and entity identities unavailable; no live selection claim.',
    'scope':'No perfect tested fixed-subset/position/cardinality strategy. All tested target/response groups contain changing qualifying roles. This is not an exhaustive classifier search.'})
# Relocate exactly the declared runtime package; execute with a foreign cwd.
manifest=json.loads((W/'package.json').read_text());rel=E/'relocated';rel.mkdir(exist_ok=True)
assert manifest['dependencies']=={'python':platform.python_version(),'packages':{}}
assert 'package.json' not in manifest['files']
for f in manifest['files']:
    p=Path(f);assert not p.is_absolute() and '..' not in p.parts and (W/p).is_file()
    dest=rel/p;dest.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(W/p,dest)
def run(root,args):
    return subprocess.run([sys.executable,'-B',str(root/manifest['entrypoint'])]+args,cwd='/tmp',capture_output=True,text=True)
args=['--difficulty','easy','--count','5','--seed','1442108295','--format','json']
a=run(W,args);b=run(W,args);c=run(rel,args)
assert a.returncode==b.returncode==c.returncode==0,(a.stderr,c.stderr)
assert a.stdout==b.stdout==c.stdout
assert json.loads(a.stdout)==json.loads((E/'batch-records.json').read_text())
rr=run(rel,['--replay-source']);assert rr.returncode==0 and len(json.loads(rr.stdout))==11
bounds=[]
for args,want in [(['--count','0'],0),(['--count','-1'],2),(['--difficulty','hard'],2),(['--difficulty','moderate'],2)]:
    res=run(W,args);assert res.returncode==want
    bounds.append({'args':args,'exit':res.returncode})
save('packaging-checks.json',{'passed':True,'python':platform.python_version(),'manifest':manifest,'deterministic':True,'relocation':True,'source_replay_relocated':11,'cli_boundaries':bounds,'cwd':'/tmp','assets':'none','runtime_files_copied':manifest['files']})
# Inspect every captured inventory item. Keep source identities distinct.
job=W.parent;inv=json.loads((job/'source/inventory.json').read_text());src=json.loads((job/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions'];source_ids={q[':question/id'] for q in src}
observed=[]
source_by_id={q[':question/id']:q for q in src}
def bank(q):
    return sorted((re.sub(r'\s+','',f[':answer-field/key']),enum(f[':answer-field/type']),sorted(a[':answer/value'] for a in f[':answer-field/choices'])) for f in q[':question/answer-fields'])
for q in inv['questions']:
    fields=q[':question/answer-fields'];has_key=all(f.get(':answer-field/correct') for f in fields)
    mode=enum(fields[0][':answer-field/type']).split('/')[-1]
    item={'question_id':q[':question/id'],'entity_id':q[':db/id'],'source':q[':question/id'] in source_ids,'response':mode,'fields':len(fields),'contains_none':any(f[':answer-field/key'] in ('None','None of the above') for f in fields)}
    if item['source']:
        assert bank(q)==bank(source_by_id[q[':question/id']])
        item['source_bank_matches']=True
    if has_key:
        verify({'question':q,'generation':{}},solutions=False)
        item['mathematical_key_verified']=True
        if mode=='checkbox':
            truths=[correct_value(f)=='true' for f in fields]
            item['correct_selectable_count']=sum(truths)
            if not any(truths):item['separate_observation']='Legacy empty-correct checkbox item; current generator explicit-None policy prevents this shape. Captured inventory has no generation metadata, so exact generation provenance cannot be reproduced.'
    observed.append(item)
save('inventory-review.json',{'basis':inv['basis'],'examined':len(observed),'items':observed,
    'retained_findings':'Source-family omission is an interface coverage defect, not an erroneous stored record. No stored source replay with an added unobserved None field was demonstrated; all 11 source banks match capture and all five non-source stored banks have four fields.',
    'provenance_limit':'Five non-source records contain no generation metadata; do not label original source questions as generated. One legacy all-false checkbox is separately observable (1f5000c7-50e0-5fb4-a184-91dafeef5f7c), but exact generated-record provenance/seed is unavailable. Empty affected_questions refers only to demonstrated, reproducible instances of the two retained findings, not a claim that stored inventory has no other weakness.'})
# Required relative-to-workspace evidence; no fabricated generation metadata.
save('affected-inventory.json',{'affected_questions':[]})
save('render-inspection.json',{'passed':True,'screenshots_inspected':['render/question-%03d.png'%i for i in range(1,7)],'observations':'All six screenshots visually inspected. Prompt targets, roots, fractions, signs, zero, option labels and worked solutions readable, no clipping/overlap/dangling delimiters. Original numbered Z0+ source preserves Arabic enumeration with Roman subset bank; ordinal correspondence retained. Four-field replay has no added None; fresh empty ordinary subset has explicit selectable None.'})
print(json.dumps({'shortcut_and_delivery_passed':True,'delivery_records':len(accepted),'semantic_instances':after['semantic_instances_ignoring_response_and_bank'],'groups':len(after['groups']),'packaging_passed':True,'inventory_examined':len(observed)}))
