import { readForecast } from './forecast.js';

self.onmessage = async () => {
  try {
    self.postMessage({ forecast: await readForecast() });
  } catch (error) {
    self.postMessage({ error: error.message || 'Unable to calculate forecast.' });
  }
};
