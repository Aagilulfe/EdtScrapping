from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


DRIVER_PATH = '/home/luc/Documents/chromedriver'

options = Options()
options.headless = True    # flag to decide if the page is displayed or not
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://planning.inalco.fr/public")

with open("source_code.html", "w") as file:
    file.write(driver.page_source)
# print(driver.page_source)

delay = 3 # seconds
try: # wait for the page to load
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[1].bouton_Edit')))
    print("Page is ready!")
except TimeoutException:
    print("Loading of page took too much time!")

driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys("Roumain L1")
driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(Keys.RETURN)

try: # wait for the table to load
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'GInterface.Instances[1].Instances[7]')))
    print("Table is ready!")
except TimeoutException:
    print("Loading of table took too much time!")

edt = driver.find_element(By.ID, "GInterface.Instances[1].Instances[7]")
print(edt)
edt.screenshot("edt.png")

if options.headless:
    time.sleep(3)
driver.quit()
print("Page closed.")