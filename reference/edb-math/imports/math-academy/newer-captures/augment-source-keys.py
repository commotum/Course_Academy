import collections
import json
from pathlib import Path
import sys
sys.path.insert(0,'/home/jake/Developer/Course_Academy/scripts')
from import_historical_question_content import Renderer
from bs4 import BeautifulSoup
root=Path('/tmp/newer-captures-prepared')
data=json.loads((root/'source-occurrences.json').read_text())
groups=collections.defaultdict(list)
for q in data['records']:
    if not q['canonical'] and any(f['type'] in ('blank','select') for f in q['answer_fields']):
        groups[q['source_directory']].append(q)
counts=collections.Counter(); conflicts=[]
for i,(directory,questions) in enumerate(groups.items(),1):
    path=Path(directory)/'activity-metadata.json'
    if not path.exists():continue
    metadata=json.loads(path.read_text())
    if not isinstance(metadata,list):continue
    metadata={x['id'].replace('question-','q-'):x for x in metadata if x.get('id')}
    for q in questions:
        raw=metadata.get(q['math_academy_id'],{}).get('raw_html','')
        if not raw or ('freeResponseTextbox' not in raw and 'correctSelection' not in raw):continue
        soup=BeautifulSoup(raw,'html.parser');renderer=Renderer(str(q['topic_id']))
        try:renderer.text(soup,True)
        except (AssertionError,IndexError,KeyError):continue
        if renderer.errors:continue
        observed={f['key']:f for f in renderer.fields}
        for field in q['answer_fields']:
            source=observed.get(field['key'])
            if not source or source['type']!=field['type'] or not source.get('correct_value'):continue
            correct=next((c for c in source['choices'] if c['value']==source['correct_value']),None)
            if not correct:continue
            if field.get('correct') and field['correct']!=correct:
                conflicts.append({'question':q['math_academy_id'],'task':q['task'],'accepted_submission':field['correct'],'history_displayed_answer':correct,'history_metadata':str(path)})
            if not field.get('correct'):counts['new_direct_keys']+=1
            field['correct']=correct;field['key_evidence']='ma_history_displayed_answer'
            if field['type']=='blank':field['choices']=[correct]
            elif not any(c==correct for c in field['choices']):
                field['choices'].append(correct)
            counts['direct_keys']+=1
    if i%300==0:print('Read history key evidence',i,'/',len(groups),flush=True)
(root/'source-occurrences.json').write_text(json.dumps(data,ensure_ascii=False)+'\n')
(root/'displayed-key-observations.json').write_text(json.dumps({'counts':counts,'different_serializations_from_accepted_submission':conflicts},indent=2)+'\n')
print(json.dumps({'counts':counts,'different_serializations':len(conflicts)},indent=2),flush=True)
