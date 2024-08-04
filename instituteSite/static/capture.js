const videoElement = document.getElementById('videoElement');
const canvasElement = document.getElementById('canvasElement');
const photoElement = document.getElementById('photoElement');
const startButton = document.getElementById('startButton');
const captureButton = document.getElementById('captureButton');

let stream;

async function startWebcam() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoElement.srcObject = stream;
        startButton.disabled = true;
        captureButton.disabled = false;
    } catch (error) {
        console.error('Error accessing webcam:', error);
    }
}

startButton.addEventListener('click', startWebcam);

function capturePhoto() {
    canvasElement.width = videoElement.videoWidth;
    canvasElement.height = videoElement.videoHeight;
    canvasElement.getContext('2d').drawImage(videoElement, 0, 0);
    const photoDataUrl = canvasElement.toDataURL('image/jpeg');

    // Display the captured photo
    photoElement.src = photoDataUrl;
    photoElement.style.display = 'block';

    // Send the captured image to the backend
    sendImageToBackend(photoDataUrl);
}

async function sendImageToBackend(photoDataUrl) {
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: photoDataUrl }),
        });

        const data = await response.json();

        if (data.redirect) {
            window.location.href = data.redirect_url;
        } else {
            // Handle other responses or show a message
            console.log(data.message);
        }
    } catch (error) {
        console.error('Error sending image to backend:', error);
    }
}

captureButton.addEventListener('click', capturePhoto);
