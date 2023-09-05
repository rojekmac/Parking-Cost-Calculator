from selenium.webdriver.common.by import By


class ParkCalcPageLocators(object):
    SUBMIT_BUTTON = (By.NAME, "Submit")
    PAGE_TITLE = (By.CLASS_NAME, "PageTitle")
    PARKING_LOT_OPTIONS = (By.ID, "ParkingLot")
    START_DATE_FIELD = (By.ID, "StartingDate")
    LEAVING_DATE_FIELD = (By.ID, "LeavingDate")
    VALET_ELEMENT = (By.XPATH, "//strong[a/@name='Valet']")
    CALCULATOR_BODY = (By.CLASS_NAME, "BodyCopy")
    SHORT_TERM_PARKING = (By.CSS_SELECTOR, "[value='Short']")
    PARKING_COST_AMOUNT = (By.CSS_SELECTOR, "[class='SubHead'] b")
    VALET_ELEMENT_RATE = (By.CSS_SELECTOR, "body > p:nth-child(4)")
    SHORT_TERM_PARKING_RATE = (By.CSS_SELECTOR, "body > p:nth-child(5)")
    CALENDAR_ICON = (By.XPATH, "//img[@alt='Pick a date']")
    MONTH_AND_YEAR = (By.CSS_SELECTOR, "body > form > table > tbody > tr:nth-child(2) > td > font > b")
    FIRST_DAY_OF_A_MONTH = (By.XPATH, "//a[text() = '1']")

    @staticmethod
    def open_calendar(driver):
        (driver.find_element(*ParkCalcPageLocators.CALENDAR_ICON).click())

    @staticmethod
    def select_first_day(driver):
        (driver.find_element(*ParkCalcPageLocators.FIRST_DAY_OF_A_MONTH).click())
