/* Fusion 360 Copilot Panel JavaScript */

// State
let currentCode = null;
let currentPlan = null;
let currentTitle = null;
let currentNotes = null;
let isExecuting = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadSettings();
    updateContext();
});

function initializeEventListeners() {
    // Chat input
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Code panel buttons
    document.getElementById('explainBtn').addEventListener('click', explainCode);
    document.getElementById('copyBtn').addEventListener('click', copyCode);
    document.getElementById('applyBtn').addEventListener('click', applyCode);
    document.getElementById('rejectBtn').addEventListener('click', rejectCode);
    
    // Execution buttons
    document.getElementById('undoBtn').addEventListener('click', undoExecution);
    document.getElementById('closeExecutionBtn').addEventListener('click', closeExecution);
    
    // Error panel
    document.getElementById('fixAndRetryBtn').addEventListener('click', fixAndRetry);
    
    // Settings
    document.getElementById('settingsBtn').addEventListener('click', openSettings);
    document.getElementById('saveSettingsBtn').addEventListener('click', saveSettings);
    document.getElementById('cancelSettingsBtn').addEventListener('click', closeSettings);
    document.getElementById('helpBtn').addEventListener('click', showHelp);
    
    // Modal close
    document.querySelectorAll('.close-btn').forEach(btn => {
        btn.addEventListener('click', closeSettings);
    });
}

// Message sending
function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Display user message
    addMessage(message, 'user');
    userInput.value = '';
    userInput.style.height = 'auto';
    
    // Simulate API call (will be connected to Python backend)
    displayGeneratingMessage();
    
    // TODO: Call Python backend via Fusion API bridge
    simulateCodeGeneration(message);
}

function addMessage(text, type = 'assistant') {
    const messagesContainer = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = `<p>${escapeHtml(text)}</p>`;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function displayGeneratingMessage() {
    const messagesContainer = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system';
    messageDiv.id = 'generatingMessage';
    messageDiv.innerHTML = '<p>Generating code... ⏳</p>';
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeGeneratingMessage() {
    const msg = document.getElementById('generatingMessage');
    if (msg) msg.remove();
}

// Simulated code generation (replace with actual backend call)
function simulateCodeGeneration(userMessage) {
    setTimeout(() => {
        removeGeneratingMessage();
        
        const response = {
            title: "Create Parametric Bracket",
            plan: [
                "Create user parameters (width, height, thickness)",
                "Create a sketch on XY plane",
                "Draw rectangle using parameters",
                "Extrude sketch with thickness parameter",
                "Name features for future edits"
            ],
            code: `# Create a parametric bracket
def create_bracket(doc):
    design = doc.design
    root = design.rootComponent
    
    # Create user parameters
    params = design.userParameters
    try:
        width_param = params.itemByName('Width')
    except:
        width_param = params.add('Width', adsk.core.ValueInput.createByReal(100), 'mm')
    
    try:
        height_param = params.itemByName('Height')
    except:
        height_param = params.add('Height', adsk.core.ValueInput.createByReal(50), 'mm')
    
    try:
        thickness_param = params.itemByName('Thickness')
    except:
        thickness_param = params.add('Thickness', adsk.core.ValueInput.createByReal(10), 'mm')
    
    print("Parameters created successfully")
    return True

# Execute
create_bracket(doc)`,
            notes: "This creates a parametric bracket. You can adjust width, height, and thickness parameters later. All features are named for easy editing."
        };
        
        showCodePanel(response);
    }, 2000);
}

function showCodePanel(response) {
    currentCode = response.code;
    currentPlan = response.plan;
    currentTitle = response.title;
    currentNotes = response.notes;
    
    // Update title
    document.getElementById('codeTitle').textContent = currentTitle;
    
    // Update plan
    if (currentPlan && currentPlan.length > 0) {
        const planList = document.getElementById('planList');
        planList.innerHTML = currentPlan.map(step => `<li>${escapeHtml(step)}</li>`).join('');
        document.getElementById('planSection').style.display = 'block';
    }
    
    // Update code
    document.getElementById('codeBlock').textContent = currentCode;
    
    // Update notes
    if (currentNotes) {
        document.getElementById('noteText').textContent = currentNotes;
        document.getElementById('notesSection').style.display = 'block';
    }
    
    // Show panel
    document.getElementById('codePanel').style.display = 'block';
    document.getElementById('executionPanel').style.display = 'none';
    document.getElementById('errorPanel').style.display = 'none';
}

function explainCode() {
    if (!currentCode) return;
    
    // TODO: Call Python backend to explain code
    addMessage(`Explanation of "${currentTitle}":\n\nThis code ${currentNotes}`, 'assistant');
}

function copyCode() {
    if (!currentCode) return;
    navigator.clipboard.writeText(currentCode);
    
    const copyBtn = document.getElementById('copyBtn');
    const originalText = copyBtn.textContent;
    copyBtn.textContent = '✓ Copied!';
    setTimeout(() => {
        copyBtn.textContent = originalText;
    }, 2000);
}

function applyCode() {
    if (!currentCode) return;
    
    isExecuting = true;
    executeCode(currentCode);
}

function rejectCode() {
    document.getElementById('codePanel').style.display = 'none';
    addMessage("Code rejected. What would you like to try instead?", 'system');
    currentCode = null;
}

function executeCode(code) {
    // TODO: Call Python backend to execute code
    const executionPanel = document.getElementById('executionPanel');
    const executionStatus = document.getElementById('executionStatus');
    
    executionPanel.style.display = 'block';
    document.getElementById('codePanel').style.display = 'none';
    executionStatus.innerHTML = '<p>Executing code in Fusion 360...</p>';
    
    // Simulate execution
    setTimeout(() => {
        // Success simulation
        executionStatus.innerHTML = '<p style="color: green;">✓ Code executed successfully!</p>';
        document.getElementById('executionOutput').innerHTML = 
            '<p>Created 3 user parameters: Width, Height, Thickness</p>' +
            '<p>Sketch "Bracket Profile" created on XY plane</p>' +
            '<p>Feature "BracketExtrude" created</p>';
        
        // For error simulation, uncomment:
        // showErrorPanel({
        //     error: "AttributeError: 'NoneType' object has no attribute 'sketchCurves'",
        //     stack_trace: "Traceback (most recent call last):\n  File ...",
        //     suggestions: ["Check that root component is not null", "Ensure design workspace is active"]
        // });
    }, 1500);
}

function undoExecution() {
    // TODO: Call Fusion API to undo
    addMessage("Last operation undone.", 'system');
    closeExecution();
}

function closeExecution() {
    document.getElementById('executionPanel').style.display = 'none';
    isExecuting = false;
}

function showErrorPanel(error) {
    document.getElementById('codePanel').style.display = 'none';
    document.getElementById('executionPanel').style.display = 'none';
    
    const errorPanel = document.getElementById('errorPanel');
    document.getElementById('errorMessage').textContent = error.error;
    
    if (error.stack_trace) {
        document.getElementById('stackTrace').textContent = error.stack_trace;
        document.getElementById('stackTraceDetails').style.display = 'block';
    }
    
    if (error.suggestions && error.suggestions.length > 0) {
        const suggestionsDiv = document.getElementById('errorSuggestions');
        suggestionsDiv.innerHTML = '<strong>Suggestions:</strong><ul>' + 
            error.suggestions.map(s => `<li>${escapeHtml(s)}</li>`).join('') + 
            '</ul>';
    }
    
    errorPanel.style.display = 'block';
}

function fixAndRetry() {
    // TODO: Call LLM to generate fix
    addMessage("Attempting to fix the code...", 'system');
    // Simulate fix
    setTimeout(() => {
        const fixedResponse = {
            title: "Fixed: Parametric Bracket",
            plan: currentPlan,
            code: currentCode.replace('root.sketchCurves', 'sketch.sketchCurves'),
            notes: "Added null check before accessing design"
        };
        showCodePanel(fixedResponse);
    }, 1500);
}

// Settings
function openSettings() {
    document.getElementById('settingsModal').style.display = 'flex';
}

function closeSettings() {
    document.getElementById('settingsModal').style.display = 'none';
}

function saveSettings() {
    const settings = {
        model: document.getElementById('modelSelect').value,
        projectRoot: document.getElementById('projectRoot').value,
        autoRun: document.getElementById('autoRunCheckbox').checked,
    };
    localStorage.setItem('copilotSettings', JSON.stringify(settings));
    closeSettings();
    addMessage("Settings saved.", 'system');
}

function loadSettings() {
    const saved = localStorage.getItem('copilotSettings');
    if (saved) {
        const settings = JSON.parse(saved);
        document.getElementById('modelSelect').value = settings.model || 'openai';
        document.getElementById('projectRoot').value = settings.projectRoot || '';
        document.getElementById('autoRunCheckbox').checked = settings.autoRun || false;
    }
}

// Context
function updateContext() {
    // TODO: Get context from Python backend
    const contextInfo = document.getElementById('contextInfo');
    contextInfo.innerHTML = `
        <p><strong>Document:</strong> Unsaved Design</p>
        <p><strong>Units:</strong> mm</p>
        <p><strong>Selection:</strong> 0 entities</p>
        <p><strong>Parameters:</strong> 0 defined</p>
    `;
}

// Help
function showHelp() {
    const helpText = `
Copilot Assistant Help

1. Write a request in natural language:
   - "Create a parametric bracket"
   - "Add M6 threaded holes"
   - "Generate a 3-axis CAM setup"

2. Review the generated code:
   - Check the plan and notes
   - Use "Explain" to understand it better

3. Apply or modify:
   - Click "Apply" to run the code
   - Click "Reject" to try a different approach
   - Edit the code and retry if needed

4. Iterate:
   - The code is undoable via Fusion undo
   - Keep refining until you get the design you want

Tips:
- Include specific dimensions and parameters
- Reference existing features by name
- Use the selection to target specific geometry
- Check the error messages for quick fixes
    `;
    addMessage(helpText, 'assistant');
}

// Utilities
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Auto-expand textarea
document.getElementById('userInput').addEventListener('input', (e) => {
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 80) + 'px';
});
