from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    is_share_public_report: bool = Field(default=False, alias="is-share-public-report")
    is_share_living_docs: bool = Field(default=False, alias="is-share-living-docs")
    is_keep_ids_in_feature: bool = Field(default=False, alias="is-keep-ids-in-feature")
    is_shows_test_type: bool = Field(default=True, alias="is-shows-test-type")
    is_run_folder_required: bool = Field(default=False, alias="is-run-folder-required")
    semantic_search: bool = Field(default=False, alias="semantic-search")
    similar_search: bool = Field(default=False, alias="similar-search")
    ai_chat: bool = Field(default=False, alias="ai-chat")
    labels_permission: bool = Field(default=False, alias="labels-permission")
    archive_storage: bool = Field(default=False, alias="archive-storage")


class ProjectAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str = ""
    status: str = ""
    tests_count: int | None = Field(default=0, alias="tests-count")
    created_at: datetime | None = Field(default=None, alias="created-at")
    lang: str | None = None
    framework: str | None = None
    url: str | None = None
    demo: bool = False
    has_living_docs: bool = Field(default=False, alias="has-living-docs")
    record_url: str | None = Field(default=None, alias="record-url")
    avatar: str | None = None
    api_key: str | None = Field(default=None, alias="api-key")
    testomatio_url: str | None = Field(default=None, alias="testomatio-url")
    branch: str | None = None
    living_doc_url: str | None = Field(default=None, alias="living-doc-url")
    project_settings: ProjectSettings | None = Field(default=None, alias="project-settings")


class Project(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    type: str
    attributes: ProjectAttributes

    @property
    def title(self) -> str:
        return self.attributes.title

    @property
    def status(self) -> str:
        return self.attributes.status

    @property
    def tests_count(self) -> int:
        return self.attributes.tests_count


class ProjectsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data: list[Project] = Field(default_factory=list)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]
