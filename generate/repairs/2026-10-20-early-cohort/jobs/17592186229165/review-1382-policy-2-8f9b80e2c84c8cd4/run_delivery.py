from independent_lib import *
samples=load(ROOT/'independent-samples.json')
easy=[r for r in samples+load(ROOT/'counterfactual-records.json')+load(ROOT/'boundary-records.json') if r['question'][':question/difficulty'].endswith('/easy')]
save('independent-easy.json',easy)
commands=[]
from concurrent.futures import ThreadPoolExecutor
def run(args):
 name,file,level=args
 cmd=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(ROOT/file),'--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),'--difficulty',level,'--output',str(ROOT/name),'--asset-root',str(ROOT),'--math-root','/media/jake/SSD/EDB/math']
 p=subprocess.run(cmd,capture_output=True,text=True);(ROOT/(name+'.log')).write_text(p.stdout+p.stderr)
 return {'command':cmd,'exit_code':p.returncode,'report':name+'/delivery.json'}
with ThreadPoolExecutor(max_workers=3) as ex: commands=list(ex.map(run,[('delivery-batch','runner-batch.json','easy'),('delivery-independent','independent-easy.json','easy'),('delivery-hard','hard-samples.json','hard')]))
save('delivery-commands.json',commands);assert all(c['exit_code']==0 for c in commands)
# Include actual delivered normalized records in the same native-grader invocation.
grading=load(ROOT/'grader-input.json')
for name in ['delivery-batch','delivery-hard']:
 for i,r in enumerate(load(ROOT/name/'accepted.json')[:5 if name=='delivery-batch' else 3]):
  y=texparse(answers(r)[0]);grading.append({'label':name+str(i),'record':r,'checks':[{'submitted':S.latex(S.factor(y)),'expected':'accepted','purpose':'equivalent delivered expression'},{'submitted':'0','expected':'rejected','purpose':'omit forcing'}]})
save('grader-delivered-input.json',grading)
cmd=[str(REPO/'generate/runs/current/check-engine'),str(ROOT/'grader-delivered-input.json'),str(ROOT/'grader-delivered-report.json')]
p=subprocess.run(cmd,capture_output=True,text=True);(ROOT/'grader-delivered.log').write_text(p.stdout+p.stderr);save('grader-command.json',{'command':cmd,'exit_code':p.returncode});assert p.returncode==0
print(json.dumps({'delivery_reports':[load(ROOT/c['report']) for c in commands],'grader_exit':p.returncode}))
