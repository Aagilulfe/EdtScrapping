from selenium import webdriver
# from selenium.webdriver.chrome.options import Options   # for Chrome browser
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class Scrapper():
    
    def __init__(self, DRIVER_PATH: str, SCREENSHOTS_SAVE_PATH: str, inalco_url="https://planning.inalco.fr/public", headless=True, window_size="--window-size=1920,1200") -> None:

        # Variable initialization
        self.inalco_url = inalco_url
        self.DRIVER_PATH = DRIVER_PATH
        self.SCREENSHOTS_SAVE_PATH = SCREENSHOTS_SAVE_PATH
        self.headless = headless
        self.window_size = window_size
        self.delay = 3

        # Options definition
        self.options = Options()
        if self.headless:
            self.options.add_argument("-headless")
        self.options.add_argument(self.window_size)

        # Driver creation
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get(self.inalco_url)


    def webpage_loading(self) -> None:

        try: # wait for the webpage to load
            myElem = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[1].bouton_Edit')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading of page took too much time!")


    def get_main_planning(self, student_language: str, student_level: str) -> None: # UE1 & UE2

        self.__goto_promotions_section()

        self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(student_language + " " + student_level)
        self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(Keys.RETURN)

        try: # wait for the table to load
            myElem = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[7]')))
            print("Table is ready!")
        except TimeoutException:
            print("Loading of table took too much time!")

        edt = self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[7]")
        edt.screenshot(self.SCREENSHOTS_SAVE_PATH + student_language + student_level + "_edt.png")
        print("=> Main planning saved\n")


    def get_class_by_code(self, class_code: str) -> None:

        self.__goto_matieres_section()

        # Change the search mode
        self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[0].bouton_Edit").click()

        # Wait for the option "Saisie du code" to be clickable
        try:
            myElem = WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.ID, 'GInterface.Instances[1].Instances[0]_1')))
            print("\"Saisie du code\" option appeared!")
        except TimeoutException:
            print("Loading of \"Saisie du code\" option took too much time!")
        self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[0]_1").click()    # Selecting "Saisie du code" option

        # Wait for the "MATIERES" section to load correctly
        try:
            myElem = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[1].bouton_Edit')))
            print("Matieres section is ready!")
        except TimeoutException:
            print("Loading of matieres section took too much time!")

        # Code search
        self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(class_code)
        self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(Keys.RETURN)

        # Wait for the class planning to load
        try:
            myElem = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[7]')))
            print("Class " + class_code + " planning is ready!")
        except TimeoutException:
            print("Loading of " + class_code + " took too much time!")
        edt_ue3_1 = self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[7]")
        time.sleep(0.5)
        edt_ue3_1.screenshot(self.SCREENSHOTS_SAVE_PATH + class_code + "_edt.png")
        print("=> Class " + class_code + " planning saved\n")


    def __goto_promotions_section(self):
        # Switch to "PROMOTIONS" section
        time.sleep(0.25)
        self.driver.find_element(By.ID, "GInterface.Instances[0].Instances[1]_Combo1").click()

    def __goto_matieres_section(self):
        # Switch to "MATIERES" section
        time.sleep(0.25)
        self.driver.find_element(By.ID, "GInterface.Instances[0].Instances[1]_Combo2").click()