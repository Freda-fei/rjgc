from selenium import webdriver
import unittest
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
        self.assertIn('To-Do',self.browser.title, "browser title was:" +self.browser.title)
        self.fail('Finish the test!')
        # 应用有一个输入待办事项的文本输入框

        # 在文本输入框输入了“Buy flowers”

        # 按回车键后，页面更新
        # 代办事项表格中显示了“1：Buy flowers”

        # 页面中又显示一个文本输入框，可以输入其他待办事项
        # 输入了一个“Send a gift to Lisi”

        # 页面再次更新，它的清单中显示了这两个待办事项

        # 想知道这个网站是否会记住他的清单
        # 他看到网站为他生成了一个唯一的URL

        # 访问URL，发现他的代办事项列表还在
        # 满意的离开了
if __name__ == '__main__':
    unittest.main()

