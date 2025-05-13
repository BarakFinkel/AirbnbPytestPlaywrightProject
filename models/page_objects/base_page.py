from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page, url : str):
        self.page = page
        self.url = url

    def goto_self(self):
        self.page.goto(self.url)