"""NLP intent extraction and entity recognition."""

import logging
from datetime import datetime
import spacy

from app.constants import MAX_INPUT_LENGTH
from app.schemas import IntentResult, ExtractedEntities

logger = logging.getLogger(__name__)

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.error("spaCy model 'en_core_web_sm' not found. Install with: python -m spacy download en_core_web_sm")
    raise

INTENT_KEYWORDS = {
    "hr_agent": ["onboard", "hire", "employee", "recruit", "joining", "staff", "payroll"],
    "finance_agent": ["invoice", "reconcile", "payment", "billing", "expense", "budget", "duplicate"],
    "it_agent": ["bug", "triage", "ticket", "crash", "error", "issue", "support", "fix"],
    "sales_agent": ["lead", "prospect", "customer", "deal", "pitch", "retail", "convert"],
    "operations_agent": ["schedule", "procure", "supply", "logistics", "vendor", "order"],
}

PRIORITY_KEYWORDS = {
    "high": ["urgent", "asap", "critical", "immediately", "emergency", "now"],
    "medium": ["soon", "today", "monday", "this week"],
    "low": ["whenever", "low priority", "sometime", "no rush"],
}


def extract_intent(text: str) -> IntentResult:
    """
    Extract intent and entities from natural language text.

    Args:
        text: Natural language input

    Returns:
        IntentResult with detected intent, entities, and priority

    Raises:
        ValueError: If text is invalid or too long
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    if len(text) > MAX_INPUT_LENGTH:
        raise ValueError(f"Input exceeds maximum length of {MAX_INPUT_LENGTH}")

    if not text.strip():
        raise ValueError("Input cannot be empty")

    try:
        logger.debug(f"Processing text: {text[:50]}...")

        # Process with spaCy
        text_lower = text.lower()
        doc = nlp(text_lower)
        original_doc = nlp(text)

        # Extract entities
        entities = ExtractedEntities()
        for ent in original_doc.ents:
            if ent.label_ == "PERSON":
                entities.persons.append(ent.text)
            elif ent.label_ in ["DATE", "TIME"]:
                entities.dates.append(ent.text)
            elif ent.label_ == "ORG":
                entities.orgs.append(ent.text)
            else:
                entities.misc.append(ent.text)

        # Detect intent
        detected_intent = "unknown"
        matched_keywords = []
        max_matches = 0

        for agent, keywords in INTENT_KEYWORDS.items():
            matches = [kw for kw in keywords if kw in text_lower]
            if len(matches) > max_matches:
                max_matches = len(matches)
                detected_intent = agent
                matched_keywords = matches

        # Detect priority
        detected_priority = "medium"
        for priority, keywords in PRIORITY_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                detected_priority = priority
                break

        result = IntentResult(
            raw_text=text,
            intent=detected_intent,
            entities=entities,
            priority=detected_priority,
            matched_keywords=matched_keywords,
            timestamp=datetime.now().isoformat()
        )

        logger.info(f"Intent detected: {detected_intent} (priority: {detected_priority})")
        return result

    except Exception as e:
        logger.error(f"Intent extraction failed: {e}", exc_info=True)
        raise ValueError(f"Failed to extract intent: {e}") from e
