from selenium import webdriver
# from selenium.webdriver.chrome.options import Options   # for Chrome browser
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
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

# DRIVER_PATH = 'drivers/chromedriver'    # for Chrome browser
DRIVER_PATH = 'drivers/geckodriver'

SCREENSHOTS_SAVE_PATH = 'screenshots/'

options = Options()
# options.headless = True    # flag to decide if the page is displayed (False) or not (True)
options.add_argument("-headless")
options.add_argument("--window-size=1920,1200")
# options.add_argument("--window-size=970,600") #bad dimensions

# driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)     # for Chrome browser
# driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)
driver = webdriver.Firefox(options=options)
driver.get("https://planning.inalco.fr/public")

# with open("source_code.html", "w") as file:
#     file.write(driver.page_source)
# print(driver.page_source)

delay = 3 # timeout delay in seconds

#WEBPAGE
try: # wait for the page to load
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[1].bouton_Edit')))
    print("Page is ready!")
except TimeoutException:
    print("Loading of page took too much time!")

#MAIN PLANNING (UE1 & UE2)
driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(student_language + " " + student_level)
driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(Keys.RETURN)

try: # wait for the table to load
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'id_41_c_g')))
    print("Table is ready!")
except TimeoutException:
    print("Loading of table took too much time!")

edt = driver.find_element(By.ID, "id_41_c_g")
edt.screenshot(SCREENSHOTS_SAVE_PATH + student_language + student_level + "_edt.png")
print("=> Main planning saved\n")

#SWITCH TO "MATIERES" SECTION
driver.find_element(By.ID, "GInterface.Instances[0].Instances[1]_Combo2").click()
driver.find_element(By.ID, "GInterface.Instances[1].Instances[0].bouton_Edit").click()
try: # wait for the option to be clickable
    myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'GInterface.Instances[1].Instances[0]_1')))
    print("\"Saisie du code\" option appeared!")
except TimeoutException:
    print("Loading of \"Saisie du code\" option took too much time!")
# time.sleep(0.5)
driver.find_element(By.ID, "GInterface.Instances[1].Instances[0]_1").click()    # Selecting "Saisie du code" option


#LOAD UE3 PLANNINGS
try: # wait for the table to load
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[1].bouton_Edit')))
    print("Matieres section is ready!")
except TimeoutException:
    print("Loading of matieres section took too much time!")

#FIRST UE3
driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(student_UE3_1)
driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(Keys.RETURN)
try: # wait for the ue3_1 to load
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[7]')))
    print("First UE3 is ready!")
except TimeoutException:
    print("Loading of first UE3 took too much time!")
edt_ue3_1 = driver.find_element(By.ID, "GInterface.Instances[1].Instances[7]")
time.sleep(0.5)
edt_ue3_1.screenshot(SCREENSHOTS_SAVE_PATH + student_UE3_1 + "_edt.png")
print("=> First UE3 planning saved\n")

#SECOND UE3
driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").clear()
driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(student_UE3_2)
driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(Keys.RETURN)
try: # wait for the ue3_1 to load
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[7]')))
    print("Second UE3 is ready!")
except TimeoutException:
    print("Loading of second UE3 took too much time!")
print()
edt_ue3_2 = driver.find_element(By.ID, "GInterface.Instances[1].Instances[7]")
time.sleep(0.5)
edt_ue3_2.screenshot(SCREENSHOTS_SAVE_PATH + student_UE3_2 + "_edt.png")
print("=> Second UE3 planning saved\n")


########################
if not (options.arguments[0] == '-headless'):
    time.sleep(3)
driver.quit()
print("Session closed.")