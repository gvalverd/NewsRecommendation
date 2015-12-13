#coding=utf-8
import numpy, math, pickle, jieba
from GlobalConfig import *
import DataHandle

docNum = 0
keyWords = {}
newsKeyWords = {}
userKeyWords = {}
userNewsMap = []
oldUserNewsMap = []
haveSetNews = {}
# haveSetNews = {"news1":1, "news2":2}
haveSetUser = {}
userList = []
newsList = []
newsVectorsLenghth = []
userVectorsLenghth = []

'''
keyWords = {"word":["wordno", "df"]}
newsKeyWords = {"news1": {"word1":"tf1","word2":"tf2"}, "new2":{...}}
改成 newsKeyWords = {"news1": {"word1":["tf1",id1],"word2":["tf2",id2],...}, ...}
这样的话 可以对空间进行大幅度压缩从90000->500不到
userKeyWords = {"user1":{"word1":tf-idf1, "word2":tf-idf2}, ...}
userNewsMap = {("user1":"News1"), ("user2":"New2")}
haveSetNews = {"news1":1, "new2":2, ...}
haveSetUser = {"user1":1, "user2":2, ...}

'''
def buildVectors(newsCnt, userCnt, userNewsBegin, flag): #flag = True only add news, flag = False add all
	#考虑到以后添加新闻和词向量
	#注意,矩阵/list/dic/作为参数，函数内改变了内容，是真实地改变，所以可以直接改变，不需要返回
	global docNum, keyWords, newsKeyWords, userNewsMap, userVectors, newsVectors,\
	haveSetNews, haveSetUser, newsList, userList, newsVectorsLenghth, userVectorsLenghth
	#print userVectors.dtype
	for ii in range(userNewsBegin,len(userNewsMap)): # A user can read a lot of news, and a news can be written by lots of users
		item = userNewsMap[ii]
		user = item[0]
		news = item[1]
		#print "build user:%s news:%s" % (user, news)
		if not news in haveSetNews:
			newsList.append(news)
			#print news
			#print newsKeyWords
			delWordsList = []
			for word in newsKeyWords[news]:
				if word in keyWords:
					#print word
					#print keyWords[word][0]
					value = newsKeyWords[news][word][0] * 1.0 * \
					math.log(docNum*1.0/keyWords[word][1], 2)
					#newsVectors[newsCnt, keyWords[word][0]] = value  #Calculate TF-IDF
					newsKeyWords[news][word][1] = value
					newsVectorsLenghth[newsCnt] += (value ** 2)
				else:
					delWordsList.append(word)
					#del newsKeyWords[news][word] #把新闻中的不是词项的删除
			for delword in delWordsList:
				del newsKeyWords[news][delword]
			haveSetNews[news] = newsCnt
			newsCnt += 1

		if flag:
			continue

		for word in newsKeyWords[news]: 
			if word in keyWords: #新闻中已经处理了，现在一定在词项里面
				#oldValue = userVectors[haveSetUser[user], keyWords[word][0]]
				if user in haveSetUser:
					oldValue = userKeyWords[user].get(word, 0)
					newValue = newsKeyWords[news][word][0] * 1.0 *\
					math.log(docNum*1.0/keyWords[word][1])
					#userVectors[haveSetUser[user], keyWords[word][0]] = oldValue + newValue
					userKeyWords[user][word] = oldValue + newValue
					userVectorsLenghth[haveSetUser[user]] += (((newValue+oldValue)**2) - (oldValue**2)) 
				else:
					userList.append(user)
					haveSetUser[user] = userCnt
					buildUser = {}
					newValue = newsKeyWords[news][word][0] * 1.0 *\
					math.log(docNum*1.0/keyWords[word][1])
					buildUser[word] = newValue
					userVectorsLenghth[userCnt] = ((newValue**2))
					userKeyWords[user] = buildUser
					userCnt += 1

				#print userVectorsLenghth[haveSetUser[user]]
	# add may change the value, so when calculate in correlation
	'''
	for i in range(len(newsVectorsLenghth)):
		newsVectorsLenghth[i] = newsVectorsLenghth[i] ** 0.5
	for i in range(len(userVectorsLenghth)):
		userVectorsLenghth[i] = userVectorsLenghth[i] ** 0.5
	'''

def storeStatisticInfo(data, filename):
	print "Store MEMORY information ..."
	with open(filename, "w") as fw:
		pickle.dump(data, fw)
	print "Store MEMORY information done ..."
	
def getStatisticInf(filename):
	print "Get MEMORY information ..."
	with open(filename, "r") as fr:
		return pickle.load(fr)

def storeDivideData():
	global docNum, keyWords, newsKeyWords, userNewsMap
	(docNum, keyWords, newsKeyWords, userNewsMap) = DataHandle.divideWords(GlobalConfig.trainningData)
	storeStatisticInfo((docNum, keyWords, newsKeyWords, userNewsMap), GlobalConfig.storeOriginInfo)

def init():
	global docNum, keyWords, newsKeyWords, userNewsMap, userKeyWords,\
	haveSetNews, haveSetUser, newsList, userList, newsVectorsLenghth, userVectorsLenghth
	#(docNum, keyWords, newsKeyWords, userNewsMap) = getStatisticInf(GlobalConfig.storeOriginInfo)	
	storeDivideData()
	keyWordsNo = len(keyWords)
	#newsVectors = numpy.zeros((GlobalConfig.newsNo, keyWordsNo))
	#userVectors = numpy.zeros((GlobalConfig.userNo, keyWordsNo))
	newsVectorsLenghth = [0 for i in range(GlobalConfig.newsNo)]
	userVectorsLenghth = [0 for i in range(GlobalConfig.userNo)] 

	buildVectors(0, 0, 0, False)
	
	#print newsKeyWords["100652919"]

	storeStatisticInfo((newsKeyWords, userKeyWords,\
	haveSetNews, haveSetUser, newsList, userList, newsVectorsLenghth, userVectorsLenghth),\
	GlobalConfig.storeVectorInfo)
	
	'''
	print max(newsVectors[0, :])
	print min(newsVectors[0, :])
	print numpy.shape(numpy.nonzero(newsVectors[0, :]))[1]
	print newsVectors[0, :]
	'''
	

def calCorrelation(newsNo, userNo):
	#print "Calculate correlation bettween news %s and user %s" % (newsNo, userNo)
	global newsKeyWords, userKeyWords, haveSetNews, haveSetUser, newsVectorsLenghth, userVectorsLenghth
	cosCorrResult = 0.0
	for word in newsKeyWords[newsNo]:
		if not word in userKeyWords[userNo]:
			continue
		else:
			cosCorrResult += newsKeyWords[newsNo][word][1] * userKeyWords[userNo][word] 
	if cosCorrResult == 0:
		return 0
	cosCorrResult = cosCorrResult/(newsVectorsLenghth[haveSetNews[newsNo]]**0.5)/(userVectorsLenghth[haveSetUser[userNo]]**0.5)
	return cosCorrResult

def getGlobalInfo():
	global newsKeyWords, userKeyWords,haveSetNews, haveSetUser, newsList, userList, newsVectorsLenghth, userVectorsLenghth
	global docNum, keyWords, userNewsMap 

	(docNum, keyWords, newsKeyWords, userNewsMap) = getStatisticInf(GlobalConfig.storeOriginInfo)
	(newsKeyWords, userKeyWords,haveSetNews, haveSetUser, newsList, userList, \
		newsVectorsLenghth, userVectorsLenghth) = getStatisticInf(GlobalConfig.storeVectorInfo)
	# 注意 newsKeyWords 不能被 覆盖
	#print newsKeyWords["100652919"]
	#print userKeyWords["281608"]
	#print newsKeyWords["100652773"]
	#print userKeyWords["281608"]["黑客"]
	#print calCorrelation("100654390", "4950986")
	chcekValue = 0
	for word in newsKeyWords["100652919"]:
		chcekValue += newsKeyWords["100652919"][word][1] ** 2
	print "chcekValue : %lf" % chcekValue
	print "actulValue : %lf" % newsVectorsLenghth[haveSetNews["100652919"]]
	
	chcekValue = 0
	for word in userKeyWords["281608"]:
		chcekValue += userKeyWords["281608"][word] ** 2
	print "chcekValue : %lf" % chcekValue
	print "actulValue : %lf" % userVectorsLenghth[haveSetUser["281608"]]
	print calCorrelation("100652919", "281608")
	print calCorrelation("100652919", "5218791")

def getFileTwoColumn(filename):
	result = []
	with open(filename, "r") as fr:
		tempLines = fr.readlines()
		#print len(tempLines)
		for one in tempLines:
			one = one.strip()
			one = one.split("\t")[:2]
			result.append(one)
	return result

def calAccuracy(day):
	recommendDataFileName = GlobalConfig.reByDayFileName + str(day)
	actualDataFileName = GlobalConfig.dayFileName + str(day)
	
	#recommendData = getFileTwoColumn(GlobalConfig.dayFileName + str(day-1))
	recommendData = getFileTwoColumn(recommendDataFileName)
	actualData = getFileTwoColumn(actualDataFileName)
	#print actualData[:10]
	#print recommendData[:10]
	
	correctNum = 0
	for one in recommendData:
		if one in actualData:
			correctNum += 1

	print "Hit number: %d " % correctNum
	if len(recommendData):
		P = correctNum*1.0/len(recommendData)
	else:
		P = 0
	if len(actualData):
		R = correctNum*1.0/len(actualData)
	else:
		R = 0
	if P + R :
		F = 2.0*P*R/(P+R)
	else:
		F = 0
	
	print "Recommend number: %d" % len(recommendData)
	print "Actual number:%d" % len(actualData)
	print "Precise rate: %lf" % P
	print "Recall rate: %lf" % R
	print "F rate: %lf" % F
	return (correctNum, len(recommendData), len(actualData), P, R, F)

def buildTheDayNews(day):
	global docNum, keyWords, newsKeyWords, userNewsMap
	theDayUser = []
	with open(GlobalConfig.dayFileName+str(day), "r") as fr:
		tempData = fr.readlines()
		for aRecord in tempData:
			aRecord = aRecord.split("\t")
			if (aRecord[-2].strip() == "NULL" and aRecord[-1].strip() == "NULL"):
				continue
			userNewsMap.append((aRecord[0], aRecord[1]))

			if aRecord[1] in newsKeyWords.keys():
				continue
			#docNum += 1
			tempWordList = jieba.cut(aRecord[-3].strip() + aRecord[-2].strip(), cut_all=False)
			tempKeyWord = {}
			for word in tempWordList:
				word = word.strip().encode("utf-8")
				#print word
				if not word in keyWords:
					continue
				#print word
				tf = tempKeyWord.get(word, 0)
				if not tf:
					tempKeyWord[word] = [1.0, 0]
				else:
					tempKeyWord[word] = [tf[0] + 1.0, 0]
				#keyWord[word] = keyWord.get(word, 0) + 1.0
			newsKeyWords[aRecord[1]] = tempKeyWord
			theDayUser.append(aRecord[0])
			#print "divideData %d" % docNum
	return set(theDayUser)

def preThreeNews(day, preDay):
	global newsKeyWords
	result = []
	for i in range(preDay):
		with open(GlobalConfig.dayFileName+str(day-i), "r") as fr:
			tempData = fr.readlines()
			for item in tempData:
				item = item.strip()
				tempNews = item.split("\t")[1]
				if tempNews in newsKeyWords:
					result.append(tempNews)
				#result.append(tempNews)
	'''
	print "Previous three news number:%d" % len(set(result))
	for news in result:
		print news
	'''
	return set(result)

def mostReadTheDay(day):
	result = []
	newsRead = {}
	with open(GlobalConfig.dayFileName+str(day), "r") as fr:
		tempData = fr.readlines()
		for oneNews in tempData:
			oneNews = oneNews.split("\t")
			newsRead[oneNews[1]] = newsRead.get(oneNews[1], 0) + 1
	#print newsRead["100654630"],newsRead["100640376"],newsRead["100654733"]
	result = sorted(newsRead.iteritems(), key=lambda x:x[1], reverse=True)
	return result

def getActiveUser(day):
	with open(GlobalConfig.activeUserFile, "r") as fr:
		for i in range(day-21):
			fr.readline()
		temp = fr.readline().strip()
		temp = temp.split("\t")
		print "The %d day has %d users." % (day, len(temp))
		result = {}
		for item in temp:
			result[item] = 1 - (temp.index(item)*1.0/len(temp))
	return result

def recommendTheDay(day, k=80, d=1):

	global newsKeyWords, userKeyWords,haveSetNews, haveSetUser, newsList, userList, newsVectorsLenghth, userVectorsLenghth
	global docNum, keyWords, userNewsMap, oldUserNewsMap
	oldUserNewsMap = userNewsMap[:] #python list复制 直接写=是浅复制,深复制需要
	theDayUser = buildTheDayNews(day)
	buildVectors(len(newsList), len(userList), len(oldUserNewsMap), True) #只增加news
	print "::%d %d" % (len(oldUserNewsMap),len(userNewsMap))
	preLatestNews = preThreeNews(day, d)
	result = []
	newUser = 0
	mostNewsTheDay = mostReadTheDay(day-1) #头一天最火的新闻
	userActive = getActiveUser(day)

	for oneUser in theDayUser:
		#k = max(30, k*userActive[oneUser])
		if not oneUser in userList:
			print "User " + str(oneUser) + " is a new user."
			newUser += 1
			for item in mostNewsTheDay:
				if mostNewsTheDay.index(item) <= k:
					result.append([oneUser, item[0]])
				else:
					break
			continue 
		print "Recommend data for user: " + str(oneUser) 
		rating = []
		for oneNews in preLatestNews:
			rating.append([oneNews, calCorrelation(oneNews, oneUser)])
		rating = sorted(rating, key = lambda x:x[1], reverse=True)
		recommendDataNum = 0
		'''
		print "user:"+oneUser
		print rating[:2]
		'''
		for item in rating:
			
			if (oneUser,item[0]) in oldUserNewsMap :#and rating.index(item) > k/5:
				#print "*********"*10
				continue
			
			recommendDataNum += 1
			if recommendDataNum <= k:
				result.append([oneUser, item[0]])
			else:
				break
			
	with open(GlobalConfig.reByDayFileName+str(day), "w") as fw:
		resultString = ""
		for item in result:
			resultString += "\t".join(item)+"\n"
		fw.write(resultString)

	buildVectors(len(newsList), len(userList), len(oldUserNewsMap), False)
	print "All new users: %d\n" % newUser

def checkUserNum():
	temp = getActiveUser(22)
	actual = []
	with open(GlobalConfig.dayFileName+"22", "r") as fr:
		tempData = fr.readlines()
		print "len %d" % len(tempData)
		#print "Actual day %d user num:%d" % (21, )
		for item in tempData:
			actual.append(item.strip().split("\t")[0])
	print len(temp)
	print len(set(actual))
	if len(temp) == len(set(actual)):
		print "Yes check."
	else:
		print "No."

def test():
	
	result = []
	getGlobalInfo()
	for i in range(21,32):
		recommendTheDay(i, k=40)
		result.append(calAccuracy(i))
	resultString = ""
	sumF = 0
	for item in result:
		sumF += item[-1]
		temp = []
		for i in item:
			temp.append(str(i))
		resultString += "\t".join(temp)+"\n"
	print sumF/11
	with open(GlobalConfig.resultFileName+"2", "w") as fw:
		fw.write(resultString)
	

if __name__ == "__main__":
	#storeDivideData()
	#init()
	test()
	#test()
	#checkUserNum()
	#print mostReadTheDay(21, 10)
	#recommendTheDay()

	'''
	ans = 0
	bestK = 0
	global newsList, userList
	global userNewsMap, oldUserNewsMap

	getGlobalInfo()
	
	oldUserNewsMap = userNewsMap[:] #python list复制 直接写=是浅复制,深复制需要
	theDayUser = buildTheDayNews(21)
	buildVectors(len(newsList), len(userList), len(oldUserNewsMap), True) #只增加news

	for k in range(1, 200, 2):
		print "Handle k is %d now best: %lf" % (k, ans) 
		recommendTheDay(21, k, 3, theDayUser)
		(P,R,F) = calAccuracy(21)
		if F > ans:
			ans = F
			bestK = k
		else:
			break
	print ans,bestK
	'''

	'''
	recommendTheDay(22)
	calAccuracy(22)
	'''
	#preThreeNews(21)
	
	#preThreeNews(21)
	
	#preThreeNews(21)
	#calAccuracy(21)
	#getFileTwoColumn(GlobalConfig.dayFileName+"21")

