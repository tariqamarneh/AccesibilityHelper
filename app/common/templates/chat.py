js_code = """
// Create the main button
var button = document.createElement('button');
button.id = 'myButton-helper'; 
button.innerHTML = 'helper';
button.style.position = 'fixed';
button.style.bottom = '10px';
button.style.right = '10px';
button.style.padding = '10px 20px';
button.style.backgroundColor = '#4CAF50';
button.style.color = 'white';
button.style.border = 'none';
button.style.borderRadius = '5px';
button.style.cursor = 'pointer';
button.style.transition = 'all 0.5s ease-in-out';
document.body.appendChild(button);

// Create the container for input field and buttons, initially hidden
var container = document.createElement('div');
container.style.position = 'fixed';
container.style.bottom = '10px';
container.style.right = '1px';
container.style.display = 'flex';
container.style.alignItems = 'center';
container.style.width = '0'; 
container.style.overflow = 'hidden';
container.style.transition = 'width 0.5s ease-in-out';
document.body.appendChild(container);

// Create the arrow button
var arrowButton = document.createElement('button');
arrowButton.innerHTML = '→';
arrowButton.style.padding = '10px';
arrowButton.style.backgroundColor = '#f1f1f1';
arrowButton.style.color = 'black';
arrowButton.style.border = 'none';
arrowButton.style.borderRadius = '5px';
arrowButton.style.cursor = 'pointer';
arrowButton.style.opacity = '0';
arrowButton.style.transition = 'opacity 0.5s ease-in-out';
arrowButton.style.marginRight = '10px';
container.appendChild(arrowButton);

// Create the microphone button
var micButton = document.createElement('button');
micButton.innerHTML = '🎤';
micButton.style.padding = '10px';
micButton.style.backgroundColor = '#f1f1f1';
micButton.style.color = 'black';
micButton.style.border = 'none';
micButton.style.borderRadius = '5px';
micButton.style.cursor = 'pointer';
micButton.style.opacity = '0';
micButton.style.transition = 'opacity 0.5s ease-in-out';
micButton.style.marginRight = '10px';
container.appendChild(micButton);

// Create the input field
var inputField = document.createElement('input');
inputField.type = 'text';
inputField.placeholder = 'What do you want to do?';
inputField.style.color = 'black';
inputField.style.padding = '10px';
inputField.style.border = '1px solid #ccc';
inputField.style.borderRadius = '5px';
inputField.style.marginRight = '10px';
inputField.style.opacity = '0';
inputField.style.transition = 'opacity 0.5s ease-in-out';
container.appendChild(inputField);

// Create the loading circle
var loadingCircle = document.createElement('div');
loadingCircle.style.border = '4px solid #f3f3f3'; /* Light grey */
loadingCircle.style.borderTop = '4px solid #3498db'; /* Blue */
loadingCircle.style.borderRadius = '50%';
loadingCircle.style.width = '24px';
loadingCircle.style.height = '24px';
loadingCircle.style.animation = 'spin 1s linear infinite';
loadingCircle.style.display = 'none'; // Initially hidden

// Create the send button
var sendButton = document.createElement('button');
sendButton.style.padding = '10px 20px';
sendButton.style.backgroundColor = '#008CBA';
sendButton.style.color = 'white';
sendButton.style.border = 'none';
sendButton.style.borderRadius = '5px';
sendButton.style.cursor = 'pointer';
sendButton.style.opacity = '0';
sendButton.style.transition = 'opacity 0.5s ease-in-out';
sendButton.style.position = 'relative';
sendButton.style.display = 'flex';
sendButton.style.alignItems = 'center';
sendButton.style.justifyContent = 'center';
sendButton.style.width = '100px'; // Fixed width to prevent shrinking

var buttonContent = document.createElement('span');
buttonContent.innerHTML = 'Send';
sendButton.appendChild(buttonContent);

// Append the loading circle to the send button
sendButton.appendChild(loadingCircle);
container.appendChild(sendButton);

// Add keyframes for the spin animation
var styleSheet = document.createElement('style');
styleSheet.type = 'text/css';
styleSheet.innerText = `
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}`;
document.head.appendChild(styleSheet);

// Add hover effect for the main button
button.onmouseover = function() {
    button.style.backgroundColor = '#45a049';
};
button.onmouseout = function() {
    button.style.backgroundColor = '#4CAF50';
};

// Expand the button and show input field and send button on click
button.onclick = function() {
    button.style.display = 'none';
    container.style.width = '350px';
    container.style.backgroundColor = '#808080'
    container.style.borderRadius = '5px';
    setTimeout(function() {
        micButton.style.opacity = '1';
        arrowButton.style.opacity = '1';
        inputField.style.opacity = '1';
        sendButton.style.opacity = '1';
    }, 10);
    console.log('clicker');
};

// Make a POST request with the input field data when the send button is clicked
sendButton.onclick = function() {
    sendButton.disabled = true;
    sendButton.style.backgroundColor = '#808080';
    sendButton.style.cursor = 'not-allowed';
    buttonContent.style.display = 'none';
    loadingCircle.style.display = 'block'; 

    var userInput = inputField.value;
    var url = 'http://127.0.0.1:8080/bot?request=' + encodeURIComponent(userInput);
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        sendButton.disabled = false;
        sendButton.style.backgroundColor = '#008CBA';
        sendButton.style.cursor = 'pointer';
        buttonContent.style.display = 'inline'; // Restore the text
        loadingCircle.style.display = 'none';
    })
    .catch(error => {
        console.error('Error:', error);
        sendButton.disabled = false;
        sendButton.style.backgroundColor = '#008CBA';
        sendButton.style.cursor = 'pointer';
        buttonContent.style.display = 'inline'; // Restore the text
        loadingCircle.style.display = 'none';
    });

    console.log('Input:', userInput);
};

// Collapse the input field and send button back into the main button on arrow button click
arrowButton.onclick = function() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
    }
    micButton.style.opacity = '0';
    arrowButton.style.opacity = '0';
    inputField.style.opacity = '0';
    sendButton.style.opacity = '0';
    container.style.width = '0';
    setTimeout(function() {
        button.style.display = 'block';
    }, 500);
};

// Audio recording functionality
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

micButton.onclick = function() {
    if (isRecording) {
        mediaRecorder.stop();
    } else {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
                mediaRecorder.start();
                isRecording = true;

                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener('stop', () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    sendAudio(audioBlob);
                    audioChunks = [];
                    isRecording = false;
                });
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
                alert('Error accessing microphone: ' + error.message);
            });
    }
};

function sendAudio(audioBlob) {
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.wav');

    fetch('http://127.0.0.1:8080/upload_audio', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}
"""
