import csv
import requests
from bs4 import BeautifulSoup

#csv 파일 생성
filename = "합격자소서_경영사무_.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

title = "회사,직무,자소서".split(",")
# print(type(title))
writer.writerow(title)

url_2 = 'https://www.jobkorea.co.kr/starter/PassAssay?FavorCo_Stat=0&Pass_An_Stat=0&OrderBy=0&EduType=0&WorkType=0&schPart=10012&isSaved=1&Page='

#30페이지까지 = 600개까지
for page in range(1,31):
    res = requests.get(url_2 + str(page))
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    CVs = soup.find_all("p", attrs={"class" : "tit"})
    for CV in CVs:
    # 회사, 직무명
        name = CV.find("span", attrs={"class": "titTx"}).get_text()
        field = CV.find_all("span",attrs={"class":"field"}, limit=2)
        field_2 = field[1].get_text()
    # 기간 초과 skip
        year = CV.find("span", attrs={"class" : "career"}).get_text()[:4]
        if int(year) < 2018:
            continue
        link = "https://www.jobkorea.co.kr" + CV.a["href"]
        res2 = requests.get(link)
        res2.raise_for_status()
        soup2 = BeautifulSoup(res2.text, "lxml")
        texts = soup2.find_all('div', attrs={'class':'tx'})
        text_sum = ""
        for i in texts:
            texts_b = i.find_all('b')
            for j in texts_b:
                text_b = j.text
                text_sum += text_b
        data = [name, field_2, text_sum]
        writer.writerow(data)


    #show > div 첫번째꺼 문자 가져오는걸로 바꿔보기..