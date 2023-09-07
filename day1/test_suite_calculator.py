import pytest
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from test_parking_lot_data import ParkingLotData
from selenium.webdriver.support.ui import Select  # Import Select class
# from selenium.webdriver.common.by import By
from locators import ParkCalcPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime


@pytest.fixture(scope="module")
def driver():
    chromedriver_path = r"C:\Drivers\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    chrome_options = Options()
    chrome_service = Service(executable_path=chromedriver_path)
    driver = WebDriver(service=chrome_service, options=chrome_options)
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def setup(driver):
    driver.get("https://www.shino.de/parkcalc/")


@pytest.fixture(scope="module")
def parking_lot_options():  # Define the parking_lot_options fixture
    return ParkingLotData().get_parking_lots()


# Asserting visibility of the elements

@pytest.mark.sanity_suite
def test_page_title_is_visible(driver):
    page_title_element = driver.find_element(*ParkCalcPageLocators.PAGE_TITLE)
    assert page_title_element.text == "PARKING COST CALCULATOR"


@pytest.mark.sanity_suite
def test_parking_lot_text_is_visible(driver):
    parking_lot_text = driver.find_elements(*ParkCalcPageLocators.CALCULATOR_BODY)[0]
    assert parking_lot_text.text == "Choose a Parking Lot"


@pytest.mark.sanity_suite
def test_parking_options_are_visible(driver):
    parking_lot_options = driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS)
    assert parking_lot_options.get_attribute("outerText").replace("\n", " ") == (
        'Valet Parking Short-Term Parking Economy Parking Long-Term Garage Parking '
        'Long-Term Surface Parking')


@pytest.mark.sanity_suite
def test_parking_lot_visibility(driver):
    entry_date = driver.find_elements(*ParkCalcPageLocators.CALCULATOR_BODY)[2]
    assert entry_date.text == "Please input entry date and time"


@pytest.mark.sanity_suite
def test_calendar_icon_visibility(driver):
    calendar_icon = driver.find_element(*ParkCalcPageLocators.ENTRY_CALENDAR_ICON)
    assert calendar_icon.is_displayed()


@pytest.mark.sanity_suite
def test_calculate_button_text_visibility(driver):
    submit_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    assert submit_button.get_attribute("value") == "Calculate"


@pytest.mark.sanity_suite
def test_valet_parking_price_visibility(driver):
    valet_parking = driver.find_element(*ParkCalcPageLocators.VALET_ELEMENT_RATE)
    assert valet_parking.text.replace("\n", " ") == "Valet Parking $18 per day $12 for five hours or less"


@pytest.mark.sanity_suite
def test_short_term_parking_price_visibility(driver):
    short_term_parking = driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING_RATE)
    assert short_term_parking.text.replace("\n", " ") == (
        "Short-Term (hourly) Parking $2.00 first hour; $1.00 each additional 1/2 "
        "hour $24.00 daily maximum")


@pytest.mark.sanity_suite
def test_long_term_parking_price_visibility(driver):
    short_term_parking = driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING_RATE)
    assert short_term_parking.text.replace("\n", " ") == (
        "Long-Term Garage Parking $2.00 per hour $12.00 daily maximum $72.00 per week (7th day free)")


@pytest.mark.sanity_suite
def test_surface_parking_price_visibility(driver):
    short_term_parking = driver.find_element(*ParkCalcPageLocators.SURFACE_PARKING_RATE)
    assert short_term_parking.text.replace("\n", " ") == (
        "Long-Term Surface Parking (North Lot) $2.00 per hour $10.00 daily maximum $60.00 per week (7th day free)")


@pytest.mark.sanity_suite
def test_economy_lot_price_visibility(driver):
    short_term_parking = driver.find_element(*ParkCalcPageLocators.ECONOMY_LOT_PARKING_RATE)
    assert short_term_parking.text.replace("\n", " ") == (
        "Economy Lot Parking $2.00 per hour $9.00 daily maximum $54.00 per week (7th day free)")


@pytest.mark.sanity_suite
def test_lost_ticket_field_visibility(driver):
    short_term_parking = driver.find_element(*ParkCalcPageLocators.LOST_TICKET_FIELD)
    assert short_term_parking.text == (
        "A Lost Ticket Fee of $10.00 will be assessed when the original parking stub cannot be produced when exiting "
        "the parking facilities (does not apply to Valet Parking).")


# Looping through the parking options to check if all options are visible
@pytest.mark.sanity_suite
def test_parking_lot_selection(driver, parking_lot_options):
    parking_lot_element = driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS)
    parking_lot_element.click()

    parking_lot_select = Select(parking_lot_element)
    available_options = [option.text for option in parking_lot_select.options]

    assert available_options == parking_lot_options, "Parking lot options do not match expected values."


# Looping through the parking options to check if all options are visible
def test_parking_lot_selection(driver, parking_lot_options):
    parking_lot_element = driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS)
    parking_lot_element.click()

    parking_lot_select = Select(parking_lot_element)
    available_options = [option.text for option in parking_lot_select.options]

    assert available_options == parking_lot_options, "Parking lot options do not match expected values."


# Valet Parking Functional Tests

def test_valet_parking_equal_5h(driver):
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/1992")
    assert start_date.get_attribute("value") == "09/01/1992"

    start_date = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_date.clear()
    start_date.send_keys("12:00")
    assert start_date.get_attribute("value") == "12:00"

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/01/1992")
    assert leaving_date.get_attribute("value") == "09/01/1992"

    start_date = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    start_date.clear()
    start_date.send_keys("12:00")
    assert start_date.get_attribute("value") == "12:00"

    submit_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    submit_button.click()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 12.00"


def test_valet_parking_less_than_5h(driver):
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("11:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/01/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("14:00")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 12.00"


def test_valet_parking_more_than_5h_less_than_1d(driver):
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("12:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/01/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("19:00")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 18.00"


def test_valet_parking_for_1d(driver):
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("12:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/02/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("12:00")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 18.00"


def test_valet_parking_multiple_days(driver):
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("12:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/02/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("15:00")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 36.00"


def test_valet_parking_no_parking(driver):
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/01/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("10:00")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 0.00"


# Short Term Parking Functional Tests

def test_short_term_parking_1_hour(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()

    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:40")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/01/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("11:40")

    submit_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    submit_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 2.00"


def test_short_term_parking_1_2_hours(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()

    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/01/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("11:12")

    submit_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    submit_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 3.00"


def test_short_term_parking_1_7_hours(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()

    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/01/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("11:42")

    submit_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    submit_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 4.00"


def test_short_term_parking_24_hours(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()

    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/02/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("10:00")

    submit_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    submit_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 24.00"


def test_short_term_parking_25_hours(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()

    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/02/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("11:00")

    submit_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    submit_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 26.00"


def test_short_term_parking_no_parking(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()

    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/01/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("10:00")

    submit_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    submit_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 0.00"


# BVA TESTS
def test_short_term_boundary_additional_halfhour(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/01/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("11:29")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 3.00"


def test_short_term_boundary_additional_hour(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/01/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("11:30")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 3.00"


def test_short_term_boundary_daily_maximum(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/02/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("09:59")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 24.00"


def test_short_term_boundary_daily_maximum_exact(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/02/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("10:00")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 24.00"


def test_short_term_boundary_after_daily_maximum(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/02/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("10:01")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 25.00"


# Long-term Garage Parking

def test_long_term_1_hour(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/01/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("11:00")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text


def test_long_term_6_hours(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/01/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("16:00")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 12.00"


def test_long_term_24_hours(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/02/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("10:00")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 12.00"


def test_long_term_30_hours(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("09/01/2023")

    start_time = driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
    start_time.clear()
    start_time.send_keys("10:00")

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("09/02/2023")

    leaving_time = driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
    leaving_time.clear()
    leaving_time.send_keys("16:00")

    calculate_button = driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
    calculate_button.click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 24.00"


# EXAMPLE
def test_short_term_parking(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("01/01/1992")
    assert start_date.get_attribute("value") == "01/01/1992"

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("01/01/1992")
    assert leaving_date.get_attribute("value") == "01/01/1992"

    driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON).click()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text.split(' ')[1] == "2.00"


# def test_valet_parking_visibility(driver):
#     valet_parking = driver.find_element_by_xpath("//a[@name='Valet']")
#     assert valet_parking.is_displayed()
#
#
# def test_valet_parking_price_visibility(driver):
#     price = driver.find_element_by_xpath("//p[contains(text(),'$18 per day')]")
#     assert price.is_displayed()


def test_entry_calendar_window_opens(driver):
    ParkCalcPageLocators.open_entry_calendar(driver)
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    # Generated current date in the format of "month year" used later in the comparison in the test
    expected_date = datetime.datetime.now().strftime("%B %Y")
    print(" Expected Date:", expected_date)
    assert driver.find_element(*ParkCalcPageLocators.MONTH_AND_YEAR).text == expected_date, "Wrong date displayed"
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def test_entry_calendar_selects_correct_date(driver):
    assert driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD).get_property("value") == "MM/DD/YYYY"
    ParkCalcPageLocators.open_entry_calendar(driver)
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(*ParkCalcPageLocators.FIRST_DAY_OF_A_MONTH).click()
    driver.switch_to.window(driver.window_handles[0])
    assert driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD).get_property("value") == "9/1/2023"


def test_leaving_calendar_opens(driver):
    assert driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD).get_property("value") == "MM/DD/YYYY"
    ParkCalcPageLocators.open_leaving_calendar(driver)
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(*ParkCalcPageLocators.FIRST_DAY_OF_A_MONTH).click()
    driver.switch_to.window(driver.window_handles[0])
    assert driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD).get_property("value") == "9/1/2023"
