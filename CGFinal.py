
import io
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

from secrets import username, password


mobile_emulation = { "deviceName": "iPhone X" }

options = webdriver.ChromeOptions()
options.add_argument('--disable-notifications')
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(options=options)




def login():

    driver.get("https://www.facebook.com/login")

    sleep(2)

    email_in = driver.find_element_by_xpath('//*[@name="email"]')
    email_in.send_keys(username)

    password_in = driver.find_element_by_xpath('//*[@name="pass"]')
    password_in.send_keys(password)

    login_btn =driver.find_element_by_xpath('//*[@name="login"]')
    login_btn.click()

    sleep(5)

def goto(RU):

    REQUEST_URL = RU
    driver.get(REQUEST_URL)


#facebook 0
def get_comments0():

    all_comments = []

    last_height=''
    while True:
        
        for i in range(1,15):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
                break
        else:
                last_height = new_height
        try:
            driver.find_element_by_partial_link_text("View more comments…").click()
        except NoSuchElementException:
            break
        

    while True:
        try:
            driver.find_element_by_class_name("_4ayj").click()
            sleep(1)
        except NoSuchElementException:
            break

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    comment = soup.find_all('div', {'data-sigil':"comment-body"})
    
    for c in comment:
        all_comments.append(c.text)



    with io.open('comments.txt', "w", encoding="utf-8") as f:
        for element in all_comments:
            f.write(element+'\n')
    
    print("Done! Thank you for you patience")




print("Enter Facebook Post URL:")
RU=input()
login()
goto(RU)
get_comments0()