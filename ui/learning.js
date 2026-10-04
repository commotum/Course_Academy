import { marked } from './vendor/marked/marked.esm.js';
import { createCoursePicker, topicReferenceURL } from './navigation.js';
import { developerModeReady, isDeveloperMode } from './developer-mode.js';
import { attachStepMenu } from './step-menu.js';

await developerModeReady;

const $ = id => document.getElementById(id);
const terminal = status => ['completed', 'failed'].includes(status);
const answered = status => ['correct', 'incorrect', 'skipped'].includes(status);
let task = null;
let busy = false;
let retryOperation = null;
let renderGeneration = 0;
let clock = { at: 0, elapsed: 0, running: false };
let typesetting = Promise.resolve();
let mathLoader = null;
const drafts = new Map();
let pendingPause = null;
let refreshAfterVisibility = false;
let currentCourseId = null;
let curriculumSnapshot = null;
let homeRendered = false;
let homeRequest = null;
let homeController = null;
let queueRequest = null;
let targetRevision = 0;
let previewStepIndex = 0;
let modeChanging = false;
let settingsRevision = 0;
let lessonView = null;
const seenTaskSteps = new Map();

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
function appendStepHeading(content, step, kind) {
  if (!step.title && kind !== 'example') return;
  const heading = el('h2', 'step-title');
  if (kind === 'example') heading.append(el('strong', '', 'Example:'));
  if (step.title) heading.append((kind === 'example' ? ' ' : '') + step.title);
  content.append(heading);
}
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
function updateHeader(data) {
  const setText = (id, value) => { if ($(id).textContent !== value) $(id).textContent = value; };
  if (data.learner) setText('learnerName', data.learner.name || 'Profile');
  if (data.course) {
    currentCourseId = data.course.id;
    const href = '/progress?course=' + encodeURIComponent(data.course.id);
    if ($('courseLink').getAttribute('href') !== href) $('courseLink').setAttribute('href', href);
    // Only learning responses supply this cache: browsing another course must
    // never replace the learner's designated study-course header.
    try {
      const header = JSON.stringify({ courseId: data.course.id, learnerName: $('learnerName').textContent });
      if (sessionStorage.getItem('course-academy.study-header') !== header) sessionStorage.setItem('course-academy.study-header', header);
    } catch { /* The app works normally when browser storage is unavailable. */ }
  }
}
async function api(path, body, options = {}) {
  if (body && (modeChanging || isDeveloperMode() && path !== '/api/preview-answer')) {
    throw new Error('Developer mode does not record activity.');
  }
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
  if (isDeveloperMode() || modeChanging) return;
  if (busy) return;
  if (path === '/api/start') void loadMath().catch(() => {});
  const body = { ...values, requestId: crypto.randomUUID() };
  const revision = settingsRevision;
  const run = async () => {
    clearError();
    setBusy(true);
    try {
      const result = await api(path, body);
      if (revision !== settingsRevision || modeChanging || isDeveloperMode()) return;
      task = result.task || result;
      history.replaceState(null, '', '/learn?taskId=' + encodeURIComponent(task.taskId));
      await renderTask(task);
      announce(answered(task.step?.status) ? (task.step.status === 'correct' ? 'Correct.' : 'Answer recorded.') : task.step?.title || 'Progress saved.');
    } catch (error) {
      if (revision !== settingsRevision) return;
      // Only a confirmed rejection may get a fresh request identity. An uncertain
      // network failure must replay the original request to avoid duplicate credit.
      if (error.code === 'basis-conflict') body.requestId = crypto.randomUUID();
      showError(error, run);
    } finally { if (revision === settingsRevision) { setBusy(false); void syncAfterVisibility(); } }
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
  homeRendered = false;
  lessonView = null;
  if (window.MathJax?.typesetClear) MathJax.typesetClear([$('main')]);
  $('main').replaceChildren();
  $('main').className = className || '';
  renderGeneration++;
}

function stopClock() {
  if (clock.running) clock.elapsed += (Date.now() - clock.at) / 1000;
  clock.running = false;
}

// Cache only presentations already returned by the task API. Earlier steps are
// review material, never an input to grading or to the current presentation.
function rememberTaskStep(data) {
  const key = `course-academy.lesson-history.${data.learner?.id || 'learner'}.${data.taskId}`;
  let seen = seenTaskSteps.get(key);
  if (!seen) {
    seen = new Map();
    try {
      const saved = JSON.parse(sessionStorage.getItem(key));
      if (Array.isArray(saved)) for (const entry of saved) {
        if (entry?.step?.itemId && Number.isInteger(entry.order) && entry.order > 0) seen.set(String(entry.step.itemId), entry);
      }
    } catch { /* Review history can still be kept in memory. */ }
    seenTaskSteps.set(key, seen);
  }
  if (data.step?.itemId) {
    const id = String(data.step.itemId);
    const order = data.progress?.presented || seen.get(id)?.order || seen.size + 1;
    for (const [item, entry] of seen) if (entry.order > order) seen.delete(item);
    seen.set(id, {
      order, step: data.step,
      number: data.progress?.stepNumber ?? data.step.stepNumber,
      total: data.progress?.totalSteps ?? data.step.totalSteps,
    });
    try { sessionStorage.setItem(key, JSON.stringify([...seen.values()])); } catch { /* Storage may be full or unavailable. */ }
  }
  return [...seen.values()].sort((a, b) => a.order - b.order);
}

function lessonCompletedSteps(number, total, complete = false) {
  const maximum = Number(total) || 1;
  return complete ? maximum : Math.min(maximum, Math.max(0, (Number(number) || 1) - 1));
}

function lessonShell(data, { preview = false, number, total, complete = false } = {}) {
  const key = `${preview ? 'preview' : 'task'}:${data.learner?.id || 'learner'}:${preview ? data.activityId : data.taskId}`;
  if (lessonView?.key !== key) {
    resetMain('lesson-main');
    const heading = el('h1', 'sr-only', data.title || 'Lesson');
    const toolbar = el('div', 'lesson-toolbar');
    const exit = actionButton('←', 'lesson-exit text-button', leaveTask);
    exit.setAttribute('aria-label', 'Exit lesson and return to Study');
    exit.title = 'Back to Study';
    const track = el('div', 'progress-track'), fill = el('div', 'progress-fill');
    track.setAttribute('role', 'progressbar'); track.setAttribute('aria-label', 'Lesson progress');
    track.setAttribute('aria-valuemin', '0'); track.append(fill);
    const position = el('span', 'lesson-position');
    const timer = el('span', 'timer', preview ? 'Preview' : duration(clock.elapsed));
    if (!preview) { timer.id = 'taskTimer'; timer.setAttribute('aria-label', 'Working time'); }
    else timer.title = 'Developer mode · Nothing recorded';
    toolbar.append(exit, track, position, timer);
    const feed = el('div', 'lesson-feed');
    $('main').append(heading, toolbar, feed);
    lessonView = { key, feed, track, fill, position, timer, current: null, currentId: null, history: new Map() };
  }
  const maximum = Number(total) || 1;
  const completed = lessonCompletedSteps(number, total, complete);
  lessonView.track.hidden = !total;
  lessonView.track.setAttribute('aria-valuemax', String(maximum));
  lessonView.track.setAttribute('aria-valuenow', String(completed));
  lessonView.track.setAttribute('aria-valuetext', complete ? 'Lesson complete' : `Step ${number || 1} of ${maximum}`);
  lessonView.fill.style.width = `${completed / maximum * 100}%`;
  lessonView.position.textContent = total ? `${String(number || 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}` : '';
  lessonView.timer.textContent = preview ? 'Preview' : duration(clock.elapsed);
  return lessonView;
}

function archiveLessonContent(content) {
  content.dataset.history = 'true';
  const meta = content.querySelector('.step-meta');
  if (meta && content.dataset.stepNumber && !meta.querySelector('.history-position')) {
    const position = el('span', 'history-position', `Step ${content.dataset.stepNumber}${content.dataset.totalSteps ? ' / ' + content.dataset.totalSteps : ''}`);
    meta.insertBefore(position, meta.firstChild);
  }
  for (const control of content.querySelectorAll('.lesson-controls, .answer-actions')) control.remove();
  for (const input of content.querySelectorAll('[data-answer-input]')) {
    input.disabled = true; input.dataset.readOnly = 'true';
  }
}

async function showLessonStep(view, identity, earlier, content, buildEarlier) {
  const generation = ++renderGeneration;
  const changedStep = view.currentId !== identity;
  if (changedStep) view.needsFocus = true;
  if (view.current) {
    if (changedStep && earlier.some(entry => entry.id === view.currentId)) {
      archiveLessonContent(view.current);
      view.history.set(view.currentId, view.current);
    } else {
      if (window.MathJax?.typesetClear) MathJax.typesetClear([view.current]);
      view.current.remove();
    }
  }
  const visible = new Set(earlier.map(entry => entry.id));
  for (const [id, node] of view.history) if (!visible.has(id)) {
    if (window.MathJax?.typesetClear) MathJax.typesetClear([node]);
    node.remove(); view.history.delete(id);
  }
  const additions = [];
  for (const entry of earlier) {
    let node = view.history.get(entry.id);
    if (!node) {
      node = buildEarlier(entry); archiveLessonContent(node);
      view.history.set(entry.id, node); additions.push(node);
    }
    view.feed.append(node);
  }
  view.current = content; view.currentId = identity;
  content.tabIndex = -1;
  view.feed.append(content);
  for (const node of [...additions, content]) await typeset(node);
  if (generation !== renderGeneration || document.hidden || lessonView !== view) return;
  if (view.needsFocus) {
    content.scrollIntoView({ block: 'start', behavior: 'instant' });
    content.focus({ preventScroll: true });
    view.needsFocus = false;
  }
}

function home({ preserve = false } = {}) {
  if (homeRequest) return homeRequest;
  const revision = targetRevision;
  const controller = new AbortController();
  homeController = controller;
  const request = loadHome(controller.signal, preserve).finally(() => {
    if (homeRequest === request) {
      homeRequest = null; homeController = null;
      if (!task && !document.hidden && revision !== targetRevision) void home();
    }
  });
  homeRequest = request;
  return request;
}
async function loadHome(signal, preserve) {
  const revision = targetRevision;
  task = null; clock.running = false;
  if (!preserve) {
    resetMain();
    $('main').append(el('div', 'loading', 'Loading your next activities…'));
  }
  setBusy(true); clearError();
  try {
    // Reuse an uncertain request so a retry cannot create duplicate pending tasks.
    if (!isDeveloperMode()) queueRequest ||= { requestId: crypto.randomUUID() };
    const data = isDeveloperMode()
      ? await api('/api/preview-home', undefined, { signal })
      : await api('/api/queue', queueRequest, { signal });
    queueRequest = null;
    if (signal.aborted || modeChanging) return;
    updateHeader(data); resetMain();
    document.title = 'Study · Course Academy';
    const head = el('div', 'page-heading');
    const intro = el('div'); intro.append(el('p', 'eyebrow', 'Your study desk'), el('h1', '', 'Next up'), el('p', 'subheading', isDeveloperMode() ? 'Preview activities without starting an attempt or recording progress.' : 'Pick an activity to continue building your knowledge.'));
    head.append(intro);
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
      if (!isDeveloperMode() && activity.expectedSeconds) meta.append(el('span', '', `About ${Math.round(activity.expectedSeconds / 60)} min`));
      if (!isDeveloperMode() && Number.isFinite(activity.xpBase)) meta.append(el('span', '', `${activity.xpBase} XP`));
      info.append(meta, el('h2', '', activity.title));
      if (activity.reason) info.append(el('p', 'queue-reason', activity.reason));
      const resume = Boolean(activity.taskId) && ['started', 'paused'].includes(short(activity.status));
      const total = activity.progress?.totalSteps;
      const number = activity.progress?.stepNumber;
      if (!isDeveloperMode() && resume && Number.isInteger(total) && total > 0 && Number.isInteger(number) && number > 0) {
        const completed = lessonCompletedSteps(number, total);
        const percentage = Math.round(completed / total * 100);
        const progress = el('div', 'queue-progress');
        const track = el('div', 'queue-progress-track'), fill = el('div', 'queue-progress-fill');
        track.setAttribute('role', 'progressbar');
        track.setAttribute('aria-label', `${activity.title} progress`);
        track.setAttribute('aria-valuemin', '0');
        track.setAttribute('aria-valuemax', String(total));
        track.setAttribute('aria-valuenow', String(completed));
        track.setAttribute('aria-valuetext', `${percentage}% complete`);
        fill.style.width = `${completed / total * 100}%`;
        track.append(fill);
        progress.append(track, el('span', 'queue-progress-value', `${percentage}%`));
        info.append(progress);
      }
      row.append(el('span', 'queue-number', String(index + 1).padStart(2, '0')), info,
        actionButton(isDeveloperMode() ? 'Preview →' : resume ? 'Resume →' : 'Begin →', 'primary', () => isDeveloperMode() ? openPreview({ activityId: activity.activityId }) : resume ? openTask(activity.taskId) : mutation('/api/start', { activityId: activity.activityId })));
      queue.append(row);
    });
    if (!activities.length) {
      const empty = el('div', 'empty-state');
      empty.append(el('h2', '', 'No ready activities yet'), el('p', '', data.message || 'There are no eligible activities with enough available questions.'));
      queue.append(empty);
    }
    $('main').append(queue);
    const foot = el('div', 'queue-foot');
    foot.append(el('span', '', `${activities.length} ${activities.length === 1 ? 'activity' : 'activities'} ready`), el('span', '', isDeveloperMode() ? 'Developer mode · Nothing recorded' : 'Your progress is saved as you work.'));
    $('main').append(foot);
    if (data.practiceNotice || data.notice) $('main').append(el('p', 'notice', data.practiceNotice || data.notice));
    homeRendered = revision === targetRevision;
  } catch (error) {
    if (error.code === 'basis-conflict') queueRequest = null;
    if (!signal.aborted) showError(error, home);
  }
  finally { if (!signal.aborted) setBusy(false); }
}
async function openTask(id) {
  if (modeChanging) return;
  if (isDeveloperMode()) return openPreview({ taskId: id });
  homeController?.abort(); homeController = null; homeRequest = null;
  homeRendered = false;
  clearError(); setBusy(true);
  void loadMath().catch(() => {});
  const revision = settingsRevision;
  try {
    let data = await api('/api/task?taskId=' + encodeURIComponent(id));
    if (revision !== settingsRevision || modeChanging || isDeveloperMode()) return;
    if (data.assignment?.id) {
      location.replace('/assignments?assignment=' + encodeURIComponent(data.assignment.id));
      return;
    }
    if (!document.hidden && short((data.task || data).status) === 'paused') {
      data = await api('/api/resume', { taskId: (data.task || data).taskId, requestId: crypto.randomUUID() });
      if (revision !== settingsRevision || modeChanging || isDeveloperMode()) return;
    }
    task = data.task || data;
    history.replaceState(null, '', '/learn?taskId=' + encodeURIComponent(id));
    await renderTask(task);
  } catch (error) { if (revision === settingsRevision) showError(error, () => openTask(id)); }
  finally { if (revision === settingsRevision) { setBusy(false); void syncAfterVisibility(); } }
}
async function leaveTask(event) {
  event?.preventDefault();
  if (busy || modeChanging) return;
  if (!task && homeRendered && $('errorBanner').hidden) {
    history.replaceState(null, '', '/home');
    return;
  }
  if (!isDeveloperMode() && task && !terminal(short(task.status))) {
    stopClock();
    setBusy(true);
    try {
      if (pendingPause) await pendingPause;
      if (short(task.status) === 'started') await api('/api/pause', { taskId: task.taskId, requestId: crypto.randomUUID() });
    }
    catch (error) { showError(error, () => leaveTask()); setBusy(false); return; }
    setBusy(false);
  }
  history.replaceState(null, '', '/home');
  await home();
}
async function explore(url) {
  if (modeChanging) return;
  if (isDeveloperMode()) { location.assign(url); return; }
  if (busy) throw new Error('Your progress is being saved. Try again in a moment.');
  setBusy(true);
  try {
    if (pendingPause) await pendingPause;
    if (task && short(task.status) === 'started') {
      stopClock();
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

async function openPreview(query) {
  if (!isDeveloperMode() || modeChanging) return;
  homeController?.abort(); homeController = null; homeRequest = null;
  homeRendered = false; clock.running = false;
  drafts.clear(); clearError(); setBusy(true);
  const revision = settingsRevision;
  try {
    const data = await api('/api/preview?' + new URLSearchParams(query));
    if (revision !== settingsRevision || modeChanging || !isDeveloperMode()) return;
    if (short(data.type) === 'assignment' && data.activityUuid) {
      location.replace('/assignments?assignment=' + encodeURIComponent(data.activityUuid));
      return;
    }
    task = data;
    previewStepIndex = 0;
    lessonView = null;
    history.replaceState(null, '', '/learn?activityId=' + encodeURIComponent(data.activityId));
    await renderPreview();
  } catch (error) { if (revision === settingsRevision) showError(error, () => openPreview(query)); }
  finally { if (revision === settingsRevision) setBusy(false); }
}

function previewContent(data, step, index, archived = false) {
  const content = el('section', 'lesson-content'), meta = el('div', 'step-meta');
  content.dataset.stepNumber = String(index + 1); content.dataset.totalSteps = String(data.steps.length);
  attachStepMenu(content, step.stepId);
  const kind = short(step.kind), fields = step.fields || [];
  if (archived) meta.append(el('span', 'history-position', `Step ${index + 1} / ${data.steps.length}`));
  if (kind !== 'example') meta.append(el('span', 'step-tag', { question: 'Practice', tutorial: 'Tutorial' }[kind] || kind));
  if (step.requiresCalculator) meta.append(el('span', '', 'Calculator required'));
  if (step.difficulty) meta.append(el('span', '', short(step.difficulty)));
  content.append(meta);
  const card = el('div', 'content-card');
  appendStepHeading(card, step, kind);
  card.append(markdown(step.markdown ?? step.problem ?? '', 'prose', fields));
  if (fields.length) {
    const form = el('form'), fieldList = el('div', 'answer-fields');
    const readOnly = archived || kind === 'example' || answered(short(step.status));
    fields.forEach(field => fieldList.append(fieldControl(field, readOnly, step.contentId)));
    form.append(fieldList);
    if (!readOnly) {
      const actions = el('div', 'answer-actions');
      const check = el('button', 'primary', 'Check preview answer'); check.type = 'submit'; check.dataset.action = 'true';
      const refresh = () => {
        const responses = collectResponses(form, fields);
        const valid = responses.every(response => response.choiceId || typeof response.value === 'string' && response.value.trim());
        check.dataset.unavailable = String(!valid); check.disabled = busy || !valid;
      };
      form.addEventListener('input', refresh); form.addEventListener('change', refresh);
      form.addEventListener('submit', async event => {
        event.preventDefault(); refresh();
        if (check.disabled || !isDeveloperMode() || lessonView?.current !== content) return;
        setBusy(true); clearError();
        try {
          const result = await api('/api/preview-answer', { activityId: data.activityId, questionId: step.contentId, responses: collectResponses(form, fields) });
          if (lessonView?.current !== content || !isDeveloperMode()) return;
          const checked = result.step || result;
          data.steps[index] = { ...step, ...checked };
          await renderPreview();
          announce(checked.status === 'correct' ? 'Correct. Preview only; nothing recorded.' : 'Incorrect. Preview only; nothing recorded.');
        } catch (error) { showError(error); }
        finally { setBusy(false); }
      });
      actions.append(check); form.append(actions); refresh();
    }
    card.append(form);
  }
  if (answered(short(step.status))) {
    const feedback = el('div', 'feedback');
    feedback.append(el('div', 'feedback-heading', short(step.status) === 'correct' ? '✓ Correct · Preview only' : 'Incorrect · Preview only'));
    if (step.feedback) feedback.append(markdown(step.feedback));
    for (const field of fields) if (field.response?.feedback) feedback.append(markdown(field.response.feedback));
    card.append(feedback);
  }
  if (step.solution || fields.some(field => field.correctAnswer)) {
    const solution = el('details', 'worked-solution');
    solution.open = kind === 'example' || answered(short(step.status));
    solution.append(el('summary', 'solution-heading', 'Solution:'));
    for (const field of fields) {
      if (field.correctAnswer) {
        solution.append(el('p', 'response-summary', `${fieldLabel(field.key)} · correct value:`), answerValue(field.correctAnswer));
        if (field.correctAnswer.feedback) solution.append(markdown(field.correctAnswer.feedback));
      }
    }
    if (step.solution) solution.append(markdown(step.solution));
    solution.addEventListener('toggle', () => { if (solution.open) void typeset(solution); });
    card.append(solution);
  }
  content.append(card);
  if (!archived) {
    const controls = el('div', 'lesson-controls');
    controls.append(index + 1 < data.steps.length
      ? actionButton('Next step →', 'primary', async () => { previewStepIndex++; clearError(); await renderPreview(); })
      : actionButton('Back to study →', 'primary', leaveTask));
    content.append(controls);
  }
  return content;
}

async function renderPreview() {
  if (!isDeveloperMode() || modeChanging || !task) return;
  const data = task, steps = data.steps || [], step = steps[previewStepIndex];
  updateHeader(data);
  document.title = `Preview${data.title ? ' · ' + data.title : ''} · Course Academy`;
  const view = lessonShell(data, { preview: true, number: previewStepIndex + 1, total: steps.length });
  if (!step) { view.feed.replaceChildren(el('p', 'notice', 'This activity has no content available to preview.')); return; }
  const earlier = steps.slice(0, previewStepIndex).map((step, index) => ({ id: `preview:${index}`, step, index }));
  await showLessonStep(view, `preview:${previewStepIndex}`, earlier,
    previewContent(data, step, previewStepIndex), entry => previewContent(data, entry.step, entry.index, true));
}

function taskContent(data, step, number, total, archived = false) {
  const content = el('section', 'lesson-content');
  if (number) content.dataset.stepNumber = String(number);
  if (total) content.dataset.totalSteps = String(total);
  attachStepMenu(content, step.stepId);
  const meta = el('div', 'step-meta');
  if (number && archived) meta.append(el('span', 'history-position', `Step ${number}${total ? ' / ' + total : ''}`));
  const kind = short(step.kind);
  if (kind !== 'example') meta.append(el('span', 'step-tag', { question: 'Practice', tutorial: 'Tutorial' }[kind] || kind));
  if (step.requiresCalculator) meta.append(el('span', '', 'Calculator required'));
  if (step.difficulty) meta.append(el('span', '', short(step.difficulty)));
  if (step.attempt) meta.append(el('span', '', `Question ${step.attempt}`));
  content.append(meta);
  const card = el('div', 'content-card');
  appendStepHeading(card, step, kind);
  card.append(markdown(step.markdown ?? step.problem ?? '', 'prose', step.fields || []));
  const isAnswered = answered(short(step.status));
  const readOnly = archived || isAnswered || short(data.status) === 'paused';
  const fields = step.fields || [];
  if (kind === 'question' && fields.length) {
    const form = el('form'); form.noValidate = false;
    const fieldList = el('div', 'answer-fields');
    const draft = drafts.get(step.itemId) || [];
    fields.forEach(field => {
      const saved = draft.find(response => response.fieldId === field.id);
      fieldList.append(fieldControl(!readOnly && saved ? { ...field, response: saved } : field, readOnly, step.itemId));
    });
    form.append(fieldList);
    if (!readOnly) {
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
        event.preventDefault(); refresh(); if (submit.disabled || lessonView?.current !== content) return;
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
    solution.append(el('h3', 'solution-heading', 'Solution:'), markdown(step.solution)); card.append(solution);
  }
  content.append(card);
  if (!archived) {
    const controls = el('div', 'lesson-controls');
    if (short(data.status) === 'paused') {
      controls.append(actionButton('Resume →', 'primary', () => mutation('/api/resume', { taskId: data.taskId })));
    } else if (step.canContinue) {
      controls.append(actionButton('Next step →', 'primary', () => mutation('/api/continue', { taskId: data.taskId, itemId: step.itemId })));
    }
    if (controls.childElementCount) content.append(controls);
  }
  return content;
}

async function renderTask(data) {
  if (modeChanging) return;
  if (isDeveloperMode()) return openPreview({ taskId: data.taskId });
  updateHeader(data);
  const status = short(data.status);
  clock = { at: Date.now(), elapsed: Number(data.elapsedSeconds) || 0, running: !document.hidden && status === 'started' && short(data.step?.status) === 'started' };
  document.title = `Lesson${data.title ? ' · ' + data.title : ''} · Course Academy`;
  const seen = rememberTaskStep(data);
  const number = data.progress?.stepNumber ?? data.step?.stepNumber;
  const total = data.progress?.totalSteps ?? data.step?.totalSteps;
  const view = lessonShell(data, { number, total, complete: status === 'completed' });
  const buildEarlier = entry => taskContent(data, entry.step, entry.number, entry.total, true);
  if (terminal(status)) {
    const done = el('section', 'lesson-content completion');
    done.append(el('div', 'completion-mark', status === 'completed' ? '✓' : '↗'), el('h2', '', status === 'completed' ? 'Activity complete' : 'More practice needed'));
    done.append(el('p', '', status === 'completed' ? 'Your answers and progress have been saved.' : 'Your answers are saved. This attempt did not establish mastery. Return to study to continue.'));
    const earned = data.xpEarned ?? data.xp?.earned ?? (typeof data.xp === 'number' ? data.xp : null);
    if (earned !== null && earned !== undefined) {
      const xp = el('div', 'completion-xp', `${earned >= 0 ? '+' : ''}${earned} `); xp.append(el('small', '', 'XP')); done.append(xp);
    }
    done.append(el('p', '', `${duration(data.elapsedSeconds)} working time`), actionButton('Back to study →', 'primary', leaveTask));
    await showLessonStep(view, 'complete', seen.map(entry => ({ ...entry, id: String(entry.step.itemId) })), done, buildEarlier);
    return;
  }
  const step = data.step;
  if (!step) { view.feed.replaceChildren(el('p', 'notice', 'No current step is available. Return to study and try again.')); return; }
  const identity = String(step.itemId);
  const earlier = seen.filter(entry => String(entry.step.itemId) !== identity).map(entry => ({ ...entry, id: String(entry.step.itemId) }));
  await showLessonStep(view, identity, earlier, taskContent(data, step, number, total), buildEarlier);
}

$('retryButton').addEventListener('click', () => retryOperation?.());
$('homeLink').addEventListener('click', leaveTask);
document.querySelector('.brand').addEventListener('click', leaveTask);
$('courseLink').addEventListener('click', async event => {
  event.preventDefault();
  try { await explore($('courseLink').href); }
  catch (error) { showError(error, () => $('courseLink').click()); }
});
createCoursePicker({
  getSnapshot: async () => {
    if (!curriculumSnapshot) curriculumSnapshot = api('/api/graph-explorer').catch(error => { curriculumSnapshot = null; throw error; });
    return curriculumSnapshot;
  },
  getCourseId: () => currentCourseId,
  onSelectCourse: course => explore('/progress?course=' + encodeURIComponent(course.id)),
  onSelectTopic: async topic => explore(topicReferenceURL(await curriculumSnapshot, topic, currentCourseId)),
});
window.addEventListener('popstate', () => {
  const params = new URL(location.href).searchParams;
  if (isDeveloperMode() && params.has('activityId')) openPreview({ activityId: params.get('activityId') });
  else if (params.has('taskId')) openTask(params.get('taskId')); else leaveTask();
});
setInterval(() => {
  if (isDeveloperMode() || modeChanging) return;
  const timer = $('taskTimer');
  if (timer) timer.textContent = duration(clock.elapsed + (clock.running ? (Date.now() - clock.at) / 1000 : 0));
}, 1000);
async function syncAfterVisibility() {
  if (isDeveloperMode() || modeChanging) return;
  if (pendingPause) await pendingPause;
  if (busy || !task) return;
  if (document.hidden) { void pauseWhenHidden(); return; }
  if (!refreshAfterVisibility) return;
  refreshAfterVisibility = false;
  await openTask(task.taskId);
}
function pauseWhenHidden({ unloading = false } = {}) {
  if (isDeveloperMode() || modeChanging) return;
  if (pendingPause) return pendingPause;
  if (!task || short(task.status) !== 'started') return;
  const taskId = task.taskId;
  stopClock();
  refreshAfterVisibility = true;
  // A hidden page waits for an in-flight answer or continuation before pausing
  // the resulting current item, rather than racing the two writes.
  if (busy && !unloading) return;
  pendingPause = api('/api/pause', { taskId, requestId: crypto.randomUUID() }, { keepalive: true })
    .then(() => { if (task?.taskId === taskId) task.status = 'paused'; })
    .catch(() => { /* Re-read authoritative state when the page becomes visible. */ })
    .finally(() => { pendingPause = null; if (!document.hidden) void syncAfterVisibility(); });
  return pendingPause;
}
function refreshPageOnReturn() {
  if (document.hidden || modeChanging) return;
  if (task) {
    if (isDeveloperMode()) return;
    refreshAfterVisibility = true;
    return syncAfterVisibility();
  }
  // Keep the list visible during the request and avoid interrupting a lesson
  // that is still opening. home() shares any already-running queue request.
  if (!busy) return home({ preserve: true });
}
document.addEventListener('visibilitychange', () => {
  if (document.hidden) pauseWhenHidden(); else void refreshPageOnReturn();
});
window.addEventListener('pagehide', () => pauseWhenHidden({ unloading: true }));
window.addEventListener('pageshow', event => {
  if (event.persisted) void refreshPageOnReturn();
});

const initialParams = new URL(location.href).searchParams;
if (isDeveloperMode() && initialParams.has('activityId')) openPreview({ activityId: initialParams.get('activityId') });
else if (initialParams.has('taskId')) openTask(initialParams.get('taskId')); else home();

for (const event of ['course-academy:developer-mode-changing', 'course-academy:profile-changing']) window.addEventListener(event, () => {
  modeChanging = true;
  settingsRevision++;
  clock.running = false;
  drafts.clear(); retryOperation = null;
  homeController?.abort();
  homeController = null; homeRequest = null;
  setBusy(true);
  renderGeneration++;
});
window.addEventListener('course-academy:developer-mode-settled', event => {
  modeChanging = false;
  // Enter inspection at the same activity; leaving it never starts a real attempt.
  if (event.detail.enabled && task?.activityId) void openPreview({ activityId: task.activityId });
  else {
    history.replaceState(null, '', '/home');
    void home({ preserve: true });
  }
});
window.addEventListener('course-academy:profile-changed', event => {
  modeChanging = false; curriculumSnapshot = null; queueRequest = null;
  refreshAfterVisibility = false;
  updateHeader(event.detail);
  history.replaceState(null, '', '/home');
  void home({ preserve: true });
});

// Changes made while browsing should refresh the study queue without interrupting a lesson.
function targetsChanged() {
  if (task) return;
  targetRevision++;
  homeRendered = false;
  if (!busy && document.visibilityState === 'visible') void home();
}
window.addEventListener('course-academy:targets-changed', targetsChanged);
window.addEventListener('storage', event => {
  if (event.key === 'course-academy-targets-changed') targetsChanged();
});
