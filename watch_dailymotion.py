import time
import threading
import random
import platform  # Import platform module
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
from random import shuffle

# Automatically install the ChromeDriver and get its path
chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Check if the OS is Ubuntu and enable headless mode if true
if platform.system() == 'Linux' and 'ubuntu' in platform.version().lower():
    chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.dailymotion.com/playlist/x977b6")
while True:
  time.sleep(60)
  driver.save_screenshot(f"screenshot_{time.time()}.png")

