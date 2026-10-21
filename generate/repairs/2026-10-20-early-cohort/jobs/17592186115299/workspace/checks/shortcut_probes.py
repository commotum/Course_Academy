"""Measure visible-answer position, label, category, and source schedule predictors."""
import collections,json,sys,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import validate_repair as c

def probes(records):
 groups=collections.defaultdict(lambda:collections.defaultdict(collections.Counter))
 for r in records:
  q=r['question'];m,kind,_=c.mathematical(r);fs=q[':question/answer-fields'];f=fs[0]
  if r['generation']['response_layout']=='radio':
   correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);position=next(i for i,a in enumerate(f[':answer-field/choices']) if a is correct);label=correct[':answer/value']
  else:
   position=next(i for i,f in enumerate(fs) if any(a[':answer/id']==f[':answer-field/correct'][1] and a[':answer/value']=='true' for a in f[':answer-field/choices']));label=fs[position][':answer-field/key']
  for key in ['schedule:'+r['generation']['template'],'bank:'+r['generation']['bank_profile'],f'visible:{m.rows}x{m.cols-1}/'+r['generation']['response_layout']+'/None='+str(any(f[':answer-field/key']=='None of the above' for f in fs))]:
   groups[key]['category'][kind]+=1;groups[key]['position'][str(position)]+=1;groups[key]['label'][label]+=1
 out={}
 for key,features in groups.items():
  out[key]={}
  for feature,counts in features.items():
   successes=max(counts.values());attempts=sum(counts.values())
   assert successes<attempts,(key,feature,counts)
   out[key][feature]={'best_fixed_cue_successes':successes,'attempts':attempts,'outcomes':dict(counts),'constant_prediction_perfect':False}
 return out

def main():
 raw=json.loads((c.E/'delivery-input.json').read_text());accepted=json.loads((c.E/'delivery/accepted.json').read_text())
 report={'passed':True,'scope':'Coverage sample stops after each source schedule exhibits its mathematically eligible cases; proportions are not estimates of production frequencies. Fixed category, answer label and option position probes are conditional on each schedule, bank and visible shape/response group. Exhaustive count-one classification is a valid consequence of mutually exclusive definitions.','before_delivery':probes(raw),'after_delivery':probes(accepted),'controlled_relevant_changes':'evidence/counterfactual-records.json','controlled_irrelevant_changes':'evidence/final-focus.json','command':'python checks/shortcut_probes.py'}
 final=json.loads((c.E/'final-delivery/accepted.json').read_text());assert len(final)==5
 fixtures=[{'label':'final-'+str(i),'record':r,'checks':c.mathematical(r)[2]} for i,r in enumerate(final)];c.dump('final-batch-native-input.json',fixtures)
 subprocess.run([str(c.REPO/'generate/runs/current/check-engine'),str(c.E/'final-batch-native-input.json'),str(c.E/'final-batch-native-report.json')],check=True)
 report['final_cli_batch']={'seed':20261021,'generated':5,'accepted':5,'classifications':dict(collections.Counter(c.mathematical(r)[1] for r in final))};c.dump('shortcut-probes.json',report)
 print(json.dumps({'passed':True,'conditional_groups':len(report['before_delivery']),'final_batch_accepted':5}))
if __name__=='__main__':main()
