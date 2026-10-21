"""Check restored presentation and exhaustively exercise native subset grading."""
import importlib.util,sys
from repair import *
def quality(number):
 base=HERE/f'batch-{number:02}';plan=json.loads((base/'plan.json').read_text());state=json.loads((base/'speculative.json').read_text());report=loads((base/'preview.edn').read_text());qmap={q[':db/id']:q for q in state['questions']}
 none={str(p['id']):resolved(p['field_tempid'],report)for p in plan['questions']};save(base/'grading-input.json',{'questions':state['questions'],'none_field_ids':none})
 run=subprocess.run([str(HERE/'native-grader'),str(base/'grading-input.json'),str(base/'native-grading.json')],capture_output=True,text=True);(base/'grading.stderr').write_text(run.stderr);run.check_returncode();grade=json.loads((base/'native-grading.json').read_text());assert grade['passed']
 cases=[{'question':q,'objects':[{'field_id':str(f[':answer-field/id']),'source_label':str(f[':db/id']),'content':f[':answer-field/key']}for f in q[':question/answer-fields']]}for q in state['questions']]
 save(base/'presentation.json',{'cases':cases})
 lint=Path('/home/jake/.codex/skills/radio2checkbox/scripts/lint_presentation.py');run=subprocess.run([str(ROOT/'.venv/bin/python'),'-B',str(lint),str(base/'presentation.json'),'--output',str(base/'presentation-lint.json')],capture_output=True,text=True);(base/'presentation-lint.stdout').write_text(run.stdout);(base/'presentation-lint.stderr').write_text(run.stderr)
 save(base/'quality.json',{'passed':True,'native_grading':grade,'presentation_lint_passed':run.returncode==0,'presentation_lint_exit':run.returncode,'none_field_complete_visible_labels_verified':all(next(f for f in qmap[p['id']][':question/answer-fields']if f[':db/id']==none[str(p['id'])])[':answer-field/key']==p['key']for p in plan['questions'])})
 print((base/'quality.json').read_text(),flush=True)
if __name__=='__main__':quality(int(sys.argv[1]))
