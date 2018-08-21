#coding: utf-8
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *

import pyperclip    #剪切板读写
import webbrowser

import http.client
import hashlib
import json
import urllib
import random

class RemoveLineBreakAndTranslate:
    def __init__(self,window):
        #输入部分
        LabelFrame1=LabelFrame(window,text="去回车前输入",height=50,width=100)
        LabelFrame1.grid(row=1,column=0,columnspan=3,padx=10,pady=10,sticky=W)
        LabelFrame1.propagate(0)    # 使组件大小不变，此时width才起作用

        label1=Label(LabelFrame1,text="语言选择：")
        label1.grid(row =1,column =2,columnspan=2)

        #英汉单选框
        self.languageSet=IntVar()
        self.languageSet.set(1)     #选中默认按钮
        EnglishButton=Radiobutton(LabelFrame1,text="英",variable = self.languageSet,value=1,command=self.EnglishButtonSet)
        ChineseButton= Radiobutton(LabelFrame1,text="中",variable=self.languageSet,value=2,command=self.ChineseButtonSet)
        EnglishButton.grid(row=2,column=2)
        ChineseButton.grid(row=2,column=3)

        self.languageSet=1          #设定初值，和选中默认按钮不一样，放的位置也不能改变

        #输入框
        self.input=StringVar()
        inScrollbar=Scrollbar(LabelFrame1)     #侧边滚动条
        self.inText=Text(LabelFrame1,height=8,width=65)
        inScrollbar.config(command=self.inText.yview)
        self.inText.config(yscrollcommand=inScrollbar.set)
        self.inText.grid(row=1,column=0,rowspan=4,sticky=W,padx=10,pady=5)
        inScrollbar.grid(row=1,column=1,rowspan=4)
        self.inText.focus()

        #运行按钮
        runButton=Button(LabelFrame1,text="去除回车",command=self.removeEnterOut)
        runButton.grid(row=3,column=2,columnspan=2)

        #清空按钮
        cleanButton1=Button(LabelFrame1,text="清空",command=self.clean1)
        cleanButton1.grid(row=4,column=2,columnspan=2)

        '''********************************************************************'''

        #中间输出部分
        LabelFrame2=LabelFrame(window,text="去回车后输出  翻译前输入",height=50,width=100)
        LabelFrame2.grid(row=3,column=0,columnspan=3,padx=10,pady=5,sticky=W)
        LabelFrame2.propagate(0)    # 使组件大小不变，此时width才起作用

        #输入和输出框
        self.output=StringVar()
        outScrollbar=Scrollbar(LabelFrame2)     #侧边滚动条
        self.outText=Text(LabelFrame2,height=8,width=65)
        outScrollbar.config(command=self.outText.yview)
        self.outText.config(yscrollcommand=outScrollbar.set)
        self.outText.grid(row=1,column=0,rowspan=3,padx=10,pady=10)
        outScrollbar.grid(row=1,column=1,rowspan=3)

        #三个按钮
        copyButton2=Button(LabelFrame2,text="复制",command=self.copy2)
        copyButton2.grid(row=1,column=2)

        translateButton=Button(LabelFrame2,text="百度翻译",command=self.translate)
        translateButton.grid(row=2,column=2)

        cleanButton2=Button(LabelFrame2,text="清空",command=self.clean2)
        cleanButton2.grid(row=3,column=2)

        '''********************************************************************'''

        #翻译输出
        LabelFrame3=LabelFrame(window,text="翻译后输出",height=50,width=100)
        LabelFrame3.grid(row=5,column=0,columnspan=3,padx=10,pady=5,sticky=W)
        LabelFrame3.propagate(0)    # 使组件大小不变，此时width才起作用

        #输出框
        self.transOutput=StringVar()
        transScrollbar=Scrollbar(LabelFrame3)     #侧边滚动条
        self.transText=Text(LabelFrame3,height=8,width=65)
        transScrollbar.config(command=self.transText.yview)
        self.transText.config(yscrollcommand=transScrollbar.set)
        self.transText.grid(row=1,column=0,rowspan=3,padx=10,pady=10)
        transScrollbar.grid(row=1,column=1,rowspan=3)

        #三个按钮
        copyButton3=Button(LabelFrame3,text="复制",command=self.copy3)
        copyButton3.grid(row=1,column=2)

        translateButton=Button(LabelFrame3,text="谷歌翻译\n网页跳转",command=self.translateGoogle)
        translateButton.grid(row=2,column=2)

        quitButton=Button(LabelFrame3,text="退出",command=self.quitWindow)
        quitButton.grid(row=3,column=2)

        '''********************************************************************'''

        #说明框
        LabelFrame4=LabelFrame(window,text="功能说明",height=50,width=100)
        LabelFrame4.grid(row=6,column=0,columnspan=3,padx=10,pady=5,sticky=W)
        LabelFrame4.propagate(0)    # 使组件大小不变，此时width才起作用

        #功能说明
        explain="""      功能：回车去除和英汉互译           注意：操作前请进行语言选择，默认英文，翻译请在联网环境下
      说明：
           1、语言选择：选择输入文字的语言类别                     4、清空：清空输入框以便再次输入
           2、去除回车：去除文字段落中的回车符                     5、复制：复制输出框文字到剪切板
           3、百度翻译：百度翻译支持的英汉互译                     6、退出：退出并结束当前运行环境
           7、谷歌翻译网页跳转：谷歌翻译官方api需收费，因此仅支持默认浏览器谷歌翻译网页跳转"""

        explainLabel=Label(LabelFrame4,text=explain)
        explainLabel.grid(row =0,column =0,sticky=W)

    def EnglishButtonSet(self):     #英语单选框
        self.languageSet=1

    def ChineseButtonSet(self):     #中文单选框
        self.languageSet=2

    def clean1(self):        #清空函数
        self.inText.delete('1.0','end')         #清空输入内容，方便再次输入
        self.inText.focus()                     #清空后光标回到当前框内

    def clean2(self):        #清空函数
        self.outText.delete('1.0','end')         #清空输入内容，方便再次输入
        self.outText.focus()                     #清空后光标回到当前框内

    def removeEnterOut(self):       #回车去除按钮调用按钮
        self.input=self.inText.get(1.0,END)
        self.removeEnter()
        self.outText.delete('1.0','end')        #重新运行前要删除原来内容
        self.outText.insert('end',self.output)


    def removeEnter(self):      #回车去除函数
        if self.languageSet==2:
            self.output=self.input.replace('\n','')
        else:
            self.output=self.input.replace('\n',' ')

    def copy2(self):                #复制按钮
        pyperclip.copy(self.output)

    def copy3(self):                #复制按钮
        pyperclip.copy(self.transOutput)

    def quitWindow(self):           #退出按钮
        flag=askyesno(title='Yes or No',message='Are you sure to quit?')
        if flag:
            window.destroy()
        else:
            pass

    def translateGoogle(self):     #谷歌翻译网页跳转按钮
        if self.languageSet==1:
            url='https://translate.google.cn/#en/zh-CN/'+ self.outText.get(1.0,END)    #这是英文-中文
        else:
            url='https://translate.google.cn/#zh-CN/en/'+ self.outText.get(1.0,END)    #这是中文-英文
        webbrowser.open(url,1,False)

    def translate(self):            #百度翻译
        appid = '20151113000005349'
        secretKey = 'osubCEzlGjzvw8qdQc41'
        myurl = '/api/trans/vip/translate'
        content =self.outText.get(1.0,END)
        if self.languageSet==1:
            fromLang = 'en' # 源语言
            toLang = 'zh'   # 翻译后的语言
        else:
            fromLang = 'zh' # 源语言
            toLang = 'en'   # 翻译后的语言

        salt = random.randint(32768, 65536)
        sign = appid + content + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
            content) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
            salt) + '&sign=' + sign

        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        response = httpClient.getresponse()             # response是HTTPResponse对象
        jsonResponse = response.read().decode("utf-8")  # 获得返回的结果，结果为json格式
        js = json.loads(jsonResponse)                   # 将json格式的结果转换字典结构
        self.transOutput = str(js["trans_result"][0]["dst"])         # 取得翻译后的文本结果
        self.transText.delete('1.0','end')              #重新运行前要删除原来内容
        self.transText.insert('end',self.transOutput)

if __name__=='__main__':
    window = Tk()
    window.geometry("620x630") #设置窗口大小
    window.title("回车去除和英汉互译")
    myGui=RemoveLineBreakAndTranslate(window)
    window.mainloop()
