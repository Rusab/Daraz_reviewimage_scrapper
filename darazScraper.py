import time
from selenium import webdriver as wb
from selenium.webdriver.chrome.options import Options
import urllib.request
from bs4 import BeautifulSoup
import os

#choose if you want to start chrome in headless mode
headless = False

#start a webdriver
if(headless):
    headless_option = Options()
    headless_option.add_argument("--headless")
    driver = wb.Chrome('chromedriver.exe', options = headless_option)
else: 
    driver = wb.Chrome('chromedriver.exe')

#list of products to scrape
url_list = [
    'https://www.daraz.com.bd/products/t1-i144906075-s1109262093.html?spm=a2a0e.home.just4u.15.735212f7edFMSl&scm=1007.28811.244313.0&pvid=95f78e5f-734b-4509-bc4e-8d607d3c8720&clickTrackInfo=pvid%3A95f78e5f-734b-4509-bc4e-8d607d3c8720%3Bchannel_id%3A0000%3Bmt%3Ahot%3Bitem_id%3A144906075%3B',
    'https://www.daraz.com.bd/products/dx-68-led-decor-1pcs-i147696679-s1073438190.html?spm=a2a0e.home.just4u.9.4c2e12f72oZ5Qb&scm=1007.28811.244313.0&pvid=92c23e84-3352-4b5c-b0a9-b499d50ee433&clickTrackInfo=pvid%3A92c23e84-3352-4b5c-b0a9-b499d50ee433%3Bchannel_id%3A0000%3Bmt%3Ahot%3Bitem_id%3A147696679%3B'
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
        for objs in objs:
            link = objs.div["style"]
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
            button_list = driver.find_elements_by_xpath('//*[@id="module_product_review"]/div/div[3]/div[2]/div/button[2]/i')
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
    product_folder = "New Panda"
    product_path = os.path.join(parent_dir, product_folder)

    if not os.path.exists(product_path):
        os.makedirs(product_path)

    scrapeImagesOf(url)
driver.quit()