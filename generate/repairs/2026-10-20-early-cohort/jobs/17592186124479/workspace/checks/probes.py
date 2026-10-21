"""Cue probes before/after shared filters and captured-source differences."""
import sys
sys.dont_write_bytecode=True
import json,re
from pathlib import Path
from collections import defaultdict
from audit import matrices,answer,field
from repair_checks import assert_varied
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence'
sys.path.insert(0,str(ROOT))
import generator as g

def read(name):return json.loads((OUT/name).read_text())
def facts(r):
    a=matrices(r['question'][':question/problem'])[0];f=field(r)
    choices=[int(c[':answer/value']) for c in f[':answer-field/choices']]
    return {'id':r['question'][':question/id'],'template':str((a.rows,a.cols,len(matrices(r['question'][':question/worked-solution']))-1,tuple(sorted(choices)))),'rows':a.rows,'cols':a.cols,'active':sum(any(a.row(i)) for i in range(a.rows)),'columns':sum(any(a.col(i)) for i in range(a.cols)),'rank':int(a.rank()),'label':re.search(r'\$([A-Z])',r['question'][':question/problem'])[1],'choices':choices}

def summarize(records,delivered_batch=False):
    fs=[facts(r) for r in records];groups=defaultdict(list);groups['overall']=fs
    for f in fs:
        groups['template/'+f['template']].append(f)
        groups['shape/'+str((f['rows'],f['cols']))].append(f)
        groups['workload/active/'+f['template']+'/'+str(f['active'])].append(f)
    probes=[]
    strategies={'rows minus one':lambda f:f['rows']-1,'rows':lambda f:f['rows'],'nonzero rows':lambda f:f['active'],'nonzero rows minus one':lambda f:f['active']-1,'nonzero columns':lambda f:f['columns'],'first choice':lambda f:f['choices'][0],'last choice':lambda f:f['choices'][-1],'minimum choice':lambda f:min(f['choices']),'maximum choice':lambda f:max(f['choices'])}
    for cue,group in groups.items():
        assert len({f['rank'] for f in group})>=2,(cue,group)
        for label,fn in strategies.items():
            successes=sum(fn(f)==f['rank'] for f in group)
            probes.append({'group':cue,'strategy':label,'successes':successes,'total':len(group)})
            if delivered_batch:assert successes<len(group),('Perfect incidental predictor',cue,label)
    # Distinct correct option positions within every workload. Labels and option
    # order are independently shuffled, but tiny groups may coincide by chance.
    labels=defaultdict(set);positions=defaultdict(list)
    for f in fs:
        labels[f['template']+'/'+f['label']].add(f['rank'])
        positions[f['template']].append(f['choices'].index(f['rank']))
    return {'label_rank_observations':{k:sorted(v) for k,v in labels.items()},'correct_choice_positions_zero_based':dict(positions),'label_limits':'Sparse label groups are observations only; counterfactual-records.json holds name fixed across changed ranks and changes name across an unchanged matrix, with native grading checked. Choice position and label are not used in rank construction.', 'count':len(fs),'semantic_instances':len({r['generation']['mathematical_fingerprint'] for r in records}),'facts':fs,'probes':probes,'baseline':'1/5 for a uniform random choice. Exact proposed batch rejects every tested strategy within each recognizable workload and active-row group. Controls are a union of independent two-item batches, boundary and counterfactual witnesses; chance coincidences in tiny subgroups are reported as fractions, not presented as evidence of a sampler rule or an actual delivered batch. Rank contrast is required for every structural control group.'}

def main():
    result={}
    for key,name in [('batch_before','repaired-batch.json'),('batch_after','delivery/accepted.json'),('control_before','control-records.json'),('control_after','delivery-controls/accepted.json')]:
        records=read(name);result[key]=summarize(records,delivered_batch=key.startswith('batch'))
        if key.startswith('batch'):assert_varied(records)
    captured=json.loads((ROOT.parent/'source/source.json').read_text())['material']['kp']
    differences=[]
    for supplied,local in zip(captured[':knowledge-point/questions'],g.KP[':knowledge-point/questions']):
        assert supplied[':question/id']==local[':question/id']
        for key in supplied:
            if supplied[key]!=local.get(key):
                assert isinstance(supplied[key],str)
                normalized=lambda x:x.replace(r'\left','').replace(r'\right','')
                assert normalized(supplied[key])==normalized(local[key]),(key,supplied[':question/id'])
                differences.append({'source_id':supplied[':question/id'],'field':key,'difference':'Scalable parentheses only; complete visible matrix stages, banks and keys checked in validate.py.'})
    result['source_evidence_difference']={'differences':differences,'old_counterexample':'Still applies to the unchanged mathematical task; fresh source replay passes and original strict batch check fails on the saved original records. No source change used to dismiss it.'}
    result['template_grouping']='Recognizable workloads use shape, operation count and full bank; source question IDs with the same workload are aliases. One duplicate control was removed by shared filtering and its identical visible mathematics remains under a different source alias. Primary delivered batch retains all five records.'
    result['selection_limits']='question_selection.rs chooses uniformly within the available positively weighted moderate pool, or first ID if weights are unconfigured. History excludes prior items; the package cannot guarantee contrasts in arbitrary remaining subsets or single-item requests. Whole delivered bank has contrasts before/after actual normalization, dedup and captured-inventory exclusion. No live learner history or policy was accessed.'
    (OUT/'pedagogical-variation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v['count'] for k,v in result.items() if isinstance(v,dict) and 'count' in v}))
if __name__=='__main__':main()
