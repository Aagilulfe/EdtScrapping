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
options.add_argument("-headless")
options.add_argument("--window-size=1920,1200")

driver = webdriver.Firefox(options=options)
driver.get("https://planning.inalco.fr/public")


delay = 3 # timeout delay in seconds

#WEBPAGE
# wait for the page to load
myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[1].bouton_Edit')))
print("Page is ready!")






########################
if not (options.arguments[0] == '-headless'):
    time.sleep(3)
driver.quit()
print("Session closed.")