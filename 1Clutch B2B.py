from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import time
from bs4 import BeautifulSoup
# import requests
from csv import writer


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


# if queryset:
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.get("https://clutch.co/")

Niche = input('Enter Niche Name: ')

name = driver.find_element(By.XPATH,'//*[@id="services"]')

name.send_keys(Niche)
driver.implicitly_wait(5)
time.sleep(5)

name.send_keys(Keys.ENTER)
driver.implicitly_wait(5)
time.sleep(2)
name.send_keys(Keys.ENTER)
driver.implicitly_wait(5)
time.sleep(1)

lists=[]
urls=[]
pages = driver.find_elements(By.XPATH,'//*[@id="providers"]/nav/ul/li')
# print(pages)
for i in pages:
#     print(i)
    url=i.find_element(By.TAG_NAME,'a')
    urls.append(url.get_attribute('href'))
for i in urls:
    page = driver.get(i)
    data = driver.find_elements(By.CLASS_NAME, 'company_info')

    for i in data:
#         print((i))
        links=i.find_element(By.TAG_NAME,'a')
#         print(links)

    #     links = [link.get_attribute('href') for link in links]
        lists.append(links.get_attribute('href'))
driver.implicitly_wait(3)
    

# response= HttpResponse(content_type='text/csv')
with open(Niche+'.csv', 'w', encoding='utf8', newline='') as f:
    thewriter = writer(f)
    header = ['Review','ReviewDate', 'Ratings', "ReviewerCompany","Person", "SpentAmount","Link","ProjectTimeline"]
    thewriter.writerow(header)
    print(len(lists))
    for link in lists:
        print(link)
        time.sleep(1)
#         page = requests.get(link)
        print(driver.get(link))
        driver.get(link)
        
        time.sleep(3)
        # driver.implicitly_wait(5)
#         print(page)
        #Extra WORK
#         R_lists=[]
        R_urls=[]
        R_pages = driver.find_elements(By.XPATH,'//*[@id="profile-feedback"]/div[3]/ul/li')
        # print(R_pages)
        for i in R_pages:
        #     print(i)
            R_url=i.find_element(By.TAG_NAME,'a')
            R_urls.append(R_url.get_attribute('href'))
        
#         pages = driver.find_elements(By.XPATH,'//*[@id="profile-feedback"]/div[3]/ul/li')
        #END EXTRA WORK
        
        review = driver.find_element(By.XPATH,'//*[@id="profile-main-nav"]/li[4]/a').click()
        driver.implicitly_wait(2)
        #Extra WORK
        R_urls=set(R_urls)
        if len(R_urls) > 0:
            print("IF CHALA")
            for i in R_urls:
                time.sleep(1)
                page = driver.get(i)
                time.sleep(3)
                # driver.implicitly_wait(5)
                review = driver.find_element(By.XPATH,'//*[@id="profile-main-nav"]/li[4]/a').click()
                R_pages = driver.find_elements(By.XPATH,'//*[@id="profile-feedback"]/div[3]/ul/li')
            #END EXTRA WORK
                soup = BeautifulSoup(driver.page_source)
                comp = soup.find_all("div", {"class":"review_data--container"})
        #         print(comp)

                for list in comp:
                    rating = list.find('span',class_="rating sg-rating__number").text.replace('\n', '')
        #       try:
                    rating = float(rating)


        #             print(type(float(rating)))
                    if rating < 4.0:
#                         print("Rating",rating)

                        url = link
                        try:
                            review1 = list.find('div', class_="field field-name-client-quote field-inline").find('p')
#                             print(review1)
                            if review1 is not None:
                                review = review1.text.replace('\n', '')
#                                 print("Review",review)
            #                                     return
                            else:
                                review = "No Review Found"
                        except:
                            review = "No Review Found"

                        company1 = list.find('div', class_="field-name-title")
                        if company1 is not None:

                            company = company1.text.replace('\n', '')
#                             print("company",type(company))
                        else:

                            company = "No Company Found"
                        try:
                            date1 = list.find('div', class_="field field-name-project-length field-inline custom_popover").find('div',class_="field-item")
                            if date1 is not None:    
                                date=date1.text.replace('\n', '')
#                                 print("date",date)
                            else:
                                date = "No Date Found"
                        except:
                            date = "No Date Found"
                        try:   
                            person1 = list.find('div', class_="field-name-full-name-display").find('div',class_="field-item")
#                             print(person1)
                            if person1 is not None:
                                person=person1.text.replace('\n', '')
#                                 print("Person",person)
                            else:
                                person = "No Person Found"
                        except:
                            person = "No Person Found"
                        try:   
                            reviewDate1 = list.find('div', class_="col-md-6 col-lg-7 review-col-reviewtxt").find("h5",class_="h5_title date")
#                             print(reviewDate1)
                            if reviewDate1 is not None:
                                reviewDate = reviewDate1.text.replace('\n', '')
#                                 print("reviewDate",reviewDate)
                            else:
                                reviewDate = "No reviewDate Found"
                        except:
                            reviewDate = "No reviewDate Found in except"
                        try:
                            cost1 = list.find('div', class_="field field-name-cost field-inline custom_popover").find('div',class_="field-item")
                            if cost1 is not None:    
                                cost=cost1.text.replace('\n', '')
#                                 print("COst",cost)
                            else:
                                cost = "No Cost Found"
            #               print(info)
                        except:
                            cost = "No Cost Found"
                        info2 = [review,reviewDate,rating,company,person,cost,url,date]
                        print("-------",info2)
                        thewriter.writerow(info2)
            # driver. quit()
        else:
            print("ELSE CHALA")
            soup = BeautifulSoup(driver.page_source)
            comp = soup.find_all("div", {"class":"review_data--container"})
        #         print(comp)

            for list in comp:
                    rating = list.find('span',class_="rating sg-rating__number").text.replace('\n', '')
        #       try:
                    rating = float(rating)


        #             print(type(float(rating)))
                    if rating < 4.0:
                        print("Rating",rating)

                        url = link
                        try:
                            review1 = list.find('div', class_="field field-name-client-quote field-inline").find('p')
#                             print(review1)
                            if review1 is not None:
                                review = review1.text.replace('\n', '')
#                                 print("Review",review)
            #                                     return
                            else:
                                review = "No Review Found"
                        except:
                            review = "No Review Found"

                        company1 = list.find('div', class_="field-name-title")
                        if company1 is not None:

                            company = company1.text.replace('\n', '')
#                             print("company",type(company))
                        else:

                            company = "No Company Found"
                        try:
                            date1 = list.find('div', class_="field field-name-project-length field-inline custom_popover").find('div',class_="field-item")
                            if date1 is not None:    
                                date=date1.text.replace('\n', '')
#                                 print("date",date)
                            else:
                                date = "No Date Found"
                        except:
                            date = "No Date Found"
                        try:   
                            person1 = list.find('div', class_="field-name-full-name-display").find('div',class_="field-item")
#                             print(person1)
                            if person1 is not None:
                                person=person1.text.replace('\n', '')
#                                 print("Person",person)
                            else:
                                person = "No Person Found"
                        except:
                            person = "No Person Found"
                        try:   
                            reviewDate1 = list.find('div', class_="col-md-6 col-lg-7 review-col-reviewtxt").find("h5",class_="h5_title date")
#                             print(reviewDate1)
                            if reviewDate1 is not None:
                                reviewDate = reviewDate1.text.replace('\n', '')
#                                 print("reviewDate",reviewDate)
                            else:
                                reviewDate = "No reviewDate Found"
                        except:
                            reviewDate = "No reviewDate Found in except"
                        try:
                            cost1 = list.find('div', class_="field field-name-cost field-inline custom_popover").find('div',class_="field-item")
                            if cost1 is not None:    
                                cost=cost1.text.replace('\n', '')
#                                 print("COst",cost)
                            else:
                                cost = "No Cost Found"
            #               print(info)
                        except:
                            cost = "No Cost Found"
                        info2 = [review,reviewDate,rating,company,person,cost,url,date]
                        print("-------",info2)
                        thewriter.writerow(info2)
