from selenium import webdriver
# from selenium.webdriver.chrome.options import Options   # for Chrome browser
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
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
myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div[1]/div/div[4]/div[1]/ul/li[1]')))
print("Page is ready!")

tutorials = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[1]/div/div[4]/div[1]/ul/li[1]")
actions = webdriver.ActionChains(driver)
actions.move_to_element(tutorials).perform()
WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[1]/div[1]/div/div[4]/div[1]/ul/li[1]/ul/li[2]')))
driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[1]/div/div[4]/div[1]/ul/li[1]/ul/li[2]").click()
print("Switched to list mode")


driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").clear()
driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys("Relations International (RI) L3")
driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(Keys.RETURN)

WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="GInterface.Instances[1].Instances[7]_Contenu_0"]')))

# Obtain the number of rows in table 
rows = len(driver.find_elements(By.XPATH, 
    "/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr"))
  
# Obtain the number of columns in table 
cols = len(driver.find_elements(By.XPATH, 
    "/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr[3]/td")) 
  
# Print rows and columns counts
print("nb of rows: ", rows) 
print("nb of cols: ", cols) 
  
# Printing the table headers 
print("Locators           "+"             Description") 
  
# Printing the data of the table 
for r in range(1, rows+1): 
    for p in range(1, cols+1): 
        
        # obtaining the text from each column of the table
        try:
            value = driver.find_element(By.XPATH, 
                "/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr["+str(r)+"]/td["+str(p)+"]").text 
            print(value, end='       ')
        except NoSuchElementException:
            break
    print() 




########################
if not (options.arguments[0] == '-headless'):
    time.sleep(20)
driver.quit()
print("Session closed.")