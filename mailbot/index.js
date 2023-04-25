import {rootSaga} from './saga.js';
import {sagaMiddleware} from './store.js';
import {addTrackingCode, trackPackage, trackAllPackages, removeTrackingCode, removeAllTrackingCodes} from './manager.js';

sagaMiddleware.run(rootSaga);

function showHelp() {
  console.log("Usage: mail-man [arg] [tracking code list]");
  console.log("\t-a tracking-code: add a tracking code to the list");
  console.log("\t-t tracking-code: track a single package");
  console.log("\t-r tracking-code: remove a package from the list");
  console.log("\t--track-all: track all packages from the list");
  console.log("\t--remove-all: remove all packages from the list");
}

var args = process.argv.slice(2);

let task = showHelp;
let codeList = [];
let getCodeList = true;

switch(args[0]) {
  case '-a':
    task = addTrackingCode;
    break;
  case '-t':
    task = trackPackage;
    break;
  case '-r':
    task = removeTrackingCode;
    break;
  case '--track-all':
    task = trackAllPackages;
    getCodeList = false;
    break;
  case '--remove-all':
    task = removeAllTrackingCodes;
    getCodeList = false;
    break;
  default:
    task = showHelp;
}

if (getCodeList) {
  codeList = args.slice(1);
  if (codeList.length === 0) {
    console.log('Error: Missing tracking codes');
    task = showHelp;
  }
}

task(codeList);
