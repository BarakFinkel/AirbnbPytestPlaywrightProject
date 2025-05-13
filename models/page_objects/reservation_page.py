from enum import Enum

from playwright.sync_api import Page, Locator
from models.page_objects.base_page import BasePage
from models.utilities.helper_methods import get_locator_containing, convert_date_string_format

class ReservationPageType(Enum):
    """
    An enum to determine the type of reservation page being presented.
    """
    TYPE_A = 1
    TYPE_B = 2

class ReservationPage(BasePage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)

        self.phone_input = self.page.get_by_test_id("login-signup-phonenumber")
        self.page_type = ReservationPageType.TYPE_A if self.phone_input.count() > 0 else ReservationPageType.TYPE_B

        self.general_edit_panel_open = self.page.locator('button:has(span[data-button-content="true"]:has-text("Change"))').first

        self.dates_edit_panel_open = self.page.get_by_test_id("checkout_platform.DATE_PICKER.edit")
        self.selected_check_in_locator = get_locator_containing(self.page, "aria-label", "Selected").first
        self.selected_check_out_locator = get_locator_containing(self.page, "aria-label", "Selected").last

        self.guests_edit_panel_open = self.get_guests_open_button_locator()
        self.guests_button = self.page.get_by_role("button", name="Guests")
        self.guests_info_locators = self.get_guests_info_locators()

        self.general_edit_panel_close = self.page.locator('[aria-label="Close"]').last

        self.price_locator = self.get_price_locator()

        self.continue_button = self.page.locator('button:has(span[data-button-content="true"]:has-text("Continue"))').first
        self.number_prefix_selector = self.page.get_by_test_id("login-signup-countrycode")

    def get_all_details(self) -> tuple[str, str, dict[str, int], int]:
        """
        Extracts all desired details from the reservation page.
        :return: A tuple containing (check_in_date, check_out_date, guests, price)
        """
        check_in_date, check_out_date = self.get_reservation_dates()
        guests = self.get_guests_info()
        price = self.get_price()
        return check_in_date, check_out_date, guests, price

    def get_reservation_dates(self) -> tuple[str, str]:
        """
        Extracts the reservation's dates in m/d/y format.
        :return: Tuple containing (check_in_date, check_out_date)
        """
        if self.page_type == ReservationPageType.TYPE_A:
            self.dates_edit_panel_open.click()
        else:
            self.general_edit_panel_open.click()

        check_in_date  = convert_date_string_format(self.selected_check_in_locator.get_attribute("aria-label"))
        check_out_date = convert_date_string_format(self.selected_check_out_locator.get_attribute("aria-label"))

        self.general_edit_panel_close.click()

        return check_in_date, check_out_date

    def get_guests_info(self) -> dict[str, int]:
        """
        Extracts the guests stepper counters.
        :return: A dictionary [containing guest_type (str) : stepper_counter_value (int)]
        """
        if self.page_type == ReservationPageType.TYPE_B:
            self.general_edit_panel_open.click()
        self.guests_edit_panel_open.click()

        guests = { key: int (val.inner_text()) for key, val in self.guests_info_locators.items() }

        self.general_edit_panel_close.click()

        return guests

    def get_price(self) -> int:
        """
        Extracts the price of the reservation from the page.
        :return: The price, rounded.
        """
        return round(float(self.price_locator.inner_text()[1:]), ndigits=None)

    def print_details(self) -> None:
        """
        Prints the reservation's details.
        :return: None
        """
        print("Deal details:")
        check_in_date, check_out_date = self.get_reservation_dates()
        print("Check in: " + check_in_date)
        print("Check out: " + check_out_date)
        for key, val in self.get_guests_info().items():
            print(f"{key}: {val}")
        print("Price: " + str(self.get_price()))

    def input_phone_number(self, prefix : int, number : int) -> None:
        """
        Inputs the phone number of the reservation.
        :return: None
        """
        if self.page_type == ReservationPageType.TYPE_B:
            self.continue_button.click()

        self.select_dial_prefix(prefix)
        self.phone_input.fill(str(number))

    def select_dial_prefix(self, prefix: int):
        """
        Selects the desired country-dial according to the entered prefix.
        :param prefix: the country code, without '+' sign.
        :return: None
        """
        formatted_prefix = "(+" + str(prefix) + ")"

        # Gets all options available from the selector
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

    def get_guests_open_button_locator(self) -> Locator:
        """
        Gets the locator to the guests button.
        :return: Appropriate Locator.
        """
        if self.page_type == ReservationPageType.TYPE_A:
            return self.page.get_by_test_id("checkout_platform.GUEST_PICKER.edit")
        else:
            return self.page.locator('[id="tab--checkout-update-details-modal-tabs--1"]')

    def get_guests_info_locators(self) -> dict[str, Locator]:
        """
        Gets the locators to the guests stepper counters.
        :return: Appropriate Locator.
        """
        if self.page_type == ReservationPageType.TYPE_A:
            return {
                "adults": self.page.get_by_test_id("GUEST_PICKER-adults-stepper-value"),
                "children": self.page.get_by_test_id("GUEST_PICKER-children-stepper-value"),
                "infants": self.page.get_by_test_id("GUEST_PICKER-infants-stepper-value"),
                "pets": self.page.get_by_test_id("GUEST_PICKER-pets-stepper-value")
            }
        else:
            return {
                "adults": self.page.get_by_test_id("checkout-update-details-modal-guest_picker-adults-stepper-value"),
                "children": self.page.get_by_test_id("checkout-update-details-modal-guest_picker-children-stepper-value"),
                "infants": self.page.get_by_test_id("checkout-update-details-modal-guest_picker-infants-stepper-value"),
                "pets": self.page.get_by_test_id("checkout-update-details-modal-guest_picker-pets-stepper-value")
            }

    def get_price_locator(self) -> Locator:
        """
        Gets the locator to the price element according to the page's type.
        :return: Appropriate Locator.
        """
        if self.page_type == ReservationPageType.TYPE_A:
            return self.page.get_by_test_id("price-item-total")
        else:
            return self.page.get_by_test_id("pd-value-TOTAL")
