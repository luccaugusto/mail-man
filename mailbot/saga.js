import {fork, takeEvery, call, put} from 'redux-saga/effects';
import {START_WORKER, CAPTCHA_SOLVED, TRACK_FETCH_SUCCESS} from './actions.js';
import {TrackBot} from './trackBot.js';
import {getSessionCookies, getSecureImage, getResult} from './api.js';
import readline from 'readline';

function* startWorkerListener() {
  yield takeEvery(START_WORKER, startWorker);
}

function* startWorker(action) {
  const trackBot = new TrackBot(action.payload);

  const sessionCookies = yield call(getSessionCookies, trackBot.headers);
  trackBot.cookies = sessionCookies;

  for (let i=0; i<1000; i++){
    const {captchaCookie, captchaImage} = yield call(getSecureImage, trackBot.headers, trackBot.cookies, `${i}.png`);
  }
  return;
  const cookieIndex = trackBot.cookies.findIndex((cookie) => cookie.split('=')[0] === captchaCookie.split('=')[0]);
  trackBot.cookies[cookieIndex] = captchaCookie;

  yield fork(solveCaptcha, captchaImage, trackBot.headers, trackBot.cookies, trackBot.trackID);
}

//TODO: retry captcha solving if it fails
function* solveCaptcha(captchaImage, headers, cookies, trackID) {
  captchaImage;
  const input = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  const question = (query) => new Promise((resolve) => input.question(query, resolve));

  const answer = yield call(question, 'Captcha answer: ');
  input.close();
  yield put({type: CAPTCHA_SOLVED, payload: {headers, cookies, trackID, answer}});
}

function* captchaSolvedListener() {
  yield takeEvery(CAPTCHA_SOLVED, fetchTrackingInformation);
}

function* fetchTrackingInformation(action) {
  const trackingInformation = yield call(
    getResult,
    action.payload.headers,
    action.payload.cookies,
    action.payload.answer,
    action.payload.trackID
  );
  yield put({type: TRACK_FETCH_SUCCESS, payload: {data: trackingInformation.data, trackID: action.payload.trackID}});
}

function* trackInfoFetchSuccess() {
  yield takeEvery(TRACK_FETCH_SUCCESS, showTrackData);
}

function showTrackData(action) {
  const data = action.payload.data;
  if (data.erro === 'true') {
    console.log(`[ERRO] erro no pacote ${action.payload.trackID}: ${data.mensagem}`);
    return;
  }
  console.log(`=== Rastreio do pacote ${data.codObjeto} ===`);;
  console.log(`    categoria: ${data.tipoPostal.categoria}`);
  console.log(`    data prevista: ${data.dtPrevista.date.substring(0, data.dtPrevista.date.length-7)}`);
  console.log("    = Histórico =");

  data.eventos.slice().reverse().forEach((e) => {
    console.log(`        ${e.dtHrCriado.date.substring(0, e.dtHrCriado.date.length-7)}: ${e.descricao}`);
  });
}

export function* rootSaga() {
  yield fork(startWorkerListener);
  yield fork(captchaSolvedListener);
  yield fork(trackInfoFetchSuccess);
}
