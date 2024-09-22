from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from typing import Type
from namedlist import namedlist
import textwrap
import matplotlib.pyplot as plt
from math import ceil
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
        self.DAYS = ['Lundi','Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
        self.Event = namedlist('Event', 'name, days, startH, startM, endH, endM, color')

        # Options definition
        self.options = Options()
        if self.headless:
            self.options.add_argument("-headless")
        self.options.add_argument(self.window_size)

        # Driver creation
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get(self.inalco_url)

    
    def draw_week_planning(self, student_promotions: list, student_elective_classes: list) -> None:
       
        data = []

        self.__goto_promotions_section()

        self.__switch_to_list_mode_in_promotion_tab()
        for promotion in student_promotions:
            data += self.__get_promotion_list(promotion[0], promotion[1], promotion[2])
            print("Promotion " + promotion[0] + " " + promotion[1] + " Gpe " + str(promotion[2]) + " list has been saved.")

        self.__goto_matieres_section()

        self.__switch_to_list_mode_in_matiere_tab()
        self.__switch_to_search_by_code()
        for elective_class in student_elective_classes:
            elective_class_data = self.__get_matiere_list(elective_class)
            # print(elective_class_data)
            data += elective_class_data
            print("Class " + elective_class + " list has been saved.")

        # for line in data:
        #     print(line)
        events, earliest, latest = self.__parser(data)

        plt.figure(figsize=(18, 9))

        plt.title('Emploi du temps de la semaine', y=1, fontsize=14)
        plt.xlim(0.5, len(self.DAYS) + 0.5)
        plt.xticks(range(1, len(self.DAYS) + 1), self.DAYS)

        plt.ylim(latest, earliest)
        plt.yticks([i/2 for i in range(ceil(earliest)*2, ceil(latest)*2+1)], ["{0}h{1}".format(h//2, 30*(h%2)) for h in range(ceil(earliest)*2, ceil(latest)*2+1)])
        plt.grid(axis='y', linestyle='--', linewidth=0.5)

        for e in events:
            self.__plotEvent(e)

        plt.savefig(self.SCREENSHOTS_SAVE_PATH + 'week_planning.png', dpi=200, bbox_inches='tight')
        print("\nWeek planning saved!")


    def webpage_loading(self) -> None:

        # Wait for the webpage to load
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[1].bouton_Edit')))
        print("Webpage is ready!\n")


    def get_promotion_by_name(self, student_language: str, student_level: str) -> None: # UE1 & UE2

        if self.promotion_function_never_called:
            self.__goto_promotions_section()
            self.promotion_function_never_called = False    # Already called once, now

        # Name search
        self.__make_search(student_language + " " + student_level)

        # Take a screenshot of the planning
        self.__save_planning(self.SCREENSHOTS_SAVE_PATH + student_language + student_level + "_edt.png")
        print("=> Promotion " + student_language + " " + student_level + " planning saved\n")


    def __get_promotion_list(self, student_language: str, student_level: str, student_group: int) -> None:
        
        self.__make_search(student_language + " " + student_level)
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table')))
        time.sleep(0.5)

        # Obtain the number of rows in table 
        rows = len(self.driver.find_elements(By.XPATH, 
            "/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr"))
        
        # Obtain the number of columns in table 
        cols = len(self.driver.find_elements(By.XPATH, 
            "/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr[3]/td")) 
        # print("rows", rows, "cols", cols)

        # Getting the data from the table
        data_list = []
        day = None
        for r in range(1, rows+1):
            data_row = []
            for p in range(1, cols+1):
                # obtaining the text from each column of the table
                try:
                    value = self.driver.find_element(By.XPATH, 
                        "/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr["+str(r)+"]/td["+str(p)+"]").text
                    # print(value, end='     ')
                    if (" Gpe " in value) and (value[-1] != str(student_group)):
                        data_row = []
                        break
                    if p == 1 and value != "" and value != " ":     # If date row
                        day = value.split(sep=" ")[0]
                        break
                    if p == 1:      # If first column of regular row
                        data_row.append(day.title())
                    else:
                        data_row.append(value)
                except NoSuchElementException:
                    break
            if len(data_row) > 2 and data_row[-1] != "" and data_row[-1] != " ":
                data_list.append(data_row)
                # print(data_row)
            # print()
        return data_list


    def get_matiere_by_code(self, class_code: str) -> None:   # ELECTIVE CLASSES

        if self.matiere_function_never_called:
            self.__goto_matieres_section()
            self.__switch_to_search_by_code()
            self.matiere_function_never_called = False      # Already called once, now

        # Code search
        self.__make_search(class_code)

        # Take a screenshot of the planning
        self.__save_planning(self.SCREENSHOTS_SAVE_PATH + class_code + "_edt.png")
        print("=> Class " + class_code + " planning saved\n")


    def __get_matiere_list(self, class_code: str) -> None:
        
        self.__make_search(class_code)
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table')))
        time.sleep(0.5)

        # Obtain the number of rows in table 
        rows = len(self.driver.find_elements(By.XPATH, 
            "/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr"))
        
        # Obtain the number of columns in table 
        cols = len(self.driver.find_elements(By.XPATH, 
            "/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr[2]/td"))
        # print("rows", rows, "cols", cols)
        # page_source = self.driver.page_source
        # fileToWrite = open("page_source.html", "w")
        # fileToWrite.write(page_source)
        # fileToWrite.close()
        
        # Getting the data from the table
        data_list = []
        day = None
        for r in range(1, rows+1):
            data_row = []
            for p in range(1, cols+1):
                # obtaining the text from each column of the table
                try:
                    value = self.driver.find_element(By.XPATH, 
                        "/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr["+str(r)+"]/td["+str(p)+"]").text
                    # print(value, end='     ')
                    if p == 1 and value != "" and value != " ":     # If date row
                        day = value.split(sep=" ")[0]
                        break
                    if p == 1:      # If first column of regular row
                        data_row.append(day.title())
                    else:
                        data_row.append(value)
                except NoSuchElementException:
                    break
            if len(data_row) > 2 and data_row[-1] != "" and data_row[-1] != " ":
                data_list.append(data_row)
                # print(data_row)
            # print()
        # for line in data_list:
        #     print(line)
        return data_list


    def __goto_promotions_section(self) -> None:
        # Switch to "PROMOTIONS" section
        WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.ID, 'GInterface.Instances[0].Instances[1]_Combo1')))
        self.driver.find_element(By.ID, "GInterface.Instances[0].Instances[1]_Combo1").click()
        WebDriverWait(self.driver, self.delay).until(lambda driver: self.__get_current_section(driver)=="DIPLOME.EDT")     # Check if we really moved to PROMOTIONS section
        print("\nMoved to \"Promotions\" section")


    def __goto_matieres_section(self) -> None:
        # Switch to "MATIERES" section
        WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.ID, 'GInterface.Instances[0].Instances[1]_Combo2')))
        self.driver.find_element(By.ID, "GInterface.Instances[0].Instances[1]_Combo2").click()
        WebDriverWait(self.driver, self.delay).until(lambda driver: self.__get_current_section(driver)=="MATIERE.EDT")     # Check if we really moved to MATIERES section
        print("\nMoved to \"Matieres\" section")
    

    def __switch_to_search_by_code(self):
        # Change the search mode
        self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[0].bouton_Edit").click()
        # Wait for the option "Saisie du code" to be clickable
        WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.ID, 'GInterface.Instances[1].Instances[0]_1')))
        self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[0]_1").click()    # Selecting "Saisie du code" option
        print("\"Saisie du code\" option selected!")


    def __switch_to_list_mode_in_promotion_tab(self) -> None:
        # Method to switch to list mode when in promotion tab
        drop_down_menu = self.driver.find_element(By.CLASS_NAME, 'item-menu_niveau1.menuitem-niveau.has-submenu.selected')
        actions = webdriver.ActionChains(self.driver)
        actions.move_to_element(drop_down_menu).perform()   # Hover to the drop down menu in order to get the choices
        WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[1]/div[1]/div/div[4]/div[1]/ul/li[1]/ul/li[2]')))
        self.driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[1]/div/div[4]/div[1]/ul/li[1]/ul/li[2]').click()
        print("Switched to list mode (promotion tab)")


    def __switch_to_list_mode_in_matiere_tab(self) -> None:
        # Method to switch to list mode when in matieres tab
        drop_down_menu = self.driver.find_element(By.CLASS_NAME, 'menu-principal_niveau1')
        actions = webdriver.ActionChains(self.driver)
        actions.move_to_element(drop_down_menu).perform()   # Hover to the drop down menu in order to get the choices
        WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[1]/div[1]/div/div[4]/div[1]/ul/li/ul/li[2]')))
        self.driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[1]/div/div[4]/div[1]/ul/li/ul/li[2]').click()
        print("Switched to list mode (matiere tab)")


    def  __get_current_section(self, driver) -> str:
        witness = driver.find_element(By.CLASS_NAME, 'item-menu_niveau1.menuitem-niveau.has-submenu.selected')  # Search for "Emploi du temps" drop down menu
        return witness.get_attribute("data-genre")


    def __has_changed(self, driver):#, driver: Type[webdriver.Firefox]) -> bool:
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

    
    def __getDay(self, prefix):
        for d in self.DAYS:
            if d.startswith(prefix):
                return d
        raise UserWarning("Invalid day: {0}".format(prefix))

    def __parser(self, data):
        latest = 0
        earliest = 24
        events = [self.Event('', '', '', '', '', '', '')]
        for course in data:
            if len(course) == 10:
                code, course_name = course[3].split("-")
                code = code.rstrip()
                course_name = course_name.lstrip()
                course_name = textwrap.fill(course_name, 32)
                events[-1].name = code + "\n" + course_name + "\n" + course[5] + "\n" + course[6]
            elif len(course) == 8:
                course_name = course[4] + "\n" + course[3] + "\n" + course[5]
                course_name = textwrap.fill(course_name, 32)
                events[-1].name = course_name
            else:
                raise Exception("Wrong course format")
            events[-1].days = [self.__getDay(course[0])]
            hours = course[2].replace(' ', '').split('-')
            start = hours[0].split('h')
            end = hours[1].split('h')
            events[-1].startH = int(start[0])
            events[-1].startM = int(start[1])
            events[-1].endH = int(end[0])
            events[-1].endM = int(end[1])
            earliest = events[-1].startH if events[-1].startH < earliest else earliest
            latest = events[-1].endH + 1 if events[-1].endH > latest else latest
            events[-1].color = "mediumpurple"
            events.append(self.Event('', '', '', '', '', '', ''))
        return events, earliest, latest + 1

    def __plotEvent(self, e):
        for day in e.days:
            # print(e)
            d = self.DAYS.index(day) + 0.52
            start = float(e.startH) + float(e.startM) / 60
            end = float(e.endH) + float(e.endM) / 60
            plt.fill_between([d, d + 0.96], [start, start], [end, end], color=e.color, edgecolor="black")
            plt.text(d + 0.02, start + 0.02, '{0}:{1:0>2}'.format(e.startH, e.startM), va='top', fontsize=7)
            plt.text(d + 0.48, (start + end) * 0.502, e.name, ha='center', va='center', fontsize=9)