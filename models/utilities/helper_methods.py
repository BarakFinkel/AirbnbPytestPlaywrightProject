import math

from playwright.sync_api import Locator

# __________________ Card Container Helper Methods __________________ #

RATING_CONTAINED_TEXT = "out of 5 average rating"
PRICE_CONTAINED_TEXT  = "per night"

def extract_rating_info(locator : Locator) -> tuple[float, int]:
    """
    A method to extract rating information from a locator pointing to a card container.
    :param locator: The locator to extract information from.
    :return: The rating and amount of reviewers.
    """
    try:
        rating_locator = locator.get_by_text(RATING_CONTAINED_TEXT, exact=False)
        rating_locator.wait_for(state="visible", timeout=200)    # Small wait window for getting the element
        text_content = rating_locator.text_content().split(" ")  # Parse the text in the element by " "
        return float(text_content[0]), int(text_content[-2])     # Return the rating and amount of reviewers
    except Exception:
        return 0.0, 0

def extract_price_info(locator : Locator) -> int:
    """
    A method to extract price information from a locator pointing to a card container.
    :param locator: The locator to extract information from.
    :return: The price.
    """
    try:
        price_locator = locator.get_by_test_id("price-availability-row").get_by_text(PRICE_CONTAINED_TEXT, exact=False)
        price_locator.wait_for(state="visible", timeout=200)
        price_texts = price_locator.text_content().split(" ")  # Get matching text and parse by " "
        price_text = price_texts[0][1:]                        # Get first queried text and remove its payment symbol char.
        cleaned = price_text.replace(",", "")      # Remove , separator
        return int(cleaned)
    except Exception:
        return 10**18