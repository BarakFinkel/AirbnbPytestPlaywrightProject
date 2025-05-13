from playwright.sync_api import Page
from models.page_objects.reservation_page.reservation_page import ReservationPage
from models.utilities.helper_methods import convert_date_string_format, remove_non_alphanumeric_and_dot


class ReservationPageTypeA(ReservationPage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.dates_edit_panel_open = page.get_by_test_id("checkout_platform.DATE_PICKER.edit")
        self.guests_edit_panel_open = page.get_by_test_id("checkout_platform.GUEST_PICKER.edit")
        self.guests_info_locators = {
            "adults": page.get_by_test_id("GUEST_PICKER-adults-stepper-value"),
            "children": page.get_by_test_id("GUEST_PICKER-children-stepper-value"),
            "infants": page.get_by_test_id("GUEST_PICKER-infants-stepper-value"),
            "pets": page.get_by_test_id("GUEST_PICKER-pets-stepper-value")
        }
        self.price_locator = page.get_by_test_id("price-item-total")

    def get_reservation_dates(self) -> tuple[str, str]:
        """
        Extracts the reservation's dates in m/d/y format.
        :return: Tuple containing (check_in_date, check_out_date)
        """
        self.dates_edit_panel_open.click()
        check_in = convert_date_string_format(self.selected_check_in_locator.get_attribute("aria-label"))
        check_out = convert_date_string_format(self.selected_check_out_locator.get_attribute("aria-label"))
        self.general_edit_panel_close.click()
        return check_in, check_out

    def get_guests_info(self) -> dict[str, int]:
        """
        Extracts the guests stepper counters.
        :return: A dictionary [containing guest_type (str) : stepper_counter_value (int)]
        """
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