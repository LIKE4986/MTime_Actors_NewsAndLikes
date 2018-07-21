# Mtime_Actors_LikesAndNews
Using actors_links downloaded from mongodb to capture each actor's likes and news.

## Main codes
* mongdbData.py
<br>download all the actors_links we need from mongodb</br>
* start.sh
<br>a script to start the program</br>
* auto_start.py
<br>determine whether there is an error and whether to restart it</br>
* LikesAndNewsCollection.py
<br>main code to crawl likes and news infomation</br>
```python
__get_actors_url()          #获取演员url
__likes_collections()       #获取演员喜爱度各项元素（姓名、喜爱度、参与人数）
__news_collections()        #获取演员新闻各项元素（标题、时间、摘要、原文链接）
__get_all()                 #获取所有演员的喜爱度与新闻（相当于一个main函数）
__star()                    #保证正常爬取的重要函数
```

## Operating environment
Based on python3.5 and selenium, first need to install:
* requests
* re
* time
* json
* pandas

## Operation struction
|star.sh|auto_star.py|get_actor_works.py|
|:---|:---|:---|
|<br>**first step**</br>used to execute this project by calling *auto_start.py*|<br>**second step**</br><br>used to calling *LikesAndNewsCollection.py*</br>also used to restart the project|<br>**thrid step**</br><br>main step</br>used to crawl all the information|

<br>**terminal instruction**</br>
```
username:~/Mtime_Actors_LikesAndNews$ sh start.sh
```
## Bullet points
Key skills applied to this project
* mongodb
<br> to download data from database</br>
* PhantomJs
* json
* pandas & csv
```python
import pandas as pd
pd_table = pd.DataFrame(dic_item)
pd_table.to_csv("filename.csv", index=False, sep='`')
```
* shell

## Sample
Take [Benshan Zhao(赵本山)](http://people.mtime.com/965769/) as an example
### Get likes
1.Get link from mongodb, using selenium to get content in this link. Required to sleep for a second,  waiting for response.</br>
<img src="https://github.com/LIKE4986/MTime_Actors_NewsAndLikes/blob/master/Mtime_Actors_Pics/likemtime.png" width="995" height="390" alt="图片加载失败时，显示这段字"/></br>
2.Save as a json_file.</br>
<img src="https://github.com/LIKE4986/MTime_Actors_NewsAndLikes/blob/master/Mtime_Actors_Pics/likesjson.png" width="572" height="78" alt="图片加载失败时，显示这段字"/></br>

|name|participants|likes|
|:---|:---|:---|
|actor's name|the number of people voted|average ratio of preference|

</br>3.Terminal
<img src="https://github.com/LIKE4986/MTime_Actors_NewsAndLikes/blob/master/Mtime_Actors_Pics/likesterminal.png" width="655" height="182" alt="图片加载失败时，显示这段字"/></br>


## Get news
1.Get link from mongodb, attach "news.html" to get content of all news.</br>
<img src="https://github.com/LIKE4986/MTime_Actors_NewsAndLikes/blob/master/Mtime_Actors_Pics/newsmtime.png" width="1029" height="722" alt="图片加载失败时，显示这段字"/></br>
2. Save as a csv_file.</br>
<img src="https://github.com/LIKE4986/MTime_Actors_NewsAndLikes/blob/master/Mtime_Actors_Pics/newscsv.png" width="1218" height="194" alt="图片加载失败时，显示这段字"/></br>
***splite by "^"***

|digest|time|title|url|
|:---|:---|:---|:---|
|digest of this news|publish time of this news|title of this news|links to this news|

</br>3.Terminal</br>
<img src="https://github.com/LIKE4986/MTime_Actors_NewsAndLikes/blob/master/Mtime_Actors_Pics/newsterminal.png" width="742" height="367" alt="图片加载失败时，显示这段字"/></br>


