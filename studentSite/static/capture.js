const videoElement = document.getElementById('videoElement');
const canvasElement = document.getElementById('canvasElement');
const photoElement = document.getElementById('photoElement');
const startButton = document.getElementById('startButton');
const captureButton = document.getElementById('captureButton');

let stream;

async function startWebcam() {
    console.log('hi')
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

/*function capturePhoto() {
    canvasElement.width = videoElement.videoWidth;
    canvasElement.height = videoElement.videoHeight;
    canvasElement.getContext('2d').drawImage(videoElement, 0, 0);
    const photoDataUrl = canvasElement.toDataURL('image/jpeg');
    photoElement.src = photoDataUrl;
    photoElement.style.display = 'block';
}

captureButton.addEventListener('click', capturePhoto);*/

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

/*async function sendImageToBackend(photoDataUrl) {
    try {
        const response = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: photoDataUrl }),
        });

        if (!response.ok) {
            throw new Error('Failed to send image to backend');
        }

        // Handle the response from backend if needed
        const responseData = await response.json();
        console.log('Backend response:', responseData);
    } catch (error) {
        console.error('Error sending image to backend:', error);
    }
}*/
async function sendImageToBackend(photoDataUrl) {
    //try {
        const response = await fetch('http://127.0.0.1:3000/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: photoDataUrl }),
        }) 
        
        .then(response => response.json())
        .then(data => {
            if (data.redirect) {
                window.location.href = data.redirect_url;
            } else {
                // Handle other responses or show a message
                console.log(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });;

        /*const responseData = await response.json();

        if (responseData.status === 'success') {
            // Redirect to the success page
            window.location.href = responseData.redirect_url;
        } else {
            // Display an error message or redirect to an error page
            alert(responseData.message);
            // Optionally, you could redirect to an error page
            // window.location.href = 'http://127.0.0.1:5000/error';
        }
    } catch (error) {
        console.error('Error sending image to backend:', error);
    }*/
}


captureButton.addEventListener('click', capturePhoto);

