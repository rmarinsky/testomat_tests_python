import pytest

from src.web.Application import Application


@pytest.mark.regression
@pytest.mark.web
def test_(login, app: Application):
    app.home_page.open()
