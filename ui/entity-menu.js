// Only elements registered by the application can provide menu actions. IDs or
// action-like attributes in rendered Markdown are never trusted.
const subjects = new WeakMap();
let menu, notice, noticeTimer, manualCopy;
let current = null, returnFocus = null, generation = 0, cleanups = [], shiftHeld = false;
let anchor = { x: 8, y: 8 };

export function attachEntityMenu(element, metadata) {
  subjects.set(element, metadata);
  if (element.tabIndex == null || element.tabIndex < 0) element.tabIndex = 0;
  element.setAttribute('aria-haspopup', 'menu');
  element.setAttribute('aria-expanded', 'false');
  initialize();
}

export function detachEntityMenu(element) {
  if (current === element) closeEntityMenu();
  subjects.delete(element);
  element.removeAttribute('aria-haspopup');
  element.removeAttribute('aria-expanded');
}

export function closeEntityMenu(restoreFocus = false) {
  generation++;
  if (menu) menu.hidden = true;
  current?.setAttribute('aria-expanded', 'false');
  returnFocus?.matches?.('.entity-actions-trigger') && returnFocus.setAttribute('aria-expanded', 'false');
  for (const cleanup of cleanups.splice(0)) cleanup();
  if (restoreFocus && returnFocus?.isConnected) returnFocus.focus({ preventScroll: true });
  current = returnFocus = null;
  shiftHeld = false;
}

function position() {
  if (!menu || menu.hidden) return;
  const bounds = menu.getBoundingClientRect();
  menu.style.left = `${Math.max(8, Math.min(anchor.x, document.documentElement.clientWidth - bounds.width - 8))}px`;
  menu.style.top = `${Math.max(8, Math.min(anchor.y, document.documentElement.clientHeight - bounds.height - 8))}px`;
}

function items() {
  return [...menu.querySelectorAll('[role="menuitem"]')].filter(item => !item.disabled && !item.closest('[hidden]'));
}

function shiftMode(held) {
  shiftHeld = Boolean(held);
  for (const link of menu.querySelectorAll('a[role="menuitem"]')) {
    const newTab = shiftHeld && link.getAttribute('aria-disabled') !== 'true';
    link.querySelector('.menu-new-tab-indicator').hidden = !newTab;
    link.setAttribute('aria-label', link.dataset.label + (newTab ? ' · Opens in a new tab' : ''));
  }
}

export function openEntityMenu(element, event = {}) {
  const metadata = subjects.get(element);
  if (!metadata || metadata.ignore?.(event.target)) return;
  event.preventDefault?.(); event.stopPropagation?.();
  closeEntityMenu();
  const version = generation;
  current = element;
  returnFocus = event.type === 'click' ? event.currentTarget || element
    : element.contains(document.activeElement) ? document.activeElement : element;
  const host = element.closest('dialog[open]') || document.body;
  host.append(menu, notice);
  menu.replaceChildren(); notice.textContent = '';
  menu.setAttribute('aria-label', metadata.title ? `${metadata.kind || 'Entity'} actions for ${metadata.title}` : `${metadata.kind || 'Entity'} actions`);
  const bounds = element.getBoundingClientRect();
  const keyboard = event.type === 'keydown' || event.type === 'click' || (!event.clientX && !event.clientY);
  anchor = { x: keyboard ? bounds.left + Math.min(bounds.width / 2, 100) : event.clientX,
    y: keyboard ? bounds.bottom + 5 : event.clientY };
  const context = {
    isCurrent: () => generation === version && current === element,
    close: closeEntityMenu,
    onClose: cleanup => cleanups.push(cleanup),
    addActions: actions => { if (context.isCurrent()) { for (const action of actions) addAction(action, context); position(); } },
  };
  for (const action of typeof metadata.actions === 'function' ? metadata.actions(context) : metadata.actions || []) addAction(action, context);
  element.setAttribute('aria-expanded', 'true');
  if (returnFocus?.matches?.('.entity-actions-trigger')) returnFocus.setAttribute('aria-expanded', 'true');
  menu.hidden = false; shiftMode(event.shiftKey); position();
  items()[0]?.focus({ preventScroll: true });
}

function addAction(action, context) {
  if (action.hidden) return;
  if (action.element) { menu.append(action.element); return; }
  const row = document.createElement('div'); row.setAttribute('role', 'none');
  const item = document.createElement(action.href ? 'a' : 'button');
  if (!action.href) item.type = 'button';
  item.setAttribute('role', 'menuitem'); item.tabIndex = -1;
  item.dataset.action = action.id || '';
  const label = document.createElement('span');
  const indicator = document.createElement('span'); indicator.className = 'menu-new-tab-indicator'; indicator.textContent = '↗';
  indicator.setAttribute('aria-hidden', 'true'); indicator.hidden = true;
  item.append(label); if (action.href) item.append(indicator);
  const reason = document.createElement('span'); reason.className = 'entity-menu-reason';
  reason.id = 'menu-reason-' + crypto.randomUUID();
  const update = patch => {
    Object.assign(action, patch);
    label.textContent = action.label; item.dataset.label = action.label;
    item.setAttribute('aria-disabled', String(Boolean(action.disabled)));
    item.title = action.reason || '';
    reason.textContent = action.reason || ''; reason.hidden = !action.reason;
    if (action.reason) item.setAttribute('aria-describedby', reason.id);
    else item.removeAttribute('aria-describedby');
    if (action.href && !action.disabled) item.href = action.href;
    else item.removeAttribute('href');
    shiftMode(shiftHeld); position();
  };
  update({});
  const blocked = event => {
    if (action.disabled) { event.preventDefault(); event.stopPropagation(); return true; }
    return false;
  };
  item.addEventListener('auxclick', event => { if (!blocked(event)) closeEntityMenu(); });
  item.addEventListener('click', event => {
    if (blocked(event)) return;
    if (action.href) {
      if (event.shiftKey || event.detail === 0 && shiftHeld) {
        event.preventDefault(); event.stopPropagation();
        const href = action.href;
        setTimeout(() => {
          const link = document.createElement('a'); link.href = href; link.target = '_blank'; link.rel = 'noopener noreferrer';
          document.body.append(link); link.click(); link.remove();
        }, 0);
        closeEntityMenu(true);
      } else closeEntityMenu();
    } else {
      event.preventDefault(); event.stopPropagation(); closeEntityMenu(true);
      Promise.resolve().then(() => action.run?.()).catch(error => showNotice(error.message || 'The action could not be completed.'));
    }
  });
  row.append(item, reason); menu.append(row);
  if (action.load) Promise.resolve().then(action.load).then(patch => {
    if (context.isCurrent()) update(patch);
  }).catch(error => {
    if (context.isCurrent()) update({ disabled: true, reason: error.message || 'Unable to check availability. Reopen the menu to retry.' });
  });
}

function subjectAt(target) {
  for (let element = target instanceof Element ? target : target?.parentElement; element; element = element.parentElement) {
    if (subjects.has(element)) return element;
  }
  return null;
}

function editing(event) {
  return (event.composedPath?.() || [event.target]).some(element => element instanceof Element &&
    element.matches('input,textarea,select,math-field,[contenteditable]:not([contenteditable="false"])'));
}

function initialize() {
  if (menu) return;
  menu = document.createElement('div'); menu.className = 'entity-context-menu'; menu.id = 'entity-context-menu'; menu.hidden = true; menu.setAttribute('role', 'menu');
  notice = document.createElement('div'); notice.className = 'entity-copy-notice'; notice.setAttribute('role', 'status'); notice.setAttribute('aria-atomic', 'true');
  document.body.append(menu, notice);
  if (typeof ResizeObserver !== 'undefined') new ResizeObserver(position).observe(menu);
  document.addEventListener('contextmenu', event => {
    if (event.shiftKey || editing(event)) { closeEntityMenu(); return; }
    const element = subjectAt(event.target);
    if (!element) { closeEntityMenu(); return; }
    openEntityMenu(element, event);
  }, true);
  document.addEventListener('keydown', event => {
    if (!menu.hidden && menu.contains(event.target)) {
      if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); closeEntityMenu(true); }
      else if (event.key === 'Tab') closeEntityMenu(true);
      else if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) {
        event.preventDefault(); event.stopPropagation();
        const choices = items(), index = choices.indexOf(document.activeElement);
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? choices.length - 1
          : (index + (event.key === 'ArrowDown' ? 1 : -1) + choices.length) % choices.length;
        choices[next]?.focus();
      } else if (event.key === ' ' && event.target.matches('a[role="menuitem"]')) { event.preventDefault(); event.target.click(); }
      shiftMode(event.shiftKey || event.key === 'Shift');
      return;
    }
    if (!menu.hidden) shiftMode(event.shiftKey || event.key === 'Shift');
    if (editing(event) || !(event.key === 'ContextMenu' || event.shiftKey && event.key === 'F10')) return;
    const element = subjectAt(event.target); if (element) openEntityMenu(element, event);
  });
  document.addEventListener('keyup', event => { if (!menu.hidden) shiftMode(event.shiftKey); });
  document.addEventListener('pointerdown', event => { if (!menu.contains(event.target)) closeEntityMenu(); }, true);
  document.addEventListener('scroll', event => { if (!menu.contains(event.target)) closeEntityMenu(); }, true);
  document.addEventListener('wheel', event => { if (!menu.contains(event.target)) closeEntityMenu(); }, { capture: true, passive: true });
  document.addEventListener('visibilitychange', () => { if (document.hidden) closeEntityMenu(); });
  window.addEventListener('resize', () => closeEntityMenu()); window.addEventListener('blur', () => closeEntityMenu());
  for (const name of ['profile-changing', 'developer-mode-changing', 'queue-changed', 'targets-changed'])
    window.addEventListener('course-academy:' + name, () => closeEntityMenu(true));
}

export function attachMenuButton(element, label = 'Content actions') {
  const tools = document.createElement('div'); tools.className = 'entity-menu-tools';
  const button = document.createElement('button'); button.type = 'button'; button.className = 'entity-actions-trigger'; button.textContent = '⋯';
  button.setAttribute('aria-label', label); button.setAttribute('aria-haspopup', 'menu');
  button.setAttribute('aria-expanded', 'false'); button.setAttribute('aria-controls', 'entity-context-menu');
  button.addEventListener('click', event => openEntityMenu(element, event));
  tools.append(button); element.append(tools);
}

function showNotice(message) {
  initialize(); clearTimeout(noticeTimer); notice.textContent = message;
  noticeTimer = setTimeout(() => { notice.textContent = ''; }, 2500);
}

export async function copyText(value, label = 'text') {
  initialize(); notice.textContent = '';
  try { await navigator.clipboard.writeText(value); showNotice(`Copied ${label}`); return; } catch { /* Try the manual copy dialog below. */ }
  if (!manualCopy) {
    manualCopy = document.createElement('dialog'); manualCopy.className = 'entity-manual-copy';
    const title = document.createElement('h2'); title.textContent = 'Copy to clipboard';
    const text = document.createElement('textarea'); text.readOnly = true; text.setAttribute('aria-label', 'Text to copy');
    const hint = document.createElement('p'); hint.textContent = 'Clipboard access was blocked. Copy this text with Ctrl+C or ⌘C.';
    const done = document.createElement('button'); done.type = 'button'; done.textContent = 'Done'; done.addEventListener('click', () => manualCopy.close());
    manualCopy.append(title, hint, text, done); document.body.append(manualCopy);
  }
  manualCopy.querySelector('textarea').value = value; manualCopy.showModal();
  manualCopy.querySelector('textarea').focus(); manualCopy.querySelector('textarea').select();
}
