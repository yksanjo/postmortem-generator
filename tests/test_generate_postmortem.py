"""Tests for the post-mortem generator."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_postmortem import generate_postmortem


def _doc():
    return generate_postmortem(
        incident_name="API Outage",
        incident_date="2024-01-15",
        duration="2 hours",
        impact="Checkout unavailable for ~30% of users",
        root_cause="Connection pool exhaustion under load",
    )


def test_returns_markdown_with_title():
    doc = _doc()
    assert doc.startswith("# Post-Mortem: API Outage")


def test_includes_required_fields():
    doc = _doc()
    assert "Checkout unavailable for ~30% of users" in doc
    assert "Connection pool exhaustion under load" in doc
    assert "2 hours" in doc


def test_formats_known_date():
    doc = _doc()
    assert "January 15, 2024" in doc


def test_default_action_items_present():
    doc = _doc()
    assert "Document lessons learned" in doc


def test_custom_timeline_and_resolution_used():
    doc = generate_postmortem(
        incident_name="DB Failover",
        incident_date="2024-02-01",
        duration="15 minutes",
        impact="Read latency spike",
        root_cause="Primary node crash",
        timeline="- 10:00 detected\n- 10:15 resolved",
        resolution="Promoted replica to primary.",
    )
    assert "10:00 detected" in doc
    assert "Promoted replica to primary." in doc


def test_unparseable_date_passed_through():
    doc = generate_postmortem(
        incident_name="X",
        incident_date="last Tuesday",
        duration="1h",
        impact="i",
        root_cause="r",
    )
    assert "last Tuesday" in doc
