#coding=utf-8

class GlobalConfig:
	allData = "../data/NewsRecommendation/NewsRecData/user_click_data.txt"
	trainningData = "../data/NewsRecommendation/user_click_data_trainning.txt"
	testData = "../data/NewsRecommendation/user_click_data_test.txt"
	stopWord = "./StopWord"
	dataSeparateTime = "2014-3-21 0:0:0"
	dataStartTime = "2014-3-01 0:0:0"
	dayFileName = "../data/NewsRecommendation/NewsRecData/ByDay/"
	reByDayFileName = "../data/NewsRecommendation/NewsRecData/ReByDay/"
	storeOriginInfo = "../data/NewsRecommendation/NewsRecData/storeInfo"
	storeVectorInfo = "../data/NewsRecommendation/NewsRecData/storeVector"
	resultFileName = "../data/NewsRecommendation/NewsRecData/result"
	aDaySeparateTime = 86400
	keyWordGiveupRate = 0.1
	userNo = 12000
	newsNo = 6000
