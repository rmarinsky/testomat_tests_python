from pydantic import BaseModel, ConfigDict, Field


class TestAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str = ""
    state: str = "manual"
    suite_id: str | None = Field(default=None, alias="suite-id")
    description: str | None = None
    priority: str | None = None
    sync: bool = True
    tags: list[str] = Field(default_factory=list)
    code: str | None = None
    file: str | None = None


class Test(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    type: str = "test"
    attributes: TestAttributes = Field(default_factory=TestAttributes)

    @property
    def title(self) -> str:
        return self.attributes.title

    @property
    def state(self) -> str:
        return self.attributes.state

    @property
    def suite_id(self) -> str | None:
        return self.attributes.suite_id

    @property
    def description(self) -> str | None:
        return self.attributes.description

    @property
    def priority(self) -> str | None:
        return self.attributes.priority

    def get_url(self, project_id: str) -> str:
        """Get the URL path for this test case."""
        return f"/projects/{project_id}/tests/{self.id}"


class TestResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data: Test
