from typing import List, Callable
from playwright.sync_api import Locator, Page
from models.utilities.helper_methods import extract_price_info, extract_rating_info

class CardContainer:

    def __init__(self, locator: Locator):
        self.container = locator
        self.price = extract_price_info(locator)
        self.rating, self.review_amount = extract_rating_info(locator)
        temp_container = self.container.locator('a').first
        temp_container.wait_for(state='visible')
        self.url = temp_container.get_attribute("href")

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
