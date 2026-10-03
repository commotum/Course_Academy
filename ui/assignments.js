import { marked } from './vendor/marked/marked.esm.js';
import { createCoursePicker, topicReferenceURL } from './navigation.js';
import { developerModeReady, isDeveloperMode } from './developer-mode.js';

await developerModeReady;

const $ = id => document.getElementById(id);
let currentCourseId = null;
let curriculumSnapshot = null;
let requestController = null;
let generation = 0;
let currentRoute = routeIdentity();
let retryOperation = null;
let mathLoader = null;
let typesetting = Promise.resolve();
let assignmentData = null;
let modeChanging = false;
let mutationPending = null;
let pendingFocusRequestId = null;
const canceledFocusRequests = new Set();
let wantedFocus = null;
let pauseRequested = false;
let receivedAt = 0;
const questionViews = new Map();
const answered = question => ['correct', 'incorrect', 'skipped'].includes(short(question.status));
const questionKey = question => String(question.stepId ?? question.id);
const entityId = value => value.entityId ?? value.id;

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function link(text, href, className = '') {
  const node = el('a', className, text); node.href = href; return node;
}
function button(text, className, action) {
  const node = el('button', className, text);
  node.type = 'button'; node.addEventListener('click', action); return node;
}
function short(value) { return String(value || '').split('/').at(-1); }
function assignmentURL(id) { return '/assignments?assignment=' + encodeURIComponent(id); }
function routeIdentity() { const url = new URL(location.href); return url.pathname + url.search; }
function topicURL(topic) { return '/topic?topic=' + encodeURIComponent(topic.uuid || topic.mathAcademyId || topic.id); }
function updateHeader(data) {
  if (data.learner) $('learnerName').textContent = data.learner.name || 'Profile';
  if (!data.course) return;
  currentCourseId = data.course.id;
  $('courseLink').href = '/progress?course=' + encodeURIComponent(data.course.id);
  try {
    const header = JSON.stringify({ courseId: data.course.id, learnerName: $('learnerName').textContent });
    if (sessionStorage.getItem('course-academy.study-header') !== header) sessionStorage.setItem('course-academy.study-header', header);
  } catch { /* The server response also fills the header when storage is unavailable. */ }
}
function dueInfo(value, now = new Date()) {
  const date = value ? new Date(value) : null;
  if (!date || !Number.isFinite(date.getTime())) return { text: 'No due date', overdue: false };
  const label = new Intl.DateTimeFormat(undefined, { month: 'short', day: 'numeric', ...(date.getFullYear() !== now.getFullYear() ? { year: 'numeric' } : {}) }).format(date);
  const overdue = date.getTime() < now.getTime();
  const today = date.toDateString() === now.toDateString();
  return { text: overdue ? `Overdue · ${label}` : today ? 'Due today' : `Due ${label}`, overdue, date };
}
function dueBadge(value) {
  const due = dueInfo(value);
  const badge = el(due.date ? 'time' : 'span', 'assignment-due' + (due.overdue ? ' overdue' : ''), due.text);
  if (due.date) { badge.dateTime = due.date.toISOString(); badge.title = due.date.toLocaleString(); }
  return badge;
}
function problemCount(value) { const count = Number(value) || 0; return `${count} ${count === 1 ? 'problem' : 'problems'}`; }
function escapeHTML(text) { return String(text).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]); }
function assetURL(value) {
  if (!value) return '';
  if (String(value).startsWith('/api/asset?')) return value;
  return '/api/asset?path=' + encodeURIComponent(String(value).replace(/^file:\/\//, ''));
}
function fieldLabel(key, index) {
  if (!key || key === 'selection') return 'Answer';
  const numbered = /^field-(\d+)$/.exec(key);
  return numbered ? `Answer ${numbered[1]}` : `Answer ${index + 1}`;
}
function markdown(value, fields = []) {
  const container = el('div', 'prose');
  // Match the lesson and topic renderers: preserve TeX before Markdown parsing.
  const math = [];
  const prefix = 'CAMATH' + crypto.randomUUID().replaceAll('-', '') + 'TOKEN';
  const placeholder = /\{\{(?:answer-field:)?([^}]+)\}\}/g;
  const fieldIndex = key => fields.findIndex(field => field.key === key);
  let source = String(value || '').replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g, match => {
    math.push(match.replace(placeholder, (whole, key) => fieldIndex(key) < 0 ? whole : `\\underbrace{\\qquad}_{\\text{answer ${fieldIndex(key) + 1}}}`));
    return prefix + (math.length - 1) + 'END';
  });
  source = source.replace(placeholder, (whole, key) => fieldIndex(key) < 0 ? whole : `<span class="field-location">${escapeHTML(fieldLabel(key, fieldIndex(key)))}</span>`);
  let html = marked.parse(source, { async: false, gfm: true, breaks: false });
  html = html.replace(new RegExp(prefix + '(\\d+)END', 'g'), (_, i) => escapeHTML(math[Number(i)]));
  const fragment = DOMPurify.sanitize(html, {
    RETURN_DOM_FRAGMENT: true, USE_PROFILES: { html: true },
    FORBID_TAGS: ['style', 'form', 'input', 'button', 'textarea', 'select', 'iframe', 'object', 'embed', 'video', 'audio'],
    FORBID_ATTR: ['style', 'srcset', 'id', 'name'],
  });
  for (const image of fragment.querySelectorAll('img')) {
    image.src = assetURL(image.getAttribute('src')); image.referrerPolicy = 'no-referrer'; image.loading = 'lazy';
    image.addEventListener('error', () => image.replaceWith(el('span', 'math-error', `Image unavailable${image.alt ? ': ' + image.alt : '.'}`)), { once: true });
  }
  for (const anchor of fragment.querySelectorAll('a')) {
    const href = anchor.getAttribute('href') || '';
    if (!/^https?:\/\//i.test(href) && !href.startsWith('/api/source?path=')) anchor.removeAttribute('href');
    else { anchor.target = '_blank'; anchor.rel = 'noopener noreferrer'; }
  }
  container.append(fragment);
  if (math.length) container.dataset.math = 'true';
  return container;
}
function answerValue(answer) {
  if (short(answer.type) === 'image') {
    const holder = el('div', 'prose'); const image = el('img');
    image.src = assetURL(answer.value); image.alt = 'Answer option'; image.loading = 'lazy';
    holder.append(image); return holder;
  }
  const value = String(answer.value ?? '');
  return markdown(short(answer.type) === 'math' && !/^\s*(\$|\\\[|\\\()/.test(value) ? '$' + value + '$' : value);
}
function fieldControl(field, question, index) {
  const set = el('fieldset', 'answer-field');
  set.dataset.fieldId = String(entityId(field));
  const label = field.key === 'selection' ? 'Choose an answer' : fieldLabel(field.key, index);
  set.append(el('legend', '', label));
  const response = field.response;
  const responseId = response?.choiceId ?? response?.entityId ?? response?.id;
  const name = `assignment-${questionKey(question)}-${entityId(field)}`;
  const type = short(field.type);
  if (type === 'blank') {
    const input = el('input', 'answer-input');
    input.type = 'text'; input.name = name; input.autocomplete = 'off'; input.spellcheck = false;
    input.setAttribute('aria-label', label); input.value = response?.value ?? '';
    input.placeholder = 'Enter your answer'; set.append(input);
  } else if (type === 'radio') {
    const choices = el('div', 'choices');
    for (const choice of field.choices || []) {
      const row = el('label', 'choice');
      const input = el('input'); input.type = 'radio'; input.name = name;
      input.value = String(entityId(choice)); input.checked = String(responseId) === input.value;
      row.append(input, answerValue(choice)); choices.append(row);
    }
    set.append(choices);
  } else if (type === 'select') {
    const previews = el('div', 'select-options');
    const select = el('select', 'answer-select'); select.name = name; select.setAttribute('aria-label', label);
    const placeholder = el('option', '', 'Select an answer…'); placeholder.value = ''; select.append(placeholder);
    (field.choices || []).forEach((choice, optionIndex) => {
      const letter = String.fromCharCode(65 + optionIndex);
      const preview = el('div', 'option-preview');
      preview.append(el('div', 'option-label', letter), answerValue(choice)); previews.append(preview);
      const option = el('option', '', letter + (short(choice.type) === 'text' ? ' · ' + choice.value : ''));
      option.value = String(entityId(choice)); option.selected = String(responseId) === option.value;
      select.append(option);
    });
    set.append(previews, select);
  }
  return set;
}
function collectResponses(view) {
  return (view.question.fields || []).map(field => {
    const set = [...view.form.querySelectorAll('fieldset')].find(node => node.dataset.fieldId === String(entityId(field)));
    if (short(field.type) === 'blank') return { fieldId: entityId(field), value: set?.querySelector('input')?.value || '' };
    const control = set?.querySelector('input:checked, select');
    return { fieldId: entityId(field), choiceId: control?.value ? Number(control.value) : '' };
  });
}
function activeQuestion(question) { return short(question.status) === 'started' && !pauseRequested; }
function duration(seconds) {
  const value = Math.max(0, Math.floor(Number(seconds) || 0));
  return `${Math.floor(value / 60)}:${String(value % 60).padStart(2, '0')}`;
}
function refreshControls() {
  for (const view of questionViews.values()) {
    const question = view.question;
    const editable = question.gradable === true && !question.isExample && (assignmentData?.preview || !answered(question));
    const disabled = modeChanging || !editable || view.submitting;
    for (const input of view.form?.querySelectorAll('input,select') || []) input.disabled = disabled;
    if (view.check) {
      const valid = collectResponses(view).every(response => response.choiceId || typeof response.value === 'string' && response.value.trim());
      view.check.disabled = disabled || Boolean(mutationPending || pendingPause || retryOperation) || !valid || (!assignmentData?.preview && !activeQuestion(question));
    }
    if (view.work) {
      view.work.textContent = activeQuestion(question) ? 'Pause question' : question.itemId ? 'Resume question' : 'Work on this question';
      view.work.disabled = modeChanging || Boolean(mutationPending || pendingPause || retryOperation) || answered(question);
      view.work.hidden = answered(question);
    }
    view.node.classList.toggle('is-active', !assignmentData?.preview && activeQuestion(question));
  }
  refreshTimers();
}
function refreshTimers() {
  if (isDeveloperMode() || modeChanging || !assignmentData) return;
  const delta = document.hidden ? 0 : Math.max(0, (Date.now() - receivedAt) / 1000);
  for (const view of questionViews.values()) {
    if (!view.timer) continue;
    const question = view.question;
    view.timer.hidden = !question.itemId;
    view.timer.textContent = `${activeQuestion(question) ? 'Working' : answered(question) ? 'Time spent' : 'Paused'} · ${duration((Number(question.elapsedSeconds) || 0) + (activeQuestion(question) ? delta : 0))}`;
  }
}
function renderQuestionFeedback(view) {
  const question = view.question;
  view.result.replaceChildren();
  if (answered(question)) {
    const feedback = el('div', 'feedback'); feedback.setAttribute('role', 'status');
    const label = short(question.status) === 'correct' ? '✓ Correct' : short(question.status) === 'skipped' ? 'Skipped' : 'Incorrect';
    feedback.append(el('div', 'feedback-heading', label + (assignmentData.preview ? ' · Preview only' : '')));
    if (question.feedback) feedback.append(markdown(question.feedback));
    for (const field of question.fields || []) if (field.response?.feedback) feedback.append(markdown(field.response.feedback));
    view.result.append(feedback);
  }
  const expose = assignmentData.preview || question.isExample || answered(question);
  if (expose && (question.solution || question.fields?.some(field => field.correctAnswer))) {
    const solution = el('details', 'worked-solution');
    solution.open = Boolean(question.isExample);
    solution.append(el('summary', 'section-label', 'Worked solution and answer key'));
    (question.fields || []).forEach((field, index) => {
      if (!field.correctAnswer) return;
      solution.append(el('p', 'response-summary', fieldLabel(field.key, index) + ' · correct answer:'), answerValue(field.correctAnswer));
      if (field.correctAnswer.feedback) solution.append(markdown(field.correctAnswer.feedback));
    });
    if (question.solution) solution.append(markdown(question.solution));
    solution.addEventListener('toggle', () => { if (solution.open) void typeset(solution); });
    view.result.append(solution);
  }
  void typeset(view.result);
}
function questionView(question) {
  const node = el('section', 'assignment-question');
  const key = questionKey(question);
  node.dataset.question = key;
  const meta = el('div', 'step-meta');
  if (question.isExample) meta.append(el('span', 'step-tag', 'Worked example'));
  if (question.requiresCalculator) meta.append(el('span', '', 'Calculator required'));
  if (question.difficulty) meta.append(el('span', '', short(question.difficulty)));
  if (meta.childElementCount) node.append(meta);
  node.append(markdown(question.problem, question.fields || []));
  const view = { key, question, node, form: null, result: el('div', 'assignment-result'), submitting: false };
  const fields = question.fields || [];
  if (fields.length && fields.every(field => ['blank', 'radio', 'select'].includes(short(field.type)))) {
    const form = el('form'); view.form = form;
    const fieldList = el('div', 'answer-fields'); view.fieldList = fieldList;
    fields.forEach((field, index) => fieldList.append(fieldControl(field, question, index)));
    form.append(fieldList);
    if (question.gradable && !question.isExample) {
      const actions = el('div', 'answer-actions assignment-question-actions');
      if (!assignmentData.preview) {
        view.timer = el('span', 'timer'); actions.append(view.timer);
        view.work = button('Work on this question', 'secondary', () => {
          if (activeQuestion(view.question)) void pauseAssignment();
          else { wantedFocus = key; void focusWantedQuestion(); }
        });
        actions.append(view.work);
      }
      const check = el('button', 'primary', assignmentData.preview ? 'Check preview answer' : 'Check answer');
      check.type = 'submit'; view.check = check; actions.append(check); form.append(actions);
      form.addEventListener('focusin', event => {
        if (!event.target.matches('input,select') || assignmentData.preview || modeChanging || answered(view.question)) return;
        wantedFocus = key; void focusWantedQuestion();
      });
      form.addEventListener('input', refreshControls); form.addEventListener('change', refreshControls);
      form.addEventListener('submit', event => { event.preventDefault(); refreshControls(); if (!check.disabled) void submitQuestion(view); });
    } else if (!question.isExample) form.append(el('p', 'assignment-note', 'This question is not configured for automatic checking.'));
    node.append(form);
  }
  node.append(view.result);
  questionViews.set(key, view);
  renderQuestionFeedback(view);
  return node;
}
function questions(content, result = []) {
  if (!content) return result;
  if (short(content.kind) === 'question') result.push(content);
  else if (content.content && typeof content.content === 'object') questions(content.content, result);
  else for (const step of content.steps || []) questions(step.content, result);
  return result;
}
function applyAssignment(data, requestGeneration) {
  if (requestGeneration !== generation || modeChanging || Boolean(data.preview) !== Boolean(assignmentData?.preview)) return;
  if (Number(data.basis) < Number(assignmentData?.basis)) return;
  assignmentData = data; receivedAt = Date.now(); updateHeader(data);
  for (const step of data.assignment.steps || []) for (const question of questions(step.content)) {
    const view = questionViews.get(questionKey(question));
    if (!view) continue;
    const responseChanged = answered(question) && JSON.stringify(question.fields) !== JSON.stringify(view.question.fields);
    const feedbackChanged = JSON.stringify([question.status, question.feedback, question.solution, question.fields]) !== JSON.stringify([view.question.status, view.question.feedback, view.question.solution, view.question.fields]);
    view.question = question;
    // Keep every other form mounted, including unsent values and keyboard focus.
    if (responseChanged && view.fieldList) {
      view.fieldList.replaceChildren(...question.fields.map((field, index) => fieldControl(field, question, index)));
      void typeset(view.fieldList);
    }
    if (feedbackChanged) renderQuestionFeedback(view);
  }
  refreshControls();
}
function coverage(topics) {
  const section = el('div', 'assignment-coverage');
  section.append(el('p', 'section-label', 'Preparation topics'));
  const list = el('ul', 'coverage-links');
  for (const topic of topics) { const row = el('li'); row.append(link(topic.title || topic.name, topicURL(topic))); list.append(row); }
  section.append(list); return section;
}
function contentView(content) {
  const body = el('div', 'assignment-content');
  if (!content) { body.append(el('p', 'assignment-note', 'Problem content is not available.')); return body; }
  switch (short(content.kind)) {
    case 'assigned-problem':
      body.append(contentView(content.content));
      if (content.topicCoverage?.length) body.append(coverage(content.topicCoverage));
      break;
    case 'question': {
      body.append(questionView(content));
      break;
    }
    case 'multistep': {
      if (content.context) { const context = el('section', 'assignment-context'); context.append(el('p', 'section-label', 'Shared context'), markdown(content.context)); body.append(context); }
      const parts = el('div', 'assignment-parts');
      for (const [index, step] of (content.steps || []).entries()) {
        const part = el('section', 'assignment-part');
        if (step.title) part.append(el('h3', 'step-title', step.title));
        else part.append(el('h3', 'step-title', `Part ${index + 1}`));
        part.append(contentView(step.content)); parts.append(part);
      }
      body.append(parts); break;
    }
    case 'tutorial': body.append(markdown(content.content)); break;
    default: body.append(el('p', 'assignment-note', 'This content is not available in the assignment view yet.'));
  }
  return body;
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
async function api(path, body = null, options = {}) {
  if (body && (modeChanging || isDeveloperMode() && path !== '/api/preview-answer')) throw new Error('Developer mode does not record activity.');
  const response = await fetch(path, {
    method: body ? 'POST' : 'GET', cache: 'no-store', credentials: 'same-origin',
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined, ...options,
  });
  let result;
  try { result = await response.json(); } catch { throw new Error('The assignments server did not return a response. Try again.'); }
  if (!response.ok || result.error) {
    const error = new Error(result.error || `The request failed (${response.status}).`);
    error.status = response.status; error.code = result.code; throw error;
  }
  return result;
}
function clearError() { $('errorBanner').hidden = true; retryOperation = null; }
function showError(error, retry) {
  $('errorText').textContent = error.message || String(error); $('errorBanner').hidden = false;
  $('retryButton').hidden = !retry; retryOperation = retry || null;
}
function focusCancellation() {
  return pendingFocusRequestId ? { cancelFocusRequestId: pendingFocusRequestId } : {};
}
function cancelFocusRetry(body) {
  if (!body.cancelFocusRequestId) return;
  canceledFocusRequests.add(body.cancelFocusRequestId);
  if (retryOperation?.focusRequestId === body.cancelFocusRequestId) clearError();
}
function confirmFocusCancellation(body) {
  if (body.cancelFocusRequestId === pendingFocusRequestId) pendingFocusRequestId = null;
}
function applyPreview(view, result) {
  const checked = result.step || result;
  const original = view.question;
  const fields = original.fields.map(field => {
    const graded = checked.fields?.find(candidate => String(entityId(candidate)) === String(entityId(field)));
    return graded ? { ...field, ...graded, id: field.id, entityId: entityId(field), choices: field.choices } : field;
  });
  view.question = { ...original, ...checked, id: original.id, entityId: original.entityId, stepId: original.stepId, gradable: original.gradable, fields };
  renderQuestionFeedback(view);
}
function runMutation(operation) {
  if (mutationPending || modeChanging) return mutationPending;
  const requestGeneration = generation;
  const focusRequestId = operation.path === '/api/assignment-focus' ? operation.body.requestId : null;
  if (focusRequestId && canceledFocusRequests.has(focusRequestId)) return;
  if (focusRequestId) pendingFocusRequestId = focusRequestId;
  if (operation.path === '/api/assignment-pause') cancelFocusRetry(operation.body);
  if (operation.view) operation.view.submitting = true;
  clearError();
  const work = (async () => {
    try {
      const data = await api(operation.path, operation.body);
      if (focusRequestId && pendingFocusRequestId === focusRequestId) pendingFocusRequestId = null;
      if (operation.path === '/api/assignment-pause') confirmFocusCancellation(operation.body);
      if (requestGeneration !== generation || modeChanging) return;
      if (operation.preview) applyPreview(operation.view, data);
      else {
        if (operation.path === '/api/assignment-pause') pauseRequested = false;
        applyAssignment(data, requestGeneration);
      }
      if (operation.path.includes('answer')) $('announcement').textContent = `${short(operation.view.question.status) === 'correct' ? 'Correct.' : 'Answer checked.'}${operation.preview ? ' Preview only; nothing recorded.' : ''}`;
    } catch (error) {
      // A failed connection or server error can leave focus committed. Keep
      // its identity so a later pause can cancel even the first unseen task.
      if (focusRequestId && error.status >= 400 && error.status < 500 && pendingFocusRequestId === focusRequestId) pendingFocusRequestId = null;
      if (requestGeneration !== generation || modeChanging) return;
      if (focusRequestId && canceledFocusRequests.has(focusRequestId)) return;
      // An uncertain outcome must replay exactly the same request. Only a
      // definite basis conflict permits a new operation identity.
      if (error.code === 'basis-conflict' && operation.body.requestId) operation.body.requestId = crypto.randomUUID();
      showError(error, () => runMutation(operation));
      if (focusRequestId) retryOperation.focusRequestId = focusRequestId;
    } finally {
      if (operation.view) operation.view.submitting = false;
      mutationPending = null;
      if (!modeChanging) refreshControls();
      if (requestGeneration === generation && !modeChanging) {
        if (!operation.preview && document.hidden && operation.path === '/api/assignment-focus') void pauseWhenHidden();
        else if (!retryOperation) void focusWantedQuestion();
      }
    }
  })();
  mutationPending = work; refreshControls(); return work;
}
function focusWantedQuestion() {
  if (!wantedFocus || mutationPending || pendingPause || retryOperation || isDeveloperMode() || modeChanging || document.hidden) return;
  const view = questionViews.get(wantedFocus);
  if (!view || answered(view.question) || !view.question.gradable || activeQuestion(view.question)) return;
  pauseRequested = false;
  return runMutation({ path: '/api/assignment-focus', body: { assignmentId: assignmentData.assignment.id, stepId: view.question.stepId, requestId: crypto.randomUUID() } });
}
function pauseAssignment() {
  if (!assignmentData || isDeveloperMode() || modeChanging || mutationPending || pendingPause) return;
  wantedFocus = null;
  return runMutation({ path: '/api/assignment-pause', body: { assignmentId: assignmentData.assignment.id, ...focusCancellation(), requestId: crypto.randomUUID() } });
}
function submitQuestion(view) {
  const preview = Boolean(assignmentData.preview);
  if (mutationPending || pendingPause || modeChanging || !preview && !activeQuestion(view.question)) return;
  wantedFocus = null; view.submitting = true;
  return runMutation({ view, preview,
    path: preview ? '/api/preview-answer' : '/api/assignment-answer',
    body: preview
      ? { activityId: assignmentData.assignment.entityId, questionId: view.question.entityId, responses: collectResponses(view) }
      : { taskId: assignmentData.assignment.taskId, itemId: view.question.itemId, responses: collectResponses(view), requestId: crypto.randomUUID() },
  });
}
let pendingPause = null;
let unloadPauseSent = false;
function pauseWhenHidden(unloading = false) {
  if (isDeveloperMode() || modeChanging || !assignmentData || (!assignmentData.assignment.taskId && !mutationPending && !pendingFocusRequestId)) return;
  wantedFocus = null; pauseRequested = true;
  const requestGeneration = generation;
  const assignmentId = assignmentData.assignment.id;
  const cancellation = focusCancellation();
  const sendPause = async body => {
    cancelFocusRetry(body);
    try {
      const data = await api('/api/assignment-pause', body, { keepalive: true });
      confirmFocusCancellation(body);
      if (requestGeneration !== generation || modeChanging) return;
      pauseRequested = false; applyAssignment(data, requestGeneration);
    } catch (error) {
      // A background pause must not replace an uncertain answer's exact retry.
      if (requestGeneration === generation && !modeChanging && !retryOperation) showError(error, () => runMutation({ path: '/api/assignment-pause', body }));
    }
  };
  // A page can unload before first-focus returns its new task id. Send a
  // keepalive fallback then; normal visibility pauses wait for focus to settle.
  if (unloading && mutationPending && !unloadPauseSent) {
    unloadPauseSent = true;
    void sendPause({ assignmentId, ...cancellation, requestId: crypto.randomUUID() });
  }
  if (pendingPause) return pendingPause;
  const body = { assignmentId, ...cancellation, requestId: crypto.randomUUID() };
  const work = (async () => {
    if (mutationPending) await mutationPending;
    if (requestGeneration !== generation || modeChanging || isDeveloperMode()) return;
    await sendPause(body);
  })().finally(() => {
    if (pendingPause === work) pendingPause = null;
    if (requestGeneration === generation && !modeChanging) { refreshControls(); if (!retryOperation) void focusWantedQuestion(); }
  });
  pendingPause = work; refreshControls();
  return work;
}
async function syncAfterVisibility() {
  if (isDeveloperMode() || modeChanging || !assignmentData) return;
  unloadPauseSent = false;
  if (pendingPause) await pendingPause;
  if (mutationPending) await mutationPending;
  if (document.hidden || modeChanging) return;
  const requestGeneration = generation;
  try { applyAssignment(await api('/api/assignment?assignment=' + encodeURIComponent(assignmentData.assignment.id)), requestGeneration); }
  catch (error) { if (requestGeneration === generation && !retryOperation) showError(error, syncAfterVisibility); }
}
async function leaveAssignment(url, pauseBody = null) {
  if (isDeveloperMode() || modeChanging || !assignmentData) { location.assign(url); return; }
  if (mutationPending) await mutationPending;
  if (pendingPause) await pendingPause;
  if (modeChanging) return;
  wantedFocus = null;
  const body = pauseBody || { assignmentId: assignmentData.assignment.id, ...focusCancellation(), requestId: crypto.randomUUID() };
  cancelFocusRetry(body);
  try { await api('/api/assignment-pause', body, { keepalive: true }); confirmFocusCancellation(body); location.assign(url); }
  catch (error) { showError(error, () => leaveAssignment(url, body)); refreshControls(); }
}
function assignmentRow(assignment, index) {
  const row = el('article', 'queue-card');
  const info = el('div');
  const meta = el('div', 'queue-meta'); meta.append(dueBadge(assignment.due), el('span', '', problemCount(assignment.problemCount)));
  if (assignment.status && ['completed', 'failed'].includes(short(assignment.status))) meta.append(el('span', '', short(assignment.status)));
  const heading = el('h2'); heading.append(link(assignment.title, assignmentURL(assignment.id)));
  info.append(meta, heading);
  row.append(el('span', 'queue-number', String(index + 1).padStart(2, '0')), info, link('View assignment', assignmentURL(assignment.id), 'primary'));
  return row;
}
function renderList(data) {
  document.title = 'Assignments · Course Academy';
  const head = el('div', 'page-heading');
  const intro = el('div'); intro.append(el('p', 'eyebrow', 'Your study desk'), el('h1', '', 'Assignments'), el('p', 'subheading', 'Your schoolwork, with the topics you need to prepare.'));
  head.append(intro, button('Refresh ↻', 'small-button', load));
  const queue = el('section', 'queue assignment-queue'); queue.setAttribute('aria-label', 'Assignments by due date');
  const assignments = data.assignments || [];
  const pending = assignments.filter(assignment => short(assignment.status) !== 'completed');
  const completed = assignments.filter(assignment => short(assignment.status) === 'completed');
  pending.forEach((assignment, index) => queue.append(assignmentRow(assignment, index)));
  if (!pending.length) {
    const empty = el('div', 'empty-state');
    empty.append(el('h2', '', completed.length ? 'All assignments completed' : 'No assignments yet'), el('p', '', completed.length ? 'Completed assignments are available below.' : 'Your imported assignments will appear here.'));
    queue.append(empty);
  }
  $('main').append(head, queue);
  if (assignments.length) {
    const foot = el('div', 'queue-foot'); foot.append(el('span', '', `${pending.length} ${pending.length === 1 ? 'assignment' : 'assignments'}`), el('span', '', 'Earliest deadlines first · Undated assignments last')); $('main').append(foot);
  }
  if (completed.length) {
    const section = el('section', 'assignment-completed'); section.append(el('h2', '', 'Completed'));
    const list = el('div', 'queue'); completed.forEach((assignment, index) => list.append(assignmentRow(assignment, index))); section.append(list); $('main').append(section);
  }
  $('announcement').textContent = `${pending.length} assignments.`;
}
function renderAssignment(data) {
  assignmentData = data; receivedAt = Date.now(); questionViews.clear();
  const assignment = data.assignment;
  document.title = `${assignment.title} · Course Academy`;
  $('main').className = 'assignment-main';
  const topline = el('div', 'lesson-topline'); topline.append(link('← Assignments', '/assignments', 'text-button'));
  if (data.preview) topline.append(el('span', '', 'Developer mode · Nothing recorded'));
  const heading = el('header', 'assignment-heading');
  heading.append(el('p', 'eyebrow', 'Assignment'), el('h1', '', assignment.title));
  const facts = el('div', 'assignment-facts'); facts.append(dueBadge(assignment.due), el('span', '', problemCount(assignment.problemCount ?? assignment.steps?.filter(step => short(step.content?.kind) === 'assigned-problem').length)));
  heading.append(facts);
  const problems = el('div', 'assignment-problems');
  const toc = el('nav', 'assignment-toc'); toc.setAttribute('aria-label', 'Assignment problems');
  let number = 0;
  for (const step of assignment.steps || []) {
    const isProblem = short(step.content?.kind) === 'assigned-problem';
    const section = el('section', isProblem ? 'assignment-problem' : 'assignment-description');
    if (isProblem) {
      number++;
      section.id = 'problem-' + number;
      const title = step.title || `Problem ${number}`;
      section.append(el('h2', 'step-title', title)); toc.append(link(title, '#' + section.id));
    } else if (step.title || step.content?.title) section.append(el('h2', 'step-title', step.title || step.content.title));
    const card = el('div', 'content-card'); card.append(contentView(step.content)); section.append(card); problems.append(section);
  }
  if (toc.childElementCount > 1) heading.append(toc);
  $('main').append(topline, heading, problems);
  refreshControls();
  $('announcement').textContent = `${assignment.title}. ${problemCount(number)}.`;
  const initialHash = location.hash;
  void typeset(problems).then(() => { if (problems.isConnected && initialHash && location.hash === initialHash) document.getElementById(initialHash.slice(1))?.scrollIntoView(); });
}
async function load({ preserve = false } = {}) {
  const request = ++generation;
  currentRoute = routeIdentity();
  assignmentData = null; questionViews.clear(); wantedFocus = null; pauseRequested = false;
  requestController?.abort(); requestController = new AbortController();
  $('main').setAttribute('aria-busy', 'true'); $('errorBanner').hidden = true; retryOperation = null;
  if (!preserve) {
    if (window.MathJax?.typesetClear) MathJax.typesetClear([$('main')]);
    $('main').className = ''; $('main').replaceChildren(el('div', 'loading', 'Loading your assignments…'));
  }
  try {
    const id = new URL(location.href).searchParams.get('assignment');
    const data = await api(id ? '/api/assignment?assignment=' + encodeURIComponent(id) : '/api/assignments', null, { signal: requestController.signal });
    if (request !== generation) return;
    if (id ? !data.assignment?.title || !Array.isArray(data.assignment.steps) : !Array.isArray(data.assignments)) throw new Error('The assignment data is unavailable. Try again.');
    if (window.MathJax?.typesetClear) MathJax.typesetClear([$('main')]);
    updateHeader(data); $('main').replaceChildren();
    if (id) renderAssignment(data); else renderList(data);
  } catch (error) {
    if (request !== generation || error.name === 'AbortError') return;
    $('main').replaceChildren();
    const empty = el('section', 'empty-state'); empty.append(el('h1', '', error.status === 404 ? 'Assignment not found' : 'Unable to load assignments'), link('← Assignments', '/assignments', 'text-button')); $('main').append(empty);
    $('errorText').textContent = error.message; $('errorBanner').hidden = false; $('retryButton').hidden = false; retryOperation = load;
  } finally { if (request === generation) $('main').setAttribute('aria-busy', 'false'); }
}
function handlePopState() {
  const route = routeIdentity();
  if (route === currentRoute) return;
  currentRoute = route;
  const paused = pauseWhenHidden();
  return Promise.resolve(paused).then(load);
}
createCoursePicker({
  getSnapshot: async () => {
    if (!curriculumSnapshot) curriculumSnapshot = api('/api/graph-explorer').catch(error => { curriculumSnapshot = null; throw error; });
    return curriculumSnapshot;
  },
  getCourseId: () => currentCourseId,
  onSelectCourse: course => leaveAssignment('/progress?course=' + encodeURIComponent(course.id)),
  onSelectTopic: async topic => leaveAssignment(topicReferenceURL(await curriculumSnapshot, topic, currentCourseId)),
});
$('retryButton').addEventListener('click', () => { if (retryOperation) void retryOperation(); });
window.addEventListener('popstate', handlePopState);
document.addEventListener('click', event => {
  const anchor = event.target.closest('a[href]');
  if (!anchor || event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || anchor.target === '_blank' || anchor.hasAttribute('download')) return;
  const url = new URL(anchor.href, location.href);
  if (url.pathname === location.pathname && url.search === location.search && url.hash) return;
  if (!assignmentData || isDeveloperMode() || modeChanging || !assignmentData.assignment.taskId && !mutationPending && !pendingFocusRequestId) return;
  event.preventDefault(); void leaveAssignment(url.href);
});
document.addEventListener('visibilitychange', () => {
  if (document.hidden) void pauseWhenHidden(); else void syncAfterVisibility();
});
window.addEventListener('pagehide', () => { void pauseWhenHidden(true); });
window.addEventListener('pageshow', event => { if (event.persisted) void syncAfterVisibility(); });
for (const event of ['course-academy:developer-mode-changing', 'course-academy:profile-changing']) window.addEventListener(event, () => {
  modeChanging = true; generation++; wantedFocus = null; retryOperation = null;
  requestController?.abort(); refreshControls();
});
for (const event of ['course-academy:developer-mode-settled', 'course-academy:profile-changed']) window.addEventListener(event, () => {
  modeChanging = false; curriculumSnapshot = null;
  void load({ preserve: true });
});
setInterval(refreshTimers, 1000);
void load();
