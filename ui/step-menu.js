// Only registered lesson containers can supply the ID; rendered Markdown cannot.
const stepIds = new WeakMap();
let menu = null;
let copyButton;
let academyButton;
let notice;
let noticeTimer;
let currentStep = null;
let returnFocus = null;

export function stepEntityId(value) {
  if (typeof value === 'number' && !Number.isSafeInteger(value)) return null;
  if (typeof value !== 'number' && typeof value !== 'string') return null;
  const id = String(value);
  return /^[1-9]\d*$/.test(id) ? id : null;
}

export function attachStepMenu(element, value, mathAcademyId = null) {
  const id = stepEntityId(value);
  if (!id) return;
  stepIds.set(element, { dbId: id, mathAcademyId: stepEntityId(mathAcademyId) });
  element.dataset.stepDbId = id;
  element.tabIndex = 0;
  if (!menu) initialize();
}

function stepAt(target) {
  for (let element = target instanceof Element ? target : target?.parentElement; element; element = element.parentElement) {
    if (stepIds.has(element)) return element;
  }
  return null;
}

function close(restoreFocus = false) {
  menu.hidden = true;
  if (restoreFocus && returnFocus?.isConnected) returnFocus.focus({ preventScroll: true });
  currentStep = null;
  returnFocus = null;
}

function open(step, x, y) {
  currentStep = step;
  returnFocus = step.contains(document.activeElement) ? document.activeElement : step;
  academyButton.hidden = !stepIds.get(step).mathAcademyId;
  menu.hidden = false;
  menu.style.left = '0px'; menu.style.top = '0px';
  const bounds = menu.getBoundingClientRect();
  menu.style.left = `${Math.max(8, Math.min(x, document.documentElement.clientWidth - bounds.width - 8))}px`;
  menu.style.top = `${Math.max(8, Math.min(y, document.documentElement.clientHeight - bounds.height - 8))}px`;
  copyButton.focus({ preventScroll: true });
}

function initialize() {
  menu = document.createElement('div');
  menu.className = 'step-context-menu'; menu.hidden = true;
  menu.setAttribute('role', 'menu'); menu.setAttribute('aria-label', 'Lesson step');
  copyButton = document.createElement('button');
  copyButton.type = 'button'; copyButton.setAttribute('role', 'menuitem');
  copyButton.textContent = 'Copy :db/id';
  academyButton = document.createElement('button');
  academyButton.type = 'button'; academyButton.setAttribute('role', 'menuitem');
  academyButton.textContent = 'Copy :ma/id';
  menu.append(copyButton, academyButton);
  notice = document.createElement('div');
  notice.className = 'step-copy-notice'; notice.setAttribute('role', 'status');
  notice.setAttribute('aria-atomic', 'true');
  document.body.append(menu, notice);

  const copy = async (key, label) => {
    const id = stepIds.get(currentStep)?.[key];
    close(true);
    if (!id) return;
    clearTimeout(noticeTimer); notice.textContent = '';
    try {
      await navigator.clipboard.writeText(id);
      notice.textContent = `Copied ${label} ${id}`;
      noticeTimer = setTimeout(() => { notice.textContent = ''; }, 2500);
    } catch {
      // Keep the ID available even when browser clipboard permission is denied.
      window.prompt(`Clipboard unavailable. Copy this ${label}:`, id);
    }
  };
  copyButton.addEventListener('click', () => copy('dbId', ':db/id'));
  academyButton.addEventListener('click', () => copy('mathAcademyId', ':ma/id'));

  const editable = target => target instanceof Element && target.closest('input, textarea, select, [contenteditable]:not([contenteditable="false"])');
  document.addEventListener('contextmenu', event => {
    if (event.shiftKey || editable(event.target)) { close(); return; }
    const step = stepAt(event.target);
    if (!step) { close(); return; }
    event.preventDefault(); event.stopPropagation();
    const bounds = step.getBoundingClientRect();
    open(step, event.clientX || bounds.left + 16, event.clientY || Math.max(8, bounds.top) + 16);
  }, true);
  document.addEventListener('keydown', event => {
    if (!menu.hidden) {
      if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); close(true); }
      else if (event.key === 'Tab') close(true);
      else if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) {
        event.preventDefault();
        const buttons = [copyButton, academyButton].filter(button => !button.hidden);
        const index = buttons.indexOf(document.activeElement);
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1
          : (index + (event.key === 'ArrowDown' ? 1 : -1) + buttons.length) % buttons.length;
        buttons[next].focus();
      }
      return;
    }
    if (editable(event.target) || !(event.key === 'ContextMenu' || event.shiftKey && event.key === 'F10')) return;
    const step = stepAt(event.target);
    if (!step) return;
    event.preventDefault();
    const bounds = step.getBoundingClientRect();
    open(step, bounds.left + 16, Math.max(8, bounds.top) + 16);
  });
  document.addEventListener('pointerdown', event => { if (!menu.contains(event.target)) close(); }, true);
  document.addEventListener('scroll', () => close(), true);
  window.addEventListener('resize', () => close());
  window.addEventListener('blur', () => close());
}
