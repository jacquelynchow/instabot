
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import random
from selenium.webdriver import ActionChains

class instaBot:
    def __init__(self, username, password, accountType, hashtagSearch):
        self.username = username 
        self.password = password
        self.accountType = accountType # food or personal account
        self.hashtagSearch = hashtagSearch # doing hashtag searches or main feed activity
        self.driver = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver') # type of driver used

    def login(self):
        driver = self.driver
        # go to the instagram login site
        driver.get("https://instagram.com/accounts/login")
        sleep(2)
        # type in username and password
        driver.find_element_by_name('username').send_keys(self.username)
        driver.find_element_by_name('password').send_keys(self.password)
        sleep(2)
        # submit button after finished typing in username and password
        driver.find_element_by_xpath('//button[@type= "submit"]').click()
        sleep(3)
        # first pop up
        driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(2)
        # second pop up
        driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(1)

    def searchHashtag(self, hashtag):
        driver = self.driver
        # get related hashtags 
        related_hashtags = [hashtag]
        foundHashtags = driver.find_elements(By.CLASS_NAME, 'LFGs8.xil3i')
        for tag in foundHashtags:
            related_hashtags.append(tag.text[1:])
        # go to every hashtag and like/comment
        for tag in related_hashtags:
            # go to the specific hashtag's post listings
            driver.get('https://www.instagram.com/explore/tags/' + tag)
            # set number of posts to go through
            amount = 4
            driver.execute_script("window.scrollTo(0, Y)")
            sleep(0.5)
            # find first most recent post
            driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[2]').click()
            i = 0
            while i <= amount:
                sleep(2)
                self.likePhoto()
                sleep(2)
                self.commentPhoto()
                sleep(4)
                # find the right arrow to go to the next post
                driver.find_element_by_class_name('_65Bje.coreSpriteRightPaginationArrow').click()
                i += 1

    def likePhoto(self):
        # like the photo
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div/div[2]/div/article[1]/div[2]/section[1]/span[1]/button').click()

    def commentPhoto(self):
        driver = self.driver
        # pick a random comment from set list
        commentsList = ['So yummy!!', 'OMG THIS LOOKS SO GOOD', 'Tasty!! <3', 'Send some over!',
            'Awesome food omg!', 'Get in my tummy!', '<3 Really want some', 'Mouthwatering...',
            ':O Amazing', 'So pretty, ahhh!', 'Delicious :)', 'Makes me hungry', 'YUMMM!', 'Omg I wanna try that',
            'I love this!!', 'Woahhh looks amazing']
        random.shuffle(commentsList)
        sleep(2)
        # find comment box on instagram page
        if self.hashtagSearch:
            # hashtag feed comment box
            entry = lambda: driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea')
        else:
            # main feed comment box
            entry = lambda: driver.find_element_by_xpath('/html/body/div[1]/section/main/section/div/div[2]/div/article[4]/div[2]/section[3]/div/form/textarea')
        # click on comment box               
        entry().click()
        # go through each letter and send/type it in
        for letter in commentsList[0]:
            entry().send_keys(letter)
            sleep(random.randint(1,8)/30)
        # hit return key when comment is ready
        entry().send_keys(Keys.RETURN)

    def likingFeed(self, likes, account):
        driver = self.driver
        #scroll a bit
        #driver.execute_script("window.scrollTo(0, 200);")
        
        #get scroll height
        #last_height = driver.execute_script("return document.body.scrollHeight")
        
        while likes > 0:
            #scroll down to bottom
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            #element = driver.find_element_by_xpath('wpO6b')
            #element.location_once_scrolled_into_view()
            action = ActionChains(driver)  
            i = 1        
            while i < likes:       
                xpath_name = "/html/body/div[1]/section/main/section/div/div[2]/div/article[" + str(i) + "]/div[2]/section[1]/span[1]/button"
                driver.find_element_by_xpath(xpath_name).click()
                #action.move_to_element(element).perform()
                sleep(2) 
                # wait for page to load
                # click the like button
                #self.likePhoto()
                #sleep(1)
                likes -= 1
                #action.send_keys(Keys.END).perform()
                sleep(.1)

            #new_height = driver.execute_script("window.scrollTo(0, 200);")
            if account.accountType == 'food':
                self.commentPhoto()
                sleep(3)

            #calculate new scroll height 
            #new_height = driver.execute_script("return document.body.scrollHeight")
            #last_height = new_height
    
    def main():
        # create classes
        personalgram = instaBot('jacquelynchow', '902173785', 'personal', False)
        #foodstagram = instaBot('jacqchereats', '834montrose', 'food', True)

        # set which account
        myInstagram = personalgram
        myInstagram.driver.set_window_size(1000,1000)

        if myInstagram == personalgram:
            # login to instagram
            personalgram.login()    
            personalgram.likingFeed(3, myInstagram)
            personalgram.driver.quit()
        else:
            # login to instagram
            foodstagram.login()    
            # pick random hashtag from randomized set list
            #hashtag_list = ['foodblogger', 'foodblog', 'foodie', 'foodporn', 'eeeeeats']
            #random.shuffle(hashtag_list)
            # hashtag feed
            #foodstagram.searchHashtag(hashtag_list[0])
            #foodstagram.driver.get('https://www.instagram.com/')
            sleep(2)
            # main feed
            foodstagram.hashtagSearch = False
            foodstagram.likingFeed(40, myInstagram)
            foodstagram.driver.quit()

main()