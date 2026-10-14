"""Validate every displayed equation and ordered solution independently of keys."""
import copy, hashlib, importlib.util, json, re, subprocess, uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from math_reader import x,y,v,D,DY,rate,prompt_rhs,fingerprint,expression
sp=g.sp
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def equivalent(a,b):
    d=sp.cancel(a-b)
    return d==0 or sp.trigsimp(d)==0

def solution_check(q):
    rhs=prompt_rhs(q[':question/problem']);f=sp.cancel(rhs.subs(y,v*x)-v);expected=f/x
    fields=q[':question/answer-fields'];assert len(fields)==1
    field=fields[0];typ=field[':answer-field/type'];assert (typ.get(':db/ident') if isinstance(typ,dict) else typ)==':answer-field.type/radio'
    bank=field[':answer-field/choices'];assert len(bank)==5
    rates=[rate(a[':answer/value']) for a in bank];matches=[i for i,r in enumerate(rates) if equivalent(r,expected)]
    assert len(matches)==1, 'Rendered bank must have exactly one correct full ODE'
    assert not any(equivalent(a,b) for i,a in enumerate(rates) for b in rates[:i]),'Equivalent distractors'
    cr=field[':answer-field/correct'];cid=str(cr[':answer/id']) if isinstance(cr,dict) else cr[1]
    assert str(bank[matches[0]][':answer/id'])==cid,'Incorrect designated answer'
    # Independently check every algebra stage, including cancellation, subtraction and separation.
    blocks=re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',q[':question/worked-solution']);assert len(blocks)==2
    assert blocks[0]==g.SOURCES['q-14315'][':question/worked-solution'].split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
    rows=blocks[1].split(r'\\');assert len(rows)>=5
    for i,row in enumerate(rows):
        row=row.replace('&','').strip().rstrip('.')
        if i==0:
            left,right=row.split('=');assert left.strip()==DY and equivalent(expression(right),rhs)
        else:
            assert equivalent(rate(row),expected), 'Invalid worked stage: '+row
    for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in bank]:
        assert text.count('{')==text.count('}') and text.count('$')%2==0
    return len(rows)

def independent(r):
    m=r['generation'];q=r['question'];assert r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['id']==g.KP_UUID
    assert q[':question/difficulty']==':question.difficulty/easy'
    assert equivalent(prompt_rhs(q[':question/problem']),g.mathematics(m['template'],m['parameters']['k'])[0])
    assert fingerprint(q[':question/problem'])==m['parameter_fingerprint']
    assert r==g.generate('easy',m['seed'],m['template'],m['parameters'],m['bank_profile'])
    solution_check(q)
    ids=[q[':question/id']]+[f[':answer-field/id'] for f in q[':question/answer-fields']]+[a[':answer/id'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
    assert len(ids)==len(set(ids));[uuid.UUID(i) for i in ids]

def checks(r):
    f=r['question'][':question/answer-fields'][0]
    return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Each source-owned radio option through actual learner grader'} for a in f[':answer-field/choices']]

def build_engine():
    deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps';harness=ROOT/'generate/runs/current/check-engine.rs'
    libs={n:max(deps.glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for n in ('course_academy_engine','serde_json')}
    cmd=['rustc','--edition=2024','-O',str(harness)]
    for n,p in libs.items():cmd+=['--extern',n+'='+str(p)]
    cmd+=['-L','dependency='+str(edb),'-L','dependency='+str(deps),'-o',str(HERE/'check-engine')];subprocess.run(cmd,check=True)
    save('engine-build.json',{'harness_sha256':sha(harness),'libraries':{str(p):sha(p) for p in libs.values()},'binary_sha256':sha(HERE/'check-engine')})

def main():
    records=[];replays=[];coverage={};review=[]
    for t,original in g.ORIGINAL.items():
        src=g.SOURCES[t];solution_check(src);r=g.generate(template=t,parameters={'k':original});independent(r)
        assert r['question'][':question/problem']==src[':question/problem'] and r['question'][':question/worked-solution']==src[':question/worked-solution']
        old=src[':question/answer-fields'][0];new=r['question'][':question/answer-fields'][0]
        assert [a[':answer/value'] for a in new[':answer-field/choices']]==[a[':answer/value'] for a in old[':answer-field/choices']]
        rhs,recipes=g.mathematics(t,original)
        for i,a in enumerate(old[':answer-field/choices']):assert equivalent(rate(a[':answer/value']),recipes[i][1]/recipes[i][0])
        replays.append({'source':t,'source_db_id':src[':db/id'],'profile':t,'matched_distractors':4,'total_distractors':4,'matched_bank':5,'total_bank':5,'missing_options':[],'extra_options':[],'correct_designation':True,'exact_prompt':True,'exact_solution':True})
        variants=[]
        for k in g.DOMAINS[t]:
            row=g.generate('easy',37,t,{'k':k});independent(row);records.append(row);variants.append(row)
        assert len({row['generation']['parameter_fingerprint'] for row in variants})==len(g.DOMAINS[t])
        a=g.generate('easy',1,t,{'k':original});b=g.generate('easy',2,t,{'k':original});assert a['question']==b['question'],'Seed must not create a new task'
        coverage[t]={'slot':'k','observed_value':original,'certified_domain':g.DOMAINS[t],'values_checked':[r['generation']['parameters']['k'] for r in variants],'uncovered_values':[],'fixed_exponents_operators_field_count_solution_stage_count':True}
        changed=next(row for row in variants if row['generation']['parameters']['k']!=original)
        assert changed['question'][':question/worked-solution'].count(r'\\')==src[':question/worked-solution'].count(r'\\')
        stale=copy.deepcopy(changed['question']);stale[':question/worked-solution']=src[':question/worked-solution']
        try:solution_check(stale)
        except AssertionError:pass
        else:raise AssertionError('Stale slot reference escaped solution validation')
        review.append('## '+t+' original\n\n'+g.markdown(r)+'\n\nChanged coefficient/argument\n\n'+g.markdown(changed))
        print('Validated template',t,flush=True)
    assert len({r['generation']['parameter_fingerprint'] for r in records})==42
    for band in ('moderate','hard'):
        try:g.generate(band)
        except ValueError:pass
        else:raise AssertionError('Unsupported level accepted')
    build_engine();save('engine-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records])
    subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    save('source-bank-replay.json',replays);save('slot-coverage.json',coverage);save('validated-previews.json',records);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    tracked=[HERE.with_suffix('.py'),HERE/'source.json',HERE/'math_reader.py',HERE/'validate.py',HERE/'check-engine']
    save('validation.json',{'status':'pass','basis':json.loads((HERE/'source.json').read_text())['basis'],'correctness':{'all_bounded_tasks':42,'all_solution_rows_checked':True,'stale_slot_negative_controls':7},'fidelity':{'complete_banks_matched':7,'complete_banks_total':7,'distractors_matched':28,'distractors_total':28,'exact_prompt_solution_replays':7},'grading':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':0},'hashes':{str(p.relative_to(ROOT)):sha(p) for p in tracked}})
if __name__=='__main__':main()
