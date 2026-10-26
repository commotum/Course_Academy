import { attachStepMenu, stepEntityId } from './step-menu.js';
import { copyText } from './entity-menu.js';
import { readTopicStudyAvailability } from './requests.js';

let defaultControls;
async function selectionControls() {
  if (!defaultControls) defaultControls = import('./targets.js').then(({ createQueueControls, createTargetControls }) => ({
    queueControls: createQueueControls({}), targetControls: createTargetControls({}),
  }));
  return defaultControls;
}

export function attachTopicMenu(element, topic, options = {}) {
  const id = stepEntityId(topic.id); if (!id) return;
  attachStepMenu(element, id, topic.mathAcademyId, {
    kind: 'topic', title: topic.title || topic.name || 'Topic', actionsButton: options.actionsButton,
    actions(context) {
      let availability;
      const readAvailability = () => availability ||= readTopicStudyAvailability(id);
      const studyHref = '/learn?topicId=' + encodeURIComponent(id);
      const reviewHref = '/learn?reviewTopicId=' + encodeURIComponent(id);
      const mode = import('./developer-mode.js').then(async module => { await module.developerModeReady; return module.isDeveloperMode(); });
      // Reuse the existing membership controller, including exact retries,
      // rollback, cross-tab refresh and mode gating. Graph callers supply their
      // controllers so the same optimistic change also repaints the graph.
      void Promise.resolve(options.queueControls ? options : selectionControls()).then(controls => {
        if (!context.isCurrent()) return;
        for (const name of ['queueControls', 'targetControls']) {
          const controller = controls[name], host = controller.createToggle(topic, { menuItem: true });
          if (!host) continue;
          context.onClose(() => controller.remove(host));
          context.addActions([{ element: host }]);
          controller.refresh();
        }
      }).catch(() => {});
      const reference = typeof options.topicHref === 'function' ? options.topicHref() : options.topicHref;
      return [
        { id: 'study-topic', label: 'Study now', href: studyHref, disabled: true, reason: 'Checking lesson availability…', load: async () => {
          if (await mode) return { label: 'Preview lesson', disabled: false, reason: '' };
          const data = await readAvailability();
          return { label: data.completed ? 'View completed lesson' : data.resumable ? 'Resume Study' : 'Study now', disabled: !data.available, reason: data.reason || '' };
        } },
        { id: 'review-topic', label: 'Practice review', href: reviewHref, disabled: true, reason: 'Checking review availability…', load: async () => {
          if (await mode) return { disabled: true, reason: 'Turn off developer mode to start a practice review.' };
          const data = await readAvailability();
          return { label: data.review?.resumable ? 'Resume practice review' : 'Practice review', disabled: !data.review?.available,
            reason: data.review?.reason || (data.review ? '' : 'Review availability could not be confirmed. Reopen the menu to retry.') };
        } },
        { id: 'open-topic', label: 'Open topic lesson', href: reference || '/topic?topic=' + encodeURIComponent(topic.uuid || topic.mathAcademyId || id) },
        { id: 'view-graph', label: 'View in graph', href: '/?course=all&topic=' + encodeURIComponent(id) },
        { id: 'copy-topic', label: 'Copy topic summary', run: () => copyText('topic-id: ' + (topic.uuid || id)
          + (topic.mathAcademyId != null ? '\nmath-academy-id: ' + topic.mathAcademyId : '')
          + '\ntopic-name: ' + (topic.title || topic.name || 'Topic'), 'topic summary') },
      ];
    },
  });
}
