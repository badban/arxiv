# !/usr/bin/env python
# -*- coding: utf-8 -*-
# badban@2016
#共41956行 th29555行 ph12401行

import re

from pymongo import MongoClient
def deleteRepetition(mergeResult):
    dictTitle={}
    dictSummary={}
    for item in mergeResult.find({}):
        if(dictTitle.get(item['title'])!=None and dictSummary.get(item['summary'])!=None):
            mergeResult.delete_one({'id':item['id']})
        if(dictTitle.get(item['title'])==None):
            dictTitle[item['title']]=item['id']
        if(dictSummary.get(item['summary'])==None):
            dictSummary[item['summary']]=item['id']
def mergeStr(strA,strB):
    list=[]
    list=strB.split(',')
    for item in list:
        if(strA.find(item)==-1):
            if(strA!=""):
                strA=strA+","+item
            else:
                strA=item
    return strA


def updateNeighbor(mergeResult):
    dictTitle={}
    counter=0
    for item in mergeResult.find({}):
        counter=counter+1
        print('第%d条'%counter)
        title=item['title']
        if(mergeResult.find({"title":title}).count()>=2):
            neighbor=""
            print('begin')
            print('title%s'%title)
            for i in mergeResult.find({"title":title}):
                if(i.get('neighbor')!=None):
                     #print(i['neighbor'])
                    neighbor=mergeStr(neighbor,i['neighbor'])
                    print(neighbor)
            print('end')
            mergeResult.update({"title":title}, {'$set':{"neighbor":neighbor}},multi=True)



def printTitle(mergeResult):
    dictTitle = {}
    for item in mergeResult.find({}):
        if(dictTitle.get(item['title'])!=None ):
            print(item['title'], "\n\nsummary1", dictTitle[item['title']], "\n\nsummary2", item['summary'])
        if (dictTitle.get(item['title']) == None):
            dictTitle[item['title']] = item['summary']


def printCount(mergeResult):
    print("总行数：%d" % mergeResult.find({}).count())
    print("ph行数：%d" % mergeResult.find({'_id': {'$regex': 'ph.*'}}).count())
    print("th行数：%d" % mergeResult.find({'_id': {'$regex': 'th.*'}}).count())

def addId(mergeResult):
    for item in mergeResult.find({}):
        _id=item['_id']
        id=_id[2:]
        mergeResult.update({"_id":_id}, {"$set": {"id": id.zfill(7)}})
def addNeighbor(mergeResult,relation):
    for item in mergeResult.find({}):
        searchResult=relation.find_one({'_id':item['id']})
        if(searchResult):
            print('addnegibor:%s'%searchResult['_id'])
            mergeResult.update({"id":item['id']}, {'$set':{"neighbor":searchResult['neighbor']}})
#通过txt文件加入关系
def addNeighborByTxt(mergeResult):
    with open('E:/code/arxivData/hepph/ph.txt')as phFile:
        counter=1
        for line in phFile.readlines():
            if(counter>4):
                list=line.split()
                result=mergeResult.find_one({'id':list[0]})
                neighbor=""
                if(result!=None):
                    if(result.get('neighbor')!=None):
                        neighbor=result['neighbor']+","+"ph"+list[1]
                    else:
                        neighbor="ph"+list[1]
                    print(list[0]+":"+neighbor)
                    mergeResult.update({"id": list[0]}, {'$set': {"neighbor": neighbor}})
            counter+=1
    with open('E:/code/arxivData/hepth/th.txt')as thFile:
        counter=1
        for line in thFile.readlines():
            if(counter>4):
                list=line.split()
                result=mergeResult.find_one({'id':list[0]})
                neighbor=""
                if(result!=None):
                    if(result.get("neighbor")!=None):
                        neighbor=result['neighbor']+","+"th"+list[1]
                    else:
                        neighbor="ph"+list[1]
                    print(list[0]+":"+neighbor)
                    mergeResult.update({"id": list[0]}, {'$set': {"neighbor": neighbor}})
            counter+=1

if __name__=="__main__":
    client = MongoClient('192.168.1.112', 27017)
    db = client.arxiv
    collection = db.hepth
    relation=db.relation
    #print(collection.find({'_id': {'$regex': 'ph.*'}}).count())
    mergeResult=db.mergeResult#合并结果
    #生成mergeResult
    #mergeResult.insert(collection.find({}))
    strth='th'
    strph='ph'
    #deleteRepetition(mergeResult)
    #添加id
    #addId(mergeResult)
    #printCount(mergeResult)
    #添加neighbor
    #addNeighbor(mergeResult,relation)
    #addNeighborByTxt(mergeResult)
    # 更新neighbor
    updateNeighbor(mergeResult)
