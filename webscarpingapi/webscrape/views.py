from bs4 import BeautifulSoup
from django.shortcuts import render
from rest_framework import generics

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# import pandas as pd
import time
# from bs4 import BeautifulSoup
import requests
from csv import writer
# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
    # from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

from rest_framework.decorators import api_view
# driver = webdriver.Chrome(ChromeDriverManager().install())

# executable_path='/home/const/Downloads/chromedriver_linux64/chromedriver'
# driver = webdriver.Chrome(executable_path)

# def view_name(request):
#     return render(request, 'home.html',{})

driver = webdriver.Firefox()
# class TeamViewList(generics.GenericAPIView):
def autologin(driver, url, User_Name, User_Password):
        
        driver.get(url)
        username = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='login']")))
        password = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='password']")))
        print(username)
        # username.clear()
        # password.clear()

        # User_Name = input("Enter the username: ")
        # User_Password = input("Enter the password: ")

        username.send_keys(User_Name)
        password.send_keys(User_Password)
        
        log_in = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[type='submit']"))).click()
        # driver.implicitly_wait(5) 
        
        return driver

def Search(flightType,arrival_cityID,departure_cityID,departDate,arrivalDate,passengers):
        driver.implicitly_wait(3) 
        driver.find_element(By.XPATH,'//*[@id="app"]/div/form/ul/li/label/span[text()="'+flightType+'"]').click()
        driver.find_element(By.XPATH,"//*[@id='app']/div/form/div/div[1]/div/div/div/div[1]/div[1]/div/input[2]").click()

        driver.find_element(By.XPATH,"//*[@id='"+departure_cityID+"']/span").click()
        driver.find_element(By.XPATH,"//*[@id='app']/div/form/div/div[1]/div/div/div/div[1]/div[2]/div/input[2]").click()

        driver.find_element(By.XPATH,"/html/body/div/table/tbody/tr/td/table/tbody/tr[3]/td[1]/div[1]/div/div/form/div/div[1]/div/div/div/div[1]/div[2]/div/ul/li[@id='"+arrival_cityID+"']/span").click()
        departure_date_dropdown = driver.find_element(By.XPATH,"//*[@id='app']/div/form/div/div[1]/div/div/div/div[2]/div[1]/span/input")
        driver.implicitly_wait(1) 
        # departure_date_dropdown.clear()
        departure_date_dropdown.send_keys(departDate)
        
        arrival_date_dropdown = driver.find_element(By.XPATH,"//*[@id='app']/div/form/div/div[1]/div/div/div/div[2]/div[2]/span/input")
        driver.implicitly_wait(1) 
        # arrival_date_dropdown.clear()
        arrival_date_dropdown.send_keys(arrivalDate)
        if passengers > 1:
            passengers = driver.find_element(By.XPATH,"//*[@id='app']/div/form/div/div[2]/div[1]/div").click()
            if passengers == 2:
                driver.find_element(By.XPATH,"//*[@id='app']/div/form/div/div[2]/div[1]/div[2]/div/div/div[1]/ul/li[1]/div/div/span[2]").click()
                driver.find_element(By.XPATH,'//*[@id="app"]/div/form/div/div[2]/div[1]/div[2]/div/div/div[2]/button').click()
                driver.find_element(By.XPATH,'//*[@id="app"]/div/form/div/div[3]/button').click()
            elif passengers == 3:
                driver.find_element(By.XPATH,"//*[@id='app']/div/form/div/div[2]/div[1]/div[2]/div/div/div[1]/ul/li[1]/div/div/span[2]").click()
                driver.find_element(By.XPATH,"//*[@id='app']/div/form/div/div[2]/div[1]/div[2]/div/div/div[1]/ul/li[1]/div/div/span[2]").click()
                driver.find_element(By.XPATH,'//*[@id="app"]/div/form/div/div[2]/div[1]/div[2]/div/div/div[2]/button').click()
                driver.find_element(By.XPATH,'//*[@id="app"]/div/form/div/div[3]/button').click()
            elif passengers == 4:
                driver.find_element(By.XPATH,"//*[@id='app']/div/form/div/div[2]/div[1]/div[2]/div/div/div[1]/ul/li[1]/div/div/span[2]").click()
                driver.find_element(By.XPATH,"//*[@id='app']/div/form/div/div[2]/div[1]/div[2]/div/div/div[1]/ul/li[1]/div/div/span[2]").click()
                driver.find_element(By.XPATH,"//*[@id='app']/div/form/div/div[2]/div[1]/div[2]/div/div/div[1]/ul/li[1]/div/div/span[2]").click()
                driver.find_element(By.XPATH,'//*[@id="app"]/div/form/div/div[2]/div[1]/div[2]/div/div/div[2]/button').click()
                driver.find_element(By.XPATH,'//*[@id="app"]/div/form/div/div[3]/button').click()
        else:
            driver.find_element(By.XPATH,'//*[@id="app"]/div/form/div/div[3]/button').click()
        driver.implicitly_wait(3)
        
        
        soup = BeautifulSoup(driver.page_source)
        lists = soup.find_all("div", {"class":"flight-option"})
        with open('FlightFares.csv', 'w', encoding='utf8', newline='') as f:
            thewriter = writer(f)
            header = ['Title','Price','Arrival Details','Departure Details']
            thewriter.writerow(header)

            for list in lists:

                titles=driver.find_elements(By.XPATH,'//*[@id="trip_1"]/div[1]/div[2]/div/ul/li')
                for i in titles:
                    title = i.text
                    print(title)
                prices = driver.find_elements(By.XPATH,'//div[@class="flight-option"]/div[2]')
                for i in prices:
                    price = i.text
                    print(price)
                price = list.find('span', class_="price").text.replace('\n', '')
        #         print(listtitle)
                departureDetails = list.find('div', class_="time leaving").text
                print(departureDetails)
                arrivalDetails = list.find('div', class_="time landing").text
                print(arrivalDetails)
                flightDuration= list.find('div', class_="flight-stops").text
        #         flightDuration=flightDuration[:-3] + ' : ' + flightDuration[-3:]
                print(flightDuration,'\n')

                
                info = [title,price,departureDetails,arrivalDetails]
                thewriter.writerow(info)
            
def ScrapeData():
        soup = BeautifulSoup(driver.page_source)
        lists = soup.find_all("div", {"class":"flight-option"})
        with open('FlightFares1.csv', 'w', encoding='utf8', newline='') as f:
            thewriter = writer(f)
            header = ['Title','Price','Arrival Details','Departure Details']
            thewriter.writerow(header)

            for list in lists:

                titles=driver.find_elements(By.XPATH,'//*[@id="trip_1"]/div[1]/div[2]/div/ul/li')
                for i in titles:
                    title = i.text
                    print(title)
                prices = driver.find_elements(By.XPATH,'//div[@class="flight-option"]/div[2]')
                for i in prices:
                    price = i.text
                    print(price)
                price = list.find('span', class_="price").text.replace('\n', '')
        #         print(listtitle)
                departureDetails = list.find('div', class_="time leaving").text
                print(departureDetails)
                arrivalDetails = list.find('div', class_="time landing").text
                print(arrivalDetails)
                flightDuration= list.find('div', class_="flight-stops").text
        #         flightDuration=flightDuration[:-3] + ' : ' + flightDuration[-3:]
                print(flightDuration,'\n')

                
                info = [title,price,departureDetails,arrivalDetails]
                thewriter.writerow(info)
                    
@api_view(['POST','GET'])
def scrap(request):
        
        # options = Options()
        # options.headless = True
        # options.add_arguments("--headless", "--window-size=1920,1080", "--disable-gpu", "--disable-extensions", "--no-sandbox", "--incognito")
        # options.add_argument("--window-size=1920,1080")

        # driver = webdriver.Chrome(options=options)

        User_Name = os.getenv("User_Name")
        print(User_Name)
        User_Password = os.getenv("User_Password")
        
        autologin(driver, 'https://www.airblue.com/agents/',User_Name, User_Password,)
        driver.fullscreen_window()
        driver.implicitly_wait(5) 
        Search('One Way','ISB','KHI',"18-May",'22-May',1)
        ScrapeData()
        

# scrap()