from selenium import webdriver
import os
import time


class InstagramBot:

    inst_followers = []
    inst_followings = []
    inst_un_followers = []

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.driver = webdriver.Chrome('chromedriver.exe')
        self.instagram_login()
        self.instagram_fetch_details()
        self.instagram_profile()
        # self.instagram_unfollow_unfollowers()

    def instagram_login(self):

        self.driver.get('http://instagram.com/accounts/login/')
        print('\nStarting engine .........')
        time.sleep(2)

        print('Signing in ..............')
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(self.username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(self.password)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(3)

        print('Setting environment .....')
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        time.sleep(2)

        print('Setting environment .....')
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        time.sleep(2)

        print('Linking user profile ....')
        self.driver.find_element_by_xpath("//a[contains(@href, '/" + self.username + "/')]").click()
        time.sleep(2)

    def instagram_fetch_details(self):
        """ GET FOLLOWERS LIST """
        print('getting followers .......')
        self.driver.find_element_by_xpath("//a[contains(@href, '/" + self.username + "/followers/')]").click()
        self.inst_followers = self._get_names()

        """ GET FOLLOWING LIST """
        print('getting following .......')
        self.driver.find_element_by_xpath("//a[contains(@href, '/" + self.username + "/following/')]").click()
        self.inst_followings = self._get_names()

        """ GET BASTARDS """
        bastards = [user for user in self.inst_followings if user not in self.inst_followers]
        time.sleep(2)

        self.inst_un_followers = bastards

    def instagram_unfollow_unfollowers(self):

        self.driver.find_element_by_xpath("//a[contains(@href, '/" + self.username + "/following/')]").click()
        time.sleep(2)

        scroll_box = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        last_ht, ht = 0, 1

        while last_ht != ht:
            last_ht = ht
            time.sleep(2)
            ht = self.driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight; """, scroll_box)

        lists = scroll_box.find_elements_by_tag_name('li')
        buttons = scroll_box.find_elements_by_xpath("//button[contains(text(), 'Following')]")
        texts = scroll_box.find_elements_by_tag_name("a")
        names = [name.text for name in texts if name.text != '']

        time.sleep(3)
        un_follower_count = 1

        for name in names:
            if name in self.inst_un_followers:
                inc = un_follower_count-1
                buttons[inc].click()
                element = scroll_box.find_element_by_xpath("//button[contains(text(), 'Cancel')]").click()
                print('UN-FOLLOWING USER | id: ', un_follower_count, ' Name: ', name)

            un_follower_count += 1

    def instagram_profile(self):

        print('\n\n_________________WELCOME ', self.username, '_________________\n')
        print('1 : Show Followers')
        print('2 : Show Followings')
        print('3 : Show Un_Followers')
        print('4 : Show Statistics')
        print('5 : Show Complete Details')
        print('6 : Unfollow Un_followers')
        print('0 : Exit')
        time.sleep(2)

        while True:
            choice = int(input('\nPlease Select Your Choice: '))
            if choice == 1:
                self._show_details(name='Followers', data=self.inst_followers)
            elif choice == 2:
                self._show_details(name='Followings', data=self.inst_followings)
            elif choice == 3:
                self._show_details(name='Un_Followers', data=self.inst_un_followers)
            elif choice == 4:
                self._show_statistics()
            elif choice == 5:
                self._show_details(name='Followers', data=self.inst_followers)
                self._show_details(name='Followings', data=self.inst_followings)
                self._show_details(name='Un_Followers', data=self.inst_un_followers)
            elif choice == 6:
                self.instagram_unfollow_unfollowers()
            elif choice == 0:
                print('THANKS FOR USING INSTA BOT')
                time.sleep(1)
                print('Terminating. . . . ')
                time.sleep(1)
                break
            else:
                pass

    def _show_details(self, name, data):
        print('\nFETCHING: ', name)
        time.sleep(1)

        print('Total: ', len(data))
        print()
        time.sleep(2)

        if data is not None:
            if len(data) > 0:
                count = 1
                for val in data:
                    print('USER | id: ', count, ' Name: ', val)
                    count += 1
            else:
                print('No User available')
        else:
            print('System required dataset please provide it')
        print('_________________________________________________')

    def _show_statistics(self):
        print('\n\n______________ ', self.username, '_______________')
        print('FOLLOWERS     : ', len(self.inst_followers))
        print('FOLLOWINGS    : ', len(self.inst_followings))
        print('UN_FOLLOWERS  : ', len(self.inst_un_followers))

    def _get_names(self):
        time.sleep(3)
        scroll_box = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            time.sleep(2)
            ht = self.driver.execute_script("""
                   arguments[0].scrollTo(0, arguments[0].scrollHeight);
                   return arguments[0].scrollHeight;
                   """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
        return names