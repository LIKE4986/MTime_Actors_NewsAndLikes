# list_error = []
# with open("./document/error_urls.txt", "r") as file:
#     for line in file:
#         list_error.append(line.strip('\n'))
# print(list_error)
# print(len(list_error))
# set_error = set(list_error)
# print(set_error)
# print(len(set_error))
#
# with open("./document/likes_error_.txt", "w") as file:
#     for each in set_error:
#         file.write(each + '\n')

allurls = []
with open("./document/actorsurls.txt", "r") as allfile:
    for line in allfile:
        allurls.append(line.strip('\n'))
# print(len(allurls), allurls)
doneurls = []
with open("./document/likes_done_.txt", "r") as donefile:
    for line in donefile:
        doneurls.append(line.strip('\n'))
# print(len(doneurls), doneurls)
errorurls = []
with open("./document/likes_error_.txt", "r") as errorfile:
    for line in errorfile:
        errorurls.append(line.strip('\n'))
# print(len(errorurls), errorurls)
repeatedurls = []
for url in doneurls:
    if url in errorurls:
        print("repeated url: ", url)
        repeatedurls.append(url)
# print(len(repeatedurls), repeatedurls)
notcrawlurls = []
for url in allurls:
    if url not in (doneurls or errorurls):
        # print("not crawl url: ", url)
        notcrawlurls.append(url)
print(len(notcrawlurls), notcrawlurls)
with open("./document/likes_notcrawl.txt","a+") as file:
    for url in notcrawlurls:
        file.write(url + '\n')