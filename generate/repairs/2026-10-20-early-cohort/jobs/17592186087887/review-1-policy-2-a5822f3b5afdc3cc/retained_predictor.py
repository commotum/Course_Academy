#!/usr/bin/env python3
"""Strict independent acceptance regression; exits 1 for the current package.
Run: .venv/bin/python reproduce_shortcut.py --package /path/to/package
The predictor receives only candidate strings/UUIDs, never the ODE or key.
"""
import sys,pathlib,json,argparse,importlib.util,re,collections
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent

def predict(field):
 bank=field[':answer-field/choices']
 root=[z for z in bank if '\\sqrt[3]' in z[':answer/value']]
 if len(root)==1:return 'unique cube root',root[0][':answer/id']
 log=[z for z in bank if 'x\\ln|x|' in z[':answer/value'] and z[':answer/value'].endswith('+Cx')]
 if len(log)==1:return 'x log and Cx',log[0][':answer/id']
 affine=[]
 for z in bank:
  m=re.fullmatch(r'y=Cx\^2[+-](\d*)x',z[':answer/value'])
  if m:affine.append((int(m.group(1) or 1),z))
 if len(affine)==2 and affine[0][0]!=affine[1][0]:return 'smaller affine coefficient',min(affine,key=lambda z:z[0])[1][':answer/id']
 return 'no recognized cue',None

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--package',type=pathlib.Path,default=E.parent/'workspace');args=ap.parse_args()
 sys.path.insert(0,str(args.package));import generator
 groups={'sample':generator.generate_batch('easy',54,826031),'runner_batch':json.loads((E/'runner-batch.json').read_text()),'delivered_batch':json.loads((E/'delivery-batch/accepted.json').read_text()),'delivered_sample':json.loads((E/'delivery-independent/accepted.json').read_text()),'stored_generated':json.loads((E/'generated-records.json').read_text())}
 results=[];native=json.loads((E/'grader-input.json').read_text());failures=[]
 for label,records in groups.items():
  for i,r in enumerate(records):
   f=r['question'][':question/answer-fields'][0];cue,aid=predict(f);correct=aid==f[':answer-field/correct'][1]
   results.append({'group':label,'index':i,'cue':cue,'question_id':r['question'][':question/id'],'predicted_id':aid,'correct':correct})
   if aid:native.append({'label':f'bank-only {label} {i}: {cue}','record':r,'checks':[{'submitted_answer_id':aid,'expected':'accepted' if correct else 'rejected','purpose':'Actual grader test of prompt-blind strategy; no response generated using key'}]})
  for cue in ('unique cube root','x log and Cx','smaller affine coefficient'):
   sub=[z for z in results if z['group']==label and z['cue']==cue]
   if sub and all(z['correct'] for z in sub):failures.append({'group':label,'cue':cue,'correct':len(sub),'total':len(sub)})
 summary={g:{'correct':sum(z['correct'] for z in results if z['group']==g),'total':len(rs)} for g,rs in groups.items()}
 (E/'shortcut-regression.json').write_text(json.dumps({'expected':'No listed bank-only strategy should perfectly answer a whole generated easy family. Original replay bank can be retained while extension banks vary eligible distractors.','baseline':0.2,'summary':summary,'failures':failures,'outcomes':results},indent=2)+'\n')
 (E/'grader-final-input.json').write_text(json.dumps(native,indent=2)+'\n')
 print(json.dumps({'summary':summary,'status':'failed' if failures else 'passed','family_stage_failures':len(failures)}))
 return 1 if failures else 0
if __name__=='__main__':sys.exit(main())
