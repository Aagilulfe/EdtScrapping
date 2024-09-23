from selenium import webdriver
# from selenium.webdriver.chrome.options import Options   # for Chrome browser
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from namedlist import namedlist
import matplotlib.pyplot as plt
from math import ceil
import textwrap

"""""""""""Student Info"""""""""""

student_language = "Polonais"
student_level = "L3"
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


def get_planning_table(promotion :str, group :int) -> list[list]:
    driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").clear()
    # driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys("Relations International (RI) L3")
    driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(promotion)
    driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").send_keys(Keys.RETURN)

    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="GInterface.Instances[1].Instances[7]_Contenu_0"]')))
    time.sleep(0.5)

    # Obtain the number of rows in table 
    rows = len(driver.find_elements(By.XPATH, 
        "/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr"))
    
    # Obtain the number of columns in table 
    cols = len(driver.find_elements(By.XPATH, 
        "/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr[3]/td")) 
    
    # Print rows and columns counts
    print("nb of rows: ", rows) 
    print("nb of cols: ", cols) 
    
    
    # Getting the data from the table
    data_list = []
    day = None
    for r in range(1, rows+1):
        data_row = []
        for p in range(1, cols+1):
            # obtaining the text from each column of the table
            try:
                value = driver.find_element(By.XPATH, 
                    "/html/body/div[3]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr["+str(r)+"]/td["+str(p)+"]").text
                # print(value, end='     ')
                if (" Gpe " in value) and (value[-1] != str(group)):
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

data_RI = get_planning_table("Relations International (RI) L3", 2)
data_polonais = get_planning_table("Polonais L3", None)
# for line in data_polonais:
#     print(line)
# for line in data_RI:
#     print(line)

data = data_polonais + data_RI

########################
if not (options.arguments[0] == '-headless'):
    time.sleep(20)
driver.quit()
print("Session closed.")



# df = DataFrame(data_list, columns=['Date', 'col1', 'Horaires', 'Intitule', 'Groupe', 'Enseignant', 'Salle', 'Batiment', 'col2', 'Type de cours'])
# print(df)


DAYS = ['Lundi','Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
Event = namedlist('Event', 'name, days, startH, startM, endH, endM, color')

def getDay(prefix):
    for d in DAYS:
        if d.startswith(prefix):
            return d
    raise UserWarning("Invalid day: {0}".format(prefix))

def parser(data):
    latest = 0
    earliest = 24
    events = [Event('', '', '', '', '', '', '')]
    for course in data:
        code, course_name = course[3].split("-")
        code = code.rstrip()
        course_name = course_name.lstrip()
        course_name = textwrap.fill(course_name, 32)
        events[-1].name = code + "\n" + course_name + "\n" + course[5] + "\n" + course[6]
        events[-1].days = [getDay(course[0])]
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
        events.append(Event('', '', '', '', '', '', ''))
    return events, earliest, latest + 1

def plotEvent(e):
    for day in e.days:
        # print(e)
        d = DAYS.index(day) + 0.52
        start = float(e.startH) + float(e.startM) / 60
        end = float(e.endH) + float(e.endM) / 60
        plt.fill_between([d, d + 0.96], [start, start], [end, end], color=e.color, edgecolor="black")
        plt.text(d + 0.02, start + 0.02, '{0}:{1:0>2}'.format(e.startH, e.startM), va='top', fontsize=7)
        plt.text(d + 0.48, (start + end) * 0.502, e.name, ha='center', va='center', fontsize=9)



events, earliest, latest = parser(data)

fig = plt.figure(figsize=(18, 9))

plt.title('Emploi du temps de la semaine', y=1, fontsize=14)
plt.xlim(0.5, len(DAYS) + 0.5)
plt.xticks(range(1, len(DAYS) + 1), DAYS)

plt.ylim(latest, earliest)
# plt.yticks(range(ceil(earliest), ceil(latest)), ["{0}h00".format(h) for h in range(ceil(earliest), ceil(latest))])
plt.yticks([i/2 for i in range(ceil(earliest)*2, ceil(latest)*2+1)], ["{0}h{1}".format(h//2, 30*(h%2)) for h in range(ceil(earliest)*2, ceil(latest)*2+1)])
plt.grid(axis='y', linestyle='--', linewidth=0.5)

for e in events:
    plotEvent(e)

# plt.show()
plt.savefig('week_planning.png', dpi=200, bbox_inches='tight')