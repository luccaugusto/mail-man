import {store} from './store.js'
import {startWorkerAction} from './actions.js';
import fs from 'fs';

export function addTrackingCode(trackingCodeList) {
  trackingCodeList.forEach((trackingCode) => {
    if (trackingCode.length != 13) {
      console.log(`Invalid tracking code: ${trackingCode}`);
    } else {
      fs.appendFile('tracking-code-list.txt', `${trackingCode}\n`, function (err) {
        if (err) throw err;
      });
    }
  });
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
  fs.readFile('tracking-code-list.txt', 'utf8', function(err, data) {
    if (err) throw err;
    const trackingCodeList = data.split('\n');
    trackPackage(trackingCodeList);
  });
}

export function removeTrackingCode(trackingCodeList) {
  const currentTrackingCodeList = fs.readFileSync('tracking-code-list.txt', 'utf8').split('\n');
  const newTrackingCodeList = currentTrackingCodeList.filter((trackingCode) => {
    return !trackingCodeList.includes(trackingCode);
  });
  fs.writeFileSync('tracking-code-list.txt', newTrackingCodeList.join('\n'));
}

export function removeAllTrackingCodes() {
  fs.writeFile('tracking-code-list.txt', '', ()=>{});
}
