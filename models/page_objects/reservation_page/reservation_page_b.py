from playwright.sync_api import Page
from models.page_objects.reservation_page.reservation_page import ReservationPage
from models.utilities.helper_methods import convert_date_string_format, remove_non_alphanumeric_and_dot


class ReservationPageTypeB(ReservationPage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.general_edit_panel_open = page.locator('button:has(span[data-button-content="true"]:has-text("Change"))').first
        self.guests_edit_panel_open = page.locator('[id="tab--checkout-update-details-modal-tabs--1"]')
        self.guests_info_locators = {
            "adults": page.get_by_test_id("checkout-update-details-modal-guest_picker-adults-stepper-value"),
            "children": page.get_by_test_id("checkout-update-details-modal-guest_picker-children-stepper-value"),
            "infants": page.get_by_test_id("checkout-update-details-modal-guest_picker-infants-stepper-value"),
            "pets": page.get_by_test_id("checkout-update-details-modal-guest_picker-pets-stepper-value")
        }
        self.price_locator = page.get_by_test_id("pd-value-TOTAL")
        self.continue_button = self.page.locator('button:has(span[data-button-content="true"]:has-text("Continue"))').first

    def input_phone_number(self, prefix: int, number: int) -> None:
        """
        Inputs the phone number of the reservation.
        :return: None
        """
        self.continue_button.click()
        super().input_phone_number(prefix, number)

    def get_reservation_dates(self) -> tuple[str, str]:
        """
        Extracts the reservation's dates in m/d/y format.
        :return: Tuple containing (check_in_date, check_out_date)
        """
        self.general_edit_panel_open.click()
        check_in = convert_date_string_format(self.selected_check_in_locator.get_attribute("aria-label"))
        check_out = convert_date_string_format(self.selected_check_out_locator.get_attribute("aria-label"))
        self.general_edit_panel_close.click()
        return check_in, check_out

    def get_guests_info(self) -> dict[str, int]:
        """
        Extracts the guests stepper counters.
        :return: A dictionary [containing guest_type (str) : stepper_counter_value (int)]
        """
        self.general_edit_panel_open.click()
        self.guests_edit_panel_open.click()
        guests = {k: int(v.inner_text()) for k, v in self.guests_info_locators.items()}
        self.general_edit_panel_close.click()
        return guests

    def get_price(self) -> int:
        """
        Extracts the price of the reservation from the page.
        :return: The price, rounded.
        """
        return round(float(remove_non_alphanumeric_and_dot(self.price_locator.inner_text())))