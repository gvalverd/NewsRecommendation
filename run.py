#coding=utf-8
import numpy, math
from GlobalConfig import *
import DataHandle

def buildVectors(docNum, keyWords, newsKeyWords, userNewsMap, haveSetUser, haveSetNews, newsList, \
	userList, newsCnt, userCnt, newsVectors, userVectors):
	#考虑到以后添加新闻和词向量
	#注意,矩阵/list/dic/作为参数，函数内改变了内容，是真实地改变，所以可以直接改变，不需要返回
	'''
	keyWords = {"word":["wordno", "df"]}
	newsKeyWords = {"news1": {"word1":"tf1","word2":"tf2"}, "new2":{...}}
	userNewsMap = {"user":"News"}
	
	(docNum, keyWords, newsKeyWords, userNewsMap) = DataHandle.divideWords(GlobalConfig.trainningData)
	
	keyWordsNo = len(newsKeyWords)
	newsVectors = numpy.zeros((GlobalConfig.newsNo, keyWordsNo))
	userVectors = numpy.zeros((GlobalConfig.userNo, keyWordsNo))
	'''
	#print userVectors.dtype
	'''
	haveSetNews = {}
	haveSetUser = {}
	newsList = []
	userList = {}
	newsCnt = 0
	userCnt = 0
	'''
	for item in userNewsMap: # A user can read a lot of news, and a news can be written by lots of users
		user = item[0]
		news = item[1]
		print "build user:%s news:%s" % (user, news)
		if not news in haveSetNews:
			newsList.append(news)
			#print news
			#print newsKeyWords
			for word in newsKeyWords[news]:
				if word in keyWords:
					#print word
					#print keyWords[word][0]

					newsVectors[newsCnt, keyWords[word][0]] = newsKeyWords[news][word] * 1.0 * \
					math.log(docNum*1.0/keyWords[word][1], 2)  #Calculate TF-IDF
			haveSetNews[news] = newsCnt
			newsCnt += 1
		if not user in haveSetUser:
			userList.append(user)
			haveSetUser[user] = userCnt
			userCnt += 1
		for word in newsKeyWords[news]:
			if word in keyWords:
				userVectors[haveSetUser[user], keyWords[word][0]] += newsKeyWords[news][word] * 1.0 *\
				math.log(docNum*1.0/keyWords[word][1])

def init():
	(docNum, keyWords, newsKeyWords, userNewsMap) = DataHandle.divideWords(GlobalConfig.trainningData)
	keyWordsNo = len(keyWords)
	newsVectors = numpy.zeros((GlobalConfig.newsNo, keyWordsNo))
	userVectors = numpy.zeros((GlobalConfig.userNo, keyWordsNo))
	haveSetNews = {}
	haveSetUser = {}
	newsList = []
	userList = []
	newsCnt = 0
	userCnt = 0
	
	buildVectors(docNum, keyWords, newsKeyWords, userNewsMap, haveSetUser, haveSetNews, newsList, userList, \
		newsCnt, userCnt, newsVectors, userVectors)
	
	print max(newsVectors[0, :])
	print newsVectors[0, :]


if __name__ == "__main__":
	init()