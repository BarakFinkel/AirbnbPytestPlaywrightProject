from playwright.sync_api import Page
from models.utilities.helper_methods import increment_n_times
from datetime import date

class SearchBar:

    def __init__(self, page: Page):
        self.page = page
        self.little_search_bar_open_button = self.page.get_by_test_id("little-search-location")
        self.search_input = self.page.get_by_test_id("structured-search-input-field-query")
        self.check_in_button = self.page.get_by_role("button").filter(has_text="Check in")
        self.check_out_button = self.page.get_by_role("button").filter(has_text="Check out")
        self.guests_num_entry_button = self.page.get_by_role("button").filter(has_text="Add guests")
        self.guests_num_assert_button = self.page.get_by_role("button").filter(has_text="Who")
        self.search_button = self.page.get_by_test_id("structured-search-input-search-button")

    def input_destination(self, destination : str) -> None:
        """
        Inputs the desired destination within the search bar's input area.
        :param destination:
        :return:
        """
        self.search_input.fill(destination)
        options = self.page.get_by_role("option")
        options.filter(has_text=destination).first.click()

    def assert_destination(self, destination : str) -> None:
        """
        Asserts that the destination is written the search bar
        :param destination:
        :return:
        """
        assert destination in self.search_input.input_value()

    def choose_dates(self, check_in_date : date, check_out_date : date) -> None:
        """
        A method that chooses the dates' corresponding check-in and check-out buttons,
        if the dates are valid.
        :param check_in_date: The check-in date.
        :param check_out_date: The check-out date.
        :return: None
        """
        today = date.today()

        # If the dates are invalid, raise an error.
        if not (today <= check_in_date < check_out_date):
            raise ValueError(f"Invalid dates: check-in={check_in_date}, check-out={check_out_date}")

        # We first get our formatted dates
        formatted_check_in_date = check_in_date.strftime("%Y-%m-%d")
        formatted_check_out_date = check_out_date.strftime("%Y-%m-%d")
        print(f"Check-in date: {formatted_check_in_date}")
        print(f"Check-out date: {formatted_check_out_date}")

        # Then, we find the buttons that match our chosen dates and click to choose them.
        self.page.locator(f'[data-state--date-string="{formatted_check_in_date}"]').first.click()
        self.page.locator(f'[data-state--date-string="{formatted_check_out_date}"]').first.click()

    def assert_dates(self, check_in_date : date, check_out_date : date) -> None:
        today = date.today()

        # We check if the dates that were already entered in the search bar are valid.
        assert (today <= check_in_date < check_out_date)

        # We get our dates in the format in which they appear in the selected dates buttons.
        formatted_check_in_date = check_in_date.strftime("%B %d").replace(" 0", " ")
        formatted_check_out_date = check_out_date.strftime("%B %d").replace(" 0", " ")

        # We then get the dates written in the search bar
        actual_check_in_date =  self.check_in_button.inner_text().split("\n")[-1]
        actual_check_out_date = self.check_out_button.inner_text().split("\n")[-1]

        # Then, we assert their match
        assert actual_check_in_date == formatted_check_in_date
        assert actual_check_out_date == formatted_check_out_date

    def choose_guests_num(self, adults: int = 0, children: int = 0, infants: int = 0, pets: int = 0) -> None:
        guest_types = {
            "adults": adults,
            "children": children,
            "infants": infants,
            "pets": pets
        }

        # For each type of guest and their amount - we click the relevant increase button 'amount' times.
        for guest_type, amount in guest_types.items():
            if amount > 0:
                increment_button = self.page.get_by_test_id(f"stepper-{guest_type}-increase-button").first
                increment_n_times(increment_button, n=amount)

    def assert_guests_num(self, adults: int = 0, children: int = 0, infants: int = 0, pets: int = 0) -> None:
        guest_types = {
            "adults": adults,
            "children": children,
            "infants": infants,
            "pets": pets
        }

        # For each type of guest and their amount - we check if it's stepper's value equals 'amount'
        for guest_type, amount in guest_types.items():
            value = int(self.page.get_by_test_id(f"stepper-{guest_type}-value").first.inner_text())
            assert value == amount

    def search(self) -> None:
        self.search_button.click()