"""Tests for NLP extraction."""

import pytest
from app.nlp.extractor import extract_intent


class TestExtractIntent:
    """Test intent extraction."""

    def test_extract_hr_intent(self):
        """Test extracting HR intent."""
        text = "Onboard new employee John"
        result = extract_intent(text)

        assert result.intent == "hr_agent"
        assert len(result.matched_keywords) > 0

    def test_extract_finance_intent(self):
        """Test extracting Finance intent."""
        text = "Reconcile invoices and find duplicates"
        result = extract_intent(text)

        assert result.intent == "finance_agent"

    def test_extract_it_intent(self):
        """Test extracting IT intent."""
        text = "There is a bug in the login page"
        result = extract_intent(text)

        assert result.intent == "it_agent"

    def test_extract_priority_high(self):
        """Test extracting high priority."""
        text = "Urgently fix the authentication error"
        result = extract_intent(text)

        assert result.priority == "high"

    def test_extract_priority_low(self):
        """Test extracting low priority."""
        text = "Sometime during the day, onboard a new employee"
        result = extract_intent(text)

        assert result.priority == "low"

    def test_extract_entities(self):
        """Test extracting named entities."""
        text = "Onboard John Smith to the Engineering department"
        result = extract_intent(text)

        # Should extract names or organizations
        assert len(result.entities.persons) > 0 or len(result.entities.orgs) > 0

    def test_extract_intent_empty_text_raises(self):
        """Test that empty text raises error."""
        with pytest.raises(ValueError):
            extract_intent("")

    def test_extract_intent_whitespace_only_raises(self):
        """Test that whitespace-only text raises error."""
        with pytest.raises(ValueError):
            extract_intent("   ")

    def test_extract_intent_too_long_raises(self):
        """Test that too-long text raises error."""
        long_text = "a" * 2001
        with pytest.raises(ValueError):
            extract_intent(long_text)

    def test_extract_intent_not_string_raises(self):
        """Test that non-string input raises error."""
        with pytest.raises(ValueError):
            extract_intent(12345)
