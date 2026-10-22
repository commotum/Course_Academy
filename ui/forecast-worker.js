import { readForecast } from './forecast.js';

self.onmessage = async event => {
  try {
    self.postMessage({ forecast: await readForecast(event.data) });
  } catch (error) {
    self.postMessage({ error: error.message || 'Unable to calculate forecast.' });
  }
};
