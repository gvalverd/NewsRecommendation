#coding=utf-8

from GlobalConfig import *
import time
import numpy
import jieba

def divideData(allFile, trainningFile, testFile):
	separateTime = int(time.mktime(time.strptime(GlobalConfig.dataStartTime, '%Y-%m-%d %H:%M:%S')))
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
	wordsList = {}
	stopWord = getStopWord()
	newsWordVector = {}
	newsKeyWord = {}
	with open(trainningFile, "r") as fr:
		i = 0
		while True:
			i += 1
			aRecord = fr.readline()
			aRecord = fr.readline()
			aRecord = fr.readline()
			if aRecord == "":
				break
			aRecord = aRecord.split("\t")

			if (aRecord[-2].strip() == "NULL" and aRecord[-1].strip() == "NULL"):
				continue
			
			#print aRecord
			if aRecord[1] in newsKeyWord.keys():
				for item in newsKeyWord[aRecord[1]]:
					wordsList[item] = wordsList.get(item, 0) + 1.0
				continue
			tempWordList = jieba.cut(aRecord[-3].strip() + aRecord[-2].strip(), cut_all=False)
			keyWord = {}
			for word in tempWordList:
				word = word.strip().encode("utf-8")
				print word
				if word.isdigit() or word == "" or word in stopWord:
					continue
				print word
				tf = keyWord.get(word, 0)
				if not tf:
					keyWord[word] = 1.0
					wordsList[word] = wordsList.get(word, 0) + 1.0 #doc frequency
				else:
					keyWord[word] = tf + 1.0
				#keyWord[word] = keyWord.get(word, 0) + 1.0
			newsKeyWord[aRecord[1]] = keyWord

			#wordsList = wordsList | set(keyWord.keys())
			#wordsList = sorted(wordsList.iteritems(), key= lambda d:d[1], reverse=True)
			print i,len(keyWord.keys()),len(wordsList)
			#print wordList
			break
	wordsList = sorted(wordsList.iteritems(), key= lambda d:d[1], reverse=True)
	print len(wordsList),len(newsKeyWord)
	print wordsList[:10]
	for i in range(len(wordsList)):
		if wordsList[i][1] == 1:
			print i
			break
	print wordsList[20000]
			

def getStopWord():
	stopWord = []
	with open(GlobalConfig.stopWord) as fw:
		stopWord = fw.readlines()
		#stopWord = set(stopWord)
		#print len(stopWord)
		stopWord = [element[:-1] for element in stopWord]  #"-1" means removing the '\n'
	#print len(set(stopWord))
	return set(stopWord)

def newDocsInLastTen(trainningList, testList):
	trainningDocs = set([i[1] for i in trainningList])
	print "All users:%d" % len(set([i[0] for i in trainningList]))
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


if __name__ == "__main__":
	#help(sorted)
	'''
	trainningList, testList = divideData(GlobalConfig.allData, GlobalConfig.trainningData, GlobalConfig.testData)
	newDocsInLastTen(trainningList, testList)
	'''
	#test()
	divideWords(GlobalConfig.trainningData)
	#print tt
	#pass
	#test()
