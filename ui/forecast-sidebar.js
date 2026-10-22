import { withForecastGoal, courseCompletionEstimates } from './forecast.js';

const cacheKey = 'course-academy.forecast.v1';
let savedForecast, pendingForecast;
const localDay = () => { const now = new Date(); return new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime(); };
function cachedForecast() {
  try {
    savedForecast ||= JSON.parse(sessionStorage.getItem(cacheKey));
    const f = savedForecast;
    if (f && Number.isFinite(f.basis) && Date.parse(f.pace?.observedThrough) === localDay()
      && f.scope?.includeQueue === true && f.scope?.weekSelection?.kind === 'all'
      && ['255', '256', '341'].every(code => f.scope.courses?.includes(code))
      && f.scope.prerequisiteDepth === 2 && Array.isArray(f.courses) && f.courses.length === 3
      && f.inventory && f.growth?.total && f.overhead && f.currentPace && f.goalPace) return f;
  } catch { /* Storage is optional; fall back to an ordinary read. */ }
  return null;
}
function saveForecast(forecast) {
  if (Date.parse(forecast.pace.observedThrough) !== localDay()) return;
  savedForecast = forecast;
  try { sessionStorage.setItem(cacheKey, JSON.stringify(forecast)); } catch { /* Keep the in-memory cache. */ }
}

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
// calculation off the UI thread, including while another page is loading.
function readSidebarForecast() {
  return new Promise((resolve, reject) => {
    const worker = new Worker('/ui/forecast-worker.js', { type: 'module' });
    const close = () => worker.terminate();
    worker.onmessage = event => {
      close();
      if (event.data.error) reject(new Error(event.data.error));
      else resolve(event.data.forecast);
    };
    worker.onerror = () => { close(); reject(new Error('Unable to calculate forecast.')); };
    worker.postMessage({});
  });
}

function sharedForecastRead() {
  const day = localDay();
  if (pendingForecast?.day === day) return pendingForecast.promise;
  // A page transition must not discard an expensive calculation. New sidebar
  // instances share this read, and its result survives navigation in storage.
  const read = { day };
  read.promise = readSidebarForecast().then(forecast => {
    saveForecast(forecast); return forecast;
  }).finally(() => { if (pendingForecast === read) pendingForecast = null; });
  pendingForecast = read;
  return read.promise;
}

export function createForecastSidebar({ signal } = {}) {
  const overall = node('section', 'study-stat-card forecast-overall');
  overall.setAttribute('aria-live', 'polite');
  overall.append(node('h2', 'stat-heading', 'Estimated completion'), node('p', 'stat-note', 'Calculating…'));
  let model = cachedForecast(), revision = 0, goalRevision = 0, latestGoal;
  signal?.addEventListener('abort', () => { revision++; }, { once: true });

  function render() {
    const p = model.pace, hasGoal = Number.isFinite(p.dailyEarnedXpGoal) && p.dailyEarnedXpGoal > 0;
    // Both displayed rates are earned XP. The model converts the goal to
    // attempted base XP using the same measured earned/base ratio.
    const average = p.observedDays ? p.earnedXp / p.observedDays : null;
    const rate = value => Number.isFinite(value) ? number(Math.ceil(value)) : '—';
    overall.title = '';
    overall.replaceChildren(node('h2', 'stat-heading', 'Estimated completion'));
    const table = node('table', 'forecast-course-table');
    const head = node('thead', ''), headings = node('tr', '');
    for (const label of ['XP/day', rate(average), hasGoal ? rate(p.dailyEarnedXpGoal) : '—']) {
      const cell = node('th', '', label); cell.scope = 'col';
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
    if (model.growth.total.isLowerBound) overall.append(node('p', 'stat-note', 'Some incoming work has unknown XP; dates may be optimistic.'));
  }

  async function refresh({ basis, dailyXpGoal } = {}) {
    if (signal?.aborted) return;
    const current = ++revision;
    if (dailyXpGoal !== undefined && dailyXpGoal !== model?.pace.dailyEarnedXpGoal) updateGoal(dailyXpGoal);
    const goalAtStart = goalRevision;
    try {
      const cached = cachedForecast();
      let forecast = cached && Number.isFinite(basis) && cached.basis === basis ? cached : await sharedForecastRead();
      // A database change may have happened while an older shared read was in
      // flight. Finish that read, then fetch the newer snapshot once.
      if (Number.isFinite(basis) && forecast.basis < basis) forecast = await sharedForecastRead();
      if (current !== revision || signal?.aborted || !overall.isConnected) return;
      const goal = goalAtStart !== goalRevision ? latestGoal
        : forecast.basis > basis ? undefined : dailyXpGoal;
      model = goal === undefined ? forecast : withForecastGoal(forecast, goal);
      saveForecast(model);
      render();
    } catch (error) {
      if (current !== revision || signal?.aborted || !overall.isConnected) return;
      if (model) { overall.title = 'Showing saved estimates; refresh unavailable.'; return; }
      overall.replaceChildren(node('h2', 'stat-heading', 'Estimated completion'), node('p', 'stat-note', 'Estimates unavailable.'));
      const retry = node('button', 'small-button', 'Try again'); retry.type = 'button';
      retry.addEventListener('click', refresh); overall.append(retry);
    }
  }
  function updateGoal(goal) {
    latestGoal = goal; goalRevision++;
    if (model) { model = withForecastGoal(model, goal); saveForecast(model); render(); }
  }
  if (model) render();
  return { cards: [overall], refresh, updateGoal };
}
