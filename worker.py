import base64
import os
import platform
import random
import time
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

def main(address="127.0.0.1", port=3333, headless=False, workers=2, delay=2):
    def task(thread_id):
        time.sleep(thread_id * delay)
        driver = create_driver(f"http://{address}:{port}/task", headless=headless)
        while True:
            try:
                crack_geetest(driver)
                time.sleep(2)
            except:
                time.sleep(1)
    
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(task, range(workers))

def create_driver(url, headless=False):
    options = webdriver.ChromeOptions()
    options.add_argument("log-level=3")
    if headless:
        options.add_argument("headless")
    else:
        options.add_argument("disable-infobars")
        options.add_argument("window-size=380,460")
    if platform.system() == "Linux":
        options.add_argument("no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

def crack_geetest(driver, bg_class="geetest_canvas_bg geetest_absolute", full_bg_class="geetest_canvas_fullbg geetest_fade geetest_absolute", slider_class="geetest_slider_button", success_class="geetest_success"):
    driver.find_element_by_class_name(slider_class)
    rand = str(random.randint(0, 100000000))
    bg_path = save_bg(driver, bg_path=os.path.join("tmp", f"bg_{rand}.png"), bg_class=bg_class)
    full_bg_path = save_full_bg(driver, full_bg_path=os.path.join("tmp", f"fullbg_{rand}.png"), full_bg_class=full_bg_class)
    distance = get_offset(full_bg_path, bg_path) - 4
    os.remove(full_bg_path)
    os.remove(bg_path)
    track = get_track(distance)
    drag_the_ball(driver, track, slider_class=slider_class)

def save_base64img(data_str, save_name):
    img_data = base64.b64decode(data_str)
    file = open(save_name, "wb")
    file.write(img_data)
    file.close()

def get_base64_by_canvas(driver, class_name, contain_type):
    bg_img = ""
    while len(bg_img) < 5000:
        get_img_js = f"return document.getElementsByClassName(\"{class_name}\")[0].toDataURL(\"image/png\");"
        bg_img = driver.execute_script(get_img_js)
        time.sleep(0.5)
    if contain_type:
        return bg_img
    else:
        return bg_img[bg_img.find(",") + 1:]

def save_bg(driver, bg_path="bg.png", bg_class="geetest_canvas_bg geetest_absolute"):
    bg_img_data = get_base64_by_canvas(driver, bg_class, False)
    save_base64img(bg_img_data, bg_path)
    return bg_path

def save_full_bg(driver, full_bg_path="fbg.png", full_bg_class="geetest_canvas_fullbg geetest_fade geetest_absolute"):
    bg_img_data = get_base64_by_canvas(driver, full_bg_class, False)
    save_base64img(bg_img_data, full_bg_path)
    return full_bg_path

def get_slider(driver, slider_class="geetest_slider_button"):
    while True:
        try:
            slider = driver.find_element_by_class_name(slider_class)
            break
        except:
            time.sleep(0.5)
    return slider

def is_pixel_equal(img1, img2, x, y):
    pix1 = img1.load()[x, y]
    pix2 = img2.load()[x, y]
    threshold = 60
    if abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(pix1[2] - pix2[2] < threshold):
        return True
    else:
        return False

def get_offset(full_bg_path, bg_path, initial_offset=39):
    full_bg = Image.open(full_bg_path)
    bg = Image.open(bg_path)
    left = initial_offset
    for i in range(left, full_bg.size[0]):
        for j in range(full_bg.size[1]):
            if not is_pixel_equal(full_bg, bg, i, j):
                left = i
                return left
    return left

def get_track(distance):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = random.randint(2, 3) / 10
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track

def drag_the_ball(driver, track, slider_class="geetest_slider_button"):
    slider = get_slider(driver, slider_class)
    ActionChains(driver).click_and_hold(slider).perform()
    while track:
        x = random.choice(track)
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
        track.remove(x)
    time.sleep(0.1)
    imitate = ActionChains(driver).move_by_offset(xoffset=-1, yoffset=0)
    time.sleep(0.015)
    imitate.perform()
    # time.sleep(random.randint(6, 10) / 10)
    imitate.perform()
    time.sleep(0.04)
    imitate.perform()
    time.sleep(0.012)
    imitate.perform()
    time.sleep(0.019)
    imitate.perform()
    time.sleep(0.033)
    ActionChains(driver).move_by_offset(xoffset=1, yoffset=0).perform()
    ActionChains(driver).pause(random.randint(6, 14) / 10).release(slider).perform()

if __name__ == "__main__":
    main()
