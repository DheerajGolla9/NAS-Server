document.addEventListener('DOMContentLoaded', function () {
    
    const diskUsageElement = document.getElementById('diskUsage');
    

    loadDiskUsage();


    async function loadDiskUsage() {
        console.log("Disk Usage");
        diskUsageElement.innerHTML = `
        <p>Total: 0 GB</p>
        <p>Used: 0 GB</p>
        <p>Free: 0 GB</p>
        <p>Disk Usage: 0%</p>
        <p>CPU Usage: 0%</p>
        <p>Memory Usage: 0%</p>
    `;
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
