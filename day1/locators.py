from selenium.webdriver.common.by import By


class ParkCalcPageLocators(object):
    CALCULATE_BUTTON = (By.NAME, "Submit")
    PAGE_TITLE = (By.CLASS_NAME, "PageTitle")
    PARKING_LOT_OPTIONS = (By.ID, "ParkingLot")
    STARTING_DATE_FIELD = (By.ID, "StartingDate")
    LEAVING_DATE_FIELD = (By.ID, "LeavingDate")
    VALET_ELEMENT = (By.XPATH, "//strong[a/@name='Valet']")
    CALCULATOR_BODY = (By.CLASS_NAME, "BodyCopy")
    SHORT_TERM_PARKING = (By.CSS_SELECTOR, "[value='Short']")
    LONG_TERM_PARKING = (By.CSS_SELECTOR, "[value='Long-Garage']")
    SURFACE_PARKING = (By.CSS_SELECTOR, "[value='Long-Surface']")
    PARKING_COST_AMOUNT = (By.CSS_SELECTOR, "[class='SubHead'] b")
    VALET_ELEMENT_RATE = (By.CSS_SELECTOR, "body > p:nth-child(4)")
    SHORT_TERM_PARKING_RATE = (By.CSS_SELECTOR, "body > p:nth-child(5)")
    LONG_TERM_PARKING_RATE = (By.CSS_SELECTOR, "body > p:nth-child(6)")
    SURFACE_PARKING_RATE = (By.CSS_SELECTOR, "body > p:nth-child(7)")
    ECONOMY_LOT_PARKING_RATE = (By.CSS_SELECTOR, "body > p:nth-child(8)")
    ENTRY_CALENDAR_ICON = (By.XPATH, "//img[@alt='Pick a date']")
    MONTH_AND_YEAR = (By.CSS_SELECTOR, "body > form > table > tbody > tr:nth-child(2) > td > font > b")
    FIRST_DAY_OF_A_MONTH = (By.XPATH, "//a[text() = '1']")
    STARTING_DATE_AM_BUTTON = (By.CSS_SELECTOR, "[name='StartingTimeAMPM'][value='AM']")
    STARTING_DATE_PM_BUTTON = (By.CSS_SELECTOR, "[name='StartingTimeAMPM'][value='PM']")
    LEAVING_DATE_AM_BUTTON = (By.CSS_SELECTOR, "[name='LeavingTimeAMPM'][value='AM']")
    LEAVING_DATE_PM_BUTTON = (By.CSS_SELECTOR, "[name='LeavingTimeAMPM'][value='PM']")
    LOST_TICKET_FIELD = (By.CSS_SELECTOR, "body i")
    STARTING_TIME_FIELD = (By.CSS_SELECTOR, "[name='StartingTime']")
    LEAVING_TIME_FIELD = (By.CSS_SELECTOR, "[name='LeavingTime']")

    @staticmethod
    def open_entry_calendar(driver):
        (driver.find_element(*ParkCalcPageLocators.ENTRY_CALENDAR_ICON).click())

    @staticmethod
    def open_leaving_calendar(driver):
        (driver.find_elements(*ParkCalcPageLocators.ENTRY_CALENDAR_ICON)[1].click())

    @staticmethod
    def select_first_day(driver):
        (driver.find_element(*ParkCalcPageLocators.FIRST_DAY_OF_A_MONTH).click())


