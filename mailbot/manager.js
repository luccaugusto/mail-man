import {store} from './store.js'
import {startWorkerAction} from './actions.js';

export function addTrackingCode(trackingCodeList) {
  console.log(trackingCodeList);
}

export function trackPackage(trackingCodeList){
  trackingCodeList.forEach((trackingCode) => {
    if (trackingCode.length != 13) {
      console.log(`Invalid tracking code: ${trackingCode}`);
    } else {
      store.dispatch(startWorkerAction(trackingCode));
    }
  });
}

export function trackAllPackages() {

}

export function removeTrackingCode(trackingCodeList) {
  console.log(trackingCodeList);
}

export function removeAllTrackingCodes() {

}
