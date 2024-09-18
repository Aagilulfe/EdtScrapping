from scrapper import Scrapper
import time

"""""""""""Student Info"""""""""""

STUDENT_LANGUAGE = "Roumain"
STUDENT_LEVEL = "L1"
STUDENT_ELECTIVE_CLASS = ["ECOA130d", "ECOA130g"]


"""""""""""""""Paths"""""""""""""""

DRIVER_PATH = 'drivers/geckodriver'
SCREENSHOTS_SAVE_PATH = 'screenshots/'


# Scrapper instanciation
scrapper_bot = Scrapper(DRIVER_PATH=DRIVER_PATH, SCREENSHOTS_SAVE_PATH=SCREENSHOTS_SAVE_PATH, headless=False)

scrapper_bot.webpage_loading()

scrapper_bot.get_main_planning(student_language=STUDENT_LANGUAGE, student_level=STUDENT_LEVEL)

for code in STUDENT_ELECTIVE_CLASS:
    scrapper_bot.get_class_by_code(class_code=code)