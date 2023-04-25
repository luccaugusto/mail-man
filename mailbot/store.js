import pkg from '@reduxjs/toolkit';
import createSagaMiddleware from 'redux-saga';
const {configureStore} = pkg;
export const sagaMiddleware = createSagaMiddleware();

export const store = configureStore({
  reducer: () => {},
  middleware: (getDefaultMiddleware) => {
    return [
      ...getDefaultMiddleware(),
      sagaMiddleware,
    ];
  },
});
