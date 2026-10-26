import { attachEntityMenu, copyText } from './entity-menu.js';

export function stepEntityId(value) {
  if (typeof value === 'number' && !Number.isSafeInteger(value)) return null;
  if (typeof value !== 'number' && typeof value !== 'string') return null;
  const id = String(value);
  return /^[1-9]\d*$/.test(id) ? id : null;
}

export function entityIdActions(value, kind = 'entity') {
  const id = stepEntityId(value);
  return [{ id: 'copy-db-id', label: `Copy ${kind} :db/id`, hidden: !id, run: () => copyEntityId(id, kind) }];
}

// Compatibility adapter: callers identify the displayed content, not its
// authored placement or learner-task presentation unless that is the subject.
export function attachStepMenu(element, value, _mathAcademyId = null, options = {}) {
  const id = stepEntityId(value); if (!id) return;
  const kind = options.kind || 'step';
  attachEntityMenu(element, {
    kind, title: options.title,
    actions: context => [...entityIdActions(id, kind), ...(options.actions?.(context) || [])],
  });
  element.dataset.stepDbId = id;
}

export async function copyEntityId(value, kind = '') {
  const id = stepEntityId(value);
  if (!id) return;
  const text = `:db/id=${id}`;
  await copyText(text, `${kind ? kind + ' ' : ''}${text}`);
}
