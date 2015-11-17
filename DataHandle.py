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
		print "All docs:%d" % len(arrayLines)
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
	print "All trainning docs:%d\nAll test docs:%d" % (len(trainningList),len(testList))
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
			print "/".join(seg_list).encode("utf-8")
			#print str(seg_list)
			break

def newDocsInLastTen(trainningList, testList):
	trainningDocs = set([i[1] for i in trainningList])
	#print [(for j in set([ i[1] for i in testList]))]
	print "All different trainning docs:%d" % len(trainningDocs)
	docsNotIn = []
	for i in testList:
		if not i[1] in trainningDocs:
			docsNotIn.append(i[1])
	print "All new test docs:%d" % len(docsNotIn)
	print "All different new test docs:%d" % len(set(docsNotIn))
	'''
	All docs:116225
	All trainning docs:94547
	All test docs:21678
	All different trainning docs:4802
	All new test docs:15773
	All different test docs:1381
	'''

def test():
	'''
	print GlobalConfig.allData
	print time.time()
	print time.gmtime(1394463264)
	print int(time.mktime(time.strptime('2014-3-4 3:2:3', '%Y-%m-%d %H:%M:%S')))
	'''
	a = [ [1, 2, 3], [1, 5, 6], [7, 8, 9]]
	c = [1, 3, 4]
	b = []
	b.append(1)
	print "All different docs:%d" % len(b)
	

if __name__ == "__main__":
	#help(sorted)
	trainningList, testList = divideData(GlobalConfig.allData, GlobalConfig.trainningData, GlobalConfig.testData)
	newDocsInLastTen(trainningList, testList)
	'''
	tt = [["3",3,3],["1",1,1],["2",2,2]]
	tt = sorted(tt, key=lambda x:int(x[0]))
	'''
	#divideWords(GlobalConfig.allData)
	#print tt
	#pass
	#test()