import { savedForecastScope, withForecastGoal, courseCompletionEstimates } from './forecast.js';

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
    const time = node('time', 'forecast-date', new Intl.DateTimeFormat(undefined,
      { month: 'short', day: 'numeric', year: 'numeric' }).format(date));
    time.dateTime = estimate.date;
    return time;
  }
  return node('span', 'forecast-status', ({ complete: 'Caught up', 'not-catching-up': 'Not catching up',
    'out-of-range': 'Too far ahead' })[estimate.status] || 'Unavailable');
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
    worker.postMessage(savedForecastScope());
  });
}

export function createForecastSidebar({ signal } = {}) {
  const overall = node('section', 'study-stat-card forecast-overall');
  const courses = node('section', 'study-stat-card forecast-courses');
  for (const [card, heading] of [[overall, 'Estimated completion'], [courses, 'Course catch-up']]) {
    card.setAttribute('aria-live', 'polite');
    card.append(node('h2', 'stat-heading', heading), node('p', 'stat-note', 'Calculating…'));
  }
  let model, request, revision = 0, goalRevision = 0, latestGoal;
  signal?.addEventListener('abort', () => { revision++; request?.abort(); }, { once: true });

  function render() {
    const p = model.pace, hasGoal = Number.isFinite(p.dailyEarnedXpGoal) && p.dailyEarnedXpGoal > 0;
    // Both displayed rates are earned XP. The model converts the goal to
    // attempted base XP using the same measured earned/base ratio.
    const average = p.observedDays ? p.earnedXp / p.observedDays : null;
    const rate = value => Number.isFinite(value) ? `${number(value)} XP/day` : 'No pace history';
    const averageLabel = p.observedDays < 7 ? `${p.observedDays}-day average` : '7-day average';
    overall.replaceChildren(node('h2', 'stat-heading', 'Estimated completion'));
    const list = node('dl', 'forecast-summary');
    for (const [label, value, estimate, available] of [
      [averageLabel, average, model.currentPace, true],
      ['Daily goal', p.dailyEarnedXpGoal, model.goalPace, hasGoal],
    ]) {
      const row = node('div', 'forecast-row'), term = node('dt', 'forecast-label', label);
      term.append(node('span', 'forecast-rate', available ? rate(value) : 'Set in Profile'));
      const detail = node('dd', 'forecast-result'); detail.append(outcome(estimate, available));
      row.append(term, detail); list.append(row);
    }
    overall.append(list, node('p', 'stat-note', 'Catch-up includes projected new work. Average excludes today.'));

    courses.replaceChildren(node('h2', 'stat-heading', 'Course catch-up'));
    const table = node('table', 'forecast-course-table');
    const head = node('thead', ''), headings = node('tr', '');
    for (const [label, value] of [['Course', null], [averageLabel, average], ['Daily goal', p.dailyEarnedXpGoal]]) {
      const cell = node('th', '', label); cell.scope = 'col';
      if (label !== 'Course') cell.append(node('span', 'forecast-rate', label === 'Daily goal' && !hasGoal ? 'Not set' : rate(Number.isFinite(value) ? value / 3 : null)));
      headings.append(cell);
    }
    head.append(headings); table.append(head);
    const body = node('tbody', '');
    for (const course of courseCompletionEstimates(model)) {
      const row = node('tr', ''), label = node('th', '', `MTH ${course.code}`); label.scope = 'row';
      row.append(label);
      for (const [estimate, available] of [[course.currentPace, true], [course.goalPace, hasGoal]]) {
        const cell = node('td', '');
        cell.append(model.scope.courses.includes(course.code) ? outcome(estimate, available) : node('span', 'forecast-status', 'Not selected'));
        row.append(cell);
      }
      body.append(row);
    }
    table.append(body);
    courses.append(table, node('p', 'stat-note', 'One third of each pace per course; each uses its own workload and growth. Based on your Targets filters.'));
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
      for (const [card, heading] of [[overall, 'Estimated completion'], [courses, 'Course catch-up']]) {
        card.replaceChildren(node('h2', 'stat-heading', heading), node('p', 'stat-note', 'Estimates unavailable.'));
      }
      const retry = node('button', 'small-button', 'Try again'); retry.type = 'button';
      retry.addEventListener('click', refresh); overall.append(retry);
    }
  }
  function updateGoal(goal) {
    latestGoal = goal; goalRevision++;
    if (model) { model = withForecastGoal(model, goal); render(); }
  }
  return { cards: [overall, courses], refresh, updateGoal };
}
