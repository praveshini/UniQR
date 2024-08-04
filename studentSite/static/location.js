
const locButton=document.getElementById('get-location');


 function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const { latitude, longitude } = position.coords;
            const time=position.timestamp;
            sendLocationToServer(latitude, longitude,time)
            console.log("klo")
        }, (error) => {
            console.error('Error getting location:', error);
        });
    } else {
        console.error('Geolocation is not supported by this browser.');
    }
};

locButton.addEventListener('click', getLocation);

function sendLocationToServer(latitude, longitude,time) {
    fetch('http://127.0.0.1:3000/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ latitude, longitude,time })
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
});
}
/*const successCallback = (position) => {
    console.log(position);
  };

  const options = {
    enableHighAccuracy: true,
  };  
  const errorCallback = (error) => {
    console.log(error);
  };
  
  navigator.geolocation.getCurrentPosition(successCallback, errorCallback,options);*/

  console.log("hi")