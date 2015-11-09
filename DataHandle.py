#coding=utf-8

from GlobalConfig import *
import time
import numpy
import jieba

def divideData(allFile, trainningFile, testFile):
	separateTime = int(time.mktime(time.strptime('2014-3-21 0:0:0', '%Y-%m-%d %H:%M:%S')))
	trainningList = []
	testList = []
	with open(allFile, "r") as fr:
		arrayLines = fr.readlines()
		for aLine in arrayLines:
			aLine = aLine.split("\t")
			if int(aLine[2]) < separateTime:
				trainningList.append(aLine)
			else:
				testList.append(aLine)
	# trainning data sort by news id
	trainningList = sorted(trainningList, key=lambda x:int(x[1]))
	# test data sort by user id
	testList = sorted(testList, key=lambda x:int(x[0]))
	print len(trainningList),len(testList)
	with open(trainningFile, "w") as fw:
		for aLine in trainningList:
			fw.write("\t".join(aLine))
	with open(testFile, "w") as fw:
		for aLine in testList:
			fw.write("\t".join(aLine))
	return trainningList, testList
	
def divideWords(trainningFile):
	wordsList = []
	with open(trainningFile, "r") as fr:
		trainningList = fr.readlines()

		for aRecord in trainningList:
			aRecord = aRecord.split("\t")
			seg_list = jieba.cut(aRecord[-2], cut_all=False)
			#print len(list(seg_list))
			seg_list = set(seg_list)
			print len(seg_list)
			print "/".join(seg_list)
			#print str(seg_list)
			break


def test():
	print GlobalConfig.allData
	print time.time()
	print time.gmtime(1394463264)
	print int(time.mktime(time.strptime('2014-3-4 3:2:3', '%Y-%m-%d %H:%M:%S')))

if __name__ == "__main__":
	#help(sorted)
	#trainningList, testList = divideData(GlobalConfig.allData, GlobalConfig.trainningData, GlobalConfig.testData)
	'''
	tt = [["3",3,3],["1",1,1],["2",2,2]]
	tt = sorted(tt, key=lambda x:int(x[0]))
	'''
	divideWords(GlobalConfig.allData)
	#print tt
	#pass