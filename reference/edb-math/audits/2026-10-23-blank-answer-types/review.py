"""Persist the individual contextual review; no heuristic-driven writes."""
import collections,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import dumps,kw
REPAIRS={
17592186232538:'The question asks for a slope; the worked solution concludes m=-4*pi. This is a mathematical constant, not prose.',
17592186232883:'This field is the x coefficient in a tangent-line equation. The worked solution derives the slope -pi*sqrt(3).',
17592186232885:'This field is the constant term in the same tangent-line equation. The solution derives pi*sqrt(3)+2.',
17592186232887:'The blank is f\u2032(x), and the solution derives the expression -6*sin(x)^2*cos(x).',
17592186232889:'The blank is f\u2032(x), and the solution derives -7*cos(x)^6*sin(x).',
}

def main():
 rows=json.loads((H/'text-blank-fields.json').read_text());reviews=[]
 for row in rows:
  a=row['answer'];q=row['questions'][0]
  if a in REPAIRS:decision='repair-to-math';reason=REPAIRS[a]
  elif row['value'] in ('<','>'):decision='retain-text';reason='This is a literal one-character comparison-token response, with no mathematical expression or TeX shortcut to enter. Preserve its existing exact-token response contract.'
  elif q['entity'] in (17592186405910,17592186405427):decision='retain-text';reason=f'This field ({row["key"]}) asks for a diagram/equation label or Roman-numeral curve identifier, not the expression represented by that label.'
  elif row['key']=='excluded':decision='retain-text';reason='The response is a prose description of excluded domain points, not a standalone expression. Preserve the words and exact-text input.'
  elif row['value']=='DNE':decision='retain-text';reason='The prompt explicitly requests the literal text DNE for a nonexistent limit.'
  elif row['value'] in ('positive','negative','approximately zero'):decision='retain-text';reason='The prompt requests a qualitative sign classification, not an evaluated integral or numerical expression.'
  elif row['value']=='less':decision='retain-text';reason='This blank completes the prose phrase “less than”; it is not the separate mathematical comparison field.'
  elif row['value'] in ('A','B','C'):decision='retain-text';reason='The prompt requests the name of a slice, polygon, graph, or marked point. This is a label, not an algebraic variable.'
  elif row['value'] in ('A, B, C, D, F','B, C, D'):decision='retain-text';reason='The prompt asks for a list of curve labels. Treating it as an algebraic expression would change the response contract.'
  else:raise AssertionError(('unreviewed',a,row['value']))
  reviews.append({'answer':a,'field':row['field'],'value':row['value'],'questions':[q['entity'] for q in row['questions']],'decision':decision,'reason':reason})
 assert len(reviews)==48 and sum(r['decision']=='repair-to-math' for r in reviews)==5
 (H/'individual-review.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n');changes=[r for r in reviews if r['decision']=='repair-to-math'];(H/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
 payload=dumps([[kw('db/cas'),r['answer'],kw('answer/type'),kw('answer.type/text'),kw('answer.type/math')] for r in changes])+'\n';(H/'transaction.edn').write_text(payload)
 print('Individually reviewed',len(reviews),'repair',len(changes),'retain',len(reviews)-len(changes));print(payload)
if __name__=='__main__':main()
