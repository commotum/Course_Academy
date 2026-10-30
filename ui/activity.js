import { decorateEquationGroups } from './equation-groups.js';
import { decorateSourceTables } from './content-tables.js';
import { attachStepMenu } from './step-menu.js';
import { marked } from './vendor/marked/marked.esm.js';
import { romanLists } from './prose-lists.js';
import { createCoursePicker, topicReferenceURL } from './navigation.js';
import { readRequest } from './requests.js';
import { inlinePrompt, mountInlineFields, checkboxControl, choiceIndicator, fieldFeedback, feedbackHeading, richSelect } from './question-fields.js';

const $ = id => document.getElementById(id);
const detailsCache = new Map();
const rows = new Map();
const dateGroups = new Map();
const weekdayFormat = new Intl.DateTimeFormat('en-US', { weekday: 'long' });
let currentCourseId = null;
let curriculumSnapshot = null;
let nextCursor = null;
let listPending = false;
let mathLoader = null;
let typesetting = Promise.resolve();
const short = value => String(value || '').split('/').at(-1);
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function duration(seconds) {
  if (seconds == null || !Number.isFinite(Number(seconds))) return 'Time unavailable';
  const value = Math.max(0, Math.floor(Number(seconds)));
  return value >= 3600 ? `${Math.floor(value / 3600)}:${String(Math.floor(value / 60) % 60).padStart(2, '0')}:${String(value % 60).padStart(2, '0')}` : `${Math.floor(value / 60)}:${String(value % 60).padStart(2, '0')}`;
}
function timestamp(value, recordedOnly = false) {
  const date = value ? new Date(value) : null;
  if (!date || !Number.isFinite(date.getTime())) return el('span', '', 'Date unavailable');
  const node = el('time', '', (recordedOnly ? 'Recorded ' : '') + new Intl.DateTimeFormat(undefined, { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' }).format(date));
  node.dateTime = date.toISOString(); node.title = date.toLocaleString();
  return node;
}
function activityDateGroup(value, now = new Date()) {
  const date = value == null || value === '' ? null : new Date(value);
  if (!date || !Number.isFinite(date.getTime())) return { key: 'unknown', label: 'Date unavailable', date: null };
  const year = date.getFullYear(), month = String(date.getMonth() + 1).padStart(2, '0'), day = String(date.getDate()).padStart(2, '0');
  // Compare local calendar days, so Yesterday also works across 23/25-hour days.
  const civilDay = date => Date.UTC(date.getFullYear(), date.getMonth(), date.getDate());
  const daysAgo = (civilDay(now) - civilDay(date)) / 86400000;
  const relative = daysAgo === 0 ? 'Today · ' : daysAgo === 1 ? 'Yesterday · ' : '';
  const label = relative + weekdayFormat.format(date) + ' ' + month + '/' + day + (year === now.getFullYear() ? '' : '/' + year);
  return { key: `${year}-${month}-${day}`, label, date };
}
function refreshDateHeadings(now = new Date()) {
  for (const group of dateGroups.values()) group.label.textContent = activityDateGroup(group.date, now).label;
}
function appendActivities(activities, now = new Date()) {
  for (const activity of activities) {
    if (rows.has(activity.taskId)) continue;
    const day = activityDateGroup(activity.completedAt, now);
    let group = dateGroups.get(day.key);
    if (!group) {
      const section = el('section', 'activity-day'); section.dataset.date = day.key;
      const heading = el('h2', 'activity-date-heading'); heading.id = 'activity-day-' + day.key;
      const label = day.date ? el('time', '', day.label) : el('span', '', day.label);
      if (day.date) label.dateTime = day.key;
      heading.append(label); section.append(heading);
      section.setAttribute('aria-labelledby', heading.id);
      group = { section, label, date: day.date };
      dateGroups.set(day.key, group); $('activityList').append(section);
    }
    const row = activityRow(activity); rows.set(activity.taskId, row); group.section.append(row);
  }
  refreshDateHeadings(now);
}
function escapeHTML(text) { return String(text).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]); }
function assetURL(value) {
  if (!value) return '';
  if (String(value).startsWith('/api/asset?')) return value;
  return '/api/asset?path=' + encodeURIComponent(String(value).replace(/^file:\/\//, ''));
}
function fieldLabel(field, index, count = 1) {
  if (field.key === 'selection') return count > 1 ? `Your answer ${index + 1}` : 'Your answer';
  return `Answer ${index + 1}`;
}
function markdown(value, fields = []) {
  const container = el('div', 'prose');
  const math = [];
  const prefix = 'CAMATH' + crypto.randomUUID().replaceAll('-', '') + 'TOKEN';
  const placeholder = /\{\{(?:answer-field:)?([^}]+)\}\}/g;
  const fieldIndex = key => fields.findIndex(field => field.key === key);
  let source = inlinePrompt(value || '', fields).replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g, match => {
    math.push(match.replace(placeholder, (whole, key) => fieldIndex(key) < 0 ? whole : `\\underbrace{\\qquad}_{\\text{answer ${fieldIndex(key) + 1}}}`));
    return prefix + (math.length - 1) + 'END';
  });
  source = source.replace(placeholder, (whole, key) => fieldIndex(key) < 0 ? whole : `<span class="field-location">${escapeHTML(fieldLabel(fields[fieldIndex(key)], fieldIndex(key), fields.length))}</span>`);
  let html = marked.parse(romanLists(source), { async: false, gfm: true, breaks: false });
  html = html.replace(new RegExp(prefix + '(\\d+)END', 'g'), (_, i) => escapeHTML(math[Number(i)]));
  const fragment = DOMPurify.sanitize(html, {
    RETURN_DOM_FRAGMENT: true, USE_PROFILES: { html: true },
    FORBID_TAGS: ['style', 'form', 'input', 'button', 'textarea', 'select', 'iframe', 'object', 'embed', 'video', 'audio'],
    FORBID_ATTR: ['style', 'srcset', 'id', 'name'],
  });
  for (const image of fragment.querySelectorAll('img')) {
    image.src = assetURL(image.getAttribute('src')); image.referrerPolicy = 'no-referrer'; image.loading = 'lazy';
    image.addEventListener('error', () => image.replaceWith(el('span', 'math-error', 'Image unavailable.')), { once: true });
  }
  for (const anchor of fragment.querySelectorAll('a')) {
    const href = anchor.getAttribute('href') || '';
    if (!/^https?:\/\//i.test(href) && !href.startsWith('/api/source?path=')) anchor.removeAttribute('href');
    else { anchor.target = '_blank'; anchor.rel = 'noopener noreferrer'; }
  }
  container.append(fragment);
  decorateEquationGroups(container);
  if (container.querySelector('.source-table')) decorateSourceTables(container);
  if (math.length) container.dataset.math = 'true';
  return container;
}
function answerValue(answer) {
  if (short(answer.type) === 'image') {
    const holder = el('div', 'prose'); const image = el('img');
    image.src = assetURL(answer.value); image.alt = 'Answer option'; image.loading = 'lazy'; holder.append(image); return holder;
  }
  const value = String(answer.value ?? '');
  return markdown(short(answer.type) === 'math' && !/^\s*(\$|\\\[|\\\()/.test(value) ? '$' + value + '$' : value);
}
function savedAnswers(item) {
  const holder = el('div', 'history-answers');
  for (const [index, field] of (item.fields || []).entries()) {
    const set = el('fieldset', 'answer-field');
    set.dataset.type = short(field.type);
    set.append(el('legend', short(field.type) === 'checkbox' ? 'sr-only' : '', fieldLabel(field, index, item.fields.length)));
    if (!field.response) {
      set.append(el('p', 'history-note', item.kind === 'example' ? 'Worked example' : ['paused', 'started', 'skipped'].includes(short(item.status)) ? 'No answer submitted' : 'No saved response'));
    } else {
      const checkbox = checkboxControl(field, label => markdown(label), true, `history-${item.itemId}-${field.id}`);
      if (checkbox) set.append(checkbox);
      else if (short(field.type) === 'radio') {
        const choices = el('div', 'choices');
        for (const choice of field.choices || []) {
          const row = el('label', 'choice'); const input = el('input');
          input.type = 'radio'; input.name = `history-${item.itemId}-${field.id}`; input.value = String(choice.id); input.disabled = true;
          input.checked = String(field.response.choiceId ?? field.response.id) === String(choice.id);
          row.append(choiceIndicator(input), answerValue(choice)); choices.append(row);
        }
        set.append(choices);
      } else if (short(field.type) === 'select') {
        const select = el('select'); select.disabled = true; select.setAttribute('aria-label', fieldLabel(field, index, item.fields.length));
        for (const choice of field.choices || []) {
          const option = el('option', '', choice.value); option.value = String(choice.id); select.append(option);
        }
        select.value = String(field.response.choiceId ?? field.response.id);
        set.append(richSelect(select, field.choices || [], answerValue));
      } else if (short(field.type) === 'blank') {
        const value = el('span', 'answer-saved-value'); value.append(answerValue(field.response)); set.append(value);
      } else set.append(answerValue(field.response));
    }
    fieldFeedback(set, field, item.status);
    holder.append(set);
  }
  return holder;
}
function loadMath() {
  if (window.MathJax?.startup?.promise) return MathJax.startup.promise;
  if (!mathLoader) mathLoader = new Promise((resolve, reject) => {
    const script = document.createElement('script'); script.src = '/ui/vendor/mathjax/tex-svg.js'; script.async = true;
    script.onload = () => window.MathJax?.startup?.promise ? MathJax.startup.promise.then(resolve, reject) : reject(new Error('Math rendering could not start.'));
    script.onerror = () => { script.remove(); reject(new Error('Math rendering could not load.')); };
    document.head.append(script);
  }).catch(error => { mathLoader = null; throw error; });
  return mathLoader;
}
function typeset(host) {
  if (!host.querySelector('[data-math]')) return Promise.resolve();
  typesetting = typesetting.catch(() => {}).then(async () => {
    if (!host.isConnected) return;
    await loadMath();
    if (host.isConnected) await MathJax.typesetPromise([host]);
  }).catch(() => {
    if (host.isConnected && !host.querySelector('.math-error')) host.append(el('p', 'math-error', 'Math notation could not be rendered. Refresh the page to try again.'));
  });
  return typesetting;
}
function resultLabel(item) {
  const state = short(item.status);
  return ({ correct: 'Correct', incorrect: 'Incorrect', skipped: 'Skipped', paused: 'Not submitted', started: 'Not submitted', completed: item.kind === 'question' ? 'Completed' : 'Viewed' })[state] || 'Not submitted';
}
function renderItem(item, number) {
  const card = el('article', 'history-question');
  attachStepMenu(card, item.contentId, item.mathAcademyId, { kind: item.kind === 'tutorial' ? 'tutorial' : 'question' });
  const heading = el('h3', 'history-question-title', item.kind === 'question' ? `Question ${number}` : item.title || 'Worked example');
  if (item.kind === 'question' && item.topic?.title) {
    heading.append(el('span', 'history-question-topic', item.topic.title));
  }
  card.append(heading);
  const prompt = markdown(item.markdown, item.fields); card.append(prompt);
  if (item.fields?.length) {
    const answers = savedAnswers(item), controls = [...answers.children];
    mountInlineFields(prompt, answers, item.fields, field => controls[item.fields.indexOf(field)]);
    if (!answers.hidden) card.append(answers);
  }
  const footer = el('div', 'history-item-meta');
  if (item.difficulty) {
    const difficulty = short(item.difficulty); const label = difficulty[0].toUpperCase() + difficulty.slice(1);
    const badge = el('span', `difficulty ${difficulty}`, difficulty[0].toUpperCase()); badge.title = label; badge.setAttribute('aria-label', `Difficulty: ${label}`);
    footer.append(badge, el('span', 'difficulty-name', label));
  } else if (item.kind === 'question') footer.append(el('span', 'history-note', 'Difficulty unavailable'));
  footer.append(timestamp(item.answeredAt, item.recordedOnly), el('span', '', `Elapsed: ${duration(item.elapsedSeconds)}`));
  const label = resultLabel(item);
  if (['correct', 'incorrect'].includes(short(item.status)) || (item.kind === 'question' && label === 'Not submitted')) {
    const result = feedbackHeading(short(item.status) === 'correct' ? 'correct' : 'incorrect');
    result.children[0].textContent = label;
    result.className = 'history-result'; footer.append(result);
  } else footer.append(el('span', 'history-result', label));
  const solution = el('details', 'history-solution');
  const hasSolution = Boolean(item.solution || item.fields?.some(field => field.correctAnswer || field.response?.feedback));
  if (hasSolution) {
    const summary = el('summary'); summary.append(footer, el('span', 'solution-toggle', 'Explanation')); solution.append(summary);
    let built = false;
    solution.addEventListener('toggle', () => {
      if (!solution.open) return;
      if (!built) {
        built = true;
        const body = el('div', 'history-explanation');
        for (const [index, field] of (item.fields || []).entries()) {
          if (field.correctAnswer && item.kind !== 'tutorial') {
            body.append(el('p', 'history-answer-label', `Correct ${item.fields.length > 1 ? `answer ${index + 1}` : 'answer'}`), answerValue(field.correctAnswer));
          }
          if (field.response?.feedback) body.append(markdown(field.response.feedback));
        }
        if (item.solution) body.append(el('h4', '', 'Worked solution'), markdown(item.solution));
        solution.append(body);
      }
      void typeset(solution);
    });
    card.append(solution);
  } else card.append(footer);
  return card;
}
function renderDetails(host, data) {
  host.replaceChildren();
  let group = null; let questionNumber = 0;
  for (const item of data.items) {
    if (item.group && item.group !== group) {
      group = item.group;
      const heading = el('h2', 'history-group', group);
      if (item.knowledgePoint) attachStepMenu(heading, item.knowledgePoint.id, item.knowledgePoint.mathAcademyId, { kind: 'knowledge point' });
      host.append(heading);
    }
    if (item.kind === 'question') questionNumber++;
    if (item.kind === 'tutorial' || item.kind === 'example') {
      const details = el('details', 'history-instruction');
      attachStepMenu(details, item.contentId, item.mathAcademyId, { kind: item.kind === 'tutorial' ? 'tutorial' : 'question' });
      details.append(el('summary', '', item.title || 'Worked example'));
      let built = false;
      details.addEventListener('toggle', () => {
        if (!details.open) return;
        if (!built) { built = true; details.append(renderItem(item, questionNumber)); }
        void typeset(details);
      });
      host.append(details);
    } else host.append(renderItem(item, questionNumber));
  }
  if (!data.items.length) host.append(el('p', 'history-note', 'No item details were recorded for this activity.'));
  void typeset(host);
}
async function api(path) {
  const response = await readRequest(path);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Unable to load activity.');
  return data;
}
function detailRequest(taskId) {
  if (!detailsCache.has(taskId)) {
    const request = api('/api/activity?taskId=' + encodeURIComponent(taskId)).then(data => {
      if (!Array.isArray(data.items)) throw new Error('Activity details are unavailable.');
      return data;
    }).catch(error => { detailsCache.delete(taskId); throw error; });
    detailsCache.set(taskId, request);
  }
  return detailsCache.get(taskId);
}
function activityRow(activity) {
  const row = el('details', 'activity-row');
  attachStepMenu(row, activity.activityId, null, { kind: 'activity' });
  row.dataset.taskId = String(activity.taskId);
  const summary = el('summary', 'activity-summary');
  const header = el('div', 'activity-summary-title');
  header.append(el('span', 'eyebrow', short(activity.type)), el('h3', '', activity.title || 'Untitled activity'));
  const meta = el('div', 'activity-summary-meta');
  meta.append(timestamp(activity.completedAt, activity.recordedOnly), el('span', '', `Elapsed: ${duration(activity.elapsedSeconds)}`));
  if (activity.questionCount) meta.append(el('span', '', `${activity.correctCount}/${activity.questionCount} correct`));
  if (activity.courseTitle) meta.append(el('span', '', activity.courseTitle));
  if (activity.status === 'failed') meta.append(el('span', 'history-result incorrect', 'Failed'));
  header.append(meta);
  const xp = el('span', 'activity-xp', activity.xp == null ? 'XP unavailable' : `${activity.xp}${activity.xpBase == null ? '' : '/' + activity.xpBase} XP`);
  summary.append(header, xp, el('span', 'activity-chevron', '⌄')); row.append(summary);
  const host = el('div', 'activity-items'); row.append(host);
  let loaded = false; let pending = false;
  async function expand() {
    if (loaded || pending) return;
    pending = true; host.setAttribute('aria-busy', 'true'); host.replaceChildren(el('p', 'history-note', 'Loading activity details…'));
    try {
      const data = await detailRequest(activity.taskId);
      if (!Array.isArray(data.items)) throw new Error('Activity details are unavailable.');
      renderDetails(host, data); loaded = true;
    } catch (error) {
      const retry = el('button', 'small-button', 'Try again'); retry.type = 'button'; retry.addEventListener('click', () => void expand());
      const message = el('p', 'history-note', error.message); message.setAttribute('role', 'alert'); host.replaceChildren(message, retry);
    } finally { pending = false; host.setAttribute('aria-busy', 'false'); }
  }
  row.addEventListener('toggle', () => { if (row.open) void expand(); });
  return row;
}
function updateHeader(data) {
  if (data.learner) $('learnerName').textContent = data.learner.name || 'Profile';
  if (data.course?.id) {
    currentCourseId = data.course.id; $('courseLink').href = '/progress?course=' + encodeURIComponent(currentCourseId);
    try { sessionStorage.setItem('course-academy.study-header', JSON.stringify({courseId: currentCourseId, learnerName: $('learnerName').textContent})); } catch { /* Header is also populated by the response. */ }
  }
}
async function load({ more = false } = {}) {
  if (listPending) return;
  listPending = true; $('main').setAttribute('aria-busy', 'true'); $('errorBanner').hidden = true;
  $('loadMore')?.setAttribute('disabled', '');
  try {
    const data = await api('/api/activity' + (more && nextCursor ? '?beforeTaskId=' + encodeURIComponent(nextCursor) : ''));
    if (!Array.isArray(data.activities)) throw new Error('Activity history is unavailable.');
    updateHeader(data);
    if (!more) {
      rows.clear(); dateGroups.clear(); $('main').replaceChildren();
      const heading = el('div', 'page-heading'); const titles = el('div');
      titles.append(el('h1', '', 'Activity'), el('p', 'history-note', 'Your completed lessons, reviews, assessments, and assignments.'));
      heading.append(titles); $('main').append(heading);
      const list = el('section', 'activity-list'); list.id = 'activityList'; list.setAttribute('aria-label', 'Completed activities'); $('main').append(list);
      const moreButton = el('button', 'small-button activity-more', 'Load more'); moreButton.id = 'loadMore'; moreButton.type = 'button'; moreButton.addEventListener('click', () => void load({more:true})); $('main').append(moreButton);
    }
    appendActivities(data.activities);
    if (!rows.size) $('activityList').append(el('p', 'empty-state', 'No completed activities yet. Your finished work will appear here.'));
    nextCursor = data.nextCursor;
    $('loadMore').hidden = !nextCursor;
    $('announcement').textContent = `${data.total} completed ${data.total === 1 ? 'activity' : 'activities'}`;
  } catch (error) {
    if (!$('activityList')) $('main').replaceChildren(el('p', 'history-note', 'Activity history could not be loaded.'))
    $('errorText').textContent = error.message; $('errorBanner').hidden = false;
    $('retryButton').onclick = () => void load({more});
  } finally { listPending = false; $('main').setAttribute('aria-busy', 'false'); $('loadMore')?.removeAttribute('disabled'); }
}
createCoursePicker({
  getSnapshot: async () => {
    if (!curriculumSnapshot) curriculumSnapshot = api('/api/graph-explorer').catch(error => { curriculumSnapshot = null; throw error; });
    return curriculumSnapshot;
  },
  getCourseId: () => currentCourseId,
  onSelectCourse: course => { location.href = '/progress?course=' + encodeURIComponent(course.id); },
  onSelectTopic: async topic => { location.href = topicReferenceURL(await curriculumSnapshot, topic, currentCourseId); },
});
window.addEventListener('course-academy:profile-changed', () => { curriculumSnapshot = null; void load(); });
window.addEventListener('focus', () => refreshDateHeadings());
document.addEventListener('visibilitychange', () => { if (!document.hidden) refreshDateHeadings(); });
void load();
