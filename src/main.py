"""
Minimal debug version of Blind Auditor MCP Server
"""
import sys
from pathlib import Path

# Debug output to stderr
print("DEBUG: Starting main_debug.py", file=sys.stderr)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

print("DEBUG: Importing FastMCP", file=sys.stderr)
from mcp.server.fastmcp import FastMCP

print("DEBUG: Importing state and rules", file=sys.stderr)
from state import SessionState
from rules import RulesLoader

# Initialize the MCP server
print("DEBUG: Creating FastMCP instance", file=sys.stderr)
mcp = FastMCP("Blind Auditor")

# Initialize global state
print("DEBUG: Initializing session state", file=sys.stderr)
session = SessionState()

# Initialize rules loader with proper path
print("DEBUG: Loading rules", file=sys.stderr)
rules_path = Path(__file__).parent.parent / "rules.json"
rules_loader = RulesLoader(str(rules_path))

# Load rules at module level (before defining tools)
try:
    rules_loader.load()
    print(f"DEBUG: Rules loaded successfully from {rules_path}", file=sys.stderr)
except Exception as e:
    print(f"DEBUG: Failed to load rules.json: {e}", file=sys.stderr)


def _generate_detailed_report(audit_history: list, code: str, language: str, max_retries: int) -> str:
    """Generate detailed audit report when retry limit is reached."""
    
    # Calculate statistics
    total_attempts = len(audit_history)
    if total_attempts == 0:
        avg_score = 0.0
    else:
        avg_score = sum([h["score"] for h in audit_history]) / float(total_attempts)
    
    # Collect all issues by category
    critical_issues = []
    warning_issues = []
    preference_issues = []
    other_issues = []
    
    for history_entry in audit_history:
        for issue in history_entry["issues"]:
            issue_upper = issue.upper()
            if "CRITICAL" in issue_upper:
                critical_issues.append(issue)
            elif "WARNING" in issue_upper:
                warning_issues.append(issue)
            elif "PREFERENCE" in issue_upper:
                preference_issues.append(issue)
            else:
                other_issues.append(issue)
    
    # Build report
    report_parts = [
        "🚨 **AUDIT LIMIT EXCEEDED - CODE REJECTED**",
        "",
        f"You have reached the maximum retry limit ({max_retries} attempts).",
        "**The code has NOT been approved and cannot be modified further.**",
        "",
        "## 📊 Audit Summary",
        f"- **Total Attempts**: {total_attempts}",
        f"- **Average Score**: {avg_score:.1f}/100",
        f"- **Status**: REJECTED",
        "",
        "## 📝 Detailed Audit History",
    ]
    
    # Add each audit attempt
    for i, history_entry in enumerate(audit_history, 1):
        report_parts.append(f"\n### Attempt {i}")
        report_parts.append(f"- **Score**: {history_entry['score']}/100")
        report_parts.append(f"- **Result**: {'PASSED' if history_entry['passed'] else 'FAILED'}")
        if history_entry["issues"]:
            report_parts.append("- **Issues**:")
            for issue in history_entry["issues"]:
                report_parts.append(f"  - {issue}")
    
    # Add issue categorization
    report_parts.extend([
        "",
        "## 🔍 Issue Categorization",
    ])
    
    if critical_issues:
        report_parts.append(f"\n### ⛔ CRITICAL Issues ({len(critical_issues)})")
        for issue in critical_issues:
            report_parts.append(f"- {issue}")
    
    if warning_issues:
        report_parts.append(f"\n### ⚠️ WARNING Issues ({len(warning_issues)})")
        for issue in warning_issues:
            report_parts.append(f"- {issue}")
    
    if preference_issues:
        report_parts.append(f"\n### 💡 PREFERENCE Issues ({len(preference_issues)})")
        for issue in preference_issues:
            report_parts.append(f"- {issue}")
    
    if other_issues:
        report_parts.append(f"\n### 📌 Other Issues ({len(other_issues)})")
        for issue in other_issues:
            report_parts.append(f"- {issue}")
    
    # Add recommendations
    report_parts.extend([
        "",
        "## 💡 Recommendations",
        "1. Review all CRITICAL issues first - these cause immediate failures",
        "2. Address WARNING issues to improve code quality",
        "3. Consider PREFERENCE issues for best practices",
        "4. Reset the session with `reset_session()` to start a new audit",
        "",
        "## 📄 Submitted Code",
        f"```{language}",
        code,
        "```",
    ])
    
    return "\n".join(report_parts)


@mcp.tool()
def submit_draft(code: str, language: str = "python") -> str:
    """Submit a code draft for audit."""
    print(f"DEBUG: submit_draft called with code length={len(code)}", file=sys.stderr)
    session.current_code = code
    session.status = "AUDITING"
    
    max_retries = rules_loader.get_max_retries()
    
    # CHANGED: Generate detailed report instead of auto-approving
    if session.retry_count >= max_retries:
        session.status = "LIMIT_EXCEEDED"
        return _generate_detailed_report(session.audit_history, code, language, max_retries)
    
    rules_formatted = rules_loader.format_rules_for_prompt()
    
    return f"""🛑 **[SYSTEM INTERVENTION: CONTEXT ISOLATION MODE]**

**STOP GENERATING**. Do not output the code yet.

You are now entering the **Blind Audit Phase**.

**Rulebook:**
{rules_formatted}

**Candidate Code:**
```{language}
{code}
```

**Instructions:**
1. **Analyze Step-by-Step (CoT)**:
   - First, list all violations found.
   - Classify each violation by severity (CRITICAL, WARNING, PREFERENCE).
   - Calculate the deduction for each violation.

2. **Scoring Rubric (Strict Enforcement)**:
   - **Start Score**: 100
   - **CRITICAL Violation**: -50 points each (Immediate FAIL)
   - **WARNING Violation**: -15 points each
   - **PREFERENCE Violation**: -5 points each
   - **Maximum Deduction**: 100 points (Minimum Score: 0)

3. **Final Decision**:
   - Call `submit_audit_result` with your findings.
   - **CRITICAL**: If score is < 80, you MUST set passed=False.
   - The system will enforce `score >= 80` to pass.
"""


@mcp.tool()
def submit_audit_result(passed: bool, issues: list[str], score: int = 0) -> str:
    """Submit the audit result."""
    print(f"DEBUG: submit_audit_result called: passed={passed}, score={score}", file=sys.stderr)
    
    # Hardcoded score validation
    MIN_SCORE = 80
    if passed and score < MIN_SCORE:
        passed = False
        issues.append(f"[SYSTEM ENFORCEMENT] Score ({score}) is below minimum threshold ({MIN_SCORE}). You cannot pass code with such a low score.")
    
    session.audit_history.append({
        "passed": passed,
        "issues": issues,
        "score": score,
        "retry_count": session.retry_count
    })
    
    if passed:
        session.status = "APPROVED"
        return f"✅ AUDIT PASSED (Score: {score}/100)\n\n```\n{session.current_code}\n```"
    else:
        session.retry_count += 1
        session.status = "IDLE"
        issues_formatted = "\n".join([f"- {issue}" for issue in issues])
        return f"❌ AUDIT FAILED (Score: {score}/100)\n\n**Issues:**\n{issues_formatted}\n\nRetry count: {session.retry_count}/{rules_loader.get_max_retries()}"



@mcp.tool()
def reset_session() -> str:
	"""Reset the current audit session."""
	print("DEBUG: reset_session called", file=sys.stderr)
	session.reset()
	return "✅ Session reset successfully."


@mcp.tool()
def update_rules(
	action: str,
	rule_id: str = "",
	severity: str = "",
	description: str = "",
	weight: int = 0
) -> str:
	"""
	Update audit rules configuration.
	
	Args:
		action: Operation to perform - "add", "remove", "update", or "list"
		rule_id: Rule identifier (required for add/remove/update)
		severity: Rule severity level - "CRITICAL", "WARNING", or "PREFERENCE" (for add/update)
		description: Rule description (for add/update)
		weight: Point deduction weight 0-100 (for add/update)
	
	Returns:
		Status message with operation result
	
	Examples:
		# List all rules
		update_rules(action="list")
		
		# Add a new rule
		update_rules(
			action="add",
			rule_id="SEC-001",
			severity="CRITICAL",
			description="No hardcoded API keys",
			weight=50
		)
		
		# Remove a rule
		update_rules(action="remove", rule_id="SEC-001")
		
		# Update a rule
		update_rules(
			action="update",
			rule_id="SEC-001",
			description="Updated description"
		)
	"""
	print(f"DEBUG: update_rules called with action={action}, rule_id={rule_id}", file=sys.stderr)
	
	# Reload rules to get latest state
	rules_loader.load()
	
	# Handle list action
	if action == "list":
		return rules_loader.list_rules()
	
	# Validate rule_id for non-list actions
	if not rule_id:
		return "❌ Error: rule_id is required for add/remove/update actions."
	
	# Handle add action
	if action == "add":
		if not severity or not description:
			return "❌ Error: severity and description are required for adding a rule."
		
		result = rules_loader.add_rule(rule_id, severity, description, weight)
		
		if result["status"] == "success":
			return f"✅ {result['message']}\n\n{rules_loader.list_rules()}"
		else:
			return f"❌ {result['message']}"
	
	# Handle remove action
	elif action == "remove":
		result = rules_loader.remove_rule(rule_id)
		
		if result["status"] == "success":
			return f"✅ {result['message']}\n\n{rules_loader.list_rules()}"
		else:
			return f"❌ {result['message']}"
	
	# Handle update action
	elif action == "update":
		# Only pass non-empty values
		update_kwargs = {}
		if severity:
			update_kwargs["severity"] = severity
		if description:
			update_kwargs["description"] = description
		if weight > 0:
			update_kwargs["weight"] = weight
		
		if not update_kwargs:
			return "❌ Error: At least one field (severity, description, or weight) must be provided for update."
		
		result = rules_loader.update_rule(rule_id, **update_kwargs)
		
		if result["status"] == "success":
			return f"✅ {result['message']}\n\n{rules_loader.list_rules()}"
		else:
			return f"❌ {result['message']}"
	
	else:
		return f"❌ Error: Invalid action '{action}'. Must be one of: add, remove, update, list"


if __name__ == "__main__":
    print("DEBUG: About to call mcp.run()", file=sys.stderr)
    sys.stderr.flush()
    mcp.run()
    print("DEBUG: mcp.run() completed (this shouldn't print)", file=sys.stderr)
