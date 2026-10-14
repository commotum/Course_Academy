"""Scoped additive replenishment with retained requests and exact-basis readback."""
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace, ModuleType
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
# Load the frozen independent verifier without running its artifact-writing driver.
v = ModuleType('substitution_validation')
v.__file__ = str(HERE / 'validate.py')
exec(compile((HERE / 'validate.py').read_text().split('\ncases=')[0], v.__file__, 'exec'), v.__dict__)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '29c362b92af75203c17cfeef7f6ebbba98537eb2f24b8e9c7196d2289d39cbe9'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = Path(json.loads((OUT / 'runtime.json').read_text())['native'])
GRADER = HERE / 'check-current-engine'
LEVELS = ('easy', 'moderate', 'hard')
QUERY = (HERE / 'reference/source-query.edn').read_text()
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(g.KP_UUID), 'course-academy-generator'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read_kp(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]

def normalize(q):
    result = {k: str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f: f[':answer-field/key']):
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a:a[':answer/value'])})
    return result

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

def fingerprint(q):
    prompt=q[':question/problem']
    mid=q.get(':question/math-academy-id')
    if mid in g.SOURCE_PARAMETERS:
        p=g.SOURCE_PARAMETERS[mid]
        t='difference' if mid=='q-18483' else 'canonical_second'
        return g.canonical_task(p,t)
    if mid == 'q-112214':
        return task_fingerprint([21,-9,0,-15,5,-10], 'reverse_difference')
    if mid == 'q-181207':
        return task_fingerprint([3,-6,-18,4,3,-2], 'ordered_values')
    # Generated prompts: read actual displayed equations, ignoring names/scales/order.
    hit=re.search(r'\$\\\{([^$]+)\$',prompt)
    assert hit, 'Unknown prompt requires source classification'
    names=[pair for pair in [('x','y'),('u','v'),('p','q'),('a','b')] if all(re.search(r'(?<![A-Za-z])'+z+r'(?![A-Za-z])',hit[1]) for z in pair)]
    assert len(names)==1
    x,y=names[0]; rows=[v.residual(z,x,y) for z in hit[1].split(';')]
    assert len(rows)==2
    coeffs=[n for row in rows for n in [row.coeff(v.X),row.coeff(v.Y),-row.subs({v.X:0,v.Y:0})]]
    assert all(n.is_Integer for n in coeffs)
    response='difference' if 'what is the value' in prompt else 'ordered_values'
    return task_fingerprint(coeffs,response)

def task_fingerprint(coeffs,response):
    p=dict(zip('ABCDEF',map(int,coeffs)));p.update(x='x',y='y')
    if response in ('difference','ordered_values'):
        return g.canonical_task(p,'difference' if response=='difference' else 'canonical_second')
    rows=[]
    for keys in ('ABC','DEF'):
        vals=[v.s.Rational(p[k]) for k in keys];pivot=next(z for z in vals if z)
        rows.append([str(z/pivot) for z in vals])
    return g.digest({'rows':sorted(rows),'response':response})

def engine_checks(rec,label):
    checks=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        correct=f[':answer-field/correct'][1]
        if f[':answer-field/type']==':answer-field.type/blank':
            a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==correct)
            n=v.s.Rational(a[':answer/value'])
            for submitted,expected in [(a[':answer/value'],'accepted'),(str(2*n)+'/2','accepted'),(str(n+1),'rejected'),(str(-n),'rejected')]:
                checks.append({'field_index':i,'submitted':submitted,'expected':expected,'purpose':'Canonical/equivalent and incorrect entries through actual blank grader'})
        else:
            checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'All complete owned choices through actual radio grader'} for a in f[':answer-field/choices'])
    return {'label':label,'record':rec,'checks':checks}

def verify_current_source(q):
    mid=q[':question/math-academy-id'];x,y=('x','y') if mid=='q-112214' else ('p','q')
    coeffs=[21,-9,0,-15,5,-10] if mid=='q-112214' else [3,-6,-18,4,3,-2]
    A,B,C,D,E,F=map(v.s.Integer,coeffs)
    prompt_block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/problem'],re.S)
    assert len(prompt_block)==1
    got=[v.residual(z,x,y) for z in prompt_block[0].split('\\\\')]
    assert got==[A*v.X+B*v.Y-C,D*v.X+E*v.Y-F]
    roots=v.s.solve(got,(v.X,v.Y));X,Y=roots[v.X],roots[v.Y]
    expected=(3,7) if mid=='q-112214' else (-2,2);assert (X,Y)==expected
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
    assert len(blocks)==4
    if mid=='q-112214':
        refs=[[21*v.X-9*v.Y,-15*v.X+5*v.Y+10],[-15*v.X+5*v.Y+10,-15*v.X+5*v.Y+10,v.Y-3*v.X+2],
              [21*v.X-9*v.Y,-6*v.X+18,-6*v.X+18,-6*v.X+18,18-6*v.X,3-v.X],
              [v.Y-3*v.X+2,v.Y-7,v.Y-7]]
    else:
        refs=[[3*v.X-6*v.Y+18,4*v.X+3*v.Y+2],[3*v.X-6*v.Y+18,3*v.X-6*v.Y+18,v.X-2*v.Y+6],
              [11*v.Y-22,11*v.Y-22,11*v.Y-22,v.Y-2],
              [3*v.X+6,3*v.X+6,3*v.X+6,v.X+2]]
    for bi,(bl,expect) in enumerate(zip(blocks,refs)):
        rows=[z.strip() for z in bl.split('\\\\')];assert len(rows)==len(expect)
        for row,want in zip(rows,expect):
            if bi==0:row=row.split('&')[0]
            assert v.s.expand(v.residual(row,x,y)-want)==0,(mid,row,want)
    flds=q[':question/answer-fields']
    if mid=='q-112214':
        assert len(flds)==1 and len(flds[0][':answer-field/choices'])==5
        vals={v.s.Rational(a[':answer/value']) for a in flds[0][':answer-field/choices']}
        assert vals=={X+Y,Y-X,X-Y,0,-X-Y}
        assert v.s.Rational(flds[0][':answer-field/correct'][':answer/value'])==Y-X==4
        assert 'y-x=7-3=4.' in q[':question/worked-solution']
    else:
        assert len(flds)==2
        for f,key,val in zip(sorted(flds,key=lambda f:f[':answer-field/key']),('field-1','field-2'),(X,Y)):
            assert f[':answer-field/key']==key and f[':answer-field/type'][':db/ident']==':answer-field.type/blank'
            assert len(f[':answer-field/choices'])==1 and v.s.Rational(f[':answer-field/correct'][':answer/value'])==val
            assert '{{'+key+'}}' in q[':question/problem']
        assert '(-2,2)' in q[':question/worked-solution']
    return {'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':normalize(q),'generation':{'template':mid,'source_evidence':True}}

def verify_current_canonical(q,captured,path):
    # Current capture renders the numbered system as a MathJax SVG and uses
    # eqalign/inline math. Verify its actual glyphs and rows before normalization.
    for k,val in captured.items():
        if k not in (':question/problem',':question/worked-solution'):
            assert canonical(q[k])==canonical(val)
    rec=g.generate('hard',21,'canonical_second',parameters=g.SOURCE_PARAMETERS['e-13010'])
    v.verify(rec)
    prompt_block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/problem'],re.S)
    assert len(prompt_block)==1
    got=[v.residual(row,'u','v') for row in prompt_block[0].split('\\\\')]
    assert got==[2*v.X+9*v.Y-6,2*v.X+6*v.Y-8]
    text=q[':question/worked-solution'];assets=re.findall(r'!\[\]\((images/[^)]+)\)',text)
    assert len(assets)==1
    asset=Path('/media/jake/SSD/EDB/math')/assets[0];digest=sha(asset)
    assert asset.stem==digest
    svg=ET.fromstring(asset.read_text());glyphs=''.join(chr(int(el.attrib['{http://www.w3.org/1999/xlink}href'].split('-')[-1],16)) for el in svg.iter('{http://www.w3.org/2000/svg}use'))
    assert glyphs=='{2u+9v−6=0(1)2u+6v−8=0(2)'
    current_blocks=re.findall(r'\\eqalign\{\s*(.*?)\n\}',text,re.S)
    generated_blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',rec['question'][':question/worked-solution'],re.S)
    assert len(current_blocks)==len(generated_blocks)==3
    row_total=0
    for current,generated in zip(current_blocks,generated_blocks):
        rows=re.split(r'\\\s*\n',current.strip());expected=generated.split('\\\\');assert len(rows)==len(expected)
        for row,want in zip(rows,expected):assert v.s.expand(v.residual(row,'u','v')-v.residual(want,'u','v'))==0
        row_total+=len(rows)
    original_numbered=re.findall(r'\$\$(.*?)\$\$',rec['question'][':question/worked-solution'],re.S)[0]
    normalized_text=re.sub(r'!\[\]\(images/[^)]+\)',lambda m:'$$'+original_numbered+'$$',text)
    normalized_text=re.sub(r'\\eqalign\{\s*(.*?)\n\}',lambda m:'\\begin{aligned}'+'\\\\'.join(re.split(r'\\\s*\n',m[1].strip()))+'\\end{aligned}',normalized_text,flags=re.S)
    normalized_text=normalized_text.replace('\\mathbin{:}',':')
    assert v.normalized(normalized_text.replace('$','')).rstrip('.')==v.normalized(rec['question'][':question/worked-solution'].replace('$','')).rstrip('.')
    result={'passed':True,'canonical_id':'e-13010','current_math_equations_unchanged':True,'all_worked_rows_matched':row_total,'prose_and_notation_matched_after_documented_markup_normalization':True,'source_asset':assets[0],'source_asset_sha256':digest,'source_svg_glyphs':glyphs,'asset_role':'standalone rendered equations; not a plot','mutations':0}
    save(path/'current-canonical-validation.json',result)

def transaction(records, kp, gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'], kw('answer/id'):uuid.UUID(a[':answer/id']), kw('answer/type'):kw(a[':answer/type']), kw('answer/value'):a[':answer/value'], kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'], kw('answer-field/id'):uuid.UUID(f[':answer-field/id']), kw('answer-field/key'):f[':answer-field/key'], kw('answer-field/type'):kw(f[':answer-field/type']), kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'):f[':answer-field/correct'][1], kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'], kw('question/id'):uuid.UUID(q[':question/id']), kw('question/problem'):q[':question/problem'], kw('question/worked-solution'):q[':question/worked-solution'], kw('question/difficulty'):kw(q[':question/difficulty']), kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'):kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator', kw('question-generator/id'):uuid.UUID(gid), kw('question-generator/script'):SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'):KP, kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms

def check_report(report, path, source):
    attrs = {e:str(a) for e,a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected attribution or retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name

USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def candidate_records(needed,added):
    # A bounded search per level; stop generating as soon as its shortage is met.
    for level in LEVELS:
        if not needed[level]:continue
        for seed in range(10000,10500):
            if added[level]>=needed[level]:break
            yield g.generate(level,seed)

def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    rows={level:[] for level in LEVELS};checks=[];source_validations=[]
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):continue
        if not q.get(':question/difficulty') or not q.get(':question/worked-solution') or not q.get(':question/answer-fields'):continue
        if not all(f.get(':answer-field/correct') for f in q[':question/answer-fields']):continue
        mid=q.get(':question/math-academy-id')
        if mid in ('q-112214','q-181207'):
            rec=verify_current_source(q);source_validations.append({'id':mid,'printed_equations_worked_stages_and_complete_answers':'passed'})
        else:
            # Only exact deterministic generator instances may be counted as authored.
            saved=list(OUT.glob('basis-*/generated.json'))
            recognized={r['question'][':question/id']:r for p in saved for r in json.loads(p.read_text())}
            assert str(q[':question/id']) in recognized,'Unknown authored content requires classification'
            rec=recognized[str(q[':question/id'])];assert normalize(q)==ordered(rec['question']);v.verify(rec)
        level=str(q[':question/difficulty'][':db/ident']).split('/')[-1];assert level in LEVELS
        checks.append(engine_checks(rec,str(q[':question/id'])));rows[level].append(q)
    if checks:
        save(path/'available-native-input.json',checks)
        subprocess.run([str(GRADER),str(path/'available-native-input.json'),str(path/'available-native-report.json')],check=True)
    result={'basis':basis,'levels':{level:{'distinct_available_tasks':len({fingerprint(q) for q in qs}), 'available_question_ids':[str(q[':question/id']) for q in qs]} for level,qs in rows.items()},'excluded_shown_or_reserved':sorted(unavailable),'incomplete_or_unrated_sources_excluded':True,'current_source_validation':source_validations}
    save(path/'available-counts.json',result);return result

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old)+len(records)
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q;assert normalize(q)==ordered(rec['question']);v.verify(rec)
    assert not transaction([],kp,intent['generator_id'])
    c=counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text());caps=json.loads((HERE/'capabilities.json').read_text())
    after=verified.get('available_counts_after',prep['available_counts']);remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'available_counts_before':prep['available_counts'],'available_counts_after':after,'shortage_remaining':remaining,'unsupported_levels_filled':False,'unsupported_nominal_shortage':{},'capability_exceptions':caps['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'capabilities.json'] if p.exists()],'note':'Supported bands replenished with distinct validated substitution systems. Generator levels and default banks are authored as documented. New current source templates are classified and validated separately, not silently treated as existing generator templates. Unrated incomplete originals are preserved and can leave an unclassified job visible. No source or learner facts modified.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def source_forward(value):
    if isinstance(value,dict):
        if ':db/ident' in value:return str(value[':db/ident'])
        return {str(k):source_forward(x) for k,x in value.items() if '/_' not in str(k)}
    if isinstance(value,(list,tuple)):
        return sorted((source_forward(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['pass'] is True and json.loads((HERE/'artifact-hashes.json').read_text())['files'][SCRIPT]==sha(HERE.with_suffix('.py'))
    for filename,digest in json.loads((HERE/'artifact-hashes.json').read_text())['files'].items():
        assert sha(ROOT/filename)==digest,'Frozen validated artifact changed: '+filename
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        save(path/'source-current.json',canonical(kp))
        captured=json.loads((HERE/'source.json').read_text())['record'];current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for q in captured[':knowledge-point/questions']:assert source_forward(current[q[':question/math-academy-id']])==source_forward(q),'Source changed; reclassify'
        verify_current_canonical(kp[':knowledge-point/canonical-example'],captured[':knowledge-point/canonical-example'],path)
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else GENERATOR_UUID
        if gen is not None:assert gen[':question-generator/script']==SCRIPT
        identities=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
        assert len(identities)<=1
        if identities:assert identities[0][0][':question-generator/script']==SCRIPT
        c=counts(kp,path,basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']));records=[];added={l:0 for l in LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
        for rec in instances:
            v.verify(rec);assert rec['knowledge_point']['db_id']==KP and not rec['generation']['evidence_only']
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        for rec in __import__('itertools').chain(instances,candidate_records(needed,added)):
            level=rec['question'][':question/difficulty'].split('/')[-1]
            if added[level]>=needed[level]:continue
            fp=fingerprint(rec['question'])
            if added[level]<needed[level] and fp not in used:
                v.verify(rec);assert not rec['generation']['evidence_only'];records.append(rec);used.add(fp);added[level]+=1
                if all(added[l]>=needed[l] for l in LEVELS):break
        # Batch lookup stable question/field/answer identities before creating entities.
        ids=[uuid.UUID(qid) for rec in records for qid in [rec['question'][':question/id'],rec['question'][':question/answer-fields'][0][':answer-field/id']]+[a[':answer/id'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]]
        existing=DB.query('[:find ?q ?id :in $ [?id ...] :where (or-join [?q ?id] [?q :question/id ?id] [?q :answer-field/id ?id] [?q :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not existing,'Existing identities require reconciliation'
        save(path/'generated.json',records)
        save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':engine_checks(r,r['question'][':question/id'])['checks']} for r in records]);subprocess.run([str(GRADER),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}),'asset_hashes':[],'dependencies':{'sympy':v.s.__version__,'python':sys.version},'source_evidence_unchanged':True,'source_basis':1356,'current_source_classification_basis':basis,'generator_default_scope':'validated radio templates; newly observed source layouts retained and checked separately'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'challenging-substitution-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
