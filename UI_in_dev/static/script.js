const chatInput = document.getElementById('chat_input');

// Function to resize the textarea
function resizeTextarea() {
  chatInput.style.height = 'auto'; // Reset height to allow expansion
  chatInput.style.height = chatInput.scrollHeight + 'px'; // Set height based on content
}

// Event listener for input changes
chatInput.addEventListener('input', resizeTextarea);

// Initial resize to ensure proper height on page load
resizeTextarea();

let currentFilePath = null;

// Function to handle file upload
function handleFileUpload() {
  const fileInput = document.getElementById('file_upload');
  const file = fileInput.files[0];

  if (file) {
    currentFilePath = file.path;
    document.getElementById('selected_file_name').textContent = "Selected file: " + file.name; // Display file name
    console.log("File uploaded:", currentFilePath); // For debugging
  }
}

function sendMessage() {
    const chatHistory = document.getElementById('chat_history');
    const chatInput = document.getElementById('chat_input');
    const message = chatInput.value;

    const userMessageElement = document.createElement('div');
    userMessageElement.classList.add('user-message');
    userMessageElement.textContent = message;
    chatHistory.appendChild(userMessageElement);
  
    // Clear the input
    chatInput.value = '';

    const formData = new FormData();
    formData.append('message', message);
  
    if (currentFilePath) { 
        formData.append('file', currentFilePath); 
    }

    fetch('/send_message', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {

    const serverResponseElement = document.createElement('div');
    serverResponseElement.classList.add('server-message');
    serverResponseElement.textContent = data.response;
    chatHistory.appendChild(serverResponseElement);
    })
}
document.getElementById('file_upload').addEventListener('change', handleFileUpload);
