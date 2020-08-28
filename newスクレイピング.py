import requests
import bs4
import re
import schedule
import time
import datetime

REMAINING_SEC = 10#間隔
line = "https://notify-api.line.me/api/notify"
access_token = ''#line notify アクセストークン
headers = {'Authorization': 'Bearer ' + access_token}

def sendmessage(nmessage):
	message = nmessage
	payload = {'message': message}
	r = requests.post(line, headers=headers, params=payload,)

def get_price():
	source = ""#商品ページURL(新品最安昇順)
	url = requests.get(source)
	soup = bs4.BeautifulSoup(url.text,"lxml")
	time = str(datetime.datetime.now())
	html = soup.select(".a-size-large")
	title = html[0].text.replace(' ','')#str商品title
	lowestprice = html[1].text.replace(',','').replace(' ','').replace('￥','')#str最低価格
	print(title+"現在価格 : "+lowestprice+"円")
	if int(lowestprice) < 23000:#条件
		print("通知を送信します・・・")
		sendmessage("\n"+time+title +"\n現在の価格: "+str(lowestprice)+"円")
		sendmessage(source)

if __name__ == '__main__':
	print("========Amazon価格監視ツール========")
	print("現在の設定:　"+str(REMAINING_SEC)+"秒間隔")
	get_price()
	schedule.every(REMAINING_SEC).seconds.do(get_price)
	while True:
		schedule.run_pending()
		time.sleep(1)