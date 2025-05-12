from playwright.sync_api import Page, Locator
from datetime import date

def increment_n_times(button: Locator, n : int) -> None:
    for i in range(n):
        button.click()

class SearchBar:

    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.get_by_test_id("structured-search-input-field-query")
        self.guests_num_button = page.get_by_test_id("structured-search-input-field-guests-button")
        self.search_button = page.get_by_test_id("structured-search-input-search-button")

    def input_destination(self, destination : str) -> None:
        self.search_input.fill(destination)
        options = self.page.get_by_role("option")
        chosen_option = options.filter(has_text=destination).first
        chosen_option.click()

    def choose_dates(self, check_in_date : date, check_out_date : date) -> None:
        today = date.today()

        if check_in_date < today or check_out_date < today or check_out_date <= check_in_date:
            raise Exception("Please enter valid vacation dates")

        formatted_check_in_date = check_in_date.strftime("%Y-%m-%d")
        formatted_check_out_date = check_out_date.strftime("%Y-%m-%d")

        self.page.locator(f'[data-state--date-string="{formatted_check_in_date}"]').click()
        self.page.locator(f'[data-state--date-string="{formatted_check_out_date}"]').click()

    def choose_guests_num(self, adults: int = 0, children: int = 0, infants: int = 0, pets: int = 0) -> None:
        self.guests_num_button.click()

        guest_types = {
            "adults": adults,
            "children": children,
            "infants": infants,
            "pets": pets
        }

        for guest_type, amount in guest_types.items():
            if amount > 0:
                increment_button = self.page.get_by_test_id(f"stepper-{guest_type}-increase-button")
                increment_n_times(increment_button, n=amount)

    def search(self) -> None:
        self.search_button.click()