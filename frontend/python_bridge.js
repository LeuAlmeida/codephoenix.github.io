// Python Bridge - Direct command execution without backend server

// Main function to run the scanner
async function runRealPythonScanner(config) {
    try {
        // Generate Python command
        const pythonCommand = generatePythonCommand(config);
        
        // Show command execution interface
        showCommandInterface(pythonCommand);
        
        // Update status to waiting for execution
        updateStatus('Waiting for command execution...', 20);
        
    } catch (error) {
        throw new Error('Error preparing scan: ' + error.message);
    }
}

// Generate the Python command with proper escaping
function generatePythonCommand(config) {
    const args = [
        `--token "${config.githubToken}"`,
        `--search-terms "${config.searchTerms.replace(/"/g, '\\"')}"`,
        `--results-per-page ${config.resultsPerPage}`,
        `--pages ${config.pages}`,
        `--sleep-time ${config.sleepTime}`
    ];
    
    if (config.startDate) {
        args.push(`--start-date "${config.startDate}"`);
    }
    
    if (config.endDate) {
        args.push(`--end-date "${config.endDate}"`);
    }
    
    const outputFile = 'scan_results.json';
    args.push(`--output-file "${outputFile}"`);
    
    return `python run_frontend_scan.py ${args.join(' ')}`;
}

// Show the command execution interface
function showCommandInterface(command) {
    const interfaceHtml = `
        <div class="bg-gray-800 rounded-xl border border-git-border p-6 mb-6">
            <h3 class="text-lg font-semibold mb-4 flex items-center">
                <i class="fas fa-terminal mr-2 text-git-accent"></i>
                Execute Command
            </h3>
            
            <div class="bg-gray-900 rounded-lg p-4 mb-4 relative group">
                <pre class="text-green-400 text-sm overflow-x-auto whitespace-pre-wrap" id="commandText">${command}</pre>
                <button onclick="copyCommand()" 
                        class="absolute top-2 right-2 bg-git-accent hover:bg-git-accent/80 text-white px-3 py-1 rounded text-xs">
                    <i class="fas fa-copy mr-1"></i>Copy
                </button>
            </div>
            
            <div class="space-y-4">
                <div class="bg-blue-900/30 border border-blue-500 rounded-lg p-4">
                    <h4 class="font-semibold text-blue-400 mb-2">How to execute:</h4>
                    <ol class="list-decimal list-inside space-y-2 text-sm text-gray-300">
                        <li>Copy the command above</li>
                        <li>Open Terminal in the project directory</li>
                        <li>Paste and run the command</li>
                        <li>Wait for execution to complete</li>
                        <li>Select the results file below</li>
                    </ol>
                </div>
                
                <div class="flex items-center space-x-4">
                    <label class="flex-1">
                        <span class="sr-only">Select results file</span>
                        <input type="file" 
                               accept=".json"
                               onChange="handleResultFileSelect(event)"
                               class="block w-full text-sm text-gray-400
                                      file:mr-4 file:py-2 file:px-4
                                      file:rounded-lg file:border-0
                                      file:text-sm file:font-semibold
                                      file:bg-git-accent file:text-white
                                      hover:file:bg-git-accent/80
                                      cursor-pointer"/>
                    </label>
                </div>
            </div>
        </div>
    `;
    
    const resultsDisplay = document.getElementById('resultsDisplay');
    resultsDisplay.innerHTML = interfaceHtml;
}

// Copy command to clipboard
function copyCommand() {
    const commandText = document.getElementById('commandText').textContent;
    navigator.clipboard.writeText(commandText)
        .then(() => showNotification('Command copied to clipboard!', 'success'))
        .catch(() => {
            const textarea = document.createElement('textarea');
            textarea.value = commandText;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            showNotification('Command copied!', 'success');
        });
}

// Handle result file selection
async function handleResultFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    try {
        const content = await readFileContent(file);
        const results = JSON.parse(content);
        
        // Process and display results
        displayResults(results);
        updateStatus('Results loaded successfully!', 100);
        showNotification('Scan results loaded successfully!', 'success');
        
    } catch (error) {
        showNotification('Error processing results: ' + error.message, 'error');
    }
}

// Read file content
function readFileContent(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(new Error('Error reading file'));
        reader.readAsText(file);
    });
}

// Display scan results
function displayResults(results) {
    const resultsDisplay = document.getElementById('resultsDisplay');
    
    if (!results || !results.output) {
        resultsDisplay.innerHTML = `
            <div class="bg-gray-800 rounded-xl border border-git-border p-6 text-center">
                <i class="fas fa-exclamation-circle text-git-accent text-4xl mb-4"></i>
                <h3 class="text-lg font-semibold mb-2">Invalid Results Format</h3>
                <p class="text-gray-400">The results file does not contain valid scan data.</p>
            </div>
        `;
        return;
    }
    
    // Parse the output for structured results
    const parsedResults = parseResults(results.output);
    
    if (parsedResults.length === 0) {
        resultsDisplay.innerHTML = `
            <div class="bg-gray-800 rounded-xl border border-git-border p-6 text-center">
                <i class="fas fa-search text-gray-400 text-4xl mb-4"></i>
                <h3 class="text-lg font-semibold mb-2">No Results Found</h3>
                <p class="text-gray-400">The scan did not find any matches for your search terms.</p>
            </div>
        `;
        return;
    }
    
    // Display each result group
    let resultsHtml = '<div class="space-y-6">';
    
    parsedResults.forEach(group => {
        resultsHtml += createResultGroupHtml(group);
    });
    
    resultsHtml += '</div>';
    resultsDisplay.innerHTML = resultsHtml;
}

// Parse raw results into structured format
function parseResults(output) {
    const results = [];
    let currentGroup = null;
    
    const lines = output.split('\n');
    for (const line of lines) {
        if (line.includes('=== Termo:')) {
            if (currentGroup) {
                results.push(currentGroup);
            }
            const term = line.split('=== Termo:')[1].split('===')[0].trim();
            currentGroup = { term, items: [] };
        } else if (currentGroup && line.includes('📁')) {
            const [repo, ...pathParts] = line.split('📁')[1].split('-').map(p => p.trim());
            const path = pathParts.join('-').trim();
            if (repo && path) {
                currentGroup.items.push({
                    repo,
                    path,
                    url: `https://github.com/${repo}/blob/main/${path}`
                });
            }
        }
    }
    
    if (currentGroup) {
        results.push(currentGroup);
    }
    
    return results;
}

// Create HTML for a result group
function createResultGroupHtml(group) {
    return `
        <div class="bg-gray-800 rounded-xl border border-git-border p-6">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-semibold flex items-center">
                    <i class="fas fa-search text-git-accent mr-2"></i>
                    ${group.term}
                </h3>
                <span class="text-sm text-gray-400">${group.items.length} result(s)</span>
            </div>
            
            <div class="space-y-3">
                ${group.items.map(item => `
                    <div class="bg-gray-700/50 rounded-lg p-4 border-l-4 border-git-accent">
                        <div class="flex items-center justify-between">
                            <div class="flex-1">
                                <div class="flex items-center space-x-2 mb-2">
                                    <i class="fab fa-github text-gray-400"></i>
                                    <span class="font-medium">${item.repo}</span>
                                    <span class="text-gray-400">-</span>
                                    <span class="text-git-accent">${item.path}</span>
                                </div>
                            </div>
                            <a href="${item.url}" target="_blank" 
                               class="ml-4 bg-git-accent hover:bg-git-accent/80 text-white px-3 py-1 rounded text-sm flex items-center">
                                <i class="fas fa-external-link-alt mr-1"></i>
                                View
                            </a>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

