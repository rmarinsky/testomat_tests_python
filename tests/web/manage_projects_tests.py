from src.web.Application import Application


def test_(login, app: Application):
    app.home_page.open()
