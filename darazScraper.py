import time
from selenium import webdriver as wb
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import urllib.request
from bs4 import BeautifulSoup
import os

#choose if you want to start chrome in headless mode
headless = False
driver_service = Service('chromedriver.exe')
#start a webdriver
if(headless):
    headless_option = Options()
    headless_option.add_argument("--headless")
    driver = wb.Chrome(service = driver_service, options = headless_option)
else: 
    driver = wb.Chrome(service = driver_service)

#list of products to scrape
url_list = [
    'https://www.daraz.com.bd/products/dettol-soap-aloe-vera-75gm-bathing-bar-soap-with-aloe-vera-extract-i125973891-s1046091443.html?spm=a2a0e.searchlist.list.4.4d105892swMENZ&search=1',
 
    ]





#scrolling function
def scrollWindow(direction = 'down'):
    SCROLL_PAUSE_TIME = 0.09
    last_height = driver.execute_script("return window.scrollY")
    if(direction == 'up'):
        sign = '-'
    else:
        sign = '+'
        
    while True:
        driver.execute_script("window.scrollTo(0, window.scrollY" + sign + "50)")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return window.scrollY")
        if new_height == last_height:
            break
        last_height = new_height
    
#gets site html infromation after browser visits url
def getDriverSoup(url, initial = True):
    if(initial):
        driver.get(url)
    scrollWindow()
    return BeautifulSoup(driver.page_source, 'html.parser')

#iterates through review sections and downloads review images
def scrapeImagesOf(url):
    flag = True
    nextPage = False
    patience = 3
    count = 1
    sec = 1
    while(flag):
        soup = getDriverSoup(url, not (nextPage))
        objs = soup.find_all(class_ = 'pdp-common-image review-image__item')

        flag = False
        for obj in objs:
            img = obj.find(class_ = "image")
            link = img.get('style')
            pos1 = link.find('url("')
            pos2 = link.find(');')
            link = link[pos1+5:pos2-1]
            print("Downloading: ", link)
            try:
                urllib.request.urlretrieve(link, product_path + '/' + str(time.time())+'.jpg')     
            except:
                print("lol")
        
        try:
            driver.execute_script("window.scrollTo(0, window.scrollY" + '-' + "1500)")
            button_list = driver.find_elements(By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/button[2]/i')
            button_list[0].click()
            sec += 1
            print("Going to section", sec)
            nextPage = True
            
            if len(objs) == 0:
                count += 1
            if count > patience:
                flag = False
            else:
                flag = True

        except:
            print("No more sections") 

for url in url_list:
    #creates directory for scraped images
    parent_dir = os.getcwd()
    product_folder = "Dettol Soap Aloe Vera"
    product_path = os.path.join(parent_dir, product_folder)

    if not os.path.exists(product_path):
        os.makedirs(product_path)

    scrapeImagesOf(url)
driver.quit()