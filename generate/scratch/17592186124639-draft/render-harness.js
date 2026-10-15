import {marked} from '/ui/vendor/marked/marked.esm.js';
import {romanLists} from '/ui/prose-lists.js';
import {checkboxControl,freeInput,choiceIndicator,fieldFeedback,blankInput,richSelect,inlinePrompt,responsesComplete} from '/ui/question-fields.js';
const short=value=>String(value||'').split('/').at(-1);
const typeset=()=>{};
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
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
    control.disabled = value || control.dataset.readOnly === 'true';
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
  if (path === '/api/start' || path === '/api/study-topic') preloadLessonRendering();
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
      task = result.task || result;
      if (path === '/api/resume' || path === '/api/start' || path === '/api/study-topic') setManualPause(task.taskId, false);
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
  let source = inlinePrompt(value, fields).replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g, match => {
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

function choiceOrder(choices, seed) {
  const hash = value => { let n = 2166136261; for (const c of value) n = Math.imul(n ^ c.charCodeAt(0), 16777619); return n >>> 0; };
  return [...choices].sort((a, b) => hash(`${seed}:${a.id}`) - hash(`${seed}:${b.id}`));
}
function fieldControl(field, readOnly, itemId, promptText = '', status = '') {
  const set = el('fieldset', 'answer-field');
  set.dataset.fieldId = String(field.id);
  set.dataset.type = short(field.type);
  const label = field.key === 'selection' ? 'Choose an answer' : fieldLabel(field.key);
  set.append(el('legend', field.key === 'selection' || short(field.type) === 'checkbox' ? 'sr-only' : '', label));
  const type = short(field.type), response = field.response;
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



window.renderRecord=async record=>{
 await MathJax.startup.promise;MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const f=q[':question/answer-fields'][0];
 const field={id:20,key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map((a,i)=>({id:100+i,type:a[':answer/type'],value:a[':answer/value']}))};
 const article=el('article','lesson-content');const card=el('div','content-card');article.append(card);document.body.append(article);
 card.append(el('p','difficulty',short(q[':question/difficulty'])||'unrated original'));
 const form=el('form');form.addEventListener('submit',e=>e.preventDefault());
 form.append(markdown(q[':question/problem'],'prose prompt',[field]));form.append(fieldControl(field,false,q[':question/id']));
 const actions=el('div','answer-actions');const check=el('button','primary','Check answer');check.type='submit';
 const refresh=()=>{check.disabled=!responsesComplete([field],collectResponses(form,[field]));};
 form.addEventListener('input',refresh);form.addEventListener('change',refresh);actions.append(check);form.append(actions);card.append(form);refresh();
 const beforeDisabled=check.disabled;const inputs=[...form.querySelectorAll('input[type=radio]')];inputs[1].click();
 const response=collectResponses(form,[field]);const selected=inputs.filter(x=>x.checked).length;
 const afterEnabled=!check.disabled;const actualSubmission=response[0].choiceId;
 const solution=el('details','worked-solution');solution.open=true;solution.append(el('summary','solution-heading','Solution:'));
 if(q[':question/worked-solution'])solution.append(markdown(q[':question/worked-solution'],'prose'));else solution.append(el('p','','Original worked solution absent.'));
 card.append(solution);await MathJax.typesetPromise([article]);
 let alignRows=[];for(const item of MathJax.startup.document.math)item.root.walkTree(n=>{if(n.kind==='mtable')alignRows.push(n.childNodes.length);});
 const clone=article.cloneNode(true);clone.querySelectorAll('mjx-container').forEach(n=>n.remove());
 return {mathjax:MathJax.version,errors:article.querySelectorAll('[data-mml-node=merror],.MathJax_Error').length,exposed:/\$|\\begin|\\end/.test(clone.innerText),overflow:article.scrollWidth>article.clientWidth,radios:inputs.length,visibleIndicators:[...article.querySelectorAll('.answer-indicator')].filter(n=>{let b=n.getBoundingClientRect(),c=getComputedStyle(n);return b.width>10&&b.height>10&&c.borderTopStyle==='solid'&&c.borderTopColor!=='rgba(0, 0, 0, 0)';}).length,beforeDisabled,afterEnabled,selected,actualSubmission,solutionOpen:solution.open,alignRows,svg:article.querySelectorAll('mjx-container svg').length};
};
