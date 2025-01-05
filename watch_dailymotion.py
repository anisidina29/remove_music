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

# Hàm để chạy một instance của trình duyệt Chrome
def run_chrome_instance(instance_id):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Check if the OS is Ubuntu and enable headless mode if true
    if platform.system() == 'Linux' and 'ubuntu' in platform.version().lower():
        chrome_options.add_argument("--headless")

    # Mở Chrome
    driver = webdriver.Chrome(options=chrome_options)
    # Tối đa hóa cửa sổ
    driver.maximize_window()
    try:
        driver.set_page_load_timeout(120)  # Increased page load timeout
        driver.get("https://www.dailymotion.com/playlist/x977b6")
    except TimeoutException as e:
        print(f"Error: Page load timed out for instance {instance_id}. Retrying...")
        driver.quit()
        return  # Exit and allow retry or further error handling
    
    # Lấy kích thước của viewport
    viewport_width = driver.execute_script("return parseInt(window.innerWidth / 2, 10)")
    viewport_height = driver.execute_script("return parseInt(window.innerHeight / 2, 10)")
    
    # Khởi tạo ActionChains
    action = ActionChains(driver)

    while True:
        # Di chuyển chuột ngẫu nhiên
        random_x = random.randint(0, viewport_width - 5)
        random_y = random.randint(0, viewport_height - 5)
        action.move_by_offset(random_x, random_y).perform()  # Di chuyển chuột
        time.sleep(random.uniform(1, 3))  # Thời gian di chuyển ngẫu nhiên
        # Di chuyển chuột đến một vị trí khác mỗi phút
        action.move_to_element_with_offset(driver.find_element(By.TAG_NAME, 'body'), random_x, random_y).perform()
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
