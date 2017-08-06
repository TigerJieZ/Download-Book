# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import urllib2
import sys

class Parser(object):
    '''http://baike.baidu.com/view/2975166.htm'''

    def find_section_urls(self,index_url):
        new_urls=set()
        page = urllib2.urlopen(index_url).read()
        page = page.decode("gbk")

        s_key = 'h1>(.+?)<'
        re_c = re.compile(s_key)
        ls = re.findall(re_c, page)
        if len(ls) > 0:
            title = ls[0]

        s_key = 'href="(.{37}?)"'
        re_c = re.compile(s_key)
        ls = re.findall(re_c, page)
        for l in ls:
            try:
                url = index_url + l
                new_urls.add(url)
            except:
                print("error!")
        return new_urls,title

    def myGetNumble(self,ch):
        if ch == "一":
            return 1
        elif ch == "零":
            return 11
        elif ch=="二" or ch=="两":
            return 2
        elif ch=="三":
            return 3
        elif ch=="四":
            return 4
        elif ch=="五":
            return 5
        elif ch=="六":
            return 6
        elif ch=="七":
            return 7
        elif ch=="八":
            return 8
        elif ch=="九":
            return 9
        elif ch=="十":
            return 10
        elif ch=="百":
            return 100
        elif ch=="千":
            return 1000
        elif "0" < ch <= "9":
            return int(ch)
        elif ch=="0":
            return 11
        else:
            return False

    def get_titleIndex(self,title):
        index = title.index("章") - 1
        if not index:
            index=title.index(".")-1
            print(index)
            exit(0)

        titleIndex=0
        i=0
        lastTemp=-1333
        while True:
            temp=self.myGetNumble(title[index])
            if lastTemp==11 and temp==1000:
                i+=1
            if lastTemp==10 and temp==100:
                titleIndex=titleIndex+10
                continue
            if temp==False:
                break
            index -= 1
            if temp==11:
                temp=0
            if temp==10:
                if i==0:
                    i+=1
                    continue
                elif not self.myGetNumble(title[index]):
                    titleIndex+=10
                    return str(titleIndex)
                else:
                    continue
            if temp==100:
                if i==0:
                    i+=2
                    continue
                else:
                    continue
            if temp==1000:
                if i==0:
                    i+=3
                    continue
                else:
                    continue
            if temp==11:
                i+=1
                continue
            titleIndex=titleIndex+temp*pow(10,i)
            i +=1
            lastTemp=temp
        return titleIndex

    def _get_new_data_section(self,soup):
        res_data = {}
        text = soup.find('div', id="text_area")
        res_data['text'] = text.get_text().decode("utf-8")
        res_data['text']=res_data['text'].replace("    ","\r\n    ").decode("utf-8")

        title = soup.find('div',id="chapter_title")
        title = title.get_text().decode("utf-8")
        title_key = r'第.*章'.decode("utf-8")
        title_c = re.compile(title_key)
        try:
            title = re.findall(title_c,title)[0].decode("utf-8")
            res_data['section_title'] = self.get_titleIndex(title)
        except IndexError:
            print("章节名解析失败".decode('utf-8'))
            print(title)
            res_data['section_title']=-1

        return res_data

    def find_books_urls(self,list_url):
        books_urls=set()

        print(list_url)
        page=urllib2.urlopen(list_url).read()
        page = page.decode("gbk")

        #http://www.23zw.me/olread/39/39224/index.html
        reKey='http://www.23zw.me/olread/\d*/\d*/'

        re_c = re.compile(reKey)
        ls = re.findall(re_c, page)
        for l in ls:
            try:
                books_urls.add(l)
            except:
                print("error!")

        return books_urls

    def find_list_urls(self):
        list_urls=[]
        i=1
        while i<=2519:
            url="http://www.23zw.me/class_0_"+str(i)+".html"
            list_urls.append(url)
            i+=1
        return list_urls

    def parser_Section(self,html_cont):
        if html_cont != None:
            soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='gbk')
            new_data = self._get_new_data_section(soup)

            return new_data
        else:
            return None