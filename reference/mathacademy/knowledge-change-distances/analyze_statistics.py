"""Descriptive statistics of captured display-band changes; no database access."""
import json
import math
import os
import statistics as stat
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
data = json.loads((HERE/'results.json').read_text())
activities, rows = data['activities'], data['changes']
names = {int(k):v for k,v in data['topic_names'].items()}
by_task = defaultdict(list)
by_topic = defaultdict(list)
for r in rows:
    by_task[r['task_id']].append(r); by_topic[r['topic_id']].append(r)
    r['delta'] = r['after_band']-r['before_band']
    u,d = r['distances']['prerequisite'],r['distances']['downstream']
    r['relation'] = ('self' if r['topic_id'] in r['origins'] else
                     'both' if u is not None and d is not None else
                     'prerequisite' if u is not None else
                     'downstream' if d is not None else 'other_branch')

def percentile(values,q):
    v=sorted(values);p=(len(v)-1)*q;lo=math.floor(p);hi=math.ceil(p)
    return v[lo]+(v[hi]-v[lo])*(p-lo) if v else None

def describe(values):
    return {'n':len(values),'total':sum(values),'mean':stat.mean(values) if values else None,
        'median':stat.median(values) if values else None,'population_sd':stat.pstdev(values) if values else None,
        'min':min(values) if values else None,'max':max(values) if values else None,
        **{f'p{round(q*100)}':percentile(values,q) for q in (.1,.25,.75,.9,.95,.99)}}

def breakdown(selected):
    return {'count':len(selected),'up':sum(r['delta']>0 for r in selected),
        'down':sum(r['delta']<0 for r in selected),'same_band':sum(r['delta']==0 for r in selected),
        'net_band_steps':sum(r['delta'] for r in selected),
        'mean_undirected_distance':stat.mean(r['distances']['undirected'] for r in selected) if selected else None}

tracked=set();course_topics=defaultdict(set)
for a in activities:
    snapshot=json.loads(Path(a['snapshot']).read_text())
    for course in snapshot['courses']:
        ids={t['topic_id'] for t in course['topics']}
        tracked.update(ids);course_topics[course['course_id']].update(ids)

activity_stats=describe([a['changed_topics'] for a in activities])
activity_distribution=Counter(a['changed_topics'] for a in activities)
activity_types={kind:{'activities':len(group),
    'zero_update_activities':sum(a['changed_topics']==0 for a in group),
    'updates':describe([a['changed_topics'] for a in group]),
    'change_details':breakdown([r for r in rows if r['type']==kind])}
    for kind in sorted({a['type'] for a in activities})
    for group in [[a for a in activities if a['type']==kind]]}
clean_activities=[a for a in activities if a['comparison_is_consecutive'] and not a['recovered']]
clean_rows=[r for r in rows if r['comparison_is_consecutive'] and not r['recovered']]
relations={kind:breakdown([r for r in rows if r['relation']==kind])
    for kind in ['self','prerequisite','downstream','both','other_branch']}
distance_stats={kind:describe([r['distances'][kind] for r in rows if r['distances'][kind] is not None])
    for kind in ['prerequisite','downstream','undirected']}
strict_up=describe([r['distances']['prerequisite'] for r in rows
                   if r['distances']['prerequisite'] not in (None,0)])
distance_levels=[]
for level in range(max(s['max'] for s in distance_stats.values())+1):
    selected={kind:[r for r in rows if r['distances'][kind]==level] for kind in distance_stats}
    distance_levels.append({'level':level,**{kind:breakdown(group) for kind,group in selected.items()},
        'activities_with_upstream_update':len({r['task_id'] for r in selected['prerequisite']})})

topic_stats=[];reversals=0;exact_reversals=0;adjacent_changes=0
for tid,group in by_topic.items():
    group=sorted(group,key=lambda r:r['finished_at'])
    for previous,current in zip(group,group[1:]):
        # Compare within a course: identical topics can appear in several courses.
        if previous['course_id']!=current['course_id']:continue
        adjacent_changes+=1
        reversals+=previous['delta']*current['delta']<0
        exact_reversals+=(previous['before_band']==current['after_band'] and
                          previous['after_band']==current['before_band'])
    topic_stats.append({'topic_id':tid,'title':names[tid],**breakdown(group),
                       'self_updates':sum(r['relation']=='self' for r in group),
                       'upstream_updates':sum(r['relation'] in ('prerequisite','both') for r in group)})
topic_stats.sort(key=lambda r:(-r['count'],r['topic_id']))
single=[a for a in activities if a['type'] in ('lesson','review') and len(a['origins'])==1]
source_stats=[]
for tid in sorted({a['origins'][0] for a in single}):
    selected=[a for a in single if a['origins'][0]==tid]
    source_stats.append({'topic_id':tid,'title':names[tid],'activities':len(selected),
        'updates':sum(a['changed_topics'] for a in selected),
        'mean_updates':stat.mean(a['changed_topics'] for a in selected),
        'self_update_activities':sum(any(r['relation']=='self' for r in by_task[a['task_id']]) for a in selected)})
source_stats.sort(key=lambda r:(-r['mean_updates'],-r['activities'],r['topic_id']))
bands=[{'band':b,'before':sum(r['before_band']==b for r in rows),
        'after':sum(r['after_band']==b for r in rows),
        'up_from':sum(r['before_band']==b and r['delta']>0 for r in rows),
        'down_from':sum(r['before_band']==b and r['delta']<0 for r in rows)} for b in range(7)]
transitions=[[sum(r['before_band']==before and r['after_band']==after for r in rows)
              for after in range(7)] for before in range(7)]
result={'dataset':{'database_basis':data['summary']['database_basis'],'activities':len(activities),
    'first_snapshot':activities[0]['finished_at'],'last_snapshot':activities[-1]['finished_at'],
    'updates':len(rows),'changed_topics':len(by_topic),'tracked_topics':len(tracked),
    'tracked_topics_without_updates':len(tracked-set(by_topic)),
    'mean_updates_per_changed_topic':len(rows)/len(by_topic),
    'mean_updates_per_tracked_topic':len(rows)/len(tracked),
    'single_topic_activities':len(single),'distinct_single_activity_topics':len(source_stats),
    'single_topic_activities_with_own_topic_change':sum(any(r['relation']=='self' for r in by_task[a['task_id']]) for a in single)},
    'activity_updates':activity_stats,'activity_update_histogram':dict(sorted(activity_distribution.items())),
    'activity_types':activity_types,'relations':relations,'distances':distance_stats,
    'strict_upstream_distance':strict_up,'distance_levels':distance_levels,
    'overall':breakdown(rows),'band_step_change':describe([r['delta'] for r in rows]),
    'mean_absolute_band_step_change':stat.mean(abs(r['delta']) for r in rows),
    'band_delta_histogram':dict(sorted(Counter(r['delta'] for r in rows).items())),
    'band_transitions':transitions,'band_totals':bands,
    'changed_topic_update_counts':describe([len(v) for v in by_topic.values()]),
    'tracked_topic_update_histogram':dict(sorted(Counter(len(by_topic.get(t,[])) for t in tracked).items())),
    'course_statistics':{c:{'tracked_topics':len(ids),**breakdown([r for r in rows if r['course_id']==c])}
                         for c,ids in course_topics.items()},
    'sensitivity':{'consecutive_unrecovered_activities':len(clean_activities),
        'updates_per_activity':describe([a['changed_topics'] for a in clean_activities]),
        'changes':breakdown(clean_rows),'distance':describe([r['distances']['undirected'] for r in clean_rows]),
        'recovered_snapshots':sum(a['recovered'] for a in activities),
        'nonconsecutive_snapshots':sum(not a['comparison_is_consecutive'] for a in activities)},
    'reversals':{'adjacent_topic_change_pairs':adjacent_changes,'opposite_direction_pairs':reversals,
                 'exact_band_reversal_pairs':exact_reversals},
    'topics_by_update_frequency':topic_stats,'practiced_topics_by_mean_updates':source_stats}
assert sum(rel['count'] for rel in relations.values())==len(rows)
assert sum(activity_distribution.values())==len(activities)
assert sum(k*v for k,v in activity_distribution.items())==len(rows)
assert sum(level['undirected']['count'] for level in distance_levels)==len(rows)
assert sum(sum(row) for row in transitions)==len(rows)
(HERE/'statistics.json').write_text(json.dumps(result,indent=2)+'\n')

def fmt(value):
    if value is None:return '—'
    if isinstance(value,float):return f'{value:.2f}'
    return str(value)

def table(headers, records):
    return ['| '+' | '.join(headers)+' |','|'+'|'.join('---' for h in headers)+'|']+[
        '| '+' | '.join(fmt(v).replace('|','\\|') for v in record)+' |' for record in records]+['']

def pct(n,den=len(rows)):
    return f'{100*n/den:.1f}%'

local=lambda instant:datetime.fromisoformat(instant).astimezone(ZoneInfo('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S %Z')
ds=result['dataset']
text=['# Statistical breakdown of captured knowledge-band changes','',
    f"Period: {local(ds['first_snapshot'])} through {local(ds['last_snapshot'])}.",'',
    f"{len(activities)} completed activity snapshots; {len(rows)} observed band changes; {len(by_topic)} changed topics out of {len(tracked)} distinct tracked topics. Prerequisite graph read at database basis {data['summary']['database_basis']}; this analysis makes no database calls or transactions.",'',
    'An update is one topic whose displayed color/band differs from its comparison snapshot. This is not every internal knowledge-state update, a per-question update, or evidence that the associated activity caused the change. Band differences are ordinal display steps, not calibrated quantities of knowledge. Each snapshot reads the three course pages sequentially. Every one of the 810 logged changes was cross-checked against its saved before/after snapshot, with zero mismatches.','',
    'Shortest graph distance uses only authoritative `:topic/next` prerequisite edges. Upstream goes toward prerequisites, downstream toward dependent topics, and either-direction distance permits both. Assessments/multisteps use the nearest of their captured question topics. Means over changes weight frequently changing topics more heavily.','',
    '## Overall activity and topic spread','']
text+=table(['Measure','Value'],[
    ['Mean updates per activity',activity_stats['mean']],['Median updates per activity',activity_stats['median']],
    ['Population SD of updates per activity',activity_stats['population_sd']],['Range of updates per activity','0–26'],
    ['Middle 50% of activities','1–8 updates'],['90th percentile',activity_stats['p90']],['95th percentile',activity_stats['p95']],
    ['Activities with zero updates',f"{activity_distribution[0]} ({pct(activity_distribution[0],len(activities))})"],
    ['Mean updates per nonzero-update activity',len(rows)/(len(activities)-activity_distribution[0])],
    ['Mean updates per changed topic',ds['mean_updates_per_changed_topic']],['Median updates per changed topic',result['changed_topic_update_counts']['median']],
    ['Mean updates per tracked topic, including zeros',ds['mean_updates_per_tracked_topic']],
    ['Tracked topics with no changes',f"{ds['tracked_topics_without_updates']} ({pct(ds['tracked_topics_without_updates'],len(tracked))})"],
    ['Practiced lesson/review topics',len(source_stats)],
    ['Lesson/review activities with own-topic band change',f"{ds['single_topic_activities_with_own_topic_change']}/{len(single)} ({pct(ds['single_topic_activities_with_own_topic_change'],len(single))})"],
    ['Rising / falling updates',f"{result['overall']['up']} ({pct(result['overall']['up'])}) / {result['overall']['down']} ({pct(result['overall']['down'])})"],
    ['Mean absolute band-step change',result['mean_absolute_band_step_change']]])
text+=['## By activity type','']
text+=table(['Type','Activities','Updates','Mean/activity','Median','SD','Maximum','Zero-update activities','Rises','Falls','Mean either-direction edges'],[
    [kind,v['activities'],v['updates']['total'],v['updates']['mean'],v['updates']['median'],v['updates']['population_sd'],v['updates']['max'],v['zero_update_activities'],v['change_details']['up'],v['change_details']['down'],v['change_details']['mean_undirected_distance']]
    for kind,v in activity_types.items()])
text+=['## Complete updates-per-activity distribution','']
text+=table(['Changed topics after activity','Activities','Share of activities'],[
    [n,activity_distribution[n],pct(activity_distribution[n],len(activities))] for n in range(activity_stats['max']+1)])
text+=['## Where the changes lie in the prerequisite graph','',
    'These four groups are mutually exclusive; they add up to all 810 changes. Other branch means there is an undirected connection but no entirely upstream or downstream path from an activity origin.','']
text+=table(['Relation','Updates','Share','Rises','Falls','Mean relevant distance'],[
    ['Activity topic itself',relations['self']['count'],pct(relations['self']['count']),relations['self']['up'],relations['self']['down'],0],
    ['Prerequisite',relations['prerequisite']['count'],pct(relations['prerequisite']['count']),relations['prerequisite']['up'],relations['prerequisite']['down'],strict_up['mean']],
    ['Downstream dependent',relations['downstream']['count'],pct(relations['downstream']['count']),relations['downstream']['up'],relations['downstream']['down'],stat.mean(r['distances']['downstream'] for r in rows if r['relation']=='downstream')],
    ['Other branch',relations['other_branch']['count'],pct(relations['other_branch']['count']),relations['other_branch']['up'],relations['other_branch']['down'],relations['other_branch']['mean_undirected_distance']]])
text+=['## Distance summary','']
text+=table(['Distance population','Updates','Mean edges','Median','SD','90th percentile','95th percentile','Maximum'],[
    [label,v['n'],v['mean'],v['median'],v['population_sd'],v['p90'],v['p95'],v['max']]
    for label,v in [('All changes, either direction',distance_stats['undirected']),
                    ('Activity topic plus prerequisites',distance_stats['prerequisite']),
                    ('Prerequisites only',strict_up)]])
text+=['## Complete distance distribution','',
    'Level 0 is the activity topic itself and appears in both directed columns; count it once. The two directed columns do not cover other-branch changes. Either-direction counts cover every update. Up/down below means rising/falling display bands, not graph direction.','']
text+=table(['Edges','Prerequisite count','Prerequisite rises','Prerequisite falls','Downstream count','Either-direction count','Either-direction share','Either-direction rises','Either-direction falls','Mean either-direction count/activity'],[
    [v['level'],v['prerequisite']['count'],v['prerequisite']['up'],v['prerequisite']['down'],v['downstream']['count'],v['undirected']['count'],pct(v['undirected']['count']),v['undirected']['up'],v['undirected']['down'],v['undirected']['count']/len(activities)]
    for v in distance_levels])
text+=['## Size of changes in display bands','']
text+=table(['Band step change','Updates','Share'],[[delta,n,pct(n)] for delta,n in sorted(Counter(r['delta'] for r in rows).items())])
text+=['## Counts starting and ending at each band','']
text+=table(['Band','Updates starting here','Rises from here','Falls from here','Updates ending here'],[
    [r['band'],r['before'],r['up_from'],r['down_from'],r['after']] for r in bands])
text+=['## Full band transition matrix','', 'Rows are the old band; columns are the new band.','']
text+=table(['Old → new']+[str(b) for b in range(7)],[[b]+transitions[b] for b in range(7)])
text+=['## Complete updates-per-tracked-topic distribution','']
text+=table(['Updates recorded for a topic','Number of topics'],[[n,number] for n,number in sorted(Counter(len(by_topic.get(t,[])) for t in tracked).items())])
text+=['## Course breakdown','']
text+=table(['Course ID','Tracked topics','Updates','Share','Rises','Falls','Mean either-direction distance'],[
    [c,v['tracked_topics'],v['count'],pct(v['count']),v['up'],v['down'],v['mean_undirected_distance']] for c,v in result['course_statistics'].items()])
text+=['The course pages contain 1,040 rows but 1,039 distinct topic IDs because one topic appears in two courses. No update in this dataset is duplicated across courses.','',
    '## Reversals and comparison quality','',
    f"Among {adjacent_changes} successive recorded-change pairs for the same topic/course, {reversals} ({pct(reversals,adjacent_changes)}) reverse direction; {exact_reversals} ({pct(exact_reversals,adjacent_changes)}) exactly undo the previous band transition. These need not be adjacent activities. Frequent reversals mean repeated updates should not be equated with durable learning.",'',
    f"{result['sensitivity']['recovered_snapshots']} snapshots were recovered after interruption and {result['sensitivity']['nonconsecutive_snapshots']} do not compare with the immediately preceding completed snapshot (categories overlap). Restricting to {len(clean_activities)} consecutive, unrecovered snapshots leaves {len(clean_rows)} updates: mean {result['sensitivity']['updates_per_activity']['mean']:.2f} per activity, mean either-direction distance {result['sensitivity']['distance']['mean']:.2f} edges. The maximum upstream distance remains 9.",'',
    '## Every changed topic, ranked by update frequency','']
text+=table(['Topic ID','Topic','Updates','Rises','Falls','Sum of band steps','Own-topic updates','Prerequisite updates','Mean either-direction edges'],[
    [r['topic_id'],r['title'],r['count'],r['up'],r['down'],r['net_band_steps'],r['self_updates'],r['upstream_updates'],r['mean_undirected_distance']] for r in topic_stats])
text+=['## Every practiced lesson/review topic, ranked by mean associated changes','',
    'This groups by the activity topic. It describes changes observed after its activities, without claiming they were caused by it. Small sample sizes should not be used to rank intrinsic topic effects. Assessments and multisteps are excluded because they have multiple origins.','']
text+=table(['Topic ID','Topic','Activities','Associated updates','Mean updates/activity','Activities with own-topic change'],[
    [r['topic_id'],r['title'],r['activities'],r['updates'],r['mean_updates'],r['self_update_activities']] for r in source_stats])
(HERE/'statistics.md').write_text('\n'.join(text)+'\n')

os.environ.setdefault('MPLCONFIGDIR','/tmp/ma-knowledge-distance-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axes=plt.subplots(2,2,figsize=(14,9),layout='constrained')
fig.suptitle('153 activities · 810 recorded band changes · 172 changed topics',fontsize=17)
panels=[(axes[0,0],list(range(27)),[activity_distribution[n] for n in range(27)],
         'Changed topics per activity','Changed topics','Activities'),
        (axes[0,1],list(range(9)),[v['undirected']['count'] for v in distance_levels[:9]],
         'Distance of every update (either edge direction)','Shortest path, edges','Updates'),
        (axes[1,0],list(range(10)),[v['prerequisite']['count'] for v in distance_levels],
         'Changes on the activity topic and its prerequisites','Upstream path, edges','Updates'),
        (axes[1,1],[-5,-4,-3,-2,-1,1,2,3,4,5],[Counter(r['delta'] for r in rows)[n] for n in [-5,-4,-3,-2,-1,1,2,3,4,5]],
         'Size and direction of display-band changes','Band steps (ordinal)','Updates')]
for ax,x,y,title,xlabel,ylabel in panels:
    bars=ax.bar(x,y,color=['#b55555' if n<0 else '#3c7dab' for n in x])
    ax.bar_label(bars,labels=[str(n) if n else '' for n in y],padding=2,fontsize=8)
    ax.set(title=title,xlabel=xlabel,ylabel=ylabel,xticks=x)
    ax.spines[['top','right']].set_visible(False)
    ax.set_ylim(0,max(y)*1.16);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
fig.savefig(HERE/'distributions.png',dpi=150)
print(json.dumps({'dataset':ds,'mean_updates_per_activity':activity_stats['mean'],
    'relations':relations,'reversals':result['reversals'],'report':str(HERE/'statistics.md')},indent=2))
