# 🛡️ Blind Auditor - MCP Server

> **"Code drunk, audit sober."** — *The Philosophy of Blind Auditor*

Blind Auditor is a **mandatory code auditing system** built on the MCP (Model Context Protocol). It uses a unique **"Thinking Isolation"** mechanism to force AI Agents to enter an independent "audit phase" and self-review their code before outputting the final result.

## 🧠 Core Philosophy: Thinking Isolation

Traditional AI coding is often "generate and output," which allows errors and biases to slip through. Blind Auditor introduces a middle layer:

1.  **Intercept**: When the Agent wants to output code, it must first submit it to Blind Auditor.
2.  **Isolate**: Blind Auditor does not return the result immediately. Instead, it injects a **mandatory system instruction**, forcing the Agent to pause its current persona and switch to a "Ruthless Auditor" role.
3.  **Audit**: In this isolated context, the Agent must scan the generated code line by line against the predefined `rules.json`.
4.  **Release**: The code is unlocked and returned to the user only when the audit score meets the threshold (default > 80) and there are no Critical issues.

## 🎯 Key Features

- **🛡️ Zero Trust Architecture**: Default distrust of the Agent's initial draft; it must pass an audit.
- **💰 Zero Extra Cost**: Reuses the host IDE's current session model, requiring no additional API Key.
- **⚖️ Bias Removal**: Forces a perspective switch via Prompt injection to break generation inertia.
- **📏 Strict Compliance**: Hard-codes team code standards (`rules.json`) into the generation process, which is more effective than simple Prompts.
- **🔄 Auto-Fix Loop**: Automatically triggers a "fix-resubmit" loop upon audit failure until compliance is met or the maximum retry count is reached.

---

## 🚀 Quick Start

### 1. Prerequisites

This project requires Python 3.8 or higher.

```bash
# Enter project directory
cd blind-auditor

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Audit Rules (`rules.json`)

Create or edit `rules.json` in the project root. This is the auditor's "Rulebook".

```json
{
  "project_name": "MyCoreProject",
  "strict_mode": true,
  "max_retries": 3,
  "rules": [
    {
      "id": "SEC-001",
      "severity": "CRITICAL",
      "description": "Strictly prohibit hardcoding any API Keys, passwords, or sensitive Tokens.",
      "weight": 50
    },
    {
      "id": "PERF-001",
      "severity": "WARNING",
      "description": "Avoid database queries or IO operations inside loops.",
      "weight": 15
    },
    {
      "id": "STYLE-001",
      "severity": "PREFERENCE",
      "description": "Use snake_case for variable names.",
      "weight": 5
    }
  ]
}
```

**Configuration Fields**:
- `severity`:
    - `CRITICAL`: Fatal error. If found, the audit fails immediately. Usually carries a high penalty.
    - `WARNING`: Warning. Moderate penalty; accumulation can lead to failure.
    - `PREFERENCE`: Style preference. Low penalty.
- `weight`: The penalty points deducted when this rule is violated (Total score: 100).

### 3. Configure IDE (Antigravity / Cursor / Windsurf)

#### Step A: Add System Prompt (Critical)

To ensure the Agent knows it must use this tool, add the following instruction to your `.cursorrules` or IDE System Prompt settings:

```markdown
# Blind Auditor Protocol
**CRITICAL INSTRUCTION**:
You are integrated with the **Blind Auditor MCP**.
Whenever you generate code for a user request, you **MUST NOT** output the code block directly to the user.

**Execution Protocol**:
1.  **Draft**: Generate the code internally in your thought process.
2.  **Submit**: Call the `submit_draft` tool with your code and language.
3.  **Obey**: The tool will return a strict "Audit Instruction". You MUST follow it exactly to audit your own code.
4.  **Finalize**: Only when the tool returns "✅ AUDIT PASSED" can you display the final code to the user.

**Prohibited**:
- Do NOT output code blocks before passing the audit.
- Do NOT skip the audit step for "simple" changes.
```

#### Step B: Configure MCP Server

Add the following to your MCP client configuration file (e.g., `claude_desktop_config.json` or IDE settings):

```json
{
  "mcpServers": {
    "blind-auditor": {
      "command": "python",
      "args": ["-m", "src.main"],
      "cwd": "/absolute/path/to/blind-auditor"
    }
  }
}
```

---

## 🔧 Tool Details

### 1. `submit_draft`
Submit a code draft.
- **Input**: `code` (content), `language` (programming language)
- **Behavior**: Locks the session and returns mandatory audit instructions.

### 2. `submit_audit_result`
Submit your audit conclusion.
- **Input**:
    - `passed` (bool): Whether you believe it passed.
    - `issues` (list): List of issues found.
    - `score` (int): Score from 0-100.
- **Behavior**:
    - If `score < 80`, forces `passed=False`.
    - If passed, unlocks the code.
    - If failed, increments retry count and requires the Agent to fix and resubmit.

### 3. `reset_session`
Resets the state and clears the retry count.

---

## 🔁 Workflow Diagram

```mermaid
graph TD
    User["User Request"] --> Agent
    Agent["Agent Generates Draft"] -->|1. submit_draft| MCP
    MCP -->|2. Inject Audit Instructions| Agent
    
    subgraph Isolation ["Thinking Isolation"]
        Agent -->|3. Self-Review| Agent
        Agent -->|4. submit_audit_result| MCP
    end
    
    MCP -->|5. Verdict| Decision{"Passed?"}
    
    Decision -->|No - Issues Found| Retry["Retry Count +1"]
    Retry -->|Limit Not Reached| Fix["Agent Fixes Code"]
    Fix -->|Resubmit| Agent
    
    Decision -->|Yes - Score >= 80| Final["✅ Output Final Code"]
    
    Retry -->|Limit Reached| Force["⚠️ Force Output - With Warning"]
```

## ❓ Troubleshooting

**Q: The Agent always outputs code directly without calling tools.**
A: Check if the System Prompt is configured correctly. You must explicitly tell the Agent "Do NOT output code directly". You can also manually remind it in the chat: "Please audit via Blind Auditor first".

**Q: Why does it fail even if I give the code 100 points?**
A: Check if any `CRITICAL` rules in `rules.json` were triggered. Current logic mainly relies on the `score` passed by the Agent, but if `passed` is `True` while `score < 80`, the system will force a rejection.

**Q: Which programming languages are supported?**
A: Theoretically, all languages are supported. Blind Auditor itself does not parse code syntax but relies on the Agent's understanding to match descriptions in `rules.json`.

---

## 🛠️ Development Guide

```bash
# Run server
python -m src.main

# Debug mode (output to stderr)
# View print statements in src/main.py
```

## 📄 License

MIT License
