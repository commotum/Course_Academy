// Forecast-owned projection of the Targets selection and course placement rules.
// The graph page keeps its own implementation, independent of this module.
import { buildTargetCalendar, filterScheduledTargets } from './target-weeks.js';

export const TARGET_COURSE_CODES = ['255','256','341'];

export function indexTargetGraph(data) {
  const nodes=data.nodes.map(n=>({...n,layer:0,order:0}));
  const nodeById=new Map(nodes.map(n=>[n.id,n]));
  const outMap=new Map(nodes.map(n=>[n.id,[]])),inMap=new Map(nodes.map(n=>[n.id,[]]));
  for(const edge of data.links) {
    if(!nodeById.has(edge.source)||!nodeById.has(edge.target))throw new Error('A prerequisite refers to a missing topic.');
    outMap.get(edge.source).push(edge.target);inMap.get(edge.target).push(edge.source);
  }
  const remaining=new Map(nodes.map(n=>[n.id,inMap.get(n.id).length]));
  const order=nodes.filter(n=>remaining.get(n.id)===0).sort((a,b)=>a.name.localeCompare(b.name)).map(n=>n.id);
  for(let i=0;i<order.length;i++) {
    const node=nodeById.get(order[i]);
    for(const id of outMap.get(node.id)) {
      nodeById.get(id).layer=Math.max(nodeById.get(id).layer,node.layer+1);
      remaining.set(id,remaining.get(id)-1);
      if(remaining.get(id)===0)order.push(id);
    }
  }
  if(order.length!==nodes.length)throw new Error('The prerequisite graph contains a cycle.');
  return {nodes,nodeById,outMap,inMap,order};
}

export function targetSelectors(snapshot, graph, options = {}, calendar = null) {
  const {nodeById}=graph, targetCourseCodes=TARGET_COURSE_CODES;
  const targetTopicVisible=id=>nodeById.get(id)?.layer>=29;
  const enabledTargetCourses=new Set(options.courses ?? targetCourseCodes);
  const targetQueueEnabled=options.includeQueue!==false;
  const targetCalendar=calendar ?? buildTargetCalendar(snapshot?.targetSchedule || []);
  // Absolute week ranges stay fixed during historical reconstruction, even if
  // a past calendar did not yet contain the selected week.
  const targetWeekSelection=options.weekSelection ?? {kind:'all'};
  function unassignedTargetIds() {
    const assigned=new Set();
    for(const course of snapshot?.courses || []){
      for(const id of [...(course.topicIds || []),...(course.targetTopicIds || [])])assigned.add(id);
    }
    for(const assignment of targetCalendar.assignments){
      for(const id of assignment.topicIds)assigned.add(id);
    }
    return [...new Set(snapshot?.learner.targets || [])].filter(id=>targetTopicVisible(id) && !assigned.has(id));
  }
  function courseFilteredTargetIds(includeQueue=targetQueueEnabled) {
    const targets=(snapshot?.learner.targets || []).filter(targetTopicVisible);
    // Targets without any course or assignment remain visible in every scope.
    const unassigned=new Set(unassignedTargetIds());
    const members=new Set();
    if(enabledTargetCourses.size!==targetCourseCodes.length){
      for(const course of snapshot?.courses || []){
        if(!targetCourseCodes.some(code=>course.code==='MTH '+code && enabledTargetCourses.has(code)))continue;
        for(const id of course.topicIds || [])members.add(id);
        for(const id of course.targetTopicIds || [])members.add(id);
      }
    }
    const selected=enabledTargetCourses.size===targetCourseCodes.length?targets:targets.filter(id=>members.has(id) || unassigned.has(id));
    // Queue is an independent source, including topics outside enabled courses.
    return includeQueue?[...new Set([...selected,...queuedGraphTopicIds()])]:selected;
  }
  function queuedGraphTopicIds() {
    return [...new Set(snapshot?.learner.queue || [])].filter(targetTopicVisible);
  }
  function targetWeekCourseIds() {
    if(enabledTargetCourses.size===targetCourseCodes.length)return null;
    return new Set((snapshot?.courses || []).filter(course=>
      targetCourseCodes.some(code=>course.code==='MTH '+code && enabledTargetCourses.has(code))).map(course=>course.id));
  }
  function targetWeekScope() {
    return {targets:courseFilteredTargetIds(false),unassigned:unassignedTargetIds(),queue:targetQueueEnabled?queuedGraphTopicIds():[],courses:targetWeekCourseIds()};
  }
  function weekFilteredTargetIds(selection, scope) {
    return filterScheduledTargets(scope.targets,targetCalendar,selection,scope.courses);
  }
  function targetIdsForWeek(selection, scope=targetWeekScope()) {
    const targets=weekFilteredTargetIds(selection,scope);
    // Unassigned targets and Queue are standing lists outside assignment weeks.
    return [...new Set([...targets,...scope.unassigned,...scope.queue])];
  }
  return {unassignedTargetIds,courseFilteredTargetIds,queuedGraphTopicIds,targetWeekCourseIds,
    targetWeekScope,targetIdsForWeek,roots:()=>targetIdsForWeek(targetWeekSelection)};

}

export function assignTargetCourses(snapshot, graph, targetCalendar, nodeIds) {
    const {nodeById,inMap,outMap}=graph;
    const targetCourseCodes=TARGET_COURSE_CODES;
    const targetTopicVisible=id=>nodeById.get(id)?.layer>=29;
    const courses=targetCourseCodes.map(code=>({key:code,label:'MTH '+code,nodeIds:new Set()}));
    const direct=new Map(), placement=new Map(), workload=new Map(courses.map(course=>[course.key,0]));
    const addMembership=(id,code)=>{
      if(!nodeById.has(id))return;
      if(!direct.has(id))direct.set(id,new Set());
      direct.get(id).add(code);
    };
    for(const course of snapshot?.courses || []){
      const band=courses.find(band=>band.label===course.code);
      if(!band)continue;
      for(const id of [...(course.topicIds || []),...(course.targetTopicIds || [])])addMembership(id,band.key);
      for(const assignment of targetCalendar.assignments){
        if(assignment.courseId===course.id)for(const id of assignment.topicIds)addMembership(id,band.key);
      }
    }
    for(const [id,membership] of direct)if(membership.size===1)placement.set(id,[...membership][0]);
    // Full-graph distances include hidden prerequisites and dependents. Filters
    // control visibility; depth never changes course placement or workload.
    const courseDistances=anchors=>new Map(courses.map(course=>{
      const pending=[...anchors].filter(([,code])=>code===course.key).map(([id])=>id);
      const distances=new Map(pending.map(id=>[id,0]));
      for(let i=0;i<pending.length;i++){
        const id=pending[i], nextDistance=distances.get(id)+1;
        for(const next of [...(inMap.get(id) || []),...(outMap.get(id) || [])]){
          if(!distances.has(next)){distances.set(next,nextDistance);pending.push(next);}
        }
      }
      return [course.key,distances];
    }));
    const closestCourses=(id,distances)=>{
      const candidates=direct.has(id)?[...direct.get(id)]:courses.map(course=>course.key);
      const nearest=Math.min(...candidates.map(code=>distances.get(code).get(id) ?? Infinity));
      return candidates.filter(code=>(distances.get(code).get(id) ?? Infinity)===nearest);
    };
    const lightest=candidates=>courses.filter(course=>candidates.includes(course.key))
      .reduce((best,course)=>best===null || workload.get(course.key)<workload.get(best)?course.key:best,null);
    // Count each saved target/queue topic once, including hidden roots, so week
    // filters and focused exploration cannot move an already placed topic.
    const roots=[...new Set([...(snapshot?.learner.targets || []),...(snapshot?.learner.queue || [])])]
      .filter(targetTopicVisible).sort((a,b)=>a-b);
    const countRoot=(id,code)=>{placement.set(id,code);workload.set(code,workload.get(code)+1);};
    for(const id of roots)if(placement.has(id))countRoot(id,placement.get(id));
    const distances=courseDistances(placement), tied=[];
    for(const id of roots){
      if(placement.has(id))continue;
      const candidates=closestCourses(id,distances);
      if(candidates.length===1)countRoot(id,candidates[0]);else tied.push({id,candidates});
    }
    for(const {id,candidates} of tied)countRoot(id,lightest(candidates));
    // Placed roots also anchor their prerequisites, including components with
    // no original course association. Extra prerequisites do not add workload.
    const expandedDistances=courseDistances(placement);
    const byCode=new Map(courses.map(course=>[course.key,course]));
    for(const id of [...nodeIds].sort((a,b)=>a-b)){
      const code=placement.get(id) ?? lightest(closestCourses(id,expandedDistances));
      byCode.get(code).nodeIds.add(id);
    }
    return courses.filter(course=>course.nodeIds.size);
  }

export function projectTargetScope(snapshot, options = {}, graph = indexTargetGraph(snapshot)) {
  const calendar=buildTargetCalendar(snapshot.targetSchedule || []);
  const selectors=targetSelectors(snapshot,graph,options,calendar);
  const roots=selectors.roots(),distances=new Map(roots.map(id=>[id,0])),pending=[...roots];
  const depth=options.prerequisiteDepth ?? snapshot.studyDefaults?.targetPrerequisiteDepth ?? 2;
  for(let i=0;i<pending.length;i++) {
    const id=pending[i],d=distances.get(id);
    if(d>=depth)continue;
    for(const next of graph.inMap.get(id) || []) {
      if(!distances.has(next)&&graph.nodeById.get(next)?.layer>=29){distances.set(next,d+1);pending.push(next);}
    }
  }
  const nodeIds=new Set(distances.keys());
  const courses=assignTargetCourses(snapshot,graph,calendar,nodeIds);
  const tracks=new Map(courses.flatMap(c=>[...c.nodeIds].map(id=>[id,c.key])));
  const targets=new Set(snapshot.learner?.targets || []),queue=new Set(snapshot.learner?.queue || []);
  const categories=new Map([...nodeIds].map(id=>[id,targets.has(id)?'target':queue.has(id)?'queue':'prerequisite']));
  return {graph,roots:new Set(roots),nodeIds,tracks,courses,categories};
}
