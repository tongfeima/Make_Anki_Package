import os
import pickle
import genanki
import time
import requests
import re

#user_name = os.environ['USERNAME']
#path = f'C:/Users/{user_name}/OneDrive/我的文档/生词本.pickle'
path = f'./生词本.pickle'
def store_word(word,description):
	with open(path, 'ab') as file:
            tup = (word,description)
            pickle.dump(tup,file)
def get_word():
    dic = {}
    with open(path,'rb') as file:
        while True:
            try:
                tup = pickle.load(file)
                dic[tup[0]] = tup[1]
            except EOFError:
                break
    return dic


front_style = '''<div style="
 font-family:微软雅黑;
 font-size: 26px;
 text-align: center;
 color: black;
 background-color: ;">
{{正面}}</div> {{音频}}'''

back_style = '''{{FrontSide}} 
<hr id=answer>
<div style="
 font-family:微软雅黑;
 font-size: 20px;
 text-align: center;
 margin: 5px 20px;
 color: black;
 background-color: ;">
{{背面}}</div> {{音频}}'''

my_model = genanki.Model(
    1091735104,'基础',
    fields=[
        {'name': '正面'},
        {'name': '背面'},
        {'name': '音频'}
    ],
    templates=[
        {
            'name': '卡片1',
            'qfmt': front_style, 
            'afmt': back_style,
        },
    ])

my_deck = genanki.Deck(2059400110,'English')

def remove_everything():
    os.remove(path)
    audio_path = f'./myaudio/'
    for i in os.walk(audio_path):
        for j in i[2]:
            os.remove(f'{audio_path}{j}')

def get_mp3(word):
    api = f'http://dict.youdao.com/dictvoice?audio={word}'
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    res = requests.get(api,headers=header,timeout=10)
    filepath = f"./myaudio/{word}.mp3"
    try:
        with open(filepath,'wb') as file:
            file.write(res.content)
    except :
        return (f'{word}单词没找到音频')


def add_note(word,description):
    my_note = genanki.Note(
    model = my_model,
    fields = [word, trans_html(description), f'[sound:{word}.mp3]'])
    return my_note


def trans_html(text):
    new_text = re.sub('\n','<br/>',text) 
    return new_text

def make_package():
    dic = get_word()
    for word,description in dic.items():
        print(description)
        my_note = add_note(word,description)
        my_deck.add_note(my_note)
        get_mp3(word)
    my_package = genanki.Package(my_deck)
    my_package.media_files = [ f'./myaudio/{word}.mp3' for word in dic.keys()]

    today = time.strftime("%Y-%m-%d", time.localtime())
    #my_package.write_to_file(f"C:/Users/{user_name}/Desktop/{today}.apkg")
    my_package.write_to_file(f"./{today}.apkg")
    remove_everything()
def check():
    if os.path.exists(path):
        return True
    else:
        return False