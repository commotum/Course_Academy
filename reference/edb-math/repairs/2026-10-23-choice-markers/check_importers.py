"""Exercise both actual assignment importers with a mixed free/blank prompt."""
import importlib.util,json,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))

def main():
 results=[]
 for date in ['2026-10-12','2026-10-13-341']:
  script=ROOT/'reference/edb-math/imports/oregon-state'/date/'prepare.py';spec=importlib.util.spec_from_file_location('importer_'+date,script);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  with tempfile.TemporaryDirectory() as d:
   vault=Path(d);path=vault/'assignment.md';path.write_text('');builder=m.CurrentBuilder(vault)
   for label in ['', '\n\nWritten response: {{proof}}', '\n\nYour response: {{proof}}']:
    quiz={'id':'q'+str(len(builder.entities)),'content':'Compute {{value}}, then justify.'+label,'fields':[{'key':'value','type':'blank','correct':{'type':'math','value':'2'}},{'key':'proof','type':'free','correct':{'type':'text','value':'A proof.'}}]}
    uid,audit=builder.canonical_question('source',quiz['id'],quiz,path)
    rows={r[':db/id']:r for r in builder.entities};q=rows[uid];assert q[':question/problem']=='Compute {{value}}, then justify.'
    fields=[rows[f] for f in q[':question/answer-fields']];assert {f[':answer-field/type'] for f in fields}=={':answer-field.type/blank',':answer-field.type/free'}
   builder.validate();results.append({'importer':str(script.relative_to(ROOT)),'mixed_free_blank_prompts':3,'validated':True})
 (HERE/'importer-verification.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
if __name__=='__main__':main()
