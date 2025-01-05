# import time
# import threading
# import random
# import platform  # Import platform module
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# import chromedriver_autoinstaller
# from random import shuffle
# import os

# # Automatically install the ChromeDriver and get its path
# chromedriver_autoinstaller.install()

# output_dir = 'screenshots/'
# os.makedirs(output_dir, exist_ok=True)

# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# # Check if the OS is Ubuntu and enable headless mode if true
# if platform.system() == 'Linux' and 'ubuntu' in platform.version().lower():
#     chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://www.dailymotion.com/playlist/x977b6")
# while True:
#   time.sleep(60)
#   driver.save_screenshot(f"screenshots/screenshot_{time.time()}.png")

import time
import random
import platform
import threading  # Import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, MoveTargetOutOfBoundsException
import chromedriver_autoinstaller
import geckodriver_autoinstaller
import msedge.selenium_tools as edge_tools
import os

# Automatically install the ChromeDriver, GeckoDriver (Firefox), and Edge Driver
chromedriver_autoinstaller.install()

output_dir = 'screenshots/'
os.makedirs(output_dir, exist_ok=True)

def random_delay(min_seconds=1, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def perform_human_like_actions(driver, element):
    actions = ActionChains(driver)
    try:
        actions.move_to_element(element).perform()
        random_delay(0.5, 1.0)
        offset_x = random.randint(-element.size['width'] // 4, element.size['width'] // 4)
        offset_y = random.randint(-element.size['height'] // 4, element.size['height'] // 4)
        actions.move_by_offset(offset_x, offset_y).click().perform()
        print(f"Clicked at offset ({offset_x}, {offset_y})")
        actions.move_by_offset(-offset_x, -offset_y).perform()
    except MoveTargetOutOfBoundsException:
        print("Move target out of bounds, skipping action")

# Hàm để chạy một instance của trình duyệt
def run_browser_instance(instance_id, browser_type='chrome'):
    if browser_type == 'chrome':
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
    elif browser_type == 'firefox':
        firefox_options = FirefoxOptions()
        firefox_options.headless = False
        driver = webdriver.Firefox(options=firefox_options)
    elif browser_type == 'edge':
        driver = webdriver.Edge()
    else:
        raise ValueError("Unsupported browser type")

    # Tối đa hóa cửa sổ
    driver.maximize_window()
    try:
        driver.set_page_load_timeout(120)  # Increased page load timeout
        driver.get("https://www.dailymotion.com/playlist/x977b6")
    except TimeoutException as e:
        print(f"Error: Page load timed out for instance {instance_id}. Retrying...")
        driver.quit()
        return  # Exit and allow retry or further error handling
    
    while True:
        try:
            perform_human_like_actions(driver, driver.find_element(By.XPATH, '//body'))
            # Chụp ảnh mỗi 60 giây
            time.sleep(60)
            driver.save_screenshot(f"{output_dir}/screenshot_{instance_id}_{time.time()}.png")
        except Exception as e:
            print(f"Error during actions: {e}")
            time.sleep(5)  # Retry after a short delay

# Số lượng threads (trình duyệt cần mở)
num_threads = 4

# Khởi tạo và chạy nhiều threads cho các trình duyệt khác nhau
threads = []
browser_types = ['chrome', 'chrome','chrome', 'chrome','chrome']

for i in range(num_threads):
    browser_type = browser_types[i % len(browser_types)]  # Alternate browsers
    thread = threading.Thread(target=run_browser_instance, args=(i + 1, browser_type))
    threads.append(thread)
    thread.start()

# Đợi các threads kết thúc (trong trường hợp này sẽ không bao giờ kết thúc)
for thread in threads:
    thread.join()

