from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SuitePyAttributes(BaseModel):
    title: str
    description: str
    emoji: Any
    code: str | None
    sync: bool
    file_type: str = Field(..., alias="file-type")
    test_count: int = Field(..., alias="test-count")
    filtered_tests: Any = Field(..., alias="filtered-tests")
    file: Any
    is_root: bool = Field(..., alias="is-root")
    jira_issues: Any = Field(..., alias="jira-issues")


class SuitePy(BaseModel):
    id: str
    type: str
    attributes: SuitePyAttributes
    relationships: dict[str, Any]
