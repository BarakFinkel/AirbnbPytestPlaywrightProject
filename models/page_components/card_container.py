from typing import List, Callable
from playwright.sync_api import Locator, Page
from models.utilities.helper_methods import extract_price_info, extract_rating_info

CARD_CONTAINER_TEST_ID = "card-container"

class CardContainer:

    def __init__(self, locator: Locator):
        self.container = locator
        self.price = extract_price_info(locator)
        self.rating, self.review_amount = extract_rating_info(locator)

    def click(self):
        self.container.click()

    def is_rated_better(self, other: "CardContainer") -> bool:
        """
        A comparator method that checks if this card is rated better than another card.
        :param other: The other CardContainer being compared.
        :return: True or False
        """
        return self.rating > other.rating or (self.rating == other.rating and self.review_amount > other.review_amount)

    def is_lower_priced(self: "CardContainer", other: "CardContainer") -> bool:
        """
        A comparator method that checks if this card is priced lower than another card.
        :param other: The other CardContainer being compared.
        :return: True or False
        """
        return self.price < other.price

    def print_card_details(self):
        print(f"* Price: {self.price}")
        print(f"* Rating: {self.rating}")
        print(f"* Review Amount: {self.review_amount}")

def extract_highest_rated_card(page: Page) -> tuple[str, int]:
    return extract_best_card(page, lambda a, b: a.is_rated_better(b))

def extract_lowest_priced_card(page: Page) -> tuple[str, int]:
    return extract_best_card(page, lambda a, b: a.is_lower_priced(b))

def extract_best_card(
    page: Page,
    is_better: Callable[[CardContainer, CardContainer], bool]
) -> tuple[str, int]:
    """
    Traverses paginated results and returns the URL and index of the best card
    according to the provided comparator.
    :param page: The starting page of the comparison.
    :param is_better: The comparator method.
    :return: The best card's page url and locator index.
    """
    best_url = ""
    best_index = -1
    best_card = None
    pager_counter = 1

    while True:
        # Tries to find any card container in the page, will break the loop if fails.
        try:
            page.get_by_test_id(CARD_CONTAINER_TEST_ID).first.wait_for(state="visible", timeout=5000)
        except TimeoutError:
            print("No cards loaded on this page.")
            break

        # 1 sec wait for the rest of the card containers to potentially load.
        page.wait_for_timeout(1000)

        # Get all visible card locators
        card_locators = page.get_by_test_id(CARD_CONTAINER_TEST_ID).all()
        card_containers = []
        count = 0

        # Construct card-container objects for each card-container location.
        for locator in card_locators:
            card = CardContainer(locator)
            card_containers.append(card)
            page.wait_for_timeout(100)
            count += 1

        # Get the best card in the current page's list.
        current_best_index = best_card_in_list(card_containers, is_better)
        current_best_card = card_containers[current_best_index]

        # If the current page's best card is better than the overall best card, we store its info as the new best card.
        if best_card is None or is_better(current_best_card, best_card):
            best_card = current_best_card
            best_index = current_best_index
            best_url = page.url

        # Move on to the next results page if it exists, or end the loop if we're done.
        next_button = page.get_by_role("link", name="Next")
        if not next_button.is_visible() or next_button.is_disabled(): break
        next_button.click()

    return best_url, best_index

def best_card_in_list(
        card_containers: List[CardContainer],
        is_better: Callable[["CardContainer", "CardContainer"], bool] ) -> int:
    """
    Extracts the best card from a list of cards, based on a given comparator.
    :param card_containers: The list of cards.
    :param is_better: The comparator method.
    :return: The best card according to the comparator.
    """
    # If the list is empty, raise a value error.
    if not card_containers:
        raise ValueError("No card containers found")

    best_index = 0

    # Iterate through the list, and save the index of the best card in it.
    for index, card in enumerate(card_containers[1:], start=1):
        if is_better(card, card_containers[best_index]):
            best_index = index

    return best_index
