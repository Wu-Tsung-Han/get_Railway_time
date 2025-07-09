import requests
from bs4 import BeautifulSoup
import time

url = "https://www.railway.gov.tw/tra-tip-web/tip"
stationDic = {}
today = time.strftime("%Y/%m/%d")
startTime = "06:00"
endTime = "12:00"

def getTrip():
    resp = requests.get(url)
    if resp.status_code != 200:
        print("URL發生錯誤"+url)
        return
    
    soup = BeautifulSoup(resp.text,"html5lib")
    stations = soup.find(id = "cityHot").ul.find_all("li")
    for station in stations:
        stationName = station.button.text
        stationID = station.button["title"]
        stationDic[stationName] = stationID

    csrf = soup.find(id="queryForm").find("input",{"name":"_csrf"})["value"]
    formData = {
        "trainTypeList":"ALL",
        "transfer":"ONE",
        "startOrEndTime":"true",
        "startStation":stationDic["臺北"],
        "endStation":stationDic["新竹"],
        "rideDate":today,
        "startTime":startTime,
        "endTime":endTime
    }
    
    queryUrl = soup.find(id="queryForm")["action"]
    qResp = requests.post("https://www.railway.gov.tw"+queryUrl, data=formData)
    qSoup = BeautifulSoup(qResp.text,"html5lib")
    trs = qSoup.find_all("tr","trip-column")
    for tr in trs:
        td = tr.find_all("td")
        print("%s : %s : %s" % (td[0].ul.li.a.text, td[1].text, td[2].text))

getTrip()