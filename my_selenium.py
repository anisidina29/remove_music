import time
import threading
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Automatically install the ChromeDriver and get its path
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
]

def create_driver(user_agent):
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={user_agent}")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def scroll_down(driver):
    for _ in range(10):
        driver.execute_script("window.scrollBy(0, 300);")
        random_delay(1, 3)

def random_delay(min_seconds=1, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def perform_human_like_actions(driver, element):
    actions = ActionChains(driver)
    
    # Hover over the element before clicking
    actions.move_to_element(element).perform()
    random_delay(0.5, 1.0)
    
    # Generate random offset within element boundaries
    offset_x = random.randint(-element.size['width'] // 4, element.size['width'] // 4)
    offset_y = random.randint(-element.size['height'] // 4, element.size['height'] // 4)
    
    # Move to a random position within the element
    actions.move_by_offset(offset_x, offset_y).click().perform()
    print(f"Clicked at offset ({offset_x}, {offset_y})")
    
    # Reset the offset
    actions.move_by_offset(-offset_x, -offset_y).perform()

def run_thread(links, thread_id):
    DRIVERS = 3
    drivers = []
    
    for i in range(DRIVERS):
        drivers.append(create_driver())
        drivers[i].get(links[i])
        perform_human_like_actions(drivers[i])
    
    # Determine the random run time in seconds (between 3 and 30 minutes)
    run_time = random.randint(600, 1800)  # 180 seconds to 1800 seconds (3 to 30 minutes)
    start_time = time.time()
    
    while time.time() - start_time < run_time:
        # Sleep for a random amount of time between 1 and 5 minutes
        sleep_time = random.randint(60, 300)  # 60 seconds to 300 seconds (1 to 5 minutes)
        time.sleep(sleep_time)
        
        for j in range(DRIVERS):
            sleep_time = random.randint(1, 10)  # 60 seconds to 300 seconds (1 to 5 minutes)
            time.sleep(sleep_time)
            drivers[j].refresh()
            perform_human_like_actions(drivers[j])
            drivers[j].save_screenshot(f"screenshot_{thread_id}_{time.time()}.png")
            print(f"Screenshot taken for URL {links[j]} by thread {thread_id}")

    # Close all driver instances
    for drv in drivers:
        drv.quit()
        
        
def main():
    user_agent = random.choice(user_agents)
    driver = create_driver(user_agent)
    driver.get("https://www.youtube.com/@Boymuscleworkout/videos")
    driver.implicitly_wait(10)  # Implicit wait to ensure elements are loaded
    
    links = []
    while len(links) < 500:
        elements = driver.find_elements(By.XPATH, '//a[@id="video-title-link"]')
        new_links = [element.get_attribute('href') for element in elements]
        links.extend([link for link in new_links if link not in links])  # Avoid duplicates
        
        print(f"Number of unique links: {len(links)}")
        
        scroll_down(driver)
    
    driver.quit()
    
    chunk_size = 10
    chunks = [links[i:i + chunk_size] for i in range(0, len(links), chunk_size)]
    
    threads = []
    for i, chunk in enumerate(chunks):
        thread = threading.Thread(target=run_thread, args=(chunk, i))
        threads.append(thread)
        random_delay(60, 300)  # Random delay before starting new thread
        thread.start()
        
        if len(threads) >= 10:
            for t in threads:
                t.join()
            threads = []
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
