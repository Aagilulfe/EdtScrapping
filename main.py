from scrapper import Scrapper
# import time

"""""""""""Student Info"""""""""""

STUDENT_LANGUAGE = "Roumain"
STUDENT_LEVEL = "L1"
STUDENT_ELECTIVE_CLASSES = ["ECOA130d", "ECOA130g"]


"""""""""""""""Paths"""""""""""""""

DRIVER_PATH = 'drivers/geckodriver'
SCREENSHOTS_SAVE_PATH = 'screenshots/'


# Scrapper instanciation
scrapper_bot = Scrapper(DRIVER_PATH=DRIVER_PATH, SCREENSHOTS_SAVE_PATH=SCREENSHOTS_SAVE_PATH, headless=True)

scrapper_bot.webpage_loading()

# scrapper_bot.goto_promotions_section()
scrapper_bot.get_promotion_by_name(student_language=STUDENT_LANGUAGE, student_level=STUDENT_LEVEL)

# scrapper_bot.goto_matieres_section()
for code in STUDENT_ELECTIVE_CLASSES:
    # scrapper_bot.goto_matieres_section()
    scrapper_bot.get_matiere_by_code(class_code=code)