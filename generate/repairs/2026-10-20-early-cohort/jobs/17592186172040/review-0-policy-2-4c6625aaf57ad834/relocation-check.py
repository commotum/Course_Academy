from review import *
import importlib.util
s=importlib.util.spec_from_file_location('gen',PK/(KP+'.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
seed=3665148268;r=g.generate('moderate',seed=seed);dump('relocated-batch-record.json',[r])
p=subprocess.run([P,R/'generate/pipeline/check_delivery.py','--input',E/'relocated-batch-record.json','--source',J/'source/source.json','--inventory',J/'source/inventory.json','--difficulty','moderate','--output',E/'delivery-relocated','--asset-root',PK/KP,'--math-root','/media/jake/SSD/EDB/math'],capture_output=True,text=True)
dump('relocation-delivery-command.json',{'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
a=json.loads((E/'delivery-relocated/accepted.json').read_text())[0];b=json.loads((E/'delivery-batch/accepted.json').read_text())[0]
dump('relocation-results.json',{'seed':seed,'delivery_exit':p.returncode,'raw_id_equal':r['question'][':question/id']==json.loads((E/'batch-records.json').read_text())[0]['question'][':question/id'],'normalized_question_equal':a['question']==b['question'],'normalized_ids':[a['question'][':question/id'],b['question'][':question/id']],'conclusion':'Absolute raw asset paths alter raw identities, but shared publication normalization recovers identical served questions after relocation.'})
print('normalized relocation equality',a['question']==b['question'])
