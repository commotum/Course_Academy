import { isDeveloperMode, developerModeReady } from './developer-mode.js';

export function createTargetControls(options) {
  return createTopicSelectionControls({ ...options, collection: 'targets' });
}

export function createQueueControls(options) {
  return createTopicSelectionControls({ ...options, collection: 'queue' });
}

// Membership always comes from the server. Storage only invalidates other
// pages; it is never used as a learner, target, or queue data source.
function createTopicSelectionControls({ readLearner, onChange = () => {}, collection }) {
  const queued = collection === 'queue';
  const changeKey = `course-academy-${collection}-changed`;
  const changeEvent = `course-academy:${collection}-changed`;
  const endpoint = queued ? '/api/queue-topic' : '/api/target';
  const noun = queued ? 'queue selection' : 'target';
  let learner = null;
  let selections = new Set();
  let pending = null;
  let revision = 0;
  let refreshNeeded = false;
  let refreshing = null;
  let profileChanging = false;
  const controls = new Set();
  const operations = new Map();
  const errors = new Map();

  function render(control) {
    const { host, button, status, topicId, title, menuItem } = control;
    const selected = selections.has(topicId);
    const operation = operations.get(topicId);
    const saving = pending === topicId;
    const action = (operation ? operation.selected : !selected) ? `Add to ${collection}` : `Remove from ${collection}`;
    host.hidden = !learner || (!queued && learner.selfDirected !== true);
    button.disabled = profileChanging || pending !== null || host.hidden || isDeveloperMode();
    button.textContent = saving ? 'Saving…' : errors.has(topicId) ? 'Retry' : selected ? (menuItem ? `Remove from ${collection}` : queued ? 'Queued' : 'Targeted') : `Add to ${collection}`;
    if (!menuItem) button.setAttribute('aria-pressed', String(selected));
    button.setAttribute('aria-busy', String(saving));
    button.setAttribute('aria-label', `${errors.has(topicId) ? 'Retry: ' : ''}${action}: ${title}`);
    button.title = isDeveloperMode() ? `${queued ? 'Queue' : 'Target'} changes are disabled in developer mode.` : action;
    status.textContent = errors.get(topicId) || '';
    if (status.textContent) button.setAttribute('aria-describedby', status.id);
    else button.removeAttribute('aria-describedby');
  }
  function renderAll() { for (const control of controls) render(control); }

  function setLearner(value) {
    revision++;
    if (learner && value?.id !== learner.id) { operations.clear(); errors.clear(); }
    learner = value || null;
    selections = new Set((learner?.[collection] || []).filter(id => Number.isSafeInteger(id) && id > 0));
    renderAll();
    onChange(learner);
  }

  async function refresh() {
    if (document.hidden || pending !== null || refreshing || !refreshNeeded) return;
    refreshNeeded = false;
    const version = revision;
    let succeeded = false;
    refreshing = (async () => {
      try {
        const value = await readLearner();
        succeeded = true;
        if (version === revision && pending === null) setLearner(value);
        else refreshNeeded = true;
      } catch { refreshNeeded = true; }
    })();
    await refreshing;
    refreshing = null;
    if (succeeded && refreshNeeded) void refresh();
  }

  async function toggle(topicId) {
    if (profileChanging || pending !== null || !learner || (!queued && learner.selfDirected !== true) || isDeveloperMode()) return;
    const operation = operations.get(topicId) || {
      action: queued ? 'queue-topic' : 'target', topicId, selected: !selections.has(topicId), requestId: crypto.randomUUID(),
    };
    operations.set(topicId, operation);
    pending = topicId; revision++; errors.delete(topicId); renderAll();
    try {
      const response = await fetch(endpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin', cache: 'no-store', body: JSON.stringify(operation),
      });
      let result;
      try { result = await response.json(); }
      catch { throw new Error('The server response was unavailable. Retry to confirm this change.'); }
      if (!response.ok || result.error) {
        const error = new Error(result.error || `Unable to save this ${noun} (${response.status}).`);
        error.code = result.code;
        throw error;
      }
      if (!result.learner || !Array.isArray(result.learner[collection])) throw new Error('Updated membership was unavailable. Retry to confirm this change.');
      operations.delete(topicId);
      setLearner(result.learner);
      try { localStorage.setItem(changeKey, crypto.randomUUID()); } catch { /* Refresh on return also works without storage. */ }
      window.dispatchEvent(new CustomEvent(changeEvent));
    } catch (error) {
      // Replaying an uncertain response must retain the original request ID.
      if (error.code === 'basis-conflict') operation.requestId = crypto.randomUUID();
      errors.set(topicId, error.message || `Unable to save this ${noun}. Try again.`);
    } finally {
      pending = null; renderAll(); void refresh();
    }
  }

  function createToggle(topic, { menuItem = false } = {}) {
    const topicId = Number(topic.id);
    if (!Number.isSafeInteger(topicId) || topicId <= 0) return null;
    const host = document.createElement('span'); host.className = 'target-control';
    const button = document.createElement('button'); button.type = 'button'; button.className = 'target-toggle';
    if (menuItem) button.setAttribute('role', 'menuitem');
    const status = document.createElement('span'); status.className = 'target-status'; status.setAttribute('role', 'status');
    status.id = 'target-status-' + crypto.randomUUID();
    const control = { host, button, status, topicId, title: topic.title || topic.name || 'Topic', menuItem };
    button.addEventListener('click', () => { void toggle(topicId); });
    host.append(button, status); controls.add(control); render(control);
    return host;
  }

  function invalidate() { refreshNeeded = true; void refresh(); }
  void developerModeReady.then(renderAll);
  window.addEventListener('course-academy:developer-mode-changing', renderAll);
  window.addEventListener('course-academy:developer-mode-changed', renderAll);
  window.addEventListener('course-academy:profile-changing', () => { profileChanging = true; renderAll(); });
  window.addEventListener('course-academy:profile-changed', event => {
    profileChanging = false;
    setLearner({ ...event.detail.learner, courseId: event.detail.course.id });
  });
  window.addEventListener('storage', event => { if (event.key === changeKey) invalidate(); });
  window.addEventListener('focus', invalidate);
  window.addEventListener('pageshow', event => { if (event.persisted) invalidate(); });
  document.addEventListener('visibilitychange', () => { if (!document.hidden) invalidate(); });

  function remove(host) {
    for (const control of controls) if (control.host === host) controls.delete(control);
  }

  return { setLearner, createToggle, remove, clear: () => controls.clear() };
}
