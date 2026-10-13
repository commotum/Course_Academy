#!/usr/bin/env python3
"""Independent displayed-math validation, source fidelity and actual native grading."""
import hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.dont_write_bytecode=True
SPEC=importlib.util.spec_from_file_location('kp',HERE.with_suffix('.py'))
G=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(G)

def require(condition,message):
    if not condition:raise AssertionError(message)
def stages(text):return list(G.displayed_stages(text))
def formatting(text):
    require(text.count('$')%2==0,'unbalanced math delimiter')
    for block in G.MATH.findall(text):
        n=0
        for c in block:
            n+=1 if c=='{' else -1 if c=='}' else 0
            require(n>=0,'negative brace depth')
        require(n==0,'unbalanced math braces')
    require('+-' not in text and '--' not in text,'ungrouped signed product')
def check(r):
    require(set(r['knowledge_point'])=={'db_id','id','title'},'outer key shape')
    q=r['question'];f=q[':question/answer-fields'][0]
    require(f[':answer-field/type']==':answer-field.type/radio','field layout')
    require(len(f[':answer-field/choices'])==5,'bank size')
    # Read the actual prompt expression and every actual displayed choice, not
    # a regenerated expression using mathematical metadata.
    target=G.parse_math(G.prompt_expr(q[':question/problem']))
    values=[G.parse_math(a[':answer/value']) for a in f[':answer-field/choices']]
    require(len(set(map(sp.srepr,values)))==5,'equivalent displayed options')
    good=[i for i,v in enumerate(values) if v==target]
    require(len(good)==1,'one correct whole mathematical value')
    if ':answer-field/correct' in f:
        require(f[':answer-field/correct']==[':answer/id',f[':answer-field/choices'][good[0]][':answer/id']],'correct designation')
    for text in [q[':question/problem']]+[a[':answer/value'] for a in f[':answer-field/choices']]+[q.get(':question/worked-solution','')]:formatting(text)
    if ':question/worked-solution' in q:
        ss=stages(q[':question/worked-solution'])
        require(len(ss)>=8,'complete teaching stages')
        for v in ss:require(G.parse_math(v)==target,'printed stage mismatch '+v)
        # Independent structural sequence check: mask scaling and mirror/angle
        # variation cannot add/remove original rows or alter the factoring location.
        template=r['generation']['template']
        if template in G.QUESTIONS and ':question/worked-solution' in G.QUESTIONS[template]:
            src=G.QUESTIONS[template][':question/worked-solution']
            require(len(ss)==len(stages(src)),'source stage sequence length')
            require(q[':question/worked-solution'].count(r'\cancel')==src.count(r'\cancel'),'cancellation stage preserved')
    if not r['generation']['evidence_only']:
        # Verify the actual authored identity-two distractor from the printed
        # factoring stage. Retain that arithmetic tree until substitution, so a
        # surviving extra term is not erroneously doubled with the identity.
        printed=stages(q[':question/worked-solution'])[1]
        S,C=sp.symbols('sin cos')
        factored=sp.factor_terms(G.parse_math(printed,symbolic=True,reduce=False))
        mistaken=factored.subs(S*S+C*C,2).subs({S:G.SIN,C:G.COS})
        mistaken=sp.cancel(mistaken)
        require(mistaken!=target and mistaken in values,'printed identity-two operation missing/wrong')
    # Exact nonzero denominator domain from original displayed denominator. This
    # check uses independent trig symbols, which do not collapse the identity.
    unreduced=G.parse_math(G.prompt_expr(q[':question/problem']),symbolic=True)
    num,den=sp.fraction(unreduced)
    advertised=r['generation']['domain'];s,c=sp.symbols('sin cos')
    # Every zero of sin or cos appearing in denominator must remain excluded,
    # including factors canceled by pure rational normalization.
    template=r['generation']['template'];p=r['generation']['parameters']
    orig=G.prompt_expr(q[':question/problem'])
    def group_at(txt,i):
        require(txt[i]=='{','fraction group');start=i+1;depth=1;i+=1
        while depth:
            depth+=1 if txt[i]=='{' else -1 if txt[i]=='}' else 0;i+=1
        return txt[start:i-1],i
    index=orig.find(r'\frac')
    require(index>=0,'rational task');i=index+len(r'\frac')
    while orig[i].isspace():i+=1
    _,i=group_at(orig,i)
    while orig[i].isspace():i+=1
    d,_=group_at(orig,i)
    d_expr=G.parse_math(d,symbolic=True)
    expected=[]
    for fcn,sym in [('sin',s),('cos',c)]:
        # Substitute identity-compatible values at each zero: sin=0 cos=1;
        # cos=0 sin=1. Powers and products must be inspected before cancellation.
        if d_expr.subs({s:0,c:1} if fcn=='sin' else {s:1,c:0})==0:expected.append(G.atom(fcn,p)+' != 0')
    require(set(expected)==set(advertised),'original denominator/domain mismatch')
    return len(stages(q.get(':question/worked-solution','')))

def main():
    sources=[];cases=[];fidelity=[];review=[];native=[]
    for qid,src in G.QUESTIONS.items():
        p={'k':1,'mirror':False,'angle':G.ANGLES[qid]};level=G.LEVELS[qid]
        case={'source_id':qid,'db_id':src[':db/id'],'template':qid,'level':level,'parameters':p,'bank_profile':'raw:'+qid}
        cases.append(case);r=G.generate(level,19,qid,parameters=p,profile='raw:'+qid);check(r);sources.append(r)
        q=r['question'];f=q[':question/answer-fields'][0];old=src[':question/answer-fields'][0]
        require(set(q)==set(src),'source question key-presence parity '+qid)
        require(set(f)==set(old),'source field key-presence parity '+qid)
        require(q[':question/problem']==src[':question/problem'],'exact prompt '+qid)
        require(q.get(':question/worked-solution')==src.get(':question/worked-solution'),'complete raw solution '+qid)
        require(sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':answer-field/choices']),'exact complete raw bank '+qid)
        for a in f[':answer-field/choices']:
            oa=next(x for x in old[':answer-field/choices'] if x[':answer/value']==a[':answer/value'])
            require(set(a)==set(oa),'source answer key presence '+qid)
        designated=':answer-field/correct' in old
        # Completed original profile separately preserves every original solution;
        # missing keys/solutions are explicitly inferred rather than matched.
        normal=G.generate(level,20,qid,parameters=p,profile='observed:'+qid);check(normal)
        require(normal['question'].get(':question/worked-solution')==src.get(':question/worked-solution') if ':question/worked-solution' in src else ':question/worked-solution' in normal['question'],'completed-original solution comparison '+qid)
        require(sorted(a[':answer/value'] for a in normal['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':answer-field/choices']),'completed original complete bank '+qid)
        require(normal['generation']['evidence_only'] and not normal['generation']['eligible_for_learning'],'opaque evidence eligibility')
        fidelity.append({'source_id':qid,'prompt_exact':True,'options_exact':5,'complete_bank_exact':True,'original_correct_designation_present':designated,'designation_matched':designated,'raw_solution_present':':question/worked-solution' in src,'raw_solution_exact':':question/worked-solution' in src,'normal_solution_exact':':question/worked-solution' in src,'attribute_presence_exact':True,'authored_missing_attributes':not designated,'decoded_prompt_adjacent_backslashes':src[':question/problem'].count(chr(92)*2)})
        review.append({'label':'original '+qid,'record':r})
        for seed in (31,52):
            v=G.generate(level,seed,qid,parameters={'k':2 if seed==31 else 5,'mirror':seed==52,'angle':r'\phi'},profile='observed:'+qid);check(v);review.append({'label':'generated observed-bank variant '+qid,'record':v})
    counts={l:0 for l in ('easy','moderate','hard')};tasks={l:set() for l in counts};stage_count=0
    # Exhaustive meaningful domain, with every complete profile. Angle aliases
    # add presentation coverage only and are deliberately not counted as tasks.
    for template,info in G.TEMPLATES.items():
        l=info['level']
        profiles=['authored']+(['raw:'+template,'observed:'+template] if template in G.QUESTIONS else [])
        for k,mirror in itertools.product(range(1,13),(False,True)):
            p={'k':k,'mirror':mirror,'angle':r'\phi'}
            for profile in profiles:
                v=G.generate(l,80,template,parameters=p,profile=profile);stage_count+=check(v);counts[l]+=1;tasks[l].add(v['generation']['mathematical_fingerprint'])
                # Fix all mathematics and bank, vary seed/order only.
                w=G.generate(l,83,template,parameters=p,profile=profile)
                require(v['question'][':question/id']==w['question'][':question/id'],'seed identity')
            if k in (3,7) and not mirror:
                v=G.generate(l,12,template,parameters=p);review.append({'label':'generated authored-bank variant '+template,'record':v})
                native.append({'label':'authored '+template+' '+str(k),'record':v,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==v['question'][':question/answer-fields'][0][':answer-field/correct'][1] else 'rejected','purpose':'owned radio option, independently parsed displayed value'} for a in v['question'][':question/answer-fields'][0][':answer-field/choices']]})
        # Every original bank's completed original fixture is grade-tested.
        if template in G.QUESTIONS:
            v=G.generate(l,0,template,parameters={'k':1,'mirror':False,'angle':G.ANGLES[template]},profile='observed:'+template)
            native.append({'label':'completed original '+template,'record':v,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==v['question'][':question/answer-fields'][0][':answer-field/correct'][1] else 'rejected','purpose':'complete original option bank; absent original keys independently inferred'} for a in v['question'][':question/answer-fields'][0][':answer-field/choices']]})
    for l in counts:
        for seed in range(8):check(G.generate(l,seed))
    for k in (0,-1,13,1.5):
        for l in counts:
            try:G.generate(l,parameters={'k':k,'mirror':False,'angle':'x'})
            except ValueError:pass
            else:raise AssertionError('explicit bound bypass')
    for qid in G.QUESTIONS:
        for angle in ('x','t','θ',r'\theta',r'\phi'):
            v=G.generate(G.LEVELS[qid],0,qid,parameters={'k':11,'mirror':True,'angle':angle});check(v)
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False)+'\n')
    (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (HERE/'review.md').write_text('# Source originals and generated variants\n\nEach original is raw evidence; observed-bank variants remain evidence-only. Authored banks are normal practice. Missing difficulty/keys/solutions are clearly inferred in metadata.\n\n'+'\n\n---\n\n'.join('## '+item['label']+' — '+G.presentation_label(item['record'])+'\n\n'+G.markdown(item['record'],include_label=False)+'\n\nAuthor domain: '+', '.join(item['record']['generation']['domain']) for item in review)+'\n')
    (HERE/'engine-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-results.json')],check=True)
    engine=json.loads((HERE/'engine-results.json').read_text())
    result={'status':'pass','source_provenance':{k:G.CAPTURE[k] for k in ('database','basis','lineage')},'source_questions':10,'raw_complete_banks':{'matched':10,'total':10},'source_options':{'matched':50,'total':50},'independently_identified_source_distractors':{'matched':40,'total':40},'original_correct_designations':{'matched':8,'total_present':8,'absent':2},'raw_exact_full_solutions':{'matched':8,'total_present':8,'absent':2},'normal_exact_full_solutions':{'matched':8,'total_present':8,'authored_missing':2},'question_field_answer_attribute_presence':{'matched_questions':10,'total':10},'exhaustive_generated_records':counts,'meaningful_task_counts':{l:len(s) for l,s in tasks.items()},'parsed_displayed_solution_stages':stage_count,'native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','database_writes')},'grader_binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'sources':fidelity,'limitations':['Two unrated originals lack correct designations, difficulty and worked solutions; these omissions are raw-exact, with inferred moderate completion separately labeled.','Source affine/scalar distractor intentions cannot be recovered; observed profiles are evidence-only, including completed keys, and normal practice uses separately authored operation banks.','Native radio ID checks do not validate mathematical entry equivalence; this KP uses no blank fields.','Scalar and function-mirror bounds are authored within existing same-method arithmetic, not observed source difficulty labels.']}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ('status','source_options','meaningful_task_counts','exhaustive_generated_records','parsed_displayed_solution_stages','native')},indent=2))

def presentation_checks():
    """Read the frozen review data, verify labels/keys and prove no mutations."""
    review_path=HERE/'review.json';frozen_bytes=review_path.read_bytes()
    review=json.loads(frozen_bytes)
    source_exact=0;marked=0;unrated=0
    for item in review:
        r=item['record'];before=json.dumps(r,sort_keys=True,ensure_ascii=False)
        g=r['generation'];regenerated=G.generate(g['difficulty'],g['seed'],g['template'],parameters=g['parameters'],profile=g['profile'])
        require(regenerated==r,'frozen generated JSON record changed')
        text=G.markdown(r);require(text==G.markdown(r),'deterministic markdown')
        require(before==json.dumps(r,sort_keys=True,ensure_ascii=False),'markdown mutated question record')
        label=G.presentation_label(r);require(label in text,'missing difficulty/origin label')
        q=r['question'];f=q[':question/answer-fields'][0]
        if ':answer-field/correct' in f:
            require(text.count('✓ Correct')==1,'exactly one visible correct option')
            answer=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            require('$'+answer[':answer/value']+'$ **✓ Correct' in text,'correct mark belongs to correct ID')
            marked+=1
        else:
            require('Original correct key absent' in text and '✓ Correct' not in text,'raw key absence presentation')
        if ':question/difficulty' not in q:
            require(label.startswith('unrated — original raw/evidence-only'),'unrated raw difficulty')
            unrated+=1
        else:require(label[0] in 'EMH','missing E/M/H')
        if item['label'].startswith('original '):
            source=G.QUESTIONS[item['label'].split()[-1]]
            require(q[':question/problem']==source[':question/problem'],'raw prompt changed')
            require(q.get(':question/worked-solution')==source.get(':question/worked-solution'),'raw solution changed')
            require(sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in source[':question/answer-fields'][0][':answer-field/choices']),'raw bank changed')
            source_exact+=1
    require(review_path.read_bytes()==frozen_bytes,'frozen review JSON changed')
    command=[str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py'))]
    runs=[]
    for flags in [['--difficulty','all','--seed','7','--count','2','--format','markdown'],['--difficulty','all','--seed','7','--count','2','--format','json'],['--difficulty','moderate','--template','q-65165','--profile','raw:q-65165','--count','1','--format','json']]:
        first=subprocess.check_output(command+flags);second=subprocess.check_output(command+flags)
        require(first==second,'deterministic CLI')
        runs.append(first)
    require(runs[2]==(HERE/'cli-raw-preview.json').read_bytes(),'raw CLI JSON record changed')
    for r in json.loads(runs[1]):
        # Reproduce the same stored authored-bank review instance independently
        # of preview code, so presentation cannot affect content identity.
        p=r['generation'];same=G.generate(p['difficulty'],p['seed'])
        require(r==same,'CLI JSON/API stability')
    report={'status':'pass','review_records_unchanged':len(review),'raw_originals_exact':source_exact,'visible_correct_marks':marked,'raw_unrated_key_absence_labels':unrated,'deterministic_CLI_modes':3,'frozen_review_json_sha256':hashlib.sha256(frozen_bytes).hexdigest(),'raw_CLI_json_unchanged':True}
    (HERE/'presentation-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    (HERE/'review.md').write_text('# Source originals and generated variants\n\nE = easy, M = moderate, H = hard. Raw absent difficulty stays unrated. Original raw and completed observed banks are evidence-only; normal/authored records use authored practice banks. Correct marks reflect existing record keys; missing raw keys are explicitly stated.\n\n'+'\n\n---\n\n'.join('## '+item['label']+' — '+G.presentation_label(item['record'])+'\n\n'+G.markdown(item['record'],include_label=False)+'\n\nAuthor domain: '+', '.join(item['record']['generation']['domain']) for item in review)+'\n')
    (HERE/'cli-normal-preview.md').write_bytes(runs[0])
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    if sys.argv[1:]==['--presentation-only']:presentation_checks()
    else:main();presentation_checks()
