from playwright.sync_api import Page
from models.page_objects.reservation_page.reservation_page_a import ReservationPageTypeA
from models.page_objects.reservation_page.reservation_page_b import ReservationPageTypeB
from models.page_objects.reservation_page.reservation_page import ReservationPage  # optional, for typing

def create_reservation_page(page: Page, url: str) -> ReservationPage:
    phone_input = page.get_by_test_id("login-signup-phonenumber")
    try:
        phone_input.wait_for(state="visible", timeout=5000)
        return ReservationPageTypeA(page, url)
    except:
        return ReservationPageTypeB(page, url)