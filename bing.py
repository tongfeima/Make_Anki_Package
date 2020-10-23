import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
def sub_space(search_word):
	if ' ' in search_word:
		new = re.sub(' ','+',search_word)
		return new
	else:
		return search_word

def is_Chinese(search_word):
    for ch in search_word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False
def enORch(search_word):
	if is_Chinese(search_word)== False:
		html = urllib.request.urlopen(f"https://cn.bing.com/dict/{search_word}"
		).read().decode('utf-8')
	else:
		search_word = urllib.parse.quote(search_word)
		html = urllib.request.urlopen(f"https://cn.bing.com/dict/search?q={search_word}"
		).read().decode('utf-8')
	return html
def edit_des(result2):
	text=''
	count=1
	end=len(result2)
	for i in result2:
		i_text=i.get_text()
		if count==end:
			i_text=re.sub(r'^..','网络释义: ',i_text)
			text = text+ i_text
		else:
			text = text+ i_text +'\n'
			count+=1
	return(text)

def bing(search_word):
	search_word=sub_space(search_word)
	try:html = enORch(search_word)
	except urllib.error.HTTPError:
		return('网络错误')
	except http.client.InvalidURL:
		return('请输入正确的英文或者中文（NameError）')

	else:

		soup = BeautifulSoup(html,features = 'lxml')
		result = soup.find('div',{'class':'qdef'})
		
		result2 = result.find_all('li')

		if result2==[]:
			return('抱歉，没有找到')
		else:
			return(edit_des(result2))
