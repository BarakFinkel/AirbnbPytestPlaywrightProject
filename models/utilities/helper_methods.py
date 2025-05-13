import re
from playwright.sync_api import Locator, Page
from datetime import date, datetime

# _________________ General Locator Helper Methods _________________ #

def get_locator_containing(page: Page, attribute : str, text : str) -> Locator:
    return page.locator(f'[{attribute}*="{text}"]')

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
        rating_locator.wait_for(state="visible", timeout=2000)    # Small wait window for getting the element
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
        price_locator.wait_for(state="visible", timeout=2000)
        price_texts = price_locator.text_content().split(" ")  # Get matching text and parse by " "
        return int(remove_non_alphanumeric_and_dot(price_texts[0]))
    except Exception:
        return 10**18 # Returning big value in case of an exception being thrown.

# ___________________ Results Page Helper Methods ___________________ #

def increment_n_times(button: Locator, n : int) -> None:
    for i in range(n):
        button.click()

# _____________________ DateTime Helper Methods _____________________ #

def format_date_range(start: date, end: date) -> str:
    # If it's within the same month - write days adjacently
    if start.month == end.month and start.year == end.year:
        return f"{start.strftime('%B')} {start.day}-{end.day}"
    else: # Specify both months
        return f"{start.strftime('%b %d')} - {end.strftime('%b %d')}"

def convert_date_string_format(date_str: str) -> str:
    """
    Converts a string from format: "12, Monday, May 2025[...]"
    to format: "5/12/2025"
    :param date_str: The date string to convert.
    :return: Formatted %d/%m/%Y date string.
    """
    # Split by commas and
    parts = date_str.split(" ")
    day   = remove_non_alphanumeric(parts[0])
    month = remove_non_alphanumeric(parts[2])
    year  = remove_non_alphanumeric(parts[3])

    # Construct the full date string
    cleaned_str = f"{day} {month} {year}"

    # Parse and format
    date_obj = datetime.strptime(cleaned_str, "%d %B %Y")
    formatted_date_obj = date_obj.strftime("%m/%d/%Y").replace("/0", "/")

    if formatted_date_obj.startswith('0'):
        formatted_date_obj = formatted_date_obj[1:]

    return formatted_date_obj

def remove_non_alphanumeric(text: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '', text)

def remove_non_alphanumeric_and_dot(text: str) -> str:
    return re.sub(r'[^a-zA-Z0-9.]', '', text)