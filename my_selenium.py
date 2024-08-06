import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Automatically install the ChromeDriver and get its path
chromedriver_autoinstaller.install()

# Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def create_driver():
    return webdriver.Chrome(options=chrome_options)

def run_thread(url, thread_id):
    DRIVERS = 10
    driver = []
    BreakRate = 10 #sec

    for i in range(DRIVERS):
        driver.append(webdriver.Chrome(options=chrome_options))
        driver[i].get(url)
        action = ActionChains(driver[i])
        action.send_keys(Keys.SPACE)
        action.perform()
    
    while True:
        # Simulate user activity
        time.sleep(10)  # Wait for 10 seconds
        
        # Refresh the page and take a screenshot
        driver.refresh()
        action.perform()
        driver.save_screenshot(f"screenshot_{thread_id}_{time.time()}.png")
        print(f"Screenshot taken for URL {url} by thread {thread_id}")

def main():
    # Fetch the list of video links
    driver = create_driver()
    driver.get("https://www.youtube.com/@Boymuscleworkout/videos")
    driver.implicitly_wait(30)  # Implicit wait to ensure elements are loaded
    
    elements = driver.find_elements(By.XPATH, '//a[@id="video-title-link"]')
    links = [element.get_attribute('href') for element in elements]
    print(len(links))
    driver.quit()
    
    # Limit the number of threads
    max_threads = max(len(links), 20)

    threads = []
    for i in range(max_threads):
        thread = threading.Thread(target=run_thread, args=(links[i], i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
