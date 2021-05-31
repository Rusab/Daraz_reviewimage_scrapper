import time
from selenium import webdriver as wb
from selenium.webdriver.chrome.options import Options
import urllib
from bs4 import BeautifulSoup
import os

#choose if you want to start chrome in headless mode
headless = True

#start a webdriver
if(headless):
    headless_option = Options()
    headless_option.add_argument("--headless")
    driver = wb.Chrome('chromedriver.exe', options = headless_option)
else: 
    driver = wb.Chrome('chromedriver.exe')

#list of products to scrape
url_list = [
    'https://www.daraz.com.bd/products/snicker-10-piece-pack-14-x-10-140-gm-i150680985-s1077384186.html?spm=a2a0e.searchlist.list.1.59a06de78wwYUh&search=1',
    'https://www.daraz.com.bd/products/snickers-chocolate-50g-india-i140612583-s1064098761.html?spm=a2a0e.searchlist.list.13.59a06de7oGthIN&search=1',
    'https://www.daraz.com.bd/products/snickers-chocolate-dubai-50grm-x-12pic600grm-i131652537-s1052056630.html?spm=a2a0e.searchlist.list.37.59a06de7sQ6pBL&search=1'
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
    product_folder = "Snickers"
    product_path = os.path.join(parent_dir, product_folder)

    if not os.path.exists(product_path):
        os.makedirs(product_path)

    scrapeImagesOf(url)
driver.quit()