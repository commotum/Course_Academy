"""Build private evidence only; never writes registered paths."""
import importlib.util,json,pathlib,re,sys
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('draft',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
s=json.loads((HERE/'source.json').read_text());cases=[];independent=[];extracted=[]
for q in s['record'][':knowledge-point/questions']:
    sid=q.get(':question/math-academy-id')
    if sid is None:
        independent.append({'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Same special-square membership recognition; not original difficulty evidence.'});continue
    t=g.TEMPLATES[sid];m=g.arrays(q[':question/problem']);ws=[]
    for l in t['labels']:
        witness=re.search(r'\$\{'+l.lower()+r'\}_\{(\d)(\d)\}=',q.get(':question/worked-solution',''))
        ws.append([int(witness[1]),int(witness[2])] if witness else None)
    case={'source_id':sid,'source_db_id':q[':db/id'],'template':sid,'level':'easy','parameters':{'matrices':[m[l] for l in t['labels']],'witnesses':ws},'bank_profile':'raw-'+sid,'unrated':':question/difficulty' not in q}
    cases.append(case)
    replay=g.generate('easy',template=sid,parameters=case['parameters'],profile=case['bank_profile'])
    print(sid,'prompt exact',replay['question'][':question/problem']==q[':question/problem'],'solution exact',replay['question'].get(':question/worked-solution')==q.get(':question/worked-solution'))
    fields=[]
    for f in q[':question/answer-fields']:
        choices=[{'source_answer_id':a[':answer/id'],'exact_value':a[':answer/value'],'recipe':('Boolean membership of the named matrix in the requested class' if not t.get('radio') else 'Subset of role slots: '+a[':answer/value']),'matched':True} for a in f[':answer-field/choices']]
        fields.append({'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'choices':choices,'correct_present':':answer-field/correct' in f})
    extracted.append({'source_id':sid,'template':sid,'bank_profile':'raw-'+sid,'kind':t['kind'],'labels':t['labels'],'roles':t['roles'],'parameters':case['parameters'],'fields':fields,'solution_stages':['square-shape check','off-diagonal zero check' if t['kind']=='diagonal' else 'diagonal-one and off-diagonal-zero checks','per-matrix decision','full selected-set conclusion'] if ':question/worked-solution' in q else [],'missing_original_attributes':[k for k in [':question/difficulty',':question/worked-solution'] if k not in q]})
(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
(HERE/'independent-inventory.json').write_text(json.dumps({**{k:s[k] for k in ['database','basis','lineage']},'questions':independent},indent=2)+'\n')
(HERE/'extraction.json').write_text(json.dumps(extracted,indent=2)+'\n')
