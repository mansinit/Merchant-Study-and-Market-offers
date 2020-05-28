import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
import seaborn as sns
import pandas as pd
import re


def create_graphs(interest_over_time_df,string):
    sns.set(color_codes=False)
    ax = interest_over_time_df.plot.line(figsize=(9, 6),title="Interest Over Time")
    ax.set_xlabel('Date')
    ax.set_ylabel('Trends Index')
    ax.tick_params(axis='both', which='major', labelsize=13)
    ax.figure.savefig('static/plot_'+string+'.png')

def create_excel(interest_over_time_df,name_list,string,final):
    interest_over_time_df.reset_index(level=0, inplace=True)
    interest_over_time_df.to_excel('static/trends_'+string+'_'+final+'.xlsx')


def food_delivery_pytrends(name_list):
    pytrend=TrendReq()
    pytrend.build_payload(kw_list=name_list,geo='AE', timeframe='today 12-m', cat=71)
    interest_over_time_df = pytrend.interest_over_time()
    interest_over_time_df = interest_over_time_df.drop('isPartial', axis=1)
    return interest_over_time_df
def offline_hypermarkets_pytrends(kw):
    pytrend = TrendReq()

    pytrend.build_payload(kw_list=kw, geo='AE', timeframe='today 12-m', cat=0)
    # pytrend.build_payload(kw_list=kw, geo='AE', timeframe='today 12-m', cat=68)
    interest_over_time_df = pytrend.interest_over_time()
    interest_over_time_df = interest_over_time_df.drop('isPartial', axis=1)

    return interest_over_time_df

def online_clothing_pytrends(kw):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=kw, geo='AE', timeframe='today 12-m', cat=68)
    interest_over_time_df = pytrend.interest_over_time()
    interest_over_time_df = interest_over_time_df.drop('isPartial', axis=1)
    return interest_over_time_df

def electronics_pytrends(kw):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=kw, geo='AE', timeframe='today 12-m', cat=5)
    interest_over_time_df = pytrend.interest_over_time()
    interest_over_time_df = interest_over_time_df.drop('isPartial', axis=1)

    return interest_over_time_df

def furniture_pytrends(kw):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=kw, geo='AE', timeframe='today 12-m', cat=270)
    interest_over_time_df = pytrend.interest_over_time()
    interest_over_time_df = interest_over_time_df.drop('isPartial', axis=1)
    return interest_over_time_df

def fastfood_pytrends(kw):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=kw, geo='AE', timeframe='today 12-m', cat=71)
    interest_over_time_df = pytrend.interest_over_time()
    interest_over_time_df = interest_over_time_df.drop('isPartial', axis=1)
    return interest_over_time_df

def jewelry_pytrends(kw):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=kw, geo='AE', timeframe='today 12-m', cat=124)
    interest_over_time_df = pytrend.interest_over_time()
    interest_over_time_df = interest_over_time_df.drop('isPartial', axis=1)
    return interest_over_time_df

def keywords_less_than_5(name_list,string):
    if string=="food_apps":
        interest_over_time_df=food_delivery_pytrends(name_list)
    elif string=="online_clothing":
        interest_over_time_df=online_clothing_pytrends(name_list)
    elif string=="offline_hypermarkets":
        interest_over_time_df=offline_hypermarkets_pytrends(name_list)
    elif string == "electronics":
        interest_over_time_df = electronics_pytrends(name_list)
    elif string == "furniture":
        interest_over_time_df = furniture_pytrends(name_list)
    elif string == "fast_food":
        interest_over_time_df = fastfood_pytrends(name_list)
    elif string == "jewelry":
        interest_over_time_df = jewelry_pytrends(name_list)

    print("************************************************************************")
    print(interest_over_time_df.mean(0))
    print(name_list)
    print("************************************************************************")
    create_graphs(interest_over_time_df,string)
    create_excel(interest_over_time_df,name_list,string,"final")

def middle_product(interest_over_time_df):
    avg_list = interest_over_time_df.mean(0)
    print(avg_list)
    x = {k: v for k, v in sorted(avg_list.items(), key=lambda item: item[1])}
    j = 0
    for key in x:
        if (j == 2):
            middle_brand = (key)
            avg_value=x[key]
        j = j + 1

    return middle_brand,avg_value


def scaling_func(df,avg_val_prev):
    scaling_list=df.values[-1].tolist()
    common=scaling_list[len(scaling_list)-1]
    list=[]
    for y in scaling_list:
        y=y*avg_val_prev/common
        list.append(y)
    return list
def keywords_more_than_5(searches,string):
    i = 0
    middle_brand = ""
    interest_over_time_df = {}
    count = 0
    flag=0
    while i < len(searches) :
        kw = []
        if i < len(searches):
            kw.append(searches[i])
        if i + 1 < len(searches):
            kw.append(searches[i + 1])
        if i + 2 < len(searches):
            kw.append(searches[i + 2])
        if i + 3 < len(searches):
            kw.append(searches[i + 3])
        if i == 0:
            if i + 4 < len(searches):
                kw.append(searches[i + 4])
            flag=1
            i=i+5
        else:
            flag=0
            kw.append(middle_brand[0])
            prev_middle_brand=middle_brand[1]
            i = i + 4
        if string == "food_apps":
            interest_over_time_df[count] = food_delivery_pytrends(kw)
        elif string == "online_clothing":
            interest_over_time_df[count] = online_clothing_pytrends(kw)
        elif string == "offline_hypermarkets":
            interest_over_time_df[count] = offline_hypermarkets_pytrends(kw)
        elif string == "electronics":
            interest_over_time_df[count] = electronics_pytrends(kw)
        elif string == "furniture":
            interest_over_time_df[count] = furniture_pytrends(kw)
        elif string == "fast_food":
            interest_over_time_df[count] = fastfood_pytrends(kw)
        elif string == "jewelry":
            interest_over_time_df[count] = jewelry_pytrends(kw)
        if kw[len(kw)-2]!=searches[len(searches)-1]:
            middle_brand = middle_product(interest_over_time_df[count])

        interest_over_time_df[count].loc['mean'] = interest_over_time_df[count].mean(0)
        if flag==1:
            interest_over_time_df[count].loc['scaling']=interest_over_time_df[count].mean(0)
        else:
            print(middle_brand[1])
            interest_over_time_df[count].loc['scaling']=scaling_func(interest_over_time_df[count],prev_middle_brand)
        count += 1
    df = pd.concat(interest_over_time_df, axis=1)
    df.columns = df.columns.droplevel(0)
    create_excel(df,searches,string,"")
    scaling_list=df.values[-1].tolist()
    keyword_list=list(df.columns.values)
    dict={}
    keyword_list=keyword_list[1:]
    scaling_list=scaling_list[1:]
    for i in range(0,len(keyword_list)):
        dict[keyword_list[i]]=scaling_list[i]
    x = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1],reverse=True)}
    list_x=[]
    for key in x:
        list_x.append(key)
    print(list_x[0:5])
    keywords_less_than_5(list_x[0:5],string)

def food_apps(url,headers):
    response = requests.get(url,headers=headers)
    content = response.content
    soup = BeautifulSoup(content,"html.parser")
    list_tr = soup.find_all("div",attrs={"class": "ic-common-section ic-blog-description-page"})
    name_list=[]
    for tr in list_tr:
        x=(tr.find_all('h2'))
        for y in x:
            name_list.append(y.text)
    print(name_list)
    if len(name_list)<=5:
        keywords_less_than_5(name_list,"food_apps")
    else:
        keywords_more_than_5(name_list,"food_apps")

def online_clothing(driver):
    results = driver.find_elements_by_xpath("/html/body/section[2]/div/div/div/div/p[3]")
    tx=[]
    for res in results:
        t = res.find_elements_by_tag_name('strong')
        for tr in t:
            if "Code" not in tr.text:
                tx.append(tr.text.strip(':'))
    if len(tx)<=5:
        keywords_less_than_5(tx,"online_clothing")
    else:
        keywords_more_than_5(tx,"online_clothing")

def electronics(driver):
    results = driver.find_elements_by_xpath("/html/body/section[2]/div/div/div/div/p[11]")
    tx=[]
    for res in results:
        t = res.find_elements_by_tag_name('strong')
        for tr in t:
            if "Code" not in tr.text:
                tx.append(tr.text.strip(':'))
    if len(tx)<=5:
        keywords_less_than_5(tx,"electronics")
    else:
        keywords_more_than_5(tx[0:len(tx)-1],"electronics")

def furniture(driver):
    results = driver.find_elements_by_xpath("/html/body/section[2]/div/div/div/div/p[5]")
    tx=[]
    for res in results:
        t = res.find_elements_by_tag_name('strong')
        for tr in t:
            if "Code" not in tr.text:
                tx.append(tr.text.strip(':'))
    if len(tx)<=5:
        keywords_less_than_5(tx,"furniture")
    else:
        keywords_more_than_5(tx,"furniture")

def offline_hypermarket(url,headers):
    response = requests.get(url, headers=headers)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    list_tr = soup.find_all("div", attrs={"class": "thumb-slid"})
    name_list=[]
    for tr in list_tr:
        x = (tr.find_all('h3'))
        for y in x:
            name_list.append(y.text)
    print(name_list)
    if len(name_list)<=5:
        keywords_less_than_5(name_list,"offline_hypermarkets")
    else:
        keywords_more_than_5(name_list,"offline_hypermarkets")
def jewelry(url,headers):
    response = requests.get(url, headers=headers)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    list_tr = soup.find_all("div", attrs={"class": "thumb-slid"})
    name_list=[]
    for tr in list_tr:
        x = (tr.find_all('h3'))
        for y in x:
            name_list.append(y.text)
    print(name_list)
    if len(name_list)<=5:
        keywords_less_than_5(name_list,"jewelry")
    else:
        keywords_more_than_5(name_list,"jewelry")

def fast_food(driver):
    results = driver.find_elements_by_xpath("/html/body/div[3]/ui-view/section/div/div[2]/div/div[2]/div/div[2]")
    list = []
    for res in results:
        link = res.find_elements_by_tag_name('a')
        for x in link:
            product_link = x.get_attribute("href")
            name = product_link[28:]
            name = re.sub('''[^a-zA-Z \n\'\.\@]''', ' ', name).strip()
            if "tgo" in name:
                name = name.split()[0]
            if name not in list and len(list) < 10:
                list.append(name)
    if len(list)<=5:
        keywords_less_than_5(list,"fast_food")
    else:
        keywords_more_than_5(list,"fast_food")

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
import os

folder = '../static/'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    os.remove(file_path)
food_apps("https://www.icoderzsolutions.com/blog/top-5-food-delivery-apps-in-uae/",headers)
offline_hypermarket("https://www.uaet10.com/listings/hypermarket/carrefour-dubai",headers)

from selenium import webdriver
driver = webdriver.Chrome(executable_path='C:\\Users\\Mansi Dhingra\\Downloads\\chromedriver.exe')
driver.get("https://liv.me/liv4deals")
online_clothing(driver)
electronics(driver)
furniture(driver)
driver.get("https://www.talabat.com/uae/top-selling")
fast_food(driver)
jewelry('https://www.uaet10.com/listings/top-jewellery/de-beers',headers)