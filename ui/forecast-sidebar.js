import { withForecastGoal, courseCompletionEstimates } from './forecast.js';

const number = value => Number(value).toLocaleString(undefined, { maximumFractionDigits: 1 });
function node(tag, className, text) {
  const element = document.createElement(tag); element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}
function outcome(estimate, hasGoal = true) {
  if (!hasGoal) return node('span', 'forecast-status', 'No goal set');
  if (estimate.status === 'estimated') {
    const date = new Date(estimate.date);
    const time = node('time', 'forecast-date', new Intl.DateTimeFormat('en-US',
      { month: '2-digit', day: '2-digit', year: '2-digit' }).format(date));
    time.dateTime = estimate.date;
    return time;
  }
  const status = node('span', 'forecast-status', ({ complete: 'Caught up', 'not-catching-up': '∞',
    'out-of-range': 'Too far ahead' })[estimate.status] || 'Unavailable');
  if (estimate.status === 'not-catching-up') status.setAttribute('aria-label', 'Not catching up at this pace');
  return status;
}

// Historical replay can take several seconds. Keep both the input read and
// calculation off the UI thread; terminating a replaced read cancels its work.
function readSidebarForecast(signal) {
  return new Promise((resolve, reject) => {
    if (signal.aborted) { reject(new Error('Forecast cancelled.')); return; }
    const worker = new Worker('/ui/forecast-worker.js', { type: 'module' });
    const close = () => { worker.terminate(); signal.removeEventListener('abort', abort); };
    const abort = () => { close(); reject(new Error('Forecast cancelled.')); };
    signal.addEventListener('abort', abort, { once: true });
    worker.onmessage = event => {
      close();
      if (event.data.error) reject(new Error(event.data.error));
      else resolve(event.data.forecast);
    };
    worker.onerror = () => { close(); reject(new Error('Unable to calculate forecast.')); };
    worker.postMessage({});
  });
}

export function createForecastSidebar({ signal } = {}) {
  const overall = node('section', 'study-stat-card forecast-overall');
  overall.setAttribute('aria-live', 'polite');
  overall.append(node('h2', 'stat-heading', 'Estimated completion'), node('p', 'stat-note', 'Calculating…'));
  let model, request, revision = 0, goalRevision = 0, latestGoal;
  signal?.addEventListener('abort', () => { revision++; request?.abort(); }, { once: true });

  function render() {
    const p = model.pace, hasGoal = Number.isFinite(p.dailyEarnedXpGoal) && p.dailyEarnedXpGoal > 0;
    // Both displayed rates are earned XP. The model converts the goal to
    // attempted base XP using the same measured earned/base ratio.
    const average = p.observedDays ? p.earnedXp / p.observedDays : null;
    const rate = value => Number.isFinite(value) ? `${number(value)} XP/day` : 'No pace history';
    overall.replaceChildren(node('h2', 'stat-heading', 'Estimated completion'));
    const table = node('table', 'forecast-course-table');
    const head = node('thead', ''), headings = node('tr', '');
    for (const label of ['', rate(average), hasGoal ? rate(p.dailyEarnedXpGoal) : 'No goal set']) {
      const cell = node('th', '', label); cell.scope = 'col';
      if (!label) cell.setAttribute('aria-label', 'Course');
      headings.append(cell);
    }
    head.append(headings); table.append(head);
    const body = node('tbody', '');
    const rows = [
      { label: 'All Courses', currentPace: model.currentPace, goalPace: model.goalPace },
      ...courseCompletionEstimates(model).map(course => ({ ...course, label: `MTH ${course.code}` })),
    ];
    for (const entry of rows) {
      const row = node('tr', ''), label = node('th', '', entry.label); label.scope = 'row';
      row.append(label);
      for (const [estimate, available] of [[entry.currentPace, true], [entry.goalPace, hasGoal]]) {
        const cell = node('td', '');
        cell.append(outcome(estimate, available));
        row.append(cell);
      }
      body.append(row);
    }
    table.append(body);
    overall.append(table);
    if (model.inventory.estimatedTopics.length || model.growth.total.estimatedTopics.length) {
      overall.append(node('p', 'stat-note', 'Includes estimated lesson XP.'));
    }
    if (model.growth.total.isLowerBound) overall.append(node('p', 'stat-note', 'Some incoming work has unknown XP; dates may be optimistic.'));
  }

  async function refresh() {
    if (signal?.aborted) return;
    const current = ++revision;
    const goalAtStart = goalRevision;
    request?.abort(); request = new AbortController();
    try {
      const forecast = await readSidebarForecast(request.signal);
      if (current !== revision || signal?.aborted || !overall.isConnected) return;
      model = goalAtStart === goalRevision ? forecast : withForecastGoal(forecast, latestGoal);
      render();
    } catch (error) {
      if (current !== revision || signal?.aborted || !overall.isConnected) return;
      overall.replaceChildren(node('h2', 'stat-heading', 'Estimated completion'), node('p', 'stat-note', 'Estimates unavailable.'));
      const retry = node('button', 'small-button', 'Try again'); retry.type = 'button';
      retry.addEventListener('click', refresh); overall.append(retry);
    }
  }
  function updateGoal(goal) {
    latestGoal = goal; goalRevision++;
    if (model) { model = withForecastGoal(model, goal); render(); }
  }
  return { cards: [overall], refresh, updateGoal };
}
