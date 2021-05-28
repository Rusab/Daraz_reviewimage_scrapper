# -*- coding: utf-8 -*-
"""
Created on Fri May 28 21:27:17 2021

@author: akash
"""
import selenium, time
from selenium import webdriver as wb
import urllib
from bs4 import BeautifulSoup
 
driver = wb.Chrome('C:/chromedriver.exe')
url = 'https://www.daraz.com.bd/products/parachute-coconut-oil-200ml-i891741-s3722311.html?spm=a2a0e.searchlistcategory.list.1.2a0b4013akIJTQ&search=1'


def scrollToBottom():
    SCROLL_PAUSE_TIME = 0.09
    last_height = driver.execute_script("return window.scrollY")
    while True:
        driver.execute_script("window.scrollTo(0, window.scrollY + 50)")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return window.scrollY")
        if new_height == last_height:
            break
        last_height = new_height
    

def getDriverSoup(url):
    driver.get(url)
    scrollToBottom()
    return BeautifulSoup(driver.page_source, 'html.parser')


def scrapeImagesOf(url):
    soup = getDriverSoup(url)
    objs = soup.find_all(class_ = 'pdp-common-image review-image__item')
    for objs in objs:
        link = objs.div["style"]
        pos1 = link.find('url("')
        pos2 = link.find(');')
        link = link[pos1+5:pos2-1]
        print("Donloading: ",link)
        urllib.request.urlretrieve(link, str(time.time())+'.jpg')
        
scrapeImagesOf(url)

 
