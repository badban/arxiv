# !/usr/bin/env python
# -*- coding: utf-8 -*-
# badban@2016

def zeroFillArxiv():
    with open('E:/code/arxivData/hepph/ph.txt','w')as phFile:
        with open('E:/code/arxivData/hepph/Cit-HepPh.txt') as hepphFile:
            counter=1
            for line in hepphFile.readlines():
                line=line[:-1]
                if(counter>4):
                    list=line.split()
                    strtemp=list[0].zfill(7)+" "+list[1].zfill(7)
                    line=strtemp
                phFile.write(line+'\n')
                counter+=1
    with open('E:/code/arxivData/hepth/th.txt','w')as thFile:
        with open('E:/code/arxivData/hepth/Cit-HepTh.txt') as hepthFile:
            counter=1
            for line in hepthFile.readlines():
                line=line[:-1]
                if(counter>4):
                    list=line.split()
                    strtemp=list[0].zfill(7)+" "+list[1].zfill(7)
                    line=strtemp
                thFile.write(line+'\n')
                counter+=1

if __name__=="__main__":
    zeroFillArxiv()