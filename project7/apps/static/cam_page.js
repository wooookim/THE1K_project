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
  const downloadURL = window.URL.createObjectURL(recordedBlob);

  // 다운로드 구현해야됨 --------------------------------------------------------
  downloadButton.href = downloadURL;
  downloadButton.download = 'test.webm';
  console.log(downloadURL);
}

recordButton.addEventListener("click", videoStart);
stopButton.addEventListener("click", stopRecording);
downloadButton.addEventListener("click", downloadRecording)









// document.addEventListener("DOMContentLoaded", () => {
//     new App();
//   })
  
//   class App {
//     constructor() {
  
//       const video = document.querySelector("#videoElement");
  
//       if (navigator.mediaDevices.getUserMedia) {
//         navigator.mediaDevices.getUserMedia({ video: true })
//           .then( (stream) => { // function 의 this와 화살표 함수의 this 가 다름
//             video.srcObject = stream;
//           })
//           .catch(function (error) {
//             console.log("Something went wrong!");
//             console.log(error);
//             return;
//           });
//       }
  
//       video.addEventListener( "loadedmetadata", () => {
//         window.requestAnimationFrame(this.draw.bind(this));
//       });
//     }
  
//     // draw(t) {
  
//     //   window.requestAnimationFrame(this.draw.bind(this));
      
//     //   // const canvas = document.querySelector("#mirrored");
//     //   // const video = document.querySelector("#videoElement");
//     //   //   canvas.width = video.videoWidth;
//     //   //   canvas.height = video.videoHeight;
  
//     //   // const ctx = canvas.getContext('2d');
//     //   // ctx.translate(video.videoWidth, 0);
//     //   // ctx.scale(-1,1);
//     //   // ctx.drawImage(video, 0, 0, 
//     //   //     video.videoWidth, 
//     //   //     video.videoHeight);  
      
//     // }
//   }

//   function takePhoto(){
//     snap.currentTime = 0;
//     snap.play();

//     const data = canvas.toDataURL('image/jpeg');

//     const link = document.createElement('a');
//     link.href = data;
//     link.innerHTML = `<img src="${data}" alt="Handsome Man" />`;
//     link.setAttribute('download', 'handsome');
    
//     strip.insertBefore(link, strip.firstChild);

// }


// function time_counter(){
//   var count_time = document.querySelector(".now_time_stamp");
//   var real_time = document.querySelector(".real_time_stamp");
// }