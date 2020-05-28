
import requests
import re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
list=['dubai','sharjah', 'abudhabi']
list_rest_final=[]
list_rest_final1=[]
c=0

for city in list:
    list_name = []
    list_name1 = []
    list_name_rep = []
    for page in range(1,25):
        url="https://www.zomato.com/{}/best-online-ordering-restaurants?page={}".format(city,page)
        url1="https://www.zomato.com/{}/best-dine-out-restaurants?page={}".format(city,page)
        response = requests.get(url,headers=headers)
        response1=requests.get(url1,headers=headers)
        print(response1)
        content = response.content
        content1= response1.content
        soup = BeautifulSoup(content,"html.parser")
        soup1 = BeautifulSoup(content1,"html.parser")
        print(soup1.prettify())
        list_tr = soup.find_all("div",attrs={"class": "col-s-11 col-m-12 plr0"})
        list_tr1 = soup1.find_all("div", attrs={"class": "col-s-16 col-m-12 pl0"})
        print(list_tr1)
        for tr in list_tr:
            dataframe ={}
            dataframe["rest_city"]=city
            x1= tr.div.a.text.strip()

            if x1 not in list_name:
                list_name.append(x1)
                dataframe["dine-out"]=""
                dataframe["rest_name"]=re.sub('''[^a-zA-Z \n\'\.\@]''','',x1).strip()
                x=tr.find("div",attrs={"class":"ta-right floating search_result_rating col-s-3 col-l-4 right pr0"})
                dataframe["res_rating"] = x.div.text.strip()
                if dataframe["res_rating"] != "Temporarily Closed":
                    if dataframe["res_rating"]!='-' :
                        if x.span :
                            dataframe["res_votes"]=x.span.text.replace(' votes','')
                        if dataframe["res_rating"] != 'NEW' :
                            if float(dataframe["res_rating"])>=4.0 and int(dataframe["res_votes"])>=100:
                                list_rest_final.append(dataframe)
        for tr in list_tr1:
            c+=1
            dataframe ={}
            dataframe["rest_city"]=city
            x1=tr.find("a",attrs={"class":"result-title hover_feedback zred bold ln24 fontsize0"}).text.strip()

            if x1 in list_name:
                list_name_rep.append(x1)
                for y in list_rest_final:
                    if x1==y["rest_name"]:
                        y["dine-out"]="Yes"
            if x1 not in list_name1 and x1 not in  list_name:
                list_name1.append(x1)
                dataframe["rest_name"]=re.sub('''[^a-zA-Z \n\'\.\@]''','',x1).strip()
                x=tr.find("div",attrs={"class":"ta-right floating search_result_rating col-s-4 clearfix"})
                dataframe["res_rating"] = x.div.text.strip()
                if dataframe["res_rating"]!="Temporarily Closed":
                    if dataframe["res_rating"]!='-' or dataframe["res_rating"]!="Temporarily Closed":
                        if x.span :
                            dataframe["res_votes"]=x.span.text.replace(' votes','')
                        if dataframe["res_rating"] != 'NEW' :
                            if float(dataframe["res_rating"])>=4.0 and int(dataframe["res_votes"])>=100:
                                list_rest_final1.append(dataframe)

import pandas
df = pandas.DataFrame(list_rest_final)
df.to_csv("zomato_res.csv",index=False)
df1 = pandas.DataFrame(list_rest_final1)
df1.to_csv("zomato_res1.csv",index=False)
