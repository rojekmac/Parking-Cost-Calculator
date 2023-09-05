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


def test_parking_lot_selection(driver, parking_lot_options):
    parking_lot_element = driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS)
    parking_lot_element.click()

    parking_lot_select = Select(parking_lot_element)
    available_options = [option.text for option in parking_lot_select.options]

    assert available_options == parking_lot_options, "Parking lot options do not match expected values."


def test_starting_date_field(driver):
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("01/01/1992")
    assert start_date.get_attribute("value") == "01/01/1992", "Start date value doesn't match expected value."


def test_valet_parking(driver):
    parking_lot_element = driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS)
    parking_lot_element.click()
    # short_term_parking = driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING)
    # short_term_parking.click()

    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("01/01/1992")
    assert start_date.get_attribute("value") == "01/01/1992", "Start date value doesn't match expected value."

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("01/01/1992")
    assert leaving_date.get_attribute("value") == "01/01/1992", "Start date value doesn't match expected value."

    submit_button = driver.find_element(*ParkCalcPageLocators.SUBMIT_BUTTON)
    submit_button.click()
    parking_cost = driver.find_element(*ParkCalcPageLocators.PARKING_COST_AMOUNT)
    assert parking_cost.text == "$ 12.00"


def test_short_term_parking(driver):
    driver.find_element(*ParkCalcPageLocators.PARKING_LOT_OPTIONS).click()
    driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING).click()
    start_date = driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD)
    start_date.clear()
    start_date.send_keys("01/01/1992")
    assert start_date.get_attribute("value") == "01/01/1992", "Start date value doesn't match expected value."

    leaving_date = driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
    leaving_date.clear()
    leaving_date.send_keys("01/01/1992")
    assert leaving_date.get_attribute("value") == "01/01/1992", "Start date value doesn't match expected value."

    driver.find_element(*ParkCalcPageLocators.SUBMIT_BUTTON).click()

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

# Asserting visibility of the elements

def test_page_title(driver):
    page_title_element = driver.find_element(*ParkCalcPageLocators.PAGE_TITLE)
    assert page_title_element.text == "PARKING COST CALCULATOR", "Page title doesn't match expected value."


def test_parking_lot_text(driver):
    parking_lot_text = driver.find_elements(*ParkCalcPageLocators.CALCULATOR_BODY)[0]
    assert parking_lot_text.text == "Choose a Parking Lot"


def test_parking_lot_visibility(driver):
    entry_date = driver.find_elements(*ParkCalcPageLocators.CALCULATOR_BODY)[2]
    assert entry_date.text == "Please input entry date and time"


def test_submit_button_text(driver):
    submit_button = driver.find_element(*ParkCalcPageLocators.SUBMIT_BUTTON)
    assert submit_button.get_attribute("value") == "Calculate", "Button text doesn't match expected value."


def test_valet_parking_price(driver):
    valet_parking = driver.find_element(*ParkCalcPageLocators.VALET_ELEMENT_RATE)
    assert valet_parking.text.replace("\n", " ") == "Valet Parking $18 per day $12 for five hours or less"


def test_short_term_parking_price(driver):
    short_term_parking = driver.find_element(*ParkCalcPageLocators.SHORT_TERM_PARKING_RATE)
    assert short_term_parking.text.replace("\n", " ") == (
        "Short-Term (hourly) Parking $2.00 first hour; $1.00 each additional 1/2 "
        "hour $24.00 daily maximum")


def test_calendar_window_opens(driver):
    ParkCalcPageLocators.open_calendar(driver)
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    # Generated current date in the format of "month year" used later in the comparison in the test
    expected_date = datetime.datetime.now().strftime("%B %Y")
    print(" Expected Date:", expected_date)
    assert driver.find_element(*ParkCalcPageLocators.MONTH_AND_YEAR).text == expected_date, "Wrong date displayed"
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def test_calendar_selects_correct_date(driver):
    ParkCalcPageLocators.open_calendar(driver)
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(*ParkCalcPageLocators.FIRST_DAY_OF_A_MONTH).click()
    driver.switch_to.window(driver.window_handles[0])
    assert driver.find_element(*ParkCalcPageLocators.START_DATE_FIELD).get_property("value") == "9/1/2023"
