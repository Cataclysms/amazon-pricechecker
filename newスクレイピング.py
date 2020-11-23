import requests
import bs4
import re
import schedule
import time
import datetime

REMAINING_SEC = 60#間隔
line = "https://notify-api.line.me/api/notify"
access_token = ''#line notify アクセストークン
headers = {'Authorization': 'Bearer ' + access_token}

nowprice = None

def sendmessage(nmessage):
	message = nmessage
	payload = {'message': message}
	r = requests.post(line, headers=headers, params=payload,)

def get_price():
	global nowprice
	source = "https://www.amazon.co.jp/gp/offer-listing/B07X47QTN3/ref=dp_olp_ALL_mbc?ie=UTF8&condition=ALL"
	url = requests.get(source)
	soup = bs4.BeautifulSoup(url.text,"lxml")
	html = soup.select(".a-size-large")
	time = str(datetime.datetime.now())
	#print(soup)
	title = html[0].text.replace(' ','')#str商品title
	lowestprice = html[1].text.replace(',','').replace(' ','').replace('￥','')#str最低価格
	print(title+"現在価格 : "+lowestprice+"円")
	if int(lowestprice) < 23000:#条件
			if nowprice == lowestprice:
				print("前回取得した金額と同じため送信されませんでした")
				return;
			print("通知を送信します・・・")
			sendmessage("\n"+time+title +"\n現在の価格: "+str(lowestprice)+"円")
			sendmessage(source)
	nowprice = lowestprice

if __name__ == '__main__':
	print("========Amazon価格監視ツール========")
	print("現在の設定:　"+str(REMAINING_SEC)+"秒間隔")
	get_price()
	schedule.every(REMAINING_SEC).seconds.do(get_price)
	while True:
		schedule.run_pending()
		time.sleep(1)