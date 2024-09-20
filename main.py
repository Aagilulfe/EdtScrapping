from scrapper import Scrapper
import os

"""""""""""Student Info"""""""""""

STUDENT_PROMOTIONS = [("Polonais", "L3"), ("Relations International (RI)", "L3")]
STUDENT_ELECTIVE_CLASSES = ["ECOA330c", "ENJB240a"]


"""""""""""""""Paths"""""""""""""""

DRIVER_PATH = 'drivers/geckodriver'
SCREENSHOTS_SAVE_PATH = 'screenshots/'

if not(os.path.isdir('screenshots')):
    print("No directory for output screenshots. Creating one...\n")
    os.makedirs('screenshots')

# Folder cleaning
for file in os.listdir(SCREENSHOTS_SAVE_PATH):
    os.remove(SCREENSHOTS_SAVE_PATH + file)


# Scrapper instanciation
scrapper_bot = Scrapper(DRIVER_PATH=DRIVER_PATH, SCREENSHOTS_SAVE_PATH=SCREENSHOTS_SAVE_PATH, headless=True)

scrapper_bot.webpage_loading()

for name in STUDENT_PROMOTIONS:
    scrapper_bot.get_promotion_by_name(student_language=name[0], student_level=name[1])

for code in STUDENT_ELECTIVE_CLASSES:
    scrapper_bot.get_matiere_by_code(class_code=code)