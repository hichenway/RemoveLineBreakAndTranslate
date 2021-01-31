# coding: utf-8
"""
@author: hichenway
@知乎: 海晨威
@contact: lyshello123@163.com
@time: 2021/1/24
@license: 商用或作为python教程，请联系邮箱
"""

from tkinter import *
from tkinter.ttk import *
import pyperclip    #剪切板读写
import webbrowser

class RemoveLineBreakAndTranslate:
    def __init__(self,window):
        #输入部分
        LabelFrame1=LabelFrame(window,text="输入",height=50,width=100)
        LabelFrame1.grid(row=1,column=0,columnspan=3,padx=10,pady=10,sticky=W)
        LabelFrame1.propagate(0)    # 使组件大小不变，此时width才起作用

        label1=Label(LabelFrame1,text="语言选择：")
        label1.grid(row =1,column =2,columnspan=2)

        #英汉单选框
        self.languageSet=IntVar()
        self.languageSet.set(1)      #选中默认按钮
        EnglishButton=Radiobutton(LabelFrame1,text="英",variable = self.languageSet,value=1,command=self.EnglishButtonSet)
        ChineseButton= Radiobutton(LabelFrame1,text="中",variable=self.languageSet,value=2,command=self.ChineseButtonSet)
        EnglishButton.grid(row=2,column=2)
        ChineseButton.grid(row=2,column=3)

        #原输入框
        # self.input=StringVar()
        # self.inputEntry=Entry(LabelFrame1,textvariable=self.input,width=70)
        # self.inputEntry.grid(row=2,column=0,rowspan=3,sticky=W,padx=10)
        # self.inputEntry.focus()      #程序运行时，光标默认出现在这里

        #输入框
        self.input=StringVar()
        inScrollbar=Scrollbar(LabelFrame1)     #侧边滚动条
        self.inText=Text(LabelFrame1,height=10,width=65)
        inScrollbar.config(command=self.inText.yview)
        self.inText.config(yscrollcommand=inScrollbar.set)
        self.inText.grid(row=1,column=0,rowspan=4,sticky=W,padx=10,pady=10)
        inScrollbar.grid(row=1,column=1,rowspan=4)
        self.inText.focus()

        #运行按钮
        runButton=Button(LabelFrame1,text="去除回车",command=self.output)
        runButton.grid(row=3,column=2,columnspan=2)

        #清空按钮
        cleanButton=Button(LabelFrame1,text="清空",command=self.clean)
        cleanButton.grid(row=4,column=2,columnspan=2)

        #输出部分
        LabelFrame2=LabelFrame(window,text="输出",height=50,width=100)
        LabelFrame2.grid(row=3,column=0,columnspan=3,padx=10,pady=10,sticky=W)
        LabelFrame2.propagate(0)    # 使组件大小不变，此时width才起作用

        #输出框
        outScrollbar=Scrollbar(LabelFrame2)     #侧边滚动条
        self.outText=Text(LabelFrame2,height=10,width=65)
        outScrollbar.config(command=self.outText.yview)
        self.outText.config(yscrollcommand=outScrollbar.set)
        self.outText.grid(row=1,column=0,rowspan=3,padx=10,pady=10)
        outScrollbar.grid(row=1,column=1,rowspan=3)

        #三个按钮
        copyButton=Button(LabelFrame2,text="复制",command=self.copy)  #command=
        copyButton.grid(row=1,column=2)

        translateButton=Button(LabelFrame2,text="翻译跳转",command=self.translate)
        translateButton.grid(row=2,column=2)

        quitButton=Button(LabelFrame2,text="退出",command=window.destroy)
        quitButton.grid(row=3,column=2)

        #说明框
        LabelFrame3=LabelFrame(window,text="简介",height=50,width=100)
        LabelFrame3.grid(row=5,column=0,columnspan=3,padx=10,pady=10,sticky=W)
        LabelFrame3.propagate(0)    # 使组件大小不变，此时width才起作用

        #解释说明
        explain="""
        功能：去除文字中的回车符并支持跳转默认浏览器执行谷歌英汉互译
        说明：
            1、选择输入文字的语言类别            2、去除文字段落中的回车符
            3、清空输入框以便再次输入            4、复制输出框文字到剪切板
            5、跳转默认浏览器英汉互译            6、退出并结束当前运行环境           
            
            """

        explainLabel=Label(LabelFrame3,text=explain)
        explainLabel.grid(row =1,column =0,sticky=W)

    def EnglishButtonSet(self):     #英语单选框
        self.languageSet=1

    def ChineseButtonSet(self):     #中文单选框
        self.languageSet=2

    def clean(self):        #清空函数
        self.inText.delete('1.0','end')         #清空输入内容，方便再次输入

    def output(self):       #回车去除按钮调用按钮
        self.input=self.inText.get(1.0,END)
        # self.input=self.inputEntry.get()
        self.removeEnter()
        self.outText.delete('1.0','end')        #重新运行前要删除原来内容
        self.outText.insert('end',self.input)


    def removeEnter(self):  #回车去除函数
        if self.languageSet==2:
            self.input=self.input.replace('\n','')
        else:
            self.input=self.input.replace('\n',' ')

    def translate(self):    #翻译按钮
        if self.languageSet==1:
            url='https://translate.google.cn/#en/zh-CN/'+ self.input    #这是英文-中文
        else:
            url='https://translate.google.cn/#zh-CN/en/'+ self.input    #这是中文-英文
        webbrowser.open(url,1,False)

    def copy(self):         #复制按钮
        pyperclip.copy(self.input)


if __name__=='__main__':
    window = Tk()
    window.geometry("620x560") #设置窗口大小
    window.title("回车去除和跳转翻译")
    myGui=RemoveLineBreakAndTranslate(window)
    window.mainloop()
