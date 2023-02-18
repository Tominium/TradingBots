from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import urllib3
import requests
import json
import time
import tkinter as tk

def whole_thing():
    def keysearch(key):
        starttime = time.time()
        url = 'https://www.supremenewyork.com/mobile_stock.json'
        response = requests.get(url=url)
        data = json.loads(response.content.decode('utf-8'))
        mylist = []
        global mylists
        mylists = mylist
        for items in data['products_and_categories']:
            if items != 'new':
                categories = items
            for x in categories.split():
                for result in data['products_and_categories']['{}'.format(x)]:
                    if keyword in result['name'].lower():
                        print('Product Found!')
                        name = result['name']
                        id = result['id']
                        cat = result['category_name']
                        price = '${}'.format(result['price']*.01)
                        link = 'https://www.supremenewyork.com/shop/{}'.format(id)
                        mylist.append(id)
                        print(len(mylist), end=""),
                        print('.)', end = ""),
                        print(name,'-',cat, '-', price)
                        browser = webdriver.Safari()
                        browser.get(link)
                        ###size selection
                        white = "//img[contains(@alt,'White')]"
                        black = "//img[contains(@alt,'Black')]"
                        large = '//*[@id="s"]/option[2]'
                        xlarge = '//*[@id="s"]/option[3]'
                        medium = '//*[@id="s"]/option[1]'
                        print("size selected")
                        #browser.find_element_by_xpath("//img[contains(@alt,'Black')]").click()

                        ###size selections

                        if browser.find_element_by_xpath('//*[@id="s"]').is_displayed():
                            print("Element found")
                            browser.find_element_by_xpath('//*[@id="s"]').click()
                            print("dipper")
                            browser.find_element_by_xpath(large).click()
                            browser.find_element_by_id('add-remove-buttons').click()
                        else:
                            print("Element not found")
                            browser.find_element_by_id('add-remove-buttons').click()
                            print('ran stuff')

                        ###add to cart
                        #browser.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()

                        ###check out
                        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, 'cart'))).click()

                        ###name
                        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="order_billing_name"]'))).send_keys('Tomin Chazhikat')

                        ###email
                        browser.find_element_by_xpath('//*[@id="order_email"]').send_keys('tchazhikat@gmail.com')

                        ###telephone number
                        browser.find_element_by_xpath('//*[@id="order_tel"]').send_keys('8323615216')

                        ###address
                        browser.find_element_by_xpath('//*[@id="bo"]').send_keys('6326 Grand Butte Court')

                        ###apt_num
                        ##browser.find_element_by_xpath('//*[@id="oba3"]').send_keys('01')

                        ###zip_code
                        browser.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys('77494')

                        ###city
                        browser.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys('Katy')

                        ###state
                        browser.find_element_by_xpath('//*[@id="order_billing_state"]').click()
                        Select(browser.find_element_by_xpath('//*[@id="order_billing_state"]')).select_by_value('TX')

                        ###country
                        browser.find_element_by_xpath('//*[@id="order_billing_country"]').click()
                        Select(browser.find_element_by_xpath('//*[@id="order_billing_country"]')).select_by_value('USA')

                        ###credit card
                        browser.find_element_by_xpath('//*[@id="rnsnckrn"]').send_keys('4345234523452345')

                        browser.find_element_by_xpath('//*[@id="credit_card_month"]')
                        Select(browser.find_element_by_xpath('//*[@id="credit_card_month"]')).select_by_value('04')

                        browser.find_element_by_xpath('//*[@id="credit_card_year"]')
                        Select(browser.find_element_by_xpath('//*[@id="credit_card_year"]')).select_by_value('2023')

                        browser.find_element_by_xpath('//*[@id="orcer"]').send_keys('123')

                        browser.find_element_by_xpath(".//*[contains(text(), 'I have read and agree to the ')]").click()
                        #######

    keyword = entry.get()
    keylist = keyword.split(",")
    print()

    for keyword in keylist:
        keysearch(keyword)

    for _ in range(240):
        try:
            if not mylists:
                print('Product Not Found, Will Look Again...')
                time.sleep(0.25)
                keysearch(keyword)
        except Exception as e:
            print('{}: or Webstore Closed'.format(e))
    print('Program Ended')
    print('------------------------------------------------------------------------------------------------------------')

r = tk.Tk()

r.title('Supreme Bot')
r.geometry('500x250')
entry = tk.Entry(r, text='Enter Keyword(s)')
button = tk.Button(r, text='Start Bot', width='25', command=whole_thing)
entry.pack(fill='both', expand=True, padx=20, pady=20)
button.pack(fill='both', expand=True, padx=20, pady=20)
r.mainloop()
