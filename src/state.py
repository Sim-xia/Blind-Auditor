"""
Session State Management for Blind Auditor
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SessionState:
    """
    Manages the state of a single auditing session.
    """
    current_code: Optional[str] = None
    retry_count: int = 0
    audit_history: list = field(default_factory=list)
    status: str = "IDLE"  # IDLE | AUDITING | APPROVED | LIMIT_EXCEEDED
    
    def reset(self):
        """Reset the session state."""
        self.current_code = None
        self.retry_count = 0
        self.audit_history = []
        self.status = "IDLE"
