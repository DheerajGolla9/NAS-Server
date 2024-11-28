document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const filesList = document.getElementById('files');
    const folderForm = document.getElementById('folderForm');
    const folderInput = document.getElementById('folderInput');

    loadFiles();

    uploadForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.message) {
                alert(data.message);
                loadFiles();
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert('Error uploading file!');
        }
    });

    folderForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const folderName = folderInput.value;

        try {
            const response = await fetch('/create_folder', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ folderName })
            });

            const data = await response.json();

            if (data.message) {
                alert(data.message);
                loadFiles();
                folderForm.reset();
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert('Error creating folder!');
        }
    });

    async function loadFiles() {
        try {
            const response = await fetch('/files');
            const files = await response.json();
            filesList.innerHTML = '';

            files.forEach(item => {
                const listItem = document.createElement('li');
                listItem.textContent = item.name;

                if (item.isFolder) {
                    // Create folder options
                    const renameButton = document.createElement('button');
                    renameButton.textContent = 'Rename';
                    renameButton.onclick = function () {
                        const newFolderName = prompt('Enter new folder name:', item.name);
                        if (newFolderName) {
                            fetch('/rename_folder', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ oldName: item.name, newName: newFolderName })
                            })
                                .then(response => response.json())
                                .then(data => {
                                    alert(data.message);
                                    loadFiles();
                                });
                        }
                    };
                    listItem.appendChild(renameButton);

                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.onclick = function () {
                        fetch(`/delete_folder/${item.name}`, { method: 'POST' })
                            .then(response => response.json())
                            .then(data => {
                                alert(data.message);
                                loadFiles();
                            })
                            .catch(error => alert('Error deleting folder!'));
                    };
                    listItem.appendChild(deleteButton);
                } else {
                    // Create file options
                    const downloadButton = document.createElement('button');
                    downloadButton.textContent = 'Download';
                    downloadButton.onclick = function () {
                        window.location.href = `/download/${item.name}`;
                    };
                    listItem.appendChild(downloadButton);

                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.onclick = function () {
                        fetch(`/delete/${item.name}`, { method: 'POST' })
                            .then(response => response.json())
                            .then(data => {
                                alert(data.message);
                                loadFiles();
                            })
                            .catch(error => {
                                console.log(error.error)
                                alert('Error deleting file!')
                            });
                    };
                    listItem.appendChild(deleteButton);
                }

                filesList.appendChild(listItem);
            });
        } catch (error) {
            alert('Error loading files!');
        }
    }

});
