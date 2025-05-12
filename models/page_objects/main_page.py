from datetime import date
from playwright.sync_api import Page
from models.base_page import BasePage
from models.page_components.search_bar import SearchBar

class MainPage(BasePage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.search_bar = SearchBar(page)

    def search_preferences(
            self,
            destination : str,
            start_date : date,
            end_date : date,
            num_of_adults : int = 0,
            num_of_children : int = 0,
            num_of_infants : int = 0,
            num_of_pets : int = 0
    ):
        self.search_bar.input_destination(destination)
        self.search_bar.choose_dates(start_date, end_date)
        self.search_bar.choose_guests_num(num_of_adults, num_of_children, num_of_infants, num_of_pets)
        self.search_bar.search()