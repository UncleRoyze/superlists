from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("testing\n")
        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        inputbox.send_keys('Kiss Chien Mien Mien')
        inputbox.send_keys(Keys.ENTER)

        roy_list_url = self.browser.current_url
        self.assertRegex(roy_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Kiss Chien Mien Mien')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Kiss Chien Mien Mien again!')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('2: Kiss Chien Mien Mien again!')

        ## We use a new browser session to make sure that no information
        ## of Roy's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kiss Chien Mien Mien', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Kiss Roy')
        inputbox.send_keys(Keys.ENTER)

        mien_list_url = self.browser.current_url
        self.assertRegex(mien_list_url, 'lists/.+')
        self.assertNotEqual(roy_list_url, mien_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kiss Chien Mien Mien', page_text)
        self.assertIn('Kiss Roy', page_text)
