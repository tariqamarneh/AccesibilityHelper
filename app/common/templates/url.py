js_code = """
// Create the input field
var inputField = document.createElement('input');
inputField.type = 'text';
inputField.placeholder = 'Enter a URL';
inputField.style.color = 'black';
inputField.style.padding = '20px';
inputField.style.border = '2px solid #ccc';
inputField.style.borderRadius = '10px';
inputField.style.marginRight = '10px';
inputField.style.fontSize = '24px';
inputField.style.width = '100%';
inputField.style.opacity = '0';
inputField.style.transition = 'opacity 0.5s ease-in-out';

// Create a container for the input field
var container = document.createElement('div');
container.style.position = 'absolute';
container.style.top = '50%';
container.style.left = '50%';
container.style.transform = 'translate(-50%, -50%)';
container.style.textAlign = 'center';
container.appendChild(inputField);

// Append the container to the body
document.body.appendChild(container);

// Make the input visible after appending to the body
setTimeout(function() {
    inputField.style.opacity = '1';
}, 0);

inputField.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const url = inputField.value;
        if (url) {
            fetch(`http://127.0.0.1:8080/open_url?url=${encodeURIComponent(url)}`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json'
                },
                body: '' // Empty body
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
        } else {
            alert('Please enter a URL');
        }
    }
});

"""