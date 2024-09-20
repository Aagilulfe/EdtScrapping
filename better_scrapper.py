from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from typing import Type

"""
Enhanced scrapping class for INALCO hyperplanning

"""

class BetterScrapper():

    def __init__(self, DRIVER_PATH: str, SCREENSHOTS_SAVE_PATH: str, inalco_url="https://planning.inalco.fr/public", headless=True, window_size="--window-size=1920,1200") -> None:
        pass