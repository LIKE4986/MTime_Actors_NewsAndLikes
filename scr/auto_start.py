#coding:utf-8
import os

error_flags = False

if __name__ == '__main__':
    trytime = 0
    while(error_flags == False):
        trytime = trytime+1
        print("第",str(trytime),"次尝试")
        os.system('python3.4 ./LikesAndNewsCollection.py')
    print("第", str(trytime), "次尝试", "任务结束")