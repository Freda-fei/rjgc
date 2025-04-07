from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
    def tearDown(self):
        self.browser.quit()
    def test_can_start_a_list_and_retrieve_it_later(self):
        # 一个在线代办事项的应用
        # 查看应用首页
        self.browser.get("http://localhost:8000")

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
        inputbox.send_keys('Give a gift to Lisi')

        # 按回车键后，页面更新
        # 代办事项表格中显示了“1：Buy flowers”
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID,'id_list_table')
        rows = table.find_elements(By.TAG_NAME,'tr')
        self.assertIn('1: Buy flowers',[row.text for row in rows])
        self.assertIn('2: Give a gift to Lisi', [row.text for row in rows])
        
        # 页面中又显示一个文本输入框，可以输入其他待办事项
        # 输入了一个“Send a gift to Lisi”
        self.fail('Finish the test!')

        # 页面再次更新，它的清单中显示了这两个待办事项

        # 想知道这个网站是否会记住他的清单
        # 他看到网站为他生成了一个唯一的URL

        # 访问URL，发现他的代办事项列表还在
        # 满意的离开了
if __name__ == '__main__':
    unittest.main()

