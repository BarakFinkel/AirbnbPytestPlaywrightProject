from datetime import date
from playwright.sync_api import Page
from models.base_page import BasePage
from models.page_components.card_container import CardContainer

class MainPage(BasePage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)

