from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

"""""""""""Student Info"""""""""""

student_language = "Roumain"
student_level = "L1"
student_UE3_1 = "ECOA130d"
student_UE3_2 = "ECOA130g"

##################################

DRIVER_PATH = 'chromedriver'

options = Options()
options.headless = False    # flag to decide if the page is displayed (False) or not (True)
options.add_argument("--window-size=1920,1200")
# options.add_argument("--window-size=970,600") #bad dimensions

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://planning.inalco.fr/public")

with open("source_code.html", "w") as file:
    file.write(driver.page_source)
# print(driver.page_source)

delay = 3 # timeout delay in seconds

#WEBPAGE
try: # wait for the page to load
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[1].bouton_Edit')))
    print("Page is ready!")
except TimeoutException:
    print("Loading of page took too much time!")

driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(student_language + " " + student_level)
driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(Keys.RETURN)

#MAIN PLANNING
try: # wait for the table to load
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[7]')))
    print("Table is ready!")
except TimeoutException:
    print("Loading of table took too much time!")

edt = driver.find_element(By.ID, "GInterface.Instances[1].Instances[7]")
edt.screenshot(student_language + student_level + "_edt.png")

#SWITCH TO "MATIERES" SECTION
driver.find_element(By.ID, "GInterface.Instances[0].Instances[1]_Combo2").click()
driver.find_element(By.ID, "GInterface.Instances[1].Instances[0].bouton_Edit").click()
time.sleep(0.5)
driver.find_element(By.ID, "GInterface.Instances[1].Instances[0]_Liste").send_keys(Keys.ARROW_DOWN)
driver.find_element(By.ID, "GInterface.Instances[1].Instances[0]_Liste").send_keys(Keys.RETURN)

# select = Select(driver.find_element(By.ID, 'GInterface.Instances[1].Instances[0]_ContenuScroll'))
# select.select_by_visible_text('Saisie du code')

# driver.find_element(By.XPATH, "//div/ul/li").click()


#FIRST UE3 PLANNING
try: # wait for the table to load
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[1].bouton_Edit')))
    print("Matieres section is ready!")
except TimeoutException:
    print("Loading of matieres section took too much time!")


########################
if not options.headless:
    time.sleep(3)
driver.quit()
print("Page closed.")