from __future__ import annotations
import pytest
from git_day_practice.agent import build_agent_plan, build_confidence_dict


def test_build_agent_plan_returns_steps() -> None:
    plan = build_agent_plan("What does Qdrant do?")
    assert isinstance(plan, list)
    assert len(plan) == 4


def test_build_agent_plan_contains_retrieve_step() -> None:
    plan = build_agent_plan("What does Qdrant do?")
    assert any("Retrieve" in step or "retrieve" in step for step in plan)


def test_build_confidence_dict_empty() -> None:
    result = build_confidence_dict([])
    assert result["top_score"] == 0.0
    assert result["avg_score"] == 0.0
    assert result["result_count"] == 0


def test_build_confidence_dict_with_results() -> None:
    results = [
        {"score": 0.9},
        {"score": 0.7},
        {"score": 0.5},
    ]
    result = build_confidence_dict(results)
    assert result["top_score"] == 0.9
    assert result["avg_score"] == 0.7
    assert result["result_count"] == 3