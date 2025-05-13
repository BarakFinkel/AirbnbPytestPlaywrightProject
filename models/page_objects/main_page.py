from datetime import date
from playwright.sync_api import Page
from models.page_objects.base_page import BasePage
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
        """
        A method that takes in expected data and inputs it within the search bar.
        :param destination: The expected destination.
        :param start_date: The expected check-in date.
        :param end_date: The expected check-out date.
        :param num_of_adults: The expected number of adults.
        :param num_of_children: The expected number of children.
        :param num_of_infants: The expected number of infants.
        :param num_of_pets: The expected number of pets.
        :return: None
        """
        self.search_bar.input_destination(destination)
        self.search_bar.choose_dates(start_date, end_date)
        self.search_bar.guests_num_entry_button.click()
        self.search_bar.choose_guests_num(num_of_adults, num_of_children, num_of_infants, num_of_pets)
        self.search_bar.search()