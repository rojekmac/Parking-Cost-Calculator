import pytest
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from test_parking_lot_data import ParkingLotData
from selenium.webdriver.support.ui import Select  # Import Select class
# from selenium.webdriver.common.by import By
from locators import ParkCalcPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from park_calc_page import ParkCalcPage
from selenium.webdriver.support import expected_conditions as EC
import datetime


@pytest.fixture(scope="module")
def driver():
    chromedriver_path = r"C:\Drivers\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    chrome_options = Options()
    chrome_service = Service(executable_path=chromedriver_path)
    driver = WebDriver(service=chrome_service, options=chrome_options)
    yield driver


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


# Valet Parking Functional Tests

@pytest.mark.functional_tests
def test_valet_parking_equal_5h(driver):
    park_calc_page = ParkCalcPage(driver)
    park_calc_page.set_starting_date("09/01/1992")
    park_calc_page.set_starting_time("12:00")
    park_calc_page.set_leaving_date("09/01/1992")
    park_calc_page.set_leaving_time("12:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 12.00"


@pytest.mark.functional_tests
def test_valet_parking_less_than_5h(driver):
    park_calc_page = ParkCalcPage(driver)
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("11:00")
    park_calc_page.set_leaving_date("09/01/2023")
    park_calc_page.set_leaving_time("14:00")

    park_calc_page.submit_button()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 12.00"


@pytest.mark.functional_tests
def test_valet_parking_more_than_5h_less_than_1d(driver):
    park_calc_page = ParkCalcPage(driver)
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("12:00")
    park_calc_page.set_leaving_date("09/01/2023")
    park_calc_page.set_leaving_time("19:00")

    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 18.00"


@pytest.mark.functional_tests
def test_valet_parking_for_1d(driver):
    park_calc_page = ParkCalcPage(driver)
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("12:00")
    park_calc_page.set_leaving_date("09/02/2023")
    park_calc_page.set_leaving_time("12:00")

    park_calc_page.submit_button()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 18.00"


@pytest.mark.functional_tests
def test_valet_parking_multiple_days(driver):
    park_calc_page = ParkCalcPage(driver)
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("12:00")
    park_calc_page.set_leaving_date("09/02/2023")
    park_calc_page.set_leaving_time("15:00")

    park_calc_page.submit_button()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 36.00"


@pytest.mark.functional_tests
def test_valet_parking_no_parking(driver):
    park_calc_page = ParkCalcPage(driver)
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("09/01/2023")
    park_calc_page.set_leaving_time("10:00")

    park_calc_page.submit_button()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 0.00"


# Short Term Parking Functional Tests
@pytest.mark.functional_tests
def test_short_term_parking_1_hour(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("10:40")
    park_calc_page.set_leaving_date("09/01/2023")
    park_calc_page.set_leaving_time("11:40")

    park_calc_page.submit_button()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 2.00"


@pytest.mark.functional_tests
def test_short_term_parking_1_2_hours(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("09/01/2023")
    park_calc_page.set_leaving_time("11:12")

    park_calc_page.submit_button()

    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 3.00"


@pytest.mark.functional_tests
def test_short_term_parking_1_7_hours(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("09/01/2023")
    park_calc_page.set_leaving_time("11:42")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 4.00"


@pytest.mark.functional_tests
def test_short_term_parking_24_hours(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("09/02/2023")
    park_calc_page.set_leaving_time("10:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 24.00"


@pytest.mark.functional_tests
def test_short_term_parking_25_hours(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    park_calc_page.set_starting_date("09/02/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("09/03/2023")
    park_calc_page.set_leaving_time("11:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 26.00"


@pytest.mark.functional_tests
def test_short_term_parking_no_parking(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("09/01/2023")
    park_calc_page.set_leaving_time("10:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 0.00"


@pytest.mark.BVA_tests
# BVA TESTS
def test_short_term_boundary_additional_halfhour(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("09/01/2023")
    park_calc_page.set_leaving_time("11:29")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 3.00"


@pytest.mark.BVA_tests
def test_short_term_boundary_additional_hour(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("09/01/2023")
    park_calc_page.set_leaving_time("11:30")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 3.00"


@pytest.mark.BVA_tests
def test_short_term_boundary_daily_maximum(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("09/02/2023")
    park_calc_page.set_leaving_time("09:59")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 24.00"


@pytest.mark.BVA_tests
def test_short_term_boundary_daily_maximum_exact(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("09/02/2023")
    park_calc_page.set_leaving_time("10:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 24.00"


@pytest.mark.BVA_tests
def test_short_term_boundary_after_daily_maximum(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    park_calc_page.set_starting_date("09/01/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("09/02/2023")
    park_calc_page.set_leaving_time("10:01")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 25.00"


# Long-term Garage Parking
@pytest.mark.functional_tests
def test_long_parking_for_2_hours(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    park_calc_page.set_starting_date("01/20/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("01/20/2023")
    park_calc_page.set_leaving_time("12:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 4.00"


@pytest.mark.functional_tests
def test_long_parking_for_5_hours(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    park_calc_page.set_starting_date("01/20/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("01/20/2023")
    park_calc_page.set_leaving_time("15:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 10.00"


@pytest.mark.functional_tests
def test_long_parking_for_a_day(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    park_calc_page.set_starting_date("01/20/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("01/21/2023")
    park_calc_page.set_leaving_time("10:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 12.00"


@pytest.mark.functional_tests
def test_long_parking_for_a_week(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    park_calc_page.set_starting_date("01/20/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("01/27/2023")
    park_calc_page.set_leaving_time("10:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 72.00"


@pytest.mark.functional_tests
def test_long_parking_for_a_week_with_extra_day(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    park_calc_page.set_starting_date("01/20/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("01/28/2023")
    park_calc_page.set_leaving_time("10:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 84.00"


@pytest.mark.functional_tests
def test_long_parking_for_4_days(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    park_calc_page.set_starting_date("01/20/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("01/24/2023")
    park_calc_page.set_leaving_time("10:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 48.00"


@pytest.mark.functional_tests
def test_long_parking_for_less_than_an_hour(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    park_calc_page.set_starting_date("01/20/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("01/20/2023")
    park_calc_page.set_leaving_time("10:30")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 2.00"


@pytest.mark.functional_tests
def test_long_parking_for_exact_week_but_not_a_whole_day_on_7th(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    park_calc_page.set_starting_date("01/20/2023")
    park_calc_page.set_starting_time("11:00")
    park_calc_page.set_leaving_date("01/27/2023")
    park_calc_page.set_leaving_time("09:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 72.00"


@pytest.mark.functional_tests
def test_long_parking_for_additional_hours_over_weekly_maximum(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    park_calc_page.set_starting_date("01/20/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("01/27/2023")
    park_calc_page.set_leaving_time("14:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 80.00"


@pytest.mark.functional_tests
def test_parking_for_multiple_weeks(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    park_calc_page.set_starting_date("01/20/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("02/03/2023")
    park_calc_page.set_leaving_time("10:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 144.00"


@pytest.mark.functional_tests
def test_half_day_parking(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    park_calc_page.set_starting_date("01/20/2023")
    park_calc_page.set_starting_time("08:00")
    park_calc_page.set_leaving_date("01/20/2023")
    park_calc_page.set_leaving_time("14:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 12.00"


@pytest.mark.functional_tests
def test_one_and_a_half_day_parking(driver):
    park_calc_page = ParkCalcPage(driver)
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.LONG_TERM_PARKING).click()
    park_calc_page.set_starting_date("01/20/2023")
    park_calc_page.set_starting_time("10:00")
    park_calc_page.set_leaving_date("01/21/2023")
    park_calc_page.set_leaving_time("14:00")
    park_calc_page.submit_button()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 20.00"


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
    assert driver.find_element(*ParkCalcPageLocators.STARTING_DATE_FIELD).get_property("value") == "MM/DD/YYYY"
    ParkCalcPageLocators.open_entry_calendar(driver)
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(*ParkCalcPageLocators.FIRST_DAY_OF_A_MONTH).click()
    driver.switch_to.window(driver.window_handles[0])
    assert driver.find_element(*ParkCalcPageLocators.STARTING_DATE_FIELD).get_property("value") == "9/1/2023"


def test_leaving_calendar_opens(driver):
    assert driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD).get_property("value") == "MM/DD/YYYY"
    ParkCalcPageLocators.open_leaving_calendar(driver)
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(*ParkCalcPageLocators.FIRST_DAY_OF_A_MONTH).click()
    driver.switch_to.window(driver.window_handles[0])
    assert driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD).get_property("value") == "9/1/2023"
