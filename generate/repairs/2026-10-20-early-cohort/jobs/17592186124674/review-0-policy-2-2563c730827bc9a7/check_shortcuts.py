import subprocess,json,pathlib,collections,sys
E=pathlib.Path(__file__).resolve().parent
commands=[]
for input_,output,index in [('boundary-records.json','shortcut-minimal.json',0),('samples.json','shortcut-fresh.json',None),('runner-batch.json','shortcut-batch.json',None),('delivery-fresh/accepted.json','shortcut-delivered-fresh.json',None),('delivery-batch/accepted.json','shortcut-delivered-batch.json',None)]:
 cmd=[sys.executable,'-B',str(E/'reproduce_shortcut.py'),'--input',input_,'--output',output]
 if index is not None:cmd+=['--index',str(index)]
 p=subprocess.run(cmd,cwd=E,capture_output=True,text=True);commands.append({'command':cmd,'exit_code':p.returncode,'summary':p.stdout.strip(),'stderr':p.stderr})
(E/'shortcut-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
print('\n'.join(x['summary'] for x in commands))
