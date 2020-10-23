import ctypes
from tkinter import *
from tkinter.ttk import *
from bing import *
import store
window = Tk()
window.title('Dictionary')
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)

if ScaleFactor==100:
	window.geometry('430x480+600+200')
	window.tk.call('tk', 'scaling')
elif ScaleFactor==125:
	window.geometry('550x550+600+200')
	window.tk.call('tk', 'scaling', ScaleFactor/75)

word = StringVar()
en = Entry(window,show=None,width=16,font=('微软雅黑',20),textvariable = word,)
en.grid(row=1,column=1,rowspan=2,columnspan=22,padx=30,pady=30)

descriptions = StringVar()
t = Text(window , font=('微软雅黑',12),width=40,height=10,)
t.grid(row=9,column=0,rowspan=7,columnspan=26,padx=30,pady=30)


def get_des():
	global getword
	global des
	getword = str.strip(word.get())#从entry中获取输入的单词
	en.delete(0, END)
	try:
		des = bing(getword)
	except AttributeError:
		des= '找不到此单词释义，请重试'
	except	UnicodeEncodeError :
		des = '请输入正确的英文或者中文（UnicodeEncodeError）'
	except NameError:
		des = '请输入正确的英文或者中文（NameError）'
	else:
		pass
	t.delete(0.0, END)
	t.insert(END,getword+'\n'*2)
	t.insert(END,des)

def store_word():
	try:
		store.store_word(getword,des)
	except NameError:
		pass
		t.insert(END,'请输入正确的英文或者中文（NameError）')
	else:
		t.insert(END,'\n\n-----已添加到生词本-----')
		check_button()
def check_button():
	if store.check():
		button3['state'] = NORMAL
	else:
		button3['state'] = DISABLED
def make_package():
	store.make_package()
	t.insert(END,'\n\n-----Anki包制作完成-----')
	check_button()

button1 = Button(window,width=10,text ='Descriptions',command = get_des, )
button1.grid(row=3,column=10,ipadx=10,ipady=10,rowspan=1,columnspan=1,padx=0,pady=10)


button2 = Button(window,width=10,text ='AddToBook',command = store_word )
button2.grid(row=3,column=11,ipadx=10,ipady=10,rowspan=1,columnspan=1,padx=0,pady=10,)

button3 = Button(window,width=10,text ='MakePac',command = make_package)
button3.grid(row=4,column=10,ipadx=10,ipady=10,rowspan=1,columnspan=3,padx=0,pady=0,)
check_button()
def press_enter(self):
	get_des()
en.bind("<Return>", press_enter)
window.mainloop()