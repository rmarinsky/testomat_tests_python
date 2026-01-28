from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ProjectSettings:
    is_share_public_report: bool = False
    is_share_living_docs: bool = False
    is_keep_ids_in_feature: bool = False
    is_shows_test_type: bool = True
    is_run_folder_required: bool = False
    semantic_search: bool = False
    similar_search: bool = False
    ai_chat: bool = False
    labels_permission: bool = False
    archive_storage: bool = False

    @classmethod
    def from_dict(cls, data: dict | None) -> "ProjectSettings | None":
        if data is None:
            return None
        return cls(
            is_share_public_report=data.get("is_share_public_report", False),
            is_share_living_docs=data.get("is_share_living_docs", False),
            is_keep_ids_in_feature=data.get("is_keep_ids_in_feature", False),
            is_shows_test_type=data.get("is_shows_test_type", True),
            is_run_folder_required=data.get("is_run_folder_required", False),
            semantic_search=data.get("semantic_search", False),
            similar_search=data.get("similar_search", False),
            ai_chat=data.get("ai_chat", False),
            labels_permission=data.get("labels_permission", False),
            archive_storage=data.get("archive_storage", False),
        )


@dataclass
class ProjectAttributes:
    title: str
    status: str
    tests_count: int
    created_at: datetime | None
    lang: str | None = None
    framework: str | None = None
    url: str | None = None
    demo: bool = False
    has_living_docs: bool = False
    record_url: str | None = None
    avatar: str | None = None
    api_key: str | None = None
    testomatio_url: str | None = None
    branch: str | None = None
    living_doc_url: str | None = None
    project_settings: ProjectSettings | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "ProjectAttributes":
        created_at = None
        if data.get("created-at"):
            created_at = datetime.fromisoformat(data["created-at"].replace("Z", "+00:00"))

        return cls(
            title=data.get("title", ""),
            status=data.get("status", ""),
            tests_count=data.get("tests-count", 0),
            created_at=created_at,
            lang=data.get("lang"),
            framework=data.get("framework"),
            url=data.get("url"),
            demo=data.get("demo", False),
            has_living_docs=data.get("has-living-docs", False),
            record_url=data.get("record-url"),
            avatar=data.get("avatar"),
            api_key=data.get("api-key"),
            testomatio_url=data.get("testomatio-url"),
            branch=data.get("branch"),
            living_doc_url=data.get("living-doc-url"),
            project_settings=ProjectSettings.from_dict(data.get("project-settings")),
        )


@dataclass
class Project:
    id: str
    type: str
    attributes: ProjectAttributes

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        return cls(
            id=data["id"],
            type=data["type"],
            attributes=ProjectAttributes.from_dict(data["attributes"]),
        )

    @property
    def title(self) -> str:
        return self.attributes.title

    @property
    def status(self) -> str:
        return self.attributes.status

    @property
    def tests_count(self) -> int:
        return self.attributes.tests_count


@dataclass
class ProjectsResponse:
    data: list[Project] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "ProjectsResponse":
        projects = [Project.from_dict(p) for p in data.get("data", [])]
        return cls(data=projects)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]
