from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os
import sys
import ddddocr
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from urllib3.exceptions import ReadTimeoutError
from lib.send_ali_sms.sms import send_sms_by_phone
import yaml

max_time = 5


def random_wait_decorator(func):
    def wrapper(*args, **kwargs):
        wait_time = random.uniform(3, max_time)  # 生成 1 到 3 秒之间的随机浮点数
        time.sleep(wait_time)  # 等待随机时间
        return func(*args, **kwargs)  # 调用原始函数

    return wrapper


class Book:
    def __init__(self, login_cnt=-1, password=None,
                 firstTripDate=None, firstTripEndDate=None,
                 firstTripFrom=None, firstTripTo=None,
                 secTripDate=None, secTripEndDate=None,
                 sedTripFrom=None, secTripTo=None, fstTrpClass=None, sndTrpClass=None,
                 phone="18973194769",customers=None
                 ):
        # driver_path = '/chromedriver-mac-arm64/chromedriver'  # 替换为您的 ChromeDriver 路径
        self.chrome_service = Service('chromedriver.exe')
        # 设置 Chrome 选项
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--incognito')
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--no-sanbox')
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("start-maximized")
        self.chrome_options.add_argument("enable-automation")
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument('--disable-web-security')
        # chrome_options.add_argument('--user-data-dir')
        self.chrome_options.add_argument('--allow-running-insecure-content')
        self.chrome_options.add_argument('--incognito')
        self.chrome_options.add_argument('--enable-unsafe-swiftshader')


        self.driver = webdriver.Chrome(service=self.chrome_service, options=self.chrome_options)
        # self.driver.implicitly_wait(10)
        self.url = "https://www.ana.co.jp/zh/cn/"
        self.wait = WebDriverWait(self.driver, 30)
        self.firstTripDate = firstTripDate
        self.firstTripEndDate = firstTripEndDate
        self.firstTripFrom = firstTripFrom
        self.firstTripTo = firstTripTo
        self.secTripDate = secTripDate
        self.secTripEndDate = secTripEndDate
        self.sedTripFrom = sedTripFrom
        self.secTripTo = secTripTo
        # self.username = username
        self.login_cnt = login_cnt
        self.password = password
        self.logout_times = 0
        self.fstTrpClass = fstTrpClass
        self.sndTrpClass = sndTrpClass
        self.fstLine = None
        self.sndLine = None
        self.fstDate = None
        self.sndDate = None
        self.phone = phone
        self.customers = customers

    @random_wait_decorator
    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @random_wait_decorator
    def send_keys_to_element(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.send_keys(text)

    @random_wait_decorator
    def wait_element(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except:
            pass

    @random_wait_decorator
    def wait_element_show(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @random_wait_decorator
    def wait_elements_return(self, locator):

        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except:
            return None

    def login(self):
        self.wait_element((By.XPATH, '//*[@data-scclick="zh_cn_TOP_txt_登录"and text()="登录"]'))
        self.driver.execute_script("document.body.style.zoom='60%'")

        elements = self.wait_elements_return((By.XPATH, '//*[@data-scclick="zh_cn_TOP_txt_登录"and text()="登录"]'))
        # 点击第一个元素（索引为0）
        if elements:
            elements[0].click()

        # 找到用户名和密码输入框
        self.wait_element((By.NAME, 'member_no'))
        self.wait_element((By.NAME, 'member_password'))
        # username_input = self.driver.find_element(By.NAME, 'member_no')  # 替换为实际的用户名输入框的选择器
        # password_input = self.driver.find_element(By.NAME, 'member_password')  # 替换为实际的密码输入框的选择器
        username_input = self.wait_element((By.NAME, 'member_no'))  # 替换为实际的用户名输入框的选择器)
        password_input = self.wait_element((By.NAME, 'member_password'))  # 替换为实际的密码输入框的选择器

        # 输入用户名和密码
        self.click_element(username_input)
        self.login_cnt += 1
        username_input.send_keys(self.customers[self.login_cnt % 4])
        self.click_element(password_input)
        password_input.send_keys(self.password)

        ele = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="asw-tab__item-box-1"]')))
        # ele = self.driver.find_element(By.XPATH, '//div[@id="asw-tab__item-box-1"]')
        self.driver.execute_script("arguments[0].scrollTop=arguments[0].scrollHeight", ele)
        self.click_element((By.ID, "login"))

        # time.sleep(3)
        ele = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="继续（登录）"]')))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", ele)
        # ele = WebDriverWait(self.driver, 30).until(
        #     EC.presence_of_element_located((By.XPATH, '//div[@class="asw-modal__body asw-scroll ps ps--active-y"]')))
        # ele = self.driver.find_element(By.XPATH, '//div[@class="asw-modal__body asw-scroll ps ps--active-y"]')
        # self.driver.execute_script("arguments[0].scrollTop=arguments[0].scrollHeight", ele)
        # ele = self.driver.find_element(By.XPATH, '//div[@class="asw-modal__body asw-scroll ps ps--active-y"]')
        # self.driver.execute_script("arguments[0].scrollTop=arguments[0].scrollHeight", ele)
        # if ele:
        #     self.driver.execute_script("arguments[0].scrollTop=arguments[0].scrollHeight", ele)
        # self.click_element((By.ID, "login"))
        self.click_element((By.XPATH, '//span[text()="继续（登录）"]'))
        # print("clicked ....")

    def run(self, first=True):
        try:
            # 打开登录页面
            if first:
                self.driver.execute_script("navigator.webdriver = undefined;")  # 使 webdriver 属性为 undefined
                self.driver.get(self.url)  # 替换为您的登录页面 URL
                # 最大化窗口

                self.driver.maximize_window()
                self.driver.execute_script("document.body.style.zoom='60%'")
                self.login()
            else:
                self.driver.execute_script("document.body.style.zoom='60%'")

            self.wait_element((By.XPATH, '//span[text()="里程兑换机票"]'))
            self.click_element((By.XPATH, '//span[text()="里程兑换机票"]'))
            # 获取当前窗口句柄
            original_window = self.driver.current_window_handle
            self.click_element((By.XPATH, '//span[text()="[国际线]里程奖励机票预订"]'))

            # 点击会打开新窗口的元素
            # print(self.driver.current_window_handle.title())

            for handle in self.driver.window_handles:
                if handle != original_window:
                    self.driver.switch_to.window(handle)
                    if first:
                        break
            self.driver.execute_script("document.body.style.zoom='60%'")

            time.sleep(random.randint(1, 5))
            self.click_element((By.XPATH, '//a[text()="Multiple cities/Mixed classes"]'))
            # 第一段Trip
            From1 = (By.XPATH,
                     '//input[@id="requestedSegment:0:departureAirportCode:field_pctext"]')
            self.send_keys_to_element(From1, self.firstTripFrom)
            self.send_keys_to_element(From1, Keys.ENTER)
            To1 = (By.XPATH, '//input[@id="requestedSegment:0:arrivalAirportCode:field_pctext"]')
            self.send_keys_to_element(To1, self.firstTripTo)
            self.send_keys_to_element(To1, Keys.ENTER)
            # 第二段Trip
            From2 = (By.XPATH,
                     '//input[@id="requestedSegment:1:departureAirportCode:field_pctext"]')
            self.send_keys_to_element(From2, self.sedTripFrom)
            self.send_keys_to_element(From2, Keys.ENTER)
            To2 = (By.XPATH,
                   '//input[@id="requestedSegment:1:arrivalAirportCode:field_pctext"]')
            self.send_keys_to_element(To2, self.secTripTo)
            self.send_keys_to_element(To2, Keys.ENTER)
            self.traverseDateSelBusTrip(self.firstTripDate, 0)
            self.traverseDateSelBusTrip(self.secTripDate, 1)

            self.click_element((By.XPATH, '//input[@value="Search"]'))
            # 下载图片并解析
            if first:
                self.decodeImgSend(True)

            self.secSeatsBook()

        finally:
            # 关闭浏览器
            input("input Enter:  ")
            self.driver.quit()

    def traverseFirDateSelBusTrip(self, newDate):
        self.click_element((By.XPATH, '//input[@id="requestedSegment:0:departureDate:field_pctext"]'))
        while True:
            try:
                self.click_element((By.XPATH, f'//td[@abbr="{newDate}"]'))
                break
            except:
                self.click_element((By.XPATH, '//a[text()="Next 3 months"]'))

    def traverseDateSelBusTrip(self, newDate, trip=0):
        if trip == 0:
            self.click_element((By.XPATH, '//input[@id="requestedSegment:0:departureDate:field_pctext"]'))
        else:
            self.click_element((By.XPATH, '//input[@id="requestedSegment:1:departureDate:field_pctext"]'))

        while True:
            try:
                self.click_element((By.XPATH, f'//td[@abbr="{newDate}"]'))
                break
            except:
                self.click_element((By.XPATH, '//a[text()="Next 3 months"]'))

    def tripDateadd(self, oridate):
        date_obj = datetime.strptime(oridate, "%Y-%m-%d")
        new_date_obj = date_obj - timedelta(days=1)
        new_date_str = new_date_obj.strftime("%Y-%m-%d")
        return new_date_str

    def logout(self):
        self.logout_times += 1
        # print(f"system has been logout for {self.logout_times} times")
        print(f"system has been logout for {self.logout_times} times")
        # eles = self.driver.find_elements(By.XPATH, '//a[text()="退出" or text()="Logout"]')
        eles = self.wait_elements_return((By.XPATH, '//a[text()="退出" or text()="Logout"]'))
        eles[0].click()
        try:
            # self.driver.find_element(By.XPATH, '//a[@id="continue-logout"]').click()
            self.click_element((By.XPATH, '//a[@id="continue-logout"]'))
        except:
            # pass
            # self.driver.find_element(By.XPATH, '//input[@value="Return to Top Page"]').click()
            self.click_element((By.XPATH, '//input[@value="Return to Top Page"]'))
        current_window = self.driver.current_window_handle
        for handle in self.driver.window_handles:
            if handle != current_window:
                self.driver.switch_to.window(handle)
                self.driver.close()
        self.driver.switch_to.window(current_window)
        self.login()
        self.run(False)

    def longtime_no_resp(self):
        # self.logout_times += 1
        # print(f"system has been logout for {self.logout_times} times")
        # print(f"system has been logout for {self.logout_times} times")
        # eles = self.driver.find_elements(By.XPATH, '//a[text()="退出" or text()="Logout"]')
        # eles[0].click()
        # self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.F5)
        self.send_keys_to_element((By.TAG_NAME, 'body'), Keys.F5)
        print(self.driver.current_url)
        print("==========")
        # self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + "r")
        self.send_keys_to_element((By.TAG_NAME, 'body'), Keys.CONTROL + "r")

        print(self.driver.current_url)
        print("==========")
        # self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + "R")
        self.send_keys_to_element((By.TAG_NAME, 'body'), Keys.CONTROL + "R")
        print(self.driver.current_url)
        print("==========")
        self.driver.get(self.driver.current_url)
        # self.driver.find_element(By.XPATH, '//input[@value="确认"]').click()
        self.click_element((By.XPATH, '//input[@value="确认"]'))
        self.logout()

    def search_all_but_without_match(self):
        try:
            # self.driver.find_element(By.XPATH, '//strong[text()="(E_A02P02_0010)"]')
            self.wait_element((By.XPATH, '//strong[text()="(E_A02P02_0010)"]'))
            # print(True)
            # eles = self.driver.find_elements(By.XPATH, '//input[@value="Close"]')
            eles = self.wait_elements_return((By.XPATH, '//input[@value="Close"]'))
            eles[1].click()
            # self.logout()
            return True
        except:
            # print(False)
            return False

    def seatsSelection(self, trip=0, date=None):
        if not self.search_all_but_without_match():
            # eles = self.driver.find_elements(By.XPATH, '//tr[@class="oneWayDisplayPlan"]')
            eles = self.wait_elements_return((By.XPATH, '//tr[@class="oneWayDisplayPlan"]'))
            path = ""
            if trip == 0:
                if self.fstTrpClass == "Economy":
                    path = "E"
                elif self.fstTrpClass == "Preminum Economy":
                    path = "N"
                elif self.fstTrpClass == "Business":
                    path = "B"
                elif self.fstTrpClass == "First":
                    path = "F"
            elif trip == 1:
                if self.sndTrpClass == "Economy":
                    path = "E"
                elif self.sndTrpClass == "Preminum Economy":
                    path = "N"
                elif self.sndTrpClass == "Business":
                    path = "B"
                elif self.sndTrpClass == "First":
                    path = "F"
            for i in range(len(eles)):  # 4 --> //tr[@class="oneWayDisplayPlan"]  get the data #
                try:
                    res = self.driver.find_element(By.XPATH, f'//td[@id="departureFlight_{i}_{path}"]//span').text
                    if res is not None and res.count('Seats available') != 0:
                        self.click_element((By.XPATH, f'//td[@id="departureFlight_{i}_{path}"]//span'))
                        if trip == 0:
                            self.fstLine = [line for line in res.split() if line.__contains__("Flight")][0].replace(",",
                                                                                                                    "")
                            if date:
                                self.fstDate = date
                        elif trip == 1:
                            self.sndLine = [line for line in res.split() if line.__contains__("Flight")][0].replace(",",
                                                                                                                    "")
                            if date:
                                self.sndDate = date
                        return True
                except:
                    pass
            return False
        else:
            return False

    def secSeatsBook(self, recursive=100):
        recursive -= 1
        newdate = self.firstTripDate
        fir_overall_falg = False
        while True:
            try:
                if self.seatsSelection(trip=0, date=newdate):
                    break
                else:
                    newdate = self.tripDateadd(newdate)
                    if newdate >= self.firstTripEndDate:
                        # click search  and input new date
                        self.click_element((By.XPATH, '//a[text()="Search Again"]'))
                        self.traverseDateSelBusTrip(newdate)
                        self.click_element((By.XPATH, '//input[@value="Search"]'))
                    else:
                        print(f"could not find seats for Business even on {self.firstTripEndDate}")
                        fir_overall_falg = True
                        break
            except ReadTimeoutError:
                self.longtime_no_resp()
        if fir_overall_falg:
            self.logout()

        self.click_element((By.ID, "nextButton"))
        sec_overall_falg = False
        newdate = self.secTripDate
        while True:
            try:
                if self.seatsSelection(trip=1, date=newdate):
                    break
                else:
                    newdate = self.tripDateadd(newdate)
                    if newdate >= self.secTripEndDate:
                        #     click search  and input new date
                        self.click_element((By.XPATH, '//a[text()="Search Again"]'))
                        self.traverseDateSelBusTrip(newdate, trip=1)
                        self.click_element((By.XPATH, '//input[@value="Search"]'))
                        self.seatsSelection(trip=0)
                        self.click_element((By.ID, "nextButton"))
                    else:
                        print(f"could not find seats for Business even on {self.secTripEndDate}")
                        sec_overall_falg = True
                        break
            except ReadTimeoutError:
                self.longtime_no_resp()
        if sec_overall_falg:
            self.logout()

        self.click_element((By.ID, "nextButton"))
        # 点击按钮
        eles = self.wait_elements_return((By.XPATH, '//input[@type="submit" and @value="Confirm"]'))
        if not eles:
            eles = self.driver.find_elements(By.XPATH, '//input[@type="submit" and @value="Confirm"]')
        for ele in eles:
            try:
                ele.click()
            except:
                pass
        cusname = self.customers[self.login_cnt % 4]
        print(f"当前用户名： {cusname}")
        print(f"第一班日期： {self.fstDate}")
        print(f"第一班班次： {self.fstLine}")
        print(f"第二班日期： {self.sndDate}")
        print(f"第二班班次： {self.sndLine}")
        send_sms_by_phone(phone=self.phone, name='T' + cusname[5:], airline=self.fstLine[6:], time=self.fstDate)

        time.sleep(random.randint(1, max_time))
        self.driver.get_screenshot_as_file('Result.png')  # 将截图保存为 screenshot.png
        # print("截图已保存为 Result.png")

    def decodeImgSend(self, first=True):
        if first:
            # 等待 img 元素可见
            self.wait_element((By.XPATH, '//div[@class="captcha"]/img'))

        self.delImg('captcha.png')
        image_element = self.driver.find_element(By.XPATH, '//div[@class="captcha"]/img')
        image_element.screenshot('captcha.png')  # 将元素截图保存为 image_screenshot.png
        # print("图像已保存为 captcha.png")
        with open('captcha.png', 'rb') as f:
            img_bytes = f.read()
        ocr = ddddocr.DdddOcr(show_ad=False)
        code = ocr.classification(img_bytes)
        # print(code)

        self.send_keys_to_element((By.XPATH, '//input[@id="captchaInput"]'), code)
        self.click_element((By.XPATH, '//input[@value="Authentication"]'))
        # time.sleep(3)

        if self.wait_element_show((By.XPATH, '//h2[contains(text(), "Destination 1")]')):
            return True
        else:
            # 第一次输入报错的情形
            self.wait_element((By.XPATH, '//div[@class="modalContainer modalError modalSmall "]'))
            eles = self.wait_elements_return((By.XPATH, '//*[@value="Close"]'))
            if not eles:
                eles = self.driver.find_elements(By.XPATH, '//*[@value="Close"]')
            eles[1].click()
            self.wait_element((By.XPATH, '//input[@id="captchaInput"]'))
            self.driver.find_element(By.XPATH, '//input[@id="captchaInput"]').clear()
            self.decodeImgSend(False)
            # 第二次输入报错
            if self.wait_element_show((By.XPATH, '//*[@id="cmnContainer"]/div[2]/ul/li')):
                error = self.driver.find_element(By.XPATH, '//*[@id="cmnContainer"]/div[2]/ul/li').text
                # print(error)
                # 可以点击确认，重新回到 点击 【里程兑换机票】 页面
                self.driver.find_element(By.XPATH, '//input[@value="确认"]').click()
                # self.run(False)
                print("image 解析2次均失败，窗口提示报错，重新登录")
                # 可以点击退出重新登录
                self.logout()

    def delImg(self, file_name):
        # 检查文件是否存在
        if os.path.isfile(file_name):
            # 删除文件
            os.remove(file_name)
            # print(f"{file_name} 已被删除。")
        else:
            print(f"{file_name} 不存在。")





def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    configpath = get_resource_path('config.yaml')
    if not os.path.exists(configpath):
        print(f"Configuration file does not exist at: {configpath}")
    else:
        with open('config.yaml', 'r', encoding='utf-8') as config_file:
            config = yaml.safe_load(config_file)

        book = Book(password=config['password'],
                    firstTripDate=config['firstTripDate'], firstTripEndDate=config['firstTripEndDate'],
                    firstTripFrom=config['firstTripFrom'], firstTripTo=config['firstTripTo'],
                    secTripDate=config['secTripDate'], secTripEndDate=config['secTripEndDate'],
                    sedTripFrom=config['sedTripFrom'], secTripTo=config['secTripTo'], fstTrpClass=config['fstTrpClass'],
                    sndTrpClass=config['sndTrpClass'],
                    phone=config['phone'],
                    customers=config['Customers']
                    )
        res = book.run(True)
        print(res)
