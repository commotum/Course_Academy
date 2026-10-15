// The server setting, shared across tabs, is authoritative. Browser storage only
// tells other pages to refresh; it never enables recording on its own.
const changeKey = 'course-academy-developer-mode-changed';
let enabled = true;
let known = false;
let changing = false;
let revision = 0;
let refreshing = null;
let operation = null;
let initialized = false;
let frozen = false;

export function isDeveloperMode() { return !known || enabled || changing || frozen; }

const toggle = document.createElement('button');
toggle.type = 'button'; toggle.className = 'profile-switch';
toggle.id = 'developerModeToggle';
toggle.setAttribute('role', 'switch');
toggle.setAttribute('aria-label', 'Developer mode');
export const developerModeControl = toggle;
const notice = document.createElement('div');
export const developerModeNotice = notice;
notice.className = 'developer-mode-error'; notice.setAttribute('role', 'alert'); notice.hidden = true;
document.body.append(notice);

function render() {
  toggle.disabled = (!known && !operation) || changing;
  // Move immediately, but keep recording gated on the confirmed server state.
  const checked = changing && operation ? operation.enabled : (known || initialized) && enabled;
  if (toggle.getAttribute('aria-checked') !== String(checked)) toggle.setAttribute('aria-checked', String(checked));
  toggle.setAttribute('aria-busy', String(changing || !known));
  toggle.title = enabled ? 'Inspection only. No timers, attempts, answers, XP, or progress are recorded.' : 'Inspect activities without recording your work. A running lesson will be paused first.';
}
function announceChange() {
  window.dispatchEvent(new CustomEvent('course-academy:developer-mode-changed', { detail: { enabled: isDeveloperMode() } }));
}
function freezePage() {
  frozen = true;
  window.dispatchEvent(new Event('course-academy:developer-mode-changing'));
}
function notifyOtherPages() {
  try { localStorage.setItem(changeKey, crypto.randomUUID()); } catch { /* Focus refresh also synchronizes tabs. */ }
}
function settlePage() {
  frozen = false;
  window.dispatchEvent(new CustomEvent('course-academy:developer-mode-settled', { detail: { enabled } }));
}
async function request(body) {
  const response = await fetch('/api/developer-mode', {
    method: body ? 'POST' : 'GET', cache: 'no-store', credentials: 'same-origin',
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  const result = await response.json();
  if (!response.ok || typeof result.enabled !== 'boolean') {
    const error = new Error(result.error || 'Developer mode could not be confirmed. Recording is disabled on this page.');
    error.code = result.code;
    throw error;
  }
  return result;
}
async function refresh() {
  if (changing || refreshing) return refreshing;
  const version = revision;
  refreshing = (async () => {
    try {
      // Resolve an uncertain toggle by replaying the same operation. A plain
      // read could race the original request and incorrectly restore recording.
      const replaying = operation !== null;
      const result = await request(operation);
      if (version !== revision) return;
      const changed = initialized && (frozen || !known || enabled !== result.enabled);
      if (changed) freezePage();
      enabled = result.enabled; known = true; frozen = false; operation = null; notice.hidden = true; render(); announceChange();
      if (replaying) notifyOtherPages();
      if (changed) settlePage();
    } catch (error) {
      if (version !== revision) return;
      if (error.code === 'basis-conflict' && operation) operation.requestId = crypto.randomUUID();
      if (initialized) freezePage();
      known = false; render(); announceChange();
      notice.textContent = error.message || 'Developer mode could not be confirmed. Refresh before studying.';
      notice.hidden = false;
    }
  })();
  await refreshing;
  refreshing = null;
  return isDeveloperMode();
}

toggle.addEventListener('click', async () => {
  if ((!known && !operation) || changing) return;
  operation ||= { enabled: !enabled, requestId: crypto.randomUUID() };
  toggle.dataset.animate = 'true';
  changing = true; revision++; render(); notice.hidden = true;
  freezePage();
  try {
    const result = await request(operation);
    enabled = result.enabled; known = true; changing = false; frozen = false; operation = null;
    render(); announceChange();
    notifyOtherPages();
    settlePage();
  } catch (error) {
    if (error.code === 'basis-conflict') operation.requestId = crypto.randomUUID();
    // Freeze the current lesson until a fresh page confirms the server state.
    // Retrying the toggle retains its request identity after an uncertain reply.
    changing = false; known = false; render(); announceChange();
    notice.textContent = (error.message || 'Unable to change developer mode.') + ' Retry the toggle or refresh this page before continuing.';
    notice.hidden = false;
  }
});

render();
export const developerModeReady = refresh().finally(() => { initialized = true; });
window.addEventListener('storage', event => { if (event.key === changeKey) void refresh(); });
window.addEventListener('focus', () => { void refresh(); });
window.addEventListener('pageshow', event => { if (event.persisted) void refresh(); });
document.addEventListener('visibilitychange', () => { if (!document.hidden) void refresh(); });
