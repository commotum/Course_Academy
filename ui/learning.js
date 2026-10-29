import { decorateSourceTables } from './content-tables.js';
import { createStudySidebar } from './study-stats.js';
import { marked } from './vendor/marked/marked.esm.js';
import { romanLists } from './prose-lists.js';
import { protectMath } from './math-protection.js';
import { createCoursePicker, topicReferenceURL } from './navigation.js';
import { developerModeReady, isDeveloperMode } from './developer-mode.js';
import { attachStepMenu } from './step-menu.js';
import { loadMathInputs, inlinePrompt, mountInlineFields, richSelect, questionFeedback, feedbackHeading, blankInput, responsesComplete, checkboxControl, freeInput, choiceIndicator, fieldFeedback } from './question-fields.js';

await developerModeReady;

const $ = id => document.getElementById(id);
const terminal = status => ['completed', 'failed'].includes(status);
const answered = status => ['correct', 'incorrect', 'skipped', 'completed', 'submitted'].includes(status);
let task = null;
let busy = false;
let retryOperation = null;
let renderGeneration = 0;
let clock = { at: 0, elapsed: 0, running: false };
let assessmentClock = null;
let reviewSaveTask = null;
let reviewSavePending = false;
let reviewSaveTimer = null;
function showReviewSaveState(state, taskId) {
  if (!state) return;
  let node = document.getElementById('reviewSaveStatus');
  if (!node) {
    node = el('div', 'review-save-status'); node.id = 'reviewSaveStatus';
    node.setAttribute('role', 'status'); node.setAttribute('aria-live', 'polite');
    document.body.append(node);
  }
  clearTimeout(reviewSaveTimer);
  const settled = reviewSaveTask === taskId && reviewSavePending && state.status === 'saved';
  reviewSaveTask = taskId;
  reviewSavePending = state.status !== 'saved';
  if (settled) {
    window.dispatchEvent(new CustomEvent('course-academy:review-saved', { detail: { taskId } }));
    window.dispatchEvent(new Event('course-academy:queue-changed'));
    try { localStorage.setItem('course-academy-queue-changed', String(Date.now())); } catch { /* This tab still refreshes. */ }
  }
  node.replaceChildren();
  node.hidden = state.status === 'saved';
  node.dataset.status = state.status;
  if (state.status === 'error') {
    node.append(el('span', '', 'Answers queued · Saving needs attention. '));
    node.append(button('Retry saving', 'text-button', async () => {
      try { showReviewSaveState(await api('/api/review-save-retry', { taskId }), taskId); }
      catch { node.firstChild.textContent = 'Answers remain queued. Retry saving. '; }
    }));
    return;
  }
  if (state.status !== 'pending') return;
  node.textContent = state.retrying ? 'Answers queued · Retrying save…' : 'Saving…';
  reviewSaveTimer = setTimeout(async () => {
    if (reviewSaveTask !== taskId) return;
    try { showReviewSaveState(await api('/api/review-save-status?taskId=' + encodeURIComponent(taskId)), taskId); }
    catch { showReviewSaveState({ status: 'pending' }, taskId); }
  }, 700);
}

let typesetting = Promise.resolve();
let mathLoader = null;
const drafts = new Map();
const manuallyPausedTasks = new Set();
let timerPausePending = false;
let answerResume = null;
function manualPauseKey(id) { return 'course-academy.manual-pause.' + String(id); }
function pausedDraftKey(id) { return 'course-academy.paused-draft.' + String(id); }
function isManuallyPaused(id) {
  if (manuallyPausedTasks.has(String(id))) return true;
  try { return sessionStorage.getItem(manualPauseKey(id)) === 'true'; } catch { return false; }
}
function setManualPause(id, paused) {
  if (paused) manuallyPausedTasks.add(String(id)); else manuallyPausedTasks.delete(String(id));
  try {
    if (paused) {
      sessionStorage.setItem(manualPauseKey(id), 'true');
      sessionStorage.setItem(pausedDraftKey(id), JSON.stringify({ itemId: task?.step?.itemId, responses: drafts.get(task?.step?.itemId) || [] }));
    } else {
      sessionStorage.removeItem(manualPauseKey(id)); sessionStorage.removeItem(pausedDraftKey(id));
    }
  } catch { /* Keep the in-page pause. */ }
}
function restorePausedDraft(data) {
  if (!isManuallyPaused(data.taskId)) return;
  try {
    const saved = JSON.parse(sessionStorage.getItem(pausedDraftKey(data.taskId)) || 'null');
    if (saved?.itemId === data.step?.itemId && Array.isArray(saved.responses)) {
      drafts.set(saved.itemId, saved.responses.filter(response => data.step.fields?.some(field => field.id === response.fieldId)));
    }
  } catch { /* Ignore an unavailable or malformed local draft. */ }
}
function preloadLessonRendering() {
  void loadMath().catch(() => {});
  void loadMathInputs().catch(() => {});
}
function refreshPauseControl() {
  const control = lessonView?.pause;
  if (!control) return;
  const paused = ['paused', 'locked', 'unlocked'].includes(short(task?.status));
  control.textContent = paused ? 'Resume' : 'Pause';
  control.setAttribute('aria-label', paused ? 'Resume lesson working time' : 'Pause lesson working time');
  control.setAttribute('aria-pressed', String(paused));
  control.dataset.unavailable = String(timerPausePending);
  control.disabled = busy || timerPausePending;
  if (control.hidden) return;
  lessonView.timer.dataset.paused = String(paused);
  lessonView.timer.title = paused ? 'Working time is paused' : 'Working time';
}
async function toggleLessonPause() {
  if (busy || timerPausePending || !task || isDeveloperMode() || modeChanging || terminal(short(task.status)) || task.type === 'assessment') return;
  const paused = ['paused', 'locked', 'unlocked'].includes(short(task.status));
  if (!paused) { setManualPause(task.taskId, true); stopClock(); updateTaskTimer(); }
  timerPausePending = true;
  refreshPauseControl();
  await mutation(paused ? '/api/resume' : '/api/pause', { taskId: task.taskId });
}
let pendingPause = null;
let assessmentSaveTimer = null;
let assessmentSave = Promise.resolve();
let assessmentDraftVersion = 0;
let assessmentResponses = null;
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
  if (kind === 'question' || (!step.title && kind !== 'example')) return;
  const heading = el('h2', 'step-title');
  if (kind === 'example') heading.append(el('strong', '', 'Example:'));
  if (step.title) heading.append((kind === 'example' ? ' ' : '') + step.title);
  if (step.knowledgePoint) attachStepMenu(heading, step.knowledgePoint.id, step.knowledgePoint.mathAcademyId, { kind: 'knowledge point' });
  content.append(heading);
}
function fieldLabel(key) {
  if (!key || key === 'selection' || key === 'answer') return 'Answer';
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
  } else if (data.course === null) {
    currentCourseId = null;
    $('courseLink').setAttribute('href', '/progress');
    try { sessionStorage.removeItem('course-academy.study-header'); } catch { /* Optional cache. */ }
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
    // Keep the initiating answer usable while its resume is being confirmed.
    // Its input/change events retain the first choice or any text entered.
    control.disabled = (value && !answerResume?.form.contains(control)) || control.dataset.readOnly === 'true';
  }
  refreshPauseControl();
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
  if (path === '/api/start' || path === '/api/study-topic' || path === '/api/review-topic') preloadLessonRendering();
  const body = { ...values, requestId: crypto.randomUUID() };
  if (path === '/api/answer' && task?.type !== 'assessment') {
    body.submissionId = body.requestId;
    stopClock(); updateTaskTimer();
  }
  const revision = settingsRevision;
  let resumeBody = null;
  let expireBody = null;
  const run = async () => {
    clearError();
    setBusy(true);
    try {
      if (pendingPause) await pendingPause;
      let result;
      try { result = await api(path, body); }
      catch (error) {
        // The last visible Next/Check button can outlive a pause from another
        // tab or an unload request. Recover only a confirmed state rejection.
        if (error.code === 'basis-conflict' && path === '/api/answer' && !document.hidden && revision === settingsRevision && !modeChanging && !isDeveloperMode()) {
          // A concurrent publisher's confirmed conflict did not save the
          // answer. Replan once, retaining the original submission cutoff.
          body.requestId = crypto.randomUUID();
          result = await api(path, body);
        } else if (error.code === 'assessment-expired') {
          expireBody ||= { taskId: body.taskId, requestId: crypto.randomUUID() };
          result = await api('/api/expire', expireBody);
        } else {
          if (error.code !== 'lesson-paused' || !['/api/continue', '/api/answer', '/api/skip'].includes(path)) throw error;
          if (document.hidden || revision !== settingsRevision || modeChanging || isDeveloperMode()) {
            refreshAfterVisibility = true; return;
          }
          resumeBody ||= { taskId: body.taskId, requestId: crypto.randomUUID() };
          const resumed = await api('/api/resume', resumeBody);
          if (revision !== settingsRevision || modeChanging || isDeveloperMode()) return;
          task = resumed.task || resumed;
          rememberTaskStep(task);
          // A different tab may already have advanced this task. Refresh rather
          // than apply the old click or answers to a different presentation.
          if (task.step?.itemId !== body.itemId || short(task.status) !== 'started' || document.hidden) result = task;
          else {
            body.requestId = crypto.randomUUID();
            result = await api(path, body);
          }
        }
      }
      if (revision !== settingsRevision || modeChanging || isDeveloperMode()) return;
      const nextTask = result.task || result;
      if (['lesson', 'review'].includes(nextTask.type) && short(nextTask.status) === 'completed'
          && (task?.taskId !== nextTask.taskId || short(task?.status) !== 'completed')) {
        // Invalidate other tabs only after the completion transaction succeeds.
        try { localStorage.setItem('course-academy-queue-changed', crypto.randomUUID()); } catch { /* Other pages also refresh on return. */ }
      }
      if (path === '/api/resume' && answerResume?.taskId === nextTask.taskId && answerResume?.itemId === nextTask.step?.itemId) {
        // Snapshot controls before reconnecting them: math editors can defer
        // input events, and dropdown teardown otherwise loses its open state.
        answerResume.capture();
      }
      task = result.task || result;
      if (path === '/api/resume' || path === '/api/start' || path === '/api/study-topic' || path === '/api/review-topic') setManualPause(task.taskId, false);
      if (path === '/api/pause' || path === '/api/resume') timerPausePending = false;
      history.replaceState(null, '', '/learn?taskId=' + encodeURIComponent(task.taskId));
      await renderTask(task);
      announce(answered(task.step?.status) ? (task.step.status === 'correct' ? 'Correct.' : task.step.status === 'incorrect' ? 'Incorrect.' : task.step.status === 'submitted' ? 'Answer saved.' : 'Skipped.') : task.step?.title || 'Progress saved.');
    } catch (error) {
      if (revision !== settingsRevision) return;
      // Only a confirmed rejection may get a fresh request identity. An uncertain
      // network failure must replay the original request to avoid duplicate credit.
      if (error.code === 'basis-conflict') body.requestId = crypto.randomUUID();
      if (path === '/api/answer' && error.code === 'validation' && task?.step?.itemId === body.itemId && short(task.status) === 'started' && !document.hidden) {
        clock.at = Date.now(); clock.running = true;
      }
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
  let source = protectMath(inlinePrompt(value, fields), match => {
    math.push(match.replace(placeholder, (whole, key) => fieldKeys.has(key)
      ? `\\underbrace{\\qquad}_{\\text{answer ${fields.findIndex(field => field.key === key) + 1}}}` : whole));
    return prefix + (math.length - 1) + 'END';
  });
  source = source.replace(placeholder, (whole, key) => fieldKeys.has(key) ? `<span class="field-location">${escapeHTML(fieldLabel(key))}</span>` : whole);
  let html = marked.parse(romanLists(source), { async: false, gfm: true, breaks: false });
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
  if (container.querySelector('.source-table')) decorateSourceTables(container);
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
const stepIdentity = step => step?.itemId != null ? String(step.itemId) : step?.reviewKey;
function rememberTaskStep(data) {
  const key = `course-academy.lesson-history.${data.learner?.id || 'learner'}.${data.taskId}`;
  let seen = seenTaskSteps.get(key);
  if (!seen) {
    seen = new Map();
    try {
      const saved = JSON.parse(sessionStorage.getItem(key));
      if (Array.isArray(saved)) for (const entry of saved) {
        if (stepIdentity(entry?.step) && Number.isInteger(entry.order) && entry.order > 0) seen.set(stepIdentity(entry.step), entry);
      }
    } catch { /* Review history can still be kept in memory. */ }
    seenTaskSteps.set(key, seen);
  }
  if (Array.isArray(data.history)) {
    // The saved presentation chain is authoritative across tabs and sessions.
    seen.clear();
    for (const entry of data.history) {
      if (stepIdentity(entry?.step) && Number.isInteger(entry.order) && entry.order > 0) seen.set(stepIdentity(entry.step), entry);
    }
  }
  if (data.step?.itemId) {
    const id = String(data.step.itemId);
    const finalAssessment = data.type === 'assessment' && terminal(short(data.status));
    const order = (finalAssessment ? data.progress?.stepNumber : data.progress?.presented) || seen.get(id)?.order || seen.size + 1;
    if (!finalAssessment) for (const [item, entry] of seen) if (entry.order > order) seen.delete(item);
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
    timerPausePending = false;
    resetMain('lesson-main');
    const heading = el('h1', 'sr-only', data.title || 'Lesson');
    attachStepMenu(heading, data.activityId, null, { kind: 'activity' });
    const toolbar = el('div', 'lesson-toolbar');
    const exit = actionButton('←', 'lesson-exit text-button', leaveTask);
    exit.setAttribute('aria-label', `Exit ${data.type || 'lesson'} and return to Study`);
    exit.title = 'Back to Study';
    const track = el('div', 'progress-track'), fill = el('div', 'progress-fill');
    track.setAttribute('role', 'progressbar'); track.setAttribute('aria-label', `${data.type === 'review' ? 'Review' : data.type === 'assessment' ? 'Assessment' : 'Lesson'} progress`);
    track.setAttribute('aria-valuemin', '0'); track.append(fill);
    const position = el('span', 'lesson-position');
    const timer = el('span', 'timer', preview ? 'Preview' : duration(clock.elapsed));
    if (!preview) { timer.id = 'taskTimer'; timer.setAttribute('aria-label', 'Working time'); }
    else timer.title = 'Developer mode · Nothing recorded';
    const pause = actionButton('Pause', 'lesson-pause text-button', toggleLessonPause);
    const timing = el('div', 'lesson-timing'); timing.append(timer, pause);
    toolbar.append(exit, track, position, timing);
    const reference = el('div', 'lesson-reference');
    const reviewLink = el('a', '', 'Review topic');
    reviewLink.target = '_blank'; reviewLink.rel = 'noopener';
    reviewLink.title = 'Open the topic lesson in a new tab';
    reference.append(reviewLink);
    toolbar.append(reference);
    const feed = el('div', 'lesson-feed');
    $('main').append(heading, toolbar, feed);
    lessonView = { key, feed, track, fill, position, timer, pause, reference, reviewLink, current: null, currentId: null, history: new Map() };
  }
  lessonView.reference.hidden = preview || complete || data.type !== 'review' || !data.reviewTopic?.uuid;
  if (!lessonView.reference.hidden) {
    lessonView.reviewLink.href = '/topic?topic=' + encodeURIComponent(data.reviewTopic.uuid) + (data.course?.id ? '&course=' + encodeURIComponent(data.course.id) : '');
  }
  const maximum = Number(total) || 1;
  const completed = lessonCompletedSteps(number, total, complete);
  lessonView.track.hidden = !total;
  lessonView.track.setAttribute('aria-valuemax', String(maximum));
  lessonView.track.setAttribute('aria-valuenow', String(completed));
  lessonView.track.setAttribute('aria-valuetext', complete ? `${data.type === 'review' ? 'Review' : data.type === 'assessment' ? 'Assessment' : 'Lesson'} complete` : `Step ${number || 1} of ${maximum}`);
  lessonView.fill.style.width = `${completed / maximum * 100}%`;
  lessonView.position.textContent = total ? `${String(number || 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}` : '';
  lessonView.timer.textContent = preview ? 'Preview' : duration(clock.elapsed);
  lessonView.pause.hidden = preview || complete || data.awaitingQuestions || data.type === 'assessment';
  refreshPauseControl();
  return lessonView;
}

function archiveLessonContent(content) {
  content.dataset.history = 'true';
  for (const control of content.querySelectorAll('.lesson-controls, .answer-actions, .assessment-controls')) control.remove();
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
    // Keep earlier math editors mounted; moving custom elements reconnects them.
    if (!view.feed.contains(node)) view.feed.append(node);
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
  task = null; clock.running = false; assessmentClock = null;
  let page = $('main').querySelector('.study-activities');
  if (!preserve || !page) {
    resetMain();
    const layout = el('div', 'study-layout');
    page = el('section', 'study-activities');
    page.append(el('div', 'loading', 'Loading your next activities…'));
    layout.append(createStudySidebar(), page); $('main').append(layout);
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
    updateHeader(data); page.replaceChildren();
    document.title = 'Study · Course Academy';
    if (data.needsCourseSelection) {
      const welcome = el('section', 'empty-state');
      welcome.append(el('p', 'eyebrow', 'Your study desk'), el('h1', '', 'Choose your first course'),
        el('p', '', 'Select a course in your profile to see lessons and begin studying.'),
        actionButton('Choose a course →', 'primary', () => $('learnerName').click()));
      page.append(welcome);
      homeRendered = revision === targetRevision;
      return;
    }
    const selfDirected = data.learner?.selfDirected === true;
    page.append(el('h1', 'sr-only', selfDirected ? 'Your study plan' : 'Next up'));
    const queue = el('section', 'queue'); queue.setAttribute('aria-label', 'Next five activities');
    const activities = (data.activities || []).slice(0, 5);
    activities.forEach((activity, index) => {
      const row = el('article', 'queue-card');
      attachStepMenu(row, activity.activityId, null, { kind: 'activity' });
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
      const queueEmpty = selfDirected && !(data.learner?.queue || []).length && !(data.learner?.targets || []).length;
      empty.append(el('h2', '', queueEmpty ? 'Your study plan is empty' : 'No ready activities yet'), el('p', '', data.message || (queueEmpty ? 'Add topics to your queue or targets, or turn off self-directed mode for course recommendations.' : selfDirected ? 'Your selected topics and their required prerequisites have no unfinished lessons with enough available questions.' : 'There are no eligible activities with enough available questions.')));
      queue.append(empty);
    }
    page.append(queue);
    if (!isDeveloperMode() && data.assessmentStatus?.unavailableReason) page.append(el('p', 'notice', data.assessmentStatus.unavailableReason + '. You can continue studying.'));
    if (data.waitingActivities?.length) {
      const waiting = el('section', 'waiting-lessons');
      waiting.append(el('h2', 'step-title', 'Unfinished practice'));
      for (const activity of data.waitingActivities) {
        const row = el('div', 'waiting-lesson');
        attachStepMenu(row, activity.activityId, null, { kind: 'activity' });
        row.append(el('span', '', `${activity.title} · ${activity.pendingCount} unfinished ${activity.pendingCount === 1 ? 'skill' : 'skills'}`), actionButton(activity.canResumePractice ? 'Resume practice →' : 'Review · waiting for questions →', 'secondary', () => openTask(activity.taskId)));
        waiting.append(row);
      }
      page.append(waiting);
    }
    if (data.notice) page.append(el('p', 'notice', data.notice));
    homeRendered = revision === targetRevision;
  } catch (error) {
    if (error.code === 'basis-conflict') queueRequest = null;
    if (!signal.aborted) showError(error, home);
  }
  finally { if (!signal.aborted) setBusy(false); }
}
async function studyTopic(id, review = false) {
  if (modeChanging || busy) return;
  if (!/^[1-9]\d*$/.test(String(id)) || !Number.isSafeInteger(Number(id))) {
    showError(new Error('A valid topic entity ID is required.')); return;
  }
  homeController?.abort(); homeController = null; homeRequest = null;
  homeRendered = false;
  if (isDeveloperMode()) {
    if (review) { showError(new Error('Turn off developer mode to start a practice review.')); return; }
    return openPreview({ topicId: id });
  }
  return mutation(review ? '/api/review-topic' : '/api/study-topic', { topicId: Number(id) });
}

async function openTask(id) {
  if (modeChanging) return;
  if (isDeveloperMode()) return openPreview({ taskId: id });
  homeController?.abort(); homeController = null; homeRequest = null;
  homeRendered = false;
  clearError(); setBusy(true);
  preloadLessonRendering();
  const revision = settingsRevision;
  try {
    let data = await api('/api/task?taskId=' + encodeURIComponent(id));
    if (revision !== settingsRevision || modeChanging || isDeveloperMode()) return;
    if (data.assignment?.id) {
      location.replace('/assignments?assignment=' + encodeURIComponent(data.assignment.id));
      return;
    }
    if ((data.task || data).expired) {
      data = await api('/api/expire', { taskId: (data.task || data).taskId, requestId: crypto.randomUUID() });
    }
    if (!document.hidden && ['paused', 'locked', 'unlocked'].includes(short((data.task || data).status)) && !isManuallyPaused(id)) {
      try { data = await api('/api/resume', { taskId: (data.task || data).taskId, requestId: crypto.randomUUID() }); }
      catch (error) {
        if (error.code !== 'assessment-expired') throw error;
        data = await api('/api/expire', { taskId: (data.task || data).taskId, requestId: crypto.randomUUID() });
      }
      if (revision !== settingsRevision || modeChanging || isDeveloperMode()) return;
    }
    task = data.task || data;
    restorePausedDraft(task);
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
      if (short(task.status) === 'started') await api('/api/pause', { taskId: task.taskId, responses: task.type === 'assessment' ? assessmentResponses?.() : undefined, requestId: crypto.randomUUID() });
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
      await api('/api/pause', { taskId: task.taskId, responses: task.type === 'assessment' ? assessmentResponses?.() : undefined, requestId: crypto.randomUUID() });
      task.status = 'paused';
    }
    location.assign(url);
  } finally { setBusy(false); }
}

function choiceOrder(choices, seed) {
  const hash = value => { let n = 2166136261; for (const c of value) n = Math.imul(n ^ c.charCodeAt(0), 16777619); return n >>> 0; };
  return [...choices].sort((a, b) => hash(`${seed}:${a.id}`) - hash(`${seed}:${b.id}`));
}
function fieldControl(field, readOnly, itemId, promptText = '', status = '') {
  const set = el('fieldset', 'answer-field');
  set.dataset.fieldId = String(field.id);
  set.dataset.type = short(field.type);
  const type = short(field.type), response = field.response;
  const genericChoice = type === 'radio' && (!field.key || field.key === 'selection' || field.key === 'answer');
  const label = genericChoice || field.key === 'selection' ? 'Choose an answer' : fieldLabel(field.key);
  const legend = el('legend', genericChoice || field.key === 'selection' || type === 'checkbox' ? 'sr-only' : '');
  const legendContent = markdown(label);
  // Legends use the same sanitized math/Markdown boundary as visible choices.
  for (const paragraph of legendContent.querySelectorAll('p')) paragraph.replaceWith(...paragraph.childNodes);
  legend.append(...legendContent.childNodes);
  set.append(legend);
  const choices = choiceOrder(field.choices || [], `${itemId}:${field.id}`);
  const responseId = response?.choiceId ?? response?.id;
  const checklist = checkboxControl(field, label => answerValue({ type: 'text', value: label }), readOnly);
  if (checklist) {
    set.append(checklist);
  } else if (type === 'free') {
    set.append(freeInput(field, label, field.id, value => markdown(value), typeset, readOnly));
  } else if (type === 'blank') {
    set.append(blankInput(field, label, field.id, readOnly));
  } else if (type === 'radio') {
    const list = el('div', 'choices');
    for (const choice of choices) {
      const option = el('label', 'choice');
      const input = el('input'); input.type = 'radio'; input.name = String(field.id); input.value = String(choice.id);
      input.checked = String(responseId) === String(choice.id); input.disabled = readOnly;
      option.append(choiceIndicator(input), answerValue(choice)); list.append(option);
    }
    set.append(list);
  } else if (type === 'select') {
    const select = el('select', 'answer-select'); select.name = String(field.id); select.disabled = readOnly;
    select.setAttribute('aria-label', label);
    const placeholder = el('option', '', 'Select an answer…'); placeholder.value = ''; select.append(placeholder);
    choices.forEach(choice => {
      const option = el('option', '', choice.value);
      option.value = String(choice.id); option.selected = String(responseId) === String(choice.id); select.append(option);
    });
    select.value = responseId == null ? '' : String(responseId);
    set.append(richSelect(select, choices, answerValue, answer => answer.id, typeset));
  }
  for (const input of set.querySelectorAll('input,select,math-field,textarea,.answer-select-trigger')) {
    input.dataset.answerInput = 'true'; input.dataset.readOnly = String(readOnly);
  }
  fieldFeedback(set, field, status);
  return set;
}
function collectResponses(form, fields) {
  return fields.map(field => {
    const set = [...form.querySelectorAll('[data-field-id]')].find(node => node.dataset.fieldId === String(field.id));
    if (['blank', 'free'].includes(short(field.type))) return { fieldId: field.id, value: set.querySelector('input,math-field,textarea').value };
    const input = set.querySelector('.answer-choice-value') || set.querySelector('input:checked, select');
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
  const content = el('section', 'lesson-content');
  content.dataset.stepNumber = String(index + 1); content.dataset.totalSteps = String(data.steps.length);
  attachStepMenu(content, step.contentId, step.mathAcademyId, { kind: step.kind === 'tutorial' ? 'tutorial' : 'question' });
  const kind = short(step.kind), fields = step.fields || [];
  const card = el('div', 'content-card');
  appendStepHeading(card, step, kind);
  const prompt = markdown(step.markdown ?? step.problem ?? '', 'prose', fields);
  card.append(prompt);
  if (fields.length) {
    const form = el('form'), fieldList = el('div', 'answer-fields');
    const readOnly = archived || kind === 'example' || answered(short(step.status));
    mountInlineFields(prompt, fieldList, fields, field => fieldControl(field, readOnly, step.contentId, step.markdown ?? step.problem, step.status));
    form.append(prompt, fieldList);
    if (!readOnly) {
      const actions = el('div', 'answer-actions');
      const check = el('button', 'primary', fields.some(field => short(field.type) === 'free') ? 'Preview response' : 'Check preview answer'); check.type = 'submit'; check.dataset.action = 'true';
      const refresh = () => {
        const responses = collectResponses(form, fields);
        const valid = responsesComplete(fields, responses);
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
          announce(checked.status === 'completed' ? 'Response preview. Nothing recorded.' : checked.status === 'correct' ? 'Correct. Preview only; nothing recorded.' : 'Incorrect. Preview only; nothing recorded.');
        } catch (error) { showError(error); }
        finally { setBusy(false); }
      });
      actions.append(check); form.append(actions); refresh();
    }
    card.append(form);
  }
  if (kind === 'question' && answered(short(step.status))) {
    const feedback = el('div', 'feedback'); questionFeedback(feedback, step.status); feedback.setAttribute('role', 'status');
    feedback.append(feedbackHeading(step.status, true));
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
        solution.append(markdown(`${fieldLabel(field.key)} · ${short(field.type) === 'free' ? 'reference answer' : 'correct value'}:`, 'response-summary'), answerValue(field.correctAnswer));
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
  await loadMathInputs();
  if (modeChanging || task !== data || !isDeveloperMode()) return;
  updateHeader(data);
  document.title = `Preview${data.title ? ' · ' + data.title : ''} · Course Academy`;
  const view = lessonShell(data, { preview: true, number: previewStepIndex + 1, total: steps.length });
  if (!step) { view.feed.replaceChildren(el('p', 'notice', 'This activity has no content available to preview.')); return; }
  const earlier = steps.slice(0, previewStepIndex).map((step, index) => ({ id: `preview:${index}`, step, index }));
  await showLessonStep(view, `preview:${previewStepIndex}`, earlier,
    previewContent(data, step, previewStepIndex), entry => previewContent(data, entry.step, entry.index, true));
}

function resumeOnAnswerInteraction(form, content, data, step) {
  let pending = false, pointerDown = false, focused = null, retry = null;
  let resumeFocus = null, dropdownOpen = false, textSelection = null, mathSelection = null;
  const sameQuestion = () => task?.taskId === data.taskId && task?.step?.itemId === step.itemId;
  const targetControl = event => {
    for (const node of event.composedPath?.() || [event.target]) {
      if (node?.dataset?.answerInput === 'true') return node;
      const trigger = node?.closest?.('.answer-dropdown')?.querySelector('.answer-select-trigger');
      if (trigger && form.contains(trigger)) return trigger;
    }
    return null;
  };
  const saveDraft = () => {
    const responses = collectResponses(form, step.fields);
    drafts.set(step.itemId, responses);
    if (isManuallyPaused(data.taskId)) {
      try { sessionStorage.setItem(pausedDraftKey(data.taskId), JSON.stringify({ itemId: step.itemId, responses })); }
      catch { /* The in-page draft remains usable without storage. */ }
    }
  };
  const resume = () => {
    if (pending || busy || timerPausePending || document.hidden || modeChanging || isDeveloperMode()
      || lessonView?.current !== content || !sameQuestion()
      || !['paused', 'locked', 'unlocked'].includes(short(task.status))) return;
    pending = true;
    const attempt = { form, taskId: data.taskId, itemId: step.itemId, capture() {
      saveDraft(); resumeFocus = focused;
      dropdownOpen = focused?.classList.contains('answer-select-trigger') && focused.getAttribute('aria-expanded') === 'true';
      textSelection = typeof focused?.selectionStart === 'number'
        ? [focused.selectionStart, focused.selectionEnd, focused.selectionDirection || 'none'] : null;
      mathSelection = focused?.tagName === 'MATH-FIELD' ? JSON.parse(JSON.stringify(focused.selection)) : null;
    } };
    answerResume = attempt;
    // A failed resume retains the existing mutation's exact request identity.
    const request = retry || (() => mutation('/api/resume', { taskId: data.taskId }));
    // Finish native click/label activation before a fast resume can replace
    // the form, including the checkbox/radio change events it generates.
    void new Promise(resolve => setTimeout(resolve, 0)).then(() => {
      if (document.hidden || modeChanging || isDeveloperMode() || lessonView?.current !== content || !sameQuestion()) return;
      return request();
    }).then(() => {
      if (!sameQuestion() || document.hidden || modeChanging || isDeveloperMode()) return;
      if (short(task.status) !== 'started') {
        if (lessonView?.current === content && retryOperation) retry = retryOperation;
        return;
      }
      if (!resumeFocus || document.activeElement && document.activeElement !== document.body && !form.contains(document.activeElement)) return;
      const index = [...form.querySelectorAll('[data-answer-input]')].indexOf(resumeFocus);
      const replacement = lessonView?.current?.querySelectorAll('[data-answer-input]')[index];
      if (!replacement || replacement.disabled) return;
      replacement.focus({ preventScroll: true });
      if (textSelection && replacement.setSelectionRange) replacement.setSelectionRange(...textSelection);
      if (mathSelection) replacement.selection = mathSelection;
      // A click on a select opens its choices as well as resuming the timer.
      if (dropdownOpen) replacement.click();
    }).catch(error => showError(error)).finally(() => {
      pending = false;
      if (answerResume === attempt) answerResume = null;
    });
  };
  form.addEventListener('pointerdown', () => { pointerDown = true; });
  for (const type of ['pointerup', 'pointercancel']) form.addEventListener(type, () => { pointerDown = false; });
  form.addEventListener('focusout', event => { if (event.relatedTarget && !form.contains(event.relatedTarget)) focused = null; });
  form.addEventListener('focusin', event => {
    const control = targetControl(event); if (!control) return;
    focused = control;
    // Let a pointer click complete its native selection before a fast response
    // can replace the form. Keyboard focus can resume immediately.
    if (!pointerDown) resume();
  });
  form.addEventListener('click', event => {
    if (event.button !== 0) return;
    const control = targetControl(event); if (!control) return;
    focused = control; saveDraft(); resume();
  });
  for (const type of ['input', 'change']) form.addEventListener(type, () => { saveDraft(); resume(); });
  form.addEventListener('submit', event => event.preventDefault());
}

function taskContent(data, step, number, total, archived = false) {
  const content = el('section', 'lesson-content');
  if (number) content.dataset.stepNumber = String(number);
  if (total) content.dataset.totalSteps = String(total);
  attachStepMenu(content, step.contentId, step.mathAcademyId, { kind: step.kind === 'tutorial' ? 'tutorial' : 'question' });
  const kind = short(step.kind);
  const card = el('div', 'content-card');
  appendStepHeading(card, step, kind);
  const prompt = markdown(step.markdown ?? step.problem ?? '', 'prose', step.fields || []);
  card.append(prompt);
  const isAnswered = answered(short(step.status));
  const paused = ['paused', 'locked', 'unlocked'].includes(short(data.status));
  const resumeFromAnswer = paused && !archived && !isAnswered && !data.awaitingQuestions && ['lesson', 'review'].includes(data.type);
  const readOnly = archived || terminal(short(data.status)) || (data.type !== 'assessment' && isAnswered) || paused && !resumeFromAnswer;
  const fields = step.fields || [];
  let assessmentControls = null;
  if (kind === 'question' && fields.length) {
    const form = el('form'); form.noValidate = false;
    const fieldList = el('div', 'answer-fields');
    const draft = drafts.get(step.itemId) || [];
    mountInlineFields(prompt, fieldList, fields, field => {
      const saved = draft.find(response => response.fieldId === field.id);
      return fieldControl(!isAnswered && saved ? { ...field, response: saved } : field, readOnly, step.itemId, step.markdown ?? step.problem, step.status);
    });
    form.append(prompt, fieldList);
    if (resumeFromAnswer) resumeOnAnswerInteraction(form, content, data, step);
    if (!readOnly && !resumeFromAnswer) {
      const actions = el('div', data.type === 'assessment' ? 'assessment-actions' : 'answer-actions');
      if (data.type === 'assessment') {
        assessmentResponses = () => collectResponses(form, fields);
        const save = () => {
          const responses = assessmentResponses();
          const version = ++assessmentDraftVersion;
          drafts.set(step.itemId, responses);
          clearTimeout(assessmentSaveTimer);
          assessmentSaveTimer = setTimeout(() => {
            const request = { taskId: data.taskId, itemId: step.itemId, responses, requestId: crypto.randomUUID() };
            assessmentSave = assessmentSave.then(() => version === assessmentDraftVersion ? api('/api/draft', request) : undefined).catch(error => {
              if (error.code !== 'assessment-expired') showError(error, () => api('/api/draft', request));
            });
          }, 100);
        };
        form.addEventListener('input', save); form.addEventListener('change', save);
        form.addEventListener('submit', event => event.preventDefault());
        const move = async questionId => {
          clearTimeout(assessmentSaveTimer); ++assessmentDraftVersion; await assessmentSave;
          return mutation('/api/navigate', { taskId: data.taskId, itemId: step.itemId, questionId, responses: collectResponses(form, fields) });
        };
        const questions = data.questions || [];
        const index = questions.findIndex(q => q.questionId === step.contentId);
        const nav = el('nav', 'assessment-navigation'); nav.setAttribute('aria-label', 'Assessment questions');
        for (const question of questions) {
          const control = actionButton(String(question.number), question.active ? 'primary' : 'secondary', () => move(question.questionId));
          control.dataset.answered = String(Boolean(question.answered));
          control.setAttribute('aria-label', `Question ${question.number}, ${question.answered ? 'answered' : 'unanswered'}`);
          if (question.active) control.setAttribute('aria-current', 'step');
          nav.append(control);
        }
        assessmentControls = el('footer', 'assessment-controls');
        actions.setAttribute('role', 'group');
        actions.setAttribute('aria-label', 'Assessment actions');
        assessmentControls.append(nav, actions);
        if (index > 0) actions.append(actionButton('Previous question', 'secondary assessment-previous', () => move(questions[index - 1].questionId)));
        if (index + 1 < questions.length) actions.append(actionButton('Next question', 'secondary assessment-next', () => move(questions[index + 1].questionId)));
        actions.append(actionButton('Submit assessment', 'primary assessment-submit', async () => {
          clearTimeout(assessmentSaveTimer); ++assessmentDraftVersion; await assessmentSave;
          return mutation('/api/submit', { taskId: data.taskId, itemId: step.itemId, responses: collectResponses(form, fields) });
        }));
        for (const control of actions.children) {
          control.setAttribute('aria-label', control.textContent);
          control.title = control.textContent;
        }
      } else {
        const submit = el('button', 'primary', 'Check answer'); submit.type = 'submit'; submit.dataset.action = 'true';
        const refresh = () => {
          const responses = collectResponses(form, fields); drafts.set(step.itemId, responses);
          const valid = responsesComplete(fields, responses);
          submit.dataset.unavailable = String(!valid); submit.disabled = busy || !valid;
        };
        form.addEventListener('input', refresh); form.addEventListener('change', refresh);
        form.addEventListener('submit', event => {
          event.preventDefault(); refresh(); if (submit.disabled || lessonView?.current !== content) return;
          mutation('/api/answer', { taskId: data.taskId, itemId: step.itemId, responses: collectResponses(form, fields) });
        });
        actions.append(submit); refresh();
      }
      if (data.type !== 'assessment') form.append(actions);
    }
    card.append(form);
  }
  if (kind === 'question' && isAnswered && short(step.status) !== 'submitted') {
    const feedback = el('div', 'feedback'); questionFeedback(feedback, step.status); feedback.setAttribute('role', 'status');
    feedback.append(feedbackHeading(step.status));
    if (step.unanswered) feedback.append(el('p', 'response-summary', 'Not answered.'));
    if (step.feedback) feedback.append(markdown(step.feedback));
    for (const field of fields) {
      if (field.response?.feedback) feedback.append(markdown(field.response.feedback));
      if (step.status === 'incorrect' && field.correctAnswer) {
        feedback.append(markdown(`${field.key === 'selection' ? 'Correct answer' : fieldLabel(field.key) + ' · correct value'}:`, 'response-summary'), answerValue(field.correctAnswer));
      }
    }
    card.append(feedback);
  }
  if (step.solution && short(step.status) !== 'submitted' && (kind === 'example' || isAnswered)) {
    const solution = el('section', 'worked-solution');
    solution.append(el('h3', 'solution-heading', 'Solution:'), markdown(step.solution)); card.append(solution);
  }
  content.append(card);
  if (assessmentControls) content.append(assessmentControls);
  if (!archived) {
    const controls = el('div', 'lesson-controls');
    if (['paused', 'locked', 'unlocked'].includes(short(data.status))) {
      controls.append(actionButton('Resume →', 'primary', () => mutation('/api/resume', { taskId: data.taskId })));
    } else if (step.canContinue) {
      if (step.practiceShortage) controls.append(el('p', 'continue-hint', 'No fresh questions remain for this skill. Continue now and return to its practice later.'));
      controls.append(actionButton(step.practiceShortage ? 'Continue to next skill →' : data.type === 'assessment' && number === total ? 'Finish assessment →' : 'Next step →', 'primary', () => mutation('/api/continue', { taskId: data.taskId, itemId: step.itemId })));
    }
    if (controls.childElementCount) content.append(controls);
  }
  return content;
}

async function renderTask(data) {
  showReviewSaveState(data.saveState, data.taskId);
  if (modeChanging) return;
  if (isDeveloperMode()) return openPreview({ taskId: data.taskId });
  const revision = settingsRevision;
  await loadMathInputs();
  if (modeChanging || task !== data || revision !== settingsRevision || isDeveloperMode()) return;
  updateHeader(data);
  const status = short(data.status);
  clock = { at: Date.now(), elapsed: Number(data.elapsedSeconds) || 0, running: !document.hidden && status === 'started' && short(data.step?.status) === 'started' };
  assessmentClock = data.type === 'assessment' && !terminal(status) && Number.isFinite(data.remainingSeconds)
    ? { at: Date.now(), remaining: data.remainingSeconds } : null;
  document.title = `${data.type === 'assessment' ? 'Assessment' : data.type === 'review' ? 'Review' : 'Lesson'}${data.title ? ' · ' + data.title : ''} · Course Academy`;
  const seen = rememberTaskStep(data);
  const number = data.progress?.stepNumber ?? data.step?.stepNumber;
  const total = data.progress?.totalSteps ?? data.step?.totalSteps;
  const view = lessonShell(data, { number, total, complete: terminal(status) });
  view.timer.setAttribute('aria-label', assessmentClock ? 'Assessment time remaining' : 'Working time');
  updateTaskTimer();
  const buildEarlier = entry => taskContent(data, entry.step, entry.number, entry.total, true);
  if (data.type === 'assessment' && terminal(status) && !view.assessmentFinished) {
    // Completion returns revealed server history. Rebuild the archived cards
    // that previously contained submitted answers without correctness feedback.
    for (const node of [...view.history.values(), ...(view.current ? [view.current] : [])]) {
      if (window.MathJax?.typesetClear) MathJax.typesetClear([node]);
      node.remove();
    }
    view.history.clear(); view.current = null; view.currentId = null;
    view.assessmentFinished = true;
  }
  if (terminal(status) || data.awaitingQuestions) {
    const done = el('section', 'lesson-content completion');
    done.append(el('div', 'completion-mark', status === 'completed' ? '✓' : '↗'), el('h2', '', data.awaitingQuestions ? 'Practice paused' : status === 'completed' ? 'Activity complete' : 'More practice needed'));
    done.append(el('p', '', data.awaitingQuestions ? 'This lesson ran out of fresh questions before practice was complete for the skills below. Your answers and working time are saved.' : status === 'completed' ? 'Your answers and progress have been saved.' : 'Your answers are saved. This attempt did not establish mastery. Return to study to continue.'));
    if (data.awaitingQuestions) {
      const pending = el('ul', 'deferred-skills');
      for (const step of data.deferredSteps || []) pending.append(el('li', '', step.title));
      done.append(pending);
      if (data.canResumePractice) done.append(el('p', 'continue-hint', 'New questions are available. Resume to finish the remaining practice.'));
      done.append(data.canResumePractice
        ? actionButton('Resume unfinished practice →', 'primary', () => mutation('/api/resume', { taskId: data.taskId }))
        : el('p', 'continue-hint', 'Waiting for new questions. You can return to this lesson from Study.'));
    }
    const earned = data.xpEarned ?? data.xp?.earned ?? (typeof data.xp === 'number' ? data.xp : null);
    const base = data.xpBase ?? data.xp?.base;
    if (data.awaitingQuestions) {
      done.append(el('p', 'continue-hint', 'Lesson XP is pending until the remaining practice is finished.'));
    } else if (earned !== null && earned !== undefined) {
      const xp = el('div', 'completion-xp', `${earned}${base != null ? '/' + base : ''} `); xp.append(el('small', '', 'XP')); done.append(xp);
    }
    if (data.assessmentScore) done.append(el('p', '', `${data.assessmentScore.correct} of ${data.assessmentScore.total} correct · ${data.assessmentScore.unanswered} unanswered`));
    const completionActions = el('div', 'completion-actions');
    const targetsLink = el('a', 'small-button', 'Back to targets →'); targetsLink.href = '/?view=targets';
    completionActions.append(actionButton('Back to study →', 'primary', leaveTask), targetsLink);
    done.append(el('p', '', `${duration(data.elapsedSeconds)} working time`), completionActions);
    await showLessonStep(view, 'complete', seen.map(entry => ({ ...entry, id: stepIdentity(entry.step) })), done, buildEarlier);
    return;
  }
  const step = data.step;
  if (!step) { view.feed.replaceChildren(el('p', 'notice', 'No current step is available. Return to study and try again.')); return; }
  const identity = String(step.itemId);
  const earlier = (data.type === "assessment" && !terminal(status) ? [] : seen).filter(entry => String(entry.step.itemId) !== identity).map(entry => ({ ...entry, id: String(entry.step.itemId) }));
  await showLessonStep(view, identity, earlier, taskContent(data, step, number, total), buildEarlier);
}

function updateTaskTimer() {
  const remaining = assessmentClock ? Math.max(0, assessmentClock.remaining - (Date.now() - assessmentClock.at) / 1000) : null;
  const timer = $('taskTimer');
  if (timer) timer.textContent = remaining === null
    ? duration(clock.elapsed + (clock.running ? (Date.now() - clock.at) / 1000 : 0))
    : `${duration(remaining)} left`;
  if (remaining === 0 && task && !terminal(short(task.status)) && !busy && !document.hidden) {
    clearTimeout(assessmentSaveTimer);
    void assessmentSave.then(() => mutation('/api/expire', { taskId: task.taskId }));
  }
}

// Menu links use the same durable pause path as the other ways to leave study.
document.addEventListener('click', event => {
  const anchor = event.target.closest('a[href]');
  if (!anchor || event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || anchor.target === '_blank' || anchor.hasAttribute('download')) return;
  if (!anchor.closest('.entity-context-menu') || !task || isDeveloperMode()) return;
  event.preventDefault(); void explore(anchor.href).catch(showError);
});
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
  if (params.has('reviewTopicId')) studyTopic(params.get('reviewTopicId'), true);
  else if (params.has('topicId')) studyTopic(params.get('topicId'));
  else if (isDeveloperMode() && params.has('activityId')) openPreview({ activityId: params.get('activityId') });
  else if (params.has('taskId')) openTask(params.get('taskId')); else leaveTask();
});
setInterval(() => {
  if (isDeveloperMode() || modeChanging) return;
  updateTaskTimer();
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
  clearTimeout(assessmentSaveTimer);
  const responses = task.type === 'assessment' ? assessmentResponses?.() : undefined;
  pendingPause = assessmentSave.then(() => api('/api/pause', { taskId, responses, requestId: crypto.randomUUID() }, { keepalive: true }))
    .then(data => { if (task?.taskId === taskId) task.status = (data.task || data).status; })
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
if (initialParams.has('reviewTopicId')) studyTopic(initialParams.get('reviewTopicId'), true);
else if (initialParams.has('topicId')) studyTopic(initialParams.get('topicId'));
else if (isDeveloperMode() && initialParams.has('activityId')) openPreview({ activityId: initialParams.get('activityId') });
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
window.addEventListener('course-academy:queue-changed', targetsChanged);
window.addEventListener('storage', event => {
  if (['course-academy-targets-changed', 'course-academy-queue-changed'].includes(event.key)) targetsChanged();
});
