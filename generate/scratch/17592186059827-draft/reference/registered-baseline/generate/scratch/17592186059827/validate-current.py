"""Current source fidelity, exact displayed-set correctness and native grading."""
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('legacy_validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
g=v.g

def save(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def clean(text):
    text=re.sub(r'\\in(?![A-Za-z])','∈',text).replace(r'\,','').replace(r'\leq',r'\le').replace(r'\lt','<')
    return text.strip().removesuffix('.')
def parse(text,variable='x'):
    text=clean(text)
    if text.startswith(('(','[')):text=variable+' ∈ '+text
    if r'\infty' in text:
        var,rest=text.split('∈');rest=rest.strip();a,_=rest[1:-1].split(',')
        return sp.Interval(v.endpoint(a),sp.oo,left_open=rest[0]=='('), (v.endpoint(a),sp.oo,var.strip(),rest[0]=='[',False)
    return v.parse(text)
def fingerprint(q):
    match=re.search(r'\$(.*?)\$',q[':question/problem']);_,info=parse(match[1]);a,b,variable,lc,rc=info
    direction='interval_to_inequality' if '∈' in clean(match[1]) else 'inequality_to_interval'
    return g.digest({'a':str(a),'b':str(b),'left_closed':lc,'direction':direction})
def inspect(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    given=re.search(r'\$(.*?)\$',q[':question/problem']).group(1);target,info=parse(given);a,b,var,lc,rc=info
    assert a<b and lc!=rc and len(f[':answer-field/choices'])==5
    values=[parse(x[':answer/value'])[0] for x in f[':answer-field/choices']]
    assert len(set(values))==5 and values.count(target)==1
    correct=[x for x in f[':answer-field/choices'] if x[':answer/id']==f[':answer-field/correct'][1]]
    assert len(correct)==1 and parse(correct[0][':answer/value'])[0]==target
    assert q[':question/difficulty']==':question.difficulty/'+r['generation']['difficulty']
    assert fingerprint(q)==r['generation']['mathematical_fingerprint']
    sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
    assert len(blocks)==2 and all(parse(x,var)[0]==target for x in blocks)
    for side,index,closed in [('left',0,lc),('right',1,rc)]:
        m=re.search('The '+side+r' endpoint \$(.*?)\$ (.*?) included in the interval. Therefore, we use \$(.*?)\$',sol)
        assert m and v.endpoint(m[1])==info[index]
        assert ('is not' in m[2].replace('*',''))==(not closed)
        expected=(('[' if closed else '(') if side=='left' else (']' if closed else ')')) if '∈' not in clean(given) else (r'\le' if closed else '<')
        assert clean(m[3]).strip()==expected,(m[3],expected)
    for text in [q[':question/problem'],sol]+[x[':answer/value'] for x in f[':answer-field/choices']]:v.format_check(text)
    return True

def normalize(q):
    def enum(x):return str(x[':db/ident']) if isinstance(x,dict) else x
    result={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
    result[':question/difficulty']=enum(q[':question/difficulty']);result[':question/answer-fields']=[]
    for f in sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']):
        ref=f[':answer-field/correct'];correct=str(ref[':answer/id']) if isinstance(ref,dict) else ref[1]
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':enum(f[':answer-field/type']),':answer-field/correct':[':answer/id',correct],':answer-field/choices':sorted([{':answer/id':str(x[':answer/id']),':answer/type':enum(x[':answer/type']),':answer/value':x[':answer/value']} for x in f[':answer-field/choices']],key=lambda x:x[':answer/value'])})
    return result

def native(records,path):
    fixtures=[{'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] else 'rejected'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]} for r in records]
    save(path/'native-input.json',fixtures)
    subprocess.run(['generate/runs/current/check-engine',str(path/'native-input.json'),str(path/'native-report.json')],check=True)

def main():
    source=json.loads((HERE/'current-source.json').read_text());cases=json.loads((HERE/'source-cases.json').read_text())+[{'source_id':'q-28834','level':'easy','template':'inequality_to_interval','bank_profile':'observed_28834','parameters':{'a':'-5','b':'-2','variable':'x','left_closed':True}},{'source_id':'q-73902','level':'moderate','template':'interval_to_inequality','bank_profile':'observed_73902','parameters':{'a':'-1','b':'2','variable':'y','left_closed':True}}]
    sources={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
    assert set(sources)=={c['source_id'] for c in cases},'New source requires reclassification'
    normals=[];replays=[];fidelity=[]
    for c in cases:
        q=sources[c['source_id']];r=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);rq=r['question'];f=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
        assert rq[':question/problem']==q[':question/problem']
        assert sorted(x[':answer/value'] for x in rf[':answer-field/choices'])==sorted(x[':answer/value'] for x in f[':answer-field/choices'])
        for attr in (':question/worked-solution',':question/difficulty'):
            old=q.get(attr);old=old.get(':db/ident') if isinstance(old,dict) else old
            assert rq.get(attr)==old
        if ':answer-field/correct' in f:
            assert next(x[':answer/value'] for x in rf[':answer-field/choices'] if x[':answer/id']==rf[':answer-field/correct'][1])==f[':answer-field/correct'][':answer/value']
            inspect(r);normals.append(r)
        else:v.inspect(r)
        replays.append(r);fidelity.append({'source_id':c['source_id'],'profile':c['bank_profile'],'prompt_match':True,'complete_bank_match':True,'choices_matched':5,'difficulty_presence_match':True,'solution_presence_and_text_match':True,'correct_presence_and_value_match':True})
    checks=0
    for level in g.LEVELS:
        for template in g.TEMPLATES:
            for seed in range(60):inspect(g.generate(level,seed,template=template));checks+=1
    for prof,level,template,pairs in [('observed_28834','easy','inequality_to_interval',[('-15','-14'),('-7','0'),('0','15'),('14','15')]),('observed_73902','moderate','interval_to_inequality',[('-15','14'),('-1','15'),('-14','1'),('-3','2')])]:
        for a,b in pairs:
            r=g.generate(level,31,template=template,profile=prof,parameters={'a':a,'b':b,'variable':'t','left_closed':True});inspect(r);normals.append(r);checks+=1
    try:g.generate('moderate',template='interval_to_inequality',profile='observed_73902',parameters={'a':'-2','b':'2','variable':'x','left_closed':True})
    except ValueError:pass
    else:raise AssertionError('Symmetric negated bank duplicates must be rejected')
    for level in g.LEVELS:
        for template in g.TEMPLATES:normals.append(g.generate(level,17,template=template))
    # Independent checker must reject an incorrect key and a displayed endpoint error.
    for kind in ('key','solution'):
        broken=copy.deepcopy(normals[0]);q=broken['question'];f=q[':question/answer-fields'][0]
        if kind=='key':f[':answer-field/correct'][1]=next(x[':answer/id'] for x in f[':answer-field/choices'] if x[':answer/id']!=f[':answer-field/correct'][1])
        else:q[':question/worked-solution']=q[':question/worked-solution'].replace('endpoint $-5$','endpoint $-4$')
        try:inspect(broken)
        except AssertionError:pass
        else:raise AssertionError('Failed mutation check '+kind)
    native(normals,HERE)
    save(HERE/'current-review.json',{'source_replays':replays,'generated':normals})
    (HERE/'current-review.md').write_text('\n\n---\n\n'.join('Source replay / generated '+r['generation']['profile']+' / '+r['generation']['difficulty']+'\n\n'+g.markdown(r) for r in replays+normals))
    names=['../17592186059827.py','validate.py','validate-current.py','source.json','current-source.json','classification.md','template-extraction.md','README.md','current-review.json','current-review.md','native-input.json','native-report.json','capabilities.json']
    save(HERE/'current-validation.json',{'passed':True,'runtime':{'python':__import__('sys').version,'sympy':sp.__version__,'native_grader_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest()},'basis':source['basis'],'lineage':source['lineage'],'fidelity':fidelity,'exact_banks':4,'exact_choices':20,'exact_observed_solutions':2,'preserved_missing_solutions_keys_ratings':2,'displayed_math_checks':checks,'mutations_rejected':['wrong key','wrong solution endpoint'],'native':json.loads((HERE/'native-report.json').read_text()),'hashes':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in names}})
    print('PASS current source: 4/4 prompts and banks; 20/20 choices; 2/2 supplied keys and full solutions; '+str(checks)+' displayed-set checks.')
if __name__=='__main__':main()
