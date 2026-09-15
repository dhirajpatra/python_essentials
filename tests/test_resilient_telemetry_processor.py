import importlib.util
import json
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "aws" / "Resilient Multi-Region Telemetry Ingestion Worker.py"
SPEC = importlib.util.spec_from_file_location("resilient_telemetry_worker", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
ResilientTelemetryProcessor = MODULE.ResilientTelemetryProcessor


def _valid_payload(device_id="device-1", timestamp=1710000001, metric_name="temp_celsius", numeric_value=42.5):
    return {
        "device_id": device_id,
        "timestamp": timestamp,
        "metric_name": metric_name,
        "numeric_value": numeric_value,
    }


def test_valid_payload_processing_flushes_when_batch_threshold_is_met():
    processor = ResilientTelemetryProcessor(batch_threshold=2)
    payload = _valid_payload()

    first_result = processor.process_incoming_message(json.dumps(payload))
    assert first_result is True

    second_result = processor.process_incoming_message(
        json.dumps({**payload, "timestamp": payload["timestamp"] + 1, "numeric_value": 45.0})
    )

    assert second_result is True
    assert processor.buffer["device-1"]["temp_celsius"] == []
    assert len(processor.processed_message_ids) == 2


def test_malformed_json_or_invalid_schema_is_sent_to_dlq():
    processor = ResilientTelemetryProcessor()

    malformed_json = '{"device_id": "device-1", "timestamp": 1710000001, "numeric_value": 42.5'
    invalid_schema = json.dumps({
        "device_id": "device-1",
        "timestamp": "not-a-number",
        "metric_name": "temp_celsius",
        "numeric_value": 42.5,
    })

    for raw_message in (malformed_json, invalid_schema):
        assert processor.process_incoming_message(raw_message) is False

    assert len(processor.dlq) == 2
    assert processor.dlq[0][0]["raw_payload"] == malformed_json
    assert processor.dlq[1][0]["raw_payload"] == invalid_schema


def test_duplicate_timestamp_is_deduplicated_per_device_metric_pair():
    processor = ResilientTelemetryProcessor(batch_threshold=2)
    payload = _valid_payload()

    first_result = processor.process_incoming_message(json.dumps(payload))
    second_result = processor.process_incoming_message(json.dumps(payload))

    assert first_result is True
    assert second_result is True
    assert len(processor.processed_message_ids) == 1
    assert processor.buffer["device-1"]["temp_celsius"] == [42.5]
