from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from django.conf import settings
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

MAX_WAIT = 10 #(1)

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        real_server = os.environ.get('REAL_SERVER')#(1)
        if real_server:
            self.live_server_url = 'http://'+real_server#(2)

        
    def tearDown(self):
        self.browser.quit()
        
    def wait_for_row_in_list_table(self,row_text):
        start_time = time.time()
        while True:#(2)
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')#(3)
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return #(4)
            except (AssertionError,WebDriverException) as e:#(5)
                if time.time() - start_time>MAX_WAIT:#(6)
                    raise e#(6)
                time.sleep(0.5)#(5)




        
    def test_can_start_a_list_and_retrieve_it_later(self):
        # 一个在线代办事项的应用
        # 查看应用首页
        self.browser.get(self.live_server_url)

        # 网页首页里包含“To-Do”这个词
        self.assertIn('To-Do',self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do',header_text)

        # 等待页面加载完成
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'id_new_item'))
        )

        # 应用有一个输入待办事项的文本输入框
        inputbox = self.browser.find_element(By.ID,'id_new_item')

        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 在文本输入框输入了“Buy flowers”
        inputbox.send_keys('Buy flowers')

        # 按回车键后，页面更新
        # 代办事项表格中显示了“1：Buy flowers”
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')


        # table = self.browser.find_element(By.ID,'id_list_table')
        # rows = table.find_elements(By.TAG_NAME,'tr')
        # self.assertIn('1: Buy flowers',[row.text for row in rows])
        # self.assertIn('2: Give a gift to Lisi', [row.text for row in rows])
        
        # 页面中又显示一个文本输入框，可以输入其他待办事项
        # 输入了一个“Send a gift to Lisi”
        # self.fail('Finish the test!')
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)


        # 页面再次更新，它的清单中显示了这两个待办事项
        self.wait_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('2: Give a gift to Lisi')
        # 想知道这个网站是否会记住他的清单
        # 他看到网站为他生成了一个唯一的URL
        # self.fail('Finish the test!')
        # 访问URL，发现他的代办事项列表还在
        # 满意的离开了

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #张三新键一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')

        #他注意到清单有个唯一的url
        zhangsan_list_url = self.browser.current_url
        self.assertRegex(zhangsan_list_url,"/lists/.+")#(1)

        #现在有一个新用户王五访问网站
        #我们使用一个新的浏览器会话
        #确保张三的信息不会从cookie中泄露出去
        self.browser.quit()
        self.browser = webdriver.Chrome()

        #王五访问首页
        #页面中看不到张三的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertNotIn('Give a gift to Lisi',page_text)

        #王五输入一个新的待办事项，创建一个清单
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #王五获得了他唯一的Url
        wangwu_list_url = self.browser.current_url
        self.assertRegex(wangwu_list_url,'lists/.+')
        self.assertNotEqual(wangwu_list_url,zhangsan_list_url)
        
        #这个页面还是没有张三的清单
        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertIn('Buy milk',page_text)

        #两个人都很满意，然后碎觉去

    def test_layout_and_styling(self):
        #张三访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        # 等待输入框加载完成
        inputbox = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'id_new_item'))
        )

        # 他新建了一个清单，看到输入框仍然完美的居中显示
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')

        #他看到输入框完美的居中显示
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta = 10
        )



# if __name__ == '__main__':
#     unittest.main()

