"""Unit tests for research project Pydantic schemas."""

import pytest
from pydantic import ValidationError

from app.schemas.research import ResearchProjectCreate, ResearchStatus


def test_research_project_create_defaults() -> None:
    project = ResearchProjectCreate(title="Quantum Entanglement Study")
    assert project.status == ResearchStatus.draft
    assert project.summary == ""


def test_research_project_create_requires_title() -> None:
    with pytest.raises(ValidationError):
        ResearchProjectCreate(title="")
