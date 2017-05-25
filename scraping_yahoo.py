# coding: UTF-8
import urllib2
import codecs
import time
from bs4 import BeautifulSoup

# 各ジャンルで取得する記事の数
ARTICLE_NUM = 1

genres = {
"国内" : "domestic" , # p32
"国際" : "world" , # p31
"経済" : "economy" , # p29
"エンタメ" : "entertainment" , # p35
"スポーツ" : "sports" , # p36
"IT・科学" : "computer" , # 29
"地域" : "local" , # p77
}

# アクセスするURL
PICKUP_URL = "https://news.yahoo.co.jp/pickup/"
PAGE_URL = "https://news.yahoo.co.jp/list/?c="

FILE_PATH = "./yahoo_news/"

# 記事番号をもとに記事をダウンロード	
def get_article(no, gn):
	try:
		url = PICKUP_URL + no
		article_html = urllib2.urlopen(url)
		soup = BeautifulSoup(article_html, "html.parser")

	except Exception as e:
		print no + " is 404"
		return

	# タイトル要素を取得する
	title_tag = soup.title
	title = title_tag.string
	# '｜' 以降は時間なので削除
	title = title.partition('|')[0]

	# 記事の内容を抽出
	hbody = soup.find("p", class_="hbody").get_text()

	# ファイルパス / ジャンル / 記事id.txt
	fileName = FILE_PATH + gn + "/" + no + ".txt"

	f = codecs.open(fileName, 'w', 'utf-8')
	article = title + hbody
	f.write(article)
	f.close()

# ページをクロールして記事への有効なリンクの配列を返す
def get_url_list(gn_en):
	url_list = []
	for i in xrange(1,1000):
		# 指定数記事を取得し終えたら終了
		if len(url_list) > ARTICLE_NUM:
			break

		# 記事一覧への URL を生成
		page_url = PAGE_URL + gn_en + "&p=" +str(i)
		print page_url

		# 生成した URL からページを取得，404なら次のページへ
		try:
			page_html = urllib2.urlopen(page_url)
		except Exception as e:
			print str(i) + " is 404"
			continue

		# 記事一覧に含まれている記事へのリンクを抽出して url_list へ格納		
		soup = BeautifulSoup(page_html, "html.parser")
		listArea = soup.find("div", class_="listArea")
		listAreaAs = listArea.find_all("a")

		# リンクに”pickup” が含まれているなら格納	
		for a_s in listAreaAs:
			link = a_s.get("href")
			link = link.encode('UTF-8')
			if link.count('pickup'):
				links = link.split('/')
				url_list.append(links[-1])	

	return url_list

if __name__ == '__main__':
	for genre in genres:
		url_list = get_url_list(genres[genre])

		for no in url_list:
			get_article(no, genres[genre])