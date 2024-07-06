from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import time


class Scraper:
    
    def __init__(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)
        self.data = []
    
    def start(self,url):
        self.driver.maximize_window()
        self.driver.get(url)
        self.check_type()
        return self.data
    
    def check_type(self):
        try:
            review_page = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf XiKgde "]')))
            overview_page = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="bJzME tTVLSc"]')))

            if review_page or overview_page:
                self.scroll()
        
        except:
            pass

        try:
            non_standard_page = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="kKWzSd"]')))
            if non_standard_page:
                self.diff_review_page()
        except:
            self.driver.quit()

    def scroll(self):
        
        try:
            ## If user is on the overview tab, Then click on the More reviews button to goto reviews page.
            self.driver.find_element(By.XPATH, "//span[contains(text(), 'More reviews')]").click()
            time.sleep(5)
        except:
            pass
        
        data_container = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf XiKgde "]')))
        num_of_scrolls = 0
            
        while True:
            current_reviews = len(self.driver.find_elements(By.CSS_SELECTOR, ".jJc9Ad"))
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', data_container)
            time.sleep(2) # wait for the reviews to load
            
            new_num_loaded_reviews = len(self.driver.find_elements(By.CSS_SELECTOR, ".jJc9Ad"))
            if current_reviews == new_num_loaded_reviews: break
            
        self.get_reviews()
            
    def get_reviews(self):
        total_reviews = self.driver.find_elements(By.CSS_SELECTOR, ".jJc9Ad")
        for review in total_reviews:
            name = review.find_element(By.CLASS_NAME, 'd4r55').text
            print(name)
        self.driver.close()
        
    def diff_review_page(self):
        start_time = time.time()
        data_container = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="kKWzSd"]')))
        num_of_scrolls = 0
            
        while True:
            current_reviews = len(self.driver.find_elements(By.CSS_SELECTOR, ".bwb7ce"))
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', data_container)
            time.sleep(4) # wait for the reviews to load
            
            new_num_loaded_reviews = len(self.driver.find_elements(By.CSS_SELECTOR, ".bwb7ce"))
            if current_reviews == new_num_loaded_reviews: break
            
        total_reviews = self.driver.find_elements(By.CSS_SELECTOR, ".bwb7ce")
        

        for review in total_reviews:
            name = review.find_element(By.CLASS_NAME, 'Vpc5Fe').text
            stars = review.find_element(By.CLASS_NAME, 'dHX2k')
            star_rating = stars.get_attribute('aria-label')  # Retrieve the aria-label attribute for the stars
            
            #Loop was breaking since some reviews didnt have comments so i placed this to keep the loop going.
            try:
                comment = review.find_element(By.CLASS_NAME, "OA1nbd").text
            except:
                comment = ''
            date_of_review = review.find_element(By.CLASS_NAME, "y3Ibjb").text
            
            self.data.append({
                'name': name,
                'rating': star_rating,
                'comment': comment,
                'date_of_review': date_of_review
            })
        self.driver.quit()
        end_time = time.time()
        
        execution_time = end_time - start_time  # Calculate the execution time
        print("Execution time:", execution_time, "seconds")
    
    
    
url = input("enter url")
s = Scraper()
s.start(url)
