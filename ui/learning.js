import { marked } from './vendor/marked/marked.esm.js';
import { createCoursePicker } from './navigation.js';

const $ = id => document.getElementById(id);
const terminal = status => ['completed', 'failed'].includes(status);
const answered = status => ['correct', 'incorrect', 'skipped'].includes(status);
let task = null;
let busy = false;
let retryOperation = null;
let renderGeneration = 0;
let clock = { at: Date.now(), elapsed: 0, running: false };
let typesetting = Promise.resolve();
let mathLoader = null;
const drafts = new Map();
let pendingPause = null;
let refreshAfterVisibility = false;
let currentCourseId = null;
let curriculumSnapshot = null;

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function button(text, className, action) {
  const node = el('button', className, text);
  node.type = 'button';
  node.addEventListener('click', action);
  return node;
}
function short(value) { return String(value || '').split('/').at(-1); }
function fieldLabel(key) {
  if (!key || key === 'selection') return 'Answer';
  const numbered = /^field-(\d+)$/.exec(key);
  return numbered ? `Answer ${numbered[1]}` : `Answer: ${key}`;
}
function announce(text) { $('announcement').textContent = text; }
function showError(error, retry) {
  $('errorText').textContent = error.message || String(error);
  $('errorBanner').hidden = false;
  retryOperation = retry;
  $('retryButton').hidden = !retry;
}
function clearError() { $('errorBanner').hidden = true; retryOperation = null; }
function duration(seconds) {
  const n = Math.max(0, Math.floor(Number(seconds) || 0));
  return `${Math.floor(n / 60)}:${String(n % 60).padStart(2, '0')}`;
}
function levelName(level) {
  return { 'early-math': 'Early Math', 'high-school-math': 'High School Math', 'university-math': 'University Math' }[short(level)] || '';
}
function updateHeader(data) {
  if (data.learner?.name) $('learnerName').textContent = data.learner.name;
  if (data.course) {
    currentCourseId = data.course.id;
    $('courseTitle').textContent = data.course.title;
    $('courseLevel').textContent = levelName(data.course.level) || 'Your current course';
    $('graphLink').href = '/?course=' + encodeURIComponent(data.course.id);
    $('courseLink').href = '/course?course=' + encodeURIComponent(data.course.id);
  }
}
async function api(path, body, options = {}) {
  const response = await fetch(path, {
    method: body ? 'POST' : 'GET',
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
    cache: 'no-store',
    ...options,
  });
  let result;
  try { result = await response.json(); } catch { throw new Error('The study server did not return a response. Check that it is running, then try again.'); }
  if (!response.ok || result.error) {
    const error = new Error(result.error || `The request failed (${response.status}).`);
    error.code = result.code; error.status = response.status;
    throw error;
  }
  return result;
}
function setBusy(value) {
  busy = value;
  $('main').setAttribute('aria-busy', String(value));
  for (const control of document.querySelectorAll('[data-action]')) {
    control.disabled = value || control.dataset.unavailable === 'true';
  }
  for (const control of document.querySelectorAll('[data-answer-input]')) {
    control.disabled = value || control.dataset.readOnly === 'true';
  }
}
function actionButton(text, className, action, enabled = true) {
  const node = button(text, className, action);
  node.dataset.action = 'true';
  node.dataset.unavailable = String(!enabled);
  node.disabled = busy || !enabled;
  return node;
}
async function mutation(path, values) {
  if (busy) return;
  if (path === '/api/start') void loadMath().catch(() => {});
  const body = { ...values, requestId: crypto.randomUUID() };
  const run = async () => {
    clearError();
    setBusy(true);
    try {
      const result = await api(path, body);
      task = result.task || result;
      history.replaceState(null, '', '/learn?taskId=' + encodeURIComponent(task.taskId));
      await renderTask(task);
      announce(answered(task.step?.status) ? (task.step.status === 'correct' ? 'Correct.' : 'Answer recorded.') : task.step?.title || 'Progress saved.');
    } catch (error) {
      // Only a confirmed rejection may get a fresh request identity. An uncertain
      // network failure must replay the original request to avoid duplicate credit.
      if (error.code === 'basis-conflict') body.requestId = crypto.randomUUID();
      showError(error, run);
    } finally { setBusy(false); void syncAfterVisibility(); }
  };
  await run();
}

function escapeHTML(text) { return String(text).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]); }
function assetURL(value) {
  if (!value) return '';
  if (String(value).startsWith('/api/asset?')) return value;
  return '/api/asset?path=' + encodeURIComponent(String(value).replace(/^file:\/\//, ''));
}
function markdown(value, className = 'prose', fields = []) {
  const container = el('div', className);
  // Protect TeX from Markdown's underscore, backslash, and table processing.
  const math = [];
  const prefix = 'CAMATH' + crypto.randomUUID().replaceAll('-', '') + 'TOKEN';
  const fieldKeys = new Set(fields.map(field => field.key));
  const placeholder = /\{\{(?:answer-field:)?([^}]+)\}\}/g;
  let source = String(value || '').replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g, match => {
    math.push(match.replace(placeholder, (whole, key) => fieldKeys.has(key)
      ? `\\underbrace{\\qquad}_{\\text{answer ${fields.findIndex(field => field.key === key) + 1}}}` : whole));
    return prefix + (math.length - 1) + 'END';
  });
  source = source.replace(placeholder, (whole, key) => fieldKeys.has(key) ? `<span class="field-location">${escapeHTML(fieldLabel(key))}</span>` : whole);
  let html = marked.parse(source, { async: false, gfm: true, breaks: false });
  html = html.replace(new RegExp(prefix + '(\\d+)END', 'g'), (_, i) => escapeHTML(math[Number(i)]));
  const fragment = DOMPurify.sanitize(html, {
    RETURN_DOM_FRAGMENT: true,
    USE_PROFILES: { html: true },
    FORBID_TAGS: ['style', 'form', 'input', 'button', 'textarea', 'select', 'iframe', 'object', 'embed'],
    FORBID_ATTR: ['style', 'srcset'],
  });
  for (const image of fragment.querySelectorAll('img')) {
    image.src = assetURL(image.getAttribute('src'));
    image.referrerPolicy = 'no-referrer';
    image.loading = 'lazy';
    image.addEventListener('error', () => {
      const note = el('span', 'math-error', `Image unavailable${image.alt ? ': ' + image.alt : '.'}`);
      image.replaceWith(note);
    }, { once: true });
  }
  for (const link of fragment.querySelectorAll('a')) {
    const href = link.getAttribute('href') || '';
    if (!/^https?:\/\//i.test(href) && !href.startsWith('#')) link.removeAttribute('href');
    else { link.target = '_blank'; link.rel = 'noopener noreferrer'; }
  }
  container.append(fragment);
  return container;
}
function answerValue(answer) {
  if (!answer) return el('span');
  const type = short(answer.type);
  if (type === 'image') {
    const holder = el('div', 'prose');
    const img = el('img'); img.src = assetURL(answer.value); img.alt = 'Answer option';
    holder.append(img); return holder;
  }
  const value = String(answer.value ?? '');
  return markdown(type === 'math' && !/^\s*(\$|\\\[|\\\()/.test(value) ? '$' + value + '$' : value);
}
function loadMath() {
  if (window.MathJax?.startup?.promise) return MathJax.startup.promise;
  if (!mathLoader) {
    mathLoader = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = '/ui/vendor/mathjax/tex-svg.js';
      script.async = true;
      script.onload = () => {
        if (window.MathJax?.startup?.promise) MathJax.startup.promise.then(resolve, reject);
        else reject(new Error('Math rendering could not start. Refresh the page to try again.'));
      };
      script.onerror = () => { script.remove(); reject(new Error('Math rendering could not load. Please try again.')); };
      document.head.append(script);
    }).catch(error => { mathLoader = null; throw error; });
  }
  return mathLoader;
}
function typeset(element) {
  typesetting = typesetting.catch(() => {}).then(async () => {
    if (!element.isConnected || !/\$|\\\(|\\\[|\\begin\{/.test(element.textContent)) return;
    await loadMath();
    if (element.isConnected) await MathJax.typesetPromise([element]);
  }).catch(error => {
    if (element.isConnected) element.append(el('p', 'math-error', error.message));
  });
  return typesetting;
}
function resetMain(className) {
  if (window.MathJax?.typesetClear) MathJax.typesetClear([$('main')]);
  $('main').replaceChildren();
  $('main').className = className || '';
  renderGeneration++;
}

async function home() {
  task = null; clock.running = false;
  resetMain();
  $('main').append(el('div', 'loading', 'Loading your next activities…'));
  setBusy(true); clearError();
  try {
    const data = await api('/api/home');
    updateHeader(data); resetMain();
    document.title = `${data.course?.title || 'Study'} · Course Academy`;
    const head = el('div', 'page-heading');
    const intro = el('div'); intro.append(el('p', 'eyebrow', 'Your study desk'), el('h1', '', 'Next up'), el('p', 'subheading', 'Pick an activity to continue building your knowledge.'));
    head.append(intro, actionButton('Refresh ↻', 'small-button', home));
    $('main').append(head);
    const queue = el('section', 'queue'); queue.setAttribute('aria-label', 'Next five activities');
    const activities = (data.activities || []).slice(0, 5);
    activities.forEach((activity, index) => {
      const row = el('article', 'queue-card');
      const info = el('div');
      const meta = el('div', 'queue-meta');
      const type = short(activity.type) || 'lesson';
      meta.append(el('span', '', type));
      if (['started', 'paused'].includes(short(activity.status))) meta.append(el('span', '', 'In progress'));
      if (activity.expectedSeconds) meta.append(el('span', '', `About ${Math.round(activity.expectedSeconds / 60)} min`));
      if (Number.isFinite(activity.xpBase)) meta.append(el('span', '', `${activity.xpBase} XP`));
      info.append(meta, el('h2', '', activity.title));
      if (activity.reason) info.append(el('p', 'queue-reason', activity.reason));
      const resume = Boolean(activity.taskId);
      row.append(el('span', 'queue-number', String(index + 1).padStart(2, '0')), info,
        actionButton(resume ? 'Resume →' : 'Begin →', 'primary', () => resume ? openTask(activity.taskId) : mutation('/api/start', { activityId: activity.activityId })));
      queue.append(row);
    });
    if (!activities.length) {
      const empty = el('div', 'empty-state');
      empty.append(el('h2', '', 'No ready activities yet'), el('p', '', data.message || 'There are no eligible activities with enough available questions.'));
      queue.append(empty);
    }
    $('main').append(queue);
    const foot = el('div', 'queue-foot');
    foot.append(el('span', '', `${activities.length} ${activities.length === 1 ? 'activity' : 'activities'} ready`), el('span', '', 'Your progress is saved as you work.'));
    $('main').append(foot);
    if (data.practiceNotice || data.notice) $('main').append(el('p', 'notice', data.practiceNotice || data.notice));
  } catch (error) { showError(error, home); }
  finally { setBusy(false); }
}
async function openTask(id) {
  clearError(); setBusy(true);
  void loadMath().catch(() => {});
  try {
    task = await api('/api/task?taskId=' + encodeURIComponent(id));
    task = task.task || task;
    history.replaceState(null, '', '/learn?taskId=' + encodeURIComponent(id));
    await renderTask(task);
  } catch (error) { showError(error, () => openTask(id)); }
  finally { setBusy(false); void syncAfterVisibility(); }
}
async function leaveTask(event) {
  event?.preventDefault();
  if (busy) return;
  if (task && !terminal(short(task.status))) {
    setBusy(true);
    try { await api('/api/pause', { taskId: task.taskId, requestId: crypto.randomUUID() }); }
    catch (error) { showError(error, () => leaveTask()); setBusy(false); return; }
    setBusy(false);
  }
  history.replaceState(null, '', '/home');
  await home();
}
async function explore(url) {
  if (busy) throw new Error('Your progress is being saved. Try again in a moment.');
  setBusy(true);
  try {
    if (pendingPause) await pendingPause;
    if (task && short(task.status) === 'started') {
      await api('/api/pause', { taskId: task.taskId, requestId: crypto.randomUUID() });
      task.status = 'paused';
    }
    location.assign(url);
  } finally { setBusy(false); }
}

function choiceOrder(choices, seed) {
  const hash = value => { let n = 2166136261; for (const c of value) n = Math.imul(n ^ c.charCodeAt(0), 16777619); return n >>> 0; };
  return [...choices].sort((a, b) => hash(`${seed}:${a.id}`) - hash(`${seed}:${b.id}`));
}
function fieldControl(field, readOnly, itemId) {
  const set = el('fieldset', 'answer-field');
  set.dataset.fieldId = String(field.id);
  set.dataset.type = short(field.type);
  const label = field.key === 'selection' ? 'Choose an answer' : fieldLabel(field.key);
  set.append(el('legend', '', label));
  const type = short(field.type), response = field.response;
  const choices = choiceOrder(field.choices || [], `${itemId}:${field.id}`);
  const responseId = response?.choiceId ?? response?.id;
  if (type === 'blank') {
    const input = el('input', 'answer-input');
    input.type = 'text'; input.name = String(field.id); input.autocomplete = 'off'; input.spellcheck = false;
    input.setAttribute('aria-label', label); input.value = response?.value ?? ''; input.disabled = readOnly;
    input.placeholder = 'Enter your answer'; set.append(input);
    if (!readOnly) set.append(el('div', 'input-help', 'Use ordinary notation or LaTeX.'));
  } else if (type === 'radio') {
    const list = el('div', 'choices');
    for (const choice of choices) {
      const option = el('label', 'choice');
      const input = el('input'); input.type = 'radio'; input.name = String(field.id); input.value = String(choice.id);
      input.checked = String(responseId) === String(choice.id); input.disabled = readOnly;
      option.append(input, answerValue(choice)); list.append(option);
    }
    set.append(list);
  } else if (type === 'select') {
    // Native option elements cannot contain typeset math; lettered previews keep the dropdown accessible.
    const previews = el('div', 'select-options');
    const select = el('select', 'answer-select'); select.name = String(field.id); select.disabled = readOnly;
    select.setAttribute('aria-label', label);
    const placeholder = el('option', '', 'Select an answer…'); placeholder.value = ''; select.append(placeholder);
    choices.forEach((choice, index) => {
      const letter = String.fromCharCode(65 + index);
      const preview = el('div', 'option-preview'); preview.append(el('div', 'option-label', letter), answerValue(choice)); previews.append(preview);
      const option = el('option', '', `${letter}${short(choice.type) === 'text' ? ' · ' + choice.value : ''}`);
      option.value = String(choice.id); option.selected = String(responseId) === String(choice.id); select.append(option);
    });
    set.append(previews, select);
  }
  for (const input of set.querySelectorAll('input,select')) {
    input.dataset.answerInput = 'true'; input.dataset.readOnly = String(readOnly);
  }
  return set;
}
function collectResponses(form, fields) {
  return fields.map(field => {
    const set = [...form.querySelectorAll('fieldset')].find(node => node.dataset.fieldId === String(field.id));
    if (short(field.type) === 'blank') return { fieldId: field.id, value: set.querySelector('input').value };
    const input = set.querySelector('input:checked, select');
    return { fieldId: field.id, choiceId: input?.value ? Number(input.value) : '' };
  });
}

async function renderTask(data) {
  updateHeader(data);
  resetMain('lesson-main');
  const generation = renderGeneration;
  const status = short(data.status);
  clock = { at: Date.now(), elapsed: Number(data.elapsedSeconds) || 0, running: status === 'started' && short(data.step?.status) === 'started' };
  document.title = `${data.title || 'Lesson'} · Course Academy`;
  const top = el('div', 'lesson-topline');
  top.append(actionButton('← Back to study', 'text-button', leaveTask));
  if (!terminal(status)) top.append(actionButton(status === 'paused' ? 'Resume' : 'Pause', 'text-button', () => mutation(status === 'paused' ? '/api/resume' : '/api/pause', { taskId: data.taskId })));
  $('main').append(top);
  const heading = el('div', 'lesson-heading');
  const headingText = el('div'); headingText.append(el('p', 'eyebrow', short(data.type) || 'Lesson'), el('h1', '', data.title || 'Lesson'));
  const timer = el('span', 'timer', duration(clock.elapsed)); timer.id = 'taskTimer'; timer.setAttribute('aria-label', 'Working time');
  heading.append(headingText, timer); $('main').append(heading);
  if (terminal(status)) {
    const done = el('section', 'completion');
    done.append(el('div', 'completion-mark', status === 'completed' ? '✓' : '↗'), el('h2', '', status === 'completed' ? 'Activity complete' : 'More practice needed'));
    done.append(el('p', '', status === 'completed' ? 'Your answers and progress have been saved.' : 'Your answers are saved. This attempt did not establish mastery. Return to study to continue.'));
    const earned = data.xpEarned ?? data.xp?.earned ?? (typeof data.xp === 'number' ? data.xp : null);
    if (earned !== null && earned !== undefined) {
      const xp = el('div', 'completion-xp', `${earned >= 0 ? '+' : ''}${earned} `); xp.append(el('small', '', 'XP')); done.append(xp);
    }
    done.append(el('p', '', `${duration(data.elapsedSeconds)} working time`), actionButton('Back to study →', 'primary', leaveTask));
    $('main').append(done); return;
  }
  if (status === 'paused') {
    const pause = el('section', 'pause-panel'), text = el('div');
    text.append(el('h2', '', 'Session paused'), el('p', '', 'Your place is saved. The working timer is stopped.'));
    pause.append(text, actionButton('Resume lesson →', 'primary', () => mutation('/api/resume', { taskId: data.taskId })));
    $('main').append(pause);
    return;
  }
  const step = data.step;
  if (!step) { $('main').append(el('p', 'notice', 'No current step is available. Return to study and try again.')); return; }
  const number = data.progress?.stepNumber ?? step.stepNumber;
  const total = data.progress?.totalSteps ?? step.totalSteps;
  if (number && total) {
    const track = el('div', 'progress-track'), fill = el('div', 'progress-fill');
    track.setAttribute('role', 'progressbar'); track.setAttribute('aria-label', 'Lesson progress'); track.setAttribute('aria-valuemin', '0'); track.setAttribute('aria-valuemax', String(total)); track.setAttribute('aria-valuenow', String(number - 1));
    fill.style.width = `${Math.min(100, Math.max(0, (number - 1) / total * 100))}%`; track.append(fill); $('main').append(track);
  }
  const content = el('section', 'lesson-content');
  const meta = el('div', 'step-meta');
  if (number) meta.append(el('span', '', `Step ${number}${total ? ' / ' + total : ''}`));
  const kind = short(step.kind);
  meta.append(el('span', 'step-tag', { question: 'Practice', example: 'Worked example', tutorial: 'Tutorial' }[kind] || kind));
  if (step.requiresCalculator) meta.append(el('span', '', 'Calculator required'));
  if (step.difficulty) meta.append(el('span', '', short(step.difficulty)));
  if (step.attempt) meta.append(el('span', '', `Question ${step.attempt}`));
  content.append(meta);
  if (step.title) content.append(el('h2', 'step-title', step.title));
  const card = el('div', 'content-card'); card.append(markdown(step.markdown ?? step.problem ?? '', 'prose', step.fields || []));
  const isAnswered = answered(short(step.status));
  const fields = step.fields || [];
  if (kind === 'question' && fields.length) {
    const form = el('form'); form.noValidate = false;
    const fieldList = el('div', 'answer-fields');
    const draft = drafts.get(step.itemId) || [];
    fields.forEach(field => {
      const saved = draft.find(response => response.fieldId === field.id);
      fieldList.append(fieldControl(!isAnswered && saved ? { ...field, response: saved } : field, isAnswered, step.itemId));
    });
    form.append(fieldList);
    if (!isAnswered) {
      const actions = el('div', 'answer-actions');
      const submit = el('button', 'primary', 'Check answer'); submit.type = 'submit'; submit.dataset.action = 'true';
      const refresh = () => {
        const responses = collectResponses(form, fields);
        drafts.set(step.itemId, responses);
        const valid = responses.every(r => r.choiceId ? true : 'value' in r && r.value.trim().length > 0);
        submit.dataset.unavailable = String(!valid); submit.disabled = busy || !valid;
      };
      form.addEventListener('input', refresh); form.addEventListener('change', refresh);
      form.addEventListener('submit', event => {
        event.preventDefault(); refresh(); if (submit.disabled) return;
        mutation('/api/answer', { taskId: data.taskId, itemId: step.itemId, responses: collectResponses(form, fields) });
      });
      actions.append(submit); form.append(actions); refresh();
    }
    card.append(form);
  }
  if (isAnswered) {
    const feedback = el('div', 'feedback');
    feedback.append(el('div', 'feedback-heading', step.status === 'correct' ? '✓ Correct' : step.status === 'skipped' ? 'Skipped' : 'Answer recorded · Incorrect'));
    if (step.feedback) feedback.append(markdown(step.feedback));
    for (const field of fields) {
      if (field.response?.feedback) feedback.append(markdown(field.response.feedback));
      if (step.status === 'incorrect' && field.correctAnswer) {
        feedback.append(el('p', 'response-summary', `${field.key === 'selection' ? 'Correct answer' : fieldLabel(field.key) + ' · correct value'}:`), answerValue(field.correctAnswer));
      }
    }
    card.append(feedback);
  }
  if (step.solution && (kind === 'example' || isAnswered)) {
    const solution = el('section', 'worked-solution');
    solution.append(el('div', 'section-label', 'Worked solution'), markdown(step.solution)); card.append(solution);
  }
  content.append(card);
  const controls = el('div', 'lesson-controls');
  const canContinue = Boolean(step.canContinue);
  const hint = kind === 'question' && !isAnswered ? 'Answer every field and check your answer to continue.' : kind === 'example' ? 'Read through the worked solution, then try it yourself.' : kind === 'tutorial' ? 'Continue when you have finished reading.' : 'Your answer has been saved.';
  controls.append(el('p', 'continue-hint', hint), actionButton('Continue →', 'primary', () => mutation('/api/continue', { taskId: data.taskId, itemId: step.itemId }), canContinue));
  content.append(controls); $('main').append(content);
  await typeset(content);
  if (generation === renderGeneration && !document.hidden) $('main').focus({ preventScroll: true });
}

$('retryButton').addEventListener('click', () => retryOperation?.());
$('homeLink').addEventListener('click', leaveTask);
document.querySelector('.brand').addEventListener('click', leaveTask);
for (const link of [$('graphLink'), $('courseLink')]) link.addEventListener('click', async event => {
  event.preventDefault();
  try { await explore(link.href); }
  catch (error) { showError(error, () => link.click()); }
});
createCoursePicker({
  getSnapshot: async () => {
    if (!curriculumSnapshot) curriculumSnapshot = api('/api/graph-explorer').catch(error => { curriculumSnapshot = null; throw error; });
    return curriculumSnapshot;
  },
  getCourseId: () => currentCourseId,
  onSelectCourse: course => explore('/?course=' + encodeURIComponent(course.id || 'all')),
  onSelectTopic: topic => explore('/?course=all&topic=' + encodeURIComponent(topic.id)),
});
window.addEventListener('popstate', () => {
  const id = new URL(location.href).searchParams.get('taskId');
  if (id) openTask(id); else leaveTask();
});
setInterval(() => {
  const timer = $('taskTimer');
  if (timer) timer.textContent = duration(clock.elapsed + (clock.running ? (Date.now() - clock.at) / 1000 : 0));
}, 1000);
async function syncAfterVisibility() {
  if (pendingPause) await pendingPause;
  if (document.hidden || busy || !refreshAfterVisibility || !task) return;
  refreshAfterVisibility = false;
  await openTask(task.taskId);
}
function pauseWhenHidden() {
  if (pendingPause) return pendingPause;
  if (!task || short(task.status) !== 'started') return;
  const taskId = task.taskId;
  clock.elapsed += clock.running ? (Date.now() - clock.at) / 1000 : 0; clock.running = false;
  refreshAfterVisibility = true;
  pendingPause = api('/api/pause', { taskId, requestId: crypto.randomUUID() }, { keepalive: true })
    .then(() => { if (task?.taskId === taskId) task.status = 'paused'; })
    .catch(() => { /* Re-read authoritative state when the page becomes visible. */ })
    .finally(() => { pendingPause = null; void syncAfterVisibility(); });
  return pendingPause;
}
document.addEventListener('visibilitychange', () => {
  if (document.hidden) pauseWhenHidden();
  else if (task) { refreshAfterVisibility = true; void syncAfterVisibility(); }
});
window.addEventListener('pagehide', pauseWhenHidden);

const initialTask = new URL(location.href).searchParams.get('taskId');
if (initialTask) openTask(initialTask); else home();
