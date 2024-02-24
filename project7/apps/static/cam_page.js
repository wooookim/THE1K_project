//DOM
const recordButton = document.querySelector(".record-button");
const stopButton = document.querySelector(".end-button");
const downloadButton = document.querySelector(".video-download");

const previewPlayer = document.querySelector("#cam");

let recorder;
let recorderedCunks;  // data input

//functions
function videoStart() {
  navigator.mediaDevices.getUserMedia({video: true, audio:false})
  .then(stream => {
    previewPlayer.srcObject = stream;
    startRecording(previewPlayer.captureStream())
  })
}

function startRecording(stream) {
  recorderedCunks = [];
  recorder = new MediaRecorder(stream);
  recorder.ondataavailable = (e) => {recorderedCunks.push(e.data)}
  recorder.start(); 
}

function stopRecording() {
  previewPlayer.srcObject.getTracks().forEach(track => track.stop());
  recorder.stop();
}

function downloadRecording() {
  const recordedBlob = new Blob(recorderedCunks, {type:"video/webm"});
  let url = URL.createObjectURL(recordedBlob);
  let a = document.createElement('a');
  a.href = url;
  a.download = 'recorded_video.webm';
  document.body.appendChild(a);
  a.click();
  setTimeout(function() {
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }, 0);
  // const downloadURL = window.URL.createObjectURL(recordedBlob);

  // // 다운로드 구현해야됨 --------------------------------------------------------
  // downloadButton.href = downloadURL;
  // downloadButton.download = 'test.webm';
  // console.log(downloadURL);
}

recordButton.addEventListener("click", videoStart);
stopButton.addEventListener("click", stopRecording);
downloadButton.addEventListener("click", downloadRecording)