import asyncio
import os
import time
import json
from bs4 import BeautifulSoup
from pyppeteer import launch
import pdfkit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
from pyhtml2pdf import converter

async def main():

    driver = webdriver.Chrome()
    driver.get("https://abrahamjuliot.github.io/creepjs/")
    driver.maximize_window()

    time.sleep(10)
    return driver.page_source


html_response = asyncio.get_event_loop().run_until_complete(main())
with open('temp.html', 'w', encoding="utf-8") as tem:
    tem.write(html_response)
dict1 = dict(Fb_id="", trust_score="", lies="", bot="")
soup = BeautifulSoup(html_response, 'html.parser')
title = soup.find('div', class_="ellipsis-all").find_all("span")
list1 = [name.text.strip() for name in title]
str1 = "".join(list1)
dict1['Fb_id'] = str1
dom = etree.HTML(str(soup))
truS = dom.xpath('//*[@id="fingerprint-data"]/div[2]/div/div[1]/div[1]/span')[0].text
dict1['trust_score'] = str(truS).strip()

lis = dom.xpath('//*[@id="fingerprint-data"]/div[2]/div/div[2]/div[2]')[0].text
dict1['lies'] = str(lis).strip()

bott = dom.xpath('//*[@id="fingerprint-data"]/div[2]/div/div[2]/div[5]/div[2]/div[1]')[0].text
dict1['bot'] = str(bott).strip()
print(dict1)


config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

# converting html file to pdf file
#pdfkit.from_file("temp.html", 'output.pdf', configuration=config)
for i in range(3):
    path = os.path.abspath('temp'+str(i+1)+'.html')
    converter.convert(f'file:///{path}', 'sample.pdf')
    with open('webscraping'+str(i+1)+'.json', 'w') as outfile:
        json.dump(dict1, outfile, indent=4)
