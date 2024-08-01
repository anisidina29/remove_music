from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import threading
import multiprocessing
import psutil

def run_thread(keyword):
    driver = webdriver.Chrome()

    try: 
        driver.get("https://www.youtube.com/")
        search_box = driver.find_element(By.XPATH, '//input[@id="search"]')
        search_box.send_keys("@Boymuscleworkout")
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        video_link = driver.find_element(By.XPATH, '//*[@id="subscribers" and contains(text(), "@Boymuscleworkout")]')
        video_link.click()
        time.sleep(5)

        playlists = driver.find_element(By.XPATH, '//yt-tab-shape[@tab-title="Playlists"]')
        playlists.click()
        time.sleep(5)
        watch_video = driver.find_element(By.XPATH, '//a[@id="video-title" and contains(text(), "{}")]'.format(keyword))
        watch_video.click()
        time.sleep(10)
        # Define the XPath of the button
        xpath = '//button[@aria-label="Loop playlist"]'

        # Find the button element by XPath
        element = driver.find_element(By.XPATH, xpath)

        # Click the button using JavaScript
        driver.execute_script("arguments[0].click();", element)

        while True:
            driver.save_screenshot("screenshot_{}_{}.png".format(keyword, time.time()))
            print("Screenshot taken for keyword: {}".format(keyword))
            time.sleep(300)

        driver.quit()
    
    except:
        driver.get("https://www.youtube.com/@Boymuscleworkout/playlists")
        time.sleep(10)
        watch_video = driver.find_element(By.XPATH, '//a[@id="video-title" and contains(text(), "{}")]'.format(keyword))
        watch_video.click()
        time.sleep(10)
        # Define the XPath of the button
        xpath = '//button[@aria-label="Loop playlist"]'

        # Find the button element by XPath
        element = driver.find_element(By.XPATH, xpath)

        # Click the button using JavaScript
        driver.execute_script("arguments[0].click();", element)

        while True:
            driver.save_screenshot("screenshot_{}_{}.png".format(keyword, time.time()))
            print("Screenshot taken for keyword: {}".format(keyword))
            time.sleep(300)

        driver.quit()

def resource_check():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    return cpu_usage < 90 and ram_usage < 90

def run_process(elements):
    threads = []
    element_index = 0

    while True:
        if element_index >= len(elements):
            break
        
        if resource_check():
            element = elements[element_index]
            thread = threading.Thread(target=run_thread, args=(element,))
            thread.start()
            threads.append(thread)
            element_index += 1
        else:
            print("High resource usage detected. Waiting...")
            time.sleep(60)  # Chờ một chút trước khi kiểm tra lại

    # Chờ tất cả các thread hoàn thành
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    elements = ["honguynvn04", "hieuvilai2007"]
    elements = elements * 600  # Lặp lại các phần tử để tạo danh sách dài hơn

    num_processes = multiprocessing.cpu_count() - 2
    processes = []
    for i in range(num_processes):
        process = multiprocessing.Process(target=run_process, args=(elements,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    print("Done!")
