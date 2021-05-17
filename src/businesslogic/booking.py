

import os
import re
from datetime import datetime
import time
from enum import Enum

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from src.helper.fileReader import FileExtensions
from src.helper.webDriverExtensions import WebDriverExtensions
from selenium.webdriver.common.action_chains import ActionChains


class TariffOptions(Enum):
    Normal = '105085073'
    Ermaeßigt = '102373921'


class Booking():
    def __init__(self):
        """Loads the environment variables and initialize all required properties.
        """
        # setup base config
        load_dotenv()
        self.baseDataFilePath = os.getenv("BASEDATA_FILE_PATH")
        self.participantsFilePath = os.getenv("PARTICIPANTS_FILE_PATH")
        self.driverPath = os.getenv("DRIVERPATH")
        self.url = os.getenv('URL')
        self.successful = False

    def initBrowser(self):
        """Inits the webdriver and set some pre settings.
        """
        print("WebDriver-EXE: '{}'".format(self.driverPath))
        self.driver = webdriver.Chrome(executable_path=self.driverPath)
        self.wait = WebDriverWait(self.driver, 10)
        # resize window
        self.driver.maximize_window()

    def openPage(self):
        """Opens the page with content of env-variable 'url' 
        """
        # Open booking page
        print("Opening page: '{}'".format(self.url))
        self.driver.get(self.url)

    def startBooking(self):
        try:
            print("Start booking...")

            # read base config file as json
            baseDataJson = FileExtensions.readFile(self.baseDataFilePath)

            # set start date
            self.__setStartDate__(baseDataJson['startDate'])
            # select the prefered slot number
            maxPeople = self.__selectSlot__(baseDataJson)
            # fill out base formular
            self.__fillBaseData__(baseDataJson)

            self.__makeScreenshot__('./orders/basedata_{}.png')
            # add friends to the booking formular
            self.__addParticipants__(maxPeople, baseDataJson['selfBooking'])
            self.__makeScreenshot__('./orders/friends_{}.png')

            # go to payment
            # self.__goToPayment__()
            self.driver.execute_script("""
            var addMessage = document.createElement('div');
            addMessage.style = 'background-color:green;font-color:black;font-size:24px;font-weight:bold;text-align:center;color:white';
            addMessage.textContent = 'Please enter your prefered payment option and finished by paying.';            
            
            document.querySelector('button.drp-course-booking-continue.drp-mt-4').parentElement.append(addMessage);""")

            element = WebDriverExtensions.WaitOnElement(
                self.wait, By.CSS_SELECTOR, "button.drp-course-booking-continue.drp-mt-4")
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()

            self.wait_until(300)
            self.successful = True
            print("Booking has finished!")
        except Exception as ex:
            print(ex)

    def endBooking(self):
        print("End")
        self.driver.quit()

    def wait_until(self, timeout, period=0.5):
        mustend = time.time() + timeout
        while time.time() < mustend:
            time.sleep(period)

    def __goToPayment__(self):
        # Forward to payment
        WebDriverExtensions.WaitOnElement(self.wait,
                                          By.CSS_SELECTOR, "button.drp-course-booking-continue.drp-mt-4").click()
        self.driver.execute_script("window.scrollTo(0,518)")

    def __makeScreenshot__(self, path):

        currentDateString = "{0}-{1}-{2}".format(
            datetime.now().year, datetime.now().month, datetime.now().day)
        fileCounter = 0
        a = 0
        while a <= 10:
            try:
                if not FileExtensions.fileExists(path.format(currentDateString)):
                    self.driver.save_screenshot(
                        path.format(currentDateString))
                    break
                elif FileExtensions.fileExists(path.format(currentDateString)):
                    self.driver.save_screenshot(
                        path.format(currentDateString)+'_{0}'.format(fileCounter))
                    break
                elif not FileExtensions.fileExists(path.format(currentDateString)+'_{0}'.format(fileCounter)):
                    self.driver.save_screenshot(
                        path.format(currentDateString)+'_{0}'.format(fileCounter))
                    break
            except Exception as ex:
                print(ex)

            fileCounter += 1
            a += 1

    def __fillBaseData__(self, baseData):
        print("----------  base data  ----------")
        print("The booking formular filled with following data:")
        # Enter Firstname
        WebDriverExtensions.WaitOnElement(self.wait,
                                          By.CSS_SELECTOR, ".drp-row:nth-child(2) > .drp-col-12 > input").send_keys(baseData['firstname'])
        print('Firstname: {}'.format(baseData['firstname']))
        # Enter last name
        WebDriverExtensions.WaitOnElement(self.wait,
                                          By.CSS_SELECTOR, ".drp-row:nth-child(3) input").send_keys(baseData['lastname'])
        print('Lastname: {}'.format(baseData['lastname']))
        # Enter street
        WebDriverExtensions.WaitOnElement(self.wait,
                                          By.CSS_SELECTOR, ".drp-row:nth-child(5) input").send_keys(baseData['street'])
        print('Street: {}'.format(baseData['street']))
        # Enter plz
        WebDriverExtensions.WaitOnElement(self.wait,
                                          By.CSS_SELECTOR, ".drp-row:nth-child(6) input").send_keys(baseData['plz'])
        print('Plz: {}'.format(baseData['plz']))
        # Enter city
        WebDriverExtensions.WaitOnElement(self.wait,
                                          By.CSS_SELECTOR, ".drp-row:nth-child(7) input").send_keys(baseData['city'])
        print('City: {}'.format(baseData['city']))
        # Enter mobile number
        WebDriverExtensions.WaitOnElement(self.wait,
                                          By.CSS_SELECTOR, ".drp-row:nth-child(8) input").send_keys(baseData['mobile'])
        print('Mobile: {}'.format(baseData['mobile']))
        # enter email adress
        WebDriverExtensions.WaitOnElement(self.wait,
                                          By.ID, "drp-course-booking-person-email").send_keys(baseData['email'])
        print('Email: {}'.format(baseData['email']))
        # Select tarif
        dropdown: WebElement = WebDriverExtensions.WaitOnElement(self.wait,
                                                                 By.CSS_SELECTOR, ".drp-course-booking-tariff-select > .drp-w-100")
        dropdown.find_element(
            By.XPATH, "//option[@value='"+TariffOptions[baseData['tariff']].value+"']").click()
        # Accept AGB
        WebDriverExtensions.WaitOnElement(
            self.wait, By.ID, "drp-course-booking-client-terms-cb").click()
        # Accept data processing
        WebDriverExtensions.WaitOnElement(self.wait,
                                          By.ID, "drp-course-booking-data-processing-cb").click()
        # self.driver.execute_script(
        #     "document.querySelector(\".drp-row:nth-child(4) input\").valueAsDate=new Date(1994,11,31)")
        WebDriverExtensions.WaitOnElement(self.wait,
                                          By.CSS_SELECTOR, ".drp-row:nth-child(4) input").send_keys(baseData['birthdate'])
        print('Birthdate: {}'.format(baseData['birthdate']))
        print("---------- /base data/ ----------")

    def __setStartDate__(self, startDate):
        days: list[WebElement] = WebDriverExtensions.WaitOnElements(
            self.wait, By.CSS_SELECTOR, 'div.drp-calendar-weeks div.drp-calendar-day.drp-calendar-day-dates')

        p: list[WebElement] = [date for date in days if str(
            date.text).replace(' ', '') == startDate]
        p[0].click()

    def __selectSlot__(self, baseData):
        slots: list[WebElement] = WebDriverExtensions.WaitOnElements(
            self.wait, By.CSS_SELECTOR, 'div.drp-course-dates-list div.drp-course-date-item.drp-mb-3')

        slot = slots[baseData['slot']-1]
        if('drp-date-not-relevant' in slot.get_attribute('class')):
            print("The slot '{}' is not available!".format(slot.text))
            # pytest.exit("The slot {0} is not available!".format(slot.text))

        element = slot.find_element_by_css_selector(
            "span.drp-course-date-item-max-participants")

        matches = re.match(
            r'(\d+)', element.text)

        maxPeople = int(matches.groups()[0])

        button = slot.find_element_by_css_selector(
            "div.drp-course-date-item-booking-box.drp-p-2 > button")
        button.click()

        return maxPeople

    def __addParticipants__(self, maxPeople, selfBooking):
        try:
            file = FileExtensions.readFile(self.participantsFilePath)

            if(len(file) == 0):
                return

            WebDriverExtensions.WaitOnElement(
                self.wait, By.CSS_SELECTOR, "button.drp-mt-2.drp-course-booking-add-participant").click()

            if(selfBooking):
                participantNumber = 1
            elif(not selfBooking):
                WebDriverExtensions.WaitOnElement(
                    self.wait, By.ID, "drp-course-booking-person-takes-part-cb").click()
                participantNumber = 0

            print("Adding friends to come with: ")
            for participant in file:
                print("Friend {}: ".format(participantNumber))

                # enter firstname
                WebDriverExtensions.WaitOnElement(
                    self.wait, By.CSS_SELECTOR, "input:is([autocomplete='section-participant{} given-name']".format(participantNumber)).send_keys(participant['firstname'])
                print("     Firstname: {}".format(participant['firstname']))

                # enter lastname
                WebDriverExtensions.WaitOnElement(
                    self.wait, By.CSS_SELECTOR, "input:is([autocomplete='section-participant{} family-name']".format(participantNumber)).send_keys(participant['lastname'])
                print("     Lastname: {}".format(participant['lastname']))

                # enter birthdate
                WebDriverExtensions.WaitOnElement(
                    self.wait, By.CSS_SELECTOR, "input:is([autocomplete='section-participant{} bday']".format(participantNumber)).send_keys(participant['birthdate'])
                print("     Birtdate: {}".format(participant['birthdate']))

                # enter email
                WebDriverExtensions.WaitOnElement(
                    self.wait, By.CSS_SELECTOR, "input:is([autocomplete='section-participant{} email']".format(participantNumber)).send_keys(participant['email'])
                print("     Email: {}".format(participant['email']))

                # select tariff
                tarifElement = WebDriverExtensions.WaitOnElements(
                    self.wait, By.CSS_SELECTOR, "div.drp-course-booking-participant-item.drp-row.drp-mb-3")[participantNumber]

                for t in TariffOptions:
                    if(t.name == participant['tariff']):
                        tarif = t
                        break

                tarifElement.find_element_by_css_selector(
                    "select.drp-w-100.drp-mb-2 option:is([value='{}'])".format(tarif.value)).click()
                print("     Tariff: {}".format(participant['tariff']))

                participantNumber += 1

                if(participantNumber is maxPeople):

                    if(len(file[maxPeople:]) != 0):
                        print(
                            "The following participants were not added, because of the maximum per slot reached: ")

                        for p in file[maxPeople:]:
                            print(p['firstname'] + " " +
                                  p['lastname'])
                    return

                # add new friend
                WebDriverExtensions.WaitOnElement(
                    self.wait, By.CSS_SELECTOR, "button.drp-mt-2.drp-course-booking-add-participant").click()

        except Exception as ex:
            raise ex
