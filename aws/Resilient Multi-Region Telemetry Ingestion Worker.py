"""
Imagine you are building a component for a resilient telemetry collection service (like your FTC Solar or Arlo pipeline). You are given a stream of JSON payloads containing IoT edge telemetry. Each payload has a device_id, a timestamp, a metric_name, and a numeric_value.

Write a Python class or module that:

Validates incoming JSON payloads against required fields and correct data types.

Processes valid metrics by calculating a moving window/batch average per device.

Implements an idempotent write mechanism that simulates publishing processed data to a downstream storage endpoint.

Handles poison/malformed messages cleanly using a Dead Letter Queue (DLQ) pattern without crashing the application process.
"""
import logging
import json
import time
from typing import Dict, List, Any, Tuple
from collections import defaultdict

# Configure structured logging for observability (Insist on Highest Standards)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TelemetryProcessor")


class InvalidPayloadException(Exception):
    """Custom exception for schema validation failures."""
    pass


class ResilientTelemetryProcessor:
    def __init__(self, batch_threshold: int = 5):
        """
        Initialize the processor with in-memory batch buffers and deduplication tracking.
        """
        self.batch_threshold = batch_threshold
        # Buffer structure: {device_id: {metric_name: [list of float values]}}
        self.buffer: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
        # Deduplication cache for idempotency: set of message hashes or (device_id, timestamp) tuples
        self.processed_message_ids: set = set()
        # Simulated Dead Letter Queue (DLQ)
        self.dlq: List[Tuple[Dict[str, Any], str]] = []

    def _validate_schema(self, payload: Dict[str, Any]) -> None:
        """
        Validates schema structure and field data types.
        """
        required_fields = {
            "device_id": str,
            "timestamp": (int, float),
            "metric_name": str,
            "numeric_value": (int, float)
        }

        for field, expected_type in required_fields.items():
            if field not in payload:
                raise InvalidPayloadException(f"Missing required field: '{field}'")
            if not isinstance(payload[field], expected_type):
                raise InvalidPayloadException(
                    f"Field '{field}' has invalid type '{type(payload[field]).__name__}'. Expected '{expected_type}'."
                )

    def _generate_dedup_key(self, payload: Dict[str, Any]) -> str:
        """
        Generates an idempotent deduplication key based on message content.
        """
        return f"{payload['device_id']}#{payload['metric_name']}#{payload['timestamp']}"

    def process_incoming_message(self, raw_message: str) -> bool:
        """
        Ingests, validates, and buffers incoming JSON message strings.
        Returns True if processed successfully, False if sent to DLQ.
        """
        try:
            # Step 1: Parse JSON
            payload = json.loads(raw_message)

            # Step 2: Validate Schema
            self._validate_schema(payload)

            # Step 3: Check Idempotency (Deduplication)
            dedup_key = self._generate_dedup_key(payload)
            if dedup_key in self.processed_message_ids:
                logger.warning(f"Duplicate message detected for key: {dedup_key}. Skipping processing.")
                return True  # Acknowledged as duplicate without re-processing

            # Step 4: Add to Buffer
            device_id = payload["device_id"]
            metric_name = payload["metric_name"]
            value = float(payload["numeric_value"])

            self.buffer[device_id][metric_name].append(value)
            self.processed_message_ids.add(dedup_key)
            logger.info(
                f"Buffered metric '{metric_name}' for device '{device_id}'. Current count: {len(self.buffer[device_id][metric_name])}")

            # Step 5: Trigger Flush if threshold met
            if len(self.buffer[device_id][metric_name]) >= self.batch_threshold:
                self.flush_device_metrics(device_id, metric_name)

            return True

        except (json.JSONDecodeError, InvalidPayloadException) as error:
            logger.error(f"Poison message encountered. Routing to DLQ. Error: {str(error)}")
            self._send_to_dlq(raw_message, str(error))
            return False
        except Exception as unhandled_error:
            logger.critical(f"Unhandled exception during message processing: {str(unhandled_error)}")
            self._send_to_dlq(raw_message, f"Unhandled: {str(unhandled_error)}")
            return False

    def flush_device_metrics(self, device_id: str, metric_name: str) -> Dict[str, Any]:
        """
        Computes aggregate metrics and writes downstream.
        """
        values = self.buffer[device_id][metric_name]
        if not values:
            return {}

        avg_value = sum(values) / len(values)
        summary = {
            "device_id": device_id,
            "metric_name": metric_name,
            "sample_size": len(values),
            "aggregate_avg": round(avg_value, 4),
            "processed_at": time.time()
        }

        # Simulate downstream persistent write (e.g., DynamoDB / Timestream)
        self._write_to_downstream_store(summary)

        # Clear local buffer for this specific metric
        self.buffer[device_id][metric_name] = []
        return summary

    def _write_to_downstream_store(self, summary_payload: Dict[str, Any]) -> None:
        """
        Simulated write operation to persistent storage.
        """
        logger.info(f"[DOWNSTREAM WRITE SUCCESS] Published aggregate: {json.dumps(summary_payload)}")

    def _send_to_dlq(self, raw_message: str, reason: str) -> None:
        """
        Routes unprocessable/poison payloads to Dead Letter Queue for auditing.
        """
        dlq_entry = {"raw_payload": raw_message, "failure_reason": reason, "timestamp": time.time()}
        self.dlq.append((dlq_entry, reason))
        logger.info(f"[DLQ ENQUEUE] Message isolated. Total DLQ Depth: {len(self.dlq)}")


# ==========================================
# VERIFICATION & TEST HARNESS
# ==========================================
if __name__ == "__main__":
    processor = ResilientTelemetryProcessor(batch_threshold=3)

    # 1. Valid Stream Inputs
    valid_msg_1 = json.dumps(
        {"device_id": "iMX8-EDGE-01", "timestamp": 1700000001, "metric_name": "temp_celsius", "numeric_value": 42.5})
    valid_msg_2 = json.dumps(
        {"device_id": "iMX8-EDGE-01", "timestamp": 1700000002, "metric_name": "temp_celsius", "numeric_value": 45.0})
    valid_msg_3 = json.dumps(
        {"device_id": "iMX8-EDGE-01", "timestamp": 1700000003, "metric_name": "temp_celsius", "numeric_value": 43.0})

    # 2. Duplicate Message (Idempotency Check)
    duplicate_msg = valid_msg_1

    # 3. Malformed / Poison Inputs (DLQ Checks)
    poison_msg_bad_type = json.dumps(
        {"device_id": "iMX8-EDGE-01", "timestamp": "INVALID_TIMESTAMP", "metric_name": "temp_celsius",
         "numeric_value": 40.0})
    poison_msg_missing_field = json.dumps({"device_id": "iMX8-EDGE-02", "metric_name": "vibration"})

    print("\n--- INGESTING VALID MESSAGES ---")
    processor.process_incoming_message(valid_msg_1)
    processor.process_incoming_message(valid_msg_2)
    processor.process_incoming_message(valid_msg_3)  # Triggers batch threshold flush!

    print("\n--- TESTING IDEMPOTENCY ---")
    processor.process_incoming_message(duplicate_msg)

    print("\n--- TESTING POISON MESSAGES (DLQ ROUTING) ---")
    processor.process_incoming_message(poison_msg_bad_type)
    processor.process_incoming_message(poison_msg_missing_field)

    print(f"\nFinal State Verification:")
    print(f"DLQ Depth: {len(processor.dlq)} (Expected: 2)")