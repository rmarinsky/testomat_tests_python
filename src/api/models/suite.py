from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SuiteAttributes(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    title: str | None = None
    description: str | None = None
    labels: list[str] | None = None
    tags: list[str] | None = None
    issues: list[str] | None = None
    jira_issues: list[str] | None = Field(default=None, alias="jira-issues")
    is_branched: bool | None = Field(default=None, alias="is-branched")
    is_detail: bool | None = Field(default=None, alias="is-detail")
    attachments: list[Any] | None = None
    emoji: str | None = None
    code: str | None = None
    sync: bool | None = None
    file_type: str | None = Field(default=None, alias="file-type")
    test_count: int | None = Field(default=None, alias="test-count")
    filtered_tests: list[Any] | None = Field(default=None, alias="filtered-tests")
    file: str | None = None
    notes: str | None = None
    created_at: datetime | None = Field(default=None, alias="created-at")
    updated_at: datetime | None = Field(default=None, alias="updated-at")
    assigned_to: str | None = Field(default=None, alias="assigned-to")
    to_url: str | None = Field(default=None, alias="to-url")
    comments_count: int | None = Field(default=None, alias="comments-count")
    position: int | None = None
    depth: int | None = None
    is_root: bool | None = Field(default=None, alias="is-root")
    public_title: str | None = Field(default=None, alias="public-title")
    parent_id: str | None = Field(default=None, alias="parent-id")
    path: str | list | None = None


class Suite(BaseModel):
    id: str | None = None
    type: str | None = None
    attributes: SuiteAttributes | None = None
    relationships: dict[str, Any] | None = None
