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

from scripts.database.edn import dumps, loads, kw
from scripts.database.images import ImageLibrary, MissingImage
from scripts.database.evidence import authoritative_question, UnsupportedContent, image_answer
from scripts.database.prepare import Preparation, Plan, Snapshot, source_uuid, ALLOWED
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

class PrepareTests(unittest.TestCase):
    def test_repeated_scalar_updates_have_one_final_guard(self):
        snapshot=source_snapshot(); old=snapshot['entities'][1]
        plan=Plan(Snapshot(snapshot)); target=plan.entity('knowledge-point',old[':knowledge-point/id'],old)
        plan.set(target,old,'knowledge-point/title','First captured title')
        plan.set(target,old,'knowledge-point/title','Last captured title')
        batch=plan.finish()
        self.assertEqual([r[2] for r in batch['assertions'] if r[1]==':knowledge-point/title'],['Last captured title'])
        self.assertNotIn('First captured title',dumps(batch['forms']))

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
        result=Preparation(source_snapshot()).prepare({'questions':[q],'judgments':[{'question_id':'q-11','status':'unavailable','reasoning':'No source fields'}]})
        self.assertFalse(result['batches'])
        self.assertTrue(result['omissions'][0]['final'])

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
        result=Preparation(source_snapshot()).prepare(content)
        self.assertIn('selected first-two question is unsupported',result['calibration']['not_transacted'])

class FakeClient:
    """Minimal source-aware fact store; applies real prepared forms and readbacks."""
    def __init__(self):
        self.t=1; self.next_id=1000; self.receipts={}; self.calls=[]; self.timeout_once=False
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
    def snapshot(self,content,directory,basis):
        def pull(eid, depth=0):
            result={':db/id':eid}
            if eid in self.idents.values():result[':db/ident']=kw(next(k for k,v in self.idents.items() if v==eid))
            for (e,a),values in self.facts.items():
                if e!=eid:continue
                vals=[pull(v,depth+1) if self.attrs[a]['type']==':db.type/ref' and depth<5 else v for v,s in values]
                result[':'+a]=vals if self.attrs[a]['many'] else vals[-1]
            return result
        return {'basis':basis,'entities':[pull(eid) for eid in sorted({e for e,a in self.facts})],
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

class PipelineTests(unittest.TestCase):
    def setup(self, directory):
        root=Path(directory); capture=root/'capture';capture.mkdir()
        cfg=SimpleNamespace(database='test',endpoint='test',math_root=root/'math',postgres_url='',source=':org/Math-Academy',derived_source=None,state_root=root/'state')
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
    def test_changed_answer_replaces_fields_preserving_old_values(self):
        with tempfile.TemporaryDirectory() as d:
            capture,cfg=self.setup(d);client=FakeClient();pipeline=DatabasePipeline(cfg,threading.Event(),client=client)
            self.assertEqual(pipeline.process(capture)['status'],'verified')
            before={e:values for (e,a),values in client.facts.items() if a=='answer/value'}
            content=json.loads((capture/'content.json').read_text())
            field=content['questions'][0]['answer_fields'][0]
            field.update(correct_value='3',choices=[{'type':'math','value':'3'}],evidence={'kind':'ma_answer','value':'3','source_file':'history.html'})
            atomic_json(capture/'content.json',content)
            result=pipeline.process(capture);self.assertEqual(result['status'],'verified',result)
            self.assertTrue(all(client.facts[(e,'answer/value')]==values for e,values in before.items()))
            self.assertEqual(pipeline.process(capture)['status'],'no_changes')

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
                    content.update(multistep_id=20,question_order=['q-11'],shared_contexts=[{'problem':'Shared setup'}])
                    content['questions'][0]['local_problem']=content['questions'][0]['problem']
                atomic_json(capture/'content.json',content)
                result=pipeline.process(capture);self.assertEqual(result['status'],'verified',result)
                self.assertFalse(result.get('omissions'))
                self.assertEqual(pipeline.process(capture)['status'],'no_changes')

    def test_unknown_outcome_replays_exact_key(self):
        with tempfile.TemporaryDirectory() as d:
            capture,cfg=self.setup(d);client=FakeClient();client.timeout_once=True
            pipeline=DatabasePipeline(cfg,threading.Event(),client=client)
            first=pipeline.process(capture);self.assertEqual(first['status'],'pending')
            self.assertTrue(first['unknown_or_unverified_commit'])
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
