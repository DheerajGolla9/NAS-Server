document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const filesList = document.getElementById('files');
    const diskUsageElement = document.getElementById('diskUsage');
    const folderForm = document.getElementById('folderForm');
    const folderInput = document.getElementById('folderInput');

    loadFiles();
    loadDiskUsage();

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
                            .catch(error => alert('Error deleting file!'));
                    };
                    listItem.appendChild(deleteButton);
                }

                filesList.appendChild(listItem);
            });
        } catch (error) {
            alert('Error loading files!');
        }
    }

    async function loadDiskUsage() {
        try {
            const response = await fetch('/system_info');
            const data = await response.json();

            if (data.error) {
                diskUsageElement.innerHTML = `Error: ${data.error}`;
                return;
            }

            const total = (data.total / (1024 * 1024 * 1024)).toFixed(2);  // GB
            const used = (data.used / (1024 * 1024 * 1024)).toFixed(2);  // GB
            const free = (data.free / (1024 * 1024 * 1024)).toFixed(2);  // GB
            const percent = data.percent;
            const cpuUsage = data.cpu_percent;
            const memoryUsage = data.memory_percent;

            diskUsageElement.innerHTML = `
                <p>Total: ${total} GB</p>
                <p>Used: ${used} GB</p>
                <p>Free: ${free} GB</p>
                <p>Disk Usage: ${percent}%</p>
                <p>CPU Usage: ${cpuUsage}%</p>
                <p>Memory Usage: ${memoryUsage}%</p>
            `;
        } catch (error) {
            diskUsageElement.innerHTML = 'Error loading disk usage info.';
        }
    }
});
