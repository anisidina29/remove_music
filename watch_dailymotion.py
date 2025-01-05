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
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
import os

# Automatically install the ChromeDriver and get its path
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

# Hàm để chạy một instance của trình duyệt Chrome
def run_chrome_instance(instance_id):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Check if the OS is Ubuntu and enable headless mode if true
    if platform.system() == 'Linux' and 'ubuntu' in platform.version().lower():
        chrome_options.add_argument("--headless")
    
    # Open Chrome
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        driver.set_page_load_timeout(120)  # Increased page load timeout
        driver.implicitly_wait(10)  # Explicitly set implicit wait to 10 seconds

        driver.get("https://www.dailymotion.com/playlist/x977b6")
    except TimeoutException as e:
        print(f"Error: Page load timed out for instance {instance_id}. Retrying...")
        driver.quit()
        return  
    
    while True:
        perform_human_like_actions(driver, driver.find_element(By.XPATH, '//body'))
        # Chụp ảnh mỗi 60 giây
        time.sleep(60)
        driver.save_screenshot(f"{output_dir}/screenshot_{instance_id}_{time.time()}.png")

# Số lượng threads (trình duyệt Chrome) cần mở
num_threads = 3

# Khởi tạo và chạy nhiều threads
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=run_chrome_instance, args=(i + 1,))
    threads.append(thread)
    thread.start()

# Đợi các threads kết thúc (trong trường hợp này sẽ không bao giờ kết thúc)
for thread in threads:
    thread.join()
