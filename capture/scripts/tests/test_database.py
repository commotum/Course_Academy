import base64
import copy
import hashlib
import json
import tempfile
import threading
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace

from scripts.database.client import EDBClient
from scripts.database.edn import dumps, loads, kw
from scripts.database.images import ImageLibrary, MissingImage
from scripts.database.evidence import authoritative_question, UnsupportedContent, image_answer
from scripts.database.prepare import Preparation, Plan, Snapshot, source_uuid, ALLOWED, choice_signature
from scripts.database.difficulty import calibrate
from scripts.database.commit import Committer, validate_report, VerificationError
from scripts.database.pipeline import DatabasePipeline
from scripts.storage import atomic_json


def question(mid='q-11', answer='2'):
    return {'math_academy_id': mid, 'topic_id': 1, 'knowledge_point_id': 'kp', 'knowledge_point': 'Addition',
            'problem': 'What is $1+1$?', 'worked_solution': '$1+1=2$', 'difficulty': 'E',
            'answer_fields': [{'key':'x','type':'blank','choices':[{'type':'math','value':answer}],
                'correct_value':answer,'evidence':{'kind':'ma_correct_grade','value':answer,'source_file':'history.html'}}]}


def source_snapshot():
    tid, kid, qid = (source_uuid(k, 1) for k in ('topic','kp','question'))
    topic = {':db/id': 1, ':topic/id':tid, ':topic/math-academy-id':1, ':topic/title':'Addition'}
    kp = {':db/id':2, ':knowledge-point/id':kid, ':knowledge-point/title':'Addition',
          ':knowledge-point/canonical-example':{':db/id':3, ':question/id':qid, ':question/math-academy-id':'e-10'}}
    example = {':db/id':3, ':question/id':qid, ':question/math-academy-id':'e-10', ':question/problem':'Example', ':question/worked-solution':'$1+1=2$'}
    topic[':topic/knowledge-points'] = [kp]
    return {'basis':1,'entities':[topic,kp,example], 'idents':[[900,kw('org/Math-Academy')]],'attributes':[]}

class EvidenceTests(unittest.TestCase):
    def test_optional_screenshot_failure_preserves_complete_source(self):
        q=question(); q['errors']=['Screenshot unavailable: browser renderer closed']
        self.assertEqual(authoritative_question(q)['math_academy_id'],'q-11')
        q['errors'].append('Image unavailable: /graphics/q-11')
        with self.assertRaises(UnsupportedContent): authoritative_question(q)

    def test_guess_is_not_an_answer(self):
        q = question(); q['answer_fields'][0].pop('evidence')
        with self.assertRaises(UnsupportedContent): authoritative_question(q)

    def test_worked_solution_quote(self):
        q = question(); q['answer_fields'][0]['evidence'] = {'kind':'worked_solution','value':'2',
            'solution_quote':'1+1=2','source_file':'history.html','matches_worked_solution':True}
        self.assertEqual(authoritative_question(q)['answer_fields'][0]['correct_value'],'2')
        q['answer_fields'][0]['evidence']['solution_quote'] = 'x=2'
        with self.assertRaises(UnsupportedContent): authoritative_question(q)

    def test_exact_source_choice_quote_preserves_original_tex(self):
        source=r'{\begin{aligned}x=-2 \\ z=-4y+8\end{aligned}'
        agent_value=source+'}'
        q=question();q['worked_solution']='The tangent is $'+source+'$.'
        q['answer_fields']=[{'key':'selection','type':'radio','choices':[{'type':'math','value':source},{'type':'math','value':'wrong'}],
            'correct_value':agent_value,'evidence':{'kind':'worked_solution','value':agent_value,
            'source_file':'solution.html','solution_quote':source,'matches_worked_solution':True}}]
        accepted=authoritative_question(q)
        field=accepted['answer_fields'][0]
        self.assertEqual(field['correct_value'],source)
        self.assertEqual(field['evidence']['value'],source)
        self.assertEqual(field['evidence']['agent_value'],agent_value)
        self.assertEqual(q['answer_fields'][0]['correct_value'],agent_value)
        self.assertEqual(authoritative_question(accepted)['answer_fields'][0]['correct_value'],source)
        q['answer_fields'][0]['evidence']['solution_quote']='The tangent is $'+source+'$.'
        with self.assertRaises(UnsupportedContent):authoritative_question(q)

    def test_solution_spacing_binds_unique_original_math_choice(self):
        from scripts.activity.evidence import finalize_answers
        q = question()
        choice = r'\int_0^2 f(x)\text{'+ '\u00a0' + r'}dx'
        value = r'\int_0^2 f(x)\,dx'
        quote = 'The integral is $' + value + '$.'
        q['worked_solution'] = quote
        q['source_file'] = 'source.html'
        q['answer_fields'] = [{'key': 'selection', 'type': 'radio', 'correct_type': 'math',
            'choices': [{'option': 'a', 'type': 'math', 'value': choice},
                        {'option': 'b', 'type': 'math', 'value': r'\int_2^0 f(x)dx'}]}]
        judgment = {'status': 'confirmed', 'answers': [{'key': 'selection', 'correct_value': choice,
            'correct_option': 'a', 'value_type': 'math', 'ma_basis': 'worked_solution',
            'ma_value': value, 'ma_evidence': quote, 'disagrees': False}]}
        accepted = authoritative_question(finalize_answers(q, [], judgment))
        self.assertEqual(accepted['answer_fields'][0]['correct_value'], choice)
        self.assertTrue(accepted['answer_fields'][0]['evidence']['source_choice_spacing'])
        self.assertEqual(authoritative_question(accepted), accepted)
        q['answer_fields'][0]['choices'][1]['value'] = r'\int_0^2 f(x)\quad dx'
        with self.assertRaises(UnsupportedContent):
            authoritative_question(finalize_answers(q, [], judgment))

    def test_plain_agent_evidence_is_not_a_structured_source_record(self):
        q=question();q['answer_fields'][0]['evidence']='The answer is 2.'
        with self.assertRaises(UnsupportedContent):authoritative_question(q)

    def test_radio_filename_mixed_choices(self):
        field = {'type':'radio','choices':[{'type':'image','value':f'assets/246-a-{i}.png'} for i in (3,1,2)] + [{'type':'text','value':'DNE'}]}
        self.assertEqual(image_answer(field),'assets/246-a-1.png')
        field['type']='blank'; self.assertIsNone(image_answer(field))
        field['type']='radio'; field['choices'][1]['value']='assets/999-a-1.png'; self.assertIsNone(image_answer(field))

class ImageTests(unittest.TestCase):
    def test_exact_hash_and_reuse(self):
        data = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><path d="M0 0"/></svg>'
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root/'capture').mkdir(); (root/'capture'/'x.svg').write_bytes(data)
            lib = ImageLibrary(root/'math',root/'capture')
            relative = lib.resolve('x.svg'); sha=hashlib.sha256(data).hexdigest()
            self.assertEqual(relative,f'images/{sha[:2]}/{sha}.svg')
            self.assertEqual((root/'math'/relative).read_bytes(),data)
            self.assertEqual(lib.resolve('x.svg'),relative)
            self.assertEqual(lib.text('![x](x.svg)'),f'![x]({relative})')
            with self.assertRaises(MissingImage): lib.resolve('https://example.test/x.svg')

    def test_svg_requires_original_local_dependencies(self):
        with tempfile.TemporaryDirectory() as d:
            library=ImageLibrary(Path(d)/'math',Path(d))
            for body in ('<use href="https://example.test/shape.svg#graph"/>','<use href="#missing"/>',
                         '<style>path {fill:url(https://example.test/fill.svg)}</style>',
                         '<style>@import \"https://example.test/theme.css\";</style>'):
                with self.subTest(body=body), self.assertRaises(MissingImage):
                    library.store(('<svg xmlns="http://www.w3.org/2000/svg">'+body+'</svg>').encode(),'diagram')
            data=b'<svg xmlns="http://www.w3.org/2000/svg"><defs><path id="graph" d="M0 0"/></defs><use href="#graph"/></svg>'
            relative=library.store(data,'diagram')
            self.assertEqual((Path(d)/'math'/relative).read_bytes(),data)

    def test_manifest_hash_guards_original_source_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);capture=root/'capture';(capture/'assets').mkdir(parents=True)
            data=b'<svg xmlns="http://www.w3.org/2000/svg"/>'
            (capture/'assets/x.svg').write_bytes(data)
            atomic_json(capture/'assets/manifest.json',{'https://example.test/x.svg':{'path':'assets/x.svg','sha256':'0'*64}})
            with self.assertRaises(MissingImage):
                ImageLibrary(root/'math',capture).resolve('https://example.test/x.svg')
            atomic_json(capture/'assets/manifest.json',{'https://example.test/x.svg':{'path':'assets/x.svg','sha256':hashlib.sha256(data).hexdigest()}})
            self.assertTrue(ImageLibrary(root/'math',capture).resolve('https://example.test/x.svg').startswith('images/'))

class PrepareTests(unittest.TestCase):
    def test_new_kp_can_use_its_separate_reference_lesson_definition(self):
        example, practice = question('e-20'), question('q-21')
        for q in (example, practice):
            q['knowledge_point_id'] = '20'
            q['knowledge_point'] = 'A new source skill'
        content = {'questions':[practice], 'canonical_examples':[example],
                   'source_lesson_definitions':{'1':{'topic_id':1,'complete':True}}}
        result = Preparation(source_snapshot()).prepare(content)
        self.assertEqual(result['omissions'], [])
        self.assertEqual(len(result['content']['canonical_examples']), 1)
        self.assertIn(':knowledge-point/questions', dumps(result['batches'][0]['forms']))
        self.assertNotIn(':activity.type/lesson', dumps(result['batches'][0]['forms']))
        for definition in [{'topic_id':2,'complete':True}, {'topic_id':1,'complete':False}]:
            with self.subTest(definition=definition):
                content['source_lesson_definitions']['1'] = definition
                refused = Preparation(source_snapshot()).prepare(content)
                self.assertTrue(any('complete example and practice pool' in o['reason'] for o in refused['omissions']))
        content['source_lesson_definitions']['1'] = {'topic_id':1,'complete':True}
        content['questions'] = []
        refused = Preparation(source_snapshot()).prepare(content)
        self.assertTrue(any('complete example and practice pool' in o['reason'] for o in refused['omissions']))

    def test_multistep_context_images_are_localized_and_markdown(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); capture=root/'capture'; capture.mkdir()
            data=b'<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0"/></svg>'
            (capture/'context.svg').write_bytes(data)
            library=ImageLibrary(root/'math',capture)
            q=question(); q['knowledge_point_id']=str(source_snapshot()['entities'][1][':knowledge-point/id'])
            content={'questions':[q], 'task_type':'multistep', 'multistep_id':20,
                     'question_order':['q-11'], 'shared_contexts':[{'problem':'<p>Use this diagram:</p><img src="context.svg">'}]}
            prepared=Preparation(source_snapshot()).prepare(content,library)
            relative='images/'+hashlib.sha256(data).hexdigest()[:2]+'/'+hashlib.sha256(data).hexdigest()+'.svg'
            contexts=[row[2] for batch in prepared['batches'] for row in batch['assertions'] if row[1]==':multistep/context']
            self.assertEqual(contexts,['Use this diagram:\n\n![]('+relative+')'])
            self.assertEqual(prepared['content']['shared_context'],contexts[0])
            self.assertEqual((root/'math'/relative).read_bytes(),data)

    def test_missing_multistep_image_omits_structure(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); q=question(); q['knowledge_point_id']=str(source_snapshot()['entities'][1][':knowledge-point/id'])
            prepared=Preparation(source_snapshot()).prepare({'questions':[q], 'task_type':'multistep',
                'multistep_id':20, 'shared_context':'![diagram](https://example.test/missing.svg)'},ImageLibrary(root/'math',root))
            self.assertTrue(any(row['kind']=='multistep' and row['final'] for row in prepared['omissions']))
            self.assertNotIn(':multistep/context',dumps(prepared['batches']))
            self.assertIn(':question/problem',dumps(prepared['batches']))

    def test_identity_payload_uses_content_and_preserves_existing_uuid(self):
        snap=source_snapshot(); point=snap['entities'][1]
        point[':knowledge-point/questions']=[{':db/id':100+i,':question/math-academy-id':'q-'+str(i)} for i in range(200)]
        captured=question();captured['html']='redundant page markup '*100
        calls=[]
        def resolve(task,payload):
            calls.append((task,payload))
            return {'decision':'existing','entity_id':str(point[':knowledge-point/id']),'evidence':'Same canonical example'}
        prep=Preparation(snap,resolve=resolve)
        chosen=prep.choose('knowledge-point revision',captured,[point])
        self.assertEqual(chosen[':knowledge-point/id'],point[':knowledge-point/id'])
        payload=calls[0][1]
        self.assertNotIn('html',payload['captured'])
        self.assertEqual(payload['captured']['fields'][0]['evidence'],captured['answer_fields'][0]['evidence'])
        self.assertNotIn(':knowledge-point/questions',payload['candidates'][0])
        self.assertEqual(payload['candidates'][0]['practice_question_count'],200)
        self.assertEqual(payload['candidates'][0][':knowledge-point/canonical-example'][':question/worked-solution'],'$1+1=2$')

    def test_repeated_scalar_updates_have_one_final_guard(self):
        snapshot=source_snapshot(); old=snapshot['entities'][1]
        plan=Plan(Snapshot(snapshot)); target=plan.entity('knowledge-point',old[':knowledge-point/id'],old)
        plan.set(target,old,'knowledge-point/title','First captured title')
        plan.set(target,old,'knowledge-point/title','Last captured title')
        batch=plan.finish()
        self.assertEqual([r[2] for r in batch['assertions'] if r[1]==':knowledge-point/title'],['Last captured title'])
        self.assertNotIn('First captured title',dumps(batch['forms']))

    def test_final_scalar_equal_to_snapshot_cancels_earlier_change(self):
        snapshot = source_snapshot(); old = snapshot['entities'][1]
        plan = Plan(Snapshot(snapshot)); target = plan.entity('knowledge-point', old[':knowledge-point/id'], old)
        plan.set(target, old, 'knowledge-point/title', 'Other observed title')
        plan.set(target, old, 'knowledge-point/title', old[':knowledge-point/title'])
        batch = plan.finish()
        self.assertEqual(batch['forms'], [])
        self.assertEqual(batch['assertions'], [])
        self.assertEqual(batch['retractions'], [])

    def test_history_without_kp_ids_resolves_each_observed_title(self):
        snapshot = source_snapshot()
        second = copy.deepcopy(snapshot['entities'][1])
        second.update({':db/id': 4, ':knowledge-point/id': source_uuid('kp', 2),
                       ':knowledge-point/title': 'Subtraction',
                       ':knowledge-point/canonical-example': {':db/id': 5,
                           ':question/math-academy-id': 'e-20'}})
        snapshot['entities'].append(second)
        snapshot['entities'][0][':topic/knowledge-points'].append(second)
        first, other = question('q-11'), question('q-12')
        for q in (first, other):
            q.pop('knowledge_point_id')
        other['knowledge_point'] = 'Subtraction'
        result = Preparation(snapshot).prepare({'questions': [first, other]})
        self.assertEqual([q['knowledge_point_id'] for q in result['content']['questions']],
                         [str(snapshot['entities'][1][':knowledge-point/id']), str(second[':knowledge-point/id'])])
        self.assertFalse(any(row[1] == ':knowledge-point/title'
                             for batch in result['batches'] for row in batch['assertions']))

    def test_missing_kp_id_preserves_existing_owner_despite_captured_example(self):
        snapshot = source_snapshot()
        second = copy.deepcopy(snapshot['entities'][1])
        second.update({':db/id': 4, ':knowledge-point/id': source_uuid('kp', 2),
                       ':knowledge-point/title': 'Subtraction',
                       ':knowledge-point/canonical-example': {':db/id': 5,
                           ':question/math-academy-id': 'e-20'}})
        snapshot['entities'].append(second)
        snapshot['entities'][0][':topic/knowledge-points'].append(second)
        snapshot['entities'].append({':db/id': 6, ':question/id': source_uuid('question', 12),
            ':question/math-academy-id': 'q-12',
            ':knowledge-point/_questions': [snapshot['entities'][1]]})
        snapshot['entities'].append({':db/id': 5, ':question/id': source_uuid('question', 20),
                                    ':question/math-academy-id': 'e-20'})
        example, practice = question('e-20'), question('q-12')
        example['knowledge_point_id'] = 'source-20'
        for q in (example, practice):
            q['knowledge_point'] = 'Subtraction'
        practice.pop('knowledge_point_id')
        result = Preparation(snapshot).prepare({'canonical_examples': [example], 'questions': [practice]})
        self.assertEqual(result['content']['questions'][0]['knowledge_point_id'],
                         str(snapshot['entities'][1][':knowledge-point/id']))
        self.assertFalse(any(row[0] == 2 and row[1] == ':knowledge-point/title'
                             for batch in result['batches'] for row in batch['assertions']))
        self.assertFalse(any(row[1] == ':knowledge-point/questions' and row[2] == 6
                             for batch in result['batches'] for row in batch['assertions']))
        self.assertFalse(any(row[1] == ':knowledge-point/questions'
                             for batch in result['batches'] for row in batch['retractions']))

    def test_full_answer_fields_and_kp_membership(self):
        snap=source_snapshot(); q=question(); q['knowledge_point_id']=str(snap['entities'][1][':knowledge-point/id'])
        result=Preparation(snap).prepare({'questions':[q],'task_type':'lesson'})
        forms=result['batches'][0]['forms']; text=dumps(forms)
        self.assertIn(':knowledge-point/questions',text)
        self.assertIn(':answer-field/correct',text)
        self.assertIn(':answer/value "2"',text)
        self.assertNotIn(':learner/',text)

    def test_missing_fields_final_omission(self):
        q=question(); q['answer_fields']=[]
        result=Preparation(source_snapshot(),resolve=lambda task,payload: {'status':'unavailable','reasoning':'No source fields','answers':[]}).prepare({'questions':[q]})
        self.assertFalse(result['batches'])
        self.assertTrue(result['omissions'][0]['final'])

    def test_saved_plain_judgment_cannot_overwrite_structured_source_evidence(self):
        q=question();q['answer_fields'][0]['choices']=[{'type':'math','value':'3'}]
        prepared=Preparation(source_snapshot(),resolve=lambda task,payload: {
            'status':'confirmed','reasoning':'My reasoning says 3','answers':[{'key':'x','ma_value':'3','ma_evidence':'My reasoning says 3'}]}).prepare({'questions':[q]})
        self.assertFalse(prepared['batches'])
        self.assertTrue(prepared['omissions'][0]['final'])
        self.assertIn('typed source choice',prepared['omissions'][0]['reason'])

    def test_unknown_question_judgment_required(self):
        q=question(); q['answer_fields']=[]
        with self.assertRaises(ValueError): Preparation(source_snapshot()).prepare({'questions':[q]})

    def test_calibration_first_two_and_formula(self):
        qs=[question('q-'+str(i)) for i in (1,2,3)]
        qs[-1]['worked_solution']='$'+('x+'*500)+'x$'
        ex={'math_academy_id':'e-10','knowledge_point_id':'kp','problem':'Example $x$','worked_solution':'$x=2$'}
        content={'task_type':'lesson','questions':qs,'canonical_examples':[ex],'lesson_definition':{'complete':True},'base_xp':13,'tutorials':[]}
        result=calibrate(content)
        self.assertEqual(result['selected_questions'],{'kp':['q-1','q-2']})
        self.assertAlmostEqual(result['multiplier']*result['unscaled_score'],13)
        self.assertEqual(result['expected_seconds'],780.)

    def test_calibration_never_substitutes_a_later_question(self):
        qs=[question('q-'+str(i)) for i in (1,2,3)]
        qs[0]['answer_fields']=[]
        ex={'math_academy_id':'e-10','topic_id':1,'knowledge_point_id':'kp','knowledge_point':'Addition','problem':'Example','worked_solution':'$x=2$'}
        content={'task_type':'lesson','questions':qs,'canonical_examples':[ex],'lesson_definition':{'complete':True},'base_xp':13,
                 'judgments':[{'question_id':'q-1','status':'unavailable','reasoning':'Source missing'}],
                 'lesson_workload_sample':{'questions_by_knowledge_point':{'kp':['q-1','q-2']}}}
        result=Preparation(source_snapshot(),resolve=lambda task,payload: {'status':'unavailable','reasoning':'Source missing','answers':[]}).prepare(content)
        self.assertIn('selected first-two question is unsupported',result['calibration']['not_transacted'])

class FakeClient:
    """Minimal source-aware fact store; applies real prepared forms and readbacks."""
    def __init__(self):
        self.t=1; self.next_id=1000; self.receipts={}; self.calls=[]; self.timeout_once=False
        self.database='math'; self.lineage='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
        self.idents={':org/Math-Academy':900,':answer-field.type/blank':901,':answer.type/math':902,':question.difficulty/easy':903,
            ':activity.type/lesson':904, ':activity.type/assignment':905}
        many={'topic/knowledge-points','knowledge-point/questions','question/answer-fields','answer-field/choices','activity/steps','multistep/steps','assigned-problem/topic-coverage'}
        refs={'topic/knowledge-points','knowledge-point/questions','knowledge-point/canonical-example','question/answer-fields','question/difficulty','answer-field/choices','answer-field/correct','answer-field/type','answer/type','activity/type','activity/steps','activity/first-step','activity/scope','step/content','step/next','multistep/steps','multistep/first-step','assigned-problem/content','assigned-problem/topic-coverage'}
        self.attrs={a:{'id':i,'type':':db.type/ref' if a in refs else ':db.type/uuid' if a.endswith('/id') else ':db.type/string','many':a in many} for i,a in enumerate(sorted(ALLOWED|{'db/txInstant'}),100)}
        self.facts={}
        for e in source_snapshot()['entities']:
            for a,v in e.items():
                if a==':db/id':continue
                values=v if self.attrs[a[1:]]['many'] else [v]
                for val in values:
                    self.facts.setdefault((e[':db/id'],a[1:]),[]).append((val[':db/id'] if isinstance(val,dict) else val,900))
    def basis(self):return self.t
    def status(self):return {'database':self.database,'lineage':self.lineage,'basis':self.t}
    def snapshot(self,content,directory,basis):
        by_entity={}
        for (eid,attr),values in self.facts.items():
            by_entity.setdefault(eid,[]).append((attr,values))
        def pull(eid, depth=0):
            result={':db/id':eid}
            if eid in self.idents.values():result[':db/ident']=kw(next(k for k,v in self.idents.items() if v==eid))
            for a,values in by_entity.get(eid,[]):
                vals=[pull(v,depth+1) if self.attrs[a]['type']==':db.type/ref' and depth<5 else v for v,s in values]
                result[':'+a]=vals if self.attrs[a]['many'] else vals[-1]
            return result
        return {'basis':basis,'lineage':self.lineage,'entities':[pull(eid) for eid in sorted({e for e,a in self.facts})],
            'attributes':[[v['id'],kw(a),kw(v['type']),kw('db.cardinality/'+('many' if v['many'] else 'one'))] for a,v in self.attrs.items()],
            'idents':[[v,kw(k)] for k,v in self.idents.items()],
            'facts':[[e,self.attrs[a]['id'],v,s] for (e,a),values in self.facts.items() for v,s in values]}
    def command(self,cmd,*options):
        opts=dict(zip(options[::2],options[1::2])); forms=loads(Path(opts['--file']).read_text()); self.calls.append((cmd,opts.copy()))
        if cmd=='transact' and opts['--request-key'] in self.receipts:return self.receipts[opts['--request-key']]
        before=self.t; source=self.idents[opts['--source']]; facts=copy.deepcopy(self.facts); temp={}
        for form in forms:
            if isinstance(form,dict) and isinstance(form[':db/id'],str):
                token=form[':db/id']; ident=next(((a,v) for a,v in form.items() if str(a).endswith('/id') and a!=':db/id'),None)
                existing=next((e for (e,a),values in facts.items() if ident and a==str(ident[0])[1:] and any(v==ident[1] for v,s in values)),None)
                temp[token]=existing or self.next_id+len(temp)
        def ref(v):return temp.get(v,self.idents.get(v,v)) if isinstance(v,str) else v
        datoms=[]
        for form in forms:
            if isinstance(form,list):
                _,e,a,v=form;e=ref(e);a=str(a)[1:];v=ref(v)
                if any(x==v for x,s in facts.get((e,a),[])):
                    facts[(e,a)]=[(x,s) for x,s in facts[(e,a)] if x!=v];datoms.append([e,self.attrs[a]['id'],v,before+1,source,False])
                continue
            e=ref(form[':db/id'])
            for attr,value in form.items():
                if attr in (':db/id', ':db/ensure'):continue
                a=str(attr)[1:];vals=value if self.attrs[a]['many'] else [value]
                for v in vals:
                    if self.attrs[a]['type']==':db.type/ref':v=ref(v)
                    current=facts.setdefault((e,a),[])
                    if not self.attrs[a]['many']:
                        for x,s in list(current):
                            if x!=v:
                                datoms.append([e,self.attrs[a]['id'],x,before+1,source,False]);current.remove((x,s))
                    if (v,source) not in current:
                        current.append((v,source));datoms.append([e,self.attrs[a]['id'],v,before+1,source,True])
        report={kw('edb/db-before-t'):before,kw('edb/db-after-t'):before+1,kw('edb/tempids'):temp,kw('edb/tx-data'):datoms}
        if cmd=='transact':
            if int(opts['--basis'])!=self.t:
                from scripts.database.client import StaleBasis
                raise StaleBasis()
            self.facts=facts;self.t+=1;self.next_id+=len(temp);report[kw('edb/committed')]=True
            text=dumps(report);self.receipts[opts['--request-key']]=text
            if self.timeout_once:self.timeout_once=False;raise TimeoutError('lost committed response')
            return text
        return dumps(report)

class QueryBackedFakeClient(FakeClient):
    """Use production snapshot selection with realistic shallow activity pulls."""
    def __init__(self):
        super().__init__()
        self.queries=[]
        self.idents.update({':activity.type/diagnostic':906, ':activity.type/assessment':907, ':activity.type/review':908})
        self.attrs['activity/course']['type']=':db.type/ref'
        self.attrs.update({'course/id':{'id':800,'type':':db.type/uuid','many':False},
                           'course/math-academy-id':{'id':801,'type':':db.type/long','many':False}})
        self.facts[(50,'course/id')]=[(source_uuid('course',7),900)]
        self.facts[(50,'course/math-academy-id')]=[(7,900)]

    def snapshot(self,content,directory,basis):
        return EDBClient.snapshot(self,content,directory,basis)

    def query(self,source,inputs,directory,name,basis=None):
        self.queries.append((name,inputs,basis))
        snapshot=FakeClient.snapshot(self,{},directory,basis)
        entities=snapshot['entities']
        def rows(attr,wanted):
            return [[e] for e in entities if e.get(attr) in wanted]
        def shallow(value):
            if isinstance(value,dict):
                result={k:shallow(v) for k,v in value.items()}
                if ':question/id' in result:
                    result[':question/answer-fields']=[{':db/id':f[':db/id'] if isinstance(f,dict) else f}
                                                     for f in result.get(':question/answer-fields',[])]
                    if isinstance(result.get(':question/difficulty'),dict):
                        result[':question/difficulty']={':db/id':result[':question/difficulty'][':db/id']}
                return result
            return [shallow(v) for v in value] if isinstance(value,list) else value
        if name.startswith('topic-'):return rows(':topic/math-academy-id',inputs[0])
        if name.startswith('questions-'):return rows(':question/math-academy-id',inputs[0])
        if name.startswith('activities-'):
            tids={e[':db/id'] for e in entities if e.get(':topic/math-academy-id') in inputs[0]}
            return shallow([[e] for e in entities if ':activity/id' in e and e.get(':activity/scope',{}).get(':db/id') in tids])
        if name in ('activity-route','multistep-activity'):return shallow(rows(':activity/id',inputs))
        if name=='activity-definition':return shallow(rows(':activity/math-academy-id',inputs))
        if name=='course':return rows(':course/math-academy-id',inputs)
        if name=='tutorials':return rows(':tutorial/math-academy-id',inputs[0])
        if name=='attributes':return snapshot['attributes']
        if name=='idents':return snapshot['idents']
        if name.startswith('facts-'):return [row for row in snapshot['facts'] if row[0] in inputs[0]]
        raise AssertionError('Unexpected snapshot query: '+name)


class PipelineTests(unittest.TestCase):
    def test_legacy_multistep_context_is_not_queried_as_a_tutorial(self):
        client=QueryBackedFakeClient()
        content={'kind':'multistep','topic_id':1,'multistep_id':20,
                 'questions':[{'math_academy_id':'q-11','topic_id':1}],
                 'tutorials':[{'math_academy_id':'step-1','content':'Shared setup.'}]}
        with tempfile.TemporaryDirectory() as directory:
            client.snapshot(content,Path(directory),1)
        self.assertFalse(any(name=='tutorials' for name,_,_ in client.queries))
        self.assertEqual(content['tutorials'][0]['math_academy_id'],'step-1')

    def test_lesson_tutorial_catalog_identity_is_still_queried(self):
        client=QueryBackedFakeClient()
        content={'kind':'lesson','topic_id':1,'questions':[],
                 'tutorials':[{'math_academy_id':'20','content':'Introduction.'}]}
        with tempfile.TemporaryDirectory() as directory:
            client.snapshot(content,Path(directory),1)
        self.assertIn(('tutorials',[[20]],1),client.queries)

    def test_wide_snapshot_batches_topics_at_one_basis_and_keeps_multistep_lineage(self):
        client=QueryBackedFakeClient()
        for tid in range(2,58):
            eid=1000+tid
            client.facts[(eid,'topic/id')]=[(source_uuid('topic',tid),900)]
            client.facts[(eid,'topic/math-academy-id')]=[(tid,900)]
        content={'questions':[{'math_academy_id':'q-'+str(tid),'topic_id':tid}
                              for tid in range(1,58)],'multistep_id':20}
        with tempfile.TemporaryDirectory() as directory:
            snapshot=client.snapshot(content,Path(directory),1)
        self.assertEqual(snapshot['lineage'],client.lineage)
        self.assertEqual({e[':topic/math-academy-id'] for e in snapshot['entities']
                          if ':topic/math-academy-id' in e},set(range(1,58)))
        for prefix in ('topic-batch-','activities-batch-'):
            reads=[q for q in client.queries if q[0].startswith(prefix)]
            self.assertEqual(len(reads),3)
            self.assertEqual([tid for _,inputs,_ in reads for tid in inputs[0]],list(range(1,58)))
        self.assertTrue(all(basis==1 for _,_,basis in client.queries))

    def setup(self, directory):
        root=Path(directory); capture=root/'capture';capture.mkdir()
        cfg=SimpleNamespace(database='math',endpoint='test',math_root=root/'math',postgres_url='',source=':org/Math-Academy',derived_source=None,state_root=root/'state')
        q=question();q['knowledge_point_id']=str(source_snapshot()['entities'][1][':knowledge-point/id'])
        atomic_json(capture/'content.json',{'task_type':'lesson','topic_id':1,'questions':[q]})
        atomic_json(capture/'capture-complete.json',{'complete':True})
        return capture,cfg
    def test_commit_verify_and_noop(self):
        with tempfile.TemporaryDirectory() as d:
            capture,cfg=self.setup(d);client=FakeClient();pipeline=DatabasePipeline(cfg,threading.Event(),client=client)
            result=pipeline.process(capture)
            self.assertEqual(result['status'],'verified',result)
            self.assertEqual(client.t,2)
            self.assertEqual(pipeline.process(capture)['status'],'no_changes')
            self.assertEqual(client.t,2)
    def test_changed_answer_preserves_complete_question_without_a_transaction(self):
        with tempfile.TemporaryDirectory() as d:
            capture,cfg=self.setup(d);client=FakeClient();pipeline=DatabasePipeline(cfg,threading.Event(),client=client)
            self.assertEqual(pipeline.process(capture)['status'],'verified')
            before=copy.deepcopy(client.facts)
            basis=client.t
            content=json.loads((capture/'content.json').read_text())
            field=content['questions'][0]['answer_fields'][0]
            field.update(correct_value='3',choices=[{'type':'math','value':'3'}],evidence={'kind':'ma_answer','value':'3','source_file':'history.html'})
            atomic_json(capture/'content.json',content)
            result=pipeline.process(capture);self.assertEqual(result['status'],'no_changes',result)
            self.assertEqual(client.facts,before)
            self.assertEqual(client.t,basis)
            self.assertEqual(pipeline.process(capture)['status'],'no_changes')

    def test_correct_choice_change_preserves_complete_question_and_original_key(self):
        with tempfile.TemporaryDirectory() as d:
            capture,cfg=self.setup(d);client=FakeClient();pipeline=DatabasePipeline(cfg,threading.Event(),client=client)
            client.idents[':answer-field.type/radio']=909
            content=json.loads((capture/'content.json').read_text())
            field=content['questions'][0]['answer_fields'][0]
            field.update(type='radio',choices=[{'type':'math','value':v} for v in ('2','3')])
            atomic_json(capture/'content.json',content)
            self.assertEqual(pipeline.process(capture)['status'],'verified')
            before=copy.deepcopy(client.facts)
            field.update(correct_value='3',evidence={'kind':'ma_answer','value':'3','source_file':'history.html'})
            atomic_json(capture/'content.json',content)
            result=pipeline.process(capture);self.assertEqual(result['status'],'no_changes',result)
            self.assertEqual(client.facts,before)
            self.assertEqual(pipeline.process(capture)['status'],'no_changes')

    def test_radio_choice_removal_cannot_orphan_historical_response(self):
        snapshot=source_snapshot();old_choice={':db/id':20,':answer/id':source_uuid('answer',20),
            ':answer/type':{':db/ident':kw('answer.type/math')},':answer/value':'3',':task-item/_responses':[{':db/id':30}]}
        field={':db/id':10,':answer-field/id':source_uuid('field',10),':answer-field/key':'x',
            ':answer-field/type':{':db/ident':kw('answer-field.type/radio')},':answer-field/choices':[old_choice]}
        old={':db/id':5,':question/id':source_uuid('question',5),':question/answer-fields':[field]}
        q=question();q['answer_fields'][0].update(type='radio',correct_type='math',choices=[{'type':'math','value':v} for v in ('1','2')])
        prep=Preparation(snapshot);plan=Plan(prep.snapshot)
        before=copy.deepcopy(old)
        prep.question(plan,q,old,False)
        batch=plan.finish()
        self.assertFalse(batch['retractions'])
        self.assertFalse(any(row[1].startswith((':answer/',':answer-field/')) or row[1]==':question/answer-fields'
                             for row in batch['assertions']))
        self.assertEqual(old,before)
        self.assertNotIn(':answer-field/correct',field)

    def test_function_application_escape_revision_preserves_response_owned_answer(self):
        incoming = '6^x \\operatorname{ln}\u20616-10x+6'
        legacy = r'6^x ln\u20616-10x+6'
        choice={':db/id':20,':answer/id':source_uuid('answer',20),
            ':answer/type':{':db/ident':kw('answer.type/math')},':answer/value':legacy,
            ':task-item/_responses':[{':db/id':30}]}
        field={':db/id':10,':answer-field/id':source_uuid('field',10),':answer-field/key':'x',
            ':answer-field/type':{':db/ident':kw('answer-field.type/radio')},
            ':answer-field/choices':[choice],':answer-field/correct':choice}
        old={':db/id':5,':question/id':source_uuid('question',5),':question/answer-fields':[field]}
        q=question();q['answer_fields'][0].update(type='radio',correct_type='math',correct_value=incoming,
            choices=[{'type':'math','value':incoming}])
        prep=Preparation(source_snapshot());plan=Plan(prep.snapshot)
        before=copy.deepcopy(old)
        prep.question(plan,q,old,False)
        batch=plan.finish()
        self.assertFalse(batch['retractions'])
        self.assertFalse(any(row[1].startswith((':answer/',':answer-field/')) or row[1]==':question/answer-fields'
                             for row in batch['assertions']))
        self.assertEqual(old,before)
        self.assertEqual(choice[':answer/value'],legacy)

    def test_function_application_compatibility_requires_a_math_operator_marker(self):
        self.assertEqual(choice_signature('math',r'ln\u20616'),choice_signature('math','\\operatorname{ln}\u20616'))
        self.assertNotEqual(choice_signature('text',r'ln\u20616'),choice_signature('text','ln\u20616'))
        self.assertNotEqual(choice_signature('math',r'\operatorname{ln}6'),choice_signature('math','ln6'))
        self.assertNotEqual(choice_signature('math','ln\u20616'),choice_signature('math','ln\u20617'))

    def duplicate_typed_choices(self, field_type, *, owned=False, owned_first=False):
        first={':db/id':20,':answer/id':source_uuid('answer',20),
               ':answer/type':{':db/ident':kw('answer.type/math')},':answer/value':'2'}
        second={**copy.deepcopy(first),':db/id':21,':answer/id':source_uuid('answer',21)}
        if owned:
            (first if owned_first else second)[':task-item/_responses']=[{':db/id':30}]
        field={':db/id':10,':answer-field/id':source_uuid('field',10),':answer-field/key':'x',
               ':answer-field/type':{':db/ident':kw('answer-field.type/'+field_type)},
               ':answer-field/choices':[first,second],':answer-field/correct':first}
        old={':db/id':5,':question/id':source_uuid('question',5),':question/answer-fields':[field]}
        q=question();q['answer_fields'][0].update(type=field_type,correct_type='math',choices=[{'type':'math','value':'2'}])
        return q,old

    def test_response_owned_duplicate_typed_choices_are_retained_without_reconciliation(self):
        for field_type in ('radio','select'):
            for owned_first in (False,True):
                with self.subTest(field_type=field_type,owned_first=owned_first):
                    q,old=self.duplicate_typed_choices(field_type,owned=True,owned_first=owned_first)
                    prep=Preparation(source_snapshot());plan=Plan(prep.snapshot)
                    before=copy.deepcopy(old)
                    prep.question(plan,q,old,False)
                    batch=plan.finish()
                    self.assertFalse(batch['retractions'])
                    self.assertFalse(any(row[1].startswith((':answer/',':answer-field/')) or row[1]==':question/answer-fields'
                                         for row in batch['assertions']))
                    self.assertEqual(old,before)

    def test_unowned_duplicate_typed_choices_are_not_deduplicated_by_recapture(self):
        for field_type in ('radio','select'):
            with self.subTest(field_type=field_type):
                q,old=self.duplicate_typed_choices(field_type)
                prep=Preparation(source_snapshot());plan=Plan(prep.snapshot)
                before=copy.deepcopy(old)
                prep.question(plan,q,old,False);batch=plan.finish()
                self.assertFalse(batch['retractions'])
                self.assertFalse(any(row[1].startswith((':answer/',':answer-field/')) or row[1]==':question/answer-fields'
                                     for row in batch['assertions']))
                self.assertEqual(old,before)

    def test_blank_duplicate_typed_response_values_keep_all_ownership(self):
        q,old=self.duplicate_typed_choices('blank',owned=True)
        prep=Preparation(source_snapshot());plan=Plan(prep.snapshot)
        prep.question(plan,q,old,False);forms=plan.finish()['forms']
        self.assertFalse(any(isinstance(f,list) and str(f[2])==':answer-field/choices' for f in forms))

    def test_owned_duplicate_choice_is_preserved_while_supported_sibling_imports(self):
        class OwnedDuplicateClient(FakeClient):
            def snapshot(self,*args):
                result=super().snapshot(*args)
                def annotate(value):
                    if isinstance(value,dict):
                        if value.get(':db/id')==10000:value[':task-item/_responses']=[{':db/id':30}]
                        for child in list(value.values()):annotate(child)
                    elif isinstance(value,list):
                        for child in value:annotate(child)
                annotate(result['entities']);return result
        with tempfile.TemporaryDirectory() as d:
            capture,cfg=self.setup(d);client=OwnedDuplicateClient();client.idents[':answer-field.type/radio']=909
            pipeline=DatabasePipeline(cfg,threading.Event(),client=client)
            content=json.loads((capture/'content.json').read_text());q=content['questions'][0]
            q['answer_fields'][0].update(type='radio',choices=[{'type':'math','value':v} for v in ('2','3')])
            atomic_json(capture/'content.json',content);self.assertEqual(pipeline.process(capture)['status'],'verified')
            fid=next(e for (e,a),values in client.facts.items() if a=='answer-field/key' and values[0][0]=='x')
            client.facts[(10000,'answer/id')]=[(source_uuid('answer','owned-duplicate'),900)]
            client.facts[(10000,'answer/type')]=[(902,900)];client.facts[(10000,'answer/value')]=[('2',900)]
            client.facts[(fid,'answer-field/choices')].append((10000,900))
            before={key:copy.deepcopy(values) for key,values in client.facts.items()
                    if key[1].startswith(('question/','answer-field/','answer/'))}
            q['problem']='A revision with ambiguous duplicate response ownership.'
            sibling=question('q-12');sibling['knowledge_point_id']=q['knowledge_point_id'];content['questions'].append(sibling)
            atomic_json(capture/'content.json',content);result=pipeline.process(capture)
            self.assertEqual(result['status'],'verified',result)
            self.assertEqual(result['omissions'],[])
            self.assertTrue(all(client.facts[key]==values for key,values in before.items()))
            self.assertIn((10000,900),client.facts[(fid,'answer-field/choices')])
            self.assertFalse(any(value==q['problem'] for (e,a),values in client.facts.items() if a=='question/problem' for value,_ in values))
            self.assertTrue(any(value=='q-12' for (e,a),values in client.facts.items() if a=='question/math-academy-id' for value,_ in values))
            self.assertEqual(pipeline.process(capture)['status'],'no_changes')

    def test_referenced_field_deletion_and_type_change_are_blocked(self):
        answer={':answer/type':{':db/ident':kw('answer.type/math')},':answer/value':'2',':task-item/_responses':[{':db/id':30}]}
        old={':question/answer-fields':[{':answer-field/key':'x',':answer-field/type':{':db/ident':kw('answer-field.type/blank')},':answer-field/choices':[answer]}]}
        for incoming in ([],[{**question()['answer_fields'][0],'type':'radio'}]):
            q=question();q.update(answer_fields=incoming,answer_fields_complete=True)
            with self.subTest(incoming=incoming),self.assertRaisesRegex(UnsupportedContent,'historical response'):
                Preparation(source_snapshot()).check_response_ownership(q,old)

    def test_existing_response_choices_are_preserved_while_siblings_import(self):
        class ReferencedClient(FakeClient):
            def snapshot(self,*args):
                result=super().snapshot(*args)
                def mark(value):
                    if isinstance(value,dict):
                        if value.get(':answer/value')=='3':value[':task-item/_responses']=[{':db/id':30}]
                        for child in list(value.values()):mark(child)
                    elif isinstance(value,list):
                        for child in value:mark(child)
                mark(result['entities']);return result
        with tempfile.TemporaryDirectory() as d:
            capture,cfg=self.setup(d);client=ReferencedClient();client.idents[':answer-field.type/radio']=909
            pipeline=DatabasePipeline(cfg,threading.Event(),client=client)
            content=json.loads((capture/'content.json').read_text());q=content['questions'][0]
            q.update(answer_fields_complete=True)
            q['answer_fields'][0].update(type='radio',choices=[{'type':'math','value':v} for v in ('2','3')])
            atomic_json(capture/'content.json',content)
            self.assertEqual(pipeline.process(capture)['status'],'verified')
            before={key:copy.deepcopy(values) for key,values in client.facts.items()
                    if key[1].startswith(('question/','answer-field/','answer/'))}
            q['problem']='A revision that removes a used option.'
            q['answer_fields'][0]['choices']=[{'type':'math','value':v} for v in ('2','4')]
            sibling=question('q-12');sibling['knowledge_point_id']=q['knowledge_point_id'];content['questions'].append(sibling)
            atomic_json(capture/'content.json',content)
            result=pipeline.process(capture)
            self.assertEqual(result['status'],'verified',result)
            self.assertEqual(result['omissions'],[])
            self.assertTrue(all(client.facts[key]==values for key,values in before.items()))
            self.assertEqual(pipeline.process(capture)['status'],'no_changes')
            stored={value for (e,a),values in client.facts.items() if a=='question/math-academy-id' for value,_ in values}
            self.assertIn('q-12',stored)
            self.assertFalse(any(value==q['problem'] for (e,a),values in client.facts.items() if a=='question/problem' for value,_ in values))

    def test_lesson_and_multistep_are_idempotent(self):
        for kind in ('lesson','multistep'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as d:
                capture,cfg=self.setup(d);client=FakeClient();pipeline=DatabasePipeline(cfg,threading.Event(),client=client)
                content=json.loads((capture/'content.json').read_text())
                content.update(task_type=kind,title='Addition',base_xp=13)
                if kind=='lesson':
                    content.update(lesson_definition={'topic_id':1,'title':'Addition','complete':True,'steps':[
                        {'math_academy_id':50,'content_id':20,'type':'tutorial','title':'Intro'},
                        {'math_academy_id':51,'content_id':10,'type':'example','title':'Addition'}]},
                        tutorials=[{'math_academy_id':20,'title':'Intro','content':'Add the values.'}],
                        canonical_examples=[{'math_academy_id':'e-10','topic_id':1,'knowledge_point_id':content['questions'][0]['knowledge_point_id'],
                            'knowledge_point':'Addition','problem':'Example','worked_solution':'$1+1=2$','answer_fields':[]}])
                else:
                    content.update(multistep_id=20,question_order=['q-11'],shared_contexts=[{'problem':'Shared setup'}],
                                   tutorials=[{'math_academy_id':'step-1','content':'Shared setup'}])
                    content['questions'][0]['local_problem']=content['questions'][0]['problem']
                atomic_json(capture/'content.json',content)
                result=pipeline.process(capture);self.assertEqual(result['status'],'verified',result)
                self.assertFalse(result.get('omissions'))
                self.assertEqual(pipeline.process(capture)['status'],'no_changes')

    def test_course_routes_reimport_without_changes(self):
        for kind in ('diagnostic','assessment','review'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as d:
                capture,cfg=self.setup(d); client=QueryBackedFakeClient()
                content=json.loads((capture/'content.json').read_text())
                content.pop('topic_id')
                content.update(task_type=kind,course_id=7,question_order=['q-11'],question_outcomes={'q-11':'correct'})
                atomic_json(capture/'content.json',content)
                pipeline=DatabasePipeline(cfg,threading.Event(),client=client)
                result=pipeline.process(capture)
                self.assertEqual(result['status'],'verified',result)
                self.assertEqual(client.t,2)
                self.assertEqual(pipeline.process(capture)['status'],'no_changes')
                self.assertEqual(client.t,2)
                routes=[query for query in client.queries if query[0]=='activity-route']
                self.assertTrue(routes)
                self.assertTrue(all(query[2] in (1,2) for query in routes))
                snapshot=client.snapshot(content,Path(d),2)
                q=next(e for e in snapshot['entities'] if e.get(':question/math-academy-id')=='q-11')
                self.assertEqual(q[':question/answer-fields'][0][':answer-field/correct'][':answer/type'][':db/ident'],':answer.type/math')

    def test_post_activity_base_xp_restores_calibration_without_changing_sample(self):
        with tempfile.TemporaryDirectory() as d:
            capture,cfg=self.setup(d)
            questions=[];examples=[]
            selected={}
            for kp in ('first','second'):
                ids=['q-'+str(10+len(questions)+i) for i in range(3)]
                selected[kp]=ids[:2]
                for mid in ids:
                    q=question(mid);q['knowledge_point_id']=kp;questions.append(q)
                examples.append({'math_academy_id':'e-'+str(len(examples)+1),'knowledge_point_id':kp,
                                 'problem':'Example $1+1$','worked_solution':'$1+1=2$'})
            content={'task_id':'lesson-1','task_type':'lesson','questions':questions,'canonical_examples':examples,
                     'base_xp':None,'lesson_definition':{'complete':True},
                     'lesson_workload_sample':{'questions_by_knowledge_point':selected,'base_xp':None}}
            atomic_json(capture/'content.json',content)
            original=(capture/'content.json').read_bytes()
            atomic_json(capture/'post-activity.json',{'completion':{'task_id':'lesson-1','earned_xp':7,'base_xp':10,'source_text':'7 / 10 XP'}})
            received=[]
            class CalibrationPipeline(DatabasePipeline):
                def _prepare(_,prepared_content,directory,basis):
                    received.append(prepared_content)
                    return {'batches':[],'omissions':[],'calibration':calibrate(prepared_content)},{}
            pipeline=CalibrationPipeline(cfg,threading.Event(),client=FakeClient())
            result=pipeline.process(capture)
            self.assertEqual(result['status'],'no_changes',result)
            self.assertEqual(result['calibration']['base_xp'],10)
            self.assertEqual(result['calibration']['expected_seconds'],600)
            self.assertEqual(result['calibration']['selected_questions'],selected)
            self.assertEqual(received[0]['lesson_workload_sample'],content['lesson_workload_sample'])
            self.assertEqual(received[0]['base_xp_evidence']['source_file'],str((capture/'post-activity.json').resolve()))
            self.assertEqual((capture/'content.json').read_bytes(),original)
            self.assertIsNone(content['base_xp'])
            existing={**content,'base_xp':13}
            self.assertEqual(pipeline._with_post_activity_base(existing,capture)['base_xp'],13)
            atomic_json(capture/'post-activity.json',{'completion':{'task_id':'another-task','base_xp':20}})
            self.assertIsNone(pipeline._with_post_activity_base(content,capture)['base_xp'])

    def test_unknown_outcome_replays_exact_key(self):
        with tempfile.TemporaryDirectory() as d:
            capture,cfg=self.setup(d);client=FakeClient();client.timeout_once=True
            pipeline=DatabasePipeline(cfg,threading.Event(),client=client)
            first=pipeline.process(capture);self.assertEqual(first['status'],'pending')
            self.assertTrue(first['unknown_or_unverified_commit'])
            diagnostic=json.loads((capture/'database/pending.json').read_text())
            self.assertIn('TimeoutError: lost committed response',diagnostic['traceback'])
            self.assertNotIn('traceback',first)
            result=pipeline.process(capture);self.assertEqual(result['status'],'verified',result)
            calls=[c[1] for c in client.calls if c[0]=='transact']
            self.assertEqual(calls[0],calls[1]);self.assertEqual(client.t,2)
    def test_verified_commit_mismatch_reconciles_without_replay(self):
        class IncompleteReadOnce(FakeClient):
            damaged=False
            def snapshot(self,content,directory,basis):
                snapshot=super().snapshot(content,directory,basis)
                if basis==2 and not self.damaged:
                    self.damaged=True
                    for e in snapshot['entities']:
                        if e.get(':question/math-academy-id')=='q-11':e.pop(':question/problem',None)
                return snapshot
        with tempfile.TemporaryDirectory() as d:
            capture,cfg=self.setup(d);client=IncompleteReadOnce();pipeline=DatabasePipeline(cfg,threading.Event(),client=client)
            result=pipeline.process(capture);self.assertEqual(result['status'],'verified',result)
            self.assertEqual(len([c for c in client.calls if c[0]=='transact']),1)
            archived=[json.loads(p.read_text()) for p in (capture/'database/requests').glob('*/result.json')]
            self.assertEqual(archived[0]['status'],'confirmed_needs_reconciliation')

    def test_unbound_stale_receipt_cannot_satisfy_request(self):
        with tempfile.TemporaryDirectory() as d:
            capture,cfg=self.setup(d);client=FakeClient();client.timeout_once=True
            pipeline=DatabasePipeline(cfg,threading.Event(),client=client)
            self.assertEqual(pipeline.process(capture)['status'],'pending')
            atomic_json(capture/'database/receipt-request.json',{'request_key':'another-request',
                'transaction_sha256':'another-hash','receipt_edn':dumps({kw('edb/committed'):True})})
            result=pipeline.process(capture);self.assertEqual(result['status'],'verified',result)
            self.assertEqual(len([c for c in client.calls if c[0]=='transact']),2)

    def test_protected_datoms_rejected(self):
        snap=FakeClient().snapshot({},Path('/tmp'),1)
        report={':edb/tx-data':[[2,999999,'bad',2,900,True]]}
        with self.assertRaises(VerificationError):validate_report(report,{'source':':org/Math-Academy','assertions':[],'retractions':[]},snap)

if __name__=='__main__':unittest.main()
