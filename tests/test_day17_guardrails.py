from __future__ import annotations

import sys
import os

# Add src to path
sys.path.insert(0, '/home/maryam205/git-day2-practice/src')

import pytest
from git_day_practice.guardrails import choose_rag_action, compute_confidence, is_query_too_vague


def test_is_query_too_vague_for_single_word() -> None:
    """Test that single word queries are considered vague"""
    assert is_query_too_vague("help") is True
    assert is_query_too_vague("hi") is True
    assert is_query_too_vague("hello") is True
    assert is_query_too_vague("?") is True


def test_is_query_too_vague_for_short_phrase() -> None:
    """Test that short vague phrases are detected"""
    assert is_query_too_vague("tell me") is True
    assert is_query_too_vague("explain") is True
    assert is_query_too_vague("what is this") is True


def test_is_query_too_vague_for_specific_query() -> None:
    """Test that specific queries are not considered vague"""
    assert is_query_too_vague("What is Qdrant and how does it work?") is False
    assert is_query_too_vague("How do I install PostgreSQL on Ubuntu?") is False
    assert is_query_too_vague("What are the benefits of using vector databases?") is False


def test_compute_confidence_empty_results() -> None:
    """Test confidence calculation with empty results"""
    confidence = compute_confidence([])
    assert confidence["top_score"] == 0.0
    assert confidence["avg_score"] == 0.0
    assert confidence["result_count"] == 0


def test_compute_confidence_with_single_result() -> None:
    """Test confidence calculation with one result"""
    results = [{"score": 0.85, "chunk_id": "c1"}]
    confidence = compute_confidence(results)
    assert confidence["top_score"] == 0.85
    assert confidence["avg_score"] == 0.85
    assert confidence["result_count"] == 1


def test_compute_confidence_with_multiple_results() -> None:
    """Test confidence calculation with multiple results"""
    results = [
        {"score": 0.90, "chunk_id": "c1"},
        {"score": 0.82, "chunk_id": "c2"},
        {"score": 0.80, "chunk_id": "c3"},
        {"score": 0.75, "chunk_id": "c4"},
    ]
    confidence = compute_confidence(results)
    assert confidence["top_score"] == 0.90
    assert confidence["avg_score"] == (0.90 + 0.82 + 0.80 + 0.75) / 4
    assert confidence["result_count"] == 4


def test_choose_rag_action_returns_clarify_for_vague_query() -> None:
    """Test that vague queries return clarify action"""
    decision = choose_rag_action("help", [])
    assert decision["action"] == "clarify"
    assert "vague" in decision["reason"].lower()


def test_choose_rag_action_returns_clarify_for_empty_query() -> None:
    """Test that empty/short queries return clarify"""
    decision = choose_rag_action("?", [])
    assert decision["action"] == "clarify"


def test_choose_rag_action_returns_refuse_for_empty_results() -> None:
    """Test that empty results trigger refuse"""
    decision = choose_rag_action("What is Qdrant?", [])
    assert decision["action"] == "refuse"
    assert "Not enough results" in decision["reason"]


def test_choose_rag_action_returns_refuse_for_low_top_score() -> None:
    """Test that low top score triggers refuse"""
    results = [
        {"score": 0.30, "chunk_id": "c1"},
        {"score": 0.25, "chunk_id": "c2"},
    ]
    decision = choose_rag_action("What is this?", results)
    assert decision["action"] == "refuse"
    assert "Top score too weak" in decision["reason"]


def test_choose_rag_action_returns_refuse_for_low_avg_score() -> None:
    """Test that low average score triggers refuse"""
    results = [
        {"score": 0.60, "chunk_id": "c1"},
        {"score": 0.30, "chunk_id": "c2"},
        {"score": 0.20, "chunk_id": "c3"},
    ]
    decision = choose_rag_action("What is this?", results)
    assert decision["action"] == "refuse"
    assert "Average score too weak" in decision["reason"]


def test_choose_rag_action_returns_answer_for_strong_results() -> None:
    """Test that strong results return answer action"""
    results = [
        {"score": 0.90, "chunk_id": "c1"},
        {"score": 0.85, "chunk_id": "c2"},
        {"score": 0.80, "chunk_id": "c3"},
    ]
    decision = choose_rag_action("What does Qdrant do?", results)
    assert decision["action"] == "answer"
    assert "sufficient" in decision["reason"].lower()
    assert decision["confidence"]["top_score"] == 0.90


def test_choose_rag_action_returns_confidence_metrics() -> None:
    """Test that confidence metrics are included in decision"""
    results = [
        {"score": 0.95, "chunk_id": "c1"},
        {"score": 0.88, "chunk_id": "c2"},
    ]
    decision = choose_rag_action("Test query?", results)
    assert "confidence" in decision
    assert decision["confidence"]["top_score"] == 0.95
    assert decision["confidence"]["avg_score"] == 0.915
    assert decision["confidence"]["result_count"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
