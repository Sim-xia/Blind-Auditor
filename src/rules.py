"""
Rules Configuration Loader for Blind Auditor
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional


class RulesLoader:
	"""Loads and manages audit rules from rules.json."""
	
	def __init__(self, rules_path: str = "rules.json"):
		self.rules_path = Path(rules_path)
		self.rules_data: Dict[str, Any] = {}
		
	def load(self) -> Dict[str, Any]:
		"""Load rules from the JSON file."""
		if not self.rules_path.exists():
			# Return default empty structure
			return {
				"project_name": "Unknown",
				"strict_mode": True,
				"max_retries": 3,
				"rules": []
			}
		
		with open(self.rules_path, 'r', encoding='utf-8') as f:
			self.rules_data = json.load(f)
		
		return self.rules_data
	
	def save(self) -> None:
		"""Save current rules data back to JSON file."""
		with open(self.rules_path, 'w', encoding='utf-8') as f:
			json.dump(self.rules_data, f, indent=2, ensure_ascii=False)
	
	def get_rules(self) -> List[Dict[str, Any]]:
		"""Get the list of rules."""
		return self.rules_data.get("rules", [])
	
	def get_max_retries(self) -> int:
		"""Get the maximum retry count."""
		return self.rules_data.get("max_retries", 3)
	
	def add_rule(self, rule_id: str, severity: str, description: str, weight: int) -> Dict[str, str]:
		"""
		Add a new rule to the rules list.
		
		Args:
			rule_id: Unique identifier for the rule (e.g., "SEC-001")
			severity: Rule severity level ("CRITICAL", "WARNING", "PREFERENCE")
			description: Description of the rule
			weight: Point deduction weight for violations
			
		Returns:
			Dict with status and message
		"""
		# Validate severity
		valid_severities = ["CRITICAL", "WARNING", "PREFERENCE"]
		if severity not in valid_severities:
			return {
				"status": "error",
				"message": f"Invalid severity '{severity}'. Must be one of: {', '.join(valid_severities)}"
			}
		
		# Check for duplicate rule_id
		existing_rules = self.get_rules()
		if any(rule.get("id") == rule_id for rule in existing_rules):
			return {
				"status": "error",
				"message": f"Rule with ID '{rule_id}' already exists. Use update_rule to modify it."
			}
		
		# Validate weight
		if not isinstance(weight, int) or weight < 0 or weight > 100:
			return {
				"status": "error",
				"message": f"Weight must be an integer between 0 and 100, got {weight}"
			}
		
		# Add the new rule
		new_rule = {
			"id": rule_id,
			"severity": severity,
			"description": description,
			"weight": weight
		}
		
		self.rules_data["rules"].append(new_rule)
		self.save()
		
		return {
			"status": "success",
			"message": f"Rule '{rule_id}' added successfully."
		}
	
	def remove_rule(self, rule_id: str) -> Dict[str, str]:
		"""
		Remove a rule by its ID.
		
		Args:
			rule_id: The ID of the rule to remove
			
		Returns:
			Dict with status and message
		"""
		existing_rules = self.get_rules()
		original_count = len(existing_rules)
		
		# Filter out the rule with matching ID
		self.rules_data["rules"] = [
			rule for rule in existing_rules 
			if rule.get("id") != rule_id
		]
		
		if len(self.rules_data["rules"]) == original_count:
			return {
				"status": "error",
				"message": f"Rule with ID '{rule_id}' not found."
			}
		
		self.save()
		return {
			"status": "success",
			"message": f"Rule '{rule_id}' removed successfully."
		}
	
	def update_rule(
		self, 
		rule_id: str, 
		severity: Optional[str] = None, 
		description: Optional[str] = None, 
		weight: Optional[int] = None
	) -> Dict[str, str]:
		"""
		Update an existing rule.
		
		Args:
			rule_id: The ID of the rule to update
			severity: New severity level (optional)
			description: New description (optional)
			weight: New weight (optional)
			
		Returns:
			Dict with status and message
		"""
		existing_rules = self.get_rules()
		rule_found = False
		
		for rule in existing_rules:
			if rule.get("id") == rule_id:
				rule_found = True
				
				# Validate and update severity
				if severity is not None:
					valid_severities = ["CRITICAL", "WARNING", "PREFERENCE"]
					if severity not in valid_severities:
						return {
							"status": "error",
							"message": f"Invalid severity '{severity}'. Must be one of: {', '.join(valid_severities)}"
						}
					rule["severity"] = severity
				
				# Update description
				if description is not None:
					rule["description"] = description
				
				# Validate and update weight
				if weight is not None:
					if not isinstance(weight, int) or weight < 0 or weight > 100:
						return {
							"status": "error",
							"message": f"Weight must be an integer between 0 and 100, got {weight}"
						}
					rule["weight"] = weight
				
				break
		
		if not rule_found:
			return {
				"status": "error",
				"message": f"Rule with ID '{rule_id}' not found."
			}
		
		self.save()
		return {
			"status": "success",
			"message": f"Rule '{rule_id}' updated successfully."
		}
	
	def list_rules(self) -> str:
		"""
		Get a formatted string of all current rules.
		
		Returns:
			Formatted string listing all rules
		"""
		rules = self.get_rules()
		if not rules:
			return "No rules configured."
		
		lines = ["Current Audit Rules:", ""]
		for i, rule in enumerate(rules, 1):
			lines.append(f"{i}. [{rule.get('severity', 'UNKNOWN')}] {rule.get('id', 'NO_ID')}")
			lines.append(f"   Description: {rule.get('description', 'No description')}")
			lines.append(f"   Weight: {rule.get('weight', 0)} points")
			lines.append("")
		
		return "\n".join(lines)
	
	def format_rules_for_prompt(self) -> str:
		"""Format rules as a readable string for prompt injection."""
		rules = self.get_rules()
		if not rules:
			return "No rules configured."
		
		formatted = []
		for rule in rules:
			severity = rule.get("severity", "UNKNOWN")
			description = rule.get("description", "")
			rule_id = rule.get("id", "")
			formatted.append(f"[{severity}] {rule_id}: {description}")
		
		return "\n".join(formatted)
