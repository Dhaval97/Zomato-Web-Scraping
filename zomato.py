#!/usr/bin/env python
# coding: utf-8

import warnings
warnings.filterwarnings("ignore")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np

loop = True

www = input("Enter Website Link: ")

if www == '':
    loop = False

if loop:
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options = options)

    driver.get(www)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(30)

    website_lst = []
    name_lst = []
    cuisine_lst = []
    phone_lst = []
    address_lst = []

    count = 0
    for i in range(8, 200):
        for j in range(1, 4):
            try:
                website = driver.find_element_by_xpath("//*[@id='root']/div/div["+f'{i}'+"]/div/div["+f'{j}'+"]/div/div/a[1]").get_attribute('href')
            except:
                continue
            if website != '':
                website_lst.append(website)
                count +=1
            else:
                break

    print('\nTotal Restaurants Captured:', count, '\n')

    count1 = 0
    for nm in website_lst:
        driver.get(nm)
    
        name = driver.find_element_by_xpath("//*[@id='root']/div/main/div/section[3]/section/section/div/div/div/h1").text
        name_lst.append(name)
    
        cuisine = driver.find_element_by_xpath("//*[@id='root']/div/main/div/section[3]/section/section/div/div/section[1]/div").text
        cuisine_lst.append(cuisine)
    
        phone = driver.find_element_by_xpath("//*[@id='root']/div/main/div/section[4]/section/article/p").text
        phone_lst.append(phone)
    
        address = driver.find_element_by_xpath("//*[@id='root']/div/main/div/section[4]/section/article/section/p").text
        address_lst.append(address)

        count1 +=1

        print('Total Data Captured:', count1, 'out of', count)

    np_website = np.array(website_lst)
    np_name = np.array(name_lst)
    np_cuisine = np.array(cuisine_lst)
    np_phone = np.array(phone_lst)
    np_address = np.array(address_lst)

    final_lst = np.concatenate(
        (np_website.reshape(len(np_website),1), np_name.reshape(len(np_name),1), np_cuisine.reshape(len(np_cuisine),1), np_phone.reshape(len(np_phone),1),
         np_address.reshape(len(np_address),1))
        ,1)

    df = pd.DataFrame(final_lst, columns = ['Website URL', 'Name', 'Cuisine', 'Phone', 'Address'])
    df.to_csv('web-scraped_data.csv', index = False, encoding='utf-8')

    driver.close()
    
    print("\nCOMPLETED SUCCESSFULLY")
else:
    print('ERROR')
