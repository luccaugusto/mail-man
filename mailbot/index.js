import pkg from '@reduxjs/toolkit';
const {configureStore} = pkg;
import createSagaMiddleware from 'redux-saga';
import {rootSaga} from './saga.js';
import {startWorkerAction} from './actions.js';

const sagaMiddleware = createSagaMiddleware();
const store = configureStore({
  reducer: () => {},
  middleware: (getDefaultMiddleware) => {
    return [
      ...getDefaultMiddleware(),
      sagaMiddleware,
    ];
  },
});

sagaMiddleware.run(rootSaga);

var args = process.argv.slice(2);

if (args.length > 0) {
  args.forEach((arg) => {
    store.dispatch(startWorkerAction(arg));
  });
}
