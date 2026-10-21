"""Reflow exact matching inline references to the reviewed long equations."""
import copy,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
MATH=re.compile(r'(?<!\\)\$\$[\s\S]*?(?<!\\)\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$])*?(?<!\\)\$')
cases=json.loads((HERE/'overflow-cases.json').read_text())['cases']
overrides=json.loads((HERE/'overflow-overrides.json').read_text())
mapping={}
for override in overrides:
    qmap=mapping.setdefault(override['question_eid'],{})
    for m in override['math_spans']:
        assert m['before'] not in qmap or qmap[m['before']]==m['after']
        qmap[m['before']]=m['after']
changes=[];results=[]
for original in cases:
    case=copy.deepcopy(original);qid=case['question'];before=case['after'].get(':question/worked-solution','');after=before;qmap=mapping[qid];spans=[]
    for match in MATH.finditer(before):
        if match[0].startswith('$$') or match[0] not in qmap:continue
        spans.append({'start':match.start(),'end':match.end(),'before':match[0],'after':qmap[match[0]]})
    for span in reversed(spans):after=after[:span['start']]+span['after']+after[span['end']:]
    if spans:
        assert re.sub(r'\s+','',before.replace('$',''))==re.sub(r'\s+','',after.replace('$',''))
        changes.append({'question_eid':qid,'attribute':':question/worked-solution','before':before,'after':after,'spans':spans,'reason':'Reflow isolated inline references to the corresponding complete options at their existing mathematical operators; display equations are unchanged.'})
        case['after'][':question/worked-solution']=after
    results.append(case)
(HERE/'solution-overrides.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
(HERE/'overflow-with-solutions.json').write_text(json.dumps({'cases':results},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'questions':len(changes),'inline_spans':sum(len(c['spans'])for c in changes)}))
