import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import math
from tkinter import Tk, Label, Entry, Button

# import data
location_spot=pd.read_csv("./raw_data/location_spot.csv")
location_mrt=pd.read_csv("./raw_data/location_mrt.csv")
location_mall=pd.read_csv("./raw_data/location_mall.csv")
location_school=pd.read_csv("./raw_data/location_school.csv")
population_density_byli=pd.read_csv("./raw_data/population_density.csv",encoding='Big5')
rent_data=pd.read_csv("./raw_data/rental_data_taipei.csv",encoding="Big5")
data=pd.read_csv("./processed_data/location_dataset_euclidean.csv",encoding='Big5')

# Build the random forest model
forest_model=RandomForestClassifier(n_estimators=100,random_state=87,max_depth=4)
X=data[['MRT_count_1000','mall_distance1000','school_distance1000','spot_distance_2000','pop_density','rental_cost']]
y=data["success"]
forest_model.fit(X,y)

# get coordinate (latitude and longitude) and li (里 = village) of an address by scraping the Taiwan Map website
def get_coordinateandli(addr):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get("http://www.map.com.tw/")
    search = browser.find_element(By.ID, "searchWord")
    search.clear()
    search.send_keys(addr)
    browser.find_element(By.XPATH, "/html/body/form/table/tbody/tr[1]/td/div[4]/table/tbody/tr/td[2]/table/tbody/tr/td[3]/div").click()
    time.sleep(1)    
    iframe = browser.find_element(By.CLASS_NAME, "winfoIframe")
    browser.switch_to.frame(iframe)
    
    addr_detail = browser.find_element(By.XPATH, "/html/body/form/div[4]/table/tbody/tr[1]/td/table/tbody/tr[4]/td").text
    index_before = addr_detail.find('區')
    index_after = addr_detail.find('里')
    li = addr_detail[index_before+1:index_after]
    
    coor_btn = browser.find_element(By.XPATH, "/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
    coor_btn.click()
    coor = browser.find_element(By.XPATH, "/html/body/form/div[5]/table/tbody/tr[2]/td")
    coor = coor.text.strip().split(" ")
    lat = coor[-1].split("：")[-1]
    log = coor[0].split("：")[-1]
    browser.quit()
    # print(lat, log)
    
    return li, lat, log

# calculate the number of MRT stations within 1000 meters
def count_MRT1000(myX,myY):
    mrt_num=0
    for i in range(len(location_mrt)):
        MRT_location=location_mrt.iloc[i,4].split(",")
        MRTX=float(MRT_location[1])
        MRTY=float(MRT_location[0])
        d=math.sqrt(math.pow(111.320*math.cos(myY)*(myX-MRTX),2)+math.pow((myY-MRTY)*110.574,2))
        if d<=1:
            mrt_num=mrt_num+1
    return mrt_num

# calculate the number of malls within 1000 meters
def count_mall1000(myX,myY):
    mall_num=0
    for i in range(len(location_mall)):
        MALL_location=location_mall.iloc[i,3].split(",")
        MALLX=float(MALL_location[1])
        MALLY=float(MALL_location[0])
        d=math.sqrt(math.pow(111.320*math.cos(myY)*(myX-MALLX),2)+math.pow((myY-MALLY)*110.574,2))
        if d<=1:
            mall_num=mall_num+1
    return mall_num

# calculate the number of MRT schools within 1000 meters
def count_school1000(myX,myY):
    school_num=0
    for i in range(len(location_school)):
        school_location=location_school.iloc[i,4].split(",")
        schoolX=float(school_location[1])
        schoolY=float(school_location[0])
        d=math.sqrt(math.pow(111.320*math.cos(myY)*(myX-schoolX),2)+math.pow((myY-schoolY)*110.574,2))
        if d<=1:
            school_num=school_num+1
    return school_num

# calculate the number of famous spots within 2000 meters
def count_spot2000(myX,myY):
    spot_num=0
    for i in range(len(location_spot)):
        spot_location=location_spot.iloc[i,4].split(",")
        spotX=float(spot_location[1])
        spotY=float(spot_location[0])
        d=math.sqrt(math.pow(111.320*math.cos(myY)*(myX-spotX),2)+math.pow((myY-spotY)*110.574,2))
        if d<=2:
            spot_num=spot_num+1
    return spot_num

# get population density
def get_population_density(li):
    li+="里"
    index=population_density_byli[population_density_byli["里名"]==li].index.values
    index=int(index)
    return population_density_byli.iloc[index][2]

# get estimated rent cost
def get_rent_cost(myX,myY):
    
    rent_X=rent_data["longitude"]
    rent_Y=rent_data["latitude"]
    distance=[]
    
    # calculate the euclidean distance between the input address and each location in the rental data
    for j in range(len(rent_data)):
        d=math.sqrt(math.pow(111.320*math.cos(myY)*(myX-rent_X[j]),2)+math.pow((myY-rent_Y[j])*110.574,2))
        distance.append(d)
    
    # take the average rent of the three closest locations as the estimated rent
    first=distance.index(min(distance))
    distance[first]=100
    
    second=distance.index(min(distance))
    distance[second]=100
    
    third=distance.index(min(distance))
    distance[third]=100
    
    cost=(rent_data.iloc[first,5]+rent_data.iloc[second,5]+rent_data.iloc[third,5])/3
    return cost

def analyze():
    current_show.config(text="Analyzing...")
    li_show.config(text="")
    MRT_show.config(text="")
    mall_show.config(text="")
    school_show.config(text="")
    spot_show.config(text="")
    popden_show.config(text="")
    renocost_show.config(text="")
    final_pred_show.config(text="")
    final_lab_show.config(text="")
    win.update()
    
    address=address_entry.get()
    
    li,coordinateY,coordinateX=get_coordinateandli(address)
    coordinateY=float(coordinateY)
    coordinateX=float(coordinateX)
    
    lishow_text = "Location: " + address + " (" + li + ")"
    li_show.config(text=lishow_text)
    
    MRT_count_1000=count_MRT1000(coordinateX,coordinateY)
    mrtshow_text="MRT stations within 1000m: "+str(MRT_count_1000)
    MRT_show.config(text=mrtshow_text)
    
    mall_count_1000=count_mall1000(coordinateX,coordinateY)
    mallshow_text="Malls within 1000m: "+str(mall_count_1000)
    mall_show.config(text=mallshow_text)
    
    school_count_1000=count_school1000(coordinateX,coordinateY)
    schoolshow_text="Schools within 1000m: "+str(school_count_1000)
    school_show.config(text=schoolshow_text)
    
    spot_count_2000=count_spot2000(coordinateX,coordinateY)
    spotshow_text="Attractions within 2000m: "+str(spot_count_2000)
    spot_show.config(text=spotshow_text)
    
    population_density=get_population_density(li)
    popudenshow_text="Population density (per km²): "+str(round(population_density,2))
    popden_show.config(text=popudenshow_text)
    
    rent_cost=get_rent_cost(coordinateX,coordinateY)
    rentcost_text="Estimated rent (per m²): "+str(round(rent_cost,2))
    renocost_show.config(text=rentcost_text)
    
    X_query=np.array([MRT_count_1000,mall_count_1000,school_count_1000,spot_count_2000,population_density,rent_cost])
    outcome=forest_model.predict_proba(X_query.reshape(1, -1))
    final_lab_show.config(text="Store Opening Success Prediction=")
    outcome_text=str(round(outcome[0][1]*100,2))+"%"
    final_pred_show.config(text=outcome_text)
    
    current_show.config(text="Analysis Result:")

# simple GUI created by TKinter
win=Tk()
win.title("Location Selection Analysis for Beverage Stores")
win.geometry("800x600+800+200")
general_font = "Arial 12"

topic_lab=Label(text="Location Selection Analysis for Beverage Stores")
topic_lab.config(font="Arial 20 bold underline")
topic_lab.place(x=35,y=30)

input_remind=Label(text="Please enter the address for the store")
input_remind.config(font=general_font)
input_remind.place(x=35,y=100)

input_example=Label(text="(Example: 台北市大安區羅斯福路四段1號) ")
input_example.config(font=general_font)
input_example.place(x=35,y=120)

address_entry=Entry()
address_entry.config(font=general_font)
address_entry.place(x=35,y=160,width=500)

btn_analysis=Button(text="Start Prediction",command=analyze)
btn_analysis.config(font=general_font)
btn_analysis.place(x=600,y=110,width=150,height=60)

current_show=Label(text="")
current_show.config(font=general_font)
current_show.place(x=35,y=200)

li_show=Label(text="")
li_show.config(font=general_font)
li_show.place(x=35,y=240)

MRT_show=Label(text="")
MRT_show.config(font=general_font)
MRT_show.place(x=35,y=280)

mall_show=Label(text="")
mall_show.config(font=general_font)
mall_show.place(x=35,y=320)

school_show=Label(text="")
school_show.config(font=general_font)
school_show.place(x=35,y=360)

spot_show=Label(text="")
spot_show.config(font=general_font)
spot_show.place(x=35,y=400)

popden_show=Label(text="")
popden_show.config(font=general_font)
popden_show.place(x=35,y=440)

renocost_show=Label(text="")
renocost_show.config(font=general_font)
renocost_show.place(x=35,y=480)

final_lab_show=Label(text="")
final_lab_show.config(font=general_font)
final_lab_show.place(x=450,y=240)

final_pred_show=Label(text="")
final_pred_show.config(font="Arial 55 underline")
final_pred_show.place(x=450,y=280)

win.mainloop()



