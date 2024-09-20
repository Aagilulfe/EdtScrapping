from selenium import webdriver
# from selenium.webdriver.chrome.options import Options   # for Chrome browser
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.remote.webelement import WebElement
from typing import Type
import time

"""
Scrapping class for INALCO hyperplanning

NB: It's mandatory to begin with promotion scrapping, and then finish with class scrapping. No alternation.
"""

class Scrapper():
    
    def __init__(self, DRIVER_PATH: str, SCREENSHOTS_SAVE_PATH: str, inalco_url="https://planning.inalco.fr/public", headless=True, window_size="--window-size=1920,1200") -> None:

        # Variable initialization
        self.inalco_url = inalco_url
        self.DRIVER_PATH = DRIVER_PATH
        self.SCREENSHOTS_SAVE_PATH = SCREENSHOTS_SAVE_PATH
        self.headless = headless
        self.window_size = window_size
        self.delay = 3
        self.last_element_retrieved = None
        self.promotion_function_never_called = True
        self.matiere_function_never_called = True

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
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[1].bouton_Edit')))
            print("Webpage is ready!\n")
        except TimeoutException:
            print("Loading of page took too much time!")


    def get_promotion_by_name(self, student_language: str, student_level: str) -> None: # UE1 & UE2

        if self.promotion_function_never_called:
            self.goto_promotions_section()
            self.promotion_function_never_called = False    # Already called once, now

        # Name search
        self.__make_search(student_language + " " + student_level)

        # Take a screenshot of the planning
        self.__save_planning(self.SCREENSHOTS_SAVE_PATH + student_language + student_level + "_edt.png")
        print("=> Promotion " + student_language + " " + student_level + " planning saved\n")


    def get_matiere_by_code(self, class_code: str) -> None:   # ELECTIVE CLASSES

        if self.matiere_function_never_called:
            self.goto_matieres_section()
            self.matiere_function_never_called = False      # Already called once, now

        # Code search
        self.__make_search(class_code)

        # Take a screenshot of the planning
        self.__save_planning(self.SCREENSHOTS_SAVE_PATH + class_code + "_edt.png")
        print("=> Class " + class_code + " planning saved\n")


    def goto_promotions_section(self) -> None:
        # Switch to "PROMOTIONS" section
        WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.ID, 'GInterface.Instances[0].Instances[1]_Combo1')))
        self.driver.find_element(By.ID, "GInterface.Instances[0].Instances[1]_Combo1").click()


    def goto_matieres_section(self) -> None:
        # Switch to "MATIERES" section
        WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.ID, 'GInterface.Instances[0].Instances[1]_Combo2')))
        self.driver.find_element(By.ID, "GInterface.Instances[0].Instances[1]_Combo2").click()

        # Change the search mode
        self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[0].bouton_Edit").click()

        # Wait for the option "Saisie du code" to be clickable
        try:
            WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.ID, 'GInterface.Instances[1].Instances[0]_1')))
            print("\"Saisie du code\" option selected!\n")
        except TimeoutException:
            print("Loading of \"Saisie du code\" option took too much time!")
        self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[0]_1").click()    # Selecting "Saisie du code" option


    def __has_changed(self, driver: Type[webdriver.Firefox]) -> bool:
        # Method that checks if grid changed
        if self.last_element_retrieved == None:
            return True

        new_grid = driver.find_element(By.CLASS_NAME, "ObjetGrille.GrilleNonInverse")
        return not(self.last_element_retrieved.id == new_grid.id)
    

    def __save_planning(self, file_name: str) -> None:
        # Wait for the class planning to load
        WebDriverWait(self.driver, self.delay).until(EC.visibility_of_element_located((By.CLASS_NAME, 'ObjetGrille.GrilleNonInverse')))
        
        # Wait for the new class grid to load (else, the same grid would be saved)
        WebDriverWait(self.driver, self.delay).until(self.__has_changed)
        print("The grid correctly changed!")
        planning = self.driver.find_element(By.CLASS_NAME, "ObjetGrille.GrilleNonInverse")
        planning.screenshot(file_name)
        
        # Update last_element_retrieved variable with the last saved element
        self.last_element_retrieved = planning


    def __make_search(self, search_input: str) -> None:
        self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").clear()
        self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(search_input)
        self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(Keys.RETURN)