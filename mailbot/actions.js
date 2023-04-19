export const GET_CAPTCHA_SUCCESS = 'GET_CAPTCHA_SUCCESS';
export const CAPTCHA_SOLVED = 'CAPTCHA_SOLVED';
export const START_WORKER = 'START_WORKER';
export const TRACK_FETCH_SUCCESS = 'TRACK_FETCH_SUCCESS';

export const startWorkerAction = (trackID) => ({
  type: START_WORKER,
  payload: trackID
});
