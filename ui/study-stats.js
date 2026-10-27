import { readRequest } from './requests.js';
import { createForecastSidebar } from './forecast-sidebar.js';

const changeKey = 'course-academy.daily-xp-goal-changed';
const cacheKey = 'course-academy.study-stats.v1';
let releaseSidebar = () => {};
const number = value => Number(value).toLocaleString(undefined, { maximumFractionDigits: 1 });
function node(tag, className, text) {
  const element = document.createElement(tag); element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}
function renderSummary(card, heading, entries) {
  card.replaceChildren(node('h2', 'stat-heading', heading));
  const summary = node('dl', 'stat-xp-summary');
  const exactDetails = node('p', 'stat-note stat-xp-details'); exactDetails.hidden = true;
  const summaryButtons = [];
  for (const [label, value, details] of entries) {
    const metric = node('div', 'stat-xp-metric');
    const term = node('dt', 'stat-xp-label', label);
    const definition = node('dd', 'stat-xp-number');
    const formatted = value == null ? '—' : Math.abs(value) >= 10000
      ? new Intl.NumberFormat(undefined, { notation: 'compact', maximumFractionDigits: 1 }).format(value).toLowerCase()
      : number(value);
    const amount = node('button', 'stat-xp-value', formatted); amount.type = 'button'; summaryButtons.push(amount);
    amount.title = details; amount.setAttribute('aria-label', details); amount.setAttribute('aria-expanded', 'false');
    amount.addEventListener('click', () => {
      const expanded = amount.getAttribute('aria-expanded') !== 'true';
      for (const sibling of summaryButtons) sibling.setAttribute('aria-expanded', 'false');
      amount.setAttribute('aria-expanded', String(expanded)); exactDetails.textContent = details; exactDetails.hidden = !expanded;
    });
    definition.append(amount); metric.append(term, definition); summary.append(metric);
  }
  card.append(summary, exactDetails);
}
export function localWeek(now = new Date()) {
  const first = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  first.setDate(first.getDate() - (first.getDay() + 6) % 7);
  return Array.from({ length: 8 }, (_, index) => new Date(first.getFullYear(), first.getMonth(), first.getDate() + index).getTime());
}
function lastSevenDays(now = new Date()) {
  return Array.from({ length: 8 }, (_, i) => new Date(now.getFullYear(), now.getMonth(), now.getDate() - 6 + i).getTime());
}

export function createStudySidebar() {
  releaseSidebar();
  const events = new AbortController();
  const sidebar = node('aside', 'study-sidebar'); sidebar.setAttribute('aria-label', 'Study statistics');
  const todayCard = node('section', 'study-stat-card');
  const weekCard = node('section', 'study-stat-card');
  const activityCard = node('section', 'study-stat-card stat-activities');
  const dailyActivityCard = node('section', 'study-stat-card stat-activities-today');
  todayCard.append(node('h2', 'stat-heading', 'XP earned'), node('p', 'stat-note', 'Loading your progress…'));
  weekCard.append(node('h2', 'stat-heading', 'This week'));
  const forecast = createForecastSidebar({ signal: events.signal });
  sidebar.append(todayCard, weekCard, ...forecast.cards, activityCard, dailyActivityCard);
  function renderActivities(card, heading, totals, suffix = '') {
    renderSummary(card, heading, [
      ['Lessons', totals?.lessons, 'completed lesson sessions'],
      ['KPs', totals?.knowledgePoints, 'distinct knowledge points in completed lessons'],
      ['Reviews', totals?.reviews, 'completed review sessions'],
    ].map(([label, value, description]) => [label, value, value == null ? `${label}: unavailable` : `${number(value)} ${description}${suffix}`]));
  }
  renderActivities(activityCard, 'Activities');
  renderActivities(dailyActivityCard, 'Activities today');
  let generation = 0, midnightTimer, renderedDay;
  releaseSidebar = () => { events.abort(); generation++; clearTimeout(midnightTimer); };
  async function load({ refreshForecast = true } = {}) {
    const revision = ++generation;
    const boundaries = lastSevenDays();
    try {
      const progress = readRequest('/api/study-stats?dayStarts=' + boundaries.join(','));
      const response = await progress;
      const data = await response.json();
      if (!response.ok || !Array.isArray(data.days) || data.days.length !== 7) throw new Error(data.error || 'Statistics are unavailable.');
      if (revision !== generation || !sidebar.isConnected) return;
      render(data, boundaries);
      sidebar.title = '';
      try { sessionStorage.setItem(cacheKey, JSON.stringify({ boundaries, data })); } catch { /* Storage is optional. */ }
      if (refreshForecast) void forecast.refresh({ basis: data.basis, dailyXpGoal: data.dailyXpGoal });
    } catch (error) {
      if (revision !== generation || !sidebar.isConnected) return;
      if (refreshForecast) void forecast.refresh();
      if (renderedDay === lastSevenDays()[6]) {
        sidebar.title = 'Showing saved statistics; refresh unavailable.';
        return;
      }
      renderActivities(dailyActivityCard, 'Activities today');
      todayCard.replaceChildren(node('h2', 'stat-heading', 'XP earned'), node('p', 'stat-note', error.message));
      const retry = node('button', 'small-button', 'Try again'); retry.type = 'button'; retry.addEventListener('click', load); todayCard.append(retry);
    }
  }
  function render(data, boundaries) {
    const now = Date.now();
    const current = boundaries.findIndex((at, i) => i < 7 && now >= at && now < boundaries[i + 1]);
    if (current !== 6) { void load(); return; }
    clearTimeout(midnightTimer);
    midnightTimer = setTimeout(() => { if (sidebar.isConnected) void load(); }, boundaries[7] - now + 50);
    const index = (new Date(boundaries[current]).getDay() + 6) % 7;
    const today = data.days[current], goal = data.dailyXpGoal;
    const weekStart = localWeek(new Date(now))[0];
    const weekXp = data.days.reduce((sum, day, i) => sum + (boundaries[i] >= weekStart ? day.earnedXp : 0), 0);
    // Each fixed weekday slot shows its latest occurrence, including today.
    const days = data.days.map((day, i) => ({ ...day, start: boundaries[i] }))
      .sort((a, b) => (new Date(a.start).getDay() + 6) % 7 - (new Date(b.start).getDay() + 6) % 7);
    renderSummary(todayCard, 'XP earned', [['Today', today.earnedXp, 0], ['This week', weekXp, 0], ['Total', data.totalEarnedXp, data.totalXpMissing || 0]].map(([label, value, missing]) => [label, value,
      value == null ? `${label}: XP unavailable` : `${label}: ${number(value)} XP${missing ? ` recorded; XP unavailable for ${number(missing)} past ${missing === 1 ? 'activity' : 'activities'}` : ''}`]));
    renderActivities(activityCard, 'Activities', data.activityTotals);
    renderActivities(dailyActivityCard, 'Activities today', today.activityTotals, ' today');
    if (goal && today.earnedXp >= goal) todayCard.append(node('p', 'stat-note stat-goal-reached', '✓ Daily goal reached'));
    weekCard.replaceChildren(node('h2', 'stat-heading', 'This week'));
    const chartGoal = goal || 200;
    const chart = node('div', 'stat-week-chart'); chart.setAttribute('aria-label', `Daily XP earned this week, out of ${number(chartGoal)} XP per day`);
    const maximum = chartGoal;
    const minimum = Math.min(0, ...days.map(day => day.earnedXp));
    const range = maximum - minimum;
    const dayDetails = node('p', 'stat-note'); dayDetails.hidden = true;
    days.forEach((day, i) => {
      const date = new Date(day.start);
      const label = new Intl.DateTimeFormat(undefined, { weekday: 'short' }).format(date);
      const bar = node('button', 'stat-day'); bar.type = 'button';
      const details = `${new Intl.DateTimeFormat(undefined, { weekday: 'long', month: 'short', day: 'numeric' }).format(date)}: ${number(day.earnedXp)} / ${number(chartGoal)} XP, ${number(day.workingSeconds / 60)} min working time${day.earnedXp >= chartGoal ? ', goal reached' : ''}`;
      bar.title = details; bar.setAttribute('aria-label', details);
      bar.setAttribute('aria-pressed', 'false');
      bar.addEventListener('click', () => {
        const selected = bar.getAttribute('aria-pressed') !== 'true';
        for (const control of chart.children) control.setAttribute('aria-pressed', 'false');
        bar.setAttribute('aria-pressed', String(selected)); dayDetails.textContent = details; dayDetails.hidden = !selected;
      });
      if (i === index) bar.setAttribute('aria-current', 'date');
      bar.dataset.future = String(i > index); bar.dataset.goalReached = String(day.earnedXp >= chartGoal);
      const column = node('span', 'stat-day-column'), fill = node('span', 'stat-day-fill');
      fill.style.height = Math.abs(Math.min(day.earnedXp, maximum)) / range * 100 + '%';
      if (day.earnedXp < 0) { fill.style.top = maximum / range * 100 + '%'; fill.dataset.negative = 'true'; }
      else fill.style.bottom = -minimum / range * 100 + '%';
      const zero = node('span', 'stat-day-zero'); zero.style.top = maximum / range * 100 + '%';
      column.append(fill, zero); bar.append(column, node('span', 'stat-day-label', label)); chart.append(bar);
    });
    weekCard.append(chart, dayDetails, node('p', 'stat-note', `${number(today.workingSeconds / 60)} min working time today`));
    renderedDay = boundaries[6];
  }
  window.addEventListener('storage', event => { if (event.key === changeKey && sidebar.isConnected) void load(); }, { signal: events.signal });
  window.addEventListener('course-academy:daily-xp-goal-changed', event => {
    if (!sidebar.isConnected) return;
    forecast.updateGoal(event.detail.dailyXpGoal);
    void load({ refreshForecast: false });
  }, { signal: events.signal });
  window.addEventListener('pageshow', () => { if (sidebar.isConnected) void load(); }, { signal: events.signal });
  document.addEventListener('visibilitychange', () => { if (!document.hidden && sidebar.isConnected) void load(); }, { signal: events.signal });
  // Show this tab's last summary immediately; always refresh from the server.
  try {
    const cached = JSON.parse(sessionStorage.getItem(cacheKey));
    const boundaries = lastSevenDays();
    if (cached?.boundaries?.length === 8 && cached.boundaries.every((at, i) => at === boundaries[i])
      && Array.isArray(cached.data?.days) && cached.data.days.length === 7) {
      render(cached.data, boundaries);
      sidebar.title = 'Refreshing saved statistics…';
    }
  } catch { /* A missing or invalid cache falls back to the ordinary read. */ }
  void load();
  return sidebar;
}
