# park_calc_page.py
from locators import ParkCalcPageLocators


class ParkCalcPage:
    def __init__(self, driver):
        self.driver = driver

    def set_starting_date(self, date_string):
        start_date = self.driver.find_element(*ParkCalcPageLocators.STARTING_DATE_FIELD)
        start_date.clear()
        start_date.send_keys(date_string)

    def set_starting_time(self, time_string):
        start_time = self.driver.find_element(*ParkCalcPageLocators.STARTING_TIME_FIELD)
        start_time.clear()
        start_time.send_keys(time_string)

    def set_leaving_date(self, date_string):
        leaving_date = self.driver.find_element(*ParkCalcPageLocators.LEAVING_DATE_FIELD)
        leaving_date.clear()
        leaving_date.send_keys(date_string)

    def set_leaving_time(self, time_string):
        leaving_time = self.driver.find_element(*ParkCalcPageLocators.LEAVING_TIME_FIELD)
        leaving_time.clear()
        leaving_time.send_keys(time_string)

    def submit_button(self):
        submit_button = self.driver.find_element(*ParkCalcPageLocators.CALCULATE_BUTTON)
        submit_button.click()
