import selenium, time
from selenium import webdriver as wb
import urllib
from bs4 import BeautifulSoup
import os
 
driver = wb.Chrome('chromedriver.exe')
url_list = [
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-i44522-s368469.html?spm=a2a0e.searchlist.list.1.7de237e5X9iobP&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-i117690248-s1036998138.html?spm=a2a0e.searchlist.list.3.7de237e5lEkE7i&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-cumilla-i100902221-s1014887987.html?spm=a2a0e.searchlist.list.7.7de237e5iniOLr&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-rangpur-i100891640-s1014889381.html?spm=a2a0e.searchlist.list.9.7de237e5SncG1i&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-khulna-i100901402-s1014897313.html?spm=a2a0e.searchlist.list.11.7de237e5e781PG&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-sylhet-i100903113-s1014897378.html?spm=a2a0e.searchlist.list.13.7de237e50Z5jGo&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-gazipur-i100902233-s1014891768.html?spm=a2a0e.searchlist.list.15.7de237e5Y5W7f3&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-savar-i100903112-s1014899298.html?spm=a2a0e.searchlist.list.19.7de237e5vKn9Mk&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-savar-i100903112-s1014899298.html?spm=a2a0e.searchlist.list.19.7de237e5uuF8Td&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-barishal-i100892715-s1014888927.html?spm=a2a0e.searchlist.list.23.7de237e5ckLFEJ&search=1https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-feni-i100899282-s1014892772.html?spm=a2a0e.searchlist.list.21.7de237e5Jco2Br&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-barishal-i100892715-s1014888927.html?spm=a2a0e.searchlist.list.23.7de237e5ckLFEJ&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-mymensingh-i100902419-s1014902160.html?spm=a2a0e.searchlist.list.29.7de237e5kQgays&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-dinajpur-i100892750-s1014897144.html?spm=a2a0e.searchlist.list.37.7de237e5jdta6E&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-bogura-i100893669-s1014894433.html?spm=a2a0e.searchlist.list.39.7de237e5XJ5lH6&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-pabna-i102854067-s1017210101.html?spm=a2a0e.searchlist.list.47.7de237e5DwkAKT&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-rajshahi-i100903105-s1014894730.html?spm=a2a0e.searchlist.list.55.7de237e5J6Cydb&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-kushtia-i100904049-s1014895674.html?spm=a2a0e.searchlist.list.57.7de237e5nJddae&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-narayanganj-i100904060-s1014891970.html?spm=a2a0e.searchlist.list.65.7de237e5ML3tnn&search=1',
    'https://www.daraz.com.bd/products/danish-lexus-vegetable-calcium-crackers-biscuit-buy-2-get-1-240gm-gopalganj-i102854520-s1017210573.html?spm=a2a0e.searchlist.list.1.2cc637e5QFQep7&search=1'
    ]


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
    

def getDriverSoup(url, initial = True):
    if(initial):
        driver.get(url)
    scrollWindow()
    return BeautifulSoup(driver.page_source, 'html.parser')


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

    parent_dir = os.getcwd()
    product_folder = "Ispahani Mirzapur Tea"
    product_path = os.path.join(parent_dir, product_folder)

    if not os.path.exists(product_path):
        os.makedirs(product_path)

    scrapeImagesOf(url)
    driver.quit()