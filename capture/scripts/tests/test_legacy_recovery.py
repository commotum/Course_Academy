"""Historical judgments remain bound to their own exact authored choices."""
import unittest
from pathlib import Path

from scripts.database.evidence import UnsupportedContent, authoritative_question
from scripts.legacy_recovery import (REVIEW_VALIDATOR_VERSION, batches, checked_original_choices,
    checked_mixed_original_choices, checked_reconstructed_choices, current_supported_reviews,
    commit_aggregate_source_repairs, finalize_reviewed_answers, source_record)


class LegacyEvidenceTests(unittest.TestCase):
    def question(self):
        return {'math_academy_id':'q-1','problem':'Find the limit.',
            'worked_solution':'The limit is $\\infty$.','source_file':'source.json',
            'answer_fields':[{'key':'selection','type':'radio','choices':[
                {'option':'0','type':'math','value':'\\infty '},
                {'option':'1','type':'math','value':'-\\infty '}]}]}

    def judgment(self):
        return {'status':'confirmed','reasoning':'The exact first choice is equivalent.',
            'answers':[{'key':'selection','correct_value':'\\infty ','correct_option':'0',
                'value_type':'math','ma_value':'\\infty','ma_basis':'worked_solution',
                'ma_evidence':'The limit is $\\infty$.','disagrees':False}]}

    def test_equivalent_agent_choice_keeps_exact_authored_whitespace(self):
        judgment=self.judgment()
        checked=authoritative_question(finalize_reviewed_answers(self.question(),judgment))
        field=checked['answer_fields'][0]
        self.assertEqual(field['correct_value'],'\\infty ')
        self.assertEqual(field['evidence']['choice_binding']['agent_solution_value'],'\\infty')
        self.assertEqual(judgment['answers'][0]['ma_value'],'\\infty')

    def test_disagreement_does_not_replace_authored_answer_with_solver_answer(self):
        judgment=self.judgment();judgment['answers'][0]['disagrees']=True
        with self.assertRaises(UnsupportedContent):
            authoritative_question(finalize_reviewed_answers(self.question(),judgment))

    def test_binding_requires_exact_typed_current_choice(self):
        for key,value in [('value_type','text'),('correct_option','1')]:
            judgment=self.judgment();judgment['answers'][0][key]=value
            with self.subTest(key=key),self.assertRaises(UnsupportedContent):
                authoritative_question(finalize_reviewed_answers(self.question(),judgment))

    def test_other_questions_quote_does_not_support_this_question(self):
        judgment=self.judgment();judgment['answers'][0]['ma_evidence']='The answer is zero.'
        with self.assertRaises(UnsupportedContent):
            authoritative_question(finalize_reviewed_answers(self.question(),judgment))

    def test_literal_quote_wrappers_require_exact_owning_source_span(self):
        judgment=self.judgment();judgment['answers'][0]['ma_evidence']='"The limit is $\\infty$."'
        checked=authoritative_question(finalize_reviewed_answers(self.question(),judgment))
        self.assertEqual(checked['answer_fields'][0]['evidence']['solution_quote'],'The limit is $\\infty$.')
        self.assertEqual(judgment['answers'][0]['ma_evidence'],'"The limit is $\\infty$."')
        judgment['answers'][0]['ma_evidence']='“The limit is $\\infty$.”'
        checked=authoritative_question(finalize_reviewed_answers(self.question(),judgment))
        self.assertEqual(checked['answer_fields'][0]['evidence']['solution_quote'],'The limit is $\\infty$.')
        judgment['answers'][0]['ma_evidence']='"The limit is $0$."'
        with self.assertRaises(UnsupportedContent):
            authoritative_question(finalize_reviewed_answers(self.question(),judgment))

    def test_batch_caps_fields_and_graphics_independently(self):
        for count,images,expected in [(21,0,[1,1]),(1,16,[1,1]),(20,0,[2]),(1,15,[2])]:
            items=[]
            for index in range(2):
                q=self.question();q['assets']=[{'path':str(i)} for i in range(images)]
                q['answer_fields']=[{**q['answer_fields'][0],'key':str(i)} for i in range(count)]
                items.append({'question':q})
            with self.subTest(fields=count,images=images):
                self.assertEqual([len(group) for group in batches(items)],expected)

    def test_review_controls_use_original_values_without_learner_metadata(self):
        question=self.question();question['answer_fields'][0]['choices'][0]['value']='assistant rendering'
        content={'questions':[question]}
        before={'problem':question['problem'],'fields':[{'key':'selection','type':'radio',
            'submitted_value':'private learner attempt','observed_selected_option':'a','choices':[
                {'option':'a','type':'math','value':'\\infty ','html':'original browser markup'},
                {'option':'b','type':'math','value':'-\\infty '}]}]}
        state={'questions':{'q-1':{'before':before,'after':{'worked_solution':question['worked_solution']}}}}
        record=source_record(Path('/tmp'), 'q-1',content,state)
        field=record['answer_fields'][0]
        self.assertEqual(field['choices'][0]['value'],'\\infty ')
        self.assertEqual(field['choices'][0]['source_option'],'a')
        self.assertNotIn('submitted_value',field)
        self.assertNotIn('observed_selected_option',field)
        self.assertNotIn('html',field['choices'][0])

    def test_partial_flag_requires_every_own_original_math_control(self):
        raw={'key':'selection','type':'radio','choices':[]};rows=[]
        for label,value in [('a','1'),('b','2')]:
            markup='<math><mn>'+value+'</mn></math>'
            raw['choices'].append({'option':label,'type':'math','value':value,'html':markup})
            rows.append('<tr><td class="questionWidget-choiceLetterCircle" id="questionWidget-choiceLetterCircle-1-'+label+'"></td><td class="questionWidget-choiceText">'+markup+'</td></tr>')
        before={'dom_id':'step-q1','fields':[raw], 'errors':[],
            'html':'<div id="step-q1"><table class="questionWidget-choicesTable">'+''.join(rows)+'</table></div>'}
        evidence=checked_original_choices(before,raw,'q-1')
        self.assertEqual(evidence['source_options'],['a','b'])
        for kind in ('missing_row','other_question','changed_math','raw_incomplete'):
            from copy import deepcopy
            changed=deepcopy(before);field=changed['fields'][0]
            if kind=='missing_row':changed['html']=changed['html'].replace(rows[1],'')
            if kind=='other_question':changed['html']=changed['html'].replace('Circle-1-b','Circle-2-b')
            if kind=='changed_math':field['choices'][1]['html']='<math><mn>3</mn></math>'
            if kind=='raw_incomplete':field['choices_complete']=False
            with self.subTest(kind=kind):self.assertIsNone(checked_original_choices(changed,field,'q-1'))

    def test_mixed_controls_require_exact_own_text_and_math_markup(self):
        from copy import deepcopy
        math='<math><mo>{</mo><mn>1</mn><mo>}</mo></math>'
        choices=[{'option':'a','dom_id':'questionWidget-choiceLetterCircle-1-a','type':'text','value':'None of the listed','html':'None of the listed'},
            {'option':'b','dom_id':'questionWidget-choiceLetterCircle-1-b','type':'math','value':'{1}','html':math}]
        raw={'key':'selection','type':'radio','choices_complete':True,'choices':choices}
        rows=''.join('<tr><td class="questionWidget-choiceLetterCircle" id="'+c['dom_id']+'"></td><td class="questionWidget-choiceText">'+c['html']+'</td></tr>' for c in choices)
        before={'dom_id':'step-q1','fields':[raw],'errors':[], 'html':'<div id="step-q1"><table class="questionWidget-choicesTable">'+rows+'</table></div>'}
        observed=deepcopy([raw]);observed[0]['choices'][1]['value']='\\{1\\}'
        self.assertIsNotNone(checked_mixed_original_choices(before,raw,'q-1'))
        self.assertIsNotNone(checked_reconstructed_choices(before,observed,'q-1'))
        for changed in ('html','type','dom_id'):
            fields=deepcopy(observed);fields[0]['choices'][0][changed]='different'
            with self.subTest(changed=changed):self.assertIsNone(checked_reconstructed_choices(before,fields,'q-1'))

    def test_aggregate_drift_is_rejected_before_any_database_transport(self):
        import hashlib,json,tempfile
        from copy import deepcopy
        from unittest.mock import patch
        from scripts.storage import atomic_json
        checked=authoritative_question(finalize_reviewed_answers(self.question(),self.judgment()))
        payload={'questions':[checked],'canonical_examples':[],'content_only':True,'historical_source_repair':True}
        digest=lambda value:hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        reviewed={'q-1':{'question':checked,'source_hash':'reviewed-source'}}
        with tempfile.TemporaryDirectory() as temp:
            directory=Path(temp)/'package';directory.mkdir()
            evidence={'scope':'structural','bindings':[{'id':'q-1','source_hash':'reviewed-source'}],
                'content_sha256':digest(payload)}
            package={'directory':str(directory)}
            for update_proof in (False,True):
                changed=deepcopy(payload);changed['questions'][0]['problem']='Edited after source review'
                proof=deepcopy(evidence)
                if update_proof:proof['content_sha256']=digest(changed)
                atomic_json(directory/'content.json',changed);atomic_json(directory/'source-evidence.json',proof)
                with self.subTest(update_proof=update_proof),patch('scripts.legacy_recovery.current_supported_reviews',return_value=reviewed),patch('scripts.database.client.EDBClient') as client:
                    with self.assertRaises(AssertionError):commit_aggregate_source_repairs(Path(temp),package,None)
                    client.assert_not_called()

    def test_structured_source_requires_unchanged_original_markup_hash(self):
        import hashlib,json,tempfile
        question=self.question();content={'questions':[question]}
        before={'problem':question['problem'],'html':'<ol type="I"><li>First</li></ol>',
            'fields':question['answer_fields']}
        state={'questions':{'q-1':{'before':before,'after':{'worked_solution':question['worked_solution']}}}}
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);path=root/'repairs/source-provenance-v2/structured-source/q-1.json'
            path.parent.mkdir(parents=True)
            part={'part':'problem','original_record':'before','value':'I. First',
                'original_html_sha256':hashlib.sha256(before['html'].encode()).hexdigest(),
                'extractor_sha256':'checked-extractor','extraction_errors':[]}
            path.write_text(json.dumps({'parts':[part]}))
            self.assertEqual(source_record(root,'q-1',content,state)['problem'],'I. First')
            before['html']='<ol type="I"><li>Different</li></ol>'
            with self.assertRaises(ValueError):source_record(root,'q-1',content,state)


    def test_database_comparison_excludes_superseded_source_or_validator(self):
        import hashlib,json,tempfile
        from unittest.mock import patch
        question=self.question()
        digest=hashlib.sha256(json.dumps(question,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        record={'id':'q-1','directory':'/tmp/original','status':'supported',
            'validator_version':REVIEW_VALIDATOR_VERSION,'source_hash':digest}
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);path=root/'batch-0000/result.json';path.parent.mkdir()
            def save():path.write_text(json.dumps({'evidence_version':2,'records':[record]}))
            save()
            with patch('scripts.legacy_recovery.source_record',return_value=question):
                self.assertEqual(set(current_supported_reviews(root)),{'q-1'})
                record['validator_version']-=1;save()
                self.assertEqual(current_supported_reviews(root),{})
                record['validator_version']=REVIEW_VALIDATOR_VERSION;save()
                question['problem']='Changed source prompt'
                self.assertEqual(current_supported_reviews(root),{})

    def test_reconstructed_controls_require_complete_original_identity_and_mathml(self):
        from copy import deepcopy
        raw={'key':'selection','type':'radio','choices':[]};rows=[]
        for option,value in [('a','7'),('b','6')]:
            identity='questionWidget-choiceLetterCircle-1-'+option
            markup='<math><mfrac linethickness="0"><mn>'+value+'</mn><mn>2</mn></mfrac></math>'
            raw['choices'].append({'option':option,'dom_id':identity,'type':'math','value':'old-'+value,'html':markup})
            rows.append('<tr><td class="questionWidget-choiceLetterCircle" id="'+identity+'"></td><td class="questionWidget-choiceText">'+markup+'</td></tr>')
        before={'dom_id':'step-q1','fields':[raw],'html':'<div id="step-q1"><table class="questionWidget-choicesTable">'+''.join(rows)+'</table></div>'}
        reconstructed=deepcopy(raw)
        for choice in reconstructed['choices']:choice['value']='source-genfrac-'+choice['value']
        proof=checked_reconstructed_choices(before,[reconstructed],'q-1')
        self.assertEqual(proof['controls'][0]['reconstructed_value'],'source-genfrac-old-7')
        for kind in ('identity','option','type','mathml','missing_choice'):
            changed=deepcopy(reconstructed)
            if kind=='identity':changed['choices'][0]['dom_id']='questionWidget-choiceLetterCircle-2-a'
            if kind=='option':changed['choices'][0]['option']='b'
            if kind=='type':changed['choices'][0]['type']='text'
            if kind=='mathml':changed['choices'][0]['html']='<math><mn>9</mn></math>'
            if kind=='missing_choice':changed['choices'].pop()
            with self.subTest(kind=kind):self.assertIsNone(checked_reconstructed_choices(before,[changed],'q-1'))


class LegacyCompletionTests(unittest.TestCase):
    def test_combined_key_transaction_refuses_any_additional_content_or_identity_edit(self):
        from copy import deepcopy
        from scripts.legacy_recovery import checked_combined_key_transaction
        from scripts.database.edn import kw
        choices=[{':db/id':100+i,':answer/type':{':db/ident':':answer.type/math'},':answer/value':value}
            for i,value in enumerate(('0','-1','1','2','-2'))]
        old={':db/id':10,':question/problem':'Prompt',':question/worked-solution':'System ${x=1$ and k=1.',
            ':question/answer-fields':[{':db/id':20,':answer-field/key':'selection',
                ':answer-field/choices':choices,':answer-field/correct':choices[3]}]}
        question={'math_academy_id':'q-106896','problem':'Prompt','worked_solution':r'System $\{x=1$ and k=1.',
            'answer_fields':[{'key':'selection','correct_type':'math','correct_value':'1',
                'choices':[{'type':'math','value':c[':answer/value']} for c in choices]}]}
        transaction=[{kw(':db/id'):10,kw(':question/worked-solution'):question['worked_solution']},
            {kw(':db/id'):20,kw(':answer-field/correct'):102}]
        checked_combined_key_transaction(transaction,old,question)
        extra=deepcopy(transaction);extra[0][kw(':question/problem')]='Changed prompt'
        with self.assertRaises(AssertionError):checked_combined_key_transaction(extra,old,question)
        changed=deepcopy(question);changed['worked_solution']=r'System $\{x=2$ and k=1.'
        with self.assertRaises(AssertionError):checked_combined_key_transaction(transaction,old,changed)
        wrong=deepcopy(transaction);wrong[1][kw(':answer-field/correct')]=104
        with self.assertRaises(AssertionError):checked_combined_key_transaction(wrong,old,question)

    def test_exact_assessment_and_diagnostic_terminal_wording_requires_existing_intent(self):
        from scripts.legacy_recovery import legacy_completion_kind
        state={'activity_complete':True,'history_complete':True,'import_complete':True,
            'completion':"You answered 7 of 11 questions correctly for a score of 64%.\nYou've been awarded 8 XP.\nCONTINUE"}
        verification={'committed':True}
        self.assertEqual(legacy_completion_kind(Path('/tmp/13980518'),state,{'task_type':'assessment'},verification),
            'original_assessment_score_and_awarded_xp')
        state['completion']='Diagnostic completed: https://mathacademy.com/tasks/14070542/diagnostics/453741/analysis#'
        self.assertEqual(legacy_completion_kind(Path('/tmp/14070542'),state,{'task_type':'diagnostic'},verification),
            'original_diagnostic_analysis_for_own_task')
        state['completion']='Diagnostic completed: https://mathacademy.com/tasks/14070542/diagnostics/453741/analysis#1'
        self.assertEqual(legacy_completion_kind(Path('/tmp/14070542'),state,{'task_type':'diagnostic'},verification),
            'original_diagnostic_analysis_for_own_task')
        self.assertIsNone(legacy_completion_kind(Path('/tmp/999'),state,{'task_type':'diagnostic'},verification))
        self.assertIsNone(legacy_completion_kind(Path('/tmp/14070542'),state,{'task_type':'review'},verification))
        self.assertIsNone(legacy_completion_kind(Path('/tmp/14070542'),state,{'task_type':'diagnostic'},{'committed':False}))
        state['capture_only']=True
        self.assertIsNone(legacy_completion_kind(Path('/tmp/14070542'),state,{'task_type':'diagnostic'},verification))


if __name__=='__main__':unittest.main()
