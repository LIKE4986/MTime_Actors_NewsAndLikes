# coding:utf-8

import json
import re
import time

import pandas as pd
import requests
from selenium import webdriver

from scr import auto_start

broswer = webdriver.PhantomJS(executable_path= '/home/hadoop/文档/MTime_Actors_NewsAndLikes-master/phantomjs')

def __get_actors_url():
    """
    读取已从数据库写入txt文件内的演员链接
    存入list_actors列表并返回该列表
    :return:
    """
    with open('./document/actorsurls.txt', 'r') as file_people:
        actors_url = file_people.readlines()
        list_actors = []
        for each in actors_url:
            list_actors.append(each.strip('\n'))
        # print(list_actors)
        # print(len(list_actors))
    file_people.close()
    return list_actors

def __likes_collections(actors_url):
    """
    根据每个演员的链接分别获取他们的喜爱度元素并存入json文件中
    url_star:       演员个人主页网址
    content:        演员个人主页网址所有内容
    name:           演员名
    participants:   参与投票人数
    likes:          该演员平均喜爱度
    actors_likes    该演员喜爱度表格（表头为：姓名、参与人数、喜爱度）
    :return:        url_star
    """
    broswer2 = webdriver.PhantomJS(executable_path='/home/hadoop/文档/MTime_Actors_NewsAndLikes-master/phantomjs')
    url_star = actors_url
    participants = 'None'
    name = 'None'
    likes = 'None'
    while(participants == 'None'):
        broswer2.get(url_star)
        print(url_star)
        content = broswer2.execute_script("return document.documentElement.outerHTML")
        name = re.findall('<h2 style=.*>(.*?)</h2>', content)[0]
        print(name)
        try:
            participants = re.findall('<p id="ratingCount" style="">(.*?)</p>', content)[0]
            print(participants)
        except:
            participants = 'None'
        try:
            likes = re.findall('<p id="finalRating" style="">(.*?)</p>', content)[0]
        except:
            likes = 'None'
        time.sleep(2)
        print('sleeping... ...')
        del broswer2
    print(name,"//", likes, "//", participants)
    dic = {}
    dic['name'] = name
    dic['participants'] = participants
    dic['likes'] = likes
    likes_rows.append(dic)
    actors_likes = pd.DataFrame(likes_rows)
    print(actors_likes)
    try:
        with open("./document/likes_info/%s.json" % name, "w") as file:
            json.dump(dic, file, ensure_ascii=False)
    except Exception as error:
        print(Exception, ":", error)

def __news_collections(url_star, name):
    """
    获取演员新闻各元素并存入csv文件中
    :param url_star:    从数据库导入的演员url
    :param name:        演员姓名
    news_url:           演员新闻url
    content_news:       演员新闻html内容
    news_rows:          一则新闻所有元素为一个列表组成的所有新闻列表
    no_exist:           不存在情况
    news_all:           所有新闻的HTML框架的列表
    pages:              新闻所有页数
    dic:                一则新闻的四个元素的字典
    title:              新闻标题
    time:               新闻时间
    digest:             新闻摘要
    url:                新闻原文链接
    actors_news:        按pd格式输出的所有新闻表格
    :return:
    """
    news_url= url_star.strip('\n') + 'news.html'  # 新闻网址
    print(news_url)
    content_news = requests.get(news_url)
    content_news = content_news.text

    news_rows = []
    #this actor do not have any news
    no_exist = re.findall('<title>(.*?)</title>', content_news)
    print(no_exist)
    if str(no_exist) == "['很抱歉，你要访问的页面不存在']":
        dic = {}
        dic['title'] = 'None'
        dic['time'] = 'None'
        dic['digest'] = 'None'
        dic['url'] = 'None'
        news_rows.append(dic)
        actors_news = pd.DataFrame(news_rows)
        actors_news.to_csv('./document/news_info/%s.csv'% name, index=False, sep='^')
    else:
        # 第一页新闻
        news = re.findall('<dd>.*?<div class=(.*?)</div>                    </dd>', content_news)
        print("news", news)
        news_all = []
        news_all.append(news)
        pages = re.findall('<a class="num" href="news-.*.html">(.*?)</a>', content_news)
        print(pages)
        if not pages:
            print('仅有一页新闻')
            pass
        else:
            all_pages = pages[-1]
            print(all_pages)
            for i in range(int(all_pages) - 1):
                url_star_news = url_star.strip('\n') + 'news-' + str(i + 2) + '.html'
                content_news_more = requests.get(url_star_news)
                content_news_more = content_news_more.text.replace("\n", '')
                # 获取新闻框架
                news_all.append(re.findall('<dd>.*?<div class=(.*?)</div>                    </dd>', content_news_more))

        for per_page in news_all:
            for per in per_page:
                dic = {}
                print(per)
                news_title = re.findall('<h3><a.*_blank">(.*?)</a></h3> ', per)[0]
                news_time = re.findall('<span class="ml12">(.*?)</span>', per)[0]
                news_digest = re.findall('<p class="db_newsinfo">(.*?)<a href', per)[0]
                news_url = re.findall('<h3><a href="(.*?)" target="_blank">.*</a></h3>', per)[0]
                dic['title'] = news_title
                dic['time'] = news_time
                dic['digest'] = news_digest
                dic['url'] = news_url
                news_rows.append(dic)
        actors_news = pd.DataFrame(news_rows)
        print(actors_news)
        try:
            actors_news.to_csv('./document/news_info/%s.csv'% name, index=False, sep='^')
        except Exception as error:
            print(Exception, ":", error)

def __get_likes():
    """
    调用获取演员链接、喜爱度和新闻的函数进行内容爬取，记录已爬取信息
    done_url:       已经爬完的演员链接的列表
    likes_done_:    记录done_url的txt文件
    urls:           演员链接
    likes_error_:   记录报错url的txt文件
    :return:
    """
    done_url = []
    with open("./document/likes_done_.txt", "r") as file_done:
        for line in file_done:
            done_url.append(line.strip('\n'))
    print(done_url)
    urls = __get_actors_url()
    for each_url in urls:
        if each_url in done_url:
            print(each_url, " already done!")
            pass
        else:
            try:
                __likes_collections(actors_url=each_url)
                print("============successfully get likes info=================")
                with open("./document/likes_done_.txt", "a+") as file_done:
                    file_done.write(each_url + '\n')
            except Exception as error:
                print(Exception, ":", error)
                with open("./document/likes_error_.txt", "a+") as journalfile:
                    journalfile.write(each_url + Exception + ":" + error + '\n')


def __get_news():
    """
        调用获取演员链接、喜爱度和新闻的函数进行内容爬取，记录已爬取信息
        done_url:       已经爬完的演员链接的列表
        news_done_:     记录done_url的txt文件
        urls:           演员链接
        name_content:   该演员就link的html内容
        actor_name:     演员姓名
        news_error_:    记录报错url的txt文件
        :return:
        """
    done_url = []
    with open("./document/news_done_.txt", "r") as file_done:
        for line in file_done:
            done_url.append(line.strip('\n'))
    print(done_url)
    urls = __get_actors_url()
    for each_url in urls:
        if each_url in done_url:
            print(each_url," already done!")
            pass
        else:
            try:
                name_content = requests.get(each_url)
                name_content = name_content.text
                actor_name = re.findall("<h2 style=.*>(.*?)</h2>", name_content)[0]
                print(actor_name)
                try:
                    __news_collections(url_star=each_url, name=actor_name)
                    print("============successfully get news info=================")
                    with open("./document/news_done_.txt", "a+") as file_done:
                        file_done.write(each_url + '\n')
                except Exception as error:
                    print(Exception, ":", error)
            except:
                with open("./document/news_error_.txt", "a+") as error_file:
                    error_file.write(each_url + '\n')
                print("actor do not exist")

def __get_all():
    try:
        __get_likes()
        __get_news()
    except Exception as error:
        print(Exception, ":", error)

def __star():
    """
    判断是否可以正常爬取，不可以，则重启，并输出错误类型
    :return:
    """
    try:
        __get_all()
        auto_start.error_flags = True
    except Exception as a:
        print(Exception,":", a)
        try:
            while True:
                broswer.close()
        except Exception as e:
            print(Exception, ":", e)
    finally:
        broswer.quit()

if __name__ == '__main__':
    likes_rows = []
    __star()