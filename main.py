import argparse
import logging
from time import sleep
from urllib.parse import quote
from selenium import webdriver
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Github(object):
    URL = 'https://github.com'

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver = webdriver.Chrome()

    def navigate(self, action='back'):
        if action == 'back':
            self.driver.execute_script("window.history.go(-1)")
        else:
            self.driver.execute_script("window.history.go(1)")

    def try_login(self, url, username, password):
        
        """  This function enables us login to GitHub
        Args:
            url: a url try to login
            username: username belongs to user
            password: password belongs to user """
        
        self.driver.get(url)

        username_input = self.driver.find_element_by_id('login_field')
        password_input = self.driver.find_element_by_id('password')
        submit_btn = self.driver.find_element_by_css_selector('#login input[type="submit"]')

        username_input.send_keys(username)
        password_input.send_keys(password)
        submit_btn.click()

    def try_search(self, text):
        text = quote(text)
        search_url = f"{self.URL}/search?q={text}"
        self.driver.get(search_url)

        the_repo_href = self.driver.find_element_by_css_selector('ul.repo-list li a')
        the_repo_href.click()
        self.logger.info('Repo has found')
        the_repo = self.driver.current_url

        # starred
        star_btn = self.driver.find_element_by_css_selector('button[title="Star intuit/karate"]')
        star_btn.click()
        self.logger.info('Repo is stared now')
        sleep(2)

        # unstar
        self.driver.get(the_repo)
        unstar_btn = self.driver.find_element_by_css_selector('button[title="Unstar intuit/karate"]')
        unstar_btn.click()
        self.logger.info('Repo is unstared now')
        sleep(3)

    def run_sign_in_scenarios(self, username, password):

        SIGN_IN_CSS_PATH = '.HeaderMenu-link.no-underline.mr-3'

        # go to github.com
        self.driver.get(self.URL)

        # select & click sign in btn
        sign_in_btn = self.driver.find_element_by_css_selector(SIGN_IN_CSS_PATH)
        sign_in_btn.click()
        sign_in_url = self.driver.current_url

        # scenario 1:
        # wrong username - correct password
        self.try_login(url=sign_in_url, username=f"{username}e", password=f"{password}")
        self.logger.info('User has  tried  to login with wrong username')
        sleep(3)

        # scenario 2:
        # correct username - wrong password
        self.try_login(url=sign_in_url, username=f"{username}", password=f"{password}e")
        self.logger.info('User has tried to login with wrong password')
        sleep(3)

        # scenario 2:
        # correct username & password
        self.try_login(url=sign_in_url, username=f"{username}", password=f"{password}")
        self.logger.info('Username & Password has been acceptad ')
        sleep(3)

    def update_settings(self):
        self.driver.get(self.URL)

        profile_icon = self.driver.find_elements_by_class_name('Header-item')[-1]
        profile_icon.click()
        sleep(2)

        settings_btn = self.driver.execute_script("return document.querySelector('#feature-enrollment-toggle')"
                                                  ".nextElementSibling.nextElementSibling")
        settings_btn.click()
        sleep(2)

        # get selectors
        name_input = self.driver.find_element_by_id('user_profile_name')
        bio_input = self.driver.find_element_by_id('user_profile_bio')
        update_btn = self.driver.execute_script("return document.getElementsByClassName('btn btn-primary')[1]")

        name_input.send_keys('Test')
        bio_input.send_keys('Test')
        update_btn.click()
        sleep(2)

        name_input = self.driver.find_element_by_id('user_profile_name')
        bio_input = self.driver.find_element_by_id('user_profile_bio')

        assert name_input.get_attribute('value') == 'Hasan Can YildirTest'
        self.logger.info('User name is updated : ' + name_input.get_attribute('value'))
        
        assert bio_input.get_attribute('value') == 'Test'
        self.logger.info("Bio is updated : " + bio_input.get_attribute('value'))
        

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='Github username')
    parser.add_argument('-p', '--password', help='Github password')
    args = parser.parse_args()

    github = Github()

    # case 1
    github.run_sign_in_scenarios(username=args.username, password=args.password)

    # case 2
    github.try_search('karate')

    # case 3
    github.update_settings()
    
    github.close()
