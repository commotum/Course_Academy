"""Audit the complete captured inventory and fresh output for diagram usage."""
import json,os,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;summary=[];render=[]
image=re.compile(r'!\[[^\]]*\]\(|<img\b|images/|\.svg(?:[)\s\"\']|$)|\.png(?:[)\s\"\']|$)',re.I)
def scan(q):
    refs=[]
    for key in (':question/problem',':question/worked-solution'):
        if image.search(q.get(key,'')):refs.append(key)
    for f in q.get(':question/answer-fields',[]):
        for a in f.get(':answer-field/choices',[]):
            kind=a.get(':answer/type');kind=kind.get(':db/ident') if isinstance(kind,dict) else kind
            if kind==':answer.type/image' or image.search(a.get(':answer/value','')):refs.append(':answer/value')
    return refs

for row in json.loads((H/'inventory.json').read_text()):
    kp=row['kp'];h=H/str(kp);k=json.loads((h/'before.json').read_text());questions=[k[':knowledge-point/canonical-example'],*k[':knowledge-point/questions']]
    refs=[{'question':q[':db/id'],'attributes':scan(q)} for q in questions if scan(q)]
    assert not refs,refs
    fresh=[]
    for level in ('easy','moderate','hard'):
        out=subprocess.run([sys.executable,str(h/'package/generator.py'),'--difficulty',level,'--count','2','--seed','2026103087722'],check=True,capture_output=True,text=True,timeout=45,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        records=json.loads(out.stdout);assert len(records)==2
        for r in records:
            assert not scan(r['question'])
            assert not r.get('assets') and not r['generation'].get('plot_assets')
        fresh+=records;render.append(records[0])
    (h/'fresh-samples.json').write_text(json.dumps(fresh,indent=2)+'\n')
    summary.append({'kp':kp,'title':row['title'],'imported':row['imported'],'active_generated':len(row['active_generated']),'total_captured_questions_including_canonical':len(questions),'stored_image_references':refs,'fresh_questions_checked':len(fresh),'fresh_plot_assets':0,'plotter_present':any('matplotlib' in p.read_text() or 'MaxNLocator' in p.read_text() for p in (h/'package').glob('*.py')),'decision':'No plotter present; presentation findings are recorded separately'})
(H/'render-input.json').write_text(json.dumps(render,indent=2)+'\n')
(H/'audit.json').write_text(json.dumps({'passed':True,'basis':json.loads((H/'inventory.json').read_text())[0]['basis'],'kps':summary,'database_writes':0},indent=2)+'\n')
print(json.dumps(summary,indent=2))
