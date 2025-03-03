(function() {
    let portGroups = [];
    let selectedSubmodules = [];
    let independentPorts = [];

    function loadConfiguration() {
        const filename = new URLSearchParams(window.location.search).get('filename');
        
        if (!filename) {
            alert('No filename found in URL.');
            return;
        }

        // Load port groups
        fetch('/get_groups')
            .then(response => response.json())
            .then(data => {
                if (data.groups) {
                    portGroups = data.groups;
                    displayPortGroups();
                }
            })
            .catch(error => {
                console.error('Error loading port groups:', error);
            });

        // Load selected submodules
        fetch('/get_selected_submodules')
            .then(response => response.json())
            .then(data => {
                if (data.submodules) {
                    selectedSubmodules = data.submodules;
                    displaySubmodules();
                }
            })
            .catch(error => {
                console.error('Error loading selected submodules:', error);
            });

        // Load independent ports
        fetch(`/get_independent_ports?filename=${filename}`)
            .then(response => response.json())
            .then(data => {
                if (data.ports) {
                    independentPorts = data.ports;
                    displayIndependentPorts();
                }
            })
            .catch(error => {
                console.error('Error loading independent ports:', error);
            });
    }

    function displayPortGroups() {
        const container = document.getElementById('port-groups-info');
        container.innerHTML = '';

        if (portGroups.length === 0) {
            container.innerHTML = '<p class="text-muted">No port groups defined</p>';
            return;
        }

        const table = document.createElement('table');
        table.className = 'table table-hover';
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Group Name</th>
                    <th>Ports</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        `;

        portGroups.forEach(group => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${group.name}</td>
                <td>${group.ports.map(port => port.name).join(', ')}</td>
            `;
            table.querySelector('tbody').appendChild(row);
        });

        container.appendChild(table);
    }

    function displayIndependentPorts() {
        const container = document.getElementById('independent-ports-info');
        container.innerHTML = '';

        if (independentPorts.length === 0) {
            container.innerHTML = '<p class="text-muted">No independent ports</p>';
            return;
        }

        const table = document.createElement('table');
        table.className = 'table table-hover';
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Port Name</th>
                    <th>Direction</th>
                    <th>Width</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        `;

        independentPorts.forEach(port => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${port.name}</td>
                <td>${port.type || 'N/A'}</td>
                <td>${port.width || '1'}</td>
            `;
            table.querySelector('tbody').appendChild(row);
        });

        container.appendChild(table);
    }

    function displaySubmodules() {
        const container = document.getElementById('submodules-info');
        container.innerHTML = '';

        if (selectedSubmodules.length === 0) {
            container.innerHTML = '<p class="text-muted">No submodules selected</p>';
            return;
        }

        const table = document.createElement('table');
        table.className = 'table table-hover';
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Submodule Name</th>
                    <th>Instance Name</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        `;

        selectedSubmodules.forEach(submodule => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${submodule.name}</td>
                <td>${submodule.instance}</td>
            `;
            table.querySelector('tbody').appendChild(row);
        });

        container.appendChild(table);
    }

    function generateDrawIO() {
        const filename = new URLSearchParams(window.location.search).get('filename');
        if (!filename) {
            alert('No filename found in URL.');
            return;
        }

        // Get all ports from groups and independent ports
        const allPorts = [
            ...portGroups.flatMap(group => group.ports),
            ...independentPorts
        ];

        fetch(`/generate/${filename}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                port_groups: portGroups,
                submodules: selectedSubmodules,
                ports: allPorts  // Add all ports information
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    console.error('Server error response:', text);
                    throw new Error(text || 'Failed to generate DrawIO file');
                });
            }
            // Try to parse as JSON first, if fails, treat as text
            return response.text().then(text => {
                console.log('Server response:', text);
                try {
                    return JSON.parse(text);
                } catch (e) {
                    return { file_path: text };
                }
            });
        })
        .then(data => {
            if (data.file_path) {
                const downloadLink = document.getElementById('download-link');
                const filePath = data.file_path;
                console.log('Setting download link to:', filePath);
                downloadLink.href = filePath;
                // Remove .v extension from filename for download
                const baseFilename = filename.replace('.v', '');
                downloadLink.download = baseFilename + '.drawio';
                
                // Show download section
                document.getElementById('download-section').classList.remove('d-none');
            } else {
                console.error('No file path in response:', data);
                throw new Error('No file path received from server');
            }
        })
        .catch(error => {
            console.error('Error generating DrawIO file:', error);
            alert(error.message || 'Failed to generate DrawIO file.');
        });
    }

    // Handle panel visibility changes
    document.addEventListener('panelVisibilityChanged', (event) => {
        if (event.detail.panelId === 'generate-drawio' && event.detail.isVisible) {
            // Force reload configuration
            portGroups = [];
            selectedSubmodules = [];
            independentPorts = [];
            loadConfiguration();
        }
    });

    // Initial load if panel is visible
    document.addEventListener('DOMContentLoaded', () => {
        const generateDrawioPanel = document.getElementById('generate-drawio');
        if (!generateDrawioPanel.classList.contains('d-none')) {
            loadConfiguration();
        }
    });

    // Expose necessary functions to global scope
    window.generateDrawIO = generateDrawIO;
    window.loadConfiguration = loadConfiguration;
})(); 