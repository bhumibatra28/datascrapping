from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from time import sleep
import xlwt
from xlwt import Workbook
from uuid import uuid4
import datetime


def getHTMLdocument(url):
    response = requests.get(url)
    return response.text


def bs4Finder(obj, attr=None, class_=None):   
    return obj.find_all(attr, class_=class_)


def urlscrapper(url):    # link scrap of cards 
    print(f'scrapping for link {url} started!')
    html = getHTMLdocument(url)
    soup = BeautifulSoup(html, 'html5lib')
    listOfUrl = []
    collection = bs4Finder(soup, class_="listingContent__mosaic")
    for elem in collection:
        res = bs4Finder(elem, class_="vendorTile__title")
        for i in res:
            listOfUrl.append(i.get('href'))
    print(f'scrapping for link {url} ended!')
    return listOfUrl


def create_link_list(bas_url: str, limit: int, start: int):    #pagenation
    listOfUrl_s = []
    for i in range(start, limit + start):
        listOfUrl_s.append(bas_url + f'&NumPage={i}')
    return listOfUrl_s


driver = webdriver.Chrome(executable_path=".\chromedriver.exe")


def get_details(url):
    driver.get(url)
    sleep(2)
    name = driver.find_element(by=By.CLASS_NAME, value="storefrontHeading__title").text
    location = driver.find_element(by=By.CLASS_NAME, value="storefrontHeading__locationName").text
    btn = driver.find_element(by=By.CLASS_NAME, value="app-default-phone-lead")
    btn.click()
    sleep(2)
    phone = driver.find_element(by=By.CLASS_NAME, value="leadModalPhoneBox__phoneNumber").get_attribute('href')
    return {
        "name": name,
        "location": location,
        "phone": phone
    }


if __name__ == "__main__":
    print("Started!!")
    links = create_link_list(
        bas_url="https://www.weddingwire.in/busc.php?id_grupo=2&id_sector=8",
        limit=9, start=319
    )
    list_of_links = []
    for link in links:
        res = urlscrapper(url=link)
        list_of_links.extend(res)
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    style = xlwt.easyxf('font: bold 1')
    sheet1.write(0, 0, "name", style)
    sheet1.write(0, 1, "location", style)
    sheet1.write(0, 2, "phone", style)
    row = 1
    CURRENT_TIME = "dataset"
    for link in list_of_links:
        res = get_details(link)
        print(res)
        sheet1.write(row, 0, res.get('name'))
        sheet1.write(row, 1, res.get('location'))
        sheet1.write(row, 2, res.get('phone'))
        row = row + 1
        wb.save(f'details{str(CURRENT_TIME)}.xls')