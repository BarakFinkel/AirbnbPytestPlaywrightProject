import pytest
from playwright.sync_api import Page
from models.page_objects.main_page import MainPage
from models.page_objects.results_page import ResultsPage
from models.page_objects.overview_page import OverviewPage
from models.page_objects.reservation_page.reservation_page import ReservationPage
from models.page_objects.reservation_page.reservation_page_factory import create_reservation_page
from datetime import timedelta, date

test_data = [
    # Format:
    # (<destination> , <start-date> , <end-date> , <adults-num> , <children-num> , <infants-num> , <pets-num> , <prefix w/o '+'> , <9-digit-phone-number>),
    ("Tel Aviv-Yafo", date.today(), date.today() + timedelta(days=1), 2, 0, 0, 0, 93, 123456789),
]

@pytest.mark.parametrize("destination, start_date, end_date, adults, children, infants, pets, prefix, phone", test_data)
def test_case_1(page: Page, destination : str, start_date : date, end_date : date, adults : int, children : int, infants : int, pets : int, prefix : int, phone : int):
    # Step 1: Open airbnb.com
    page.goto("https://www.airbnb.com/homes?locale=en")
    main_page = MainPage(page, page.url)

    # Step 2: Search the desired vacation details.
    main_page.search_preferences(destination, start_date, end_date, adults, children, infants, pets)
    page.wait_for_timeout(2000)

    # Step 3: Validate Search According To Preferences.
    results_page = ResultsPage(page, page.url)
    results_page.assert_preferences(destination, start_date, end_date, adults, children, infants, pets)

    # Step 3: Find and print the highest-rated result.
    results_page.extract_highest_rated_card(print_result=True)

    # Step 4: Find and print the lowest-rated result.
    results_page.extract_lowest_priced_card(print_result=True)

@pytest.mark.parametrize("destination, start_date, end_date, adults, children, infants, pets, prefix, phone", test_data)
def test_case_2(page: Page, destination : str, start_date : date, end_date : date, adults : int, children : int, infants : int, pets : int, prefix : int, phone : int):
    # Step 1: Open airbnb.com
    page.goto("https://www.airbnb.com/homes?locale=en")
    main_page = MainPage(page, page.url)

    # Step 2: Search the desired vacation details.
    main_page.search_preferences(destination, start_date, end_date, adults, children, infants, pets)
    # page.wait_for_timeout(2000)

    # Step 3: Validate Search According To Preferences.
    results_page = ResultsPage(page, page.url)
    results_page.assert_preferences(destination, start_date, end_date, adults, children, infants, pets)

    # Step 3: Find and print the highest-rated result.
    best_result_url = results_page.extract_highest_rated_card(print_result=True)

    # Step 4: Go to the best result's overview page:
    page.goto(best_result_url)
    # page.wait_for_timeout(3000)

    # Step 5: Go over the reservation's overview page, save and print its details.
    overview_page = OverviewPage(page, page.url)
    o_check_in_date, o_check_out_date, o_guests, o_price = overview_page.get_all_details()
    overview_page.print_details()

    # Step 6: Click the reserve button, validate reservation details, and enter a phone number.
    overview_page.click_reserve()
    # page.wait_for_timeout(3000)
    reservation_page = ReservationPage(page, page.url)
    r_check_in_date, r_check_out_date, r_guests, r_price = reservation_page.get_all_details()

    assert o_check_in_date   == r_check_in_date
    assert o_check_out_date  == r_check_out_date
    assert o_price           == r_price
    for key in o_guests:
        assert o_guests[key] == r_guests[key]

    reservation_page.input_phone_number(prefix, phone)

def test_case_3(page: Page):
    page.goto("https://www.airbnb.com/rooms/699210620444564680?adults=2&check_in=2025-05-21&check_out=2025-05-23&guests=2&search_mode=regular_search&source_impression_id=p3_1747174043_P3ETn4ssilkqp1NU&previous_page_section_name=1000&federated_search_id=d1feb4dd-a84e-408e-a73d-b4e55cdce338&locale=en")

    # Step 5: Go over the reservation's overview page, save and print its details.
    overview_page = OverviewPage(page, page.url)
    o_check_in_date, o_check_out_date, o_guests, o_price = overview_page.get_all_details()
    overview_page.print_details()

    # Step 6: Click the reserve button, validate reservation details, and enter a phone number.
    overview_page.click_reserve()
    reservation_page = create_reservation_page(page, page.url)
    r_check_in_date, r_check_out_date, r_guests, r_price = reservation_page.get_all_details()

    assert o_check_in_date   == r_check_in_date
    assert o_check_out_date  == r_check_out_date
    assert o_price           == r_price
    for key in o_guests:
        assert o_guests[key] == r_guests[key]

    reservation_page.input_phone_number(93, 123456789)
