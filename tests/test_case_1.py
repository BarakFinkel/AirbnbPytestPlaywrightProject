from playwright.sync_api import Page, expect
from models.page_objects.main_page import MainPage
from models.page_components.card_container import CardContainer, extract_highest_rated_card, extract_lowest_priced_card
from datetime import date

def test_case_1(page: Page):

    # Step 1: Open airbnb.com
    page.goto("https://www.airbnb.com/?locale=en")
    main_page = MainPage(page, page.url)

    # Step 2: Search the desired vacation details.
    main_page.search_preferences("Tel Aviv-Yafo", date(2025, 5, 12), date(2025, 5, 13), num_of_adults=2)
    page.wait_for_timeout(2000)

    first_results_page_url = page.url

    '''
    # Step 3: Find the highest-rated result.
    highest_rated_url, highest_rated_index = extract_highest_rated_card(page)
    page.goto(highest_rated_url)
    best_rated_card_container = CardContainer(page.get_by_test_id("card-container").nth(highest_rated_index))
    print(
        f"Best Rating Result: {best_rated_card_container.rating},\n"
        f"was reviewed by {best_rated_card_container.review_amount} customers.\n"
        f"Found as result no. {highest_rated_index + 1} on {page.url}\n\n"
    )
    
    page.goto(first_results_page_url)
    '''

    # Step 4: Find the lowest-priced result.
    lowest_priced_url, lowest_priced_index = extract_lowest_priced_card(page)
    page.goto(lowest_priced_url)
    best_priced_card_container = CardContainer(page.get_by_test_id("card-container").nth(lowest_priced_index))

    print(f"Best Price Result:")
    best_priced_card_container.print_card_details()
    print(f"Found as result no. {lowest_priced_index + 1} on {page.url}\n")
