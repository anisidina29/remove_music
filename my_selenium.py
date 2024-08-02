from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import threading
import multiprocessing


def run_thread(keyword):
    driver = webdriver.Chrome()

    try: 
        driver.get("https://www.youtube.com/")

        # Tìm ô tìm kiếm
        search_box = driver.find_element(By.XPATH, '//input[@id="search"]')

        # Gõ từ khóa vào ô tìm kiếm
        search_box.send_keys("@Boymuscleworkout")

        # Nhấn Enter để tìm kiếm
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        # Tìm và nhấp vào liên kết của kênh
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
            # Chụp ảnh màn hình
            driver.save_screenshot("screenshot_{}_{}.png".format(keyword, time.time()))
            print("Screenshot taken for keyword: {}".format(keyword))

            # Chờ 10 phút trước khi chụp ảnh màn hình tiếp theo
            time.sleep(300)

        #Đóng trình duyệt khi kết thúc
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
            # Chụp ảnh màn hình
            driver.save_screenshot("screenshot_{}_{}.png".format(keyword, time.time()))
            print("Screenshot taken for keyword: {}".format(keyword))

            # Chờ 10 phút trước khi chụp ảnh màn hình tiếp theo
            time.sleep(300)

        # Đóng trình duyệt khi kết thúc
        driver.quit()
# elements = ['kimnguyennanh', 'hmatuan9', 'rforrachman', 'mixed', 'tuangym98', 'huutinh103', 'bimostreetworkout', 'duongkimmochii', 'honguynvn04', 'buiquoc_sw', 'Hpp358965']
# elements = elements + elements
# # Số lượng luồng bạn muốn chạy
# n_threads = len(elements)

def run_process(elements):
    # Tạo và khởi chạy các luồng trong mỗi process
    threads = []
    for element in elements:
            thread = threading.Thread(target=run_thread, args=(element,))
            thread.start()
            threads.append(thread)

    # Chờ tất cả các luồng hoàn thành trong mỗi process
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    # List các elements bạn muốn xử lý
    elements = ["honguynvn04", "hieuvilai2007"]
    elements = elements + elements + elements + elements + elements + elements

    # Số lượng process muốn tạo, có thể sử dụng multiprocessing.cpu_count() để lấy số lượng core CPU
    num_processes = multiprocessing.cpu_count() - 2

    # Tạo và khởi chạy các process
    processes = []
    for i in range(num_processes):
        process = multiprocessing.Process(target=run_process, args=(elements,))
        process.start()
        processes.append(process)

    # Chờ tất cả các process hoàn thành
    for process in processes:
        process.join()

    print("Done!")
