# Airbnb Automated Testing Project

This project is an automated UI testing framework for Airbnb, built using **Playwright** in Python. It uses the **Page Object Model (POM)** architecture to ensure scalability and maintainability.

---

## Project Structure

```
.
├── models  
│   ├── page_objects
│   │   ├── base_page.py
│   │   ├── main_page.py
│   │   ├── results_page.py
│   │   ├── overview_page.py
│   │   └── reservation_page
│   │       ├── reservation_page.py
│   │       ├── reservation_page_a.py
│   │       ├── reservation_page_b.py
│   │       └── reservation_page_factory.py
│   ├── page_components
│   │   ├── search_bar.py
│   │   └── card_container.py
│   └── utilities
│       └── helper_methods.py
├── tests
│   └── test.py
├── pytest.ini
├── README.md
└── requirements.txt
```

---

## Tech & Frameworks

* **Language**: Python
* **Testing Framework**: Playwright
* **Design Pattern**: Page Object Model (POM)

---

## Features Tested

- Performing a search with given parameters (location, date range, guests).
- Asserting results match search preferences.
- Extracting and printing:
  - Highest-rated result
  - Lowest-priced result
- Verifying page and reservation data.
- Filling reservation details including e.g phone number.

---

## Page Object Model Structure

### Pages:

* **BasePage**: Shared navigation functionality for all pages.
* **MainPage**: Entry to and execution of the search feature.
* **ResultsPage**: Assertions of main page search details & extraction of 'best' result available.
* **OverviewPage**: Displays details of a selected listing.
* **ReservationPage**: Booking and checkout UI elements. Has a base class, 2 sub-classes, and a factory that constructs one of the sub-classes according to the page's properties.

### Components:

* **SearchBar**: Encapsulation of search bar behavior (destination, dates, guests).
* **CardContainer**: Handle of individual result cards and their data (price, rating, etc).

---

## Helper Methods

Custom utility methods for:

* Converting and formatting strings and dates
* Extracting attributes
* Locating elements based on partial attribute matches

---

## Installation & Run Instructions

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run all tests via terminal**:

   ```bash
   pytest
   ```

3. **Run specific test**:

   ```bash
   pytest tests/tests.py::test_case_1
   pytest tests/tests.py::test_case_2
   ```
---

## Adding More Test Examples

Test data is passed using pytest.mark.parametrize, and defined in a list of tuples in test/tests.py .
each tuple should match the format:

   ```python
   # (<destination>, <start-date>, <end-date>, <adults>, <children>, <infants>, <pets>, <prefix>, <9-digit-phone>)
   ```
### Example:

   ```python
    ("Tel Aviv-Yafo", date(2025, 5, 13), date(2025, 5, 14), 2, 0, 0, 0, 972, 123456789)
   ```
