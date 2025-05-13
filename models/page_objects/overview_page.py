from playwright.sync_api import Page
from models.page_objects.base_page import BasePage
from models.utilities.helper_methods import remove_non_alphanumeric


class OverviewPage(BasePage):

    def __init__(self, page: Page, url: str):
        super().__init__(page, url)

        # Handles popup in case it happens.
        self.page.add_locator_handler(self.page.locator('[aria-label="Translation on"]'),
                                     lambda  : self.page.keyboard.press("Escape", delay=500))

        self.check_in_locator = self.page.get_by_test_id("change-dates-checkIn")
        self.check_out_locator = self.page.get_by_test_id("change-dates-checkOut")

        self.guests_open_button = self.page.locator('[aria-labelledby="guests-label GuestPicker-book_it-trigger"]')
        self.guests_close_button = self.page.locator('[aria-labelledby="GuestPicker-book_it-form"]').get_by_role("button", name="Close")
        self.guests_info_locators = {
            "adults": self.page.get_by_test_id("GuestPicker-book_it-form-adults-stepper-value"),
            "children": self.page.get_by_test_id("GuestPicker-book_it-form-children-stepper-value"),
            "infants": self.page.get_by_test_id("GuestPicker-book_it-form-infants-stepper-value"),
            "pets": self.page.get_by_test_id("GuestPicker-book_it-form-pets-stepper-value")
        }

        self.price_locator = self.page.locator('[class="_j1kt73"]').last

        self.reserve_button = self.page.get_by_test_id("homes-pdp-cta-btn").last

    def get_all_details(self) -> tuple[str, str, dict[str, int], int]:
        """
        Extracts all desired details from the overview page.
        :return: A tuple containing (check_in_date, check_out_date, guests, price)
        """
        check_in = self.get_check_in_date()
        check_out = self.get_check_out_date()
        guests = self.get_guests_info()
        price = self.get_price()
        return check_in, check_out, guests, price

    def get_check_in_date(self) -> str:
        """
        Extracts the offer's check-in date.
        :return: The check-in date
        """
        self.check_in_locator.wait_for(state="visible", timeout=3000)
        return self.check_in_locator.inner_text()

    def get_check_out_date(self) -> str:
        """
        Extracts the offer's check-out date.
        :return: The check-out date
        """
        self.check_in_locator.wait_for(state="visible", timeout=3000)
        return self.check_out_locator.inner_text()

    def get_guests_info(self) -> dict[str, int]:
        """
        Extracts the guests stepper counters.
        :return: A dictionary [containing guest_type (str) : stepper_counter_value (int)]
        """
        self.guests_open_button.click()
        guests = { key: int(val.inner_text()) for key, val in self.guests_info_locators.items() }
        self.guests_close_button.click()
        return guests

    def get_price(self) -> int:
        """
        Extracts the price of the offer from the page.
        :return: The price, rounded.
        """
        return int(remove_non_alphanumeric(self.price_locator.inner_text()))

    def print_details(self):
        """
        Prints the offer's details.
        :return: None
        """
        print("Deal details:")
        print("Check in: " + self.get_check_in_date())
        print("Check out: " + self.get_check_out_date())
        for key, val in self.get_guests_info().items():
            print(f"{key}: {str(val)}")
        print("Price: " + str(self.get_price()))

    def click_reserve(self) -> None:
        """
        Clicks the reserve button.
        :return: None
        """
        self.reserve_button.click()
