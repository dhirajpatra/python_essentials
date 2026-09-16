"""
pip install spacy
python -m spacy download en_core_web_sm

PIIDetector.PATTERNS["PASSPORT"] = r'\b[A-Z]{1,2}\d{6,9}\b'

Key Features
Feature
Description
Hybrid Detection
Combines regex (structured PII) + spaCy NER (names, orgs, locations)
8+ PII Types
Email, phone, SSN, credit card, IP, date, name, org, location
Deduplication
Resolves overlapping spans by confidence and span length
Redaction
Full redaction or type-specific placeholders
Summary Report
JSON report with counts by type and detection method
Graceful Fallback
Works in regex-only mode if spaCy is unavailable
Compiled Patterns
Regex compiled once at init for repeated-use performance
"""
import json
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple


@dataclass
class PIIEntity:
    """Represents a detected PII entity"""
    text: str
    label: str
    start: int
    end: int
    confidence: float = 1.0
    detection_method: str = "regex"  # 'regex' or 'ner'

    def to_dict(self) -> dict:
        return asdict(self)


class PIIDetector:
    """
    Hybrid PII Detector using Regex patterns and spaCy NER.

    Supports detection of:
    - Email addresses
    - Phone numbers (US/International)
    - SSN (Social Security Numbers)
    - Credit Card numbers
    - IP Addresses
    - Names, Organizations, Locations (via NER)
    """

    # Compiled regex patterns for performance
    PATTERNS = {
        "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "PHONE_US": r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
        "SSN": r'\b\d{3}-\d{2}-\d{4}\b',
        "CREDIT_CARD": r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b',
        "IP_ADDRESS": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        "DATE_ISO": r'\b\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])\b',
    }

    def __init__(self, use_ner: bool = True, spacy_model: str = "en_core_web_sm"):
        """
        Initialize PII Detector.

        Args:
            use_ner: Whether to enable spaCy NER for names/orgs/locations
            spacy_model: spaCy model name (must be installed)
        """
        self.use_ner = use_ner
        self.nlp = None

        if use_ner:
            try:
                import spacy
                self.nlp = spacy.load(spacy_model)
                print(f"[INFO] Loaded spaCy model: {spacy_model}")
            except OSError:
                print(f"[WARN] spaCy model '{spacy_model}' not found.")
                print(f"[WARN] Install with: python -m spacy download {spacy_model}")
                print("[WARN] Falling back to regex-only mode.")
                self.use_ner = False
            except ImportError:
                print("[WARN] spaCy not installed. Install with: pip install spacy")
                self.use_ner = False

        # Compile regex patterns once
        self._compiled_patterns = {
            label: re.compile(pattern)
            for label, pattern in self.PATTERNS.items()
        }

    def detect(self, text: str) -> List[PIIEntity]:
        """
        Detect all PII entities in the given text.

        Args:
            text: Input text to scan

        Returns:
            List of PIIEntity objects sorted by position
        """
        entities: List[PIIEntity] = []

        # 1. Regex-based detection
        entities.extend(self._detect_regex(text))

        # 2. NER-based detection
        if self.use_ner and self.nlp:
            entities.extend(self._detect_ner(text))

        # Sort by start position and deduplicate overlapping spans
        entities.sort(key=lambda e: e.start)
        entities = self._deduplicate(entities)

        return entities

    def _detect_regex(self, text: str) -> List[PIIEntity]:
        """Detect PII using regex patterns"""
        entities = []
        for label, pattern in self._compiled_patterns.items():
            for match in pattern.finditer(text):
                entities.append(PIIEntity(
                    text=match.group(),
                    label=label,
                    start=match.start(),
                    end=match.end(),
                    confidence=0.95,
                    detection_method="regex"
                ))
        return entities

    def _detect_ner(self, text: str) -> List[PIIEntity]:
        """Detect PII using spaCy Named Entity Recognition"""
        entities = []
        doc = self.nlp(text)

        # Map spaCy labels to our PII categories
        ner_mapping = {
            "PERSON": "NAME",
            "ORG": "ORGANIZATION",
            "GPE": "LOCATION",
            "LOC": "LOCATION",
            "FAC": "LOCATION",
        }

        for ent in doc.ents:
            if ent.label_ in ner_mapping:
                entities.append(PIIEntity(
                    text=ent.text,
                    label=ner_mapping[ent.label_],
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=0.85,
                    detection_method="ner"
                ))

        return entities

    @staticmethod
    def _deduplicate(entities: List[PIIEntity]) -> List[PIIEntity]:
        """Remove overlapping entities, keeping higher confidence ones"""
        if not entities:
            return []

        filtered = [entities[0]]
        for current in entities[1:]:
            previous = filtered[-1]
            # Check overlap
            if current.start < previous.end:
                # Keep the one with higher confidence, or longer span
                if current.confidence > previous.confidence:
                    filtered[-1] = current
                elif (current.confidence == previous.confidence and
                      len(current.text) > len(previous.text)):
                    filtered[-1] = current
            else:
                filtered.append(current)

        return filtered

    def redact(self, text: str, replacement: str = "[REDACTED]") -> Tuple[str, List[PIIEntity]]:
        """
        Redact PII from text.

        Args:
            text: Input text
            replacement: String to replace PII with

        Returns:
            Tuple of (redacted_text, list_of_detected_entities)
        """
        entities = self.detect(text)
        if not entities:
            return text, []

        # Build redacted text from right to left to preserve indices
        redacted = text
        for entity in reversed(entities):
            redacted = redacted[:entity.start] + replacement + redacted[entity.end:]

        return redacted, entities

    def summarize(self, text: str) -> Dict:
        """Generate a summary report of PII found in text"""
        entities = self.detect(text)

        summary = {
            "total_pii_found": len(entities),
            "by_type": {},
            "by_method": {"regex": 0, "ner": 0},
            "entities": [e.to_dict() for e in entities]
        }

        for entity in entities:
            summary["by_type"][entity.label] = summary["by_type"].get(entity.label, 0) + 1
            summary["by_method"][entity.detection_method] += 1

        return summary


def main():
    """Demonstrate PII detection capabilities"""

    sample_text = """
    Contact John Smith at john.smith@example.com or call (555) 123-4567.
    His SSN is 123-45-6789 and credit card 4111111111111111.
    He works at Acme Corporation located in New York City.
    Server IP: 192.168.1.100. Date of birth: 1990-05-15.
    Please reach out to Jane Doe at jane.doe@company.org for more info.
    """

    print("=" * 70)
    print("PII DETECTOR DEMONSTRATION")
    print("=" * 70)

    # Initialize detector
    detector = PIIDetector(use_ner=True)

    # 1. Detect PII
    print("\n📋 DETECTED PII:")
    print("-" * 70)
    entities = detector.detect(sample_text)
    for entity in entities:
        print(f"  [{entity.label:<15}] '{entity.text}' "
              f"(pos: {entity.start}-{entity.end}, "
              f"conf: {entity.confidence:.2f}, "
              f"method: {entity.detection_method})")

    # 2. Summary report
    print("\n📊 SUMMARY REPORT:")
    print("-" * 70)
    summary = detector.summarize(sample_text)
    print(json.dumps(summary, indent=2))

    # 3. Redaction
    print("\n🔒 REDACTED TEXT:")
    print("-" * 70)
    redacted_text, _ = detector.redact(sample_text)
    print(redacted_text)

    # 4. Custom redaction placeholder per type
    print("\n🔒 TYPE-SPECIFIC REDACTION:")
    print("-" * 70)
    custom_redacted = sample_text
    entities = detector.detect(sample_text)
    type_placeholders = {
        "EMAIL": "[EMAIL]",
        "PHONE_US": "[PHONE]",
        "SSN": "[SSN]",
        "CREDIT_CARD": "[CC]",
        "NAME": "[NAME]",
        "ORGANIZATION": "[ORG]",
        "LOCATION": "[LOC]",
        "IP_ADDRESS": "[IP]",
        "DATE_ISO": "[DATE]",
    }
    for entity in reversed(entities):
        placeholder = type_placeholders.get(entity.label, "[REDACTED]")
        custom_redacted = (custom_redacted[:entity.start] +
                           placeholder +
                           custom_redacted[entity.end:])
    print(custom_redacted)


if __name__ == "__main__":
    main()
