"""
As part of a Developer Transformation initiative,
your goal is to prevent breaking API contract changes from entering staging environments
while keeping developer friction near zero.

Write a Python module that takes a proposed API schema definition (e.g., OpenAPI endpoint payload),
validates it against an organizational safety policy
(e.g., ensuring mandatory metadata headers, strict payload size constraints,
and non-breaking data type changes), and outputs structured diagnostic feedback for CI/CD pipelines.
"""
import json
import logging
from typing import Dict, List, Any, Tuple

# Configure structured JSON-compatible logging for CI/CD pipeline integration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DevXPolicyEnforcer")


class PolicyViolationException(Exception):
    """Custom exception for Developer Transformation gate failures."""
    pass


class DeveloperPolicyGatekeeper:
    def __init__(self, mandatory_headers: List[str] = None, max_payload_bytes: int = 1048576):
        """
        Initialize policy controls. Default max payload: 1MB.
        """
        self.mandatory_headers = mandatory_headers or ["X-Correlation-ID", "X-Client-ID"]
        self.max_payload_bytes = max_payload_bytes

    def evaluate_contract(self, current_schema: Dict[str, Any], proposed_schema: Dict[str, Any]) \
            -> Tuple[bool, List[str]]:
        """
        Evaluates a proposed API schema against safety rules and backward compatibility.
        Returns: (is_compliant: bool, violations: List[str])
        """
        violations = []

        # Rule 1: Check mandatory enterprise headers
        headers = proposed_schema.get("headers", {})
        for required_header in self.mandatory_headers:
            if required_header not in headers:
                violations.append(f"MISSING_HEADER: Mandatory header '{required_header}' is missing.")

        # Rule 2: Enforce payload size policies (Prevent Monolithic/Bloated endpoints)
        payload_body = proposed_schema.get("body_schema", {})
        serialized_size = len(json.dumps(payload_body).encode('utf-8'))
        if serialized_size > self.max_payload_bytes:
            violations.append(
                f"PAYLOAD_TOO_LARGE: Schema body size ({serialized_size} bytes) exceeds limit ({self.max_payload_bytes} bytes)."
            )

        # Rule 3: Backward Compatibility Check (Prevent breaking removal of fields)
        current_fields = current_schema.get("body_schema", {}).get("properties", {})
        proposed_fields = payload_body.get("properties", {})

        for field_name, field_meta in current_fields.items():
            if field_name not in proposed_fields:
                violations.append(f"BREAKING_CHANGE: Field '{field_name}' was removed from the request schema.")
            else:
                # Check for type mutation (e.g., string -> integer)
                old_type = field_meta.get("type")
                new_type = proposed_fields[field_name].get("type")
                if old_type != new_type:
                    violations.append(
                        f"TYPE_MUTATION: Field '{field_name}' type changed from '{old_type}' to '{new_type}'."
                    )

        is_compliant = len(violations) == 0
        return is_compliant, violations


# ==========================================
# CI/CD TEST HARNESS
# ==========================================
if __name__ == "__main__":
    gatekeeper = DeveloperPolicyGatekeeper(max_payload_bytes=500)

    # 1. Existing Production Schema v1
    v1_schema = {
        "headers": {"X-Correlation-ID": "string", "X-Client-ID": "string"},
        "body_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"},
                "amount": {"type": "number"}
            }
        }
    }

    # 2. Proposed v2 Schema with Breaking Changes & Missing Header
    v2_breaking_schema = {
        "headers": {"X-Correlation-ID": "string"},  # Missing X-Client-ID
        "body_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "integer"},  # Type Mutation
                # "amount" field deleted (Breaking Removal)
                "currency": {"type": "string"}
            }
        }
    }

    logger.info("Evaluating proposed schema against CI/CD DevX policy gate...")
    passed, issues = gatekeeper.evaluate_contract(v1_schema, v2_breaking_schema)

    if not passed:
        logger.error(f"[GATE REJECTED] Found {len(issues)} policy violations:")
        for issue in issues:
            print(f"  ❌ {issue}")
    else:
        logger.info("✅ [GATE PASSED] Schema is backward-compatible and compliant.")