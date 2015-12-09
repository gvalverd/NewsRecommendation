#coding=utf-8

from GlobalConfig import *
import time
import numpy
import jieba

def divideData(allFile, trainningFile, testFile):
	separateTime = int(time.mktime(time.strptime(GlobalConfig.dataSeparateTime, '%Y-%m-%d %H:%M:%S')))
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

def getTimeSep(timeString):
	return int(time.mktime(time.strptime(timeString, '%Y-%m-%d %H:%M:%S'))) 

def getTimeString(intTime):
	format = "%Y年%m月%d日 %H:%M:%S"
	value = time.localtime(intTime)
	dt = time.strftime(format, value)
	return dt

def divideDataByDay(allFile):
	dayNews = [[] for i in range(31)]
	dayFileName = GlobalConfig.dayFileName
	startTime = getTimeSep(GlobalConfig.dataStartTime)
	oneDayTime = GlobalConfig.aDaySeparateTime
	with open(allFile, "r") as fr:
		while True:
			aLine = fr.readline()
			if aLine == "":
				break
			aRecord = aLine.split("\t")
			theDay = (int(aRecord[2])-startTime)/oneDayTime
			print getTimeString(int(aRecord[2]))
			print theDay
			dayNews[theDay].append(aLine)
	for i in range(31):
		with open(dayFileName + str(i+1), "w") as fw:
			for j in dayNews[i]:
				fw.write(j) 


def divideWords(trainningFile):
	wordsList = {}
	stopWord = getStopWord()
	newsKeyWord = {}
	userNewsMap = []
	docNum = 0
	with open(trainningFile, "r") as fr:
		while True:
			aRecord = fr.readline()
			#aRecord = fr.readline()
			#aRecord = fr.readline()
			if aRecord == "":
				break
			aRecord = aRecord.split("\t")
			
			if (aRecord[-2].strip() == "NULL" and aRecord[-1].strip() == "NULL"):
				continue
			#userNewsMap[aRecord[0]] = aRecord[1] # A user can read lots of news can't 
			userNewsMap.append((aRecord[0], aRecord[1]))
			
			#print aRecord
			if aRecord[1] in newsKeyWord.keys():
				#相同文档，只统计出现一次得情况
				'''
				for item in newsKeyWord[aRecord[1]]:
					wordsList[item][1] = wordsList[item][1] + 1.0
				'''
				continue
			docNum += 1
			tempWordList = jieba.cut(aRecord[-3].strip() + aRecord[-2].strip(), cut_all=False)
			keyWord = {}
			for word in tempWordList:
				word = word.strip().encode("utf-8")
				#print word
				if word.isdigit() or word == "" or word in stopWord:
					continue
				#print word
				tf = keyWord.get(word, 0)
				if not tf:
					keyWord[word] = [1.0, 0]
					
					if word in wordsList:
						wordsList[word][1] = wordsList[word][1] + 1.0
					else:
						wordsList[word] = [0, 1.0]
						#wordNo = wordNo + 1 # Record the key word's index
					#wordsList[word][1] = wordsList.get(word, 0)[1] + 1.0 #doc frequency
				else:
					keyWord[word] = [tf[0] + 1.0, 0]
				#keyWord[word] = keyWord.get(word, 0) + 1.0
			newsKeyWord[aRecord[1]] = keyWord

			#wordsList = wordsList | set(keyWord.keys())
			#wordsList = sorted(wordsList.iteritems(), key= lambda d:d[1], reverse=True)
			#print docNum,len(keyWord.keys()),len(wordsList)
			print "divideData %d" % docNum
			#print wordList
			#break
	tempWordsList = sorted(wordsList.iteritems(), key= lambda d:d[1][1], reverse=True)
	#print len(tempWordsList),len(newsKeyWord)
	# Attention tempWordsList is list [("****",[wordNo, docF])]
	#print tempWordsList[:10]
	for i in range(len(tempWordsList)):
		if tempWordsList[i][1][1] >= docNum * GlobalConfig.keyWordGiveupRate:
			del wordsList[tempWordsList[i][0]] # del the key word no is also changed
		else:
			break
	wordNo = 0
	for word in wordsList:
		wordsList[word][0] = wordNo
		wordNo += 1
	print "Key words num: %d" % len(wordsList)
	print "News lenth: %d " % len(userNewsMap)

	#print newsKeyWord["100649537"]
	return (docNum, wordsList, newsKeyWord, userNewsMap)
			

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
	
	#trainningList, testList = divideData(GlobalConfig.allData, GlobalConfig.trainningData, GlobalConfig.testData)
	#newDocsInLastTen(trainningList, testList)
	divideDataByDay(GlobalConfig.allData)
	#test()
	#divideWords(GlobalConfig.trainningData)
	#print tt
	#pass
	#test()
