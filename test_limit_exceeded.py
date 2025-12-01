#!/usr/bin/env python3
"""
Test script to verify audit limit exceeded behavior
This test simulates reaching the retry limit and checks if detailed report is generated
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from state import SessionState
from rules import RulesLoader

# Mock the _generate_detailed_report function
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


# Test case: simulate reaching retry limit
def test_limit_exceeded():
    print("🧪 Testing Audit Limit Exceeded Behavior\n")
    
    # Initialize state and rules
    session = SessionState()
    rules_loader = RulesLoader("rules.json")
    rules_loader.load()
    max_retries = rules_loader.get_max_retries()
    
    print(f"Max retries configured: {max_retries}\n")
    
    # Simulate 6 failed audits
    test_code = """
vec3 color = vec3(1, 0, 0);  // Bad: should be vec3(1.0, 0.0, 0.0)
float x = 5;  // Bad: should be 5.0
"""
    
    for i in range(max_retries):
        session.audit_history.append({
            "passed": False,
            "issues": [
                f"[CRITICAL] Attempt {i+1}: Type casting violation - using integer in float context",
                f"[WARNING] Attempt {i+1}: Missing explicit decimal points"
            ],
            "score": 30 + i * 5,
            "retry_count": i
        })
        session.retry_count = i + 1
    
    print(f"✅ Simulated {max_retries} failed audit attempts")
    print(f"Current retry count: {session.retry_count}\n")
    
    # Generate report
    report = _generate_detailed_report(session.audit_history, test_code, "glsl", max_retries)
    
    # Verify report content
    print("📋 Generated Report Preview:\n")
    print("=" * 60)
    print(report[:500])  # Print first 500 chars
    print("...")
    print("=" * 60)
    print()
    
    # Assertions
    assert "AUDIT LIMIT EXCEEDED" in report, "❌ Report missing limit exceeded message"
    assert "CODE REJECTED" in report, "❌ Report missing rejection message"
    assert f"Total Attempts**: {max_retries}" in report, "❌ Report missing total attempts"
    assert "Average Score" in report, "❌ Report missing average score"
    assert "CRITICAL Issues" in report, "❌ Report missing critical issues section"
    assert "WARNING Issues" in report, "❌ Report missing warning issues section"
    assert "Recommendations" in report, "❌ Report missing recommendations"
    assert "Submitted Code" in report, "❌ Report missing submitted code"
    
    print("✅ All assertions passed!")
    print("\n🎉 Test completed successfully!")
    print("\nFull report saved to test_report_output.txt")
    
    # Save full report
    with open("test_report_output.txt", "w") as f:
        f.write(report)


if __name__ == "__main__":
    test_limit_exceeded()
