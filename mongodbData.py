from pymongo import MongoClient

#连接mongodb并读取演员信息
"""
people:     所有filmmaker_page人员
key:        查找键值
actors:     所有演员
:return:
"""
conn = MongoClient('192.168.235.55', 27017) #连接mongodb
db = conn['admin']  #连接数据库名
db.authenticate("admin", "123456")    #密码
db = conn['team_behind_sc'] #use team_behind_sc(数据库)
people = db['Filmmaker_page']

set_actors = set()
# list_actors = []
for person in people.find():    #将所有filmmaker_page信息读取出
    # print(person)
    for key in person:      #查找所有演员
        if key == '演员':
            actors = person['演员']
            # print(actors)
            for i in actors:
                links = actors[i].replace(' ', '.')
                # print(links)
                set_actors.add(links)
list_actors = list(set_actors)
for actors_url in list_actors:
    with open('people.txt', 'a+') as file:
        file.write(str(actors_url) + '\n')
print(list_actors)
# for each in list_actors:
#     print(each)
#     with open('people.txt', 'a+') as file:
#         file.write(str(each) + '\n')
