import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const source = await readFile(new URL('../ui/activity.js', import.meta.url), 'utf8');
const code = source.slice(source.indexOf('const $'), source.indexOf('createCoursePicker({'));
const fieldUI = (await readFile(new URL('../ui/question-fields.js', import.meta.url), 'utf8')).replace(/^[\s\S]*?(?=\/\/ Shared presentation)/, '').replaceAll('export ', '');
function fixture() {
  const calls = []; let fail = false; let malformed = false; let pages = [];
  class Element extends EventTarget {
    constructor(tag) { super(); this.tagName = tag; this.children = []; this.attrs = {}; this.dataset = {}; this.className = ''; this.text = ''; }
    append(...nodes) { this.children.push(...nodes); }
    replaceChildren(...nodes) { this.children = nodes; }
    get textContent() { return this.text + this.children.map(n => n.textContent || '').join(' '); }
    set textContent(value) { this.text = String(value); this.children = []; }
    setAttribute(key, value) { this.attrs[key] = value; }
    removeAttribute(key) { delete this.attrs[key]; }
    querySelector() { return null; }
    get isConnected() { return true; }
  }
  const elements = new Map(['main', 'errorBanner', 'errorText', 'retryButton', 'announcement', 'learnerName', 'courseLink'].map(id => [id, new Element('div')]));
  const document = {createElement: tag => new Element(tag), getElementById(id) {
    const find = node => node.id === id ? node : node.children.map(find).find(Boolean);
    return find(elements.get('main')) || elements.get(id) || null;
  }};
  const context = vm.createContext({ document, window: {}, Intl, Date, Number, Map, String, Promise,
    readRequest: async path => { calls.push(path); return {ok: !fail, json: async () => fail ? {error:'Try later'} : malformed ? {} : path.includes('taskId=') ? {items:[], activity:{taskId:10}} : pages.shift()}; },
    checkboxControl: () => null,
    attachStepMenu: (node, id, ma, options = {}) => { node.dataset.stepDbId = id; node.dataset.mathAcademyId = ma; node.dataset.contentKind = options.kind; },
  });
  vm.runInContext(fieldUI + '\n' + code, context);
  return {context, calls, document, setPages(value) {pages=value;}, setFail(value) {fail=value;}, setMalformed(value) {malformed=value;}, run: code => vm.runInContext(code, context)};
}
const flush = () => new Promise(resolve => setImmediate(resolve));

test('activity rows defer loading, reuse an expanded history, and make no mutations', async () => {
  const f=fixture();
  const row=f.run('activityRow({taskId:10,title:"Calculus",type:"lesson",xp:8,xpBase:10,elapsedSeconds:61,questionCount:2,correctCount:1})');
  assert.equal(f.calls.length,0);
  row.open=true; row.dispatchEvent(new Event('toggle')); await flush();
  assert.deepEqual(f.calls,['/api/activity?taskId=10']);
  assert.match(row.textContent,/8\/10 XP/); assert.match(row.textContent,/1\/2 correct/);
  assert.match(row.textContent,/Elapsed: 1:01/);
  row.open=false; row.dispatchEvent(new Event('toggle')); row.open=true; row.dispatchEvent(new Event('toggle')); await flush();
  assert.equal(f.calls.length,1);
});
test('concurrent expansions coalesce and rejected requests can be retried', async () => {
  const f=fixture();
  await Promise.all([f.run('detailRequest(10)'),f.run('detailRequest(10)')]); assert.equal(f.calls.length,1);
  f.setFail(true); await assert.rejects(f.run('detailRequest(11)'),/Try later/);
  f.setFail(false); await f.run('detailRequest(11)'); assert.equal(f.calls.length,3);
});
test('malformed responses do not poison the detail cache', async () => {
  const f=fixture(); f.setMalformed(true); await assert.rejects(f.run('detailRequest(10)'),/unavailable/);
  f.setMalformed(false); await f.run('detailRequest(10)'); assert.equal(f.calls.length,2);
});
test('missing recorded data is distinguished from zero time and incorrect answers', () => {
  const f=fixture(); assert.equal(f.run('duration(null)'),'Time unavailable'); assert.equal(f.run('duration(0)'),'0:00'); assert.equal(f.run('duration(3661)'),'1:01:01');
  assert.equal(f.run('timestamp(null).textContent'),'Date unavailable');
  assert.equal(f.run('resultLabel({status:"paused",kind:"question"})'),'Not submitted');
  assert.equal(f.run('resultLabel({status:"incorrect",kind:"question"})'),'Incorrect');
});

test('history cards and group headings identify their displayed entities rather than presentations', () => {
  const f = fixture();
  f.run("markdown = value => el('div', 'prose', value || '')");
  const card = f.run('renderItem({itemId:101,stepId:202,contentId:303,mathAcademyId:"q-123",kind:"question",fields:[],status:"correct"},1)');
  assert.equal(card.dataset.stepDbId, 303);
  assert.equal(card.dataset.mathAcademyId, 'q-123');
  assert.equal(card.dataset.contentKind, 'question');
  const host = f.run("el('div')"); f.context.host = host;
  f.run('renderDetails(host,{items:[{itemId:101,stepId:202,contentId:303,kind:"example",title:"Skill",group:"Skill",knowledgePoint:{id:404},fields:[]}]})');
  assert.equal(host.children[0].dataset.stepDbId, 404);
  assert.equal(host.children[0].dataset.contentKind, 'knowledge point');
  assert.equal(host.children[1].dataset.stepDbId, 303);
  const row = f.run('activityRow({taskId:101,activityId:505,title:"Lesson"})');
  assert.equal(row.dataset.stepDbId, 505);
});

test('quiz question headings show their own topic without changing question numbering', () => {
  const f = fixture();
  f.run("markdown = value => el('div', 'prose', value || '')");
  const first = f.run('renderItem({contentId:303,kind:"question",fields:[],status:"correct",topic:{id:40,title:"Linear equations"}},1)');
  const second = f.run('renderItem({contentId:304,kind:"question",fields:[],status:"incorrect",topic:{id:43,title:"Fractions"}},2)');
  assert.match(first.children[0].textContent, /Question 1.*Topic: Linear equations/);
  assert.match(second.children[0].textContent, /Question 2.*Topic: Fractions/);
  assert.equal(first.children[0].children[0].className, 'history-question-topic');
  const lesson = f.run('renderItem({contentId:305,kind:"question",fields:[],status:"correct"},3)');
  assert.equal(lesson.children[0].textContent, 'Question 3');
});

test('activity date headings include Today, Yesterday, weekday and padded dates, with years when needed', () => {
  const f = fixture();
  assert.equal(f.run('activityDateGroup(new Date(2026,9,17,9),new Date(2026,9,17,18)).label'), 'Today · Saturday 10/17');
  assert.equal(f.run('activityDateGroup(new Date(2026,9,16,23),new Date(2026,9,17,18)).label'), 'Yesterday · Friday 10/16');
  assert.equal(f.run('activityDateGroup(new Date(2026,9,15),new Date(2026,9,17)).label'), 'Thursday 10/15');
  assert.equal(f.run('activityDateGroup(new Date(2026,0,2),new Date(2026,9,17)).label'), 'Friday 01/02');
  assert.equal(f.run('activityDateGroup(new Date(2025,11,31),new Date(2026,0,1)).label'), 'Yesterday · Wednesday 12/31/2025');
  for (const value of ['null', 'undefined', '""', '"invalid"']) {
    assert.equal(f.run(`activityDateGroup(${value}).label`), 'Date unavailable');
  }
});

test('grouping uses local completion days and handles daylight saving boundaries', () => {
  const previousTZ = process.env.TZ;
  process.env.TZ = 'America/Los_Angeles';
  try {
    const f = fixture();
    assert.equal(f.run('activityDateGroup("2026-10-18T06:30:00Z",new Date("2026-10-18T07:30:00Z")).label'), 'Yesterday · Saturday 10/17');
    assert.equal(f.run('activityDateGroup("2026-10-18T07:01:00Z",new Date("2026-10-18T07:30:00Z")).label'), 'Today · Sunday 10/18');
    assert.equal(f.run('activityDateGroup(new Date(2026,10,1,0,10),new Date(2026,10,2,0,10)).label'), 'Yesterday · Sunday 11/01');
    assert.equal(f.run('activityDateGroup(new Date(2026,2,8,0,10),new Date(2026,2,9,0,10)).label'), 'Yesterday · Sunday 03/08');
  } finally {
    if (previousTZ === undefined) delete process.env.TZ;
    else process.env.TZ = previousTZ;
  }
});

test('pagination merges same-day entries, preserves expanded rows, and resets groups on reload', async () => {
  const f = fixture();
  const activity = (taskId, completedAt) => ({ taskId, completedAt, activityId: taskId + 100, title: `Lesson ${taskId}` });
  f.setPages([
    { activities: [activity(10, '2026-10-17T12:00:00Z'), activity(11, '2026-10-16T12:00:00Z')], total: 4, nextCursor: 11 },
    { activities: [activity(11, '2026-10-16T12:00:00Z'), activity(12, '2026-10-16T10:00:00Z'), activity(13, '2026-10-15T12:00:00Z')], total: 4, nextCursor: null },
    { activities: [activity(14, '2026-10-17T12:00:00Z')], total: 1, nextCursor: null },
  ]);
  await f.run('load()');
  const list = f.document.getElementById('activityList');
  assert.equal(list.children.length, 2);
  const row = list.children[1].children[1]; row.open = true;
  await f.run('load({more:true})');
  assert.equal(list.children.length, 3);
  assert.deepEqual(list.children.map(group => group.children.length - 1), [1, 2, 1]);
  assert.equal(list.children[1].children[1], row);
  assert.equal(row.open, true);
  assert.equal(list.children[0].children[0].tagName, 'h2');
  assert.equal(row.children[0].children[0].children[1].tagName, 'h3');
  assert.deepEqual(f.calls, ['/api/activity', '/api/activity?beforeTaskId=11']);
  assert.equal(f.document.getElementById('loadMore').hidden, true);
  await f.run('load()');
  const reloaded = f.document.getElementById('activityList');
  assert.equal(reloaded.children.length, 1);
  assert.equal(reloaded.children[0].children[1].dataset.taskId, '14');
});

test('unknown dates share a group and relative headings refresh without fetching or replacing rows', () => {
  const f = fixture();
  f.run("const list=el('section');list.id='activityList';$('main').append(list)");
  f.run('appendActivities([{taskId:1,completedAt:new Date(2026,9,17,12)},{taskId:2},{taskId:3,completedAt:"invalid"}],new Date(2026,9,17,18))');
  const list = f.document.getElementById('activityList');
  assert.equal(list.children.length, 2);
  assert.equal(list.children[0].children[0].textContent, 'Today · Saturday 10/17');
  assert.equal(list.children[1].children[0].textContent, 'Date unavailable');
  assert.equal(list.children[1].children.length, 3);
  const row = list.children[0].children[1];
  f.run('refreshDateHeadings(new Date(2026,9,18,1))');
  assert.equal(list.children[0].children[0].textContent, 'Yesterday · Saturday 10/17');
  assert.equal(list.children[0].children[1], row);
  assert.equal(f.calls.length, 0);
});
