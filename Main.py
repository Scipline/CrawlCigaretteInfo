"""
@Author       : XiaoZong
@Since        : 2023-1-7 13:20:23
@LastEditor   : XiaoZong
@LastEditTime : 2023-1-8 23:35:38
@FileName     : Main .py
@Description  :selenium4.7.2，chrome107.0.5304.63。需要手动填写验证码并登录。爬取广东烟草电子商务网站所有香烟名字和图片，批发价和零售价
"""
import csv
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
options = Options()  # 新版加启动配置
options.binary_location = r"D:\DownSoft\Chrome\App\chrome.exe"  # 指定chrome程序路径
options.add_argument('–headless')  # 无头浏览模式
options.add_argument('--no-sandbox')  # 在 root 权限下运行。指定第三方浏览器时地址栏只显示data，需要加此行
options.add_argument("--no-referrers")  # 不发送 Http-Referer 头
options.add_argument("--start-maximized")  # 启动时窗口最大化
# options.add_argument('–homedir={}')  # 指定主目录存放位置
# options.add_argument('--disk-cache-dir={临时文件目录}')  # 指定临时文件目录
options.add_argument("--ignore-certificate-errors")  # 忽略不信任证书
options.add_argument('--ignore-ssl-errors')  # 处理SSL证书错误问题
options.add_argument('--disable-setuid-sandbox')  # 禁用沙盒
options.add_argument('--disable-notifications')  # 禁用通知警告
options.add_argument('--disable-dev-shm-usage')  # 使用硬盘来存储获取的内容，而不是使用内存.大量渲染时候写入/tmp而非/dev/shm
options.add_argument('--disable-infobars')  # 禁用提示
options.add_argument('--disable-web-security')  # 关闭安全策略
options.add_argument('--disable-xss-auditor')  # 禁止xss防护
options.add_argument("--disable-popup-blocking")  # 允许弹窗
options.add_argument("--disable-java")  # 禁用 java
options.add_argument("--disable-javascript")  # 禁用Javascript
options.add_argument('--disable-extensions')  # 禁用扩展
options.add_argument('--disable-webgl')  # 禁用webgl
options.add_argument("-–no-first-run")  # 初始化时为空白页面
options.add_argument(
    "--disable-blink-features=AutomationControlled")  # 除window.navigator.webdriver，否则调用远程webdriver时则会报错
options.add_argument('--no-default-browser-check')  # 不做浏览器默认检查
options.add_experimental_option('useAutomationExtension', False)  # 去除新版本 chrome 取消‘Chrome 正在受到自动软件的控制’提示
options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])  # 忽略无用的日志
# options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 设置开发者模式启动，该模式下webdriver属性为正常值
options.add_argument("--user-data-dir=D:\\DownSoft\\Chrome\\Data\\Default")  # 加载配置启动浏览器，不然就以一个全新的浏览窗口启动
options.add_experimental_option("detach", True)
s = Service("chromedriver.exe")
driver = webdriver.Chrome(options=options, service=s)
driver.implicitly_wait(10)  # 隐式等待。网页加载数据需要时间，智能化等待。
driver.get('https://www.yueyigou.com/wdk?action=ecw.page&method=display&site_id=maoming&inclient=&page_id=page_cigalist')

# E1=driver.find_element(By.ID, 'login_username')
# E2=driver.find_element(By.ID, 'login_userpwd')
# E1.clear()
# E1.send_keys("账号")
# E2.clear()
# E2.send_keys("密码")

# 10秒内手动填写验证码并点击登录
time.sleep(10)
driver.get('https://www.yueyigou.com/wdk?action=ecw.page&method=display&site_id=maoming&inclient=&page_id=page_cigalist')
name_ciga_all = []
price_buy_all = []
price_sale_all = []
photo_urls = []
page = driver.find_element(By.CLASS_NAME, 'page_bar')
totalpage = driver.find_element(By.XPATH, '//*[@id="page_bar"]/div/span[2]').text.replace("共", "").replace("页", "")


def get_info():
    name_ciga = [p.text for p in driver.find_elements(By.CLASS_NAME, 'ciga_list_list_item_title')]
    photo = driver.find_elements(By.CLASS_NAME, 'ciga_list_list_item_img')
    photo_url = [p.find_element(By.TAG_NAME, "img").get_attribute("src") for p in photo]
    price = driver.find_elements(By.CLASS_NAME, 'ciga_list_list_item_bar_price')
    price_buy = [p.find_element(By.CLASS_NAME, "ciga_list_list_item_bar_price_t").text.replace("批发价：", "") for p in price]
    price_sale = [p.find_element(By.CLASS_NAME, "ciga_list_list_item_bar_price_b").text.replace("建议零售价：", "") for p in price]
    name_ciga_all.extend(name_ciga)
    price_buy_all.extend(price_buy)
    price_sale_all.extend(price_sale)
    photo_urls.extend(photo_url)


def down_photo():
    mHeaders = {}
    mHeaders["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"
    mHeaders["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    for name, url in zip(name_ciga_all, photo_urls):
        r = requests.get(url, headers=mHeaders)
        with open(f"{name}.png", 'wb') as f:
            f.write(r.content)


def write_data():
    headers = ['商品', '批发价', '零售价']
    rows = zip(name_ciga_all, price_buy_all, price_sale_all)
    with open('Data/cigarette.csv', 'w', encoding='utf8', newline='') as f:
        ciga = csv.writer(f)
        ciga.writerow(headers)
        ciga.writerows(rows)


if __name__ == "__main__":
    while True:
        currentpage = page.get_attribute("currentpage")
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "ciga_list_list_item_img")))
        get_info()
        if int(currentpage) < int(totalpage):
            driver.find_element(By.CLASS_NAME, "pagebar_gonext").click()
            time.sleep(3)
        elif int(currentpage) == int(totalpage):
            break
    # print(name_ciga_all)
    # print(price_sale_all)
    # print(price_buy_all)
    write_data()
    down_photo()
