## 项目介绍

用selenium批量爬取[广东烟草电子商务网站](https://www.yueyigou.com/)上的香烟清单，图片，批发价，零售价。**需要有账号登录**。

页面链接既不改变URL，也不重载页面，数据动态从服务器加载，因此使用selenium。

## 技术要求

- selenium

- 必要导入语句

  ```python
  from selenium import webdriver # 启动浏览器
  from selenium.webdriver.chrome.options import Options # chrome启动配置
  from selenium.webdriver.chrome.service import Service # chromedriver驱动服务
  from selenium.webdriver.common.by import By # 元素定位
  ```

## 学习经验

1. 用到selenium的强制等待，显式等待和隐式等待

   - 强制等待：`time.sleep(3)`，用于页数切换过快，网站页数未更新
   - 显式等待：`WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "ciga_list_list_item_img")))`，用于等待所有图片加载完全才切换下一页图片
   - 隐式等待：`driver.implicitly_wait(10) ` ，打开全部网页加载数据需要缓冲时间

2. 解决代码执行完成，自动关闭浏览器窗口

   ​	`options.add_experimental_option("detach", True)`

3. 自定义浏览器，可用于第三方基于chromium浏览器。自定义数据目录，可缓存登录信息。

   `options.binary_location = r"D:\DownSoft\Chrome\App\chrome.exe"`

   `options.add_argument("--user-data-dir=D:\\DownSoft\\Chrome\\Data\\Default") `

4. selenium_v4之后的元素定位方式

   ```python
   # 根据xpath选择元素(万金油)
   driver.find_element(By.XPATH, '//*[@id="kw"]') 
   # 根据css选择器选择元素
   driver.find_element(By.CSS_SELECTOR, '#kw') 
   # 根据name属性值选择元素
   driver.find_element(By.NAME, 'wd') 
   # 根据类名选择元素
   driver.find_element(By.CLASS_NAME, 's_ipt') 
   # 根据链接文本选择元素
   driver.find_element(By.LINK_TEXT, 'hao123') 
   # 根据包含文本选择
   driver.find_element(By.PARTIAL_LINK_TEXT, 'hao') 
   # 根据标签名选择
   # 目标元素在当前html中是唯一标签或众多标签第一个时候使用
   driver.find_element(By.TAG_NAME, 'title') 
   # 根据id选择
   driver.find_element(By.ID, 'su') 
   ```
   
5. chromedriver启动配置

   ```python
   options = Options()  # 新版加启动配置
   options.binary_location = r"D:\DownSoft\Chrome\App\chrome.exe"  # 指定chrome程序路径
   # 指定下载路径，无头模式不可用
   download_path = r""
   prefs = {"download.default_directory": download_path}
   options.add_experimental_option("prefs", prefs)
   # options.add_argument('–headless')# 无头浏览模式
   options.add_argument('--incognito')  # 无痕浏览
   options.add_argument('--no-sandbox')  # 在 root 权限下运行。指定第三方浏览器时地址栏只显示data，需要加此行
   # options.add_argument(f'--user-agent={user_agent}')# 添加 User Agent
   # options.add_argument(f'--proxy-server=http://{proxy}')# 添加代理
   options.add_argument("--no-referrers")  # 不发送 Http-Referer 头
   # options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
   # options.add_argument("--window-size=1920,1050")  # 指定浏览器分辨率
   options.add_argument("--start-maximized")  # 启动时窗口最大化
   # options.add_argument('–homedir={}')  # 指定主目录存放位置
   options.add_argument('--disk-cache-dir={临时文件目录}')  # 指定临时文件目录
   options.add_argument("--ignore-certificate-errors")  # 忽略不信任证书
   options.add_argument('--ignore-ssl-errors')  # 处理SSL证书错误问题
   options.add_argument('--disable-setuid-sandbox')  # 禁用沙盒
   options.add_argument('--disable-notifications')  # 禁用通知警告
   options.add_argument("--disable-application-cache")  # 禁用缓存
   options.add_argument('--disable-dev-shm-usage')  # 使用硬盘来存储获取的内容，而不是使用内存.大量渲染时候写入/tmp而非/dev/shm
   # options.add_argument('--disable-gpu')  # 禁用GPU加速
   options.add_argument('--disable-infobars')  # 禁用提示
   options.add_argument('--disable-web-security')  # 关闭安全策略
   options.add_argument('--disable-xss-auditor')  # 禁止xss防护
   options.add_argument("--disable-popup-blocking")  # 允许弹窗
   options.add_argument("--disable-java")  # 禁用 java
   options.add_argument("--disable-javascript")  # 禁用Javascript
   options.add_argument("--disable-plugins")  # 禁用插件
   options.add_argument("--disable-images")  # 禁用图像
   options.add_argument('--disable-extensions')  # 禁用扩展
   options.add_argument('--disable-webgl')  # 禁用webgl
   options.add_argument("-–no-first-run")  # 初始化时为空白页面
   options.add_argument(
       "--disable-blink-features=AutomationControlled")  # 除window.navigator.webdriver，否则调用远程webdriver时则会报错
   # options.add_argument('--enable-automation')  # 通知(通知用户其浏览器正由自动化测试控制)
   # options.add_argument('--host-resolver-rules=MAP www.baidu.com 127.0.0.1')  # 添加屏蔽规则
   options.add_argument('--no-default-browser-check')  # 不做浏览器默认检查
   options.add_experimental_option('useAutomationExtension', False)  # 去除新版本 chrome 取消‘Chrome 正在受到自动软件的控制’提示
   options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])  # 忽略无用的日志
   # options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 设置开发者模式启动，该模式下webdriver属性为正常值
   options.add_argument(
       '--user-data-dir=D:\\Software1\\Chrome_106.0.5249.119_64bit_Portable\\Chrome\\Data')  # 加载配置启动浏览器，不然就以一个全新的浏览窗口启动
   # 版本已经更新,之前的 executable_path 被重构到了 Service 函数里。不再使用
   # driver = webdriver.Chrome(chrome_options=options, executable_path=executable_path)
   options.add_experimental_option("detach", True) # 浏览器不自动关闭
   ```
   
   

