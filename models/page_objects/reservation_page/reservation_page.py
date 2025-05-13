from playwright.sync_api import Page
from models.page_objects.base_page import BasePage

class ReservationPage(BasePage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.general_edit_panel_close = self.page.locator('[aria-label="Close"]').last
        self.selected_check_in_locator = self.page.locator(f'[{"aria-label"}*="{"Selected"}"]').first
        self.selected_check_out_locator = self.page.locator(f'[{"aria-label"}*="{"Selected"}"]').last
        self.continue_button = self.page.locator('button:has(span[data-button-content="true"]:has-text("Continue"))').first
        self.number_prefix_selector = self.page.get_by_test_id("login-signup-countrycode")
        self.phone_input = self.page.get_by_test_id("login-signup-phonenumber")

    def get_all_details(self) -> tuple[str, str, dict[str, int], int]:
        """
        Extracts all desired details from the reservation page.
        :return: A tuple containing (check_in_date, check_out_date, guests, price)
        """
        check_in_date, check_out_date = self.get_reservation_dates()
        guests = self.get_guests_info()
        price = self.get_price()
        return check_in_date, check_out_date, guests, price

    def select_dial_prefix(self, prefix: int) -> None:
        """
        Selects the desired country-dial according to the entered prefix.
        :param prefix: the country code, without '+' sign.
        :return: None
        """
        formatted_prefix = f"(+{prefix})"

        # Gets all options available from the selector
        self.number_prefix_selector.click()
        options = self.number_prefix_selector.locator("option")
        count = options.count()

        # Goes over all of them, potentially finds a match and selects it.
        # Otherwise, will raise an error.
        for i in range(count):
            text = options.nth(i).text_content()
            if formatted_prefix in text:
                value = options.nth(i).get_attribute("value")
                self.number_prefix_selector.select_option(value=value)
                return

        raise ValueError(f"No option found containing '{prefix}'")

    def input_phone_number(self, prefix: int, number: int) -> None:
        """
        Inputs the phone number of the reservation.
        :return: None
        """
        self.select_dial_prefix(prefix)
        self.phone_input.fill(str(number))

    def print_details(self) -> None:
        """
        Prints the reservation's details.
        :return: None
        """
        print("Deal details:")
        check_in_date, check_out_date = self.get_reservation_dates()
        print(f"Check in: {check_in_date}")
        print(f"Check out: {check_out_date}")
        for key, val in self.get_guests_info().items():
            print(f"{key}: {val}")
        print(f"Price: {self.get_price()}")

    # Abstract Methods to be implemented by child classes:
    def get_reservation_dates(self) -> tuple[str, str]: ...

    def get_guests_info(self) -> dict[str, int]: ...

    def get_price(self) -> int: ...