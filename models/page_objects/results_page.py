from datetime import date
from typing import Callable

from playwright.sync_api import Page
from models.page_objects.base_page import BasePage
from models.page_components.card_container import CardContainer, best_card_in_list
from models.page_components.search_bar import SearchBar

WEBSITE_PREFIX = "https://airbnb.com"

class ResultsPage(BasePage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.locator    = page.get_by_test_id("card-container")
        self.search_bar = SearchBar(page)
        self.first_url  = page.url
        self.next_page_button = page.get_by_role("link", name="Next")

    def assert_preferences(
            self,
            destination: str,
            start_date: date,
            end_date: date,
            num_of_adults: int = 0,
            num_of_children: int = 0,
            num_of_infants: int = 0,
            num_of_pets: int = 0
    ):
        """
        A method that takes in expected data and asserts their match within the search bar.
        :param destination: The expected destination.
        :param start_date: The expected check-in date.
        :param end_date: The expected check-out date.
        :param num_of_adults: The expected number of adults.
        :param num_of_children: The expected number of children.
        :param num_of_infants: The expected number of infants.
        :param num_of_pets: The expected number of pets.
        :return: None
        """
        self.search_bar.little_search_bar_open_button.click()
        self.search_bar.assert_destination(destination)
        self.search_bar.assert_dates(start_date, end_date)
        self.search_bar.assert_guests_num(num_of_adults, num_of_children, num_of_infants, num_of_pets)

    def goto_first_page(self):
        self.page.goto(self.first_url)

    def extract_highest_rated_card(self, print_result : bool) -> str:
        return self.extract_best_card(lambda a, b: a.is_rated_better(b), print_result)

    def extract_lowest_priced_card(self, print_result : bool) -> str:
        return self.extract_best_card(lambda a, b: a.is_lower_priced(b), print_result)

    def extract_best_card(self, is_better: Callable[[CardContainer, CardContainer], bool], print_result : bool) -> str:
        """
        Traverses paginated results and returns the URL and index of the best card
        according to the provided comparator.
        :param is_better: The comparator method.
        :param print_result: A parameter to toggle printing the result of the method.
        :return: The best card's page url and locator index.
        """
        best_page_index = -1
        best_card_index = -1
        best_result_url = ""
        best_card = None
        page_count = 0

        while True:
            # Wait for the first and list card container locators.
            self.locator.first.wait_for(state="visible", timeout=10000)
            self.locator.last.wait_for(state="visible", timeout=10000)

            # Get all visible card locators
            card_locators = self.locator.all()
            card_containers = [CardContainer(locator) for locator in card_locators]

            # Get the best card in the current page's list.
            current_best_index = best_card_in_list(card_containers, is_better)
            current_best_card = card_containers[current_best_index]

            # If the current page's best card is better than the overall best card, we store its info as the new best card.
            if best_card is None or is_better(current_best_card, best_card):
                best_card = current_best_card
                best_page_index = page_count
                best_card_index = current_best_index
                best_result_url = best_card.url

            # If we can move to the next page, we do so.
            # Otherwise, we break the loop.
            if not self.next_page_button.is_visible() or self.next_page_button.is_disabled():
                break
            self.next_page_button.click()
            page_count += 1

        # Print result if requested
        if print_result:
            print("\nBest Choice Details:")
            print("Found in page no. " + str(best_page_index + 1) + " at index: " + str(best_card_index + 1))
            print(best_card.print_card_details())
            print("Result URL: " + WEBSITE_PREFIX + best_result_url + "\n")

        # Lastly, go back to the first page and return the result
        self.goto_first_page()
        return WEBSITE_PREFIX + best_result_url