document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const filesList = document.getElementById('files');

    // Load files on page load
    loadFiles();

    // Handle the form submission for file upload
    uploadForm.addEventListener('submit', async function (e) {
        e.preventDefault(); // Prevent default form submission

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch('/upload', { // No need for full URL, relative path works
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.message) {
                alert(data.message); // Show success message
                loadFiles(); // Reload file list
            } else {
                alert(data.error); // Show error message
            }
        } catch (error) {
            alert('Error uploading file!');
        }
    });

    // Function to load the list of files
    async function loadFiles() {
        try {
            const response = await fetch('/files'); // No need for full URL, relative path works
            const files = await response.json();

            filesList.innerHTML = ''; // Clear existing file list

            files.forEach(file => {
                const listItem = document.createElement('li');
                listItem.textContent = file;
                
                // Create a download button for each file
                const downloadButton = document.createElement('button');
                downloadButton.textContent = 'Download';
                downloadButton.onclick = function () {
                    window.location.href = `/download/${file}`; // Trigger file download
                };
                listItem.appendChild(downloadButton);
                
                filesList.appendChild(listItem);
            });
        } catch (error) {
            alert('Error loading file list!');
        }
    }
});
